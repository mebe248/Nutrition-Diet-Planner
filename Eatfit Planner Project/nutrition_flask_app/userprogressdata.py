from nutrition_flask_app import models
from nutrition_flask_app.app import db
from datetime import datetime


class Userprogress:

    def get_user_progress(self, user_name):
        user_info = models.User.query.filter_by(username=user_name).one()
        user_diet_info = models.User_Food_Plan.query.filter_by(iduser_plan=user_info.id).one()

        # Calculating total values for Carb,protein,fat from the nutrition table
        carb_total = db.session.query(
            db.func.sum(models.User_Nutrition_Details.carbohydrate).label("total_carbohydrate")).filter_by(
            iduser_nutrition=user_info.id).one()
        protein_total = db.session.query(
            db.func.sum(models.User_Nutrition_Details.protein).label("total_protein")).filter_by(
            iduser_nutrition=user_info.id).one()
        fat_total = db.session.query(db.func.sum(models.User_Nutrition_Details.fat).label("total_fat")).filter_by(
            iduser_nutrition=user_info.id).one()
        sugar_total = db.session.query(db.func.sum(models.User_Nutrition_Details.sugar).label("total_sugar")) \
            .filter_by(iduser_nutrition=user_info.id).one()
        weight_total = db.session.query(
            db.func.sum(models.User_Nutrition_Details.serving_weight).label("total_serving_weight")).filter_by(
            iduser_nutrition=user_info.id).one()
        calories_total = db.session.query(
            db.func.sum(models.User_Nutrition_Details.calories).label("total_calories")).filter_by(
            iduser_nutrition=user_info.id).one()

        # Checking if user exists in statistics table
        user_exists = db.session.query(models.User_Day_Statistics).filter_by(
            iduser_statistics=user_info.id) is not None

        if user_exists:
            day_exists = db.session.query(models.User_Day_Statistics).filter_by(days=0,
                                                                                iduser_statistics=user_info.id).first() \
                         is not None

            if day_exists:

                user_progress_time = models.User_Day_Statistics.query.filter_by(iduser_statistics=user_info.id).first()
                day_difference = int(
                    int(datetime.now().strftime('%d')) - int(user_progress_time.timestamp.strftime('%d')))

                exists_day_difference = db.session.query(models.User_Day_Statistics).filter_by(days=day_difference,
                                                                                               iduser_statistics=
                                                                                               user_info.id).first() is not None

                if exists_day_difference:

                    user_statistics_new = models.User_Day_Statistics.query.filter_by(iduser_statistics=user_info.id,
                                                                                     days=day_difference).one()
                    user_statistics_new.total_carbohydrate = carb_total[0]
                    user_statistics_new.total_protein = protein_total[0]
                    user_statistics_new.total_fat = fat_total[0]
                    user_statistics_new.total_sugar = sugar_total[0]
                    user_statistics_new.total_serving_weight = weight_total[0]
                    user_statistics_new.total_calories = calories_total[0]
                    user_statistics_new.days = day_difference
                    db.session.merge(user_statistics_new)
                    db.session.commit()
                else:
                    user_statistics_new = models.User_Day_Statistics(days=day_difference,
                                                                     total_carbohydrate=carb_total[0],
                                                                     total_protein=protein_total[0],
                                                                     total_fat=fat_total[0],
                                                                     total_sugar=sugar_total[0],
                                                                     total_serving_weight=weight_total[0],
                                                                     total_calories=calories_total[0],
                                                                     iduser_statistics=user_info.id)
                    db.session.add(user_statistics_new)
                    db.session.commit()
            else:

                user_statistics = models.User_Day_Statistics(days=0, total_carbohydrate=carb_total[0],
                                                             total_protein=protein_total[0],
                                                             total_fat=fat_total[0], total_sugar=sugar_total[0],
                                                             total_serving_weight=weight_total[0],
                                                             total_calories=calories_total[0],
                                                             iduser_statistics=user_info.id)
                db.session.add(user_statistics)
                db.session.commit()
        else:

            user_statistics = models.User_Day_Statistics(days=0, total_carbohydrate=carb_total[0],
                                                         total_protein=protein_total[0],
                                                         total_fat=fat_total[0], total_sugar=sugar_total[0],
                                                         total_serving_weight=weight_total[0],
                                                         total_calories=calories_total[0],
                                                         iduser_statistics=user_info.id)
            db.session.add(user_statistics)
            db.session.commit()

        keys_values = [carb_total[0], protein_total[0], fat_total[0], sugar_total[0], weight_total[0],
                       calories_total[0],
                       user_info.id, user_diet_info.user_carbohydrate_ratio, user_diet_info.user_protein_ratio,
                       user_diet_info.user_fat_ratio]

        return keys_values
