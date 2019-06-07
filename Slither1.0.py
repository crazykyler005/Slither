import pygame
import time
import random
pygame.init()

FPS = 15

white = (255,255,255)
black = (0,0,0)
red = [255,0,0]
green = [0,0,0]

displaySize = (800,600)
gameDisplay = pygame.display.set_mode((displaySize))
pygame.display.set_caption('Slither')
pygame.display.update()

movement_speed = 10
snakeSize = 10
snake_position_x = displaySize[0]/2
snake_position_y = displaySize[1]/2
appleSize = 10

clock = pygame.time.Clock()

font = pygame.font.SysFont(None,25)

def randomColor(color):
    allowed_values = [0,1,2]
    #To avoid background looking like the snake or apple
    allowed_values.remove(random.randrange(0,3))
    color = [0,0,0]
    for rgb in allowed_values:
        color[rgb] = random.randrange(0,256)
        print(color[rgb])
        print(rgb)
    return color

def message_to_screen(msg,color):
    screen_text = font.render(msg,True,color)
    gameDisplay.blit(screen_text, [displaySize[0]/2,displaySize[1]/2])

def snake(snakeSize, snakeList, snakeColor):
    for XnY in snakeList:
        pygame.draw.rect(gameDisplay, snakeColor, [XnY[0],XnY[1],snakeSize,snakeSize])

def gameLoop():

    snakeList = []
    snakeLenght = 1
    gameExit = False
    gameOver = False
    lead_x = displaySize[0]/2
    lead_y = displaySize[1]/2
    lead_x_change = 0
    lead_y_change = 0 
    randAppleX = random.randrange(0,displaySize[0] - appleSize,10)
    randAppleY = random.randrange(0,displaySize[1] - appleSize,10)
    appleColor = red
    snakeColor = black

    while not gameExit:
        while gameOver == True:
            pygame.event.clear() #removes all key events from queue
            gameDisplay.fill(white)
            message_to_screen("Game over, press Q/ESC to quit or c/space to continue",red)
            pygame.display.update()   

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
                        gameExit = True
                        gameOver = False
                    if (event.key == pygame.K_c) or (event.key == pygame.K_SPACE):
                        gameLoop()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                gameOver = False
            if event.type == pygame.KEYDOWN: #when key is pressed
                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_a): #left arrow
                    lead_x_change = -movement_speed
                    lead_y_change = 0
                elif (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d): #right arrow
                    lead_x_change = movement_speed
                    lead_y_change = 0
                elif (event.key == pygame.K_UP) or (event.key == pygame.K_w): #left arrow
                    lead_y_change = -movement_speed
                    lead_x_change = 0
                elif (event.key == pygame.K_DOWN) or (event.key == pygame.K_s): #right arrow
                    lead_y_change = movement_speed
                    lead_x_change = 0

        if (lead_x == randAppleX) and (lead_y == randAppleY): #if apple and snake overlap each other
            randAppleX = random.randrange(0,displaySize[0] - appleSize,10)
            randAppleY = random.randrange(0,displaySize[1] - appleSize,10)
            snakeLenght += 1
            snakeColor = [appleColor[0],appleColor[1],appleColor[2]]
            appleColor = randomColor(appleColor)

            while (lead_x == randAppleX) and (lead_y == randAppleY): #if they spawn on each other
                randAppleX = random.randrange(0,displaySize[0] - appleSize,10)
                randAppleY = random.randrange(0,displaySize[1] - appleSize,10)

        lead_x += lead_x_change #continual direction movement for x direction pressed
        lead_y += lead_y_change #For y direction pressed


        if lead_x <= 0 or lead_x >= displaySize[0] or lead_y <= 0 or lead_y >= displaySize[1]:
            gameOver = True

        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, appleColor, [randAppleX,randAppleY,appleSize,appleSize])

        snakeHead = []
        snakeHead.append(lead_x) #append add 1 item to the list
        snakeHead.append(lead_y)
        #moving x&y elements onto snakeList while removing values in lead_x&y
        if len(snakeList) > snakeLenght:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
        snakeList.append(snakeHead)

        snake(10,snakeList,snakeColor)

        pygame.display.update()

        clock.tick(FPS) #frames per second

    pygame.quit()
    quit()
gameLoop()