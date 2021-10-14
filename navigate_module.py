from round_1_data import *

class path:
	def __init__(self,start_dir='W',path_no=0):
		self.upper_limit = path_def[path_no][3][1]
		self.lower_limit = path_def[path_no][3][0]
		self.center = (self.upper_limit + self.lower_limit )/2
		self.path_no = path_no
		print(path_def[path_no][0][0])
		self.sub_path=0
		self.curr_dir = path_def[path_no][0][self.sub_path]
		self.t_dir = path_def[path_no][0][self.sub_path+1]
		self.t_lim = path_def[path_no][1][self.sub_path]
		self.t_lim_offset = path_def[path_no][2][self.sub_path]
		self.turn_path = path_def[path_no][4][self.sub_path]
		self.is_reversed = False
		self.temp = False
		self.assign_dir(path_def[path_no][0][0])
	def turn(self):
		if not self.turn_path :
			self.upper_limit = self.t_lim +5 
			self.lower_limit = self.t_lim -5
			self.center = self.t_lim # +50			
		'''
		# for round 1
		if self.sub_path !=1:
			self.upper_limit = self.t_lim +5 
			self.lower_limit = self.t_lim -5
			self.center = self.t_lim # +50'''
			
		self.assign_dir(self.t_dir)

		self.sub_path += 1
		self.curr_dir = self.t_dir

		if len(path_def[self.path_no][1])>=self.sub_path:
			self.t_dir = path_def[self.path_no][0][self.sub_path+1]
			self.t_lim = path_def[self.path_no][1][self.sub_path]
			self.t_lim_offset = path_def[self.path_no][2][self.sub_path]
			self.turn_path = path_def[self.path_no][4][self.sub_path]

		print(self.upper_limit,self.lower_limit)

	def assign_dir(self,dir):
		if dir =='S' or dir =='N':
			self.mov_dir = 0  

			self.l_dir = 'r' 
			self.r_dir = 'l'
			if (dir == 'S' and not(self.is_reversed)) or self.temp:
				self.l_dir = 'l' 
				self.r_dir = 'r'
				self.temp = True
			#self.l_dir = 'move right' 
			#self.r_dir = 'move left' 
		else:
			self.mov_dir = 1 
			self.l_dir = 'l'
			self.r_dir = 'r'
			#self.l_dir = 'move down' l
			#self.r_dir = 'move up' r
		if self.t_dir == 'S' or self.t_dir =='W':
			self.t_msg = 'e'    # default = e
		else:
			self.t_msg = 'i'

class bot_state:
	def __init__(self):
		self.pos = None
		self.is_reversed = None