import pygame
import math

import config
import player
import enemy

pygame.init()

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pygame.time.Clock()

player = player.Player()
enemies = [enemy.Enemy()]
removed_enemies = []
background = pygame.image.load("img/background.png")

interval = 3000


def draw():
    sprites = pygame.sprite.Group()
    sprites.add(player)
    for i in enemies:
        sprites.add(i)
    sprites.draw(screen)

def collision():
    global removed_enemies
    for i in enemies:
        if player.rect.colliderect(i.rect):
            removed_enemies.append(i)
            player.lives -= 1

def spawn_enemy():
    enemies.append(enemy.Enemy())

    global interval

    if interval >= 1250:
        interval -= 100

    for i in enemies:
        i.speed += 2

last_spawn_time = pygame.time.get_ticks()
last_score_time = pygame.time.get_ticks()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if player.lives <= 0:
        running = False

    screen.blit(background, (0, 0))
    screen.blit(pygame.font.SysFont(None, 48).render(f"SCORE: {str(player.score)}", True, (0, 0, 0)), (10, 10))

    removed_enemies = []

    player.movement()

    for i in enemies:
        if i.position.x < 0:
            enemies.remove(i)

        i.movement()

    collision()
    draw()

    current_time = pygame.time.get_ticks()

    if current_time - last_spawn_time >= interval:
        spawn_enemy()
        last_spawn_time = current_time

    if current_time - last_score_time >= 500:
        player.score += 1
        last_score_time = current_time


    for i in removed_enemies:
        enemies.remove(i)


    pygame.display.update()
    clock.tick(config.FPS)
