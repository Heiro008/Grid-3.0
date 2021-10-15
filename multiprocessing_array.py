# implemented using array method

import multiprocessing as mp
import cv2
import time 
import numpy as np

cap = cv2.VideoCapture(0)


def bot(shared_memory,bot_no):
	mp_array, np_array = shared_memory
	while True:
		_ = np_array.astype("uint8").copy()  # example of some processing done on the array
		print(_.shape,bot_no)
		cv2.imshow(str(bot_no),_)
		if (cv2.waitKey(1) == 27):
			break
		'''
		while True:
			try:
				mp_array.release()
				break
			# it already unlocked, wait until its locked again which means a new frame is ready
			except ValueError:
				pass
		'''
def main():
	n_frames = 100
	mp_array = mp.Array("I", int(np.prod((480, 640, 3))))   # , lock=mp.Lock()
	# create a numpy view of the array
	np_array = np.frombuffer(mp_array.get_obj(), dtype="I").reshape((480, 640, 3))
	shared_memory = (mp_array, np_array)
	proc1 = mp.Process(target=bot,
	                  args=( shared_memory,0))
	proc2 = mp.Process(target=bot,
	                  args=( shared_memory,1))

	proc1.start()
	proc2.start()

	while True:

		got, frame = cap.read()

		if (cv2.waitKey(1) == 27):
			break

		
		#mp_array.acquire()
		np_array[:] = frame # produce a fresh array
		
		cv2.imshow("video", frame)	


	proc.terminate()
	proc1.terminate()
	proc2.terminate()
	cap.release() 
	cv2.destroyAllWindows()


	
if __name__ == '__main__':
	main()

