from peewee import Expression, OP
from src.Logger import errorLogger
from src.main.DataAccessLayer.ConnectionProxy.Tables import StoreManagerAppointment
from src.main.DataAccessLayer.ConnectionProxy.DbProxy import DbProxy, and_exprs

"""
Represent the table of store managers appointments.
NOT the domain StoreManagerAppointment.
"""


class StoreManagerAppointmentData:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if StoreManagerAppointmentData.__instance is None:
            StoreManagerAppointmentData()
        return StoreManagerAppointmentData.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if StoreManagerAppointmentData.__instance is not None:
            errorLogger("This class is a singleton!")
            raise Exception("This class is a singleton!")
        else:
            self.__tbl = StoreManagerAppointment
            self.__attr_appointee_username = "appointee_username"
            self.__attr_store_name = "store_name"
            self.__attr_appointer_username = "appointer_username"
            self.__attr_can_edit_inventory = "can_edit_inventory"
            self.__attr_can_edit_policies = "can_edit_policies"
            self.__attr_can_appoint_owner = "can_appoint_owner"
            self.__attr_can_delete_owner = "can_delete_owner"
            self.__attr_can_appoint_manager = "can_appoint_manager"
            self.__attr_can_edit_manager_permissions = "can_edit_manager_permissions"
            self.__attr_can_delete_manager = "can_delete_manager"
            self.__attr_can_close_store = "can_close_store"
            self.__attr_can_answer_user_questions = "can_answer_user_questions"
            self.__attr_can_watch_purchase_history = "can_watch_purchase_history"
            self.__attributes_as_dictionary = {self.__attr_appointee_username: self.__tbl.appointee_username,
                                               self.__attr_store_name: self.__tbl.store_name,
                                               self.__attr_appointer_username: self.__tbl.appointer_username,
                                               self.__attr_can_edit_inventory: self.__tbl.can_edit_inventory,
                                               self.__attr_can_edit_policies: self.__tbl.can_edit_policies,
                                               self.__attr_can_appoint_owner: self.__tbl.can_appoint_owner,
                                               self.__attr_can_delete_owner: self.__tbl.can_delete_owner,
                                               self.__attr_can_appoint_manager: self.__tbl.can_appoint_manager,
                                               self.__attr_can_edit_manager_permissions:
                                                   self.__tbl.can_edit_manager_permissions,
                                               self.__attr_can_delete_manager: self.__tbl.can_delete_manager,
                                               self.__attr_can_close_store: self.__tbl.can_close_store,
                                               self.__attr_can_answer_user_questions:
                                                   self.__tbl.can_answer_user_questions,
                                               self.__attr_can_watch_purchase_history:
                                                   self.__tbl.can_watch_purchase_history}
            StoreManagerAppointmentData.__instance = self

    def read(self, attributes_to_read: [str], appointee_username: str = "", store_name: str = "",
             appointer_username: str = "", can_edit_inventory: bool = None,
             can_edit_policies: bool = None, can_appoint_owner: bool = None, can_delete_owner: bool = None,
             can_appoint_manager: bool = None, can_edit_manager_permissions: bool = None,
             can_delete_manager: bool = None, can_close_store: bool = None,
             can_answer_user_questions: bool = None, can_watch_purchase_history: bool = None):
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
        :param can_edit_inventory:
        :param can_edit_policies:
        :param can_appoint_owner:
        :param can_delete_owner:
        :param can_appoint_manager:
        :param can_edit_manager_permissions:
        :param can_delete_manager:
        :param can_close_store:
        :param can_answer_user_questions:
        :param can_watch_purchase_history:
        :return: dict of the result data.
        """
        if len(attributes_to_read) > 0:
            for attribute in attributes_to_read:
                if attribute.lower() not in self.__attributes_as_dictionary.keys():
                    raise AttributeError("Attribute " + attribute + " doesn't exist in " + str(type(self.__tbl)) + ".")
        else:
            # TODO: Check if work.
            attributes_to_read = self.__attributes_as_dictionary.keys()

        const_lst = []
        if not (appointee_username == ""):
            const_lst.append((Expression(self.__tbl.appointee_username, OP.EQ, appointee_username)))
        if not (store_name == ""):
            const_lst.append(Expression(self.__tbl.store_name, OP.EQ, store_name))
        if not (appointer_username == ""):
            const_lst.append((Expression(self.__tbl.appointer_username, OP.EQ, appointer_username)))
        if not (can_edit_inventory is None):
            const_lst.append((Expression(self.__tbl.can_edit_inventory, OP.EQ, can_edit_inventory)))
        if not (can_edit_policies is None):
            const_lst.append((Expression(self.__tbl.can_edit_policies, OP.EQ, can_edit_policies)))
        if not (can_appoint_owner is None):
            const_lst.append((Expression(self.__tbl.can_appoint_owner, OP.EQ, can_appoint_owner)))
        if not (can_delete_owner is None):
            const_lst.append((Expression(self.__tbl.can_delete_owner, OP.EQ, can_delete_owner)))
        if not (can_appoint_manager is None):
            const_lst.append((Expression(self.__tbl.can_appoint_manager, OP.EQ, can_appoint_manager)))
        if not (can_edit_manager_permissions is None):
            const_lst.append((Expression(self.__tbl.can_edit_manager_permissions, OP.EQ, can_edit_manager_permissions)))
        if not (can_delete_manager is None):
            const_lst.append((Expression(self.__tbl.can_delete_manager, OP.EQ, can_delete_manager)))
        if not (can_close_store is None):
            const_lst.append((Expression(self.__tbl.can_close_store, OP.EQ, can_close_store)))
        if not (can_answer_user_questions is None):
            const_lst.append((Expression(self.__tbl.can_answer_user_questions, OP.EQ, can_answer_user_questions)))
        if not (can_watch_purchase_history is None):
            const_lst.append((Expression(self.__tbl.can_watch_purchase_history, OP.EQ, can_watch_purchase_history)))
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
            if self.__attr_can_edit_inventory in attributes_to_read:
                data_as_dictionary[self.__attr_can_edit_inventory] = data_obj.can_edit_inventory
            if self.__attr_can_edit_policies in attributes_to_read:
                data_as_dictionary[self.__attr_can_edit_policies] = data_obj.can_edit_policies
            if self.__attr_can_appoint_owner in attributes_to_read:
                data_as_dictionary[self.__attr_can_appoint_owner] = data_obj.can_appoint_owner
            if self.__attr_can_delete_owner in attributes_to_read:
                data_as_dictionary[self.__attr_can_delete_owner] = data_obj.can_delete_owner
            if self.__attr_can_appoint_manager in attributes_to_read:
                data_as_dictionary[self.__attr_can_appoint_manager] = data_obj.can_appoint_manager
            if self.__attr_can_edit_manager_permissions in attributes_to_read:
                data_as_dictionary[self.__attr_can_edit_manager_permissions] = data_obj.can_edit_manager_permissions
            if self.__attr_can_delete_manager in attributes_to_read:
                data_as_dictionary[self.__attr_can_delete_manager] = data_obj.can_delete_manager
            if self.__attr_can_close_store in attributes_to_read:
                data_as_dictionary[self.__attr_can_close_store] = data_obj.can_close_store
            if self.__attr_can_answer_user_questions in attributes_to_read:
                data_as_dictionary[self.__attr_can_answer_user_questions] = data_obj.can_answer_user_questions
            if self.__attr_can_watch_purchase_history in attributes_to_read:
                data_as_dictionary[self.__attr_can_watch_purchase_history] = data_obj.can_watch_purchase_history
            output_lst.append(data_as_dictionary)

        return output_lst

    def write(self, appointee_username: str, store_name: str, appointer_username: str, can_edit_inventory: bool = False,
              can_edit_policies: bool = False, can_appoint_owner: bool = False, can_delete_owner: bool = False,
              can_appoint_manager: bool = False, can_edit_manager_permissions: bool = False,
              can_delete_manager: bool = False, can_close_store: bool = False,
              can_answer_user_questions: bool = False, can_watch_purchase_history: bool = False):
        """
        write store manager appointment to db.

        :param appointee_username: pk
        :param store_name:pk
        :param appointer_username:
        :param can_edit_inventory:
        :param can_edit_policies:
        :param can_appoint_owner:
        :param can_delete_owner:
        :param can_appoint_manager:
        :param can_edit_manager_permissions:
        :param can_delete_manager:
        :param can_close_store:
        :param can_answer_user_questions:
        :param can_watch_purchase_history:
        :return:
        """
        attributes_as_dictionary = {self.__attributes_as_dictionary[self.__attr_appointee_username]: appointee_username,
                                    self.__attributes_as_dictionary[self.__attr_store_name]: store_name,
                                    self.__attributes_as_dictionary[self.__attr_appointer_username]: appointer_username,
                                    self.__attributes_as_dictionary[self.__attr_can_edit_inventory]: can_edit_inventory,
                                    self.__attributes_as_dictionary[self.__attr_can_edit_policies]: can_edit_policies,
                                    self.__attributes_as_dictionary[self.__attr_can_appoint_owner]: can_appoint_owner,
                                    self.__attributes_as_dictionary[self.__attr_can_delete_owner]: can_delete_owner,
                                    self.__attributes_as_dictionary[self.__attr_can_appoint_manager]:
                                        can_appoint_manager,
                                    self.__attributes_as_dictionary[self.__attr_can_edit_manager_permissions]:
                                        can_edit_manager_permissions,
                                    self.__attributes_as_dictionary[self.__attr_can_delete_manager]: can_delete_manager,
                                    self.__attributes_as_dictionary[self.__attr_can_close_store]: can_close_store,
                                    self.__attributes_as_dictionary[self.__attr_can_answer_user_questions]:
                                        can_answer_user_questions,
                                    self.__attributes_as_dictionary[self.__attr_can_watch_purchase_history]:
                                        can_watch_purchase_history
                                    }

        return (DbProxy.get_instance()).write(self.__tbl, attributes_as_dictionary)

    def update(self, old_appointee_username: str = "", old_store_name: str = "", old_appointer_username: str = "",
               old_can_edit_inventory: bool = None, old_can_edit_policies: bool = None,
               old_can_appoint_owner: bool = None, old_can_delete_owner: bool = None,
               old_can_appoint_manager: bool = None, old_can_edit_manager_permissions: bool = None,
               old_can_delete_manager: bool = None, old_can_close_store: bool = None,
               old_can_answer_user_questions: bool = None, old_can_watch_purchase_history: bool = None,
               new_appointee_username: str = "", new_store_name: str = "", new_appointer_username: str = "",
               new_can_edit_inventory: bool = None, new_can_edit_policies: bool = None,
               new_can_appoint_owner: bool = None, new_can_delete_owner: bool = None,
               new_can_appoint_manager: bool = None, new_can_edit_manager_permissions: bool = None,
               new_can_delete_manager: bool = None, new_can_close_store: bool = None,
               new_can_answer_user_questions: bool = None, new_can_watch_purchase_history: bool = None
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
        const_lst = []
        if not (old_appointee_username == ""):
            const_lst.append((Expression(self.__tbl.appointee_username, OP.EQ, old_appointee_username)))
        if not (old_store_name == ""):
            const_lst.append(Expression(self.__tbl.store_name, OP.EQ, old_store_name))
        if not (old_appointer_username == ""):
            const_lst.append((Expression(self.__tbl.appointer_username, OP.EQ, old_appointer_username)))
        if not (old_can_edit_inventory is None):
            const_lst.append((Expression(self.__tbl.can_edit_inventory, OP.EQ, old_can_edit_inventory)))
        if not (old_can_edit_policies is None):
            const_lst.append((Expression(self.__tbl.can_edit_policies, OP.EQ, old_can_edit_policies)))
        if not (old_can_appoint_owner is None):
            const_lst.append((Expression(self.__tbl.can_appoint_owner, OP.EQ, old_can_appoint_owner)))
        if not (old_can_delete_owner is None):
            const_lst.append((Expression(self.__tbl.can_delete_owner, OP.EQ, old_can_delete_owner)))
        if not (old_can_appoint_manager is None):
            const_lst.append((Expression(self.__tbl.can_appoint_manager, OP.EQ, old_can_appoint_manager)))
        if not (old_can_edit_manager_permissions is None):
            const_lst.append((Expression(self.__tbl.can_edit_manager_permissions, OP.EQ,
                                         old_can_edit_manager_permissions)))
        if not (old_can_delete_manager is None):
            const_lst.append((Expression(self.__tbl.can_delete_manager, OP.EQ, old_can_delete_manager)))
        if not (old_can_close_store is None):
            const_lst.append((Expression(self.__tbl.can_close_store, OP.EQ, old_can_close_store)))
        if not (old_can_answer_user_questions is None):
            const_lst.append((Expression(self.__tbl.can_answer_user_questions, OP.EQ, old_can_answer_user_questions)))
        if not (old_can_watch_purchase_history is None):
            const_lst.append((Expression(self.__tbl.can_watch_purchase_history, OP.EQ, old_can_watch_purchase_history)))
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
        if not (new_can_edit_inventory is None):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_can_edit_inventory]] = \
                new_can_edit_inventory
        if not (new_can_edit_policies is None):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_can_edit_policies]] = \
                new_can_edit_policies
        if not (new_can_appoint_owner is None):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_can_appoint_owner]] = \
                new_can_appoint_owner
        if not (new_can_delete_owner is None):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_can_delete_owner]] = \
                new_can_delete_owner
        if not (new_can_appoint_manager is None):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_can_appoint_manager]] = \
                new_can_appoint_manager
        if not (new_can_edit_manager_permissions is None):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_can_edit_manager_permissions]] = \
                new_can_edit_manager_permissions
        if not (new_can_delete_manager is None):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_can_delete_manager]] = \
                new_can_delete_manager
        if not (new_can_close_store is None):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_can_close_store]] = \
                new_can_close_store
        if not (new_can_answer_user_questions is None):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_can_answer_user_questions]] = \
                new_can_answer_user_questions
        if not (new_can_watch_purchase_history is None):
            attributes_as_dictionary[self.__attributes_as_dictionary[self.__attr_can_watch_purchase_history]] = \
                new_can_watch_purchase_history
        if len(attributes_as_dictionary) == 0:
            raise AttributeError("Nothing to update")

        return DbProxy.get_instance().update(self.__tbl, attributes_as_dictionary, where_expr)

    def delete(self, appointee_username: str = "", store_name: str = "", appointer_username: str = "",
               can_edit_inventory: bool = None, can_edit_policies: bool = None, can_appoint_owner: bool = None,
               can_delete_owner: bool = None, can_appoint_manager: bool = None,
               can_edit_manager_permissions: bool = None, can_delete_manager: bool = None, can_close_store: bool = None,
               can_answer_user_questions: bool = None, can_watch_purchase_history: bool = None):
        """
        Delete store manager appointments from the DB.
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
        if not (can_edit_inventory is None):
            const_lst.append((Expression(self.__tbl.can_edit_inventory, OP.EQ, can_edit_inventory)))
        if not (can_edit_policies is None):
            const_lst.append((Expression(self.__tbl.can_edit_policies, OP.EQ, can_edit_policies)))
        if not (can_appoint_owner is None):
            const_lst.append((Expression(self.__tbl.can_appoint_owner, OP.EQ, can_appoint_owner)))
        if not (can_delete_owner is None):
            const_lst.append((Expression(self.__tbl.can_delete_owner, OP.EQ, can_delete_owner)))
        if not (can_appoint_manager is None):
            const_lst.append((Expression(self.__tbl.can_appoint_manager, OP.EQ, can_appoint_manager)))
        if not (can_edit_manager_permissions is None):
            const_lst.append((Expression(self.__tbl.can_edit_manager_permissions, OP.EQ, can_edit_manager_permissions)))
        if not (can_delete_manager is None):
            const_lst.append((Expression(self.__tbl.can_delete_manager, OP.EQ, can_delete_manager)))
        if not (can_close_store is None):
            const_lst.append((Expression(self.__tbl.can_close_store, OP.EQ, can_close_store)))
        if not (can_answer_user_questions is None):
            const_lst.append((Expression(self.__tbl.can_answer_user_questions, OP.EQ, can_answer_user_questions)))
        if not (can_watch_purchase_history is None):
            const_lst.append((Expression(self.__tbl.can_watch_purchase_history, OP.EQ, can_watch_purchase_history)))
        where_expr = and_exprs(const_lst)
        return (DbProxy.get_instance()).delete(self.__tbl, where_expr=where_expr)
