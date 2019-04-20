
from Nutrients import *
import copy

def calories_need(gender, age, weight, height, activity, goal):
    '''
    Calculates dialy calories need based on a formula that takes into account of
    gender, age, weight, height, and activity level

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
    carb_g = calories * carb_perc / 4
    protein_g = calories * protein_perc / 4
    fat_g = calories * protein_perc / 9

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
    [ID, group_string, name, weight_chosen, amount_chosen, unit_chosen, \
        nutrition_dict, serving_take] = food

    energy = nutrition_dict['208']

    if ('oil' in name) or (energy < 40) or (energy > 500) or (weight_chosen == 0):
        #print('check energy: %s, and is %s' %(energy, 'false'))
        return False

    # category_set = categories_existed(food_list)
    # if category in category_set:
    #     return False

    return True


def meal(macros, calories_limit, tolerance):
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
    while (count <= 100) and (unbalanced):

        if (total[0] >= calories_lowlim) and (unbalanced == False):
            break

        count += 1
        ID, group, name = random_food()
        food = get_food_info(ID, group, name)

        # pick another food if this one does not pass check
        while (check_food(food, food_list) == False):
            ID, group, name = random_food()
            food = get_food_info(ID, group, name)

        [ID, group_string, name, weight, amount, unit, nut, serving_take] = food
        energy, carb, protein, fat = nut['208'], nut['205'], nut['203'], nut['204']

        new_total = list(map(sum, zip(total, [energy, carb, protein, fat])))
        # Determine how many servings of this food to take
        if (total[0] < calories_uplim) & (total[1] < carb_uplim) & (total[2] < protein_uplim) & \
            (total[3] < fat_uplim):

            serving_max = max(int(200 / (weight * amount)), 3)
            if (serving_max <= 1) or (energy > 200):
                serving_take = 1
            else:
                serving_take = random.randint(1, serving_max)

            # Check whether any of macro has been exceeded after taking these serving
            while (serving_take > 1):
                new_total = copy.deepcopy(total)
                for  j in range(0, serving_take):
                    new_total = list(map(sum, zip(total, [energy, carb, protein, fat])))

                # Break the while loop if none of macro is exceeded by taking these servings
                # Otherwise, take out 1 serving of this food
                if (new_total[1] <= carb_uplim) and (new_total[2] <= protein_uplim) and \
                    (new_total[3] <= fat_uplim):
                    break
                else:
                    serving_take -= 1

            new_total = copy.deepcopy(total)
            for  j in range(0, serving_take):
                new_total = list(map(sum, zip(new_total, [energy, carb, protein, fat])))

        #print('energy is %s, serving_take: %s' %(energy, serving_take))

        # If taking this food, add to total and append to list
        if (serving_take >= 1):
            total = copy.deepcopy(new_total)
            food[-1] = serving_take
            food_list.append(food)

        # Determine whether the macros are unbalanced
        carb_diff = abs(total[1] - carb_limit) / carb_limit
        protein_diff = abs(total[2] - protein_limit) / protein_limit
        fat_diff = abs(total[3] - fat_limit) / fat_limit

        if (carb_diff > tolerance) or (protein_diff > tolerance) or (fat_diff > tolerance):
            if (total[0] >= calories_lowlim) or (total[1] >= carb_lowlim) or (total[2] >= protein_lowlim) or (total[3] >= fat_lowlim):
                food_list.pop(0)
                total = [0, 0, 0, 0]
                for item in food_list:
                    nut_this = item[6]
                    total = [total[0] + nut_this['208'] * item[-1], total[1] + nut_this['205'] * item[-1], \
                        total[2] + nut_this['203'] * item[-1], total[3] + nut_this['204'] * item[-1]]
        else:
            unbalanced = False


        print(total)

    print([calories_limit, carb_limit, protein_limit, fat_limit])
    print(food_list)



if (__name__ == '__main__'):
    calories_limit = calories_need('m', 25, 72, 176, 1.3, 1)
    macros = macros_need(calories_limit)
    meal(macros, calories_limit, 0.16)
