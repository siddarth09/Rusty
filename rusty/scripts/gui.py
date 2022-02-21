import rospy
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import cv2
import subprocess as sub
import signal


class Gui:

    def __init__(self,master):

        self.main=master
        self.command="clear"
        self.status="false"
        self.title=Label(self.main, text='RUSTY', font=("Times", "68", "bold"))
        self.title.place(relx=0.5,rely=0.2,anchor=CENTER)
        self.tagline=Label(self.main, text='Service robot', font=("Times", "18", "bold"))
        self.tagline.place(relx=0.5,rely=0.3,anchor=CENTER)
        self.startbutton=Button(self.main, text='START HOME SERVICE', command=self.startcore, font=("Times", "15", "bold"))
        self.menu=Button(self.main, text='MENU', command=self.display, font=("Times", "15", "bold"))
        self.menu.place(relx=0.50, rely=0.90, anchor=CENTER)
        self.exit=Button(self.main, text='Close', command=self.close, font=("Times", "15", "bold"))
        #self.exit.place(relx=0.70, rely=0.90, anchor=CENTER)
        #Gazebo
        self.gazebo=Button(self.main, text='GAZEBO', command=self.viewworld, font=("Times", "15", "bold"))
        #SLAM 
        self.slam=Button(self.main, text='SLAM', command=self.SLAM, font=("Times", "15", "bold"))
        #RVIZ 
        self.rviz=Button(self.main, text='RVIZ', command=self.viewrviz, font=("Times", "15", "bold"))

        #navigation
        self.nav=Button(self.main, text='NAVIGATION', command=self.naavigation, font=("Times", "15", "bold"))
    def startcore(self):
        
        if self.status==True:
            os.system("gnome terminal -e roscore")


    def display(self):
        """
        Displaying options for user to see
        """
        
        self.menu.place_forget()
        
        self.tagline.configure(text="CONTROL PANEL")
        self.gazebo.place(relx=0.2,rely=0.50,anchor=CENTER)
        self.exit.place(relx=0.70, rely=0.90, anchor=CENTER)
        self.slam.place(relx=0.20, rely=0.60, anchor=CENTER)
        self.rviz.place(relx=0.20,rely=0.70,anchor=CENTER)
        self.nav.place(relx=0.20,rely=0.80,anchor=CENTER)
    def viewworld(self):
        """
        Function to view different gazebo worlds

        TASK:= add a radio button for the worlds present
        1.empty.world
        2.house.world
        3.godown.world

        @chevula haarvish
        """
        world_name="empty"
        os.system("roslaunch rusty gazebo.launch world_name:={}".format(world_name))

    def viewrviz(self):
        os.system("roslaunch rusty_description display.launch")

    def SLAM(self):
        os.system("cd ~/rosworkspace/src/Rusty/rusty/scripts")
        os.system("chmod +x test_slam.sh")
        os.system("./test_slam.sh")

    def naavigation(self):
        os.system("cd ~/rosworkspace/src/Rusty/rusty/scripts")
        os.system("chmod +x navigation.sh")
        os.system("./navigation.sh")
        messagebox.showinfo(title='NAVIGATION TEST', message='Please use 2D nav to move the robot in the world')

        """
        @chevulahaarvish

        call me when you see this
        """


    def close(self):
        signal.signal(signal.SIGINT, exit(1))
       

if __name__=="__main__":
    root=Tk()
    root.title("RUSTY")
    root.geometry("500x500")

    myrobot=Gui(root)
    root.mainloop()
  
