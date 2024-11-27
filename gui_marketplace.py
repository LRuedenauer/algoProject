# Status: Not FINAL, dgaida2, 15.10.2024

# main file

import tkinter as tk
import threading

from auctionapp_init import AuctionAppInit


class AuctionApp(AuctionAppInit):
    # *** CONSTRUCTORS ***
    def __init__(self, root):
        super().__init__(root)

        self.start_update_timer()

    # *** Alle 30 Sekunden wird überprüft welche Auktionen abgelaufen sind und die Listen werden aktualisiert ***

    def update_listboxes(self):
        self._check_auctions_expiry()

        top_auction = self._auctions.get_top_auction(True)

        if top_auction is not None:
            self.system_messages.push(
                "Die TOP Auktion mit {0} Geboten ist Auktion {1} in der man ein {2} für aktuell {3} € ersteigern kann.".format(
                    top_auction[0], top_auction[1], self._auctions.get_item_name(top_auction[1]),
                    self._auctions.get_highest_bid(top_auction[1])
                ))
            # print('TOP Auction: {}'.format(top_auction))

        top_user = self._auctions.get_top_rated_user(True)

        if top_user is not None:
            self.system_messages.push("Der am besten bewertete User mit {0:.1f} Sternen ist user {1}.".format(
                    top_user[0], top_user[1])
                )

        # Aktualisieren Sie alle Listboxen hier
        self.add_items2all_items_list()
        self.search_items()

        if self._current_user:
            self.update_lists()

        # TODO: warum wird das gemacht? current_thread wird nicht weiter genutzt
        current_thread = threading.current_thread()

        # Wiederhole die Aktualisierung alle 30 Sekunden (30000 Millisekunden)
        self.root.after(30000, self.update_listboxes)

    def start_update_timer(self):
        # Starte den Timer zur Aktualisierung der Listboxen
        self.update_listboxes()

    # *** PRIVATE METHODS ***

    def _check_auctions_expiry(self):
        for auction_id, auction in self._auctions.items():
            # gehe alle Auktionen durch, die abgelaufen sind, aber noch nicht als verkauft gelten. das sind Auktionen,
            # bei denen der neue Käufer noch nicht eingetragen ist. der Käufer wird in handle_expired_auction() gesetzt.
            # da wir über jede Auktion nur einmal informieren wollen, ist die Abfrage auction.sold wichtig
            if auction.expired() and not auction.sold():
                success = self._auctions.handle_expired_auction(auction_id)

                if auction.seller_id() == self._current_user.id():
                    if success:
                        self.system_messages.push(
                            "Ihr {0} wurde gerade erfolgreich für {1:.2f} € versteigert.".format(
                                auction.get_item_name(), auction.get_highest_bid()))
                    else:
                        self.system_messages.push(
                            "Ihre Auktion für {0} ist ausgelaufen, hat aber keinen Käufer gefunden.".format(
                                auction.get_item_name()))

                if auction.purchaser_id() == self._current_user.id():
                    self.system_messages.push(
                        "Sie haben {0} gerade erfolgreich für {1:.2f} € ersteigert.".format(
                            auction.get_item_name(), auction.get_highest_bid()))

                if auction.is_user_bidding(self._current_user.id()):
                    if auction.purchaser_id() != self._current_user.id():
                        self.system_messages.push(
                            "Die Auktion für {0} wurde gerade beendet, allerdings wurde Ihr Angebot überboten.".format(
                                auction.get_item_name()))

    # *** ... ***


if __name__ == "__main__":
    root = tk.Tk()
    app = AuctionApp(root)
    root.mainloop()
