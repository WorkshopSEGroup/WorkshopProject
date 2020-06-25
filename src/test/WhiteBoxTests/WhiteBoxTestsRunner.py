"""
    test suite class - used to organize the tests and run them together
"""
import unittest
# from src.test.WhiteBoxTests.UnitTests import TestCases
# ---------------------------------- unit tests imports ----------------------------------------------------------------
from src.test.WhiteBoxTests.UnitTests.TestCases.DomainLayer.DeliveryComponent.FacadeDeliveryTests \
     import FacadeDeliveryTests as Uc1
from src.test.WhiteBoxTests.UnitTests.TestCases.DomainLayer.PaymentComponent.FacadePaymentTests \
    import FacadePaymentTests as Uc2
from src.main.DataAccessLayer.ConnectionProxy.Tables import rel_path
from src.main.DataAccessLayer.DataAccessFacade import DataAccessFacade
from src.test.WhiteBoxTests.UnitTests.TestCases.DomainLayer.StoreComponent.PurchasePolicyComposite.Leaves.\
    BundleDealPolicyTests import BundleDealPolicyTests as Uc3
from src.test.WhiteBoxTests.UnitTests.TestCases.DomainLayer.StoreComponent.PurchasePolicyComposite.Leaves.\
    MaxAmountPolicyTests import MaxAmountPolicyTests as Uc4
from src.test.WhiteBoxTests.UnitTests.TestCases.DomainLayer.StoreComponent.PurchasePolicyComposite.Leaves.\
    MinAmountPolicyTests import MinAmountPolicyTests as Uc5
from src.test.WhiteBoxTests.UnitTests.TestCases.DomainLayer.StoreComponent.PurchasePolicyComposite.Leaves.\
    ProhibitedDatePolicyTests import ProhibitedDatePolicyTests as Uc6
from src.test.WhiteBoxTests.UnitTests.TestCases.DomainLayer.StoreComponent.PurchasePolicyComposite.PurchasePolicyTests\
    import PurchasePolicyTests as Uc7
from src.test.WhiteBoxTests.UnitTests.TestCases.DomainLayer.StoreComponent.StoreInventoryTests \
    import StoreInventoryTests as Uc8
from src.test.WhiteBoxTests.UnitTests.TestCases.DomainLayer.StoreComponent.StoreTests \
    import StoreTests as Uc9
from src.test.WhiteBoxTests.UnitTests.TestCases.DomainLayer.TradeComponent.TradeControlTestCase \
    import TradeControlTestCase as Uc10
from src.test.WhiteBoxTests.UnitTests.TestCases.DomainLayer.UserComponent.ShoppingBasketTests \
    import ShoppingBasketTests as Uc11
from src.test.WhiteBoxTests.UnitTests.TestCases.DomainLayer.UserComponent.ShoppingCartTests \
    import ShoppingCartTests as Uc12
from src.test.WhiteBoxTests.UnitTests.TestCases.DomainLayer.UserComponent.UserTests \
    import UserTests as Uc13
from src.test.WhiteBoxTests.UnitTests.TestCases.ServiceLayer.StoreOwnerOrManagerTests \
    import StoreOwnerOrManagerTests as Uc14
from src.test.WhiteBoxTests.UnitTests.TestCases.ServiceLayer.SubscriberRoleTests \
    import SubscriberRoleTests as Uc15
from src.test.WhiteBoxTests.UnitTests.TestCases.ServiceLayer.SystemManagerRoleTests \
    import SystemManagerRoleTests as Uc16
from src.test.WhiteBoxTests.UnitTests.TestCases.ServiceLayer.TradeControlServiceTests \
    import TradeControlServiceTests as Uc17
from src.test.WhiteBoxTests.UnitTests.TestCases.ServiceLayer.GuestRoleTests \
    import GuestRoleTest as Uc18
# ---------------------------------- end unit tests imports ------------------------------------------------------------
# ---------------------------------- integration tests imports ---------------------------------------------------------
from src.test.WhiteBoxTests.IntegrationTests.DomainLayer.StoreComponent.PurchasePolicyComposite.PurchasePolicyTests \
    import PurchasePolicyTests as Ut1
from src.test.WhiteBoxTests.IntegrationTests.DomainLayer.StoreComponent.PurchasePolicyComposite.Leaves.\
    ProhibitedDatePolicyTests import ProhibitedDatePolicyTests as Ut2
from src.test.WhiteBoxTests.IntegrationTests.DomainLayer.StoreComponent.PurchasePolicyComposite.Leaves.\
    MinAmountPolicyTests import MinAmountPolicyTests as Ut3
from src.test.WhiteBoxTests.IntegrationTests.DomainLayer.StoreComponent.PurchasePolicyComposite.Leaves.\
    MaxAmountPolicyTests import MaxAmountPolicyTests as Ut4
from src.test.WhiteBoxTests.IntegrationTests.DomainLayer.StoreComponent.PurchasePolicyComposite.Leaves.\
    BundleDealPolicyTests import BundleDealPolicyTests as Ut5
from src.test.WhiteBoxTests.IntegrationTests.DomainLayer.StoreComponent.DiscountPolicyComposite.DiscountPolicyTests \
    import DiscountPolicyTests as Ut6
from src.test.WhiteBoxTests.IntegrationTests.DomainLayer.StoreComponent.StoreInventoryTests import \
    StoreInventoryTests as Ut7
from src.test.WhiteBoxTests.IntegrationTests.DomainLayer.StoreComponent.StoreTests import StoreTests as Ut8
from src.test.WhiteBoxTests.IntegrationTests.DomainLayer.UserComponent.UserTests import UserTests as Ut9
from src.test.WhiteBoxTests.IntegrationTests.DomainLayer.UserComponent.ShoppingCartTests import \
    ShoppingCartTests as Ut10
from src.test.WhiteBoxTests.IntegrationTests.DomainLayer.UserComponent.ShoppingBasketTests import \
    ShoppingBasketTests as Ut11
from src.test.WhiteBoxTests.IntegrationTests.DomainLayer.TradeComponent.TradeControlTestCase import \
    TradeControlTestCase as Ut12
from src.test.WhiteBoxTests.IntegrationTests.ServiceLayer.GuestRoleTests import GuestRoleTest as Ut13
from src.test.WhiteBoxTests.IntegrationTests.ServiceLayer.SystemManagerRoleTests import SystemManagerRoleTests as Ut14
from src.test.WhiteBoxTests.IntegrationTests.ServiceLayer.SubscriberRoleTests import SubscriberRoleTests as Ut15
from src.test.WhiteBoxTests.IntegrationTests.ServiceLayer.StoreOwnerOrManagerTests import \
    StoreOwnerOrManagerTests as Ut16
# ---------------------------------- end integration tests imports -----------------------------------------------------


class WhiteBoxTestsRunner:
    # Build test suit
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    # add all tests to test suite
    # suite.addTests(loader.loadTestsFromModule(TestCases))

    # add individual tests to the test suite
# ---------------------------------- add unit tests --------------------------------------------------------------------
#     TODO: for some reason they give error in runner but not in tests, check it out later
    suite.addTest(loader.loadTestsFromTestCase(Uc1))
    suite.addTest(loader.loadTestsFromTestCase(Uc2))
    suite.addTest(loader.loadTestsFromTestCase(Uc3))
    suite.addTest(loader.loadTestsFromTestCase(Uc4))
    suite.addTest(loader.loadTestsFromTestCase(Uc5))
    suite.addTest(loader.loadTestsFromTestCase(Uc6))
    suite.addTest(loader.loadTestsFromTestCase(Uc7))
    suite.addTest(loader.loadTestsFromTestCase(Uc8))
    suite.addTest(loader.loadTestsFromTestCase(Uc9))
    suite.addTest(loader.loadTestsFromTestCase(Uc10))
    suite.addTest(loader.loadTestsFromTestCase(Uc11))
    suite.addTest(loader.loadTestsFromTestCase(Uc12))
    suite.addTest(loader.loadTestsFromTestCase(Uc13))
    suite.addTest(loader.loadTestsFromTestCase(Uc14))
    suite.addTest(loader.loadTestsFromTestCase(Uc15))
    suite.addTest(loader.loadTestsFromTestCase(Uc16))
    suite.addTest(loader.loadTestsFromTestCase(Uc17))
    suite.addTest(loader.loadTestsFromTestCase(Uc18))
# ---------------------------------- add unit tests end ----------------------------------------------------------------

# ---------------------------------- add integration tests -------------------------------------------------------------
    suite.addTest(loader.loadTestsFromTestCase(Ut1))
    suite.addTest(loader.loadTestsFromTestCase(Ut2))
    suite.addTest(loader.loadTestsFromTestCase(Ut3))
    suite.addTest(loader.loadTestsFromTestCase(Ut4))
    suite.addTest(loader.loadTestsFromTestCase(Ut5))
    suite.addTest(loader.loadTestsFromTestCase(Ut6))
    suite.addTest(loader.loadTestsFromTestCase(Ut7))
    suite.addTest(loader.loadTestsFromTestCase(Ut8))
    suite.addTest(loader.loadTestsFromTestCase(Ut9))
    suite.addTest(loader.loadTestsFromTestCase(Ut10))
    suite.addTest(loader.loadTestsFromTestCase(Ut11))
    suite.addTest(loader.loadTestsFromTestCase(Ut12))
    suite.addTest(loader.loadTestsFromTestCase(Ut13))
    suite.addTest(loader.loadTestsFromTestCase(Ut14))
    suite.addTest(loader.loadTestsFromTestCase(Ut15))
    suite.addTest(loader.loadTestsFromTestCase(Ut16))

# ---------------------------------- add integration tests end ---------------------------------------------------------

    if not ("testing" in rel_path):
        raise ReferenceError("The Data Base is not the testing data base.\n"
                             "\t\t\t\tPlease go to src.main.DataAccessLayer.ConnectionProxy.RealDb.rel_path\n"
                             "\t\t\t\t and change rel_path to test_rel_path.\n"
                             "\t\t\t\tThanks :D")

    # pass runner the suite and run it
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

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
    unittest.main()


