import unittest

from src.main.DataAccessLayer.ConnectionProxy.Tables import rel_path
from src.main.DataAccessLayer.DataAccessFacade import DataAccessFacade
from src.main.DomainLayer.StoreComponent.AppointmentStatus import AppointmentStatus
from src.main.DomainLayer.StoreComponent.ManagerPermission import ManagerPermission
from src.main.DomainLayer.StoreComponent.PurchasePolicyComposite.PurchasePolicy import PurchasePolicy
from src.main.DomainLayer.StoreComponent.Store import Store
from src.main.DomainLayer.TradeComponent.TradeControl import TradeControl
from src.main.DomainLayer.UserComponent.User import User
from src.test.WhiteBoxTests.UnitTests.Stubs.StubUser import StubUser
from unittest.mock import MagicMock


class TradeControlTestCase(unittest.TestCase):
    def setUp(self):
        if not ("testing" in rel_path):
            raise ReferenceError("The Data Base is not the testing data base.\n"
                                 "\t\t\t\tPlease go to src.main.DataAccessLayer.ConnectionProxy.RealDb.rel_path\n"
                                 "\t\t\t\t and change rel_path to test_rel_path.\n"
                                 "\t\t\t\tThanks :D")
        self.tradeControl = TradeControl.get_instance()
        self.user = StubUser()
        self.user.set_password_and_nickname("nickname", "password")
        self.purchase_policy_mock = PurchasePolicy()

    def test_add_sys_manager_success_and_fail(self):
        managers_num = len(self.tradeControl.get_managers())
        self.assertTrue(self.tradeControl.add_system_manager("nickname", "password")['response'])
        self.assertFalse(self.tradeControl.add_system_manager("nickname", "password")['response'])
        self.assertEqual(len(self.tradeControl.get_managers()), managers_num + 1)

    def test_register_guest(self):
        self.assertTrue(self.tradeControl.register_guest("eden", "passwoed")['response'])
        self.assertFalse(self.tradeControl.register_guest("eden", "passwoed")['response'])

    def test_login_guest(self):
        self.assertFalse(self.tradeControl.login_subscriber("eden", "passwoed")['response'])
        self.assertTrue(self.tradeControl.register_guest("eden", "passwoed")['response'])
        self.assertTrue(self.tradeControl.login_subscriber("eden", "passwoed")['response'])
        self.assertFalse(self.tradeControl.login_subscriber("eden", "passwoed")['response'])

    def test_subscribe_success_and_fail(self):
        subscribers_num = len(self.tradeControl.get_subscribers())
        self.assertTrue(self.tradeControl.subscribe(self.user))
        self.assertFalse(self.tradeControl.subscribe(self.user))
        self.assertEqual(len(self.tradeControl.get_subscribers()), subscribers_num + 1)
        self.assertTrue(self.tradeControl.get_subscriber(self.user.get_nickname()))
        self.tradeControl.unsubscribe(self.user)

    def test_unsubscribe_success_and_fail(self):
        self.tradeControl.subscribe(self.user)
        subscribers_num = len(self.tradeControl.get_subscribers())
        self.assertTrue(self.tradeControl.unsubscribe("nickname"))
        self.assertFalse(self.tradeControl.unsubscribe("nickname"))
        self.assertEqual(len(self.tradeControl.get_subscribers()), subscribers_num - 1)

    def test_close_and_open_store(self):
        stores_num = len(self.tradeControl.get_stores())
        self.tradeControl.set_curr_user(self.user)
        self.assertFalse(self.tradeControl.open_store("myFirstStore")['response'])
        self.user.register("name", "213456")
        self.assertFalse(self.tradeControl.open_store("myFirstStore")['response'])
        self.user.login("name", "213456")
        self.assertTrue(self.tradeControl.open_store("myFirstStore")['response'])
        self.assertEqual(len(self.tradeControl.get_stores()), stores_num + 1)
        self.assertTrue(self.tradeControl.close_store("myFirstStore"))
        self.assertFalse(self.tradeControl.close_store("myFirstStore"))
        self.assertEqual(len(self.tradeControl.get_stores()), stores_num)

    def test_validate_nickname(self):
        self.assertTrue(self.tradeControl.validate_nickname("nickname"))
        self.tradeControl.subscribe(self.user)
        self.assertFalse(self.tradeControl.validate_nickname("nickname"))
        self.tradeControl.unsubscribe("nickname")

    def test_get_subscriber(self):
        self.assertEqual(self.tradeControl.get_subscriber("nickname"), None)
        self.tradeControl.subscribe(self.user)
        self.assertEqual(self.tradeControl.get_subscriber("nickname"), self.user)
        self.tradeControl.unsubscribe("nickname")

    def test_get_products_by(self):
        self.user.register("eden", "213456")
        self.user.login("eden", "213456")
        self.tradeControl.set_curr_user(self.user)
        self.tradeControl.open_store("myStore")
        self.tradeControl.open_store("myStore2")
        store1 = self.tradeControl.get_store("myStore")
        store2: Store = self.tradeControl.get_store("myStore2")
        store1.add_products("eden", [{"name": "Chair", "price": 100, "category": "Furniture", "amount": 5, "purchase_type": 0},
                                     {"name": "Sofa", "price": 100, "category": "Furniture", "amount": 5, "purchase_type": 0}])
        store2.add_products("eden", [{"name": "TV", "price": 100, "category": "Electric", "amount": 5, "purchase_type": 0},
                                     {"name": "Sofa", "price": 100, "category": "Furniture", "amount": 5, "purchase_type": 0}])
        ls = self.tradeControl.get_products_by(1, "Sofa")['response']
        self.assertEqual(len(ls), 2)
        ls = self.tradeControl.get_products_by(2, "o")['response']
        self.assertEqual(len(ls), 2)
        ls = self.tradeControl.get_products_by(2, "a")['response']
        self.assertEqual(len(ls), 3)
        ls = self.tradeControl.get_products_by(3, "Furniture")['response']
        self.assertEqual(len(ls), 3)
        self.tradeControl.close_store("myStore")
        self.tradeControl.close_store("myStore2")

    def test_logout_subscriber(self):
        self.assertFalse(self.tradeControl.logout_subscriber()['response'])
        self.assertTrue(self.tradeControl.register_guest("eden", "passwoed")['response'])
        self.assertTrue(self.tradeControl.login_subscriber("eden", "passwoed")['response'])
        self.assertTrue(self.tradeControl.logout_subscriber())

    def test_add_and_remove_products(self):
        self.user.register("eden", "213456")
        self.user.login("eden", "213456")
        self.tradeControl.set_curr_user(self.user)
        self.tradeControl.open_store("myStore")
        self.tradeControl.open_store("myStore2")
        store1 = self.tradeControl.get_store("myStore")
        self.assertFalse(self.tradeControl.add_products("Store", [
            {"name": "Chair", "price": 100, "category": "Furniture", "amount": 5, "purchase_type": 0},
            {"name": "Sofa", "price": 100, "category": "Furniture", "amount": 5, "purchase_type": 0}])['response'])
        self.assertTrue(self.tradeControl.add_products("myStore", [
            {"name": "Chair", "price": 100, "category": "Furniture", "amount": 5, "purchase_type": 0},
            {"name": "Sofa", "price": 100, "category": "Furniture", "amount": 5, "purchase_type": 0}])['response'])
        self.assertNotEqual(store1.get_product("Chair"), None)
        self.assertNotEqual(store1.get_product("Sofa"), None)
        self.assertTrue(self.tradeControl.remove_products("myStore", ["Sofa"]))
        self.assertNotEqual(store1.get_product("Chair"), None)
        self.assertEqual(store1.get_product("Sofa"), None)

    def test_edit_product(self):
        self.user.register("eden", "213456")
        self.user.login("eden", "213456")
        self.tradeControl.set_curr_user(self.user)
        self.tradeControl.open_store("myStore")
        store1 = self.tradeControl.get_store("myStore")
        self.tradeControl.add_products("myStore", [
            {"name": "Chair", "price": 100, "category": "Furniture", "amount": 5, "purchase_type": 0},
            {"name": "Sofa", "price": 100, "category": "Furniture", "amount": 5, "purchase_type": 0}])

        self.assertTrue(self.tradeControl.edit_product("myStore", "Chair", "price", 155)['response'])
        self.assertEqual(155, store1.get_product("Chair").get_price())
        self.assertEqual("Chair", store1.get_product("Chair").get_name())

        self.assertTrue(self.tradeControl.edit_product("myStore", "Chair", "name", "ch")['response'])
        self.assertEqual("ch", store1.get_product("ch").get_name())
        self.assertEqual(155, store1.get_product("ch").get_price())

        self.assertFalse(self.tradeControl.edit_product("myStore", "blaa", "name", "ch")['response'])
        self.tradeControl.close_store("myStore")

    def test_appoint_additional_owner(self):
        self.user.register("eden", "213456")
        self.user.login("eden", "213456")
        self.tradeControl.register_guest("appointee", "213456")
        self.tradeControl.set_curr_user(self.user)
        self.tradeControl.open_store("myStore")
        store1 = self.tradeControl.get_store("myStore")
        self.assertTrue(self.tradeControl.appoint_additional_owner("appointee", "myStore")['response'])
        self.assertFalse(self.tradeControl.appoint_additional_owner("a", "myStore")['response'])
        self.assertTrue(store1.is_owner("appointee"))
        self.assertFalse(store1.is_owner("a"))

    def test_update_agreement_participants(self):
        self.curr_user = User()
        self.curr_user.get_nickname = MagicMock(return_value="nickname")
        self.tradeControl.set_curr_user(self.curr_user)

        self.store_mock = Store("store")
        self.store_mock.update_agreement_participants = MagicMock(return_value=True)
        self.tradeControl.get_store = MagicMock(return_value=self.store_mock)
        res = self.tradeControl.update_agreement_participants("appointee", "store", AppointmentStatus.APPROVED)
        self.assertTrue(res["response"])

        self.store_mock.update_agreement_participants = MagicMock(return_value=False)
        self.tradeControl.get_store = MagicMock(return_value=self.store_mock)
        res = self.tradeControl.update_agreement_participants("appointee", "store", AppointmentStatus.APPROVED)
        self.assertFalse(res["response"])

    def test_get_appointment_status(self):
        self.store_mock = Store("store")
        self.store_mock.get_appointment_status = MagicMock(return_value=AppointmentStatus.APPROVED)
        self.tradeControl.get_store = MagicMock(return_value=self.store_mock)
        res = self.tradeControl.get_appointment_status("appointee", "store")
        self.assertEqual(res, AppointmentStatus.APPROVED)

        self.store_mock.get_appointment_status = MagicMock(return_value=AppointmentStatus.DECLINED)
        self.tradeControl.get_store = MagicMock(return_value=self.store_mock)
        res = self.tradeControl.get_appointment_status("appointee", "store")
        self.assertEqual(res, AppointmentStatus.DECLINED)

    def test_remove_owner(self):
        owner1 = StubUser()
        owner1.register("owner1", "password")
        owner1.login("owner1", "password")
        self.tradeControl.set_curr_user(owner1)
        self.tradeControl.open_store("myStore")
        self.tradeControl.register_guest("manager1", "213456")
        self.tradeControl.appoint_store_manager("manager1", "myStore", [])

        # failed - owner2 is not store owner
        self.tradeControl.register_guest("owner2", "213456")
        res = self.tradeControl.remove_owner("owner2", "myStore")
        self.assertEqual(res['response'], [])
        self.assertEqual(res['msg'], "Error! remove store owner failed.")

        # success
        self.tradeControl.appoint_additional_owner("owner2", "myStore")
        owner2 = StubUser()
        owner2.register("owner2", "password")
        owner2.login("owner2", "password")
        self.tradeControl.set_curr_user(owner2)
        self.tradeControl.register_guest("owner3", "213456")
        self.tradeControl.appoint_additional_owner("owner3", "myStore")

        self.tradeControl.register_guest("manager2", "213456")
        self.tradeControl.appoint_store_manager("manager2", "myStore", [])

        owner3 = StubUser()
        owner3.register("owner3", "password")
        owner3.login("owner3", "password")
        self.tradeControl.set_curr_user(owner3)
        self.tradeControl.register_guest("manager3", "213456")
        self.tradeControl.appoint_store_manager("manager3", "myStore", [])

        self.tradeControl.set_curr_user(owner1)
        res = self.tradeControl.remove_owner("owner2", "myStore")
        self.assertEqual(res['response'], ['owner2 removed as owner', 'owner3 removed as owner',
                                           'manager3 removed as manager', 'manager2 removed as manager'])
        self.assertEqual(res['msg'], "Store owner owner2 and his appointees were removed successfully.")
        store = self.tradeControl.get_store("myStore")
        self.assertTrue(store.is_manager("manager1"))
        self.assertFalse(store.is_manager("manager2"))
        self.assertFalse(store.is_manager("manager3"))
        self.assertTrue(store.is_owner("owner1"))
        self.assertFalse(store.is_owner("owner2"))
        self.assertFalse(store.is_owner("owner3"))

    def test_appoint_store_manager(self):
        self.user.register("eden", "213456")
        self.user.login("eden", "213456")
        self.tradeControl.register_guest("appointee", "213456")
        self.tradeControl.set_curr_user(self.user)
        self.tradeControl.open_store("myStore")
        store1 = self.tradeControl.get_store("myStore")
        self.assertTrue(self.tradeControl.appoint_store_manager("appointee", "myStore", [])['response'])
        self.assertFalse(self.tradeControl.appoint_store_manager("a", "myStore", [])['response'])
        self.assertTrue(store1.is_manager("appointee"))
        self.assertFalse(store1.is_manager("a"))

    def test_edit_manager_permissions(self):
        self.user.register("eden", "213456")
        self.user.login("eden", "213456")
        self.tradeControl.register_guest("appointee", "213456")
        self.tradeControl.set_curr_user(self.user)
        self.tradeControl.open_store("myStore")
        store1 = self.tradeControl.get_store("myStore")
        self.assertTrue(
            self.tradeControl.appoint_store_manager("appointee", "myStore", [ManagerPermission.APPOINT_OWNER])[
                'response'])
        self.assertTrue(
            self.tradeControl.edit_manager_permissions("myStore", "appointee", [ManagerPermission.EDIT_INV]))
        self.assertTrue(ManagerPermission.EDIT_INV in store1.get_permissions("appointee"))
        self.assertFalse(ManagerPermission.APPOINT_OWNER in store1.get_permissions("appointee"))

    def setup_for_policies(self):
        self.tradeControl.set_curr_user(self.user)
        self.user.register("name", "213456")
        self.user.login("name", "213456")
        self.tradeControl.open_store("store1")
        self.store_mock = Store("store1")
        self.store_mock.get_name = MagicMock(return_value="store1")
        self.store_mock.define_purchase_policy = MagicMock(return_value={"response": True, "msg": "ok"})
        self.store_mock.is_owner = MagicMock(return_value=True)

    def test_define_purchase_policy(self):
        self.setup_for_policies()

        # valid details
        self.store_mock.purchase_policy_exists = MagicMock(
            return_value={"response": False, "msg": "no policy exists by the name"})
        self.purchase_policy_mock.add_purchase_policy = MagicMock(return_value={"response": True, "msg": "ok"})

        res = self.tradeControl.define_purchase_policy(self.store_mock.get_name(), {"name": "policy1",
                                                                                    "products": ["product1",
                                                                                                 "product2"],
                                                                                    "bundle": True})
        self.assertTrue(res)

        # invalid details
        # policy already exist
        self.store_mock.purchase_policy_exists = MagicMock(
            return_value={"response": True, "msg": "ok"})
        self.purchase_policy_mock.add_purchase_policy = MagicMock(return_value={"response": True, "msg": "ok"})

        res = self.tradeControl.define_purchase_policy(self.store_mock.get_name(), {"name": "policy1",
                                                                                    "products": ["product1",
                                                                                                 "product2"],
                                                                                    "bundle": True})["response"]
        self.assertFalse(res)

        # invalid policy details
        self.store_mock.define_purchase_policy = MagicMock(return_value={"response": False, "msg": "invalid details"})
        self.store_mock.purchase_policy_exists = MagicMock(
            return_value={"response": False, "msg": "no policy exists by the name"})

        res = self.tradeControl.define_purchase_policy(self.store_mock.get_name(), {"name": "policy1",
                                                                                    "products": ["product1",
                                                                                                 "product2"]})[
            "response"]
        self.assertFalse(res)
        self.tradeControl.reset_purchase_policies(self.store_mock.get_name())

    def test_update_purchase_policy(self):
        self.setup_for_policies()
        self.store_mock.purchase_policy_exists = MagicMock(
            return_value={"response": False, "msg": "no policy exists by the name"})
        self.purchase_policy_mock.add_purchase_policy = MagicMock(return_value={"response": True, "msg": "ok"})

        self.tradeControl.define_purchase_policy(self.store_mock.get_name(),
                                                 {"name": "policy1", "products": ["product1", "product2"],
                                                  "min_amount": 5})
        # valid update
        self.store_mock.purchase_policy_exists = MagicMock(
            return_value={"response": True, "msg": "ok"})
        self.purchase_policy_mock.update = MagicMock(return_value={"response": True, "msg": "updated"})

        res = self.tradeControl.update_purchase_policy(self.store_mock.get_name(), {"name": "policy1",
                                                                                    "products": ["product1",
                                                                                                 "product2"],
                                                                                    "min_amount": 9})["response"]
        self.assertTrue(res)

        # invalid update
        # policy doesn't exist
        self.store_mock.purchase_policy_exists = MagicMock(
            return_value={"response": False, "msg": "policy doesn't exist"})
        self.purchase_policy_mock.update = MagicMock(return_value={"response": True, "msg": "updated"})

        res = self.tradeControl.update_purchase_policy(self.store_mock.get_name(), {"name": "policy2",
                                                                                    "products": ["product1",
                                                                                                 "product2"],
                                                                                    "min_amount": 9})["response"]
        self.assertFalse(res)

        # invalid policy details
        self.store_mock.purchase_policy_exists = MagicMock(
            return_value={"response": True, "msg": "ok"})
        self.purchase_policy_mock.update = MagicMock(return_value={"response": False, "msg": "can't update"})

        res = self.tradeControl.update_purchase_policy(self.store_mock.get_name(),
                                                       {"name": "policy2", "products": ["product1", "product2"]})[
            "response"]
        self.assertFalse(res)
        self.tradeControl.reset_purchase_policies(self.store_mock.get_name())

    def test_get_policies(self):
        self.setup_for_policies()

        # no policies exist yet
        res = self.tradeControl.get_policies("purchase", self.store_mock.get_name())["response"]
        self.assertTrue(len(res) == 0)

        # policies exist
        self.store_mock.purchase_policy_exists = MagicMock(
            return_value={"response": False, "msg": "no policy exists by the name"})
        self.purchase_policy_mock.add_purchase_policy = MagicMock(return_value={"response": True, "msg": "ok"})
        self.tradeControl.define_purchase_policy(self.store_mock.get_name(), {"name": "policy1",
                                                                              "products": ["product1",
                                                                                           "product2"],
                                                                              "min_amount": 5})

        res = self.tradeControl.get_policies("purchase", self.store_mock.get_name())["response"]
        self.assertTrue(len(res) > 0)
        self.tradeControl.reset_purchase_policies(self.store_mock.get_name())

    def tearDown(self):
        # pass
        (TradeControl.get_instance()).__delete__()
        # self.tradeControl.logout_subscriber()
        # self.tradeControl.unsubscribe("nickname")
        # self.tradeControl.unsubscribe("eden")
        # self.tradeControl.unsubscribe("appointee")
        # self.tradeControl.unsubscribe("owner1")
        # self.tradeControl.unsubscribe("owner2")
        # self.tradeControl.unsubscribe("owner3")
        # self.tradeControl.unsubscribe("manager1")
        # self.tradeControl.unsubscribe("manager2")
        # self.tradeControl.unsubscribe("manager3")
        (DataAccessFacade.get_instance()).delete_purchases()
        # (DataAccessFacade.get_instance()).delete_discount_policies()
        (DataAccessFacade.get_instance()).delete_statistics()
        (DataAccessFacade.get_instance()).delete_store_owner_appointments()
        (DataAccessFacade.get_instance()).delete_products_in_baskets()
        (DataAccessFacade.get_instance()).delete_products()
        (DataAccessFacade.get_instance()).delete_store_manager_appointments()
        (DataAccessFacade.get_instance()).delete_stores()
        (DataAccessFacade.get_instance()).delete_users()

    def __repr__(self):
        return repr("TradeControlTestCase")


if __name__ == '__main__':
    unittest.main()
