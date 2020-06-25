from peewee import Expression, OP
from src.Logger import errorLogger
from src.main.DataAccessLayer.ConnectionProxy.Tables import StoreOwnerAppointment
from src.main.DataAccessLayer.ConnectionProxy.DbProxy import DbProxy, and_exprs

"""
Represent the table of store owners appointments.
NOT the domain StoreOwnerAppointment.
"""


class StoreOwnerAppointmentData:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if StoreOwnerAppointmentData.__instance is None:
            StoreOwnerAppointmentData()
        return StoreOwnerAppointmentData.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if StoreOwnerAppointmentData.__instance is not None:
            errorLogger("This class is a singleton!")
            raise Exception("This class is a singleton!")
        else:
            self.__tbl = StoreOwnerAppointment
            self.__attr_appointee_username = "appointee_username"
            self.__attr_store_name = "store_name"
            self.__attr_appointer_username = "appointer_username"
            self.__attributes_as_dictionary = {self.__attr_appointee_username: self.__tbl.appointee_username,
                                               self.__attr_store_name: self.__tbl.store_name,
                                               self.__attr_appointer_username: self.__tbl.appointer_username}
            StoreOwnerAppointmentData.__instance = self

    def read(self, attributes_to_read: [str], appointee_username: str = "", store_name: str = "",
             appointer_username: str = ""):
        """
        Read store owner appointment from db.
        Raise exception if an attribute in attributes_to_read is illegal.
        <attribute> will composite a constraint of where to read.
        example(if old_username != ""), it will composite the constraint-
                                               where(user.username == username).

        :param attributes_to_read: lst of attributes to read.
        :param appointee_username: pk.
        :param store_name: pk.
        :param appointer_username:
        :return: dict of the result data.
        """
        if len(attributes_to_read) > 0:
            for attribute in attributes_to_read:
                if attribute.lower() not in self.__attributes_as_dictionary.keys():
                    raise AttributeError("Attribute " + attribute + " doesn't exist in " + str(type(self.__tbl)) + ".")
        else:
            attributes_to_read = self.__attributes_as_dictionary.keys()

        const_lst = []
        if not (appointee_username == ""):
            const_lst.append((Expression(self.__tbl.appointee_username, OP.EQ, appointee_username)))
        if not (store_name == ""):
            const_lst.append(Expression(self.__tbl.store_name, OP.EQ, store_name))
        if not (appointer_username == ""):
            const_lst.append((Expression(self.__tbl.appointer_username, OP.EQ, appointer_username)))
        where_expr = and_exprs(const_lst)

        result = (DbProxy.get_instance()).read(self.__tbl, where_expr=where_expr)
        output_lst = []
        for data_obj in result:
            data_as_dictionary = {}
            if self.__attr_appointee_username in attributes_to_read:
                data_as_dictionary[self.__attr_appointee_username] = data_obj.appointee_username.username
            if self.__attr_store_name in attributes_to_read:
                data_as_dictionary[self.__attr_store_name] = data_obj.store_name.store_name
            if self.__attr_appointer_username in attributes_to_read:
                data_as_dictionary[self.__attr_appointer_username] = data_obj.appointer_username.username
            output_lst.append(data_as_dictionary)

        return output_lst

    def write(self, appointee_username: str, store_name: str, appointer_username: str):
        """
        write store owner appointment to db.

        :param appointee_username: pk
        :param store_name:pk
        :param appointer_username:
        :return:
        """
        attributes_as_dictionary = {self.__attributes_as_dictionary[self.__attr_appointee_username]: appointee_username,
                                    self.__attributes_as_dictionary[self.__attr_store_name]: store_name,
                                    self.__attributes_as_dictionary[self.__attr_appointer_username]: appointer_username}

        return (DbProxy.get_instance()).write(self.__tbl, attributes_as_dictionary)

    def update(self, old_appointee_username: str = "", old_store_name: str = "", old_appointer_username: str = "",
               new_appointee_username: str = "", new_store_name: str = "", new_appointer_username: str = ""):
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
        if not (old_appointee_username == ""):
            const_lst.append((Expression(self.__tbl.appointee_username, OP.EQ, old_appointee_username)))
        if not (old_store_name == ""):
            const_lst.append(Expression(self.__tbl.store_name, OP.EQ, old_store_name))
        if not (old_appointer_username == ""):
            const_lst.append((Expression(self.__tbl.appointer_username, OP.EQ, old_appointer_username)))
        where_expr = and_exprs(const_lst)

        attributes_as_dictionary = {}
        if not (new_appointee_username == ""):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_appointee_username]] = \
                new_appointee_username
        if not (new_store_name == ""):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_store_name]] = new_store_name
        if not (new_appointer_username == ""):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_appointer_username]] = \
                new_appointer_username
        if len(attributes_as_dictionary) == 0:
            raise AttributeError("Nothing to update")

        return DbProxy.get_instance().update(self.__tbl, attributes_as_dictionary, where_expr)

    def delete(self, appointee_username: str = "", store_name: str = "", appointer_username: str = ""):
        """
        Delete store owner appointments from the DB.
        <attribute> will composite a constraint of where to delete.
        example(if old_username != ""), it will composite the constraint-
                                               where(user.username == username).

        :return: the number of deleted rows.
        """
        const_lst = []
        if not (appointee_username == ""):
            const_lst.append((Expression(self.__tbl.appointee_username, OP.EQ, appointee_username)))
        if not (store_name == ""):
            const_lst.append(Expression(self.__tbl.store_name, OP.EQ, store_name))
        if not (appointer_username == ""):
            const_lst.append((Expression(self.__tbl.appointer_username, OP.EQ, appointer_username)))
        where_expr = and_exprs(const_lst)
        return (DbProxy.get_instance()).delete(self.__tbl, where_expr=where_expr)
