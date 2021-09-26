import os


def to_bool(value):
    return str(value).strip().lower() in ['true', 'yes', 'y', '1']


class Config:
    SERVER_MODE = to_bool(os.getenv('SERVER_MODE', False))
    RESOLUTION = os.getenv('RESOLUTION', (1280, 720))
    GRAVITY = int(os.getenv('GRAVITY', 600))
    PLAYER_SPEED = int(os.getenv('PLAYER_SPEED', 300))
    PLAYER_JUMP_SPEED = int(os.getenv('PLAYER_JUMP_SPEED', 400))
