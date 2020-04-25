from src.main.DomainLayer.ManagerPermission import ManagerPermission
from src.main.DomainLayer.User import User
from src.main.DomainLayer.TradeControl import TradeControl
from src.main.DomainLayer.Security import Security


class StoreOwnerRole:

    def __init__(self, subscriber):
        self.__store_owner = subscriber

    # use case 4.1.1
    def add_products(self, user_nickname, store_name, products_details) -> bool:
        """
        :param user_nickname: owner's nickname
        :param store_name: store's name
        :param products_details: list of tuples (product_name, product_price, product_amounts, product_category)
        :return: empty list if ALL products were added successfully, else list of products who weren't added
        """
        subscriber = self.get_subscriber(user_nickname)
        store = self.get_store(store_name)
        if store is not None and subscriber is not None and store.is_owner(user_nickname) and \
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
        subscriber = self.get_subscriber(user_nickname)
        store = self.get_store(store_name)
        if store is None and \
                subscriber is not None and\
                store.is_owner(user_nickname) and \
                subscriber.is_registered() and \
                subscriber.is_logged_in():
            store.remove_products(products_names)
            return True
        return False

    # use 4.1.3
    def edit_product(self, nickname, store_name, product_name, op, new_value) -> bool:
        subscriber = self.get_subscriber(nickname)
        store = self.get_store(store_name)
        if store is not None and \
                subscriber is not None and \
                store.is_owner(nickname) and \
                subscriber.is_registered() and \
                subscriber.is_logged_in():
            if op == "name":
                store.change_name(product_name, new_value)
            elif op == "price":
                store.change_price(product_name, new_value)
            elif op == "amount":
                store.change_amount(product_name, new_value)
            else:
                return False
            return True
        return False

    # TODO: use case 4.2 - edit purchase and discount policies
    def edit_purchase_and_discount_policies(self):
        pass

    # use case 4.3
    def appoint_additional_owner(self, nickname, store_name):
        """
        :param nickname: nickname of the new owner of the store
        :param store_name: the store to add owner to
        :return: True on success, else False
        """
        subscriber = self.get_subscriber(nickname)
        store = self.get_store(store_name)
        if subscriber is not None and \
                store is not None and \
                self.__store_owner.is_registered() \
                and store.is_owner(self.__store_owner.get_nickname()):
            return store.add_owner(subscriber)
        return None

    # use case 4.5
    def appoint_store_manager(self, manager_nickname, store_name, permissions):
        """
        :param manager_nickname: new manager's nickname
        :param store_name: store's name
        :param permissions: ManagerPermission[] ->list of permissions (list of Enum)
        :return: 
        """
        subscriber = self.get_subscriber(manager_nickname)
        store = self.get_store(store_name)
        if subscriber is not None and \
                store is not None and \
                self.__store_owner.is_registered() and \
                store.is_owner(self.__store_owner.get_nickname()) and \
                not store.is_owner(manager_nickname) and \
                not store.is_manager(manager_nickname):
            return store.add_manager(subscriber, permissions, self.__store_owner)
        return False

    # use case 4.6
    def edit_manager_permissions(self, store_name, manager_nickname, permissions):
        manager = self.get_subscriber(manager_nickname)
        store = self.get_store(store_name)
        if manager is not None and \
                store is not None and \
                self.__store_owner.is_registered() and \
                self.__store_owner.is_logged_in() and \
                store.is_owner(self.__store_owner.get_nickname()) and \
                store.is_manager(manager_nickname):
            return store.edit_manager_permissions(manager, permissions, self.__store_owner)
        return False

    # use case 4.7
    def remove_manager(self, store_name, manager_nickname, permissions):
        manager = self.get_subscriber(manager_nickname)
        store = self.get_store(store_name)
        if manager is not None and \
                store is not None and \
                self.__store_owner.is_registered() and \
                self.__store_owner.is_logged_in() and \
                store.is_owner(self.__store_owner.get_nickname()) and \
                store.is_manager(manager_nickname):
            return store.remove_manager(manager, permissions, self.__store_owner)
        return False

    # use case 4.10 - View store’s purchase history
    def display_store_purchases(self, nickname, store_name):
        """
        :param self:
        :param nickname: of the store owner
        :param store_name: name of the store - (string)
        :return: purchases list
        """
        subscriber = self.get_subscriber(nickname)
        store = self.get_store(store_name)
        # checking preconditions
        if subscriber is not None and \
                store is not None and \
                subscriber.is_registered() and \
                subscriber.is_logged_in() and \
                store.is_owner(nickname):
            return store.get_purchases()
        return []

    def get_store(self, store_name):
        return TradeControl.get_instance().get_store(store_name)

    def get_subscriber(self, nickname):
        return TradeControl.get_instance().get_subscriber(nickname)

    # def check_if_owns_the_store(self, user_name, store_name) -> bool:
    #     user = TradeControl.get_instance().getUser(user_name)
    #     if user is None or not user.is_loggedIn():
    #         return False
    #     store = self.get_store(store_name)
    #     if user in store.get_owners():
    #         return True

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
