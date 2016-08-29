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
from window import Window
import time

PYGAME_DEBUG = False

pyg_window = None
if PYGAME_DEBUG:
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (800,100)
    pygame.init()
    pyg_window = pygame.display.set_mode([GAME_W,GAME_H])


red = [f for f in listdir("Class_Sprites/RedSig") if isfile(join("Class_Sprites/RedSig", f))]
targets = []
names = []

for f in sorted(red)[0:2]:
    load = cv2.imread("Class_Sprites/RedSig/"+f,1)
    targets.append(load)
    #b,g,r = cv2.split(load) 
    #targets.append(cv2.merge([r,g,b]))     
    names.append(f)

ptr = 0

# Try to grab TF2 window, first.
while True:
    name = Window.get_current_active_window_name()
    if 'cp_' in name or 'ctf_' in name:
        break 
    
print 'Connected to screen!'
gg2window = Window()

while True:

    ptr = ptr + 1
    ptr = ptr % len(targets)

    # Takes about 0.01s
    capture = gg2window.screenshot()


    # Takes 0.1 s
    res = cv2.matchTemplate(capture,targets[ptr],cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    print min_val
    #2 mil is a good thresh
    if (min_val < 10.0) and (win32api.GetAsyncKeyState(ord('H')) != 0):
        # Shoot it!
        click(gg2window.get_rect()[0]+min_loc[0]+(targets[ptr].shape[1]/2),gg2window.get_rect()[1]+min_loc[1]+(targets[ptr].shape[0]/2))
        print names[ptr]
        print min_val
        ptr = ptr - 1


    if PYGAME_DEBUG:
        pygame.event.wait()
          # Draw 
        display_capture = surf.make_surface(capture)
        display_capture =  pygame.transform.rotate(display_capture, -90)
        display_capture = pygame.transform.flip(display_capture, True, False)

        pygame.draw.rect(display_capture, (0,255,0), (min_loc[0],min_loc[1],20,20), 10)
        pyg_window.blit(display_capture, [0,0,GAME_W,GAME_H])
        pygame.display.flip()

