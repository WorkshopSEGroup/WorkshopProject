"""
    test class for use case 2.6 - save products to basket
"""
from src.test.BlackBoxTests.AcceptanceTests.ProjectTest import ProjectTest


class SaveProductsTest(ProjectTest):

    def setUp(self) -> None:
        pass

    def test_success(self):
        pass

    def test_fail(self):
        pass

    def test_fatal_error(self):
        self.reusableTests.test_server_error()

    def tearDown(self) -> None:
        pass