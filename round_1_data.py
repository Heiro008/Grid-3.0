color_def = [[(170,116,153),(210,255,255)],     #red
			 [(51,135,113),(73,255,255)],		#green
			 [(149,119,105),(170,255,255)],		#pink
			 [(117,103,70),(136,190,232)]]		#violet


bot = [ '192.168.251.7',
		'192.168.251.187',
		'192.168.43.126',
		'192.168.43.197']
# deifne 1 extra turn direction and limit and directions > limits by 1
is_round_1 = False
# pixel range 1200x720												
path_def = [[['W','N','S','E','E'],[175, 100,515,655], [0,     0,650,720],[510,520]],
			[['W','N','S','E','E'],[110, 100,580,655], [0,     0,780,720],[575,585]],
			[['W','S','N','E','E'],[120,1140,645,650], [0,  1300,300,720],[640,650]],
			[['W','S','N','E','E'],[185,1140,720,645], [0,  1300,300,720],[715,725]],
			[['W','S','N','E','E'],[500,500,340,1200], [400, 600,240,720],[340,350]],	
			[['W','E','E'],[100,600,0],[120,130]],
			[['W','E','E'],[100,600,0],[140,150]],
			[['W','E','E'],[100,600,0],[160,170]],
			[['W','E','E'],[100,600,0],[180,190]]]



#['N','W','W','S','S'],[500,1000,500,0],[500,510]