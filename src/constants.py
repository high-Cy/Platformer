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
DEAD_ANI = 500
HURT_ANI = 100
ATTACK_ANI = 100
JUMP_ANI = 0
DUST_ANI = 50
TILE_ANI = 200

# Timers
KILL_TIMER = 500            # kill sprite
HURT_TIMER = 1000           # 1 second of invisibility after hurt
ENDSCREEN_TIMER = 5000      # displays text after winning or losing level
OVERWORLD_TIMER = 1000      # pause when transitioning between lvl & overworld

# Enemy Constants
ENEMY_SPEED = 1
ENEMY_SPEED_2 = 2
ENEMY_DEAD_ANI = 400
RUN_ANI_2 = 400
MOVE_COUNTER = 50
IDLE_COUNTER = 50

# items
HEALTH_POTION = 'Health'
DIAMOND1 = 'Diamond1'
DIAMOND2 = 'Diamond2'
KEY = 'Key'

# diamond scores
D1_SCORE = 1
D2_SCORE = 5

# heal amount
HEAL_AMOUNT = 3

SKY_HORIZON = 5

SOUND_VOLUME = 0.2
