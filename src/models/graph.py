from models.drone import Drone
from models.zone import Zone
from models.connection import Connection
from collections import defaultdict
from utils.exceptions import DuplicateZoneError, DuplicateConnectionError
from utils.exceptions import ZoneNotFoundError


class Graph:
    """Class that creates the graph representaton of the map"""
    def __init__(self) -> None:
        self.zones: dict[str, Zone] = {}
        self.adjacency: defaultdict[str, list[Connection]] = defaultdict(list)
        self.seen_connections: set[frozenset[str]] = set()
        self.start_zone: Zone | None = None
        self.end_zone: Zone | None = None
        self.nb_drones_check = False
        self.nb_drones_count: int = 0
        self.drones_list: list[Drone] = []

    def add_zone(self, zone: Zone) -> None:
        """
        Add's zone to zones dictionary
        Also checks for duplicate zones
        """
        if zone.zone_name in self.zones:
            raise DuplicateZoneError("Found duplicate zone"
                                     f"{zone.zone_name} in file...")

        if zone.is_start:
            self.start_zone = zone
        elif zone.is_end:
            self.end_zone = zone
        self.zones[zone.zone_name] = zone

    def add_connection(self, connection: Connection) -> None:
        """
        Add's connections to adjacency list in
        a bi-directional way
        Checks for duplicate connections
        """
        key = frozenset({
            connection.zone_a.zone_name,
            connection.zone_b.zone_name
        })

        if key in self.seen_connections:
            raise DuplicateConnectionError("Found duplicate connection"
                                           f"{key} in file...")
        self.seen_connections.add(key)
        self.adjacency[connection.zone_a.zone_name].append(connection)
        self.adjacency[connection.zone_b.zone_name].append(connection)

    def get_zone(self, name: str) -> Zone:
        """Retrieves zone from zones dictionary if found"""
        print("This is zones", self.zones)
        if name not in self.zones:
            raise ZoneNotFoundError(f"Zone {name} not found in graph")
        return self.zones[name]

    def get_connections_for_zone(self, name: str) -> list[Connection]:
        """Retrieves connection from adjacency list"""
        return self.adjacency[name]
