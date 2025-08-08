# pieces_class.py
# 棋子类定义

import pygame
from game_constants import *


# 初始化棋子类
# 为Piece类添加一个类变量用于生成唯一索引
class Piece:
    _next_index = 1  # 类变量，用于生成唯一索引，从1开始

    def __init__(self, x, y, color, piece_type):
        self.x = x
        self.y = y
        self.color = color
        self.piece_type = piece_type
        self.original_x = x  # 保存初始位置用于重置
        self.original_y = y
        # 为每个棋子分配唯一索引
        self.index = Piece._next_index
        Piece._next_index += 1
        # 缩放图片以适应棋盘格子
        self.image = pygame.transform.scale(piece_images[(color, piece_type)], (SQUARE_SIZE, SQUARE_SIZE))
        self.image_on = pygame.transform.scale(piece_on_images[(color, piece_type)], (SQUARE_SIZE, SQUARE_SIZE))
        self.control = False

    def draw(self, screen):
        # 绘制棋子图片
        if self.control:
            screen.blit(self.image_on, (self.x * SQUARE_SIZE, self.y * SQUARE_SIZE))
        else:
            screen.blit(self.image, (self.x * SQUARE_SIZE, self.y * SQUARE_SIZE))
        # # 如果棋子被选中，绘制选中标识
        # if hasattr(self, 'selected') and self.selected:
        #     pygame.draw.rect(screen, WHITE, (
        #         self.x * SQUARE_SIZE, self.y * SQUARE_SIZE, 
        #         SQUARE_SIZE, SQUARE_SIZE
        #     ), 3)

    def is_valid_move(self, new_x, new_y, pieces, football=None):
        # 检查是否移动到棋盘外
        if not (0 <= new_x < BOARD_WIDTH and 0 <= new_y < BOARD_HEIGHT):
            return False

        # 检查是否移动到自己棋子的位置
        for piece in pieces:
            if piece.x == new_x and piece.y == new_y:
                return False

        # 检查是否移动到足球的位置
        if football and football.x == new_x and football.y == new_y:
            # 此时足球可能会向后一格
            delta_x = new_x - self.x
            football_new_x = football.x + (
                0 if delta_x == 0 else
                1 if delta_x > 1 else
                -1 if delta_x < -1 else
                delta_x
            )
            delta_y = new_y - self.y
            football_new_y = football.y + (
                0 if delta_y == 0 else
                1 if delta_y > 1 else
                -1 if delta_y < -1 else
                delta_y
            )
            # 检查足球是否移动到棋盘外
            if not (0 <= football_new_x < BOARD_WIDTH and 0 <= football_new_y < BOARD_HEIGHT):
                return False
            # 检查足球是否移动到自己棋子的位置
            for piece in pieces:
                if piece.x == football_new_x and piece.y == football_new_y:
                    return False

        # 根据棋子类型检查移动规则
        if self.piece_type == PieceType.GOALKEEPER:
            # 守门员只能在球门区域移动，且每回合只能移动一步
            if (self.y == 0 and not (BOARD_WIDTH // 2 - 1 <= new_x <= BOARD_WIDTH // 2 + 1 and new_y == 0)) or \
                    (self.y == BOARD_HEIGHT - 1 and not (
                            BOARD_WIDTH // 2 - 1 <= new_x <= BOARD_WIDTH // 2 + 1 and new_y == BOARD_HEIGHT - 1)):
                return False
            # 守门员每回合只能移动一步
            if abs(new_x - self.x) + abs(new_y - self.y) != 1:
                return False

        elif self.piece_type == PieceType.DEFENDER:
            # 后卫每回合只能往前后左右四个方向移动1格
            if abs(new_x - self.x) + abs(new_y - self.y) != 1:
                return False
            # 后卫只能待在自己的半场
            if (self.color == RED and new_y >= BOARD_HEIGHT // 2) or \
                    (self.color == BLUE and new_y < BOARD_HEIGHT // 2):
                return False
            # 后卫不能进入第一行或最后一行
            if new_y == 0 or new_y == BOARD_HEIGHT - 1:
                return False

        elif self.piece_type == PieceType.MIDFIELDER:
            # 中场每回合只能往前后左右四个方向移动1格，或者往对角线方向移动1格
            if not ((abs(new_x - self.x) + abs(new_y - self.y) == 1) or \
                    (abs(new_x - self.x) == 1 and abs(new_y - self.y) == 1)):
                return False
            # 中场不能进入第一行或最后一行
            if new_y == 0 or new_y == BOARD_HEIGHT - 1:
                return False
            # 中场不能和球门相邻
            if (new_x, new_y) in FieldArea.BLUE_PENALTY_AREA or (new_x, new_y) in FieldArea.RED_PENALTY_AREA:
                return False

        elif self.piece_type == PieceType.FORWARD:
            # 前锋每回合只能往前后左右四个方向移动1至2格，或者往对角线方向移动1格
            move_valid = False
            # 前后左右移动1格
            if abs(new_x - self.x) + abs(new_y - self.y) == 1:
                move_valid = True
            # 前后左右移动2格
            elif (abs(new_x - self.x) == 2 and new_y == self.y) or \
                    (abs(new_y - self.y) == 2 and new_x == self.x):
                # 检查移动路径上是否有棋子
                step_x = 1 if new_x > self.x else -1 if new_x < self.x else 0
                step_y = 1 if new_y > self.y else -1 if new_y < self.y else 0
                middle_x = self.x + step_x
                middle_y = self.y + step_y
                for piece in pieces:
                    if piece.x == middle_x and piece.y == middle_y:
                        return False
                move_valid = True
            # 对角线移动1格
            elif abs(new_x - self.x) == 1 and abs(new_y - self.y) == 1:
                move_valid = True

            if not move_valid:
                return False

            # 前锋不能进入第一行或最后一行
            if new_y == 0 or new_y == BOARD_HEIGHT - 1:
                return False
            # 前锋不能和球门相邻
            if (new_x, new_y) in FieldArea.BLUE_NEAR_GOAL_AREA or (new_x, new_y) in FieldArea.RED_NEAR_GOAL_AREA:
                return False

        return True

    def get_valid_moves(self, pieces, football=None):
        # 获取所有有效的移动位置
        valid_moves = []
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                if self.is_valid_move(x, y, pieces, football):
                    valid_moves.append((x, y))
        return valid_moves

    def move(self, new_x, new_y, football, red_pieces, blue_pieces):
        # 带球移动：移动棋子并根据规则更新足球位置
        old_x, old_y = self.x, self.y
        self.x, self.y = new_x, new_y

        # 检查是否移动到足球原位置上
        if football and football.x == new_x and football.y == new_y:
            # 此时足球可能会向后一格
            delta_x = new_x - old_x
            football_new_x = football.x + (
                0 if delta_x == 0 else
                1 if delta_x > 1 else
                -1 if delta_x < -1 else
                delta_x
            )
            delta_y = new_y - old_y
            football_new_y = football.y + (
                0 if delta_y == 0 else
                1 if delta_y > 1 else
                -1 if delta_y < -1 else
                delta_y
            )

            # 检查足球新位置是否有效（为空或有对方棋子）
            valid = True
            opponent_pieces = blue_pieces if self.color == RED else red_pieces
            for piece in red_pieces + blue_pieces:
                if piece.x == football_new_x and piece.y == football_new_y:
                    valid = False
                    break

            if valid and 0 <= football_new_x < BOARD_WIDTH and 0 <= football_new_y < BOARD_HEIGHT:
                football.x, football.y = football_new_x, football_new_y
                return True  # 足球跟随移动

        # 检查足球是否与原位置相邻
        if football.is_adjacent_to_piece(Piece(old_x, old_y, self.color, self.piece_type)):
            # 计算足球的新位置（跟随移动）
            football_new_x = football.x + (new_x - old_x)
            football_new_y = football.y + (new_y - old_y)

            # 检查足球新位置是否有效（为空或有对方棋子）
            valid = True
            for piece in red_pieces + blue_pieces:
                if piece.x == football_new_x and piece.y == football_new_y:
                    valid = False
                    break

            if valid and 0 <= football_new_x < BOARD_WIDTH and 0 <= football_new_y < BOARD_HEIGHT:
                football.x, football.y = football_new_x, football_new_y
                return True  # 足球跟随移动
        return False  # 足球未移动


# 定义足球类，重写绘制方法
class FootballPiece(Piece):
    def __init__(self, x, y):
        super().__init__(x, y, GREEN, -1)  # -1 表示不是常规棋子
        self.index = 0  # 足球的index固定为0
        self.control = False
        self.image = pygame.transform.scale(piece_images[(GREEN, PieceType.FOOTBALL)], (SQUARE_SIZE, SQUARE_SIZE))
        self.image_on = pygame.transform.scale(piece_on_images[(GREEN, PieceType.FOOTBALL)], (SQUARE_SIZE, SQUARE_SIZE))

    def draw(self, screen):
        # 绘制棋子图片
        if self.control:
            screen.blit(self.image_on, (self.x * SQUARE_SIZE, self.y * SQUARE_SIZE))
        else:
            screen.blit(self.image, (self.x * SQUARE_SIZE, self.y * SQUARE_SIZE))

    def is_adjacent_to_piece(self, piece):
        # 检查足球是否与指定棋子在上下左右四个方向相邻
        dx = abs(self.x - piece.x)
        dy = abs(self.y - piece.y)
        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

    def is_adjacent_to_current_pieces(self, current_pieces):
        # 检查足球是否与任何己方棋子相邻
        for piece in current_pieces:
            if self.is_adjacent_to_piece(piece):
                return True
        return False

    def is_valid_move(self, new_x, new_y, pieces):
        # 检查目标位置是否在棋盘内
        if not (0 <= new_x < BOARD_WIDTH and 0 <= new_y < BOARD_HEIGHT):
            return False

        # 检查目标位置是否有棋子
        for piece in pieces:
            if piece.x == new_x and piece.y == new_y:
                return False

        # 足球每回合只能往前后左右四个方向移动1至2格，或者往对角线方向移动1格

        # 前后左右移动1格
        if abs(new_x - self.x) + abs(new_y - self.y) == 1:
            return True
        # 前后左右移动2格
        elif (abs(new_x - self.x) == 2 and new_y == self.y) or \
                (abs(new_y - self.y) == 2 and new_x == self.x):
            return True
        # 对角线移动1格
        elif abs(new_x - self.x) == 1 and abs(new_y - self.y) == 1:
            return True

        # 足球可以往对角线方向移动2格，但是中间不能越过棋子
        elif abs(new_x - self.x) == 2 and abs(new_y - self.y) == 2:
            # 检查中间位置是否有棋子
            middle_x = (self.x + new_x) // 2
            middle_y = (self.y + new_y) // 2
            for piece in pieces:
                if piece.x == middle_x and piece.y == middle_y:
                    return False
            return True

        # 足球可以前后移动3格，但是不能越过两个人
        if abs(new_y - self.y) == 3 and abs(new_x - self.x) == 0:
            # 检查移动路径上是否有棋子
            step_y = 1 if new_y > self.y else -1
            for i in range(1, 4):
                middle_y = self.y + step_y * i
                for piece in pieces:
                    if piece.x == self.x and piece.y == middle_y:
                        return False
            return True

        return False

    def get_valid_moves(self, pieces):
        # 获取所有有效的移动位置
        valid_moves = []
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                if self.is_valid_move(x, y, pieces):
                    valid_moves.append((x, y))
        return valid_moves

    def move(self, new_x, new_y):
        # 移动足球并根据规则更新位置
        self.x, self.y = new_x, new_y
        return True

    # 球门开球位置
    def get_own_goal_position(self, pieces, current_player):
        # 获取所有有效的移动位置
        valid_moves = []
        if current_player == RED_TEAM:
            # 在红方半场
            for x in range(BOARD_WIDTH):
                for y in range(1, BOARD_HEIGHT // 2):
                    for piece in pieces:
                        if piece.x == x and piece.y == y:
                            break
                    else:
                        valid_moves.append((x, y))
        elif current_player == BLUE_TEAM:
            # 在蓝方半场
            for x in range(BOARD_WIDTH):
                for y in range(BOARD_HEIGHT // 2, BOARD_HEIGHT - 1):
                    for piece in pieces:
                        if piece.x == x and piece.y == y:
                            break
                    else:
                        valid_moves.append((x, y))
        return valid_moves

    def is_in_opponent_goal(self, current_player):
        # 检查足球是否进入对方球门
        if current_player == RED_TEAM:
            if self.y == BOARD_HEIGHT - 1 and (BOARD_WIDTH // 2 - 1 <= self.x <= BOARD_WIDTH // 2 + 1):
                return True
        elif current_player == BLUE_TEAM:
            if self.y == 0 and (BOARD_WIDTH // 2 - 1 <= self.x <= BOARD_WIDTH // 2 + 1):
                return True
        return False

    def is_in_own_goal(self, current_player):
        # 检查足球是否在己方球门
        if current_player == RED_TEAM:
            if self.y == 0 and (BOARD_WIDTH // 2 - 1 <= self.x <= BOARD_WIDTH // 2 + 1):
                return True
        elif current_player == BLUE_TEAM:
            if self.y == BOARD_HEIGHT - 1 and (BOARD_WIDTH // 2 - 1 <= self.x <= BOARD_WIDTH // 2 + 1):
                return True
        return False
