from Tkinter import *

class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.hi_there = Button(self)
        self.hi_there["text"] = "Start",
        self.hi_there["command"] = self.clicked

        self.hi_there.pack({"side": "left"})
        self.hi_there.bind('<Button-1>', self.clicked)

    def clicked(self):
        self.hi_there.destroy()
        self.frame = FrameOne(self, controller = self)
        self.frame.pack({"side": "left"})
        self.show_frame(self.frame)

    def show_frame(self, frame):
        frame.tkraise()



class FrameOne(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller
        label = Label(self, text="Please chooser your gender", font=("Arial Bold", 50))
        label.pack(side="top", fill="x", pady=10)
        self.enter_gender()

    def enter_gender(self):
        self.male_button = Button(self, font=("Arial Bold", 36))
        self.male_button['text'] = 'Male'
        self.male_button.pack()
        self.male_button.bind('<Button-1>', self.clicked_male())

        self.female_button = Button(self, font=("Arial Bold", 36))
        self.female_button['text'] = 'Female'
        self.female_button.pack()

    def clicked_male(self):
        #self.male_button.destroy()
        #self.female_button.destroy()

        self.frame = FrameTwo(self, 'm')
        self.frame.pack()
        self.frame.tkraise()

class FrameTwo(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        if (controller == 'm'):
            label = Label(self, text="You are a male", font=("Arial Bold", 50))
            label.pack(side="top", fill="x", pady=10)

root = Tk()
app = Application()
app.master.title('Meal Generator')
app.master.geometry('1000x750')
app.master.maxsize(2000, 1500)


app.mainloop()
root.destroy()
