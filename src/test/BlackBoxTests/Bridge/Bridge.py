"""
    abstract class representing the:
                                    - implementor in the Bridge pattern
                                    - target in the adapter pattern
                                    - subject in the proxy pattern  
"""
# from __future__ import annotations
from abc import ABC, abstractmethod

from src.Logger import logger


class Bridge(ABC):

    def __init__(self):
        super().__init__()

    # Register tests bridged functions
    @abstractmethod
    def register_user(self, username, password) -> bool:
        pass

    # Payment System tests bridged functions
    @abstractmethod
    def connect_payment_sys(self):
        pass

    @abstractmethod
    def commit_payment(self, username, amount, credit, date) -> bool:
        pass

    @abstractmethod
    def disconnect_payment_sys(self):
        pass

    @logger
    def is_delivery_connected(self):
        pass

    # delivery System tests bridged functions
    @abstractmethod
    def connect_delivery_sys(self):
        pass

    @abstractmethod
    def deliver(self, username, address) -> bool:
        pass

    @abstractmethod
    def disconnect_delivery_sys(self):
        pass

    @logger
    def is_payment_connected(self):
        pass

    @logger
    # init system functions
    def init_sys(self):
        pass

    @logger
    def remove_user(self, username):
        pass

    @logger
    # login functions
    def login(self, username, password):
        pass

    @logger
    # logout functions
    def logout(self):
        pass

    @logger
    # search products functions
    def search_product(self, option, string):
        pass

    @logger
    def filter_products(self, filter_details, products):
        pass

    @logger
    # view stores' products functions
    def view_stores(self):
        pass

    @logger
    # save products functions
    def add_products_to_cart(self, nickname, products_stores_quantity_ls):
        pass

    @logger
    # view personal history functions
    def view_personal_history(self):
        pass

    @logger
    # open store functions
    def open_store(self, name):
        pass

    @logger
    def delete_store(self, store):
        pass

    @logger
    # manage stock functions
    def add_products_to_store(self, user_nickname, store_name, products_details):
        pass

    @logger
    def edit_products_in_store(self, nickname, store_name, product_name, op, new_value):
        pass

    @logger
    def remove_products_from_store(self, user_nickname, store_name, products_names):
        pass

    @logger
    # add store owner functions
    def appoint_additional_owner(self, nickname, store_name):
        pass

    @logger
    # add store manager functions
    def appoint_additional_manager(self, nickname, store_name, permissions):
        pass

    @logger
    # remove manager functions
    def remove_manager(self, store_name, manager_nickname, permissions):
        pass

    def __repr__(self):
        return repr("Bridge")