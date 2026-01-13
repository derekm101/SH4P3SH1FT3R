import pygame
import math
import random
import os
from sys import exit #terminates program

#Setting Window
winWidth = 626
winHeight = 417
mapBorder = 65
pygame.init()
window = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("SH4P3SH1FT3R")
pygame.font.init()
game_font = pygame.font.SysFont("Ariel", 50)

#FPS and Timers
clock = pygame.time.Clock()
FPS = 60
abilityTimer = 0
enemyTimer = 0
invTimer = 0
enInvTimer = 0
timer = 0
time = 0
score = 0
gameStarted = True
countmsg = 0
eCountmsg = 0

#player_properties
playerShapes = ["squareplayer.png", "circleplayer.png"]
playerShapesIndex = 0
playerX = winWidth/4.0
playerY = winHeight/2.0
playerW = 60
playerH = 52
#enemy_properties
enemies = []
enemyImages = ["bat.png", "blob.png", "critter.png", "opposum.png", "rat.png", "snake.png", "spider.png"]
enemyImageIndex = 0
enemyX = winWidth/1.25
enemyY = winHeight/2
enemyW = None
enemyH = None
#images
def load_image(image_name, scale=None):
    image = pygame.image.load(os.path.join("images", image_name))
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    return image
bg_image = load_image("sewer_background.png")
bg_x = 0
bg_y = 0
bg_speed = 8
icon1 = pygame.image.load("images/squareplayer.png")
player_image = load_image(playerShapes[playerShapesIndex])
enemy_image = load_image(enemyImages[enemyImageIndex])
pygame.display.set_icon(icon1)

def load_sprite_sheet(sheetname, width, height):
    sheet = pygame.image.load(sheetname).convert_alpha()
    sprites = []
    for i in range(sheet.get_width()//width):
        rect = pygame.Rect(i * width, 0, width, height)
        sprites.append(sheet.subsurface(rect))
    return sprites

class Player(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self, playerX, playerY, playerW, playerH)
        self.position = winHeight/1.19
        self.jump = 0
        self.shape = "square" #default
        self.maxhealth = 30
        self.health = self.maxhealth
        self.invincible = False
        self.frames = load_sprite_sheet("images/pixilart-sprite.png", 100, 100)
        self.current_frame = 0
        self.animation_speed = 0.2
        self.frame_timer = 0
        if self.shape == "circle":
            self.image = self.frames[self.current_frame]
        else:
            self.image = player_image
        #physics
        self.velX = 0
        self.velY = 0
        self.gravity = 0.4
        self.applyG = True
        self.falling = None
        self.inertia = None
        self.direction = None

        #classes
        class Square():
            def __init__(self):
                self.shape = "square"
                self.attackDmg = 15
                self.kbDist = 10
                self.dash = 0
                self.speed = 3
                self.jumpHeight = -6.5
                Player.maxhealth = 30
                Player.health = Player.maxhealth

        class Circle():
            def __init__(self):
                self.shape = "circle"
                self.attackDmg = 12
                self.kbDist = 7
                self.speed = 3.5
                self.jumpHeight = -7
                Player.maxhealth = 20
                Player.health = Player.maxhealth
                #Specalties
                self.charge = 0
                self.isCharging = False
        
        self.square = Square()
        self.circle = Circle()

class Enemy(pygame.Rect):
    def __init__(self):
        #Calling Global Variables
        global enemyImageIndex, enemyW, enemyH
        #Setting Values
        enemyW = None
        enemyH = None
        self.attackDmg = None
        self.kb = None
        self.speed = None
        self.jumpHeight = None
        self.type = enemyImageIndex
        self.score = 0
        self.health = 0
        self.invincible = False
        #Individual Values
        if self.type == 0:#bat
            enemyW = 49
            enemyH = 51
            self.name = enemyImages[self.type].split(".")[0]
            self.attackDmg = 6
            self.kb = None
            self.speed = 4
            self.jumpHeight = -6
            self.score = 20
            self.health = 20
        elif self.type == 1:#blob; boss?
            enemyW = 56
            enemyH = 32
            self.name = enemyImages[self.type].split(".")[0]
            self.attackDmg = 2
            self.kb = None
            self.speed = 2
            self.jumpHeight = -2
            self.score = 5
            self.health = 10
        elif self.type == 2:#critter
            enemyW = 34
            enemyH = 25
            self.name = enemyImages[self.type].split(".")[0]
            self.attackDmg = 3
            self.kb = None
            self.speed = 4
            self.jumpHeight = -4
            self.score = 10
            self.health = 10
        elif self.type == 3:#opposum; miniboss?
            enemyW = 70
            enemyH = 58
            self.name = enemyImages[self.type].split(".")[0]
            self.attackDmg = 12
            self.kb = None
            self.speed = 3
            self.jumpHeight = -3
            self.score = 25
            self.health = 60
        elif self.type == 4:#rat
            enemyW = 39
            enemyH = 41
            self.name = enemyImages[self.type].split(".")[0]
            self.attackDmg = 5
            self.kb = None
            self.speed = 5
            self.jumpHeight = -4
            self.score = 15
            self.health = 30
        elif self.type == 5:#snake; miniboss?
            enemyW = 61
            enemyH = 28
            self.name = enemyImages[self.type].split(".")[0]
            self.attackDmg = 15
            self.kb = None
            self.speed = 7
            self.jumpHeight = -3
            self.score = 30
            self.health = 50
        elif self.type == 6:#spider; miniboss?
            enemyW = 78
            enemyH = 42
            self.name = enemyImages[self.type].split(".")[0]
            self.attackDmg = 10
            self.kb = None
            self.speed = 5
            self.jumpHeight = -7
            self.score = 25
            self.health = 40
        #Initializing Image
        pygame.Rect.__init__(self, enemyX, enemyY, enemyW, enemyH)
        self.image = load_image(enemyImages[self.type])
        self.position = winHeight/1.19
        #Physics
        self.velX = 0
        self.velY = 0
        self.gravity = 0.4
        self.applyG = True
        self.falling = None
        self.inertia = 0.1
        self.direction = None

player = Player()
square = player.square
circle = player.circle
enemy = Enemy()

def animate_player():
    if player.shape == "circle":
        if player.velX != 0 or player.velY != 0:
            player.frame_timer += player.animation_speed
            if player.frame_timer >= 1:
                player.frame_timer = 0
                player.current_frame = (player.current_frame + 1) % len(player.frames)
                player.image = player.frames[player.current_frame]
        elif player.velX == 0 and player.velY == 0:
            player.image = player.frames[0]
        elif player.falling:
            player.image = player.frames[2]
    elif player.shape == "square":
        player.image = player_image


def draw():
    window.blit(bg_image, (bg_x, bg_y))
    window.blit(bg_image, ((bg_x + winWidth) - bg_speed, bg_y))
    window.blit(bg_image, ((bg_x - winWidth) + bg_speed, bg_y))

    if gameStarted:
        for e in enemies:
            window.blit(e.image, e)

        if player.shape == "circle":
            window.blit(player.image, (player.x, player.y - 20))
        else:
            window.blit(player.image, player)
        pygame.draw.rect(window, "red", (15, 395, 10*player.maxhealth, 10))
        pygame.draw.rect(window, "green", (15, 395, 10*player.health, 10))

        #timer and score
        text_time = "Time: " + str((timer - time)//1000)
        text_surface = game_font.render(text_time, False, "white")
        window.blit(text_surface, (450, 380))   
    else:
        window.fill("#334B2F")
        text_ask = "Press 'SHIFT' To Start..."
        text_score = "Total Score: " + str(score)
        text_ftime = "Time Survived: " + str((timer - time)//1000)
        text_surface = game_font.render(text_ask, False, "white")
        text_surface2 = game_font.render(text_score, False, "black")
        text_surface3 = game_font.render(text_ftime, False, "black")
        window.blit(text_surface, (winWidth/5.5, winHeight/5.5))
        window.blit(text_surface2, (winWidth/5.5, 250))
        window.blit(text_surface3, (winWidth/5.5, 350))



def playerMovement(e):
    global invTimer, countmsg
    #--Player Movements (PM)--
    keys = pygame.key.get_pressed()
    if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_UP or e.key == pygame.K_SPACE or e.key == pygame.K_w:
            if player.shape == "square" and player.jump < 1:
                player.velY = square.jumpHeight
                player.jump += 1
            elif player.shape == "circle" and player.jump < 1:
                player.velY = circle.jumpHeight
                player.jump += 1
        elif e.key == pygame.K_s or e.key == pygame.K_DOWN:
            if player.shape == "square":
                player.velX = 0
                player.velY += 4
                player.invincible = True
                print("Player is now INVINCIBLE!")
                invTimer = (pygame.time.get_ticks() + 750)
                countmsg = 0

    #Square
    if player.shape == "square":
        # if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and (player.jump < 1):
        #     player.velY = square.jumpHeight
        #     player.jump += 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.velX = -square.speed
            player.direction = "right"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.velX = square.speed
            player.direction = "left"
    #Circle
    if player.shape == "circle" and not circle.isCharging:
        # if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and (player.jump < 1):
        #     player.velY = circle.jumpHeight
        #     player.jump += 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.velX = -circle.speed
            player.direction = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.velX = circle.speed
            player.direction = "right"

def enemyMovement():
    global mapBorder, enInvTimer, eCountmsg
    for e in enemies:
        #AI
        moveChance = random.randint(1, 5)
        invChance = random.randint(1,10)
        if e.type == 0:
            e.velY = e.jumpHeight
            if moveChance == 1:
                lungeChance = random.randint(1, 3)
                if lungeChance == 1:
                    e.velX = -e.speed
                    e.direction = "left"
                    e.velY = e.jumpHeight
                elif lungeChance == 2:
                    e.velX = e.speed
                    e.direction = "right"
                    e.velY = e.jumpHeight
                elif lungeChance == 3:
                    e.velY = e.jumpHeight
            elif (moveChance == 2 or moveChance == 3) and e.x > 0:
                e.velX = -e.speed
                e.direction = "left"
            elif (moveChance == 4 or moveChance == 5) and e.x < 500:
                e.velX = e.speed
                e.direction = "right"
        else:
            if moveChance == 1: 
                lungeChance2 = random.randint(1, 3)
                if lungeChance2 == 1:
                    e.velX = -e.speed
                    e.direction = "left"
                    e.velY = e.jumpHeight
                elif lungeChance2 == 2:
                    e.velX = e.speed
                    e.direction = "right"
                    e.velY = e.jumpHeight
                elif lungeChance2 == 3:
                    e.velY = e.jumpHeight
            elif (moveChance == 2 or moveChance == 3) and e.x > 0: 
                e.velX = -e.speed
                e.direction = "left"
            elif (moveChance == 4 or moveChance == 5) and e.x < 500: 
                e.velX = e.speed
                e.direction = "right"
        if invChance == 1:
            e.invincible = True
            enInvTimer = (pygame.time.get_ticks() + 500)
            eCountmsg = 0


def spawnEnemy():
    global enemyImageIndex, enemyX, enemyY
    spawnChance = random.randint(1, 8 + (5*len(enemies)))
    enemyImageIndex = random.randint(0, 6)
    enemyX = winWidth + (20*(random.randint(10, 50)))
    enemyY = winHeight / 1.5
    new_enemy = Enemy()
    if len(enemies) < 1:
        enemies.append(new_enemy)
    elif spawnChance == 1 and len(enemies) < 5:
        enemies.append(new_enemy)



def objectCollisions():
    player.y = max(player.y + player.velY, mapBorder)
    player.y = min(player.y - player.gravity, ((player.position) - player.height))
    if player.shape == "square":
        player.x = max(player.x + player.velX, 0.5)
        player.x = min(player.x + player.velX, (winWidth - player.width))
    elif player.shape == "circle":
        player.x = max(player.x + player.velX, - 15)
        player.x = min(player.x + player.velX, (winWidth - player.width - 15))

    if (player.x == (winWidth - player.width - 15) and player.shape == "circle") or (player.x <= (player.width/4) and player.shape == "circle"):
        player.jump = 0

    for e in enemies:
        e.y = max(e.y + e.velY, mapBorder)
        e.y = min(e.y - e.gravity, ((e.position) - e.height))
        e.x = max(e.x + e.velX, 0.5)
        e.x = min(e.x + e.velX, (winWidth - e.width))
        if e.applyG:
            e.velY += e.gravity
        if e.y != round(e.position - e.height):
            e.falling = True
        elif e.y == round(e.position - e.height):
            e.falling = False

def applyInertia():
    global bg_speed

    if player.shape == "square":
        player.inertia = 0.095
    elif player.shape == "circle":
        player.inertia = 0.085

    if player.velX != 0 and not player.falling:
        if player.velX < 0:
            player.velX = min(0, player.velX + player.inertia)
        elif player.velX > 0:
            player.velX = max(0, player.velX - player.inertia)

    for e in enemies:
        if e.velX != 0 and not e.falling:
            if e.velX < 0:
                e.velX = min(0, e.velX + e.inertia)
            elif e.velX > 0:
                e.velX = max(0, e.velX - e.inertia)    

    bg_speed = max(8, bg_speed - 1)

def poweringUp():
    if player.shape == "circle":
        player.applyG = False
        player.velY = 0
        player.velX = 0
        circle.charge += 0.1
    
def launch(amount):
    global invTimer, countmsg
    if player.direction == "right":
        player.velX += amount
        print("Player Launched")
    elif player.direction == "left":
        player.velX -= amount
        print("Player Launched")
    player.invincible = True
    print("Player is now INVINCIBLE!")
    countmsg = 0
    invTimer = (pygame.time.get_ticks() + 750)
    circle.charge = 0
    circle.isCharging = False
    player.applyG = True

def playerSpecialMoves(e):
    global player_image, playerShapes, playerShapesIndex, abilityTimer, invTimer, countmsg
    if e.type == pygame.KEYDOWN:
        #Changing Shape
        if e.key == pygame.K_f:
            if player.shape == "square":
                player.shape = "circle"
                playerShapesIndex = 1
            elif player.shape == "circle":
                player.shape = "square"
                playerShapesIndex = 0
                player_image = load_image(playerShapes[playerShapesIndex])
                player.image = player_image
        #Player Special Moves
        if e.key == pygame.K_r:
            if player.shape == "square" and square.dash < 1: #square
                    if player.direction == "right":
                        player.velX += -4
                        print("Player Dashed")
                    elif player.direction == "left":
                        player.velX += 4
                        print("Player Dashed")
                    square.dash += 1
                    abilityTimer = (pygame.time.get_ticks() + 1500)
                    player.invincible = True
                    print("Player is now INVINCIBLE!")
                    countmsg = 0
                    invTimer = (pygame.time.get_ticks() + 750)
            elif square.dash >= 1:
                print(timer)
                print(abilityTimer)
                print("Dash on Cooldown")
            if e.type == pygame.KEYDOWN and player.shape == "circle" and e.key == pygame.K_r: #circle
                circle.isCharging = True
                circle.charge += 3
                poweringUp()
    elif e.type == pygame.KEYUP: 
        if e.key == pygame.K_r:
            if player.shape == "circle":
                launch(circle.charge)
                circle.charge = 0
                circle.isCharging = False
                player.applyG = True

def moveScreen():
    global bg_x
    global bg_speed
    if player.velX > 0 and player.velX <= (bg_speed // 2):
        bg_x -= bg_speed//1.5
    elif player.velX < 0  and player.velX >= -(bg_speed // 2):
        bg_x -= bg_speed // 3
    elif player.velX == 0 and not circle.isCharging:
        bg_x -= bg_speed // 3
    elif player.velX == 0 and circle.isCharging:
        bg_x -= bg_speed // 3.25
    elif player.velX > bg_speed // 2:
        bg_x -= player.velX
    elif player.velX < bg_speed // 2:
        max(bg_x - player.velX//1.5, 10)
    if bg_x <= (8 - winWidth):
        bg_x = 0

def gameOver():
    global timer, time, enemies, gameStarted
    time += timer//1000
    gameStarted = False

while True:
    #End Screen
    while not gameStarted:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() #quits the window
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                gameStarted = True
                player.health = player.maxhealth
                enemies.clear()
                time = pygame.time.get_ticks()
                score = 0
                player.velX = 0
                player.velY = 0
                circle.charge = 0
                circle.isCharging = False
                player.applyG = True
                player.x = winWidth/4.0
                player.y = winHeight/2.0
        draw()
        pygame.display.update()

    #Main Game Code:
    if gameStarted:
        enemyTimer = pygame.USEREVENT + 1
        contactTimer = pygame.USEREVENT + 2
        pygame.time.set_timer(enemyTimer, 500)
        pygame.time.set_timer(contactTimer, 100)
    while gameStarted: #game loop to keep aplication running
        timer = pygame.time.get_ticks()
        #Event Checker
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() #quits the window
                exit()
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_DOWN):
                playerMovement(event)
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                playerSpecialMoves(event)
            elif event.type == enemyTimer:
                enemyMovement()
                spawnEnemy()
            elif event.type == contactTimer:
                for e in enemies:
                    if player.colliderect(e) and not player.invincible:
                        player.health = max(0, player.health - e.attackDmg)
                        if player.health == 0:
                            gameOver()
                    elif player.colliderect(e) and player.invincible and not e.invincible:
                        if player.shape == "square":
                            e.health = max(0, e.health - (square.attackDmg + player.velX/4))
                            print(f"{e.name} has {round(e.health, 2)} health points left! ")
                        elif player.shape == "circle":
                            e.health = max(0, e.health - (circle.attackDmg + player.velX/4))
                            print(f"{e.name} has {round(e.health, 2)} health points left! ")
                        if e.health <= 0:
                            print(f"{e.name} defeated! \n{e.score} points gained!")
                            score += e.score
                            enemies.remove(e)
                    elif player.colliderect(e) and player.invincible and e.invincible:
                        print(f"{e.name} blocked the attack!")
        #Additional
        if circle.isCharging:
            poweringUp()
        #Gravity
        if player.applyG:
            player.velY += player.gravity
        #Checks
        if player.y != round(player.position - player.height):
            player.falling = True
        elif player.y == round(player.position - player.height):
            player.falling = False
            player.jump = 0
        if abilityTimer <= timer and square.dash >= 1:
            square.dash = 0
            abilityTimer = 0
            print("Cooldown Finished")
        if invTimer <= timer and countmsg == 0:
            countmsg = 1
            invTimer = 0
            player.invincible = False
            print("!-Player is no longer invincible-!")
        if enInvTimer <= timer:
            enInvTimer = 0
            for e in enemies:
                e.invincible = False
        #Calling Functions
        objectCollisions()
        applyInertia()
        playerMovement(event)
        moveScreen()
        animate_player()
        draw()
        #test
        pygame.display.update() #"draws" elements
        clock.tick(FPS) #updates window x amount of times per second
