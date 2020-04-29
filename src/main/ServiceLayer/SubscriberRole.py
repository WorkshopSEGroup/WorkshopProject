from src.Logger import logger
from src.main.DomainLayer.TradeComponent.TradeControl import TradeControl


class SubscriberRole:

    def __init__(self):
        pass

    # @logger
    @staticmethod
    # use case 3.1
    def logout():
        """
        logs the subscriber out of the system
        :return: True if succeeded, otherwise False
        """
        return TradeControl.get_instance().logout_subscriber()

    @staticmethod
    @logger
    # 3.2 open store
    def open_store(store_name: str):
        """
        Opens a new store with the given store name
        :param store_name: String
        :return: true if the store is created, else false
        """
        return TradeControl.get_instance().open_store(store_name)

    @staticmethod
    @logger
    # use case 3.7
    def view_personal_purchase_history():
        """
        View the subscriber's purchase history
        :return: list of json objects containing the subscriber's purchase history or None if none exist
        """
        return TradeControl.get_instance().view_personal_purchase_history()

    def __repr__(self):
        return repr("SubscriberRole")
