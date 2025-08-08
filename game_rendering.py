# game_functions.py
# 游戏逻辑函数

from pickle import TRUE
import pygame
from game_constants import *
from pieces_class import Piece, FootballPiece


# 绘制棋盘
def draw_board(screen, field_image):
    screen.fill(WHITE)
    # 绘制背景图片
    screen.blit(field_image, (0, 0))
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            pygame.draw.rect(screen, BLACK, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
            # 检查是否为球门格子
            if (x, y) in FieldArea.RED_GOAL or (x, y) in FieldArea.BLUE_GOAL:
                # 创建临时Surface用于半透明绘制
                temp_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                temp_surface.fill(GOAL_COLOR)
                screen.blit(temp_surface, (x * SQUARE_SIZE, y * SQUARE_SIZE))


# 绘制棋子
def draw_pieces(screen, red_pieces, blue_pieces, football):
    for piece in red_pieces:
        piece.draw(screen)
    for piece in blue_pieces:
        piece.draw(screen)
    football.draw(screen)


# 绘制计分和回合数界面
def draw_score_and_round(screen, red_score, blue_score, current_player, round_count, red_coach_image, blue_coach_image,
                         music_on, back_on):
    # 计算右侧区域的位置
    score_area_x = WIDTH
    score_area_center_x = WIDTH + SCORE_AREA_WIDTH // 2

    # 绘制红方教练图片（顶部）- 缩小50%
    red_coach_x = score_area_x + 0.25 * SQUARE_SIZE
    red_coach_y = 0.5 * SQUARE_SIZE
    # 获取原始图片尺寸并缩小50%
    small_red_coach_image = pygame.transform.scale(red_coach_image, (SCORE_AREA_WIDTH // 2, SCORE_AREA_WIDTH // 2))
    screen.blit(small_red_coach_image, (red_coach_x, red_coach_y))

    # 红方得分放在教练图片下方
    red_score_y = red_coach_y + (SCORE_AREA_WIDTH // 2) + 0.5 * SQUARE_SIZE
    font = pygame.font.SysFont('Microsoft YaHei', FONT_SIZE)
    red_score_text = font.render(f"红方得分: {red_score}", True, FONT_COLOR)
    red_score_x = score_area_center_x - red_score_text.get_width() // 2
    screen.blit(red_score_text, (red_score_x, red_score_y))

    # 中间显示当前回合的教练图片 - 放大填满背景宽度
    # 计算填满右侧区域宽度的图片尺寸
    target_width = SCORE_AREA_WIDTH - 0.5 * SQUARE_SIZE
    if current_player == RED_TEAM:
        large_current_coach_image = pygame.transform.scale(red_coach_image, (target_width, target_width))
    else:
        large_current_coach_image = pygame.transform.scale(blue_coach_image, (target_width, target_width))

    # 计算图片位置使其居中
    current_coach_x = score_area_x + 0.25 * SQUARE_SIZE
    current_coach_height = large_current_coach_image.get_height()
    current_coach_y = (HEIGHT - current_coach_height) // 2 - 0.5 * SQUARE_SIZE  # 稍微向上调整
    screen.blit(large_current_coach_image, (current_coach_x, current_coach_y))

    # 中间显示回合数（调整位置到图片下方）
    round_text = font.render(f"回合: {round_count}", True, FONT_COLOR)
    round_y = current_coach_y + current_coach_height + 10
    round_x = score_area_center_x - round_text.get_width() // 2
    screen.blit(round_text, (round_x, round_y))

    # 加一个箭头指示当前回合
    arrow_size = 20
    arrow_y = round_y + round_text.get_height() + 20
    arrow_x = score_area_center_x - arrow_size // 2
    if current_player == RED_TEAM:
        # 红方回合，红色箭头
        pygame.draw.polygon(screen, RED, [
            (arrow_x, arrow_y),
            (arrow_x + arrow_size, arrow_y),
            (arrow_x + arrow_size // 2, arrow_y - arrow_size)
        ])
    else:
        # 蓝方回合，蓝色箭头
        pygame.draw.polygon(screen, BLUE, [
            (arrow_x, arrow_y),
            (arrow_x + arrow_size, arrow_y),
            (arrow_x + arrow_size // 2, arrow_y - arrow_size)
        ])

    # 绘制蓝方教练图片（底部）- 缩小50%
    # 获取原始图片尺寸并缩小50%
    blue_coach_x = score_area_x + 0.25 * SQUARE_SIZE
    small_blue_coach_image = pygame.transform.scale(blue_coach_image, (SCORE_AREA_WIDTH // 2, SCORE_AREA_WIDTH // 2))
    blue_coach_y = HEIGHT - (SCORE_AREA_WIDTH // 2) - 0.5 * SQUARE_SIZE
    screen.blit(small_blue_coach_image, (blue_coach_x, blue_coach_y))

    # 蓝方得分放在教练图片上方
    blue_score_text = font.render(f"蓝方得分: {blue_score}", True, FONT_COLOR)
    blue_score_x = score_area_center_x - blue_score_text.get_width() // 2
    blue_score_y = blue_coach_y - blue_score_text.get_height() - 0.5 * SQUARE_SIZE
    screen.blit(blue_score_text, (blue_score_x, blue_score_y))

    # 音乐开关按钮 - 放置在计分板右下角
    music_button_x = score_area_x + SCORE_AREA_WIDTH - music_button_image.get_width()
    music_button_y = HEIGHT - music_button_image.get_height()
    # 根据音乐状态选择图片
    if music_on:
        screen.blit(music_button_image, (music_button_x, music_button_y))
    else:
        screen.blit(music_button_off_image, (music_button_x, music_button_y))

    # 撤销开关按钮 - 放置音乐开关上方
    back_button_x = music_button_x
    back_button_y = music_button_y - back_button_image.get_height()  # - 0.125 * SQUARE_SIZE
    # 根据撤销状态选择图片
    if back_on:
        screen.blit(back_button_image, (back_button_x, back_button_y))
    else:
        screen.blit(back_button_off_image, (back_button_x, back_button_y))

    # 规则按钮 - 放置在计分板右上角
    rules_button_x = score_area_x + SCORE_AREA_WIDTH - rules_button_image.get_width()
    rules_button_y = 0  # 顶部
    screen.blit(rules_button_image, (rules_button_x, rules_button_y))

    return music_button_x, music_button_y, back_button_x, back_button_y, rules_button_x, rules_button_y


# 绘制开始选择弹窗
def draw_start_popup(screen, movements_every_round, start_player, game_mode, max_rounds, max_goals, rounds_input_active,
                     goals_input_active, red_coach_image, blue_coach_image, music_on):
    popup_x = (TOTAL_WIDTH - POPUP_WIDTH) // 2
    popup_y = (HEIGHT - POPUP_HEIGHT) // 2
    # 绘制弹窗背景图片
    screen.blit(popup_image, (popup_x, popup_y))
    # 绘制弹窗边框
    pygame.draw.rect(screen, BLACK, (popup_x, popup_y, POPUP_WIDTH, POPUP_HEIGHT), 2)

    font = pygame.font.SysFont('Microsoft YaHei', FONT_SIZE)
    small_font = pygame.font.SysFont('Microsoft YaHei', int(0.6 * FONT_SIZE))

    small_red_coach_image = pygame.transform.scale(red_coach_image, (POPUP_WIDTH // 4, POPUP_WIDTH // 4))
    small_blue_coach_image = pygame.transform.scale(blue_coach_image, (POPUP_WIDTH // 4, POPUP_WIDTH // 4))

    # 标题
    title_text = font.render("游戏设置", True, BLACK)
    screen.blit(title_text, (popup_x + POPUP_WIDTH // 2 - title_text.get_width() // 2, popup_y + 0.75 * SQUARE_SIZE))

    # 选择先行方
    player_text = small_font.render("选择先行方:", True, BLACK)
    screen.blit(player_text, (popup_x + 1.5 * SQUARE_SIZE, popup_y + 2.25 * SQUARE_SIZE))

    # 红方按钮（直接使用教练图片）
    red_button_x = popup_x + 1.5 * SQUARE_SIZE
    red_button_y = popup_y + 3.75 * SQUARE_SIZE
    # 计算按钮中心位置
    red_button_center_x = red_button_x + BUTTON_WIDTH // 2
    red_button_center_y = red_button_y + BUTTON_HEIGHT // 2
    # 根据是否选中调整图片大小
    if start_player == 0:
        # 选中状态 - 正常大小
        red_coach_display = small_red_coach_image
        red_button_rect = small_red_coach_image.get_rect(center=(red_button_center_x, red_button_center_y))
    else:
        # 未选中状态 - 缩小50%
        red_coach_width, red_coach_height = small_red_coach_image.get_size()
        red_coach_display = pygame.transform.smoothscale(small_red_coach_image,
                                                         (int(red_coach_width * 0.5), int(red_coach_height * 0.5)))
        red_button_rect = red_coach_display.get_rect(center=(red_button_center_x, red_button_center_y))
    # 直接绘制教练图片作为按钮
    screen.blit(red_coach_display, red_button_rect.topleft)

    # 蓝方按钮（直接使用教练图片）
    blue_button_x = popup_x + POPUP_WIDTH - 1.5 * SQUARE_SIZE - BUTTON_WIDTH
    blue_button_y = popup_y + 3.75 * SQUARE_SIZE
    # 计算按钮中心位置
    blue_button_center_x = blue_button_x + BUTTON_WIDTH // 2
    blue_button_center_y = blue_button_y + BUTTON_HEIGHT // 2
    # 根据是否选中调整图片大小
    if start_player == 1:
        # 选中状态 - 正常大小
        blue_coach_display = small_blue_coach_image
        blue_button_rect = small_blue_coach_image.get_rect(center=(blue_button_center_x, blue_button_center_y))
    else:
        # 未选中状态 - 缩小50%
        blue_coach_width, blue_coach_height = small_blue_coach_image.get_size()
        blue_coach_display = pygame.transform.smoothscale(small_blue_coach_image,
                                                          (int(blue_coach_width * 0.5), int(blue_coach_height * 0.5)))
        blue_button_rect = blue_coach_display.get_rect(center=(blue_button_center_x, blue_button_center_y))
    # 直接绘制教练图片作为按钮
    screen.blit(blue_coach_display, blue_button_rect.topleft)

    # 选择游戏模式
    mode_text = small_font.render("选择游戏模式:", True, BLACK)
    screen.blit(mode_text, (popup_x + 1.5 * SQUARE_SIZE, popup_y + 5.25 * SQUARE_SIZE))

    # 回合制勾选框（圆形）
    rounds_checkbox_x = popup_x + 1.5 * SQUARE_SIZE
    rounds_checkbox_y = popup_y + 6.25 * SQUARE_SIZE
    checkbox_radius = 0.25 * SQUARE_SIZE
    # 绘制圆形边框
    pygame.draw.circle(screen, BLACK, (rounds_checkbox_x + checkbox_radius, rounds_checkbox_y + checkbox_radius),
                       checkbox_radius, 2)
    # 填充内部为白色
    pygame.draw.circle(screen, WHITE, (rounds_checkbox_x + checkbox_radius, rounds_checkbox_y + checkbox_radius),
                       checkbox_radius - 2)
    if game_mode == 'rounds':
        # 绘制选中状态的圆点
        pygame.draw.circle(screen, BLACK, (rounds_checkbox_x + checkbox_radius, rounds_checkbox_y + checkbox_radius),
                           checkbox_radius - 6)

    # 回合数输入框
    rounds_input_x = rounds_checkbox_x + 1 * SQUARE_SIZE
    rounds_input_y = rounds_checkbox_y - 0.125 * SQUARE_SIZE
    pygame.draw.rect(screen, WHITE if rounds_input_active else NEUTRAL_COLOR,
                     (rounds_input_x, rounds_input_y + 0.125 * SQUARE_SIZE, 1.25 * SQUARE_SIZE, 0.625 * SQUARE_SIZE))
    pygame.draw.rect(screen, BLACK,
                     (rounds_input_x, rounds_input_y + 0.125 * SQUARE_SIZE, 1.25 * SQUARE_SIZE, 0.625 * SQUARE_SIZE), 2)
    rounds_value_text = small_font.render(str(max_rounds), True, BLACK)
    screen.blit(rounds_value_text,
                (rounds_input_x + 0.25 * SQUARE_SIZE, rounds_input_y - 0.3 * FONT_SIZE + 0.375 * SQUARE_SIZE))

    rounds_text = small_font.render("回合数制", True, BLACK)
    screen.blit(rounds_text,
                (rounds_input_x + 1.5 * SQUARE_SIZE, rounds_input_y - 0.3 * FONT_SIZE + 0.375 * SQUARE_SIZE))

    # 一球定胜负勾选框（圆形）
    one_goal_checkbox_x = popup_x + 1.5 * SQUARE_SIZE
    one_goal_checkbox_y = popup_y + 7.25 * SQUARE_SIZE
    checkbox_radius = 0.25 * SQUARE_SIZE
    # 绘制圆形边框
    pygame.draw.circle(screen, BLACK, (one_goal_checkbox_x + checkbox_radius, one_goal_checkbox_y + checkbox_radius),
                       checkbox_radius, 2)
    # 填充内部为白色
    pygame.draw.circle(screen, WHITE, (one_goal_checkbox_x + checkbox_radius, one_goal_checkbox_y + checkbox_radius),
                       checkbox_radius - 2)
    if game_mode == 'goals':
        # 绘制选中状态的圆点
        pygame.draw.circle(screen, BLACK,
                           (one_goal_checkbox_x + checkbox_radius, one_goal_checkbox_y + checkbox_radius),
                           checkbox_radius - 6)

    # 球数输入框
    goals_input_x = one_goal_checkbox_x + 1 * SQUARE_SIZE
    goals_input_y = one_goal_checkbox_y - 0.125 * SQUARE_SIZE

    pygame.draw.rect(screen, WHITE if goals_input_active else NEUTRAL_COLOR,
                     (goals_input_x, goals_input_y + 0.125 * SQUARE_SIZE, 1.25 * SQUARE_SIZE, 0.625 * SQUARE_SIZE))
    pygame.draw.rect(screen, BLACK,
                     (goals_input_x, goals_input_y + 0.125 * SQUARE_SIZE, 1.25 * SQUARE_SIZE, 0.625 * SQUARE_SIZE), 2)
    goals_value_text = small_font.render(str(max_goals), True, BLACK)
    screen.blit(goals_value_text,
                (goals_input_x + 0.25 * SQUARE_SIZE, goals_input_y - 0.3 * FONT_SIZE + 0.375 * SQUARE_SIZE))

    one_goal_text = small_font.render("球定胜负", True, BLACK)
    screen.blit(one_goal_text,
                (goals_input_x + 1.5 * SQUARE_SIZE, goals_input_y - 0.3 * FONT_SIZE + 0.375 * SQUARE_SIZE))

    # 选择每回合移动次数
    moves_text = small_font.render("选择每回合移动次数:", True, BLACK)
    screen.blit(moves_text, (popup_x + 1.5 * SQUARE_SIZE, popup_y + 8.25 * SQUARE_SIZE))

    # 创建三个圆形勾选框
    checkbox_radius = 0.25 * SQUARE_SIZE
    checkbox_y = popup_y + 9.25 * SQUARE_SIZE

    # 1次移动选项
    move1_checkbox_x = popup_x + 1.5 * SQUARE_SIZE
    # 绘制圆形边框
    pygame.draw.circle(screen, BLACK, (move1_checkbox_x + checkbox_radius, checkbox_y + checkbox_radius),
                       checkbox_radius, 2)
    # 填充内部为白色
    pygame.draw.circle(screen, WHITE, (move1_checkbox_x + checkbox_radius, checkbox_y + checkbox_radius),
                       checkbox_radius - 2)
    if movements_every_round == 1:
        # 绘制选中状态的圆点
        pygame.draw.circle(screen, BLACK, (move1_checkbox_x + checkbox_radius, checkbox_y + checkbox_radius),
                           checkbox_radius - 6)
    move1_text = small_font.render("1次", True, BLACK)
    screen.blit(move1_text, (move1_checkbox_x + 0.6 * SQUARE_SIZE, checkbox_y - 0.125 * SQUARE_SIZE))

    # 2次移动选项
    move2_checkbox_x = popup_x + 3.5 * SQUARE_SIZE
    # 绘制圆形边框
    pygame.draw.circle(screen, BLACK, (move2_checkbox_x + checkbox_radius, checkbox_y + checkbox_radius),
                       checkbox_radius, 2)
    # 填充内部为白色
    pygame.draw.circle(screen, WHITE, (move2_checkbox_x + checkbox_radius, checkbox_y + checkbox_radius),
                       checkbox_radius - 2)
    if movements_every_round == 2:
        # 绘制选中状态的圆点
        pygame.draw.circle(screen, BLACK, (move2_checkbox_x + checkbox_radius, checkbox_y + checkbox_radius),
                           checkbox_radius - 6)
    move2_text = small_font.render("2次", True, BLACK)
    screen.blit(move2_text, (move2_checkbox_x + 0.6 * SQUARE_SIZE, checkbox_y - 0.125 * SQUARE_SIZE))

    # 3次移动选项
    move3_checkbox_x = popup_x + 5.5 * SQUARE_SIZE
    # 绘制圆形边框
    pygame.draw.circle(screen, BLACK, (move3_checkbox_x + checkbox_radius, checkbox_y + checkbox_radius),
                       checkbox_radius, 2)
    # 填充内部为白色
    pygame.draw.circle(screen, WHITE, (move3_checkbox_x + checkbox_radius, checkbox_y + checkbox_radius),
                       checkbox_radius - 2)
    if movements_every_round == 3:
        # 绘制选中状态的圆点
        pygame.draw.circle(screen, BLACK, (move3_checkbox_x + checkbox_radius, checkbox_y + checkbox_radius),
                           checkbox_radius - 6)
    move3_text = small_font.render("3次", True, BLACK)
    screen.blit(move3_text, (move3_checkbox_x + 0.6 * SQUARE_SIZE, checkbox_y - 0.125 * SQUARE_SIZE))

    # 确认按钮 - 使用图片样式
    confirm_button_x = popup_x + POPUP_WIDTH // 2 - start_button_image.get_width() // 2
    confirm_button_y = popup_y + 10.25 * SQUARE_SIZE
    screen.blit(start_button_image, (confirm_button_x, confirm_button_y))

    # 音乐开关按钮 - 放置在右下角
    music_button_x = popup_x + POPUP_WIDTH - music_button_image.get_width()
    music_button_y = popup_y + POPUP_HEIGHT - music_button_image.get_height()
    # 根据音乐状态选择图片
    if music_on:
        screen.blit(music_button_image, (music_button_x, music_button_y))
    else:
        screen.blit(music_button_off_image, (music_button_x, music_button_y))

    # 返回按钮和输入框的坐标
    return red_button_rect, blue_button_rect, rounds_checkbox_x, rounds_checkbox_y, one_goal_checkbox_x, one_goal_checkbox_y, move1_checkbox_x, move2_checkbox_x, move3_checkbox_x, checkbox_y, rounds_input_x, rounds_input_y, goals_input_x, goals_input_y, confirm_button_x, confirm_button_y, music_button_x, music_button_y


# 绘制游戏结束弹窗
def draw_game_over_popup(screen, winner):
    popup_x = (TOTAL_WIDTH - POPUP_WIDTH) // 2
    popup_y = (HEIGHT - POPUP_HEIGHT) // 2
    # 绘制弹窗背景图片
    screen.blit(popup_image, (popup_x, popup_y))
    # 绘制弹窗边框
    pygame.draw.rect(screen, BLACK, (popup_x, popup_y, POPUP_WIDTH, POPUP_HEIGHT), 2)

    font = pygame.font.SysFont('Microsoft YaHei', FONT_SIZE)
    small_font = pygame.font.SysFont('Microsoft YaHei', int(0.8 * FONT_SIZE))

    game_over_text = font.render("游戏结束", True, BLACK)
    screen.blit(game_over_text, (popup_x + POPUP_WIDTH // 2 - game_over_text.get_width() // 2, popup_y + 50))

    if winner == '平局':
        winner_text = font.render(f"{winner}!", True, BLACK)
    elif winner == '红方':
        winner_text = font.render(f"{winner}获胜!", True, RED)
    elif winner == '蓝方':
        winner_text = font.render(f"{winner}获胜!", True, BLUE)
    screen.blit(winner_text, (popup_x + POPUP_WIDTH // 2 - winner_text.get_width() // 2, popup_y + 100))

    # 插入胜利队伍图片
    # 确保图片大小适合弹窗
    max_team_image_width = POPUP_WIDTH - 10  # 几乎使用弹窗全宽度，留一点边距
    max_team_image_height = 180  # 进一步增加最大高度

    if winner == '红方':
        # 计算合适的尺寸
        team_image_ratio = red_team_image.get_width() / red_team_image.get_height()
        # 优先保证宽度，使图片更宽
        new_team_width = max_team_image_width  # 直接使用最大宽度
        new_team_height = int(new_team_width / team_image_ratio)
        new_team_height = min(new_team_height, max_team_image_height)
        # 调整图片大小
        resized_team_image = pygame.transform.smoothscale(red_team_image, (new_team_width, new_team_height))
        # 下移图片并居中
        screen.blit(resized_team_image, (popup_x + POPUP_WIDTH // 2 - new_team_width // 2, popup_y + 160))
    elif winner == '蓝方':
        # 计算合适的尺寸
        team_image_ratio = blue_team_image.get_width() / blue_team_image.get_height()
        # 优先保证宽度，使图片更宽
        new_team_width = max_team_image_width  # 直接使用最大宽度
        new_team_height = int(new_team_width / team_image_ratio)
        new_team_height = min(new_team_height, max_team_image_height)
        # 调整图片大小
        resized_team_image = pygame.transform.smoothscale(blue_team_image, (new_team_width, new_team_height))
        # 下移图片并居中
        screen.blit(resized_team_image, (popup_x + POPUP_WIDTH // 2 - new_team_width // 2, popup_y + 160))
    else:
        # 计算合适的尺寸
        team_image_ratio = draw_image.get_width() / draw_image.get_height()
        # 优先保证宽度，使图片更宽
        new_team_width = max_team_image_width  # 直接使用最大宽度
        new_team_height = int(new_team_width / team_image_ratio)
        new_team_height = min(new_team_height, max_team_image_height)
        # 调整图片大小
        resized_team_image = pygame.transform.smoothscale(draw_image, (new_team_width, new_team_height))
        # 下移图片并居中
        screen.blit(resized_team_image, (popup_x + POPUP_WIDTH // 2 - new_team_width // 2, popup_y + 160))

    # 再来一局按钮 - 移到图片下方
    restart_button_x = popup_x + POPUP_WIDTH // 2 - BUTTON_WIDTH // 2 - 80
    restart_button_y = popup_y + 160 + new_team_height + 20  # 图片底部 + 间距
    pygame.draw.rect(screen, GREEN, (restart_button_x, restart_button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, BLACK, (restart_button_x, restart_button_y, BUTTON_WIDTH, BUTTON_HEIGHT), 2)
    restart_text = small_font.render("再来一局", True, WHITE)
    screen.blit(restart_text, (restart_button_x + BUTTON_WIDTH // 2 - restart_text.get_width() // 2,
                               restart_button_y + BUTTON_HEIGHT // 2 - restart_text.get_height() // 2))

    # 退出按钮 - 移到图片下方
    exit_button_x = popup_x + POPUP_WIDTH // 2 - BUTTON_WIDTH // 2 + 80
    exit_button_y = popup_y + 160 + new_team_height + 20  # 图片底部 + 间距
    pygame.draw.rect(screen, YES_COLOR, (exit_button_x, exit_button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, BLACK, (exit_button_x, exit_button_y, BUTTON_WIDTH, BUTTON_HEIGHT), 2)
    exit_text = small_font.render("退出", True, WHITE)
    screen.blit(exit_text, (exit_button_x + BUTTON_WIDTH // 2 - exit_text.get_width() // 2,
                            exit_button_y + BUTTON_HEIGHT // 2 - exit_text.get_height() // 2))

    return restart_button_x, restart_button_y, exit_button_x, exit_button_y


# 绘制规则弹窗
def draw_rules_popup(screen):
    popup_x = (TOTAL_WIDTH - POPUP_WIDTH) // 2
    popup_y = (HEIGHT - POPUP_HEIGHT) // 2
    # 绘制弹窗背景图片
    screen.blit(popup_image, (popup_x, popup_y))
    # 绘制弹窗边框
    pygame.draw.rect(screen, BLACK, (popup_x, popup_y, POPUP_WIDTH, POPUP_HEIGHT), 2)

    font = pygame.font.SysFont('Microsoft YaHei', FONT_SIZE)
    small_font = pygame.font.SysFont('Microsoft YaHei', int(0.5 * FONT_SIZE))

    # 标题
    title_text = font.render("游戏规则", True, BLACK)
    screen.blit(title_text, (popup_x + POPUP_WIDTH // 2 - title_text.get_width() // 2, popup_y + 20))

    # 读取规则文件
    try:
        with open('rules.txt', 'r', encoding='utf-8') as f:
            rules_content = f.read()
    except FileNotFoundError:
        rules_content = "未找到规则文件，请确保rules.txt存在于项目根目录"

    # 显示规则内容
    y_offset = 60
    for line in rules_content.splitlines():
        if line.strip():
            rule_text = small_font.render(line.strip(), True, BLACK)
            screen.blit(rule_text, (popup_x + 30, popup_y + y_offset))
            y_offset += 25
        else:
            y_offset += 10

    # 关闭按钮
    close_button_x = popup_x + POPUP_WIDTH // 2 - BUTTON_WIDTH // 2
    close_button_y = popup_y + POPUP_HEIGHT - 60
    pygame.draw.rect(screen, YES_COLOR, (close_button_x, close_button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, BLACK, (close_button_x, close_button_y, BUTTON_WIDTH, BUTTON_HEIGHT), 2)
    close_text = small_font.render("关闭", True, WHITE)
    screen.blit(close_text, (close_button_x + BUTTON_WIDTH // 2 - close_text.get_width() // 2,
                             close_button_y + BUTTON_HEIGHT // 2 - close_text.get_height() // 2))

    return close_button_x, close_button_y


# 绘制退出确认弹窗
def draw_quit_popup(screen):
    popup_x = (TOTAL_WIDTH - POPUP_WIDTH) // 2
    popup_y = (HEIGHT - POPUP_HEIGHT) // 2
    # 绘制弹窗背景图片
    screen.blit(popup_image, (popup_x, popup_y))
    # 绘制弹窗边框
    pygame.draw.rect(screen, BLACK, (popup_x, popup_y, POPUP_WIDTH, POPUP_HEIGHT), 2)

    small_font = pygame.font.SysFont('Microsoft YaHei', 24)

    question_text = small_font.render("确定要退出游戏吗？", True, BLACK)
    screen.blit(question_text, (popup_x + POPUP_WIDTH // 2 - question_text.get_width() // 2, popup_y + 30))

    yes_button_x = popup_x + 50
    yes_button_y = popup_y + 80
    no_button_x = popup_x + POPUP_WIDTH - 50 - BUTTON_WIDTH
    no_button_y = popup_y + 80

    pygame.draw.rect(screen, YES_COLOR, (yes_button_x, yes_button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, NO_COLOR, (no_button_x, no_button_y, BUTTON_WIDTH, BUTTON_HEIGHT))

    yes_text = small_font.render("是", True, WHITE)
    no_text = small_font.render("否", True, WHITE)

    screen.blit(yes_text, (yes_button_x + BUTTON_WIDTH // 2 - yes_text.get_width() // 2,
                           yes_button_y + BUTTON_HEIGHT // 2 - yes_text.get_height() // 2))
    screen.blit(no_text, (no_button_x + BUTTON_WIDTH // 2 - no_text.get_width() // 2,
                          no_button_y + BUTTON_HEIGHT // 2 - no_text.get_height() // 2))

    return yes_button_x, yes_button_y, no_button_x, no_button_y
