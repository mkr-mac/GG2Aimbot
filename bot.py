import PIL.ImageGrab as screen
import numpy as np
import sys, pygame
import pygame.surfarray as surf
import cv2
import os
GAME_W = 790
GAME_H = 670

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (800,100)

pygame.init()
window = pygame.display.set_mode([GAME_W,GAME_H])

# Load images
from os import listdir
from os.path import isfile, join
red = [f for f in listdir("Class_Sprites/RedSig") if isfile(join("Class_Sprites/RedSig", f))]
targets = []

for f in red:
    targets.append(cv2.imread("Class_Sprites/RedSig/"+f,1))


while True:
    pygame.event.wait()
    capture = np.asarray(screen.grab([0,0,GAME_W,GAME_H]))

    b,g,r = cv2.split(capture)       # get b,g,r
    capture = cv2.merge([r,g,b])     # switch it to rgb
    cv2.imwrite("out.png",capture)

    # Draw 
    display_capture = surf.make_surface(capture)
    display_capture =  pygame.transform.rotate(display_capture, -90)
    display_capture = pygame.transform.flip(display_capture, True, False)
 

    res = cv2.matchTemplate(capture,targets[0],cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    print min_val
    pygame.draw.rect(display_capture, (0,255,0), (min_loc[0],min_loc[1],20,20), 10)
    window.blit(display_capture, [0,0,GAME_W,GAME_H])
    pygame.display.flip()