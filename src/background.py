import pygame
import math

import config

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/background.png").convert()
        self.image = pygame.transform.scale(self.image, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.tiles = math.ceil((config.SCREEN_WIDTH/self.image.get_width())) + 1
        self.scroll = 0

    def update(self):
        self.scroll -= 5

        if self.scroll*-1 > self.image.get_width():
            self.scroll = 0

    def draw(self, _screen):
        for i in range(self.tiles):
            _screen.blit(self.image, (i*self.image.get_width() + self.scroll, 0))
