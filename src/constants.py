CAPTION = 'Platformer'
# ICON = ''

TILE_SIZE = 64
TILE_NUM_Y = 11

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = TILE_NUM_Y * TILE_SIZE
FPS = 60

# Game Variables
MAX_HEALTH = 5
GRAVITY = 0.75
WALK_SPEED = 5
JUMP_GRAVITY = 1
JUMP_VEL = -15

# Action Index
IDLE_IDX = 'idle'
RUN_IDX = 'run'
DEAD_IDX = 'die'
HIT_IDX = 'hit'
ATTACK_IDX = 'attack'
JUMP_IDX = 'jump'
LAND_IDX = 'land'

# Animation Cooldowns
IDLE_ANI = 200
RUN_ANI = 100
DEAD_ANI = 300
HURT_ANI = 100
ATTACK_ANI = 100
JUMP_ANI = 0
DUST_ANI = 50
TILE_ANI = 200

# Timers
KILL_TIMER = 500  # kill sprite
HURT_TIMER = 1000  # 1 second of invisibility after hurt

# Enemy Constants
ENEMY_SPEED = 1
ENEMY_SPEED_2 = 2
RUN_ANI_2 = 400
MOVE_COUNTER = 50
IDLE_COUNTER = 50

# items
HEALTH = 'Health'
DOUBJUMP = 'Doub_Jump'
APPLE = 'Apple'
COIN1 = 'Coin1'
COIN2 = 'Coin2'
COIN3 = 'Coin3'
KEY = 'Key'
