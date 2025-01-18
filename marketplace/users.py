# Status: FINAL, dgaida2, 15.10.2024

# definiert die Klasse Users.
# Users ist eine Menge von disjunkten Mengen (nur für drittes Praktikum) von der Klasse User,
# damit man Users in Praktikumsgruppen einsortieren kann. Für das erste und zweite Praktikum ist die Klasse
# Praktikumsgruppe lediglich ein Dictionary
# in der Klasse werden die csv-Dateien user.csv und friends.csv gelesen.

import csv
import marketplace.user
import marketplace.praktikumsgruppen
from typing import List
from marketplace.distance_calculator import DistanceCalculator


class Users(marketplace.praktikumsgruppen.Praktikumsgruppen):
    # *** CONSTRUCTORS ***
    def __init__(self, csvfile, *args):
        super().__init__()

        self._read_users_from_csvfile(csvfile)

        self._read_friends_csv('friends.csv')

        # erstelle Praktikumsgruppen als Menge disjunkter Mengen bzw. als dictionary (1. und 2. Praktikum)
        super().create_groups(list(self.keys()), self._groupnumbers)

    # *** PUBLIC SET methods ***

    # *** PUBLIC methods ***

    def add(self, user_id, password, name_family="", name_first="", gps_coord=(None, None), address=""):
        """
        Adds the given user with the user_id to the dictionary that the Users parent class Praktikumsgruppen is
        inheriting from
        :param user_id: user id of user
        :param password: password of user
        :param name_family: family name of user
        :param name_first: first name of user
        :param gps_coord: Tuple with Längen- und Breitengrad des erfundenen Wohnorts des Nutzers
        :param address: String mit Adresse die zu GPS Koordinaten gehört
        """
        self[user_id] = marketplace.user.User(user_id, password, name_family, name_first, gps_coord, address)

    def calc_distance_between_users(self, user_id1, user_id2):
        # TODO for students: calculate distance between gps coordinates of user1 and user2 using a map and an
        #  algorithm that calculates the shortest distance on the map

        user1 = self[user_id1]
        user2 = self[user_id2]

        # TODO for students: replace this naive implementation of distance manhattan with distance gotten
        #  from graph algorithm
        distance = sum(abs(a - b) for a, b in zip(user1.gps_coords(), user2.gps_coords()))

        return distance

    # *** PUBLIC GET methods ***

    def get_name_of_user(self, user_id):
        node = self[user_id]
        return node.name()

    def num_users(self):
        return len(self.keys())

    def password_valid(self, user_id, password):
        return self[user_id].password_valid(password)

    def get_user_pretty_print_for_list(self, user_id):
        return (self[user_id].pretty_print() + "\t in Praktikumsgruppe repräsentiert durch: " +
               (self.find_byid(user_id, True)))

    def get_friends_andgroupmembers_pretty_print(self, user_id):
        """
        Returns list of friends and group members for the given user_id that is shown on GUI.

        :param user_id: usually the current user id
        :return:
        """
        friends = self[user_id].friends()

        friend_names = [self.get_user_pretty_print_for_list(friend) for friend in friends]

        group_members = self.get_groupmembers(user_id)
        
        if group_members is None:
            return friend_names

        # entferne mich selbst aus der Gruppe, da ich ja weiß, dass ich (user_id) in der Gruppe bin
        group_members.remove(user_id)

        group_members_pp = [self.get_user_pretty_print_for_list(member) for member in group_members]

        return friend_names + group_members_pp

    def get_mutual_friends(self, user_id):
        """

        :param user_id: usually the current user id
        :return: dictionary with friends of the friends of given user_id together with the information with how
        many friends of user_id these friends are friends with
        """
        friends = self[user_id].friends()
        mutual_friends_count = {}

        for friend in friends:
            friend_friends = self[friend].friends()
            for mutual_friend in friend_friends:
                if mutual_friend != user_id and mutual_friend not in friends:
                    if mutual_friend in mutual_friends_count:
                        mutual_friends_count[mutual_friend] += 1
                    else:
                        mutual_friends_count[mutual_friend] = 1

        return mutual_friends_count

    def suggest_friends(self, user_id, num_common_friends=2, distance_threshold=0.1, pretty_print=True):
        """
        Suggests friends for a given user based on:
        1. Users who share at least num_common_friends mutual friends.
        2. Users who are geographically close within distance_threshold.

        :param user_id: ID of the user to suggest friends for.
        :param num_common_friends: Minimum number of mutual friends for suggestions.
        :param distance_threshold: Maximum distance for geographic suggestions.
        :param pretty_print: If True, returns pretty-printed user details.
        :return: List of suggested friend user IDs or pretty-printed details.
        """
        if user_id not in self:
            raise ValueError("User ID not found in the user list.")

        #Gemeinsame Freunde analysieren
        mutual_friends_count = self.get_mutual_friends(user_id)
        suggested_by_friends = [
            (friend_id, count) for friend_id, count in mutual_friends_count.items()
            if count >= num_common_friends
        ]
        suggested_by_friends.sort(key=lambda x: x[1], reverse=True)  # Sortiere nach Anzahl gemeinsamer Freunde

        #Geografische Nähe analysieren
        user_location = self[user_id].gps_coords()
        suggested_by_distance = []
        for other_user_id in self.all_user_ids():
            if other_user_id != user_id and other_user_id not in self[user_id].friends():
                distance = self.calc_distance_between_users(user_id, other_user_id)
                if distance <= distance_threshold:
                    suggested_by_distance.append((other_user_id, distance))
        suggested_by_distance.sort(key=lambda x: x[1])  # Sortiere nach Distanz (nächster zuerst)

        #Kombiniere die beiden Listen, ohne Duplikate
        suggested_friends = []
        suggested_friends.extend([friend_id for friend_id, _ in suggested_by_friends])
        suggested_friends.extend([
            friend_id for friend_id, _ in suggested_by_distance
            if friend_id not in suggested_friends
        ])

        #Pretty-Print (optional)
        if pretty_print:
            return [self[friend_id].pretty_print() for friend_id in suggested_friends]

        return suggested_friends

    def are_users_connected(self, user_id1, user_id2, degree=3):
        """
        Überprüft, ob zwei Benutzer bis zu einem bestimmten Grad über das Freundesnetzwerk verbunden sind.

        :param user_id1: ID des ersten Benutzers.
        :param user_id2: ID des zweiten Benutzers.
        :param degree: Maximale Anzahl von Verbindungsebenen.
        :return: True, wenn die Benutzer verbunden sind, sonst False.
        """
        if user_id1 not in self or user_id2 not in self:
            raise ValueError("Einer oder beide Benutzer existieren nicht im Netzwerk.")

        if user_id1 == user_id2:
            return True  # Ein Benutzer ist immer mit sich selbst verbunden

        from collections import deque

        # BFS (Breadth-First Search) für die Suche
        queue = deque([(user_id1, 0)])  # Starte mit dem ersten Benutzer, Grad 0
        visited = set()  # Vermeide doppelte Besuche

        while queue:
            current_user, current_degree = queue.popleft()

            # Wenn der maximale Grad überschritten ist, breche ab
            if current_degree >= degree:
                continue

            friends = self[current_user].friends()

            for friend in friends:
                if friend == user_id2:
                    return True  # Verbindung gefunden
                if friend not in visited:
                    visited.add(friend)
                    queue.append((friend, current_degree + 1))  # Erhöhe den Grad um 1

        return False  # Keine Verbindung gefunden

    # HINZUGEFÜGT
    def all_user_ids(self):
        """Gibt eine Liste aller Nutzer-IDs zurück."""
        return list(self.keys())

    # *** PUBLIC STATIC methods ***

    # *** PRIVATE methods ***

    def _read_users_from_csvfile(self, csvfile):
        """
        Read the given csvfile that contains all students that want to do the Praktikum in this semester
        including their GM-ID, Names and number of their Praktikumsgruppe

        :param csvfile: csv file that has to be created at the beginning of the semester containing all students
        in this semester
        """
        with open(csvfile, newline='', encoding='utf-8-sig') as csvfile:
            csvreader = csv.reader(csvfile)
            # Skip header row
            next(csvreader)

            # private member variable containing the Praktikumsgruppe number of the students in the order that the
            # students are read from the csv file
            self._groupnumbers = []

            for row in csvreader:
                user_id, name_family, name_first, password, groupnum, gps_coords, address = row
                # macht aus String wieder das Tuple mit long und lat Koordinaten
                gps_coords = eval(gps_coords)
                self.add(user_id, password, name_family, name_first, gps_coords, address)
                self._groupnumbers.append(groupnum)

    def _read_friends_csv(self, file_path):
        """
        Funktion, um die friends.csv-Datei einzulesen und ein Dictionary zu erstellen
        :param file_path: path to friends.csv file
        """
        with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Überspringe die Header-Zeile
            for row in csvreader:
                user_id = row[0]
                friends = row[1].split(', ')
                self[user_id].friends_add_list(friends)
                for friend in friends:  # gehe alle Freunde durch und füge user_id ebenfalls als Freund hinzu
                    self[friend].friends_add(user_id)

    def get_friend_recommendations(self, user_id: str) -> List[str]:
        if not hasattr(self, '_distance_calculator'):
            self._distance_calculator = DistanceCalculator()
        return self._distance_calculator.find_nearby_friends_of_friends(user_id, self)
    # *** PUBLIC methods to return class properties ***

    # *** PRIVATE variables ***
