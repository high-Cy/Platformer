CAPTION = 'Platformer'
# ICON = ''

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.7)
FPS = 60

# Game Variables
MAX_HEALTH = 5
GRAVITY = 0.75
WALK_SPEED = 3
JUMP_GRAVITY = 1
JUMP_VEL = -12

# Action Index
IDLE_IDX = 'idle'
RUN_IDX = 'run'
DEAD_IDX = 'die'
HIT_IDX = 'hit'
ATTACK_IDX = 'attack'
JUMP_IDX = 'jump'

# Animation Cooldowns
IDLE_ANI = 200
RUN_ANI = 100
DEAD_ANI = 400
HURT_ANI = 100
ATTACK_ANI = 100
JUMP_ANI = 0

# Timers
KILL_TIMER = 300  # kill sprite
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
