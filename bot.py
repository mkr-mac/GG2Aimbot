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
<<<<<<< HEAD
onlyfiles = [f for f in listdir("Class_Sprites/Red/") if isfile(join("Class_Sprites/Red/", f))]
print onlyfiles

while True:
	capture = surf.make_surface(np.asarray(screen.grab([0,0,GAME_W,GAME_H])))
	capture =  pygame.transform.rotate(capture, -90)
	capture = pygame.transform.flip(capture, True, False)
	window.blit(capture, [0,0,GAME_W,GAME_H])
	pygame.display.flip()
'''
img = cv2.imread('messi5.jpg',0)
img2 = img.copy()
template = cv2.imread('template.jpg',0)
w, h = template.shape[::-1]

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

for meth in methods:
    img = img2.copy()
    method = eval(meth)

    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv2.rectangle(img,top_left, bottom_right, 255, 2)

    plt.subplot(121),plt.imshow(res,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)

    plt.show()
'''
=======
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
>>>>>>> 6d6fa42309d8b5fc69381436ef7c8d7eb11f54b8
