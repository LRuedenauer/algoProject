import tkinter as tk  # Importiert das tkinter-Modul, um GUI-Anwendungen zu erstellen

# Definiert die Klasse SystemMessages
# über die Methode push() können Nachrichten in der Warteschlange gespeichert werden.
# Nachrichten in der Warteschlange werden nacheinander in dem tk.Label _lbl_sysmessage
# für 5 Sekunden angezeigt, bis keine Nachrichten mehr in der Warteschlange existieren.
# in der GUI werden diese Nachrichten oben links angezeigt.

class SystemMessages:
    # *** CONSTRUCTORS ***
    def __init__(self, label: tk.Label):
        """
        Initialisiert das SystemMessages-Objekt.
        :param label: Ein tk.Label-Widget, das für die Anzeige von Nachrichten verwendet wird.
        """
        self._queue = []  # Warteschlange (Queue) für die Nachrichten, initialisiert als leere Liste
        self._lbl_sysmessage = label  # Das Label, das für die Anzeige von Nachrichten genutzt wird
        self._displaying = False  # Ein Flag, das anzeigt, ob derzeit eine Nachricht angezeigt wird

    # *** PUBLIC SET methods ***

    # *** PUBLIC methods ***

    def push(self, message):
        """
        Fügt eine Nachricht zur Warteschlange hinzu. Wenn gerade keine Nachricht angezeigt wird,
        wird die nächste Nachricht aus der Warteschlange angezeigt.
        :param message: Die Nachricht, die in die Warteschlange eingefügt werden soll
        """
        self._queue.append(message)  # Fügt die Nachricht ans Ende der Warteschlange hinzu
        if not self._displaying:  # Wenn keine Nachricht gerade angezeigt wird
            self._display_next_message()  # Zeige die nächste Nachricht an

    # *** PUBLIC GET methods ***


    # *** PUBLIC STATIC methods ***


    # *** PRIVATE methods ***

    def _display_next_message(self):
        """
        Zeigt die nächste Nachricht in der Warteschlange an. Wenn keine Nachrichten mehr vorhanden sind,
        wird das Label zurückgesetzt.
        """
        if not self._queue:  # Wenn die Warteschlange leer ist
            self._displaying = False  # Setze das Flag, dass keine Nachricht angezeigt wird
            self._lbl_sysmessage.config(text="-", bg='#d9d9d9')  # Setze das Label zurück auf Standard (kein Text, grauer Hintergrund)
            return  # Beende die Methode, weil es keine Nachrichten mehr gibt

        self._displaying = True  # Setze das Flag, dass eine Nachricht angezeigt wird
        message = self._queue.pop(0)  # Entnehme die erste Nachricht aus der Warteschlange (FIFO-Prinzip)
        self._lbl_sysmessage.config(text=message, bg='yellow')  # Zeige die Nachricht im Label an, Hintergrund wird gelb

        # Wenn keine Nachrichten mehr in der Warteschlange sind, zeige die letzte Nachricht für 15 Sekunden an
        # Andernfalls zeige jede Nachricht für 3 Sekunden an
        if len(self._queue) == 0:
            display_time = 15  # 15 Sekunden für die letzte Nachricht
        else:
            display_time = 3  # 3 Sekunden für alle anderen Nachrichten

        # Nach der angegebenen Zeit (in Millisekunden) wird die nächste Nachricht angezeigt
        self._lbl_sysmessage.after(display_time * 1000, self._display_next_message)  # Wartet die Zeit ab und ruft dann _display_next_message erneut auf

    # *** PUBLIC methods to return class properties ***


    # *** PRIVATE variables ***

