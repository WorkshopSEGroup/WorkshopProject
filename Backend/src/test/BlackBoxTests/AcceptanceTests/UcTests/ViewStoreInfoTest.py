"""
    test class for use case 2.4 - view stores' info and products
"""
from Backend.src.Logger import logger
from Backend.src.test.BlackBoxTests.AcceptanceTests.ProjectTest import ProjectTest


class ViewStoreInfoTest(ProjectTest):
    # @logger
    def setUp(self) -> None:
        super().setUp()
        self.register_user(self._username, self._password)
        self.login(self._username, self._password)
        self.open_store(self._store_name)
        self.add_products_to_store(self._store_name,
                                   [{"name": "product", "price": 10, "category": "general", "amount": 5}])

    # @logger
    def test_success(self):
        # existing stores in the system
        res = self.view_stores()
        self.assertTrue(res)
        res = self.display_stores_or_products_info(self._store_name, True, False)
        self.assertTrue(res)
        res = self.display_stores_or_products_info(self._store_name, False, True)
        self.assertTrue(res)

    # @logger
    def test_fail(self):
        # no products exist in the store
        self.remove_products_from_store(self._store_name, ["product"])
        res = self.display_stores_or_products_info(self._store_name, False, True)
        self.assertFalse(res)
        # no stores exists in the system
        self.remove_store(self._store_name)
        res = self.display_stores_or_products_info(self._store_name, True, False)
        self.assertFalse(res)

    # @logger
    def tearDown(self) -> None:
        self.delete_user(self._username)
        self.remove_products_from_store(self._store_name, ["product"])
        self.remove_store(self._store_name)

    def __repr__(self):
        return repr("ViewStoreInfoTest")