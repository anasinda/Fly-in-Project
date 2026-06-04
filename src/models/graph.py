from src.models.drone import Drone
from src.models.zone import Zone
from src.models.connection import Connection
from collections import defaultdict
from src.utils.exceptions import DuplicateZoneError, DuplicateConnectionError
from src.utils.exceptions import ZoneNotFoundError


class Graph:
    """Represent the parsed map as zones and bidirectional connections."""

    def __init__(self) -> None:
        """Initialize empty graph containers and simulation state."""
        self.zones: dict[str, Zone] = {}
        self.adjacency: defaultdict[str, list[Connection]] = defaultdict(list)
        self.seen_connections: set[frozenset[str]] = set()
        self.start_zone: Zone | None = None
        self.end_zone: Zone | None = None
        self.nb_drones_check = False
        self.nb_drones_count: int = 0
        self.drones_list: list[Drone] = []
        self.in_end: dict[str, Drone] = {}

    def add_zone(self, zone: Zone) -> None:
        """Add a zone to the graph and reject duplicate names."""
        if zone.zone_name in self.zones:
            raise DuplicateZoneError(
                "Found duplicate zone" f"{zone.zone_name} in file..."
            )

        if zone.is_start:
            self.start_zone = zone
        elif zone.is_end:
            self.end_zone = zone
        self.zones[zone.zone_name] = zone

    def add_connection(self, connection: Connection) -> None:
        """Add a bidirectional connection and reject duplicates."""
        key = frozenset({
            connection.zone_a.zone_name,
            connection.zone_b.zone_name
        })

        if key in self.seen_connections:
            raise DuplicateConnectionError(
                "Found duplicate connection" f"{key} in file..."
            )
        self.seen_connections.add(key)
        self.adjacency[connection.zone_a.zone_name].append(connection)
        self.adjacency[connection.zone_b.zone_name].append(connection)

    def get_zone(self, name: str) -> Zone:
        """Return a zone by name."""
        if name not in self.zones:
            raise ZoneNotFoundError(f"Zone {name} not found in graph")
        return self.zones[name]

    def get_zone_connections(self, zone: str) -> list[Connection]:
        """Return every connection attached to a zone."""
        return self.adjacency[zone]
