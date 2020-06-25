import unittest
from datetime import datetime

import jsonpickle

from src.main.DomainLayer.StoreComponent.DiscountPolicyComposite.CompositeFlag import CompositeFlag
from src.main.DomainLayer.StoreComponent.DiscountPolicyComposite.DiscountPolicy import DiscountPolicy
from src.main.DomainLayer.StoreComponent.DiscountPolicyComposite.Leaves.ConditionalDiscountPolicy import \
    ConditionalDiscountPolicy
from src.main.DomainLayer.StoreComponent.ManagerPermission import ManagerPermission
from src.main.DomainLayer.StoreComponent.Product import Product
from src.main.DomainLayer.StoreComponent.Purchase import Purchase
from src.main.DomainLayer.StoreComponent.Store import Store
from src.main.DomainLayer.StoreComponent.StoreAppointment import StoreAppointment
from src.main.DomainLayer.UserComponent.User import User
from src.main.DataAccessLayer.DataAccessFacade import DataAccessFacade


class StoreTests(unittest.TestCase):
    # @logger
    def setUp(self):
        self.store: Store = Store("myStore")
        self.owner = User()
        self.owner.register("Eytan", "password")
        self.store.get_owners_appointments().append(StoreAppointment(None, self.owner, []))
        self.manager = User()
        self.manager.register("Not Eytan", "Yes Password")
        self.store.get_store_manager_appointments().append(StoreAppointment(self.owner, self.manager,
                                                                            [ManagerPermission.EDIT_INV]))
        (DataAccessFacade.get_instance()).write_user("Eytan", "password")
        (DataAccessFacade.get_instance()).write_user("Not Eytan", "Yes Password")
        (DataAccessFacade.get_instance()).write_store("myStore", "Eytan")
        dis_details = {'name': "p1", 'product': "Eytan"}
        later_date = datetime(2021, 8, 21)
        pre_con__details = {'product': "Eytan", 'min_amount': 2, 'min_basket_price': None}
        leaf_pol1 = ConditionalDiscountPolicy(2.5, later_date, dis_details, pre_con__details)
        dis_details = {'name': "p2", 'product': "Eytan"}
        pre_con__details = {'product': "all", 'min_amount': None, 'min_basket_price': 1}
        leaf_pol2 = ConditionalDiscountPolicy(5, later_date, dis_details, pre_con__details)
        self.__policy = DiscountPolicy(jsonpickle.encode(leaf_pol1), jsonpickle.encode(leaf_pol2),
                                       CompositeFlag.XOR, 10, "Comp_Pol", later_date)
        self.store.get_discount_policies().insert(0, self.__policy)

        # self.__product1 = {"name": "Chair", "price": 100, "category": "Furniture", "amount": 10}
        # self.__product2 = {"name": "TV", "price": 10, "category": "Electric", "amount": 1}
        # self.__product3 = {"name": "Sofa", "price": 1, "category": "Furniture", "amount": 2}

    # @logger
    def test_get_products_by(self):
        self.store.add_products("Eytan", [{"name": "Chair", "price": 100, "category": "Furniture", "amount": 10,
                                           "purchase_type": 0},
                                          {"name": "TV", "price": 10, "category": "Electric", "amount": 1,
                                           "purchase_type": 0},
                                          {"name": "Sofa", "price": 1, "category": "Furniture", "amount": 2,
                                           "purchase_type": 0}])
        product1: Product = Product("Chair", 100, "Furniture")
        product2: Product = Product("TV", 10, "Electric")
        product3: Product = Product("Sofa", 1, "Furniture")

        # Option 1- All valid
        ls = self.store.get_products_by(1, "Chair")
        self.assertEqual(len(ls), 1)
        self.assertTrue(product1 in ls)

        # Option 1- Not an existing product
        ls = self.store.get_products_by(1, "EytanIsTheBestEver!!!")
        self.assertEqual(len(ls), 0)

        # Option 2- All valid
        ls = self.store.get_products_by(2, "a")
        self.assertEqual(len(ls), 2)
        self.assertTrue(product1 in ls)
        self.assertTrue(product3 in ls)

        # Option 2- Empty products list
        ls = self.store.get_products_by(2, "EytanIsTheBestEver!!!")
        self.assertEqual(len(ls), 0)

        # Option 3 - All valid
        ls = self.store.get_products_by(3, "Furniture")
        self.assertEqual(len(ls), 2)
        self.assertTrue(product1 in ls)
        self.assertTrue(product3 in ls)

        ls = self.store.get_products_by(3, "Electric")
        self.assertEqual(len(ls), 1)
        self.assertTrue(product2 in ls)

        # Option 3 - Not an existing category
        ls = self.store.get_products_by(3, "EytanIsTheBestEver!!!")
        self.assertEqual(len(ls), 0)

    # @logger
    def test_add_products(self):
        product1: Product = Product("Chair", 100, "Furniture")
        product3: Product = Product("Sofa", 1, "Furniture")

        # All Valid - New Products
        self.assertTrue(
            self.store.add_products("Eytan", [{"name": "Chair", "price": 100, "category": "Furniture", "amount": 5,
                                               "purchase_type": 0},
                                              {"name": "Sofa", "price": 1, "category": "Furniture", "amount": 3,
                                               "purchase_type": 0}]))
        self.assertEqual(len(self.store.get_products_by(2, "")), 2)
        self.assertTrue(product1 in self.store.get_products_by(2, ""))
        self.assertTrue(product3 in self.store.get_products_by(2, ""))

        # All valid - Existing products
        self.assertTrue(
            self.store.add_products("Eytan", [{"name": "Chair", "price": 100, "category": "Furniture", "amount": 6,
                                               "purchase_type": 0}]))
        self.assertEqual(len(self.store.get_products_by(2, "")), 2)
        self.assertTrue(product1 in self.store.get_products_by(2, ""))
        self.assertTrue(product3 in self.store.get_products_by(2, ""))

        # Invalid Product - negative price
        self.assertFalse(
            self.store.add_products("Eytan",
                                    [{"name": "Eytan's Toy", "price": -99, "category": "Furniture", "amount": 5,
                                      "purchase_type": 0}])['response'])
        self.assertEqual(len(self.store.get_products_by(2, "")), 2)
        products_names = [product.get_name() for product in self.store.get_products_by(2, "")]
        self.assertFalse("Eytan's Toy" in products_names)
        self.assertTrue(product1 in self.store.get_products_by(2, ""))
        self.assertTrue(product3 in self.store.get_products_by(2, ""))

        # Invalid amount - negative amount
        self.assertFalse(
            self.store.add_products("Eytan",
                                    [{"name": "Eytan's Toy", "price": 1, "category": "Furniture", "amount": -5,
                                      "purchase_type": 0}])['response'])
        self.assertEqual(len(self.store.get_products_by(2, "")), 2)
        products_names = [product.get_name() for product in self.store.get_products_by(2, "")]
        self.assertFalse("Eytan's Toy" in products_names)
        self.assertTrue(product1 in self.store.get_products_by(2, ""))
        self.assertTrue(product3 in self.store.get_products_by(2, ""))

        # Invalid Product - invalid name
        self.assertFalse(
            self.store.add_products("Eytan", [{"name": "", "price": 100, "category": "Furniture", "amount": 5,
                                               "purchase_type": 0}])['response'])
        self.assertEqual(len(self.store.get_products_by(2, "")), 2)
        products_names = [product.get_name() for product in self.store.get_products_by(2, "")]
        self.assertFalse("" in products_names)
        self.assertTrue(product1 in self.store.get_products_by(2, ""))
        self.assertTrue(product3 in self.store.get_products_by(2, ""))

        # Invalid Product - invalid category
        self.assertFalse(
            self.store.add_products("Eytan", [{"name": "Eytan's Toy", "price": 100, "category": "", "amount": 5,
                                               "purchase_type": 0}])['response'])
        self.assertEqual(len(self.store.get_products_by(2, "")), 2)
        products_names = [product.get_name() for product in self.store.get_products_by(2, "")]
        self.assertFalse("Eytan's Toy" in products_names)
        self.assertTrue(product1 in self.store.get_products_by(2, ""))
        self.assertTrue(product3 in self.store.get_products_by(2, ""))

    # @logger
    def test_add_product(self):
        product1: Product = Product("Chair", 100, "Furniture")
        product3: Product = Product("Sofa", 1, "Furniture")

        # All valid

        # First Addition
        self.assertTrue(self.store.add_product("Eytan", "Chair", 100, "Furniture", 5, 0))
        self.assertEqual(self.store.get_inventory().len(), 1)
        self.assertTrue(product1 in self.store.get_products_by(2, ""))
        self.assertEqual(self.store.get_inventory().get_amount("Chair"), 5)

        # Second Addition
        self.assertTrue(self.store.add_product("Eytan", "Sofa", 1, "Furniture", 0, 0))
        self.assertEqual(self.store.get_inventory().len(), 2)
        self.assertTrue(product1 in self.store.get_products_by(2, ""))
        self.assertTrue(product3 in self.store.get_products_by(2, ""))
        self.assertEqual(self.store.get_inventory().get_amount("Sofa"), 0)

        # Adding existing product
        self.assertTrue(self.store.add_product("Eytan", "Chair", 100, "Furniture", 5, 0))
        self.assertEqual(self.store.get_inventory().len(), 2)
        self.assertTrue(product1 in self.store.get_products_by(2, ""))
        self.assertTrue(product3 in self.store.get_products_by(2, ""))
        self.assertEqual(self.store.get_inventory().get_amount("Chair"), 10)

        # Invalid

        # Negative amount
        self.assertFalse(self.store.add_product("Eytan", "Chair", 100, "Furniture", -5, 0))
        self.assertEqual(self.store.get_inventory().len(), 2)
        self.assertTrue(product1 in self.store.get_products_by(2, ""))
        self.assertTrue(product3 in self.store.get_products_by(2, ""))
        self.assertEqual(self.store.get_inventory().get_amount("Chair"), 10)

        # Negative price
        self.assertFalse(self.store.add_product("Eytan", "Chair", -100, "Furniture", 5, 0))
        self.assertEqual(self.store.get_inventory().len(), 2)
        self.assertTrue(product1 in self.store.get_products_by(2, ""))
        self.assertTrue(product3 in self.store.get_products_by(2, ""))
        self.assertEqual(self.store.get_inventory().get_amount("Chair"), 10)

        # Empty name
        self.assertFalse(self.store.add_product("Eytan", "", 100, "Furniture", 5, 0))
        self.assertEqual(self.store.get_inventory().len(), 2)
        products_names = [product.get_name() for product in self.store.get_products_by(2, "")]
        self.assertFalse("" in products_names)
        self.assertTrue(product1 in self.store.get_products_by(2, ""))
        self.assertTrue(product3 in self.store.get_products_by(2, ""))
        self.assertEqual(self.store.get_inventory().get_amount("Chair"), 10)

        # Empty category
        self.assertFalse(self.store.add_product("Eytan", "Eytan's Toy", 100, "", 5, 0))
        self.assertEqual(self.store.get_inventory().len(), 2)
        products_names = [product.get_name() for product in self.store.get_products_by(2, "")]
        self.assertFalse("Eytan's Toy" in products_names)
        self.assertTrue(product1 in self.store.get_products_by(2, ""))
        self.assertTrue(product3 in self.store.get_products_by(2, ""))

    # @logger
    def test_remove_products(self):
        product1: Product = Product("Chair", 100, "Furniture")
        product3: Product = Product("Sofa", 1, "Furniture")

        self.store.add_product("Eytan", "Chair", 100, "Furniture", 5, 0)

        # All Valid - one product
        self.assertTrue(self.store.remove_products("Eytan", ["Chair"]))
        self.assertEqual(self.store.get_inventory().len(), 0)

        self.store.add_product("Eytan", "Chair", 100, "Furniture", 5,0)
        self.store.add_product("Eytan", "Chair", 100, "Furniture", 5, 0)
        self.store.add_product("Eytan", "Sofa", 1, "Furniture", 3, 0)

        # All valid - two products
        self.assertEqual(self.store.get_inventory().len(), 2)
        self.assertTrue(self.store.remove_products("Eytan", ["Chair", "Sofa"]))
        self.assertEqual(self.store.get_inventory().len(), 0)

        self.store.add_product("Eytan", "Chair", 100, "Furniture", 5, 0)
        self.store.add_product("Eytan", "Chair", 100, "Furniture", 5, 0)
        self.store.add_product("Eytan", "Sofa", 1, "Furniture", 3, 0)

        # All valid - not all inventory removed
        self.assertTrue(self.store.remove_products("Eytan", ["Chair"]))
        self.assertEqual(self.store.get_inventory().len(), 1)
        self.assertTrue(product3 in self.store.get_products_by(2, ""))

        # All valid - Manager
        self.assertTrue(self.store.remove_products("Not Eytan", ["Sofa"]))
        self.assertEqual(self.store.get_inventory().len(), 0)

        # Invalid product
        self.assertFalse(self.store.remove_products("Not Eytan", ["Eytan's Toy"]))

        # Invalid - Manager/Owner
        self.assertFalse(self.store.remove_products("", ["Chair", "Sofa"]))

        bad_manager = User()
        bad_manager.register("Half Eytan, half not Eytan", "Definitely Password")
        self.store.get_store_manager_appointments().append(
            StoreAppointment(self.owner, bad_manager, [ManagerPermission.WATCH_PURCHASE_HISTORY]))

        # Invalid - Manager permissions
        self.store.add_product("Eytan", "Chair", 100, "Furniture", 5, 0)
        self.store.add_product("Eytan", "Chair", 100, "Furniture", 5, 0)
        self.assertFalse(self.store.remove_products(bad_manager.get_nickname(), ["Chair"]))
        self.assertEqual(self.store.get_inventory().len(), 1)
        self.assertTrue(product1 in self.store.get_products_by(2, ""))
        self.assertEqual(self.store.get_inventory().get_amount("Chair"), 10)

    # @logger
    def test_remove_product(self):
        product2: Product = Product("Not Chair", 1, "Furniture")

        # All valid - Empty inventory
        self.assertFalse(self.store.remove_product("Chair"))

        self.store.add_product("Eytan", "Chair", 100, "Furniture", 5, 0)
        self.store.add_product("Eytan", "Not Chair", 1, "Furniture", 3, 0)

        # All valid
        self.assertTrue(self.store.remove_product("Chair"))
        self.assertEqual(self.store.get_inventory().len(), 1)
        self.assertTrue(product2 in self.store.get_products_by(2, ""))

        # Invalid - Not an existing product
        self.assertFalse(self.store.remove_product("Eytan's Toy"))

    # @logger
    def test_change_price(self):
        self.store.add_product("Eytan", "Chair", 100, "Furniture", 5, 0)

        # All valid - first change
        self.assertTrue(self.store.change_price("Chair", 13))
        self.assertEqual(self.store.get_product("Chair").get_price(), 13)

        # All valid - second change
        self.assertTrue(self.store.change_price("Chair", 8.5))
        self.assertEqual(self.store.get_product("Chair").get_price(), 8.5)

        # Invalid- not existing product
        self.assertFalse(self.store.change_price("NNNN", 8))
        self.assertIsNone(self.store.get_product("NNNN"))

        # Invalid- negative price
        self.assertFalse(self.store.change_price("Chair", -8))
        self.assertEqual(self.store.get_product("Chair").get_price(), 8.5)

        # Edge case - change to zero
        self.assertTrue(self.store.change_price("Chair", 0.0))
        self.assertEqual(self.store.get_product("Chair").get_price(), 0)

    # @logger
    def test_change_name(self):
        self.store.add_product("Eytan", "Chair", 100, "Furniture", 5, 0)

        # All valid - first change
        self.assertTrue(self.store.change_name("Chair", "Chair222"))
        self.assertIsNotNone(self.store.get_product("Chair222"))
        self.assertIsNone(self.store.get_product("Chair"))

        # All valid - second change
        self.assertTrue(self.store.change_name("Chair222", "Blaaaa"))
        self.assertIsNotNone(self.store.get_product("Blaaaa"))
        self.assertIsNone(self.store.get_product("Chair222"))

        # Invalid - Not an existing product
        self.assertFalse(self.store.change_name("NNNN", "blaaa"))
        self.assertIsNone(self.store.get_product("NNNN"))
        self.assertIsNone(self.store.get_product("blaaa"))

        # Invalid - Empty name
        self.assertFalse(self.store.change_name("Blaaaa", ""))
        self.assertIsNone(self.store.get_product(""))
        self.assertIsNotNone(self.store.get_product("Blaaaa"))

    # @logger
    def test_change_amount(self):
        self.store.add_product("Eytan", "Chair", 100, "Furniture", 5, 0)

        # All valid - first change
        self.assertTrue(self.store.change_amount("Chair", 13))
        self.assertEqual(self.store.get_inventory().get_amount("Chair"), 13)

        # All valid - second change
        self.assertTrue(self.store.change_amount("Chair", 8))
        self.assertEqual(self.store.get_inventory().get_amount("Chair"), 8)

        # Invalid- not existing product
        self.assertFalse(self.store.change_amount("NNNN", 8))
        self.assertIsNone(self.store.get_product("NNNN"))

        # Invalid- negative amount
        self.assertFalse(self.store.change_amount("Chair", -8))
        self.assertEqual(self.store.get_inventory().get_amount("Chair"), 8)

        # Edge case - change to zero
        self.assertTrue(self.store.change_amount("Chair", 0))
        self.assertEqual(self.store.get_inventory().get_amount("Chair"), 0)

    # @logger
    def test_add_owner(self):
        user = User()
        user.register("eden", "password")
        (DataAccessFacade.get_instance()).write_user("eden", "password")

        # All valid
        result = self.store.add_owner("Eytan", user)
        self.assertTrue(result['response'])
        self.assertEqual(len(self.store.get_owners()), 2)
        self.assertTrue(user in self.store.get_owners())
        self.assertTrue(self.owner in self.store.get_owners())

        guest = User()

        # Invalid - user doesn't register
        self.assertFalse(self.store.add_owner("Eytan", guest)['response'])
        self.assertEqual(len(self.store.get_owners()), 2)
        self.assertTrue(user in self.store.get_owners())
        self.assertTrue(self.owner in self.store.get_owners())

        owner = User()
        owner.register("probably eden", "password")

        # Invalid - Owner doesn't exist
        self.assertFalse(self.store.add_owner("Eytan Not an Owner", owner)['response'])
        self.assertEqual(len(self.store.get_owners()), 2)
        self.assertTrue(user in self.store.get_owners())
        self.assertTrue(self.owner in self.store.get_owners())

        # Invalid - Already owner
        result = self.store.add_owner(self.owner.get_nickname(), user)['response']
        self.assertFalse(result)
        self.assertEqual(len(self.store.get_owners()), 2)
        self.assertTrue(user in self.store.get_owners())
        self.assertTrue(self.owner in self.store.get_owners())

        # Invalid - Circular appointments
        self.assertFalse(self.store.add_owner(user.get_nickname(), self.owner)['response'])
        self.assertEqual(len(self.store.get_owners()), 2)
        self.assertTrue(user in self.store.get_owners())
        self.assertTrue(self.owner in self.store.get_owners())

        manager = User()
        manager.register("Half Eytan, half not Eytan", "Definitely Password")
        (DataAccessFacade.get_instance()).write_user("Half Eytan, half not Eytan", "Definitely Password")
        self.store.get_store_manager_appointments().append(
            StoreAppointment(self.owner, manager, [ManagerPermission.WATCH_PURCHASE_HISTORY]))
        self.assertTrue(manager in self.store.get_managers())

        # All valid - appoint manager as owner
        # self.assertTrue(self.store.add_owner("Eytan", manager)['response'])
        # self.assertEqual(len(self.store.get_owners()), 3)
        # self.assertTrue(user in self.store.get_owners())
        # self.assertTrue(manager in self.store.get_owners())
        # self.assertTrue(self.owner in self.store.get_owners())
        # self.assertFalse(manager in self.store.get_managers())

    # @logger
    def test_is_owner(self):
        user = User()
        user.register("eden", "password")

        # All Valid
        self.store.add_owner("Eytan", user)
        self.assertTrue(self.store.is_owner("eden"))

        # Invalid - Not an existing user
        self.assertFalse(self.store.is_owner("not eden"))

        user2 = User()
        user2.register("Maybe Eden", "Definitely password")

        # Invalid - Existing user, not an owner
        self.assertFalse(self.store.is_owner("Maybe Eden"))

        self.store.add_manager(user, user2, [ManagerPermission.WATCH_PURCHASE_HISTORY])

        # Invalid - Existing manager
        self.assertFalse(self.store.is_owner("Maybe Eden"))

    # @logger
    def test_add_manager(self):
        user = User()
        user.register("eden", "password")

        # All valid
        self.assertTrue(self.store.add_manager(self.owner, user, [ManagerPermission.APPOINT_MANAGER,
                                                                  ManagerPermission.EDIT_MANAGER_PER]))
        self.assertEqual(2, len(self.store.get_managers()))
        self.assertTrue(user in self.store.get_managers())
        self.assertTrue(self.manager in self.store.get_managers())

        guest = User()

        # Invalid - user doesn't register
        self.assertFalse(self.store.add_manager(self.owner, guest, [ManagerPermission.WATCH_PURCHASE_HISTORY]))
        self.assertEqual(len(self.store.get_managers()), 2)
        self.assertTrue(user in self.store.get_managers())
        self.assertTrue(self.manager in self.store.get_managers())

        manager = User()
        manager.register("probably eden", "password")
        guest.register("Just Guest", "Password")

        # Invalid - Owner/manager isn't manager/owner
        self.assertFalse(self.store.add_manager(guest, manager, [ManagerPermission.WATCH_PURCHASE_HISTORY]))
        self.assertEqual(len(self.store.get_managers()), 2)
        self.assertTrue(user in self.store.get_managers())
        self.assertTrue(self.manager in self.store.get_managers())

        # Invalid - Already Manager
        self.assertFalse(self.store.add_manager(self.owner, user, [ManagerPermission.WATCH_PURCHASE_HISTORY]))
        self.assertEqual(len(self.store.get_managers()), 2)
        self.assertTrue(user in self.store.get_managers())
        self.assertTrue(self.manager in self.store.get_managers())

        # All Valid - Appoint by manager
        self.assertTrue(self.store.add_manager(user, manager, [ManagerPermission.APPOINT_MANAGER]))

        # Invalid - Circular appointments
        self.assertFalse(self.store.add_manager(manager, user, [ManagerPermission.WATCH_PURCHASE_HISTORY]))
        self.assertEqual(len(self.store.get_managers()), 3)
        self.assertTrue(user in self.store.get_managers())
        self.assertTrue(self.manager in self.store.get_managers())
        self.assertTrue(manager in self.store.get_managers())

        self.store.edit_manager_permissions(user, manager.get_nickname(), [ManagerPermission.USERS_QUESTIONS])

        # Invalid - Manager doesn't have permissions
        self.assertFalse(self.store.add_manager(manager, guest, [ManagerPermission.WATCH_PURCHASE_HISTORY]))
        self.assertEqual(len(self.store.get_managers()), 3)
        self.assertTrue(user in self.store.get_managers())
        self.assertTrue(self.manager in self.store.get_managers())
        self.assertTrue(manager in self.store.get_managers())

    # @logger
    def test_is_manger(self):
        user = User()
        user.register("eden", "password")

        # All Valid
        self.store.add_manager(self.owner, user, [ManagerPermission.USERS_QUESTIONS])
        self.assertTrue(self.store.is_manager("eden"))

        # Invalid - Not an existing user
        self.assertFalse(self.store.is_manager("not eden"))

        user2 = User()
        user2.register("Maybe Eden", "Definitely password")

        # Invalid - Existing user, not an owner
        self.assertFalse(self.store.is_manager("Maybe Eden"))

        # Invalid - Existing manager
        self.assertFalse(self.store.is_manager(self.owner.get_nickname()))

    # @logger
    def test_has_permission(self):
        user = User()
        user.register("eden", "password")
        self.store.add_manager(self.owner, user, [ManagerPermission.USERS_QUESTIONS, ManagerPermission.EDIT_MANAGER_PER])

        # All Valid - one permission.
        self.assertTrue(self.store.has_permission(self.manager.get_nickname(), ManagerPermission.EDIT_INV))

        # All Valid - two permission.
        self.assertTrue(self.store.has_permission(user.get_nickname(), ManagerPermission.USERS_QUESTIONS))

        user2 = User()
        user2.register("Not a manager", "Password")

        # Invalid - not a manager
        self.assertFalse(self.store.has_permission(user2.get_nickname(), ManagerPermission.USERS_QUESTIONS))

        # Invalid - manager without the correct permission
        self.assertFalse(self.store.has_permission(user.get_nickname(), ManagerPermission.EDIT_POLICIES))

        # Invalid - Owner
        # self.assertFalse(self.store.has_permission(self.owner.get_nickname(), ManagerPermission.EDIT_POLICIES))

        # Invalid - User doesn't exist
        self.assertFalse(self.store.has_permission("user.get_nickname()", ManagerPermission.EDIT_POLICIES))

    # @logger
    def test_edit_product(self):
        product1_args = ("Chair", 100, "Furniture")
        product1: Product = Product(*product1_args)
        self.store.add_product("Eytan", *product1_args, 10, 0)

        # OP name

        # All valid - owner
        self.assertTrue(self.store.edit_product(self.owner.get_nickname(), product1.get_name(), "name", "Eytan"))
        self.assertEqual(len(self.store.get_products_by(1, "Chair")), 0)
        product1.set_name("Eytan")
        self.assertEqual(len(self.store.get_products_by(1, "Eytan")), 1)
        self.assertTrue(product1 in self.store.get_products_by(1, "Eytan"))

        # All valid - manager
        self.assertTrue(self.store.edit_product(self.manager.get_nickname(), product1.get_name(), "name", "Chair"))
        self.assertEqual(len(self.store.get_products_by(1, "Eytan")), 0)
        product1.set_name("Chair")
        self.assertEqual(len(self.store.get_products_by(1, "Chair")), 1)
        self.assertTrue(product1 in self.store.get_products_by(1, "Chair"))

        # Invalid - product doesn't exist
        self.assertFalse(self.store.edit_product(self.manager.get_nickname(), "product1.get_name()", "name", "Chair2"))
        self.assertEqual(len(self.store.get_products_by(1, "product1.get_name()")), 0)

        # Invalid - Manager/owner doesn't exist
        self.assertFalse(self.store.edit_product("self.manager.get_nickname()", "Chair", "name", "Eytan"))
        self.assertEqual(len(self.store.get_products_by(1, "Eytan")), 0)

        manager = User()
        manager.register("probably eden", "password")
        self.store.add_manager(self.owner, manager, [ManagerPermission.EDIT_POLICIES])

        # Invalid - Manager without permissions
        self.assertFalse(self.store.edit_product(manager, "Chair", "name", "Eytan"))
        self.assertEqual(len(self.store.get_products_by(1, "Eytan")), 0)

        # OP price

        # All valid - owner
        self.assertTrue(self.store.edit_product(self.owner.get_nickname(), product1.get_name(), "price", 20))
        self.assertEqual(len(self.store.get_products_by(1, "Chair")), 1)
        product1.set_price(20)
        self.assertTrue(product1 in self.store.get_products_by(1, "Chair"))

        # All valid - manager
        self.assertTrue(self.store.edit_product(self.manager.get_nickname(), product1.get_name(), "price", 2))
        self.assertEqual(len(self.store.get_products_by(1, "Chair")), 1)
        product1.set_price(2)
        self.assertTrue(product1 in self.store.get_products_by(1, "Chair"))

        # All valid - float
        self.assertTrue(self.store.edit_product(self.manager.get_nickname(), product1.get_name(), "price", 2.12))
        self.assertEqual(len(self.store.get_products_by(1, "Chair")), 1)
        product1.set_price(2.12)
        self.assertTrue(product1 in self.store.get_products_by(1, "Chair"))

        # All valid - edge case - 0
        self.assertTrue(self.store.edit_product(self.manager.get_nickname(), product1.get_name(), "price", 0))
        self.assertEqual(len(self.store.get_products_by(1, "Chair")), 1)
        product1.set_price(0)
        self.assertTrue(product1 in self.store.get_products_by(1, "Chair"))

        # Invalid - product doesn't exist
        self.assertFalse(self.store.edit_product(self.manager.get_nickname(), "product1.get_name()", "price", 20))
        self.assertEqual(len(self.store.get_products_by(1, "product1.get_name()")), 0)
        for product in self.store.get_products_by(2, ""):
            self.assertFalse(product.get_price() == 20)

        # Invalid - Manager/owner doesn't exist
        self.assertFalse(self.store.edit_product("self.manager.get_nickname()", "Chair", "price", 15))
        self.assertEqual(len(self.store.get_products_by(1, "Chair")), 1)
        self.assertFalse(self.store.get_products_by(1, "Chair")[0].get_price(), 15)

        manager = User()
        manager.register("probably eden", "password")
        self.store.add_manager(self.owner, manager, [ManagerPermission.EDIT_POLICIES])

        # Invalid - Manager without permissions
        self.assertFalse(self.store.edit_product(manager, "Chair", "price", 13))
        self.assertEqual(len(self.store.get_products_by(1, "Chair")), 1)
        self.assertFalse(self.store.get_products_by(1, "Chair")[0].get_price(), 13)

        # Invalid - negative price
        self.assertFalse(self.store.edit_product(manager, "Chair", "price", -13))
        self.assertEqual(len(self.store.get_products_by(1, "Chair")), 1)
        self.assertFalse(self.store.get_products_by(1, "Chair")[0].get_price(), -13)

        # OP amount

        # All valid - owner
        self.assertTrue(self.store.edit_product(self.owner.get_nickname(), product1.get_name(), "amount", 20))
        self.assertEqual(self.store.get_inventory().get_amount("Chair"), 20)

        # All valid - manager
        self.assertTrue(self.store.edit_product(self.manager.get_nickname(), product1.get_name(), "amount", 2))
        self.assertEqual(self.store.get_inventory().get_amount("Chair"), 2)

        # All valid - edge case - 0
        self.assertTrue(self.store.edit_product(self.manager.get_nickname(), product1.get_name(), "amount", 0))
        self.assertEqual(self.store.get_inventory().get_amount("Chair"), 0)

        # Invalid - product doesn't exist
        self.assertFalse(self.store.edit_product(self.manager.get_nickname(), "product1.get_name()", "amount", 20))
        self.assertEqual(len(self.store.get_products_by(1, "product1.get_name()")), 0)
        for product in self.store.get_products_by(2, ""):
            self.assertFalse(self.store.get_inventory().get_amount(product.get_name()) == 20)

        # Invalid - Manager/owner doesn't exist
        self.assertFalse(self.store.edit_product("self.manager.get_nickname()", "Chair", "amount", 15))
        self.assertEqual(len(self.store.get_products_by(1, "Chair")), 1)
        self.assertFalse(self.store.get_inventory().get_amount("Chair"), 15)

        manager = User()
        manager.register("probably eden", "password")
        self.store.add_manager(self.owner, manager, [ManagerPermission.EDIT_POLICIES])

        # Invalid - Manager without permissions
        self.assertFalse(self.store.edit_product(manager, "Chair", "amount", 13))
        self.assertEqual(len(self.store.get_products_by(1, "Chair")), 1)
        self.assertFalse(self.store.get_inventory().get_amount("Chair"), 13)

        # Invalid - negative price
        self.assertFalse(self.store.edit_product(manager, "Chair", "amount", -13))
        self.assertEqual(len(self.store.get_products_by(1, "Chair")), 1)
        self.assertFalse(self.store.get_inventory().get_amount("Chair"), -13)

    # @logger
    def test_edit_manager_permissions(self):
        manager1 = User()
        manager1.register("probably eden", "password")
        self.store.add_manager(self.owner, manager1,
                               [ManagerPermission.EDIT_MANAGER_PER, ManagerPermission.APPOINT_MANAGER])

        manager2 = User()
        manager2.register("almost definitely eden", "password")
        self.store.add_manager(manager1, manager2, [ManagerPermission.EDIT_POLICIES])

        # All valid - owner
        self.assertTrue(self.store.edit_manager_permissions(self.owner, self.manager.get_nickname(),
                                                            [ManagerPermission.EDIT_POLICIES]))
        self.assertTrue(self.store.has_permission(self.manager.get_nickname(), ManagerPermission.EDIT_POLICIES))
        self.assertFalse(self.store.has_permission(self.manager.get_nickname(), ManagerPermission.EDIT_INV))

        # All valid - manager
        self.assertTrue(self.store.edit_manager_permissions(manager1, manager2.get_nickname(),
                                                            [ManagerPermission.EDIT_INV]))
        self.assertTrue(self.store.has_permission(manager2.get_nickname(), ManagerPermission.EDIT_INV))
        self.assertFalse(self.store.has_permission(manager2.get_nickname(), ManagerPermission.EDIT_POLICIES))

        # All valid - owner, two permissions
        self.assertTrue(self.store.edit_manager_permissions(self.owner, self.manager.get_nickname(),
                                                            [ManagerPermission.WATCH_PURCHASE_HISTORY,
                                                             ManagerPermission.DEL_OWNER]))
        self.assertTrue(self.store.has_permission(self.manager.get_nickname(), ManagerPermission.WATCH_PURCHASE_HISTORY))
        self.assertTrue(self.store.has_permission(self.manager.get_nickname(), ManagerPermission.DEL_OWNER))
        self.assertFalse(self.store.has_permission(self.manager.get_nickname(), ManagerPermission.EDIT_POLICIES))

        # All valid - owner, two permissions
        self.assertTrue(self.store.edit_manager_permissions(self.owner, self.manager.get_nickname(),
                                                            [ManagerPermission.WATCH_PURCHASE_HISTORY,
                                                             ManagerPermission.DEL_OWNER]))
        self.assertTrue(
            self.store.has_permission(self.manager.get_nickname(), ManagerPermission.WATCH_PURCHASE_HISTORY))
        self.assertTrue(self.store.has_permission(self.manager.get_nickname(), ManagerPermission.DEL_OWNER))
        self.assertFalse(self.store.has_permission(self.manager.get_nickname(), ManagerPermission.EDIT_POLICIES))

        # All valid - empty permissions
        self.assertTrue(self.store.edit_manager_permissions(self.owner, manager1.get_nickname(), []))
        for i in range(1, 11):
            self.assertFalse(self.store.has_permission(manager1.get_nickname(), ManagerPermission(i)))

        user = User()
        user.register("not an owner", "not a password")

        # Invalid - not an owner
        self.assertFalse(self.store.edit_manager_permissions(user, self.manager.get_nickname(),
                                                            [ManagerPermission.EDIT_POLICIES]))
        self.assertTrue(
            self.store.has_permission(self.manager.get_nickname(), ManagerPermission.WATCH_PURCHASE_HISTORY))
        self.assertTrue(self.store.has_permission(self.manager.get_nickname(), ManagerPermission.DEL_OWNER))
        self.assertFalse(self.store.has_permission(self.manager.get_nickname(), ManagerPermission.EDIT_POLICIES))

        self.store.add_owner(self.owner.get_nickname(), user)

        # Invalid - not a manager
        self.assertFalse(self.store.edit_manager_permissions(self.owner, user,
                                                             [ManagerPermission.EDIT_POLICIES]))
        for appointment in self.store.get_store_manager_appointments():
            self.assertFalse(appointment.get_appointee().get_nickname() == user.get_nickname())

        self.store.add_owner(self.owner.get_nickname(), user)

        # Invalid - not the owner which appoint the manager
        self.assertFalse(self.store.edit_manager_permissions(user, self.manager.get_nickname(),
                                                             [ManagerPermission.EDIT_POLICIES]))
        self.assertTrue(
            self.store.has_permission(self.manager.get_nickname(), ManagerPermission.WATCH_PURCHASE_HISTORY))
        self.assertTrue(self.store.has_permission(self.manager.get_nickname(), ManagerPermission.DEL_OWNER))
        self.assertFalse(self.store.has_permission(self.manager.get_nickname(), ManagerPermission.EDIT_POLICIES))

        # Invalid - try change permissions to an owner
        self.assertFalse(self.store.edit_manager_permissions(self.owner, user,
                                                             [ManagerPermission.EDIT_POLICIES]))
        for appointment in self.store.get_store_manager_appointments():
            self.assertFalse(appointment.get_appointee().get_nickname() == user.get_nickname())

    # @logger
    def test_remove_manager(self):
        # def remove_manager(self, appointer_nickname: str, appointee_nickname: str) -> bool:
        manager1 = User()
        manager1.register("probably eden", "password")
        self.store.add_manager(self.owner, manager1,
                               [ManagerPermission.DEL_MANAGER, ManagerPermission.APPOINT_MANAGER])

        manager2 = User()
        manager2.register("almost definitely eden", "password")
        self.store.add_manager(manager1, manager2, [ManagerPermission.EDIT_POLICIES])

        # Invalid - not the right permissions
        self.assertFalse(self.store.remove_manager(manager2.get_nickname(), self.manager.get_nickname()))
        self.assertTrue(self.manager in self.store.get_managers())

        # All valid - manager as appointer
        self.assertTrue(self.store.remove_manager(manager1.get_nickname(), manager2.get_nickname()))
        self.assertFalse(manager2 in self.store.get_managers())

        # All valid - owner as appointer
        self.assertTrue(self.store.remove_manager(self.owner.get_nickname(), manager1.get_nickname()))
        self.assertFalse(manager1 in self.store.get_managers())

        managers = self.store.get_managers()

        # Invalid - not an existing manager
        self.assertFalse(self.store.remove_manager(self.owner.get_nickname(), manager1.get_nickname()))
        self.assertEqual(len(managers), len(self.store.get_managers()))
        for m in managers:
            self.assertTrue(m in self.store.get_managers())

        # Invalid - not an existing appointer
        self.assertFalse(self.store.remove_manager(manager2.get_nickname(), self.manager.get_nickname()))
        self.assertEqual(len(managers), len(self.store.get_managers()))
        for m in managers:
            self.assertTrue(m in self.store.get_managers())

        user = User()
        user.register("not an owner", "not a password")
        self.store.add_owner(self.owner.get_nickname(), user)

        # Invalid - not the owner that appoint the manager
        self.assertFalse(self.store.remove_manager(user.get_nickname(), self.manager.get_nickname()))
        self.assertEqual(len(managers), len(self.store.get_managers()))
        for m in managers:
            self.assertTrue(m in self.store.get_managers())

    # @logger
    def test_get_purchases(self):
        self.store.edit_manager_permissions(self.owner, self.manager.get_nickname(),
                                            [ManagerPermission.WATCH_PURCHASE_HISTORY])
        purchase: Purchase = Purchase([{"product_name": "Chair", "product_price": 100, "amount": 5},
                                          {"product_name": "Sofa", "product_price": 1, "amount": 1}], 501,
                                         self.store.get_name(), self.owner.get_nickname())
        self.store.add_purchase(purchase)

        # All valid - owner
        self.assertListEqual(self.store.get_purchases(self.owner.get_nickname()), [purchase])

        # All valid - manager
        self.assertListEqual(self.store.get_purchases(self.manager.get_nickname()), [purchase])

        user = User()
        user.register("just a user", "but a special password")

        # Invalid - not an owner/manager
        self.assertListEqual(self.store.get_purchases(user.get_nickname()), [])

        self.store.add_manager(self.owner, user, [ManagerPermission.DEL_MANAGER])

        # Invalid - not the right permissions
        self.assertListEqual(self.store.get_purchases(user.get_nickname()), [])

    # @logger
    def test_is_in_store_inventory(self):
        self.store.add_product("Eytan", "Eytan's Product", 100, "Eytan Category", 5, 0)
        self.store.add_product("Eytan", "not Eytan's Product", 10, "Eytan Category", 2, 0)

        # All valid one product
        amount_per_product = [["Eytan's Product", 4]]
        result = self.store.is_in_store_inventory(amount_per_product)
        self.assertTrue(result)

        # All valid two products
        amount_per_product = [["Eytan's Product", 4], ["not Eytan's Product", 1]]
        result = self.store.is_in_store_inventory(amount_per_product)
        self.assertTrue(result)

        # Exactly the same as in stock
        amount_per_product = [["Eytan's Product", 5], ["not Eytan's Product", 2]]
        result = self.store.is_in_store_inventory(amount_per_product)
        self.assertTrue(result)

        # One product not enough in stock
        amount_per_product = [["Eytan's Product", 6], ["not Eytan's Product", 1]]
        result = self.store.is_in_store_inventory(amount_per_product)
        self.assertFalse(result)

        # Two product not enough in stock
        amount_per_product = [["Eytan's Product", 6], ["not Eytan's Product", 10]]
        result = self.store.is_in_store_inventory(amount_per_product)
        self.assertFalse(result)

        # One product doesn't exist
        amount_per_product = [["Eytan's social life", 5], ["not Eytan's Product", 1]]
        result = self.store.is_in_store_inventory(amount_per_product)
        self.assertFalse(result)

        # Two things that doesn't exist
        amount_per_product = [["Eytan's social life", 1], ["Liverpool's primer league title", 1]]
        result = self.store.is_in_store_inventory(amount_per_product)
        self.assertFalse(result)

    def test_purchase_policy_exists(self):
        self.store.define_purchase_policy({"name": "policy1", "products": ["product1"], "min_amount": 8})
        # policy exists
        res = self.store.purchase_policy_exists({"name": "policy1", "products": ["product1"], "min_amount": 8})
        self.assertTrue(res)

        # policy doesn't exist
        res = self.store.purchase_policy_exists({"name": "policy2", "products": ["product1", "product2"], "min_amount": 8})
        self.assertFalse(res)

        res = self.store.purchase_policy_exists({"products": ["product1", "product2"], "min_amount": 8})
        self.assertFalse(res)

        res = self.store.purchase_policy_exists({"name": "policy2", "products": ["product1"], "min_amount": 10})
        self.assertFalse(res)

    def test_add_purchase_policy(self):
        # valid details
        res = self.store.define_purchase_policy({"name": "policy1",
                                                 "products": ["product1"], "min_amount": 8})["response"]
        self.assertTrue(res)

        # invalid details
        res = self.store.define_purchase_policy({"name": "policy2",
                                                 "products": ["product1"]})["response"]
        self.assertFalse(res)

        res = self.store.define_purchase_policy({"products": ["product1"], "min_amount": 8})["response"]
        self.assertFalse(res)

    def test_update_purchase_policy(self):
        self.store.define_purchase_policy({"name": "policy1",
                                           "products": ["product1"], "min_amount": 8})
        # valid update
        res = self.store.update_purchase_policy({"name": "policy1",
                                           "products": ["product1"], "min_amount": 4})["response"]
        self.assertTrue(res)

        # invalid update
        res = self.store.update_purchase_policy({"name": "policy2",
                                                 "products": ["product1"], "min_amount": 4})["response"]
        self.assertFalse(res)

    def test_get_purchase_policies(self):
        # no policies exist
        res = self.store.get_purchase_policies()
        self.assertTrue(len(res) == 0)

        # policies exist
        self.store.define_purchase_policy({"name": "policy1",
                                           "products": ["product1"], "min_amount": 8})
        res = self.store.get_purchase_policies()
        self.assertTrue(len(res) > 0)

    def test_remove_owner(self):
        store: Store = Store("store1")
        store.get_owners_appointments().append(StoreAppointment(None, self.owner, []))
        owner1 = User()
        owner1.register("owner1", "password")
        store.add_owner(self.owner.get_nickname(), owner1)

        owner2 = User()
        owner2.register("owner2", "password")
        store.add_owner("owner1", owner2)

        owner3 = User()
        owner3.register("owner3", "password")
        store.add_owner("owner2", owner3)

        manager1 = User()
        manager1.register("manager1", "password")
        store.add_manager(owner3, manager1, [])

        manager2 = User()
        manager2.register("manager2", "password")
        store.add_manager(self.owner, manager2, [])

        # failed owner2 didn't appoint owner 2 as owner
        res = store.remove_owner("owner2", "owner1")
        self.assertEqual(res['response'], [])
        self.assertEqual(res['msg'], "Error! remove store owner failed.")

        # failed
        res = store.remove_owner("owner", "owner1")
        self.assertEqual(res['response'], [])
        self.assertEqual(res['msg'], "Error! remove store owner failed.")

        # success
        res = store.remove_owner(self.owner.get_nickname(), "owner1")

        self.assertEqual(res['response'], ['owner1 removed as owner', 'owner2 removed as owner', 'owner3 removed as owner', 'manager1 removed as manager'])
        self.assertEqual(res['msg'], "Store owner owner1 and his appointees were removed successfully.")
        self.assertFalse(store.is_owner('owner1'))
        self.assertFalse(store.is_owner('owner2'))
        self.assertFalse(store.is_owner('owner3'))
        self.assertFalse(store.is_manager('manager1'))
        self.assertTrue(store.is_manager('manager2'))

    def test_remove_owner_appointees(self):
        store: Store = Store("store")
        store.get_owners_appointments().append(StoreAppointment(None, self.owner, []))
        owner1 = User()
        owner1.register("owner1", "password")
        store.add_owner(self.owner.get_nickname(), owner1)

        owner2 = User()
        owner2.register("owner2", "password")
        store.add_owner("owner1", owner2)

        owner3 = User()
        owner3.register("owner3", "password")
        store.add_owner("owner2", owner3)

        manager1 = User()
        manager1.register("manager1", "password")
        store.add_manager(owner3, manager1, [])

        manager2 = User()
        manager2.register("manager2", "password")
        store.add_manager(self.owner, manager2, [])

        res = store.remove_owner_appointees("owner1")

        self.assertEqual(res, ['owner2 removed as owner', 'owner3 removed as owner', 'manager1 removed as manager'])
        self.assertTrue(store.is_owner('owner1'))
        self.assertFalse(store.is_owner('owner2'))
        self.assertFalse(store.is_owner('owner3'))
        self.assertFalse(store.is_manager('manager1'))
        self.assertTrue(store.is_manager('manager2'))

    def test_purchase_immediate(self):
        # purchase_immediate(self, product_name: str, product_price: int, amount: int, basket_price: int, prod_lst:[]):
        # ret format{'amount': 2, 'product_name': 'Eytan', 'product_price': 10} != 9
        result = self.store.purchase_immediate("Eytan", 10, 2, 0, ["Eytan"])
        self.assertEqual(9, result['product_price'])

        result = self.store.purchase_immediate("Eytan", 10, 2, 3, ["Eytan"])
        self.assertEqual(10, result['product_price'])

        result = self.store.purchase_immediate("Eytan2", 10, 2, 3, ["Eytan"])
        self.assertEqual(10, result['product_price'])

    # # @logger
    def tearDown(self) -> None:
        (DataAccessFacade.get_instance()).delete_stores()
        (DataAccessFacade.get_instance()).delete_users()
        self.store.reset_policies()
        self.store = None

    def __repr__(self):
        return repr("StoreTests")
