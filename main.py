# Import Stuff That we need
import math
import random

import pygame
from pygame import mixer as mixer

game_state = "play"
clock = pygame.time.Clock()


# Make Our Difficulty Error
class DifficultyError(Exception):
    pass


# Set the basic styling
pygame.init()
screen = pygame.display.set_mode((800, 600))
is_running = True
title = "Diamond Protekt"
background = pygame.image.load('images/background.png')
pygame.display.set_caption(title)
icon = pygame.image.load("images/space-invaders.png")
pygame.display.set_icon(icon)
# Load and play music
music = ["music/music.mp3", "music/music2.mp3", "music/music3.mp3"]
mixer.music.load(random.choice(music))
mixer.music.play(-1)

# Player
player_img = pygame.image.load("images/player.png")
player_x = 370
player_y = 480
player_x_change = 0
player_y_change = 0

# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemy_number = 0

difficulty = "medium"

# Use enemy_number to control what difficulty does
if difficulty == "easy":
    enemy_number = 3
elif difficulty == "medium":
    enemy_number = 6
elif difficulty == "hard":
    enemy_number = 9
else:
    raise DifficultyError("Incorrect Difficulty")
for i in range(enemy_number):
    enemy_img.append(pygame.image.load('images/enemy.png'))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(5)
    enemy_y_change.append(40)

# Bullet
bulletImg = pygame.image.load('images/bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

diamond_img = pygame.image.load('images/diamond.png')
diamond_x = 370
diamond_y = 480


def diamond(x, y):
    screen.blit(diamond_img, (x, y))


score_value = 0
text = pygame.font.Font('fonts/Azonix.otf', 32)
text_x = 10
text_y = 10

color = 255

time_text = pygame.font.Font("fonts/Capture it.ttf", 32)
comment = "Keep Going! You got this!!"
comment_x = 380
comment_y = 10

game_over_font = pygame.font.Font('fonts/Positive System.otf', 100)


def comment_def(x, y):
    write = time_text.render(comment, True, (255, color, color))
    screen.blit(write, (x, y))


# Show the score
def show_score(x, y):
    if game_state == "play":
        score = text.render(f"Score: {str(score_value)}", True, (255, 255, 255))
        screen.blit(score, (x, y))
    elif game_state == "over":
        score = text.render(f"Score: {str(score_value)}", True, (255, 255, 255))
        screen.blit(score, (x, y))


# Show the GAME OVER text
def game_over_text():
    over_text = game_over_font.render(f"GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (110, 250))


# Draw The Enemy
def enemy(x, y, e):
    screen.blit(enemy_img[e], (x, y))


# Draw The Player
def player(x, y):
    screen.blit(player_img, (x, y))


# Fire The Bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Detect Collisions
def collision(bullet_xcor, bullet_ycor, enemy_xcor, enemy_ycor):
    dist = math.sqrt(math.pow(enemy_xcor - bullet_xcor, 2) + (math.pow(enemy_ycor - bullet_ycor, 2)))
    if dist < 27:
        return True
    else:
        return False


# Game Loop
while is_running:
    screen.blit(background, (0, 0))
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_UP:
                player_y_change += -5
            if event.key == pygame.K_DOWN:
                player_y_change += 5
            if game_state == "play":
                if event.key == pygame.K_o:
                    player_x = 370
                    player_y = 480
            if game_state == "over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        exit()
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('sounds/laser.wav')
                    bullet_sound.play()
                    fire_bullet(player_x, bullet_y)
                    bullet_x = player_x
                    bullet_y = player_y

                fire_bullet(player_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player_x_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_y_change = 0

    # Player Movement
    player_x += player_x_change
    player_y += player_y_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    if player_y <= 0:
        player_y = 0
    elif player_y >= 536:
        player_y = 536
    # Enemy Movement
    for i in range(enemy_number):
        if enemy_y[i] > 440:
            for h in range(enemy_number):
                enemy_y[h] = 2000
            game_over_text()
            game_state = "over"

            comment = "       You Snooze, You Lose!"
            score_value = "Dead!"
            break
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 5
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -5
            enemy_y[i] += enemy_y_change[i]
        # Use the collision function to detect a collision
        detect = collision(bullet_x, bullet_y, enemy_x[i], enemy_y[i])
        if detect:
            collide_sound = mixer.Sound('sounds/explosion.wav')
            collide_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1

            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
        bullet_x -= bullet_x_change

        # Score and other stuff
    if game_state == "play":
        diamond(diamond_x, diamond_y)
    if game_state == "over":
        color = 0
    comment_def(comment_x, comment_y)
    show_score(text_x, text_y)
    player(player_x, player_y)
    pygame.display.update()
pygame.quit()
