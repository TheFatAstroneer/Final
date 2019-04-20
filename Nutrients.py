import random

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

def get_food_info(ID, group, name):
    '''
    Nutrition ID:
        '208': 'energy (kcal)',
        '205': 'carb (g)'
        '203': 'protein (g)'
        '204': 'fat (g)'
    '''

    # find serving size of the food
    amount_list, unit_list, weight_list = [], [], []
    weight_fileName = 'FOOD/WEIGHT.txt'
    count= 0
    with open(weight_fileName) as fw:
        for j, line in enumerate(fw):
            ID_string = line.split('~')[1]
            if (ID == ID_string):
                amount_list.append(float(line.split('^')[2]))
                unit_list.append(line.split('~')[5])
                weight_list.append(float(line.split('^')[4]))
                count += 1
            if (count > 4):
                break

    # pick one serving definition
    weight_chosen, amount_chosen, unit_chosen = 0, 0, 0
    if (len(amount_list) > 1):
        for i in range(0, len(weight_list)):
            weight = weight_list[i]
            # Prefer serving size of 50g -- 250g
            if (weight > 50) and (weight < 250):
                weight_chosen = weight
                amount_chosen, unit_chosen = amount_list[i], unit_list[i]
        if (weight_chosen == 0):
            weight_chosen = weight_list[0]
            amount_chosen, unit_chosen = amount_list[0], unit_list[0]

    # get nutrition definition
    nut_dict = {
        '208': 'energy (kcal)',
        '205': 'carb (g)',
        '203': 'protein (g)',
        '204': 'fat (g)'
    }

    # get food energy, carbohydrate, protein, fat and put in a dictionary
    nutrition_dict = nut_dict.copy()
    count = 0
    food_nutrition_fileName = 'FOOD/NUT_DATA.txt'
    with open(food_nutrition_fileName) as fn:
        for j, line in enumerate(fn):
            ID_string = line.split('~')[1]
            if (ID == ID_string):
                nut_type = line.split('~')[3]
                nut_value = float(line.split('^')[2])
                if (nut_type in nut_dict.keys()):
                    nutrition_dict[nut_type] = nut_value
                    count += 1
            if (count >= 4):
                break


    fw.close()
    fn.close()

    return [ID, group, name, weight_chosen, amount_chosen, unit_chosen, nutrition_dict, 0]

def random_food():
    species = 7792
    random_num = random.randint(0, species - 1)

    # find group and name of the food
    food_des_fileName = 'FOOD/FOOD_DES.txt'

    ID, group, name = '','', ''
    with open(food_des_fileName) as fd:
        for i, line in enumerate(fd):
            if (i == random_num):
                ID = line.split('~')[1]
                group = line.split('~')[3]
                name= line.split('~')[5]
                break

    fd.close()

    return ID, group, name

if (__name__ == '__main__'):
    ID, group, name = random_food()
    print(get_food_info(ID, group, name))
