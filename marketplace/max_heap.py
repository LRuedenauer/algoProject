# Die Klasse MaxHeap implementiert einen Max-Heap
import heapq


# TODO: Diese Klasse implementieren Sie in Praktikum 2

class MaxHeap:
    def __init__(self):
        """ Initialisierung des Max-Heaps.
            Ein Knoten speichert die Anzahl der Bieter für eine Auktion sowie die ID-Nummer der Auktion.
            Die Auktion mit den meisten Bietern soll an der Spitze des Max-Heaps stehen.

        heap: Eine Liste zur Speicherung des Heaps, bestehend aus Tupeln in der Form (bid_count, auction_id).
        auction_map: Eine Hash-Map, welche die Position der Auktionen im Max-Heap speichert.
                     (key = auction_id, value = (bid_count, heap_index))
        """
        self.heap = []
        self.auction_map = {}

        # TODO: wenn Sie die anderen Methoden implementiert haben, können Sie diese Zeile auskommentieren
        #raise NotImplementedError

    # *** PUBLIC methods ***

    def add_auction(self, auction_id, bid_count):
        """ Fügt eine neue Auktion zum Max-Heap hinzu.
            Wenn die Auktion schon im heap ist, wird die Auktion nicht hinzugefügt.

        Args:
            auction_id: Die ID-Nummer der Auktion.
            bid_count: Die Anzahl der Bieter für diese Auktion.
        """
        if auction_id in self.auction_map:
            raise ValueError("Auktion existiert bereits")
        #geändert
        # Auktion wird zum Heap hinzugefügt
        # negatives Vorzeichen kehrt die Reihenfolge der Elemente um, sodass das größte Gebot (die Auktion mit den meisten Bietern) immer an der Spitze des Heaps steht
        heapq.heappush(self.heap, (-bid_count, auction_id))

        # Der Index des letzten Elements im Heap ist immer len(self.heap) - 1, da die Indizierung bei 0 beginnt
        # Die Position wird als len(self.heap) - 1 in der Hash-Map gespeichert
        self.auction_map[auction_id] = (bid_count, len(self.heap)-1)

    def update_bidders(self, auction_id, new_bid_count):
        """ Aktualisiert die Anzahl der Bieter für eine Auktion.
            Wenn die Auktion nicht im Heap ist, wird keine Auktion geändert.

        Args:
            auction_id: Die ID-Nummer der Auktion.
            new_bid_count: Die neue Anzahl der Bieter für diese Auktion.
        """
        if auction_id not in self.auction_map:
            raise ValueError("Auktion existiert nicht")
        """ Geändert
            Die alte Anzahl der Bieter und Index"""
        old_bid_count, index = self.auction_map[auction_id]

        # Entfernt das alte Tupel und fügt das neue hinzu
        self.heap[index] = (new_bid_count, auction_id)
        self.auction_map[auction_id] = (new_bid_count, index)

        """ Heapify um die Struktur wiederherzustellen
            Wird nach dem Hinzufügen eines neuen Elements verwendet, das an der letzten Position im Heap eingefügt wurde
            Wird verwendet, um sicherzustellen, dass das neue Element die Heap-Eigenschaft nicht verletzt"""
        if new_bid_count > old_bid_count:  # HINZUGEFÜGT
            self._heapify_up(index)
        elif new_bid_count < old_bid_count:
            self._heapify_down(index)
        """ Wird nach dem Entfernen eines Elements oder nach einer Änderung der Anzahl der Bieter für eine Auktion verwendet (wenn sich die Position des Elements im Heap ändert)
            Wird verwendet, um das Element nach unten zu verschieben, wenn es an einer Position ist, die die Heap-Eigenschaft verletzt"""


    def remove(self, auction_id):
        """ Entfernt die Auktion aus dem Max-Heap.
            Wenn die Auktion nicht im Heap ist, wird keine Auktion entfernt.

        Args:
            auction_id: Die ID-Nummer der Auktion.
        """
        if auction_id not in self.auction_map:
            raise ValueError("Auktion existiert nicht")

        """ Geändert
        #   Hole die Index und entferne aus dem Heap
            Zuerst wird Hash-Map (auction_map) abgefragt, um die Position (Index) der Auktion im Heap zu finden
            pop(auction_id) entfernt das Tuple aus der Hash-Map und gibt es zurück"""
        bid_count, index = self.auction_map.pop(auction_id)
        # Dies ersetzt das Element an der Position index im Heap mit dem Element an der letzten Position
       # self.heap[index] = self.heap[-1]
        # Nun wird das letzte Element entfernt (das ursprünglich das zu entfernende Element war)
        #self.heap.pop()

        """ Diese Bedingung stellt sicher, dass die Heapify-Operationen nur ausgeführt werden, wenn der Heap nach der Entfernung noch Elemente enthält
            Es könnte sein, dass der Heap nach dem Entfernen des letzten Elements leer ist dann müssen keine Heapify-Operationen durchgeführt werden"""
        if index < len(self.heap):
          #  self._heapify_up(index)
            self._heapify_down(index)

    # *** PUBLIC GET methods ***

    def get_auction_with_max_bidders(self):
        """ Gibt die Auktion mit der höchsten Anzahl an Bietern zurück.

        Returns:
            Tuple[int, int]: (bid_count, auction_id)
        """
        if not self.heap:
            return None
        return self.heap[0][0], self.heap[0][1]

    def get_auction_bidders(self, auction_id):
        """ Gibt die Anzahl der Bieter für eine Auktion zurück.
            Wenn die Auktion nicht im Max-Heap ist, wird None zurückgegeben.

        Args:
            auction_id: Die ID-Nummer der Auktion.

        Returns:
            Optional[int]: bid_count
        """
        if auction_id in self.auction_map:
            return self.auction_map[auction_id][0]
        return None

    # *** PRIVATE methods ***

    def _swap(self, i, j):
        """ Hilfsfunktion zum Tauschen von zwei Auktionen im Max-Heap.
            Aktualisiert ebenfalls die Position der Auktionen in der auction_map.

        Args:
            i: Index der ersten Auktion im Max-Heap.
            j: Index der zweiten Auktion im Max-Heap.
        """
        """ Geändert 
            Tauscht zwei Elemente im Heap"""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.auction_map[self.heap[i][1]] = (self.heap[i][0], i)
        self.auction_map[self.heap[j][1]] = (self.heap[j][0], j)

    def _heapify_up(self, index):
        """ Führt das Heapify-Up-Verfahren durch, um die Heap-Eigenschaft nach oben hin wiederherzustellen.

        Args:
            index: Der Index des Elements, das nach oben "heapified" werden soll.
        """
        """ Geändert
            Heapify-Up Verfahrens. """
        while index > 0:                                        # prüft, ob der aktuelle Index des Elements nicht der Wurzelknoten ist
            parent_index = (index - 1) // 2                     # Berechnung gibt den Index des Elternteils des aktuellen Elements zurück, // ganzzahligen Division-Operator
            if self.heap[parent_index][0] >= self.heap[index][0]: # Elternteil größer >= dem aktuellen Element, dann ist die Struktur des Heaps in Ordnung und es ist keine weitere Änderung erforderlich
                break
            self._swap(parent_index, index)                     # aktuelle Element > Elternteil (im Falle eines Max-Heaps), wird das Element mit seinem Elternteil vertauscht, um die Heap-Eigenschaft zu wahren. Das _swap() ist eine Hilfsmethode, die die beiden Elemente im Array vertauscht
            index = parent_index

    def _heapify_down(self, index):
        """ Führt das Heapify-Down-Verfahren durch, um die Heap-Eigenschaft nach unten hin wiederherzustellen.

        Args:
            index: Der Index des Elements, das nach unten "heapified" werden soll.
        """
        """ Geändert
            Heapify-Down Verfahren. """
        n = len(self.heap)          # n = Länge des Heaps, also die Anzahl der Elemente im Heap
        while 2 * index + 1 < n:    # Schleife wird fortgesetzt, solange das linke Kind (2 * index + 1) des aktuellen Knotens (index) im Heap existiert
            left = 2 * index + 1    # Hier werden die Indizes des linken und rechten Kindes des aktuellen Knotens (index) berechnet
            right = 2 * index + 2
            largest = index         # größte Element (in Bezug auf den Max-Heap) zunächst das aktuelle Element

            """ Überprüft, ob der Index des linken Kindes innerhalb der Grenzen des Heaps liegt (left < n)
                Wenn das linke Kind tatsächlich existiert und der Wert dieses Kindes (self.heap[left][0]) > als der Wert des aktuellen Knotens (self.heap[largest][0]), wird der largest-Index auf das linke Kind gesetzt"""
            if left < n and self.heap[left][0] > self.heap[largest][0]:
                largest = left
            if right < n and self.heap[right][0] > self.heap[largest][0]: # Danach dasselbe für das rechte Kind
                largest = right
            if largest == index: # Wenn largest == index der Wert des aktuellen Knotens gleich den Werten seiner Kinder, in dem Fall ist der Heap bereits in Ordnung und die Schleife kann abgebrochen werden
                break
            self._swap(index, largest) # Wenn das aktuelle Element nicht das größte Element ist, wird das aktuelle Element mit dem größten Kind (largest) getauscht
            index = largest

