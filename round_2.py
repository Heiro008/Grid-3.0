import cv2
import time
import numpy as np
from navigate_module import *
from round_2_data import *
import socket 
import multiprocessing as mp
import math
from operator import xor

bot_1_pos = mp.Queue()
bot_2_pos = mp.Queue()
bot_data = [bot_1_pos,bot_2_pos]

mp_array = mp.Array("I", int(np.prod((720, 1280, 3))))   # , lock=mp.Lock()
# create a numpy view of the array
image_array = np.frombuffer(mp_array.get_obj(), dtype="I").reshape((720, 1280, 3))

disable_bot = mp.Array('B',2)        # array to control the bot movement used by monitor func

con1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
con2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


con1.connect(('192.168.233.187',8888))
con2.connect(('192.168.233.126',8888))

def color_to_path(bot_no):

	frame = image_array.astype("uint8").copy() 
	for i,j in enumerate(color_def):
		lower = j[0]
		upper = j[1]
		mask = cv2.inRange(frame,lower,upper)
		cnts,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

		for k,c in enumerate(cnts):
			if len(c)<10:
				m = cv2.moments(c)
				cx = int(m['m10']/m['m00'])
				cy = int(m['m01']/m['m00'])

				if cx>some_value and cy>some_value:			#need to define some_value
					return bot_paths[bot_no][i]
				elif cx<some_value and cy<some_value:
					return bot_paths[bot_no][i]
	color_to_bot(bot_no)						#loop until it finds some path map


def send_msg(msg,con):
	#print(con)
	con.send(msg)

url = 'http://192.168.233.166:8080/video'

cap = cv2.VideoCapture(url)
cap.set(cv2.CAP_PROP_FPS, 60)
#video = cv2.VideoWriter('video4.mp4',cv2.VideoWriter_fourcc(*'MJPG'),30, (1440,1280))

 
def bot(bot_no):

	print(bot_no)
	if bot_no ==0:
		con = con1
	else:
		con = con2
	print(con)
	c_time =0
	count =0
	flag = False

	# define a mechanism to map the path
	#path_no = color_to_path(shared_memory,bot_no)
	path_no = bot_no

	lower = color_def[bot_no][0]
	upper = color_def[bot_no][1]

	print(path_no)
	bot_s = bot_state()
	path1 = path(path_no = path_no)
	center = None
	theta =0	
	angle =0
	c_time = time.time()
	is_correct = False
	while True:
		contor_detected = False

		frame = image_array.astype("uint8").copy()  # example of some processing done on the array
		#print(frame.shape,bot_no)

		#print(time.time()-c_time)
		c_time = time.time()
		if (time.time() - c_time) > 0.7:
			c_time = time.time()
			is_correct = False
		count +=1
		#frame = cv2.flip(frame,1)
		#blurred = cv2.GaussianBlur(frame,(11,11),0)
		#frame = cv2.bilateralFilter(frame,5,150,150)
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv,lower,upper)

		cnts,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
		for i,c in enumerate(cnts):
			if len(c)> 40:
				rect = cv2.minAreaRect(c)
				center = rect[0]				#center (x,y)
				bot_s.pos = center				#store the bot coordinates in bot_state class
				size = rect[1]
				angle = int(rect[2])
				contor_detected = True
				hyp = math.sqrt((path1.t_lim_offset-center[~path1.mov_dir])**2+(path1.center-center[path1.mov_dir])**2)
				#adj = math.fabs(path1.center-center[path1.mov_dir])
				opp = math.fabs(center[~path1.mov_dir]-path1.t_lim_offset)
				theta = int(math.degrees(math.asin(opp/hyp)))

		if contor_detected and count > 100:
			# stop the bot if collision is detected
			if disable_bot[bot_no]:
				send_msg('h'.encode('utf-8'),con)
				continue

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
				send_msg('c{}\n'.format(0).encode('utf-8'),con)
			
			else:
				if center[path1.mov_dir]>path1.center:
					send_msg((path1.r_dir+'{}\n').format(diff).encode('utf-8'),con)				
					#print(path1.r_dir)
				elif center[path1.mov_dir]<path1.center:					
					send_msg((path1.l_dir+'{}\n').format(diff).encode('utf-8'),con)
					#print(path1.l_dir)
					#pass
				else:
					print('correct angle and centered')
	
			if path1.curr_dir == 'W' or path1.curr_dir == 'N':
				if center[~path1.mov_dir]<(path1.t_lim):  #+50
					is_correct = False
					for i in range(50):
						#print('turn '+path1.t_dir)
						#print(path1.t_msg)
						if path1.turn_path == 1:
							path1.is_reversed = True
							send_msg('s'.encode('utf-8'),con)
						elif path1.turn_path == 2:
							send_msg('h'.encode('utf-8'),con)
							flag = True
						else:
							send_msg((path1.t_msg+'\n').encode('utf-8'),con)
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
						if path1.turn_path == 1:
							path1.is_reversed = True
							send_msg('s'.encode('utf-8'),con)
						elif path1.turn_path == 2:
							send_msg('h'.encode('utf-8'),con)
						else:
							send_msg((path1.t_msg+'\n').encode('utf-8'),con)
						time.sleep(0.020)
					#time.sleep(1)
					if flag:
						break
					path1.turn()
			bot_s.curr_dir = path1.curr_dir
			bot_s.is_revesed = path1.is_reversed
			bot_data[bot_no].put(bot_s)
			cv2.imshow(str(bot_no),mask)
			if (cv2.waitKey(1) == 27):
				break
	#if flag:
	#	bot(bot_no)
	cv2.destroyAllWindows()
	

def monitor(): 			# monitors the bot coordinates and updates the control
	
	offset_map = {'W':[-100,0],
				  'E':[100,0],
				  'N':[0,-100],
				  'S':[0,100]
				}
	bot_state = None
	boundary_length = 100
	while True:	
		for i in range(2):
			while not bot_data[i].empty():
				bot_state[i] = bot_data[i].get()
			# bot_state[].pos[0] = x coordinate 
		if (bot_state[0].pos[0] < bot_state[1].pos[0] + boundary_length &&
			bot_state[0].pos[0] + boundary_length 	  > bot_state[1].pos[0] &&
			bot_state[0].pos[1] < bot_state[1].pos[1] + boundary_length &&
			boundary_length     + bot_state[0].pos[1] > bot_state[1].pos[1]) and bot_state :
													'''	 based on this logic
													 	(rect1.x < rect2.x + rect2.w &&
												        rect1.x + rect1.w > rect2.x &&
												        rect1.y < rect2.y + rect2.h &&
												        rect1.h + rect1.y > rect2.y) '''

		 	print(collision detected)
		 	disable_bot[0] = 1
		 else:
		 	disable_bot[0]=0
		 	disable_bot[1]=0
		time.sleep(0.1)

		
def main():

	proc1 = mp.Process(target=bot, args=(0,))
	proc2 = mp.Process(target=bot, args=(1,))
	start = True
	while True:

		got, frame = cap.read()
		image_array[:] = frame
		if got and start:
			start = False
			proc1.start()
			proc2.start()
		if (cv2.waitKey(1) == 27):
			break

		cv2.imshow("video", frame)

	proc1.terminate()
	proc2.terminate()
	cap.release() 
	cv2.destroyAllWindows()



if __name__ =='__main__':
	main()