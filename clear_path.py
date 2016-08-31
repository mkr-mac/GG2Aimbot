from PIL import Image
import math

#Doubles/Floats only!
def clear_path(x1, y1, x2, y2, screen):
	if(x2 != x1):
		m = -(y2-y1)/(x2-x1)
	else:
		if(y2 > y1):
			m = 41640.0
		else:
			m = -41640.0
	
	if(math.fabs(m)>1):
		for y in xrange(int(y1), int(y2)):
			xpix = (m*(y1-y))+x1
			pixel_color = screen[math.floor(xpix), y]
			if (pixel_color == [0,0,0]):
				return False
		return True
	else:
		for x in xrange(int(x1), int(x2)):
			ypix = (m*(x1-x))+y1
			pixel_color = screen[math.floor(xpix), y]
			if (pixel_color == [0,0,0]):
				return False
		return True
