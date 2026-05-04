from sys import exit
import utils.exceptions as exc
from models.graph import Graph
from models.graph_keys import GraphKeys
from models.zone import Zone
from models.zone_types import ZoneType


class ErrorChecker:
    def nb_drones_validator(self,
                                line_number: int,
                                nb_drones: str,
                                drone_count: int,
                                graph: Graph) -> None:

        # Check if value is a number, turn to integer
        # Check if less then or equal to zero
        if not drone_count.isdigit():
            raise ValueError(f"{drone_count} is not a number")
        else:
            drone_count = int(drone_count)
            if drone_count <= 0:
                raise ValueError(f"Drone count {drone_count} not acceptable")

        # Check if we already have nb_drones
        # Else set as found and register it
        if graph.nb_drones_check:
            raise exc.DuplicateDroneCountLineError("Found duplicate"
                                                   f"{nb_drones} at line"
                                                   f"{line_number}")
        else:
            graph.nb_drones_check = True
            graph.nb_drones_count = drone_count

    def zone_data_validator(self,
                            x: str,
                            y: str,
                            zone_name: str,
                            zone: str,
                            line_number: int) -> Zone:

        # Check if x & y are digits, turn to ints
        if not x.isdigit() or not y.isdigit():
            raise ValueError(f"{x} or {y} is not  number")
        else:
            x, y = map(int, [x, y])

        # Save meatadata in dictionary, check for wrong type of data
        # and return zone object
        metadata: dict[GraphKeys, str] = dict()
        if "[" in zone:
            extradata = zone.split("[")[-1].replace("]", "")
            for data in extradata.split():
                try:
                    key, value = data.split("=")
                    key = GraphKeys(key)
                    if value.isdigit():
                        value = int(value)
                    metadata[key] = value
                except ValueError as key_error:
                    print(f"File line number: {line_number}\n")
                    raise ("Error type: ", key_error)

            try:
                if GraphKeys.MAX_DRONES in metadata:
                    if not metadata[GraphKeys.MAX_DRONES].isdigit:
                        raise ValueError("max_drones:"
                                        f"{metadata[GraphKeys.MAX_DRONES]}"
                                        "is not a number")
            except ValueError as max_drone_type_error:
                print(f"File line number: {line_number}\n")
                raise max_drone_type_error

            try:
                zone_type: str = ZoneType(metadata.get(GraphKeys.ZONE, "normal")).value
            except ValueError as zone_type_error:
                print(f"File line number: {line_number}\n")
                raise zone_type_error

            zone_color: str = metadata.get(GraphKeys.COLOR, None)
            zone_capacity: int = metadata.get(GraphKeys.MAX_DRONES, 1)
            zone_obj = Zone(x, y,
                            zone_name.strip(),
                            zone_type,
                            zone_color.strip(),
                            zone_capacity)
            return zone_obj


    def connection_validator(self, connection_line: str, graph: Graph) -> None:
        pass

