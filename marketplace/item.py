# Definiert die Klasse Item.
# Die Klasse beschreibt ein Produkt, das über den Marktplatz über eine Auktion ersteigert/verkauft werden kann.
# Ein Produkt hat einen Namen, eine Beschreibung und ein Wert für ein Mindestgebot. Der Besitzer des Produkts
# wird über die Auktion definiert, da der Besitzer in der Auktion ja wechselt. die eindeutige Identifizierung eines
# Produkts erfolgt über die id der zugehörigen Auktion, deshalb hat diese Klasse keine id.

class Item:
    """
    Class representing an item

    Attributes:
        _name (str): name of item
        _description (str): description of the item as one sentence
        _value_min (float): minimum value in € for which the item may be sold (Mindestgebot)
    """

    # *** CONSTRUCTORS ***
    def __init__(self, name: str, description: str, value_min: float) -> None:
        """
        Standard constructor

        :param name: name of item
        :param description: sentence describing the item
        :param value_min: minimum value in € for which the item may be sold (Mindestgebot)
        """
        self._name = name
        self._description = description

        self._value_min = value_min

    # *** PUBLIC SET methods ***

    # *** PUBLIC methods ***

    # *** PUBLIC GET methods ***

    # *** PUBLIC STATIC methods ***

    # *** PRIVATE methods ***

    # *** PUBLIC methods to return class properties ***

    def name(self):
        return self._name

    def description(self):
        return self._description

    def value_min(self):
        return self._value_min

    # *** PRIVATE variables ***
