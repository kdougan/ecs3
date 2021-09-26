from esper import World
from pygame import Vector2
from src.components import *
from src.processors import *


def create_world(game):
    world = World()
    world.game = game

    add_processors(world)

    create_entities(world)

    return world


def add_processors(world):
    if not world.game.config.SERVER_MODE:
        world.renderer = RenderProcessor(world)

    world.add_processor(EventProcessor())
    world.add_processor(PhysicsProcessor())
    # world.add_processor(CollisionProcessor())
    resolution = Vector2(world.game.config.RESOLUTION)
    world.add_processor(MovementProcessor(
        Vector2((int(resolution.x), int(resolution.y))) * 0.5
    ))


def create_entities(world):
    world.create_entity(
        Renderable(image='square'),
        Transform(
            position=Vector2(100, 100),
            scale=Vector2(16, 16),
            rotation=0
        ),
        Velocity(0, 0),
        Physics(gravity=world.game.config.GRAVITY),
        PlayerControlled(),
        Collider()
    )
    world.create_entity(
        Renderable(image='square'),
        Transform(
            position=Vector2(100, 200),
            scale=Vector2(16, 16),
            rotation=0
        ),
        Velocity(0, 0),
        Physics(gravity=world.game.config.GRAVITY),
        Collider(fixed=True)
    )
