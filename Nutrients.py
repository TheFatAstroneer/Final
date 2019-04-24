import random
import heapq
import pickle

food_list = []

def read_food_group():
    fileName = 'Food/FD_GROUP.txt'
    f = open(fileName,'r')
    lines = [line for line in f]


    ID_list, name_list = [], []
    for line in lines:
        ID_list.append(line.split('~')[1])
        name_list.append(line.split('~')[3])

    f.close()
    return ID_list, name_list


class Food():
    def __init__(self, ID, group, name):
        self.ID, self.group, self.name = ID, group, name
        self.serving_amount, self.unit, self.serving_weight = None, None, None
        self.nut_list = [0, 0, 0, 0]
        self.serving_take = 0

    def store_serving(self, serving_amount, unit, serving_weight):
        self.serving_amount = serving_amount
        self.unit = unit
        self.serving_weight = serving_weight

    def store_nutrition(self, nut_type, nut_value):
        nut_dict = {
            '208': 0,
            '205': 1,
            '203': 2,
            '204': 3
        }
        index = nut_dict[nut_type]
        self.nut_list[index] = nut_value

    def getnut(self):
        if (self.serving_amount == None or self.serving_amount == 0):
            return self.nut_list
        else:
            nut_per_serving = list(map(lambda x: x / self.serving_amount, self.nut_list))
            return nut_per_serving

    def get(self):
        info = [self.ID, self.group, self.name, self.serving_amount, self.unit, self.serving_weight, self.nut_list]
        return info

    def __lt__(self, Food2):
        return self.nut_list[0] < Food2.nut_list[0]

def choose_serving(this_amount, this_unit, this_weight):
    # pick one serving definition
    weight_chosen, amount_chosen, unit_chosen = 0, 0, 0
    if (len(this_amount) > 0):
        for i in range(0, len(this_weight)):
            weight = this_weight[i]
            # Prefer serving size of 50g -- 250g
            if (weight > 50) and (weight < 250):
                weight_chosen = weight
                amount_chosen, unit_chosen = this_amount[i], this_unit[i]
        if (weight_chosen == 0):
            weight_chosen = this_weight[0]
            amount_chosen, unit_chosen = this_amount[0], this_unit[0]
    return weight_chosen, amount_chosen, unit_chosen

def read_food_info():

    # find group and name of the food
    food_des_fileName = 'FOOD/FOOD_DES.txt'

    ID, group, name = '', '', ''
    index = 0
    index_dict = dict()
    with open(food_des_fileName) as fd:
        for i, line in enumerate(fd):
            ID = line.split('~')[1]
            group = line.split('~')[3]
            name= line.split('~')[5]
            this_Food = Food(ID, group, name)
            food_list.append(this_Food)
            index_dict[ID] = index
            index += 1

    # find serving size of the food
    this_amount, this_unit, this_weight = [], [], []
    weight_fileName = 'FOOD/WEIGHT.txt'
    last_ID = '0'
    this_Food = food_list[0]
    with open(weight_fileName) as fw:
        for j, line in enumerate(fw):
            ID_string = line.split('~')[1]
            if not (ID_string == last_ID) and not (last_ID == '0'):
                #if reading a new food, choose one of servings and store into Food object in list
                weight_chosen, amount_chosen, unit_chosen = choose_serving(this_amount, this_unit, this_weight)
                # find the index of this food in the food_list
                index = index_dict[last_ID]
                this_food = food_list[index]
                this_food.store_serving(amount_chosen, unit_chosen, weight_chosen)
                #reset food serving lists
                this_amount, this_unit, this_weight = [], [], []

            this_amount.append(float(line.split('^')[2]))
            this_unit.append(line.split('~')[5])
            this_weight.append(float(line.split('^')[4]))
            last_ID = ID_string


    # get food energy, carbohydrate, protein, fat and put in a dictionary
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


def save_food_info(food_list):
    with open('food_info', 'wb') as file:
        pickle.dump(food_list, file)


if (__name__ == '__main__'):
    food_list = read_food_info()
    save_food_info(food_list)
    print(food_list[1000].get())
    print(food_list[1000].getnut())
