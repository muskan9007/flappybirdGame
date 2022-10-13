import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports

# Global Variables for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = int(SCREENHEIGHT * 0.8)
GAME_SPRITES = {}
GAME_SOUNDS = {}

PLAYER = 'sprites/bird.png'
BACKGROUND = 'sprites/background.png'
PIPE = 'sprites/pipe.png'
fullfinalscore = []
SCORE = 0
FINALSCORE = [0]
# HIGHSCORE = max(FINALSCORE)
def welcomeScreen():
    """
    Shows welcome images on the screen
    """

    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    finalscore = []
    # highscore = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    newpipe1 = getRandomPipe()
    newpipe2 = getRandomPipe()
    # my list of upper pipes
    upperpipes = [{'x': SCREENWIDTH+200, 'y': newpipe1[0]['y']},
                  {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newpipe2[0]['y']}
                  ]
    # my list of lower pipes
    lowerpipes = [{'x': SCREENWIDTH+200, 'y': newpipe1[1]['y']},
                  {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newpipe2[1]['y']}
                  ]
    pipeVelX = -6
    playerVely = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # It's velocity while flapping
    playerFlapped = False # It's only true when player is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVely = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
        crashTest = isCollide(playerx, playery, upperpipes, lowerpipes)
        if crashTest:
            finalscore.append(score)
            # print(finalscore)
            FINALSCORE.append(finalscore[0])
            highscore = max(FINALSCORE)
            # print(highscore)
            return

        # checking for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperpipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][1].get_width()/2
            if pipeMidPos < playerMidPos < pipeMidPos + 13:
                score += 1
                # print('Your score is {}'.format(score))
                # print(finalscore)
                GAME_SOUNDS['point'].play()
            if playerVely < playerMaxVelY and not playerFlapped:
                playerVely += playerAccY
            if playerFlapped:
                playerFlapped = False
            playerHeight = GAME_SPRITES['player'].get_height()
            playery = playery + min(playerVely, GROUNDY - playery - playerHeight)

            # move the pipes to left
            for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
                upperpipe['x'] += pipeVelX
                lowerpipe['x'] += pipeVelX

            # Adding new pipes as the previous one crosses leftmost of the screen
            if 0 < upperpipes[0]['x'] < 5:
                newpipe = getRandomPipe()
                upperpipes.append(newpipe[0])
                lowerpipes.append(newpipe[1])

            # if pipe is out of the screen remove it
            if upperpipes[0]['x'] < -GAME_SPRITES['pipe'][1].get_width():
                upperpipes.pop(0)
                lowerpipes.pop(0)
            x = -0.01
            # if score == 5:
            #     pipeVelX += -0.04
            #     if 0 < upperpipes[0]['x'] < 1 or 0 < upperpipes[1]['x'] < 3:
            #         score += 1
            #         newpipe = getRandomPipe()
            #         upperpipes.append(newpipe[0])
            #         lowerpipes.append(newpipe[1])
            #     elif upperpipes[0]['x'] < -GAME_SPRITES['pipe'][1].get_width():
            #         upperpipes.pop(0)
            #         lowerpipes.pop(0)

            # Blitting the screen
            SCREEN.blit(GAME_SPRITES['background'], (0, 0))
            for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
                SCREEN.blit(GAME_SPRITES['pipe'][0], (int(upperpipe['x']), int(upperpipe['y']))) # blitting upper pipes
                SCREEN.blit(GAME_SPRITES['pipe'][1], (int(lowerpipe['x']), int(lowerpipe['y']))) # blitting lower pipes

            SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
            SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
            myDigits = [int(x) for x in list(str(score))]
            width = 0
            for digit in myDigits:
                width += GAME_SPRITES['numbers'][digit].get_width()
            Xoffset = int((SCREENWIDTH - width)/2)
            for digit in myDigits:
                SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, int(SCREENHEIGHT*0.02)))
                Xoffset += GAME_SPRITES['numbers'][digit].get_width()
            highDigits = [int(x) for x in list(str(max(FINALSCORE)))]

            highscoreX = int(SCREENWIDTH/4.2)
            highscoreY = int(SCREENHEIGHT*0.9)
            Hxoffset = int((SCREENWIDTH -width)/1.1)
            for digit in highDigits:
                SCREEN.blit(GAME_SPRITES['numbers'][digit], (Hxoffset, highscoreY))
                Hxoffset += GAME_SPRITES['numbers'][digit].get_width()
            SCREEN.blit(GAME_SPRITES['highscore'], (highscoreX, highscoreY))
            pygame.display.update()
            FPSCLOCK.tick(FPS)



def isCollide(playerx, playery, upperpipes, lowerpipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperpipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if playery < pipeHeight + pipe['y'] and (abs(playerx - pipe['x']) - 3.5) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerpipes:
        if playery + GAME_SPRITES['player'].get_height() > pipe['y'] and (abs(playerx - pipe['x']) - 3.5) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True




def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][1].get_height()
    offset = int(SCREENHEIGHT/4)
    y2 = random.randrange(offset, int(SCREENHEIGHT-GAME_SPRITES['base'].get_height()-1.2*offset))
    pipeX = SCREENWIDTH + 2
    y1 = pipeHeight - y2 + offset
    pipe = [{'x': pipeX, 'y':-y1}, # upper pipe
            {'x': pipeX, 'y': y2} # lower pipe
            ]
    return pipe
if __name__ == "__main__":

    # This will be the main point from where our game will start
    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Muskan')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('sprites/0.png').convert_alpha(),
        pygame.image.load('sprites/1.png').convert_alpha(),
        pygame.image.load('sprites/2.png').convert_alpha(),
        pygame.image.load('sprites/3.png').convert_alpha(),
        pygame.image.load('sprites/4.png').convert_alpha(),
        pygame.image.load('sprites/5.png').convert_alpha(),
        pygame.image.load('sprites/6.png').convert_alpha(),
        pygame.image.load('sprites/7.png').convert_alpha(),
        pygame.image.load('sprites/8.png').convert_alpha(),
        pygame.image.load('sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] =pygame.image.load('sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180),
                           pygame.image.load(PIPE).convert_alpha()
                           )

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('audio/wing.wav')
    GAME_SOUNDS['game over'] = pygame.mixer.Sound('audio/game over.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['highscore'] = pygame.image.load('sprites/highscore(1).png')
    HIGHSCORE = max(FINALSCORE)
    while True:
        welcomeScreen()
        mainGame()
        # print(FINALSCORE)





