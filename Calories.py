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
    '''
    Calculates grams of carb, protein, and fat needed for the meal, based on the macro percentages
    from user input
    **Parameters**
        calories: *float*
            total calories needed for this meal
        carb_perc: *float*
            percent calories intake from carb
        protein_perc: *float*
            percent calories intake from protein
    **Return**
        carb_g, protein_g, fat_g: *float*
            grams of carb, protein, and fat needded for this meal
    '''
    fat_perc = 100 - carb_perc - protein_perc
    carb_g = calories * carb_perc / 100.0 / 3.87           #3.87 Cal from 1 gram of carbohydrates
    protein_g = calories * protein_perc / 100.0 / 4.27     #4.27 Cal from 1 gram of protein
    fat_g = calories * protein_perc /100.0 / 8.79          #8.79 Cal from 1 gram of fat

    return carb_g, protein_g, fat_g

def categories_existed(food_list):
    '''
    Stores all categories of foods in a set
    **Parameters**
        food_list: *list* *Food*
            A list of Food objects
    **Return**
        cat_set: *set* *String*
            A set that contains categories of foods, as category identifiers listed in database.
    '''

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
    '''
    Determine whether a food item is suitable to added to the meal
    **Parameters**
        food: *Food*
            The Food object that is been checked
        food_list: *list* *Food*
            The preliminarily selected list of food for the meal
    **Return**
        *boolean*
            True for food passing the check. False for failing the check
    '''
    nut = food.getnut()
    [ID, group, name, amount, unit, weight, nut_list] = food.get()
    energy = nut[0]                #Calories of the food

    # Do not include categories of spices or baby food
    if (group == '0200') or (group == '0300'):
        return False

    # Do not include oils or if the food calories are too low or too high
    if ('oil' in name) or (energy < 50) or (energy > 400) or (weight == 0):
        #print('check energy: %s, and is %s' %(energy, 'false'))
        return False

    # Do not include food that has no serving info
    if (amount == None) or (unit == None) or (weight == None):
        return False

    # Only takes food in different categories
    cat_set = categories_existed(food_list)
    if food.group in cat_set:
        return False

    return True

def calc_total(food_list):
    '''
    Calculates the total calories and macros from all foods in a meal
    **Parameters**
        food_list: *list* *Food*
            The list of foods to be served to the meal
    **Return**
        total: *list* *float*
            The list that contains calories, grams of carb, grams of protein, and grams of fat
    '''
    total = [0, 0, 0, 0]
    for food in food_list:
        nut = food.getnut()
        nut_total = list(map(lambda x: x * food.serving_take, nut))
        total = list(map(sum, zip(total, nut_total)))
    return total


def meal(macros, calories_limit, tolerance):
    '''
    Generates a meal that contains randomly selected several food items that meets the energy and
    nutrition needs of the user.
    Each food is randomly selected from the database and has to pass the check.
    The number of servings for each food is also random.
    The total energy and each macro in the meal adds up to the meal calories need within a tolerance
    **Parameters**
        macros: *list* *float*
            A list containing macros needed for this meal
        calories_limit: *float*
            The calories needed for this meal
        tolerance: *float*
            A fraction that indicates that the total energy and each total macro of this meal must
            be within the range of
            (energy or macros)*(1-tolerance) and (energy or macros)*(1+tolerance)
    **Return**
        food_list: *list* *Food*
            A list that contains food items in this meal generated
    '''
    # Get list of all food in database
    foods = read_saved('food_info')

    # Defines upper limits of energy and macros based on tolerance
    # The lower limit for each is always 95%
    carb_limit, protein_limit, fat_limit = macros
    uplimit = 1 + tolerance
    carb_uplim, protein_uplim, fat_uplim = carb_limit * uplimit, protein_limit * \
        uplimit, fat_limit * uplimit
    carb_lowlim, protein_lowlim, fat_lowlim = carb_limit * 0.95, protein_limit * 0.95, \
        fat_limit * 0.95
    calories_uplim, calories_lowlim = calories_limit * uplimit, calories_limit * 0.95

    count = 1                       # Keeps track of iterations of getting random food
    total = [0.0, 0.0, 0.0, 0.0]
    food_list = []
    unbalanced = True               # True if each macro is within tolerance range

    # Grab a random food and determine how many servings to take in each iteration until total
    # calories and macros meet criteria. The max number of iteration allowed is 50,000
    while (count <= 50000) and (unbalanced):
        # Break out loop when criteria are met
        if (total[0] >= calories_lowlim) and (unbalanced == False):
            break

        count += 1
        this_food = random_food(foods)                  # grab a random food from database
        # pick another food if this one does not pass check
        while (check_food(this_food, food_list) == False):
            this_food = random_food(foods)

        [ID, group_string, name, amount, unit, weight, nut] = this_food.get()
        [energy, carb, protein, fat] = this_food.getnut()

        # Adds one serving of this food to the total calories and macros
        # and determine how many servings of this food to take if total does not exceed limits
        new_total = list(map(sum, zip(total, [energy, carb, protein, fat])))
        if (total[0] < calories_uplim) & (total[1] < carb_uplim) & (total[2] < protein_uplim) & \
            (total[3] < fat_uplim):
            # Pick number of servings depending on the energy content of the food
            if (energy < 80):
                serving_take = random.randint(1, 3)
            elif (energy < 120):
                serving_take = random.randint(1, 2)
            else:
                serving_take = 1

            # Check whether any of macro has been exceeded after taking these servings
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

        # If taking this food, add to total and append to meal list
        if (serving_take >= 1):
            total = copy.deepcopy(new_total)
            this_food.serving_take = serving_take
            food_list.append(this_food)

        # Determine whether the macros are unbalanced by calculating percentage of difference
        carb_diff = abs(total[1] - carb_limit) / carb_limit
        protein_diff = abs(total[2] - protein_limit) / protein_limit
        fat_diff = abs(total[3] - fat_limit) / fat_limit

        # If one of macros exceeds limit but not all macros are within defined range, take out
        # the first food in the list and keep iterating
        if (carb_diff > tolerance) or (protein_diff > tolerance) or (fat_diff > tolerance):
            if (total[0] >= calories_lowlim) or (total[1] >= carb_lowlim) or \
                (total[2] >= protein_lowlim) or (total[3] >= fat_lowlim):
                food_list.pop(0)
                total = calc_total(food_list)
        else:
            unbalanced = False

        # If no correct list is generated every 10,000 iterations, start over
        if (count > 0) and (count % 10000 == 0):
            total = [0,0,0,0]

    if not (unbalanced):
        assign_pics(food_list)              # add images to each food selected in food_list
        return food_list
    else:
        # Rerun this method if fails, until a valid list is generated
        meal(macros, calories_limit, tolerance)


if (__name__ == '__main__'):
    calories_limit = calories_need('m', 25, 72, 176, 1.3, 1)
    # macros = macros_need(calories_limit)
    # meal(macros, calories_limit, 0.15)

    # foods = read_saved()
    # print(random_food(foods).get())
