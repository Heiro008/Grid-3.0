import cv2
import time
import numpy as np
from navigate_module import *
from round_1_data import *
import socket 
import imutils
import multiprocessing
import math
from operator import xor
con = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
con1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
con2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
con3 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
con.connect(('192.168.251.7',8888))
con1.connect(('192.168.251.187',8888))
con2.connect(('192.168.251.126',8888))
con3.connect(('192.168.251.197',8888))
def color_check():
	flag = False
	while True:
		got, frame = cap.read()
		for i,j in enumerate(color_def):
			#print(i,j[0])
			lower = np.array(j[0],dtype='uint8')
			upper = np.array(j[1],dtype='uint8')
			mask = cv2.inRange(frame,lower,upper)
			if mask.argmax():
				return i,lower,upper
				flag = True
				break
		if flag:
			break
	cap.release()

def color_to_path(color):
	return color

def next(path_no):
	print(path_no)
	print(bot[path_no])
	global con
	if path_no==1:
		con = con1
	elif path_no ==2:
		con = con2
	elif path_no == 3:
		con = con3
	return color_def[path_no][0],color_def[path_no][1]

def send_msg(msg):
	try:
		con.send(msg)
	except:
		pass


url = 'http://192.168.251.238:8080/video'

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 60)
#video = cv2.VideoWriter('video4.mp4',cv2.VideoWriter_fourcc(*'MJPG'),30, (1440,1280))
path_no = 0
c_time = 0
count = 0
def main():
	c_time =0
	count =0
	global path_no
	flag = False
	lower,upper=next(path_no)
	#lower = (14,84,231)
	#lower = (0,75,244)
	#upper = (43,255,255)	
	#path_no=color_to_path(color)
	print(path_no)
	path1 = path(path_no = path_no)
	center = None
	theta =0	
	angle =0
	c_time = time.time()
	is_correct = False
	while True:
		is_done = False
		#print(time.time()-c_time)
		if (time.time() - c_time) > 0.7:
			c_time = time.time()
			is_correct = False
		count +=1
		got , frame = cap.read()
		frame = cv2.rotate(frame , cv2.ROTATE_90_CLOCKWISE)
		#frame = cv2.flip(frame,1)
		#frame = imutils.resize(frame,width = 600)
		#blurred = cv2.GaussianBlur(frame,(11,11),0)
		#frame = cv2.bilateralFilter(frame,5,150,150)
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		mask = cv2.inRange(hsv,lower,upper)
		masked = cv2.bitwise_and(frame,frame,mask = mask)
		output = np.concatenate((frame,masked),axis = 1)
		output1 = cv2.resize(output,(1440,1000))
		#video.write(output)
		#mask = cv2.erode(mask, None,iterations=2)
		#mask = cv2.dilate(mask,None,iterations=2)
		#output = cv2.bitwise_and(frame,frame,mask=mask)
		#cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


		cnts,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
		for i,c in enumerate(cnts):
			if len(c)> 40:
				rect = cv2.minAreaRect(c)
				center = rect[0]
				#width = int(rect[1][0])
				#height = int(rect[1][1])
				size = rect[1]
				angle = int(rect[2])
				#	print('contor detected')
				is_done = True
				hyp = math.sqrt((path1.t_lim_offset-center[~path1.mov_dir])**2+(path1.center-center[path1.mov_dir])**2)
				adj = math.fabs(path1.center-center[path1.mov_dir])
				opp = math.fabs(center[~path1.mov_dir]-path1.t_lim_offset)
				theta = int(math.degrees(math.asin(opp/hyp)))

		#print('diff :',diff)
		if is_done and count > 100:
# replaced	not path1.move_dir = xor(path1.mov_dir,path1.curr_dir!='E')
			if xor(xor(path1.mov_dir,(path1.curr_dir!='E' and path1.curr_dir!='S')),center[path1.mov_dir]>path1.center):
				#if height > width
				if rect[1][path1.mov_dir]> rect[1][~path1.mov_dir]:
					angle = 90-angle
				else:
					angle = 180 - angle
			else:
				if rect[1][path1.mov_dir]> rect[1][~path1.mov_dir]:
					angle =90 +angle
			

			diff = angle - theta
			if diff > -2 and diff < 2 or is_correct:
				#print('correct angle')
				is_correct = True
				send_msg('c{}\n'.format(0).encode('utf-8'))
			
			else:
				if center[path1.mov_dir]>path1.center:
					send_msg((path1.r_dir+'{}\n').format(diff).encode('utf-8'))				
					#print(path1.r_dir)
				elif center[path1.mov_dir]<path1.center:					
					send_msg((path1.l_dir+'{}\n').format(diff).encode('utf-8'))
					#print(path1.l_dir)
					#pass
				else:
					print('correct angle and centered')
					#correct path
			
				#send to go forward
				'''
			if center[path1.mov_dir] not in range(path1.lower_limit,path1.upper_limit):
				if center[path1.mov_dir]>path1.upper_limit:
					print('move '+path1.r_dir)
					#down

					#con.send((path1.r_dir+'{}\n').format(center[path1.mov_dir]-path1.upper_limit).encode('utf-8'))

				if center[path1.mov_dir]<path1.lower_limit:
					print('move '+path1.l_dir)
					#con.send((path1.l_dir+'{}\n').format(path1.lower_limit-center[path1.mov_dir]).encode('utf-8'))


			else:

				print('corect path')
				#con.send('c{}\n'.format(0).encode('utf-8'))
				'''
			if path1.curr_dir == 'W' or path1.curr_dir == 'N':
				if center[~path1.mov_dir]<(path1.t_lim):  #+50
					is_correct = False
					for i in range(50):
						#print('turn '+path1.t_dir)
						#print(path1.t_msg)
						#print(path1.sub_path)
						if path1.sub_path == 1:
							path1.is_reversed = True
							send_msg('s'.encode('utf-8'))
						elif path1.sub_path == 3:
							send_msg('h'.encode('utf-8'))
							flag = True
						else:
							send_msg((path1.t_msg+'\n').encode('utf-8'))
						time.sleep(0.020)
					#time.sleep(1)
					if flag:
						break
					path1.turn()
						 
			else:
				if center[~path1.mov_dir]>(path1.t_lim):  # -50
					is_correct = False
					for i in range(50):
						#print('turn '+path1.t_dir)
						#print(path1.t_msg)
						if path1.sub_path == 3:
							send_msg('h'.encode('utf-8'))
							flag = True
						elif path1.sub_path == 1:
							path1.is_reversed = True
							send_msg('s'.encode('utf-8'))
						else:
							send_msg((path1.t_msg+'\n').encode('utf-8'))
						time.sleep(0.020)
					#time.sleep(1)
					if flag:
						break
					path1.turn()
					#next()					#define next()
					
					#path_no += 1
					#break
					

					#path1.turn()
		#output = cv2.bitwise_and(frame,frame,mask=mask)
		#print('hyp : {0} adj : {1} theta : {2} angle : {3}'.format(int(hyp),int(adj),theta,angle))

		#print('theta:{0} angle:{1}'.format(int(theta),int(angle)))
		cv2.imshow("output",output1)
		if(cv2.waitKey(1)==27):
			break

	if flag:
		path_no += 1
		if path_no <=3:
			con.detach()
			main()

	cap.release()
	#video.release()
	con.detach()
	cv2.destroyAllWindows()



if __name__ =='__main__':
	main()