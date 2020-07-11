from PIL import Image
from PIL import ImageTk
import tkinter as tk
import threading,datetime,cv2,os,time,imutils
from tkinter import filedialog
import numpy as np

class GetPic:
	def __init__(self):
		self.cap = cv2.VideoCapture(1)
		self.root = tk.Tk()
		self.root.geometry("1080x600")
		self.rate = 1
		self.size = (300,225)
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
		btn_close.place(x=850,y=600)
		btn_submit = tk.Button(self.root, text="Submit",command = self.submit )
		btn_submit.place(x=850,y=550)
		self.size_text = tk.Text(self.root, height=1, width=5)
		self.size_text.place(x=850,y=500)
		self.lbl_size = tk.Label(self.root, text = "Enter the width of the pictures (in px, default is 300 x 225 px)")
		self.lbl_size.place(x=700,y=450)
		self.rate_text = tk.Text(self.root, height=1, width=5)
		self.rate_text.place(x=850,y=400)
		self.lbl_rate = tk.Label(self.root, text = "Enter rate at which the pictures should be taken (in seconds, default is 1 picture per second)")
		self.lbl_rate.place(x=700,y=350)
		self.max_text = tk.Text(self.root, height=1, width=5)
		self.max_text.place(x=850,y=300)
		self.lbl_max_pic = tk.Label(self.root, text = "Enter maximum number of pictures to be taken")
		self.lbl_max_pic.place(x=850,y=250)
		btn_start = tk.Button(self.root, text="Start snapshots",command = self.takeSnapshot )
		btn_start.place(x=850,y=200)
		btn_save = tk.Button(self.root, text="Save directory",command = self.save_path )
		btn_save.place(x=850,y=150)
		btn_pause = tk.Button(self.root, text="Pause/Resume taking pictures",command = self.pause_resume )
		btn_pause.place(x=850,y=100)
		self.signal = tk.Label(self.root, text = "Indicator: Pictures will be taken once start snapshots is pressed")
		self.signal.place(x=450,y=50)
		self.stopEvent = threading.Event()
		self.thread = threading.Thread(target=self.videoLoop, args=())
		self.thread.start()
		self.root.wm_title("Take pictures")

	def videoLoop(self):
		try:
			while not self.stopEvent.is_set():
				_, self.frame = self.cap.read()
				self.frame = imutils.resize(self.frame,self.size[0])
				img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
				image = Image.fromarray(img)
				image = ImageTk.PhotoImage(image)
				if self.panel is None:
					self.panel = tk.Label(image=image)
					self.panel.image = image
					self.panel.place(x=0,y=0)
				else:
					self.panel.configure(image=image)
					self.panel.image = image
					if self.flag == True and self.pause == False:
						if (self.piccount != self.max_pics ):
							time.sleep(self.rate)
							filename = "{}.jpg".format(str(self.piccount + 1))
							cv2.imwrite(os.path.sep.join((self.outputpath, filename)), img)
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
