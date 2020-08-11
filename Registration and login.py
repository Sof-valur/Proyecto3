# Import modules #
import tkinter
import os

import face_recognition
import cv2
import pickle
import os
import numpy as np

import tkinter as tk
from tkinter import messagebox

from pathlib import Path
import glob
 

# class: Dlib Face Unlock #
# Purpose: This class will compare the live camera with the photos in the directory to see if they are the same
class Dlib_Face_Unlock:
	""" When this class is run at startup it will look for any changes in the system, be it an added or removed face """
	def __init__(self):
		""" This is to detect if the directory is found or not """
		try:
			""" This will open the existing pickle file to load in the encoded faces of the users who has sign up for the service """
			with open (r'C:\Users\ExtremeTech\Source\Repos\Proyecto31\labels.pickle', 'rb') as self.f:
				self.og_labels = pickle.load(self.f)
			print(self.og_labels)
			""" error checking """
		except FileNotFoundError:
			""" A message if the face is not found"""
			print("No label.pickle file detected, will create required pickle files")

		""" This will be used to for selecting the photos """
		self.current_id = 0
		""" Creating a blank ids dictionary """
		self.labels_ids = {}
		""" This is the directory where all the users are stored """
		self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		self.image_dir = os.path.join(self.BASE_DIR, 'images')
		for self.root, self.dirs, self.files in os.walk(self.image_dir):
			for self.file in self.files:
				if self.file.endswith('png') or self.file.endswith('jpg'):
					self.path = os.path.join(self.root, self.file)
					self.label = os.path.basename(os.path.dirname(self.path)).replace(' ', '-').lower()
					if not self.label in self.labels_ids:
						self.labels_ids[self.label] = self.current_id
						self.current_id += 1
						self.id = self.labels_ids[self.label]

		print(self.labels_ids)

		self.og_labels=0
		if self.labels_ids != self.og_labels:
			""" If the dictionary change then the new dictionary will be dump into the pickle file """
			with open('labels.pickle', 'wb') as self.file:
				pickle.dump(self.labels_ids, self.file)

			self.known_faces = []
			for self.i in self.labels_ids:
				noOfImgs = len([filename for filename in os.listdir('images/' + self.i)
									if os.path.isfile(os.path.join('images/' + self.i, filename))])
				print(noOfImgs)
				for imgNo in range(1,(noOfImgs+1)):
					self.directory = os.path.join(self.image_dir, self.i, str(imgNo)+'.png')
					self.img = face_recognition.load_image_file(self.directory)
					self.img_encoding = face_recognition.face_encodings(self.img)[0]
					self.known_faces.append([self.i, self.img_encoding])
			print(self.known_faces)
			print("No Of Imgs"+str(len(self.known_faces)))
			with open('KnownFace.pickle','wb') as self.known_faces_file:
				pickle.dump(self.known_faces, self.known_faces_file)
		else:
			with open (r'C:\Users\ExtremeTech\Source\Repos\Proyecto31\KnownFace.pickle','rb') as self.faces_file:
				self.known_faces = pickle.load(self.faces_file)
			print(self.known_faces) 

	# The purpose of this function is to turn the device's camera on #
	def ID(self):
		""" Turning on the camera to get a photo of the user """
		self.cap = cv2.VideoCapture(0)
		self.running = True
		self.face_names = []
		while self.running == True:
			self.ret, self.frame = self.cap.read()
			self.small_frame = cv2.resize(self.frame, (0,0), fx = 0.5, fy = 0.5)
			self.rgb_small_frame = self.small_frame[:, :, ::-1]
			if self.running:
				self.face_locations = face_recognition.face_locations(self.frame)
				self.face_encodings = face_recognition.face_encodings(self.frame, self.face_locations)
				""" Creating a names list to append the users identify into """
				self.face_names = []
				for self.face_encoding in self.face_encodings:
					""" Looping though the known_faces dictionary """
					for self.face in self.known_faces:
						self.matches = face_recognition.compare_faces([self.face[1]], self.face_encoding)
						print(self.matches)
						self.name = 'Unknown'
						self.face_distances = face_recognition.face_distance([self.face[1]], self.face_encoding)
						self.best_match = np.argmin(self.face_distances)
						print(self.best_match)
						print('This is the match in best match', self.matches[self.best_match])
						if self.matches[self.best_match] == True:
							self.running = False
							self.face_names.append(self.face[0])
							break
						next
			print("The best match(es) is"+str(self.face_names))
			self.cap.release()
			cv2.destroyAllWindows()
			break
		return self.face_names


# This function is in charge of create new users or add a new photo of the user #
def register():
	""" Create images folder """
	if not os.path.exists("images"):
		os.makedirs("images")
	""" Create folder of person (IF NOT EXISTS) in the images folder """
	Path("images/"+name.get()).mkdir(parents=True, exist_ok=True)
	#Obtain the number of photos already in the folder
	numberOfFile = len([filename for filename in os.listdir('images/' + name.get())
						if os.path.isfile(os.path.join('images/' + name.get(), filename))])
	""" Add 1 because we start at 1 """
	numberOfFile+=1
	""" Take a photo code """
	cam = cv2.VideoCapture(0)
	
	cv2.namedWindow("test")

	while True:
		ret, frame = cam.read()
		cv2.imshow("test", frame)
		if not ret:
			break
		k = cv2.waitKey(1)
		
		if k % 256 == 27:
			""" ESC pressed """
			print("Escape hit, closing...")
			cam.release()
			cv2.destroyAllWindows()
			break
		elif k % 256 == 32:
			""" SPACE pressed """
			img_name = str(numberOfFile)+".png"
			cv2.imwrite(img_name, frame)
			print("{} written!".format(img_name))
			os.replace(str(numberOfFile)+".png", "images/"+name.get().lower()+"/"+str(numberOfFile)+".png")
			cam.release()
			cv2.destroyAllWindows()
			break
	raiseFrame(loginFrame)


# This function is the login #
def login1():
	""" After someone has registered, the face scanner needs to load again with the new face """
	dfu = Dlib_Face_Unlock()
	""" Will return the user's name as a list, will return an empty list if no matches """
	user = dfu.ID()
	if user == []:
		messagebox.showerror("Alert", "Face Not Recognised")
		return
	
	os.system("python MainWindow.py") 
	

# Delete login success window function #
def del_pass_not_recognized():
    screen_4.destroy()


# Delete login success window function #
def del_user_not_found():
    screen_5.destroy()


# Login success function #
def login_success():
    screen_8 = tkinter.Toplevel(screen)
    screen_8.title("Dashboard")
    screen_8.geometry("700x500")
    tkinter.Label(screen_8, text="Welcome to the dashboard").pack()
    tkinter.Button(screen_8, text="Create notes").pack()
    tkinter.Button(screen_8, text="View notes").pack()
    tkinter.Button(screen_8, text="Delete notes").pack()


# password not recognized function #
def password_not_recognized():
    global screen_4
    screen_4 = tkinter.Toplevel(screen)
    screen_4.title("Success")
    screen_4.geometry("700x500")
    tkinter.Label(screen_4, text="Password Error").pack()
    tkinter.Button(screen_4, text="OK", command=del_pass_not_recognized()).pack()


# username not found function #
def username_not_found():
    global screen_5
    screen_5 = tkinter.Toplevel(screen)
    screen_5.title("Success")
    screen_5.geometry("700x500")
    tkinter.Label(screen_5, text="Username not found").pack()
    tkinter.Button(screen_5, text="OK", command=del_user_not_found()).pack()


# Register use function #
def register_user():
	nombre_info = nombre.get()
	edad_info = edad.get()
	cedula_info = cedula.get()
	email_info = email.get()
	residencia_info = residencia.get()  

	file = open(nombre_info, "w")
	file.write(nombre_info + "\n")
	file.write(edad_info + "\n")
	file.write(cedula_info + "\n")
	file.write(email_info + "\n")
	file.write(residencia_info + "\n") 
	file.close()

	if not os.path.exists("images"):
		os.makedirs("images")

	"""Create folder of person (IF NOT EXISTS) in the images folder """
	Path("images/"+nombre.get()).mkdir(parents=True, exist_ok=True)
	""" Obtain the number of photos already in the folder """
	numberOfFile = len([filename for filename in os.listdir('images/' + nombre.get())
						if os.path.isfile(os.path.join('images/' + nombre.get(), filename))])
	""" Add 1 because we start at 1 """
	numberOfFile+=1
	""" Take a photo code """
	cam = cv2.VideoCapture(0)
	
	cv2.namedWindow("test")

	while True:
		ret, frame = cam.read()
		cv2.imshow("test", frame)
		if not ret:
			break
		k = cv2.waitKey(1)
		
		if k % 256 == 27:
			# ESC pressed
			print("Escape hit, closing...")
			cam.release()
			cv2.destroyAllWindows()
			break
		elif k % 256 == 32:
			# SPACE pressed
			img_name = str(numberOfFile)+".png"
			cv2.imwrite(img_name, frame)
			print("{} written!".format(img_name))
			os.replace(str(numberOfFile)+".png", "images/"+nombre.get().lower()+"/"+str(numberOfFile)+".png")
			cam.release()
			cv2.destroyAllWindows()
			break

	nombre_entry.delete(0, tkinter.END)
	edad_entry.delete(0, tkinter.END)
	cedula_entry.delete(0, tkinter.END)
	email_entry.delete(0, tkinter.END)
	residencia_entry.delete(0, tkinter.END)

	tkinter.Label(screen_1, text="Registration Success", fg="green", font=("Times New Roman", 11)).pack()


# Login verify function #
def login_verify():
	username_1 = username_verify.get()
	password_1 = password_verify.get()
	username_entry_1.delete(0, tkinter.END)
	password_entry_1.delete(0, tkinter.END)
	list_of_files = os.listdir()
	if username_1 in list_of_files:
		file_1 = open(username_1, "r")
		verify = file_1.read().splitlines()
		if password_1 in verify:
			login_success()
		else:
			password_not_recognized()
	else:
		username_not_found()


# Register function #
def register():
	""" Register screen variable """
	global screen_1
	screen_1 = tkinter.Toplevel(screen)
	screen_1.title("Register")
	screen_1.geometry("700x500")

	global nombre
	global edad
	global cedula
	global email
	global residencia
	global nombre_entry
	global edad_entry
	global cedula_entry
	global email_entry
	global residencia_entry

	nombre = tkinter.StringVar()
	edad = tkinter.StringVar()
	cedula = tkinter.StringVar()
	email = tkinter.StringVar()
	residencia = tkinter.StringVar()
	""" Displaying username and password on screen """
	tkinter.Label(screen_1, text="Please enter details below").pack()
	tkinter.Entry(screen_1, text="")
	tkinter.Label(screen_1, text="Nombre Completo *").pack()
	nombre_entry = tkinter.Entry(screen_1, textvariable=nombre)
	nombre_entry.pack()
	tkinter.Label(screen_1, text="Edad *").pack()
	edad_entry = tkinter.Entry(screen_1, textvariable=edad)
	edad_entry.pack()
	tkinter.Label(screen_1, text="Cedula *").pack()
	cedula_entry = tkinter.Entry(screen_1, textvariable=cedula)
	cedula_entry.pack()
	tkinter.Label(screen_1, text="Email *").pack()
	email_entry = tkinter.Entry(screen_1, textvariable=email)
	email_entry.pack()
	tkinter.Label(screen_1, text="Residencia *").pack()
	residencia_entry = tkinter.Entry(screen_1, textvariable=residencia)
	residencia_entry.pack()

	""" Register button """
	tkinter.Label(screen_1, text="").pack()
	tkinter.Button(screen_1, text="Register", width=10, height=1, command=register_user).pack()


# Login function #
def login():
    global screen_2
    screen_2 = tkinter.Toplevel(screen)
    screen_2.title("Login")
    screen_2.geometry("700x500")
    tkinter.Label(screen_2, text="Please enter details below to login").pack()
    tkinter.Entry(screen_2, text="")

    global username_verify
    global password_verify

    username_verify = tkinter.StringVar()
    password_verify = tkinter.StringVar()

    global username_entry_1
    global password_entry_1

    tkinter.Label(screen_2, text="Username *").pack()
    username_entry_1 = tkinter.Entry(screen_2, textvariable=username_verify)
    username_entry_1.pack()
    tkinter.Label(screen_2, text="").pack()
    tkinter.Label(screen_2, text="Password *").pack()
    password_entry_1 = tkinter.Entry(screen_2, textvariable=password_verify)
    password_entry_1.pack()
    tkinter.Label(screen_2, text="").pack()
    tkinter.Button(screen_2, text="Login", width=10, height=1, command=login_verify).pack()


# Function for main screen #
def main_screen():
    # screen variables and buttons #
    global screen
    screen = tkinter.Tk()
    screen.geometry("700x500")
    screen.title("Registration")
    tkinter.Label(text="REGISTRATION", bg="grey", width="500", height="2", font=("Times New Roman", 13)).pack()
    tkinter.Label(text="").pack()
    tkinter.Button(text="Login", height="2", width="30", command=login1).pack()
    tkinter.Label(text="").pack()
    tkinter.Button(text="Register", height="2", width="30", command=register).pack()

    # main screen gameloop #
    screen.mainloop()


# call main screen #
main_screen()
