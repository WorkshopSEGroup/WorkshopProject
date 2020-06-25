from src.Logger import logger
from src.main.DomainLayer.TradeComponent.TradeControl import TradeControl
from src.main.DomainLayer.UserComponent.User import User
from src.main.ResponseFormat import ret


class SystemManagerRole:

    def __init__(self):
        pass

# ---------------------------------------------------- U.C 6.4 ---------------------------------------------------------
    @staticmethod
    @logger
    def view_user_purchase_history(viewed_user: str) -> {'response': list, 'msg': str}:
        """
        This function returns all the purchases that are done by a specific user.
        :param viewed_user: the user to view.
        :return: list of json objects containing the users' purchases or None if none exist
        """
        return TradeControl.get_instance().view_user_purchase_history(viewed_user)

    @staticmethod
    @logger
    def view_store_purchases_history(store_name: str) -> {'response': list, 'msg': str}:
        """
        :param store_name: the store to view
        :return: list of purchases
        """
        return TradeControl.get_instance().view_store_purchases_history(store_name)

    @staticmethod
    @logger
    def add_system_manager(username: str, password: str):
        """
        Add new system manager(a.k.a admin)

        :param username: new admin's username
        :param password: new admin's password
        :return: True if successful, False else.
        """
        return (TradeControl.get_instance()).add_system_manager(username, password)

    def __repr__(self):
        return repr("SystemManagerRole")

    @staticmethod
    @logger
    def get_visitors_cut(start_date, end_date):
        return TradeControl.get_instance().get_visitors_cut(start_date, end_date)

