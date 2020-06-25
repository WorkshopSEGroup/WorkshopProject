from datetime import datetime

from peewee import Expression, OP
from src.Logger import errorLogger
from src.main.DataAccessLayer.ConnectionProxy.Tables import Statistic
from src.main.DataAccessLayer.ConnectionProxy.DbProxy import DbProxy, and_exprs

"""
Represent the table of Statistic.
"""


class StatisticData:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if StatisticData.__instance is None:
            StatisticData()
        return StatisticData.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if StatisticData.__instance is not None:
            errorLogger("This class is a singleton!")
            raise Exception("This class is a singleton!")
        else:
            self.__tbl = Statistic
            self.__attr_date = "date"
            self.__attr_guests = "guests"
            self.__attr_subscribers = "subscribers"
            self.__attr_store_managers = "store_managers"
            self.__attr_store_owners = "store_owners"
            self.__attr_system_managers = "system_managers"
            self.__attributes_as_dictionary = {self.__attr_date: self.__tbl.date,
                                               self.__attr_guests: self.__tbl.guests,
                                               self.__attr_subscribers: self.__tbl.subscribers,
                                               self.__attr_store_managers: self.__tbl.store_managers,
                                               self.__attr_store_owners: self.__tbl.store_owners,
                                               self.__attr_system_managers: self.__tbl.system_managers}
            StatisticData.__instance = self

    def read(self, attributes_to_read: [str], date: datetime = None, guests: int = None, subscribers: int = None,
             store_managers: int = None, store_owners: int = None, system_managers: int = None):
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
        if len(attributes_to_read) > 0:
            for attribute in attributes_to_read:
                if attribute.lower() not in self.__attributes_as_dictionary.keys():
                    raise AttributeError("Attribute " + attribute + " doesn't exist in " + str(type(self.__tbl)) + ".")
        else:
            attributes_to_read = self.__attributes_as_dictionary.keys()

        const_lst = []
        if not (date is None):
            const_lst.append(Expression(self.__tbl.date, OP.EQ, date))
        if not (guests is None):
            const_lst.append(Expression(self.__tbl.guests, OP.EQ, guests))
        if not (subscribers is None):
            const_lst.append(Expression(self.__tbl.subscribers, OP.EQ, subscribers))
        if not (store_managers is None):
            const_lst.append(Expression(self.__tbl.store_managers, OP.EQ, store_managers))
        if not (store_owners is None):
            const_lst.append(Expression(self.__tbl.store_owners, OP.EQ, store_owners))
        if not (system_managers is None):
            const_lst.append(Expression(self.__tbl.system_managers, OP.EQ, system_managers))
        where_expr = and_exprs(const_lst)

        result = (DbProxy.get_instance()).read(self.__tbl, where_expr=where_expr)
        output_lst = []
        for data_obj in result:
            user_data_as_dictionary = {}
            if self.__attr_date in attributes_to_read:
                user_data_as_dictionary[self.__attr_date] = data_obj.date
            if self.__attr_guests in attributes_to_read:
                user_data_as_dictionary[self.__attr_guests] = data_obj.guests
            if self.__attr_subscribers in attributes_to_read:
                user_data_as_dictionary[self.__attr_subscribers] = data_obj.subscribers
            if self.__attr_store_managers in attributes_to_read:
                user_data_as_dictionary[self.__attr_store_managers] = data_obj.store_managers
            if self.__attr_store_owners in attributes_to_read:
                user_data_as_dictionary[self.__attr_store_owners] = data_obj.store_owners
            if self.__attr_system_managers in attributes_to_read:
                user_data_as_dictionary[self.__attr_system_managers] = data_obj.system_managers
            output_lst.append(user_data_as_dictionary)

        return output_lst

    def write(self, date: datetime = datetime(datetime.now().year, datetime.now().month, datetime.now().day),
              guests: int = 0, subscribers: int = 0, store_managers: int = 0, store_owners: int = 0,
              system_managers: int = 0):
        """
        Write a statistics to db.
        :return: size of user tbl after inserting the new one.
        """
        attributes_as_dictionary = {self.__attributes_as_dictionary[self.__attr_date]: date,
                                    self.__attributes_as_dictionary[self.__attr_guests]: guests,
                                    self.__attributes_as_dictionary[self.__attr_subscribers]: subscribers,
                                    self.__attributes_as_dictionary[self.__attr_store_managers]: store_managers,
                                    self.__attributes_as_dictionary[self.__attr_store_owners]: store_owners,
                                    self.__attributes_as_dictionary[self.__attr_system_managers]: system_managers}

        return (DbProxy.get_instance()).write(self.__tbl, attributes_as_dictionary)

    def update(self, old_date: datetime = None, old_guests: int = None, old_subscribers: int = None,
               old_store_managers: int = None, old_store_owners: int = None, old_system_managers: int = None,
               new_date: datetime = None, new_guests: int = None, new_subscribers: int = None,
               new_store_managers: int = None, new_store_owners: int = None, new_system_managers: int = None):
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
        const_lst = []
        if not (old_date is None):
            const_lst.append(Expression(self.__tbl.date, OP.EQ, old_date))
        if not (old_guests is None):
            const_lst.append(Expression(self.__tbl.guests, OP.EQ, old_guests))
        if not (old_subscribers is None):
            const_lst.append(Expression(self.__tbl.subscribers, OP.EQ, old_subscribers))
        if not (old_store_managers is None):
            const_lst.append(Expression(self.__tbl.store_managers, OP.EQ, old_store_managers))
        if not (old_store_owners is None):
            const_lst.append(Expression(self.__tbl.store_owners, OP.EQ, old_store_owners))
        if not (old_system_managers is None):
            const_lst.append(Expression(self.__tbl.system_managers, OP.EQ, old_system_managers))
        where_expr = and_exprs(const_lst)

        attributes_as_dictionary = {}
        if not (new_date is None):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_date]] = new_date
        if not (new_guests is None):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_guests]] = new_guests
        if not (new_subscribers is None):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_subscribers]] = new_subscribers
        if not (new_store_managers is None):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_store_managers]] = new_store_managers
        if not (new_store_owners is None):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_store_owners]] = new_store_owners
        if not (new_system_managers is None):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_system_managers]] = new_system_managers

        if len(attributes_as_dictionary) == 0:
            raise AttributeError("Nothing to update")

        return DbProxy.get_instance().update(self.__tbl, attributes_as_dictionary, where_expr)

    def delete(self, date: datetime = None, guests: int = None, subscribers: int = None,
               store_managers: int = None, store_owners: int = None, system_managers: int = None):
        """
        Delete statistics from the DB.
        <attribute> will composite a constraint of where to delete.
        example(if old_username != ""), it will composite the constraint-
                                               where(user.username == username).

        :return: the number of deleted rows.
        """
        const_lst = []
        if not (date is None):
            const_lst.append(Expression(self.__tbl.date, OP.EQ, date))
        if not (guests is None):
            const_lst.append(Expression(self.__tbl.guests, OP.EQ, guests))
        if not (subscribers is None):
            const_lst.append(Expression(self.__tbl.subscribers, OP.EQ, subscribers))
        if not (store_managers is None):
            const_lst.append(Expression(self.__tbl.store_managers, OP.EQ, store_managers))
        if not (store_owners is None):
            const_lst.append(Expression(self.__tbl.store_owners, OP.EQ, store_owners))
        if not (system_managers is None):
            const_lst.append(Expression(self.__tbl.system_managers, OP.EQ, system_managers))
        where_expr = and_exprs(const_lst)

        return (DbProxy.get_instance()).delete(self.__tbl, where_expr=where_expr)
