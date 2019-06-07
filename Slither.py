import pygame
import time
import random
import simplejson as json

pygame.init()

#FPS = 12

white = (255,255,255)
black = (0,0,0)
red = [255,0,0]
green = [0,155,0]

displaySize = (800,600)
gameDisplay = pygame.display.set_mode((displaySize))
pygame.display.set_caption('Slither')

icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)

head_image = pygame.image.load('snake_head.png')
tail_image = pygame.image.load('snake_tail.png')
apple_image = pygame.image.load('apple.png')

pygame.display.update()

movement_speed = 20
snakeBlockSize = 20
snake_position_x = displaySize[0]/2
snake_position_y = displaySize[1]/2
appleSize = 30

clock = pygame.time.Clock()

font = pygame.font

file = open("verisonNumber.txt", "r")
verisonNumber = file.readline()
file.close()

def randomColor(color):
    allowed_values = [0,1,2]
    #To avoid background colors being too similar to the background
    allowed_values.remove(random.randrange(0, 3))
    color = [0,0,0]

    for rgb in allowed_values:
        color[rgb] = random.randrange(0, 256)
        #print(color[rgb])
        #print(rgb)
    return color

def text_objects(text,color,size):
    #you can either type in a number or string value to define a font size
    if size == "small":
        textSurface = font.SysFont("comicsansms",25).render(text, True, color)
    elif size == "med":
        textSurface = font.SysFont("comicsansms",50).render(text, True, color)
    elif size == "large":
        textSurface = font.SysFont("comicsansms",80).render(text, True, color)
    else: #custom size
        textSurface = font.SysFont("comicsansms",size).render(text, True, color)
    return textSurface,textSurface.get_rect()

def message_to_screen(msg,color,y_displace = 0,size=25, x_displace = 0):
    textSurface, textRect = text_objects(msg, color,size)
    textRect.center = (displaySize[0]/2 - x_displace),(displaySize[1]/2 - y_displace)
    gameDisplay.blit(textSurface, textRect)

def randAppleGen():
    randAppleX = random.randrange(0,displaySize[0] - appleSize,10)
    randAppleY = random.randrange(0,displaySize[1] - appleSize,10)
    return randAppleX,randAppleY

def pause():

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                elif (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)

        message_to_screen("Paused", black, -100, size="large")
        message_to_screen("Press p to continue or q/ESC to quit.", black, 25)
        pygame.display.update()
        clock.tick(5)
    

def gameIntro():

    intro = True

    while intro:

        gameDisplay.fill(white)
        message_to_screen("Welcome To Slither",green,220,"large")
        message_to_screen("The objective of the game is to eat red apples", black, 20)
        message_to_screen("The more apples you eat, the longer you get", black, -20)
        message_to_screen("If you go off the edges or run into yourself you lose", black, -60)
        message_to_screen("Press c/space to play, p to pause or q/ESC to quit", black, -200)
        message_to_screen("v"+verisonNumber,black,y_displace=-displaySize[1]/2+20, x_displace = -displaySize[0]/2+45)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    quit()
                if (event.key == pygame.K_c) or (event.key == pygame.K_SPACE):
                    intro = False

        pygame.display.update()
        clock.tick(15)

def grab_score():

    file_name = 'score.json'

    try:
        with open(file_name) as jFile:
            data = json.load(jFile)
    except FileNotFoundError:
        print("creating "+file_name)
        f = open(file_name, "w")
        data = {
            'high_score': 0
        }
        json.dump(data, f)
        f.close()
    except Exception:
        print("Something when wrong when opening "+file_name)
        f = open(file_name, "w")
        data = {
            'high_score': 0
        }
        json.dump(data, f)
        f.close()
    return data

def snake(snakeSize, snakeList, snakeColor, direction,tail_angle):
    head = pygame.transform.rotate(head_image,direction)
    tail = pygame.transform.rotate(tail_image,tail_angle)
    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))

    if len(snakeList) > 1:
        gameDisplay.blit(tail, (snakeList[0][0],snakeList[0][1]))
    for XnY in snakeList [1:-1]:
        pygame.draw.rect(gameDisplay, snakeColor, [XnY[0],XnY[1],snakeSize,snakeSize])

def gameLoop():
    snakeList = []
    snakeLength = 1
    gameExit = False
    gameOver = False
    lead_x = displaySize[0]/2
    lead_y = displaySize[1]/2
    lead_x_change = 20
    lead_y_change = 0 
    grid_x = 0 
    grid_y = 0
    
    randAppleX, randAppleY = randAppleGen()

    snakeColor = green
    new_angle = 270
    current_angle = new_angle
    score = 0
    jsonData = grab_score()
    high_score = jsonData['high_score']
    scoreColor = black
    gridColor = black
    gridSwitch = True

    tail_angles = [270]
    changeInX = lead_x
    changeInY = lead_y
    scoreTextSize = 25
    setPace = 5
    FPS = 10

    while not gameExit:
        if gameOver is True:
            # make sure score is only saved once while in game over screen
            if score > high_score:
                jsonData['high_score'] = score
                with open('score.json', 'w') as f:
                    json.dump(jsonData, f)

            while gameOver is True:
                pygame.event.clear() #removes all key events from queue
                gameDisplay.fill(white)
                message_to_screen("Game over", red, 50, "med")
                message_to_screen("Press q/ESC to quit or c/space to continue", black, -20)
                if score > high_score:
                    message_to_screen("New high-score: " + str(score), black, -60)
                else:
                    message_to_screen("Score: " + str(score), black, -60)
                    message_to_screen("High Score: "+str(high_score), black, -90)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameExit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
                            gameExit = True
                            gameOver = False
                        if (event.key == pygame.K_c) or (event.key == pygame.K_SPACE):
                            gameLoop()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN: #when key is pressed
                if ((event.key == pygame.K_LEFT) or (event.key == pygame.K_a)) and (current_angle != 270): #left
                    lead_x_change = -movement_speed
                    lead_y_change = 0
                    new_angle = 90

                elif ((event.key == pygame.K_RIGHT) or (event.key == pygame.K_d)) and (current_angle != 90): #right
                    lead_x_change = movement_speed
                    lead_y_change = 0
                    new_angle = 270

                elif ((event.key == pygame.K_UP) or (event.key == pygame.K_w)) and (current_angle != 180): #up
                    lead_y_change = -movement_speed
                    lead_x_change = 0
                    new_angle = 0

                elif ((event.key == pygame.K_DOWN) or (event.key == pygame.K_s)) and (current_angle != 0): #down
                    lead_y_change = movement_speed
                    lead_x_change = 0
                    new_angle = 180

                elif event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_g:
                    if gridSwitch is True:
                        gridSwitch = False
                        print("to false")
                    elif gridSwitch is False:
                        gridSwitch = True
                        print("to true")

        #if apple and snake head overlap each other
        if (lead_x > randAppleX and lead_x < randAppleX+appleSize) or (lead_x + snakeBlockSize > randAppleX and lead_x + snakeBlockSize < randAppleX + appleSize):
            if (lead_y > randAppleY and lead_y < randAppleY+appleSize) or (lead_y + snakeBlockSize > randAppleY and lead_y + snakeBlockSize < randAppleY + appleSize):
                randAppleX,randAppleY = randAppleGen()
                score += 1
                scoreColor = randomColor(scoreColor)
                gridColor = scoreColor
                if high_score <= score:
                    scoreTextSize = 60
                if snakeLength == 0:
                    tail_angles.append(new_angle)
                        
                snakeLength += 1

                # if they spawn on each other
                while (lead_x > randAppleX and lead_x < randAppleX+appleSize) or (lead_x + snakeBlockSize > randAppleX and lead_x + snakeBlockSize < randAppleX + appleSize) and (lead_y > randAppleY and lead_y < randAppleY+appleSize) or (lead_y + snakeBlockSize > randAppleY and lead_y + snakeBlockSize < randAppleY + appleSize):
                        randAppleX,randAppleY = randAppleGen()

        lead_x += lead_x_change #continual direction movement for x direction pressed
        lead_y += lead_y_change #For y direction pressed

        #if snake goes out of bounds
        if lead_x < 0 or lead_x >= displaySize[0] or lead_y < 0 or lead_y >= displaySize[1]:
            gameOver = True

        snakeHead = []
        snakeHead.append(lead_x) #append add 1 item to the list
        snakeHead.append(lead_y)

        # since event listeners can change new_angle multiple times before 1 frame finishes,
        # it's better to append the tail_angle outside of the event listener
        if snakeLength > 0 and new_angle != current_angle:
            if new_angle == 90 and new_angle != 270:
                tail_angles.append(90)
            if new_angle == 180 and new_angle != 0:
                tail_angles.append(180)
            if new_angle == 0 and new_angle != 180:
                tail_angles.append(0)
            if new_angle == 270 and new_angle != 90:
                tail_angles.append(270)

        #moving x&y elements onto snakeList while removing values in lead_x&y
        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
        snakeList.append(snakeHead)
        
        #if a tail exisits
        if len(snakeList) > 1:
            #if the tail ends x and y values change then the direction in which the tail end is going changes
            if changeInX != snakeList[1][0] and changeInY != snakeList[1][1]:#and len(snakeList)>2
            
                #delete last angle used
                del tail_angles[0]
                changeInX = snakeList[0][0]
                changeInY = snakeList[0][1]

        gameDisplay.fill(white)

        # logic for drawing the grid lines
        if gridSwitch is True:
            
            while grid_y != displaySize[0]:  # drawing vertical lines
                pygame.draw.rect(gameDisplay, gridColor, [grid_y-1, 0, 3, displaySize[1]])

                s = pygame.Surface((3,displaySize[1]))  # the size of your rect
                s.set_alpha(225)                # alpha level
                s.fill((255,255,255))           # this fills the entire surface
                gameDisplay.blit(s, (grid_y-1,0))    # (0,80) are the top-left coordinates

                grid_y += snakeBlockSize

                while grid_x != displaySize[1]:  # drawing horizontal lines
                    pygame.draw.rect(gameDisplay, gridColor, [0, grid_x-1, displaySize[0], 3])

                    s = pygame.Surface((displaySize[0], 3))  # the size of your rect
                    s.set_alpha(225)                # alpha level
                    s.fill((255, 255, 255))           # this fills the entire surface
                    gameDisplay.blit(s, (0, grid_x-1))    # (0,80) are the top-left coordinates

                    grid_x += snakeBlockSize

        grid_x = 0
        grid_y = 0

        gameDisplay.blit(apple_image, (randAppleX, randAppleY))

        snake(snakeBlockSize, snakeList, snakeColor, new_angle, tail_angles[0])
        message_to_screen("Score:", black, y_displace=280, x_displace=displaySize[1]/2+40, size="small")
        message_to_screen(str(score), scoreColor, y_displace=280, x_displace = 282, size = scoreTextSize)
        if gridSwitch is True:
            message_to_screen("Toggle Grid off (g)", black, y_displace=280, x_displace=-displaySize[1]/2+20, size="small")
        if gridSwitch is False:
            message_to_screen("Toggle Grid on (g)", black, y_displace=280, x_displace=-displaySize[1]/2+10, size="small")
        
        if scoreTextSize > 25:
            scoreTextSize -= 3
        else:
            scoreColor = black
        pygame.display.update()
        if snakeLength == setPace:
            setPace += 11
            FPS += 1.5

        current_angle = new_angle

        clock.tick(FPS) #frames per second/game pace

    pygame.quit()
    quit()

gameIntro()
gameLoop()