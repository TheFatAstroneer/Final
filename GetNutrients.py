import requests
import random

def search_database(item_name = '', category_ID = '', max = 3):
    search_api_pre = 'https://api.nal.usda.gov/ndb/search/?format=xml&q='
    search_api_post1 = '&max='
    search_api_post2 = '&offset=0&api_key='
    key_api = '1vOkwBMWYlKXtrwiWrvbBkhT1hrzpDk1V9mBayoR'

    if (len(category_ID) > 0):
        category_ID = '&fg=' + category_ID


    search_api = search_api_pre + category_ID + item_name + search_api_post1 \
        + str(max) + search_api_post2 + key_api

    search_results = requests.get(search_api)

    return search_results

def food_report(ID):
    search_api_pre = 'https://api.nal.usda.gov/ndb/reports/?ndbno='
    search_api_post = '&type=f&format=json&api_key='
    key_api = '1vOkwBMWYlKXtrwiWrvbBkhT1hrzpDk1V9mBayoR'

    report_api = search_api_pre + ID + search_api_post + key_api

    results = requests.get(report_api)

    return results

def categories_dict():

        categories_dict = {
        '3500': 'American Indian/Alaska Native Foods',
        '0300': 'Baby Foods',
        '1800': 'Baked Products',
        '1300': 'Beef Products',
        '1400': 'Beverages',
        '0800': 'Breakfast Cereals',
        '2000': 'Cereal Grains and Pasta',
        '0100': 'Dairy and Egg Products',
        '2100': 'Fast Foods',
        '0400': 'Fats and Oils',
        '1500': 'Finfish and Shellfish Products',
        '0900': 'Fruits and Fruit Juices',
        '1700': 'Lamb, Veal, and Game Products',
        '1600': 'Legumes and Legume Products',
        '2200': 'Meals, Entrees, and Side Dishes',
        '1200': 'Nut and Seed Products',
        '1000': 'Pork Products',
        '0500': 'Poultry Products',
        '3600': 'Restaurant Foods',
        '0700': 'Sausages and Luncheon Meats',
        '2500': 'Snacks',
        '0600': 'Soups, Sauces, and Gravies',
        '0200': 'Spices and Herbs',
        '1900': 'Sweets',
        '1100': 'Vegetables and Vegetable Products'
        }

        categories_set = {'American Indian/Alaska Native Foods', 'Baby Foods', 'Baked Products',
        'Beef Products', 'Beverages', 'Breakfast Cereals', 'Cereal Grains and Pasta',
        'Dairy and Egg Products', 'Fast Foods', 'Fats and Oils', 'Finfish and Shellfish Products',
        'Fruits and Fruit Juices', 'Lamb, Veal, and Game Products', 'Legumes and Legume Products',
        'Meals, Entrees, and Side Dishes', 'Nut and Seed Products', 'Nut and Seed Products',
        'Pork Products', 'Poultry Products', 'Restaurant Foods', 'Sausages and Luncheon Meats',
        'Snacks', 'Soups, Sauces, and Gravies', 'Spices and Herbs', 'Sweets',
        'Vegetables and Vegetable Products'
        }

        return categories_dict, categories_set

def random_categories():

    categories = categories_dict()[0]

    count = 0
    int_random = random.randint(0, len(categories) - 1)

    for ID, name in categories.items():
        if (count == int_random):
            return ID
        count += 1

    return 0


def read_search(search_results):
    parsed_list = search_results.split('<item offset=')

    name_list, ID_list = [], []
    for i in range(1, len(parsed_list)):
        food_item = parsed_list[i]
        name_list.append(str(food_item.split('<name>')[1].split('<')[0]))
        ID_list.append(str(food_item.split('<ndbno>')[1].split('<')[0]))

    return name_list, ID_list


def read_report(report):
    serving_name = str(report.split("Energy")[1].split('''"label":''')[1].split('''"''')[1])
    serving_qty = str(report.split("Energy")[1].split('''"qty":''')[1].split(''',''')[0])
    serving_amount = float(report.split("Energy")[1].split('''"eqv": ''')[1].split(''',''')[0])
    serving_unit = str(report.split("Energy")[1].split('''"eunit":''')[1].split('''"''')[1])
    serving_description = serving_qty + ' ' + serving_name + ' (' + \
        str(serving_amount) + serving_unit + ')'

    category = str(report.split('''"fg"''')[1].split('''"''')[1])
    energy_amount = float(report.split("Energy")[1].split('''"value":''')[2].split(''' ''')[1])
    energy_unit = str(report.split("Energy")[1].split('''"unit":''')[1].split('''"''')[1])

    protein_amount = float(report.split("Protein")[1].split('''"value":''')[2].split(''' ''')[1])
    protein_unit = str(report.split("Protein")[1].split('''"unit":''')[1].split('''"''')[1])

    fat_amount = float(report.split("fat")[1].split('''"value":''')[2].split(''' ''')[1])
    #fat_unit = str(report.split("fat")[1].split('''"unit":''')[1].split('''"''')[1])

    carb_amount = float(report.split("Carbohydrate")[1].split('''"value":''')[2].split(''' ''')[1])
    #carb_unit = str(report.split("Carbohydrate")[1].split('''"unit":''')[1].split('''"''')[1])

    fiber_amount = 0.0
    sugar_amount = 0.0
    try:
        fiber_amount = float(report.split("Fiber")[1].split('''"value":''')[2].split('''"''')[1])
        #fiber_unit = str(report.split("Fiber")[1].split('''"unit":''')[1].split('''"''')[1])

        sugar_amount = float(report.split("Sugars")[1].split('''"value":''')[2].split('''"''')[1])
        #sugar_unit = str(report.split("Sugars")[1].split('''"unit":''')[1].split('''"''')[1])
    except:
        pass

    return [serving_description, serving_amount, category, energy_amount, energy_unit, carb_amount,\
        protein_amount, fat_amount, fiber_amount, sugar_amount, protein_unit, 0]


def random_food():

    random_category = random_categories()
    food_list = search_database('', random_category, 100).text
    name_list, ID_list = read_search(food_list)

    int_random = random.randint(0, len(name_list) - 1)
    name, ID = name_list[int_random], ID_list[int_random]

    report = food_report(ID).text

    try:
        nutrients = [name, ID] + read_report(report)
    except IndexError:
        nutrients = 0

    return nutrients

if (__name__ == '__main__'):
    print(random_food())
