import sys

import pygame
from esper import Processor
from pygame import Vector2
from src.assets import AssetManager
from src.components import Collider, Collision, Physics, PlayerControlled, Renderable
from src.components import Transform
from src.components import Velocity


class RenderProcessor(Processor):
    """Processor for rendering."""

    def __init__(self, world):
        pygame.init()
        self.world = world
        resolution = Vector2(self.world.game.config.RESOLUTION)
        self.window = pygame.display.set_mode(
            (int(resolution.x), int(resolution.y)), pygame.DOUBLEBUF, 32)
        pygame.display.set_caption('Pygame ECS')
        self.display = pygame.Surface(resolution*0.5)

        self.asset_manager = AssetManager()

    def process(self):
        """Render the input data."""
        self.window.fill((0, 0, 0))
        self.display.fill((30, 10, 30))

        for _, (rend, transform) in self.world.get_components(Renderable, Transform):
            surf = self.asset_manager.get_image(rend.image)
            scale = (int(transform.scale.x), int(transform.scale.y))
            self.display.blit(
                pygame.transform.scale(surf, scale),
                transform.position
            )

        pygame.transform.scale(
            self.display, self.window.get_size(), self.window)
        pygame.display.flip()


class EventProcessor(Processor):
    def process(self):
        for event in pygame.event.get():
            if (
                event.type != pygame.QUIT
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
                or event.type == pygame.QUIT
            ):
                pygame.quit()
                sys.exit()
            for ent, (velocity, _) in self.world.get_components(Velocity, PlayerControlled):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        velocity.y -= self.world.game.config.PLAYER_JUMP_SPEED
                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_a, pygame.K_d]:
                        velocity.x = 0
                    if event.key == pygame.K_SPACE:
                        velocity.y = 0

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_a]:
                velocity.x = -self.world.game.config.PLAYER_SPEED
            if pressed[pygame.K_d]:
                velocity.x = self.world.game.config.PLAYER_SPEED


class PhysicsProcessor(Processor):
    def process(self):
        for _, (physics, velocity) in self.world.get_components(Physics, Velocity):
            velocity.y += physics.gravity * self.world.delta_time


class MovementProcessor(Processor):
    def __init__(self, bounds=None):
        self.bounds = bounds

    def process(self):
        for ent, (velocity, transform) in self.world.get_components(Velocity, Transform):
            if collision := self.world.try_component(ent, Collision):
                if collision.right:
                    transform.position.x = collision.rect.left
                elif collision.left:
                    transform.position.x = collision.rect.right - transform.scale.x
                if collision.top:
                    transform.position.y = collision.rect.bottom
                elif collision.bottom:
                    transform.position.y = collision.rect.top - transform.scale.y

                if collision.left or collision.right:
                    velocity.x = 0
                if collision.top or collision.bottom:
                    velocity.y = 0

                self.world.remove_component(ent, Collision)

            transform.position += velocity * self.world.delta_time

            if self.bounds:
                self.check_bounds(transform, velocity)

    def check_bounds(self, transform, velocity):
        width = transform.scale.x
        left = transform.position.x
        right = transform.position.x + width
        if left < 0:
            transform.position.x = 0
        elif right > self.bounds.x:
            transform.position.x = self.bounds.x - width

        height = transform.scale.y
        top = transform.position.y
        bottom = transform.position.y + height
        if top < 0:
            transform.position.y = 0
            velocity.y = 0
        elif bottom > self.bounds.y:
            transform.position.y = self.bounds.y - height
            velocity.y = 0


class CollisionProcessor(Processor):
    def process(self):
        for ent, (transform, velocity, collider) in self.world.get_components(Transform, Velocity, Collider):
            for _, (transform2, _) in self.world.get_components(Transform, Collider):
                if transform == transform2 or collider.fixed:
                    continue

                rect1 = pygame.Rect(transform.position,
                                    transform.scale.xy)
                rect2 = pygame.Rect(transform2.position,
                                    transform2.scale.xy)

                if collision := self.check_collision(rect1, velocity, rect2):
                    self.world.add_component(ent, collision)

    def check_collision(self, rect1, velocity, rect2):
        collision = Collision(rect2)
        did_collide = False
        rect1.y -= velocity.y * self.world.delta_time
        if rect1.colliderect(rect2):
            if velocity.x > 0:
                rect1.right = rect2.left
                collision.right = True
            elif velocity.x < 0:
                rect1.left = rect2.right
                collision.left = True
            did_collide = True

        rect1.y += velocity.y * self.world.delta_time
        if rect1.colliderect(rect2):
            if velocity.y > 0:
                rect1.bottom = rect2.top
                collision.bottom = True
            elif velocity.y < 0:
                rect1.top = rect2.bottom
                collision.top = True
            did_collide = True

        if did_collide:
            return collision
