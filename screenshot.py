import win32gui
import win32ui 
import win32con
import numpy
import struct
import cv2

class GGScreen:
	def __init__(self,screen_w,screen_h):
		hwnd = win32gui.FindWindow(None, "Sublime Text 2")
		wDC = win32gui.GetWindowDC(hwnd)
		self.dcObj = win32ui.CreateDCFromHandle(wDC)
		self.cDC = self.dcObj.CreateCompatibleDC()
		self.dataBitMap = win32ui.CreateBitmap()
		self.dataBitMap.CreateCompatibleBitmap(self.dcObj,screen_w,screen_h)
		self.cDC.SelectObject(self.dataBitMap)
		self.screen_w, self.screen_h = screen_w, screen_h

	# This version is faster, and it also gets the window no matter where it is on the screen, and only the window we need.
	def screenshot(self):
		self.cDC.BitBlt((0,0), (self.screen_w,self.screen_h), self.dcObj, (0,0), win32con.SRCCOPY)
		self.dataBitMap.SaveBitmapFile(self.cDC, 'temp')
		cv2.imread('temp',1)

	def finish(self):
		# Free Resources
		dcObj.DeleteDC()
		cDC.DeleteDC()
		win32gui.ReleaseDC(hwnd, wDC)
		win32gui.DeleteObject(dataBitMap.GetHandle())

