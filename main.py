import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background.png')
pygame.mixer.music.load('back_music.wav')
pygame.mixer.music.play(-1)
pygame.display.set_caption("SPACE INVADERS")
icon = pygame.image.load('ufo_icon.png')
pygame.display.set_icon(icon)
player_img = pygame.image.load('player.png')
player_x = 370
player_y = 480
playerx_change = 0
enemy_img = []
enemy_x = []
enemy_y = []
enemyx_change = []
enemyy_change = []
num = 6
for i in range(num):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemyx_change.append(4)
    enemyy_change.append(40)
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bulletx_change = 0
bullety_change = 10
bullet_state = "ready"


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


font = pygame.font.Font('freesansbold.ttf', 64)


def gameover():
    text1 = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(text1, (200, 250))


score = 0
font2 = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 10


def scorer(x, y):
    text = font2.render("SCORE : " + str(score), True, (255, 255, 255))
    screen.blit(text, (x, y))


def collision(enemy_x, enemy_y, bullet_x, bullet_y):
    d = math.sqrt(math.pow((enemy_x - bullet_x), 2) + math.pow((enemy_y - bullet_y), 2))
    if d < 27:
        return True
    else:
        return False


run = True
while run:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -5
            if event.key == pygame.K_RIGHT:
                playerx_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulleter = pygame.mixer.Sound('bullet_fire.wav')
                    bulleter.play()
                    bullet_x = player_x
                    bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0
    player_x += playerx_change
    if player_x <= 0:
        player_x = 0
    if player_x >= 736:
        player_x = 736
    for i in range(num):
        if enemy_y[i] > 440:
            for j in range(num):
                enemy_y[j] = 2000
            gameover()
            break
        enemy_x[i] += enemyx_change[i]
        if enemy_x[i] <= 0:
            enemyx_change[i] = 4
            enemy_y[i] += enemyy_change[i]
        elif enemy_x[i] >= 736:
            enemyx_change[i] = -4
            enemy_y[i] += enemyy_change[i]
        c = collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if c:
            exp = pygame.mixer.Sound('explosion.wav')
            exp.play()
            bullet_y = 480
            bullet_state = "ready"
            score += 1
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)
        enemy(enemy_x[i], enemy_y[i], i)
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        bullet(bullet_x, bullet_y)
        bullet_y -= bullety_change
    player(player_x, player_y)
    scorer(textx, texty)
    pygame.display.update()
