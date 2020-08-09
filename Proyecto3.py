### Import all ###
import face_recognition
import cv2
import pickle
import os
import numpy as np

import tkinter as tk
from tkinter import messagebox

from pathlib import Path
import glob


###  ###
class Dlib_Face_Unlock:
    def __init__(self):
        try:
            root_dir = os.path.dirname(os.path.abspath("Proyecto3.py"))
            ### create new files if they're not in the pc ###
            if not os.path.exists(root_dir + '/images'):
                os.makedirs(root_dir + '/images')
            if not os.path.exists(root_dir + '/KnownFace.pickle'):
                os.makedirs(root_dir + '/KnownFace.pickle')
            if not os.path.exists(root_dir + '/labels.pickle'):
                os.makedirs(root_dir + '/labels.pickle')

            with open (root_dir + '/labels.pickle') as self.f:
                self.og_labels = pickle.load(self.f)
            print(self.og_labels)

        except FileNotFoundError:
            print("No label.pickle file detected, will create required pickle files")

        self.current_id = 0
        self.labels_ids = {}

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_dir = os.path.join(self.base_dir, 'images')
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
        self.og_labels = 0
        if self.labels_ids != self.og_labels:
            with open('labels.pickle','wb') as self.file:
                pickle.dump(self.labels_ids, self.file)

            self.known_faces = []
            for self.i in self.labels_ids:
                num_imgs = len([filename for filename in os.listdir('images/' + self.i)
                                if os.path.isfile(os.path.join('images/' + self.i, filename))])
                print(num_imgs)
                for img_num in range(1, (num_imgs+1)):
                    self.directory = os.path.join(self.image_dir, self.i, str(img_num)+'png')
                    self.img = face_recognition.load_image_file(self.directory)
                    self.img_encoding = face_recognition.face_encodings(self.img)[0]
                    self.known_faces.append([self.i, self.img_encoding])
                print(self.known_faces)
                print("Num of Imgs"+str(len(self.known_faces)))
                with open('KnownFace.pickle','wb') as self.known_faces_file:
                    pickle.dump(self.known_faces, self.known_faces_file)
            else:
                with open(root_dir+'/labels.pickle', 'rb') as self.faces_file:
                    self.known_faces = pickle.load(self.faces_file)
                print(self.known_faces)

    ### Method: ID ###
    """ This method will be used to create a live feed
    turning the camera on, then take a pic and encode the users face
    after that, it will be compared to in the known faces, identifying the user"""
    def ID(self):
    ### Turning the camera on to get a photo of the user ###
        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.faces_names = []
        while self.running == True:
            self.ret, self.frame = self.cap.read()
            self.small_frame = cv2.resize(self.frame, (0,0), fx = 0.5, fy = 0.5)
            self.rgb_small_frame = self.small_frame[:, :, ::-1]
            if self.running:
                self.faces_locations = face_recognition.face_locations(self.frame)
                self.face_encodings = face_recognition.face_encodings(self.frame, self.faces_locations)
                self.face_names = []

                for self.face_encoding in self.face_encodings:
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

def register():
    Path("images/"+name.get()).mkdir(parents=True, exist_ok=True)
    numberOfFile = len([filename for filename in os.listdir('images/' + name.get())
                        if os.path.isfile(os.path.join('images/' + name.get(), filename))])
    numberOfFile += 1
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")

    while True:
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k % 256 == 27:
            print("escape hit, closing...")
            cam.release()
            cv2.destroyAllWindows()
            break
        elif k % 256 == 32:
            img_name = str(numberOfFile)+".png"
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            os.replace(str(numberOfFile)+".png", "images/"+name.get().lower()+"/"+str(numberOfFile)+".png")
            cam.release()
            cv2.destroyAllWindows()
            break
    raiseFrame (loginFrame)

def login():
    dfu = Dlib_Face_Unlock()
    user = dfu.ID()
    if user == []:
        messagebox.showerror("Alert", "Face not Recognised")
        return
    loggedInUser.set(user[0])
    raiseFrame(userMenuFrame)




### Acá es donde va el login, hice uno básico para probar el programa :3 ###
#Tkinter

root = tk.Tk()
root.title("Face Login Example")

loginFrame = tk.Frame(root)
regFrame = tk.Frame(root)
userMenuFrame = tk.Frame(root)

frameList = [loginFrame, regFrame, userMenuFrame]

for frame in frameList:
    frame.grid(row=0, column=0, sticky='news')
    frame.configure(bg='white')


def raiseFrame(frame):
    frame.tkraise()


def regFrameRaiseFrame():
    raiseFrame(regFrame)


def logFrameRaiseFrame():
    raiseFrame(loginFrame)

name = tk.StringVar()
loggedInUser = tk.StringVar()


tk.Label(loginFrame, text="Face Recognition", bg="white", font=("Courier", 60)).grid(row=1, column=1, columnspan=5)
loginButton = tk.Button(loginFrame, text="Login", bg="white", font=("Arial", 30), command=login)
loginButton.grid(row=2, column=5)
regButton = tk.Button(loginFrame, text="Register", command=regFrameRaiseFrame,bg="white", font=("Arial", 30))
regButton.grid(row=2, column=1)

tk.Label(regFrame, text="Register", font=("Courier", 60), bg="white").grid(row=1, column=1, columnspan=5)
tk.Label(regFrame, text="Name: ", font=("Arial", 30), bg="white").grid(row=1, column=1)
nameEntry = tk.Entry(regFrame, textvariable=name, font=("Arial",30)).grid(row=2, column=2)

registerButton = tk.Button(regFrame,text="Register", command=register,bg="white", font=("Arial", 30))
registerButton.grid(row=3, column=2)

tk.Label(userMenuFrame, text="Hello, ", font=("Courier", 60), bg="white").grid(row=1, column=1)
tk.Label(userMenuFrame, textvariable=loggedInUser, font=("Courier", 60), bg="white", fg="red").grid(row=1,column=1)
tk.Button(userMenuFrame, text="Back", font=("Arial", 30), command=logFrameRaiseFrame).grid(row=2, column=1)


dfu = Dlib_Face_Unlock
raiseFrame(loginFrame)
root.mainloop()