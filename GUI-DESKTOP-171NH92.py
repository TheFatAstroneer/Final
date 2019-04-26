try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

from Calories import *




class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        #self.configure(width = 400, height = 300, background="bisque")
        self.master.geometry('600x700')
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
        #self.frame.tkraise()

    def newFrame2(self, controller):
        self.newF2 = FrameTwo(self, controller)


    def newFrame3(self):

        #self.newF2.grid_forget()
        self.newFrame = FrameThree(self, '')


class FrameOne(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.configure(width = 800, height = 1200)
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
        self.enter_activity()
        self.enter_goal()

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


    def enter_weight(self):
        self.ask_weight = Label(self, text = 'Please enter your weight(kg):', font = ('Arial', 14))
        self.ask_weight.grid(row = 3, column = 0, pady = 30)

        self.enter_weight = Entry(self, width = 15)
        self.enter_weight.grid(row = 3, column = 1, pady = 30)

    def enter_height(self):
        self.ask_height = Label(self, text = 'Please enter your height(cm):', font = ('Arial', 14))
        self.ask_height.grid(row = 4, column = 0, pady = 30)

        self.enter_height = Entry(self, width = 15)
        self.enter_height.grid(row = 4, column = 1, pady = 30)

    def enter_activity(self):
        this_font = ('Arial', 14)
        self.ask_act = Label(self, text = 'Activity level:', font = this_font)
        self.ask_act.grid(row = 5, column = 0)

        self.var = DoubleVar()
        self.act1 = Radiobutton(self, text="Not active", variable=self.var, value=1.2, font = this_font)
        self.act1.grid(row = 5, column = 1)
        self.act2 = Radiobutton(self, text="Slightly active", variable=self.var, value=1.375, font = this_font)
        self.act2.grid(row = 6, column = 1)
        self.act3 = Radiobutton(self, text="Very active", variable=self.var, value=1.55, font = this_font)
        self.act3.grid(row = 7, column = 1)

    def enter_goal(self):
        separator = Label(self, height = 1)
        separator.grid(row = 8)

        this_font = ('Arial', 14)
        self.ask_goal = Label(self, text = 'What is your goal?', font = this_font)
        self.ask_goal.grid(row = 9, column = 0)

        self.var2 = DoubleVar()
        self.goal1 = Radiobutton(self, text="Lose weight", variable=self.var2, value=0.8, font = this_font)
        self.goal1.grid(row = 9, column = 1)
        self.goal2 = Radiobutton(self, text="Maintain weight", variable=self.var2, value=1, font = this_font)
        self.goal2.grid(row = 10, column = 1)
        self.goal3 = Radiobutton(self, text="Gain active", variable=self.var2, value=1.1, font = this_font)
        self.goal3.grid(row = 11, column = 1)

        separator2 = Label(self, height = 1)
        separator2.grid(row = 12)

    def chk_input(self, event):
        try:

            ## DEBUG:
            self.age = 25
            self.weight = 72
            self.height = 176
            self.activity = 1.3
            self.goal = 1.0

            # self.age = float(self.enter_age.get())
            # self.weight = float(self.enter_weight.get())
            # self.height = float(self.enter_height.get())
            # self.activity = float(self.var.get())
            # self.goal = float(self.var2.get())

            self.confirmed()
        except ValueError or TypeError:
            pass

    def confirm(self):
        self.enter = Button(self, text = 'Enter', font = ('Arial', 16))
        self.enter.grid(row = 20, columnspan = 2)

        self.enter.bind('<Button-1>', self.chk_input)

    def confirmed(self):
        self.controller = [self.gender, self.age, self.weight, self.height, self.activity, self.goal]

        self.grid_forget()

        #self.newFrame = FrameTwo(self, self.controller)
        self.master.newFrame2(self.controller)


class FrameTwo(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)

        # frame = Frame(master)
        self.grid()
        #self.configure(width = 800, height = 900)
        [self.gender, self.age, self.weight, self.height, self.activity, self.goal] = controller

        self.add_title()
        self.display_calories()
        self.enter_macros()
        self.confirm2()

    def add_title(self):
        self.title = Label(self, text = '            Pick your macros!            ', bg = 'gray', \
            font = ('Arial Boad', 30))
        self.title.configure(anchor = 'center', justify = CENTER)
        self.title.grid(row = 0, columnspan = 2, sticky = 'we')

    def display_calories(self):
        separator = Label(self, height = 3)
        separator.grid(row = 1)

        daily_calories = int(calories_need(self.gender, self.age, self.weight, self.height, \
            self.activity, self.goal))
        self.show_calories1 = Label(self, text = 'Your daily calories need is:', font = ('Arial', 20))
        self.show_calories1.grid(row = 2, column = 0)

        self.show_calories2 = Label(self, text = daily_calories, font = ('Arial Bold', 20))
        self.show_calories2.grid(row = 2, column = 1)

        separator2 = Label(self,height = 1)
        separator2.grid(row = 3)

        meal_calories = int(daily_calories / 3)
        self.show_calories3 = Label(self, text = 'Your calories need this meal is:', font = ('Arial', 20))
        self.show_calories3.grid(row = 4, column = 0)

        self.show_calories4 = Label(self, text = meal_calories, font = ('Arial Bold', 20))
        self.show_calories4.grid(row = 4, column = 1)

    def update_fat(self, event):
        self.enter_fat.configure(text = str(100 - self.var_carb.get() - self.var_protein.get()))

    def enter_macros(self):
        separator = Label(height = 3)
        separator.grid(row = 11)

        this_font = ('Arial', 16)
        self.var_carb, self.var_protein = IntVar(), IntVar()

        self.ask_carb = Label(self, text = 'Percent calories intake from carbohydrate:', font = this_font)
        self.ask_carb.grid(row = 12, column = 0, sticky = 'e')
        self.enter_carb = Scale(self, from_ = 0, to = 60, orient = HORIZONTAL, variable = self.var_carb, font = this_font)
        self.enter_carb.grid(row = 12, column = 1)

        self.ask_protein = Label(self, text = 'Percent calories intake from protein:', font = this_font)
        self.ask_protein.grid(row = 13, column = 0, sticky = 'e')
        self.enter_protein = Scale(self, from_ = 0, to = 40, orient = HORIZONTAL, variable = self.var_protein, font = this_font)
        self.enter_protein.grid(row = 13, column = 1)

        separator2 = Label(self, height = 1)
        separator2.grid(row = 14)

        self.ask_fat = Label(self, text = 'Percent calories intake from fat:', font = this_font)
        self.ask_fat.grid(row = 15, column = 0, sticky = 'e')
        self.enter_fat = Label(self, text = '100', font = this_font)
        self.enter_fat.grid(row = 15, column = 1)

        self.enter_carb.bind('<ButtonRelease-1>', self.update_fat)
        self.enter_protein.bind('<ButtonRelease-1>', self.update_fat)

    def confirm2(self):
        separator = Label(self, height = 3)
        separator.grid(row = 20)

        self.enter2 = Button(self, text = 'Enter', font = ('Arial', 20))
        self.enter2.grid(row = 21, columnspan = 2)
        self.enter2.bind('<Button-1>', self.confirmed2)

    def confirmed2(self, event):
        # self.controller = [self.var_carb.get(), self.var_protein.get()]
        # self.newFrame = FrameThree(self, self.controller)

        self.grid_forget()
        self.master.newFrame3()


class FrameThree(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        #master.frame.destroy()
        self.grid()

        self.add_title()

    def add_title(self):
        self.title = Label(self, text = '         Serving your meal...         ', bg = 'gray', \
            font = ('Arial Boad', 30))
        self.title.configure(anchor = 'center', justify = CENTER)
        self.title.grid(row = 0, columnspan = 2, sticky = 'we')


root = Tk()
app = Application(master = root)
app.master.title('Meal Generator')
# app.master.geometry('100x80')
# app.master.maxsize(2000, 1500)


app.mainloop()
app.destroy()
