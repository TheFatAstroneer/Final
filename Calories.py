from Nutrients import *
import pickle
import copy

def read_saved():
    with open('food_info', 'rb') as file:
        foods = pickle.load(file)
    return foods

def random_food(foods):
    species = 7792
    random_num = random.randint(0, species - 1)
    return foods[random_num]

def calories_need(gender, age, weight, height, activity, goal):
    '''
    Calculates dialy calories need based on a formula that takes into account of
    gender, age, weight, height, and activity level
    Harris-Benedict equation

    goal:
    Weight loss: 0.8
    Weight maintain: 1
    Weight gain: 1.1
    '''

    if (gender == 'm'):
        calories = (10 * weight + 6.25 * height - 5 * age + 5) * activity * goal
    else:
        calories = (10 * weight + 6.25 * height - 5 * age - 161) * activity * goal

    return calories

def macros_need(calories):

    carb_perc, protein_perc, fat_perc = 0.5, 0.25, 0.25
    carb_g = calories * carb_perc / 3.87
    protein_g = calories * protein_perc / 4.27
    fat_g = calories * protein_perc / 8.79

    return carb_g, protein_g, fat_g

def categories_existed(food_list):
    category_set = set()
    all_categories = categories_dict()[1]

    # Add the category of each food in food_list into the category set
    for food in food_list:
        food_cat = food[4]

        if food_cat in all_categories:
            category_set.add(food_cat)

    return category_set

def check_food(food, food_list):

    nut = food.getnut()
    [ID, group, name, amount, unit, weight, nut_list] = food.get()
    energy = nut[0]

    if ('oil' in name) or (energy < 40) or (energy > 500) or (weight == 0):
        #print('check energy: %s, and is %s' %(energy, 'false'))
        return False

    # category_set = categories_existed(food_list)
    # if category in category_set:
    #     return False

    return True


def meal(macros, calories_limit, tolerance):

    def calc_total(food_list):
        total = [0, 0, 0, 0]
        for food in food_list:
            nut = food.getnut()
            nut_total = list(map(lambda x: x * food.serving_take, nut))
            total = list(map(sum, zip(total, nut_total)))
        return total

    # get list of all food in database
    foods = read_saved()

    carb_limit, protein_limit, fat_limit = [macro / 3 for macro in macros]
    calories_limit = calories_limit / 3
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

            serving_take = random.randint(1, 2)

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
            total = [0,0,0,0
            ]

        # for food in food_list:
        #     print(food.get())
        #print(total)
    print(total)
    print('limit is %s' %[calories_limit, carb_limit, protein_limit, fat_limit])
    for food in food_list:
        print(food.get())
        print(food.serving_take)
    print(not unbalanced)
    print(count)



if (__name__ == '__main__'):
    calories_limit = calories_need('m', 25, 72, 176, 1.3, 1)
    macros = macros_need(calories_limit)
    meal(macros, calories_limit, 0.1)

    # foods = read_saved()
    # print(random_food(foods).get())
