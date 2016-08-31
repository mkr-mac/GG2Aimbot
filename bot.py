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
from clear_path import clear_path
from window import Window
import time
import math

PYGAME_DEBUG = False
LOCAL_SEARCH_RADIUS = 50

pyg_window = None

# Launch a pygame window. 
if PYGAME_DEBUG:
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (800,100)
    pygame.init()
    pyg_window = pygame.display.set_mode([GAME_W,GAME_H])

# Load in the list of targets and their names. Only loads REDs for now.
red = [f for f in listdir("Class_Sprites/RedSig") if isfile(join("Class_Sprites/RedSig", f))]
targets = []
names = []
for f in sorted(red):
    load = cv2.imread("Class_Sprites/RedSig/"+f,1)
    targets.append(load)
    names.append(f)

# Wait for the TF2 window to pop up.
while True:
    name = Window.get_current_active_window_name()
    if 'cp_' in name or 'ctf_' in name or 'arena_' in name or 'koth_' in name:
        break 
    
print 'Connected to screen!'
gg2window = Window()
gg2window.launch_screenshot_thread()

target_location = None
target_type_index = 0

while True:
    # Get latest screencapture
    capture = gg2window.get_screenshot()
    # If we do not have a target, we need to search the whole screen to find one.
    if target_location == None:
        print 'Searching...'
        # For each RED target, compare the template against the screen.
        for i,target in enumerate(targets):
            match = cv2.matchTemplate(capture,target,cv2.TM_SQDIFF)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
            # If the squared difference is less than 10 it's probably a match.
            if (min_val < 10.0):
                target_location = min_loc
                target_type_index = i
                break
    else:
        # We found a target! See if it's in the neighborhood and shoot it!
        # Don't go out of the window, tho.
        x_search_min = max(0,target_location[0]-LOCAL_SEARCH_RADIUS)
        x_search_max = min(gg2window.get_rect()[2],target_location[0]+LOCAL_SEARCH_RADIUS)
        y_search_min = max(0,target_location[1]-LOCAL_SEARCH_RADIUS)
        y_search_max = min(gg2window.get_rect()[3],target_location[1]+LOCAL_SEARCH_RADIUS)
        search_area = capture[y_search_min:y_search_max,x_search_min:x_search_max]
        match = cv2.matchTemplate(search_area,targets[target_type_index],cv2.TM_SQDIFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)

        if (min_val < 10.0):
            # The target is here on the screen
            target_location = [x_search_min + min_loc[0],y_search_min + min_loc[1]]

            if  (win32api.GetAsyncKeyState(ord('H')) != 0):
				if (clear_path(gg2window.get_rect()[0]+(gg2window.get_rect()[2])/2,gg2window.get_rect()[1]+(gg2window.get_rect()[3])/2,gg2window.get_rect()[0] + target_location[0] + (targets[target_type_index].shape[1]/2), gg2window.get_rect()[1]+ target_location[1] +(targets[target_type_index].shape[0]/2), capture)):
					# When we click, we know that the next screencap will have our mouse position over the target, and so will be invalid. 
					# As a result, we put the cursor position somewhere else and skip to the next frame
					click(gg2window.get_rect()[0] + target_location[0] + (targets[target_type_index].shape[1]/2), gg2window.get_rect()[1]+ target_location[1] +(targets[target_type_index].shape[0]/2))
					gg2window.dirty_frame_start()
					win32api.SetCursorPos((target_location[0],target_location[1]-50))
					time.sleep(0.05)
					gg2window.dirty_frame_end()
					# now the dirty frame has passed. Give the computer some time to generate a new frame.
					time.sleep(0.05)

        else:
            target_location = None
            target_type_index = None

    
     

    if PYGAME_DEBUG:
        pygame.event.wait()
          # Draw 
        display_capture = surf.make_surface(capture)
        display_capture =  pygame.transform.rotate(display_capture, -90)
        display_capture = pygame.transform.flip(display_capture, True, False)

        pygame.draw.rect(display_capture, (0,255,0), (min_loc[0],min_loc[1],20,20), 10)
        pyg_window.blit(display_capture, [0,0,GAME_W,GAME_H])
        pygame.display.flip()

