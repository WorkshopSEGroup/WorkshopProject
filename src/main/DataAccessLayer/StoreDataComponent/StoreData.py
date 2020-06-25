from peewee import Expression, OP
from src.Logger import errorLogger
from src.main.DataAccessLayer.ConnectionProxy.Tables import Store
from src.main.DataAccessLayer.ConnectionProxy.DbProxy import DbProxy, and_exprs
import jsonpickle

"""
Represent the table of stores.
NOT the domain stores.
"""


class StoreData:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if StoreData.__instance is None:
            StoreData()
        return StoreData.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if StoreData.__instance is not None:
            errorLogger("This class is a singleton!")
            raise Exception("This class is a singleton!")
        else:
            self.__tbl = Store
            self.__attr_store_name = "store_name"
            self.__attr_founder_username = "founder_username"
            self.__attributes_as_dictionary = {self.__attr_store_name: self.__tbl.store_name,
                                               self.__attr_founder_username: self.__tbl.founder_username}
            StoreData.__instance = self

    def read(self, attributes_to_read: [str], store_name="", founder_username=""):
        """
        Read users from db.
        Raise exception if an attribute in attributes_to_read is illegal.
        <attribute> will composite a constraint of where to read.
        example(if old_username != ""), it will composite the constraint-
                                               where(user.username == username).

        :param founder_username:
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
            attributes_to_read = [self.__attr_store_name, self.__attr_founder_username]

        const_lst = []
        if not (store_name == ""):
            const_lst.append(Expression(self.__tbl.store_name, OP.EQ, store_name))
        if not (founder_username == ""):
            const_lst.append(Expression(self.__tbl.founder_username, OP.EQ, founder_username))
        where_expr = and_exprs(const_lst)

        result = (DbProxy.get_instance()).read(self.__tbl, where_expr=where_expr)
        output_lst = []
        for data_obj in result:
            data_as_dictionary = {}
            if self.__attr_store_name in attributes_to_read:
                data_as_dictionary[self.__attr_store_name] = data_obj.store_name
            if self.__attr_founder_username in attributes_to_read:
                data_as_dictionary[self.__attr_founder_username] = data_obj.founder_username.username
            output_lst.append(data_as_dictionary)

        return output_lst

    def write(self,  store_name="", founder_username=""):
        """
        Write a store to db.

        :param store_name:
        :param founder_username:
        :return: size of user tbl after inserting the new one.
        """
        attributes_as_dictionary = {self.__attributes_as_dictionary[self.__attr_store_name]: store_name,
                                    self.__attributes_as_dictionary[self.__attr_founder_username]: founder_username}

        return (DbProxy.get_instance()).write(self.__tbl, attributes_as_dictionary)

    def update(self, old_store_name: str = "", old_founder_username: str = "",
               new_store_name: str = "", new_founder_username: str = ""):
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
        if not (old_store_name == ""):
            const_lst.append(Expression(self.__tbl.store_name, OP.EQ, old_store_name))
        if not (old_founder_username == ""):
            const_lst.append(Expression(self.__tbl.founder_username, OP.EQ, old_founder_username))
        where_expr = and_exprs(const_lst)

        attributes_as_dictionary = {}
        if not (new_store_name == ""):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_store_name]] = new_store_name
        if not (new_founder_username == ""):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_founder_username]] = \
                new_founder_username

        if len(attributes_as_dictionary) == 0:
            raise AttributeError("Nothing to update")

        return DbProxy.get_instance().update(self.__tbl, attributes_as_dictionary, where_expr)

    def delete(self,  store_name="", founder_username=""):
        """
        Delete users from the DB.
        <attribute> will composite a constraint of where to delete.
        example(if old_username != ""), it will composite the constraint-
                                               where(user.username == username).

        :return: the number of deleted rows.
        """
        const_lst = []
        if not (store_name == ""):
            const_lst.append(Expression(self.__tbl.store_name, OP.EQ, store_name))
        if not (founder_username == ""):
            const_lst.append(Expression(self.__tbl.founder_username, OP.EQ, founder_username))
        where_expr = and_exprs(const_lst)
        return (DbProxy.get_instance()).delete(self.__tbl, where_expr=where_expr)
