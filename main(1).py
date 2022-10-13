import random
import sys
import pygame
from pygame.locals import *

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
BACKGROUND = "E:/Flappy bird game/sprites/background.png"
PIPE = "E:/Flappy bird game/sprites/pipe.png"
PLAYER = "E:/Flappy bird game/sprites/bird.png"
def welcomeScreen():
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            #     pygame.quit()
            #     sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


if __name__ == " main(1) ":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappybird with Vedant')
    GAME_SPRITES["numbers"] = (
            pygame.image.load("E:/Flappy bird game/sprites/0.png").convert_alpha,
            pygame.image.load("E:/Flappy bird game/sprites/1.png").convert_alpha,
            pygame.image.load("E:/Flappy bird game/sprites/2.png").convert_alpha,
            pygame.image.load("E:/Flappy bird game/sprites/3.png").convert_alpha,
            pygame.image.load("E:/Flappy bird game/sprites/4.png").convert_alpha,
            pygame.image.load("E:/Flappy bird game/sprites/5.png").convert_alpha,
            pygame.image.load("E:/Flappy bird game/sprites/6.png").convert_alpha,
            pygame.image.load("E:/Flappy bird game/sprites/7.png").convert_alpha,
            pygame.image.load("E:/Flappy bird game/sprites/8.png").convert_alpha,
            pygame.image.load("E:/Flappy bird game/sprites/9.png").convert_alpha
    )
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert_alpha
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha, 180), pygame.image.load(PIPE).convert_alpha)
    GAME_SPRITES['base'] = pygame.image.load('E:/Flappy bird game/sprites/base.png')
    GAME_SPRITES['message'] = pygame.image.load('E:/Flappy bird game/sprites/message.png')
    GAME_SPRITES['player'] = pygame.image.load('E:/Flappy bird game/sprites/bird.png')

    GAME_SOUNDS['die'] = pygame.mixer.Sound('E:/Flappy bird game/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('E:/Flappy bird game/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('E:/Flappy bird game/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('E:/Flappy bird game/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('E:/Flappy bird game/audio/wing.wav')

    while True:
        welcomeScreen()