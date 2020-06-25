import unittest
from datetime import datetime

from src.main.DataAccessLayer.DataAccessFacade import DataAccessFacade
from src.main.DataAccessLayer.ConnectionProxy.Tables import rel_path
from peewee import IntegrityError
from src.main.DataAccessLayer.ConnectionProxy.Tables import create_tables


class DataAccessFacadeTests(unittest.TestCase):

    def setUp(self) -> None:
        if not ("testing" in rel_path):
            raise ReferenceError("The Data Base is not the testing data base.\n"
                                 "\t\t\t\tPlease go to src.main.DataAccessLayer.ConnectionProxy.RealDb.rel_path\n"
                                 "\t\t\t\t and change rel_path to test_rel_path.\n"
                                 "\t\t\t\tThanks :D")
        self.__today_with_hour = datetime(datetime.now().year, datetime.now().month, datetime.now().day,
                                          datetime.now().hour,
                                          datetime.now().minute)
        self.__today_without_hour = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
        try:
            create_tables()
        except Exception as e:
            # print(e)
            pass
        try:
            DataAccessFacade.get_instance().write_user("Eytan", "Eytan's password", False)
            DataAccessFacade.get_instance().write_user("Anna", "Anna's password", False)
            DataAccessFacade.get_instance().write_user("Lady Anna", "Anna's password", False)
            DataAccessFacade.get_instance().write_user("System manager",
                                                       "not Eytan's password", True)
            DataAccessFacade.get_instance().write_store("Eytan's store", "Eytan")
            DataAccessFacade.get_instance().write_product("Eytan's product",
                                                          "Eytan's store", 12.12,
                                                          "Eytan's", 13, 0)
            DataAccessFacade.get_instance().write_store_manager_appointment(
                "Anna", "Eytan's store",
                "Eytan", ["EDIT_INV", "CLOSE_STORE"])
            (DataAccessFacade.get_instance()).write_products_in_basket("Anna", "Eytan's store",
                                                                       "Eytan's product", 12)
            (DataAccessFacade.get_instance()).write_store_owner_appointment("Lady Anna",
                                                                            "Eytan's store",
                                                                            "Eytan")
            (DataAccessFacade.get_instance()).write_statistic()
            (DataAccessFacade.get_instance()).write_purchase("Anna", "Eytan's store", 12, self.__today_with_hour,
                                                             [{"product_name": "Eytan's product",
                                                               "product_price": 12,
                                                               "amount": 1}])
            (DataAccessFacade.get_instance()).write_products_in_basket("Anna", "Eytan's store",
                                                                       "Eytan's product", 12)
        except IntegrityError:
            pass
        except Exception as e:
            print(e)
            raise ValueError("My error. check set up.")

    def test_read_users(self):
        # Select all
        result = (DataAccessFacade.get_instance()).read_users()['response']
        self.assertListEqual(result,
                             [{'username': "Eytan", 'password': "Eytan's password", 'is_system_manager': False},
                              {'username': "Anna", 'password': "Anna's password", 'is_system_manager': False},
                              {'username': 'Lady Anna', 'password': "Anna's password", 'is_system_manager': False},
                              {'username': "System manager", 'password': "not Eytan's password",
                               'is_system_manager': True}])

        # Select specific columns
        result = (DataAccessFacade.get_instance()).read_users(["username", "password"])['response']
        self.assertListEqual(result,
                             [{'username': "Eytan", 'password': "Eytan's password"},
                              {'username': "Anna", 'password': "Anna's password"},
                              {'username': 'Lady Anna', 'password': "Anna's password"},
                              {'username': "System manager", 'password': "not Eytan's password"}])

        # Select specific user
        result = (DataAccessFacade.get_instance()).read_users(username="Eytan")['response']
        self.assertListEqual(result,
                             [{'username': "Eytan", 'password': "Eytan's password", 'is_system_manager': False}])

        # Select specific columns in specific user
        result = (DataAccessFacade.get_instance()).read_users(['username', 'password'], username="Eytan")['response']
        self.assertListEqual(result,
                             [{'username': "Eytan", 'password': "Eytan's password"}])

        # Select with composite where constraint.
        result = (DataAccessFacade.get_instance()).read_users(username="Eytan", password="Eytan's password")['response']
        self.assertListEqual(result,
                             [{'username': "Eytan", 'password': "Eytan's password", 'is_system_manager': False}])

        # Select result is empty.
        result = (DataAccessFacade.get_instance()).read_users(username="Yarin", password="Yarin's password")['response']
        self.assertListEqual(result, [])

        # Invalid - attributes list contains not attribute key
        result = (DataAccessFacade.get_instance()).read_users(['username3', 'password'], username="Eytan")['response']
        self.assertFalse(result)

    def test_write_user(self):
        # Insert 1 with default is_sys_man
        result = (DataAccessFacade.get_instance()).write_user("Yarin", "Yarin's password")['response']
        self.assertTrue(result)
        self.assertGreater(
            len((DataAccessFacade.get_instance()).read_users([], "Yarin", "Yarin's password")['response']), 0)

        # Insert 1 with is_sys_man
        result = (DataAccessFacade.get_instance()).write_user("Yarin2", "Yarin's password", True)['response']
        self.assertTrue(result)
        self.assertGreater(
            len((DataAccessFacade.get_instance()).read_users([], "Yarin2", "Yarin's password")['response']), 0)

        # Invalid - pk already exist
        result = (DataAccessFacade.get_instance()).write_user("Yarin", "Eytan")['response']
        self.assertFalse(result)

    def test_update_users(self):
        # update specific user password
        result = (DataAccessFacade.get_instance()).update_users(old_username="Eytan",
                                                                new_password="new password")['response']
        self.assertTrue(result)
        self.assertGreater(len((DataAccessFacade.get_instance()).read_users([], username="Eytan",
                                                                            password="new password")['response']), 0)

        # update all users password
        result = (DataAccessFacade.get_instance()).update_users(new_password="system password")['response']
        self.assertTrue(result)
        self.assertGreater(
            len((DataAccessFacade.get_instance()).read_users([], password="system password")['response']), 0)

        # not pk constraint
        result = \
            (DataAccessFacade.get_instance()).update_users(old_is_system_manager=True, new_is_system_manager=False)[
                'response']
        self.assertTrue(result)
        self.assertGreaterEqual(
            len((DataAccessFacade.get_instance()).read_users([], is_system_manager=False)['response']), 2)

        # composite constraint
        result = (DataAccessFacade.get_instance()).update_users(old_is_system_manager=False,
                                                                old_username="Eytan",
                                                                new_is_system_manager=True)['response']
        self.assertTrue(result)
        self.assertGreaterEqual(
            len((DataAccessFacade.get_instance()).read_users([], is_system_manager=False)['response']), 1)

        # Invalid: nothing to update
        result = (DataAccessFacade.get_instance()).update_users()['response']
        self.assertFalse(result)

    def test_delete_users(self):
        # delete specific user
        result = (DataAccessFacade.get_instance()).delete_users(username="Eytan")['response']
        self.assertTrue(result)

        # insert new user
        (DataAccessFacade.get_instance()).write_user("Yarin2", "Yarin's password", True)

        # delete several users
        result = (DataAccessFacade.get_instance()).delete_users(is_system_manager=True)['response']
        self.assertTrue(result)

        # insert new users
        (DataAccessFacade.get_instance()).write_user("Yarin", "Yarin's password", True)
        (DataAccessFacade.get_instance()).write_user("Yarin2", "Yarin's password", False)

        # composite constraint
        result = (DataAccessFacade.get_instance()).delete_users(password="Yarin's password", is_system_manager=False)
        self.assertTrue(result)

    def test_write_store(self):
        result = (DataAccessFacade.get_instance()).write_store("not Eytan's store", "Eytan")['response']
        self.assertTrue(result)
        self.assertGreater(len((DataAccessFacade.get_instance()).read_stores([], store_name="not Eytan's store",
                                                                             founder_username="Eytan")['response']), 0)
        result = (DataAccessFacade.get_instance()).write_store("Anna's store", "not Anna")['response']
        self.assertFalse(result)

    def test_read_stores(self):
        (DataAccessFacade.get_instance()).write_store("not Eytan's store", "Eytan")

        result = (DataAccessFacade.get_instance()).read_stores([], founder_username="Eytan")['response']
        new_result = [(e['store_name'], e['founder_username']) for e in result]
        self.assertListEqual([("Eytan's store", "Eytan"),
                              ("not Eytan's store", "Eytan")], new_result)

        result = (DataAccessFacade.get_instance()).read_stores(["store_name"], founder_username="Eytan")['response']
        self.assertListEqual([{"store_name": "Eytan's store"},
                              {"store_name": "not Eytan's store"}], result)

        result = (DataAccessFacade.get_instance()).read_stores(["storename"], founder_username="Eytan")['response']
        self.assertFalse(result)

    def test_update_stores(self):
        # update
        result = \
            (DataAccessFacade.get_instance()).update_stores("Eytan's store", new_founder_username="System manager")[
                'response']
        self.assertEqual(1, result)
        post_cond_result = [(e['store_name'], e['founder_username']) for e in
                            (DataAccessFacade.get_instance()).read_stores([], store_name="Eytan's store")['response']]
        self.assertListEqual([("Eytan's store", "System manager")], post_cond_result)

        result = (DataAccessFacade.get_instance()).update_stores()['response']
        self.assertFalse(result)

    def test_delete_stores(self):
        (DataAccessFacade.get_instance()).write_store("not Eytan's store", "Eytan")

        # valid
        result = (DataAccessFacade.get_instance()).delete_stores("not Eytan's store")['response']
        self.assertTrue(result)
        self.assertListEqual([], (DataAccessFacade.get_instance()).read_stores([], "not Eytan's store")['response'])

        # delete nothing
        result = (DataAccessFacade.get_instance()).delete_stores("not Eytan's store")['response']
        self.assertTrue(result)

    def test_write_product(self):
        # valid
        result = DataAccessFacade.get_instance().write_product("not Eytan's product",
                                                               "Eytan's store", 12.12,
                                                               "not Eytan's", 12, 0)['response']
        self.assertTrue(result)
        lst = (DataAccessFacade.get_instance()).read_products([], "not Eytan's product")['response']
        self.assertEqual(len(lst), 1)

        # invalid
        result = DataAccessFacade.get_instance().write_product("not Eytan's product",
                                                               "Eytan's store", 12.12,
                                                               "not Eytan's", 12, 0)['response']
        self.assertFalse(result)
        self.assertEqual(len((DataAccessFacade.get_instance()).read_products([], "not Eytan's product")['response']), 1)

    def test_read_products(self):
        result_lst = (DataAccessFacade.get_instance()).read_products([], "Eytan's product")['response']
        res = [(result['product_name'], result['store_name'], result['price'], result['category'],
                result['amount'], result['purchase_type']) for result in result_lst]
        for r in res:
            self.assertEqual(("Eytan's product", "Eytan's store", 12.12, "Eytan's", 12, 0), r)

        result = (DataAccessFacade.get_instance()).read_products(["product_name"], "Eytan's product")['response']
        for i in result:
            self.assertEqual(i['product_name'], "Eytan's product")

        result = (DataAccessFacade.get_instance()).read_products(["product_ame"], "Eytan's product")['response']
        self.assertEqual([], result)

    def test_update_products(self):
        result = (DataAccessFacade.get_instance()).update_products(new_amount=20)['response']
        self.assertTrue(result)
        self.assertListEqual((DataAccessFacade.get_instance()).read_products(['amount'])['response'], [{'amount': 20}])

        result = (DataAccessFacade.get_instance()).update_products(old_store_name="Eytan's store",
                                                                   old_product_name="Eytan's product",
                                                                   new_amount=11)['response']
        self.assertTrue(result)
        self.assertListEqual((DataAccessFacade.get_instance()).read_products(['amount'])['response'], [{'amount': 11}])

        result = (DataAccessFacade.get_instance()).update_products(old_amount=20, new_amount=13)['response']
        self.assertTrue(result)
        self.assertListEqual((DataAccessFacade.get_instance()).read_products(['amount'], amount=13)['response'], [])

        result = (DataAccessFacade.get_instance()).update_products(old_amount=20)['response']
        self.assertFalse(result)

    def test_delete_products(self):
        DataAccessFacade.get_instance().write_product("not Eytan's product",
                                                      "Eytan's store", 12.12,
                                                      "not Eytan's", 12, 0)

        # valid
        result = (DataAccessFacade.get_instance()).delete_products(product_name="not Eytan's product")['response']
        self.assertTrue(result)
        self.assertListEqual([], (DataAccessFacade.get_instance()).read_products([], "not Eytan's product")['response'])

        # invalid - nothing to delete
        result = (DataAccessFacade.get_instance()).delete_products(product_name="not Eytan's product")['response']
        self.assertTrue(result)
        self.assertListEqual([], (DataAccessFacade.get_instance()).read_products([], "not Eytan's product")['response'])

    def test_write_store_manager_appointment(self):
        (DataAccessFacade.get_instance()).write_user("Boss Anna", "password")
        result = DataAccessFacade.get_instance().write_store_manager_appointment(
            "Boss Anna", "Eytan's store",
            "Eytan", ["EDIT_INV", "CLOSE_STORE"])['response']
        self.assertTrue(result)
        managers = [man['appointee_username'] for man in
                    (DataAccessFacade.get_instance()).read_store_manager_appointments(["appointee_username"],
                                                                                      appointee_username=
                                                                                      "Boss Anna")['response']]
        self.assertListEqual(["Boss Anna"], managers)

        # invalid
        result = DataAccessFacade.get_instance().write_store_manager_appointment(
            "Boss Anna", "Eytan's store",
            "Anna", ["EDIT_INV", "CLOSE_STORE"])['response']
        self.assertFalse(result)

    def test_read_store_manager_appointments(self):
        result_dic = (DataAccessFacade.get_instance()).read_store_manager_appointments(["appointee_username",
                                                                                        "store_name",
                                                                                        "appointer_username"],
                                                                                       ["EDIT_INV", "DEL_OWNER"]) \
            ['response']
        result_tup = [(sma['appointee_username'], sma['store_name'],
                       sma['appointer_username'], sma['can_edit_inventory'], sma['can_delete_owner'])
                      for sma in result_dic]
        self.assertListEqual(result_tup, [('Anna', "Eytan's store", 'Eytan', True, False)])

        result_dic = (DataAccessFacade.get_instance()).read_store_manager_appointments(["appointee_username",
                                                                                        "store_name",
                                                                                        "appointer_username"],
                                                                                       ["EDIT_INV", "DEL_OWNER"],
                                                                                       appointee_username="Anna") \
            ['response']
        result_tup = [(sma['appointee_username'], sma['store_name'],
                       sma['appointer_username'], sma['can_edit_inventory'], sma['can_delete_owner'])
                      for sma in result_dic]
        self.assertListEqual(result_tup, [('Anna', "Eytan's store", 'Eytan', True, False)])

    def test_update_store_manager_appointments(self):
        result = (DataAccessFacade.get_instance()).update_store_manager_appointments(old_appointee_username="Anna",
                                                                                     new_permissions_lst=["EDIT_INV",
                                                                                                          "DEL_OWNER",
                                                                                                          "WATCH_PURCHASE_HISTORY"]
                                                                                     )['response']
        self.assertTrue(result)
        self.assertEqual(len((DataAccessFacade.get_instance()).read_store_manager_appointments([], [],
                                                                                               permissions_lst= \
                                                                                                   [
                                                                                                       "WATCH_PURCHASE_HISTORY"])
                             ['response']), 1)

        result = (DataAccessFacade.get_instance()).update_store_manager_appointments(old_appointee_username="Anna"
                                                                                     )['response']
        self.assertFalse(result)

    def test_delete_store_manager_appointments(self):
        (DataAccessFacade.get_instance()).write_user("Boss Anna", "password")
        DataAccessFacade.get_instance().write_store_manager_appointment(
            "Boss Anna", "Eytan's store",
            "Eytan", ["EDIT_INV", "WATCH_PURCHASE_HISTORY"])

        # valid
        result = (DataAccessFacade.get_instance()).delete_store_manager_appointments(permissions_lst=
                                                                                     ["EDIT_INV",
                                                                                      "WATCH_PURCHASE_HISTORY"]) \
            ['response']
        self.assertTrue(result)
        self.assertListEqual([], (DataAccessFacade.get_instance()).read_store_manager_appointments([],
                                                                                                   [],
                                                                                                   "Boss Anna") \
            ['response'])

        # nothing to delete
        result = (DataAccessFacade.get_instance()).delete_store_manager_appointments(permissions_lst=
                                                                                     ["EDIT_INV",
                                                                                      "WATCH_PURCHASE_HISTORY"]) \
            ['response']
        self.assertTrue(result)
        self.assertListEqual([], (DataAccessFacade.get_instance()).read_store_manager_appointments([],
                                                                                                   [],
                                                                                                   "Boss Anna") \
            ['response'])

    def test_write_products_in_basket(self):
        result = (DataAccessFacade.get_instance()).write_products_in_basket("Eytan", "Eytan's store",
                                                                            "Eytan's product", 12)['response']
        self.assertTrue(result)
        self.assertGreater(len((DataAccessFacade.get_instance()).read_products_in_baskets([], "Eytan",
                                                                                          product_name=
                                                                                          "Eytan's product")[
                                   'response']), 0)

        result = (DataAccessFacade.get_instance()).write_products_in_basket("Eytan", "Eytan's store",
                                                                            "Eytan's product", 12)['response']
        self.assertFalse(result)
        self.assertEqual(len((DataAccessFacade.get_instance()).read_products_in_baskets([], "Eytan",
                                                                                        product_name=
                                                                                        "Eytan's product")[
                                 'response']), 1)

        result = (DataAccessFacade.get_instance()).write_products_in_basket("Eytan", "Eytan's store",
                                                                            "Eytans product", 12)['response']
        self.assertFalse(result)
        self.assertEqual(len((DataAccessFacade.get_instance()).read_products_in_baskets([], "Eytan",
                                                                                        product_name=
                                                                                        "Eytans product")[
                                 'response']), 0)

    def test_read_products_in_baskets(self):
        (DataAccessFacade.get_instance()).write_products_in_basket("Eytan", "Eytan's store",
                                                                   "Eytan's product", 12)
        result = (DataAccessFacade.get_instance()).read_products_in_baskets([], "Eytan",
                                                                            product_name=
                                                                            "Eytan's product")['response']
        self.assertEqual(result[0], {'username': 'Eytan', 'store_name': "Eytan's store", 'product_name':
            "Eytan's product", 'amount': 12})
        result = (DataAccessFacade.get_instance()).read_products_in_baskets([], "Eytan",
                                                                            product_name=
                                                                            "Eytans product")[
            'response']
        self.assertListEqual([], result)

    def test_update_products_in_baskets(self):
        result = (DataAccessFacade.get_instance()).update_products_in_baskets(old_username="Anna",
                                                                              new_username="Eytan")['response']
        self.assertTrue(result)
        self.assertGreater(len((DataAccessFacade.get_instance()).read_products_in_baskets([],
                                                                                          username="Eytan")[
                                   'response']), 0)

        result = (DataAccessFacade.get_instance()).update_products_in_baskets(old_username="Eytan")['response']
        self.assertFalse(result)

    def test_delete_products_in_baskets(self):
        result = (DataAccessFacade.get_instance()).delete_products_in_baskets(username="Anna")['response']
        self.assertTrue(result)
        self.assertEqual(len((DataAccessFacade.get_instance()).read_products_in_baskets([], username="Anna")
                             ['response']), 0)

        result = (DataAccessFacade.get_instance()).delete_products_in_baskets(username="Anna")['response']
        self.assertTrue(result)

    def test_write_store_owner_appointment(self):
        result = (DataAccessFacade.get_instance()).write_store_owner_appointment("Anna", "Eytan's store", "Eytan")
        self.assertTrue(result)
        self.assertGreater(len((DataAccessFacade.get_instance()).read_store_owner_appointments([],
                                                                                               appointee_username="Anna"
                                                                                               )
                               ['response']), 0)

        result = (DataAccessFacade.get_instance()).write_store_owner_appointment("Anna", "Eytan's store", "Eytan")[
            'response']
        self.assertFalse(result)

    def test_read_store_owner_appointments(self):
        result_dic = (DataAccessFacade.get_instance()).read_store_owner_appointments(["appointee_username",
                                                                                      "store_name",
                                                                                      "appointer_username"]) \
            ['response']
        result_tup = [(soa['appointee_username'], soa['store_name'],
                       soa['appointer_username'])
                      for soa in result_dic]
        self.assertListEqual(result_tup, [('Lady Anna', "Eytan's store", 'Eytan')])

        result_dic = (DataAccessFacade.get_instance()).read_store_owner_appointments(["appointee_username",
                                                                                      "store_name",
                                                                                      "appointer_username"],
                                                                                     appointee_username="Lady Anna") \
            ['response']
        result_tup = [(soa['appointee_username'], soa['store_name'],
                       soa['appointer_username'])
                      for soa in result_dic]
        self.assertListEqual(result_tup, [('Lady Anna', "Eytan's store", 'Eytan')])

    def test_update_store_owner_appointments(self):
        result = (DataAccessFacade.get_instance()).update_store_owner_appointments(old_appointee_username="Lady Anna",
                                                                                   new_appointee_username="Anna") \
            ['response']
        self.assertTrue(result)
        self.assertEqual(len((DataAccessFacade.get_instance()).read_store_owner_appointments(appointee_username="Anna")
                             ['response']), 1)

        result = (DataAccessFacade.get_instance()).update_store_owner_appointments(old_appointee_username="Anna"
                                                                                   )['response']
        self.assertFalse(result)

    def test_delete_store_owner_appointments(self):
        (DataAccessFacade.get_instance()).write_user("Boss Anna", "password")
        DataAccessFacade.get_instance().write_store_owner_appointment(
            "Boss Anna", "Eytan's store",
            "Eytan")

        # valid
        result = (DataAccessFacade.get_instance()).delete_store_owner_appointments(appointee_username="Boss Anna") \
            ['response']
        self.assertTrue(result)
        self.assertListEqual([], (DataAccessFacade.get_instance()).read_store_owner_appointments([], "Boss Anna") \
            ['response'])

        # nothing to delete
        result = (DataAccessFacade.get_instance()).delete_store_owner_appointments(appointee_username="Boss Anna") \
            ['response']
        self.assertTrue(result)

    def test_write_statistic(self):
        result = (DataAccessFacade.get_instance()).write_statistic(datetime(2020, 12, 12), 1, 2, 3, 4, 5)
        self.assertTrue(result)
        self.assertGreater(len((DataAccessFacade.get_instance()).read_statistics([], guests=1)['response']), 0)

        result = DataAccessFacade.get_instance().write_statistic()['response']
        self.assertFalse(result)

    def test_read_statistics(self):
        result = (DataAccessFacade.get_instance()).read_statistics([], date=self.__today_without_hour)['response']
        self.assertListEqual([{'date': datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0),
                               'guests': 0, 'subscribers': 0, 'store_managers': 0, 'owners': 0, 'system_managers': 0}],
                             result)

        # Nothing to read
        result = (DataAccessFacade.get_instance()).read_statistics([], date=datetime(1212,
                                                                                     datetime.now().month,
                                                                                     datetime.now().day))['response']
        self.assertListEqual([], result)

    def test_update_statistics(self):
        result = (DataAccessFacade.get_instance()).update_statistics(old_date=self.__today_without_hour, new_guests=3)[
            'response']
        self.assertTrue(result)
        self.assertGreater(len((DataAccessFacade.get_instance()).read_statistics([], guests=3)['response']), 0)

        result = (DataAccessFacade.get_instance()).update_statistics(old_date=self.__today_without_hour)['response']
        self.assertFalse(result)

    def test_delete_statistics(self):
        result = (DataAccessFacade.get_instance()).delete_statistics(date=self.__today_without_hour)['response']
        self.assertTrue(result)
        self.assertEqual(len((DataAccessFacade.get_instance()).read_statistics([], date=self.__today_without_hour)
                             ['response']), 0)

        # Nothing to delete
        result = (DataAccessFacade.get_instance()).delete_statistics(date=self.__today_without_hour)['response']
        self.assertTrue(result)

    # def test_write_discount_policy(self):
    #     (DataAccessFacade.get_instance()).write_discount_policy("p1", "Eytan's store",
    #                                                             "Eytan's product", 12, self.__today)
    #     (DataAccessFacade.get_instance()).write_discount_policy("p2", "Eytan's store",
    #                                                             "Eytan's product", 12, self.__today)
    #     result = (DataAccessFacade.get_instance()).write_discount_policy("Eytan's policy", "Eytan's store",
    #                                                                      "Eytan's product", 12, self.__today,
    #                                                                      precondition_product="all")['response']
    #     self.assertTrue(result)
    #     self.assertGreaterEqual(
    #         len((DataAccessFacade.get_instance()).read_discount_policies([], valid_until=self.__today)[
    #                 'response']), 3)
    #
    #     result = (DataAccessFacade.get_instance()).write_discount_policy("Eytan's Composite policy", "Eytan's store",
    #                                                                      "Eytan's product", 12, self.__today,
    #                                                                      policy1_name="p1", policy2_name="p2",
    #                                                                      flag=1)['response']
    #     self.assertTrue(result)
    #     self.assertGreaterEqual(
    #         len((DataAccessFacade.get_instance()).read_discount_policies([], valid_until=self.__today)[
    #                 'response']), 4)
    #
    # def test_read_discount_policies(self):
    #     self.assertTrue(False)
    #
    # def test_update_discount_policies(self):
    #     self.assertTrue(False)
    #
    # def test_delete_discount_policies(self):
    #     self.assertTrue(False)
    def test_write_purchase(self):
        result = (DataAccessFacade.get_instance()).write_purchase("Lady Anna", "Eytan's store", 12,
                                                                  self.__today_with_hour,
                                                                  [{"product_name": "Eytan's product",
                                                                    "product_price": 12,
                                                                    "amount": 1}])
        self.assertTrue(result['response'])
        x = (DataAccessFacade.get_instance()).read_purchases(username="Anna")['response']
        self.assertGreater(len(x), 0)

        result = (DataAccessFacade.get_instance()).write_purchase("Anna", "Eytan's store", 240, self.__today_with_hour,
                                                                  [{"product_name": "Eytan's product",
                                                                    "product_price": 12,
                                                                    "amount": 20}])
        self.assertFalse(result['response'])

    def test_read_purchases(self):
        result = (DataAccessFacade.get_instance()).read_purchases([], username="Anna", product_amount=1)['response']
        self.assertListEqual([{'username': 'Anna', 'store_name': "Eytan's store", 'total_price': 12.0,
                               'date': self.__today_with_hour, 'products_lst': [{'purchase_id': "Eytan's product",
                                                                                 'product_purchase_price': 12.0,
                                                                                 'amount': 1}]}],
                             result)

        # invalid - nothing to read
        result = (DataAccessFacade.get_instance()).read_purchases([], username="Eytan", product_amount=1)['response']
        self.assertListEqual([], result)

    def test_delete_purchases(self):
        (DataAccessFacade.get_instance()).write_purchase("Lady Anna", "Eytan's store", 12,
                                                         self.__today_with_hour,
                                                         [{"product_name": "Eytan's product",
                                                           "product_price": 12,
                                                           "amount": 1}])
        result = (DataAccessFacade.get_instance()).delete_purchases(username="Lady Anna",
                                                                    product_name="Eytan's product")
        self.assertTrue(result)
        self.assertEqual(len((DataAccessFacade.get_instance()).read_purchases([], username="Lady Anna",
                                                                              product_name="Eytan's product")[
                                 'response']), 0)
        self.assertGreaterEqual(len((DataAccessFacade.get_instance()).read_purchases([],
                                                                                     product_name="Eytan's product")[
                                        'response']), 1)

    def test_update_purchases(self):
        result = (DataAccessFacade.get_instance()).update_purchases(old_product_name="Eytan's product",
                                                                    new_username="Eytan")['response']
        self.assertTrue(result)
        self.assertGreater(len((DataAccessFacade.get_instance()).read_purchases([], username="Eytan")[
                               'response']), 0)

        result = (DataAccessFacade.get_instance()).update_purchases(old_username="Anna")['response']
        self.assertFalse(result)

    def tearDown(self) -> None:
        (DataAccessFacade.get_instance()).delete_purchases()
        # (DataAccessFacade.get_instance()).delete_discount_policies()
        (DataAccessFacade.get_instance()).delete_statistics()
        (DataAccessFacade.get_instance()).delete_store_owner_appointments()
        (DataAccessFacade.get_instance()).delete_products_in_baskets()
        (DataAccessFacade.get_instance()).delete_products()
        (DataAccessFacade.get_instance()).delete_store_manager_appointments()
        (DataAccessFacade.get_instance()).delete_stores()
        (DataAccessFacade.get_instance()).delete_users()


if __name__ == '__main__':
    # DataAccessFacadeTests.tearDown()
    unittest.main()
