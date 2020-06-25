import unittest
from src.main.CommunicationLayer import WebService
# from src.main.CommunicationLayer import WebSocketService

# TODO - mocks
class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.__username = "Yarin"
        self.__store_name = "Some Store"

    def test_open_store(self):
        # valid
        WebService.create_new_publisher(self.__store_name, self.__username)
        self.assertIsNotNone(WebService.get_store(self.__store_name))

        # not valid
        self.assertFalse(WebService.create_new_publisher(self.__store_name, self.__username))
        self.assertFalse(WebService.create_new_publisher(self.__store_name, "another user"))

    def test_add_subscriber(self):
        WebService.create_new_publisher("store number 2", self.__username)
        # valid
        # WebService.add_subscriber_to_store(self.__store_name, self.__username)
        self.assertEqual(True, WebService.is_subscribed_to_store("store number 2", self.__username))

        # not valid
        self.assertFalse(WebService.is_subscribed_to_store(self.__store_name, "Ron"))
        self.assertNotEqual(True, WebService.is_subscribed_to_store("Other Store", self.__username))
        self.assertFalse(WebService.add_subscriber_to_store(self.__store_name, self.__username, True))

        # add another subscriber to same store
        WebService.add_subscriber_to_store("store number 2", "new owner", True)
        self.assertEqual(True, WebService.is_subscribed_to_store("store number 2", "new owner"))

        # subscribe self.user to another store
        WebService.create_new_publisher("New Store", self.__username)
        self.assertEqual(True, WebService.is_subscribed_to_store("New Store", self.__username))

        WebService.add_subscriber_to_store("New Store", "Ron", True)
        self.assertEqual(True, WebService.is_subscribed_to_store("New Store", self.__username))

    def test_remove_subscriber(self):
        WebService.create_new_publisher("remove test store", "first owner")
        WebService.add_subscriber_to_store("remove test store", self.__username, True)

        # valid
        self.assertEqual(0, WebService.remove_subscriber_from_store("remove test store", self.__username))
        self.assertEqual(False, WebService.is_subscribed_to_store("remove test store", self.__username))
        self.assertEqual(1, WebService.get_store("remove test store").amount_of_subscribers())

        # not valid
        self.assertEqual(-1, WebService.remove_subscriber_from_store(self.__store_name, self.__username))
        self.assertEqual(-2, WebService.remove_subscriber_from_store("Store", self.__username))
        self.assertEqual(-1, WebService.remove_subscriber_from_store(self.__store_name, "Username"))

    def test_update_queue_after_purchase(self):
        # WebService.handle_purchase(user_name=self.__username, )
        WebService.create_new_publisher(self.__store_name, self.__username)
        store = WebService.get_store(self.__store_name)

        # valid
        store.add_msg('msg', 'message')
        self.assertEqual(1, len(store.retrieveMsgs(self.__username)))


if __name__ == '__main__':
    unittest.main()
