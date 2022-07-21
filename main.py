# import modules
import pygame
import random
import math

# initalize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))
title = pygame.display.set_caption("Star Battle")
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

# player
player_image = pygame.image.load('images/spaceship.png')
playerX = 370
playerY = 480
change_playerX = 0

def player(x, y):
    screen.blit(player_image, (x, y))

# enemy
enemy_image = []
enemyX = []
enemyY = []
change_enemyX = []
change_enemyY = []
num_enemies = 15

for x in range(num_enemies):
    enemy_image.append(pygame.image.load('images/enemy.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(0, 150))
    change_enemyX.append(0.5)
    change_enemyY.append(40)

def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))

# laser
laser_image = pygame.image.load('images/laser.png')
laserX = 0
laserY = 480
change_laserY = 2
# ready - ready to be fired
# fire - laser is moving
laser_state = "ready"

def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laser_image, (x + 25, y + 10))
 
def collision(enemyX, enemyY, laserX, laserY):
    # distance formula
    dist = math.sqrt(math.pow((enemyX - laserX), 2)) + (math.pow((enemyY - laserY), 2))
    if dist < 27:
        return True
    else:
        return False

# game loop
run = True
score_value = 0
font = pygame.font.Font('font.otf', 32)
textX = 10
textY = 10

game_over_font = pygame.font.Font('font.otf', 64)

def game_over():
    global game_over_font
    text = game_over_font.render("GAME OVER!", True, (0, 0, 0))
    screen.blit(text, (200, 250))

def score(x, y):
    score = font.render("Score: " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))

isOver = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # when key is pressed
        if event.type == pygame.KEYDOWN:
            # x value changes
            if event.key == pygame.K_LEFT:
                change_playerX = -0.3
            if event.key == pygame.K_RIGHT:
                change_playerX = 0.3
            if event.key == pygame.K_SPACE:
                # makes sure that there isn't a bullet already being fired
                if laser_state == "ready":
                    # gets one instance of x-coordinate
                    laserX = playerX
                    fire_laser(laserX, laserY)
        # when key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                change_playerX = 0 
 
    screen.fill((61, 183, 228))

    playerX += change_playerX

    if playerX <= 0:
        playerX = 0
    if playerX >= 740:
        playerX = 740

    for i in range(num_enemies):

        if enemyY[i] >= playerY:
            for x in range(num_enemies):
                change_enemyY[x] == 2000
                game_over()
                isOver = True
                break

        enemyX[i] += change_enemyX[i]

        if enemyX[i] <= 0:
            change_enemyX[i] = 0.4
            enemyY[i] += change_enemyY[i]
        if enemyX[i] >= 740:
            change_enemyX[i] = -0.4
            enemyY[i] += change_enemyY[i]
        
        # collision
        is_collision = collision(enemyX[i], enemyY[i], laserX, laserY)

        if isOver == False:
            if is_collision == True:
                laserX = 480
                laser_state = "ready"
                score_value = score_value + 1
                enemyX[i] = random.randint(1, 739)
                enemyY[i] = random.randint(50, 150)
        
        enemy(enemyX[i], enemyY[i], i)

    # laser reload
    if laserY <= 0:
        laserY = 480
        laser_state = "ready"
    if laser_state == "fire":
        fire_laser(laserX, laserY)
        laserY -= change_laserY
        
    player(playerX, playerY)
    score(textX, textY)
    pygame.display.update()

