import logging

# from src.Logger import Logger

from src.Logger import Logger
from src.main.DomainLayer import Product


def logger(f, name=None):
    # if logger.fhwr isn't defined and open ...
    try:
        if logger.fhwr:
            pass
    except:
        # ... open it
        logger.fhwr = open("WorkshopProject.log", "w")
    if name is None:
        name = f.__qualname__

    def wrapped(*args, **kwargs):
        logger.fhwr.write("The function " + str(name) + " was called\n"
                          + "arguments: " + str(args) + str(kwargs) + "\n\n")
        result = f(*args, **kwargs)
        return result

    wrapped.__doc__ = f.__doc__
    return wrapped


# def logger(f):
#     logging.basicConfig(filename="WorkshopProject.txt",
#                         format='%(asctime)s >> %(levelName)s: %(message)s',
#                         # format='%(asctime)s >> %(levelName)s: %(module)s %(funcName)s %(message)s',
#                         filemode='w')
#
#     # Creating a self._logger object with the relevant module name
#     logger = logging.getLogger(__name__)
#
#     # Setting the threshold of self._logger to DEBUG
#     logger.setLevel(logging.INFO)
#
#     def wrapped(*args, **kwargs):
#         logger.info("The function "+str(f.__qualname__)+" was called\n"
#                 +"arguments: "+ str(args)+str(kwargs)+"\n\n")
#         result = f(*args, **kwargs)
#         return result
#     wrapped.__doc__ = f.__doc__
#     return wrapped()

class StoreInventory:

    def __init__(self):
        # list of the pairs (product, amount)
        self.__inventory = []
        # list of search functions: __fun_map[0] = searchProductsByName(product_name)
        #                           __fun_map[1] = searchProductByKeyword(keyword)
        #                           __fun_map[2] = searchProductByCategory(category)
        #  all the functions returns list of products
        self.__fun_map = [lambda product_name: list(
            filter(lambda product: product.get_name() == product_name, [x[0] for x in self.__inventory])),
                          lambda keyword: list(
                              filter(lambda product: keyword in product.get_name(), [x[0] for x in self.__inventory])),
                          lambda category: list(filter(lambda product: product.get_category() == category,
                                                       [x[0] for x in self.__inventory]))]
        # logging.basicConfig(filename="WorkshopProject.log",
        #                     format='%(asctime)s >> %(levelName)s: %(message)s',
        #                     # format='%(asctime)s >> %(levelName)s: %(module)s %(funcName)s %(message)s',
        #                     filemode='w')
        #
        # # Creating a self._logger object with the relevant module name
        # self.logger = logging.getLogger(__name__)
        #
        # # Setting the threshold of self._logger to INFO
        # self.logger.setLevel(logging.INFO)

    @logger
    def add_product(self, product: Product, amount) -> bool:
        """
        :param product: Product
        :param amount: amount of product
        :return: true,and the inventory updated with the new product or the products amount is increased
        """
        # msg = "The function StoreIventory.add_product(" + str(product) + ", " + str(amount) + ") was called"
        # logging.LogRecord(name =__name__, level= logging.INFO, func= self.add_product,
        #                   pathname="src/WorkshopProject.log", msg="function call", args=(product, amount))
        # Logger().add_to_log(msg)
        # product.set_name("1")
        products_ls = self.__fun_map[0](product.get_name())
        if len(products_ls):
            old_product_amount = self.get_amount_of_product(product.get_name())
            self.remove_product(product.get_name())
            self.__inventory.append((product, amount + old_product_amount))
        else:
            self.__inventory.append((product, amount))
        return True

    @logger
    def get_product(self, product_name):
        products_list = self.__fun_map[0](product_name)
        if len(products_list):
            return products_list[0]
        return None

    @logger
    def get_products_by(self, opt, string):
        """
        :param opt: search option = 1-byName, 2- byKeyword, 3- byCategoru
        :param string: for opt: 1 -> productName, 2 -> string, 3 -> category
        :return: list of products according to the selected searching option
        """
        ls = self.__fun_map[opt - 1](string)
        return ls

    @logger
    def remove_product(self, product_name):
        """
        :param product_name: product to delete from inventory
        :return: True if the inventory updated without the product
        """
        for p in self.__inventory:
            if product_name == p[0].get_name():
                self.__inventory.remove(p)
                return True
        return False

    @logger
    def change_amount(self, product_name, new_amount) -> bool:
        """
        :param product_name: product name to edit
        :param new_amount: number to replace with
        :return: True if the product updated with new amount on inventory
        """
        # product = self.get_product(product_name)
        # if product is not None:
        #     product.set_amount(new_amount)
        #     return True
        for i in self.__inventory:
            if i[0].get_name() == product_name:
                self.__inventory.remove(i)
                self.__inventory.append((i[0], new_amount))
                return True
        return False

    @logger
    def len(self):
        """
        :return: amount of products on inventory
        """
        return len(self.__inventory)

    @logger
    def get_amount_of_product(self, product_name):
        for i in self.__inventory:
            if i[0].get_name() == product_name:
                return i[1]
        return None

    @logger
    def is_in_stock(self, product_name, requested_amount):
        """
        This function check if the product exist in the store inventory.
        If it does exist, check if the quantity of the product in the stock inventory is enough for making the purchase.

        :param product_name: the name of the product to search in inventory.
        :param requested_amount: the requested amount.
        :return: if is in stock true,
                 else false.
        """
        amount_in_stock = self.get_amount_of_product(product_name)
        if amount_in_stock:
            if int(amount_in_stock) >= requested_amount:
                return True
        else:
            return False

    def __repr__(self):
        return repr("StoreInventory")
