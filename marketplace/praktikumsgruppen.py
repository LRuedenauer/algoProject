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
        self._weight = 1  # Gewicht (Anzahl Knoten) des (Teil-)Baumes, der in dem SetNode Objekt verwurzelt ist, ist am Anfang immer 1

    # *** PUBLIC SET methods ***

    # TODO: implementieren Sie in Praktikum 3 die benötigten Methoden
    # hinzugefügt braucht man, weil ist sonst eine private Eigenschaft

    def get_parent(self):
        return self._parent


    def get_weight(self):
        return self._weight

    # *** PUBLIC methods to return class properties ***

    # TODO: implementieren Sie in Praktikum 3 die benötigten Methoden
    #hinzugefügt braucht man, weil ist sonst eine private Eigenschaft

    def set_parent(self, value):
        self._parent = value

    def set_weight(self, value):
        self._weight = value

# Definiert die Klassen Praktikumsgruppen und SetNode, implementiert als Dictionary


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

    # hinzugefügt
    def find(self, node):
        """
        Findet die Wurzel des Knotens und wendet Pfadverkürzung an,
        um die Struktur zu optimieren.

        Args:
            node (SetNode): Der zu suchende Knoten.

        Returns:
            SetNode: Die Wurzel des Baums, zu dem der Knoten gehört.
        """
        # Wenn der Knoten ungleich des Parent Knoten ist
        if node != node.get_parent():
            # Rekursive Suche mit Pfadverkürzung
            root = self.find(node.get_parent())
            node.set_parent(root)
        return node

    # die Methode existiert nur aus Kompatibilitätsgründen und wird im 3. Praktikum implementiert
    # hinzugefügt
    def find_byid(self, user_id, return_id=False):
        """
        Finds the root of the set (Praktikumsgruppe) containing the user by ID.

        Args:
            user_id (str): The ID of the user.
            return_id (bool): Whether to return the ID of the root node (True) or the root node itself (False, default).

        Returns:
            SetNode or str: The root node or its ID, depending on return_id.
        """
        user = self[user_id] # SetNode-Objekt abrufen
        root = self.find(user) # Root-Knoten finden

        if return_id:           # true
            return root.id()    # user id des Wurzelknotens (root) wird zurückgegeben
        else:
            return root         # der gesamte Wurzelknoten wird zurückgegeben

    # hinzugefügt
    def union(self, user_id1, user_id2):
        """
        Vereint die Mengen, die die Benutzer mit den angegebenen IDs enthalten.
        Verwendet Gewichtung, um den kleineren Baum unter den größeren zu hängen.

        Args:
            user_id1 (str): Die ID des ersten Benutzers.
            user_id2 (str): Die ID des zweiten Benutzers.
        """
        # Sicherstellen, dass beide Benutzer-IDs existieren
        if user_id1 not in self or user_id2 not in self:
            raise ValueError("Beide Benutzer-IDs müssen existieren.")

        # `find_byid` verwenden, um die Wurzeln der Mengen zu finden
        root1 = self.find_byid(user_id1)
        root2 = self.find_byid(user_id2)

        # Wenn root1 und root2 gleich sind, wird abgebrochen
        if root1 == root2:
            return

        # Wenn root1 mehr Gewicht hat, root2 unter root1 hängen
        # Andernfalls root1 unter root2 hängen
        if root1.get_weight() >= root2.get_weight():
            root2.set_parent(root1)
            root1.set_weight(root1.get_weight() + root2.get_weight())
        else:
            root1.set_parent(root2)
            root2.set_weight(root2.get_weight() + root1.get_weight())




    def create_groups(self, user_ids, groupnumbers):
        """
        Creates groups from the provided user IDs and group numbers.

        Args:
            user_ids (list): A list of user IDs.
            groupnumbers (list): A list of group numbers corresponding to the user IDs.
        """
        # TODO: implement in Praktikum 1
        if len(user_ids) != len(groupnumbers):
            raise ValueError("Die Anzahl der Benutzer-IDs und Gruppennummern muss übereinstimmen.")

        # hinzugefügt
        # Initialisiert die Benutzer und ordnet die Gruppen zu
        group_map = {}  # Mappt Gruppennummern auf Wurzel-IDs

        for user_id, group_id in zip(user_ids, groupnumbers): # zip 2 Listen werden parallel durchlaufen
            # Benutzer werden initialisiert, falls sie nicht vorhanden sind
            if user_id not in self:
                self[user_id] = SetNode() # neuer Eintrag im dictionary

            # Prüft, ob die Gruppe bereits existiert
            if group_id in group_map:
                # Führt die Benutzer zusammen, wenn die Gruppe bereits existiert
                self.union(user_id, group_map[group_id])
            else:
                # Setzt die aktuelle Benutzer-ID als Wurzel der Gruppe
                group_map[group_id] = user_id


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

        # hinzugefügt
        # Überprüft, ob der Benutzer in der Datenstruktur existiert
        if user_id not in self:
            raise ValueError(f"Benutzer mit ID {user_id} wurde nicht gefunden.")

        # Findet die "Wurzel" des Benutzers, um seine Gruppe zu identifizieren
        parent_id = self.find_byid(user_id, return_id=True)

        # Geht durch alle Benutzer und prüft, ob sie zur gleichen Gruppe gehören
        groupmember_ids = []
        for user_id, set_node in self.items():  # Schleife über die Items (user_id und SetNode)
            # Findet für jeden Benutzer seine Wurzel und vergleicht sie mit der des angegebenen Benutzers
            if self.find_byid(user_id, return_id=True) == parent_id:
                groupmember_ids.append(user_id) # append fügt am Ende der Liste user id hinzu



        # Rückgabe der Liste aller Benutzer-IDs, die zur gleichen Gruppe gehören
        return groupmember_ids


    # *** PUBLIC STATIC methods ***

    # *** PRIVATE methods ***

    # *** PUBLIC methods to return class properties ***

    # *** PRIVATE variables ***
