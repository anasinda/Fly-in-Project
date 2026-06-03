import matplotlib.pyplot as plt
from src.models.graph import Graph
from src.models.connection import Connection
from src.models.zone import Zone


class Visualizer:
    def __init__(self, graph: Graph, turns: int, simulation_log: list[list[str]]) -> None:
        self.graph = graph
        self.turns = turns
        self.current_turn: int = 0
        self.simualtion_log = simulation_log
        self.fig, self.ax = plt.subplots(figsize=(19.2, 10.8))
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)


    def on_key(self, event) -> None:
        if event.key == 'right':
            if self.current_turn < self.turns:
                self.draw_graph()
                self.draw_drones()
                self.current_turn += 1
        elif event.key == 'left':
            if self.current_turn > 0:
                self.current_turn -= 1
                self.draw_graph()
                self.draw_drones()
            else:
                self.draw_graph()
        elif event.key == 'enter':
            self.current_turn = 0
            self.draw_graph()


    def draw_drones(self) -> None:
        if self.current_turn < self.turns:
            turn_moves = self.simualtion_log[self.current_turn]
            seen: dict[str, int] = {}
            for move in turn_moves:
                parts = move.split('-')
                drone_id = parts[0]
                destination = '-'.join(parts[1:])
                count = seen.get(destination, 0)
                seen[destination] = count + 1
                offset = count * 0.15
                if len(parts) == 2:
                    zone = self.graph.get_zone(parts[1])
                    if zone:
                        self.ax.scatter(zone.x + offset, zone.y, s=100, color='gray')
                        self.ax.text(zone.x + offset, zone.y + 0.4, drone_id,
                                    ha='center', va='top', fontsize=10, color='gray')
                elif len(parts) == 3:
                    zone_a = self.graph.get_zone(parts[1])
                    zone_b = self.graph.get_zone(parts[2])
                    if zone_a and zone_b:
                        mid_x = (zone_a.x + zone_b.x) / 2
                        mid_y = (zone_a.y + zone_b.y) / 2
                        self.ax.scatter(mid_x + offset, mid_y, s=100, color='gray')
                        self.ax.text(mid_x + offset, mid_y + 0.4, drone_id,
                                    ha='center', va='top', fontsize=10, color='gray')
        self.ax.text(0.0020, 0.0040, f"Turn: {self.current_turn + 1}", transform=self.ax.transAxes, fontsize=9)
        self.fig.canvas.draw()

    def draw_graph(self) -> None:
        self.ax.cla()
        for connections in self.graph.adjacency.values():
            for connection in connections:
                x = [connection.zone_a.x, connection.zone_b.x]
                y = [connection.zone_a.y, connection.zone_b.y]
                self.ax.plot(x, y, color='black')

        for zone in self.graph.zones.values():
            self.ax.scatter(zone.x, zone.y, s=800, color=zone.zone_color)
            self.ax.text(zone.x, zone.y, zone.zone_name, ha='center', va='center')
        self.ax.set_aspect('equal')
        self.fig.canvas.draw()

    def run(self):
        self.draw_graph()
        plt.show()
