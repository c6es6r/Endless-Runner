import pygame
import math

import config
import game

pygame.init()

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pygame.time.Clock()

game = game.Game()

while game.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False

    pygame.display.update()
    clock.tick(config.FPS)
