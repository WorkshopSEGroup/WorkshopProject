import requests

from src.Logger import logger
from src.main.DomainLayer.PaymentComponent.PaymentSubject import PaymentSubject
from requests.exceptions import HTTPError, ConnectionError, ProxyError, SSLError, Timeout


class RealPayment(PaymentSubject):

    def __init__(self):
        super().__init__()
        self.__url = 'https://cs-bgu-wsep.herokuapp.com/'
        self.__max_timeout = 10

    @logger
    def is_connected(self) -> bool:
        try:
            res = requests.post(self.__url, data={'action_type': 'handshake'}, timeout=self.__max_timeout)

            if res is not None and res.text == "OK":
                return True
            else:
                # if response from the server is not "OK" or if the server didn't reply
                return False
        except Exception:
            # if there is a connection error or the server timed out
            return False

    @logger
    def commit_payment(self, payment_details: {'card_number': str, 'month': str, 'year': str, 'holder': str,
                                               'ccv': str, 'id': str}) -> {'response': bool, 'msg': str}:
        """

        :param payment_details:
        :return: dict = {'response': bool, 'msg': str}:
                 response = true if successful, otherwise false
        """
        try:
            res = requests.post(self.__url,
                                data={'action_type': 'pay', 'card_number': payment_details.get('card_number'),
                                      'month': payment_details.get('month'), 'year': payment_details.get('year'),
                                      'holder': payment_details.get('holder'), 'ccv': payment_details.get('ccv'),
                                      'id': payment_details.get('id')},
                                timeout=self.__max_timeout)
            if res is None:
                return {'response': False, 'msg': "Payment failed. Server didn't reply"}

            transaction_id = int(res.text)

            if res is not None and 10000 <= transaction_id <= 100000:
                return {'response': True, 'msg': res.text}
            else:
                return {'response': False, 'msg': "Payment failed. Transaction has failed."}
        except (HTTPError, ConnectionError, ProxyError, SSLError, ValueError):
            return {'response': False, 'msg': "Payment failed. An error occurred during connection to the server."}
        except Timeout:
            return {'response': False, 'msg': "Payment failed. The request timed out."}

    @logger
    def cancel_pay(self, transaction_id: str) -> {'response': bool, 'msg': str}:
        """

        :param transaction_id:
        :return: dict = {'response': bool, 'msg': str}:
                 response = true if successful, otherwise false
        """
        try:
            res = requests.post(self.__url,
                                data={'action_type': 'cancel_pay', ' transaction_id': transaction_id},
                                timeout=self.__max_timeout)
            if res is None:
                return {'response': False, 'msg': "Payment cancellation failed. Server didn't reply"}

            cancellation = int(res.text)

            if res is not None and cancellation == 1:
                return {'response': True, 'msg': "Payment was cancelled successfully."}
            else:
                return {'response': False, 'msg': "Payment cancellation failed."}
        except (HTTPError, ConnectionError, ProxyError, SSLError, ValueError):
            return {'response': False, 'msg': "Payment cancellation failed. An error occurred during connection to "
                                              "the server."}
        except Timeout:
            return {'response': False, 'msg': "Payment cancellation failed. The request timed out."}

    def cause_connection_error(self):
        self.__url = 'https://errorUrl/'

    def cause_timeout_error(self):
        self.__max_timeout = 0.001

    def set_connection_back(self):
        self.__url = 'https://cs-bgu-wsep.herokuapp.com/'
        self.__max_timeout = 10

