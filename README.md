*This project has been created as part of the 42 curriculum by anasinda.*

# Fly-in-Project

## Description

Fly-in is a drone routing and simulation system that efficiently navigates multiple drones from a central start zone to a target end zone through a constrained graph network. The project combines pathfinding algorithms, conflict resolution, and visual simulation to optimize drone movement while respecting zone capacities, connection limits, and movement costs.

Key features:
- **Multi-path pathfinding**: Discovers multiple disjoint or overlapping paths using Dijkstra's algorithm with dynamic cost adjustment
- **Conflict-free scheduling**: Manages zone capacity and connection bandwidth constraints in real time
- **Zone types**: Supports normal, restricted, priority, and blocked zones with different movement costs
- **Interactive visualization**: Matplotlib-based display to step through the simulation turn by turn
- **Parser**: Robust file parsing with error handling for map definitions

## Instructions

### Setup

```bash
make venv          # Create a virtual environment
make install       # Install dependencies
```

### Running the Simulation

```bash
make run MAP=maps/easy/01_linear_path.txt
```

Other map examples:
- `maps/easy/02_simple_fork.txt` — basic path splitting
- `maps/medium/01_dead_end_trap.txt` — dead ends and backtracking
- `maps/hard/03_ultimate_challenge.txt` — advanced optimization
- `maps/challenger/01_the_impossible_dream.txt` — research benchmark

### Debug Mode

```bash
make debug MAP=maps/easy/01_linear_path.txt
```

Enter the Python debugger (pdb) to step through execution.

### Linting

```bash
make lint          # Run flake8 and mypy with standard checks
make lint-strict   # Run mypy in strict mode for rigorous validation
make clean         # Remove __pycache__ and .mypy_cache
```

## Algorithm & Implementation Strategy

### Pathfinding: Dijkstra with Dynamic Cost Adjustment

The `Pathfinder` class uses Dijkstra's algorithm to compute the shortest path between start and end zones. The `MultiPathfinder` wraps this to discover multiple disjoint paths by:
1. Running Dijkstra to find the shortest path
2. Temporarily increasing zone costs along that path to encourage alternative routes
3. Repeating until no new paths are found
4. Resetting costs and returning all discovered paths

This approach balances path diversity with optimality, allowing drones to spread across the network.

### Scheduling & Conflict Resolution

The `Simulator` runs a turn-by-turn event loop:
- **Check in-transit drones**: Advance drones moving through restricted zones (2-turn movement)
- **Dispatch ready drones**: Send drones from their current zone to the next if:
  - The connection has link capacity
  - The destination zone has drone capacity
  - Reservations are honored (restricted zones block new entries)
- **Resolve conflicts**: If a drone cannot move and no in-transit drones are active, a deadlock is raised

Drones use round-robin path assignment to balance load across discovered paths.

### Data Structures

- **Graph**: Adjacency list representation with zones and bidirectional connections
- **Zone**: Tracks current occupancy, capacity, type (normal/restricted/priority/blocked), and temporary cost
- **Connection**: Tracks current usage and max link capacity
- **Drone**: Maintains current position, assigned path, and progress index

## Visual Representation

The `Visualizer` class renders the graph and simulation state using Matplotlib:
- **Zones**: Displayed as colored circles (color from map metadata)
- **Connections**: Black lines connecting zones
- **Drones**: Gray dots with IDs, positioned at their current zone or midpoint of connection (if in-transit)
- **Navigation**: Use arrow keys to step forward/backward through turns; press Enter to reset

This allows users to visually inspect drone movement, identify bottlenecks, and validate the correctness of the simulation without reading raw logs.

## Resources

### Documentation & References
- Dijkstra's Algorithm: https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/
- Graph Theory: https://www.youtube.com/watch?v=sWsXBY19o8I
- Python Type Hints: https://docs.python.org/3/library/typing.html

### Tools Used
- **matplotlib**: Graph visualization and interactive simulation display
- **mypy**: Static type checking for Python
- **flake8**: Code style and quality checks
- **webcolors**: Parsing zone color metadata

### AI Usage

AI was used minimally and selectively:
- **Documentation**: Generating initial docstring templates for classes and methods (all manually reviewed and simplified)
- **Type hints**: Suggesting type annotations for function signatures (validated against the codebase)
- **Error handling**: Brainstorming exception scenarios and recovery strategies
- **Topic and concepts**: Explain what needs to be learned and where to learn it

All AI-generated content was critically reviewed, tested, and adapted to fit the project's coding style and requirements. The core algorithms, simulation logic, and visualization were implemented from first principles.
