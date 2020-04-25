from src.main.DomainLayer.User import User
from src.main.DomainLayer.TradeControl import TradeControl
from src.main.DomainLayer.Security import Security


class StoreOwnerRole:

    def __init__(self, subscriber):
        self.__store_owner = subscriber

    # def open_store_func(self, user_name, store_name) -> bool:
    #     user = self.find_user_by_name(user_name)
    #     if user is None or not user.is_loggedIn():
    #         return False
    #     self.validate_store_name(store_name)
    #     new_store = TradeControl.getInstance().open_store(self, store_name)
    #     if new_store is None:
    #         return False
    #     else:
    #         return new_store.add_owner(user) and appointment.appoint_owner(None, self, new_store)

    # def check_if_owns_the_store(self, user_name, store_name) -> bool:
    #     user = TradeControl.get_instance().getUser(user_name)
    #     if user is None or not user.is_loggedIn():
    #         return False
    #     store = self.get_store(store_name)
    #     if user in store.get_owners():
    #         return True

    # use case 4.1.1
    def add_products(self, user_nickname, store_name, products_details) -> bool:
        """
        :param user_nickname: owner's nickname
        :param store_name: store's name
        :param products_details: list of tuples (product_name, product_price, product_amounts, product_category)
        :return: empty list if ALL products were added successfully, else list of products who weren't added
        """
        store = TradeControl.get_instance().get_store(store_name)
        subscriber = TradeControl.get_instance().get_subscriber(user_nickname)
        if store is None and subscriber is not None and store.is_owner(user_nickname) and \
                subscriber.is_registered() and subscriber.is_logged_in():
            store.add_products(products_details)
            return True
        return False

    # use 4.1.2
    def remove_products(self, user_nickname, store_name, products_names) -> bool:
        """
        :param user_name: owner's name
        :param store_name: store's name
        :param products_names: list of products name to remove
        :return: True if all products were removed, else return False
        """
        store = TradeControl.get_instance().get_store(store_name)
        subscriber = TradeControl.get_instance().get_subscriber(user_nickname)
        if store is None and subscriber is not None and store.is_owner(user_nickname) and \
                subscriber.is_registered() and subscriber.is_logged_in():
            store.remove_products(products_names)
            return True
        return False

    # use 4.1.3
    def edit_product(self, nickcname, store_name, product_name, op, new_value) -> bool:
        store = TradeControl.get_instance().get_store(store_name)
        subscriber = TradeControl.get_instance().get_subscriber(nickcname)
        if store is None and subscriber is not None and store.is_owner(nickcname) and \
                subscriber.is_registered() and subscriber.is_logged_in():
            if op is "name":
                store.change_name(product_name, new_value)
            elif op is "price":
                store.change_price(product_name, new_value)
            elif op is "amount":
                store.change_amount(product_name, new_value)
            else:
                return False
            return True
        return False

    # use case 4.10 - View store’s purchase history
    @staticmethod
    def display_store_purchases(self, nickname, store_name):
        """
        :param self:
        :param nickname: of the store owner
        :param store_name: name of the store - (string)
        :return: purchases list
        """
        subscriber = TradeControl.get_instance().get_subscriber(nickname)
        store = TradeControl.get_instance().get_store(store_name)
        # checking preconditions
        if subscriber is not None and store is not None and \
                subscriber.is_registered() and subscriber.is_logged_in() and store.is_owner(nickname):
            return store.get_purchases()
        return []

    # @staticmethod
    # def get_store(self, store_name):
    #     return TradeControl.getInstance().get_store(store_name)

    # @staticmethod
    # def validate_store_name(self, store_name):
    #     TradeControl.getInstance().validate_store_name(store_name)

    # @staticmethod
    # def display_purchase_info(self, purchase, store):
    #     """
    #     :param self:
    #     :param purchase:
    #     :param store: name of the store - (string?)
    #     :return: returns a Purchase object
    #     """
    #     store = TradeControl.get_instance().get_store(store)
    #     store.get_purchase_info(purchase)
