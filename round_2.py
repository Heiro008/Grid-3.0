import cv2
import time
import numpy as np
from navigate_module import *
from round_2_data import *
import socket 
import multiprocessing as mp
import math
from operator import xor
import destination_path_mapper as dpm

bot_1_pos = mp.Queue()
bot_2_pos = mp.Queue()
bot_data = [bot_1_pos,bot_2_pos]

mp_array = mp.Array("I", int(np.prod((960, 1280, 3))))   # , lock=mp.Lock()  (480, 640, 3)
# create a numpy view of the array
image_array = np.frombuffer(mp_array.get_obj(), dtype="I").reshape((960, 1280, 3))

disable_bot = mp.Array('B',3)        # array to control the bot movement used by monitor func
frame_read = mp.Array('B',2)
special_path = mp.Array('B',2)
job_count = mp.Array('i',3)			# to specify the no of packages sorted

con1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
con2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


con1.connect(('192.168.21.187',8888))    	#187
con2.connect(('192.168.21.126',8888))		#197

bot_paths = dpm.parse_excel_data()			#list of path numbers corresponding to destinations of package
#bot_paths = [[0,1,2,3,4,5,6,7,8],[0,1,2,3,4,5,6,7,8]]
#bot_paths = [[8,8,8],[0,0,0]]

def send_msg(msg,con):
	#print(con)
	try:
		con.send(msg)
	except:
		pass

url = 'http://192.168.233.166:8080/video'

cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FPS, 60)
#video = cv2.VideoWriter('video4.mp4',cv2.VideoWriter_fourcc(*'MJPG'),30, (1440,1280))

 
def bot(bot_no,zone_no):

	if bot_no ==0:
		con = con1
	else:
		con = con2

	#print(con)
	c_time =0
	count =0
	flag = False

	# define a mechanism to map the path
	path_no = bot_paths[zone_no][job_count[zone_no]]
	#path_no = bot_no
	if bot_no==3:
		path_no = bot_paths[zone_no][job_count[zone_no%2]]
		if job_count[2]==0:
			path_no = 4 						# path 4 is the path from temp location to induct zone
	lower = color_def[bot_no][0]
	upper = color_def[bot_no][1]

	print(job_count[zone_no])

	path1 = path(path_no = path_no,zone_no=zone_no)
	center = None
	theta =0	
	angle =0
	c_time = time.time()
	is_correct = False
	while True:
		while not frame_read[bot_no]:				#pooling method 
			continue								#loop runs only when new frame is read
		frame_read[bot_no] = 0

		contor_detected = False

		frame = image_array.astype("uint8").copy()  # example of some processing done on the array
		#print(frame.shape,bot_no)

		#print(str(bot_no)+': ',time.time()-c_time)
		#c_time = time.time()
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
			if len(c)> 100:
				rect = cv2.minAreaRect(c)
				center = rect[0]				#center (x,y)
				path1.pos = center				#store the bot coordinates in bot_state class
				size = rect[1]
				angle = int(rect[2])
				contor_detected = True
				hyp = math.sqrt((path1.t_lim_offset-center[~path1.mov_dir])**2+(path1.center-center[path1.mov_dir])**2)
				#adj = math.fabs(path1.center-center[path1.mov_dir])
				opp = math.fabs(center[~path1.mov_dir]-path1.t_lim_offset)
				theta = int(math.degrees(math.asin(opp/hyp)))

		if contor_detected and count > 50:
			# stop the bot if collision is detected
			if disable_bot[bot_no]:
				print('diasabled')
				send_msg('p'.encode('utf-8'),con)
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
							send_msg('s{}\n'.format(path1.belt_msg).encode('utf-8'),con)
							if special_path[bot_no]:
								path1.special_path = 1
								special_path[bot_no]=0
						elif path1.turn_path == 2:
							send_msg('p'.encode('utf-8'),con)
							flag = True
						elif path1.turn_path == 3:				# for third bot
							disable_bot[bot_no] = 1
						else:
							send_msg((path1.t_msg+'\n').encode('utf-8'),con)
						time.sleep(0.010)
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
							send_msg('s{}\n'.format(path1.belt_msg).encode('utf-8'),con)
							if special_path[bot_no]:
								path1.special_path = 1
								special_path[bot_no]=0
						elif path1.turn_path == 2:
							send_msg('p'.encode('utf-8'),con)
							flag = True
						elif path1.turn_path == 3:				# for third bot
							disable_bot[bot_no] = 1
						else:
							send_msg((path1.t_msg+'\n').encode('utf-8'),con)
						time.sleep(0.010)
					#time.sleep(1)
					if flag:
						break
					path1.turn()

		bot_data[bot_no].put(path1)

		#cv2.imshow(str(bot_no),mask)

		if (cv2.waitKey(1) == 27):
			break
	if flag and job_count[path1.zone_no]<=8:
		if bot_no == 2:
			job_count[path1.zone_no]+=1

			job_count[2] = int(not job_count[2])
			if path1.path_no in range(6,9):
				zone_no = 3
			elif path1.path_no in range(3):
				zone_no = 4
			bot(bot_no,zone_no)
		else:
			job_count[path1.zone_no]+=1
			bot(bot_no,path1.zone_no)
	cv2.destroyAllWindows()
	

def monitor(): 			# monitors the bot coordinates and updates the control
	
	offset_map = {'W':[-120,0],
				  'E':[120,0],
				  'N':[0,-120],
				  'S':[0,120]
				}
	boundary = [70,160]      # width(horozontal) , height(vertical)
	bot_state = [None,None]
	flag = False
	boundary_length = 100
	while True:	
		for i in range(2):
			while not bot_data[i].empty():
				bot_state[i] = bot_data[i].get()
				flag = True
			# bot_state[].pos[0] = x coordinate 
		if flag:
			rect0_x = int(bot_state[0].pos[0] + offset_map[bot_state[0].curr_dir][0])
			rect0_y = int(bot_state[0].pos[1] + offset_map[bot_state[0].curr_dir][1])
			rect0_w = boundary[bot_state[0].mov_dir]
			rect0_h = boundary[~bot_state[0].mov_dir]
			rect1_x = int(bot_state[1].pos[0] + offset_map[bot_state[1].curr_dir][0])
			rect1_y = int(bot_state[1].pos[1] + offset_map[bot_state[1].curr_dir][1])
			rect1_w = boundary[bot_state[1].mov_dir] 	
			rect1_h = boundary[~bot_state[1].mov_dir]

			coll_img = np.zeros((960, 1280, 3),np.uint8) 
			#print(int(bot_state[0].pos[0]))
			cv2.circle(coll_img,(int(bot_state[0].pos[0]),int(bot_state[0].pos[1])),5,(0,0,255),-1)
			cv2.circle(coll_img,(int(bot_state[1].pos[0]),int(bot_state[1].pos[1])),5,(0,0,255),-1)

			cv2.rectangle(coll_img, (int(rect0_x-rect0_w/2),int(rect0_y-rect0_h/2)),(int(rect0_x+rect0_w/2),int(rect0_y+rect0_h/2)),(0,0,255),1)
			cv2.rectangle(coll_img, (int(rect1_x-rect1_w/2),int(rect1_y-rect1_h/2)),(int(rect1_x+rect1_w/2),int(rect1_y+rect1_h/2)),(0,0,255),1)
			
			coll_img = cv2.resize(coll_img,(int(coll_img.shape[1] * 50 / 100),int(coll_img.shape[0] * 50 / 100)))
			
			cv2.imshow("collision image",coll_img)
			
			if (cv2.waitKey(10) == 27):
				break
			if (rect0_x < rect1_x + rect1_w	and 
			    rect0_x + rect0_w > rect1_x and
				rect0_y < rect1_y + rect1_h and
				rect0_h + rect0_y > rect1_y) :
				'''											based on this logic
														 	(rect0.x < rect1.x + rect1.w &&
													        rect0.x + rect0.w > rect1.x &&
													        rect0.y < rect1.y + rect1.h &&
													        rect0.h + rect0.y > rect1.y)
				'''
				print('collision detected')
				
				if bot_state[0].is_reversed:
					disable_bot[1] = 1
				else :
					disable_bot[0] = 1

				if bot_state[0].is_reversed and bot_state[1].is_reversed:
					if bot_state[0].turn_path == 2:
						disable_bot[0] = 1
					else:
						disable_bot[1] = 0

			else:
				disable_bot[0]=0
				disable_bot[1]=0
			
			# check for special paths if none of the bot is in special_path mode {nand operation}
			if not (bot_state[0].special_path or bot_state[1].special_path):
				if bot_state[0].zone_no == 0:
					if (bot_state[1].path_no in range(3)) and (bot_state[0].path_no in range(6,9)):
						if (not (bot_state[0].is_reversed or bot_state[1].is_reversed)) and bot_state[0].sub_path>=1 and bot_state[1].sub_path>=1:
							special_path[0]=1
							special_path[1]=1
				else:
					if (bot_state[0].path_no in range(3)) and (bot_state[1].path_no in range(6,9)):
						if (not (bot_state[0].is_reversed or bot_state[1].is_reversed)) and bot_state[0].sub_path>=1 and bot_state[1].sub_path>=1:
							special_path[0]=1
							special_path[1]=1
			# define a method for selecting the special path

		time.sleep(0.15)
	cv2.destroyAllWindows()

		
def main():

	proc1 = mp.Process(target=bot, args=(0,0))
	proc2 = mp.Process(target=bot, args=(1,1))
	
	proc4 = mp.Process(target=monitor)
	start = True
	c_time = time.time()
	while True:
		#print('main: ',time.time()-c_time)
		#c_time = time.time()
		got, frame = cap.read()
		frame_read[0] = 1
		frame_read[1] = 1
		image_array[:] = frame
		if got and start:
			start = False
			proc1.start()
			proc2.start()
			proc4.start()
		if (cv2.waitKey(1) == 27):
			break
		frame = cv2.resize(frame,(int(frame.shape[1] * 50 / 100),int(frame.shape[0] * 50 / 100)))
		cv2.imshow("video", frame)

	proc1.terminate()
	proc2.terminate()

	proc4.terminate()
	cap.release() 
	cv2.destroyAllWindows()

if __name__ =='__main__':
	main()