from flask import jsonify, make_response, request
from nutrition_flask_app.app import app, login_manager, db
from nutrition_flask_app.usersignup import Usersignup
from nutrition_flask_app.userfooddata import Userfooddetails
from nutrition_flask_app.userprogressdata import Userprogress
from nutrition_flask_app.useraccountdetails import Useraccount
from nutrition_flask_app import models
from flask_login import login_user, login_required, logout_user, current_user

nutritiondiet_user = Usersignup()
nutritiondiet_food = Userfooddetails()
nutritiondiet_progress = Userprogress()
nutritiondiet_user_account = Useraccount()


@login_manager.user_loader
def load_user(user_id):
    user = models.User.query.filter_by(id=user_id).first()
    return user


"""
  Home Page 
"""


@app.route('/')
def home():
    return "Welcome to the Nutrition Diet planner"


"""
   Sign-up page for the users
"""


@app.route('/register', methods=['POST', 'GET'])
def register_user():
    try:
        request_body = request.get_json()
        if 'full_name' and 'user_name' and 'email' and 'password' not in request_body:
            return make_response(jsonify(error="The body must contain 'full_name','user_name', 'email' and 'password'"),
                                 400)
        full_name = request_body['full_name']
        user_name = request_body['user_name']
        email = request_body['email']
        password = request_body['password']

        result = nutritiondiet_user.create_user_account(full_name, user_name, email, password)

        user = models.User.query.filter_by(username=user_name).first()
        if result == 1:
            login_user(user)
            return make_response(jsonify(f"Account created for {user_name}"), 200)
        else:
            return make_response(jsonify(
                message=f"Account already exist with username {user_name}.Please sign up with different user name."),
                400)
    except Exception as e:
        print(f'error: {str(e)}')
        return make_response(jsonify(error=str(e)), 400)


"""
    Sign-in info page for the users
"""


@app.route('/signin', methods=['POST', 'GET'])
def user_signin():
    if request.method == 'GET':
        return make_response(jsonify(f" Please sign in to your account "), 200)

    elif request.method == 'POST':
        try:
            request_body = request.get_json()
            if 'user_name' and 'password' not in request_body:
                return make_response(jsonify(error="The body must contain 'user_name' and 'password'"), 400)
            user_name = request_body['user_name']
            password = request_body['password']

            user = models.User.query.filter_by(username=user_name).first()

            if not user:
                return make_response(
                    jsonify(message=f"Account with {user_name} does not exist .Please sign up for a new account."), 400)
            else:
                result = nutritiondiet_user.signin_user(user_name, password)
                if result == 1:
                    login_user(user)
                    return make_response(jsonify(f"{user_name} signed in! "), 200)
                elif result == 2:
                    return make_response(
                        jsonify(message=f" Username and Password does not match! .Please enter your password again."),
                        400)

        except Exception as e:
            print(f'error: {str(e)}')
            return make_response(jsonify(error=str(e)), 400)


"""
    Users- Home page
"""


@app.route('/home', methods=['POST', 'GET'])
@login_required
def user_home():
    return f"User Home page - Hi, {current_user.username} "


"""
   Home Page - Enter the food plan details (Total ratio limit of Carb,Fat and Protein based on the food plan)
"""


@app.route('/home/<string:username>/foodplan', methods=['POST'])
@login_required
def user_foodplan_details(username):
    try:

        request_body = request.get_json()
        if 'food_plan' and 'carbohydrate_limit' and 'protein_limit' and 'fat_limit' not in request_body:
            return make_response(jsonify(error="The body must contain 'food_plan', 'carbohydrate_limit',\
                                                'protein_limit' and 'fat_limit'"), 400)

        food_plan = request_body['food_plan']
        carbohydrate_limit = request_body['carbohydrate_limit']
        protein_limit = request_body['protein_limit']
        fat_limit = request_body['fat_limit']
        user_info = nutritiondiet_food.store_user_food_plan(food_plan, carbohydrate_limit, protein_limit, fat_limit,
                                                            username)
        return make_response(
            jsonify(f"User {username}'s food plan:{user_info.user_diet_plan}, "
                    f' Carbohydrate ratio: {user_info.user_carbohydrate_ratio}%,'
                    f' Protein ratio: {user_info.user_protein_ratio}%,'
                    f' Fat ratio: {user_info.user_fat_ratio}%'), 200)
    except Exception as e:
        print(f'error: {str(e)}')
        return make_response(jsonify(error=str(e)), 400)


""""
   Home page -Fetching and displaying food details from external API
"""


@app.route('/home/<string:username>/food/add', methods=['POST', 'GET'])
@login_required
def fetch_api_food_details(username):
    try:

        request_body = request.get_json()
        if 'food_name' and 'quantity' not in request_body:
            return make_response(jsonify(error="The body must contain 'food_name' and 'quantity' "), 400)
        food_name = request_body['food_name']
        quantity = request_body['quantity']
        response = nutritiondiet_food.get_api_response(food_name)
        if response is None:
            return make_response(jsonify(error="Error fetching data from external API"), 500)
        else:
            result = nutritiondiet_food.store_api_data(food_name, quantity, username)
        return make_response(jsonify(f'Added {result.food_name}!'), 200)

    except Exception as e:
        print(f'error: {str(e)}')
        return make_response(jsonify(error=str(e)), 400)


""""
   Home page -Clearing the entered data on the sections
"""


@app.route('/home/<string:username>/clear', methods=['GET'])
@login_required
def user_clear_data(username):
    try:
        qry = models.User.query.filter_by(username=username).one()
        models.User_Nutrition_Details.query.filter_by(iduser_nutrition=qry.id).delete()
        models.User_Day_Statistics.query.filter_by(iduser_statistics=qry.id).delete()
        db.session.commit()
        return make_response(jsonify(f'All the entered data are cleared'), 200)

    except Exception as e:
        print(f'error: {str(e)}')
        return make_response(jsonify(error=str(e)), 400)


"""" 
    Progress page - Showing the total ratio of the carb,protein and fat limit consumed by the user .
"""


@app.route('/progress/<string:username>', methods=['GET'])
@login_required
def user_progress_ratio(username):
    try:
        total_keys = nutritiondiet_progress.get_user_progress(username)
        ratio_carb = round((total_keys[0] / total_keys[4]) * 100, 2)
        ratio_fat = round((total_keys[1] / total_keys[4]) * 100, 2)
        ratio_protein = round((total_keys[2] / total_keys[4]) * 100, 2)

        return make_response(
            jsonify(
                f' Consumed Carbohydrate: You have reached {ratio_carb}% of {total_keys[7]}%, '
                f' Consumed Protein: You have reached {ratio_protein}% of {total_keys[8]}%, '
                f' Consumed Fat: You have reached {ratio_fat}% of {total_keys[9]}%'), 200)
    except Exception as e:
        print(f' error: {str(e)}')
        return make_response(jsonify(error=str(e)), 400)


"""" 
    User page - Information on account
"""


@app.route('/account/<string:user_name>', methods=['GET'])
@login_required
def user_account_details(user_name):
    try:
        result = nutritiondiet_user_account.get_user_details(user_name)
        return make_response(
            jsonify(
                f' Name: {result[0]}, username : {user_name}, Food plan: {result[1]}'), 200)

    except Exception as e:
        print(f' error: {str(e)}')
        return make_response(jsonify(error=str(e)), 400)


"""
    User - Logout
"""


@app.route('/account/logout')
@login_required
def user_logout():
    logout_user()
    return make_response(jsonify(f'User Logged out!'))
