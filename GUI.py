try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        #self.configure(width = 400, height = 300, background="bisque")
        self.master.geometry('600x500')
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.hi_there = Button(self, width = 80, height = 40, font = ('Arial Bold', 40))
        self.hi_there["text"] = "Start"
        self.hi_there["command"] = self.clicked

        self.hi_there.pack(anchor = CENTER, expand = True, fill = BOTH)
        self.hi_there.bind('<Button-1>', self.clicked)

    def clicked(self, event):
        self.hi_there.destroy()
        self.frame = FrameOne(self)
        #self.frame.grid()
        self.show_frame(self.frame)

    def show_frame(self, frame):
        frame.tkraise()



class FrameOne(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.configure(width = 800, height = 900)
        #self.grid_propagate(0)
        self.grid(sticky = 'wens')
        self.controller = None
        self.label = Label(self, text="Tell me something about you!", font=("Arial Bold", 30))
        self.label.configure(anchor = 'center', bg = 'gray')
        self.label.grid(columnspan = 2)

        self.enter_age()
        self.enter_gender()
        self.enter_weight()
        self.enter_height()
        self.confirm()


    def enter_gender(self):
        self.gender = None
        self.male_button = Button(self, font=("Arial Bold", 18))
        self.male_button['text'] = 'Male'
        self.male_button.grid(row = 1, column = 0, pady = 15)
        self.male_button.bind('<Button-1>', self.clicked_male)

        self.female_button = Button(self, font=("Arial Bold", 18))
        self.female_button['text'] = 'Female'
        self.female_button.grid(row = 1, column = 1, pady = 15)
        self.female_button.bind('<Button-1>', self.clicked_female)

    def clicked_male(self, event):
        # self.frame = FrameTwo(self, 'm')
        # self.frame.pack()
        # self.frame.tkraise()

        self.male_button.configure(bg = 'gray')
        self.male_button.configure(relief = 'sunken')
        self.gender = 'm'
        self.female_button.configure(bg = 'white')
        self.female_button.configure(relief = 'raised')

    def clicked_female(self, event):
        self.female_button.configure(bg = 'gray')
        self.female_button.configure(relief = 'sunken')
        self.gender = 'f'
        self.male_button.configure(bg = 'white')
        self.male_button.configure(relief = 'raised')

    def enter_age(self):
        self.ask_age = Label(self, text = 'Please enter your age:', font = ('Arial', 14))
        self.ask_age.grid(row = 2, column = 0, pady = 30)

        self.enter_age = Entry(self, width = 15)
        self.enter_age.grid(row = 2, column = 1, pady = 30)
        self.age = self.enter_age.get()

    def enter_weight(self):
        self.ask_weight = Label(self, text = 'Please enter your weight(kg):', font = ('Arial', 14))
        self.ask_weight.grid(row = 3, column = 0, pady = 30)

        self.enter_weight = Entry(self, width = 15)
        self.enter_weight.grid(row = 3, column = 1, pady = 30)
        self.weight = self.enter_weight.get()

    def enter_height(self):
        self.ask_height = Label(self, text = 'Please enter your height(cm):', font = ('Arial', 14))
        self.ask_height.grid(row = 4, column = 0, pady = 30)

        self.enter_height = Entry(self, width = 15)
        self.enter_height.grid(row = 4, column = 1, pady = 30)
        self.height = self.enter_height.get()

    def confirm(self):
        self.enter = Button(self, text = 'Enter', font = ('Arial', 16))
        self.enter.grid(row = 5, columnspan = 2)
        self.enter.bind('<Button-1>', self.confirmed)

    def confirmed(self, event):
        self.controller = self.gender, self.weight, self.height
        self.newFrame = FrameTwo(self, self.controller, self)
        self.newFrame.tkraise()

class FrameTwo(Frame):
    def __init__(self, master, controller, frameOne):
        Frame.__init__(self, master)
        frameOne.grid_forget()
        self.controller = controller
        self.gender = None

        if (self.controller == 'm'):
            self.gender = 'm'
        else:
            self.gender = 'f'

        self.show()

    def show(self):
        self.lbl = Label(self, text = 'adsasds:', font = ('Arial', 14))
        self.grid()

root = Tk()
app = Application(master = root)
app.master.title('Meal Generator')
# app.master.geometry('100x80')
# app.master.maxsize(2000, 1500)


app.mainloop()
app.destroy()
