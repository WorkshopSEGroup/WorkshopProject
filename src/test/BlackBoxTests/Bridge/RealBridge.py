"""
    class representing the:
                            - concrete implementor in the Bridge pattern
                            - adapter in the the adapter pattern
                            - real subject in the proxy pattern
"""
from src.main.DomainLayer.DeliveryComponent.DeliveryProxy import DeliveryProxy
from src.test.BlackBoxTests.Bridge.Bridge import Bridge
from src.main.DomainLayer.PaymentComponent.PaymentProxy import PaymentProxy
from src.main.ServiceLayer.TradeControlService import TradeControlService
from src.main.DomainLayer.TradeComponent.TradeControl import TradeControl
from src.main.ServiceLayer.GuestRole import GuestRole


class RealBridge(Bridge):

    def __init__(self):
        super().__init__()
        self.__paymentSys = PaymentProxy.get_instance()
        self.__deliverySys = DeliveryProxy.get_instance()
        self.__trade_control_srv = TradeControlService()
        self.__trade_control = TradeControl.get_instance()
        self.__guest_role = GuestRole()
        self.__subscriber = None
        # self.__store_manager = StoreManagerRole(self.__subscriber)
        self.__store_owner = None

    def register_user(self, username, password) -> bool:
        self.__guest_role = GuestRole()
        res = self.__guest_role.register(username, password)
        return res is not None

    def connect_payment_sys(self):
        self.__paymentSys.connect()

    def disconnect_payment_sys(self):
        self.__paymentSys.disconnect()

    def commit_payment(self, username, amount, credit, date) -> bool:
        return self.__paymentSys.commit_payment(username, amount, credit, date)

    def is_payment_connected(self):
        return self.__paymentSys.is_connected()

    def connect_delivery_sys(self):
        self.__deliverySys.connect()

    def deliver(self, username, address) -> bool:
        return self.__deliverySys.deliver_products(username, address)

    def disconnect_delivery_sys(self):
        self.__deliverySys.disconnect()

    def is_delivery_connected(self):
        return self.__deliverySys.is_connected()

    def init_sys(self):
        self.__trade_control_srv.init_system()

    def remove_user(self, username):
        self.__trade_control.unsubscribe(username)
        self.__trade_control.remove_manager(str, )

    def login(self, username, password):
        res = self.__guest_role.login(username, password)
        self.__subscriber = res
        return res is not None

    def search_product(self, option, string):
        res = self.__guest_role.search_products_by(option, string)
        return res is not None and len(res) != 0

    def filter_products(self, filter_details, products):
        res = self.__guest_role.filter_products_by(filter_details, products)
        return res is not None and len(res) != 0

    def view_stores(self):
        res = self.__guest_role.display_stores()
        return res is not None and len(res) != 0

    def logout(self):
        return self.__subscriber.logout()

    def add_products_to_cart(self, nickname, products_stores_quantity_ls):
        return self.__guest_role.save_products_to_basket(nickname, products_stores_quantity_ls)

    def view_personal_history(self):
        pass
    # TODO

    def open_store(self, name):
        res = self.__subscriber.open_store(name)
        self.__store_owner = res
        return res is not None

    def delete_store(self, store_name):
        self.__trade_control.close_store(store_name)

    def add_products_to_store(self, user_nickname, store_name, products_details):
        self.__store_owner.add_products(,
        return self.__store_owner.get_store(store_name).get_product(products_details[0][0]) is not None

    def edit_products_in_store(self, nickname, store_name, product_name, op, new_value):
        self.__store_owner.edit_product("", product_name, op, new_value)
        return self.__store_owner.get_store(store_name).get_product(product_name).get_price() == new_value

    def remove_products_from_store(self, user_nickname, store_name, products_names):
        self.__store_owner.remove_products(store_name, )
        return self.__store_owner.get_store(store_name).get_product(products_names) is None

    def appoint_additional_owner(self, nickname, store_name):
        self.__store_owner.appoint_additional_owner(,
        return self.__store_owner.get_store(store_name).is_owner(nickname)

    def appoint_additional_manager(self, nickname, store_name, permissions):
        self.__store_owner.appoint_store_manager(permissions,,
        return self.__store_owner.get_store(store_name).is_manager(nickname)

    def remove_manager(self, store_name, manager_nickname, permissions):
        res = self.__store_owner.get_store(store_name).is_manager(manager_nickname)
        self.__store_owner.remove_manager(str, )
        return not self.__store_owner.get_store(store_name).is_manager(manager_nickname) and res
