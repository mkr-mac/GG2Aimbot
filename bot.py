import PIL.ImageGrab as screen
import numpy as np
import sys, pygame
import pygame.surfarray as surf
import cv2
import os
import win32api, win32con, time
from os import listdir
from os.path import isfile, join
from click import click
PYGAME_DEBUG = False
GAME_W = 790
GAME_H = 670

window = None
if PYGAME_DEBUG:
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (800,100)
    pygame.init()
    window = pygame.display.set_mode([GAME_W,GAME_H])


red = [f for f in listdir("Class_Sprites/RedSig") if isfile(join("Class_Sprites/RedSig", f))]
targets = []
names = []

for f in red:
    targets.append(cv2.imread("Class_Sprites/RedSig/"+f,1))
    names.append(f)

ptr = 0

while True:
    ptr = ptr + 1

    ptr = ptr % len(targets)
    capture = np.asarray(screen.grab([0,0,GAME_W,GAME_H]))

    b,g,r = cv2.split(capture)       # get b,g,r
    capture = cv2.merge([r,g,b])     # switch it to rgb

    res = cv2.matchTemplate(capture,targets[ptr],cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    #2 mil is a good thresh
    if (min_val < 1000.0) and (win32api.GetAsyncKeyState(ord('H')) != 0):
        # Shoot it!
        click(min_loc[0]+(targets[ptr].shape[1]/2),min_loc[1]+(targets[ptr].shape[0]/2))
        ptr = ptr  = ptr - 1
        print names[ptr]
        print min_val


    if PYGAME_DEBUG:
        pygame.event.wait()
          # Draw 
        display_capture = surf.make_surface(capture)
        display_capture =  pygame.transform.rotate(display_capture, -90)
        display_capture = pygame.transform.flip(display_capture, True, False)

        pygame.draw.rect(display_capture, (0,255,0), (min_loc[0],min_loc[1],20,20), 10)
        window.blit(display_capture, [0,0,GAME_W,GAME_H])
        pygame.display.flip()

