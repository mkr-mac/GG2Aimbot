from PIL import Image
import math

def clear_path(x1, y1, x2, y2, screen):
	if(x2 != x1):
		m = -(y2-y1)/(x2-x1)
	else:
		if(y2 > y1):
			m = 41640.0
		else:
			m = -41640.0
	pict = Image.open(screen).convert('RGB')
	if(math.fabs(m)>1):
		for y in xrange(int(y1), int(y2)):
			xpix = (m*(y1-y))+x1
			r, g ,b = pict.getpixel((math.floor(xpix), y))
			if (r == 0 and g == 0 and b == 0):
				return False
		return True
	else:
		for x in xrange(int(x1), int(x2)):
			ypix = (m*(x1-x))+y1
			r, g ,b = pict.getpixel((x, math.floor(ypix)))
			if (r == 0 and g == 0 and b == 0):
				return False
		return True
