import pygame
import random
import math
from pygame import mixer

#initialize pygame
pygame.init()

#Create Screen
screen = pygame.display.set_mode((800,600))

#Create Background

background = pygame.image.load('spacebackground.jpg')

#Create Background Soun

mixer.music.load("badass.mp3")
mixer.music.play(-1)

#Title and Icon(Icon is from Flaticon.com)
pygame.display.set_caption("Cowboys In Space")
icon = pygame.image.load('gun.png')
pygame.display.set_icon(icon)

# Cowboy Player
playerImg = pygame.image.load('cowboy64.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy Player
#CREATING MULTIPLE ENEMIES
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 12
enemyX_changevar=10

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien64.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(15,150))
    enemyX_change.append(6)
    enemyY_change.append(40)

#Bullet
#Ready state means you cant see the bullet on the screen
#Fire - The bullet is fired.
bulletImg = pygame.image.load('bullet24.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 30
bullet_state = "ready"



#SCORE
hits = 0
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score: " + str(score_value),True, (0,0,255))
    screen.blit(score, (x, y))

over_font = pygame.font.Font('freesansbold.ttf', 64)

end_game = False
def game_over_text():
    over_text = over_font.render("GAME OVER" , True, (255, 255, 255))
    screen.blit(over_text, (200, 200))

#For drawing character
def player(x,y):
    screen.blit(playerImg, (x, y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x[i] , y[i]))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x + 16, y + 10))

#COLLISION DETECTION
#Use Distance Formula

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False

def player_dead(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2))
    if distance < 50:
        return True
    else:
        return False

#Game Loop
running = True
while running:

    # RGB Red Green Blue every color in the world is made up of these values 0-255
    screen.fill((50, 50, 50))

    #Add background after fill so that color doesnt go over
    screen.blit(background, (0,0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #if keystroke is pressed check whether its right of left.. MOVING CHARACTER
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change += -9
            if event.key == pygame.K_RIGHT:
                playerX_change += 9
            if event.key == pygame.K_UP:
                playerY_change += -9
            if event.key == pygame.K_DOWN:
                playerY_change += 9
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    #Get Current x-coordinate of spaceship
                    #bullet_Sound = mixer.Sound('cartoon-shot.wav')
                    #bullet_Sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX , bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0



    playerX += playerX_change
    playerY += playerY_change

# Setting Boundaries

    if playerX <= -30:
        playerX = -30
    # Screen pixels (800) - size of character (128)
    elif playerX >= 700:
        playerX = 700
    if playerY <= 5:
        playerY = 5
    elif playerY >= 535:
        playerY = 535


#ENemy Movement

    #MULTIPLE ENEMIES
    for i in range(num_of_enemies):

        # GAME OVER
        #player_die = isCollision(enemyX[i], enemyY[i], playerX, playerY)
        player_die = player_dead(enemyX[i], enemyY[i], playerX, playerY)
        if player_die:
            end_game = True
            for j in range(num_of_enemies):
                enemyY[j] = -5000
            #game_over_text()
            break


        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = enemyX_changevar #6
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 735:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = -enemyX_changevar #-6
        if enemyY[i] >= 735:
            enemyY[i] = random.randint(15, 150)





            # COLLISION CODE

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)


        if collision:
            bulletY = playerY
            bullet_state = "ready"
            hits += 1
            if hits % 2 == 0:
                score_value +=1
                bulletY = playerY
                bullet_state = "ready"
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(15, 150)
                #enemyX_changevar *=1.2
        enemy(enemyX, enemyY, i)



#Bullet Movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"



    # player() must be called after screen.fill


    player(playerX, playerY)
    show_score(textX,textY)
    if end_game:
        game_over_text()
    pygame.display.update()