import cv2
import numpy as np
from round_2_data import *

cap = cv2.VideoCapture(2)
dir = list()
dir_inv = list()
limits = list()
limits_inv = list()
offset = list()
offset_inv = list()
center = None
is_first = True
turn_path = list()

offset_value = 100    
count = 0
overshoot = 30

key = None
x_i =0
x_f = 0
y_i = 0
y_f = 0
def path_def(event,x,y,falgs,param):
	global is_first,x_i,y_i,img,count
	if event ==cv2.EVENT_LBUTTONDOWN:
		#print("pressed")
		if is_first:
			x_i = x
			y_i = y
			is_first = False
		else:
			x_f = x
			y_f = y
			is_first = True
			cv2.line(img,(x_i,y_i),(x_f,y_f),(0,255,255),5)
			count+= 1
			if abs(x_i-x_f) < 20 :
				if (y_i>y_f):
					dir.append('N')
					dir_inv.append('S')
					offset.append(y_f - offset_value)
					offset_inv.append(y_i + offset_value)
					y_f = y_f + overshoot
					y_i = y_i - overshoot
				else:
					dir.append('S')
					dir_inv.append('N')
					offset.append(y_f + offset_value)
					offset_inv.append(y_i - offset_value)
					y_f = y_f - overshoot
					y_i = y_i + overshoot
				limits.append(y_f)
				limits_inv.append(y_i)
			elif abs(y_i-y_f) < 20:
				if (x_f>x_i):
					dir.append('E')
					dir_inv.append('W')
					offset.append(x_f + offset_value)
					offset_inv.append(x_i - offset_value)
					x_f = x_f - overshoot
					x_i = x_i + overshoot
				else:
					dir.append('W')
					dir_inv.append('E')
					offset.append(x_f - offset_value)
					offset_inv.append(x_i + offset_value)
					x_f = x_f + overshoot
					x_i = x_i - overshoot

				limits.append(x_f)
				limits_inv.append(x_i)


img = np.zeros((960, 1280, 3),np.uint8)    # (480,640,3)  (960, 1280, 3)

bot_no = 0

def main():
	global key,frame,count,limits,offset,dir,img
	cv2.namedWindow('path parser')
	while True:
		got , frame = cap.read()
		cv2.setMouseCallback('path parser',path_def,frame)
		
		#frame = cv2.flip(frame,1)
		lower = color_def[bot_no][0]
		upper = color_def[bot_no][1]
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv,lower,upper)

		cnts,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
		for i,c in enumerate(cnts):
			if len(c)> 100:
				rect = cv2.minAreaRect(c)
				center = rect[0]				#center (x,y)
				
				cv2.circle(frame, (int(center[0]),int(center[1])),7,(0,0,255),-1)


		out = cv2.bitwise_or(img,frame)
		cv2.imshow('path parser',out)
		key = cv2.waitKey(1)
		if key == 113:
			break
		if key == 27:
			img = np.zeros((960, 1280, 3),np.uint8)
			count = 0
			dir.clear()
			dir_inv.clear()
			limits.clear()
			limits_inv.clear()
			offset.clear()
			offset_inv.clear()
			turn_path.clear()
		if key == 32:
			for j in range(1,3,1):
				for i in range(count-1):
					turn_path.append(0)
				turn_path.append(j)

			limits_inv.reverse()
			dir_inv.reverse()
			offset_inv.reverse()
			limits+=limits_inv
			offset+=offset_inv
			dir+=dir_inv
			dir+=dir_inv[-1]
			if len(limits_inv) > 1:
				center = [limits_inv[-2]]
			else:
				center = [y_i+30]
			print('[',dir,',',limits,',',offset,',',center,',',turn_path,'],')
			
			#img = np.zeros((960, 1280, 3),np.uint8)
			
			count = 0
			dir.clear()
			dir_inv.clear()
			limits.clear()
			limits_inv.clear()
			offset.clear()
			offset_inv.clear()
			turn_path.clear()
		if key == 115:
			limits_inv.reverse()
			if len(limits_inv) > 1:
				center = [limits_inv[-2]]
			else:
				center = [y_i]
			dir+=dir[-1]
			print('[',dir,',',limits,',',offset,',',center,',','[0,2]','],')

			count = 0
			dir.clear()
			dir_inv.clear()
			limits.clear()
			limits_inv.clear()
			offset.clear()
			offset_inv.clear()
			turn_path.clear()
	cap.release()

if __name__=='__main__':
	main()