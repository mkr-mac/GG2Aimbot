import win32gui
import win32ui 
import win32con
import numpy
import struct
import cv2
import threading

class Window:
	# Loads in the active window and prepares it for screenshotting
	def __init__(self):
		self.handle = win32gui.GetForegroundWindow()

		self.screen_w = self.get_rect()[2]
		self.screen_h = self.get_rect()[3]

		wDC = win32gui.GetWindowDC(self.handle)
		self.dcObj = win32ui.CreateDCFromHandle(wDC)
		self.cDC = self.dcObj.CreateCompatibleDC()
		self.dataBitMap = win32ui.CreateBitmap()
		self.dataBitMap.CreateCompatibleBitmap(self.dcObj,self.screen_w,self.screen_h)
		self.cDC.SelectObject(self.dataBitMap)
		self.dirty_frame = False

	def launch_screenshot_thread(self):
		self.screenshot = None
		t = threading.Thread(target=self.screenshot_thread)
		t.daemon = True
		t.start()

	def get_screenshot(self):
		while self.screenshot == None:
			pass
		return self.screenshot

	def screenshot_thread(self):
		while True:
			self.cDC.BitBlt((0,0), (self.screen_w,self.screen_h), self.dcObj, (0,0), win32con.SRCCOPY)
			self.dataBitMap.SaveBitmapFile(self.cDC, 'temp')
			if self.dirty_frame:
				continue
			else:
				self.screenshot = cv2.imread('temp',1)

	def dirty_frame_start(self):
		self.dirty_frame = True

	def dirty_frame_end(self):
		self.dirty_frame = False

	# X Y W H
	def get_rect(self):
	 	rect =  win32gui.GetWindowRect(self.handle)
	 	return [rect[0],rect[1], rect[2] - rect[0], rect[3] - rect[1]]

	def finish(self):
		# Free Resources
		dcObj.DeleteDC()
		cDC.DeleteDC()
		win32gui.ReleaseDC(hwnd, wDC)
		win32gui.DeleteObject(dataBitMap.GetHandle())

	@staticmethod
	def get_current_active_window_name():
		return win32gui.GetWindowText(win32gui.GetForegroundWindow())


