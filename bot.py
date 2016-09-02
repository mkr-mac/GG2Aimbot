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

DEBUG_DISPLAY = False
LOCAL_SEARCH_RADIUS = 200

class Bot:

	def __init__(self):
		self.load_red_class_signatures()
		self.wait_for_game_window()
		self.gg2window = Window()
		self.gg2window.launch_screenshot_thread()
		print 'Connected to screen!'
		if DEBUG_DISPLAY:
			self.pygame_display = PyGameDisplay()
			self.pygame_display 


	def load_red_class_signatures(self):
		# Load in the list of targets and their names. Only loads REDs for now.
		red = [f for f in listdir("Class_Sprites/RedSig") if isfile(join("Class_Sprites/RedSig", f))]
		self.targets = []
		self.names = []
		for f in sorted(red):
			load = cv2.imread("Class_Sprites/RedSig/"+f,1)
			self.targets.append(load)
			self.names.append(f)


	def wait_for_game_window(self):
		# Wait for the TF2 window to pop up.
		while True:
			name = Window.get_current_active_window_name()
			if 'cp_' in name or 'ctf_' in name or 'arena_' in name or 'koth_' in name:
				break 
		
	def get_match_location(self,capture,target_index):
		# For each RED target, compare the template against the screen.
		match = cv2.matchTemplate(capture,self.targets[target_index],cv2.TM_SQDIFF)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
		# If the squared difference is less than 10 it's probably a match.
		if (min_val < 10.0):
			return min_loc 
		else: 
			return None

	def get_search_area_dimensions(self):
		x_min = max(0,self.target_location[0]-LOCAL_SEARCH_RADIUS)
		x_max = min(self.gg2window.get_rect()[2],self.target_location[0]+LOCAL_SEARCH_RADIUS)
		y_min = max(0,self.target_location[1]-LOCAL_SEARCH_RADIUS)
		y_max = min(self.gg2window.get_rect()[3],self.target_location[1]+LOCAL_SEARCH_RADIUS)
		return [x_min,x_max,y_min,y_max]

	def shoot(self,x,y):
			# When we click, we know that the next screencap will have our mouse position over the target, and so will be invalid. 
			# As a result, we put the cursor position somewhere else and skip to the next frame
			click(x,y)
			self.gg2window.dirty_frame_start()
			win32api.SetCursorPos([x,y-50])
			time.sleep(0.05)
			self.gg2window.dirty_frame_end()
			# now the dirty frame has passed. Give the computer some time to generate a new frame.
			time.sleep(0.05)

	def run(self):
		# If a target is found, this will store their location and their index.
		self.target_location = None
		self.target_type_index = 0
		# This will iterate through all the targers to try to make a match
		self.target_iterator = 0

		while True:
		# Get latest screencapture
			capture = self.gg2window.get_screenshot()
	
			# If we do not have a target, we need to search the whole screen to find one.
			if self.target_location == None:
				location = self.get_match_location(capture,self.target_iterator)
				if location is None:
					 self.target_iterator = (self.target_iterator + 1) % len(self.targets)
				else:
					self.target_location = location
					self.target_type_index = self.target_iterator
			   
			# Target detected
			else:
				dims = self.get_search_area_dimensions()
				search_area = capture[dims[2]:dims[3],dims[0]:dims[1]]
				location = self.get_match_location(search_area,self.target_type_index)

				if location is None:
					self.target_location = None
					self.target_type_index = None
				else:
					# UPDATE TARGET TRACKING: TODO, this expression doesnt seem to work.
					self.target_location = [dims[0] + location[0], dims[2] + location[1]]
					x_center = self.gg2window.get_rect()[0]+(self.gg2window.get_rect()[2])/2
					y_center = self.gg2window.get_rect()[1]+(self.gg2window.get_rect()[3])/2
					x_target = self.gg2window.get_rect()[0]+ self.target_location[0] + (self.targets[self.target_type_index].shape[1]/2)
					y_target = self.gg2window.get_rect()[1]+ self.target_location[1] + (self.targets[self.target_type_index].shape[0]/2)

					#if clear_path(x_center,y_center,x_target,y_target, capture) and 
					if (win32api.GetAsyncKeyState(ord('H')) != 0):
						self.shoot(x_target,y_target)
Bot().run()