from nutrition_flask_app.app import db, DB_NAME
from os import path
from sqlalchemy import func


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'username': self.username,
            'email': self.email,
            'password': self.password,
        }

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')


class User_Food_Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_diet_plan = db.Column(db.String(100), nullable=False)
    user_carbohydrate_ratio = db.Column(db.Integer, nullable=True)
    user_protein_ratio = db.Column(db.Integer, nullable=True)
    user_fat_ratio = db.Column(db.Integer, nullable=True)

    iduser_plan = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    iduser_plan_rel = db.relationship('User', foreign_keys='User_Food_Plan.iduser_plan')

    def serialize(self):
        return {
            'user_diet_plan': self.user_diet_plan,
            'user_carbohydrate_ratio': self.user_carbohydrate_ratio,
            'user_protein_ratio': self.user_protein_ratio,
            'user_fat_ratio ': self.user_fat_ratio,

        }


class User_Nutrition_Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(100), nullable=False)
    carbohydrate = db.Column(db.Integer, nullable=True)
    protein = db.Column(db.Integer, nullable=True)
    fat = db.Column(db.Integer, nullable=True)
    sugar = db.Column(db.Integer, nullable=True)
    serving_weight = db.Column(db.Integer, nullable=True)
    calories = db.Column(db.Integer, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)

    iduser_nutrition = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    iduser_nutrition_rel = db.relationship('User', foreign_keys='User_Nutrition_Details.iduser_nutrition')

    def serialize(self):
        return {
            'food_name': self.food_name,
            'carbohydrate': self.carbohydrate,
            'protein': self.protein,
            'fat': self.fat,
            'sugar': self.sugar,
            'serving_weight': self.serving_weight,
            'calories': self.calories,
            'quantity': self.quantity
        }


class User_Day_Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    days = db.Column(db.Integer, nullable=False)
    total_carbohydrate = db.Column(db.Integer, nullable=True)
    total_protein = db.Column(db.Integer, nullable=True)
    total_fat = db.Column(db.Integer, nullable=True)
    total_sugar = db.Column(db.Integer, nullable=True)
    total_serving_weight = db.Column(db.Integer, nullable=True)
    total_calories = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.current_timestamp())

    iduser_statistics = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    iduser_statistics_rel = db.relationship('User', foreign_keys='User_Day_Statistics.iduser_statistics')

    def serialize(self):
        return {
            'total_carbohydrate': self.total_carbohydrate,
            'total_protein': self.total_protein,
            'total_fat': self.total_fat,
            'total_sugar': self.total_sugar,
            'total_serving_weight': self.total_serving_weight,
            'total_calories': self.total_calories
        }


if not path.exists('nutrition_flask_app/' + DB_NAME):
    db.create_all()
    print('Database created')

