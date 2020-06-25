import peewee
from datetime import datetime
from src.Logger import errorLogger
from src.main.ResponseFormat import ret
from src.main.DataAccessLayer.ConnectionProxy.DbProxy import DbProxy
from src.main.DataAccessLayer.UserDataComponent.UserData import UserData
from src.main.DataAccessLayer.StoreDataComponent.StoreData import StoreData
from src.main.DataAccessLayer.StoreDataComponent.ProductData import ProductData
from src.main.DataAccessLayer.StoreDataComponent.PurchaseData import PurchaseData
from src.main.DataAccessLayer.UserDataComponent.StatisticData import StatisticData
from src.main.DataAccessLayer.UserDataComponent.ProductsInBasket import ProductsInBasketData
from src.main.DataAccessLayer.StoreDataComponent.DiscountPolicyData import DiscountPolicyData
from src.main.DataAccessLayer.StoreDataComponent.ProductsInPurchaseData import ProductsInPurchaseData
from src.main.DataAccessLayer.StoreDataComponent.StoreOwnerAppointmentData import StoreOwnerAppointmentData
from src.main.DataAccessLayer.StoreDataComponent.StoreManagerAppointmentData import StoreManagerAppointmentData
from src.main.DataAccessLayer.StoreDataComponent.CompositeDiscountPolicyData import CompositeDiscountPolicyData
from src.main.DataAccessLayer.StoreDataComponent.ConditionalDiscountPolicyData import ConditionalDiscountPolicyData

"""
This class is the facade class for the DA layer.

It should contain 4 function for each persistent domain object: read, write, update and delete.
read = select query.
write = insert query.
update = update query.
delete = delete query.

Our persistent domain objects:
    store component:
        Purchase policy
        Discount policy
        Product
        Purchase
        Store
        Store inventory
        Store manager appointment
    user component:
        Shopping cart
        Shopping basket
        User(only subscribers).
"""


class DataAccessFacade:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if DataAccessFacade.__instance is None:
            DataAccessFacade()
        return DataAccessFacade.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DataAccessFacade.__instance is not None:
            errorLogger("This class is a singleton!")
            raise Exception("This class is a singleton!")
        else:
            self.__proxy = DbProxy.get_instance()
            self.__proxy.connect()
            self.__execution_failed_error_msg = "We having some tech problems, but we will rise again!"
            DataAccessFacade.__instance = self

    def get_proxy(self):
        return self.__proxy

    def write_user(self, username: str, password: str, is_system_manager: bool = False):
        """
        Write a user to db.

        :param username: pk
        :param password: user password.
        :param is_system_manager:
        :return: size of user tbl after inserting the new one.
        """
        try:
            return self.__proxy.execute([UserData.get_instance().write(username, password, is_system_manager)])
        except Exception:
            return ret(False, self.__execution_failed_error_msg)

    def read_users(self, attributes_to_read=None, username: str = "", password: str = "",
                   is_system_manager: bool = None):
        """
        Read users from db.
        <attribute> will composite a constraint of where to read.
        example(if old_username != ""), it will composite the constraint-
                                               where(user.username == username).

        :param attributes_to_read: the list of attributes that will return from the db.
                                    type: [str]
        :param username: pk
        :param password:
        :param is_system_manager:
        :return: list of dictionaries that contain attributes_to_read fields.
        """
        if attributes_to_read is None:
            attributes_to_read = []
        try:
            return ret(UserData.get_instance().read(attributes_to_read, username, password, is_system_manager),
                       "Successful.")
        except Exception:
            return ret([], self.__execution_failed_error_msg)

    def update_users(self, old_username: str = "", old_password: str = "", old_is_system_manager: bool = None,
                     new_username: str = "", new_password: str = "", new_is_system_manager: bool = None):
        """
        Update users in the db.
        old_<attribute> will composite a constraint of where to update.
        example(if old_username != ""), it will composite the constraint-
                                                where(user.username == old_username).
        new_<attribure> will update the <attribute> to the new value.
        example(if new_username != ""), it will update-
                                                update(user.username = new_username).


        :param old_username: pk. will composite a constraint on the username.
        :param old_password: will composite a constraint on the password.
        :param old_is_system_manager: will composite a constraint on the is_system_manager.
        :param new_username: pk. will update the username to the new value.
        :param new_password: will update the password to the new value.
        :param new_is_system_manager: will update the is_system_manager to the new value.
        :return: the number of updated rows.
        """
        try:
            return self.__proxy.execute([UserData.get_instance().update(old_username,
                                                                        old_password,
                                                                        old_is_system_manager,
                                                                        new_username,
                                                                        new_password,
                                                                        new_is_system_manager)])
        except Exception:
            return ret(False, self.__execution_failed_error_msg)

    def delete_users(self, username: str = "", password: str = "", is_system_manager: bool = None):
        """
        Delete users from the DB.
        <attribute> will composite a constraint of where to delete.
        example(if old_username != ""), it will composite the constraint-
                                                where(user.username == username).

        :param username: pk. will composite a constraint of where to update.
        :param password: will composite a constraint of where to update.
        :param is_system_manager: will composite a constraint of where to update.
        :return: the number of deleted rows.
        """
        try:
            return self.__proxy.execute([UserData.get_instance().delete(username, password, is_system_manager)])
        except Exception:
            return ret(False, self.__execution_failed_error_msg)

    def write_store(self, store_name: str, founder_name: str):
        """
        Write a store to db.

        :param store_name.
        :param founder_name.
        :return:
        """
        try:
            return self.__proxy.execute([StoreData.get_instance().write(store_name, founder_name)])
        except Exception:
            return ret(False, self.__execution_failed_error_msg)

    def read_stores(self, attributes_to_read=None, store_name="", founder_username=""):
        """
        Read users from db.
        <attribute> will composite a constraint of where to read.
        example(if old_username != ""), it will composite the constraint-
                                               where(user.username == username).

        :param store_name:
        :param founder_username:
        :param attributes_to_read: the list of attributes that will return from the db.
                                    type: [str]
        :return: list of dictionaries that contain attributes_to_read fields.
        """
        if attributes_to_read is None:
            attributes_to_read = []
        try:
            return ret(StoreData.get_instance().read(attributes_to_read, store_name, founder_username), "Successful.")
        except Exception:
            return ret([], self.__execution_failed_error_msg)

    def update_stores(self, old_store_name="", old_founder_username="",
                      new_store_name="", new_founder_username=""):
        """
        Update stores in the db.
        old_<attribute> will composite a constraint of where to update.
        example(if old_username != ""), it will composite the constraint-
                                                where(user.username == old_username).
        new_<attribure> will update the <attribute> to the new value.
        example(if new_username != ""), it will update-
                                                update(user.username = new_username).


        :param new_store_name: pk.
        :param new_founder_username.
        :param old_founder_username.
        :param old_store_name: pk.
        :return: the number of updated rows.
        """
        try:
            return self.__proxy.execute(
                [StoreData.get_instance().update(old_store_name, old_founder_username, new_store_name,
                                                 new_founder_username)])
        except Exception:
            return ret(False, self.__execution_failed_error_msg)

    def delete_stores(self, store_name="", founder_username=""):
        """
        Delete stores from the DB.
        <attribute> will composite a constraint of where to delete.
        example(if old_username != ""), it will composite the constraint-
                                                where(user.username == username).

        :param store_name.
        :param founder_username.
        :return: number of deleted rows.
        """
        try:
            return self.__proxy.execute([StoreData.get_instance().delete(store_name, founder_username)])
        except Exception:
            return ret(False, self.__execution_failed_error_msg)

    def write_product(self, product_name: str, store_name: str, price: float, category: str, amount: int,
                      purchase_type: int):
        """
        Write a product to db.

        :param purchase_type:
        :param product_name: pk
        :param store_name: pk
        :param price:
        :param category:
        :param amount:
        :return: size of user tbl after inserting the new one.
        """
        try:
            return self.__proxy.execute([ProductData.get_instance().write(product_name, store_name, price, category,
                                                                          amount, purchase_type)])
        except Exception:
            return ret(False, self.__execution_failed_error_msg)

    def read_products(self, attributes_to_read=None, product_name: str = "", store_name: str = "", price: float = None,
                      category: str = "", amount: int = None, purchase_type: int = None):
        """
        Read products from db.
        <attribute> will composite a constraint of where to read.
        example(if old_username != ""), it will composite the constraint-
                                               where(user.username == username).

        :param product_id:
        :param purchase_type:
        :param product_name: pk
        :param store_name: pk
        :param price:
        :param category:
        :param amount:
        :param attributes_to_read: the list of attributes that will return from the db.
                                    type: [str]
        :return: list of dictionaries that contain attributes_to_read fields.
        """
        if attributes_to_read is None:
            attributes_to_read = []
        try:
            return ret(
                ProductData.get_instance().read(attributes_to_read, None, product_name, store_name, price, category,
                                                amount, purchase_type), "Successful.")
        except Exception:
            return ret([], self.__execution_failed_error_msg)

    def update_products(self, old_product_name: str = "", old_store_name: str = "", old_price: float = None,
                        old_category: str = "", old_amount: int = None, old_purchase_type: int = None,
                        new_product_name: str = "", new_store_name: str = "", new_price: float = None,
                        new_category: str = "", new_amount: int = None, new_purchase_type: int = None):
        """
        Update products in the db.
        old_<attribute> will composite a constraint of where to update.
        example(if old_username != ""), it will composite the constraint-
                                                where(user.username == old_username).
        new_<attribute> will update the <attribute> to the new value.
        example(if new_username != ""), it will update-
                                                update(user.username = new_username).


        :param new_purchase_type:
        :param old_purchase_type:
        :param old_product_name:  pk
        :param old_store_name: pk
        :param old_price:
        :param old_category:
        :param old_amount:
        :param new_product_name: pk
        :param new_store_name: pk
        :param new_price:
        :param new_category:
        :param new_amount:
        :return: the number of updated rows.
        """
        try:
            return self.__proxy.execute(
                [ProductData.get_instance().update(None, old_product_name, old_store_name, old_price, old_category,
                                                   old_amount, old_purchase_type, new_product_name, new_store_name,
                                                   new_price, new_category, new_amount, new_purchase_type)])
        except Exception as e:
            # print(e)
            return ret(False, self.__execution_failed_error_msg)

    def delete_products(self, product_name: str = "", store_name: str = "", price: float = None, category: str = "",
                        amount: int = None, purchase_type: int = None):
        """
        Delete products from the DB.
        <attribute> will composite a constraint of where to delete.
        example(if old_username != ""), it will composite the constraint-
                                                where(user.username == username).

        :param purchase_type:
        :param product_name: pk.
        :param store_name: pk.
        :param price: pk.
        :param category: pk.
        :param amount: pk.
        :return: the number of deleted rows.
        """
        try:
            return self.__proxy.execute(
                [ProductData.get_instance().delete(None, product_name, store_name, price, category, amount,
                                                   purchase_type)])
        except Exception:
            return ret(False, self.__execution_failed_error_msg)

    def __prepare_permission_args(self, lst_permissions: [], attr_to_read=False):
        map_per_name_to_column = [("EDIT_INV", "can_edit_inventory"),
                                  ("EDIT_POLICIES", "can_edit_policies"),
                                  ("APPOINT_OWNER", "can_appoint_owner"),
                                  ("DEL_OWNER", "can_delete_owner"),
                                  ("APPOINT_MANAGER", "can_appoint_manager"),
                                  ("EDIT_MANAGER_PER", "can_edit_manager_permissions"),
                                  ("DEL_MANAGER", "can_delete_manager"),
                                  ("CLOSE_STORE", "can_close_store"),
                                  ("USERS_QUESTIONS", "can_answer_user_questions"),
                                  ("WATCH_PURCHASE_HISTORY", "can_watch_purchase_history")]
        if type(lst_permissions) is tuple:
            return lst_permissions
        output = []
        for i in range(len(map_per_name_to_column)):
            if map_per_name_to_column[i][0] in lst_permissions:
                if attr_to_read:
                    output.insert(len(output), map_per_name_to_column[i][1])
                else:
                    output.insert(len(output), True)
            else:
                if not attr_to_read:
                    output.insert(len(output), None)
        return tuple(output)

    def read_store_manager_appointments(self, attributes_to_read=None,
                                        permissions_to_read=None,
                                        appointee_username: str = "",
                                        store_name: str = "",
                                        appointer_username: str = "",
                                        permissions_lst=None):
        """
        Read store manager appointment from db.
        Raise exception if an attribute in attributes_to_read is illegal.
        <attribute> will composite a constraint of where to read.
        example(if old_username != ""), it will composite the constraint-
                                               where(user.username == username).

        :param permissions_lst: lst of permissions names.
        :param permissions_to_read: lst of permissions names.
        :param attributes_to_read: lst of attributes to read.
        :param appointee_username: pk.
        :param store_name: pk.
        :param appointer_username:
        """
        if permissions_lst is None:
            permissions_lst = []
        if permissions_to_read is None:
            permissions_to_read = []
        if attributes_to_read is None:
            attributes_to_read = []
        attributes_to_read.extend(list(self.__prepare_permission_args(permissions_to_read, True)))
        try:
            return ret((StoreManagerAppointmentData.get_instance()).read(attributes_to_read,
                                                                         appointee_username,
                                                                         store_name,
                                                                         appointer_username,
                                                                         *self.__prepare_permission_args(
                                                                             permissions_lst)),
                       "Successful.")
        except Exception:
            return ret([], self.__execution_failed_error_msg)

    def write_store_manager_appointment(self, appointee_username: str, store_name: str, appointer_username: str,
                                        permissions_lst=None):
        """
        write store manager appointment to db.

        :param permissions_lst:
        :param appointee_username: pk
        :param store_name:pk
        :param appointer_username:
        :return:
        """
        if permissions_lst is None:
            permissions_lst = []
        lst_per_args = list(self.__prepare_permission_args(permissions_lst))
        da_per_lst = []
        for i in range(len(lst_per_args)):
            if lst_per_args[i] is None:
                da_per_lst.insert(len(da_per_lst), False)
            else:
                da_per_lst.insert(len(da_per_lst), True)
        try:
            return self.__proxy.execute(
                [StoreManagerAppointmentData.get_instance().write(appointee_username, store_name, appointer_username,
                                                                  *tuple(da_per_lst))])
        except Exception:
            return ret(False, self.__execution_failed_error_msg)

    def update_store_manager_appointments(self, old_appointee_username: str = "", old_store_name: str = "",
                                          old_appointer_username: str = "",
                                          old_permissions_lst=None,
                                          new_appointee_username: str = "", new_store_name: str = "",
                                          new_appointer_username: str = "",
                                          new_permissions_lst=None
                                          ):
        """
        Update store manager appointment in the db.
        old_<attribute> will composite a constraint of where to update.
        example(if old_username != ""), it will composite the constraint-
                                                where(user.username == old_username).
        new_<attribute> will update the <attribute> to the new value.
        example(if new_username != ""), it will update-
                                                update(user.username = new_username).

        :return: the number of updated rows.
        """
        if old_permissions_lst is None:
            old_permissions_lst = []
        if new_permissions_lst is None:
            new_permissions_lst = []
        elif len(new_permissions_lst) == 0:
            new_permissions_lst = (False, False, False, False, False, False, False, False, False, False)
        try:
            return self.__proxy.execute(
                [StoreManagerAppointmentData.get_instance().update(old_appointee_username, old_store_name,
                                                                   old_appointer_username,
                                                                   *self.__prepare_permission_args(old_permissions_lst),
                                                                   new_appointee_username, new_store_name,
                                                                   new_appointer_username,
                                                                   *self.__prepare_permission_args(
                                                                       new_permissions_lst))])
        except Exception as e:
            print(e)
            return ret(False, self.__execution_failed_error_msg)

    def delete_store_manager_appointments(self, appointee_username: str = "", store_name: str = "",
                                          appointer_username: str = "", permissions_lst=None):
        """
        Delete store manager appointments from the DB.
        <attribute> will composite a constraint of where to delete.
        example(if old_username != ""), it will composite the constraint-
                                               where(user.username == username).

        :return: the number of deleted rows.
        """
        if permissions_lst is None:
            permissions_lst = []
        try:
            return self.__proxy.execute(
                [StoreManagerAppointmentData.get_instance().delete(appointee_username, store_name,
                                                                   appointer_username,
                                                                   *self.__prepare_permission_args(
                                                                       permissions_lst))])
        except Exception:
            return ret(False, self.__execution_failed_error_msg)

    def read_products_in_baskets(self, attributes_to_read=None, username: str = "", store_name: str = "",
                                 product_name: str = "", amount: int = None):
        """
        Read products in basket from db.
        Raise exception if an attribute in attributes_to_read is illegal.
        <attribute> will composite a constraint of where to read.
        example(if old_username != ""), it will composite the constraint-
                                               where(user.username == username).

        :param store_name: pk
        :param product_name: pk
        :param username: pk.
        :param amount:
        :param attributes_to_read: the list of attributes that will return from the db.
                                    type: [str]

        :return: list of dictionaries that contain attributes_to_read fields.
        """
        if attributes_to_read is None:
            attributes_to_read = []
        product_as_lst = self.read_products(["product_id"], store_name=store_name, product_name=product_name)[
            'response']
        product_ref = None
        if len(product_as_lst) > 0:
            if product_name != "" and store_name != "":
                product_ref = product_as_lst[0]['product_id']
        else:
            if product_name != "" or store_name != "":
                return ret([], self.__execution_failed_error_msg)

        try:
            return ret((ProductsInBasketData.get_instance()).read(attributes_to_read, username, product_ref, amount),
                       "Successful.")
        except Exception as e:
            # print(e)
            return ret([], self.__execution_failed_error_msg)

    def write_products_in_basket(self, username: str, store_name: str, product_name: str, amount: int):
        """
        Write product in basket to db.

        :param product_name: pk.
        :param store_name: pk.
        :param username:
        :param amount:
        :return: size of user tbl after inserting the new one.
        """
        product_as_lst = self.read_products(["product_id"], store_name=store_name, product_name=product_name)[
            'response']
        product_ref = None
        if len(product_as_lst) > 0:
            product_ref = product_as_lst[0]['product_id']
        else:
            return ret(False, "Product " + product_name + "  doesn't exist in store " + store_name + ".")

        try:
            return self.__proxy.execute([ProductsInBasketData.get_instance().write(username, product_ref, amount)])
        except Exception as e:
            # print(e)
            return ret(False, self.__execution_failed_error_msg)

    def update_products_in_baskets(self, old_username: str = "", old_store_name: str = "", old_product_name: str = "",
                                   old_amount: int = None,
                                   new_username: str = "", new_store_name: str = "", new_product_name: str = "",
                                   new_amount: int = None):
        """
        Update products in basket in the db.
        old_<attribute> will composite a constraint of where to update.
        example(if old_username != ""), it will composite the constraint-
                                                where(user.username == old_username).
        new_<attribute> will update the <attribute> to the new value.
        example(if new_username != ""), it will update-
                                                update(user.username = new_username).

        :return: the number of updated rows.
        """
        product_as_lst = self.read_products(["product_id"], store_name=old_store_name, product_name=old_product_name)[
            'response']
        old_product_ref = None
        if len(product_as_lst) > 0:
            if old_product_name != "" and old_store_name != "":
                old_product_ref = product_as_lst[0]['product_id']

        product_as_lst = self.read_products(["product_id"], store_name=new_store_name, product_name=new_product_name)[
            'response']
        new_product_ref = None
        if len(product_as_lst) > 0:
            if new_product_name != "" and new_store_name != "":
                new_product_ref = product_as_lst[0]['product_id']

        try:
            return self.__proxy.execute([(ProductsInBasketData.get_instance()).update(old_username, old_product_ref,
                                                                                      old_amount, new_username,
                                                                                      new_product_ref, new_amount)])
        except Exception as e:
            # print(e)
            return ret(False, self.__execution_failed_error_msg)

    def delete_products_in_baskets(self, username: str = "", store_name: str = "", product_name: str = "",
                                   amount: int = None):
        """
        Delete product in basket from the DB.
        <attribute> will composite a constraint of where to delete.
        example(if old_username != ""), it will composite the constraint-
                                               where(user.username == username).

        :return: the number of deleted rows.
        """

        product_as_lst = self.read_products(["product_id"], store_name=store_name, product_name=product_name)[
            'response']
        product_ref = None
        if len(product_as_lst) > 0:
            if product_name != "" or store_name != "":
                product_ref = product_as_lst[0]['product_id']

        try:
            return self.__proxy.execute([(ProductsInBasketData.get_instance()).delete(username, product_ref, amount)])
        except Exception as e:
            # print(e)
            return ret(False, self.__execution_failed_error_msg)

    def read_store_owner_appointments(self, attributes_to_read=None,
                                      appointee_username: str = "",
                                      store_name: str = "",
                                      appointer_username: str = ""):
        """
        Read store manager appointment from db.
        Raise exception if an attribute in attributes_to_read is illegal.
        <attribute> will composite a constraint of where to read.
        example(if old_username != ""), it will composite the constraint-
                                               where(user.username == username).

        :param attributes_to_read: lst of attributes to read.
        :param appointee_username: pk.
        :param store_name: pk.
        :param appointer_username:
        """
        if attributes_to_read is None:
            attributes_to_read = []
        try:
            return ret((StoreOwnerAppointmentData.get_instance()).read(attributes_to_read,
                                                                       appointee_username,
                                                                       store_name,
                                                                       appointer_username),
                       "Successful.")
        except Exception:
            return ret([], self.__execution_failed_error_msg)

    def write_store_owner_appointment(self, appointee_username: str, store_name: str, appointer_username: str):
        """
        write store manager appointment to db.

        :param appointee_username: pk
        :param store_name:pk
        :param appointer_username:
        :return:
        """
        try:
            return self.__proxy.execute(
                [StoreOwnerAppointmentData.get_instance().write(appointee_username, store_name, appointer_username)])
        except Exception:
            return ret(False, self.__execution_failed_error_msg)

    def update_store_owner_appointments(self, old_appointee_username: str = "", old_store_name: str = "",
                                        old_appointer_username: str = "",
                                        new_appointee_username: str = "", new_store_name: str = "",
                                        new_appointer_username: str = ""):
        """
        Update store manager appointment in the db.
        old_<attribute> will composite a constraint of where to update.
        example(if old_username != ""), it will composite the constraint-
                                                where(user.username == old_username).
        new_<attribute> will update the <attribute> to the new value.
        example(if new_username != ""), it will update-
                                                update(user.username = new_username).

        :return: the number of updated rows.
        """
        try:
            return self.__proxy.execute(
                [StoreOwnerAppointmentData.get_instance().update(old_appointee_username, old_store_name,
                                                                 old_appointer_username,
                                                                 new_appointee_username, new_store_name,
                                                                 new_appointer_username)])
        except Exception:
            return ret(False, self.__execution_failed_error_msg)

    def delete_store_owner_appointments(self, appointee_username: str = "", store_name: str = "",
                                        appointer_username: str = ""):
        """
        Delete store manager appointments from the DB.
        <attribute> will composite a constraint of where to delete.
        example(if old_username != ""), it will composite the constraint-
                                               where(user.username == username).

        :return: the number of deleted rows.
        """
        try:
            return self.__proxy.execute(
                [StoreOwnerAppointmentData.get_instance().delete(appointee_username, store_name,
                                                                 appointer_username)])
        except Exception:
            return ret(False, self.__execution_failed_error_msg)

    def read_statistics(self, attributes_to_read=None, date: datetime = None, guests: int = None,
                        subscribers: int = None, store_managers: int = None, store_owners: int = None,
                        system_managers: int = None):
        """
        Read statistics from db.
        Raise exception if an attribute in attributes_to_read is illegal.
        <attribute> will composite a constraint of where to read.
        example(if old_username != ""), it will composite the constraint-
                                               where(user.username == username).

        :param date:
        :param guests:
        :param subscribers:
        :param store_managers:
        :param store_owners:
        :param system_managers:
        :param attributes_to_read: the list of attributes that will return from the db.
                                    type: [str]

        :return: list of dictionaries that contain attributes_to_read fields.
        """
        if attributes_to_read is None:
            attributes_to_read = []
        try:
            return ret(
                (StatisticData.get_instance()).read(attributes_to_read, date, guests, subscribers, store_managers,
                                                    store_owners, system_managers), "Successful.")
        except Exception as e:
            # print(e)
            return ret([], self.__execution_failed_error_msg)

    def write_statistic(self, date: datetime = datetime(datetime.now().year, datetime.now().month, datetime.now().day),
                        guests: int = 0, subscribers: int = 0, store_managers: int = 0, store_owners: int = 0,
                        system_managers: int = 0):
        """
        Write a statistics to db.
        :return: size of user tbl after inserting the new one.
        """
        try:
            return self.__proxy.execute([(StatisticData.get_instance()).write(date, guests, subscribers, store_managers,
                                                                              store_owners, system_managers)])
        except Exception as e:
            # print(e)
            return ret([], self.__execution_failed_error_msg)

    def update_statistics(self, old_date: datetime = None, old_guests: int = None, old_subscribers: int = None,
                          old_store_managers: int = None, old_store_owners: int = None, old_system_managers: int = None,
                          new_date: datetime = None, new_guests: int = None, new_subscribers: int = None,
                          new_store_managers: int = None, new_store_owners: int = None,
                          new_system_managers: int = None):
        """
        Update statistics in the db.
        old_<attribute> will composite a constraint of where to update.
        example(if old_username != ""), it will composite the constraint-
                                                where(user.username == old_username).
        new_<attribure> will update the <attribute> to the new value.
        example(if new_username != ""), it will update-
                                                update(user.username = new_username).
        :return: the number of updated rows.
        """
        try:
            return self.__proxy.execute([(StatisticData.get_instance()).update(old_date, old_guests, old_subscribers,
                                                                               old_store_managers,
                                                                               old_store_owners, old_system_managers,
                                                                               new_date, new_guests, new_subscribers,
                                                                               new_store_managers,
                                                                               new_store_owners, new_system_managers
                                                                               )
                                         ])
        except Exception as e:
            # print(e)
            return ret([], self.__execution_failed_error_msg)

    def delete_statistics(self, date: datetime = None, guests: int = None, subscribers: int = None,
                          store_managers: int = None, store_owners: int = None, system_managers: int = None):
        """
        Delete statistics from the DB.
        <attribute> will composite a constraint of where to delete.
        example(if old_username != ""), it will composite the constraint-
                                               where(user.username == username).

        :return: the number of deleted rows.
        """
        try:
            return self.__proxy.execute(
                [(StatisticData.get_instance()).delete(date, guests, subscribers, store_managers,
                                                       store_owners, system_managers)
                 ])
        except Exception as e:
            # print(e)
            return ret([], self.__execution_failed_error_msg)

    # def read_discount_policies(self, attributes_to_read=None, discount_policy_id: int = None, policy_name: str = "",
    #                            store_name="", product_name: str = "", percentage: float = None,
    #                            valid_until: datetime = None, is_active: bool = None,
    #                            precondition_product: str = "", precondition_min_amount: int = None,
    #                            precondition_min_basket_price: int = None,
    #                            policy1_name: str = "", policy2_name: str = "", flag: int = None):
    #     """
    #     Read discount policy from db.
    #     Raise exception if an attribute in attributes_to_read is illegal.
    #     <attribute> will composite a constraint of where to read.
    #     example(if old_username != ""), it will composite the constraint-
    #                                            where(user.username == username).
    #
    #     :param founder_username:
    #     :param store_name:
    #     :param attributes_to_read: the list of attributes that will return from the db.
    #                                 type: [str]
    #
    #     :return: list of dictionaries that contain attributes_to_read fields.
    #     """
    #     if attributes_to_read is None:
    #         attributes_to_read = []
    #     try:
    #         # mother_discount = (DiscountPolicyData.get_instance()).read(attributes_to_read, discount_policy_id,
    #         #                                                            policy_name, store_name, product_name,
    #         #                                                            percentage, valid_until, is_active)
    #         # output_lst = []
    #         # for policy in mother_discount:
    #         #     policy_as_lst = (ConditionalDiscountPolicyData.get_instance()).read([],
    #         #                                                                         policy_ref=policy[
    #         #                                                                             'discount_policy_id'])[
    #         #         'response']
    #         #     if len(policy_as_lst) > 0:
    #         #         daughter_policy = policy_as_lst[0]
    #         #         policy['precondition_product'] = daughter_policy['precondition_product']
    #         #         policy['precondition_min_amount'] = daughter_policy['precondition_min_amount']
    #         #         policy['precondition_min_basket_price'] = daughter_policy['precondition_min_basket_price']
    #         #         policy.pop("discount_policy_id")
    #         #
    #         #     else:
    #         #         policy_as_lst = (CompositeDiscountPolicyData.get_instance()).read([],
    #         #                                                                           policy_ref=policy[
    #         #                                                                               'discount_policy_id'])[
    #         #             'response']
    #         #         if len(policy_as_lst) > 0:
    #         #             daughter_policy = policy_as_lst[0]
    #         #             policy['policy1'] = self.read_discount_policies([],
    #         #                                                             policy_name=daughter_policy['policy1'],
    #         #                                                             store_name=policy['store_name'])['response'][0]
    #         #             policy['policy1'].pop("discount_policy_id")
    #         #             policy['policy2'] = self.read_discount_policies([],
    #         #                                                             policy_name=daughter_policy['policy2'],
    #         #                                                             store_name=policy['store_name'])['response'][0]
    #         #             policy['policy2'].pop("discount_policy_id")
    #         #             policy['flag'] = daughter_policy['flag']
    #         #             policy.pop("discount_policy_id")
    #         #         else:
    #         #             policy.pop("discount_policy_id")
    #         #
    #         #     output_lst.insert(len(output_lst), policy)
    #         # return ret(output_lst, "successful.")
    #         return (DiscountPolicyData.get_instance()).read([])
    #     except Exception as e:
    #         print(e)
    #         return ret([], self.__execution_failed_error_msg)
    #
    # def write_discount_policy(self, policy_name: str, store_name: str, product_name: str, percentage: float,
    #                           valid_until: datetime, is_active: bool = True,
    #                           precondition_product: str = "", precondition_min_amount: int = None,
    #                           precondition_min_basket_price: float = None,
    #                           policy1_name: str = "", policy2_name: str = "", flag: int = None):
    #     """
    #     Write a store to db.
    #
    #     :param store_name:
    #     :param founder_username:
    #     :return: size of user tbl after inserting the new one.
    #     """
    #     try:
    #         result = self.__proxy.execute([(DiscountPolicyData.get_instance()).write(policy_name, store_name,
    #                                                                                  product_name, percentage,
    #                                                                                  valid_until, is_active)])
    #         if result['response'] and (precondition_product != "" or precondition_min_amount is not None or
    #                                    precondition_min_basket_price is not None):
    #             policy_as_lst = (DataAccessFacade.get_instance()).read_discount_policies(["discount_policy_id"],
    #                                                                                      policy_name=policy_name,
    #                                                                                      store_name=store_name)[
    #                 'response']
    #             policy_ref = policy_as_lst[0]['discount_policy_id']
    #             return self.__proxy.execute([(ConditionalDiscountPolicyData.get_instance()).
    #                                         write(policy_ref,
    #                                               precondition_product,
    #                                               precondition_min_amount,
    #                                               precondition_min_basket_price)])
    #
    #         if result['response'] and (policy1_name != "" and store_name != "" and
    #                                    policy2_name != "" and
    #                                    flag is not None):
    #             policy_as_lst = (DataAccessFacade.get_instance()).read_discount_policies(["discount_policy_id"],
    #                                                                                      policy_name=policy_name,
    #                                                                                      store_name=store_name)[
    #                 'response']
    #             policy_ref = policy_as_lst[0]['discount_policy_id']
    #             pol1_as_lst = (DataAccessFacade.get_instance()).read_discount_policies(["discount_policy_id"],
    #                                                                                    policy_name=policy1_name,
    #                                                                                    store_name=store_name)[
    #                 'response']
    #             pol1_ref = pol1_as_lst[0]['discount_policy_id']
    #             pol2_as_lst = (DataAccessFacade.get_instance()).read_discount_policies(["discount_policy_id"],
    #                                                                                    policy_name=policy2_name,
    #                                                                                    store_name=store_name)[
    #                 'response']
    #             pol2_ref = pol2_as_lst[0]['discount_policy_id']
    #             return self.__proxy.execute([(CompositeDiscountPolicyData.get_instance()).write(policy_ref,
    #                                                                                             pol1_ref,
    #                                                                                             pol2_ref,
    #                                                                                             flag),
    #                                          (DiscountPolicyData.get_instance()).update(old_discount_policy_id=pol1_ref,
    #                                                                                     new_is_active=False),
    #                                          (DiscountPolicyData.get_instance()).update(old_discount_policy_id=pol2_ref,
    #                                                                                     new_is_active=False)])
    #
    #         return result
    #     except Exception as e:
    #         print(e)
    #         return ret(False, self.__execution_failed_error_msg)
    #
    # def update_discount_policies(self, old_discount_policy_id: int = None, old_policy_name: str = "",
    #                              old_store_name: str = "", old_product_name: str = "", old_percentage: float = None,
    #                              old_valid_until: datetime = None, old_is_active: bool = None,
    #                              new_policy_name: str = "",
    #                              new_store_name="", new_product_name: str = "", new_percentage: float = None,
    #                              new_valid_until: datetime = None, new_is_active: bool = None):
    #     """
    #     Update users in the db.
    #     old_<attribute> will composite a constraint of where to update.
    #     example(if old_username != ""), it will composite the constraint-
    #                                             where(user.username == old_username).
    #     new_<attribute> will update the <attribute> to the new value.
    #     example(if new_username != ""), it will update-
    #                                             update(user.username = new_username).
    #
    #     :return: the number of updated rows.
    #     """
    #     try:
    #         return self.__proxy.execute([(DiscountPolicyData.get_instance()).update(old_discount_policy_id,
    #                                                                                 old_policy_name, old_store_name,
    #                                                                                 old_product_name, old_percentage,
    #                                                                                 old_valid_until, old_is_active,
    #                                                                                 new_policy_name, new_store_name,
    #                                                                                 new_product_name, new_percentage,
    #                                                                                 new_valid_until, new_is_active
    #                                                                                 )])
    #     except Exception as e:
    #         # print(e)
    #         return ret(False, self.__execution_failed_error_msg)
    #
    # def delete_discount_policies(self, discount_policy_id: int = None, policy_name: str = "",
    #                              store_name="", product_name: str = "", percentage: float = None,
    #                              valid_until: datetime = None,
    #                              is_active: bool = None):
    #     """
    #     Delete users from the DB.
    #     <attribute> will composite a constraint of where to delete.
    #     example(if old_username != ""), it will composite the constraint-
    #                                            where(user.username == username).
    #
    #     :return: the number of deleted rows.
    #     """
    #     try:
    #         return self.__proxy.execute([(DiscountPolicyData.get_instance()).delete(discount_policy_id,
    #                                                                                 policy_name, store_name,
    #                                                                                 product_name, percentage,
    #                                                                                 valid_until, is_active)])
    #     except Exception as e:
    #         # print(e)
    #         return ret(False, self.__execution_failed_error_msg)

    def write_purchase(self, username: str, store_name: str, total_price: float, date: datetime, products_lst):
        # products_lst -> [{"product_name": str, "product_price": float, "amount": int}]
        # mother_write_query, daughters_write_queries_attributes: [{}],
        #                                       other_update_stoke_queries: [], other_update_basket_queries: []
        try:
            mother_write_query = (PurchaseData.get_instance()).write(username, store_name,
                                                                     total_price, date)
            daughters_write_queries_attributes = []
            other_update_stoke_queries = []
            other_update_basket_queries = []
            for product in products_lst:
                product_name = product['product_name']
                product_price = product['product_price']
                product_amount: int = product['amount']
                write_to_products_in_purchase_query = (ProductsInPurchaseData.get_instance()).write(product_name,
                                                                                                    product_price,
                                                                                                    product_amount,
                                                                                                    username,
                                                                                                    store_name)
                product_as_lst = self.read_products(["product_id"], store_name=store_name, product_name=product_name)[
                    'response']
                if len(product_as_lst) == 0:
                    raise ValueError()
                product_ref = product_as_lst[0]['product_id']
                remove_products_in_basket_query = (ProductsInBasketData.get_instance()).delete(
                    username=username,
                    product_ref=product_ref)
                product_original_amount: int = self.read_products(["amount"], product_name, store_name)['response'][
                    0]['amount']
                new_amount: int = product_original_amount - product_amount
                update_stock_amount_query = (ProductData.get_instance()).update(old_product_name=product_name,
                                                                                old_store_name=store_name,
                                                                                new_amount=new_amount)

                daughters_write_queries_attributes.insert(len(daughters_write_queries_attributes),
                                                          write_to_products_in_purchase_query)
                other_update_stoke_queries.insert(len(other_update_stoke_queries), update_stock_amount_query)
                # TODO: NEEDED?!?!
                other_update_basket_queries.insert(len(other_update_basket_queries), remove_products_in_basket_query)

            return self.__proxy.execute_atomic_purchase_write(mother_write_query, daughters_write_queries_attributes,
                                                              other_update_stoke_queries, other_update_basket_queries)

        except Exception as e:
            # print(e)
            return ret(False, self.__execution_failed_error_msg)

    def read_purchases(self, attributes_to_read=None, username: str = "", store_name: str = "",
                       total_price: float = None, date: datetime = None,
                       product_name: str = "", product_purchase_price: float = None, product_amount: int = None):

        if attributes_to_read is None:
            attributes_to_read = []
        try:
            purchases_ids_as_lst = (PurchaseData.get_instance()).read(['purchase_id'], username=username,
                                                                      store_name=store_name,
                                                                      total_price=total_price,
                                                                      date=date)
            output_lst = []
            for purchase_id_as_dictionary in purchases_ids_as_lst:
                purchase_id = purchase_id_as_dictionary['purchase_id']
                purchase_as_dictionary_as_lst = (PurchaseData.get_instance()).read(attributes_to_read,
                                                                                   purchase_id=purchase_id)
                purchase_as_dictionary: dict = purchase_as_dictionary_as_lst[0]
                purchase_as_dictionary['products_lst'] = (ProductsInPurchaseData.get_instance()) \
                    .read([], purchase_id=purchase_id, product_name=product_name,
                          product_purchase_price=product_purchase_price, amount=product_amount)
                if len(purchase_as_dictionary['products_lst']) > 0:
                    output_lst.insert(len(output_lst), purchase_as_dictionary)

            return ret(output_lst, "Successful.")
        except Exception as e:
            # print(e)
            return ret([], self.__execution_failed_error_msg)

    def delete_purchases(self, username: str = "", store_name: str = "", total_price: float = None,
                         date: datetime = None,
                         product_name: str = "", product_purchase_price: float = None, product_amount: int = None):
        try:
            queries = []
            if product_name != "" or product_purchase_price is not None or product_amount is not None:
                purchases_ids_as_lst_first_draft = (ProductsInPurchaseData.get_instance()).read(["purchase_id"],
                                                                                                product_name=
                                                                                                product_name,
                                                                                                product_purchase_price=
                                                                                                product_purchase_price,
                                                                                                amount=product_amount)
                purchases_ids_as_lst = []
                for purchase_id_as_lst_first_draft in purchases_ids_as_lst_first_draft:
                    purchase_id = purchase_id_as_lst_first_draft['purchase_id']
                    lst = (PurchaseData.get_instance()).read(["purchase_id"],
                                                             purchase_id=purchase_id,
                                                             username=username,
                                                             store_name=store_name,
                                                             total_price=total_price,
                                                             date=date)
                    if len(lst) > 0:
                        purchases_ids_as_lst.insert(0, lst[0])
                for purchases_id_as_dictionary in purchases_ids_as_lst:
                    purchase_id = purchases_id_as_dictionary['purchase_id']
                    queries.insert(len(queries), (PurchaseData.get_instance()).delete(purchase_id=purchase_id))

                return self.__proxy.execute(queries)
            purchases_ids_as_lst = (PurchaseData.get_instance()).read(['purchase_id'], username=username,
                                                                      store_name=store_name,
                                                                      total_price=total_price,
                                                                      date=date)

            for purchases_id_as_dictionary in purchases_ids_as_lst:
                purchase_id = purchases_id_as_dictionary['purchase_id']
                queries.insert(len(queries), (PurchaseData.get_instance()).delete(purchase_id=purchase_id))
            return self.__proxy.execute(queries)

        except Exception as e:
            # print(e)
            return ret([], self.__execution_failed_error_msg)

    def update_purchases(self, old_username: str = "", old_store_name: str = "",
                         old_total_price: float = None, old_date: datetime = None, old_product_name: str = "",
                         old_product_purchase_price: float = None, old_product_amount: int = None,
                         new_username: str = "", new_store_name: str = "", new_total_price: float = None,
                         new_date: datetime = None, new_product_name: str = "", new_product_purchase_price: float = None
                         , new_product_amount: int = None):
        try:
            queries = []
            if old_product_name != "" or old_product_purchase_price is not None or old_product_amount is not None:
                purchases_ids_as_lst_first_draft = (ProductsInPurchaseData.get_instance()).read(["purchase_id"],
                                                                                                product_name=old_product_name,
                                                                                                product_purchase_price=
                                                                                                old_product_purchase_price,
                                                                                                amount=old_product_amount)
                purchases_ids_as_lst = []
                for purchase_id_as_lst_first_draft in purchases_ids_as_lst_first_draft:
                    purchase_id = purchase_id_as_lst_first_draft['purchase_id']
                    lst = (PurchaseData.get_instance()).read(["purchase_id"],
                                                             purchase_id=purchase_id,
                                                             username=old_username,
                                                             store_name=old_store_name,
                                                             total_price=old_total_price,
                                                             date=old_date)
                    if len(lst) > 0:
                        purchases_ids_as_lst.insert(0, lst[0])
                for purchases_id_as_dictionary in purchases_ids_as_lst:
                    purchase_id = purchases_id_as_dictionary['purchase_id']
                    if (new_product_name != "" or new_product_purchase_price is not None or new_product_amount is not
                            None):
                        queries.insert(len(queries),
                                       (ProductsInPurchaseData.get_instance()).update(purchase_id,
                                                                                      new_product_name=new_product_name,
                                                                                      new_product_purchase_price=
                                                                                      new_product_purchase_price,
                                                                                      new_amount=new_product_amount))

                    queries.insert(len(queries), (PurchaseData.get_instance()).update(old_purchase_id=purchase_id,
                                                                                      new_username=new_username,
                                                                                      new_store_name=new_store_name,
                                                                                      new_total_price=new_total_price,
                                                                                      new_date=new_date))
                return self.__proxy.execute(queries)

            purchases_ids_as_lst = (PurchaseData.get_instance()).read(['purchase_id'], old_username=old_username,
                                                                      old_store_name=old_store_name,
                                                                      old_total_price=old_total_price,
                                                                      old_date=old_date)

            for purchases_id_as_dictionary in purchases_ids_as_lst:
                purchase_id = purchases_id_as_dictionary['purchase_id']
                if (new_product_name != "" or new_product_purchase_price is not None or new_product_amount is not
                        None):
                    queries.insert(len(queries),
                                   (ProductsInPurchaseData.get_instance()).update(purchase_id,
                                                                                  new_product_name=new_product_name,
                                                                                  new_product_purchase_price=
                                                                                  new_product_purchase_price,
                                                                                  new_amount=new_product_amount))

                    queries.insert(len(queries), (PurchaseData.get_instance()).update(old_purchase_id=purchase_id,
                                                                                      new_username=new_username,
                                                                                      new_store_name=new_store_name,
                                                                                      new_total_price=new_total_price,
                                                                                      new_date=new_date))
            return self.__proxy.execute(queries)

        except Exception as e:
            # print(e)
            return ret([], self.__execution_failed_error_msg)
