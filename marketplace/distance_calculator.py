import osmnx as ox

from typing import Tuple, Dict, List


class DistanceCalculator:
    def __init__(self):
        # Cache für bereits berechnete Distanzen
        self._distance_cache = {}
        # Graph für ganz NRW laden und cachen
        self._map_graph = ox.graph.graph_from_place('North Rhine-Westphalia, Germany',
                                                    network_type='drive')

    def calculate_distance(self, origin_coords: Tuple[float, float],
                           dest_coords: Tuple[float, float]) -> float:
        """
        Berechnet die Fahrstrecke zwischen zwei Koordinatenpaaren

        Args:
            origin_coords: (Latitude, Longitude) des Startpunkts
            dest_coords: (Latitude, Longitude) des Zielpunkts

        Returns:
            Distanz in Metern
        """
        # Cache-Key erstellen
        cache_key = f"{origin_coords}_{dest_coords}"

        # Wenn Distanz bereits berechnet wurde, aus Cache zurückgeben
        if cache_key in self._distance_cache:
            return self._distance_cache[cache_key]

        try:
            # Nächste Knoten im Graph finden
            origin = ox.distance.nearest_nodes(self._map_graph,
                                               origin_coords[1],
                                               origin_coords[0])
            destination = ox.distance.nearest_nodes(self._map_graph,
                                                    dest_coords[1],
                                                    dest_coords[0])

            # Kürzesten Pfad berechnen
            shortest_path = ox.distance.shortest_path(self._map_graph,
                                                      origin,
                                                      destination,
                                                      weight='length')

            # Gesamtdistanz des Pfads berechnen
            total_distance = sum(self._map_graph[path[0]][path[1]][0]['length']
                                 for path in zip(shortest_path[:-1], shortest_path[1:]))

            # Distanz im Cache speichern
            self._distance_cache[cache_key] = total_distance

            return total_distance

        except Exception as e:
            print(f"Fehler bei der Distanzberechnung: {e}")
            return float('inf')  # Unendlich zurückgeben bei Fehler

    def find_nearby_friends_of_friends(self, user_id: str, users: Dict, max_distance: float = 50000) -> List[str]:
        """
        Findet Freunde von Freunden innerhalb einer bestimmten Distanz

        Args:
            user_id: ID des Nutzers
            users: Dictionary mit allen Nutzern
            max_distance: Maximale Distanz in Metern (Standard: 50km)

        Returns:
            Liste von Nutzer-IDs der nahegelegenen Freunde von Freunden
        """
        user = users[user_id]
        user_coords = user.get_coordinates()

        # Set für besuchte Nutzer
        visited = {user_id}
        # Liste für Empfehlungen
        recommendations = []

        # Freunde der Freunde finden (2 Ebenen tief)
        queue = [(friend_id, 1) for friend_id in user.friends()]

        while queue:
            current_id, depth = queue.pop(0)

            if current_id in visited:
                continue

            visited.add(current_id)
            current_user = users[current_id]

            # Distanz zum aktuellen Nutzer berechnen
            distance = self.calculate_distance(user_coords, current_user.get_coordinates())

            # Wenn Nutzer nah genug ist und nicht direkt befreundet, als Empfehlung hinzufügen
            if distance <= max_distance and current_id not in user.friends():
                recommendations.append((current_id, distance))

            # Wenn wir noch nicht zu tief sind, Freunde des aktuellen Nutzers zur Queue hinzufügen
            if depth < 2:
                for friend_id in current_user.friends():
                    if friend_id not in visited:
                        queue.append((friend_id, depth + 1))

        # Nach Distanz sortieren und nur IDs zurückgeben
        return [rec[0] for rec in sorted(recommendations, key=lambda x: x[1])]