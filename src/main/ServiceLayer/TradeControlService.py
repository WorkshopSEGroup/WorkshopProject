from datetime import datetime

from src.Logger import loggerStaticMethod
from src.main.DomainLayer.DeliveryComponent.DeliveryProxy import DeliveryProxy
from src.main.DomainLayer.PaymentComponent.PaymentProxy import PaymentProxy
from src.main.DomainLayer.TradeComponent.TradeControl import TradeControl
from src.main.ServiceLayer.GuestRole import GuestRole
from src.main.ServiceLayer.StoreOwnerOrManagerRole import StoreOwnerOrManagerRole
from src.main.ServiceLayer.SubscriberRole import SubscriberRole
from src.main.ServiceLayer.SystemManagerRole import SystemManagerRole
from src.main.ResponseFormat import ret
from ast import literal_eval
import os


class TradeControlService:

    def __init__(self):
        pass

    # use case 1.1
    @staticmethod
    def init_system():
        # Getting the file path
        abs_path = os.path.dirname(os.path.abspath(__file__))
        # rel_path = os.path.join(abs_path, 'init_sys_file_v3.txt')
        rel_path = os.path.join(abs_path, 'init_sys_file_v4.txt')
        if rel_path.split(".")[1] != "txt":
            print("Wrong format.")
            exit(1)
        rel_path = rel_path

        # init important vars
        delimiter = "//"
        funcs_as_dictionary = {"register": GuestRole.register,
                               "login": GuestRole.login,
                               "logout": SubscriberRole.logout,
                               "display_stores": GuestRole.display_stores,
                               "add_system_manager": SystemManagerRole.add_system_manager,
                               "open_store": TradeControlService.open_store,
                               # "open_store": SubscriberRole.open_store,
                               "add_products": StoreOwnerOrManagerRole.add_products,
                               "appoint_store_manager": StoreOwnerOrManagerRole.appoint_store_manager,
                                # Todo: test the below funcs.
                               "display_stores_or_products_info": GuestRole.display_stores_or_products_info,
                               "search_products_by": GuestRole.search_products_by,
                               "filter_products_by": GuestRole.filter_products_by,
                               "save_products_to_basket": GuestRole.save_products_to_basket,
                               "view_shopping_cart": GuestRole.view_shopping_cart,
                               "update_shopping_cart": GuestRole.update_shopping_cart,
                               "purchase_products": GuestRole.purchase_products,
                               "purchase_basket": GuestRole.purchase_basket,
                               "confirm_payment": GuestRole.confirm_payment,
                               "remove_products": StoreOwnerOrManagerRole.remove_products,
                               "edit_product": StoreOwnerOrManagerRole.edit_product,
                               "appoint_additional_owner": StoreOwnerOrManagerRole.appoint_additional_owner,
                               "remove_owner": StoreOwnerOrManagerRole.remove_owner,
                               "get_manager_permissions": StoreOwnerOrManagerRole.get_manager_permissions,
                               "get_appointees": StoreOwnerOrManagerRole.get_appointees,
                               "remove_manager": StoreOwnerOrManagerRole.remove_manager,
                               "display_store_purchases": StoreOwnerOrManagerRole.display_store_purchases,
                               "close_store": StoreOwnerOrManagerRole.close_store,
                               "get_purchase_operator": StoreOwnerOrManagerRole.get_purchase_operator,
                               "set_purchase_operator": StoreOwnerOrManagerRole.set_purchase_operator,
                               "get_policies": StoreOwnerOrManagerRole.get_policies,
                               "update_purchase_policy": StoreOwnerOrManagerRole.update_purchase_policy,
                               "define_purchase_policy": StoreOwnerOrManagerRole.define_purchase_policy,
                               "update_discount_policy": StoreOwnerOrManagerRole.update_discount_policy,
                               "define_discount_policy": StoreOwnerOrManagerRole.define_discount_policy,
                               "define_composite_policy": StoreOwnerOrManagerRole.define_composite_policy,
                               "get_discount_policy": StoreOwnerOrManagerRole.get_discount_policy,
                               "delete_policy": StoreOwnerOrManagerRole.delete_policy,
                               "get_managed_stores": StoreOwnerOrManagerRole.get_managed_stores,
                               "view_user_purchase_history": SystemManagerRole.view_user_purchase_history,
                               "view_personal_purchase_history": SubscriberRole.view_personal_purchase_history,
                               "view_store_purchases_history": SystemManagerRole.view_store_purchases_history}

        types_lst = [literal_eval, TradeControlService.convert_to_datetime, int, float, str]

        # Open file for validation of functions.
        file = open(rel_path, "rt")
        for line in file:
            func_blueprints = line.split(delimiter)
            if func_blueprints[0].replace("\n", "").lower() not in funcs_as_dictionary.keys():
                return ret(False, "Action doesn't exist. Please check the input format.")
        file.close()

        # Open file for executing the commands
        file = open(rel_path, "rt")
        try:
            for unedited_line in file:
                line = unedited_line.replace("\n", "")
                # Separating func_name, arg1, arg2...
                func_blueprints = line.split(delimiter)
                func = funcs_as_dictionary[func_blueprints[0].lower()]
                # Two strategies - if function have arguments, and if doesn't
                if len(func_blueprints) > 1:
                    # Getting the list of args
                    args = []
                    for j in range(1, len(func_blueprints)):
                        args.insert(len(args), func_blueprints[j])
                    # Converting str args to correct type
                    args_after_validating = []
                    for arg in args:
                        for typ in types_lst:
                            try:
                                arg_after_validation = typ(arg)
                                args_after_validating.insert(len(args_after_validating), arg_after_validation)
                                break
                            except Exception:
                                pass
                    # Execute the func
                    func_return_value = func(*(tuple(args_after_validating)))
                    # If failed, return false/None and msg.
                    if type(func_return_value['response']) is bool:
                        if not func_return_value['response']:
                            file.close()
                            return func_return_value
                    else:
                        if func_return_value['response'] is None:
                            file.close()
                            return func_return_value
                else:
                    # If the func doesn't have args, just execute it.
                    func_return_value = func()
                    # If failed, return false/None and msg.
                    if type(func_return_value['response']) is bool:
                        if not func_return_value['response']:
                            file.close()
                            return func_return_value
                    else:
                        if func_return_value['response'] is None:
                            file.close()
                            return func_return_value
        except Exception as ex:
            # print(ex)
            file.close()
            # TODO - THE BUG
            return ret(False, "An unknown error has occurred. Please check the input file arguments.")

        # connecting to external systems.
        if not DeliveryProxy.get_instance().is_connected():
            return {'response': False, 'msg': "Init system failed! connection to delivery system failed"}
        if not PaymentProxy.get_instance().is_connected():
            return {'response': False, 'msg': "Init system failed! connection to delivery system failed"}

        file.close()
        return ret(True, "Init Done. Welcome to the new Amazon!")

    @staticmethod
    def open_store(store_name):
        result = SubscriberRole.open_store(store_name)
        from src.main.CommunicationLayer.WebService import create_new_publisher
        create_new_publisher(store_name, TradeControlService.get_curr_username())
        return result

    @staticmethod
    def convert_to_datetime(arg: str):
        # format day.month.year
        output: [] = []
        date_blueprints = arg.split(".")
        for part in date_blueprints:
            output.insert(0, int(part))
        return datetime(*tuple(output))

    # @staticmethod
    # def init_system():
    #     loggerStaticMethod("init_system", [])
    #     if not DeliveryProxy.get_instance().is_connected() and not PaymentProxy.get_instance().is_connected():
    #         if TradeControl.get_instance().register_guest("TradeManager", "123456789"):
    #             if not DeliveryProxy.get_instance().connect():
    #                 return {'response': False, 'msg': "Init system failed! connection to delivery system failed"}
    #             if not PaymentProxy.get_instance().connect():
    #                 return {'response': False, 'msg': "Init system failed! connection to delivery system failed"}
    #             res = TradeControl.get_instance().add_system_manager("TradeManager", "123456789")
    #             if res['response']:
    #                 return {'response': True, 'msg': "Init system was successful!"}
    #             return {'response': False, 'msg': "Init system failed! " + res['msg']}
    #     return {'response': False, 'msg': "Init system failed!"}

    # functions for tests
    @staticmethod
    def remove_user(nickname: str):
        TradeControl.get_instance().unsubscribe(nickname)

    @staticmethod
    def remove_manager(store_name: str, appointee_nickname: str):
        TradeControl.get_instance().remove_manager(store_name, appointee_nickname)

    @staticmethod
    def remove_store(store_name: str):
        TradeControl.get_instance().close_store(store_name)

    # external system tests functions
    @staticmethod
    def is_payment_connected():
        return PaymentProxy.get_instance().is_connected()

    @staticmethod
    def commit_payment( payment_details: {'card_number': str, 'month': str, 'year': str, 'holder': str,
                                               'ccv': str, 'id': str}):
        return PaymentProxy.get_instance().commit_payment(payment_details)

    @staticmethod
    def cancel_payment(transaction_id: str):
        return PaymentProxy.get_instance().cancel_pay(transaction_id)

    def cause_payment_timeout(self):
        PaymentProxy.get_instance().cause_timeout_error()

    def cause_payment_con_error(self):
        PaymentProxy.get_instance().cause_connection_error()

    def set_connection_payment_back(self):
        PaymentProxy.get_instance().set_connection_back()

    @staticmethod
    def is_delivery_connected():
        return DeliveryProxy.get_instance().is_connected()

    @staticmethod
    def deliver(delivery_details: {'name': str, 'address': str, 'city': str, 'country': str,
                                                  'zip': str}):
        return DeliveryProxy.get_instance().deliver_products(delivery_details)

    @staticmethod
    def cancel_delivery(transaction_id: str):
        return DeliveryProxy.get_instance().cancel_supply(transaction_id)

    @staticmethod
    def cause_delivery_timeout():
        DeliveryProxy.get_instance().cause_timeout_error()

    @staticmethod
    def cause_delivery_con_error():
        DeliveryProxy.get_instance().cause_connection_error()

    @staticmethod
    def set_connection_delivery_back():
        DeliveryProxy.get_instance().set_connection_back()
    # end external system tests functions

    @staticmethod
    def subscribe_user(nickname: str, password: str):
        TradeControl.get_instance().register_test_user(nickname, password)

    @staticmethod
    def remove_purchase(store_name: str, purchase_date: datetime):
        TradeControl.get_instance().remove_purchase(store_name, purchase_date)

    @staticmethod
    def set_user(nickname: str):
        TradeControl.get_instance().set_curr_user_by_name(nickname)

    @staticmethod
    def get_store(store_name):
        return TradeControl.get_instance().get_store(store_name)

    @staticmethod
    def get_user_type():
        return TradeControl.get_instance().get_user_type()

    @staticmethod
    def get_product_details(store_name, product_name):
        return TradeControl.get_product_details(store_name, product_name)

    @staticmethod
    def get_curr_username():
        return TradeControl.get_instance().get_curr_username()

    @staticmethod
    def inc_todays_guests_counter():
        TradeControl.get_instance().inc_todays_guests_counter()

    def __repr__(self):
        return repr("TradeFacadeService")
