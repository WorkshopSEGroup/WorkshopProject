from src.Logger import errorLogger, loggerStaticMethod, logger
from src.main.DomainLayer.DeliveryComponent.DeliverySubject import DeliverySubject
from src.main.DomainLayer.DeliveryComponent.RealDelivery import RealDelivery


class DeliveryProxy(DeliverySubject):
    __instance = None
    __realSubject = RealDelivery()

    @staticmethod
    def get_instance():
        """ Static access method. """
        loggerStaticMethod("FacadeDelivery.get_instance", [])
        if DeliveryProxy.__instance is None:
            DeliveryProxy()
        return DeliveryProxy.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DeliveryProxy.__instance is not None:
            errorLogger("This class is a singleton!")
            raise Exception("This class is a singleton!")
        else:
            super().__init__()
            # self.__isConnected = False
            # if DeliveryProxy.__realSubject:
            #     DeliveryProxy.__instance = self.__realSubject
            # else:
            DeliveryProxy.__instance = self

    @logger
    def is_connected(self) -> bool:
        if self.__realSubject is None:
            return False

        # return self.__isConnected
        return self.__realSubject.is_connected()

    @logger
    def deliver_products(self, delivery_details: {'name': str, 'address': str, 'city': str, 'country': str,
                                                  'zip': str}) -> {'response': bool, 'msg': str, 'tid': int or None}:
        """
        :delivery_details:
        :return: dict = {'response': bool, 'msg': str}:
                 response = true if successful, otherwise false
        """
        # try:
        if self.__realSubject is None:
            return {'response': False, 'msg': "Delivery failed. System is down!"}

        if not self.__realSubject.is_connected():
            return {'response': False, 'msg': "Delivery failed. Delivery system is not connected"}

        delivered = self.__realSubject.deliver_products(delivery_details)

        if delivered["response"]:
            return {"response": True, "msg": "Delivery was successful. Transaction ID: " + delivered["msg"], "tid": delivered["msg"]}
        return delivered

    @logger
    def cancel_supply(self, transaction_id: str) -> {'response': bool, 'msg': str}:
        """
            cancel delivery
        :param transaction_id:
        :return:dict = {'response': bool, 'msg': str}:
                 response = true if successful, otherwise false
        """
        if self.__realSubject is None:
            return {'response': False, 'msg': "Delivery cancellation failed. System is down!"}

        if not self.__realSubject.is_connected():
            return {'response': False, 'msg': "Delivery cancellation failed. Delivery system is not connected."}

        return self.__realSubject.cancel_supply(transaction_id)

    def cause_connection_error(self):
        self.__realSubject.cause_connection_error()

    def cause_timeout_error(self):
        self.__realSubject.cause_timeout_error()

    def set_connection_back(self):
        self.__realSubject.set_connection_back()

    def set_real(self, real: RealDelivery):
        self.__realSubject = real

    def __delete__(self):
        DeliveryProxy.__instance = None

    def __repr__(self):
        return repr("DeliveryProxy")
