try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

from Calories import *
from PIL import ImageTk,Image

'''
A fun little tool that randomly generates food ingridients for making a meal that meets users'
calories need and macro nutrition preferences.

This is the main script that generates an graphic user interface that allows user to input body
information and preferences of diet.
The interface then presents the meal randomly generated based on this info, using Calories.py,
which uses food data obtained in Nutrition.py

Other scripts that need to be in the same directory:
    Nutrition.py
    GetFoodPic.py
    Calories.py
'''

class Start(Frame):
    '''
    The first frame that contains a start button.
    Uses grid widget organizer.
    **Parameter**
        Frame: *Class*
            This object inherits Frame class of Tkinter
    '''
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.geometry('600x700')
        self.grid()
        self.createWidgets()

    # Creates a start button and puts the button at center of the frame
    def createWidgets(self):
        self.separator = Label(self, height = 18)
        self.separator.grid(row = 0)

        self.hi_there = Button(self, text = 'Start', font = ('Arial Bold', 40))
        self.hi_there.grid(row = 10, sticky = 'WE', padx = 215)
        self.hi_there.bind('<Button-1>', self.clicked)

    # Clicks the button and opens up the next frame
    def clicked(self, event):
        # Destroys the curret widgets before initializing next frame (FrameOne)
        self.hi_there.destroy()
        self.separator.destroy()
        self.frame = FrameOne(self)

    def newFrame2(self, controller):
        # Initializes the second frame
        self.newF2 = FrameTwo(self, controller)

    def newFrame3(self, controller):
        # Initializes the third frame
        self.newF3 = FrameThree(self, controller)


class FrameOne(Frame):
    '''
    The second frame of the interface. This frame asks the user about their body information and
    diet preferences. This object inherits Frame class in Tkinter.
    '''
    def __init__(self, master):
        # This frame is a slave object of the Start frame
        Frame.__init__(self, master)
        self.configure(width = 800, height = 1200)
        self.grid(sticky = 'wens')
        self.controller = None

        # Adds title to the frame
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

    # Creates two buttons that allow users to select genders
    def enter_gender(self):
        self.male_button = Button(self, font=("Arial Bold", 18))
        self.male_button['text'] = 'Male'
        self.male_button.grid(row = 1, column = 0, pady = 15)
        self.male_button.bind('<Button-1>', self.clicked_male)

        self.female_button = Button(self, font=("Arial Bold", 18))
        self.female_button['text'] = 'Female'
        self.female_button.grid(row = 1, column = 1, pady = 15)
        self.female_button.bind('<Button-1>', self.clicked_female)

    # Configures male button when it is clicked or female button is clicked
    def clicked_male(self, event):
        self.male_button.configure(bg = 'gray')
        self.male_button.configure(relief = 'sunken')
        self.gender = 'm'
        self.female_button.configure(bg = 'white')
        self.female_button.configure(relief = 'raised')

    # Configures female button when it is clicked or male button is clicked
    def clicked_female(self, event):
        self.female_button.configure(bg = 'gray')
        self.female_button.configure(relief = 'sunken')
        self.gender = 'f'
        self.male_button.configure(bg = 'white')
        self.male_button.configure(relief = 'raised')

    # Creates a Entry widget for users to enter their age
    def enter_age(self):
        self.ask_age = Label(self, text = 'Please enter your age:', font = ('Arial', 14))
        self.ask_age.grid(row = 2, column = 0, pady = 30)

        self.enter_age = Entry(self, width = 15)
        self.enter_age.grid(row = 2, column = 1, pady = 30)

    # Creates a Entry widget for users to enter their weight
    def enter_weight(self):
        self.ask_weight = Label(self, text = 'Please enter your weight(kg):', font = ('Arial', 14))
        self.ask_weight.grid(row = 3, column = 0, pady = 30)

        self.enter_weight = Entry(self, width = 15)
        self.enter_weight.grid(row = 3, column = 1, pady = 30)

    # Creates a Entry widget for users to enter their height
    def enter_height(self):
        self.ask_height = Label(self, text = 'Please enter your height(cm):', font = ('Arial', 14))
        self.ask_height.grid(row = 4, column = 0, pady = 30)

        self.enter_height = Entry(self, width = 15)
        self.enter_height.grid(row = 4, column = 1, pady = 30)

    # Creates widgets for users to select their activity level
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

    # Creates widgets for users to select their goal
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
        self.goal3 = Radiobutton(self, text="Gain weight", variable=self.var2, value=1.1, font = this_font)
        self.goal3.grid(row = 11, column = 1)

        separator2 = Label(self, height = 1)
        separator2.grid(row = 12)

    # Check that inputs can be read as floats before triggering the next frame
    def chk_input(self, event):
        try:
            ## DEBUG:
            # self.age = 25
            # self.weight = 72
            # self.height = 176
            # self.activity = 1.3
            # self.goal = 1.0

            self.age = float(self.enter_age.get())
            self.weight = float(self.enter_weight.get())
            self.height = float(self.enter_height.get())
            self.activity = float(self.var.get())
            self.goal = float(self.var2.get())

            self.confirmed()
        except ValueError or TypeError:
            pass

    # Creates amd Binds the Enter button clicks to triggering next frame
    def confirm(self):
        self.enter = Button(self, text = 'Enter', font = ('Arial', 16))
        self.enter.grid(row = 20, columnspan = 2)
        self.enter.bind('<Button-1>', self.chk_input)

    # Calls the next frame and passes info to it
    def confirmed(self):
        self.controller = [self.gender, self.age, self.weight, self.height, self.activity, self.goal]

        ### DEBUG:
        print(self.controller)

        self.grid_forget()                #Clears current frame
        self.master.newFrame2(self.controller)             #Calls the next frame


class FrameTwo(Frame):
    '''
    This frame takes body info and preferences from the last frame, and calculates daily and meal
    calories needs. This frame also allows uses to select each macro nutrition percentage.
    This frame is a slave frame of the start frame.
    '''
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.grid()
        [self.gender, self.age, self.weight, self.height, self.activity, self.goal] = controller

        self.add_title()
        self.display_calories()
        self.enter_macros()
        self.confirm2()

    # Adds title to the frame
    def add_title(self):
        self.title = Label(self, text = 'Pick your macros!', bg = 'gray', \
            font = ('Arial Boad', 30))
        self.title.configure(anchor = 'center', justify = CENTER)
        self.title.grid(row = 0, columnspan = 2, sticky = 'we')

    # Displays dialy and meal calories in the frame
    def display_calories(self):
        # Creates separators to add empty spacers between widgets
        self.separator0 = Label(self, height = 3)
        self.separator0.grid(row = 1)

        self.daily_calories = int(calories_need(self.gender, self.age, self.weight, self.height, \
            self.activity, self.goal))
        self.show_calories1 = Label(self, text = 'Your daily calories need is:', font = ('Arial', 20))
        self.show_calories1.grid(row = 2, column = 0)

        self.show_calories2 = Label(self, text = self.daily_calories, font = ('Arial Bold', 20))
        self.show_calories2.grid(row = 2, column = 1)

        separator2 = Label(self,height = 1)
        separator2.grid(row = 3)

        self.meal_calories = int(self.daily_calories / 3)
        self.show_calories3 = Label(self, text = 'Your calories need this meal is:', font = ('Arial', 20))
        self.show_calories3.grid(row = 4, column = 0)

        self.show_calories4 = Label(self, text = self.meal_calories, font = ('Arial Bold', 20))
        self.show_calories4.grid(row = 4, column = 1)

        self.separator01 = Label(self, height = 4)
        self.separator01.grid(row = 5)

    # The fat percentage is a dependent variable that changes when user changes carb and protein
    # intake percentages
    def update_fat(self, event):
        self.enter_fat.configure(text = str(100 - self.var_carb.get() - self.var_protein.get()))

    # Allows users to adjust calories intake percentages from each macro nutrition
    def enter_macros(self):
        separator = Label(height = 3)
        separator.grid(row = 11)

        this_font = ('Arial', 16)
        self.var_carb, self.var_protein = IntVar(), IntVar()

        self.ask_carb = Label(self, text = 'Percent calories intake from carbohydrate:', font = this_font)
        self.ask_carb.grid(row = 12, column = 0, sticky = 'e')
        self.enter_carb = Scale(self, from_ = 10, to = 60, orient = HORIZONTAL, variable = self.var_carb, font = this_font)
        self.enter_carb.set(55)
        self.enter_carb.grid(row = 12, column = 1)

        self.ask_protein = Label(self, text = 'Percent calories intake from protein:', font = this_font)
        self.ask_protein.grid(row = 13, column = 0, sticky = 'e')
        self.enter_protein = Scale(self, from_ = 10, to = 40, orient = HORIZONTAL, \
            variable = self.var_protein, font = this_font)
        self.enter_protein.set(25)
        self.enter_protein.grid(row = 13, column = 1)

        separator2 = Label(self, height = 1)
        separator2.grid(row = 14)

        self.ask_fat = Label(self, text = 'Percent calories intake from fat:', font = this_font)
        self.ask_fat.grid(row = 15, column = 0, sticky = 'e')
        self.enter_fat = Label(self, text = '20', font = this_font)
        self.enter_fat.grid(row = 15, column = 1)

        # Changes fat percentage value when mouse releases after scrolling the other two macros
        self.enter_carb.bind('<ButtonRelease-1>', self.update_fat)
        self.enter_protein.bind('<ButtonRelease-1>', self.update_fat)

    # Creates Enter button and binds it with calling the next frame
    def confirm2(self):
        separator = Label(self, height = 3)
        separator.grid(row = 20)

        self.enter2 = Button(self, text = 'Enter', font = ('Arial', 20))
        self.enter2.grid(row = 21, columnspan = 2)
        self.enter2.bind('<Button-1>', self.confirmed2)

    # Call the next frame
    def confirmed2(self, event):
        # Clears current widgets
        self.grid_forget()
        self.master.newFrame3([self.meal_calories, self.var_carb.get(), self.var_protein.get()])


class FrameThree(Frame):
    '''
    The last frame that displays randomly generated food items for the meal
    This frame is a slave of the start frmae.
    '''
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.master.master.geometry('600x900')
        self.grid()

        # Get calories and percent calories intake from each macro
        self.controller = controller
        [self.meal_calories, self.carb_perc, self.protein_perc] = self.controller
        #Defines tolerance of total calories and macros from criteria as a fraction
        self.tolerance = 0.15

        self.add_title()
        self.show_meal()
        self.show_images()

    # Adds title to the frame
    def add_title(self):
        self.title = Label(self, text = '             Serving your meal...           ', bg = 'gray'\
            , font = ('Arial Boad', 30))
        self.title.configure(anchor = 'center', justify = CENTER)
        self.title.grid(row = 0, columnspan = 2, sticky = 'we')

    # Displays each food item and the total calories and macros of the meal
    def show_meal(self):
        self.separator = Label(self, height = 3)
        self.separator.grid(row = 10)

        # Get randomly generated meal using methods in Calories.py
        self.macros_g = macros_need(self.meal_calories, self.carb_perc, self.protein_perc)
        self.food_list = None
        while (self.food_list == None):
            self.food_list = meal(self.macros_g, self.meal_calories, self.tolerance)

        name_font = ('Arial', 16)
        serving_font = ('Arial', 12)
        nut_font = ('Arial', 12)
        food_count = 0
        if not (self.food_list == 0):
            self.img = []   #Stores pictures so that they do not get chewed up by garbage collectors

            # Displays name, serving, nutritions, and image of each food in meal
            for food in self.food_list:
                [ID, group_string, name, amount, unit, weight, nut] = food.get()
                nut = food.getnut()
                serving_take = food.serving_take

                # Truncate food name if name is long
                try:
                    name_show = name.split(',')[0] + ',' + name.split(',')[1]
                    if (len(list(name_show)) > 50):
                        name_show = name_show.split(',')[0]
                except:
                    name_show = name

                # Create label to show food names and nutritions
                self.food_label = Label(self, text = name_show, font = name_font)
                self.food_label.grid(row = 10 + food_count * 5, column = 0)

                # Create label show how much of what serving to take for each food
                if (serving_take == 1):
                    serving_show = '1 serving: ' + str(amount) + ' ' + unit + ' (' + str(weight) + 'g)'
                else:
                    serving_show = '' + str(serving_take) + ' servings: ' + str(amount) + ' ' \
                        + unit + ' (' + str(weight) + 'g)'
                self.serving_label = Label(self, text = serving_show, font = serving_font)
                self.serving_label.grid(row = 11 + food_count * 5, column = 0)

                # Create label to show calories and macros of each food
                nut_show = str(int(nut[0])) + ' Cal, containing ' + str(int(nut[1])) + 'g carb, ' \
                    + str(int(nut[2])) + 'g protein, ' + str(int(nut[3])) + 'g fat'
                self.nut_label = Label(self, text = nut_show, font = nut_font)
                self.nut_label.grid(row = 12 + food_count * 5, column = 0)

                self.separator2 = Label(self, height = 1)
                self.separator2.grid(row = 14 + food_count * 5, column = 0)
                food_count += 1

            # CaLculates and displays total calories and macros of the meal
            [cal, carb, protein, fat] = calc_total(self.food_list)
            self.summary_string1 = 'total calories: ' + str(int(cal))
            self.summary_string2 = 'carb ' + str(int(carb)) + 'g, protein ' + str(int(protein)) + \
                'g, fat ' + str(int(fat)) + 'g'
            self.summary_line1 = Label(self, font = ('Arial Bold', 14), text = self.summary_string1)
            self.summary_line2 = Label(self, font = ('Arial Bold', 14), text = self.summary_string2)
            self.summary_line1.grid(row = 5, column = 0)
            self.summary_line2.grid(row = 6, column = 0)

            self.separator3 = Label(self, height = 2)
            self.separator3.grid(row = 4, columnspan = 2)

            # Creates a button that allows users to choose regenerating random meal
            self.again_button = Button(self, text = 'Try Again', font = ('Arial', 20))
            self.again_button.grid(row = 5, rowspan = 2, column = 1, sticky = 'w')
            self.again_button.bind('<Button-1>', self.rerun)

    # Creates canvas widget to display the picture of the food, and places image next to text
    def show_images(self):
        food_count = 0
        for food in self.food_list:
            self.image = Canvas(self, width = 120, height = 120)
            self.img.append(ImageTk.PhotoImage(food.pic))
            self.image.create_image(60, 60, anchor = CENTER, image = self.img[food_count])
            self.image.grid(row = 10 + food_count * 5, rowspan = 4, column = 1, sticky = 'nswe')
            food_count += 1

    # Destroys this frame and regenerates one
    def rerun(self, event):
        self.master.newFrame3(self.controller)
        self.destroy()

if (__name__ == '__main__'):
    root = Tk()
    app = Start(master = root)
    app.master.title('Meal Generator')
    app.mainloop()
    app.destroy()
