from src.Logger import errorLogger, logger, loggerStaticMethod
from src.main.DomainLayer.PaymentComponent.PaymentSubject import PaymentSubject
from src.main.DomainLayer.PaymentComponent.RealPayment import RealPayment


class PaymentProxy(PaymentSubject):
    __instance = None
    __realSubject = RealPayment()

    @staticmethod
    def get_instance():
        """ Static access method. """
        loggerStaticMethod("FacadePayment.get_instance", [])
        if PaymentProxy.__instance is None:
            PaymentProxy()
        return PaymentProxy.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if PaymentProxy.__instance is not None:
            errorLogger("This class is a singleton!")
            raise Exception("This class is a singleton!")
        else:
            super().__init__()
            PaymentProxy.__instance = self

    @logger
    def is_connected(self) -> bool:
        if self.__realSubject is None:
            return False
        return self.__realSubject.is_connected()

    @logger
    # need to check payment details with system once a system is set
    def commit_payment(self, payment_details: {'card_number': str, 'month': str, 'year': str, 'holder': str,
                                               'ccv': str, 'id': str}) -> {'response': bool, 'msg': str, 'tid': int or None}:
        """

        :param payment_details:
        :return: dict = {'response': bool, 'msg': str}:
                 response = true if successful, otherwise false
        """
        if self.__realSubject is None:
            return {'response': False, 'msg': "Payment failed. System is down!"}

        if not self.__realSubject.is_connected():
            return {'response': False, 'msg': "Payment failed. Delivery system is not connected"}

        payed = self.__realSubject.commit_payment(payment_details)

        if payed["response"]:
            return {"response": True, "msg": "Payment was successful. Transaction ID: " + payed["msg"], "tid": payed["msg"]}
        return payed

    @logger
    def cancel_pay(self, transaction_id: str) -> {'response': bool, 'msg': str}:
        """

        :param transaction_id:
        :return: dict = {'response': bool, 'msg': str}:
                 response = true if successful, otherwise false
        """

        if self.__realSubject is None:
            return {'response': False, 'msg': "Payment cancellation failed. System is down!"}

        if not self.__realSubject.is_connected():
            return {'response': False, 'msg': "Payment cancellation failed. Delivery system is not connected."}

        return self.__realSubject.cancel_pay(transaction_id)

    def cause_connection_error(self):
        self.__realSubject.cause_connection_error()

    def cause_timeout_error(self):
        self.__realSubject.cause_timeout_error()

    def set_connection_back(self):
        self.__realSubject.set_connection_back()

    def set_real(self, real: RealPayment or None):
        self.__realSubject = real

    def __delete__(self):
        PaymentProxy.__instance = None

    def __repr__(self):
        return repr("FacadePayment")