import unittest
from unittest.mock import MagicMock
from src.main.DomainLayer.DeliveryComponent.DeliveryProxy import DeliveryProxy
from src.main.DomainLayer.DeliveryComponent.RealDelivery import RealDelivery
from src.main.DomainLayer.TradeComponent.TradeControl import TradeControl


class FacadeDeliveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.__delivery_sys: DeliveryProxy = DeliveryProxy.get_instance()
        self.__real_delivery_mock = RealDelivery()
        self.__delivery_sys.set_real(self.__real_delivery_mock)
        self.__valid_username = "username"
        self.__delivery_details = {'name': "nickname", 'address': "address 12", 'city': "ct", 'country': "i",
                                   'zip': "123"}

    def test_is_connected(self):
        # test that system is connected fine
        self.__real_delivery_mock.is_connected = MagicMock(return_value=True)
        self.assertTrue(self.__delivery_sys.is_connected())
        # test connection error
        self.__real_delivery_mock.is_connected = MagicMock(return_value=False)
        res = self.__real_delivery_mock.is_connected()
        self.assertFalse(self.__delivery_sys.is_connected())

    def test_deliver(self):
        # test valid delivery
        self.__real_delivery_mock.deliver_products = MagicMock(return_value={"response": True, "msg": "ok"})
        self.assertTrue(self.__delivery_sys.deliver_products(self.__delivery_details)["response"])
        # test connection error
        self.__real_delivery_mock.is_connected = MagicMock(return_value=False)
        self.assertFalse(self.__delivery_sys.deliver_products(self.__delivery_details)["response"])
        # test invalid delivery details
        self.__real_delivery_mock.deliver_products = MagicMock(return_value={"response": False, "msg": "ok"})
        self.assertFalse(self.__delivery_sys.deliver_products({'name': "nickname", 'address': "address 12",
                                                               'city': "ct", 'country': "i"})["response"])
        self.assertFalse(self.__delivery_sys.deliver_products({'name': "nickname", 'address': "address 12",
                                                               'city': "ct", 'zip': "123"})["response"])
        self.assertFalse(self.__delivery_sys.deliver_products({'name': "nickname", 'address': "address 12",
                                                               'country': "i", 'zip': "123"})["response"])
        self.assertFalse(self.__delivery_sys.deliver_products({'name': "nickname", 'city': "ct", 'country': "i",
                                                               'zip': "123"})["response"])
        self.assertFalse(self.__delivery_sys.deliver_products({'address': "address 12", 'city': "ct", 'country': "i",
                                                               'zip': "123"})["response"])
        self.assertFalse(self.__delivery_sys.deliver_products({'name': "nickname", 'address': "address 12",
                                                               'city': "ct"})["response"])
        self.assertFalse(self.__delivery_sys.deliver_products({'name': "nickname",
                                                               'address': "address 12"})["response"])
        self.assertFalse(self.__delivery_sys.deliver_products({'name': "nickname"})["response"])
        self.assertFalse(self.__delivery_sys.deliver_products({'city': "ct", 'country': "i", 'zip': "123"})["response"])
        self.assertFalse(self.__delivery_sys.deliver_products({'country': "i", 'zip': "123"})["response"])

    def test_cancel_delivery(self):
        # test valid delivery cancellation
        self.__real_delivery_mock.cancel_supply = MagicMock(return_value={"response": True, "msg": "ok"})
        res = self.__delivery_sys.cancel_supply("2020")
        self.assertTrue(res["response"])
        # test connection error
        self.__real_delivery_mock.is_connected = MagicMock(return_value=False)
        self.assertFalse(self.__delivery_sys.cancel_supply("2020")["response"])
        # test invalid delivery cancellation
        self.__real_delivery_mock.cancel_supply = MagicMock(return_value={"response": False, "msg": "ok"})
        self.assertFalse(self.__delivery_sys.cancel_supply("1")["response"])

    def tearDown(self) -> None:
        (TradeControl.get_instance()).__delete__()

    if __name__ == '__main__':
        unittest.main()

    def __repr__(self):
        return repr ("FacadeDeliveryTests")