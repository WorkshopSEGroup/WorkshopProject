from datetime import datetime

from src.main.DomainLayer.StoreComponent.PurchasePolicyComposite.PurchaseComponent import PurchaseComponent


class MaxAmountPolicy(PurchaseComponent):

    def __init__(self, max_amount: int, products: [str]):
        super().__init__()
        self._name = "max_amount"
        self.__amount = max_amount
        self.__products = products

    def can_purchase(self, details: [{"product_name": str, "amount": int}], curr_date: datetime) -> bool:
        for product in details:
            flag = product["amount"] <= self.__amount
            if ("all" in self.__products and flag) or (product["product_name"] in self.__products and flag):
                return True
        return False

    def equals(self, details: {"products": [str], "min_amount": int or None, "max_amount": int or None,
                               "dates": [dict] or None, "bundle": bool or None}) -> bool:
        if details.get("max_amount") \
                and details.get("max_amount") == self.__amount \
                and set(self.__products) == set(details["products"]):
            # for product in self.__products:
            #     if product not in details["products"]:
            #         return False
            return True
        return False

    def get_name(self):
        return self._name

    def get_details(self, dictionary: dict):
        dictionary[self._name] = self.__amount
        return dictionary

    def update(self, details: {"name": str, "products": [str], "min_amount": int or None, "max_amount": int or None,
                               "dates": [dict] or None, "bundle": bool or None}):
        if details.get("max_amount"):
            self.__products = details["products"]
            self.__amount = details["max_amount"]

    def get_products(self):
        return self.__products

    def get_max_amount(self):
        return self.__amount