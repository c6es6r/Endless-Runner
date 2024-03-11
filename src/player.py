import pygame
import config

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.jump_power = 19
        self.gravity = 0.8
        self.position = pygame.Vector2(config.SCREEN_WIDTH/6,
                                       config.COLLISION_HEIGHT)
        self.velocity = pygame.Vector2()
        self.image = pygame.image.load("img/player.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.base = self.image
        self.rect = self.base.get_rect(center=self.position)
        self.jumnping = True
        
        self.keys = []

        self.lives = 1
        self.score = 0

    def movement(self):
        self.velocity.y += self.gravity

        self.keys = pygame.key.get_pressed()

        if (self.keys[pygame.K_UP] or self.keys[pygame.K_SPACE]) and\
                self.jumping is False:
            self.velocity.y = -self.jump_power
            self.jumping = True

        if self.keys[pygame.K_DOWN] or self.keys[pygame.K_s]:
            self.velocity.y += 4

        self.position += self.velocity

        if self.position.y > config.COLLISION_HEIGHT:
            self.position.y = config.COLLISION_HEIGHT
            self.velocity.y = 0
            self.jumping = False

        self.rect = self.base.get_rect(center=self.position)
