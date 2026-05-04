from sys import exit
import utils.exceptions as exc
from models.graph import Graph
from models.graph_keys import GraphKeys


class ErrorChecker:
    def nb_drones_error_checker(self,
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

    def zone_error_checker(self,
                           zone: str,
                           graph: Graph,
                           x: str,
                           y: str) -> :

        # Check if x and y are digits, turn to integers
        # Check if less then zero
        if not x.isdigit() or not y.isdigit():
            raise ValueError(f"{x} or {y} is not  number")
        else:
            x, y = map(int, [x, y])
            if x < 0 or y < 0:
                raise ValueError(f"x position: {x}"
                                 f"or y position: {y} not acceptable")


    def zone_metadata_error_checker(self, metadata: dict[str, str]) -> None:

        for data in metadata:
            try:
                GraphKeys(data)
            except ValueError as key_error:
                print(f"")

