import pygame
from pygame import Rect
from pygame import Vector2


class Renderable:
    def __init__(self, image: str, depth: int = 0):
        self.image = image
        self.depth = depth


class Transform:
    def __init__(self, position: Vector2, rotation: int, scale: Vector2):
        self.position = position
        self.rotation = rotation
        self.scale = scale


class Velocity(pygame.Vector2):
    pass


class Physics:
    def __init__(self, gravity: float = 0.0, damping: float = 0.0, friction: float = 0.0):
        self.gravity = gravity
        self.damping = damping
        self.friction = friction


class PlayerControlled:
    pass


class Collider:
    def __init__(self, fixed: bool = False) -> None:
        self.fixed = fixed


class Collision:
    def __init__(self, rect: Rect, top: bool = False, bottom: bool = False, left: bool = False, right: bool = False) -> None:
        self.rect = rect
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
