import eventlet
import jsonpickle
from flask import Flask, request
# import os
from flask_cors import CORS
from flask import jsonify
from dateutil.parser import *
# from dateutil import parser

# from src.main.CommunicationLayer import WebSocketService
from src.main.CommunicationLayer.StorePublisher import StorePublisher
from src.main.DomainLayer.StoreComponent.AppointmentStatus import AppointmentStatus
from src.main.DomainLayer.StoreComponent.ManagerPermission import ManagerPermission
from src.main.ServiceLayer.GuestRole import GuestRole
from src.main.ServiceLayer.StoreOwnerOrManagerRole import StoreOwnerOrManagerRole
from src.main.ServiceLayer.SubscriberRole import SubscriberRole
from src.main.ServiceLayer.SystemManagerRole import SystemManagerRole
from src.main.ServiceLayer.TradeControlService import TradeControlService
from flask_socketio import SocketIO, join_room, leave_room
import os

app = Flask(__name__)
CORS(app)

socket = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet')

# 1 - purchase
# 2 - add+remove manager
# 3 - else

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
    return jsonify(data=response)


@app.route('/display_stores_products', methods=['POST'])
def display_stores_products():
    if request.is_json:
        request_dict = request.get_json()
        store_name = request_dict.get('store_name')
        store_info_flag = request_dict.get('store_info_flag')
        products_info_flag = request_dict.get('products_info_flag')
        response = GuestRole.display_stores_or_products_info(store_name, store_info_flag, products_info_flag)
        if response:
            return jsonify(msg=response["msg"], data=response["response"])
        return jsonify(msg="get store products failed", data=response["response"], status=400)


@app.route('/view_shopping_cart', methods=['GET'])
def view_shopping_cart():
    response = GuestRole.view_shopping_cart()
    return jsonify(data=response["response"], msg=response["msg"])


@app.route('/search_products_by', methods=['POST'])
def search_products_by():
    if request.is_json:
        request_dict = request.get_json()
        search_option = request_dict.get('search_option')  # by name, keyword or category
        input_str = request_dict.get('input')
        response = GuestRole.search_products_by(search_option, input_str)  # list of Products (Object)
        return jsonify(msg=response["msg"], data=response["response"])
    return jsonify(msg="Oops, communication error.", data=[])


@app.route('/filter_products_by', methods=['POST'])
def filter_products_by():
    if request.is_json:
        request_dict = request.get_json()
        filter_option = request_dict.get('filter_option')  # by name, keyword or category
        products_ls = request_dict.get('products_ls')

        if filter_option == 1:
            min_price = request_dict.get('min_price')
            max_price = request_dict.get('max_price')
            response = GuestRole.filter_products_by(products_ls, filter_option, min_price=min_price, max_price=max_price)  # list of Products (Object)
        else:
            if filter_option == 2:
                category = request_dict.get('category')
                response = GuestRole.filter_products_by(products_ls, filter_option, category=category)  # list of Products (Object)

        return jsonify(msg=response["msg"], data=response["response"])
    return jsonify(msg="Oops, communication error.", data=[])


@app.route('/get_categories', methods=['GET'])
def get_categories():
    # response = GuestRole.get_categories()
    return jsonify(data=["category1", "category2"])


@app.route('/add_products_to_cart', methods=['POST'])
def add_products_to_cart():
    if request.is_json:
        request_dict = request.get_json()
        products = request_dict.get('products')
        response = GuestRole.save_products_to_basket(products)
        # if response:
        return jsonify(msg=response['msg'], data=response['response'])
    # return jsonify(msg="Registration failed", data=response['response'], status=400)


@app.route('/update_or_remove_from_shopping_cart', methods=['POST'])
def update_or_remove_from_shopping_cart():
    # flag: str, products_details: [{"product_name": str, "store_name": str, "amount": int}]) \

    if request.is_json:
        request_dict = request.get_json()
        action_type = request_dict.get('action_type')
        products_details = [{'product_name': request_dict.get("product_name"),
                             'store_name': request_dict.get("store_name"),
                             'amount': request_dict.get("amount")
                            }]
        response = GuestRole.update_shopping_cart(action_type, products_details)
        if response:
            return jsonify(msg=response['msg'], data=response['response'])
    return jsonify(msg="purchase confirmation failed", data=response["response"], status=400)


@app.route('/purchase_products', methods=['GET'])
def purchase_products():
    response = GuestRole.purchase_products()
    if response:
        # print(response)
        # print(purchases)
        # print(purchases[0])
        # print(purchases[0]["store_name"])

        # print("after handle")
        return jsonify(data=response)
    return jsonify(msg="purchase products failed", data=response["response"], status=400)


@app.route('/confirm_purchase', methods=['POST'])
def confirm_purchase():
    if request.is_json:
        request_dict = request.get_json()
        delivery_details = request_dict.get('delivery_details')
        payment_details = request_dict.get('payment_details')
        details = request_dict.get("purchases")
        response = GuestRole.confirm_payment(delivery_details, payment_details, details)
        if response['response']:
            # purchases = details["purchases"]
            # map(lambda purchase: handle_purchase_msg(purchase["store_name"]), purchases)
            for purchase in details["purchases"]:
                handle_purchase_msg(purchase["store_name"])
        if response:
            return jsonify(msg=response['msg'], data=response['response'])
    return jsonify(msg="purchase confirmation failed", data=response["response"], status=400)


# AND MANY MORE OTHER FUNCTIONS ..... TODO

# ------------------------------ STORE OWNER AND MANAGER ROLE SERVICES ------------------------------------#


@app.route('/get_managed_stores', methods=['GET'])
def get_managed_stores():
    response = StoreOwnerOrManagerRole.get_managed_stores()
    return jsonify(data=response)


@app.route('/get_manager_permissions', methods=['POST'])
def get_manager_permissions():
    if request.is_json:
        request_dict = request.get_json()
        store_name = request_dict.get('store_name')  # str
        response = StoreOwnerOrManagerRole.get_manager_permissions(store_name)
        numlist = [enum.value for enum in response]
        return jsonify(data=numlist)
    return jsonify(data=[])


@app.route('/get_owned_stores', methods=['GET'])
def get_owned_stores():
    response = StoreOwnerOrManagerRole.get_owned_stores()
    return jsonify(data=response)


@app.route('/appoint_store_manager', methods=['POST'])
def appoint_store_manager():
    if request.is_json:
        request_dict = request.get_json()
        appointee_nickname = request_dict.get('appointee_nickname')  # str
        store_name = request_dict.get('store_name')  # str
        permissions = request_dict.get('permissions')  # list of tuples
        response = StoreOwnerOrManagerRole.appoint_store_manager(appointee_nickname, store_name, permissions)
        if response:
            return jsonify(msg=response["msg"], data=response["response"])
    return jsonify(msg="Oops, communication error")


@app.route('/remove_manager', methods=['POST'])
def remove_manager():
    if request.is_json:
        request_dict = request.get_json()
        appointee_nickname = request_dict.get('nickname')  # str
        store_name = request_dict.get('store_name')  # str
        response = StoreOwnerOrManagerRole.remove_manager(store_name, appointee_nickname)
        if response:
            return jsonify(msg="Removed manager " + appointee_nickname + " successfully!")
    return jsonify(msg="Oops, communication error")


@app.route('/remove_owner', methods=['POST'])
def remove_owner():
    if request.is_json:
        request_dict = request.get_json()
        appointee_nickname = request_dict.get('nickname')  # str
        store_name = request_dict.get('store_name')  # str
        response = StoreOwnerOrManagerRole.remove_owner(appointee_nickname, store_name)
        if response:
            handle_remove_owner_msg(appointee_nickname, store_name)
            return jsonify(msg=response['msg'], data=response['response'])
    return jsonify(msg="Oops, communication error--")
# remove_owner(self, appointee_nickname: str, store_name: str)


@app.route('/appoint_store_owner', methods=['POST'])
def appoint_store_owner():
    if request.is_json:
        request_dict = request.get_json()
        appointee_nickname = request_dict.get('appointee_nickname')  # str
        store_name = request_dict.get('store_name')  # str
        response = StoreOwnerOrManagerRole.appoint_additional_owner(appointee_nickname, store_name)
        if response:
            if response["msg"] == "The request is pending approval":
                # ----------------appointment agreement----------------------
                msg = f"New owner appointment at store {store_name} - action required!"
                notify_all(store_name, {'username': appointee_nickname, 'messages': msg, 'store': store_name}, "agreement")
            elif response["response"]:
                # if add_subscriber_to_store(store_name, appointee_nickname, False):
                #     print(_users)
                #     # create_new_publisher()
                #     if appointee_nickname in _users:
                #         print(_users[appointee_nickname])
                #         join_room(store_name, _users[appointee_nickname])
                appointee_msg = {'messages':'Congratulations! you are now one of ' + store_name + ' owners', 'storename': store_name}
                if appointee_nickname in _users:
                    add_subscriber_to_store(store_name, appointee_nickname, True)
                    # get_store(store_name).add_personal_msg(appointee_nickname, appintee_msg)
                    _users_with_their_own_rooms.append(appointee_nickname)
                    join_room(store_name, _users[appointee_nickname])
                    join_room(appointee_nickname, _users[appointee_nickname])
                    socket.emit('message', msg=appointee_msg, room=appointee_nickname)
                else:
                    add_subscriber_to_store(store_name, appointee_nickname, False)
                    get_store(store_name).add_personal_msg(appointee_nickname, appointee_msg)
                    # join_room(appointee_nickname, _users[appointee_nickname])
            return jsonify(msg=response["msg"], data=response["response"])
    return jsonify(msg="Oops, communication error")


@app.route('/handle_appointment_agreement_response', methods=['POST'])
def handle_appointment_agreement_response():
    if request.is_json:
        request_dict = request.get_json()
        appointee_nickname = request_dict.get('appointee_nickname')
        store_name = request_dict.get('store_name')
        appointment_agreement_response = request_dict.get('appointment_agreement_response')
        if appointment_agreement_response == 1:
            appointment_agreement_response = AppointmentStatus.DECLINED
        if appointment_agreement_response == 2:
            appointment_agreement_response = AppointmentStatus.APPROVED
        response = StoreOwnerOrManagerRole.update_agreement_participants(appointee_nickname, store_name,
                                                                         appointment_agreement_response)
        if response:
            # check is the status of the agreement is approved already
            if response["response"]:
                status = StoreOwnerOrManagerRole.get_appointment_status(appointee_nickname, store_name)
                if status == AppointmentStatus.APPROVED:
                    response = StoreOwnerOrManagerRole.appoint_additional_owner(appointee_nickname, store_name)
                    add_subscriber_to_store(store_name, appointee_nickname, False)
                    msg = f"New owner {appointee_nickname} appointed at store {store_name}!"
                    notify_all(store_name, {'username': appointee_nickname, 'messages': msg, 'store': store_name}, "agreement")
            return jsonify(msg=response["msg"])
    return jsonify(msg="Oops, communication error")


@app.route('/get_managers_appointees', methods=['POST'])
def get_managers_appointees():
    if request.is_json:
        request_dict = request.get_json()
        store_name = request_dict.get('store_name')  # str
        response = StoreOwnerOrManagerRole.get_appointees(store_name, "MANAGERS")
        return jsonify(data=response)
    return jsonify(data=[])


@app.route('/get_owners_appointees', methods=['POST'])
def get_owners_appointees():
    if request.is_json:
        request_dict = request.get_json()
        store_name = request_dict.get('store_name')  # str
        response = StoreOwnerOrManagerRole.get_appointees(store_name, "OWNERS")
        return jsonify(data=response)
    return jsonify(data=[])


def numbersToEnum(ls):
    enumList: ManagerPermission = []
    for num in ls:
        if num == 1 and (ManagerPermission.EDIT_INV not in enumList):
            enumList.append(ManagerPermission.EDIT_INV)
        if num == 2 and (ManagerPermission.EDIT_POLICIES not in enumList):
            enumList.append(ManagerPermission.EDIT_POLICIES)
        if num == 3 and (ManagerPermission.APPOINT_OWNER not in enumList):
            enumList.append(ManagerPermission.APPOINT_OWNER)
        if num == 4 and (ManagerPermission.DEL_OWNER not in enumList):
            enumList.append(ManagerPermission.DEL_OWNER)
        if num == 5 and (ManagerPermission.APPOINT_MANAGER not in enumList):
            enumList.append(ManagerPermission.APPOINT_MANAGER)
        if num == 6 and (ManagerPermission.EDIT_MANAGER_PER not in enumList):
            enumList.append(ManagerPermission.EDIT_MANAGER_PER)
        if num == 7 and (ManagerPermission.DEL_MANAGER not in enumList):
            enumList.append(ManagerPermission.DEL_MANAGER)
        if num == 8 and (ManagerPermission.CLOSE_STORE not in enumList):
            enumList.append(ManagerPermission.CLOSE_STORE)
        if num == 9 and (ManagerPermission.USERS_QUESTIONS not in enumList):
            enumList.append(ManagerPermission.USERS_QUESTIONS)
        if num == 10 and (ManagerPermission.WATCH_PURCHASE_HISTORY not in enumList):
            enumList.append(ManagerPermission.WATCH_PURCHASE_HISTORY)
    return enumList


@app.route('/edit_manager_permissions', methods=['POST'])
def edit_manager_permissions():
    if request.is_json:
        request_dict = request.get_json()
        store_name = request_dict.get('store_name')  # str
        appointee_nickname = request_dict.get('appointee_nickname')  # str
        permissions = request_dict.get('permissions')  # str
        response = StoreOwnerOrManagerRole.edit_manager_permissions(store_name, appointee_nickname, permissions)
        if response:
            return jsonify(data=response, msg="Permissions of manager " + appointee_nickname + " were updated successfully!")
        else:
            return jsonify(data=False, msg="Oops, update permissions failed.")
    return jsonify(data=False, msg="Oops, communication error.")


@app.route('/view_store_purchases_history', methods=['POST'])
def view_store_purchases_history():
    if request.is_json:
        request_dict = request.get_json()
        store_name = request_dict.get('store_name')  # str
        response = StoreOwnerOrManagerRole.display_store_purchases(store_name)
        return jsonify(msg=response["msg"], data=response["response"])
    return jsonify(msg="Oops, communication error.", data=[])


@app.route('/get_policies', methods=['POST'])
def get_policies():
    if request.is_json:
        request_dict = request.get_json()
        store_name = request_dict.get('store_name')  # str
        policy_type = request_dict.get('policy_type')  # str
        response = StoreOwnerOrManagerRole.get_policies(policy_type, store_name)
        return jsonify(msg=response["msg"], data=response["response"])

    return jsonify(msg="Oops, communication error.")


@app.route('/get_purchase_operator', methods=['POST'])
def get_purchase_operator():
    if request.is_json:
        request_dict = request.get_json()
        store_name = request_dict.get('store_name')  # str
        response = StoreOwnerOrManagerRole.get_purchase_operator(store_name)
        if response == "xor" or response == "and" or response == "or":
            return jsonify(msg="Retrieved purchases policies operator successfully!", data=response)

    return jsonify(msg="Oops, communication error.")


@app.route('/set_purchase_operator', methods=['POST'])
def set_purchase_operator():
    if request.is_json:
        request_dict = request.get_json()
        store_name = request_dict.get('store_name')  # str
        operator = request_dict.get('operator')  # str
        response = StoreOwnerOrManagerRole.set_purchase_operator(store_name, operator)
        return jsonify(msg="Retrieved purchases policies operator successfully!", data=response)

    return jsonify(msg="Oops, communication error.")


from datetime import datetime


@app.route('/add_and_update_purchase_policy', methods=['POST'])
def add_and_update_purchase_policy():
    if request.is_json:
        request_dict = request.get_json()
        action_type = request_dict.get('action_type')
        store_name = request_dict.get('store_name')
        policy_name = request_dict.get('policy_name')
        products = request_dict.get('products')
        min_amount = request_dict.get('min_amount')
        max_amount = request_dict.get('max_amount')
        bundle = request_dict.get('bundle')
        string_dates = request_dict.get('dates')
        dates = []
        # convert string to dates
        if string_dates is None:
            dates = None
        else:
            for date in string_dates:
                dates += [parse(date)]

        details = {"name": policy_name, "products": products,
                    "min_amount": min_amount, "max_amount": max_amount,
                    "dates": dates, "bundle": bundle}
        if action_type == 'add':
            response = StoreOwnerOrManagerRole.define_purchase_policy(store_name, details)
        else:
            response = StoreOwnerOrManagerRole.update_purchase_policy(store_name, details)
        return jsonify(msg=response['msg'], data=response['response'])

    return jsonify(msg="Oops, communication error.")


@app.route('/add_and_update_dicount_policy', methods=['POST'])
def add_and_update_dicount_policy():
    if request.is_json:
        request_dict = request.get_json()
        action_type = request_dict.get('action_type')
        store_name = request_dict.get('store_name')
        policy_name = request_dict.get('policy_name')
        product_name = request_dict.get('product_name')
        date = parse(request_dict.get('date'))
        percentage = request_dict.get('percentage')
        product = request_dict.get('product')
        min_amount = request_dict.get('min_amount')
        min_purchase_price = request_dict.get('min_purchase_price')

        discount_details = {'name': policy_name, 'product': product_name}
        discount_precondition = {'product': product,
                                'min_amount': min_amount,
                                'min_basket_price': min_purchase_price}

        if product is None and min_amount is None and min_purchase_price is None:
            discount_precondition = None
        if action_type == 'add':
            response = StoreOwnerOrManagerRole.define_discount_policy(store_name, percentage, date, discount_details, discount_precondition)
        else:
            new_policy_name = request_dict.get('new_policy_name')
            discount_details = {'name': new_policy_name, 'product': product_name}
            response = StoreOwnerOrManagerRole.update_discount_policy(store_name, policy_name, percentage, date, discount_details, discount_precondition)
        return jsonify(msg=response['msg'], data=response['response'])

    return jsonify(msg="Oops, communication error.")


@app.route('/add_composite_dicount_policy', methods=['POST'])
def add_composite_dicount_policy():
    if request.is_json:
        request_dict = request.get_json()
        store_name = request_dict.get('store_name')
        policy1 = request_dict.get('policy1')
        policy2 = request_dict.get('policy2')
        date = parse(request_dict.get('date'))
        percentage = request_dict.get('percentage')
        new_policy_name = request_dict.get('new_policy_name')
        operator = request_dict.get('operator')

        response = StoreOwnerOrManagerRole.define_composite_policy(store_name, policy1, policy2, operator, percentage, new_policy_name, date)

        return jsonify(msg=response['msg'], data=response['response'])

    return jsonify(msg="Oops, communication error.")


@app.route('/delete_policy', methods=['POST'])
def delete_policy():
    if request.is_json:
        request_dict = request.get_json()
        policy_type = request_dict.get('policy_type')
        store_name = request_dict.get('store_name')
        policy_name = request_dict.get('policy_name')

        if policy_type == 'discount':
            response = StoreOwnerOrManagerRole.delete_policy(store_name, policy_name)
        else:
            response = StoreOwnerOrManagerRole.define_purchase_policy(store_name, policy_name)
            # response = {'response': False, 'msg': 'need to implement delete_purchase_policy'}
        return jsonify(msg=response['msg'], data=response['response'])

    return jsonify(msg="Oops, communication error.")


@app.route('/add_product', methods=['POST'])
def add_product():
    if request.is_json:
        request_dict = request.get_json()
        store_name = request_dict.get('store_name')
        products_details = request_dict.get('products_details')
        response = StoreOwnerOrManagerRole.add_products(store_name, products_details)
        if response["response"]:
            return jsonify(msg="Congrats! Product was added!")
        return jsonify(msg="Oops, product wasn't added")


@app.route('/edit_product', methods=['POST'])
def edit_product():
    if request.is_json:
        errors = []
        request_dict = request.get_json()
        store_name = request_dict.get('store_name')
        product_name = request_dict.get('product_name')
        new_product_name = request_dict.get('new_product_name')
        amount = request_dict.get('amount')
        price = request_dict.get('price')
        category = request_dict.get('category')
        purchase_type = request_dict.get('purchase_type')

        # if new_product_name is not None and new_product_name == "":
        #     return jsonify(msg="Oops, product's name can't be an emtpy string.")
        # if amount is not None p amount < 0:
        #     return jsonify(msg="Oops, product's amount can't be smaller than 0.")
        # if price < 0:
        #     return jsonify(msg="Oops, product's amount can't be smaller than 0.")

        if amount is not None:
            if not StoreOwnerOrManagerRole.edit_product(store_name, product_name, "amount", amount)["response"]:
                errors.append("Product Amount")
        if price is not None:
            if not StoreOwnerOrManagerRole.edit_product(store_name, product_name, "price", price)["response"]:
                errors.append("Product Price")
        if category is not None:
            if not StoreOwnerOrManagerRole.edit_product(store_name, product_name, "category", category)["response"]:
                errors.append("Category")
        if purchase_type is not None:
            if not StoreOwnerOrManagerRole.edit_product(store_name, product_name, "purchase_type", purchase_type)["response"]:
                errors.append("Purchase Type")
        if new_product_name is not None:
            if not StoreOwnerOrManagerRole.edit_product(store_name, product_name, "name", new_product_name)["response"]:
                errors.append("Product Name")

        error_str = ""
        for error in errors:
            error_str += ", " + error

        if len(errors) == 0:
            return jsonify(msg="Congrats! Product was edited successfully!")
        return jsonify(msg="Oops, issue with product edit, couldn't update: " + error_str)


@app.route('/remove_product', methods=['POST'])
def remove_product():
    if request.is_json:
        request_dict = request.get_json()
        store_name = request_dict.get('store_name')
        products_name = request_dict.get('product_name')
        response = StoreOwnerOrManagerRole.remove_products(store_name, [products_name])
        if response:
            return jsonify(msg="Congrats! Product was removed!")
    return jsonify(msg="Oops, product wasn't removed")


@app.route('/get_product_details', methods=['POST'])
def get_product_details():
    if request.is_json:
        request_dict = request.get_json()
        store_name = request_dict.get('store_name')  # str
        products_details = request_dict.get('product_name')
        response = TradeControlService.get_product_details(store_name, products_details)
    return jsonify(data=response)


# ------------------------------ SUBSCRIBER ROLE SERVICES -------------------------------------------------#


@app.route('/logout', methods=['GET'])
def logout():
    user_type =TradeControlService.get_user_type()
    username =TradeControlService.get_curr_username()
    response = SubscriberRole.logout()
    if response:
        # if user_type == "OWNER":
        #     websocket_logout(username)
        return jsonify(msg="Logged out successfully!")
    return jsonify(msg="Logout failed")


@app.route('/open_store', methods=['POST'])
def open_store():
    if request.is_json:
        request_dict = request.get_json()
        store_name = request_dict.get('store_name')
        result = SubscriberRole.open_store(store_name)
        # websocket_open_store(TradeControlService.get_curr_username(), store_name)
        create_new_publisher(store_name, TradeControlService.get_curr_username())
        return jsonify(data=result['response'], msg=result['msg'])
    return jsonify(msg="Oops, store wasn't opened.")


@app.route('/view_personal_purchase_history', methods=['GET'])
def view_personal_purchase_history():
    response = SubscriberRole.view_personal_purchase_history()
    return jsonify(msg=response["msg"], data=response["response"]) # NEED TO BE CHEKED, STAM ASITI


# ------------------------------ SYSTEM MANAGER ROLE SERVICES ---------------------------------------------#

# @app.route('/system_initialized', methods=['POST'])
# def system_initialized():
#     result = TradeControlService.is_sys_initialized()
#     return jsonify(data=result)

@app.route('/view_user_purchase_history', methods=['POST'])
def view_user_purchase_history():
    if request.is_json:
        request_dict = request.get_json()
        viewed_user = request_dict.get('nickname')
        response = SystemManagerRole.view_user_purchase_history(viewed_user)
        if response:  # if not None
            return jsonify(msg=response['msg'], data=response['response'])
    return jsonify(msg="Oops, error with communication!", data=response)


@app.route('/view_any_store_purchase_history', methods=['POST'])
def view_any_store_purchase_history():
    if request.is_json:
        request_dict = request.get_json()
        store_name = request_dict.get('store_name')
        response = SystemManagerRole.view_store_purchases_history(store_name)
        if response:  # if not None
            return jsonify(msg=response['msg'], data=response['response'])
    return jsonify(msg="Oops, error with communication!", data=response)


@app.route('/get_visitors_cut', methods=['POST'])
def get_visitors_cut():
    if request.is_json:
        request_dict = request.get_json()
        start_date = request_dict.get('start_date')
        end_date = request_dict.get('end_date')
        # print(f'request = {request_dict}. start= {start_date}, end = {end_date}')
        response = SystemManagerRole.get_visitors_cut(start_date, end_date)
        # response = {'msg': 'succc',
        #             'response': [{'date': datetime(2020, 6, 15), 'guests': 3, 'subscribers': 4, 'store_managers': 5, 'store_owners': 6, 'system_managers': 7},
        #                          {'date': datetime(2020, 6, 16), 'guests': 3, 'subscribers': 3, 'store_managers': 3, 'store_owners': 10, 'system_managers': 3},
        #                          {'date': datetime(2020, 6, 17), 'guests': 3, 'subscribers': 6, 'store_managers': 3, 'store_owners': 3, 'system_managers': 3},
        #                          {'date': datetime(2020, 6, 18), 'guests': 3, 'subscribers': 3, 'store_managers': 1, 'store_owners': 3, 'system_managers': 3},
        #                          {'date': datetime(2020, 6, 19), 'guests': 3, 'subscribers': 3, 'store_managers': 3, 'store_owners': 0, 'system_managers': 3},
        #                          {'date': datetime(2020, 6, 20), 'guests': 7, 'subscribers': 6, 'store_managers': 5, 'store_owners': 4, 'system_managers': 3}]}
        if response:  # if not None
            return jsonify(msg=response['msg'], data=response['response'])
    return jsonify(msg="Oops, error with communication!", data=response)


# @app.route('/view_store_purchases_history', methods=['POST'])
# def view_store_purchases_history():
#     if request.is_json:
#         request_dict = request.get_json()
#         store_name = request_dict.get('store_name')
#     #     response = SystemManagerRole.view_store_purchases_history(store_name)
#     #     if response:  # if not None
#     #         return jsonify(msg="success", data=response)
#     # return jsonify(msg="fail", data=response)
#     return jsonify(data=["store_purchase1", "store_purchase2"])
#

# ------------------------------ TRADE CONTROL SERVICE ----------------------------------------------------#

@app.route('/init_system', methods=['GET'])
def init_system():
    result = TradeControlService.init_system()
    return jsonify(data=result['response'], msg=result['msg'])


@app.route('/get_user_type', methods=['GET'])
def get_user_type():
    result = TradeControlService.get_user_type()
    return jsonify(data=result)


@app.route('/get_curr_user_nickname', methods=['GET'])
def get_curr_user_nickname():
    result = TradeControlService.get_curr_username()
    return jsonify(data=result)

# ------------------------------ WEBSOCKET ----------------------------------------------------#

_users = {}  # dict of <username>: <its session ID>
_stores: [StorePublisher] = []  # list of StorePublisher
_users_with_their_own_rooms = [] # list of usernames that subsribed to room with their own name
_system_managers = [] # list <system_manager_nickname, sid, is_in_daily_cuts_window>

# @socket.on('')
@socket.on('connect')
def connect():
    print(f"connect event. sid --> {request.sid}")
    username = TradeControlService.get_curr_username()
    print(f"curr_nickname = {username}")
    if (username != ""):
        _users[username] = request.sid
        # print ("in if")
        for store in _stores:
            # print ("in for")
            if store.is_subscribed_to_store(username) and not store.is_logged_in(username):
                # print("before join")
                join_room(room=store.store_name(), sid=_users[username])
                print(f"username {username} is added as a subscriber to store {store.store_name()} publisher")
    else:
        TradeControlService.inc_todays_guests_counter()

    print(f"users list: {_users}")


# @socket.on('join')
# def join(data):
#     print("recieved join request")
#     _users[data['username']] = request.sid
#     join_room(room=data['store'], sid=_users[data['username']])
#     print(f"{data['username']} has been subscribed to store {data['storename']}")

@socket.on('join')
def websocket_open_store(data):
    if data:
        username= data['username']
        storename= data['store']
        print(f"open store u= {username}, s = {storename}")
        # socket.emit('message', {}) - works!
        print(f"stores are {_stores}")
        store = get_store(storename)
        if store is not None and store.is_subscribed_to_store(username):
            # print(f"new: open store (store name = {storename}) msg from {username} ")
            append_user_to_room(storename, username, request.sid)
            print (f"append user {username} to new store {storename}")
            # create_new_publisher(storename, username)
        else:
            print(f"store is already exists! {get_store(storename)}")
    else:
        print(f"recieved wrong join msg --> {data}")


def create_new_publisher(storename, username):
    if get_store(storename) is None:
        if username == "":
            print("no curr username")
        else:
            store = StorePublisher(storename, username)
            # print(f"store = {store}")
            _stores.append(store)
            # print(f"{storename} has been added by {username}")
            store.subscribe_owner(username, True)


def append_user_to_room(storename, username, sid):
    _users[username] = sid
    # _users[username] = flask_request.sid
    print(f"users = {_users}")
    join_room(room=storename, sid=_users[username])
    print(f"append {username} to {storename} room with sid = {sid}")
    # print(f"{username} has been subscribed to store {storename}")


@socket.on('unsubscribe')
def leave(data):
    # TODO - add check that exists
    print("socket sent msg 'unsbscribe'")
    leave_room(room=data['store'], sid=_users[data['username']])
    print(f"{data['username']} has been removed as subscriber of store {data['storename']}")


# def unsbscribe(username, storename):
#     leave_room(room=storename, sid=_users[username])
#     # print(f"{username} has been removed as subscriber of store {storename}")


def notify_all(store_name, msg, event):
    # socket.send(msgs, json=True, room=storename)
    store = get_store(store_name)
    store.add_msg(msg, event)
    print (store)
    print(f"room = {store_name}, msg = {msg}")
    socket.emit(event, msg, room=store_name)  # event = str like 'purchase', 'remove_owner', 'new_owner'
    # socket.send({
    #         'messages': [msg]
    #     }, room=store_name)


def handle_purchase_msg(store_name):
    msg = f"A purchase has been made at store {store_name}"
    print(f"send msg: {msg}")
    notify_all(store_name, {'messages': msg, 'store': store_name}, 'message')
    # notify_all(store_name, jsonify(messages=msg, store=store_name))


# FOR ANNA
def handle_agreement_msg(appointe_name, store_name):
    msg = f"Would you like to appoint {appointe_name} as owner in store {store_name}?"
    print(f"send msg: {msg}")
    notify_all(store_name, {'messages': msg, 'store': store_name, 'appointee_nickname': appointe_name}, "agreement")
    # notify_all(store_name, jsonify(messages=msg, store=store_name))


def handle_remove_owner_msg(user_name, store_name):
    if not remove_subscriber_from_store(store_name, user_name):
        print ("error in store publisher- remove owner")
    sid = _users[user_name]
    if sid:
        leave_room(room=store_name, sid=user_name)
        if not TradeControlService.get_user_type() == 'OWNER' and user_name in _users_with_their_own_rooms:
            leave_room(room=user_name, sid=sid)
            _users_with_their_own_rooms.remove(user_name)
    msg = f"{user_name} was removed as owner from store {store_name}"
    print(f"send msg: {msg}")
    notify_all(store_name, {'username':user_name, 'messages':msg, 'store':store_name}, 'message')
    # notify_all(store_name, jsonify(username=user_name, messages=msg, store=store_name))
    # print(f"send msg: {msg}")

@socket.on('login')
def handle_login(data):
    username = data['username']
    user_sid = request.sid
    _users[username] = user_sid
    print(_users)
    # user_sid = _users(username)
    if (TradeControlService.get_user_type() == 'OWNER'):
        join_room(username, user_sid)
        _users_with_their_own_rooms.append(username)
        print (f"insert {username} to it's room. sid = {user_sid}")
        for store in _stores:
            if store.is_subscribed_to_store(username):
                store_name = store.store_name()
                print(f"search for msgs to {username} at store {store_name}")
                join_room(room=store_name, sid=user_sid)
                msgs = store.retrieveMsgs(username)
                print (msgs)
                for msg, event in msgs:
                    print (f"send msg '{msg}' only to {username}. event type is {event}")
                    socket.emit(event, msg, room=username)
                appointee_msgs = store.get_personal_msgs(username)
                for msg in appointee_msgs:
                    print (f"send msg '{msg}' only to {username}")
                    socket.emit('message', msg, room=username)

def get_store(store_name) -> StorePublisher:
    for store in _stores:
        if store.store_name() == store_name:
            # print(f"in get store, correct for {store} with {store.store_name()}")
            return store
    return None


def add_subscriber_to_store(store_name, owner_nickname, is_logged_in):
    store = get_store(store_name)
    if store is None:
        # print(f"store {store_name} is none, owner is {owner_nickname}")
        return False
    if store.is_subscribed_to_store(owner_nickname):
        return False
    store.subscribe_owner(owner_nickname, is_logged_in)
    return True


def remove_subscriber_from_store(store_name, owner_nickname):
    store = get_store(store_name)
    if store is None:
        return -2
    return store.unsubscribe_owner(owner_nickname)


def is_subscribed_to_store(store_name, nickname):
    store = get_store(store_name)
    if store is not None:
        return store.is_subscribed_to_store(nickname)
    # print(f"store {store_name} is none. nickname is {nickname}")
    return False

@socket.on('logout')
def logout_from_stores(data):
    if (data):
        username = data['username']
        print(f"logout username= {username}")
        sid = request.sid
        for store in _stores:
            if store.is_subscribed_to_store(username):
                store.logout_subscriber(username)
                if sid:
                    print (f"leave room: store name = {store.store_name()} , sid = {sid}")
                if sid:
                    storename=store.store_name()
                    leave_room(room=storename, sid= sid)
        if username in _users_with_their_own_rooms:
            leave_room(room=username, sid= sid)
            _users_with_their_own_rooms.remove(username)
        del _users[username]
    else:
        print(f"error with logout message at websocket. recieved: {data}")
#
#
# def delete_user(username):
#     sid = _users[username]
#     if sid:
#         del _users[username]


def websocket_logout(username):
    if username != '':
        logout_from_stores(username)
        sid = _users[username]
        if sid:
            del _users[username]
        print (f"user list after logout of {username} = {_users}")
        # for user in _users:
        #     (user_name, sid) = user
        #     if username == user_name:
        #         del _users[user_name]
        #         print (f"user list = {_users}")

# TODO - add call
def send_daily_cut_update(statistics_update):
    for sys_man in _system_managers:
        (nickname, sid, is_in_daily_cuts_window) = sys_man
        if is_in_daily_cuts_window and sid is not None:
            if not nickname in _users_with_their_own_rooms:
                _users_with_their_own_rooms.append(nickname)
                join_room(nickname, _users[nickname])
            socket.emit('daily_cut', statistics_update, room=nickname)

    pass