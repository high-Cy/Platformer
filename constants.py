CAPTION = 'Platformer'

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.7)
FPS = 60

# Game Variables
GRAVITY = 0.75
WALK_SPEED = 3
JUMP_GRAVITY = 1
JUMP_VEL = -11

# Action Index
IDLE_IDX = 0
RUN_IDX = 1
DEAD_IDX = 2
HURT_IDX = 3
ATTACK_IDX = 4
JUMP_IDX = 5

# Animation Cooldowns
IDLE_ANI = 200
RUN_ANI = 100
DEAD_ANI = 400
HURT_ANI = 100
ATTACK_ANI = 100
JUMP_ANI = 0

# Timers
KILL_TIMER = 300  # kill sprite
HURT_TIMER = 3000  # 3 second of invisibility after hurt

# Items
HEALTH = 'Health'
DOUBJUMP = 'Doub_Jump'
APPLE = 'Apple'
COIN1 = 'Coin1'
COIN2 = 'Coin2'
COIN3 = 'Coin3'
KEY = 'Key'
