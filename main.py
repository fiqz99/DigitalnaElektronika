import pygame
import random
import time
from copy import deepcopy
import pyrandint

pygame.init()
#--Pocetne konstante
white = (255, 255, 255)
black = (0, 0, 0)
green = (34, 139, 34)
blue = (64, 224, 208)
selected_option = 0.30
arrowImg = pygame.image.load('arrow.png')
ABOUT_MESSAGE = ["Projekat iz Digitalne Elektronike", "Autor: Filip Stefanović,", "student treće godine smera RTSI"]
screen = pygame.display.set_mode((800, 600))
running = True
gameState = "menu" #pocetno stanje, imamo jos stanja "playing", "about" i "game over"
clock = pygame.time.Clock()
img = pygame.image.load('bird.png')
backgroundImg = pygame.image.load('background.png')
backgroundImg2 = pygame.image.load('mainmenubg.jpg')
profilePhoto = pygame.image.load('photo.png')
#-
x = 150
y = 200
moveY = 0

blockX = 800
blockY = 0

blockWidth = 50
blockHeight = random.randint(0, 300)
gap = img.get_size()[1] * 5

# speed of blocks
blockMove = 5

score = 0
game_over = False
#---------------Ispisivanje teksta-------------------------------------------------------------------------------
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
def message_display(game_display, text, x, y, font_size, color, centered_x=False, centered_y=False):
    font = pygame.font.Font(None,font_size)
    TextSurf, TextRect = text_objects(text, font, color)
    if centered_x and centered_y:
        TextRect.center = ((400),(300))
    elif centered_x:
        TextRect.center = ((400),y)
    elif centered_y:
        TextRect.center = (x,(300))
    else:
        TextRect.center = (x,y)
    game_display.blit(TextSurf, TextRect)
#---------------------Definicije-----------------------------------------------------------------------
def showScore(currentScore):
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render('Score:' + str(currentScore), True, white)
    screen.blit(text, [3, 3])

def blocks (blockX, blockY, blockWidth, blockHeight, gap):
    pygame.draw.rect(screen, green, [blockX,blockY,blockWidth,blockHeight])
    pygame.draw.rect(screen,green, [blockX,blockY + blockHeight + gap,blockWidth,600])

def makeTextObjects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def bird(x, y, image):
    screen.blit(image, (x, y))

#-------Glavna petlja---------------------
while running:
    screen.fill((0, 0, 0))


    # Klikom na X menja stanje i izlazi iz loop-a
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if gameState == 'playing' or gameState == 'game over' or gameState == 'about':
                    gameState = 'menu'
            elif gameState == "menu":  # ----------------Menu Events-------------
                if event.key == pygame.K_DOWN:
                    if selected_option < 0.45:
                        selected_option += 0.10
                    else:
                        selected_option = 0.30
                elif event.key == pygame.K_UP:
                    if selected_option > 0.35:
                        selected_option -= 0.10
                    else:
                        selected_option = 0.50
                elif event.key == pygame.K_RETURN:
                    if selected_option < 0.35:
                        # reinit()
                        gameState = 'playing'
                    elif selected_option == 0.40:
                        gameState = 'about'
                    elif selected_option == 0.50:
                        running = False
            elif gameState == "playing":
                if event.key == pygame.K_SPACE:
                    moveY = -5
            elif gameState == "game over":
                if event.key == pygame.K_SPACE:
                    gameState = 'playing'
        if event.type == pygame.KEYUP:
            if gameState == "playing":
                if event.key == pygame.K_SPACE:
                    moveY = 5




                    #MENI
    if gameState=="menu":
        bird(0, 0, backgroundImg2)
        screen.blit(arrowImg, (800/4 + 43, 600/8 + 600*selected_option - 33))
        if pygame.font:
            # menu title
            message_display(screen, "Flappy bird", 0, 75 + round(600 * 0.15), 60, white,True)
            # menu items
            message_display(screen, "Play", 0, 75 + round(600 * 0.30), 50, white, True)
            message_display(screen, "About", 0, 75 + round(600 * 0.40), 50, white, True)
            message_display(screen, "Quit", 0, 75 + round(600 * 0.50), 50, white, True)

    elif gameState == 'about':
        bird(50, 90, profilePhoto)
        if pygame.font:
            for line in ABOUT_MESSAGE:
                message_display(screen, line, 520, 200 + ABOUT_MESSAGE.index(line) * 35, 30, white)
            message_display(screen, "Press ESC to return to menu!", 0, 500, 40, white, True)

    if gameState == "playing":

        y = y+moveY
        #screen.fill(blue)
        bird(0, 0, backgroundImg)
        bird(x, y, img)
        showScore(score)

        #nivoi u zavisnosti od skora
        if score >= 10 and score <20:
            blockMove = 6
            gap = img.get_size()[1] * 3.3
        if score >= 20 and score <30:
            blockMove = 7
            gap = img.get_size()[1] * 3.1
        if score >= 30 and score <40:
            blockMove = 8
            gap = img.get_size()[1] * 3.3
        if score >= 40:
            blockMove = 8
            gap = img.get_size()[1] * 2.5

        blocks(blockX, blockY, blockWidth, blockHeight, gap)
        blockX -= blockMove

        if y> 600 - img.get_size()[1] or y<0:
            gameState = "game over"

        if blockX < (-1* blockWidth):
            blockX = 800
            blockHeight = random.randint(0, 300)

        #detekcija sudara
        if x+img.get_size()[0] > blockX and x< blockX + blockWidth:
            if y<blockHeight or y + img.get_size()[1]> blockHeight + gap:
                gameState = "game over"

        if x>blockX + blockWidth and x< blockX+ blockWidth + img.get_size()[0]/5:
            score +=1

    if gameState == 'game over':
        x = 150
        y = 200
        moveY = 0
        blockX = 800
        blockY = 0
        blockWidth = 50
        blockHeight = random.randint(0, 300)
        gap = img.get_size()[1] * 5
        blockMove = 5
        score = 0
        game_over = False
        message_display(screen, "Press SPACE to try again, or ESC to return to menu!", 0, 300, 40, white, True)


    pygame.display.update()
    clock.tick(80)

pygame.quit()
quit()