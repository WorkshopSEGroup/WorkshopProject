# {'date': datetime(2020, 6, 15), 'guests': 3, 'subscribers': 4, 'store_managers': 5, 'store_owners': 6, 'system_managers': 7},
#         #                          {'date':
import datetime

from src.Logger import logger
from src.main.DataAccessLayer.DataAccessFacade import DataAccessFacade


class Statistics:

    def __init__(self):
        self.__date = datetime.datetime.today()
        # print(f"self date = {self.__date}")
        self.__guests_amount : int = 0
        self.__subscribers_amount = 0
        self.__store_managers_amount = 0
        self.__store_owners_amount = 0
        self.__system_managers_amount = 0
        self.__DB_handler = DataAccessFacade.get_instance()
        self.save_date_statistics_on_DB()

    @logger
    def get_date (self):
        return self.__date

    @logger
    def guests_amount (self):
        return self.__guests_amount

    @logger
    def subscribers_amount (self):
        return self.__subscribers_amount

    @logger
    def store_managers_amount (self):
        return self.__store_managers_amount

    @logger
    def store_owners_amount (self):
        return self.__store_owners_amount

    @logger
    def system_managers_amount (self):
        return self.__system_managers_amount

    @logger
    def inc_guests_counter(self):
        if self.correct_date('guest'):
            self.__guests_amount += 1
            self.__DB_handler.update_statistics(old_date=self.__date, new_guests=self.__guests_amount)
            return True
        return 'guest'

    @logger
    def inc_subscribers_counter(self):
        if self.correct_date('subscriber'):
            self.__subscribers_amount += 1
            self.__DB_handler.update_statistics(old_date=self.__date, new_subscribers=self.__subscribers_amount)
            return True
        return 'subscriber'

    @logger
    def inc_store_managers_counter(self):
        if self.correct_date('store_manager'):
            self.__store_managers_amount += 1
            self.__DB_handler.update_statistics(old_date=self.__date, new_store_managers=self.__store_managers_amount)
            return True
        return 'store_manager'

    @logger
    def inc_store_owners_counter(self):
        if self.correct_date('owner'):
            self.__store_owners_amount += 1
            self.__DB_handler.update_statistics(old_date=self.__date, new_store_owners=self.__store_owners_amount)
            return True
        return 'owner'

    @logger
    def inc_system_managers_counter(self):
        if self.correct_date('system_manager'):
            self.__system_managers_amount += 1
            self.__DB_handler.update_statistics(old_date=self.__date, new_system_managers=self.__system_managers_amount)
            return True
        return 'system_manager'

    @logger
    def save_date_statistics_on_DB(self):
        return self.__DB_handler.write_statistic(self.__date, self.__guests_amount, self.__subscribers_amount,
                                                  self.__store_managers_amount, self.__store_owners_amount,
                                                  self.__system_managers_amount)
        # return True

    @logger
    def correct_date(self, counter_kind):
        # print(f"check the dates: self={self.__date.date().day}, today={datetime.datetime.today().day}")
        if (self.__date.date().day == datetime.datetime.today().day):
            # print("works")
            return True
        return False

    @logger
    def in_range(self, start_date, end_date):
        # TODO
        return True

    def __repr__(self):
        str = f'guests = {self.__guests_amount}     subscribers = {self.__subscribers_amount}       ' \
              f'store managers = {self.__store_managers_amount}     store owners = {self.__store_owners_amount}     ' \
              f'system managers = {self.__system_managers_amount}'
        return repr(str)

    # def reset_daily_statistics(self, counter_kind):
    #     self.__date = datetime.datetime.today()
    #     self.__guests_amount = 0
    #     self.__subscribers_amount = 0
    #     self.__store_managers_amount = 0
    #     self.__store_owners_amount = 0
    #     self.__system_managers_amount = 0


