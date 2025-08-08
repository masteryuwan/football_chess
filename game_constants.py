# game_constants.py
# 游戏常量和配置

from turtle import back
import pygame

# 获取屏幕尺寸
pygame.init()
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# 定义常量，窗口大小设为屏幕的三分之二
BOARD_WIDTH = 9
BOARD_HEIGHT = 16
# 根据屏幕尺寸调整方块大小，保证棋盘在新窗口合适显示
SQUARE_SIZE = min((screen_width * 2 // 3 - 200) // BOARD_WIDTH, screen_height * 2 // 3 // BOARD_HEIGHT)
WIDTH = BOARD_WIDTH * SQUARE_SIZE
HEIGHT = BOARD_HEIGHT * SQUARE_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GOAL_COLOR = (200, 200, 0, 128)
FONT_COLOR = BLACK
FONT_SIZE = int(30 * (screen_height / 1000))
# 右侧计分区域宽度
SCORE_AREA_WIDTH = 4 * SQUARE_SIZE
# 调整窗口宽度
TOTAL_WIDTH = WIDTH + SCORE_AREA_WIDTH
# 弹窗相关常量
POPUP_WIDTH = 8 * SQUARE_SIZE
POPUP_HEIGHT = 12 * SQUARE_SIZE
BUTTON_WIDTH = 2 * SQUARE_SIZE
BUTTON_HEIGHT = 1 * SQUARE_SIZE
YES_COLOR = (0, 255, 0)
NO_COLOR = (255, 0, 0)
RED_BUTTON_COLOR = (255, 50, 50)
BLUE_BUTTON_COLOR = (50, 50, 255)
NEUTRAL_COLOR = (200, 200, 200)
# 定义队伍
RED_TEAM = 0
BLUE_TEAM = 1


def change_team(current_team):
    return BLUE_TEAM if current_team == RED_TEAM else RED_TEAM


class PieceIndex:
    NO_PIECE = -1
    FOOTBALL = 0
    RED_GOALKEEPER = 1
    RED_DEFENDER_RIGHT = 2
    RED_DEFENDER_LEFT = 3
    RED_MIDFIELDER_RIGHT = 4
    RED_MIDFIELDER_LEFT = 5
    RED_FORWARD_RIGHT = 6
    RED_FORWARD_LEFT = 7
    BLUE_GOALKEEPER = 8
    BLUE_DEFENDER_LEFT = 9
    BLUE_DEFENDER_RIGHT = 10
    BLUE_MIDFIELDER_LEFT = 11
    BLUE_MIDFIELDER_RIGHT = 12
    BLUE_FORWARD_LEFT = 13
    BLUE_FORWARD_RIGHT = 14


# 定义棋子类型枚举
class PieceType:
    GOALKEEPER = 0
    DEFENDER = 1
    MIDFIELDER = 2
    FORWARD = 3
    FOOTBALL = -1


# 定义球场区域
class FieldArea:
    RED_GOAL = [(3, 0), (4, 0), (5, 0)]
    BLUE_GOAL = [(3, BOARD_HEIGHT - 1), (4, BOARD_HEIGHT - 1), (5, BOARD_HEIGHT - 1)]
    RED_NEAR_GOAL_AREA = [(3, 1), (4, 1), (5, 1)]
    BLUE_NEAR_GOAL_AREA = [(3, BOARD_HEIGHT - 2), (4, BOARD_HEIGHT - 2), (5, BOARD_HEIGHT - 2)]
    RED_PENALTY_AREA = [(3, 1), (4, 1), (5, 1), (3, 2), (4, 2), (5, 2)]
    BLUE_PENALTY_AREA = [(3, BOARD_HEIGHT - 2), (4, BOARD_HEIGHT - 2), (5, BOARD_HEIGHT - 2), (3, BOARD_HEIGHT - 3),
                         (4, BOARD_HEIGHT - 3), (5, BOARD_HEIGHT - 3)]
# 定义游戏音效：


class GameSound:
    KICK = 1
    RUN = 2
    RUN_WITH_FOOTBALL = 3
    GOAL = 4


# 加载棋子图片
piece_images = {
    (RED, PieceType.GOALKEEPER): pygame.image.load('picture/red_goalkeeper.png'),
    (RED, PieceType.DEFENDER): pygame.image.load('picture/red_defender.png'),
    (RED, PieceType.MIDFIELDER): pygame.image.load('picture/red_midfielder.png'),
    (RED, PieceType.FORWARD): pygame.image.load('picture/red_forward.png'),
    (BLUE, PieceType.GOALKEEPER): pygame.image.load('picture/blue_goalkeeper.png'),
    (BLUE, PieceType.DEFENDER): pygame.image.load('picture/blue_defender.png'),
    (BLUE, PieceType.MIDFIELDER): pygame.image.load('picture/blue_midfielder.png'),
    (BLUE, PieceType.FORWARD): pygame.image.load('picture/blue_forward.png'),
    (GREEN, PieceType.FOOTBALL): pygame.image.load('picture/football.png'),
}
piece_on_images = {
    (RED, PieceType.GOALKEEPER): pygame.image.load('picture/red_goalkeeper_on.png'),
    (RED, PieceType.DEFENDER): pygame.image.load('picture/red_defender_on.png'),
    (RED, PieceType.MIDFIELDER): pygame.image.load('picture/red_midfielder_on.png'),
    (RED, PieceType.FORWARD): pygame.image.load('picture/red_forward_on.png'),
    (BLUE, PieceType.GOALKEEPER): pygame.image.load('picture/blue_goalkeeper_on.png'),
    (BLUE, PieceType.DEFENDER): pygame.image.load('picture/blue_defender_on.png'),
    (BLUE, PieceType.MIDFIELDER): pygame.image.load('picture/blue_midfielder_on.png'),
    (BLUE, PieceType.FORWARD): pygame.image.load('picture/blue_forward_on.png'),
    (GREEN, PieceType.FOOTBALL): pygame.image.load('picture/football_on.png'),
}

# 加载教练图片
red_coach_image = pygame.image.load('picture/red_coach.png')
blue_coach_image = pygame.image.load('picture/blue_coach.png')

# 加载队伍图片
red_team_image = pygame.image.load('picture/red_team.png')
blue_team_image = pygame.image.load('picture/blue_team.png')
draw_image = pygame.image.load('picture/draw.png')

field_image = pygame.image.load('picture/football_field.png')
field_image = pygame.transform.scale(field_image, (WIDTH, HEIGHT))
# 加载弹窗背景图片
popup_image = pygame.image.load('picture/popup.png')
# 缩放弹窗背景图片以适应弹窗尺寸
popup_image = pygame.transform.scale(popup_image, (POPUP_WIDTH, POPUP_HEIGHT))

# 加载按钮图片
start_button_image = pygame.image.load('picture/start_button.png')
start_button_image = pygame.transform.scale(start_button_image, (3 * SQUARE_SIZE, 1.5 * SQUARE_SIZE))
music_button_image = pygame.image.load('picture/music_button.png')
music_button_image = pygame.transform.scale(music_button_image, (1.5 * SQUARE_SIZE, 1.5 * SQUARE_SIZE))
music_button_off_image = pygame.image.load('picture/music_button_off.png')
music_button_off_image = pygame.transform.scale(music_button_off_image, (1.5 * SQUARE_SIZE, 1.5 * SQUARE_SIZE))
back_button_image = pygame.image.load('picture/back_button.png')
back_button_image = pygame.transform.scale(back_button_image, (1.5 * SQUARE_SIZE, 1.5 * SQUARE_SIZE))
back_button_off_image = pygame.image.load('picture/back_button_off.png')
back_button_off_image = pygame.transform.scale(back_button_off_image, (1.5 * SQUARE_SIZE, 1.5 * SQUARE_SIZE))
rules_button_image = pygame.image.load('picture/rules_button.png')
rules_button_image = pygame.transform.scale(rules_button_image, (1.5 * SQUARE_SIZE, 1.5 * SQUARE_SIZE))

# 加载音乐和音效
sound_background = pygame.mixer.Sound('sound/Green Pitch Rhythm.mp3')
sound_kick = pygame.mixer.Sound('sound/kick.mp3')
sound_run = pygame.mixer.Sound('sound/run.mp3')
sound_run_with_football = pygame.mixer.Sound('sound/run_with_football.mp3')
sound_cheer = pygame.mixer.Sound('sound/cheer.mp3')
