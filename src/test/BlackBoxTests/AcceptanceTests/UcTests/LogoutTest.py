"""
    test class for use case 3.1 - logout
"""
from src.test.BlackBoxTests.AcceptanceTests.ProjectTest import ProjectTest


class LogoutTest(ProjectTest):

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