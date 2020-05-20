import unittest

import jsonpickle

from Backend.src.Logger import logger
from Backend.src.main.DomainLayer.StoreComponent.Product import Product
from Backend.src.main.DomainLayer.StoreComponent.Purchase import Purchase
from Backend.src.main.DomainLayer.StoreComponent.Store import Store
from Backend.src.main.DomainLayer.UserComponent.User import User
from Backend.src.main.ServiceLayer.StoreOwnerOrManagerRole import StoreOwnerOrManagerRole, TradeControl
from Backend.src.main.DomainLayer.StoreComponent.ManagerPermission import ManagerPermission


class StoreOwnerOrManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.__store_owner_or_manager_role: StoreOwnerOrManagerRole = StoreOwnerOrManagerRole()
        (TradeControl.get_instance()).register_guest("eytan", "eytan as password")
        (TradeControl.get_instance()).login_subscriber("eytan", "eytan as password")
        self.__user: User = (TradeControl.get_instance()).get_curr_user()
        (TradeControl.get_instance()).get_managers().append(self.__user)
        (TradeControl.get_instance()).open_store("eytan as store")
        self.__store: Store = (TradeControl.get_instance()).get_store("eytan as store")
        self.__store_owner_or_manager_role.add_products(self.__store.get_name(),
                                                        [{"name": "eytan",
                                                          "price": 12,
                                                          "category": "eytan as category",
                                                          "amount": 21}])

    def test_close_store(self):
        user = User()
        user_nickname = "Eytan"
        user_password = "Eytan's password"
        user.register(user_nickname, user_password)

        (TradeControl.get_instance()).set_curr_user(user)
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)
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

    @logger
    def test_add_products(self):
        (TradeControl.get_instance()).register_guest("eytan", "eytan as password")
        (TradeControl.get_instance()).login_subscriber("eytan", "eytan as password")
        user_nickname = "eytan"
        user_password = "eytan as password"
        product = Product("Eytan's product", 12, "Eytan's category")
        product_as_dictionary = {"name": product.get_name(),
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5}

        manager = User()
        manager.register("manager", "manager")
        store: Store = Store("myStore")
        # store.add_product("Eytan's product", 12, "Eytan's category", 5)
        (TradeControl.get_instance()).get_stores().append(store)
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners().append(self.__user)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners()
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_INV])

        lst = (TradeControl.get_instance()).get_store(store.get_name()).get_owners()

        # All valid - owner

        self.assertTrue(self.__store_owner_or_manager_role.add_products(store.get_name(), [product_as_dictionary]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).get_product(product.get_name()))
        self.assertEqual(5, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount(product.get_name()))

        product_as_dictionary = {"name": "N is for name",
                                 "price": 3,
                                 "category": "C is for category",
                                 "amount": 0}

        # All valid - owner -edge case -> amount = 0
        self.assertTrue(self.__store_owner_or_manager_role.add_products(store.get_name(), [product_as_dictionary]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product(product_as_dictionary['name']))
        self.assertEqual(0, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount(product_as_dictionary['name']))

        product_as_dictionary = {"name": "N is for No-way-in-hell-we-get-less-then-100",
                                 "price": 3,
                                 "category": "C is for category",
                                 "amount": -99}

        # Invalid - negative amount
        self.assertFalse(self.__store_owner_or_manager_role.add_products(store.get_name(), [product_as_dictionary]))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))

        product_as_dictionary = {"name": "N is for No-way-in-hell-we-get-less-then-100",
                                 "price": 3,
                                 "category": "C is for category",
                                 "amount": 99}

        # Invalid - store doesn't exist
        self.assertFalse(self.__store_owner_or_manager_role.add_products("store.get_name()", [product_as_dictionary]))

        (TradeControl.get_instance()).logout_subscriber()
        product_as_dictionary = {"name": "N is for Never said goodbye",
                                 "price": 3,
                                 "category": "C is for category",
                                 "amount": 15}

        # Invalid - curr_user is logged out
        self.assertFalse(self.__store_owner_or_manager_role.add_products(store.get_name(), [product_as_dictionary]))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))

        product_as_dictionary = {"name": product.get_name(),
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5}

        # All valid - Manager

        (TradeControl.get_instance()).set_curr_user(manager)
        TradeControl.get_instance().login_subscriber(manager.get_nickname(), "manager")

        # Test both manager and add to a product that already exist.
        self.assertTrue(self.__store_owner_or_manager_role.add_products(store.get_name(), [product_as_dictionary]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).get_product(product.get_name()))
        self.assertEqual(10, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount(product.get_name()))

        product_as_dictionary = {"name": "N is for name",
                                 "price": 3,
                                 "category": "C is for category",
                                 "amount": 0}

        # All valid - owner -edge case -> amount = 0
        self.assertTrue(self.__store_owner_or_manager_role.add_products(store.get_name(), [product_as_dictionary]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product(product_as_dictionary['name']))
        self.assertEqual(0, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount(product_as_dictionary['name']))

        product_as_dictionary = {"name": "N is for No-way-in-hell-we-get-less-then-100",
                                 "price": 3,
                                 "category": "C is for category",
                                 "amount": -99}

        # Invalid - negative amount
        self.assertFalse(self.__store_owner_or_manager_role.add_products(store.get_name(), [product_as_dictionary]))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))

        product_as_dictionary = {"name": "N is for No-way-in-hell-we-get-less-then-100",
                                 "price": 3,
                                 "category": "C is for category",
                                 "amount": 99}

        # Invalid - store doesn't exist
        self.assertFalse(self.__store_owner_or_manager_role.add_products("store.get_name()", [product_as_dictionary]))

        product_as_dictionary = {"name": "Name a better striker then RvP. I dare you.",
                                 "price": 3,
                                 "category": "C is for category",
                                 "amount": 99}
        (TradeControl.get_instance()).get_store(store.get_name()). \
            edit_manager_permissions(self.__user, manager.get_nickname(), [ManagerPermission.USERS_QUESTIONS])

        # Invalid- not right permissions:
        self.assertFalse(self.__store_owner_or_manager_role.add_products(store.get_name(), [product_as_dictionary]))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))

        (TradeControl.get_instance()).logout_subscriber()

        product_as_dictionary = {"name": "N is for Never said goodbye",
                                 "price": 3,
                                 "category": "C is for category",
                                 "amount": 15}

        # Invalid - curr_user is logged out
        self.assertFalse(self.__store_owner_or_manager_role.add_products(store.get_name(), [product_as_dictionary]))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))

        user1 = User()
        user1.register("dry", "country")
        (TradeControl.get_instance()).logout_subscriber()
        (TradeControl.get_instance()).set_curr_user(user1)
        (TradeControl.get_instance()).login_subscriber(user1.get_nickname(), "country")

        # Invalid - not a manager or a user
        self.assertFalse(self.__store_owner_or_manager_role.add_products(store.get_name(), [product_as_dictionary]))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))

    @logger
    def test_remove_products(self):
        (TradeControl.get_instance()).register_guest("eytan", "eytan as password")
        (TradeControl.get_instance()).login_subscriber("eytan", "eytan as password")
        user_nickname = "eytan"
        user_password = "eytan as password"
        product = Product("Eytan's product", 12, "Eytan's category")
        product_as_dictionary = {"name": product.get_name(),
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5}

        manager = User()
        manager.register("manager", "manager")
        store: Store = Store("myStore")
        (TradeControl.get_instance()).get_stores().append(store)
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners().append(self.__user)
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_INV])

        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])

        # All valid - owner - one product
        self.assertTrue(
            self.__store_owner_or_manager_role.remove_products(store.get_name(), [product_as_dictionary['name']]
                                                               ))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))

        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])
        product_as_dictionary2 = {"name": "I'll be there for you",
                                  "price": product.get_price(),
                                  "category": product.get_category(),
                                  "amount": 5}
        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary2])

        # All valid - owner - two products
        self.assertTrue(
            self.__store_owner_or_manager_role.remove_products(store.get_name(), [product_as_dictionary['name'],
                                                                                  product_as_dictionary2['name']]
                                                               ))
        lst = [e for e in (TradeControl.get_instance()).get_products_by(2, "") if e['store_name'] == store.get_name()]
        self.assertEqual(0, len(lst))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary2['name']))

        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])
        product_as_dictionary2 = {"name": "I'll be there for you",
                                  "price": product.get_price(),
                                  "category": product.get_category(),
                                  "amount": 5}
        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary2])

        # All valid - owner - two products
        self.assertTrue(
            self.__store_owner_or_manager_role.remove_products(store.get_name(), [product_as_dictionary['name']]
                                                               ))
        lst = [e for e in (TradeControl.get_instance()).get_products_by(2, "") if e['store_name'] == store.get_name()]
        self.assertEqual(1, len(lst))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product(product_as_dictionary2['name']))

        product_as_dictionary = {"name": "It's my life",
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5}
        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])

        # Invalid - store doesn't exist
        self.assertFalse(
            self.__store_owner_or_manager_role.remove_products("store.get_name()", [product_as_dictionary['name']]))

        # Invalid - product doesn't exist
        self.assertFalse(self.__store_owner_or_manager_role.remove_products(store.get_name(), ["product.get_name()"]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product(product_as_dictionary['name']))

        # valid - empty list
        self.assertTrue(self.__store_owner_or_manager_role.remove_products(store.get_name(), []))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product(product_as_dictionary['name']))

        (TradeControl.get_instance()).logout_subscriber()

        store2: Store = Store("store2")
        (TradeControl.get_instance()).get_stores().append(store2)
        product_as_dictionary = {"name": "Born to be my baby",
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5}
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)
        (TradeControl.get_instance()).get_store(store2.get_name()).get_owners().append(self.__user)
        (TradeControl.get_instance()).get_store(store2.get_name()).add_manager(self.__user, manager,
                                                                               [ManagerPermission.EDIT_INV])
        (TradeControl.get_instance()).add_products(store2.get_name(), [product_as_dictionary])

        # Invalid - product exist in a different store.
        self.assertFalse(
            self.__store_owner_or_manager_role.remove_products(store.get_name(), [product_as_dictionary['name']]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store2.get_name()).
                             get_product(product_as_dictionary['name']))

        # Invalid - curr_user logged out
        self.assertFalse(
            self.__store_owner_or_manager_role.remove_products(store.get_name(), [product_as_dictionary['name']]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store2.get_name()).
                             get_product(product_as_dictionary['name']))

        # Clean all
        (TradeControl.get_instance()).__delete__()

        product = Product("Eytan's product", 12, "Eytan's category")
        product_as_dictionary = {"name": product.get_name(),
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5}

        manager = User()
        manager.register("manager", "manager")
        store: Store = Store("myStore")
        (TradeControl.get_instance()).get_stores().append(store)
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners().append(self.__user)
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_INV])
        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])
        (TradeControl.get_instance()).logout_subscriber()
        (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "manager")

        # All valid - manager - one product
        self.assertTrue(
            self.__store_owner_or_manager_role.remove_products(store.get_name(), [product_as_dictionary['name']]
                                                               ))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))

        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])
        product_as_dictionary2 = {"name": "I'll be there for you",
                                  "price": product.get_price(),
                                  "category": product.get_category(),
                                  "amount": 5}
        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary2])

        # All valid - manager - two products
        self.assertTrue(
            self.__store_owner_or_manager_role.remove_products(store.get_name(), [product_as_dictionary['name'],
                                                                                  product_as_dictionary2['name']]
                                                               ))
        lst = [e for e in (TradeControl.get_instance()).get_products_by(2, "") if e['store_name'] == store.get_name()]
        self.assertEqual(0, len(lst))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary2['name']))

        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])
        product_as_dictionary2 = {"name": "I'll be there for you",
                                  "price": product.get_price(),
                                  "category": product.get_category(),
                                  "amount": 5}
        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary2])

        # All valid - manager - two products
        self.assertTrue(
            self.__store_owner_or_manager_role.remove_products(store.get_name(), [product_as_dictionary['name']]
                                                               ))
        lst = [e for e in (TradeControl.get_instance()).get_products_by(2, "") if e['store_name'] == store.get_name()]
        self.assertEqual(1, len(lst))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product(product_as_dictionary2['name']))

        product_as_dictionary = {"name": "It's my life",
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5}
        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])

        # Invalid - store doesn't exist
        self.assertFalse(
            self.__store_owner_or_manager_role.remove_products("store.get_name()", [product_as_dictionary['name']]))

        # Invalid - product doesn't exist
        self.assertFalse(self.__store_owner_or_manager_role.remove_products(store.get_name(), ["product.get_name()"]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product(product_as_dictionary['name']))

        # valid - empty list
        self.assertTrue(self.__store_owner_or_manager_role.remove_products(store.get_name(), []))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product(product_as_dictionary['name']))

        store2: Store = Store("store2")
        (TradeControl.get_instance()).get_stores().append(store2)

        product_as_dictionary = {"name": "Born to be my baby",
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5}
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)
        (TradeControl.get_instance()).get_store(store2.get_name()).get_owners().append(self.__user)
        (TradeControl.get_instance()).get_store(store2.get_name()).add_manager(self.__user, manager,
                                                                               [ManagerPermission.EDIT_INV])
        (TradeControl.get_instance()).add_products(store2.get_name(), [product_as_dictionary])

        (TradeControl.get_instance()).logout_subscriber()
        (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "country")

        # Invalid - product exist in a different store.
        self.assertFalse(
            self.__store_owner_or_manager_role.remove_products(store.get_name(), [product_as_dictionary['name']]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store2.get_name()).
                             get_product(product_as_dictionary['name']))

        (TradeControl.get_instance()).get_store(store2.get_name()). \
            edit_manager_permissions(self.__user, manager.get_nickname(), [ManagerPermission.USERS_QUESTIONS])

        # Invalid - manager doesn't have permissions
        self.assertFalse(
            self.__store_owner_or_manager_role.remove_products(store2.get_name(), [product_as_dictionary['name']]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store2.get_name()).
                             get_product(product_as_dictionary['name']))

        (TradeControl.get_instance()).logout_subscriber()

        # Invalid - curr_user logged out
        self.assertFalse(
            self.__store_owner_or_manager_role.remove_products(store2.get_name(), [product_as_dictionary['name']]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store2.get_name()).
                             get_product(product_as_dictionary['name']))

        user = User()
        user.register("dry", "country")
        (TradeControl.get_instance()).logout_subscriber()
        (TradeControl.get_instance()).set_curr_user(user)
        (TradeControl.get_instance()).login_subscriber(user.get_nickname(), "country")

        # Invalid - not a manager or a user
        self.assertFalse(
            self.__store_owner_or_manager_role.remove_products(store.get_name(), [product_as_dictionary['name']]))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store2.get_name()).
                             get_product(product_as_dictionary['name']))

    @logger
    def test_edit_product(self):
        (TradeControl.get_instance()).register_guest("eytan", "eytan as password")
        (TradeControl.get_instance()).login_subscriber("eytan", "eytan as password")
        user_nickname = "eytan"
        user_password = "eytan as password"
        product = Product("Eytan's product", 12, "Eytan's category")
        product_as_dictionary = {"name": product.get_name(),
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5}

        manager = User()
        manager.register("manager", "manager")
        store: Store = Store("myStore")
        (TradeControl.get_instance()).get_stores().append(store)
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners().append(self.__user)
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_INV])

        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])

        # All valid - owner - name
        self.assertTrue(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   "name",
                                                                   "new_name"))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product("new_name"))

        # Invalid - owner - name is only whitespaces
        self.assertFalse(self.__store_owner_or_manager_role.edit_product(store.get_name(), "new_name",
                                                                    "name",
                                                                    "      "))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product("      "))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product("new_name"))
        exist_product_as_dictionary = {"name": "Eagle's statue",
                                       "price": product.get_price(),
                                       "category": product.get_category(),
                                       "amount": 5}
        (TradeControl.get_instance()).add_products(store.get_name(), [exist_product_as_dictionary])

        # Invalid - owner - another product with the same name as the new name already exist
        self.assertFalse(self.__store_owner_or_manager_role.edit_product(store.get_name(), "new_name",
                                                                    "name",
                                                                    exist_product_as_dictionary['name']))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product(exist_product_as_dictionary['name']))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product("new_name"))

        product_as_dictionary = {"name": "new_name",
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5}

        # All valid - owner - price
        self.assertTrue(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   "price",
                                                                   21.12))
        self.assertEqual(21.12, (TradeControl.get_instance()).get_store(store.get_name()).get_product("new_name").
                         get_price())

        # Invalid - owner - price - negative price
        self.assertFalse(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                    "price",
                                                                    -31.12))
        self.assertEqual(21.12, (TradeControl.get_instance()).get_store(store.get_name()).get_product("new_name").
                         get_price())

        # Valid - owner - edge case - price = 0
        self.assertTrue(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   "price",
                                                                   0))
        self.assertEqual(0, (TradeControl.get_instance()).get_store(store.get_name()).get_product("new_name").
                         get_price())

        # Restore- price
        self.assertTrue(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   "price",
                                                                   21.12))
        self.assertEqual(21.12, (TradeControl.get_instance()).get_store(store.get_name()).get_product("new_name").
                         get_price())

        # All valid - owner - amount
        self.assertTrue(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   'amount',
                                                                   1986))
        self.assertEqual(1986, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount("new_name"))

        # Invalid - owner - amount
        self.assertFalse(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                    'amount',
                                                                    -16))
        self.assertEqual(1986, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount("new_name"))

        # All valid - owner - amount - Edge case - amount = 0
        self.assertTrue(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   'amount',
                                                                   0))
        self.assertEqual(0, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount("new_name"))

        # Restore - amount
        self.assertTrue(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   'amount',
                                                                   1986))
        self.assertEqual(1986, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount("new_name"))

        product_as_dictionary = {"name": "It's my life",
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5}
        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])

        # Invalid - store doesn't exist
        self.assertFalse(
            self.__store_owner_or_manager_role.edit_product("store.get_name()", product_as_dictionary['name'], "name",
                                                       "Never say goodbye"))

        # Invalid - product doesn't exist
        self.assertFalse(self.__store_owner_or_manager_role.edit_product(store.get_name(), "product.get_name()", "name",
                                                                    "Never say goodbye"))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product("Never say goodbye"))

        # valid - invalid op
        self.assertFalse(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                    "Bed of roses",
                                                                    "Always"))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product("Always"))

        store2: Store = Store("store2")
        (TradeControl.get_instance()).get_stores().append(store2)
        product_as_dictionary = {"name": "Born to be my baby",
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5}
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)
        (TradeControl.get_instance()).get_store(store2.get_name()).get_owners().append(self.__user)
        (TradeControl.get_instance()).get_store(store2.get_name()).add_manager(self.__user, manager,
                                                                               [ManagerPermission.EDIT_INV])
        (TradeControl.get_instance()).add_products(store2.get_name(), [product_as_dictionary])

        # Invalid - product exist in a different store.
        self.assertFalse(
            self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'], "name",
                                                       "eytan"))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store2.get_name()).
                             get_product(product_as_dictionary['name']))

        (TradeControl.get_instance()).logout_subscriber()

        # Invalid - curr_user logged out
        self.assertFalse(
            self.__store_owner_or_manager_role.edit_product(store2.get_name(), product_as_dictionary['name'], "name",
                                                       "eytan"))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store2.get_name()).
                             get_product(product_as_dictionary['name']))

        # Clean all
        (TradeControl.get_instance()).__delete__()

        product = Product("Eytan's product", 12, "Eytan's category")
        product_as_dictionary = {"name": product.get_name(),
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5}

        manager = User()
        manager.register("manager", "manager")
        store: Store = Store("myStore")
        (TradeControl.get_instance()).get_stores().append(store)
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners().append(self.__user)
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_INV])

        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])

        (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "manager")

        # All valid - manager - name
        self.assertTrue(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   "name",
                                                                   "new_name"))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product(product_as_dictionary['name']))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product("new_name"))

        # Invalid - manager - name is only whitespaces
        self.assertFalse(self.__store_owner_or_manager_role.edit_product(store.get_name(), "new_name",
                                                                    "name",
                                                                    "      "))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product("      "))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product("new_name"))
        exist_product_as_dictionary = {"name": "Eagle's statue",
                                       "price": product.get_price(),
                                       "category": product.get_category(),
                                       "amount": 5}
        (TradeControl.get_instance()).add_products(store.get_name(), [exist_product_as_dictionary])

        # Invalid - manager - another product with the same name as the new name already exist
        self.assertFalse(self.__store_owner_or_manager_role.edit_product(store.get_name(), "new_name",
                                                                    "name",
                                                                    exist_product_as_dictionary['name']))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product(exist_product_as_dictionary['name']))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store.get_name()).
                             get_product("new_name"))

        product_as_dictionary = {"name": "new_name",
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5}

        # All valid - manager - price
        self.assertTrue(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   "price",
                                                                   21.12))
        self.assertEqual(21.12, (TradeControl.get_instance()).get_store(store.get_name()).get_product("new_name").
                         get_price())

        # Invalid - manager - price - negative price
        self.assertFalse(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                    "price",
                                                                    -31.12))
        self.assertEqual(21.12, (TradeControl.get_instance()).get_store(store.get_name()).get_product("new_name").
                         get_price())

        # Valid - manager - edge case - price = 0
        self.assertTrue(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   "price",
                                                                   0))
        self.assertEqual(0, (TradeControl.get_instance()).get_store(store.get_name()).get_product("new_name").
                         get_price())

        # Restore- price
        self.assertTrue(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   "price",
                                                                   21.12))
        self.assertEqual(21.12, (TradeControl.get_instance()).get_store(store.get_name()).get_product("new_name").
                         get_price())

        # All valid - manager - amount
        self.assertTrue(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   'amount',
                                                                   1986))
        self.assertEqual(1986, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount("new_name"))

        # Invalid - manager - amount
        self.assertFalse(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                    'amount',
                                                                    -16))
        self.assertEqual(1986, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount("new_name"))

        # All valid - manager - amount - Edge case - amount = 0
        self.assertTrue(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   'amount',
                                                                   0))
        self.assertEqual(0, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount("new_name"))

        # Restore - amount
        self.assertTrue(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                   'amount',
                                                                   1986))
        self.assertEqual(1986, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount("new_name"))

        product_as_dictionary = {"name": "It's my life",
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5}
        (TradeControl.get_instance()).add_products(store.get_name(), [product_as_dictionary])

        # Invalid - store doesn't exist
        self.assertFalse(
            self.__store_owner_or_manager_role.edit_product("store.get_name()", product_as_dictionary['name'], "name",
                                                       "Never say goodbye"))

        # Invalid - product doesn't exist
        self.assertFalse(self.__store_owner_or_manager_role.edit_product(store.get_name(), "product.get_name()", "name",
                                                                    "Never say goodbye"))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product("Never say goodbye"))

        # valid - invalid op
        self.assertFalse(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                    "Bed of roses",
                                                                    "Always"))
        self.assertIsNone((TradeControl.get_instance()).get_store(store.get_name()).
                          get_product("Always"))

        store2: Store = Store("store2")
        (TradeControl.get_instance()).get_stores().append(store2)
        product_as_dictionary = {"name": "Born to be my baby",
                                 "price": product.get_price(),
                                 "category": product.get_category(),
                                 "amount": 5}
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)
        (TradeControl.get_instance()).get_store(store2.get_name()).get_owners().append(self.__user)
        (TradeControl.get_instance()).get_store(store2.get_name()).add_manager(self.__user, manager,
                                                                               [ManagerPermission.EDIT_INV])
        (TradeControl.get_instance()).add_products(store2.get_name(), [product_as_dictionary])

        # Invalid - product exist in a different store.
        self.assertFalse(
            self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'], "name",
                                                       "eytan"))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store2.get_name()).
                             get_product(product_as_dictionary['name']))

        (TradeControl.get_instance()).logout_subscriber()

        # Invalid - curr_user logged out
        self.assertFalse(
            self.__store_owner_or_manager_role.edit_product(store2.get_name(), product_as_dictionary['name'], "name",
                                                       "eytan"))
        self.assertIsNotNone((TradeControl.get_instance()).get_store(store2.get_name()).
                             get_product(product_as_dictionary['name']))

        (TradeControl.get_instance()).get_store(store.get_name()). \
            edit_manager_permissions(self.__user, manager.get_nickname(), [ManagerPermission.USERS_QUESTIONS])

        # Invalid - manager doesn't have permissions
        self.assertFalse(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                    'amount',
                                                                    2000))
        self.assertEqual(1986, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount("new_name"))

        user = User()
        user.register("dry", "country")
        (TradeControl.get_instance()).logout_subscriber()
        (TradeControl.get_instance()).set_curr_user(user)
        (TradeControl.get_instance()).login_subscriber(user.get_nickname(), "country")

        # Invalid - not a manager or an owner
        self.assertFalse(self.__store_owner_or_manager_role.edit_product(store.get_name(), product_as_dictionary['name'],
                                                                    'amount',
                                                                    2000))
        self.assertEqual(1986, (TradeControl.get_instance()).get_store(store.get_name()).get_inventory().
                         get_amount("new_name"))


    @logger
    def test_appoint_additional_owner(self):
        (TradeControl.get_instance()).register_guest("eytan", "eytan as password")
        (TradeControl.get_instance()).login_subscriber("eytan", "eytan as password")
        user_nickname = "eytan"
        user_password = "eytan as password"
        manager = User()
        manager.register("manager", "manager")
        store: Store = Store("myStore")
        # store.add_product("Eytan's product", 12, "Eytan's category", 5)
        (TradeControl.get_instance()).get_stores().append(store)
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners().append(self.__user)
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_INV])

        new_owner = User()
        new_owner.register("I", "Owned this tests")
        (TradeControl.get_instance()).subscribe(new_owner)
        (TradeControl.get_instance()).subscribe(manager)

        # All valid
        self.assertTrue(self.__store_owner_or_manager_role.appoint_additional_owner(new_owner.get_nickname(),
                                                                               store.get_name()))
        self.assertIn(new_owner, (TradeControl.get_instance()).get_store(store.get_name()).get_owners())

        # All valid - add a manager as an owner
        self.assertTrue(self.__store_owner_or_manager_role.appoint_additional_owner(manager.get_nickname(),
                                                                               store.get_name()))
        self.assertIn(manager, (TradeControl.get_instance()).get_store(store.get_name()).get_owners())
        self.assertNotIn(manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        # Restore
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners().remove(manager)

        # Invalid - new owner already an owner
        self.assertFalse(self.__store_owner_or_manager_role.appoint_additional_owner(new_owner.get_nickname(),
                                                                                store.get_name()))
        self.assertIn(new_owner, (TradeControl.get_instance()).get_store(store.get_name()).get_owners())

        # Restore
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners().remove(new_owner)

        (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "country")

        # Invalid - appointer is not an owner
        self.assertFalse(self.__store_owner_or_manager_role.appoint_additional_owner(new_owner.get_nickname(),
                                                                                store.get_name()))
        self.assertNotIn(new_owner, (TradeControl.get_instance()).get_store(store.get_name()).get_owners())

        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).logout_subscriber()

        # Invalid - appointer is not logged in
        self.assertFalse(self.__store_owner_or_manager_role.appoint_additional_owner(new_owner.get_nickname(),
                                                                                store.get_name()))
        self.assertNotIn(new_owner, (TradeControl.get_instance()).get_store(store.get_name()).get_owners())

        # Restore
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)

        # Invalid - appointee doesn't exist
        self.assertFalse(self.__store_owner_or_manager_role.appoint_additional_owner("new_owner.get_nickname()",
                                                                                store.get_name()))

        # Invalid - store doesn't exist
        self.assertFalse(self.__store_owner_or_manager_role.appoint_additional_owner(new_owner.get_nickname(),
                                                                                "store.get_name()"))

        store2: Store = Store("Not store")
        store2.get_owners().append(new_owner)

        # Valid - appointee owns another store
        self.assertTrue(self.__store_owner_or_manager_role.appoint_additional_owner(new_owner.get_nickname(),
                                                                               store.get_name()))
        self.assertIn(new_owner, (TradeControl.get_instance()).get_store(store.get_name()).get_owners())

    @logger
    def test_appoint_store_manager(self):
        (TradeControl.get_instance()).register_guest("eytan", "eytan as password")
        (TradeControl.get_instance()).login_subscriber("eytan", "eytan as password")
        user_nickname = "eytan"
        user_password = "eytan as password"
        manager = User()
        manager.register("manager", "manager")
        store: Store = Store("myStore")
        # store.add_product("Eytan's product", 12, "Eytan's category", 5)
        (TradeControl.get_instance()).get_stores().append(store)
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners().append(self.__user)
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_INV])

        new_manager = User()
        new_manager.register("I", "manage this tests")
        (TradeControl.get_instance()).subscribe(new_manager)
        (TradeControl.get_instance()).subscribe(manager)

        # All valid
        self.assertTrue(self.__store_owner_or_manager_role.appoint_store_manager(new_manager.get_nickname(),
                                                                            store.get_name(),
                                                                            [ManagerPermission.WATCH_PURCHASE_HISTORY]))
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())
        self.assertTrue((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.WATCH_PURCHASE_HISTORY))

        # Invalid - new_manager is already a manager
        self.assertFalse(self.__store_owner_or_manager_role.appoint_store_manager(new_manager.get_nickname(),
                                                                             store.get_name(),
                                                                             [ManagerPermission.USERS_QUESTIONS]))
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())
        self.assertTrue((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.WATCH_PURCHASE_HISTORY))

        # Restore
        (TradeControl.get_instance()).get_store(store.get_name()).remove_manager(user_nickname,
                                                                                 new_manager.get_nickname())

        (TradeControl.get_instance()).appoint_additional_owner(new_manager.get_nickname(), store.get_name())

        # Invalid - new manager is an owner
        self.assertFalse(self.__store_owner_or_manager_role.appoint_store_manager(new_manager.get_nickname(),
                                                                             store.get_name(),
                                                                             [ManagerPermission.EDIT_INV]))
        self.assertNotIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        # Restore
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners().remove(new_manager)

        (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "country")

        # Invalid - appointer is a manager without permissions
        self.assertFalse(self.__store_owner_or_manager_role.appoint_store_manager(new_manager.get_nickname(),
                                                                             store.get_name(),
                                                                             [ManagerPermission.DEL_OWNER]))
        self.assertNotIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).logout_subscriber()

        # Invalid - appointer is not logged in
        self.assertFalse(self.__store_owner_or_manager_role.appoint_store_manager(new_manager.get_nickname(),
                                                                             store.get_name(),
                                                                             [ManagerPermission.EDIT_INV]))
        self.assertNotIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_owners())

        # Restore
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)

        # Invalid - appointee doesn't exist
        self.assertFalse(self.__store_owner_or_manager_role.appoint_store_manager("new_manager.get_nickname()",
                                                                             store.get_name(),
                                                                             [ManagerPermission.DEL_OWNER]))

        # Invalid - store doesn't exist
        self.assertFalse(self.__store_owner_or_manager_role.appoint_store_manager(new_manager.get_nickname(),
                                                                             "store.get_name()",
                                                                             [ManagerPermission.EDIT_INV]))

        # Valid - manager_permissions list is empty
        self.assertTrue(self.__store_owner_or_manager_role.appoint_store_manager(new_manager.get_nickname(),
                                                                            store.get_name(),
                                                                            []))
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        # Restore
        (TradeControl.get_instance()).get_store(store.get_name()).remove_manager(user_nickname,
                                                                                 new_manager.get_nickname())

        store2: Store = Store("Not store")
        store2.get_owners().append(self.__user)
        (TradeControl.get_instance()).get_stores().append(store2)
        (TradeControl.get_instance()).appoint_additional_owner(new_manager.get_nickname(), store2.get_name())

        # Valid - appointer manages another store
        self.assertTrue(self.__store_owner_or_manager_role.appoint_store_manager(new_manager.get_nickname(),
                                                                            store.get_name(),
                                                                            [ManagerPermission.EDIT_INV]))
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
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners().append(self.__user)
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.APPOINT_MANAGER])

        new_manager = User()
        new_manager.register("I", "manage this tests")
        (TradeControl.get_instance()).subscribe(new_manager)

        # All valid
        self.assertTrue(self.__store_owner_or_manager_role.appoint_store_manager(new_manager.get_nickname(),
                                                                            store.get_name(),
                                                                            [ManagerPermission.WATCH_PURCHASE_HISTORY]))
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())
        self.assertTrue((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.WATCH_PURCHASE_HISTORY))

        # Invalid - new_manager is already a manager
        self.assertFalse(self.__store_owner_or_manager_role.appoint_store_manager(new_manager.get_nickname(),
                                                                             store.get_name(),
                                                                             [ManagerPermission.USERS_QUESTIONS]))
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())
        self.assertTrue((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.WATCH_PURCHASE_HISTORY))

        # Restore
        (TradeControl.get_instance()).get_store(store.get_name()).remove_manager(user_nickname,
                                                                                 new_manager.get_nickname())

        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)
        (TradeControl.get_instance()).appoint_additional_owner(new_manager.get_nickname(), store.get_name())
        (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "manager")

        # Invalid - new manager is an owner
        self.assertFalse(self.__store_owner_or_manager_role.appoint_store_manager(new_manager.get_nickname(),
                                                                             store.get_name(),
                                                                             [ManagerPermission.EDIT_INV]))
        self.assertNotIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        # Restore
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners().remove(new_manager)

        (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).logout_subscriber()

        # Invalid - appointer is not logged in
        self.assertFalse(self.__store_owner_or_manager_role.appoint_store_manager(new_manager.get_nickname(),
                                                                             store.get_name(),
                                                                             [ManagerPermission.EDIT_INV]))
        self.assertNotIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        # Restore
        (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "manager")

        # Invalid - appointee doesn't exist
        self.assertFalse(self.__store_owner_or_manager_role.appoint_store_manager("new_manager.get_nickname()",
                                                                             store.get_name(),
                                                                             [ManagerPermission.DEL_OWNER]))

        # Invalid - store doesn't exist
        self.assertFalse(self.__store_owner_or_manager_role.appoint_store_manager(new_manager.get_nickname(),
                                                                             "store.get_name()",
                                                                             [ManagerPermission.EDIT_INV]))

        store2: Store = Store("Not store")
        store2.get_owners().append(self.__user)
        (TradeControl.get_instance()).get_stores().append(store2)
        (TradeControl.get_instance()).appoint_additional_owner(new_manager.get_nickname(), store2.get_name())

        # Valid - appointee manages another store
        self.assertTrue(self.__store_owner_or_manager_role.appoint_store_manager(new_manager.get_nickname(),
                                                                            store.get_name(),
                                                                            [ManagerPermission.EDIT_INV]))
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

    @logger
    def test_edit_manager_permissions(self):
        (TradeControl.get_instance()).register_guest("eytan", "eytan as password")
        (TradeControl.get_instance()).login_subscriber("eytan", "eytan as password")
        user_nickname = "eytan"
        user_password = "eytan as password"
        manager = User()
        manager.register("manager", "manager")
        store: Store = Store("myStore")
        # store.add_product("Eytan's product", 12, "Eytan's category", 5)
        (TradeControl.get_instance()).get_stores().append(store)
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners().append(self.__user)
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_INV])

        new_manager = User()
        new_manager.register("I", "manage this tests")
        new_owner = User()
        new_owner.register("Bed", "of roses")
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners().append(new_owner)
        (TradeControl.get_instance()).subscribe(new_manager)
        (TradeControl.get_instance()).subscribe(manager)
        self.__store_owner_or_manager_role.appoint_store_manager(new_manager.get_nickname(),
                                                            store.get_name(),
                                                            [ManagerPermission.USERS_QUESTIONS])

        # All valid - new permissions is an empty list
        self.assertTrue(self.__store_owner_or_manager_role.edit_manager_permissions(store.get_name(),
                                                                               new_manager.get_nickname(),
                                                                               []))
        self.assertFalse((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.USERS_QUESTIONS))

        # All valid - owner
        self.assertTrue(self.__store_owner_or_manager_role.edit_manager_permissions(store.get_name(),
                                                                               new_manager.get_nickname(),
                                                                               [ManagerPermission.EDIT_MANAGER_PER]))
        self.assertTrue((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.EDIT_MANAGER_PER))

        # Invalid - store doesn't exist
        self.assertFalse(self.__store_owner_or_manager_role.edit_manager_permissions("store.get_name()",
                                                                                new_manager.get_nickname(),
                                                                                [ManagerPermission.EDIT_INV]))

        # Invalid - manager doesn't exist
        self.assertFalse(self.__store_owner_or_manager_role.edit_manager_permissions(store.get_name(),
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
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners().append(self.__user)
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_MANAGER_PER,
                                                                               ManagerPermission.APPOINT_MANAGER])

        (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "manager")

        new_manager = User()
        new_manager.register("I", "manage this tests")
        new_owner = User()
        new_owner.register("Bed", "of roses")
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners().append(new_owner)
        (TradeControl.get_instance()).subscribe(new_manager)
        (TradeControl.get_instance()).subscribe(manager)
        self.__store_owner_or_manager_role.appoint_store_manager(new_manager.get_nickname(),
                                                            store.get_name(),
                                                            [ManagerPermission.USERS_QUESTIONS])

        # All valid - new permissions is an empty list
        self.assertTrue(self.__store_owner_or_manager_role.edit_manager_permissions(store.get_name(),
                                                                               new_manager.get_nickname(),
                                                                               []))
        self.assertFalse((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.USERS_QUESTIONS))

        # All valid - manager
        self.assertTrue(self.__store_owner_or_manager_role.edit_manager_permissions(store.get_name(),
                                                                               new_manager.get_nickname(),
                                                                               [ManagerPermission.EDIT_MANAGER_PER]))
        self.assertTrue((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.EDIT_MANAGER_PER))

        # Invalid - store doesn't exist
        self.assertFalse(self.__store_owner_or_manager_role.edit_manager_permissions("store.get_name()",
                                                                                new_manager.get_nickname(),
                                                                                [ManagerPermission.EDIT_INV]))

        # Invalid - new manager doesn't exist
        self.assertFalse(self.__store_owner_or_manager_role.edit_manager_permissions(store.get_name(),
                                                                                "new_manager.get_nickname()",
                                                                                [ManagerPermission.EDIT_INV]))

        (TradeControl.get_instance()).set_curr_user(new_owner)
        (TradeControl.get_instance()).login_subscriber(new_owner.get_nickname(), "of roses")

        # Invalid - the changer isn't the appointer
        self.assertFalse(self.__store_owner_or_manager_role.edit_manager_permissions(store.get_name(),
                                                                                new_manager.get_nickname(),
                                                                                [ManagerPermission.DEL_OWNER]))
        self.assertTrue((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.EDIT_MANAGER_PER))
        self.assertFalse((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.DEL_OWNER))

        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)
        self.__store_owner_or_manager_role.edit_manager_permissions(store.get_name(),
                                                               manager.get_nickname(),
                                                               [ManagerPermission.DEL_OWNER])

        (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "manager")

        # Invalid - manager doesn't have permissions
        self.assertFalse(self.__store_owner_or_manager_role.edit_manager_permissions(store.get_name(),
                                                                                new_manager.get_nickname(),
                                                                                [ManagerPermission.DEL_OWNER]))
        self.assertTrue((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.EDIT_MANAGER_PER))
        self.assertFalse((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.DEL_OWNER))

        (TradeControl.get_instance()).logout_subscriber()

        # Invalid - manager doesn't login
        self.assertFalse(self.__store_owner_or_manager_role.edit_manager_permissions(store.get_name(),
                                                                                new_manager.get_nickname(),
                                                                                [ManagerPermission.DEL_OWNER]))
        self.assertTrue((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.EDIT_MANAGER_PER))
        self.assertFalse((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.DEL_OWNER))

        user = User()
        user.register("I am", "just a user")
        (TradeControl.get_instance()).set_curr_user(user)
        (TradeControl.get_instance()).login_subscriber(user.get_nickname(), "just a user")

        # Invalid - not a manager or an owner
        self.assertFalse(self.__store_owner_or_manager_role.edit_manager_permissions(store.get_name(),
                                                                                new_manager.get_nickname(),
                                                                                [
                                                                                    ManagerPermission.WATCH_PURCHASE_HISTORY]))
        self.assertTrue((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.EDIT_MANAGER_PER))
        self.assertFalse((TradeControl.get_instance()).get_store(store.get_name()).has_permission(
            new_manager.get_nickname(), ManagerPermission.WATCH_PURCHASE_HISTORY))

    @logger
    def test_remove_manager(self):
        (TradeControl.get_instance()).register_guest("eytan", "eytan as password")
        (TradeControl.get_instance()).login_subscriber("eytan", "eytan as password")
        user_nickname = "eytan"
        user_password = "eytan as password"
        manager = User()
        manager.register("manager", "manager")
        store: Store = Store("myStore")
        # store.add_product("Eytan's product", 12, "Eytan's category", 5)
        (TradeControl.get_instance()).get_stores().append(store)
        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners().append(self.__user)
        (TradeControl.get_instance()).get_store(store.get_name()).add_manager(self.__user, manager,
                                                                              [ManagerPermission.EDIT_MANAGER_PER,
                                                                               ManagerPermission.APPOINT_MANAGER])

        new_manager = User()
        new_manager.register("I", "manage this tests")
        new_owner = User()
        new_owner.register("Bed", "of roses")
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners().append(new_owner)
        (TradeControl.get_instance()).subscribe(new_manager)
        (TradeControl.get_instance()).subscribe(manager)
        self.__store_owner_or_manager_role.appoint_store_manager(new_manager.get_nickname(),
                                                            store.get_name(),
                                                            [ManagerPermission.USERS_QUESTIONS])

        # All valid
        self.assertTrue(self.__store_owner_or_manager_role.remove_manager(store.get_name(), new_manager.get_nickname()))
        self.assertNotIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        # Invalid - manager doesn't exist
        self.assertFalse(self.__store_owner_or_manager_role.remove_manager(store.get_name(), new_manager.get_nickname()))

        # Restore
        self.__store_owner_or_manager_role.appoint_store_manager(new_manager.get_nickname(),
                                                            store.get_name(),
                                                            [ManagerPermission.USERS_QUESTIONS])

        # Invalid - store doesn't exist
        self.assertFalse(self.__store_owner_or_manager_role.remove_manager("store.get_name()", new_manager.get_nickname()))

        (TradeControl.get_instance()).logout_subscriber()

        # Invalid - curr_user is logged out
        self.assertFalse(self.__store_owner_or_manager_role.remove_manager(store.get_name(), new_manager.get_nickname()))
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        (TradeControl.get_instance()).set_curr_user(new_owner)
        (TradeControl.get_instance()).login_subscriber(new_owner.get_nickname(), "of roses")

        # Invalid - the removing owner isn't the appointer
        self.assertFalse(self.__store_owner_or_manager_role.remove_manager(store.get_name(), new_manager.get_nickname()))
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
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners().append(self.__user)
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
        (TradeControl.get_instance()).get_store(store.get_name()).get_owners().append(new_owner)
        (TradeControl.get_instance()).subscribe(new_manager)
        (TradeControl.get_instance()).subscribe(manager)
        self.__store_owner_or_manager_role.appoint_store_manager(new_manager.get_nickname(),
                                                            store.get_name(),
                                                            [ManagerPermission.USERS_QUESTIONS])

        # All valid
        self.assertTrue(self.__store_owner_or_manager_role.remove_manager(store.get_name(), new_manager.get_nickname()))
        self.assertNotIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        # Invalid - removed manager doesn't exist
        self.assertFalse(self.__store_owner_or_manager_role.remove_manager(store.get_name(), new_manager.get_nickname()))

        # Restore
        self.__store_owner_or_manager_role.appoint_store_manager(new_manager.get_nickname(),
                                                            store.get_name(),
                                                            [ManagerPermission.USERS_QUESTIONS])

        # Invalid - store doesn't exist
        self.assertFalse(self.__store_owner_or_manager_role.remove_manager("store.get_name()", new_manager.get_nickname()))

        (TradeControl.get_instance()).logout_subscriber()

        # Invalid - curr_user is logged out
        self.assertFalse(self.__store_owner_or_manager_role.remove_manager(store.get_name(), new_manager.get_nickname()))
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        (TradeControl.get_instance()).set_curr_user(new_owner)
        (TradeControl.get_instance()).login_subscriber(new_owner.get_nickname(), "of roses")

        # Invalid - the removing owner isn't the appointer
        self.assertFalse(self.__store_owner_or_manager_role.remove_manager(store.get_name(), new_manager.get_nickname()))
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        user = User()
        user.register("I hate", "testing")
        (TradeControl.get_instance()).set_curr_user(user)
        (TradeControl.get_instance()).login_subscriber(user.get_nickname(), "testing")

        # Invalid - user isn't an owner or a manager
        self.assertFalse(self.__store_owner_or_manager_role.remove_manager(store.get_name(), new_manager.get_nickname()))
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

        (TradeControl.get_instance()).set_curr_user(self.__user)
        (TradeControl.get_instance()).login_subscriber(user_nickname, user_password)
        self.__store_owner_or_manager_role.edit_manager_permissions(store.get_name(),
                                                               manager.get_nickname(),
                                                               [ManagerPermission.DEL_OWNER])

        (TradeControl.get_instance()).set_curr_user(manager)
        (TradeControl.get_instance()).login_subscriber(manager.get_nickname(), "manager")

        # Invalid manager doesn't have permissions
        self.assertFalse(self.__store_owner_or_manager_role.remove_manager(store.get_name(), new_manager.get_nickname()))
        self.assertIn(new_manager, (TradeControl.get_instance()).get_store(store.get_name()).get_managers())

    @logger
    def test_display_store_purchases(self):
        # Empty purchases
        lst = self.__store_owner_or_manager_role.display_store_purchases(self.__store.get_name())
        # print(type(lst))
        self.assertListEqual([], lst)

        (TradeControl.get_instance()).get_store(self.__store.get_name()).add_purchase \
            (Purchase([{"product_name": "eytan", "product_price": 12, "amount": 1}], 12, self.__store.get_name(),
                      self.__user.get_nickname()))

        # Not empty
        lst = self.__store_owner_or_manager_role.display_store_purchases(self.__store.get_name())
        self.assertEqual(1, len(lst))
        purchases_lst = [jsonpickle.decode(e).get_products() for e in
                         self.__store_owner_or_manager_role.display_store_purchases(self.__store.get_name())]
        self.assertListEqual([{"product_name": "eytan", "product_price": 12, "amount": 1}], purchases_lst[0])

    @logger
    def tearDown(self):
        (TradeControl.get_instance()).__delete__()

    def __repr__(self):
        return repr("StoreOwnerOrManagerRoleTests")


if __name__ == '__main__':
    unittest.main()