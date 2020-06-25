from datetime import datetime

from peewee import Expression, OP
from src.Logger import errorLogger
from src.main.DataAccessLayer.ConnectionProxy.Tables import Purchase, ProductsInPurchase
from src.main.DataAccessLayer.ConnectionProxy.DbProxy import DbProxy, and_exprs

"""
Represent the table of store owners appointments.
NOT the domain StoreOwnerAppointment.
"""


class ProductsInPurchaseData:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if ProductsInPurchaseData.__instance is None:
            ProductsInPurchaseData()
        return ProductsInPurchaseData.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if ProductsInPurchaseData.__instance is not None:
            errorLogger("This class is a singleton!")
            raise Exception("This class is a singleton!")
        else:
            self.__tbl = ProductsInPurchase
            self.__attr_purchase_id = "purchase_id"
            self.__attr_product_name = "product_name"
            self.__attr_product_purchase_price = "product_purchase_price"
            self.__attr_amount = "amount"
            self.__attributes_as_dictionary = {self.__attr_purchase_id: self.__tbl.purchase_id,
                                               self.__attr_product_name: self.__tbl.product_name,
                                               self.__attr_product_purchase_price: self.__tbl.product_purchase_price,
                                               self.__attr_amount: self.__tbl.amount}
            ProductsInPurchaseData.__instance = self

    def read(self, attributes_to_read: [str], purchase_id: int = None, product_name: str = "",
             product_purchase_price: float = None, amount: int = None):
        """
        Read store owner appointment from db.
        Raise exception if an attribute in attributes_to_read is illegal.
        <attribute> will composite a constraint of where to read.
        example(if old_username != ""), it will composite the constraint-
                                               where(user.username == username).

        :return: dict of the result data.
        """
        if len(attributes_to_read) > 0:
            for attribute in attributes_to_read:
                if attribute.lower() not in self.__attributes_as_dictionary.keys():
                    raise AttributeError("Attribute " + attribute + " doesn't exist in " + str(type(self.__tbl)) + ".")
        else:
            attributes_to_read: list = list(self.__attributes_as_dictionary.keys())
            attributes_to_read.remove(self.__attr_purchase_id)

        const_lst = []
        if not (purchase_id is None):
            const_lst.append((Expression(self.__tbl.purchase_id, OP.EQ, purchase_id)))
        if not (product_name == ""):
            const_lst.append((Expression(self.__tbl.product_name, OP.EQ, product_name)))
        if not (product_purchase_price is None):
            const_lst.append((Expression(self.__tbl.product_purchase_price, OP.EQ, product_purchase_price)))
        if not (amount is None):
            const_lst.append((Expression(self.__tbl.amount, OP.EQ, amount)))
        where_expr = and_exprs(const_lst)

        result = (DbProxy.get_instance()).read(self.__tbl, where_expr=where_expr)
        output_lst = []
        for data_obj in result:
            data_as_dictionary = {}
            if self.__attr_purchase_id in attributes_to_read:
                data_as_dictionary[self.__attr_purchase_id] = data_obj.purchase_id
            if self.__attr_product_name in attributes_to_read:
                data_as_dictionary[self.__attr_product_name] = data_obj.product_name
            if self.__attr_product_purchase_price in attributes_to_read:
                data_as_dictionary[self.__attr_product_purchase_price] = data_obj.product_purchase_price
            if self.__attr_amount in attributes_to_read:
                data_as_dictionary[self.__attr_amount] = data_obj.amount
            output_lst.append(data_as_dictionary)

        return output_lst

    def write(self, product_name: str, product_purchase_price: float,
              amount: int, username: str, store_name: str):
        """
        write store owner appointment to db.

        :return:
        """
        attributes_as_dictionary = {self.__attributes_as_dictionary[self.__attr_product_name]: product_name,
                                    self.__attributes_as_dictionary[self.__attr_product_purchase_price]:
                                        product_purchase_price,
                                    self.__attributes_as_dictionary[self.__attr_amount]: amount}

        return attributes_as_dictionary

    def update(self, old_purchase_id: int = None, old_product_name: str = "",
               old_product_purchase_price: float = None, old_amount: int = None,
               new_product_name: str = "", new_product_purchase_price: float = None, new_amount: int = None):
        """
        Update store owner appointment in the db.
        old_<attribute> will composite a constraint of where to update.
        example(if old_username != ""), it will composite the constraint-
                                                where(user.username == old_username).
        new_<attribute> will update the <attribute> to the new value.
        example(if new_username != ""), it will update-
                                                update(user.username = new_username).

        :return: the number of updated rows.
        """
        const_lst = []
        if not (old_purchase_id is None):
            const_lst.append((Expression(self.__tbl.purchase_id, OP.EQ, old_purchase_id)))
        if not (old_product_name == ""):
            const_lst.append((Expression(self.__tbl.product_name, OP.EQ, old_product_name)))
        if not (old_product_purchase_price is None):
            const_lst.append((Expression(self.__tbl.product_purchase_price, OP.EQ, old_product_purchase_price)))
        if not (old_amount is None):
            const_lst.append((Expression(self.__tbl.amount, OP.EQ, old_amount)))
        where_expr = and_exprs(const_lst)

        attributes_as_dictionary = {}
        if not (new_product_name == ""):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_product_name]] = \
                new_product_name
        if not (new_product_purchase_price is None):
            attributes_as_dictionary[
                self.__attributes_as_dictionary[self.__attr_product_purchase_price]] = new_product_purchase_price
        if not (new_amount is None):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_amount]] = \
                new_amount
        if len(attributes_as_dictionary) == 0:
            raise AttributeError("Nothing to update")

        return DbProxy.get_instance().update(self.__tbl, attributes_as_dictionary, where_expr)

    def delete(self, purchase_id: int = None, product_name: str = "", product_purchase_price: float = None,
               amount: int = None):
        """
        Delete store owner appointments from the DB.
        <attribute> will composite a constraint of where to delete.
        example(if old_username != ""), it will composite the constraint-
                                               where(user.username == username).

        :return: the number of deleted rows.
        """
        const_lst = []
        if not (purchase_id is None):
            const_lst.append((Expression(self.__tbl.purchase_id, OP.EQ, purchase_id)))
        if not (product_name == ""):
            const_lst.append((Expression(self.__tbl.product_name, OP.EQ, product_name)))
        if not (product_purchase_price is None):
            const_lst.append((Expression(self.__tbl.product_purchase_price, OP.EQ, product_purchase_price)))
        if not (amount is None):
            const_lst.append((Expression(self.__tbl.amount, OP.EQ, amount)))
        where_expr = and_exprs(const_lst)
        return (DbProxy.get_instance()).delete(self.__tbl, where_expr=where_expr)

    # def __read_purchase_id(self, username: str = "", store_name: str = ""):
    #     """
    #     Read store owner appointment from db.
    #     Raise exception if an attribute in attributes_to_read is illegal.
    #     <attribute> will composite a constraint of where to read.
    #     example(if old_username != ""), it will composite the constraint-
    #                                            where(user.username == username).
    #
    #     :return: dict of the result data.
    #     """
    #     attributes_to_read = ["purchase_id"]
    #     const_lst = []
    #     if not (username == ""):
    #         const_lst.append((Expression(Purchase.username, OP.EQ, username)))
    #     if not (store_name == ""):
    #         const_lst.append(Expression(Purchase.store_name, OP.EQ, store_name))
    #     where_expr = and_exprs(const_lst)
    #
    #     result = (DbProxy.get_instance()).read(Purchase, where_expr=where_expr)
    #     output_lst = []
    #     for data_obj in result:
    #         data_as_dictionary = {}
    #         if "purchase_id" in attributes_to_read:
    #             data_as_dictionary["purchase_id"] = data_obj.purchase_id
    #         output_lst.append(data_as_dictionary)
    #
    #
    #     if len(output_lst) > 0:
    #         last = -1
    #         for i in range(len(output_lst)):
    #             last = max(output_lst[i]['purchase_id'])
    #         return last
    #     return None
