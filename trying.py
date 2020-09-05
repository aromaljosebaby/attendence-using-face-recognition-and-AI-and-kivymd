from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
#from opencvhelper import  KV
import shutil
from tkinter.filedialog import askdirectory, askopenfile
from tkinter import Tk
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast
import face_recognition
import os
import cv2
import pickle
import numpy as np
from datetime import date, datetime
from csv import writer
from helpers import KV



class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class TestNavigationDrawer(MDApp):

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.screen=Builder.load_string(KV)
        self.shud_we_train=False
        return self.screen
        #return Builder.load_string(KV)
    def lol(self):
        self.song = self.screen.ids.songname.text
        print(self.song)

    def add_img_to_train_folder(self):

        #self.add_img = True

        self.student_name=self.screen.ids.studentname.text
        self.student_rollnumber = self.screen.ids.studentrollnumber.text

        if(self.student_name==''):
            self.opening_dialogue_bos(title='Error',text='Please enter student name')

        if (self.student_rollnumber == ''):
            self.opening_dialogue_bos(title='Error', text='Please enter student rollnumber')

        else:
            files = [('text file', '*.jpg')]
            root = Tk()
            root.withdraw()
            # file = askdirectory()
            source = askopenfile()
            if source==None:
                self.opening_dialogue_bos(title='No image selected',text='Select image to add')


            else:
                source=source.name
                l = source.split('/')
                folder_type = l[len(l) - 1].split('.')[1]


                file_name = 'Train Images'
                student_name = self.student_name.lower()
                student_rollnumber=self.student_rollnumber

                parent_dir = os.getcwd()
                path = os.path.join(parent_dir, file_name)
                destination = f'{path}\{student_rollnumber}_{student_name}.{folder_type}'

                try:
                    os.mkdir(path)
                except FileExistsError:
                    pass
                shutil.move(source, destination)
                self.shud_we_train=True
                self.popup(text='Image succesfully added')

    def deleting_image_from_train_folder(self):



        self.student_rollnumber_for_deleting = self.screen.ids.deletingsrollnumber.text
        if (self.student_rollnumber_for_deleting== ''):
            self.opening_dialogue_bos(title='Error', text='Please enter student rollnumber')
        else:
            cur_dir = os.getcwd()
            roll_number = self.student_rollnumber_for_deleting
            for r, d, f in os.walk(os.path.join(cur_dir, 'Train Images')):
                for file in f:
                    if (file.endswith('.png') or file.endswith('.jpg')):
                        image_name = file
                        full_path = os.path.join(r, file)
                        # l=os.path.join(r, file)
                        if roll_number in image_name:
                            os.remove(full_path)
                            self.shud_we_train=True
                            self.popup(text='Image succesfully removed')
                        else:
                            self.opening_dialogue_bos(title='Error', text='Please enter valid student rollnumber')


    def start_attendence(self):
        if(self.shud_we_train==True):
            self.opening_dialogue_bos(title='Note', text='Please Proceed to train to update the changes')

        else:
            cur_dir = os.getcwd()
            try:
                loading = pickle.loads(open('encodings.pickle', 'rb').read())
            except FileNotFoundError:
                self.opening_dialogue_bos(title='Error', text='First Add Image and then click on Train Images')

            else:

                encodeListKnown = loading['encodings']
                classNames = loading['names']
                todays_date = date.today()

                def giving_heading_to_csv():
                    todays_date = date.today()
                    # with open(f'C:/Users/user/PycharmProjects/deletesoon/AttendenceRegister/{todays_date}.csv', 'w+') as f:
                    with open(f'{cur_dir}/AttendenceRegister/{todays_date}.csv', 'w+') as f:
                        l = f.readline()
                        if l != 'Name,Time\n':
                            csv_writer = writer(f)
                            csv_writer.writerow(['Name', 'RollNumber', 'Time'])

                giving_heading_to_csv()

                def markAttendence(name):
                    # print(f'{name}tat is name variable')
                    rollnumber = name.split('_')[0]
                    name = name.split('_')[1]

                    with open(f'{cur_dir}/AttendenceRegister/{todays_date}.csv', 'r+') as f:

                        myDataList = f.readlines()
                        # print(myDataList)

                        nameList = []
                        for line in myDataList:
                            entry = line.split(',')

                            nameList.append(entry[0])

                        if name not in nameList:
                            now = datetime.now()
                            dtString = now.strftime('%H:%M:%S')
                            f.writelines(f'{name},{rollnumber},{dtString}')
                            f.write('\n')

                cap = cv2.VideoCapture(0)

                while True:
                    success, img = cap.read()
                    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # converting each frame to smaller size for speed
                    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

                    facesCurFrame = face_recognition.face_locations(
                        imgS)  # list of region of interest of all faces in the current frame
                    encodesCurFrame = face_recognition.face_encodings(imgS,
                                                                      facesCurFrame)  # the encodings of the current faces in frame

                    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                        matches = face_recognition.compare_faces(encodeListKnown,
                                                                 encodeFace)  # comparing encoding btw the current frame pic and the list of uploaded images
                        faceDis = face_recognition.face_distance(encodeListKnown,
                                                                 encodeFace)  # will give any array showing accuracy of the current image in frame with all pictures saved

                        matchIndex = np.argmin(
                            faceDis)  # gives the index of the smallest number in the distance list, ie smallest will be matching person

                        if matches[matchIndex]:
                            name = classNames[matchIndex].upper()

                            y1, x2, y2, x1 = faceLoc
                            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

                            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                            markAttendence(name)

                    cv2.imshow('Webcam', img)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                cap.release()
                cv2.destroyAllWindows()

    def train_img(self):

        path = 'Train Images'

        images = []  # array of numpy values of images
        classNames = []  # an array of just names of ppl
        myList = os.listdir(path)

        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])

        def findEncodings(images):
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)

            return encodeList

        encodeListKnown = findEncodings(images)

        #print('Encoding complete')
        self.shud_we_train=False
        self.popup(text='Training succesfully completed')

        data = {'encodings': encodeListKnown, 'names': classNames}

        f = open('encodings.pickle', 'wb')
        f.write(pickle.dumps(data))
        f.close()


    def check_for_blank_close(self,obj):
        self.blank_check_dialogue.dismiss()



    def opening_dialogue_bos(self,title,text):
        close_btn = MDRaisedButton(text='Close', on_release=self.check_for_blank_close)
        self.blank_check_dialogue = MDDialog(title=title,
                                             text=text,
                                             buttons=[close_btn])
        self.blank_check_dialogue.open()

    def popup(self,text):
        toast(text)



TestNavigationDrawer().run()
