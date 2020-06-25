from peewee import Expression, OP
from src.Logger import errorLogger
from src.main.DataAccessLayer.ConnectionProxy.Tables import Product
from src.main.DataAccessLayer.ConnectionProxy.DbProxy import DbProxy, and_exprs
import jsonpickle

"""
Represent the table of products.
NOT the domain product.
"""


class ProductData:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if ProductData.__instance is None:
            ProductData()
        return ProductData.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if ProductData.__instance is not None:
            errorLogger("This class is a singleton!")
            raise Exception("This class is a singleton!")
        else:
            self.__tbl = Product
            self.__attr_product_id = "product_id"
            self.__attr_product_name = "product_name"
            self.__attr_store_name = "store_name"
            self.__attr_price = "price"
            self.__attr_category = "category"
            self.__attr_amount = "amount"
            self.__attr_purchase_type = "purchase_type"
            self.__attributes_as_dictionary = {self.__attr_product_id: self.__tbl.product_id,
                                               self.__attr_product_name: self.__tbl.product_name,
                                               self.__attr_store_name: self.__tbl.store_name,
                                               self.__attr_price: self.__tbl.price,
                                               self.__attr_category: self.__tbl.category,
                                               self.__attr_amount: self.__tbl.amount,
                                               self.__attr_purchase_type: self.__tbl.purchase_type}
            ProductData.__instance = self

    def read(self, attributes_to_read: [str], product_id: int = None, product_name: str = "", store_name: str = "",
             price: float = None, category: str = "", amount: int = None, purchase_type: int = None):
        """
        Read users from db.
        Raise exception if an attribute in attributes_to_read is illegal.
        <attribute> will composite a constraint of where to read.
        example(if old_username != ""), it will composite the constraint-
                                               where(user.username == username).

        :param product_id:
        :param product_name:
        :param price:
        :param category:
        :param amount:
        :param purchase_type:
        :param store_name:
        :param attributes_to_read: the list of attributes that will return from the db.
                                    type: [str]

        :return: list of dictionaries that contain attributes_to_read fields.
        """
        if len(attributes_to_read) > 0:
            for attribute in attributes_to_read:
                if attribute.lower() not in self.__attributes_as_dictionary.keys():
                    raise AttributeError("Attribute " + attribute + " doesn't exist in " + str(type(self.__tbl)) + ".")
        else:
            attributes_to_read = list(self.__attributes_as_dictionary.keys())
            attributes_to_read.remove(self.__attr_product_id)

        const_lst = []
        if not (product_id is None):
            const_lst.append(Expression(self.__tbl.product_id, OP.EQ, product_id))
        if not (product_name == ""):
            const_lst.append(Expression(self.__tbl.product_name, OP.EQ, product_name))
        if not (store_name == ""):
            const_lst.append(Expression(self.__tbl.store_name, OP.EQ, store_name))
        if not (price is None):
            const_lst.append(Expression(self.__tbl.price, OP.EQ, price))
        if not (category == ""):
            const_lst.append(Expression(self.__tbl.category, OP.EQ, category))
        if not (amount is None):
            const_lst.append(Expression(self.__tbl.amount, OP.EQ, amount))
        if not (purchase_type is None):
            const_lst.append(Expression(self.__tbl.purchase_type, OP.EQ, purchase_type))
        where_expr = and_exprs(const_lst)

        result = (DbProxy.get_instance()).read(self.__tbl, where_expr=where_expr)
        output_lst = []
        for data_obj in result:
            user_data_as_dictionary = {}
            if self.__attr_product_id in attributes_to_read:
                user_data_as_dictionary[self.__attr_product_id] = data_obj.product_id
            if self.__attr_product_name in attributes_to_read:
                user_data_as_dictionary[self.__attr_product_name] = data_obj.product_name
            if self.__attr_store_name in attributes_to_read:
                user_data_as_dictionary[self.__attr_store_name] = data_obj.store_name.store_name
            if self.__attr_price in attributes_to_read:
                user_data_as_dictionary[self.__attr_price] = data_obj.price
            if self.__attr_category in attributes_to_read:
                user_data_as_dictionary[self.__attr_category] = data_obj.category
            if self.__attr_amount in attributes_to_read:
                user_data_as_dictionary[self.__attr_amount] = data_obj.amount
            if self.__attr_purchase_type in attributes_to_read:
                user_data_as_dictionary[self.__attr_purchase_type] = data_obj.purchase_type
            output_lst.append(user_data_as_dictionary)

        return output_lst

    def write(self, product_name: str, store_name: str, price: float, category: str, amount: int, purchase_type: int):
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
        attributes_as_dictionary = {self.__attributes_as_dictionary[self.__attr_product_name]: product_name,
                                    self.__attributes_as_dictionary[self.__attr_store_name]: store_name,
                                    self.__attributes_as_dictionary[self.__attr_price]: price,
                                    self.__attributes_as_dictionary[self.__attr_category]: category,
                                    self.__attributes_as_dictionary[self.__attr_amount]: amount,
                                    self.__attributes_as_dictionary[self.__attr_purchase_type]: purchase_type}

        return (DbProxy.get_instance()).write(self.__tbl, attributes_as_dictionary)

    def update(self, old_product_id: int = None, old_product_name: str = "", old_store_name: str = "", old_price: float = None,
               old_category: str = "", old_amount: int = None, old_purchase_type: int = None,
               new_product_name: str = "", new_store_name: str = "", new_price: float = None,
               new_category: str = "", new_amount: int = None, new_purchase_type: int = None):
        """
        Update users in the db.
        old_<attribute> will composite a constraint of where to update.
        example(if old_username != ""), it will composite the constraint-
                                                where(user.username == old_username).
        new_<attribute> will update the <attribute> to the new value.
        example(if new_username != ""), it will update-
                                                update(user.username = new_username).

        :return: the number of updated rows.
        """
        const_lst = []
        if not (old_product_id is None):
            const_lst.append(Expression(self.__tbl.product_id, OP.EQ, old_product_id))
        if not (old_product_name == ""):
            const_lst.append(Expression(self.__tbl.product_name, OP.EQ, old_product_name))
        if not (old_store_name == ""):
            const_lst.append(Expression(self.__tbl.store_name, OP.EQ, old_store_name))
        if not (old_price is None):
            const_lst.append(Expression(self.__tbl.price, OP.EQ, old_price))
        if not (old_category == ""):
            const_lst.append(Expression(self.__tbl.category, OP.EQ, old_category))
        if not (old_amount is None):
            const_lst.append(Expression(self.__tbl.amount, OP.EQ, old_amount))
        if not (old_purchase_type is None):
            const_lst.append(Expression(self.__tbl.purchase_type, OP.EQ, old_purchase_type))
        where_expr = and_exprs(const_lst)

        attributes_as_dictionary = {}
        if not (new_product_name == ""):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_product_name]] = new_product_name
        if not (new_store_name == ""):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_store_name]] = new_store_name
        if not (new_price is None):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_price]] = new_price
        if not (new_category == ""):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_category]] = new_category
        if not (new_amount is None):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_amount]] = new_amount
        if not (new_purchase_type is None):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_purchase_type]] = new_purchase_type

        if len(attributes_as_dictionary) == 0:
            raise AttributeError("Nothing to update")

        return DbProxy.get_instance().update(self.__tbl, attributes_as_dictionary, where_expr)

    def delete(self, product_id: int = None, product_name: str = "", store_name: str = "", price: float = None,
               category: str = "", amount: int = None, purchase_type: int = None):
        """
        Delete users from the DB.
        <attribute> will composite a constraint of where to delete.
        example(if old_username != ""), it will composite the constraint-
                                               where(user.username == username).

        :return: the number of deleted rows.
        """
        const_lst = []
        if not (product_id is None):
            const_lst.append(Expression(self.__tbl.product_id, OP.EQ, product_id))
        if not (product_name == ""):
            const_lst.append(Expression(self.__tbl.product_name, OP.EQ, product_name))
        if not (store_name == ""):
            const_lst.append(Expression(self.__tbl.store_name, OP.EQ, store_name))
        if not (price is None):
            const_lst.append(Expression(self.__tbl.price, OP.EQ, price))
        if not (category == ""):
            const_lst.append(Expression(self.__tbl.category, OP.EQ, category))
        if not (amount is None):
            const_lst.append(Expression(self.__tbl.amount, OP.EQ, amount))
        if not (purchase_type is None):
            const_lst.append(Expression(self.__tbl.purchase_type, OP.EQ, purchase_type))
        where_expr = and_exprs(const_lst)
        return (DbProxy.get_instance()).delete(self.__tbl, where_expr=where_expr)
