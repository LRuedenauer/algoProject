# Implementiert den ADT Stack (Stapel) mit der Datenstruktur: verkettete Liste

class Stack(list):
    # *** CONSTRUCTORS ***
    def __init__(self):
        super().__init__()

    # *** PUBLIC methods ***

    def push(self, item):
        """Fügt ein Element oben auf den Stapel."""
        self.append(item)

    # laut Vorlesung gibt es diese Methode nicht in einem Stack
    def update(self, item, item_new):
        for i, myitem in enumerate(self):
            if myitem == item:
                self[i] = item_new

    # *** PUBLIC GET methods ***

    # Die Methode pop() wird bereits durch die parent Klasse list implementiert

    def peek(self):
        """Gibt das oberste Element des Stapels zurück, ohne es zu entfernen.
        Gibt None zurück, wenn der Stapel leer ist."""
        if self.is_empty():
            return None
        return self[-1]

    def is_empty(self):
        """Überprüft, ob der Stapel leer ist."""
        return len(self) == 0

    def size(self):
        """Gibt die Anzahl der Elemente im Stapel zurück."""
        return len(self)
