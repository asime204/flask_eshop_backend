from flask import Blueprint, request, jsonify
from ..models import Prints, User, Cart
from ..apiauthhelper import basic_auth_required, token_auth_required, basic_auth
from flask_cors import cross_origin, CORS
from flask_login import current_user
import requests


api = Blueprint('api', __name__)
CORS(api, origins = ['*'])

@api.route('/api/populate')
@cross_origin
def populate():

    url = "https://api.nasa.gov/planetary/apod?api_key=kFHR3AFVVyE6UWjaIGXtd1dHO4ey1Z9SZcGlG6J0&start_date=2022-12-01&end_date=2023-01-01"

    monthly_apod = {}

    response = requests.get(url)
    if response.status_code == 200:
        apod_month_list = response.json()
        # print(apod_month_list)
        for apod in apod_month_list:
            monthly_apod['title'] = apod['title']
            monthly_apod['img_url'] = apod['url']
            monthly_apod['price'] = 20 # RNG here next

            title = monthly_apod['item_name']
            img_url = monthly_apod['img_url']
            price =  monthly_apod['price']

            print = Prints(title, img_url, price)
            print.saveToDB()


            continue
            # return render_template('home.html', posts = posts)
    print = Prints.query.all()
    print(print)
    return jsonify([print.serialize for print in print])
  
@api.route('/api/prints')
@cross_origin()
def getPrints():
    prints = Prints.query.all()
    print(prints)

    new_prints = []
    for p in prints:
        new_prints.append(p.to_dict())
    
    return {
        'status': 'ok',
        'totalResults': len(prints),
        'prints': [p.to_dict() for p in prints]
    }

@api.route('/api/cart')
@cross_origin()
def getCart():
    cart = Cart.query.all()

    cart_items = []
    for p in cart:
        cart_items.append(p.to_dict())
    
    return {
        'status': 'ok',
        'totalResults': len(cart),
        'prints': [p.to_dict() for p in cart]
    }

@api.route('/api/prints/<int:print_id>')
# @cross_origin()
def getPrint(print_id):
    print = Prints.query.get(print_id)
    if print:
        return {
            'status': 'ok',
            'totalResults': 1,
            'print': 
            print.to_dict()
        }
    else:
        return {
            'status': 'not ok',
            'message': 'The post you are looking for does not exist.'
        }



########## CONVERT THIS TO ADDTOCART ROUTE##########

# @api.route('/api/posts/create', methods = ["POST"])
# # @cross_origin()
# @token_auth_required
# def addToCart(user):
    
#     data = request.json ## WHERE IS THIS COMING FROM?

#     print = data['print_id']
#     img_url = data['img_url']

#     ## for now, accept the user_id parameter from the JSON body
#     ### HOWEVER, this is not the correct way, we need to authenticate them somehow
#     #### we will cover this in BASIC/TOKEN auth

#     cart = Cart(user.id, print_id, quantity)
#     cart.saveToDB()
    
#     return {
#         'status': 'ok',
#         'message': 'Succesfullly added to Cart!'
#     }

# @api.route('/api/posts/update/<post_id>', methods = ["POST"])
# @basic_auth_required
# def updatePost(user, post_id):
#     data = request.json

#     title = data['title']
#     img_url = data['img_url']

#     ## for now, accept the user_id parameter from the JSON body
#     ### HOWEVER, this is not the correct way, we need to authenticate them somehow
#     #### we will cover this in BASIC/TOKEN auth

#     post = Post(title, img_url, user.id)
#     post.saveToDB()
    
#     return {
#         'status': 'ok',
#         'message': 'Succesfullly created post!'
#     }

################# AUTH ROUTES API ####################

@api.route('/api/signup', methods=["POST"])
@cross_origin()
def signUpPageAPI():
    headers = request.headers
    print(headers)

    data = request.json

    username = data['username']
    email = data['email']
    password = data['password']
    


    # add user to database
    user = User(username, email, password)

    user.saveToDB()

    return {
        'status': 'ok',
        'message': "Successfully created an account!"
    }

@api.route('/api/login', methods=["POST"])
@basic_auth.login_required
def getToken():
    user = basic_auth.current_user()
    return {
        'status': 'ok',
        'user': user.to_dict()
    }