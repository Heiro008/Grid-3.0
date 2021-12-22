# import the data for required round
from round_2_data import *

turn_msg ={
			'S':{'E':'e','W':'i'},
			'N':{'E':'i','W':'e'},
			'E':{'N':'e','S':'i'},
			'W':{'N':'i','S':'e'}
			}
class path:
	def __init__(self,path_no=0,zone_no=0):
		#self.upper_limit = path_def[path_no][3][1]
		#self.lower_limit = path_def[path_no][3][0]
		#self.center = (self.upper_limit + self.lower_limit )/2
		self.center = path_def[zone_no][path_no][3][0]
		self.path_no = path_no

		#print(path_def[zone_no][path_no][0][0])

		self.sub_path=0
		self.curr_dir = path_def[zone_no][path_no][0][self.sub_path]
		self.t_dir = path_def[zone_no][path_no][0][self.sub_path+1]
		self.t_lim = path_def[zone_no][path_no][1][self.sub_path]
		self.t_lim_offset = path_def[zone_no][path_no][2][self.sub_path]
		self.turn_path = path_def[zone_no][path_no][4][self.sub_path]
		self.is_reversed = False
		self.temp = False
		self.pos = None
		self.zone_no = zone_no
		self.special_path = 0
		self.flag = True
		if zone_no == 1 and (path_no in [6,7,8]):
			self.belt_msg = 1
		else:
			self.belt_msg = 0
		#self.belt_msg = belt_dir[self.zone_no][self.path_no]

		self.assign_dir(path_def[zone_no][path_no][0][0])

	def turn(self):
		if not self.turn_path :
			#self.upper_limit = self.t_lim +5 
			#self.lower_limit = self.t_lim -5
			self.center = self.t_lim # +50			
		'''
		# for round 1
		if self.sub_path !=1:
			self.upper_limit = self.t_lim +5 
			self.lower_limit = self.t_lim -5
			self.center = self.t_lim # +50'''

		if self.special_path and self.flag:
			self.sub_path = 0
			self.flag = False

		if not self.special_path:
			self.sub_path += 1
			self.curr_dir = self.t_dir

			if len(path_def[self.zone_no][self.path_no][1])>=self.sub_path:
				self.t_dir = path_def[self.zone_no][self.path_no][0][self.sub_path+1]
				self.t_lim = path_def[self.zone_no][self.path_no][1][self.sub_path]
				self.t_lim_offset = path_def[self.zone_no][self.path_no][2][self.sub_path]
				self.turn_path = path_def[self.zone_no][self.path_no][4][self.sub_path]
		else:
			# assign special paths and change zone number
			if self.sub_path == 0 :
				self.zone_no = int(not self.zone_no)

				print('path=',self.path_no)
				self.center = special_path_def[self.zone_no][self.path_no][3][0]
				self.curr_dir = special_path_def[self.zone_no][self.path_no][0][self.sub_path]
				self.t_dir = special_path_def[self.zone_no][self.path_no][0][self.sub_path+1]
				self.t_lim = special_path_def[self.zone_no][self.path_no][1][self.sub_path]
				self.t_lim_offset = special_path_def[self.zone_no][self.path_no][2][self.sub_path]
				self.turn_path = special_path_def[self.zone_no][self.path_no][4][self.sub_path]
				self.sub_path +=1 

			else:
				self.curr_dir = self.t_dir
				if len(special_path_def[self.zone_no][self.path_no][1])>=self.sub_path:
					self.t_dir = special_path_def[self.zone_no][self.path_no][0][self.sub_path+1]
					self.t_lim = special_path_def[self.zone_no][self.path_no][1][self.sub_path]
					self.t_lim_offset = special_path_def[self.zone_no][self.path_no][2][self.sub_path]
					self.turn_path = special_path_def[self.zone_no][self.path_no][4][self.sub_path]
				self.sub_path += 1
				
			


		self.assign_dir(self.curr_dir)

		#print(self.center)

	def assign_dir(self,dir):
		if dir =='N':
			self.mov_dir = 0  
			self.l_dir = 'r' 
			self.r_dir = 'l'
			if self.is_reversed:
				self.l_dir = 'l' 
				self.r_dir = 'r'
			'''
			if (dir == 'S' and not(self.is_reversed)) or self.temp:
				self.l_dir = 'l' 
				self.r_dir = 'r'
				self.temp = True
			'''
		elif dir == 'S':
			self.mov_dir = 0
			self.l_dir = 'l' 
			self.r_dir = 'r'
			if self.is_reversed:
				self.l_dir = 'r' 
				self.r_dir = 'l'
		elif dir == 'W':
			self.mov_dir = 1 	
			self.l_dir = 'l'
			self.r_dir = 'r'
			if self.is_reversed:
				self.l_dir = 'r' 
				self.r_dir = 'l'
		elif dir =='E':
			self.mov_dir = 1 	
			self.l_dir = 'r'
			self.r_dir = 'l'
			if self.is_reversed:
				self.l_dir = 'l'
				self.r_dir = 'r'
		'''
		else:
			self.mov_dir = 1 	
			self.l_dir = 'l'
			self.r_dir = 'r'
		'''
			#self.l_dir = 'move down' l
			#self.r_dir = 'move up' r
		'''
		if self.t_dir == 'S' or self.t_dir =='W':
			self.t_msg = 'e'    # default = e
			if self.is_reversed:
				self.t_msg = 'i'
		else:
			self.t_msg = 'i'
		'''
		if not self.turn_path :
			self.t_msg = turn_msg[dir][self.t_dir]

class bot_state:
	def __init__(self):
		self.pos = None
		self.is_reversed = None
		self.curr_dir = None
		self.mov_dir = None