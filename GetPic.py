from PIL import Image
from PIL import ImageTk
import tkinter as tk
import threading,datetime,cv2,os,time,glob
from tkinter import filedialog
import numpy as np

class GetPic:
	def __init__(self):
		self.cap = cv2.VideoCapture(0)
		self.root = tk.Tk()
		self.rate = 1
		self.size = (300,300)
		self.pause = False
		self.piccount = 0
		self.max_pics = 0
		self.outputpath = ""
		self.frame = None
		self.thread = None
		self.stopEvent = None
		self.flag = False
		self.panel = None
		btn_close = tk.Button(self.root, text="Close",command = self.close)
		btn_close.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)
		btn_submit = tk.Button(self.root, text="Submit",command = self.submit )
		btn_submit.pack(side="bottom", fill="x", expand="yes", padx=10,pady=10)
		self.size_text = tk.Text(self.root, height=1, width=5)
		self.size_text.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)
		self.lbl_size = tk.Label(self.root, text = "Enter the size of the pictures in the form of 'a,b' (in px, default is 300 x 300 px)")
		self.lbl_size.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)
		self.rate_text = tk.Text(self.root, height=1, width=5)
		self.rate_text.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)
		self.lbl_rate = tk.Label(self.root, text = "Enter rate at which the pictures should be taken (in seconds, default is 1 picture per second)")
		self.lbl_rate.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)
		self.max_text = tk.Text(self.root, height=1, width=5)
		self.max_text.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)
		self.lbl_max_pic = tk.Label(self.root, text = "Enter maximum number of pictures to be taken")
		self.lbl_max_pic.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)
		btn_start = tk.Button(self.root, text="Start snapshots",command = self.takeSnapshot )
		btn_start.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)
		btn_save = tk.Button(self.root, text="Save directory",command = self.save_path )
		btn_save.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)
		btn_pause = tk.Button(self.root, text="Pause/Resume taking pictures",command = self.pause_resume )
		btn_pause.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)
		self.signal = tk.Label(self.root, text = "Pictures will be taken once start snapshots is pressed")
		self.signal.pack(side="bottom", fill="both", expand="yes", padx=10,pady=10)
		self.stopEvent = threading.Event()
		self.thread = threading.Thread(target=self.videoLoop, args=())
		self.thread.start()
		self.root.wm_title("Take pictures")

	def videoLoop(self):
		try:
			while not self.stopEvent.is_set():
				if self.pause == True: continue
				_, self.frame = self.cap.read()
				self.frame = cv2.resize(self.frame, self.size, interpolation=cv2.INTER_LINEAR)
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
							time.sleep(self.rate)
							filename = "{}.jpg".format(str(self.piccount + 1))
							path = os.path.sep.join((self.outputpath, filename))
							cv2.imwrite(path, self.frame)
							self.piccount = self.piccount + 1
							self.signal["text"] = "Saved {}".format(filename)
						else:
							self.flag = False
		except RuntimeError as e:
			print("[INFO] caught a RuntimeError")
	def submit(self):
		if self.max_text.get("1.0","end-1c") == "":
			self.signal["text"] = "Please enter the number of pictures to be taken"
		else:
			if int(float(self.max_text.get("1.0","end-1c"))) <= 0:
				self.signal["text"] = "Please enter a positive integer only"
				return
			self.max_pics = int(float(self.max_text.get("1.0","end-1c")))
		if self.size_text.get("1.0","end-1c") != "":
			self.size = tuple([int(float(i)) for i in (self.size_text.get("1.0","end-1c")).split(',')])
			print(self.size)
		if self.rate_text.get("1.0","end-1c") != "":
			self.rate = float(self.rate_text.get("1.0","end-1c"))

	def takeSnapshot(self):
		if self.outputpath == "":
			self.save_path()
		self.flag = True

	def close(self):
		self.signal["text"] = "Finished taking pictures"
		self.flag = False
		self.cap.release()
		self.stopEvent.set()
		cv2.destroyAllWindows()
		self.root.quit()
	def pause_resume(self):
		if self.pause == False:
			self.signal["text"] = "Paused"
			self.pause = True
		else:
			self.signal["text"] = "Resumed"
			self.pause = False
	def save_path(self):
	    self.outputpath = filedialog.askdirectory()

instance = GetPic()
instance.root.mainloop()
