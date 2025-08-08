# game_class.pu
# 游戏类，包含游戏设置和状态变量

import pygame
from game_constants import *
from pieces_class import Piece, FootballPiece


# 初始化双方棋子和足球
def init_game_pieces(start_player):
    # 重置棋子索引计数器
    Piece._next_index = 1
    # 红方棋子布局
    red_goalkeeper = Piece(BOARD_WIDTH // 2, 0, RED, PieceType.GOALKEEPER)  # 守门员在球门中间
    red_defenders = [  # 后卫在第二行
        Piece(2, 1, RED, PieceType.DEFENDER),  # 第三列
        Piece(6, 1, RED, PieceType.DEFENDER)   # 第七列
    ]
    red_midfielders = [  # 中场在第四行
        Piece(2, 3, RED, PieceType.MIDFIELDER),  # 第三列
        Piece(6, 3, RED, PieceType.MIDFIELDER)   # 第七列
    ]
    red_forwards = [  # 前锋在第六行
        Piece(2, 5, RED, PieceType.FORWARD),  # 第三列
        Piece(6, 5, RED, PieceType.FORWARD)   # 第七列
    ]
    red_pieces = [red_goalkeeper] + red_defenders + red_midfielders + red_forwards

    # 蓝方棋子布局
    blue_goalkeeper = Piece(BOARD_WIDTH // 2, BOARD_HEIGHT - 1, BLUE, PieceType.GOALKEEPER)  # 守门员在球门中间
    blue_defenders = [  # 后卫在倒数第二行
        Piece(2, BOARD_HEIGHT - 2, BLUE, PieceType.DEFENDER),  # 第三列
        Piece(6, BOARD_HEIGHT - 2, BLUE, PieceType.DEFENDER)   # 第七列
    ]
    blue_midfielders = [  # 中场在倒数第四行
        Piece(2, BOARD_HEIGHT - 4, BLUE, PieceType.MIDFIELDER),  # 第三列
        Piece(6, BOARD_HEIGHT - 4, BLUE, PieceType.MIDFIELDER)   # 第七列
    ]
    blue_forwards = [  # 前锋在倒数第六行
        Piece(2, BOARD_HEIGHT - 6, BLUE, PieceType.FORWARD),  # 第三列
        Piece(6, BOARD_HEIGHT - 6, BLUE, PieceType.FORWARD)   # 第七列
    ]
    blue_pieces = [blue_goalkeeper] + blue_defenders + blue_midfielders + blue_forwards

    # 根据先行方设置足球初始位置（坐标从0开始计数）
    if start_player == 1:  # 蓝方先行
        football = FootballPiece(2, 9)  # 第3列第10行 -> 转换为从0开始计数
    else:  # 红方先行
        football = FootballPiece(6, 6)  # 第7列第7行 -> 转换为从0开始计数

    return red_pieces, blue_pieces, football


class Game:
    
    def __init__(self):
        
        # 游戏设置变量
        self.start_player = 1  # 默认为蓝方先行(1)
        self.game_mode = 'goals'  # 默认为回合制
        self.max_rounds = 100  # 默认100回合
        self.max_goals = 1  # 默认1球定胜负
        self.movements_every_round = 2    # 每个回合最多移动次数
        self.rounds_input_active = False  # 回合数输入框是否激活
        self.goals_input_active = False  # 球数输入框是否激活
        
        # 初始化游戏状态变量
        self.red_pieces, self.blue_pieces, self.football = init_game_pieces(self.start_player)
        self.current_player = self.start_player
        self.red_score = 0  # 红方得分
        self.blue_score = 0  # 蓝方得分
        self.round_count = 0     # 回合数
        self.player_turn_count = 0    # 玩家当前回合移动次数
        self.moved_piece = []   # 用于标记回合内移动过的棋子
        self.running = True      # 游戏是否运行
        self.show_quit_popup = False    # 是否显示退出弹窗
        self.show_start_popup = True  # 游戏开始时显示设置弹窗
        self.show_game_over_popup = False
        self.selected_piece = PieceIndex.NO_PIECE  # 用于标记选中的棋子
        self.valid_moves = []    # 用于存储选中棋子的有效移动位置
        self.round_goal = False  # 用于判断回合内是否有进球
        self.winner = None
        
        # 游戏撤销备份
        self.back = False
        self.back_red_pieces = []
        self.back_blue_pieces = []
        self.back_football = None
        self.back_current_player = 0
        self.back_red_score = 0
        self.back_blue_score = 0
        self.back_round_count = 0     
        self.back_player_turn_count = 0    
        self.back_moved_piece = []   
        self.back_selected_piece = PieceIndex.NO_PIECE  
        self.back_valid_moves = []    
        self.back_round_goal = False  
        self.back_winner = None

        
        # 加载音效
        self.kick_sound = sound_kick
        self.run_sound = sound_run
        self.run_with_football_sound = sound_run_with_football
        self.goal_sound = sound_cheer
        self.music_on = True  # 音乐默认为打开状态

    # 切换音乐开关状态
    def toggle_music(self):
        self.music_on = not self.music_on
        return self.music_on


    # 获取棋子对象的函数
    def get_piece_by_index(self, index):
        if index == 0:
            return self.football
        for piece in self.red_pieces + self.blue_pieces:
            if piece.index == index:
                return piece
        return None

    def football_contral(self):
        if self.current_player == RED_TEAM:
            return self.football.is_adjacent_to_current_pieces(self.red_pieces)
        else:
            return self.football.is_adjacent_to_current_pieces(self.blue_pieces)

    def turn_over(self):
        goal = False
        # 玩家操作回合结束
        self.moved_piece.append(self.selected_piece)
        self.selected_piece = -1
        self.valid_moves = []
        
        self.player_turn_count += 1
        if not self.round_goal: 
            self.round_goal = self.check_goal()
        goal = self.round_goal

        # 回合结束
        if self.player_turn_count >= self.movements_every_round:
            self.current_player = change_team(self.current_player)
            self.player_turn_count = 0
            self.moved_piece = []
            self.round_count += 1
            self.round_goal = False
        
        # 返回是否进球
        return goal

    # 检查足球是否进入对方球门
    def check_goal(self):
        if (self.football.x, self.football.y) in FieldArea.RED_GOAL:
            # 足球进入红方球门，蓝方得分
            self.blue_score += 1
            return True
        
        elif (self.football.x, self.football.y) in FieldArea.BLUE_GOAL:
            # 足球进入蓝方球门，红方得分
            self.red_score += 1
            return True

        return False

    # 检查棋子是否受控
    def check_piece_control(self):
        # 先全部设置为未受控
        for piece in self.red_pieces + self.blue_pieces:
            piece.control = False
        self.football.control = False
        # 己方棋子没有移动过的受控
        if self.current_player == RED_TEAM:
            for piece in self.red_pieces:
                if piece.index not in self.moved_piece:
                    piece.control = True
        else:
            for piece in self.blue_pieces:
                if piece.index not in self.moved_piece:
                    piece.control = True
        # 足球与己方棋子相邻的受控
        if self.football_contral():
            self.football.control = True

    # 检查游戏是否结束
    def check_game_over(self):
        game_over = False
        if self.game_mode == 'goals':
            # 一球定胜负模式，只要有一方得分就结束
            if self.red_score >= self.max_goals or self.blue_score >= self.max_goals:
                self.winner = '蓝方' if self.blue_score > self.red_score else '红方'
                game_over = True
        elif self.game_mode == 'rounds' and self.round_count >= self.max_rounds:
            # 回合制模式，达到最大回合数
            self.winner = '蓝方' if self.blue_score > self.red_score else '红方' if self.red_score > self.blue_score else '平局'
            game_over = True
        return game_over

    # 播放足球音效
    def play_sound(self, sound_type):
        if sound_type == GameSound.KICK:
            if self.kick_sound:
                try:
                    self.kick_sound.play()
                except pygame.error as e:
                    print(f"播放音效时出错: {e}")
            else:
                print("音效未加载，无法播放")
        elif sound_type == GameSound.RUN:
            if self.run_sound:
                try:
                    self.run_sound.play()
                except pygame.error as e:
                    print(f"播放音效时出错: {e}")
            else:
                print("音效未加载，无法播放")
        elif sound_type == GameSound.RUN_WITH_FOOTBALL:
            if self.run_with_football_sound:
                try:
                    self.run_with_football_sound.play()
                except pygame.error as e:
                    print(f"播放音效时出错: {e}")
            else:
                print("音效未加载，无法播放")
        elif sound_type == GameSound.GOAL:
            if self.goal_sound:
                try:
                    self.goal_sound.play()
                except pygame.error as e:
                    print(f"播放音效时出错: {e}")
            else:
                print("音效未加载，无法播放")

    # 重置游戏状态
    def reset_game(self):
        self.start_player = change_team(self.start_player)
        self.red_pieces, self.blue_pieces, self.football = init_game_pieces(self.start_player)
        self.current_player = self.start_player
        self.red_score = 0  # 红方得分
        self.blue_score = 0  # 蓝方得分
        self.round_count = 0     # 回合数
        self.player_turn_count = 0    # 玩家当前回合移动次数
        self.moved_piece = []   # 用于标记回合内移动过的棋子
        self.running = True      # 游戏是否运行
        self.show_quit_popup = False    # 是否显示退出弹窗
        self.show_start_popup = False  # 游戏开始时显示设置弹窗
        self.show_game_over_popup = False
        self.selected_piece = PieceIndex.NO_PIECE  # 用于标记选中的棋子
        self.valid_moves = []    # 用于存储选中棋子的有效移动位置
        self.round_goal = False  # 用于判断回合内是否有进球
        self.winner = None
        self.clear_backup()


    def save_backup(self):
        self.back = True
        self.back_piece_x = []
        self.back_piece_y = []
        for piece in [self.football] + self.red_pieces + self.blue_pieces:
            self.back_piece_x.append(piece.x)
            self.back_piece_y.append(piece.y)
        self.back_current_player = self.current_player
        self.back_red_score = self.red_score
        self.back_blue_score = self.blue_score
        self.back_round_count = self.round_count
        self.back_player_turn_count = self.player_turn_count
        # 创建moved_piece列表的深拷贝以实现真正的备份
        self.back_moved_piece = self.moved_piece.copy()
        self.back_selected_piece = PieceIndex.NO_PIECE
        self.back_valid_moves = []
        self.back_round_goal = self.round_goal
        self.back_winner = self.winner
        print(self.back_moved_piece)

    def excute_back(self):
        if self.back:
            for i,piece in enumerate([self.football] + self.red_pieces + self.blue_pieces):
                piece.x = self.back_piece_x[i]
                piece.y = self.back_piece_y[i]
            self.current_player = self.back_current_player
            self.red_score = self.back_red_score
            self.blue_score = self.back_blue_score
            self.round_count = self.back_round_count
            self.player_turn_count = self.back_player_turn_count
            self.moved_piece = self.back_moved_piece
            self.selected_piece = self.back_selected_piece
            self.valid_moves = self.back_valid_moves
            self.round_goal = self.back_round_goal
            self.winner = self.back_winner

            #清除备份
            self.clear_backup()

    def clear_backup(self):
         # 游戏清除备份
        self.back = False
        self.back_piece_x = []
        self.back_piece_y = []
        self.back_current_player = 0
        self.back_red_score = 0
        self.back_blue_score = 0
        self.back_round_count = 0     
        self.back_player_turn_count = 0    
        self.back_moved_piece = []   
        self.back_selected_piece = PieceIndex.NO_PIECE  
        self.back_valid_moves = []    
        self.back_round_goal = False  
        self.back_winner = None