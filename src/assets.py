import pygame


class AssetManager:
    def __init__(self):
        self.master = pygame.image.load('assets/master.png').convert_alpha()

        self.tile_size = (16, 16)
        self.sprites = {
            'square': self.slice(0, 0)
        }

    def slice(self, row, column):
        x = row * self.tile_size[0]
        y = column * self.tile_size[1]
        width, height = self.tile_size
        surf = self.master.subsurface(x, y, width, height)
        return surf.subsurface(surf.get_bounding_rect())

    def get_image(self, name):
        return self.sprites[name]
