# Status: Not FINAL, dgaida2, 15.10.2024

# Definiert die Basis Klasse für Klasse AuctionApp.
# In dieser Klasse werden alle GUI Elemente erstellt. Die wichtigste Methode ist create_widgets()

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from collections import Counter

import marketplace.auctions
import marketplace.user
import marketplace.trie
import marketplace.auction
import marketplace.systemmessages
import marketplace.avl_tree
from marketplace import avl_tree


class AuctionAppInit:
    def __init__(self, root):
        self.root = root
        self.root.title("Online-Marktplatz für Auktionen")

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self._auctions = marketplace.auctions.Auctions("auctions.csv")

        self._users = self._auctions.users()

        # der aktuell eingeloggte user
        self._current_user = None

        # erstelle gui
        self.create_widgets()

        self.root.bind("<Configure>", self.update_tooltip_position)
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        # füge alle Auktionen zur Liste der Auktionen hinzu
        self.add_items2all_items_list()

        self.trie = marketplace.trie.Trie()
        self.avl_tree = avl_tree.AVLTree()

        self.tooltip = None
        self.initialize_trie()

        self.enable_widgets(False)  # Initially disable all widgets

    def create_frame_useraccount(self):
        self.frame_useraccount = ttk.Frame(self.root)
        self.frame_useraccount.grid(row=0, column=6, padx=5, pady=5, sticky="ew")

        # Nutzername und Passwort
        self.username_entry = tk.Entry(self.frame_useraccount)
        self.username_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.username_entry.insert(0, "")

        self.password_entry = tk.Entry(self.frame_useraccount, show='*')
        self.password_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.password_entry.insert(0, "")

        self.login_btn = tk.Button(self.frame_useraccount, text="Einloggen", command=self.login)
        self.login_btn.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.register_btn = tk.Button(self.frame_useraccount, text="Registrieren", command=self.register)
        self.register_btn.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        tk.Label(self.frame_useraccount, text="     ").grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        self.logout_btn = tk.Button(self.frame_useraccount, text="Logout", command=self.logout)
        self.logout_btn.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        self.account_btn = tk.Button(self.frame_useraccount, text="Mein Account", command=self.my_account)
        self.account_btn.grid(row=0, column=6, padx=5, pady=5, sticky="ew")

        self.frame_useraccount.columnconfigure(0, weight=1)
        self.frame_useraccount.columnconfigure(1, weight=1)
        self.frame_useraccount.columnconfigure(2, weight=1)
        self.frame_useraccount.columnconfigure(3, weight=1)
        self.frame_useraccount.columnconfigure(4, weight=0)
        self.frame_useraccount.columnconfigure(5, weight=1)
        self.frame_useraccount.columnconfigure(6, weight=1)

    def create_frame_systemmessage(self):
        self.frame_systemmessage = ttk.Frame(self.root)
        self.frame_systemmessage.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.frame_systemmessage.columnconfigure(0, weight=1)
        self.frame_systemmessage.columnconfigure(1, weight=2)

        tk.Label(self.frame_systemmessage, text="Systemnachricht: ").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.lbl_sysmessage = tk.Label(self.frame_systemmessage, text="-")
        self.lbl_sysmessage.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.system_messages = marketplace.systemmessages.SystemMessages(self.lbl_sysmessage)

    def create_frame_myauctions(self):
        self.frame_myauctions = ttk.Frame(self.frame_left)
        self.frame_myauctions.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.frame_myauctions.rowconfigure(1, weight=1)
        self.frame_myauctions.columnconfigure(0, weight=1)

        # Liste mit Auktionen
        tk.Label(self.frame_myauctions, text="Meine Auktionen").grid(row=0, column=0, columnspan=3, padx=5, pady=5,
                                                                     sticky="ew")
        self.item_listbox = tk.Listbox(self.frame_myauctions, width=110)
        self.item_listbox.grid(row=1, column=0, rowspan=7, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.item_listbox.bind('<<ListboxSelect>>', self.on_item_listbox_select)

        self.add_item_btn = tk.Button(self.frame_myauctions, text="Auktion hinzufügen", command=self.add_item_widget)
        self.add_item_btn.grid(row=1, column=4, padx=5, pady=5, sticky="ew")

        self.delete_item_btn = tk.Button(self.frame_myauctions, text="Auktion löschen", command=self.delete_item)
        self.delete_item_btn.grid(row=2, column=4, padx=5, pady=5, sticky="ew")

        self.view_option = tk.StringVar(value="offered")

        self.show_bids_radio = tk.Radiobutton(self.frame_myauctions, text="Meine Gebote", variable=self.view_option,
                                              value="bids",
                                              command=self.add_myitems2items_list)
        self.show_bids_radio.grid(row=9, column=0, padx=5, pady=5, sticky="nsew")

        self.show_won_items_radio = tk.Radiobutton(self.frame_myauctions, text="Gewonnene Auktionen",
                                                   variable=self.view_option,
                                                   value="won", command=self.add_myitems2items_list)
        self.show_won_items_radio.grid(row=9, column=1, padx=5, pady=5, sticky="nsew")

        self.show_offered_items_radio = tk.Radiobutton(self.frame_myauctions, text="Angebotene Artikel",
                                                       variable=self.view_option,
                                                       value="offered", command=self.add_myitems2items_list)
        self.show_offered_items_radio.grid(row=10, column=0, padx=5, pady=5, sticky="nsew")

        self.show_recommended_items_radio = tk.Radiobutton(self.frame_myauctions, text="Empfohlene Auktionen",
                                                           variable=self.view_option, value="recommended",
                                                           command=self.add_myitems2items_list)
        self.show_recommended_items_radio.grid(row=10, column=1, padx=5, pady=5, sticky="nsew")

        self.show_sold_items_radio = tk.Radiobutton(self.frame_myauctions, text="Verkaufte Artikel",
                                                    variable=self.view_option, value="sold",
                                                    command=self.add_myitems2items_list)
        self.show_sold_items_radio.grid(row=9, column=2, padx=5, pady=5, sticky="nsew")

    def create_frame_friends(self):
        self.frame_friends = ttk.Frame(self.frame_left)
        self.frame_friends.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.frame_friends.rowconfigure(1, weight=1)
        self.frame_friends.columnconfigure(0, weight=1)
        self.frame_friends.columnconfigure(1, weight=1)

        # Liste meiner Freunde
        tk.Label(self.frame_friends, text="Meine Freunde und Gruppenmitglieder", justify='left').grid(row=0, column=0,
                                                                                                      padx=5, pady=5,
                                                                                                      sticky="nsew")
        self.friends_listbox = tk.Listbox(self.frame_friends, width=50)
        self.friends_listbox.grid(row=1, column=0, rowspan=7, padx=5, pady=5, sticky="nsew")
        self.friends_listbox.bind('<<ListboxSelect>>', self.on_friends_listbox_select)

        self.btn_add_friend = tk.Button(self.frame_friends, text="Freund hinzufügen", command=self.add_friend)
        self.btn_add_friend.grid(row=1, column=4, padx=5, pady=5, sticky="nsew")

        self.remove_friend_btn = tk.Button(self.frame_friends, text="Freund entfernen", command=self.remove_friend)
        self.remove_friend_btn.grid(row=2, column=4, padx=5, pady=5, sticky="nsew")

        tk.Label(self.frame_friends, text="User mit denen meine Freunde befreundet sind").grid(row=0, column=1, padx=5,
                                                                                               pady=5, sticky="nsew")
        self.mutual_friends_listbox = tk.Listbox(self.frame_friends, width=50)
        self.mutual_friends_listbox.grid(row=1, column=1, rowspan=7, padx=5, pady=5, sticky="nsew")

    def create_frame_search_bid(self):
        # Frame to contain search and bid btn.
        self.frame_search_bid = ttk.Frame(self.root)
        self.frame_search_bid.grid(row=5, column=6, padx=5, pady=5, sticky="nsew")

        self.frame_search_bid.rowconfigure(2, weight=1)
        self.frame_search_bid.columnconfigure(0, weight=1)

        # Liste mit allen Artikeln und Suche
        self.search_entry = tk.Entry(self.frame_search_bid)
        self.search_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        # self.search_entry.insert(0, "Suchbegriff")
        self.search_entry.bind('<KeyRelease>', self.show_suggestions)

        self.search_btn = tk.Button(self.frame_search_bid, text="Suchen", command=self.search_items)
        self.search_btn.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Frame to contain the listbox and scrollbar.
        self.frame = ttk.Frame(self.frame_search_bid)
        self.frame.grid(row=2, column=0, rowspan=12, columnspan=12, padx=5, pady=5, sticky="nsew")
        # Create a scrollbar with vertical orientation.
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL)

        tk.Label(self.frame_search_bid, text="Alle Auktionen", justify='left').grid(row=0, column=0, columnspan=12,
                                                                                    padx=5, pady=5, sticky="ew")
        self.all_items_listbox = tk.Listbox(self.frame, width=140, height=30,
                                            yscrollcommand=self.scrollbar.set)
        # self.all_items_listbox.grid(row=6, column=6, rowspan=13, columnspan=6, padx=5, pady=5)
        # Bind the <<ListboxSelect>> event to the on_listbox_select function
        self.all_items_listbox.bind('<<ListboxSelect>>', self.on_listbox_select)
        # Link it to the listbox.
        self.scrollbar.config(command=self.all_items_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.all_items_listbox.pack()

    def create_frame_auction_detail(self, listbox="all_items"):
        if listbox == "all_items":
            selected = self.all_items_listbox.curselection()
        elif listbox == "item":
            selected = self.item_listbox.curselection()
        else:
            raise ValueError("listbox must be 'all_items' or 'item'")

        # Frame löschen, wenn er existiert
        if hasattr(self, 'frame_auction_detail'):
            for widget in self.frame_auction_detail.winfo_children():
                widget.destroy()
            self.frame_auction_detail.grid_forget()

        self.frame_auction_detail = ttk.Frame(self.frame_search_bid)
        self.frame_auction_detail.grid(row=14, column=0, rowspan=4, columnspan=12, padx=5, pady=5, sticky="nsew")

        if selected:
            if listbox == "all_items":
                auction_desc = self.all_items_listbox.get(selected)
            elif listbox == "item":
                auction_desc = self.item_listbox.get(selected)
            else:
                raise ValueError("listbox must be 'all_items' or 'item'")

            auction_id = marketplace.auction.Auction.get_id_from_pretty_print(auction_desc)

            # Auktion-ID
            auction_id_label = tk.Label(self.frame_auction_detail, text=f"Auktion-ID: {auction_id}")
            auction_id_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

            # Produktname
            item_name = self._auctions.get_item_name(auction_id)
            item_name_label = tk.Label(self.frame_auction_detail, text=f"Produktname: {item_name}")
            item_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

            # Produktbeschreibung
            item_description = self._auctions.get_item_description(auction_id)
            item_description_label = tk.Label(self.frame_auction_detail,
                                              text=f"Produktbeschreibung: {item_description}")
            item_description_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

            # Mindestgebot
            min_value = self._auctions.get_item_value_min(auction_id)
            min_value_label = tk.Label(self.frame_auction_detail, text=f"Mindestgebot: {min_value:.2f} €")
            min_value_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

            # Höchstes Gebot
            highest_bid = self._auctions.get_highest_bid(auction_id)
            highest_bid_label = tk.Label(self.frame_auction_detail, text=f"Höchstes Gebot: {highest_bid:.2f} €")
            highest_bid_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

            # Höchstbietender
            highest_bidder = self._auctions.get_highest_bidder(auction_id)
            highest_bidder_label = tk.Label(self.frame_auction_detail, text=f"Höchstbietender: {highest_bidder}")
            highest_bidder_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

            # Ende der Auktion in
            time_left = self._auctions.get_time_left(auction_id)
            time_left_label = tk.Label(self.frame_auction_detail, text=f"Ende der Auktion in: {time_left:.0f} s")
            time_left_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")

            # Verkäufer
            seller_id = self._auctions.get_seller_id(auction_id)
            seller_id_label = tk.Label(self.frame_auction_detail, text=f"Verkäufer: {seller_id}")
            seller_id_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

            self.bid_amount_entry = tk.Entry(self.frame_auction_detail)
            self.bid_amount_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
            self.bid_amount_entry.insert(0, "50")

            self.bid_btn = tk.Button(self.frame_auction_detail, text="Bieten", command=self.place_bid)
            self.bid_btn.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

    def create_widgets(self):
        self.create_frame_systemmessage()

        self.create_frame_useraccount()

        self.root.rowconfigure(5, weight=1)
        self.root.columnconfigure(6, weight=1)

        # placeholder
        # tk.Label(self.root, text="     ").grid(row=4, column=2, padx=5, pady=5)

        self.frame_left = ttk.Frame(self.root)
        self.frame_left.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

        self.frame_left.rowconfigure(0, weight=1)
        self.frame_left.columnconfigure(0, weight=1)

        self.create_frame_myauctions()

        self.create_frame_friends()

        self.create_frame_search_bid()

        self.create_frame_auction_detail()

    # *** FUNCTION HANDLES invoked by tk widget items ***

    def add_myitems2items_list(self):
        self.item_listbox.delete(0, tk.END)
        value = self.view_option.get()

        user_id = self._current_user.id()
        user_id_pass = None

        if value == 'offered':
            auctions = self._auctions.get_auctions_offered(user_id)
        elif value == 'won':
            auctions = self._auctions.get_auctions_won(user_id)
        elif value == 'bids':
            auctions = self._auctions.get_auctions_bid_in(user_id)
            user_id_pass = user_id
        elif value == 'recommended':
            auctions = self._auctions.get_auctions_is_recommended(user_id)
        elif value == 'sold':
            auctions = self._auctions.get_auctions_sold(user_id)
        else:
            auctions = []

        for auction_id in auctions:
            self.item_listbox.insert(tk.END, self._auctions[auction_id].pretty_print(False, user_id_pass))

    def on_listbox_select(self, event):
        self.create_frame_auction_detail(listbox="all_items")

    def on_friends_listbox_select(self, event):
        # Get the selected index 
        selected_index = self.friends_listbox.curselection()
        if selected_index:
            self.remove_friend_btn.config(state=tk.NORMAL)
        else:
            self.remove_friend_btn.config(state=tk.DISABLED)

    def on_item_listbox_select(self, event):
        # Get the selected index
        selected_index = self.item_listbox.curselection()
        value = self.view_option.get()

        if selected_index and value == 'offered':
            self.delete_item_btn.config(state=tk.NORMAL)
        elif selected_index and value == 'bids':
            self.create_frame_auction_detail(listbox="item")
        elif selected_index and value == 'recommended':
            self.create_frame_auction_detail(listbox="item")
        else:
            self.delete_item_btn.config(state=tk.DISABLED)

    def my_account(self):
        if self._current_user:
            account_info = tk.Toplevel(self.root)
            account_info.title("Mein Account")

            tk.Label(account_info, text="Nutzername:").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
            tk.Label(account_info, text=self._current_user.name()).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

            tk.Label(account_info, text="Passwort:").grid(row=1, column=0, padx=5, pady=5, sticky="ew")
            tk.Label(account_info, text=self._current_user.password()).grid(row=1, column=1, padx=5, pady=5,
                                                                            sticky="ew")

            tk.Label(account_info, text="ID:").grid(row=2, column=0, padx=5, pady=5, sticky="ew")
            tk.Label(account_info, text=self._current_user.id()).grid(row=2, column=1, padx=5, pady=5, sticky="ew")

            tk.Label(account_info, text="Budget:").grid(row=3, column=0, padx=5, pady=5, sticky="ew")
            tk.Label(account_info, text=f"{self._current_user.balance():.2f} €").grid(row=3, column=1, padx=5, pady=5,
                                                                                      sticky="ew")
        else:
            messagebox.showerror("Fehler", "Kein Nutzer eingeloggt")

    def login(self):
        userid = self.username_entry.get()
        password = self.password_entry.get()

        if userid in self._users and self._users.password_valid(userid, password):
            self._current_user = self._users.get(userid)

            self.system_messages.push("Erfolgreich eingeloggt.")

            self._auctions.start_simulation_init(userid)

            self.update_lists()
            self.enable_widgets()
        else:
            messagebox.showerror("Login Fehler", "Ungültiger Benutzername oder Passwort")

    def register(self):
        userid = self.username_entry.get()
        password = self.password_entry.get()

        if userid not in self._users:
            self._users.add(userid, password)
            messagebox.showinfo("Erfolg",
                                f"Registrierung des Nutzers {userid} erfolgreich! Loggen Sie sich bitte ein.")
        else:
            messagebox.showerror("Fehler", f"Benutzername {userid} bereits vergeben")

    def add_friend(self):
        friend_id = AuctionAppInit.simple_input("Freund hinzufügen", "GM-ID des Nutzers:")
        if friend_id:
            friend = self._users.get_user_pretty_print_for_list(friend_id)
            self._current_user.friends_add(friend_id)
            self.friends_listbox.insert(tk.END, friend)

            self._auctions.get_auctions_friends_offer(self._current_user.id())
            self._auctions.get_auctions_friends_bid_in(self._current_user.id())

    def remove_friend(self):
        selected_friend_index = self.friends_listbox.curselection()
        if selected_friend_index:
            friend_name = self.friends_listbox.get(selected_friend_index)

            friend_id = marketplace.user.User.get_id_from_pretty_print(friend_name)

            # lösche Freund nur, wenn er ein Freund ist. da in der Liste auch Gruppenmitglieder sind, die nicht
            # unbedingt auch Freunde sein müssen
            if self._current_user.is_friend(friend_id):
                # freund aus freundesliste von _current_user löschen
                success = self._current_user.friends_delete(friend_id)

                self.friends_listbox.delete(selected_friend_index)

                self._auctions.get_auctions_friends_offer(self._current_user.id())
                self._auctions.get_auctions_friends_bid_in(self._current_user.id())

    def search_items(self):
        search_term = self.search_entry.get()

        # wieder alle Auktionen anzeigen
        self.add_items2all_items_list()
        
        if search_term == "":
            return

        results = [item for item in self.all_items_listbox.get(0, tk.END) if search_term.lower() in item.lower()]
        self.all_items_listbox.delete(0, tk.END)
        for item in results:
            self.all_items_listbox.insert(tk.END, item)
        self.hide_tooltip()

    def add_item_widget(self):
        new_item_widget = tk.Toplevel(self.root)
        new_item_widget.title("Artikel hinzufügen")

        tk.Label(new_item_widget, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.new_article_name = tk.Entry(new_item_widget)
        self.new_article_name.grid(row=0, column=1, padx=5, pady=5)
        self.new_article_name.insert(0, "Produktname")

        tk.Label(new_item_widget, text="Beschreibung:").grid(row=1, column=0, padx=5, pady=5)
        self.new_article_description = tk.Entry(new_item_widget)
        self.new_article_description.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(new_item_widget, text="Mindestgebot (€):").grid(row=2, column=0, padx=5, pady=5)
        self.new_min_value = tk.Entry(new_item_widget)
        self.new_min_value.grid(row=2, column=1, padx=5, pady=5)
        self.new_min_value.insert(0, "1")

        ok_button = tk.Button(new_item_widget, text="OK", command=lambda: self.add_new_auction(new_item_widget))
        ok_button.grid(row=3, column=0, columnspan=2, pady=10)

    def delete_item(self):
        selected = self.item_listbox.curselection()
        if selected:
            auction_desc = self.item_listbox.get(selected)
            auction_id = marketplace.auction.Auction.get_id_from_pretty_print(auction_desc)

            success = self._auctions.delete(auction_id)

            if success:
                self.item_listbox.delete(selected)

                index = self.search_auction_id_in_all_items_listbox(auction_id)
                # index = self.all_items_listbox.get(0, tk.END).index(auction_desc)
                self.all_items_listbox.delete(index)

                self.system_messages.push("Auktion erfolgreich gelöscht.")
            else:
                self.system_messages.push("Auktion darf nicht gelöscht werden, da User darauf bieten.")

    def place_bid(self):
        bid_amount = self.bid_amount_entry.get()
        selected = self.all_items_listbox.curselection()
        value = self.view_option.get()
        is_all_items_listbox = True

        # habe len(selected) == 0 ergänzt, da selected ein leeres tuple ist, wenn in all_items_listbox nichts
        # selektiert ist
        if (selected is None or len(selected) == 0) and (value == 'recommended' or value == 'bids'):
            selected = self.item_listbox.curselection()
            is_all_items_listbox = False

        if bid_amount and selected:
            if is_all_items_listbox:
                auction_desc = self.all_items_listbox.get(selected)
            else:
                auction_desc = self.item_listbox.get(selected)

            auction_id = marketplace.auction.Auction.get_id_from_pretty_print(auction_desc)
            success = self._auctions.bid_in_auction(auction_id, self._current_user, float(bid_amount))

            if not success:
                messagebox.showerror("Fehler",
                                     "Nicht genügend Guthaben oder Ihr Gebot ist unter dem Mindestgebot")
            else:
                self.update_listbox_item(selected, auction_id)
                self.system_messages.push("Gebot erfolgreich abgegeben für {0}.".format(
                    self._auctions[auction_id].get_item_name()))
        else:
            print('place_bid fails: ', bid_amount, selected, is_all_items_listbox, value)
# VERÄNDERT
    def show_suggestions(self, event):
        search_text = self.search_entry.get()
        if search_text:
            #suggestions = self.trie.search(search_text)
            avl_suggestions = self.avl_tree.find_most_likely_words(search_text)
            self.show_tooltip(avl_suggestions)
        else:
            self.hide_tooltip()

    def on_select(self, event):
        selected = event.widget.get(event.widget.curselection())
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, selected)
        self.hide_tooltip()

    def logout(self):
        self._current_user = None
        self.enable_widgets(False)

    # *** PRIVATE METHODS ***

    def enable_widgets(self, enable=True):
        widgets = [
            self.add_item_btn, self.delete_item_btn, self.show_bids_radio,
            self.show_won_items_radio, self.show_offered_items_radio, self.show_recommended_items_radio,
            self.friends_listbox, self.btn_add_friend, self.remove_friend_btn,
            self.search_entry, self.search_btn, self.all_items_listbox,
            self.logout_btn, self.account_btn, self.show_sold_items_radio
        ]
        for widget in widgets:
            # bid_btn is set to NORMAL in method on_listbox_select below
            if (enable and widget is not self.remove_friend_btn
                    and widget is not self.delete_item_btn):
                widget.config(state=tk.NORMAL)
            else:
                widget.config(state=tk.DISABLED)

    def update_lists(self):
        self.add_myitems2items_list()

        self.add_myfriends2friends_list()
        self.add_users2mutualfriends_list()

    def add_myfriends2friends_list(self):
        self.friends_listbox.delete(0, tk.END)

        friends = self._users.get_friends_andgroupmembers_pretty_print(self._current_user.id())

        self.friends_listbox.insert(0, *friends)

        self._auctions.get_auctions_friends_offer(self._current_user.id())
        self._auctions.get_auctions_friends_bid_in(self._current_user.id())

    def add_users2mutualfriends_list(self):
        self.mutual_friends_listbox.delete(0, tk.END)

        mutual_friends = self._users.suggest_friends(self._current_user.id(), 3)

        self.mutual_friends_listbox.insert(0, *mutual_friends)

    def update_listbox_item(self, selected_index, auction_id):
        # Get the selected index
        if selected_index:
            # Get the new value from the user
            new_value = self._auctions[auction_id].pretty_print()
            if new_value:
                # Delete the old entry
                self.all_items_listbox.delete(selected_index)
                # Insert the new entry at the same position
                self.all_items_listbox.insert(selected_index, new_value)

    def add_items2all_items_list(self):
        # speichern welches Element in der Liste ausgewählt war, damit es auch am Ende der
        # Funktion wieder ausgewählt werden kann
        selected_index = self.all_items_listbox.curselection()
        if selected_index:
            auction_desc = self.all_items_listbox.get(selected_index)

            auction_id_before = marketplace.auction.Auction.get_id_from_pretty_print(auction_desc)
        else:
            auction_id_before = None

        # alle Elemente in Liste löschen und Auktionen die nicht ausgelaufen sind, wieder
        # in liste einfügen
        self.all_items_listbox.delete(0, tk.END)

        for auction_id, auction in self._auctions.items():
            if not auction.expired():
                self.all_items_listbox.insert(tk.END, auction.pretty_print())

        # wenn vor dem Löschvorgang ein Element in der Liste ausgewählt war, dieses wieder auswählen,
        # wenn Element noch in Liste existiert
        if auction_id_before:
            self.search_auction_id_in_all_items_listbox(auction_id_before)

    def search_auction_id_in_all_items_listbox(self, auction_id_searching):
        item = None

        for item in range(self.all_items_listbox.size()):
            auction_desc = self.all_items_listbox.get(item)

            auction_id = marketplace.auction.Auction.get_id_from_pretty_print(auction_desc)

            if auction_id == auction_id_searching:
                self.all_items_listbox.select_set(item)
                break

        return item

    def add_new_auction(self, widget):
        item_name = self.new_article_name.get()
        description = self.new_article_description.get()
        value_min = self.new_min_value.get()

        user_id = self._current_user.id()

        # Aufrufen der Methode add_new_auction der Auktionsklasse
        auction = self._auctions.add_new_auction(user_id, item_name, description, value_min)

        if self.view_option.get() == 'offered':
            self.item_listbox.insert(tk.END, auction.pretty_print(False))
        self.all_items_listbox.insert(tk.END, auction.pretty_print())

        self.system_messages.push("Neue Auktion erfolgreich erstellt.")

        # Schließen des Fensters
        widget.destroy()

    # *** TRIE: für Autovervollständigung bei Suche nach Produkten in Liste ***


    # BEARBEITET
    def initialize_trie(self):
        # Holen Sie sich alle Produktnamen von den Auktionen
        product_names = self._auctions.get_all_item_names()

        # Holen Sie sich alle Nutzer-IDs aus der Benutzerdatenbank
        user_ids = self._users.all_user_ids()  # Diese Methode muss implementiert sein und alle User-IDs zurückgeben

        # Kombinieren Sie die Listen von Produktnamen und Nutzer-IDs
        combined_entries = product_names + user_ids

        # Zählen Sie die Häufigkeit der kombinierten Einträge, um doppelte Einträge zu verwalten
        counter = Counter(combined_entries)
        tuple_list = list(counter.items())

        # Fügen Sie jeden Eintrag sowohl in den Trie als auch in den AVL-Baum ein
        for entry, count in tuple_list:
            self.trie.insert(entry)  # Fügt den Eintrag (Produktname oder Nutzer-ID) in das Trie ein
            self.avl_tree.insert(entry, count)  # Fügt den Eintrag in den AVL-Baum ein mit Häufigkeit

    def show_tooltip(self, suggestions):
        if self.tooltip:
            self.tooltip.destroy()

        # Calculate the height and width of the Listbox based on content
        max_height = 10  # Maximum number of items to show before adding a scrollbar
        num_items = min(len(suggestions), max_height)  # Limit the number of visible items

        if num_items > 0:
            # Create a new tooltip window
            self.tooltip = tk.Toplevel(self.root)
            self.tooltip.wm_overrideredirect(True)  # Remove window decorations

            # Calculate the position to display the tooltip
            x, y, _, _ = self.search_entry.bbox("insert")
            x += self.search_entry.winfo_rootx()
            y += self.search_entry.winfo_rooty() + 25
            self.tooltip.geometry(f"+{x}+{y}")  # Set initial position

            # Create the Listbox for suggestions
            listbox = tk.Listbox(self.tooltip)
            listbox.pack()

            # Add suggestions to the Listbox
            for suggestion in suggestions:
                listbox.insert(tk.END, suggestion)

            listbox.bind("<<ListboxSelect>>", self.on_select)

            # Determine the maximum width needed for the suggestions
            max_width = max(len(s) for s in suggestions) + 2  # Add padding to width

            # Set height and width of the Listbox to accommodate the suggestions
            listbox.config(height=num_items, width=max_width)
            listbox.update_idletasks()  # Update Listbox geometry calculations

            # Correctly calculate width and height of the Listbox after updates
            width = listbox.winfo_reqwidth()  # Use winfo_reqwidth() to get requested width
            height = listbox.winfo_reqheight()  # Use winfo_reqheight() to get requested height

            # Update tooltip size based on Listbox size
            self.tooltip.geometry(f"{width}x{height}+{x}+{y}")

    def hide_tooltip(self):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

    def update_tooltip_position(self, event):
        """Update tooltip position when the window is moved or resized."""
        if self.tooltip:
            x, y, _, _ = self.search_entry.bbox("insert")
            x += self.search_entry.winfo_rootx()
            y += self.search_entry.winfo_rooty() + 25
            self.tooltip.geometry(f"+{x}+{y}")

    # *** PRIVATE STATIC METHODS ***

    def _on_closing(self):
        """Handle the window close event to clean up threads and resources."""

        # Signal the thread to stop
        self._auctions.stop_simulation()

        self.root.destroy()

    @staticmethod
    def simple_input(title, prompt):
        return simpledialog.askstring(title, prompt)
