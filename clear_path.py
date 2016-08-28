from PIL import Image
import math

def clear_path(x1, y1, x2, y2, screen):
	m = -(y2-y1)/(x2-x1)
	pict = Image.open(screen).convert('RGB')
	if(math.fabs(m)>1):
		for y in range(y1, y2):
			xpix = (m*(y1-y))+x1
			r, g ,b = pict.getpixel((math.floor(xpix), y))
			if (r == 0 and g == 0 and b == 0):
				return False
		return True
	else:
		for x in range(x1, x2):
			ypix = (m*(x1-x))+y1
			r, g ,b = pict.getpixel((x, math.floor(ypix)))
			if (r == 0 and g == 0 and b == 0):
				return False
		return True

clear_path(412, 440, 600, 600, "boom_headshot.png")