import pygame
import random

import config

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 4
        self.position = pygame.Vector2(config.SCREEN_WIDTH-8, random.randint(10, 200))
        self.image = pygame.image.load("img/bird.png")
        self.base = self.image
        self.rect = self.base.get_rect(center=self.position)

    def movement(self):
        self.position.x -= self.speed

        self.rect = self.base.get_rect(center=self.position)
