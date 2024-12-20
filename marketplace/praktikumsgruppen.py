# Definiert die Klassen Praktikumsgruppen und SetNode, implementiert als Dictionary


class SetNode:
    """
    TODO for students: die Klasse user.User erbt von SetNode. diese Klasse wird eigentlich erst in Praktikum 3 benötigt.
    für Praktikum 1 und 2 müsste User nicht von dieser Klasse erben
    Class representing a node in a disjoint set (union-find) structure.

    Attributes:
        _parent (SetNode): The parent node in the union-find structure.
        _weight (int): The weight (number of nodes) of the (sub-)tree rooted in the current node.
    """

    # *** CONSTRUCTORS ***
    def __init__(self):
        """
        Initializes a new SetNode.
        """
        # TODO: werden nur für Praktikum 3 benötigt
        self._parent = self  # parent Knoten des SetNode Objekts. self bedeutet, dass der Knoten ein Wurzelknoten ist
        self._weight = 1  # Gewicht (Anzahl Knoten) des (Teil-)Baumes, der in dem SetNode Objekt verwurzelt ist

    # *** PUBLIC SET methods ***

    # TODO: implementieren Sie in Praktikum 3 die benötigten Methoden

    # *** PUBLIC methods to return class properties ***

    # TODO: implementieren Sie in Praktikum 3 die benötigten Methoden

# Definiert die Klassen Praktikumsgruppen und SetNode, implementiert als Dictionary


class SetNode:
    """
    TODO for students: die Klasse user.User erbt von SetNode. diese Klasse wird eigentlich erst in Praktikum 3 benötigt.
    für Praktikum 1 und 2 müsste User nicht von dieser Klasse erben
    Class representing a node in a disjoint set (union-find) structure.

    Attributes:
        _parent (SetNode): The parent node in the union-find structure.
        _weight (int): The weight (number of nodes) of the (sub-)tree rooted in the current node.
    """

    # *** CONSTRUCTORS ***
    def __init__(self):
        """
        Initializes a new SetNode.
        """
        # TODO: werden nur für Praktikum 3 benötigt
        self._parent = self  # parent Knoten des SetNode Objekts. self bedeutet, dass der Knoten ein Wurzelknoten ist
        self._weight = 1  # Gewicht (Anzahl Knoten) des (Teil-)Baumes, der in dem SetNode Objekt verwurzelt ist

    # *** PUBLIC SET methods ***

    # TODO: implementieren Sie in Praktikum 3 die benötigten Methoden

    # *** PUBLIC methods to return class properties ***

    # TODO: implementieren Sie in Praktikum 3 die benötigten Methoden


class Praktikumsgruppen(dict):
    """
    In Praktikum 1 und 2: Dictionary containing all students. Die Klasse user.Users erbt von dieser Klasse.
    In Praktikum 3: Class representing a collection of disjoint sets for grouping users into practical groups.

    Methods:
        find(node): Finds the root of the set containing the node, with path compression.
        find_byid(user_id, return_id=False): Finds the root of the set containing the user by ID.
        union(user_id1, user_id2): Unions the sets containing the two users.
        create_groups(user_ids, groupnumbers): Creates groups from the provided user IDs and group numbers.
        get_groupmembers(user_id): Gets the members of the group containing the user.
        print_ds(): Prints the disjoint set structure.
    """

    # *** CONSTRUCTORS ***
    def __init__(self):
        """
        Initializes a new Praktikumsgruppen object.
        """
        super().__init__()

    # *** PUBLIC methods ***

    # TODO in Praktikum 3: implement find(node), find_byid(user_id, return_id=False) and
    #  union(user_id1, user_id2)

    # die Methode existiert nur aus Kompatibilitätsgründen und wird im 3. Praktikum implementiert
    def find_byid(self, user_id, return_id=False):
        """
        Finds the root of the set (Praktikumsgruppe) containing the user by ID.

        Args:
            user_id (str): The ID of the user.
            return_id (bool): Whether to return the ID of the root node (True) or the root node itself (False, default).

        Returns:
            SetNode or str: The root node or its ID, depending on return_id.
        """
        if user_id not in self:
            raise ValueError(f"Benutzer-ID {user_id} wurde nicht gefunden.")

            # Return the user object or ID
        return self[user_id] if not return_id else user_id

        #return user_id

    def create_groups(self, user_ids, groupnumbers):
        """
        Creates groups from the provided user IDs and group numbers.

        Args:
            user_ids (list): A list of user IDs.
            groupnumbers (list): A list of group numbers corresponding to the user IDs.
        """
        # TODO: implement in Praktikum 1
        #pass
        if len(user_ids) != len(groupnumbers):
            raise ValueError("Die Länge von user_ids und groupnumbers muss übereinstimmen.")

        for user_id, group_number in zip(user_ids, groupnumbers):
            # Hole das Benutzerobjekt anhand der ID
            user_obj = self.find_byid(user_id, return_id=False)

            # Verknüpfen Sie das Benutzerobjekt mit der Gruppennummer
            self[user_obj] = group_number



    # *** PUBLIC GET methods ***

    def get_groupmembers(self, user_id):
        """
        Gets the members of the group containing the user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            list: A list of user IDs in the same group.

        Raises:
            ValueError: If the user_id is not found in any group.
        """
        if user_id not in self:
            raise ValueError(f"Benutzer-ID {user_id} wurde keiner Gruppe zugeordnet.")

        # Gruppennummer des Benutzers abrufen
        user_group_number = self[user_id]

        # Benutzer der gleichen Gruppe aus der group_map zurückgeben
        return [uid for uid, group_number in self.items() if group_number == user_group_number]

    # *** PUBLIC STATIC methods ***

    # *** PRIVATE methods ***

    # *** PUBLIC methods to return class properties ***

    # *** PRIVATE variables ***

class Praktikumsgruppen(dict):
    """
    In Praktikum 1 und 2: Dictionary containing all students. Die Klasse user.Users erbt von dieser Klasse.
    In Praktikum 3: Class representing a collection of disjoint sets for grouping users into practical groups.

    Methods:
        find(node): Finds the root of the set containing the node, with path compression.
        find_byid(user_id, return_id=False): Finds the root of the set containing the user by ID.
        union(user_id1, user_id2): Unions the sets containing the two users.
        create_groups(user_ids, groupnumbers): Creates groups from the provided user IDs and group numbers.
        get_groupmembers(user_id): Gets the members of the group containing the user.
        print_ds(): Prints the disjoint set structure.
    """

    # *** CONSTRUCTORS ***
    def __init__(self):
        """
        Initializes a new Praktikumsgruppen object.
        """
        super().__init__()

    # *** PUBLIC methods ***

    # TODO in Praktikum 3: implement find(node), find_byid(user_id, return_id=False) and
    #  union(user_id1, user_id2)

    # die Methode existiert nur aus Kompatibilitätsgründen und wird im 3. Praktikum implementiert
    def find_byid(self, user_id, return_id=False):
        """
        Finds the root of the set (Praktikumsgruppe) containing the user by ID.

        Args:
            user_id (str): The ID of the user.
            return_id (bool): Whether to return the ID of the root node (True) or the root node itself (False, default).

        Returns:
            SetNode or str: The root node or its ID, depending on return_id.
        """

        return user_id

    def create_groups(self, user_ids, groupnumbers):
        """
        Creates groups from the provided user IDs and group numbers.

        Args:
            user_ids (list): A list of user IDs.
            groupnumbers (list): A list of group numbers corresponding to the user IDs.
        """
        # TODO: implement in Praktikum 1
        #pass



    # *** PUBLIC GET methods ***

    def get_groupmembers(self, user_id):
        """
        Gets the members of the group containing the user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            list: A list of user IDs in the same group.

        Raises:
            ValueError: If the user_id is not found in any group.
        """
        if user_id not in self:
            raise ValueError(f"Benutzer-ID {user_id} wurde keiner Gruppe zugeordnet.")

        # Gruppennummer des Benutzers abrufen
        user_group_number = self[user_id]

        # Benutzer der gleichen Gruppe aus der group_map zurückgeben
        return [uid for uid, group_number in self.items() if group_number == user_group_number]

    # *** PUBLIC STATIC methods ***

    # *** PRIVATE methods ***

    # *** PUBLIC methods to return class properties ***

    # *** PRIVATE variables ***
