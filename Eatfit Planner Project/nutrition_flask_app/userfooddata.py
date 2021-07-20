import requests
from nutrition_flask_app.api_info import userid, app_key
from nutrition_flask_app import models
from nutrition_flask_app.app import db

class Userfooddetails:

    # User food plan details
    def store_user_food_plan(self, food_plan, carbohydrate_limit, protein_limit, fat_limit, user_name):
        user_details = models.User.query.filter_by(username=user_name).one()
        exists = db.session.query(models.User_Food_Plan).filter_by(iduser_plan=user_details.id).first() is not None
        if exists:
            query_user = models.User_Food_Plan.query.filter_by(iduser_plan=user_details.id).one()
            query_user.user_diet_plan = food_plan
            query_user.user_carbohydrate_ratio = carbohydrate_limit
            query_user.user_protein_ratio = protein_limit
            query_user.user_fat_ratio = fat_limit
            db.session.merge(query_user)
            db.session.commit()
        else:
            query_user = models.User_Food_Plan(user_diet_plan=food_plan,
                                               user_carbohydrate_ratio=carbohydrate_limit,
                                               user_protein_ratio=protein_limit, user_fat_ratio=fat_limit,
                                               iduser_plan=user_details.id)
            db.session.add(query_user)
            db.session.commit()
        return query_user


    # Fetching api
    def get_api_response(self, food_name):
        url = "https://trackapi.nutritionix.com/v2/natural/nutrients"

        headers = {'Content-Type': "application/json",
                   'x-app-id': userid,
                   'x-app-key': app_key,
                   'x-remote-user-id': "0",
                   'cache-control': "no-cache"
                   }

        data_api = '{"query":' + '"' + food_name + '"' + '}'
        return requests.post(url, headers=headers, data=data_api)


    # for main table - food_nutrition_list
    def store_api_data(self, food_name, qty, user_name):
        keys = []
        result = self.get_api_response(food_name)
        nutrition_list_info = result.json()

        columns = ['food_name', 'nf_total_carbohydrate', 'nf_protein', 'nf_total_fat', 'nf_sugars',
                   'serving_weight_grams', 'nf_calories']
        for values in iter(nutrition_list_info.items()):
            for index in values[1]:
                for c in columns:
                    if index[c] is None:
                        index[c] = 0
                keys = tuple(index[c] for c in columns)

        user_info = models.User.query.filter_by(username=user_name).one()

        food_name_exists = models.User_Nutrition_Details.query.filter_by(food_name=keys[0],
                                                                         iduser_nutrition=user_info.id).first() is not None
        if food_name_exists:
            query = models.User_Nutrition_Details.query.filter_by(food_name=keys[0],
                                                                  iduser_nutrition=user_info.id).first()
            result = query.quantity + qty
            query.quantity = result
            query.carbohydrate = keys[1] * result
            query.protein = keys[2] * result
            query.fat = keys[3] * result
            query.sugar = keys[4] * result
            query.serving_weight = keys[5] * result
            query.calories = keys[6] * result
            db.session.merge(query)
            db.session.commit()
        else:
            query = models.User_Nutrition_Details(food_name=keys[0], carbohydrate=(keys[1] * qty),
                                                  protein=keys[2] * qty, fat=keys[3] * qty,
                                                  sugar=keys[4] * qty, serving_weight=keys[5] * qty,
                                                  calories=keys[6] * qty,
                                                  quantity=qty, iduser_nutrition=user_info.id)
            list_new = list(keys)
            list_new.append(qty)
            list_new.append(user_info.id)
            keys_new = tuple(list_new)
            db.session.add(query, keys_new)
            db.session.commit()

        return query
