from flask import Flask, request
# import os
from flask_cors import CORS
from flask import jsonify

from src.main.CommunicationLayer import WebSocketService
from src.main.ServiceLayer.GuestRole import GuestRole
from src.main.ServiceLayer.SubscriberRole import SubscriberRole

app = Flask(__name__)
CORS(app)


# ------------------------------ GUEST ROLE SERVICES ------------------------------------#
@app.route('/register', methods=['POST'])
def register():
    req = request
    if request.is_json:
        request_dict = request.get_json()
        nickname = request_dict.get('nickname')
        password = request_dict.get('password')
        response = GuestRole.register(nickname, password)  # seems OK, checked
        if response:
            return jsonify(msg=response['msg'], data=response['response'])
        # return jsonify(msg="Registered successfully!")
    return jsonify(msg="Registration failed", data=response['response'], status=400)


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        request_dict = request.get_json()
        nickname = request_dict.get('nickname')
        password = request_dict.get('password')
        response = GuestRole.login(nickname, password)  # seems OK, need to verify later
        if response:
            return jsonify(msg=response['msg'], data=response['response'])
    return jsonify(msg="Login failed", data=response['response'], status=400)


@app.route('/display_stores', methods=['GET'])
def display_stores():
    response = GuestRole.display_stores()  # BUG
    return jsonify(data=response)  # should be list of Store objects (maybe)
    # LETS RETURN JUST THE STORE'S NAME (INSTEAD OF STORE OBJECTS)
    # return jsonify(data=["STORE1", "STORE2"])


@app.route('/view_shopping_cart', methods=['GET'])
def view_shopping_cart():
    # response = GuestRole.view_shopping_cart()
    # return jsonify(data=response)  # list of Products (Object)
    return jsonify(data=["Product1", "Product2"])


@app.route('/search_products_by', methods=['POST'])
def search_products_by():
    if request.is_json:
        request_dict = request.get_json()
        search_option = request_dict.get('search_option')  # by name, keyword or category
        input_str = request_dict.get('input')
        # response = GuestRole.search_products_by(search_option, input_str)  # list of Products (Object)
        # return jsonify(data=response)
        return jsonify(data=["Product1", "Product2"])


@app.route('/get_categories', methods=['GET'])
def get_categories():
    # response = GuestRole.get_categories()
    return jsonify(data=["category1", "category2"])


@app.route('/filter_products_by', methods=['POST'])
def filter_products_by():
    return jsonify(data=["Product1"])
    # if request.is_json:
    #     request_dict = request.get_json()
    #     products = request_dict.get('products')
    #     filter_option = request_dict.get('filter_option')  # by name, keyword or category
    #     input = request_dict.get('input')
    #     if filter_option == 1:
    #         min = input.min
    #         max = input.max
    #         response = GuestRole.search_products_by(products, filter_option, min, max)  # list of Products (Object)
    #     else:
    #         response = GuestRole.search_products_by(products, filter_option, input)  # list of Products (Object)


@app.route('/add_products_to_cart', methods=['POST'])
def add_products_to_cart():
    # if request.is_json:
    #     request_dict = request.get_json()
    #     products = request_dict.get('products')
    #     response = GuestRole.save_products_to_basket()
    return jsonify(msg="Added to cart successfully!")


@app.route('/update_shopping_cart', methods=['POST'])
def update_shopping_cart():
    return jsonify(msg="Updated successfully!")


@app.route('/purchase_products', methods=['POST'])
def purchase_products():
    # if request.is_json:
        # TODO
    return jsonify(msg="Updated successfully!")


# AND MANY MORE OTHER FUNCTIONS ..... TODO

# ------------------------------ STORE OWNER AND MANAGER ROLE SERVICES ------------------------------------#

@app.route('/add_product', methods=['POST'])
def add_product():
    if request.is_json:
        request_dict = request.get_json()
        # product_name = request_dict.get('product_name')
        response = SubscriberRole.add_product(request_dict)
        if response:
            return jsonify(msg="Congrats! Product was added!")
    return jsonify(msg="Oops, product wasn't added")

# ------------------------------ SUBSCRIBER ROLE SERVICES -------------------------------------------------#


@app.route('/logout', methods=['GET'])
def logout():
    response = SubscriberRole.logout()
    if response:
        return jsonify(msg="Logged out successfully")
    return jsonify(msg="Logout failed")


@app.route('/open_store', methods=['POST'])
def open_store():
    if request.is_json:
        request_dict = request.get_json()
        store_name = request_dict.get('store_name')
        result = SubscriberRole.open_store(store_name)
        WebSocketService.open_store(store_name, SubscriberRole.username, result)
        # if response:
        return jsonify(data=result['response'], msg=result['msg'])
    return jsonify(msg="Oops, store wasn't opened")


@app.route('/view_personal_purchase_history', methods=['GET'])
def view_personal_purchase_history():
    # response = SubscriberRole.view_personal_purchase_history()
    # return jsonify(msg="Logged out successfully", data=response) # NEED TO BE CHEKED, STAM ASITI

    return jsonify(data=["purchase1", "purchase2"])


# ------------------------------ SYSTEM MANAGER ROLE SERVICES ---------------------------------------------#

@app.route('/view_user_purchase_history', methods=['POST'])
def view_user_purchase_history():
    if request.is_json:
        request_dict = request.get_json()
        viewed_user = request_dict.get('nickname')
    #     response = SystemManagerRole.view_user_purchase_history(viewed_user)
    #     if response:  # if not None
    #         return jsonify(msg="success", data=response)
    # return jsonify(msg="fail", data=response)
    return jsonify(data=["user_purchase1", "user_purchase2"])


@app.route('/view_store_purchases_history', methods=['POST'])
def view_store_purchases_history():
    if request.is_json:
        request_dict = request.get_json()
        store_name = request_dict.get('store_name')
    #     response = SystemManagerRole.view_store_purchases_history(store_name)
    #     if response:  # if not None
    #         return jsonify(msg="success", data=response)
    # return jsonify(msg="fail", data=response)
    return jsonify(data=["store_purchase1", "store_purchase2"])


# ------------------------------ TRADE CONTROL SERVICE ----------------------------------------------------#
