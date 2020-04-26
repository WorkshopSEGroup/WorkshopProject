from functools import reduce

from src.Logger import logger, loggerStaticMethod
from src.main.DomainLayer.FacadePayment import FacadePayment, date_time
from src.main.DomainLayer.Store import Store
from src.main.DomainLayer.User import User


class TradeControl:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        loggerStaticMethod("TradeControl.get_instance",[])
        if TradeControl.__instance is None:
            TradeControl()
        return TradeControl.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if TradeControl.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.__managers = []
            self.__stores = []
            self.__subscribers = []
            self.__next_purchase_id = 0
            TradeControl.__instance = self

    @logger
    def add_sys_manager(self, subscriber: User):
        for s in self.__managers:
            if s.get_nickname() == subscriber.get_nickname():
                return False
        self.__managers.append(subscriber)
        return True

    @logger
    def subscribe(self, user: User):
        for s in self.__subscribers:
            if s.get_nickname() == user.get_nickname():
                return False
        self.__subscribers.append(user)
        return True

    @logger
    def unsubscribe(self, nickname):
        for s in self.__subscribers:
            if s.get_nickname() == nickname:
                self.__subscribers.remove(s)
                return True
        return False

    @logger
    def remove_manager(self, nickname):
        for s in self.__managers:
            if s.get_nickname() == nickname:
                self.__managers.remove(s)
                return True
        return False

    @logger
    def open_store(self, store_name) -> Store:
        for s in self.__stores:
            if s.get_name() == store_name:
                return None
        store = Store(store_name)
        self.__stores.append(store)
        return store

    @logger
    def close_store(self, store_name) -> bool:
        for s in self.__stores:
            if s.get_name() == store_name:
                self.__stores.remove(s)
                return True
        return False

    @logger
    def validate_nickname(self, nickname):
        for u in self.__subscribers:
            if u.get_nickname() == nickname:
                return False
        return True

    @logger
    def get_subscriber(self, nickname):
        for u in self.__subscribers:
            if u.get_nickname() == nickname:
                return u
        return None

    @logger
    def get_products_by(self, search_opt, string):
        list_of_lists = list(map(lambda store: store.get_products_by(search_opt, string), self.__stores))
        list_ = reduce(lambda acc, curr: acc + curr, list_of_lists)
        return list_

    @logger
    def get_store(self, store_name):
        for s in self.__stores:
            if s.get_name() == store_name:
                return s
        return None

    @logger
    def get_subscribers(self):
        return self.__subscribers

    @logger
    def get_stores(self):
        return self.__stores

    @logger
    def get_managers(self):
        return self.__managers

    @logger
    def is_manager(self, username: str):
        for manager in self.__managers:
            if manager.get_nickname() == username:
                return True
        return False

    @logger
    def get_manager(self, username: str):
        for manager in self.__managers:
            if manager.get_nickname() == username:
                return manager
        return None

    @logger
    # get a user instance for guest
    def get_guest(self):
        guest = User()
        return guest

    @logger
    def get_next_purchase_id(self):
        output = self.__next_purchase_id
        self.__next_purchase_id = self.__next_purchase_id + 1
        return output

    @logger
    def make_payment(self, username: str, amount: float, credit: str, date: date_time) -> bool:
        """
        Take a payment details + amount and send them to the facade-payment.

        :param username: the user to make the payment.
        :param amount: the price to pay.
        :param credit: credit number.
        :param date: expr date of the credit.
        :return: True if the payment succeed.
                 False else.
        """
        return (FacadePayment.get_instance()).commit_payment(username, amount, credit, date)

    def __repr__(self):
        return repr("TradeControl")