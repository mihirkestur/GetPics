from PIL import Image
from PIL import ImageTk
import tkinter as tk
import threading,datetime,imutils,cv2,os,time,glob
from tkinter import filedialog
import numpy as np

class GetPic:
	def __init__(self, cap):
		self.pause = False
		self.piccount = 0
		self.max_pics = 0
		self.outputpath = ""
		self.cap = cap
		self.frame = None
		self.thread = None
		self.stopEvent = None
		self.flag = False
		self.root = tk.Tk()
		self.panel = None
		def submit(self):
			if max_pics.get("1.0","end-1c") == "":
				print("[INFO] Not possible, please enter a number")
			else:
				self.max_pics = int(float(max_pics.get("1.0","end-1c")))
		btn_submit = tk.Button(self.root, text="Submit",command = lambda : submit(self) )
		btn_submit.pack(side="bottom", fill="x", expand="yes", padx=10,pady=10)
		max_pics = tk.Text(self.root, height=1, width=5)
		max_pics.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)
		btn_start = tk.Button(self.root, text="Start snapshots",command = self.takeSnapshot )
		btn_start.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)
		btn_stop = tk.Button(self.root, text="Stop snapshots",command = self.onClose)
		btn_stop.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)
		btn_save = tk.Button(self.root, text="Save directory",command = self.save_path )
		btn_save.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)
		btn_pause = tk.Button(self.root, text="Pause/Resume taking pictures",command = self.pause_resume )
		btn_pause.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)
		self.stopEvent = threading.Event()
		self.thread = threading.Thread(target=self.videoLoop, args=())
		self.thread.start()
		self.root.wm_title("Take pictures")

	def videoLoop(self):
		try:
			while not self.stopEvent.is_set():
				if self.pause == True: continue
				_, self.frame = self.cap.read()
				self.frame = cv2.resize(self.frame, (300,225), interpolation=cv2.INTER_LINEAR)
				img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
				image = Image.fromarray(img)
				image = ImageTk.PhotoImage(image)
				if self.panel is None:
					self.panel = tk.Label(image=image)
					self.panel.image = image
					self.panel.pack(side="top", padx=10, pady=10)
				else:
					self.panel.configure(image=image)
					self.panel.image = image
					if self.flag:
						if (self.piccount != self.max_pics ):
							time.sleep(0.5)
							filename = "{}.jpg".format(str(self.piccount))
							path = os.path.sep.join((self.outputpath, filename))
							cv2.imwrite(path, self.frame)
							self.piccount = self.piccount + 1
							print("[INFO] saved {}".format(filename))
						else:
							self.flag = False
		except RuntimeError as e:
			print("[INFO] caught a RuntimeError")

	def takeSnapshot(self):
		if self.outputpath == "":
			self.save_path()
		if self.max_pics == 0:
			print("[INFO] Please enter number")
			return
		self.flag = True

	def onClose(self):
		self.flag = False
		print("[INFO] Finished taking pictures")
		self.stopEvent.set()
		cap.release()
		cv2.destroyAllWindows()
		self.root.quit()
	def pause_resume(self):
		if self.pause == False:
			self.pause = True
		else:
			self.pause = False
	def save_path(self):
	    self.outputpath = filedialog.askdirectory()

print("[INFO] Starting the camera...")
cap = cv2.VideoCapture(1)
instance = GetPic(cap)
instance.root.mainloop()

