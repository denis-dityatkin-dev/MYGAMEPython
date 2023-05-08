import random
from os import listdir
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
pygame.init()
FPS = pygame.time.Clock()
screen = width, heigth = 800, 600
BLACK = 0, 0 , 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
font = pygame.font.SysFont('Verdana', 20)
main_surface = pygame.display.set_mode(screen)
IMGS_PATH = 'goose'
ball_imgs = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]
ball = ball_imgs[0]
ball_rect = ball.get_rect()
ball_speed = 5
def create_enemy():
    enemy_image = pygame.image.load('enemy.png').convert_alpha()
    enemy = pygame.transform.scale(enemy_image, (enemy_image.get_width() // 2, enemy_image.get_height() // 2))
    enemy_rect = pygame.Rect(width, random.randint(0, heigth), *enemy.get_size())
    if enemy_rect.right >= width or enemy_rect.left <= 0:
        enemy_speed = random.randint(4, 6)
    return [enemy, enemy_rect, enemy_speed]
def create_bonus():
    bonus_image = pygame.image.load('bonus.png').convert_alpha()
    bonus = pygame.transform.scale(bonus_image, (bonus_image.get_width() // 2, bonus_image.get_height() // 2))
    bonus_rect = pygame.Rect(random.randint(0, width), 0, *bonus.get_size())
    if bonus_rect.bottom >= heigth or bonus_rect.top <= 0:
        bonus_speed = random.randint(4, 6)
    return [bonus, bonus_rect, bonus_speed]
bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2500)
CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)
img_index = 0
scores = 0
enemies = []
bonuses = []
is_working = True
while is_working:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(ball_imgs):
                img_index = 0
            ball = ball_imgs[img_index]
    pressed_keys = pygame.key.get_pressed()
    bgX -= bg_speed
    bgX2 -= bg_speed
    if bgX < -bg.get_width():
        bgX = bg.get_width()
    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()
    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))
    main_surface.blit(ball, ball_rect)
    main_surface.blit(font.render(str(scores), True, RED), (width - 30, 0))
    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
        if ball_rect.colliderect(enemy[1]):
            is_working = False
            game_over_text = font.render('GAME OVER', True, RED)
            game_over_rect = game_over_text.get_rect(center=(width/2, heigth/2))
            main_surface.blit(game_over_text, game_over_rect)
            pygame.display.update()
            pygame.time.delay(1000) # изменено на 1000 миллисекунд
            pygame.quit()
            quit()
    for bonus in bonuses:
        bonus[1] = bonus[1].move(0,bonus[2])
        main_surface.blit(bonus[0], bonus[1])
        if bonus[1].bottom >= heigth:
            bonuses.pop(bonuses.index(bonus))
        if ball_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1
    if pressed_keys[K_DOWN] and not ball_rect.bottom >= heigth:
        ball_rect = ball_rect.move(0, ball_speed)
    if pressed_keys[K_UP] and not ball_rect.top <= 0:
        ball_rect = ball_rect.move(0, -ball_speed)
    if pressed_keys[K_RIGHT] and not ball_rect.right >= width:
        ball_rect = ball_rect.move(ball_speed, 0)
    if pressed_keys[K_LEFT] and not ball_rect.left <= 0:
        ball_rect = ball_rect.move(-ball_speed, 0)
    pygame.display.flip()
