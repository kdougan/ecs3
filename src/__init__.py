import time
from src.config import Config
from src.world import create_world


class Game:
    def __init__(self):
        self.config = Config()
        self.world = create_world(self)

    def run(self):
        t = 0
        dt = 1 / 60

        current_time = time.perf_counter()

        while 1:
            new_time = time.perf_counter()
            frame_time = new_time - current_time
            current_time = new_time

            while frame_time > 0:

                delta_time = min(frame_time, dt)

                self.world.delta_time = delta_time
                self.world.game_time = t

                self.world.process()

                frame_time -= delta_time
                t += delta_time

            if not self.config.SERVER_MODE:
                self.world.renderer.process()

    def create_processors(self):
        pass
