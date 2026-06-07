import matplotlib.pyplot as plt
from matplotlib.backend_bases import Event, KeyEvent
from src.models.graph import Graph


class Visualizer:
    """Render the graph and move through the simulation turn by turn."""

    def __init__(self, graph: Graph, turns: int,
                 simulation_log: list[list[str]]) -> None:
        """Store visualization state and create the matplotlib figure."""
        self.graph = graph
        self.turns = turns
        self.current_turn: int = 0
        self.simulation_log = simulation_log
        self.fig, self.ax = plt.subplots(figsize=(19.2, 10.8))
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)

    def on_key(self, event: Event) -> None:
        """Handle key presses for stepping through turns."""
        if not isinstance(event, KeyEvent):
            return
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
        """Draw drone markers for the current turn."""
        if self.current_turn < self.turns:
            turn_moves = self.simulation_log[self.current_turn]
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
                        self.ax.scatter((zone.x + offset),
                                        zone.y,
                                        s=400,
                                        color='gray', zorder=4)
                        self.ax.text((zone.x + offset),
                                     (zone.y + 0.4),
                                     drone_id,
                                     ha='center',
                                     va='top',
                                     fontsize=14,
                                     color='gray', zorder=5)
                elif len(parts) == 3:
                    zone_a = self.graph.get_zone(parts[1])
                    zone_b = self.graph.get_zone(parts[2])
                    if zone_a and zone_b:
                        mid_x = (zone_a.x + zone_b.x) / 2
                        mid_y = (zone_a.y + zone_b.y) / 2
                        self.ax.scatter((mid_x + offset),
                                        mid_y,
                                        s=400,
                                        color='gray')
                        self.ax.text((mid_x + offset),
                                     (mid_y + 0.4),
                                     drone_id,
                                     ha='center',
                                     va='top',
                                     fontsize=14,
                                     color='gray')
        self.ax.text(0.0020,
                     0.0040,
                     f"Turn: {self.current_turn + 1}",
                     transform=self.ax.transAxes,
                     fontsize=9)
        self.fig.canvas.draw()

    def draw_graph(self) -> None:
        """Draw the map nodes and connections."""
        self.ax.cla()
        for connections in self.graph.adjacency.values():
            for connection in connections:
                x = [connection.zone_a.x, connection.zone_b.x]
                y = [connection.zone_a.y, connection.zone_b.y]
                self.ax.plot(x, y, color='black', zorder=1)

        for zone in self.graph.zones.values():
            self.ax.scatter(zone.x,
                            zone.y,
                            s=1500,
                            color=zone.zone_color, zorder=2)
            self.ax.text(zone.x,
                         zone.y,
                         zone.zone_name,
                         ha='center',
                         va='center', zorder=3)
        all_y = [zone.y for zone in self.graph.zones.values()]
        min_y = min(all_y) - 1
        max_y = max(all_y) + 1
        self.ax.set_ylim(min_y, max_y)

    def run(self) -> None:
        """Open the visualization window."""
        self.draw_graph()
        plt.show()
