from datetime import datetime
import hashlib, binascii, os

from src.Logger import secureLogger, logger
from src.main.DomainLayer.StoreComponent.Product import Product
from src.main.DomainLayer.StoreComponent.Purchase import Purchase
from src.main.DomainLayer.UserComponent.Login import Login
from src.main.DomainLayer.UserComponent.Registration import Registration
from src.main.DomainLayer.UserComponent.ShoppingCart import ShoppingCart, DiscountType, PurchaseType


# from Backend.src.main.DomainLayer.StoreComponent.Purchase import Purchase
# from src.test.WhiteBoxTests.UnitTests.Stubs.StubUser import StubUser


class User:
    def __init__(self):
        self.guest_id = id
        self.__registrationState = Registration()
        self.__loginState = Login()
        # self.__appointment = StoreManagerAppointment()
        self.__shoppingCart = ShoppingCart()
        self.__purchase_history = []

    @secureLogger
    def register(self, username: str, password: str) -> dict:
        # if self.__registrationState.get_nickname() is not None:
        #     return False
        if self.is_registered():
            return {'response': False, 'msg': "Guest " + username + " is already registered"}
        if username.strip() == "":
            return {'response': False,
                    'msg': "Invalid nickname, has to include at least one character and can't include spaces alone"}
        if password.strip() == "":
            return {'response': False, 'msg': "Invalid nickname or password"}
        self.__registrationState.register(username, password)
        return {'response': True, 'msg': "Guest registered successfully"}

    @logger
    def unregistered(self):
        self.__registrationState.unregistered()

    @secureLogger
    def login(self, nickname: str, password: str):
        if not self.check_password(password):
            return {'response': False, 'msg': "Incorrect password"}
        if self.is_logged_in():
            return {'response': False, 'msg': "Subscriber " + nickname + " is already logged in"}
        if self.check_nickname(nickname):
            self.__loginState.login()
            if self.__registrationState.get_nickname() == "TradeManager":
                return {'response': True, 'msg': "SYS_MANAGER"}
            return {'response': True, 'msg': "Subscriber logged in successfully"}
        return {'response': False, 'msg': "Incorrect nickname"}

    @logger
    def logout(self):
        if not self.is_logged_in():
            return False

        # Else
        self.__loginState.logout()
        return True

    # @secureLogger
    # def check_password(self, password):
    #     return self.__registrationState.get_password() == password

    @secureLogger
    def check_password(self, provided_password):
        saved_password = self.__registrationState.get_password()
        salt = saved_password[:64]
        saved_password = saved_password[64:]
        pass_hash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
        pass_hash = binascii.hexlify(pass_hash).decode('ascii')
        return pass_hash == saved_password

    @logger
    def check_nickname(self, nickname):
        return self.__registrationState.get_nickname() == nickname

    @logger
    def is_logged_in(self):
        return self.__loginState.is_logged_in()

    @logger
    def is_logged_out(self):
        return not self.__loginState.is_logged_in()

    @logger
    def is_registered(self):
        return self.__registrationState.is_registered()

    @logger
    def save_products_to_basket(self, products_stores_quantity_ls: [{"store_name": str,
                                                                     "product": Product,
                                                                     "amount": int}]):
        return self.__shoppingCart.add_products(products_stores_quantity_ls)

    @logger
    def view_shopping_cart(self) -> {'response': list, 'msg': str}:
        """
        :return: dict: {'response': [{"store_name": str,
                                     "basket": [{"product_name": str
                                                 "amount": int}, ...]
                                    }, ...],
                        'msg': str}
        """
        return self.__shoppingCart.view_shopping_cart()

    @logger
    def remove_from_shopping_cart(self, products_details: [{"product_name": str, "store_name": str}]) -> {
        'response': bool, 'msg': str}:
        """
        :param products_details: [{"product_name": str,
                                       "store_name": str}, ...]
        :return: dict = {'response': bool, 'msg': str}
                 True on success, False when one of the products doesn't exist in the shopping cart
        """
        return self.__shoppingCart.remove_products(products_details)

    @logger
    def update_quantity_in_shopping_cart(self, products_details: [
        {"product_name": str, "store_name": str, "amount": int}]) -> {'response': bool, 'msg': str}:
        """
        :param flag: action option - "remove"/"update"
        :param products_details: [{"product_name": str,
                                       "store_name": str,
                                       "amount": int}, ...]
        :return: dict = {'response': bool, 'msg': str}
                 True on success, False when one of the products doesn't exist in the shopping cart
        """
        return self.__shoppingCart.update_quantity(products_details)

    @logger
    def complete_purchase(self, purchase: Purchase):
        # add purchase to purchase history
        self.__purchase_history.append(purchase)
        # delete purchase from shopping cart
        self.__shoppingCart.get_store_basket(purchase.get_store_name()).complete_purchase(purchase.get_products())
        return True

    @logger
    def remove_purchase(self, store_name: str, date: datetime):
        for p in self.__purchase_history:
            if p.get_store_name() == store_name and p.get_date() == date:
                self.__purchase_history.remove(p)
        return True

    # --------------------------------------GETTERS & SETTERS--------------------------------------------------------

    @logger
    def get_nickname(self):
        return self.__registrationState.get_nickname()

    @logger
    def get_login(self) -> Login:
        return self.__loginState

    @logger
    def get_purchase_history(self):
        return self.__purchase_history

    @logger
    def set_registration_state(self, registration):
        self.__registrationState = registration
        return True

    @logger
    def set_login_state(self, login):
        self.__loginState = login
        return True

    @logger
    def set_shopping_cart(self, shopping_cart):
        self.__shoppingCart = shopping_cart

    @logger
    def set_purchase_history(self, purchase_hist):
        self.__purchase_history = purchase_hist

    @logger
    def get_password(self):
        return self.__registrationState.get_password()

    @logger
    def get_shopping_cart(self) -> ShoppingCart:
        return self.__shoppingCart

    @logger
    def register_from_db(self, username, password):
        self.__registrationState.register_from_db(username, password)

    def __repr__(self):
        # if self.is_registered:
        #     return repr(self.get_nickname)
        return repr("User")
        # return repr("User")

    def __eq__(self, other):
        try:
            # from src.test.WhiteBoxTests.UnitTests.Stubs.StubUser import StubUser
            if other == 'StoreOwnerOrManager':
                return False
            #     return self.get_nickname() == other.get_nickname()
            # elif type(other) is type (StubUser()):
            # print(f"self = {self}, other = {other}")
            return other.get_nickname() == self.get_nickname()
            # else:s

                # print (f"expected User. recieved {type(other)}")
                # return False
        except Exception:
            return False
