from datetime import datetime

from src.Logger import errorLogger, logger
from src.main.DomainLayer.StoreComponent.AppointmentStatus import AppointmentStatus
from src.main.DomainLayer.StoreComponent.Purchase import Purchase
from src.main.DomainLayer.StoreComponent.Store import Store
from src.main.DomainLayer.StoreComponent.StoreAppointment import StoreAppointment
from src.main.DomainLayer.TradeComponent.Statistics import Statistics
from src.main.DomainLayer.UserComponent.DiscountType import DiscountType
from src.main.DomainLayer.UserComponent.PurchaseType import PurchaseType
from src.main.DomainLayer.UserComponent.User import User
from src.main.DomainLayer.StoreComponent.ManagerPermission import ManagerPermission
from src.main.DataAccessLayer.DataAccessFacade import DataAccessFacade
from src.main.ResponseFormat import ret
import jsonpickle


class TradeControl:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        # loggerStaticMethod("TradeControl.get_instance", [])
        if TradeControl.__instance is None:
            TradeControl()
        return TradeControl.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if TradeControl.__instance is not None:
            errorLogger("This class is a singleton!")
            raise Exception("This class is a singleton!")
        else:
            self.__today = datetime(datetime.today().year, datetime.today().month, datetime.today().day) # TODO?
            self.__curr_user = User()
            self.__managers = []
            self.__subscribers = self.__pull_subscribers_from_db()
            self.__stores = self.__pull_stores_from_db()
            self.__pull_shopping_carts()
            self.__pull_personal_purchases()
            # except Exception as e:
            #     print(e)
            # self.__stores.append(Store("Einat"))
            self.__statistics : [Statistics] = [Statistics()]
            # self.__stores.append(Store("einat"))
            # self.__stores.append(Store("Eden"))
            (DataAccessFacade.get_instance()).write_statistic()
            TradeControl.__instance = self

    @logger
    def get_sys_managers_amount(self):
        return len(self.__managers)

    @logger
    # ------- TradeControlService function
    def add_system_manager(self, nickname: str, password: str) -> dict:
        """
        adds system manager if not already exist
        :param nickname:
        :param password:
        :return: dict = {'response': bool, 'msg': str}
        """

        for s in self.__managers:
            if s.get_nickname() == nickname:
                return {'response': False, 'msg': "User " + nickname + " is already a system manager"}

        if self.get_subscriber(nickname):
            temp = User()
            temp.register(nickname, password)
            self.__managers.append(temp)
            db_result = (DataAccessFacade.get_instance()).update_users(old_username=nickname,
                                                                       new_is_system_manager=True)
            if not db_result['response']:
                return db_result
            return {'response': True, 'msg': "User " + nickname + " was registered as system manager successfully"}
        else:
            if len(self.__managers) == 0:
                self.register_guest(nickname, password)
                self.__managers.append(self.get_subscriber(nickname))
                db_result = (DataAccessFacade.get_instance()).update_users(old_username=nickname,
                                                                           new_is_system_manager=True)
                if not db_result['response']:
                    return db_result
                return {'response': True, 'msg': "User " + nickname + " was registered as system manager successfully"}
            else:
                return {'response': False, 'msg': "User " + nickname + " is not registered as a subscriber"}

    @logger
    def register_test_user(self, nickname: str, password: str):
        """
        TODO: I think its for AT
        :param nickname:
        :param password:
        :return:
        """
        user = User()
        user.register(nickname, password)
        self.subscribe(user)

    @logger
    # ----   Guest functions   ----
    def register_guest(self, nickname: str, password: str) -> {'response': bool, 'msg': str}:
        """
        register new guest if not exist already
        :param nickname:
        :param password:
        :return: {'response': bool, 'msg': str}
        """
        if not self.validate_nickname(nickname):
            return {'response': False, 'msg': "Invalid nickname, nickname already exist"}
        new_suscriber = User()
        result = new_suscriber.register(nickname, password)
        if result['response']:
            self.subscribe(new_suscriber)
            db_result = (DataAccessFacade.get_instance()).write_user(username=nickname,
                                                                     password=new_suscriber.get_password())
            return db_result
        return result

    @logger
    def login_subscriber(self, nickname: str, password: str) -> {'response': bool, 'msg': str}:
        """
        :param nickname:
        :param password:
        :return: dict = {'response': bool, 'msg': str}
        """
        self.__curr_user = self.get_subscriber(nickname)
        if self.__curr_user is None or not self.__curr_user.is_registered():
            return {'response': False, 'msg': "Subscriber " + nickname + " is not registered."}
        if self.__curr_user.is_logged_out():
            # domain_result = self.__curr_user.login(nickname, password)
            # if domain_result['response']:
            #     new_subscribers = (DataAccessFacade.get_instance()).read_statistics(['subscribers'], date=self.__today)[
            #                           'response'][0]['subscribers'] + 1
            #     db_result = (DataAccessFacade.get_instance()).update_statistics(old_date=self.__today,
            #                                                                     new_subscribers=new_subscribers)
            #     if not db_result['response']:
            #         return db_result
            #     if self.__curr_user in self.__managers:
            #         new_system_managers = (DataAccessFacade.get_instance()).read_statistics(['system_managers'],
            #                                                                                 date=self.__today)[
            #                                   'response'][0]['system_managers'] + 1
            #         db_result = (DataAccessFacade.get_instance()).update_statistics(old_date=self.__today,
            #                                                                         new_system_managers=
            #                                                                         new_system_managers)
            #         if not db_result['response']:
            #             return db_result
            #     if len(self.get_managed_stores()) > 0:
            #         new_store_managers = (DataAccessFacade.get_instance()).read_statistics(['store_managers'],
            #                                                                                date=self.__today)[
            #                                  'response'][0]['store_managers'] + 1
            #         db_result = (DataAccessFacade.get_instance()).update_statistics(old_date=self.__today,
            #                                                                         new_store_managers=
            #                                                                         new_store_managers)
            #         if not db_result['response']:
            #             return db_result
            #
            #     if len(self.get_owned_stores()) > 0:
            #         new_store_owners = (DataAccessFacade.get_instance()).read_statistics(['store_owners'],
            #                                                                              date=self.__today)[
            #                                'response'][0]['store_owners'] + 1
            #         db_result = (DataAccessFacade.get_instance()).update_statistics(old_date=self.__today,
            #                                                                         new_store_owners=
            #                                                                         new_store_owners)
            #         if not db_result['response']:
            #             return db_result
            #
            #     return domain_result
            answer = self.__curr_user.login(nickname, password)
            if answer:
                # update statistics
                if self.get_user_type() == 'OWNER':
                    if not self.__statistics[0].inc_store_owners_counter():
                        self.reset_statistics('owner')
                if self.get_user_type() == 'SYSTEMMANAGER':
                    if not self.__statistics[0].inc_system_managers_counter():
                        self.reset_statistics('system_manager')
                if self.get_user_type() == 'SUBSCRIBER':
                    if not self.__statistics[0].inc_subscribers_counter():
                        self.reset_statistics('subscriber')
                if self.get_user_type() == 'MANAGER':
                    if not self.__statistics[0].inc_store_managers_counter():
                        self.reset_statistics('store_manager')
            return answer
        return {'response': False, 'msg': "Subscriber " + nickname + " already logged in"}

    @logger
    def subscribe(self, user: User):
        if self.validate_nickname(user.get_nickname()):
            self.__subscribers.append(user)
            return True
        return False

    @logger
    def unsubscribe(self, nickname):
        for s in self.__subscribers:
            if s.get_nickname() == nickname:
                self.__subscribers.remove(s)
                s.unregistered()
                db_result = (DataAccessFacade.get_instance()).delete_users(username=nickname)
                if not db_result['response']:
                    return db_result
                return True
        return False
        #         return {'response': True, 'msg': "User " + nickname + " was unsubscribe successfully"}
        # return {'response': False, 'msg': "User " + nickname + " is not a subscriber"}

    @logger
    def open_store(self, store_name) -> {'response': bool, 'msg': str}:
        if self.__curr_user.is_registered() and self.__curr_user.is_logged_in() and not store_name.strip() == "":
            for store in self.__stores:
                if store.get_name() == store_name:
                    return {'response': False, 'msg': "Error! Store name " + store_name + " already exist"}

            store = Store(store_name)
            store.get_owners_appointments().append(StoreAppointment(None, self.__curr_user, []))
            self.__stores.append(store)
            # db_result = (DataAccessFacade.get_instance()).write_store(store_name,
            #                                                           self.get_curr_user().get_nickname())
            # if not db_result['response']:
            #     return db_result
            # new_store_owners = (DataAccessFacade.get_instance()).read_statistics(['store_owners'],
            #                                                                      date=self.__today)[
            #                        'response'][0]['store_owners'] + 1
            # db_result = (DataAccessFacade.get_instance()).update_statistics(old_date=self.__today,
            #                                                                 new_store_owners=
            #                                                                 new_store_owners)
            # if not db_result['response']:
            #     return db_result
            self.__statistics[0].inc_store_owners_counter()
            return {'response': True, 'msg': "Store " + store_name + " opened successfully"}
        return {'response': False, 'msg': "Error! user doesn't have permission to open a store"}

    @logger
    def close_store(self, store_name) -> bool:
        if self.__curr_user.is_registered() and self.__curr_user.is_logged_in() and not store_name.strip() == "":
            store: Store = self.get_store(store_name)
            if store is None:
                return False

            if self.__curr_user not in store.get_owners():
                return False

            self.__stores.remove(store)
            # TODO
            db_result = (DataAccessFacade.get_instance()).delete_stores(store_name=store_name)
            if not db_result['response']:
                return db_result
            return True
        return False

    @logger
    def validate_nickname(self, nickname: str) -> bool:
        if nickname.strip() == "":
            return False
        for u in self.__subscribers:
            if u.get_nickname() == nickname:
                return False
        return True

    @logger
    def get_subscriber(self, nickname: str) -> User:
        for u in self.__subscribers:
            if u.get_nickname() == nickname:
                return u
        return None

    @logger
    def get_products_by(self, search_opt: int, string: str) -> {'response': list, 'msg': str}:
        list_of_products = []
        s: Store
        for s in self.__stores:
            products = s.get_products_by(search_opt, string)
            list(map(lambda product: list_of_products.append({"store_name": s.get_name(),
                                                              "product_name": product.get_name(),
                                                              "price": product.get_price(),
                                                              "category": product.get_category(),
                                                              "amount": s.get_inventory().get_amount(
                                                                  product.get_name())}), products))
        if len(list_of_products) == 0:
            return {'response': list_of_products, 'msg': "Error! There are no results"}
        return {'response': list_of_products, 'msg': "Products was retrieved successfully"}

    @logger
    def filter_products_by(self,
                           products_ls: [{"store_name": str, "product_name": str, "price": float, "category": str,
                                          "amount": (int or None)}],
                           filter_by_option: int, min_price: (float or None) = None,
                           max_price: (float or None) = None, category: (str or None) = None) -> {'response': list,
                                                                                                  'msg': str}:
        """
        This function have two options:
            Either filter_by_option == 1, and then the function should get min price and max price.
            Or filter_by_option == 2, and then the function should get category.

        The other parameters should be None, but this isn't a constraint. If they are not none, the program will ignore
                                                                                                                   them.

        Any other option should return an empty list(A.K.A Error).

        :param products_ls: list of product to filter. the user should get them by searching products.
                            Each element in the list should be a dictionary:
                                {"store_name": str, "product_name": str, "price": float, "category": str}
                                :key store_name: the name( A.K.A Unique id) of the store that sells the product.
                                :key product_name: the name( A.K.A Unique id) of the product.
                                :key price: the price of the product with the id @product_name
                                                        in the store with the id @ store_name.
                                :key category: the category of the product with the id @product_name
                                                        in the store with the id @ store_name.

        :param filter_by_option: which filter to apply. either 1: by price or
                                                               2: by category
        :param min_price: only used with option 1. this is the minimum price to filter by.
        :param max_price: only used with option 1. this is the maximum price to filter by.
        :param category: only used with option 2. this is the category to filter by.
        :return: a list of the filtered product.
                 an empty list if an error occurs.
        """
        if len(products_ls) == 0:
            return {'response': [], 'msg': "Error! There are no products to filter"}

        if filter_by_option == 1:
            if min_price is None or max_price is None:
                return {'response': [], 'msg': "Error! All field max/min price can't be empty"}

        else:
            if filter_by_option == 2:
                if category is None:
                    return {'response': [], 'msg': "Error! All field category can't be empty"}
            else:
                return {'response': [], 'msg': "Error! No filter option was selected"}

        # filter by Price Range
        if filter_by_option == 1:
            try:
                ls = []
                for p in products_ls:
                    if p['price'] >= min_price and p['price'] <= max_price:
                        ls.append(p)
                # ls = list(filter(lambda product_dictionary: min_price <= product_dictionary['price'] and product_dictionary['price'] <= max_price,
                #                  products_ls))
                return {'response': ls, 'msg': "Action Filter by price range was successful"}
            except Exception:
                return {'response': [], 'msg': "Error in filter action"}
        # filter by Category
        else:
            try:
                ls = list(filter(lambda product_dictionary: category == product_dictionary['category'],
                                 products_ls))
                return {'response': ls, 'msg': "Action Filter by category was successful"}

            except Exception:
                return {'response': [], 'msg': "Error in filter action"}

            # 'response':
            # '{"py/object": "src.main.DomainLayer.StoreComponent.Store.Store",
            # "_Store__name": "s",
            # "_Store__owners":
            #   [{"_User__registrationState": {
            #       "_Registration__username": "s",
            #    "_Store__StoreManagerAppointments": [],
            # 'msg': 'Store info was retrieved successfully'}

    # @logger
    def get_store_info(self, store_name) -> dict:
        """
        :param store_name:
        :return: dict = {'response': store json object, 'msg': str}
        """
        store = self.get_store(store_name)
        if store is None:
            return {'response': None, 'msg': "Store" + store_name + " doesn't exist"}

        owners = []
        list(map(lambda curr: owners.append(curr.get_nickname()), store.get_owners()))
        managers = []
        list(map(lambda curr: managers.append(curr.get_nickname()), store.get_managers()))

        return {'response': {"name": store_name, "owners": owners, "managers": managers},
                'msg': "Store info was retrieved successfully"}

    @logger
    def get_store_inventory(self, store_name):
        store = self.get_store(store_name)
        if store is None:
            return {'response': None, 'msg': "Store" + store_name + " doesn't exist"}

        if store.get_inventory().is_empty():
            return {'response': None, 'msg': "Store inventory is empty"}

        inventory = store.get_inventory().get_inventory()

        res = []
        list(map(lambda curr: res.append({"name": curr["product"].get_name(), "price": curr["product"].get_price(),
                                          "category": curr["product"].get_category(), "amount": curr["amount"],
                                          "discount_type": curr["product"].get_discount_type().name,
                                          "purchase_type": curr["product"].get_purchase_type().name}), inventory))

        return {'response': res, 'msg': "Store inventory was retrieved successfully"}

    @logger
    def save_products_to_basket(self, products_stores_quantity_ls: [{"store_name": str, "product_name": str,
                                                                     "amount": int}]) -> {
        'response': bool, 'msg': str}:
        for element in products_stores_quantity_ls:
            if element is None:
                return {'response': False, 'msg': "Error! Invalid input"}
        stores_names = [product_as_dictionary['store_name'] for product_as_dictionary in products_stores_quantity_ls]
        for store_name in stores_names:
            if self.get_store(store_name) is None:
                return {'response': False, 'msg': "Error! Store " + store_name + "doesn't exist"}

        ls = list(map(lambda x: {"store_name": x["store_name"],
                                 "product": self.get_store(x["store_name"]).get_product(x["product_name"]),
                                 "amount": x["amount"]},
                      products_stores_quantity_ls))
        domain_result = self.__curr_user.save_products_to_basket(ls)
        if domain_result['response']:
            for product_dict in products_stores_quantity_ls:
                db_result = (DataAccessFacade.get_instance()).write_products_in_basket(
                    username=self.__curr_user.get_nickname(),
                    store_name=product_dict['store_name'],
                    product_name=product_dict['product_name'],
                    amount=product_dict['amount'])
                if not db_result['response']:
                    return db_result
        return domain_result

    @logger
    def view_shopping_cart(self) -> {'response': list, 'msg': str}:
        """
        :return: dict: {'response': [{"store_name": str,
                                     "basket": [{"product_name": str
                                                 "amount": int}, ...]
                                    }, ...],
                        'msg': str}
        """
        return self.__curr_user.view_shopping_cart()

    @logger
    def remove_from_shopping_cart(self, products_details: [{"product_name": str, "store_name": str}]) -> {
        'response': bool, 'msg': str}:
        """
        :param products_details: [{"product_name": str,
                                       "store_name": str}, ...]
        :return: dict = {'response': bool, 'msg': str}
                 True on success, False when one of the products doesn't exist in the shopping cart
        """
        domain_result = self.__curr_user.remove_from_shopping_cart(products_details)
        if domain_result['response']:
            for product_dict in products_details:
                db_result = (DataAccessFacade.get_instance()).delete_products_in_baskets(
                    username=self.__curr_user.get_nickname(),
                    store_name=product_dict['store_name'],
                    product_name=product_dict['product_name'])
                if not db_result['response']:
                    return db_result
        return domain_result

    @logger
    def update_quantity_in_shopping_cart(self,
                                         products_details: [{"product_name": str, "store_name": str, "amount": int}]) \
            -> {'response': bool, 'msg': str}:
        """
        :param products_details: [{"product_name": str,
                                       "store_name": str,
                                       "amount": int}, ...]
        :return: dict = {'response': bool, 'msg': str}
                 True on success, False when one of the products doesn't exist in the shopping cart
        """
        domain_result = self.__curr_user.update_quantity_in_shopping_cart(products_details)
        if domain_result['response']:
            for product_dict in products_details:
                db_result = (DataAccessFacade.get_instance()).update_products_in_baskets(
                    old_username=self.__curr_user.get_nickname(),
                    old_store_name=product_dict['store_name'],
                    old_product_name=product_dict['product_name'],
                    new_amount=product_dict['amount'])
                if not db_result['response']:
                    return db_result
        return domain_result

    # @logger
    def get_store(self, store_name) -> Store:
        for s in self.__stores:
            if s.get_name() == store_name:
                return s
        return None

    @logger
    def get_stores_names(self) -> {'response': list, 'msg': str}:
        stores = []
        list(map(lambda store: stores.append(store.get_name()), self.__stores))
        if len(stores) == 0:
            return {'response': [], 'msg': "There are no stores"}
        return {'response': stores, 'msg': "Stores were retrieved successfully"}

    # u.c 2.8
    @logger
    def purchase_products(self) -> {'response': dict, 'msg': str}:
        """
            purchase all products in shopping cart according to the policies
        :return: dict = {'response': dict, 'msg': str}
                response = None if no purchase can be made, else dict
                {"total_price": float, "baskets":
                        [{"store_name": str, "basket_price": float, "products":
                                    [{"product_name", "product_price", "amount"}]
                        }]
                }
        """
        # baskets = [{"store_name": str, "basket": ShoppingBasket}]
        baskets = self.__curr_user.get_shopping_cart().get_shopping_baskets()
        total_price = 0
        purchase_baskets = []
        # basket = ShoppingBasket
        for basket in baskets:
            # ls = {"total_price": float, "baskets":
            #                 [{"store_name": str, "basket_price": float, "products":
            #                             [{"product_name", "product_price", "amount"}]
            #                 }]
            #         }
            purchase_ls = self.purchase_basket(basket["store_name"])
            if purchase_ls["response"] is not None:
                purchase_res = purchase_ls["response"]
                purchase_baskets += purchase_res["purchases"]
                total_price += purchase_res["total_price"]
        if len(purchase_baskets) == 0:
            return []
        return {"total_price": total_price, "purchases": purchase_baskets}

    @logger
    def purchase_basket(self, store_name: str) -> {'response': dict, 'msg': str}:
        """
            purchase single basket from user cart by given store name, according to the policies
        :param store_name: store name
        :return: None if basket doesn't exist or some policy prevents purchase, else purchase dict
                {"total_price": float, "baskets":
                        [{"store_name": str, "basket_price": float, "products":
                                    [{"product_name", "product_price", "amount"}]
                        }]
                }
        """
        basket = self.__curr_user.get_shopping_cart().get_store_basket(store_name)
        if basket is None:
            return {'response': None, 'msg': "Store basket doesn't exist"}

        purchase = self.get_store(store_name).purchase_basket(basket)
        if purchase["response"] is None:
            return {'response': None, 'msg': purchase["msg"]}

        # {"store_name": self.__name, "basket_price": basket_price, "products": products_purchases}
        return {'response': {"total_price": purchase["response"]["basket_price"], "purchases": [purchase["response"]]},
                'msg': "Great Success! Purchase products successful"}

    @logger
    def accept_purchases(self, purchase_ls: dict):
        """
            after payment confirmation, add purchases to user and store history
        :param purchase_ls: dict
                {"total_price": float, "baskets":
                        [{"store_name": str, "basket_price": float, "products":
                                    [{"product_name", "product_price", "amount"}]
                        }]
                }
        :return: void
        """
        if purchase_ls is None or len(purchase_ls) == 0:
            return {'response': False, 'msg': "Empty purchase list provided"}

        nickname = self.__curr_user.get_nickname()
        now = datetime(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour,
                       datetime.now().minute)
        # purchase ->
        # [{"store_name": str, "basket_price": float, "products": [{"product_name", "product_price", "amount"}]}]
        for purchase in purchase_ls["purchases"]:
            new_purchase = Purchase(purchase["products"], purchase["basket_price"], purchase["store_name"], nickname)
            # add products to users' purchase history and remove them from the cart
            self.__curr_user.complete_purchase(new_purchase)
            # update store inventory and add purchases to purchase history
            self.get_store(purchase["store_name"]).complete_purchase(new_purchase)
            product_lst_for_db = [{'product_name': purchas['product_name'],
                                   'product_price': purchas['product_price'],
                                   'amount': purchas['amount']} for purchas in purchase["products"]]
            db_result = (DataAccessFacade.get_instance()).write_purchase(username=nickname,
                                                                         store_name=purchase["store_name"],
                                                                         total_price=purchase["basket_price"],
                                                                         date=now,
                                                                         products_lst=product_lst_for_db)
            print(db_result)
        return {'response': True, 'msg': "Great Success! Purchase complete"}

    @logger
    def remove_purchase(self, store_name: str, purchase_date: datetime):
        self.get_store(store_name).remove_purchase(self.__curr_user.get_nickname(), purchase_date)
        self.__curr_user.remove_purchase(store_name, purchase_date)

    # ---------------------------------------------------

    # --------------   subscriber functions   --------------
    @logger
    def logout_subscriber(self) -> {'response': bool, 'msg': str}:
        if not self.__curr_user.is_registered():
            return {'response': False, 'msg': "Subscriber isn't registered"}
        if not self.__curr_user.is_logged_in():
            return {'response': False, 'msg': "Subscriber isn't logged in"}

        self.__curr_user.logout()
        self.__curr_user = User()
        return {'response': True, 'msg': "Subscriber was logged out successfully"}

    @logger
    def view_personal_purchase_history(self) -> {'response': list, 'msg': str}:
        if self.__curr_user.is_registered() and self.__curr_user.is_logged_in():
            purchases = self.__curr_user.get_purchase_history()
            ls = []
            list(map(lambda purchase: ls.append({"store_name": purchase.get_store_name(),
                                                 "nickname": purchase.get_nickname(),
                                                 "date": purchase.get_date().strftime("%d/%m/%Y, %H:%M:%S"),
                                                 "total_price": purchase.get_total_price(),
                                                 "products": purchase.get_products()}), purchases))
            if len(ls) == 0:
                return {'response': [], 'msg': "There are no previous purchases"}
            return {'response': ls, 'msg': "Purchase history was retrieved successfully"}
        return {'response': None, 'msg': "User has no permissions to view personal purchase history"}

    # ----------------------------------

    # ---- system manager functions ----
    @logger
    def view_user_purchase_history(self, nickname: str):
        if self.is_manager(self.__curr_user.get_nickname()):
            viewed_user = self.get_subscriber(nickname)
            if viewed_user:
                purchases = viewed_user.get_purchase_history()
                ls = []
                list(map(lambda purchase: ls.append({"store_name": purchase.get_store_name(),
                                                     "nickname": purchase.get_nickname(),
                                                     "date": purchase.get_date().strftime("%d/%m/%Y, %H:%M:%S"),
                                                     "total_price": purchase.get_total_price(),
                                                     "products": purchase.get_products()}), purchases))
                # ls = []
                # list(map(lambda purchase: ls.append(jsonpickle.encode(purchase)), viewed_user.get_purchase_history()))
                if len(ls) == 0:
                    return {'response': [], 'msg': "There are no previous purchases for user " + nickname}
                return {'response': ls, 'msg': nickname + " purchases history was retrieved successfully"}
            else:
                return {'response': None, 'msg': "Error, Subscriber " + nickname + " doesn't exist by that name."}
        else:
            return {'response': None, 'msg': "User is not a system manager"}

    @logger
    def view_store_purchases_history(self, store_name):
        if self.is_manager(self.__curr_user.get_nickname()):
            viewed_store = self.get_store(store_name)
            if viewed_store:
                owner_nickname = viewed_store.get_owners()[0].get_nickname()
                purchases = viewed_store.get_purchases(owner_nickname)
                ls = []
                list(map(lambda purchase: ls.append({"store_name": purchase.get_store_name(),
                                                     "nickname": purchase.get_nickname(),
                                                     "date": purchase.get_date().strftime("%d/%m/%Y, %H:%M:%S"),
                                                     "total_price": purchase.get_total_price(),
                                                     "products": purchase.get_products()}), purchases))
                # ls = []
                # list(map(lambda curr_product: ls.append(jsonpickle.encode(curr_product)),
                #          viewed_store.get_purchases(self.__curr_user.get_nickname())))
                if len(ls) == 0:
                    return {'response': [], 'msg': "There are no previous purchases for store " + store_name}
                return {'response': ls, 'msg': store_name + " purchases history was retrieved successfully"}
            else:
                return {'response': None, 'msg': "Error, Store " + store_name + " doesn't exist."}
        else:
            return {'response': None, 'msg': "User is not a system manager"}

    @logger
    def is_manager(self, nickname):
        for m in self.__managers:
            if m.get_nickname() == nickname:
                return True
        return False

    # ----------------------------------

    # @logger
    def add_products(self, store_name: str,
                     products_details: [{"name": str, "price": int, "category": str, "amount": int,
                                         "purchase_type": int}]) -> {'response': bool, 'msg': str}:
        """
        :param store_name: store's name
        :param products_details: list of JSONs, each JSON is one details record, for one product
        :return: dict = {'response': bool, 'msg': str}
                response = True if products were added, False otherwise
        """
        store: Store = self.get_store(store_name)
        if (store and
                (store.is_owner(self.__curr_user.get_nickname()) or
                 store.is_manager(self.__curr_user.get_nickname())) and
                self.__curr_user.is_registered() and
                self.__curr_user.is_logged_in()):
            domain_result = store.add_products(self.__curr_user.get_nickname(), products_details)
            if domain_result['response']:
                for product_as_dict in products_details:
                    amount = self.get_store(store_name).get_inventory().get_amount(product_as_dict['name'])
                    db_write_result = (DataAccessFacade.get_instance()).write_product(
                        product_name=product_as_dict['name'],
                        store_name=store_name,
                        price=product_as_dict['price'],
                        category=product_as_dict['category'],
                        amount=product_as_dict['amount'],
                        purchase_type=
                        product_as_dict['purchase_type'])
                    if not db_write_result['response']:
                        db_update_result = (DataAccessFacade.get_instance()).update_products(
                            old_product_name=product_as_dict['name'], old_store_name=store_name,
                            new_amount=amount)
                        if not db_update_result['response']:
                            return db_update_result
                return domain_result
        return {'response': False, 'msg': "User has no permissions to add products to the store"}

    @logger
    def remove_products(self, store_name: str, products_names: list) -> bool:
        """
        :param store_name: store's name
        :param products_names: list of product's names (str) to remove
        :return: True if all products were removed, False otherwise
        """
        store: Store = self.get_store(store_name)
        for product_name in products_names:
            if store is not None and not store.get_product(product_name):
                return False

        if (store is not None and
                self.__curr_user.is_registered() and
                self.__curr_user.is_logged_in() and
                (store.is_owner(self.__curr_user.get_nickname()) or
                 store.is_manager(self.__curr_user.get_nickname()))):
            domain_result = store.remove_products(self.__curr_user.get_nickname(), products_names)
            if domain_result:
                for product_name in products_names:
                    db_result = (DataAccessFacade.get_instance()).delete_products(product_name=product_name,
                                                                                  store_name=store_name)
                    if not db_result['response']:
                        return db_result['response']
                return domain_result
        return False

    @logger
    def edit_product(self, store_name: str, product_name: str, op: str, new_value) -> {'response': bool, 'msg': str}:
        """
        :param store_name: store's name
        :param product_name: product's name to edit
        :param op: edit options - name, price, amount
        :param new_value: new value to set to
        :return: dict =  {'response': bool, 'msg': str}
        """
        store: Store = self.get_store(store_name)
        if (store is not None and
                self.__curr_user.is_registered() and
                self.__curr_user.is_logged_in()):
            # (store.is_owner(self.__curr_user.get_nickname()) or
            #  store.is_manager(self.__curr_user.get_nickname())) and \
            # store.product_in_inventory(product_name):

            # Check if the new name is already exist in the sore. if does, return false.
            if op.lower() == "name":
                if (store.get_name(), new_value) in [(e['store_name'], e['product_name']) for e in
                                                     (self.get_products_by(1, new_value))['response']]:
                    return {'response': False, 'msg': "check this condition"}
            result = store.edit_product(self.__curr_user.get_nickname(), product_name, op, new_value)
            if result:
                if op.lower() == "name":
                    db_result = (DataAccessFacade.get_instance()).update_products(old_store_name=store_name,
                                                                                  old_product_name=product_name,
                                                                                  new_product_name=new_value)
                    if not db_result['response']:
                        return db_result
                elif op.lower() == "price":
                    db_result = (DataAccessFacade.get_instance()).update_products(old_store_name=store_name,
                                                                                  old_product_name=product_name,
                                                                                  new_price=new_value)
                    if not db_result['response']:
                        return db_result
                elif op.lower() == "amount":
                    db_result = (DataAccessFacade.get_instance()).update_products(old_store_name=store_name,
                                                                                  old_product_name=product_name,
                                                                                  new_amount=new_value)
                    if not db_result['response']:
                        return db_result
                return {'response': True, 'msg': "Product was edited successfully"}
            return {'response': False, 'msg': "Edit product failed."}
        return {'response': False, 'msg': "Edit product failed."}

    def get_product_details(self, store_name, product_name):
        store = self.get_store(store_name)
        product = store.get_product(product_name)
        return {"name": product.get_name(), "price": product.get_price(), "category": product.get_category(),
                "amount": store.get_inventory().get_amount(product_name),
                "purchase_type": product.get_purchase_type().name}

    @logger
    def remove_owner(self, appointee_nickname: str, store_name: str) -> {'response': [], 'msg': str}:
        """
        the function removes appointee_nickname as owner from the store, in addition to him it removes all the managers
        and owners appointee_nickname appointed.
        :param appointee_nickname: nickname of the owner we want to remove as owner
        :param store_name: store the owner will be removed from as owner
        :return: dict =  {'response': [], 'msg': str}
                 response = nicknames list of all the removed appointees -> the appointee_nickname of the owner we want
                            to remove and all the appointees he appointed, we had to remove as well.
        """
        store = self.get_store(store_name)
        appointee = self.get_subscriber(appointee_nickname)
        if appointee is not None and \
                store is not None and \
                self.__curr_user.is_registered() and \
                self.__curr_user.is_logged_in() and \
                store.is_owner(self.__curr_user.get_nickname()) and \
                appointee.is_registered() and \
                store.is_owner(appointee_nickname):
            domain_result = store.remove_owner(self.__curr_user.get_nickname(), appointee_nickname)
            if len(domain_result['response']) > 0:
                db_result = (DataAccessFacade.get_instance()).delete_store_owner_appointments(
                    appointee_username=appointee_nickname,
                    store_name=store_name,
                    appointer_username=self.__curr_user.get_nickname())
                if not db_result['response']:
                    return ret([], db_result['msg'])
                return domain_result
        return {'response': [], 'msg': "Error! remove store owner failed."}

    @logger
    def appoint_additional_owner(self, appointee_nickname: str, store_name: str) -> {'response': bool, 'msg': str}:
        """
        :param appointee_nickname: nickname of the new owner that will be appointed
        :param store_name: store the owner will be added to
        :return: dict =  {'response': bool, 'msg': str}
                 response = True on success, else False
        """
        appointee = self.get_subscriber(appointee_nickname)
        store = self.get_store(store_name)

        if store is None:
            return {'response': False, 'msg': "Store " + store_name + " doesn't exist"}
        if appointee is None:
            return {'response': False, 'msg': "Appointee " + appointee_nickname + " is not a subscriber"}
        if store.is_owner(appointee_nickname):
            return {'response': False, 'msg': "appointee " + appointee_nickname + " is already a store owner"}
        if self.__curr_user.is_registered() and \
                appointee.is_registered() and \
                self.__curr_user.is_logged_in() and \
                (store.is_owner(self.__curr_user.get_nickname()) or store.is_manager(self.__curr_user.get_nickname())):
            result = store.add_owner(self.__curr_user.get_nickname(), appointee)
            return result
            # if result:
            #     return {'response': True, 'msg': appointee_nickname + " was added successfully as a store owner"}
            # return {'response': False, 'msg': "User has no permissions"}
        return {'response': False, 'msg': "User has no permissions"}

    # @logger
    def update_agreement_participants(self, appointee_nickname: str, store_name: str,
                                      owner_response: AppointmentStatus):
        """
        :param appointee_nickname: nickname of the new owner that will be appointed
        :param store_name: store the owner will be added to
        :param owner_response: the owners response - declined/approved
        :return: dict =  {'response': bool, 'msg': str}
                 response = True on success, else False
        """
        store = self.get_store(store_name)
        result = store.update_agreement_participants(appointee_nickname, self.__curr_user.get_nickname(),
                                                     owner_response)
        if result:
            return {'response': True,
                    'msg': "Approved the appointment of " + appointee_nickname + " as a new store owner"}
        return {'response': False, 'msg': "Declined the appointment of " + appointee_nickname + " as a new store owner"}

    @logger
    def get_appointment_status(self, appointee_nickname: str, store_name: str) -> AppointmentStatus:
        """
        :param appointee_nickname: the nickname of the user being appointed as new store owner
        :param store_name: store the owner should be added to
        :return: AppointmentStatus - DECLINED = 1,APPROVED = 2, PENDING = 3
        """
        store = self.get_store(store_name)
        return store.get_appointment_status(appointee_nickname)

    @logger
    # TODO: eden check permissions with gui!!!!!
    def appoint_store_manager(self, appointee_nickname: str, store_name: str, permissions: [int or enumerate]) -> \
            {'response': bool, 'msg': str}:
        """
        :param appointee_nickname: nickname of the new manager that will be appointed
        :param store_name: store's name
        :param permissions: ManagerPermission[] -> list of permissions (list of ints)
        :return: dict = {'response': bool, 'msg': str}
                 response = True on success, else False
        """
        appointee = self.get_subscriber(appointee_nickname)
        store = self.get_store(store_name)
        try:
            permissions_as_enums = [ManagerPermission(per) for per in permissions]
        except Exception:
            permissions_as_enums = permissions

        if appointee is None:
            return {'response': False, 'msg': "Appointee " + appointee_nickname + " is not a subscriber"}
        if store is None:
            return {'response': False, 'msg': "Store " + store_name + " doesn't exist"}
        if store.is_owner(appointee_nickname):
            return {'response': False, 'msg': "appointee " + appointee_nickname + " is already a store owner"}
        if store.is_manager(appointee_nickname):
            return {'response': False, 'msg': "appointee " + appointee_nickname + " is already a store manager"}

        if self.__curr_user.is_registered() and appointee.is_registered() and \
                self.__curr_user.is_logged_in() and \
                (store.is_owner(self.__curr_user.get_nickname()) or store.is_manager(
                    self.__curr_user.get_nickname())):
            result = store.add_manager(self.__curr_user, appointee, permissions_as_enums)
            if result:
                db_result = (DataAccessFacade.get_instance()).write_store_manager_appointment(appointee_username=
                                                                                              appointee_nickname,
                                                                                              store_name=store_name,
                                                                                              appointer_username=
                                                                                              self.__curr_user.
                                                                                              get_nickname(),
                                                                                              permissions_lst=
                                                                                              [perm.name
                                                                                               for perm
                                                                                               in permissions_as_enums])
                if not db_result['response']:
                    return db_result
                return {'response': True, 'msg': appointee_nickname + " was added successfully as a store manager"}
            return {'response': False, 'msg': "User has no permissions"}
        return {'response': False, 'msg': "User has no permissions"}

    def get_manager_permissions(self, store_name) -> list:
        """
        :param store_name:
        :return: returns the permissions of the current user
        """
        store: Store = self.get_store(store_name)
        if store is not None and \
                self.__curr_user.is_registered() and \
                self.__curr_user.is_logged_in() and \
                store.is_manager(self.__curr_user.get_nickname()):
            return store.get_permissions(self.__curr_user.get_nickname())
        return False

    @logger
    # TODO: If permissions type is [int], convert to [ManagerPermissions]
    def edit_manager_permissions(self, store_name: str, appointee_nickname: str, permissions: list) -> bool:
        """
        :param store_name: store's name
        :param appointee_nickname: manager's nickname who's permissions will be edited
        :param permissions: ManagerPermission[] ->list of permissions (list of Enum)
        :return: dict = {'response': bool, 'msg': str}
                 response = True on success, else False
        """
        appointee = self.get_subscriber(appointee_nickname)
        store = self.get_store(store_name)
        if (appointee is not None and
                store is not None and
                self.__curr_user.is_registered() and
                appointee.is_registered() and
                self.__curr_user.is_logged_in() and
                (store.is_owner(self.__curr_user.get_nickname()) or store.is_manager(
                    self.__curr_user.get_nickname())) and
                store.is_manager(appointee_nickname)):
            domain_result = store.edit_manager_permissions(self.__curr_user, appointee_nickname, permissions)
            if domain_result:
                db_result = (DataAccessFacade.get_instance()).update_store_manager_appointments(old_appointee_username=
                                                                                                appointee_nickname,
                                                                                                old_store_name=
                                                                                                store_name,
                                                                                                new_permissions_lst=[
                                                                                                    perm.name for perm
                                                                                                    in permissions])
                if not db_result['response']:
                    return db_result['response']
                return True
        return False

    @logger
    def get_appointees(self, store_name: str, managers_or_owners: str) -> list:
        """
        returns for the current manager/owner all the managers he appointed
        :param appointer_nickname:
        :param managers_or_owners: "MANAGERS" or "OWNERS" to get a list of the managers or owners that appointer_nickname appointed
        :return: returns a list of nicknames, of all the managers appointer_nickname appointed
        """
        store: Store = self.get_store(store_name)
        if store is not None and \
                self.__curr_user.is_registered() and \
                self.__curr_user.is_logged_in() and \
                (store.is_owner(self.__curr_user.get_nickname()) or store.is_manager(
                    self.__curr_user.get_nickname())):
            return store.get_appointees(self.__curr_user.get_nickname(), managers_or_owners)
        return []

    @logger
    def remove_manager(self, store_name: str, appointee_nickname: str) -> bool:
        """
        :param store_name: store's name
        :param appointee_nickname: manager's nickname who's will be removed
        :return: True if removed successfully, else False
        """
        store = self.get_store(store_name)
        appointee = self.get_subscriber(appointee_nickname)
        if (appointee is not None and
                store is not None and
                self.__curr_user.is_registered() and
                appointee.is_registered() and
                self.__curr_user.is_logged_in() and
                (store.is_owner(self.__curr_user.get_nickname()) or store.is_manager(
                    self.__curr_user.get_nickname())) and
                store.is_manager(appointee_nickname)):
            domain_result = store.remove_manager(self.__curr_user.get_nickname(), appointee_nickname)
            if domain_result:
                db_result = (DataAccessFacade.get_instance()).delete_store_manager_appointments(appointer_username=
                                                                                                appointee_nickname,
                                                                                                store_name=store_name)
                if not db_result['response']:
                    return db_result['response']
                return True
        return False

    @logger
    def display_store_purchases(self, store_name: str) -> {'response': list, 'msg': str}:
        """
        :param store_name: store's name
        :return: dict = {'response': list, 'msg': str}
                 response = purchases list
        """
        store = self.get_store(store_name)
        if store is not None and \
                self.__curr_user.is_registered() and \
                self.__curr_user.is_logged_in() and \
                (store.is_owner(self.__curr_user.get_nickname()) or store.is_manager(self.__curr_user.get_nickname())):
            # if not store.get_purchases(self.__curr_user.get_nickname()):
            #     return {'response': [], 'msg': "There are no previous purchases"}
            lst = []
            purchases = store.get_purchases(self.__curr_user.get_nickname())
            list(map(lambda purchase: lst.append({"store_name": purchase.get_store_name(),
                                                  "nickname": purchase.get_nickname(),
                                                  "date": purchase.get_date().strftime("%d/%m/%Y, %H:%M:%S"),
                                                  "total_price": purchase.get_total_price(),
                                                  "products": purchase.get_products()}), purchases))
            # list(map(lambda curr_product: lst.append(jsonpickle.encode(curr_product)),
            #          ))
            if len(lst) == 0:
                return {'response': [], 'msg': "There are no previous purchases"}
            return {'response': lst, 'msg': "Purchase history was retrieved successfully"}
        return {'response': [], 'msg': "User has no permissions to view store purchase history"}

    # ------------------- 4.2 --------------------
    @logger
    def get_policies(self, policy_type: str, store_name: str) -> [dict] or None:
        """
                according to the given type, displays a list of policies for the store
        :param policy_type: can be "purchase" or "discount"
        :param store_name:
        :return: list of policies or empty list, returns None if user is not owner of the store or if invalid flag
        """
        store = self.get_store(store_name)
        if store is None or not store.is_owner(self.__curr_user.get_nickname()):
            return {'response': None, 'msg': "Store doesn't exist, or user un-authorized for this action"}

        if policy_type == "purchase":
            return {'response': store.get_purchase_policies(), 'msg': "Great Success! Purchase policies retrieved"}
        elif policy_type == "discount":
            return {'response': store.get_discount_policies_as_dictionary_lst(), 'msg':
                "Great Success! Purchase policies retrieved"}
        return {'response': None, 'msg': "Not a valid choice of purchase type"}

    @logger
    def define_store_purchase_operator(self, store_name: str, operator: str):
        """
            set operator for store purchase policies
        :param store_name:
        :param operator: and/or/xor
        :return: none
        """
        store: Store = self.get_store(store_name)
        store.set_purchase_operator(operator)

    @logger
    def get_store_purchase_operator(self, store_name: str):
        """
            returns purchase policies operator of the store
        :param store_name:
        :return: and/or/xor
        """
        store: Store = self.get_store(store_name)
        return store.get_purchase_operator()

    @logger
    # TODO: eden check type of dates: [dict] / [datetime]
    def define_purchase_policy(self, store_name: str,
                               details: {"name": str, "products": [str], "min_amount": int or None,
                                         "max_amount": int or None, "dates": [datetime] or None,
                                         "bundle": bool or None}) \
            -> {'response': bool, 'msg': str}:
        """
            define requires valid and unique policy name, none empty list of products and at least one more detail
        :param store_name:
        :param details: {"name": str,                             -> policy name
                        "products": [str],                       -> list of product names
                        "min_amount": int or None,               -> minimum amount of products required
                        "max_amount": int or None,               -> maximum amount of products required
                        "dates": [dict] or None,                 -> list of prohibited dated for the given products
                        "bundle": bool or None}                  -> true if the products are bundled together
           i.e. details can be: {"products", "bundle"} / {"products", "min_amount"} etc.
        :return: true if successful, otherwise false with details for failure
        """
        store = self.get_store(store_name)
        if store is None:
            return {'response': False, 'msg': "Store doesn't exist"}

        if details.get("products") is None \
                or details.get("name") is None \
                or not self.at_least_one(details, False):
            return {'response': False, 'msg': "Error! Policy name, product(s) and at least one rule must be added"}

        if store.purchase_policy_exists(details):
            return {'response': False,
                    'msg': "Error! A policy by the given name already exist, or a policy with the same details exists."}

        if not store.is_owner(self.__curr_user.get_nickname()):
            return {'response': False, 'msg': "Oopsie poopsie...User un-authorized for this action"}
        return store.define_purchase_policy(details)

    @logger
    def update_purchase_policy(self, store_name: str, details: {"name": str, "products": [str],
                                                                "min_amount": int or None, "max_amount": int or None,
                                                                "dates": [dict] or None, "bundle": bool or None}) \
            -> {'response': bool, 'msg': str}:
        """
            update must have valid policy name of an existing policy and at least one more detail
        :param store_name:
        :param details: {"name": str,                            -> policy name
                        "products": [str] or None,               -> list of product names
                        "min_amount": int or None,               -> minimum amount of products required
                        "max_amount": int or None,               -> maximum amount of products required
                        "dates": [dict] or None,                 -> list of prohibited dated for the given products
                        "bundle": bool or None}                  -> true if the products are bundled together
           i.e. details can be: {"products", "bundle"} / {"products", "min_amount"} etc.
        :return: true if successful, otherwise false with details for failure
        """
        store = self.get_store(store_name)
        if store is None:
            return {'response': False, 'msg': "Store doesn't exist"}

        if details.get("name") is None \
                or not self.at_least_one(details, True):
            return {'response': False, 'msg': "Policy name and at least one rule must be added"}

        if not store.purchase_policy_exists(details):
            return {'response': False, 'msg': "Purchase policy doesn't exist"}

        if not store.is_owner(self.__curr_user.get_nickname()):
            return {'response': False, 'msg': "User un-authorized for this action"}
        return store.update_purchase_policy(details)

    @logger
    def define_discount_policy(self, store_name: str,
                               percentage: float,
                               valid_until: datetime,
                               discount_details: {'name': str,
                                                  'product': str},
                               discount_precondition: {'product': str,
                                                       'min_amount': int or None,
                                                       'min_basket_price': str or None} or None
                               ) \
            -> {'response': bool, 'msg': str}:
        store: Store = self.get_store(store_name)
        if store is None:
            return {'response': False, 'msg': "Store doesn't exist"}

        if (not store.is_owner(self.__curr_user.get_nickname()) and
                not store.is_manager(self.__curr_user.get_nickname()) and
                store.is_manager(self.__curr_user.get_nickname()) and store.has_permission(
                    self.__curr_user.get_nickname(),
                    ManagerPermission.EDIT_POLICIES)):
            return {'response': False, 'msg': "You don't have the permissions to change policy."}

        try:
            return store.define_discount_policy(percentage, valid_until, discount_details, discount_precondition)
        except Exception:
            return {'response': False, 'msg': "An unknown error has occurred. please try again."}

    @logger
    def update_discount_policy(self, store_name: str, policy_name: str,
                               percentage: float = -999,
                               valid_until: datetime = None,
                               discount_details: {'name': str,
                                                  'product': str} = None,
                               discount_precondition: {'product': str,
                                                       'min_amount': int or None,
                                                       'min_basket_price': str or None} or None = None
                               ) \
            -> {'response': bool, 'msg': str}:
        store: Store = self.get_store(store_name)
        if store is None:
            return {'response': False, 'msg': "Store doesn't exist"}

        if (not store.is_owner(self.__curr_user.get_nickname()) and
                not store.is_manager(self.__curr_user.get_nickname()) and
                store.is_manager(self.__curr_user.get_nickname()) and store.has_permission(
                    self.__curr_user.get_nickname(),
                    ManagerPermission.EDIT_POLICIES)):
            return {'response': False, 'msg': "You don't have the permissions to change policy."}

        try:
            return store.update_discount_policy(policy_name, percentage, valid_until, discount_details,
                                                discount_precondition)
        except Exception:
            return {'response': False, 'msg': "An unknown error has occurred. please try again."}

    @logger
    def define_composite_policy(self, store_name: str, policy1_name: str, policy2_name: str, flag: str,
                                percentage: float, name: str, valid_until: datetime):

        store: Store = self.get_store(store_name)
        if store is None:
            return {'response': False, 'msg': "Store doesn't exist"}

        if (not store.is_owner(self.__curr_user.get_nickname()) and
                not store.is_manager(self.__curr_user.get_nickname()) and
                store.is_manager(self.__curr_user.get_nickname()) and store.has_permission(
                    self.__curr_user.get_nickname(),
                    ManagerPermission.EDIT_POLICIES)):
            return {'response': False, 'msg': "You don't have the permissions to change policy."}
        try:
            return store.define_composite_policy(policy1_name, policy2_name, flag, percentage, name, valid_until)
        except Exception:
            return {'response': False, 'msg': "An unknown error has occurred. please try again."}

    @logger
    def get_discount_policy(self, store_name: str, policy_name: str):
        store: Store = self.get_store(store_name)
        if store is None:
            return {'response': False, 'msg': "Store doesn't exist"}
        try:
            return store.get_discount_policy(policy_name)
        except Exception:
            return {'response': False, 'msg': "An unknown error has occurred. please try again."}

    @logger
    def delete_purchase_policy(self, store_name: str, policy_name: str):
        store: Store = self.get_store(store_name)
        if store is None:
            return {'response': False, 'msg': "Store doesn't exist"}
        try:
            if store.delete_purchase_policy(policy_name):
                return {'response': True, 'msg': "Policy deleted successfully."}
            return {'response': False, 'msg': "Policy doesn't exists"}
        except Exception:
            return {'response': False, 'msg': "An unknown error has occurred. please try again."}

    @staticmethod
    @logger
    def delete_policy(store_name: str, policy_name: str):
        try:
            return (TradeControl.get_instance()).get_store(store_name).delete_policy(policy_name)
        except Exception:
            return ret(False, "Store doesn't exist.")

    @staticmethod
    @logger
    def at_least_one(details: {"name": str, "operator": str, "products": [str], "min_amount": int or None,
                               "max_amount": int or None, "dates": [dict] or None, "bundle": bool or None},
                     check_product: bool):
        """
            check if at least one of the given details is not none
        :param details:
        :param check_product:
        :return:
        """
        res = details.get("min_amount") is not None \
              or details.get("max_amount") is not None \
              or details.get("dates") is not None \
              or details.get("bundle") is not None
        if check_product:
            res = res or details.get("products") is not None
        return res

    # function for ut teardown
    def reset_purchase_policies(self, store_name: str):
        store = self.get_store(store_name)
        store.reset_policies()

    # ------------------- 4.2 --------------------

    # ----------- Getters & Setters --------------
    @logger
    def get_subscribers(self):
        return self.__subscribers

    @logger
    def get_stores(self):
        return self.__stores

    @logger
    def get_managers(self):
        return self.__managers

    @staticmethod
    @logger
    def get_guest():
        guest = User()
        return guest

    @logger
    def set_curr_user(self, curr: User):
        self.__curr_user = curr

    @logger
    def set_curr_user_by_name(self, nickname: str):
        self.__curr_user = self.get_subscriber(nickname)

    @logger
    def get_curr_user(self):
        return self.__curr_user

    @logger
    def get_curr_username(self):
        if self.__curr_user is not None and self.__curr_user.is_logged_in():  # TODO - maybe without is_logged_in?
            return self.__curr_user.get_nickname()
        return ""

    @logger
    def get_owned_stores(self):
        stores = []
        for store in self.__stores:
            # owners = store.get_owners()
            # if self.__curr_user.get_nickname() in owners:
            if store.is_owner(self.__curr_user.get_nickname()):
                stores.append(store.get_name())
        return stores
        # if len(stores) == 0:
        #     return {'response': [], 'msg': "There are no stores"}
        # return {'response': stores, 'msg': "Stores were retrieved successfully"}

    def get_managed_stores(self):
        stores = []
        for store in self.__stores:
            if store.is_manager(self.__curr_user.get_nickname()):
                stores.append(store.get_name())
        return stores
        # if len(stores) == 0:
        #     return {'response': [], 'msg': "There are no stores"}
        # return {'response': stores, 'msg': "Stores were retrieved successfully"}

    @logger
    def get_user_type(self):
        roles = []
        system_managers = [user.get_nickname() for user in self.__managers]
        if self.__curr_user is None:
            print("curr user is None")
            return "GUEST"
        if self.__curr_user.get_nickname() in system_managers:
            return "SYSTEMMANAGER"
        if self.__curr_user.is_registered():
            roles.append("SUBSCRIBER")
        for store in self.__stores:
            if store.is_owner(self.__curr_user.get_nickname()):
                roles.append("OWNER")
            elif store.is_manager(self.__curr_user.get_nickname()):
                roles.append("MANAGER")

        if "OWNER" in roles:
            return "OWNER"
        if "MANAGER" in roles:
            return "MANAGER"
        if "SUBSCRIBER" in roles:
            return "SUBSCRIBER"
        return "GUEST"

    def __repr__(self):
        return repr("TradeControl")

    def __delete__(self):
        TradeControl.__instance = None

    # ---------------------------------------------------------------------------------------

    @logger
    def __pull_subscribers_from_db(self) -> list:
        subscribers_from_db = (DataAccessFacade.get_instance()).read_users([])['response']
        output_lst = []
        for subscriber in subscribers_from_db:
            user = User()
            user.register_from_db(subscriber['username'], subscriber['password'])
            if subscriber['is_system_manager']:
                self.get_managers().insert(0, user)
            output_lst.insert(0, user)
        return output_lst
    @logger
    def __pull_stores_from_db(self) -> list:
        stores_from_db = (DataAccessFacade.get_instance()).read_stores([])['response']
        output_lst = []
        for store in stores_from_db:
            store_name = store['store_name']
            store_obj = Store(store['store_name'])
            store_obj.get_owners_appointments().append(StoreAppointment(None,
                                                                        self.get_subscriber(store['founder_username']),
                                                                        []))
            products_from_db = (DataAccessFacade.get_instance()).read_products([], store_name=store['store_name'])[
                'response']
            for product in products_from_db:
                # print(product)
                store_obj.add_product(store['founder_username'], product['product_name'],
                                      product['price'], product['category'], product['amount'],
                                      product['purchase_type'])
            store_owners_from_db = (DataAccessFacade.get_instance()).read_store_owner_appointments([],
                                                                                                   store_name=store_name
                                                                                                   )['response']
            for owner_appointment in store_owners_from_db:
                store_obj.get_owners_appointments().append(StoreAppointment(self.get_subscriber(
                    owner_appointment['appointer_username']),
                    self.get_subscriber(
                        owner_appointment['appointee_username']),
                    []))
            store_managers_from_db = (DataAccessFacade.get_instance()).read_store_manager_appointments([],
                                                                                                       store_name=
                                                                                                       store_name)[
                'response']
            for manager_appointment in store_managers_from_db:
                new_permissions: list = [key for key in list(manager_appointment.keys()) if manager_appointment[key]]
                new_permissions.remove("appointee_username")
                new_permissions.remove("appointer_username")
                new_permissions.remove("store_name")
                store_obj.get_store_manager_appointments().append(StoreAppointment(self.get_subscriber(
                    manager_appointment['appointer_username']),
                    self.get_subscriber(
                        manager_appointment['appointee_username']),
                    self.__convert_permissions_from_db(
                        new_permissions)))
            store_purchases_from_db = (DataAccessFacade.get_instance()).read_purchases([], store_name=store_name)[
                'response']
            for purchase_dict in store_purchases_from_db:
                prod_lst = [{'product_name': product_dict['product_name'],
                             'product_price': product_dict['product_purchase_price'],
                             'amount': product_dict['amount']} for product_dict in purchase_dict['products_lst']]
                purchase: Purchase = Purchase(total_price=purchase_dict['total_price'], store_name=store_name,
                                              username=purchase_dict['username'], products_list=prod_lst,
                                              purchase_time=purchase_dict['date'])
                store_obj.get_purchases(store['founder_username']).append(purchase)
                # print(purchase_dict)
            output_lst.insert(0, store_obj)
        return output_lst

    def __convert_permissions_from_db(self, permissions: list) -> list:
        map_per_name_to_column = [("EDIT_INV", "can_edit_inventory"),
                                  ("EDIT_POLICIES", "can_edit_policies"),
                                  ("APPOINT_OWNER", "can_appoint_owner"),
                                  ("DEL_OWNER", "can_delete_owner"),
                                  ("APPOINT_MANAGER", "can_appoint_manager"),
                                  ("EDIT_MANAGER_PER", "can_edit_manager_permissions"),
                                  ("DEL_MANAGER", "can_delete_manager"),
                                  ("CLOSE_STORE", "can_close_store"),
                                  ("USERS_QUESTIONS", "can_answer_user_questions"),
                                  ("WATCH_PURCHASE_HISTORY", "can_watch_purchase_history")]

        output = []
        all_permissions = []
        for i in range(1, 11):
            all_permissions.insert(i - 1, ManagerPermission(i))
        for i in range(len(map_per_name_to_column)):
            if map_per_name_to_column[i][1] in permissions:
                for per_as_enum in all_permissions:
                    if per_as_enum.name == map_per_name_to_column[i][0]:
                        output.insert(0, per_as_enum)
        return output

    def __pull_shopping_carts(self):
        for subscriber in self.__subscribers:
            subs_name = subscriber.get_nickname()
            shopping_cart_from_db = (DataAccessFacade.get_instance()).read_products_in_baskets([], username=subs_name)[
                'response']
            products_stores_quantity_ls = []
            for basket_as_dic in shopping_cart_from_db:
                dictionary = {"store_name": basket_as_dic['store_name'],
                              "product": self.get_store(basket_as_dic['store_name']).get_product(
                                  basket_as_dic['product_name']),
                              "amount": basket_as_dic['amount']}
                products_stores_quantity_ls.insert(0, dictionary)
            subscriber.save_products_to_basket(products_stores_quantity_ls)

    def __pull_personal_purchases(self):
        for user in self.__subscribers:
            user_purchases_from_db = (DataAccessFacade.get_instance()).read_purchases([], username=user.get_nickname())[
                'response']
            for purchase_dict in user_purchases_from_db:
                prod_lst = [{'product_name': product_dict['product_name'],
                             'product_price': product_dict['product_purchase_price'],
                             'amount': product_dict['amount']} for product_dict in purchase_dict['products_lst']]
                purchase: Purchase = Purchase(total_price=purchase_dict['total_price'],
                                              store_name=purchase_dict['store_name'],
                                              username=purchase_dict['username'],
                                              products_list=prod_lst,
                                              purchase_time=purchase_dict['date'])
                user.get_purchase_history().insert(0, purchase)



    # ------------------------------------------- UC 6.5 ---------------------------------------------------------

    @logger
    def get_visitors_cut(self, start_date, end_date):
        visitors_cut = []
        for s in self.__statistics:
            if s.in_range(start_date, end_date):
                date = s.get_date()
                # print (f'date = {date}. year = {date.year}, day = {date.day}')
                # visitors_cut.append({'date':date, 'guests': s.guests_amount(),
                visitors_cut.append({'date': datetime(date.year, date.month, date.day), 'guests': s.guests_amount(),
                                     'subscribers': s.subscribers_amount(),
                                     'store_managers': s.store_managers_amount(), 'store_owners': s.store_owners_amount(),
                                     'system_managers': s.system_managers_amount()})
        # print(f'visitor cuts = {visitors_cut}')
        answer = {'msg': 'succc', 'response': visitors_cut}
        # print (f'ans = {answer}')
        return answer

    @logger
    def inc_todays_guests_counter(self):
        self.__statistics[0].inc_guests_counter()

    @logger
    def reset_statistics(self, counter_type):
        today_statistics = Statistics()
        if counter_type == 'guest':
            today_statistics.inc_guests_counter()
        elif counter_type == 'subscriber':
            today_statistics.inc_subscribers_counter()
        elif counter_type == 'store_manager':
            today_statistics.inc_store_managers_counter()
        elif counter_type == 'store_owner':
            today_statistics.__store_owners_amount()
        elif counter_type == 'system_manager':
            today_statistics.inc_system_managers_counter()
        else:
            print("problem at TradeControl.reset_statistics") # TODO- delete
        self.__statistics.append(today_statistics)
        print(f"statistics: {self.__statistics}. todays = {today_statistics}")