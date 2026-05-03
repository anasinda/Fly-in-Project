from sys import exit
import utils.exceptions as exc


class ErrorChecker:
    def nb_drones_error_checker(self,
                                nb_drones: str,
                                drone_count: int,
                                graph_drones_check: bool,
                                graph_drones_count: int) -> None:

        # Check if value is a number
        if not drone_count.isdigit():
            raise ValueError(f"{drone_count} is not a number")

        # Turn string number to integer number and check if negative or zero
        drone_count = int(drone_count)
        if drone_count <= 0:
            raise ValueError(f"Drone count {drone_count} not acceptable")

        # Check if we already have nb_drones
        if graph_drones_check:
            raise exc.DuplicateDroneCountLineError("Found duplicate"
                                                   f"{nb_drones} at line"
                                                   f"{self.line_number}")

        # Set nb_drones as found and register it
        graph_drones_check = True
        graph_drones_count = drone_count
