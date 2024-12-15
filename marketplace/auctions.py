import marketplace.auction
import marketplace.item
import marketplace.users
import marketplace.simulator
from marketplace.max_heap import MaxHeap
import random
import threading
import csv


class Auctions(dict):
    """
    Class representing a dictionary of auctions

    Attributes:
        _id_next_auction (int):
        _heap (marketplace.max_heap.MaxHeap):
        _users (marketplace.users.Users): contains all users of the platform
        _my_simulator (marketplace.simulator.Simulator): simulates other users selling and buying stuff
        _stop_event (threading.Event): needed to stop simulator when user wants to close application
        _heap_users_rated (marketplace.max_heap.MaxHeap): tracks the top-rated users efficiently
    """

    def __init__(self, csvfile, *args):
        super().__init__(self)

        self._id_next_auction = 0

        try:
            self._heap = MaxHeap()
        except NotImplementedError:
            self._heap = None

        # Create a MaxHeap to store top-rated users
        self._heap_users_rated = MaxHeap()

        self._users = marketplace.users.Users("user.csv")

        self._read_auctions_from_csvfile(csvfile)

        self._place_random_bids(num_bids=10 * self._users.num_users())

        self._my_simulator = marketplace.simulator.Simulator()

        self._stop_event = threading.Event()

    def add_new_auction(self, user_id: str, item_name: str, description="", value_min=1):
        """
        Adds a new auction to the dictionary for the given item

        :param user_id: id of a user.
        :param item_name: Name of the item to be sold
        :param description: a sentence describing the item
        :param value_min: minimal value of the item in €
        :return:
        """
        item = marketplace.item.Item(item_name, description, value_min)

        auction, auction_id = self._new_auction(user_id, item)

        self[auction_id] = auction

        return auction

    def add_user_rating(self, seller_id: str, rating: int):
        """
        Allows users to rate a seller (1 to 5 stars).

        :param seller_id: ID of the seller being rated
        :param rating: Rating value (1 to 5 stars)
        """
        if seller_id in self._users:
            user = self._users[seller_id]
            user.add_rating(rating)

            # Update the MaxHeap with the new rating
            mean_rating = user.get_rating_stars_mean()
            self._heap_users_rated.update(seller_id, mean_rating)

    def get_top_rated_user(self, with_num_stars=False):
        """
        Returns user ID of the top-rated user, leveraging the MaxHeap for efficiency.
        :param with_num_stars: If True, return stars together with user_id.
        :return:
        """
        if not self._heap_users_rated:
            return None

        top_user = self._heap_users_rated.get_top_user()
        if with_num_stars:
            return top_user  # Returns (mean_stars, user_id)
        else:
            return top_user[1]  # Returns only user_id

    def start_top_rated_user_notifications(self):
        """
        Periodically logs the top-rated user every 30 seconds.
        """

        def notify():
            if self._stop_event.is_set():
                return

            top_user = self.get_top_rated_user(with_num_stars=True)
            if top_user:
                mean_stars, user_id = top_user
                print(
                    f"System Message: Top-rated seller is {user_id} with an average rating of {mean_stars:.2f} stars.")

            timer = threading.Timer(30, notify)
            timer.start()
            self._timer = timer

        notify()

    def bid_in_auction(self, auction_id, user, bid_amount):
        if auction_id in self:
            success = self[auction_id].bid(user, bid_amount)
            if success and self._heap is not None:
                self._heap.update_bidders(auction_id, self[auction_id].bid_count())
            return success

    def delete(self, auction_id):
        # funktioniert nur, wenn noch niemand auf diese Auktion geboten hat, sonst kann man Auktion nicht löschen
        # muss dann auch item in self[auction_id] löschen, bzw. muss das?
        if not self[auction_id].is_any_bidder():
            del self[auction_id]
            return True
        else:
            return False

    def start_simulation_init(self, current_user_id):
        self._start_simulator(current_user_id)

    def stop_simulation(self):
        self._stop_event.set()

        if hasattr(self, '_timer') and self._timer.is_alive():
            self._timer.cancel()

    def __delitem__(self, key):
        super().__delitem__(key)
        if self._heap is not None:
            self._heap.remove(key)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if self._heap is not None:
            self._heap.add_auction(value.id(), value.bid_count())

    def get_time_left(self, auction_id):
        return self[auction_id].get_time_left()

    def get_auction_ends(self, auction_id):
        return self[auction_id].auction_ends()

    def get_seller_id(self, auction_id):
        return self[auction_id].seller_id()

    def get_purchaser_id(self, auction_id):
        return self[auction_id].purcahser_id()

    def get_item(self, auction_id):
        return self[auction_id].item()

    def get_item_name(self, auction_id):
        return self[auction_id].get_item_name()

    def get_all_item_names(self):
        return [self.get_item_name(auction_id) for auction_id in self]

    def get_item_description(self, auction_id):
        return self[auction_id].get_item_description()

    def get_item_value_min(self, auction_id: str):
        return self[auction_id].get_item_value_min()

    def get_users_bidding(self, auction_id: str):
        return self[auction_id].users_bidding()

    def get_highest_bid(self, auction_id: str):
        return self[auction_id].get_highest_bid()

    def get_highest_bidder(self, auction_id: str):
        return self[auction_id].get_highest_bidder()

    def get_auctions_offered(self, user_id):
        return [auction_id for auction_id, auction in self.items()
                if auction.seller_id() == user_id and not auction.sold()]

    def get_auctions_bid_in(self, user_id: str):
        return [auction_id for auction_id, auction in self.items()
                if auction.is_user_bidding(user_id) and not auction.sold()]

    def get_auctions_sold(self, user_id: str):
        return [auction_id for auction_id, auction in self.items()
                if auction.seller_id() == user_id and auction.sold_success()]

    def get_auctions_won(self, user_id: str):
        return [auction_id for auction_id, auction in self.items() if auction.purchaser_id() == user_id]

    def get_auctions_is_recommended(self, user_id: str):
        return [auction_id for auction_id, auction in self.items()
                if auction.is_recommended2user(user_id) and not auction.sold()]

    def get_is_user_bidding(self, auction_id, user_id):
        return self[auction_id].is_user_bidding(user_id)

    def get_bid_of_user(self, auction_id: str, user_id: str):
        return self[auction_id].get_bid_of_user(user_id)

    def get_last_bid(self, auction_id: str):
        return self[auction_id].get_last_bid()

    def get_auctions_friends_offer(self, user_id: str):
        friends = self._users[user_id].friends()
        friends_auctions = {}

        for friend_id in friends:
            auctions_friend = self.get_auctions_offered(friend_id)
            for auction_id in auctions_friend:
                if auction_id in friends_auctions:
                    friends_auctions[auction_id] += 1
                else:
                    friends_auctions[auction_id] = 1

        if friends_auctions:  # friends_actions could also be empty, then max throws an error
            max_auction = max(friends_auctions, key=friends_auctions.get)

            self[max_auction].recommend2user(user_id)

    def get_auctions_friends_bid_in(self, user_id: str):
        friends = self._users[user_id].friends()
        friends_auctions = {}

        for friend_id in friends:
            auctions_friend = self.get_auctions_bid_in(friend_id)
            for auction_id in auctions_friend:
                if auction_id in friends_auctions:
                    friends_auctions[auction_id] += 1
                else:
                    friends_auctions[auction_id] = 1

        if friends_auctions:  # friends_actions could also be empty, then max throws an error
            max_auction = max(friends_auctions, key=friends_auctions.get)

            self[max_auction].recommend2user(user_id)

    def get_top_auction(self, with_num_bids=False):

        if not self._heap:
            return None
        if with_num_bids:
            return self._heap.get_auction_with_max_bidders()
        else:
            return self._heap.get_auction_with_max_bidders()[1]

    def get_active_auctions(self):
        auctions_active = {}
        for auction_id, auction in self.items():
            if not auction.sold():
                auctions_active[auction_id] = auction

        return auctions_active

    @staticmethod
    def sort_time_left(auctions_dict):
        auctions_dict_sorted = dict(sorted(auctions_dict.items(), key=lambda x: x[1].auction_ends(), reverse=False))

        return auctions_dict_sorted

    def _new_auction(self, user_id, item):
        auction_id = self._create_new_auction_id()

        auction = marketplace.auction.Auction(auction_id, user_id, item)

        return auction, auction_id

    def _create_new_auction_id(self):
        auction_id = "a" + str(self._id_next_auction)
        self._id_next_auction += 1
        return auction_id

    def _read_auctions_from_csvfile(self, csvfile):
        auctions = {}

        with open(csvfile, newline='', encoding='utf-8-sig') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)

            for row in csvreader:
                item_name, description, user_id, value_min = row

                item = marketplace.item.Item(item_name, description, float(value_min))
                auction, auction_id = self._new_auction(user_id, item)

                auctions[auction_id] = auction

        auctions = self.sort_time_left(auctions)

        for auction in auctions:
            self[auction] = auctions[auction]

    def _place_random_bids(self, num_bids=10, user_ids=None, show_message=False, current_user_id=None):
        if user_ids is None:
            user_ids = list(self._users.keys())

        auctions_active = self.get_active_auctions()

        auction_ids = list(auctions_active)

        if len(auction_ids) < num_bids:
            raise ValueError(f"Nicht genügend Auktionen vorhanden, um {num_bids} zufällige Gebote zu platzieren.")

        for _ in range(num_bids):
            random_user = random.choice(user_ids)
            random_auction = random.choice(auction_ids)

            min_bid = self.get_item_value_min(random_auction)

            random_bid = min_bid + random.randint(1, 50)
            self.bid_in_auction(random_auction, self._users[random_user], random_bid)

            if show_message:
                bid_by_current_customer = self.get_bid_of_user(random_auction, current_user_id)
                if bid_by_current_customer is not None and bid_by_current_customer < random_bid:
                    print('Angebot von current_user wurde überboten')
                    print('Letzte Auktion kam von Nutzer {0}, das steht auch im Stapel: {1}'.format(
                        random_user, self.get_last_bid(random_auction)))

    def _start_simulator(self, current_user_id: str):
        if self._stop_event.is_set():
            return

        self._my_simulator.place_random_bids(self, current_user_id)

        self._my_simulator.create_random_auctions(self, current_user_id)

        self._my_simulator.randomly_rate_users(self._users, current_user_id)

        timer = threading.Timer(30, self._start_simulator, args=(current_user_id,))
        timer.start()
        self._timer = timer

    def _set_purchaser_id(self, auction_id):
        purchaser_id = self[auction_id].set_purchaser_id()
        seller_id = self[auction_id].seller_id()
        highest_bid = self[auction_id].get_highest_bid()

        if self._heap is not None:
            self._heap.remove(auction_id)

        if purchaser_id in self._users:
            self._users[seller_id].increase_balance(highest_bid)

            for (bid_of_user, user_id) in self[auction_id].users_bidding():
                if user_id != purchaser_id:
                    self._users[user_id].increase_balance(-bid_of_user)

            return True
        else:
            return False

    def handle_expired_auction(self, auction_id):
        if not self[auction_id].sold():
            return self._set_purchaser_id(auction_id)
        else:
            return False

    def id_next_auction(self):
        return self._id_next_auction

    def users(self):
        return self._users
