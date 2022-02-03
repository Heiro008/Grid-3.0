# import the data for required round
from round_2_data import *

turn_msg ={
			'S':{'E':'e','W':'i'},
			'N':{'E':'i','W':'e'},
			'E':{'N':'e','S':'i'},
			'W':{'N':'i','S':'e'}
			}
class Path:
	def __init__(self,path_no=0,zone_no=0):
		#self.upper_limit = path_def[path_no][3][1]
		#self.lower_limit = path_def[path_no][3][0]
		#self.center = (self.upper_limit + self.lower_limit )/2
		 
		self.path_no = path_no

		#print(path_def[zone_no][path_no][0][0])

		self.sub_path=0
		self.curr_dir = path_def[zone_no][path_no][0][self.sub_path]
		self.t_dir = path_def[zone_no][path_no][0][self.sub_path+1]
		self.t_lim = path_def[zone_no][path_no][1][self.sub_path]
		self.t_lim_offset = path_def[zone_no][path_no][2][self.sub_path]
		self.turn_path = path_def[zone_no][path_no][4][self.sub_path]
		self.is_reversed = False
		if zone_no == 3:
			self.is_reversed = True
		self.temp = False
		self.pos = None
		self.zone_no = zone_no
		self.special_path = 0
		self.flag = True
		if zone_no == 1 and (path_no in [6,7,8]):
			self.belt_msg = 1
		else:
			self.belt_msg = 0
			if zone_no == 2:
				self.belt_msg = 0
			elif zone_no == 3:
				self.belt_msg =1
		#self.belt_msg = belt_dir[self.zone_no][self.path_no]
		if self.t_dir == 'N':
			self.center = path_def[zone_no][path_no][3][0] + 30
		else:
			self.center = path_def[zone_no][path_no][3][0] - 30

		self.assign_dir(path_def[zone_no][path_no][0][0])

	def turn(self):
		if not self.turn_path :
			if self.t_dir == 'N' or self.t_dir == 'S':
				self.center = self.t_lim + 30
				if self.is_reversed:
					self.center = self.t_lim + 40    # overshoot +- 10
			else:
				if self.zone_no == 0:
					self.center = self.t_lim - 30
					if self.is_reversed:
						self.center = self.t_lim - 30    # overshoot +- 10
				else:
					self.center = self.t_lim + 30
					if self.is_reversed:
						self.center = self.t_lim + 30   # overshoot +- 5

			#print('center ',self.center)
			
		else:
			if self.is_reversed:
				if self.t_dir == 'N' or self.t_dir == 'S':	
					self.center = self.center + 7
				else:
					if self.zone_no == 0:
						self.center = self.center - 10
					if self.zone_no == 1:
						self.center = self.center - 5


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
				if self.zone_no == 2:
					self.zone_no = 3
				elif self.zone_no == 3:
					self.zone_no = 2
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

		if not self.turn_path :
			self.t_msg = turn_msg[dir][self.t_dir]

class bot_state:
	def __init__(self):
		self.pos = None
		self.is_reversed = None
		self.curr_dir = None
		self.mov_dir = None