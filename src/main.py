import pygame
import sys

import config

import player
import enemy
import background

pygame.init()

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame. RESIZABLE)
clock = pygame.time.Clock()

player = player.Player()
enemies = [enemy.Enemy()]
removed_enemies = []
background = background.Background()

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

def get_last_hi_score():
    try:
        with open("data/scores.txt", "r") as file:
            return int(file.read())
    except ValueError:
        return 0

hi_score = get_last_hi_score()

last_spawn_time = pygame.time.get_ticks()
last_score_time = pygame.time.get_ticks()

running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if player.lives <= 0:
        game_over = True

    if game_over:
        if player.score > hi_score:
            hi_score = player.score

        screen.fill((0, 0, 0))
        screen.blit(pygame.font.SysFont(None, 48).render(f"HI-SCORE: {hi_score}", True, (0, 255, 0)), (config.SCREEN_WIDTH/3, config.SCREEN_HEIGHT/4))
        screen.blit(pygame.font.SysFont(None, 48).render(f"SCORE: {player.score}", True, (0, 0, 255)), (config.SCREEN_WIDTH/3, config.SCREEN_HEIGHT/3))
        screen.blit(pygame.font.SysFont(None, 48).render("press r to restart", True, (255, 255, 255)), (config.SCREEN_WIDTH/3, config.SCREEN_HEIGHT/2))
        screen.blit(pygame.font.SysFont(None, 48).render("press q to quit", True, (255, 255, 255)), (config.SCREEN_WIDTH/3, config.SCREEN_HEIGHT/1.5))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            player.score = 0
            player.lives = 1
            enemies = [enemy.Enemy()]

            interval = 3000

            last_spawn_time = pygame.time.get_ticks()
            last_score_time = pygame.time.get_ticks()

            game_over = False

        if keys[pygame.K_q]:
            with open("data/scores.txt", "w") as file:
                file.write(str(player.score))
            running = False

        pygame.display.update()

    else:
        print(hi_score)



        if pygame.key.get_pressed()[pygame.K_q]:
            running = False

        removed_enemies = []

        player.movement()

        for i in enemies:
            if i.position.x < 0:
                removed_enemies.append(i)

            i.movement()

        collision()


        background.draw(screen)
        screen.blit(pygame.font.SysFont(None, 48).render(f"SCORE: {str(player.score)}", True, (0, 0, 0)), (10, 10))
        screen.blit(pygame.font.SysFont(None, 48).render(f"FPS: {str(int(clock.get_fps()))}", True, (0, 0, 0)), (config.SCREEN_WIDTH-130, 10))

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


        background.update()

        pygame.display.update()
        clock.tick(config.FPS)
