from Nutrients import *
import pickle
import copy

'''
This script calculates Calories and macros needed for the user based on user information given, and
has a method that selects food that fullfills Calories and macros needs.
'''

def read_saved(food_info):
    '''
    Read saved file that contains information of all foods grabbed from database using Pickle
    **Parameters**
        food_info: *string*
            The name for the file being read
    **Returns**
        foods: *list*, *Food*
            A list of Food objects being read
    '''
    with open(food_info, 'rb') as file:
        foods = pickle.load(file)
    return foods

def random_food(foods):
    '''
    Get a random Food object from the list of all foods (total of 7792 foods)
    **Parameters**
        foods: *list*, *Food*
            A list of Food objects being read
    **Returns**
        *Food*
            A food object
    '''
    items = 7792
    random_num = random.randint(0, items - 1)
    return foods[random_num]

def calories_need(gender, age, weight, height, activity, goal):
    '''
    Calculates dialy calories need based on a formula that takes into account of
    gender, age, weight, height, and activity level using Harris-Benedict equation

    **Parametrs**
        gender: *string*
            'm': male, 'f': female
        age: *int*
        weight: *float*
            body weight in kilograms
        height: *float*
            body height in centimetres
        activity level (multipliers to Calories): *float*
            Not active: 1
            Slightly active: 1.5
            Very active: 1.5
        goal (multiplier to Calories): *float*
            Weight loss: 0.8
            Weight maintain: 1
            Weight gain: 1.1
    **Returns**
        calories: *float*
            Calculated daily calories need in Cal.
    '''

    if (gender == 'm'):
        calories = (10 * weight + 6.25 * height - 5 * age + 5) * activity * goal
    else:
        calories = (10 * weight + 6.25 * height - 5 * age - 161) * activity * goal

    return calories

def macros_need(calories, carb_perc = 50, protein_perc = 25):
    fat_perc = 100 - carb_perc - protein_perc
    carb_g = calories * carb_perc / 100.0 / 3.87
    protein_g = calories * protein_perc / 100.0 / 4.27
    fat_g = calories * protein_perc /100.0 / 8.79

    return carb_g, protein_g, fat_g

def categories_existed(food_list):
    cat_set = set()
    all_cat = {'0100', '0200', '0300', '0400', '0500', '0600', '0700', '0800', '0900', '1000',
                '1100', '1200', '1300', '1400', '1500', '1600', '1700', '1800', '1900', '2000',
                '2100', '2200', '2500', '3500', '3600'}

    # Add the category of each food in food_list into the category set
    for food in food_list:
        if food.group in all_cat:
            cat_set.add(food.group)

    return cat_set

def check_food(food, food_list):
    nut = food.getnut()
    [ID, group, name, amount, unit, weight, nut_list] = food.get()
    energy = nut[0]

    if (group == '0200') or (group == '0300'):
        return False

    if ('oil' in name) or (energy < 40) or (energy > 500) or (weight == 0):
        #print('check energy: %s, and is %s' %(energy, 'false'))
        return False

    if (amount == None) or (unit == None) or (weight == None):
        return False

    cat_set = categories_existed(food_list)
    if food.group in cat_set:
        return False

    return True

def calc_total(food_list):
    total = [0, 0, 0, 0]
    for food in food_list:
        nut = food.getnut()
        nut_total = list(map(lambda x: x * food.serving_take, nut))
        total = list(map(sum, zip(total, nut_total)))
    return total


def meal(macros, calories_limit, tolerance):
    # get list of all food in database
    foods = read_saved('food_info')

    carb_limit, protein_limit, fat_limit = macros
    uplimit = 1 + tolerance
    carb_uplim, protein_uplim, fat_uplim = carb_limit * uplimit, protein_limit * uplimit, fat_limit * uplimit
    carb_lowlim, protein_lowlim, fat_lowlim = carb_limit * 0.95, protein_limit * 0.95, fat_limit * 0.95
    calories_uplim, calories_lowlim = calories_limit * uplimit, calories_limit * 0.95

    count = 1
    total = [0.0, 0.0, 0.0, 0.0]
    food_list = []
    unbalanced = True

    # Grab a random food and determine how many servings to take
    while (count <= 50000) and (unbalanced):

        if (total[0] >= calories_lowlim) and (unbalanced == False):
            break

        count += 1
        this_food = random_food(foods)
        # pick another food if this one does not pass check
        while (check_food(this_food, food_list) == False):
            this_food = random_food(foods)

        [ID, group_string, name, amount, unit, weight, nut] = this_food.get()
        [energy, carb, protein, fat] = this_food.getnut()

        new_total = list(map(sum, zip(total, [energy, carb, protein, fat])))
        # Determine how many servings of this food to take
        if (total[0] < calories_uplim) & (total[1] < carb_uplim) & (total[2] < protein_uplim) & \
            (total[3] < fat_uplim):
            if (energy < 80):
                serving_take = random.randint(1, 3)
            elif (energy < 120):
                serving_take = random.randint(1, 2)
            else:
                serving_take = 1

            # Check whether any of macro has been exceeded after taking these serving
            while (serving_take > 1):
                new_total = copy.deepcopy(total)
                for j in range(0, serving_take):
                    new_total = list(map(sum, zip(total, [energy, carb, protein, fat])))

                # Break the while loop if none of macro is exceeded by taking these servings
                # Otherwise, take out 1 serving of this food
                if (new_total[1] <= carb_uplim) and (new_total[2] <= protein_uplim) and \
                    (new_total[3] <= fat_uplim):
                    break
                else:
                    serving_take -= 1

            new_total = copy.deepcopy(total)
            for j in range(0, serving_take):
                new_total = list(map(sum, zip(new_total, [energy, carb, protein, fat])))

        #print('energy is %s, serving_take: %s' %(energy, serving_take))

        # If taking this food, add to total and append to list
        if (serving_take >= 1):
            total = copy.deepcopy(new_total)
            this_food.serving_take = serving_take
            food_list.append(this_food)

        # Determine whether the macros are unbalanced
        carb_diff = abs(total[1] - carb_limit) / carb_limit
        protein_diff = abs(total[2] - protein_limit) / protein_limit
        fat_diff = abs(total[3] - fat_limit) / fat_limit

        if (carb_diff > tolerance) or (protein_diff > tolerance) or (fat_diff > tolerance):
            if (total[0] >= calories_lowlim) or (total[1] >= carb_lowlim) or (total[2] >= protein_lowlim) or (total[3] >= fat_lowlim):
                food_list.pop(0)
                total = calc_total(food_list)
        else:
            unbalanced = False

        if (count > 0) and (count % 10000 == 0):
            total = [0,0,0,0]

    if not (unbalanced):
        # add images to each food selected in food_list
        assign_pics(food_list)

        return food_list
    else:
         meal(macros, calories_limit, tolerance)



if (__name__ == '__main__'):
    calories_limit = calories_need('m', 25, 72, 176, 1.3, 1)
    # macros = macros_need(calories_limit)
    # meal(macros, calories_limit, 0.15)

    # foods = read_saved()
    # print(random_food(foods).get())
