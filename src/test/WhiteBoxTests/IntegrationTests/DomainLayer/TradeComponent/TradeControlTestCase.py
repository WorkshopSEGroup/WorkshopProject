import unittest
from datetime import datetime
from unittest.mock import MagicMock

from src.main.DataAccessLayer.DataAccessFacade import DataAccessFacade
from src.main.DomainLayer.StoreComponent.ManagerPermission import ManagerPermission
from src.main.DomainLayer.StoreComponent.Product import Product
from src.main.DomainLayer.StoreComponent.Store import Store
from src.main.DomainLayer.StoreComponent.StoreAppointment import StoreAppointment
from src.main.DomainLayer.TradeComponent.TradeControl import TradeControl
from src.main.DomainLayer.UserComponent.DiscountType import DiscountType
from src.main.DomainLayer.UserComponent.PurchaseType import PurchaseType
from src.main.DomainLayer.UserComponent.ShoppingBasket import ShoppingBasket
from src.main.DomainLayer.UserComponent.User import User
from src.main.DataAccessLayer.ConnectionProxy.Tables import rel_path, IntegrityError


class TradeControlTestCase(unittest.TestCase):
    def setUp(self):
        if not ("testing" in rel_path):
            raise ReferenceError("The Data Base is not the testing data base.\n"
                                 "\t\t\t\tPlease go to src.main.DataAccessLayer.ConnectionProxy.RealDb.rel_path\n"
                                 "\t\t\t\t and change rel_path to test_rel_path.\n"
                                 "\t\t\t\tThanks :D")
        self.__user = User()
        self.__user_nickname = "Eytan"
        self.__user_password = "Eytan's password"
        self.__user.register(self.__user_nickname, self.__user_password)
        self.__eytans_store = "Eytan's store"
        self.__today_without_hour = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
        (DataAccessFacade.get_instance()).write_user("Mr. Eytan", self.__user_password)
        (DataAccessFacade.get_instance()).write_store("Eytan's store", "Mr. Eytan")
        # (DataAccessFacade.get_instance()).write_product("Eytan's product", "Eytan's store", 12, "Eytan's", 21, 0)
        try:
            DataAccessFacade.get_instance().write_user("Eytan", "Eytan's password", False)
            DataAccessFacade.get_instance().write_user("Anna", "Anna's password", False)
            DataAccessFacade.get_instance().write_user("Lady Anna", "Anna's password", False)
            DataAccessFacade.get_instance().write_user("System manager",
                                                       "not Eytan's password", True)
            DataAccessFacade.get_instance().write_store("Eytan's store", "Eytan")
            DataAccessFacade.get_instance().write_product("Eytan's product",
                                                          "Eytan's store", 12,
                                                          "Eytan's", 21, 0)
            DataAccessFacade.get_instance().write_store_manager_appointment(
                "Anna", "Eytan's store",
                "Eytan", ["EDIT_INV", "CLOSE_STORE"])
            (DataAccessFacade.get_instance()).write_products_in_basket("Anna", "Eytan's store",
                                                                       "Eytan's product", 12)
            (DataAccessFacade.get_instance()).write_store_owner_appointment("Lady Anna",
                                                                            "Eytan's store",
                                                                            "Eytan")
            (DataAccessFacade.get_instance()).write_statistic()
            (DataAccessFacade.get_instance()).write_purchase("Anna", "Eytan's store", 12, self.__today_without_hour,
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

    def test_add_system_manager(self):
        # All valid - first manager
        TradeControl.get_instance().register_guest("RvP", "RvP's password")
        rvp = (TradeControl.get_instance()).get_subscriber("RvP")
        self.assertTrue((TradeControl.get_instance()).add_system_manager("RvP", "RvP's password"))

        # rvp = User()
        # rvp.register("RvP", "RvP's password")

        self.assertEqual(2, len((TradeControl.get_instance()).get_managers()))
        self.assertIn(rvp, (TradeControl.get_instance()).get_managers())

        # All valid - not first manager
        self.assertTrue((TradeControl.get_instance()).add_system_manager(self.__user_nickname, self.__user_password))
        self.assertEqual(3, len((TradeControl.get_instance()).get_managers()))
        lst = (TradeControl.get_instance()).get_managers()
        self.assertIn(self.__user, (TradeControl.get_instance()).get_managers())
        self.assertIn(rvp, (TradeControl.get_instance()).get_managers())

        # Invalid - already a manager.
        self.assertFalse(
            (TradeControl.get_instance()).add_system_manager(self.__user_nickname, self.__user_password)['response'])
        self.assertEqual(3, len((TradeControl.get_instance()).get_managers()))
        self.assertIn(self.__user, (TradeControl.get_instance()).get_managers())
        self.assertIn(rvp, (TradeControl.get_instance()).get_managers())

        # Invalid - user doesn't exist
        self.assertFalse(
            (TradeControl.get_instance()).add_system_manager("self.__user_nickname", "self.__user_password")[
                'response'])
        self.assertEqual(3, len((TradeControl.get_instance()).get_managers()))
        self.assertIn(self.__user, (TradeControl.get_instance()).get_managers())
        self.assertIn(rvp, (TradeControl.get_instance()).get_managers())

        user = User()
        user.register("I want it", "That way")

        # Invalid -Incorrect password
        self.assertFalse(
            (TradeControl.get_instance()).add_system_manager(user.get_nickname(), self.__user_password)['response'])
        self.assertEqual(3, len((TradeControl.get_instance()).get_managers()))
        self.assertIn(self.__user, (TradeControl.get_instance()).get_managers())
        self.assertIn(rvp, (TradeControl.get_instance()).get_managers())

    def test_register_guest(self):
        # All valid
        self.assertTrue((TradeControl.get_instance()).register_guest("Valid", "Valid")['response'])
        user = User()
        user.register("Valid", "Valid")
        self.assertEqual(user, (TradeControl.get_instance()).get_subscriber("Valid"))

        # valid -  register another user
        self.assertTrue((TradeControl.get_instance()).register_guest("Valid2", "Valid3")['response'])
        user = User()
        user.register("Valid", "Valid")
        self.assertEqual(user, (TradeControl.get_instance()).get_subscriber("Valid"))
        user = User()
        user.register("Valid2", "Valid3")
        self.assertIn(user, (TradeControl.get_instance()).get_subscribers())

        (TradeControl.get_instance()).set_curr_user = User()

        # Invalid - user already exist
        self.assertFalse((TradeControl.get_instance()).register_guest("Valid", "Valid")['response'])
        user = User()
        user.register("Valid", "Valid")
        self.assertEqual(user, (TradeControl.get_instance()).get_subscriber("Valid"))

        # Invalid - empty username
        self.assertFalse((TradeControl.get_instance()).register_guest("", "Valid")['response'])
        user = User()
        user.register("", "Valid")
        self.assertNotIn(user, (TradeControl.get_instance()).get_subscribers())

        # Invalid - empty password
        self.assertFalse((TradeControl.get_instance()).register_guest("Invalid", "")['response'])
        user = User()
        user.register("Invalid", "")
        self.assertNotIn(user, (TradeControl.get_instance()).get_subscribers())

    def test_login_subscriber(self):
        (TradeControl.get_instance()).register_guest("Valid", "Valid")

        # All valid
        self.assertTrue((TradeControl.get_instance()).login_subscriber("Valid", "Valid")['response'])
        user = (TradeControl.get_instance()).get_curr_user()
        self.assertTrue(user.is_logged_in())

        # Invalid - user already logged in
        self.assertFalse((TradeControl.get_instance()).login_subscriber("Valid", "Valid")['response'])
        self.assertTrue(user.is_logged_in())

        user.logout()

        # Invalid - incorrect password
        self.assertFalse((TradeControl.get_instance()).login_subscriber("Valid", "Invalid")['response'])
        self.assertFalse(user.is_logged_in())

        # Invalid - user doesn't exist
        self.assertFalse((TradeControl.get_instance()).login_subscriber("user.get_nickname()", "Valid")['response'])
        self.assertFalse(user.is_logged_in())

    def test_subscribe(self):
        user = User()
        user.register("Valid", "Valid")

        # All valid
        self.assertTrue((TradeControl.get_instance()).subscribe(user))
        self.assertIn(user, (TradeControl.get_instance()).get_subscribers())

        # Invalid - user already exist
        self.assertFalse((TradeControl.get_instance()).subscribe(user))
        self.assertIn(user, (TradeControl.get_instance()).get_subscribers())

    def test_unsubscribe(self):
        (TradeControl.get_instance()).register_guest("Valid", "Valid")
        user = User()
        user.register("Valid", "Valid")
        (TradeControl.get_instance()).register_guest("db_check_Valid", "Valid")
        # All valid
        self.assertTrue((TradeControl.get_instance()).unsubscribe(user.get_nickname()))
        self.assertNotIn(user, (TradeControl.get_instance()).get_subscribers())

        # Invalid - user already unsubscribed
        self.assertFalse((TradeControl.get_instance()).unsubscribe(user.get_nickname()))
        self.assertNotIn(user, (TradeControl.get_instance()).get_subscribers())

    def test_open_store(self):
        stores_num = len(TradeControl.get_instance().get_stores())
        # (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber("Lady Anna", "Anna's password")
        (TradeControl.get_instance()).get_curr_user().is_logged_in = MagicMock(return_value=True)

        # All valid
        self.assertTrue((TradeControl.get_instance()).open_store("s3"))
        self.assertEqual(stores_num + 1, len((TradeControl.get_instance()).get_stores()))
        store: Store = (TradeControl.get_instance()).get_store("myFirstStore")
        self.assertIsNotNone(store)
        self.assertIn((TradeControl.get_instance()).get_curr_user(), store.get_owners())

        stores_num = stores_num + 1

        # Invalid - store already exist
        self.assertFalse((TradeControl.get_instance()).open_store("myFirstStore")['response'])
        self.assertEqual(stores_num, len((TradeControl.get_instance()).get_stores()))
        self.assertIsNotNone((TradeControl.get_instance()).get_store("myFirstStore"))

        bad_user = User()
        (TradeControl.get_instance()).set_curr_user(bad_user)

        # Invalid - curr_user doesn't register
        self.assertFalse((TradeControl.get_instance()).open_store("not myFirstStore")['response'])
        self.assertEqual(stores_num, len((TradeControl.get_instance()).get_stores()))
        self.assertIsNone((TradeControl.get_instance()).get_store("not myFirstStore"))

        not_logged_in_user = User()
        not_logged_in_user.register("I am", "Logged out")
        (TradeControl.get_instance()).set_curr_user(not_logged_in_user)

        # Invalid - curr_user doesn't register
        self.assertFalse((TradeControl.get_instance()).open_store("not myFirstStore")['response'])
        self.assertEqual(stores_num, len((TradeControl.get_instance()).get_stores()))
        self.assertIsNone((TradeControl.get_instance()).get_store("not myFirstStore"))

        (TradeControl.get_instance()).set_curr_user(self.__user)

        # Invalid - store name is empty
        self.assertFalse((TradeControl.get_instance()).open_store("          ")['response'])
        self.assertEqual(stores_num, len((TradeControl.get_instance()).get_stores()))
        self.assertIsNone((TradeControl.get_instance()).get_store("          "))

    def test_close_store(self):
        (TradeControl.get_instance()).register_guest(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).open_store("myFirstStore")
        stores_num = len(TradeControl.get_instance().get_stores())

        # All valid
        self.assertTrue((TradeControl.get_instance()).close_store("myFirstStore"))
        self.assertEqual(stores_num - 1, len((TradeControl.get_instance()).get_stores()))
        store: Store = (TradeControl.get_instance()).get_store("myFirstStore")
        self.assertIsNone(store)

        stores_num = stores_num - 1

        # Invalid - store already been closed
        self.assertFalse((TradeControl.get_instance()).close_store("myFirstStore"))
        self.assertEqual(stores_num, len((TradeControl.get_instance()).get_stores()))
        self.assertIsNone((TradeControl.get_instance()).get_store("myFirstStore"))

        (TradeControl.get_instance()).open_store("not myFirstStore")
        (TradeControl.get_instance()).get_curr_user().logout()

        stores_num = stores_num + 1

        # Invalid - curr_user is logged out
        self.assertFalse((TradeControl.get_instance()).close_store("not myFirstStore"))
        self.assertEqual(stores_num, len((TradeControl.get_instance()).get_stores()))
        self.assertIsNotNone((TradeControl.get_instance()).get_store("not myFirstStore"))

        bad_user = User()
        (TradeControl.get_instance()).set_curr_user(bad_user)  # reset curr_user
        (TradeControl.get_instance()).register_guest("bad", "user")
        (TradeControl.get_instance()).login_subscriber("bad", "user")

        # Invalid - curr_user doesn't own the stores he try to close
        self.assertFalse((TradeControl.get_instance()).close_store("not myFirstStore"))
        self.assertEqual(stores_num, len((TradeControl.get_instance()).get_stores()))
        self.assertIsNotNone((TradeControl.get_instance()).get_store("not myFirstStore"))

    def test_validate_nickname(self):
        # All valid
        self.assertTrue((TradeControl.get_instance()).validate_nickname("Valid"))

        # All valid - numbers
        self.assertTrue((TradeControl.get_instance()).validate_nickname("Valid12"))

        # All valid - special chars
        self.assertTrue((TradeControl.get_instance()).validate_nickname("Valid's @nickname"))

        # Invalid - empty name
        self.assertFalse((TradeControl.get_instance()).validate_nickname(""))

        # Invalid - only whitespaces name
        self.assertFalse((TradeControl.get_instance()).validate_nickname("              "))

        (TradeControl.get_instance()).subscribe(self.__user)

        # Invalid - name already taken
        self.assertFalse((TradeControl.get_instance()).validate_nickname(self.__user_nickname))

    def test_get_subscriber(self):
        (TradeControl.get_instance()).subscribe(self.__user)

        # All valid
        self.assertEqual(self.__user, (TradeControl.get_instance()).get_subscriber(self.__user_nickname))

        # Invalid - user doesn't exist
        self.assertIsNone((TradeControl.get_instance()).get_subscriber("self.__user_nickname"))

    def test_get_products_by(self):
        (TradeControl.get_instance()).register_guest(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).open_store("myFirstStore")

        store = (TradeControl.get_instance()).get_store("myFirstStore")

        # One store
        store.add_products("Eytan", [{"name": "Chair", "price": 100, "category": "Furniture", "amount": 10,
                                      "purchase_type": 0, "discount_type": 0},
                                     {"name": "TV", "price": 10, "category": "Electric", "amount": 1,
                                      "purchase_type": 0, "discount_type": 0},
                                     {"name": "Sofa", "price": 1, "category": "Furniture", "amount": 2,
                                      "purchase_type": 0, "discount_type": 0}])
        product1: Product = Product("Chair", 100, "Furniture")
        product2: Product = Product("TV", 10, "Electric")
        product3: Product = Product("Sofa", 1, "Furniture")

        # Option 1- All valid
        ls = [result_as_dictionary['product_name'] for result_as_dictionary in
              (TradeControl.get_instance()).get_products_by(1, "Chair")['response']]
        self.assertEqual(len(ls), 1)
        self.assertTrue(product1.get_name() in ls)

        # Option 1- Not an existing product
        ls = [result_as_dictionary['product_name'] for result_as_dictionary in
              (TradeControl.get_instance()).get_products_by(1, "EytanIsTheBestEver!!!!")['response']]
        self.assertEqual(len(ls), 0)

        # Option 2- All valid
        ls = [result_as_dictionary['product_name'] for result_as_dictionary in
              (TradeControl.get_instance()).get_products_by(2, "a")['response']]
        self.assertEqual(len(ls), 3)
        self.assertTrue(product1.get_name() in ls)
        self.assertTrue(product3.get_name() in ls)

        # Option 2- Empty products list
        ls = [result_as_dictionary['product_name'] for result_as_dictionary in
              (TradeControl.get_instance()).get_products_by(2, "EytanIsTheBestEver!!!!!")['response']]
        self.assertEqual(len(ls), 0)

        # Option 3 - All valid
        ls = [result_as_dictionary['product_name'] for result_as_dictionary in
              (TradeControl.get_instance()).get_products_by(3, "Furniture")['response']]
        self.assertEqual(len(ls), 2)
        self.assertTrue(product1.get_name() in ls)
        self.assertTrue(product3.get_name() in ls)

        ls = [result_as_dictionary['product_name'] for result_as_dictionary in
              (TradeControl.get_instance()).get_products_by(3, "Electric")['response']]
        self.assertEqual(len(ls), 1)
        self.assertTrue(product2.get_name() in ls)

        # Option 3 - Not an existing category
        ls = [result_as_dictionary['product_name'] for result_as_dictionary in
              (TradeControl.get_instance()).get_products_by(3, "EytanIsTheBestEver!!!!!")['response']]
        self.assertEqual(len(ls), 0)

        # Two stores (A.K.A more then one store)
        (TradeControl.get_instance()).open_store("not myFirstStore")

        not_store = (TradeControl.get_instance()).get_store("not myFirstStore")
        not_store.add_products("Eytan", [{"name": "Chair", "price": 100, "category": "Furniture", "amount": 10,
                                          "purchase_type": 0, "discount_type": 0},
                                         {"name": "TV", "price": 10, "category": "Electric", "amount": 1,
                                          "purchase_type": 0, "discount_type": 0},
                                         {"name": "Sofa", "price": 1, "category": "Furniture", "amount": 2,
                                          "purchase_type": 0, "discount_type": 0},
                                         {"name": "Pillow", "price": 5, "category": "Accessories", "amount": 5,
                                          "purchase_type": 0, "discount_type": 0}])
        product1: Product = Product("Chair", 100, "Furniture")
        product2: Product = Product("TV", 10, "Electric")
        product3: Product = Product("Sofa", 1, "Furniture")
        diff_product: Product = Product("Pillow", 5, "Accessories")

        # Option 1- All valid
        ls = [(result_as_dictionary['store_name'], result_as_dictionary['product_name']) for result_as_dictionary in
              (TradeControl.get_instance()).get_products_by(1, "Chair")['response']]
        self.assertEqual(len(ls), 2)
        self.assertTrue((store.get_name(), product1.get_name()) in ls)
        self.assertTrue((not_store.get_name(), product1.get_name()) in ls)

        # Option 1- Not an existing product
        ls = [(result_as_dictionary['store_name'], result_as_dictionary['product_name']) for result_as_dictionary in
              (TradeControl.get_instance()).get_products_by(1, "EytanIsTheBestEver!!!!")['response']]
        self.assertEqual(len(ls), 0)

        # Option 2- All valid
        ls = [(result_as_dictionary['store_name'], result_as_dictionary['product_name']) for result_as_dictionary in
              (TradeControl.get_instance()).get_products_by(2, "a")['response']]
        self.assertEqual(len(ls), 5)
        self.assertTrue((store.get_name(), product1.get_name()) in ls)
        self.assertTrue((store.get_name(), product3.get_name()) in ls)
        self.assertTrue((not_store.get_name(), product1.get_name()) in ls)
        self.assertTrue((not_store.get_name(), product3.get_name()) in ls)

        # Option 2- Empty products list
        ls = [(result_as_dictionary['store_name'], result_as_dictionary['product_name']) for result_as_dictionary in
              (TradeControl.get_instance()).get_products_by(2, "EytanIsTheBestEver!!!!!")['response']]
        self.assertEqual(len(ls), 0)

        # Option 3 - All valid
        ls = [(result_as_dictionary['store_name'], result_as_dictionary['product_name']) for result_as_dictionary in
              (TradeControl.get_instance()).get_products_by(3, "Furniture")['response']]
        self.assertEqual(len(ls), 4)
        self.assertTrue((store.get_name(), product1.get_name()) in ls)
        self.assertTrue((store.get_name(), product3.get_name()) in ls)
        self.assertTrue((not_store.get_name(), product1.get_name()) in ls)
        self.assertTrue((not_store.get_name(), product3.get_name()) in ls)

        ls = [(result_as_dictionary['store_name'], result_as_dictionary['product_name']) for result_as_dictionary in
              (TradeControl.get_instance()).get_products_by(3, "Electric")['response']]
        self.assertEqual(len(ls), 2)
        self.assertTrue((store.get_name(), product2.get_name()) in ls)
        self.assertTrue((not_store.get_name(), product2.get_name()) in ls)

        # Option 3 - Not an existing category
        ls = [(result_as_dictionary['store_name'], result_as_dictionary['product_name']) for result_as_dictionary in
              (TradeControl.get_instance()).get_products_by(3, "EytanIsTheBestEver!!!!!")['response']]
        self.assertEqual(len(ls), 0)

        # Valid - product exist only in on store
        ls = [(result_as_dictionary['store_name'], result_as_dictionary['product_name']) for result_as_dictionary in
              (TradeControl.get_instance()).get_products_by(1, "Pillow")['response']]
        self.assertEqual(len(ls), 1)
        self.assertFalse((store.get_name(), diff_product.get_name()) in ls)
        self.assertTrue((not_store.get_name(), diff_product.get_name()) in ls)

    def test_filter_products_by(self):
        (TradeControl.get_instance()).register_guest(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).open_store("myFirstStore")

        store = (TradeControl.get_instance()).get_store("myFirstStore")

        store.add_products("Eytan", [{"name": "Chair", "price": 100, "category": "Furniture", "amount": 10,
                                      "purchase_type": 0, "discount_type": 0},
                                     {"name": "TV", "price": 10, "category": "Electric", "amount": 1,
                                      "purchase_type": 0, "discount_type": 0},
                                     {"name": "Sofa", "price": 1, "category": "Furniture", "amount": 2,
                                      "purchase_type": 0, "discount_type": 0}])

        # Option 1

        # All valid
        product_ls = (TradeControl.get_instance()).get_products_by(2, "")['response']
        expected = [(product_as_dictionary['store_name'],
                     product_as_dictionary['product_name'],
                     product_as_dictionary['price'],
                     product_as_dictionary['category']) for product_as_dictionary in product_ls]

        result = [(product_as_dictionary['store_name'],
                   product_as_dictionary['product_name'],
                   product_as_dictionary['price'],
                   product_as_dictionary['category']) for product_as_dictionary in
                  (TradeControl.get_instance()).filter_products_by(product_ls, 1, min_price=0, max_price=101)[
                      'response']]
        self.assertListEqual(expected, result)

        product_ls = (TradeControl.get_instance()).get_products_by(2, "")['response']
        expected = [(product_as_dictionary['store_name'],
                     product_as_dictionary['product_name'],
                     product_as_dictionary['price'],
                     product_as_dictionary['category']) for product_as_dictionary in product_ls]

        # All valid - edge case -> min price = some_product price & max price = some_product price
        result = [(product_as_dictionary['store_name'],
                   product_as_dictionary['product_name'],
                   product_as_dictionary['price'],
                   product_as_dictionary['category']) for product_as_dictionary in
                  (TradeControl.get_instance()).filter_products_by(product_ls, 1, min_price=1, max_price=100)[
                      'response']]

        self.assertListEqual(expected, result)

        product_ls = (TradeControl.get_instance()).get_products_by(2, "")['response']
        expected = [(product_as_dictionary['store_name'],
                     product_as_dictionary['product_name'],
                     product_as_dictionary['price'],
                     product_as_dictionary['category']) for product_as_dictionary in product_ls if
                    product_as_dictionary['price'] >= 5]

        # All valid - actually doing some filtering.
        result = [(product_as_dictionary['store_name'],
                   product_as_dictionary['product_name'],
                   product_as_dictionary['price'],
                   product_as_dictionary['category']) for product_as_dictionary in
                  (TradeControl.get_instance()).filter_products_by(product_ls, 1, min_price=5, max_price=200)[
                      'response']]

        self.assertListEqual(expected, result)

        # Invalid - no min price
        result = [(product_as_dictionary['store_name'],
                   product_as_dictionary['product_name'],
                   product_as_dictionary['price'],
                   product_as_dictionary['category']) for product_as_dictionary in
                  (TradeControl.get_instance()).filter_products_by(product_ls, 1, max_price=200)['response']]

        self.assertListEqual([], result)

        # Invalid - no max price
        result = [(product_as_dictionary['store_name'],
                   product_as_dictionary['product_name'],
                   product_as_dictionary['price'],
                   product_as_dictionary['category']) for product_as_dictionary in
                  (TradeControl.get_instance()).filter_products_by(product_ls, 1, min_price=0.1)['response']]

        self.assertListEqual([], result)

        # Invalid - empty product_ls
        result = [(product_as_dictionary['store_name'],
                   product_as_dictionary['product_name'],
                   product_as_dictionary['price'],
                   product_as_dictionary['category']) for product_as_dictionary in
                  (TradeControl.get_instance()).filter_products_by([], 1, min_price=0.1, max_price=200)['response']]

        self.assertListEqual([], result)

        # Option 2

        # All valid
        product_ls = (TradeControl.get_instance()).get_products_by(2, "")['response']
        expected = [(product_as_dictionary['store_name'],
                     product_as_dictionary['product_name'],
                     product_as_dictionary['price'],
                     product_as_dictionary['category']) for product_as_dictionary in product_ls
                    if product_as_dictionary['category'] == "Furniture"]

        result = [(product_as_dictionary['store_name'],
                   product_as_dictionary['product_name'],
                   product_as_dictionary['price'],
                   product_as_dictionary['category']) for product_as_dictionary in
                  (TradeControl.get_instance()).filter_products_by(product_ls, 2, category="Furniture")['response']]
        self.assertListEqual(expected, result)

        # Invalid - no category
        result = [(product_as_dictionary['store_name'],
                   product_as_dictionary['product_name'],
                   product_as_dictionary['price'],
                   product_as_dictionary['category']) for product_as_dictionary in
                  (TradeControl.get_instance()).filter_products_by(product_ls, 2)['response']]
        self.assertListEqual([], result)

        # Invalid - category doesn't exist
        result = [(product_as_dictionary['store_name'],
                   product_as_dictionary['product_name'],
                   product_as_dictionary['price'],
                   product_as_dictionary['category']) for product_as_dictionary in
                  (TradeControl.get_instance()).filter_products_by(product_ls, 2, category="Eytan's category")[
                      'response']]
        self.assertListEqual([], result)

        # Invalid - empty product_ls
        result = [(product_as_dictionary['store_name'],
                   product_as_dictionary['product_name'],
                   product_as_dictionary['price'],
                   product_as_dictionary['category']) for product_as_dictionary in
                  (TradeControl.get_instance()).filter_products_by([], 2, category="Furniture")['response']]
        self.assertListEqual([], result)

        # Neither of the options

        # Invalid - option doesn't exist
        result = [(product_as_dictionary['store_name'],
                   product_as_dictionary['product_name'],
                   product_as_dictionary['price'],
                   product_as_dictionary['category']) for product_as_dictionary in
                  (TradeControl.get_instance()).filter_products_by([], 3, category="Furniture")['response']]
        self.assertListEqual([], result)

        # Invalid - option doesn't exist
        result = [(product_as_dictionary['store_name'],
                   product_as_dictionary['product_name'],
                   product_as_dictionary['price'],
                   product_as_dictionary['category']) for product_as_dictionary in
                  (TradeControl.get_instance()).filter_products_by(product_ls, 3, min_price=12.2, max_price=43)[
                      'response']]
        self.assertListEqual([], result)

    def test_logout_subscriber(self):
        (TradeControl.get_instance()).register_guest(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)

        # All valid
        self.assertTrue((TradeControl.get_instance()).logout_subscriber()['response'])

        # Invalid - user already logged out
        self.assertFalse((TradeControl.get_instance()).logout_subscriber()['response'])

    def test_save_products_to_basket(self):
        # TODO: Maybe add a test to check if try to purchase more amount then the store have.

        # db-testing
        #(TradeControl.get_instance()).register_guest("Anna", "Anna's password")
        (TradeControl.get_instance()).login_subscriber("Lady Anna", "Anna's password")

        product_as_dictionary = {"product_name": "Eytan's product", "amount": 4, "store_name": "Eytan's store"}
        self.assertTrue((TradeControl.get_instance()).save_products_to_basket([product_as_dictionary]))
        self.assertEqual(len((TradeControl.get_instance()).get_subscriber("Anna").get_shopping_cart()
                             .get_shopping_baskets()), 1)

        (TradeControl.get_instance()).logout_subscriber()

        # rest of tests

        (TradeControl.get_instance()).register_guest(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).open_store("myStore")
        (TradeControl.get_instance()).add_products("myStore", [
            {"name": "Eytan's product", "price": 12, "category": "Eytan's category", "amount": 5,
             "purchase_type": 0, "discount_type": 0}])
        product = Product("Eytan's product", 12, "Eytan's category")
        # store: Store = Store("myStore")
        # store.add_product("", "Eytan's product", 12, "Eytan's category", 5)
        # (TradeControl.get_instance()).get_stores().append(store)
        product_as_dictionary = {"product_name": product.get_name(), "amount": 4, "store_name": "myStore"}
        product_to_add = (product,
                          product_as_dictionary['amount'])

        basket = ShoppingBasket()
        basket.add_product(*product_to_add)
        expected = ("myStore", basket)

        shopping_cart = (TradeControl.get_instance()).get_curr_user().get_shopping_cart()

        # All valid
        self.assertTrue((TradeControl.get_instance()).save_products_to_basket([product_as_dictionary]))
        self.assertEqual(len(shopping_cart.get_shopping_baskets()), 1)
        self.assertIn(expected, [(basket['store_name'], basket['basket']) for basket in
                                 shopping_cart.get_shopping_baskets()])

        # Valid - empty basket
        self.assertTrue((TradeControl.get_instance()).save_products_to_basket([]))
        self.assertEqual(len(shopping_cart.get_shopping_baskets()), 1)
        self.assertIn(expected, [(basket['store_name'], basket['basket']) for basket in
                                 shopping_cart.get_shopping_baskets()])

        # invalid - basket = None
        self.assertFalse(
            (TradeControl.get_instance()).save_products_to_basket([product_as_dictionary, None])['response'])
        self.assertEqual(len(shopping_cart.get_shopping_baskets()), 1)
        self.assertIn(expected, [(basket['store_name'], basket['basket']) for basket in
                                 shopping_cart.get_shopping_baskets()])

        bad_basket = {"product_name": "", "amount": 4, "store_name": "myStore",
                      "discount_type": DiscountType.DEFAULT, "purchase_type": PurchaseType.DEFAULT}

        # invalid - product = None
        self.assertFalse((TradeControl.get_instance()).save_products_to_basket([bad_basket])['response'])
        self.assertEqual(len(shopping_cart.get_shopping_baskets()), 1)
        self.assertIn(expected, [(basket['store_name'], basket['basket']) for basket in
                                 shopping_cart.get_shopping_baskets()])

        bad_basket = {"product_name": product.get_name(), "amount": -4, "store_name": "myStore",
                      "discount_type": DiscountType.DEFAULT, "purchase_type": PurchaseType.DEFAULT}

        # invalid - negative amount
        self.assertFalse((TradeControl.get_instance()).save_products_to_basket([bad_basket])['response'])
        self.assertEqual(len(shopping_cart.get_shopping_baskets()), 1)
        self.assertIn(expected, [(basket['store_name'], basket['basket']) for basket in
                                 shopping_cart.get_shopping_baskets()])
        bad_basket = {"product_name": product.get_name(), "amount": -4, "store_name": "myStore",
                      "discount_type": DiscountType.DEFAULT, "purchase_type": PurchaseType.DEFAULT}

        bad_basket = {"product_name": product, "amount": 0, "store_name": "myStore",
                      "discount_type": DiscountType.DEFAULT, "purchase_type": PurchaseType.DEFAULT}

        # invalid - Edge case - amount = 0
        self.assertFalse((TradeControl.get_instance()).save_products_to_basket([bad_basket])['response'])
        self.assertEqual(len(shopping_cart.get_shopping_baskets()), 1)
        self.assertIn(expected, [(basket['store_name'], basket['basket']) for basket in
                                 shopping_cart.get_shopping_baskets()])

    def test_remove_from_shopping_cart(self):

        # db tests
        (TradeControl.get_instance()).login_subscriber("Anna", "Anna's password")

        product_as_dictionary = {"product_name": "Eytan's product", "store_name": "Eytan's store"}
        self.assertTrue((TradeControl.get_instance()).remove_from_shopping_cart([product_as_dictionary]))
        self.assertEqual(len((TradeControl.get_instance()).get_subscriber("Anna").get_shopping_cart()
                             .get_shopping_baskets()), 0)

        (TradeControl.get_instance()).logout_subscriber()

        # rest tests

        (TradeControl.get_instance()).register_guest(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).open_store("myStore")
        (TradeControl.get_instance()).add_products("myStore", [
            {"name": "Eytan's product", "price": 12, "category": "Eytan's category", "amount": 5,
             "purchase_type": 0},
            {"name": "eytan as product", "price": 10, "category": "Eytan's category", "amount": 100,
             "purchase_type": 0}])

        product = Product("Eytan's product", 12, "Eytan's category")
        product2 = Product("eytan as product", 10, "Eytan's category")
        store_name = "myStore"

        product_as_dictionary = {"product_name": product.get_name(), "amount": 100, "store_name": store_name,
                                 "discount_type": DiscountType.DEFAULT, "purchase_type": PurchaseType.DEFAULT}

        product_as_dictionary2 = {"product_name": product2.get_name(), "amount": 100, "store_name": store_name,
                                  "discount_type": DiscountType.DEFAULT, "purchase_type": PurchaseType.DEFAULT}

        (TradeControl.get_instance()).save_products_to_basket([product_as_dictionary, product_as_dictionary2])

        product_details_as_dictionary = {"product_name": product.get_name(),
                                         "store_name": store_name,
                                         "amount": 15}
        product_details_as_dictionary2 = {"product_name": product2.get_name(),
                                          "store_name": store_name,
                                          "amount": 15}

        # All valid
        self.assertTrue((TradeControl.get_instance()).remove_from_shopping_cart([product_details_as_dictionary]))
        self.assertEqual(1,
                         len((TradeControl.get_instance()).get_curr_user().get_shopping_cart().get_shopping_baskets()))
        self.assertIsNone((TradeControl.get_instance()).get_curr_user().get_shopping_cart().
            get_store_basket(store_name).get_product(
            (product_details_as_dictionary['product_name'])))
        self.assertIsNotNone((TradeControl.get_instance()).get_curr_user().get_shopping_cart().
            get_store_basket(store_name).get_product(
            (product_details_as_dictionary2['product_name'])))

        product_details_as_dictionary = {"product_name": product2.get_name(),
                                         "store_name": "store.get_name()",
                                         "amount": 15}

        # Invalid - store doesn't exist
        self.assertFalse(
            (TradeControl.get_instance()).remove_from_shopping_cart([product_details_as_dictionary])['response'])

        product_details_as_dictionary = {"product_name": "product2.get_name()",
                                         "store_name": store_name,
                                         "amount": 15}

        # Invalid - product doesn't exist
        self.assertFalse(
            (TradeControl.get_instance()).remove_from_shopping_cart([product_details_as_dictionary])['response'])

        # Valid - empty product_details
        self.assertTrue((TradeControl.get_instance()).remove_from_shopping_cart([])['response'])

    def test_update_quantity_in_shopping_cart(self):

        # db tests
        (TradeControl.get_instance()).login_subscriber("Anna", "Anna's password")

        product_as_dictionary = {"product_name": "Eytan's product", "amount": 44, "store_name": "Eytan's store"}
        self.assertTrue((TradeControl.get_instance()).update_quantity_in_shopping_cart([product_as_dictionary]))
        self.assertEqual(len((TradeControl.get_instance()).get_subscriber("Anna").get_shopping_cart()
                             .get_shopping_baskets()), 1)

        (TradeControl.get_instance()).logout_subscriber()

        # rest tests

        product = Product("Eytan's product", 12, "Eytan's category")
        store: Store = Store("myStore")
        user: User = User()
        user.register('Eytan', '12')

        store.get_owners_appointments().append(StoreAppointment(None, user, []))
        store.add_product("Eytan", "Eytan's product", 12, "Eytan's category", 5, 0)

        (TradeControl.get_instance()).get_stores().append(store)
        product_as_dictionary = {"product_name": product.get_name(), "amount": 4, "store_name": store.get_name(),
                                 "discount_type": DiscountType.DEFAULT, "purchase_type": PurchaseType.DEFAULT}

        product1: Product = Product("not Eytan's product", 9, "Eytan's category")
        product2: Product = Product("maybe Eytan's product", 8, "Eytan's category")
        store.add_product("Eytan", "not Eytan's product", 9, "Eytan's category", 3, 0)
        store1: Store = Store("Not my store")

        # store1.get_owners().append(user)
        store1.get_owners_appointments().append(StoreAppointment(None, user, []))

        store1.add_product("Eytan", "Eytan's product", 12, "Eytan's category", 5, 0)
        store1.add_product("Eytan", "not Eytan's product", 9, "Eytan's category", 12, 0)
        store1.add_product("Eytan", "maybe Eytan's product", 8, "Eytan's category", 5, 0)

        (TradeControl.get_instance()).get_stores().append(store1)
        product_as_dictionary_var1 = {"product_name": product1.get_name(), "amount": 3, "store_name": store.get_name(),
                                      "discount_type": DiscountType.DEFAULT, "purchase_type": PurchaseType.DEFAULT}
        product_as_dictionary_var3 = {"product_name": product1.get_name(), "amount": 12,
                                      "store_name": store1.get_name(),
                                      "discount_type": DiscountType.DEFAULT, "purchase_type": PurchaseType.DEFAULT}
        product_as_dictionary_var2 = {"product_name": product2.get_name(), "amount": 5, "store_name": store1.get_name(),
                                      "discount_type": DiscountType.DEFAULT, "purchase_type": PurchaseType.DEFAULT}
        (TradeControl.get_instance()).save_products_to_basket([product_as_dictionary,
                                                               product_as_dictionary_var1,
                                                               product_as_dictionary_var2,
                                                               product_as_dictionary_var3])
        shopping_cart = (TradeControl.get_instance()).get_curr_user().get_shopping_cart()

        # All Valid - product only in one store
        self.assertTrue(
            (TradeControl.get_instance()).update_quantity_in_shopping_cart([{"product_name": product.get_name(),
                                                                             "store_name": store.get_name(),
                                                                             "amount": 123}])['response'])
        self.assertEqual(123, TradeControl.get_instance().get_curr_user().get_shopping_cart().
                         get_store_basket(store.get_name()).get_product_amount(product.get_name()))

        # All Valid - product in two stores, but change only in one
        self.assertTrue(
            (TradeControl.get_instance()).update_quantity_in_shopping_cart([{"product_name": product1.get_name(),
                                                                             "store_name": store.get_name(),
                                                                             "amount": 234}])['response'])
        self.assertEqual(234, TradeControl.get_instance().get_curr_user().get_shopping_cart().
                         get_store_basket(store.get_name()).get_product_amount(product1.get_name()))
        self.assertEqual(12, TradeControl.get_instance().get_curr_user().get_shopping_cart().
                         get_store_basket(store1.get_name()).get_product_amount(product1.get_name()))

        # Invalid - product not in store
        self.assertFalse(
            (TradeControl.get_instance()).update_quantity_in_shopping_cart([{"product_name": product2.get_name(),
                                                                             "store_name": store.get_name(),
                                                                             "amount": 234}])['response'])
        self.assertNotEqual(234, TradeControl.get_instance().get_curr_user().get_shopping_cart().
                            get_store_basket(store1.get_name()).get_product_amount(product2.get_name()))

        # Invalid - negative amount
        self.assertFalse(
            (TradeControl.get_instance()).update_quantity_in_shopping_cart([{"product_name": product.get_name(),
                                                                             "store_name": store.get_name(),
                                                                             "amount": -999}])['response'])
        self.assertNotEqual(-999, TradeControl.get_instance().get_curr_user().get_shopping_cart().
                            get_store_basket(store.get_name()).get_product_amount(product.get_name()))

    def test_add_products(self):
        product = Product("Eytan's product", 12, "Eytan's category")
        product_as_dictionary = {"name": product.get_name(),
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5,
                                 "purchase_type": 0}

        (TradeControl.get_instance()).set_curr_user(TradeControl.get_instance().get_subscriber("Mr. Eytan"))
        (TradeControl.get_instance()).get_curr_user().is_logged_in = MagicMock(return_value=True)

        # db tests
        self.assertTrue((TradeControl.get_instance()).add_products("Eytan's store", [product_as_dictionary]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store("Eytan's store").get_product(product.get_name()))
        self.assertEqual(26, (TradeControl.get_instance()).get_store("Eytan's store").get_inventory().
                         get_amount(product.get_name()))

        (TradeControl.get_instance()).logout_subscriber()

        manager = User()
        manager.register("manager", "manager")
        store: Store = Store("myStore")
        # store.add_product("Eytan's product", 12, "Eytan's category", 5)
        (TradeControl.get_instance()).get_stores().append(store)
        # (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).register_guest(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners_appointments().append(
            StoreAppointment(None, self.__user, []))
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_INV])

        # All valid - owner

        self.assertTrue((TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).get_product(product.get_name()))
        self.assertEqual(5, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount(product.get_name()))

        product_as_dictionary = {"name": "N is for name",
                                 "price": 3,
                                 "category": "C is for category",
                                 "amount": 0,
                                 "purchase_type": 0}

        # All valid - owner -edge case -> amount = 0
        self.assertTrue((TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product(product_as_dictionary['name']))
        self.assertEqual(0, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount(product_as_dictionary['name']))

        product_as_dictionary = {"name": "N is for No-way-in-hell-we-get-less-then-100",
                                 "price": 3,
                                 "category": "C is for category",
                                 "amount": -99,
                                 "purchase_type": 0}

        # Invalid - negative amount
        self.assertFalse(
            (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])['response'])
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))

        product_as_dictionary = {"name": "N is for No-way-in-hell-we-get-less-then-100",
                                 "price": 3,
                                 "category": "C is for category",
                                 "amount": 99,
                                 "purchase_type": 0}

        # Invalid - store doesn't exist
        self.assertFalse(
            (TradeControl.get_instance()).add_products("store.get_name()", [product_as_dictionary])['response'])

        (TradeControl.get_instance()).logout_subscriber()
        product_as_dictionary = {"name": "N is for Never said goodbye",
                                 "price": 3,
                                 "category": "C is for category",
                                 "amount": 15,
                                 "purchase_type": 0}

        # Invalid - curr_user is logged out
        self.assertFalse(
            (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])['response'])
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))

        product_as_dictionary = {"name": product.get_name(),
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5,
                                 "purchase_type": 0}

        # All valid - Manager

        # (TradeControl.get_instance()).set_curr_user(manager)
        TradeControl.get_instance().register_guest(manager.get_nickname(), "manager")
        TradeControl.get_instance().login_subscriber(manager.get_nickname(), "manager")

        # Test both manager and add to a product that already exist.
        self.assertTrue((TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).get_product(product.get_name()))
        self.assertEqual(10, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount(product.get_name()))

        product_as_dictionary = {"name": "N is for name",
                                 "price": 3,
                                 "category": "C is for category",
                                 "amount": 0,
                                 "purchase_type": 0}

        # All valid - owner -edge case -> amount = 0
        self.assertTrue((TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product(product_as_dictionary['name']))
        self.assertEqual(0, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount(product_as_dictionary['name']))

        product_as_dictionary = {"name": "N is for No-way-in-hell-we-get-less-then-100",
                                 "price": 3,
                                 "category": "C is for category",
                                 "amount": -99,
                                 "purchase_type": 0}

        # Invalid - negative amount
        self.assertFalse(
            (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])['response'])
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))

        product_as_dictionary = {"name": "N is for No-way-in-hell-we-get-less-then-100",
                                 "price": 3,
                                 "category": "C is for category",
                                 "amount": 99,
                                 "purchase_type": 0}

        # Invalid - store doesn't exist
        self.assertFalse(
            (TradeControl.get_instance()).add_products("store.get_name()", [product_as_dictionary])['response'])

        product_as_dictionary = {"name": "Name a better striker then RvP. I dare you.",
                                 "price": 3,
                                 "category": "C is for category",
                                 "amount": 99,
                                 "purchase_type": 0}
        (TradeControl.get_instance()).get_store(store.get_name()). \
            edit_manager_permissions(self.__user, manager.get_nickname(), [ManagerPermission.USERS_QUESTIONS])

        # Invalid- not right permissions:
        self.assertFalse(
            (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])['response'])
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))

        (TradeControl.get_instance()).logout_subscriber()

        product_as_dictionary = {"name": "N is for Never said goodbye",
                                 "price": 3,
                                 "category": "C is for category",
                                 "amount": 15,
                                 "purchase_type": 0}

        # Invalid - curr_user is logged out
        self.assertFalse(
            (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])['response'])
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))

        user = User()
        user.register("dry", "country")
        (TradeControl.get_instance()).logout_subscriber()
        (TradeControl.get_instance()).set_curr_user(user)
        (TradeControl.get_instance()).login_subscriber(user.get_nickname(), "country")

    def test_remove_products(self):
        product = Product("Eytan's product", 12, "Eytan's category")
        product_as_dictionary = {"name": product.get_name(),
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5,
                                 "purchase_type": 0}

        (TradeControl.get_instance()).set_curr_user(TradeControl.get_instance().get_subscriber("Mr. Eytan"))
        (TradeControl.get_instance()).get_curr_user().is_logged_in = MagicMock(return_value=True)

        # All valid - db test - one product
        self.assertTrue((TradeControl.get_instance()).remove_products(self.__eytans_store, ["Eytan's product"]
                                                                      ))
        self.assertIsNone((TradeControl.get_instance()).get_store(self.__eytans_store).
                          get_product(product_as_dictionary['name']))

        (TradeControl.get_instance()).logout_subscriber()

        manager = User()
        manager.register("manager", "manager")
        store: Store = Store("myStore")
        (TradeControl.get_instance()).get_stores().append(store)
        # (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).register_guest(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners_appointments().append(
            StoreAppointment(None, self.__user, []))
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_INV])

        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])

        # All valid - owner - one product
        self.assertTrue((TradeControl.get_instance()).remove_products(store.get_name(), [product_as_dictionary['name']]
                                                                      ))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))

        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])
        product_as_dictionary2 = {"name": "I'll be there for you",
                                  "price": product.get_price(),
                                  "category": product.get_category(),
                                  "amount": 5,
                                  "purchase_type": 0}
        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary2])

        # All valid - owner - two products
        self.assertTrue((TradeControl.get_instance()).remove_products(store.get_name(), [product_as_dictionary['name'],
                                                                                         product_as_dictionary2['name']]
                                                                      ))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary2['name']))

        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])
        product_as_dictionary2 = {"name": "I'll be there for you",
                                  "price": product.get_price(),
                                  "category": product.get_category(),
                                  "amount": 5,
                                  "purchase_type": 0}
        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary2])

        # All valid - owner - two products
        self.assertTrue((TradeControl.get_instance()).remove_products(store.get_name(), [product_as_dictionary['name']]
                                                                      ))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product(product_as_dictionary2['name']))

        product_as_dictionary = {"name": "It's my life",
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5,
                                 "purchase_type": 0}
        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])

        # Invalid - store doesn't exist
        self.assertFalse(
            (TradeControl.get_instance()).remove_products("store.get_name()", [product_as_dictionary['name']]))

        # Invalid - product doesn't exist
        self.assertFalse((TradeControl.get_instance()).remove_products(store.get_name(), ["product.get_name()"]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product(product_as_dictionary['name']))

        # valid - empty list
        self.assertTrue((TradeControl.get_instance()).remove_products(store.get_name(), []))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product(product_as_dictionary['name']))

        (TradeControl.get_instance()).logout_subscriber()

        store2: Store = Store("store2")
        (TradeControl.get_instance()).get_stores().append(store2)
        product_as_dictionary = {"name": "Born to be my baby",
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5,
                                 "purchase_type": 0}
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).get_store(store2.get_name()).get_owners_appointments().append(
            StoreAppointment(None, self.__user, []))
        (TradeControl.get_instance()).get_store(store2.get_name()).add_manager(self.__user, manager,
                                                                               [ManagerPermission.EDIT_INV])
        (TradeControl.get_instance()).add_products(store2.get_name(), [product_as_dictionary])

        # Invalid - product exist in a different store.
        self.assertFalse(
            (TradeControl.get_instance()).remove_products(store.get_name(), [product_as_dictionary['name']]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store2.get_name()).
                             get_product(product_as_dictionary['name']))

        # Invalid - curr_user logged out
        self.assertFalse(
            (TradeControl.get_instance()).remove_products(store.get_name(), [product_as_dictionary['name']]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store2.get_name()).
                             get_product(product_as_dictionary['name']))

        # Clean all
        (TradeControl.get_instance()).__delete__()

        product = Product("Eytan's product", 12, "Eytan's category")
        product_as_dictionary = {"name": product.get_name(),
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5,
                                 "purchase_type": 0}

        manager = User()
        manager.register("manager", "manager")
        store: Store = Store("myStore")
        (TradeControl.get_instance()).get_stores().append(store)
        # (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).register_guest(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners_appointments().append(
            StoreAppointment(None, self.__user, []))
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_INV])
        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])
        (TradeControl.get_instance()).logout_subscriber()
        # (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).register_guest(manager.get_nickname(), "manager")
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "manager")

        # All valid - manager - one product
        self.assertTrue((TradeControl.get_instance()).remove_products(store.get_name(), [product_as_dictionary['name']]
                                                                      ))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))

        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])
        product_as_dictionary2 = {"name": "I'll be there for you",
                                  "price": product.get_price(),
                                  "category": product.get_category(),
                                  "amount": 5,
                                  "purchase_type": 0}
        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary2])

        # All valid - manager - two products
        self.assertTrue((TradeControl.get_instance()).remove_products(store.get_name(), [product_as_dictionary['name'],
                                                                                         product_as_dictionary2['name']]
                                                                      ))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary2['name']))

        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])
        product_as_dictionary2 = {"name": "I'll be there for you",
                                  "price": product.get_price(),
                                  "category": product.get_category(),
                                  "amount": 5,
                                  "purchase_type": 0}
        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary2])

        # All valid - manager - two products
        self.assertTrue((TradeControl.get_instance()).remove_products(store.get_name(), [product_as_dictionary['name']]
                                                                      ))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product(product_as_dictionary2['name']))

        product_as_dictionary = {"name": "It's my life",
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5,
                                 "purchase_type": 0}
        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])

        # Invalid - store doesn't exist
        self.assertFalse(
            (TradeControl.get_instance()).remove_products("store.get_name()", [product_as_dictionary['name']]))

        # Invalid - product doesn't exist
        self.assertFalse((TradeControl.get_instance()).remove_products(store.get_name(), ["product.get_name()"]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product(product_as_dictionary['name']))

        # valid - empty list
        self.assertTrue((TradeControl.get_instance()).remove_products(store.get_name(), []))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product(product_as_dictionary['name']))

        store2: Store = Store("store2")
        (TradeControl.get_instance()).get_stores().append(store2)

        product_as_dictionary = {"name": "Born to be my baby",
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5,
                                 "purchase_type": 0}
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).get_store(store2.get_name()).get_owners_appointments().append(
            StoreAppointment(None, self.__user, []))
        (TradeControl.get_instance()).get_store(store2.get_name()).add_manager(self.__user, manager,
                                                                               [ManagerPermission.EDIT_INV])
        (TradeControl.get_instance()).add_products(store2.get_name(), [product_as_dictionary])

        (TradeControl.get_instance()).logout_subscriber()
        (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "country")

        # Invalid - product exist in a different store.
        self.assertFalse(
            (TradeControl.get_instance()).remove_products(store.get_name(), [product_as_dictionary['name']]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store2.get_name()).
                             get_product(product_as_dictionary['name']))

        (TradeControl.get_instance()).get_store(store2.get_name()). \
            edit_manager_permissions(self.__user, manager.get_nickname(), [ManagerPermission.USERS_QUESTIONS])

        # Invalid - manager doesn't have permissions
        self.assertFalse(
            (TradeControl.get_instance()).remove_products(store2.get_name(), [product_as_dictionary['name']]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store2.get_name()).
                             get_product(product_as_dictionary['name']))

        (TradeControl.get_instance()).logout_subscriber()

        # Invalid - curr_user logged out
        self.assertFalse(
            (TradeControl.get_instance()).remove_products(store2.get_name(), [product_as_dictionary['name']]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store2.get_name()).
                             get_product(product_as_dictionary['name']))

        user = User()
        user.register("dry", "country")
        (TradeControl.get_instance()).logout_subscriber()
        (TradeControl.get_instance()).set_curr_user(user)
        (TradeControl.get_instance()).login_subscriber(user.get_nickname(), "country")

        # Invalid - not a manager or a user
        self.assertFalse(
            (TradeControl.get_instance()).remove_products(store.get_name(), [product_as_dictionary['name']]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store2.get_name()).
                             get_product(product_as_dictionary['name']))

    def test_edit_product(self):
        product = Product("Eytan's product", 12, "Eytan's category")
        product_as_dictionary = {"name": product.get_name(),
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5,
                                 "purchase_type": 0}

        (TradeControl.get_instance()).set_curr_user(TradeControl.get_instance().get_subscriber("Mr. Eytan"))
        (TradeControl.get_instance()).get_curr_user().is_logged_in = MagicMock(return_value=True)

        # All valid - owner - db_ tests
        self.assertTrue((TradeControl.get_instance()).edit_product(self.__eytans_store, product_as_dictionary['name'],
                                                                   "name",
                                                                   "new_name"))
        self.assertIsNone((TradeControl.get_instance()).get_store(self.__eytans_store).
                          get_product(product_as_dictionary['name']))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(self.__eytans_store).
                             get_product("new_name"))

        # All valid - owner - db_ tests
        self.assertTrue((TradeControl.get_instance()).edit_product(self.__eytans_store, "new_name",
                                                                   "amount",
                                                                   44))
        self.assertEqual((TradeControl.get_instance()).get_store(self.__eytans_store).
                         get_inventory().get_amount("new_name"), 44)

        # All valid - owner - db_ tests
        self.assertTrue((TradeControl.get_instance()).edit_product(self.__eytans_store, "new_name",
                                                                   "price",
                                                                   12.44))
        self.assertEqual((TradeControl.get_instance()).get_store(self.__eytans_store).
                         get_product("new_name").get_price(), 12.44)

        (TradeControl.get_instance()).logout_subscriber()

        manager = User()
        manager.register("manager", "manager")
        store: Store = Store("myStore")
        (TradeControl.get_instance()).get_stores().append(store)
        # (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).register_guest(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners_appointments().append(
            StoreAppointment(None, self.__user, []))
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_INV])

        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])

        # All valid - owner - name
        self.assertTrue((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   "name",
                                                                   "new_name"))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product("new_name"))

        # Invalid - owner - name is only whitespaces
        self.assertFalse((TradeControl.get_instance()).edit_product(store.get_name(), "new_name",
                                                                    "name",
                                                                    "      ")['response'])
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product("      "))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product("new_name"))
        exist_product_as_dictionary = {"name": "Eagle's statue",
                                       "price": product.get_price(),
                                       "category": product.get_category(),
                                       "amount": 5,
                                       "purchase_type": 0}
        (TradeControl.get_instance()).add_products(store.get_name(), [exist_product_as_dictionary])

        # Invalid - owner - another product with the same name as the new name already exist
        self.assertFalse((TradeControl.get_instance()).edit_product(store.get_name(), "new_name",
                                                                    "name",
                                                                    exist_product_as_dictionary['name'])['response'])
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product(exist_product_as_dictionary['name']))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product("new_name"))

        product_as_dictionary = {"name": "new_name",
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5,
                                 "purchase_type": 0}

        # All valid - owner - price
        self.assertTrue((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   "price",
                                                                   21.12)['response'])
        self.assertEqual(21.12, (TradeControl.get_instance()).get_store(store.get_name()).get_product("new_name").
                         get_price())

        # Invalid - owner - price - negative price
        self.assertFalse((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                    "price",
                                                                    -31.12)['response'])
        self.assertEqual(21.12, (TradeControl.get_instance()).get_store(store.get_name()).get_product("new_name").
                         get_price())

        # Valid - owner - edge case - price = 0
        self.assertTrue((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   "price",
                                                                   0)['response'])
        self.assertEqual(0, (TradeControl.get_instance()).get_store(store.get_name()).get_product("new_name").
                         get_price())

        # Restore- price
        self.assertTrue((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   "price",
                                                                   21.12)['response'])
        self.assertEqual(21.12, (TradeControl.get_instance()).get_store(store.get_name()).get_product("new_name").
                         get_price())

        # All valid - owner - amount
        self.assertTrue((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   'amount',
                                                                   1986)['response'])
        self.assertEqual(1986, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount("new_name"))

        # Invalid - owner - amount
        self.assertFalse((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                    'amount',
                                                                    -16)['response'])
        self.assertEqual(1986, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount("new_name"))

        # All valid - owner - amount - Edge case - amount = 0
        self.assertTrue((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   'amount',
                                                                   0)['response'])
        self.assertEqual(0, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount("new_name"))

        # Restore - amount
        self.assertTrue((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   'amount',
                                                                   1986)['response'])
        self.assertEqual(1986, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount("new_name"))

        product_as_dictionary = {"name": "It's my life",
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5,
                                 "purchase_type": 0}
        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])

        # Invalid - store doesn't exist
        self.assertFalse(
            (TradeControl.get_instance()).edit_product("store.get_name()", product_as_dictionary['name'], "name",
                                                       "Never say goodbye")['response'])

        # Invalid - product doesn't exist
        self.assertFalse((TradeControl.get_instance()).edit_product(store.get_name(), "product.get_name()", "name",
                                                                    "Never say goodbye")['response'])
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product("Never say goodbye"))

        # valid - invalid op
        self.assertFalse((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                    "Bed of roses",
                                                                    "Always")['response'])
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product("Always"))

        store2: Store = Store("store2")
        (TradeControl.get_instance()).get_stores().append(store2)
        product_as_dictionary = {"name": "Born to be my baby",
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5,
                                 "purchase_type": 0}
        (TradeControl.get_instance()).register_guest(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).get_store(store2.get_name()).get_owners_appointments().append(
            StoreAppointment(None, self.__user, []))
        (TradeControl.get_instance()).get_store(store2.get_name()).add_manager(self.__user, manager,
                                                                               [ManagerPermission.EDIT_INV])
        (TradeControl.get_instance()).add_products(store2.get_name(), [product_as_dictionary])

        # Invalid - product exist in a different store.
        self.assertFalse(
            (TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'], "name",
                                                       "eytan")['response'])
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store2.get_name()).
                             get_product(product_as_dictionary['name']))

        (TradeControl.get_instance()).logout_subscriber()

        # Invalid - curr_user logged out
        self.assertFalse(
            (TradeControl.get_instance()).edit_product(store2.get_name(), product_as_dictionary['name'], "name",
                                                       "eytan")['response'])
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store2.get_name()).
                             get_product(product_as_dictionary['name']))

        # Clean all
        (TradeControl.get_instance()).__delete__()

        product = Product("Eytan's product", 12, "Eytan's category")
        product_as_dictionary = {"name": product.get_name(),
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5,
                                 "purchase_type": 0}

        manager = User()
        manager.register("manager", "manager")
        store: Store = Store("myStore")
        (TradeControl.get_instance()).get_stores().append(store)
        (TradeControl.get_instance()).register_guest(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners_appointments().append(
            StoreAppointment(None, self.__user, []))
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_INV])

        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])

        (TradeControl.get_instance()).register_guest(manager.get_nickname(), "manager")
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "manager")

        # All valid - manager - name
        self.assertTrue((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   "name",
                                                                   "new_name")['response'])
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product("new_name"))

        # Invalid - manager - name is only whitespaces
        self.assertFalse((TradeControl.get_instance()).edit_product(store.get_name(), "new_name",
                                                                    "name",
                                                                    "      ")['response'])
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product("      "))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product("new_name"))
        exist_product_as_dictionary = {"name": "Eagle's statue",
                                       "price": product.get_price(),
                                       "category": product.get_category(),
                                       "amount": 5,
                                       "purchase_type": 0}
        (TradeControl.get_instance()).add_products(store.get_name(), [exist_product_as_dictionary])

        # Invalid - manager - another product with the same name as the new name already exist
        self.assertFalse((TradeControl.get_instance()).edit_product(store.get_name(), "new_name",
                                                                    "name",
                                                                    exist_product_as_dictionary['name'])['response'])
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product(exist_product_as_dictionary['name']))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product("new_name"))

        product_as_dictionary = {"name": "new_name",
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5,
                                 "purchase_type": 0}

        # All valid - manager - price
        self.assertTrue((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   "price",
                                                                   21.12)['response'])
        self.assertEqual(21.12, (TradeControl.get_instance()).get_store(store.get_name()).get_product("new_name").
                         get_price())

        # Invalid - manager - price - negative price
        self.assertFalse((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                    "price",
                                                                    -31.12)['response'])
        self.assertEqual(21.12, (TradeControl.get_instance()).get_store(store.get_name()).get_product("new_name").
                         get_price())

        # Valid - manager - edge case - price = 0
        self.assertTrue((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   "price",
                                                                   0)['response'])
        self.assertEqual(0, (TradeControl.get_instance()).get_store(store.get_name()).get_product("new_name").
                         get_price())

        # Restore- price
        self.assertTrue((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   "price",
                                                                   21.12)['response'])
        self.assertEqual(21.12, (TradeControl.get_instance()).get_store(store.get_name()).get_product("new_name").
                         get_price())

        # All valid - manager - amount
        self.assertTrue((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   'amount',
                                                                   1986)['response'])
        self.assertEqual(1986, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount("new_name"))

        # Invalid - manager - amount
        self.assertFalse((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                    'amount',
                                                                    -16)['response'])
        self.assertEqual(1986, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount("new_name"))

        # All valid - manager - amount - Edge case - amount = 0
        self.assertTrue((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   'amount',
                                                                   0)['response'])
        self.assertEqual(0, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount("new_name"))

        # Restore - amount
        self.assertTrue((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   'amount',
                                                                   1986)['response'])
        self.assertEqual(1986, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount("new_name"))

        product_as_dictionary = {"name": "It's my life",
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5,
                                 "purchase_type": 0}
        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])

        # Invalid - store doesn't exist
        self.assertFalse(
            (TradeControl.get_instance()).edit_product("store.get_name()", product_as_dictionary['name'], "name",
                                                       "Never say goodbye")['response'])

        # Invalid - product doesn't exist
        self.assertFalse((TradeControl.get_instance()).edit_product(store.get_name(), "product.get_name()", "name",
                                                                    "Never say goodbye")['response'])
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product("Never say goodbye"))

        # valid - invalid op
        self.assertFalse((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                    "Bed of roses",
                                                                    "Always")['response'])
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product("Always"))

        store2: Store = Store("store2")
        (TradeControl.get_instance()).get_stores().append(store2)
        product_as_dictionary = {"name": "Born to be my baby",
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5,
                                 "purchase_type": 0}
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).get_store(store2.get_name()).get_owners_appointments().append(
            StoreAppointment(None, self.__user, []))
        (TradeControl.get_instance()).get_store(store2.get_name()).add_manager(self.__user, manager,
                                                                               [ManagerPermission.EDIT_INV])
        (TradeControl.get_instance()).add_products(store2.get_name(), [product_as_dictionary])

        # Invalid - product exist in a different store.
        self.assertFalse(
            (TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'], "name",
                                                       "eytan")['response'])
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store2.get_name()).
                             get_product(product_as_dictionary['name']))

        (TradeControl.get_instance()).logout_subscriber()

        # Invalid - curr_user logged out
        self.assertFalse(
            (TradeControl.get_instance()).edit_product(store2.get_name(), product_as_dictionary['name'], "name",
                                                       "eytan")['response'])
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store2.get_name()).
                             get_product(product_as_dictionary['name']))

        (TradeControl.get_instance()).get_store(store.get_name()). \
            edit_manager_permissions(self.__user, manager.get_nickname(), [ManagerPermission.USERS_QUESTIONS])

        # Invalid - manager doesn't have permissions
        self.assertFalse((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                    'amount',
                                                                    2000)['response'])
        self.assertEqual(1986, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount("new_name"))

        user = User()
        user.register("dry", "country")
        (TradeControl.get_instance()).logout_subscriber()
        (TradeControl.get_instance()).register_guest(user.get_nickname(), "country")
        (TradeControl.get_instance()).login_subscriber(user.get_nickname(), "country")

        # Invalid - not a manager or an owner
        self.assertFalse((TradeControl.get_instance()).edit_product(store.get_name(), product_as_dictionary['name'],
                                                                    'amount',
                                                                    2000)['response'])
        self.assertEqual(1986, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount("new_name"))

    def test_appoint_additional_owner(self):
        manager = User()
        manager.register("manager", "manager")
        store: Store = Store("myStore")
        # store.add_product("Eytan's product", 12, "Eytan's category", 5)
        (TradeControl.get_instance()).get_stores().append(store)
        (TradeControl.get_instance()).register_guest(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners_appointments().append(
            StoreAppointment(None, self.__user, []))
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_INV])

        new_owner = User()
        new_owner.register("I", "Owned this tests")
        (TradeControl.get_instance()).subscribe(new_owner)
        (TradeControl.get_instance()).subscribe(manager)

        # All valid
        self.assertTrue((TradeControl.get_instance()).appoint_additional_owner(new_owner.get_nickname(),
                                                                               store.get_name()))
        self.assertIn(new_owner, (TradeControl.get_instance()).get_store(store.get_name()).get_owners())

        # All valid - add a manager as an owner
        self.assertTrue((TradeControl.get_instance()).appoint_additional_owner(manager.get_nickname(),
                                                                               store.get_name()))
        self.assertIn(manager, (TradeControl.get_instance()).get_store(store.get_name()).get_owners())
        self.assertNotIn(manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        # Restore
        (TradeControl.get_instance()).remove_owner(manager.get_nickname(), store.get_name())

        # Invalid - new owner already an owner
        self.assertFalse((TradeControl.get_instance()).appoint_additional_owner(new_owner.get_nickname(),
                                                                                store.get_name())['response'])
        self.assertIn(new_owner, (TradeControl.get_instance()).get_store(store.get_name()).get_owners())

        # Restore
        (TradeControl.get_instance()).remove_owner(new_owner.get_nickname(), store.get_name())

        (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "country")

        # Invalid - appointer is not an owner
        self.assertFalse((TradeControl.get_instance()).appoint_additional_owner(new_owner.get_nickname(),
                                                                                store.get_name())['response'])
        self.assertNotIn(new_owner, (TradeControl.get_instance()).get_store(store.get_name()).get_owners())

        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).logout_subscriber()

        # Invalid - appointer is not logged in
        self.assertFalse((TradeControl.get_instance()).appoint_additional_owner(new_owner.get_nickname(),
                                                                                store.get_name())['response'])
        self.assertNotIn(new_owner, (TradeControl.get_instance()).get_store(store.get_name()).get_owners())

        # Restore
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)

        # Invalid - appointee doesn't exist
        self.assertFalse((TradeControl.get_instance()).appoint_additional_owner("new_owner.get_nickname()",
                                                                                store.get_name())['response'])

        # Invalid - store doesn't exist
        self.assertFalse((TradeControl.get_instance()).appoint_additional_owner(new_owner.get_nickname(),
                                                                                "store.get_name()")['response'])

        store2: Store = Store("Not store")
        store2.get_owners_appointments().append(StoreAppointment(self.__user, new_owner, []))

        # Valid - appointee owns another store
        self.assertTrue((TradeControl.get_instance()).appoint_additional_owner(new_owner.get_nickname(),
                                                                               store.get_name())['response'])
        self.assertIn(new_owner, (TradeControl.get_instance()).get_store(store.get_name()).get_owners())

    # @logger
    def test_appoint_store_manager(self):
        manager = User()
        manager.register("manager", "manager")
        store: Store = Store("myStore")
        # store.add_product("Eytan's product", 12, "Eytan's category", 5)
        (TradeControl.get_instance()).get_stores().append(store)
        (TradeControl.get_instance()).register_guest(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners_appointments().append(
            StoreAppointment(None, self.__user, []))
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_INV])

        new_manager = User()
        new_manager.register("I", "manage this tests")
        (TradeControl.get_instance()).subscribe(new_manager)
        (TradeControl.get_instance()).subscribe(manager)

        # All valid
        self.assertTrue((TradeControl.get_instance()).appoint_store_manager(new_manager.get_nickname(),
                                                                            store.get_name(),
                                                                            [ManagerPermission.WATCH_PURCHASE_HISTORY]))
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())
        self.assertTrue((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.WATCH_PURCHASE_HISTORY))

        # Invalid - new_manager is already a manager
        self.assertFalse((TradeControl.get_instance()).appoint_store_manager(new_manager.get_nickname(),
                                                                             store.get_name(),
                                                                             [ManagerPermission.USERS_QUESTIONS])[
                             'response'])
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())
        self.assertTrue((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.WATCH_PURCHASE_HISTORY))

        # Restore
        (TradeControl.get_instance()).get_store(store.get_name()).remove_manager(self.__user_nickname,
                                                                                 new_manager.get_nickname())

        (TradeControl.get_instance()).appoint_additional_owner(new_manager.get_nickname(), store.get_name())

        # Invalid - new manager is an owner
        self.assertFalse((TradeControl.get_instance()).appoint_store_manager(new_manager.get_nickname(),
                                                                             store.get_name(),
                                                                             [ManagerPermission.EDIT_INV])['response'])
        self.assertNotIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        # Restore
        (TradeControl.get_instance()).remove_owner(new_manager.get_nickname(), store.get_name())

        (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "country")

        # Invalid - appointer is a manager without permissions
        self.assertFalse((TradeControl.get_instance()).appoint_store_manager(new_manager.get_nickname(),
                                                                             store.get_name(),
                                                                             [ManagerPermission.DEL_OWNER])['response'])
        self.assertNotIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).logout_subscriber()

        # Invalid - appointer is not logged in
        self.assertFalse((TradeControl.get_instance()).appoint_store_manager(new_manager.get_nickname(),
                                                                             store.get_name(),
                                                                             [ManagerPermission.EDIT_INV])['response'])
        self.assertNotIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_owners())

        # Restore
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)

        # Invalid - appointee doesn't exist
        self.assertFalse((TradeControl.get_instance()).appoint_store_manager("new_manager.get_nickname()",
                                                                             store.get_name(),
                                                                             [ManagerPermission.DEL_OWNER])['response'])

        # Invalid - store doesn't exist
        self.assertFalse((TradeControl.get_instance()).appoint_store_manager(new_manager.get_nickname(),
                                                                             "store.get_name()",
                                                                             [ManagerPermission.EDIT_INV])['response'])

        # Valid - manager_permissions list is empty
        self.assertTrue((TradeControl.get_instance()).appoint_store_manager(new_manager.get_nickname(),
                                                                            store.get_name(),
                                                                            [])['response'])
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        # Restore
        (TradeControl.get_instance()).get_store(store.get_name()).remove_manager(self.__user_nickname,
                                                                                 new_manager.get_nickname())

        store2: Store = Store("Not store")
        store2.get_owners_appointments().append(StoreAppointment(None, self.__user, []))
        (TradeControl.get_instance()).get_stores().append(store2)
        (TradeControl.get_instance()).appoint_additional_owner(new_manager.get_nickname(), store2.get_name())

        # Valid - appointer manages another store
        self.assertTrue((TradeControl.get_instance()).appoint_store_manager(new_manager.get_nickname(),
                                                                            store.get_name(),
                                                                            [ManagerPermission.EDIT_INV])['response'])
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        # Clear
        (TradeControl.get_instance()).__delete__()

        # As a manager with permissions

        manager = User()
        manager.register("manager", "manager")
        (TradeControl.get_instance()).subscribe(manager)
        store: Store = Store("myStore")
        (TradeControl.get_instance()).get_stores().append(store)
        (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "manager")
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners_appointments().append(
            StoreAppointment(None, self.__user, []))
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.APPOINT_MANAGER])

        new_manager = User()
        new_manager.register("I", "manage this tests")
        (TradeControl.get_instance()).subscribe(new_manager)

        # All valid
        self.assertTrue((TradeControl.get_instance()).appoint_store_manager(new_manager.get_nickname(),
                                                                            store.get_name(),
                                                                            [ManagerPermission.WATCH_PURCHASE_HISTORY])[
                            'response'])
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())
        self.assertTrue((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.WATCH_PURCHASE_HISTORY))

        # Invalid - new_manager is already a manager
        self.assertFalse((TradeControl.get_instance()).appoint_store_manager(new_manager.get_nickname(),
                                                                             store.get_name(),
                                                                             [ManagerPermission.USERS_QUESTIONS])[
                             'response'])
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())
        self.assertTrue((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.WATCH_PURCHASE_HISTORY))

        # Restore
        (TradeControl.get_instance()).get_store(store.get_name()).remove_manager(self.__user_nickname,
                                                                                 new_manager.get_nickname())

        (TradeControl.get_instance()).register_guest(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).appoint_additional_owner(new_manager.get_nickname(), store.get_name())
        (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "manager")

        # Invalid - new manager is an owner
        self.assertFalse((TradeControl.get_instance()).appoint_store_manager(new_manager.get_nickname(),
                                                                             store.get_name(),
                                                                             [ManagerPermission.EDIT_INV])['response'])
        self.assertNotIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        # Restore
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)

        (TradeControl.get_instance()).remove_owner(new_manager.get_nickname(), store.get_name())

        (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).logout_subscriber()

        # Invalid - appointer is not logged in
        self.assertFalse((TradeControl.get_instance()).appoint_store_manager(new_manager.get_nickname(),
                                                                             store.get_name(),
                                                                             [ManagerPermission.EDIT_INV])['response'])
        self.assertNotIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        # Restore
        (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "manager")

        # Invalid - appointee doesn't exist
        self.assertFalse((TradeControl.get_instance()).appoint_store_manager("new_manager.get_nickname()",
                                                                             store.get_name(),
                                                                             [ManagerPermission.DEL_OWNER])['response'])

        # Invalid - store doesn't exist
        self.assertFalse((TradeControl.get_instance()).appoint_store_manager(new_manager.get_nickname(),
                                                                             "store.get_name()",
                                                                             [ManagerPermission.EDIT_INV])['response'])

        store2: Store = Store("Not store")
        store2.get_owners_appointments().append(StoreAppointment(None, self.__user, []))
        (TradeControl.get_instance()).get_stores().append(store2)
        (TradeControl.get_instance()).appoint_additional_owner(new_manager.get_nickname(), store2.get_name())

        # Valid - appointee manages another store
        self.assertTrue((TradeControl.get_instance()).appoint_store_manager(new_manager.get_nickname(),
                                                                            store.get_name(),
                                                                            [ManagerPermission.EDIT_INV])['response'])
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

    # @logger
    def test_edit_manager_permissions(self):
        manager = User()
        manager.register("manager", "manager")
        store: Store = Store("myStore")
        # store.add_product("Eytan's product", 12, "Eytan's category", 5)
        (TradeControl.get_instance()).get_stores().append(store)
        (TradeControl.get_instance()).register_guest(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners_appointments().append(
            StoreAppointment(None, self.__user, []))
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_INV])

        new_manager = User()
        new_manager.register("I", "manage this tests")
        new_owner = User()
        new_owner.register("Bed", "of roses")
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners_appointments().append(
            StoreAppointment(self.__user, new_owner, []))
        (TradeControl.get_instance()).subscribe(new_manager)
        (TradeControl.get_instance()).subscribe(manager)
        (TradeControl.get_instance()).appoint_store_manager(new_manager.get_nickname(),
                                                            store.get_name(),
                                                            [ManagerPermission.USERS_QUESTIONS])

        # All valid - new permissions is an empty list
        self.assertTrue((TradeControl.get_instance()).edit_manager_permissions(store.get_name(),
                                                                               new_manager.get_nickname(),
                                                                               []))
        self.assertFalse((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.USERS_QUESTIONS))

        # All valid - owner
        self.assertTrue((TradeControl.get_instance()).edit_manager_permissions(store.get_name(),
                                                                               new_manager.get_nickname(),
                                                                               [ManagerPermission.EDIT_MANAGER_PER]))
        self.assertTrue((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.EDIT_MANAGER_PER))

        # Invalid - store doesn't exist
        self.assertFalse((TradeControl.get_instance()).edit_manager_permissions("store.get_name()",
                                                                                new_manager.get_nickname(),
                                                                                [ManagerPermission.EDIT_INV]))

        # Invalid - manager doesn't exist
        self.assertFalse((TradeControl.get_instance()).edit_manager_permissions(store.get_name(),
                                                                                "new_manager.get_nickname()",
                                                                                [ManagerPermission.EDIT_INV]))

        # Clear all
        TradeControl.get_instance().__delete__()

        # Manager

        manager = User()
        manager.register("manager", "manager")
        store: Store = Store("myStore")
        # store.add_product("Eytan's product", 12, "Eytan's category", 5)
        (TradeControl.get_instance()).get_stores().append(store)
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners_appointments().append(
            StoreAppointment(None, self.__user, []))
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_MANAGER_PER,
                                                                               ManagerPermission.APPOINT_MANAGER])

        (TradeControl.get_instance()).register_guest(manager.get_nickname(), "manager")
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "manager")

        new_manager = User()
        new_manager.register("I", "manage this tests")
        new_owner = User()
        new_owner.register("Bed", "of roses")
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners_appointments().append(
            StoreAppointment(None, new_owner, []))
        (TradeControl.get_instance()).subscribe(new_manager)
        (TradeControl.get_instance()).subscribe(manager)
        (TradeControl.get_instance()).appoint_store_manager(new_manager.get_nickname(),
                                                            store.get_name(),
                                                            [ManagerPermission.USERS_QUESTIONS])

        # All valid - new permissions is an empty list
        self.assertTrue((TradeControl.get_instance()).edit_manager_permissions(store.get_name(),
                                                                               new_manager.get_nickname(),
                                                                               []))
        self.assertFalse((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.USERS_QUESTIONS))

        # All valid - manager
        self.assertTrue((TradeControl.get_instance()).edit_manager_permissions(store.get_name(),
                                                                               new_manager.get_nickname(),
                                                                               [ManagerPermission.EDIT_MANAGER_PER]))
        self.assertTrue((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.EDIT_MANAGER_PER))

        # Invalid - store doesn't exist
        self.assertFalse((TradeControl.get_instance()).edit_manager_permissions("store.get_name()",
                                                                                new_manager.get_nickname(),
                                                                                [ManagerPermission.EDIT_INV]))

        # Invalid - new manager doesn't exist
        self.assertFalse((TradeControl.get_instance()).edit_manager_permissions(store.get_name(),
                                                                                "new_manager.get_nickname()",
                                                                                [ManagerPermission.EDIT_INV]))

        (TradeControl.get_instance()).register_guest(new_owner.get_nickname(), "of roses")
        (TradeControl.get_instance()).login_subscriber(new_owner.get_nickname(), "of roses")

        # Invalid - the changer isn't the appointer
        self.assertFalse((TradeControl.get_instance()).edit_manager_permissions(store.get_name(),
                                                                                new_manager.get_nickname(),
                                                                                [ManagerPermission.DEL_OWNER]))
        self.assertTrue((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.EDIT_MANAGER_PER))
        self.assertFalse((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.DEL_OWNER))

        (TradeControl.get_instance()).register_guest(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).edit_manager_permissions(store.get_name(),
                                                               manager.get_nickname(),
                                                               [ManagerPermission.DEL_OWNER])

        (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "manager")

        # Invalid - manager doesn't have permissions
        self.assertFalse((TradeControl.get_instance()).edit_manager_permissions(store.get_name(),
                                                                                new_manager.get_nickname(),
                                                                                [ManagerPermission.DEL_OWNER]))
        self.assertTrue((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.EDIT_MANAGER_PER))
        self.assertFalse((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.DEL_OWNER))

        (TradeControl.get_instance()).logout_subscriber()

        # Invalid - manager doesn't login
        self.assertFalse((TradeControl.get_instance()).edit_manager_permissions(store.get_name(),
                                                                                new_manager.get_nickname(),
                                                                                [ManagerPermission.DEL_OWNER]))
        self.assertTrue((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.EDIT_MANAGER_PER))
        self.assertFalse((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.DEL_OWNER))

        user = User()
        user.register("I am", "just a user")
        (TradeControl.get_instance()).register_guest(user.get_nickname(), "just a user")
        (TradeControl.get_instance()).login_subscriber(user.get_nickname(), "just a user")

        # Invalid - not a manager or an owner
        self.assertFalse((TradeControl.get_instance()).edit_manager_permissions(store.get_name(),
                                                                                new_manager.get_nickname(),
                                                                                [
                                                                                    ManagerPermission.WATCH_PURCHASE_HISTORY]))
        self.assertTrue((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.EDIT_MANAGER_PER))
        self.assertFalse((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.WATCH_PURCHASE_HISTORY))

    # @logger
    def test_remove_manager(self):
        manager = User()
        manager.register("manager", "manager")
        store: Store = Store("myStore")
        # store.add_product("Eytan's product", 12, "Eytan's category", 5)
        (TradeControl.get_instance()).get_stores().append(store)
        (TradeControl.get_instance()).register_guest(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners_appointments().append(
            StoreAppointment(None, self.__user, []))
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_MANAGER_PER,
                                                                               ManagerPermission.APPOINT_MANAGER])

        new_manager = User()
        new_manager.register("I", "manage this tests")
        new_owner = User()
        new_owner.register("Bed", "of roses")
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners_appointments().append(
            StoreAppointment(self.__user, new_owner, []))
        (TradeControl.get_instance()).subscribe(new_manager)
        (TradeControl.get_instance()).subscribe(manager)
        (TradeControl.get_instance()).appoint_store_manager(new_manager.get_nickname(),
                                                            store.get_name(),
                                                            [ManagerPermission.USERS_QUESTIONS])

        # All valid
        self.assertTrue((TradeControl.get_instance()).remove_manager(store.get_name(), new_manager.get_nickname()))
        self.assertNotIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        # Invalid - manager doesn't exist
        self.assertFalse((TradeControl.get_instance()).remove_manager(store.get_name(), new_manager.get_nickname()))

        # Restore
        (TradeControl.get_instance()).appoint_store_manager(new_manager.get_nickname(),
                                                            store.get_name(),
                                                            [ManagerPermission.USERS_QUESTIONS])

        # Invalid - store doesn't exist
        self.assertFalse((TradeControl.get_instance()).remove_manager("store.get_name()", new_manager.get_nickname()))

        (TradeControl.get_instance()).logout_subscriber()

        # Invalid - curr_user is logged out
        self.assertFalse((TradeControl.get_instance()).remove_manager(store.get_name(), new_manager.get_nickname()))
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        (TradeControl.get_instance()).register_guest(new_owner.get_nickname(), "of roses")
        (TradeControl.get_instance()).login_subscriber(new_owner.get_nickname(), "of roses")

        # Invalid - the removing owner isn't the appointer
        self.assertFalse((TradeControl.get_instance()).remove_manager(store.get_name(), new_manager.get_nickname()))
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        # Clear all
        (TradeControl.get_instance()).__delete__()

        # Manager

        manager = User()
        manager.register("manager", "manager")
        store: Store = Store("myStore")
        # store.add_product("Eytan's product", 12, "Eytan's category", 5)
        (TradeControl.get_instance()).get_stores().append(store)
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners_appointments().append(
            StoreAppointment(None, self.__user, []))
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_MANAGER_PER,
                                                                               ManagerPermission.APPOINT_MANAGER,
                                                                               ManagerPermission.DEL_MANAGER])

        (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "manager")

        new_manager = User()
        new_manager.register("I", "manage this tests")
        new_owner = User()
        new_owner.register("Bed", "of roses")
        second_owner = User()
        second_owner.register("Bed2", "of roses")
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners_appointments().append(
            StoreAppointment(manager, new_owner, []))
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners_appointments().append(
            StoreAppointment(manager, second_owner, []))
        (TradeControl.get_instance()).register_guest("I", "manage this tests")
        (TradeControl.get_instance()).register_guest("Bed", "of roses")
        (TradeControl.get_instance()).register_guest("Bed2", "of roses")
        (TradeControl.get_instance()).login_subscriber("Bed", "of roses")

        # (TradeControl.get_instance()).subscribe(new_manager)
        # (TradeControl.get_instance()).subscribe(manager)
        (TradeControl.get_instance()).appoint_store_manager(new_manager.get_nickname(),
                                                            store.get_name(),
                                                            [ManagerPermission.USERS_QUESTIONS])

        # All valid
        self.assertTrue((TradeControl.get_instance()).remove_manager(store.get_name(), new_manager.get_nickname()))
        self.assertNotIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        # Invalid - removed manager doesn't exist
        self.assertFalse((TradeControl.get_instance()).remove_manager(store.get_name(), new_manager.get_nickname()))

        # Restore
        (TradeControl.get_instance()).appoint_store_manager(new_manager.get_nickname(),
                                                            store.get_name(),
                                                            [ManagerPermission.USERS_QUESTIONS])

        # Invalid - store doesn't exist
        self.assertFalse((TradeControl.get_instance()).remove_manager("store.get_name()", new_manager.get_nickname()))

        (TradeControl.get_instance()).logout_subscriber()

        # Invalid - curr_user is logged out
        self.assertFalse((TradeControl.get_instance()).remove_manager(store.get_name(), new_manager.get_nickname()))
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        (TradeControl.get_instance()).login_subscriber(second_owner.get_nickname(), "of roses")

        # Invalid - the removing owner isn't the appointer
        self.assertFalse((TradeControl.get_instance()).remove_manager(store.get_name(), new_manager.get_nickname()))
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())
        (TradeControl.get_instance()).logout_subscriber()

        user = User()
        user.register("I hate", "testing")
        # (TradeControl.get_instance()).set_curr_user(user)
        (TradeControl.get_instance()).register_guest(user.get_nickname(), "testing")
        (TradeControl.get_instance()).login_subscriber(user.get_nickname(), "testing")

        # Invalid - user isn't an owner or a manager
        self.assertFalse((TradeControl.get_instance()).remove_manager(store.get_name(), new_manager.get_nickname()))
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(self.__user_nickname, self.__user_password)
        (TradeControl.get_instance()).edit_manager_permissions(store.get_name(),
                                                               manager.get_nickname(),
                                                               [ManagerPermission.DEL_OWNER])

        (TradeControl.get_instance()).register_guest(manager.get_nickname(), "manager")
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "manager")

        # Invalid manager doesn't have permissions
        self.assertFalse((TradeControl.get_instance()).remove_manager(store.get_name(), new_manager.get_nickname()))
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

    def test_remove_owner(self):
        trade = (TradeControl.get_instance())
        owner1 = User()
        owner1.register("owner1", "password")
        owner1.login("owner1", "password")
        trade.set_curr_user(owner1)
        trade.open_store("myStore")
        trade.register_guest("manager1", "213456")
        trade.appoint_store_manager("manager1", "myStore", [])

        # failed - owner2 is not store owner
        trade.register_guest("owner2", "213456")
        res = trade.remove_owner("owner2", "myStore")
        self.assertEqual(res['response'], [])
        self.assertEqual(res['msg'], "Error! remove store owner failed.")

        # success
        trade.appoint_additional_owner("owner2", "myStore")
        owner2 = User()
        owner2.register("owner2", "password")
        owner2.login("owner2", "password")
        trade.set_curr_user(owner2)
        trade.register_guest("owner3", "213456")
        trade.appoint_additional_owner("owner3", "myStore")

        trade.register_guest("manager2", "213456")
        trade.appoint_store_manager("manager2", "myStore", [])

        owner3 = User()
        owner3.register("owner3", "password")
        owner3.login("owner3", "password")
        trade.set_curr_user(owner3)
        trade.register_guest("manager3", "213456")
        trade.appoint_store_manager("manager3", "myStore", [])

        trade.set_curr_user(owner1)
        res = trade.remove_owner("owner2", "myStore")
        self.assertEqual(res['response'], ['owner2 removed as owner', 'owner3 removed as owner',
                                           'manager3 removed as manager', 'manager2 removed as manager'])
        self.assertEqual(res['msg'], "Store owner owner2 and his appointees were removed successfully.")
        store = trade.get_store("myStore")
        self.assertTrue(store.is_manager("manager1"))
        self.assertFalse(store.is_manager("manager2"))
        self.assertFalse(store.is_manager("manager3"))
        self.assertTrue(store.is_owner("owner1"))
        self.assertFalse(store.is_owner("owner2"))
        self.assertFalse(store.is_owner("owner3"))

    def test_view_statistics(self):
        start_date = datetime(2020, 6, 5)
        end_date = datetime.today()
        trade_control: TradeControl = (TradeControl.get_instance())
        statistics = trade_control.get_visitors_cut(start_date, end_date)['response']
        self.assertTrue(len(statistics)== 1)
        self.assertTrue(statistics[0]['guests']== 0)
        self.assertTrue(statistics[0]['subscribers']== 0)
        self.assertTrue(statistics[0]['store_managers']== 0)
        self.assertTrue(statistics[0]['store_owners']== 0)
        self.assertTrue(statistics[0]['system_managers']== 0)

        trade_control.inc_todays_guests_counter()
        statistics = trade_control.get_visitors_cut(start_date, end_date)['response']
        self.assertTrue(len(statistics)== 1)
        self.assertTrue(statistics[0]['subscribers']== 0)
        self.assertTrue(statistics[0]['store_managers']== 0)
        self.assertTrue(statistics[0]['store_owners']== 0)
        self.assertTrue(statistics[0]['system_managers']== 0)
        self.assertTrue(statistics[0]['guests']== 1)

        # statistics[0].inc_subscribers_counter()
        # self.assertTrue(statistics[0].subscribers_amount(), 1)
        # statistics[0].inc_store_managers_counter()
        # self.assertTrue(statistics[0].store_managers_amount(), 1)
        # statistics[0].inc_store_owners_counter()
        # self.assertTrue(statistics[0].store_owners_amount(), 1)
        # statistics[0].inc_system_managers_counter()
        # self.assertTrue(statistics[0].system_managers_amount(), 1)

    def tearDown(self):
        (DataAccessFacade.get_instance()).delete_purchases()
        # (DataAccessFacade.get_instance()).delete_discount_policies()
        (DataAccessFacade.get_instance()).delete_statistics()
        (DataAccessFacade.get_instance()).delete_store_owner_appointments()
        (DataAccessFacade.get_instance()).delete_products_in_baskets()
        (DataAccessFacade.get_instance()).delete_products()
        (DataAccessFacade.get_instance()).delete_store_manager_appointments()
        (DataAccessFacade.get_instance()).delete_stores()
        (DataAccessFacade.get_instance()).delete_users()
        TradeControl.get_instance().__delete__()

    def __repr__(self):
        return repr("TradeControlTestCase")


if __name__ == '__main__':
    unittest.main()
