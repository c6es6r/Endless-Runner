import pygame

import config

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 10
        self.position = pygame.Vector2(config.SCREEN_WIDTH, config.COLLISION_HEIGHT)
        self.velocity = pygame.Vector2()
        self.image = pygame.image.load("img/enemy.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.base = self.image
        self.rect = self.base.get_rect(center=self.position)

    def movement(self):
        self.velocity = pygame.Vector2()
        self.position.x -= self.speed

        self.rect = self.base.get_rect(center=self.position)
