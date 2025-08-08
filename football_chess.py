# football_chess.py
# 足球棋游戏主文件

import pygame
from game_constants import *
from game_rendering import *
from game_class import Game
from game_class import init_game_pieces

# 初始化字体
font = pygame.font.SysFont('Microsoft YaHei', FONT_SIZE)
small_font = pygame.font.SysFont('Microsoft YaHei', int(0.6 * FONT_SIZE))

# 创建窗口，默认就带有最小化、最大化、关闭按钮
window_width = min(TOTAL_WIDTH, screen_width * 2 // 3)
window_height = min(HEIGHT, screen_height * 2 // 3)
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("足球棋")

# 初始化pygame音频系统
pygame.mixer.init()

# 播放背景音乐，设置音量为50%

try:
    sound_background.set_volume(0.5)  # 0.0-1.0 范围
    sound_background.play(-1)  # -1 表示循环播放
except pygame.error as e:
    print(f"播放背景音乐时出错: {e}")

# 初始化游戏
game = Game()
# 添加规则弹窗控制标志
game.show_rules_popup = False

# 显示开始弹窗
while game.show_start_popup and game.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
            game.show_start_popup = False
        elif event.type == pygame.KEYDOWN:
            if game.rounds_input_active:
                if event.key == pygame.K_BACKSPACE:
                    game.max_rounds = game.max_rounds // 10
                elif event.unicode.isdigit():
                    new_value = game.max_rounds * 10 + int(event.unicode)
                    if 1 <= new_value <= 300:
                        game.max_rounds = new_value
                    elif new_value < 20:
                        game.max_rounds = 20
                    elif new_value > 300:
                        game.max_rounds = 300
            elif game.goals_input_active:
                if event.key == pygame.K_BACKSPACE:
                    game.max_goals = game.max_goals // 10
                elif event.unicode.isdigit():
                    new_value = game.max_goals * 10 + int(event.unicode)
                    if 1 <= new_value <= 5:
                        game.max_goals = new_value
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # 确保显示的值不是0
            display_max_rounds = game.max_rounds if game.max_rounds > 0 else 100
            display_max_goals = game.max_goals if game.max_goals > 0 else 1
            red_button_rect, blue_button_rect, rounds_checkbox_x, rounds_checkbox_y, one_goal_checkbox_x, one_goal_checkbox_y, move1_checkbox_x, move2_checkbox_x, move3_checkbox_x, checkbox_y, confirm_button_x, confirm_button_y, rounds_input_x, rounds_input_y, goals_input_x, goals_input_y, music_button_x, music_button_y = draw_start_popup(
                screen, game.movements_every_round, game.start_player, game.game_mode, display_max_rounds,
                display_max_goals, game.rounds_input_active, game.goals_input_active, red_coach_image, blue_coach_image,
                game.music_on
            )
            # 点击红方按钮
            if red_button_rect.collidepoint(mouse_x, mouse_y):
                game.start_player = 0
            # 点击蓝方按钮
            elif blue_button_rect.collidepoint(mouse_x, mouse_y):
                game.start_player = 1
            # 点击回合制勾选框
            elif (rounds_checkbox_x <= mouse_x <= rounds_checkbox_x + 20 and
                  rounds_checkbox_y <= mouse_y <= rounds_checkbox_y + 20):
                game.game_mode = 'rounds'
                game.rounds_input_active = False
                game.goals_input_active = False
                # 如果回合数为0，则重置为默认值100
                if game.max_rounds == 0:
                    game.max_rounds = 100
            # 点击一球定胜负勾选框
            elif (one_goal_checkbox_x <= mouse_x <= one_goal_checkbox_x + 20 and
                  one_goal_checkbox_y <= mouse_y <= one_goal_checkbox_y + 20):
                game.game_mode = 'goals'
                game.rounds_input_active = False
                game.goals_input_active = False
                # 如果球数为0，则重置为默认值1
                if game.max_goals == 0:
                    game.max_goals = 1
            # 点击回合数输入框
            elif (rounds_input_x <= mouse_x <= rounds_input_x + 50 and
                  rounds_input_y <= mouse_y <= rounds_input_y + 20):
                game.rounds_input_active = not game.rounds_input_active
                game.goals_input_active = False
                if game.rounds_input_active:
                    game.max_rounds = 0  # 清空原有数值
            # 点击球数输入框
            elif (goals_input_x <= mouse_x <= goals_input_x + 50 and
                  goals_input_y <= mouse_y <= goals_input_y + 20):
                game.goals_input_active = not game.goals_input_active
                game.rounds_input_active = False
                if game.goals_input_active:
                    game.max_goals = 0  # 清空原有数值
            # 点击1次移动选项
            elif (move1_checkbox_x <= mouse_x <= move1_checkbox_x + 20 and
                  checkbox_y <= mouse_y <= checkbox_y + 20):
                game.movements_every_round = 1
            # 点击2次移动选项
            elif (move2_checkbox_x <= mouse_x <= move2_checkbox_x + 20 and
                  checkbox_y <= mouse_y <= checkbox_y + 20):
                game.movements_every_round = 2
            # 点击3次移动选项
            elif (move3_checkbox_x <= mouse_x <= move3_checkbox_x + 20 and
                  checkbox_y <= mouse_y <= checkbox_y + 20):
                game.movements_every_round = 3
            # 点击确认按钮
            elif (confirm_button_x <= mouse_x <= confirm_button_x + start_button_image.get_width() and
                  confirm_button_y <= mouse_y <= confirm_button_y + start_button_image.get_height()):
                # 如果球数为0，则重置为默认值1
                if game.max_goals == 0:
                    game.max_goals = 1
                # 如果回合数为0，则重置为默认值100
                if game.max_rounds == 0:
                    game.max_rounds = 100
                game.show_start_popup = False
                # 设置当前玩家
                game.current_player = game.start_player
                # 重新初始化棋子和足球
                game.red_pieces, game.blue_pieces, game.football = init_game_pieces(game.start_player)
    # 确保显示的值不是0
    display_max_rounds = game.max_rounds if game.max_rounds > 0 else 100
    display_max_goals = game.max_goals if game.max_goals > 0 else 1

    # 调用draw_start_popup并获取按钮位置
    red_button_rect, blue_button_rect, rounds_checkbox_x, rounds_checkbox_y, one_goal_checkbox_x, one_goal_checkbox_y, move1_checkbox_x, move2_checkbox_x, move3_checkbox_x, checkbox_y, rounds_input_x, rounds_input_y, goals_input_x, goals_input_y, confirm_button_x, confirm_button_y, music_button_x, music_button_y = draw_start_popup(
        screen, game.movements_every_round, game.start_player, game.game_mode, display_max_rounds, display_max_goals,
        game.rounds_input_active, game.goals_input_active, red_coach_image, blue_coach_image, game.music_on
    )
    # 绘制弹窗

    # 处理鼠标点击事件
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = event.pos
        # 点击红方按钮
        if red_button_rect.collidepoint(mouse_x, mouse_y):
            game.start_player = 0
        # 点击蓝方按钮
        elif blue_button_rect.collidepoint(mouse_x, mouse_y):
            game.start_player = 1
        # 点击回合制勾选框
        elif (rounds_checkbox_x <= mouse_x <= rounds_checkbox_x + 20 and
              rounds_checkbox_y <= mouse_y <= rounds_checkbox_y + 20):
            game.game_mode = 'rounds'
        # 点击一球定胜负勾选框
        elif (one_goal_checkbox_x <= mouse_x <= one_goal_checkbox_x + 20 and
              one_goal_checkbox_y <= mouse_y <= one_goal_checkbox_y + 20):
            game.game_mode = 'goals'
        # 点击1次移动选项
        elif (move1_checkbox_x <= mouse_x <= move1_checkbox_x + 20 and
              checkbox_y <= mouse_y <= checkbox_y + 20):
            game.movements_every_round = 1
        # 点击2次移动选项
        elif (move2_checkbox_x <= mouse_x <= move2_checkbox_x + 20 and
              checkbox_y <= mouse_y <= checkbox_y + 20):
            game.movements_every_round = 2
        # 点击3次移动选项
        elif (move3_checkbox_x <= mouse_x <= move3_checkbox_x + 20 and
              checkbox_y <= mouse_y <= checkbox_y + 20):
            game.movements_every_round = 3
        # 点击确认按钮
        elif (confirm_button_x <= mouse_x <= confirm_button_x + BUTTON_WIDTH and
              confirm_button_y <= mouse_y <= confirm_button_y + BUTTON_HEIGHT):
            # 如果球数为0，则重置为默认值1
            if game.max_goals == 0:
                game.max_goals = 1
            # 如果回合数为0，则重置为默认值100
            if game.max_rounds == 0:
                game.max_rounds = 100
            game.show_start_popup = False
            # 设置当前玩家
            game.current_player = game.start_player
            # 重新初始化棋子和足球
            game.red_pieces, game.blue_pieces, game.football = init_game_pieces(game.start_player)
        # 点击音乐开关按钮
        elif (music_button_x <= mouse_x <= music_button_x + music_button_image.get_width() and
              music_button_y <= mouse_y <= music_button_y + music_button_image.get_height()):
            game.toggle_music()
            # 更新音乐按钮图像
            if game.music_on:
                sound_background.set_volume(0.5)
            else:
                sound_background.set_volume(0)

    pygame.display.flip()

clock = pygame.time.Clock()

# 游戏主循环
while game.running:
    clock.tick(60)  # 控制游戏帧率
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.show_quit_popup = True
        elif event.type == pygame.MOUSEBUTTONDOWN and game.show_quit_popup:
            mouse_x, mouse_y = event.pos
            yes_button_x, yes_button_y, no_button_x, no_button_y = draw_quit_popup(screen)
            # 判断是否点击了“是”按钮
            if (yes_button_x <= mouse_x <= yes_button_x + BUTTON_WIDTH and
                    yes_button_y <= mouse_y <= yes_button_y + BUTTON_HEIGHT):
                game.running = False
            # 判断是否点击了“否”按钮
            elif (no_button_x <= mouse_x <= no_button_x + BUTTON_WIDTH and
                  no_button_y <= mouse_y <= no_button_y + BUTTON_HEIGHT):
                game.show_quit_popup = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game.show_quit_popup and not game.show_game_over_popup:
            mouse_x, mouse_y = event.pos
            # 只处理棋盘区域的点击
            if mouse_x < WIDTH:
                clicked_x = mouse_x // SQUARE_SIZE
                clicked_y = mouse_y // SQUARE_SIZE
                if 0 <= clicked_x < BOARD_WIDTH and 0 <= clicked_y < BOARD_HEIGHT:
                    # 检查是否点击了当前玩家的棋子
                    current_pieces = game.red_pieces if game.current_player == RED_TEAM else game.blue_pieces
                    opponent_pieces = game.blue_pieces if game.current_player == RED_TEAM else game.red_pieces
                    all_pieces = game.red_pieces + game.blue_pieces  # 包含所有棋子的集合

                    # 球在己方球门时大力开球
                    if game.football.is_in_own_goal(game.current_player):
                        # 球在己方球门时，只能选中足球
                        if game.selected_piece == PieceIndex.NO_PIECE:
                            # 选中足球    
                            if game.football.x == clicked_x and game.football.y == clicked_y:
                                game.selected_piece = PieceIndex.FOOTBALL
                                # 获取有效移动位置
                                game.valid_moves = game.football.get_own_goal_position(all_pieces, game.current_player)
                                break
                            break
                        # 移动足球
                        elif game.selected_piece == PieceIndex.FOOTBALL:
                            # 移动
                            if (clicked_x, clicked_y) in game.valid_moves:
                                game.save_backup()
                                game.football.move(clicked_x, clicked_y)
                                game.play_sound(GameSound.KICK)
                                game.turn_over()
                                if game.check_game_over():
                                    game.show_game_over_popup = True

                    # 是否选中棋子
                    if game.selected_piece == PieceIndex.NO_PIECE:
                        # 选中足球    
                        if game.football.x == clicked_x and game.football.y == clicked_y:
                            # 检查是否选中了足球
                            if game.football_contral():
                                # 如果足球不在对方球门里：
                                if not game.football.is_in_opponent_goal(game.current_player):
                                    game.selected_piece = PieceIndex.FOOTBALL
                                    # 获取有效移动位置
                                    piece = game.get_piece_by_index(game.selected_piece)
                                    game.valid_moves = game.football.get_valid_moves(all_pieces)
                                    break
                                else:
                                    # 如果足球在对方球门里，不能移动
                                    break
                            else:
                                # 足球不受玩家控制
                                break

                        for piece in current_pieces:
                            # 选中己方棋子
                            if piece.x == clicked_x and piece.y == clicked_y:
                                # 每回合不能重复移动同一棋子
                                if piece.index in game.moved_piece:
                                    game.selected_piece = PieceIndex.NO_PIECE
                                    game.valid_moves = []
                                    break
                                else:
                                    game.selected_piece = piece.index
                                    # 获取有效移动位置
                                    piece = game.get_piece_by_index(game.selected_piece)
                                    game.valid_moves = piece.get_valid_moves(all_pieces, game.football)
                                    break
                        # 如果没有点击己方棋子，也没有点击有效移动位置，检查是否点击了足球

                    # 是否移动选中棋子
                    else:
                        # 选中足球
                        if game.selected_piece == PieceIndex.FOOTBALL:
                            # 是否重复选择同一枚棋子
                            if game.football.x == clicked_x and game.football.y == clicked_y:
                                game.selected_piece = -1
                                game.valid_moves = []
                                break
                            # 移动
                            elif (clicked_x, clicked_y) in game.valid_moves:
                                game.save_backup()
                                game.football.move(clicked_x, clicked_y)
                                # 移动足球后播放音效
                                game.play_sound(GameSound.KICK)
                                # 操作结束
                                goal = game.turn_over()
                                if goal:
                                    game.play_sound(GameSound.GOAL)
                                # 检查游戏是否结束
                                if game.check_game_over():
                                    game.show_game_over_popup = True
                                break

                        # 选中己方棋子
                        elif game.selected_piece > 0:
                            piece = game.get_piece_by_index(game.selected_piece)
                            # 是否重复选择同一枚棋子
                            if piece and piece.x == clicked_x and piece.y == clicked_y:
                                game.selected_piece = -1
                                game.valid_moves = []
                                break
                            # 是否点击了有效移动位置
                            elif (clicked_x, clicked_y) in game.valid_moves:
                                # 移动棋子
                                game.save_backup()
                                moved_football = piece.move(
                                    clicked_x, clicked_y, game.football, game.red_pieces, game.blue_pieces
                                )
                                if moved_football:
                                    game.play_sound(GameSound.RUN_WITH_FOOTBALL)
                                else:
                                    game.play_sound(GameSound.RUN)
                                # 操作结束
                                goal = game.turn_over()
                                if goal:
                                    game.play_sound(GameSound.GOAL)
                                # 检查游戏是否结束
                                if game.check_game_over():
                                    game.show_game_over_popup = True
                                break
            elif mouse_x > WIDTH:
                # 点击音乐按钮
                if music_button_x <= mouse_x <= music_button_x + music_button_image.get_width() and music_button_y <= mouse_y <= music_button_y + music_button_image.get_height():
                    game.toggle_music()
                    if game.music_on:
                        sound_background.set_volume(0.5)
                    else:
                        sound_background.set_volume(0)
                # 点击撤销按钮
                elif back_button_x <= mouse_x <= back_button_x + back_button_image.get_width() and back_button_y <= mouse_y <= back_button_y + back_button_image.get_height():
                    if game.back:
                        game.excute_back()
                # 点击规则按钮
                elif rules_button_x <= mouse_x <= rules_button_x + rules_button_image.get_width() and rules_button_y <= mouse_y <= rules_button_y + rules_button_image.get_height():
                    game.show_rules_popup = True
                break

        draw_board(screen, field_image)

        # 高亮显示有效移动位置
        if game.selected_piece != PieceIndex.NO_PIECE and game.valid_moves:
            for (x, y) in game.valid_moves:
                temp_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                temp_surface.fill((0, 255, 0, 100))  # 半透明绿色
                screen.blit(temp_surface, (x * SQUARE_SIZE, y * SQUARE_SIZE))

        game.check_piece_control()
        draw_pieces(screen, game.red_pieces, game.blue_pieces, game.football)
        # 调用draw_score_and_round并获取音乐按钮位置、撤销按钮位置和规则按钮位置
        music_button_x, music_button_y, back_button_x, back_button_y, rules_button_x, rules_button_y = draw_score_and_round(
            screen, game.red_score, game.blue_score, game.current_player, game.round_count, red_coach_image,
            blue_coach_image, game.music_on, game.back)

        # 显示规则弹窗
        if game.show_rules_popup:
            close_button_x, close_button_y = draw_rules_popup(screen)
            # 处理关闭按钮点击
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # 检查是否点击关闭按钮
                if close_button_x <= mouse_x <= close_button_x + BUTTON_WIDTH and close_button_y <= mouse_y <= close_button_y + BUTTON_HEIGHT:
                    game.show_rules_popup = False

        # 显示游戏结束弹窗
        if game.show_game_over_popup:
            restart_button_x, restart_button_y, exit_button_x, exit_button_y = draw_game_over_popup(screen, game.winner)
            # 处理再来一局按钮点击
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # 检查是否点击再来一局按钮
                if restart_button_x <= mouse_x <= restart_button_x + BUTTON_WIDTH and restart_button_y <= mouse_y <= restart_button_y + BUTTON_HEIGHT:
                    # 调用reset_game函数重新开始游戏
                    game.reset_game()
                    game.show_game_over_popup = False
                # 检查是否点击退出按钮
            elif exit_button_x <= mouse_x <= exit_button_x + BUTTON_WIDTH and exit_button_y <= mouse_y <= exit_button_y + BUTTON_HEIGHT:
                game.running = False

        if game.show_quit_popup:
            draw_quit_popup(screen)

        pygame.display.flip()

# 退出 Pygame
pygame.quit()
