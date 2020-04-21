class Product:
    def __init__(self, name, price):
        # self.__id = id
        self.__name = name
        self.__price = price
        # self.__rate = 0 TODO - for search 2.5
        # TODO - add category here or on Store? (for search - use case 2.5)
        # TODO - add more details? for each new detail need to open set_detail for use case 4.1 - owner can edit product's details

    def get_name (self):
        return self.__name

    def set_price (self, new_price):
        self.__price=new_price

    def set_name(self, new_name):
        self.__name = new_name



pass