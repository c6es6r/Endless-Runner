import pygame
import math

import config
import player

pygame.init()

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pygame.time.Clock()

player = player.Player()

running = True

def draw():
    sprites = pygame.sprite.Group()
    sprites.add(player)
    sprites.draw(screen)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(pygame.image.load("img/background.png"), (0, 0))

    player.movement()

    draw()

    pygame.display.update()
    clock.tick(config.FPS)
