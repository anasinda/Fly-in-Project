import re
import webcolors
from sys import argv
from src.models.connection import Connection
from src.models.drone import Drone
from src.models.zone import Zone
from src.models.graph import Graph
from src.utils.graph_keys import GraphKeys
from src.utils.zone_types import ZoneType
from src.utils.exceptions import (ParserError,
                                  MetadataError,
                                  ConnectionError,
                                  ZoneNotFoundError,
                                  DuplicateZoneError,
                                  DuplicateConnectionError)


class Parser:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.line_number: int = 0

    def zone_parser(self, line: re.Match | None) -> None:
        if line is not None:
            zone_placeholder: str = line.group(1)
            zone_name: str = line.group(2)
            x: int = int(line.group(3))
            y: int = int(line.group(4))
            metadata: str | None = line.group(5)
            zone_type: ZoneType = ZoneType.NORMAL
            zone_color: str | None = None
            zone_capacity: int = 1
            zone_catagory: dict[str, str] = {
                "start_hub": "is_start",
                "end_hub": "is_end"
            }
        zone_check = zone_catagory.get(zone_placeholder, None)

        if metadata:
            split_metadata: list[str] = metadata.split()
            store_metadata: dict[str, str] = {}
            for data in split_metadata:
                if "=" not in data:
                    raise MetadataError(f"Invalid metadata format: {data}")
                key, value = data.split("=", 1)
                try:
                    GraphKeys(key)
                    store_metadata[key] = value
                except ValueError:
                    raise ParserError(f"Invalid key: {key}")

            for key, item in store_metadata.items():
                if key == GraphKeys.ZONE.value:
                    try:
                        ZoneType(item)
                        zone_type = ZoneType(item)
                    except ValueError:
                        raise ParserError(f"Invalid zone type: {item}")
                elif key == GraphKeys.COLOR.value:
                    if item != "rainbow":
                        try:
                            webcolors.name_to_rgb(item)
                            zone_color = item
                        except ValueError:
                            raise ParserError(f"Invalid color: {item}")
                elif key == GraphKeys.MAX_DRONES.value:
                    try:
                        if int(item) <= 0:
                            raise ParserError(f"Number isn't supported {item}")
                        else:
                            zone_capacity = int(item)
                    except ValueError:
                        raise ParserError(f"Invalid value: {item}")

        zone_obj = Zone(x, y, zone_name, zone_type, zone_color, zone_capacity)

        if zone_check:
            setattr(zone_obj, zone_check, True)

        try:
            self.graph.add_zone(zone_obj)
        except DuplicateZoneError:
            raise DuplicateZoneError

        self.graph.zones[zone_name] = zone_obj

    def connection_parser(self, line: re.Match | None) -> None:
        if line is not None:
            zone_a: str = line.group(1)
            zone_b: str = line.group(2)
            metadata: str | None = line.group(3)
            max_link_cap: int = 1

        if zone_a not in self.graph.zones or zone_b not in self.graph.zones:
            raise ConnectionError(f"{zone_a} or {zone_b} not in zones list")

        if metadata:
            key, value = metadata.split("=", 1)
            try:
                GraphKeys(key)
            except ValueError:
                raise ParserError(f"Invalid key: {key}")

            try:
                max_link_cap = int(value)
                if max_link_cap <= 0:
                    raise ValueError(f"Number isn't supported {max_link_cap}")
            except ValueError:
                raise ParserError(f"Invalid value: {max_link_cap}")

        connection_obj = Connection(
            self.graph.zones[zone_a], self.graph.zones[zone_b], max_link_cap
        )
        try:
            self.graph.add_connection(connection_obj)
        except DuplicateConnectionError:
            raise DuplicateConnectionError

    def drone_setter(self, graph: Graph, start_zone) -> None:
        for drone_id in range(1, graph.nb_drones_count + 1):
            drone_obj = Drone(drone_id, start_zone)
            if graph.start_zone is not None:
                graph.start_zone.current_drones += 1
            graph.drones_list.append(drone_obj)

    def run_parser(self) -> None:
        nb_drones_re = re.compile(r"^nb_drones:\s+(-?\d+)$")
        zone_re = re.compile(
            r"^(start_hub|end_hub|hub):\s+"
            r"(\w+)\s+"
            r"(-?\d+)\s+"
            r"(-?\d+)"
            r"(?:\s+\[(.*)\])?$"
        )
        connection_re = re.compile(
            r"^connection:\s+"
            r"(\w+)-(\w+)"
            r"(?:\s+\[(\w+=\d+)\])?$"
        )

        try:
            file_path = argv[1]
            try:
                with open(file_path, "r") as file:
                    try:
                        for line in file:
                            line = line.strip()
                            if not line or line.startswith("#"):
                                continue
                            elif res := nb_drones_re.match(line):
                                if int(res.group(1)) <= 0:
                                    raise ParserError(
                                        f"Line {self.line_number}: "
                                        f"Invalid number: {res.group(1)}")
                                self.graph.nb_drones_count = int(res.group(1))
                            elif res := zone_re.match(line):
                                self.zone_parser(res)
                            elif res := connection_re.match(line):
                                self.connection_parser(res)
                            else:
                                raise ParserError(
                                    f"Line {self.line_number}: "
                                    f"Invalid syntax: {line}"
                                )
                    except (
                        ParserError,
                        MetadataError,
                        DuplicateConnectionError,
                        ConnectionError
                    ) as p_error:
                        print(f"[PARSING ERROR] {p_error}")
                        exit(1)
            except FileNotFoundError:
                print("[PARSING ERROR] No such file or directory: "
                      f"{file_path}")
                exit(1)
        except IndexError:
            print("[PARSING ERROR] No file was sent")
            exit(1)
        try:
            if self.graph.end_zone and self.graph.start_zone:
                self.drone_setter(self.graph, self.graph.start_zone)
            else:
                raise ZoneNotFoundError("No start or end zone found")
        except ZoneNotFoundError as z_error:
            print("[PARSING ERROR]", z_error)
            exit(1)
