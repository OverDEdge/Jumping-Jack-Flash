import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BROWN = (106, 55, 5)
LIGHTBLUE = (0, 155, 155)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Jumping Jack Flash"
INSTRUCTIONS_ARROWS = "Arrow Keys to Move"
INSTRUCTIONS_SPACE = "Space to Jump"
PRESS_TO_PLAY = "Press any Key to Start Playing or Press 'ESC' to Quit"
PRESS_TO_PLAY_AGAIN = "Press any Key to Start Playing Again or Press 'ESC' to Quit"
GAME_OVER_TEXT = "Game Over - You Died!"
SCORE_TEXT = "Your Score was: "
NEW_HIGHSCORE_TEXT = "Congrats! You set a new High Score of: "
HIGH_SCORE_TEXT = "High Score: "
BGCOLOR = BLACK
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
HS_FILE = "highscore.txt"
HIT_RECT = 0.5

# Text settings
FONT_NAME = 'arial'

# Player settings
PLAYER_HEALTH = 100
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SPEED = TILESIZE * 8
PLAYER_RUN = 0.5
PLAYER_GRAVITY = 0.4
PLAYER_JUMP_SPEED = -7.5
PLAYER_JUMP_FORCE = 0.32
PLAYER_JUMP_LIMIT = -6
PLAYER_FRICTION = -0.1
PLAYER_START_POS = (1 * TILESIZE, GRIDHEIGHT * TILESIZE - 100)

# Enemy settings
SLIME_EASY_SPAWN_PCT = 20
SLIME_MID_SPAWN_PCT = 50
SLIME_HARD_SPAWN_PCT = 80
SLIME_HARD_SCORE = 800
SLIME_MID_SCORE = 400
SLIME_SPEED = 1

# Graphics
PLAYER_SPRITESHEET = 'p3_spritesheet.png'
PLAYER_WALK_IMAGES = [(0, 0, 72, 97), (73, 0, 72, 97),
                        (146, 0, 72, 97), (0, 98, 72, 97), (73, 98, 72, 97),
                        (146, 98, 72, 97), (219, 0, 72, 97),
                        (292, 0, 72, 97), (219, 98, 72, 97),
                        (365, 0, 72, 97), (292, 98, 72, 97)]
PLAYER_STAND_IMAGES = [(67, 196, 66, 92), (0, 196, 66, 92)]
PLAYER_JUMP_IMAGES = [(438, 93, 67, 94)]
SWITCH_PLAYER_WALKING_IMAGE = 50
SWITCH_PLAYER_STANDING_IMAGE = 400
PLAYER_SCALE = (2, 2)
PLAYER_LAYER = 2
POW_LAYER = 1
PLATFORM_LAYER = 1
MOB_LAYER = 2
PLANET_LAYER = 0
WINDOW_X = 200
WINDOW_Y = 45
PLANET_SPAWN_RATE = 400

PLANET_IMAGE_NAME = 'planet{}.png'
PLANET_WIDTH = 300
PLANET_HEIGHT = 300
PLANET_SPEED = 1
PLANET_UPDATE_RATE = 50

TILES_SPRITESHEET = 'spritesheet_jumper.png'
TILES_PLATFORM_IMAGES = [(0, 192, 380, 94), (232, 1288, 200, 100),
                        (0, 864, 380, 94), (382, 0, 200, 100),
                        (0, 384, 380, 94), (213, 1662, 201, 100),
                        (0, 672, 380, 94), (208, 1879, 201, 100),
                        (0, 480, 380, 94), (213, 1764, 201, 100)]
PLATFORMS_SCALE = (2, 3)
PLATFORM_FAST = 1
PLATFORM_SLOW = 0.5
PLATFORM_SPEED = [PLATFORM_FAST, PLATFORM_SLOW]
PLATFORM_X_UPDATE = 50
PLATFORM_MOVE = 100
NOT_MOVING_PLATFORMS = 61
SLOW_MOVING_PLATFORMS = 20

ENEMY1_SPRITESHEET = 'enemies_spritesheet.png'
ENEMY1_SCALE = (2, 2)
SLIME_MOVE_IMAGES = [(52, 125, 50, 28), (0, 125, 51, 26)]
SWITCH_SLIME_MOVING_IMAGE = 300

# Sound
JUMP_SOUND = 'jump_11.wav'
BG_GAME_SOUND = 'Background Music 2.ogg'
BG_START_SOUND = 'little town - orchestral.ogg'
BG_END_SOUND = 'rpgcasaibgm.ogg'
FADEOUT = 500

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 40), (PLAYER_START_POS[0] - 50, HEIGHT * 3 / 4), (125, HEIGHT - 350), (450, 200), (900, 100), (300, 100), (50, 200), (200, 160), (500, 500), (200, HEIGHT - 80)]

# Mob settings
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
MOB_SPEED = TILESIZE
MOB_IMAGES = []
