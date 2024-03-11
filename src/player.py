import pygame

import config

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.jump_power = 192
        self.position = pygame.Vector2(config.SCREEN_WIDTH/6, config.COLLISION_HEIGHT)
        self.velocity = pygame.Vector2()
        self.image = pygame.image.load("img/player.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.base = self.image
        self.rect = self.base.get_rect(center=self.position)

        self.current_keys = []
        self.previous_keys = []

        self.lives = 1
        self.score = 0

    def movement(self):
        self.velocity = pygame.Vector2()
        self.velocity.y += 4

        self.current_keys = pygame.key.get_pressed()

        if (self.current_keys[pygame.K_SPACE] or self.current_keys[pygame.K_UP]) and self.previous_keys[pygame.K_SPACE] == False and self.position.y >= config.COLLISION_HEIGHT:
            self.velocity.y -= self.jump_power

        if self.current_keys[pygame.K_DOWN] or self.current_keys[pygame.K_s]:
            self.velocity.y += 4

        # check out of bounds
        if self.position.y > config.COLLISION_HEIGHT:
            self.position.y = config.COLLISION_HEIGHT

        self.position += self.velocity
        self.rect = self.base.get_rect(center=self.position)
        self.previous_keys = self.current_keys
