FPS = 30

MOUSE_MODE_ROTATION = 0
MOUSE_MODE_TRANSLATION = 1

KEY_ZOOM_IN = b"+"
KEY_ZOOM_OUT = b"-"
KEY_FOV_INC = 101
KEY_FOV_DEC = 103
KEY_RESET = b"d"
KEY_RESET_PROJECTION = b"0"
KEY_EXIT = b"\x1b"

SCALE_MIN = 0.1
SCALE_MAX = 5

FOV_MIN = 0
FOV_MAX = 90

Z_NEAR = 0.01
Z_FAR = 100000
ROTATION_FACTOR = 100 # Track ball speed
MAP_SIZE = 9

MOVE_FRONT = b'w'
MOVE_BACK = b's'
MOVE_RIGHT = b'a'
MOVE_LEFT = b'd'
STOP = b' '

TICK = 0.005 # 1/FPS

BOTTOM_LEFT_FRONT = 0
BOTTOM_LEFT_BACK = 1
BOTTOM_RIGHT_BACK = 2
BOTTOM_RIGHT_FRONT = 3
TOP_LEFT_FRONT = 4
TOP_LEFT_BACK = 5
TOP_RIGHT_BACK = 6
TOP_RIGHT_FRONT = 7


UNIT_LENGTH = 0.5
WALL_HEIGHT = 4
ROAD_HEIGHT = 1
VELOCITY = UNIT_LENGTH*0.5
MAX_VELOCITY = UNIT_LENGTH*5

SENSITIVITY_X = 1
SENSITIVITY_Y = 0.2

NP_DTYPE = "float32"

WALL = 1
ROAD = 0


GAMEOVER_BITMAP_STRING = [ # Pixel Art for "D E A D"
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
    [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
]

GAMECLEAR_BITMAP_STRING = [
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
    
]