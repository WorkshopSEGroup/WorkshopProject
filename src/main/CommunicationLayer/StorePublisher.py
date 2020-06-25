from jsonpickle import json


# from src.main.CommunicationLayer.WebSocketService import notifyPurchase
# from src.main.CommunicationLayer.WebSocketService import send_msg
from src.Logger import logger


class StorePublisher:

    def __init__(self, store_name, owner_nickname):
        # print ("in constructor")
        self.__name = store_name
        # list of all owners ( lastReadMsg: int, nickname: string, ws:websocket)
        # lastReadMsg = last msg id (from msgs) the owner have read
        self.__subscribers = [(owner_nickname, 0, True, [])]
        # list of all notifications (id: int, msg: string, is_logged_in: bool, personal_msgs:list)
        self.__msgs = []
        # print(f"store name- {self.__name}, it's subscriber - {self.__subscribers}")

    @logger
    def add_msg(self, msg, event):  # the setStatus function
        """

        :param msg:
        :return:
        """
        self.__msgs.append((len(self.__msgs), msg, event))
        print (f"at storePublisher {self.__name}, msgs= {self.__msgs}. last add_msg call with msg {msg}")
        # self.notifyAll()

    # def notifyAll(self):
    #     """
    #     check for each subscriber if there is a new msg- and send it if there is at least 1
    #     :return:
    #     """
    #     for (name, last_msg_id, is_logged_in, personal_msgs) in self.__subscribers:
    #         amount_of_msgs = len(self.__msgs)  # maybe len-1
    #         if is_logged_in and last_msg_id < amount_of_msgs:
    #             self.notify(name)
    #
    # def notify(self, user_name):
    #     """
    #     if there is a new msg to send to the subscriber with user_name - send it
    #     :param user_name: of owner
    #     :return:
    #     """
    #     lastMsgID = self.get_last_read_msg_id(user_name)
    #     if lastMsgID > -1:
    #         # for (msg_id, msg) in self.__msgs:
    #         #     if msg_id > lastMsgID:
    #         #         send_msg(user_name, msg)
    #         unread_msgs = []
    #         for msg_id, msg, event in self.__msgs:
    #             if msg_id > lastMsgID:
    #                 unread_msgs += msg
    #                 self.inc_last_unread_msg(user_name)

    @logger
    def retrieveMsgs(self, user_name):
        """
        if there is a new msg to send to the subscriber with user_name - send it
        :param user_name: of owner
        :return:
        """
        self.login_subscriber(user_name)
        lastMsgID = self.get_last_read_msg_id(user_name)
        print(f"last read msg id of subscriber {user_name} is {lastMsgID}")
        if lastMsgID > -1 or (lastMsgID == 0 and self.amount_of_msgs() == 1):
            # for (msg_id, msg) in self.__msgs:
            #     if msg_id > lastMsgID:
            #         send_msg(user_name, msg)
            unread_msgs = []
            for msg_id, msg, event in self.__msgs:
                if msg_id > lastMsgID or msg_id == 0:
                    unread_msgs.append((msg, event))
                    # unread_msgs += (msg, event)
                    self.inc_last_unread_msg(user_name)
                # elif msg_id == 0:
                #     unread_msgs.append((msg, event))
            print(f"unread msgs at store {self.__name} are {unread_msgs}")
            return unread_msgs

    @logger
    def get_last_read_msg_id(self, user_name):
        """
        returns the id of the last msg the subscriber with user_name has read
        :param user_name: subscriber nickname
        :return: msg id on queue. unique values: -1 if no msgs since the user subscribed, -2 as false
        """
        for (name, msg_id, is_logged_in, personal_msgs) in self.__subscribers:
            if name == user_name:
                return msg_id
        return -2

    @logger
    def retrieve_msg_by_id(self, user_name, last_read_msg_id):  # maybe add store_name, or add store controller
        """
        sends unread msgs to the owner with user_name (if its a subscriber to this store)
        assumes validate input
        :param user_name: of owner
        :param last_read_msg_id: last read msg by the client-side
        :return:
        """
        last_read_msg_by_server = self.get_last_read_msg_id(user_name)
        if last_read_msg_by_server == last_read_msg_id:
            self.inc_last_msg_id(user_name)
            return self.__msgs[last_read_msg_id + 1]

    @logger
    def subscribe_owner(self, nick_name, is_logged_in):  # maybe add store_name, or add store controller
        """
        by receive new appointment of store owner, this func will subscribe the owner to the
        relevant store-topic-publisher, the owner will receive only msgs that have been sent after
        his appointment
        :param nick_name: owner-to-subscribe nickname
        """
        if (self.is_subscribed_to_store(nick_name)):
            return False
        self.__subscribers.append((nick_name, len(self.__msgs), is_logged_in, []))
        # print(f"subscribers: {self.__subscribers}")
        return True
        # return some validation?

    @logger
    def unsubscribe_owner(self, nick_name):
        """
        delete owner from the store's subscribers list (probably will be called from remove owner)
        if the owner is not on subscribers list - the func will do nothing
        :param nick_name: of the removed owner
        """
        counter = 0
        for subscriber in self.__subscribers:
            if counter != 0:
                (owner_name, last_read_msg, is_logged_in, personal_msgs) = subscriber
                if owner_name == nick_name:
                    # print(f"owner {owner_name}, id {last_read_msg}, sub {subscriber}")
                    self.__subscribers.remove(subscriber)
                    # self.__subscribers.remove((owner_name, last_read_msg))
                    # print(f"is subscribe --> {self.is_subscribed_to_store(owner_name)}")
                    # print(f"subscribers: {self.__subscribers}")
                    return 0
            else:
                counter = counter+1
        return -1
        # return some validation?

    @logger
    def logout_subscriber(self, username):
        for subscriber in self.__subscribers:
            (owner_name, last_read_msg, is_logged_in, personal_msgs) = subscriber
            if owner_name == username:
                self.__subscribers.remove(subscriber)
                self.__subscribers.append((owner_name, last_read_msg, False, personal_msgs))

    @logger
    def store_name(self):
        return self.__name

    @logger
    def subscribers(self):
        return self.__subscribers

    @logger
    def amount_of_subscribers(self):
        return len(self.__subscribers)

    @logger
    def amount_of_msgs(self):
        return len(self.__msgs)

    @logger
    def is_subscribed_to_store(self, nickname):
        if self.__subscribers is None:
            # print ("is sub error")
            return False
        # print("is subscribe subscribers: " + str(self.__subscribers))
        for (owner_name, last_read_msg, is_logged_in, personal_msgs) in self.__subscribers:
            if owner_name == nickname:
                return True
            # print(f"nickname = {owner_name}, last id = {last_read_msg}")
        # print(f"cannot find owner {nickname}")
        return False

    @logger
    def inc_last_unread_msg(self, user_name):
        for username, lastUnreadMsg, is_logged_in, personal_msgs in self.__subscribers:
            if user_name == username:
                lastUnreadMsg += 1

    def __repr__(self):
        return repr(f"{self.__name} Publisher Details --> Subscribers: {self.__subscribers}, Msgs: {self.__msgs}")

    @logger
    def login_subscriber(self, user_name):
        for subscriber in self.__subscribers:
            (username, msg_id, is_logged_in, personal_msgs) = subscriber
            if user_name == username:
                self.__subscribers.remove(subscriber)
                self.__subscribers.append((username, msg_id, True, personal_msgs))
                print (f"connect {user_name} to msgs from store {self.__name}")
                return True
        return False

    @logger
    def is_logged_in(self, user_name):
        for subscriber in self.__subscribers:
            (username, msg_id, is_logged_in, personal_msgs) = subscriber
            if user_name == username and is_logged_in:
                return True
        return False

    @logger
    def add_personal_msg(self, user_name, msg):
        for subscriber in self.__subscribers:
            (username, msg_id, is_logged_in, personal_msgs) = subscriber
            if user_name == username:
                personal_msgs.append(msg)

    @logger
    def get_personal_msgs(self, user_name):
        msgs=[]
        for subscriber in self.__subscribers:
            (username, msg_id, is_logged_in, personal_msgs) = subscriber
            if user_name == username:
                self.__subscribers.remove(subscriber)
                self.__subscribers.append((username, msg_id, is_logged_in, []))
                print(f"p = {personal_msgs}")
                return personal_msgs
        return msgs