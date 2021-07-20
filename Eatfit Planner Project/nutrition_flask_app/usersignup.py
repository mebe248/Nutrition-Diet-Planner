from nutrition_flask_app import models
from nutrition_flask_app.app import db
import enum


class result(enum.Enum):
    passwordmatch = 1
    passwordnotmatch= 2
    nouser = 3


class Usersignup:

    def create_user_account(self, full_name, user_name, email, password):
        user_count = models.User.query.filter_by(username=user_name).count()
        if user_count == 0:
            user_new = models.User(full_name=full_name, username=user_name, email=email, password=password)
            db.session.add(user_new)
            db.session.commit()
            return 1
        else:
            return 0

    def signin_user(self, user_name, password):
        user_count = models.User.query.filter_by(username=user_name).count()
        if user_count == 1:
            query_user = models.User.query.filter_by(username=user_name).one()
            if query_user.password == password:
                return result.passwordmatch.value
            else:
                return result.passwordnotmatch.value
        else:
            return result.nouser
