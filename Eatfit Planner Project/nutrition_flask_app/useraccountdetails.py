from nutrition_flask_app import models
from nutrition_flask_app.app import db

class Useraccount:

    def get_user_details(self, user_name):
        user_exists = db.session.query(models.User).filter_by(username=user_name).first() is not None
        if user_exists:
            user_info = models.User.query.filter_by(username=user_name).first()
            user_diet_info = models.User_Food_Plan.query.filter_by(iduser_plan=user_info.id).one()
            account_info = [user_info.full_name, user_diet_info.user_diet_plan]
            return account_info
