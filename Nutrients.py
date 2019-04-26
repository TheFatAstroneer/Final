import random
import pickle
from PIL import Image
from GetFoodPic import *

'''
This script accesses food database (https://fdc.nal.usda.gov/download-datasets.html), obtained
from USDA website and saved to txt files in the same directory.

An object called 'Food' is defined, and each instance stores information of one food item in the
database. All food objects obtained from the database are stored in a list, which is then written
to a file 'food_info' in the same directory, which can be later acessed.

'''
class Food():
    '''
    This object stores all related nutrition information of one food item found in the database,
    including ID identifier (used in database), name, food category, servings, nutrition.
    '''

    def __init__(self, ID, group, name):
        '''
        initialize the object.
        **Parameters**:
            ID: *string*
                The ID identifier for this food used in USDA SR Legacy database
            group: *string*
                The food category identifier for this food.
            name: *string*
                The name of this food in the database.
        '''
        self.ID, self.group, self.name = ID, group, name
        self.serving_amount, self.unit, self.serving_weight = None, None, None
        self.nut_list = [0, 0, 0, 0]
        self.serving_take = 0
        self.pic = None                 #The picture for this food, grabbed and used in Calories.py
        self.pic_name = None

    def store_serving(self, serving_amount, unit, serving_weight):
        '''
        Method that allows input of serving information into this food object
        **Parameters**
            serving_amount: *float*
                The number of servings
            unit: *string*
                The name of serving unit. For example: 'oz (ounce)'
            serbing_weight: *float*
                The weight of each serving in grams.
        **Return**
            None
        '''
        self.serving_amount = serving_amount
        self.unit = unit
        self.serving_weight = serving_weight

    def store_nutrition(self, nut_type, nut_value):
        '''
        Method that allows input of nutrition information into this food object. The nutrition that
        can be stored is Calories, carbohydrate, protein, and fat (values are for 100 grams of food)
        **Parameters**
            nut_type: *string*
                The identifiers for different types of nutrition information
                '208': Calories, '205': carbohydrate, '203': protein, '204': fat
            nut_value: *float*
                The value of the nutrition being stored. The unit for Calories is Cal, and grams for
                carbohydrate, protein, and fat
        **Return**
            None
        '''
        # Relates nutrition type identifier to the index of the list being stored
        nut_dict = {
            '208': 0,
            '205': 1,
            '203': 2,
            '204': 3
        }
        index = nut_dict[nut_type]
        self.nut_list[index] = nut_value

    def getnut(self):
        '''
        This method allows output of nutrition data after the value of each nutrition is being
        normalized by serving weight.
        **Return**
            nut_per_serving: *list* *float*
            A list containing values of Calories(Cal), carbohydrate(g), protein(g), fat(g) per
            serving
        '''
        # Some food grabbed from database has no serving data. In this case, no normalization is
        # performed.
        if (self.serving_amount == None or self.serving_amount == 0):
            return self.nut_list
        else:
            nut_per_serving = list(map(lambda x: x / self.serving_amount, self.nut_list))
            return nut_per_serving

    def get(self):
        '''
        Output the all information stored in this food object.
        **Returns**
            info: *list*
            A list containing all food info.
        '''
        info = [self.ID, self.group, self.name, self.serving_amount, self.unit, \
            self.serving_weight, self.nut_list]
        return info

    def __lt__(self, Food2):
        # Comparison method of this object. Compare by calories value.
        return self.nut_list[0] < Food2.nut_list[0]

def choose_serving(this_amount, this_unit, this_weight):
    '''
    Multiple definitions of serving may be obtained from the dabase. This function picks one serving
    definition to be used for other methods.
    **Parameters**:
        this_amount: *list* *float*
            The list containing all definitions of number of servings
        this_unit: *list* *string*
            The list containing all definitions of serving unit
        this_weight: *list* *float*
            The list containing all definitions of weight of serving in grams
    **Returns**
        weight_chosen: *float*
        amount_chosen: *float*
        unit_chosen: *float*
        The chosen serving weight, amount, and unit.
    '''
    weight_chosen, amount_chosen, unit_chosen = 0, 0, 0
    if (len(this_amount) > 0):
        for i in range(0, len(this_weight)):
            weight = this_weight[i]
            # Prefer serving size of 50g -- 250g
            if (weight > 50) and (weight < 250):
                weight_chosen = weight
                amount_chosen, unit_chosen = this_amount[i], this_unit[i]
        if (weight_chosen == 0):
            # Just pick the first one in the list if none of servings are within 50g to 250g.
            weight_chosen = this_weight[0]
            amount_chosen, unit_chosen = this_amount[0], this_unit[0]
    return weight_chosen, amount_chosen, unit_chosen

def read_food_info():
    '''
    This methods reads all food items from three database files: the first one contains ID, category
        identifier, and name of each food. The second file contains serving info of each food.
        The third file contains all nutrition data of each food.
    **Parameters**:
        None
    **Returns**:
        food_list: *list* *Food*
            A list containing all foods stored as Food objects
    '''
    food_list = []                 #initialize food_list

    # find ID, group and name of the food from the first database file
    food_des_fileName = 'FOOD/FOOD_DES.txt'
    ID, group, name = '', '', ''
    index = 0
    index_dict = dict()                     #Links food ID to position of this food in the database
    with open(food_des_fileName) as fd:
        for i, line in enumerate(fd):
            ID = line.split('~')[1]
            group = line.split('~')[3]
            name= line.split('~')[5]
            this_Food = Food(ID, group, name)             #Creates Food object for each food
            food_list.append(this_Food)
            index_dict[ID] = index
            index += 1

    # find serving size of each food
    # each food may has multiple servings defined -- occupy multiple lines in the txt file
    this_amount, this_unit, this_weight = [], [], []
    weight_fileName = 'FOOD/WEIGHT.txt'
    last_ID = '0'            # Creates a variable to store ID of the last food being read
    this_Food = food_list[0]
    with open(weight_fileName) as fw:
        for j, line in enumerate(fw):
            ID_string = line.split('~')[1]
            if not (ID_string == last_ID) and not (last_ID == '0'):
                #if reading a new food, choose one of servings and store into Food object in list
                weight_chosen, amount_chosen, unit_chosen = choose_serving(this_amount, this_unit, \
                    this_weight)
                # find the index of this food in the food_list
                index = index_dict[last_ID]
                this_food = food_list[index]
                this_food.store_serving(amount_chosen, unit_chosen, weight_chosen)
                #reset food serving lists
                this_amount, this_unit, this_weight = [], [], []
            # all serving definitions of this food are stored using lists
            this_amount.append(float(line.split('^')[2]))
            this_unit.append(line.split('~')[5])
            this_weight.append(float(line.split('^')[4]))
            last_ID = ID_string


    # Get food energy, carbohydrate, protein, fat and put in a dictionary
    # Iterate through the list with Food objects and input nutrition info into each object.
    nut_set = {'208', '205', '203', '204'}
    food_nutrition_fileName = 'FOOD/NUT_DATA2.txt'
    count = 0
    last_ID = '0'
    this_Food = food_list[0]
    with open(food_nutrition_fileName) as fn:
        for j, line in enumerate(fn):
            ID_string = line.split('''"''')[1]
            # if reading a new food from the file
            if not (ID_string == last_ID) and not (last_ID == '0'):
                count += 1
                this_Food = food_list[count]
            nut_type = line.split(',')[1].split('''"''')[1]
            nut_value = float(line.split(',')[2])
            if (nut_type in nut_set):
                this_Food.store_nutrition(nut_type, nut_value)
            last_ID = ID_string

    return food_list


def assign_pics(food_list):
    '''
    This method grabs a picture given the name of the food using Google Search.
    The image found is stroed in the Food object.
    **Parameters**
        food_list: *list* *Food*
            A list containing Food objects
    '''
    for food in food_list:
        # Only add picture if no picture is in the Food object
        if (food.pic == None):
            name = food.name
            #Truncate food name if name is long
            try:
                name = name.split(',')[0] + ',' + name.split(',')[1]
            except:
                pass

            # The actual method that gets image from website is written in GetFoodPic.py
            filename = get_image(name)
            img = Image.open(filename)
            food.pic = img
            food.pic_name = filename

def save_food_info(food_list):
    '''
    Stores all food information into a file on harddrive using Pickle.
    **Parameters**
        food_lilst: *list* *Food*
            A list containing food objects
    '''
    with open('food_info', 'wb') as file:
        pickle.dump(food_list, file)

if (__name__ == '__main__'):
    food_list = read_food_info()
    save_food_info(food_list)
