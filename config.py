import os

# Display Settings
SCREEN_WIDTH = 240
SCREEN_HEIGHT = 240
FPS = 30
BACKGROUND_COLOR = (255, 255, 255)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game Physics
GRAVITY = 9.81
FRICTION = 0.98
MAX_POWER = 100
MIN_POWER = 10

# Golf Settings
MAX_SHOTS = 6
PAR = 3

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')

# Platform detection
def is_raspberry_pi():
    try:
        import board
        return True
    except ImportError:
        return False

IS_RASPBERRY_PI = is_raspberry_pi()