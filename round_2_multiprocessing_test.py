# implementation using queue method


import multiprocessing as mp
import cv2
import time 

image = mp.Queue()
cap = cv2.VideoCapture(0)
class temp:
	def __init__(self,n):
		self.no = n
def func(n):
	return n

class bot:
	def __init__(self,n):
		self.pos = n
		self.coordinates = mp.Queue()

bot_1_pos = mp.Queue()
bot_2_pos = mp.Queue()
bot_pos = [bot_1_pos,bot_2_pos]

def bot_1(a):
	got = False
	t1 = temp(10)
	if a == 1:
		b = bot(1)
	else:
		b = bot(2)

	while True:
		while not image.empty():
			print('process 1 ',t1.no,func(a))
			data = image.get()
			got = True
		if got:
			image.put(data)
			print(data.shape)	
			bot_pos[a].put(data[0][1])
			got = False
			
			if cv2.waitKey(1)==27:
				break
			cv2.imshow(str(a),data)
		


def bot_2(a):
	t1 = temp(20)
	got = False
	while True:
		while not image.empty():
			print('process 2 ',t1.no,func(a))
			data = image.get()
			print(data.shape)
		if got:
			print(data.shape)
			got = False
		time.sleep(0.1)	


def main():
	p1 = mp.Process(target=bot_1,args=(0,))
	p2 = mp.Process(target=bot_1,args=(1,))
	p1.start()
	p2.start()

	while True:

		got, frame = cap.read()
		image.put(frame)
		
		if (cv2.waitKey(1) == 27):
			break

		cv2.imshow("video", frame)


	p1.terminate()
	#p2.terminate()
	cap.release() 
	cv2.destroyAllWindows()
	print(bot_pos[0].get())
	print(bot_pos[1].get())
	quit()
	
if __name__ == '__main__':
	main()



