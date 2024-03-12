import pygame
import sys
import random

import config

import player
import enemy
import background
import bird

pygame.init()

pygame.display.set_caption("game")
pygame.display.set_icon(pygame.image.load("img/icon.png"))

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame. RESIZABLE)
clock = pygame.time.Clock()

player = player.Player()

enemies = [enemy.Enemy()]
removed_enemies = []

background = background.Background()

birds = [bird.Bird()]
removed_birds = []
bird_timer = 0

interval = 3000
min_interval = 600

def display_tutorial(_screen):
    _screen.fill((255, 0, 0))
    _screen.blit(pygame.font.SysFont(None, 48).render("make the player jump with space or up", True, (255, 255, 255)), (config.SCREEN_WIDTH/3, config.SCREEN_HEIGHT/3))
    _screen.blit(pygame.font.SysFont(None, 48).render("pull the player to the ground with down", True, (255, 255, 255)), (config.SCREEN_WIDTH/3, config.SCREEN_HEIGHT/2))
    _screen.blit(pygame.font.SysFont(None, 48).render("press space to start the game", True, (255, 255, 255)), (config.SCREEN_WIDTH/3, config.SCREEN_HEIGHT/1.5))

def draw(_screen):
    sprites = pygame.sprite.Group()
    sprites.add(player)
    for i in enemies:
        sprites.add(i)
    for i in birds:
        sprites.add(i)
    sprites.draw(_screen)

def collision():
    global removed_enemies
    for i in enemies:
        if player.rect.colliderect(i.rect):
            removed_enemies.append(i)
            player.lives -= 1

def spawn_enemy():
    enemies.append(enemy.Enemy())

    global interval

    if interval > min_interval:
        interval -= 100

    elif interval < min_interval:
        interval = min_interval

    for i in enemies:
        i.speed += 5  


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
tutorial = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if tutorial:
        screen.fill((0, 0, 0))
        screen.blit(pygame.font.SysFont(None, 48).render("make the player jump with space or up", True, (255, 255, 255)), (config.SCREEN_WIDTH/4, config.SCREEN_HEIGHT/3))
        screen.blit(pygame.font.SysFont(None, 48).render("pull the player to the ground with down", True, (255, 255, 255)), (config.SCREEN_WIDTH/4, config.SCREEN_HEIGHT/2))
        screen.blit(pygame.font.SysFont(None, 48).render("press space to start the game", True, (255, 255, 255)), (config.SCREEN_WIDTH/4, config.SCREEN_HEIGHT/1.5))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            tutorial = False
    else:
        if player.lives <= 0:
            game_over = True

        if game_over:
            if player.score > hi_score:
                hi_score = player.score

            # Death Screen
            screen.fill((0, 0, 0))
            screen.blit(pygame.font.SysFont(None, 48).render(f"HI-SCORE: {hi_score}", True, (0, 255, 0)), (config.SCREEN_WIDTH/3, config.SCREEN_HEIGHT/4))
            screen.blit(pygame.font.SysFont(None, 48).render(f"SCORE: {player.score}", True, (0, 0, 255)), (config.SCREEN_WIDTH/3, config.SCREEN_HEIGHT/3))
            screen.blit(pygame.font.SysFont(None, 48).render("press r to restart", True, (255, 255, 255)), (config.SCREEN_WIDTH/3, config.SCREEN_HEIGHT/2))
            screen.blit(pygame.font.SysFont(None, 48).render("press q to quit", True, (255, 255, 255)), (config.SCREEN_WIDTH/3, config.SCREEN_HEIGHT/1.5))

            keys = pygame.key.get_pressed()

            if keys[pygame.K_r]:
                player.position = pygame.Vector2(config.SCREEN_WIDTH/6, config.COLLISION_HEIGHT)
                player.score = 0
                player.lives = 1
                enemies = [enemy.Enemy()]
                birds = [bird.Bird()]

                interval = 3000

                last_spawn_time = pygame.time.get_ticks()
                last_score_time = pygame.time.get_ticks()

                game_over = False

            if keys[pygame.K_q]:
                with open("data/scores.txt", "w") as file:
                    file.write(str(hi_score))
                running = False

            pygame.display.update()

        else:
            if pygame.key.get_pressed()[pygame.K_q]:
                running = False

            player.movement()

            # Adding Enemies To Be Removed + Moving Enemy
            removed_enemies = []
            for i in enemies:
                if i.position.x < 0:
                    removed_enemies.append(i)

                i.movement()

            # Adding Birds To Be Removed + Moving Bird
            removed_birds = []
            for i in birds:
                if i.position.x < 0:
                    removed_birds.append(i)
                
                i.movement()

            collision()

            # Draw Background + UI
            background.draw(screen)
            screen.blit(pygame.font.SysFont(None, 48).render(f"SCORE: {str(player.score)}", True, (0, 0, 0)), (10, 10))
            screen.blit(pygame.font.SysFont(None, 48).render(f"FPS: {str(int(clock.get_fps()))}", True, (0, 0, 0)), (config.SCREEN_WIDTH-130, 10))

            draw(screen)

            current_time = pygame.time.get_ticks()

            # Spawn Enemy
            if current_time - last_spawn_time >= interval:
                spawn_enemy()
                last_spawn_time = current_time
            
            # Spawn Bird
            if bird_timer >= random.randint(200, 400):
                birds.append(bird.Bird())
                bird_timer = 0

            # Increase Score
            if current_time - last_score_time >= 500:
                player.score += 1
                last_score_time = current_time

            # Remove Enemies
            for i in removed_enemies:
                enemies.remove(i)

            # Remove Birds
            for i in removed_birds:
                birds.remove(i)

            bird_timer += 1

            background.update()

    pygame.display.update()
    clock.tick(config.FPS)
