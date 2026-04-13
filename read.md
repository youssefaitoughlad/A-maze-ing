*This project has been created as part of the 42 curriculum by <login1>[, <login2>[, <login3>[...]]].*

# A-Maze-ing 🧠

A-Maze-ing is a Python-based maze generation and solving system that builds, validates, and visualizes mazes using graph algorithms.

The project implements a complete pipeline:

* Parsing structured configuration files
* Generating valid mazes using depth-first search (DFS)
* Solving mazes with shortest-path algorithms (BFS)
* Exporting mazes in a compact hexadecimal format
* Rendering mazes visually with optional features

This project focuses on algorithmic correctness, data validation, and modular system design, making it both a practical tool and a demonstration of software engineering principles.

## Features

* **Configurable Maze Generation**
  Generate mazes of arbitrary size using a configuration file.

* **Perfect Maze Support**
  Ensures a fully connected maze with exactly one unique path between any two cells.

* **Shortest Path Solver**
  Computes the optimal path from entry to exit using breadth-first search (BFS).

* **Hexadecimal Encoding**
  Stores maze structure efficiently using bitmask-based hex representation.

* **Robust Configuration Validation**
  Validates all inputs (dimensions, entry/exit points, constraints) before execution.

* **42 Pattern Integration**
  Embeds a predefined “42” pattern inside the maze while preserving validity.

* **Deterministic Generation (Seed Support)**
  Reproduce identical mazes using a fixed random seed.

* **Modular Architecture**
  Clean separation between parsing, generation, solving, and rendering components.

* **Error Handling**
  Gracefully handles invalid configurations and runtime issues.

## Instructions

### Installation

Install project dependencies using Poetry:

```bash
make install
```

---

### Running the Program

Run the maze generator using the default configuration file:

```bash
make run
```

---

### Debug Mode

Run the program with the Python debugger:

```bash
make debug
```

---

### Code Quality Checks

Run standard linting (flake8 + mypy):

```bash
make lint
```

Run strict linting:

```bash
make lint-strict
```

---

### Build Package

Build the project as a distributable package:

```bash
make build
```

---

### Clean Project

Remove cache files and build artifacts:

```bash
make clean
```

---

### Configuration

The program uses a configuration file (default: `config.txt`) passed automatically via the Makefile.

You can modify the following variables inside the Makefile:

```makefile
MAIN = a_maze_ing.py
CONFIG = config.txt
```

---

### Output

The program generates a maze file containing:

* A hexadecimal representation of the maze grid
* Entry and exit coordinates
* The computed shortest path

## Resources

### Documentation & References

* Python Official Documentation — [https://docs.python.org/3/](https://docs.python.org/3/)
* Poetry Documentation — [https://python-poetry.org/docs/](https://python-poetry.org/docs/)
* Graph Theory Basics — [https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)](https://en.wikipedia.org/wiki/Graph_%28discrete_mathematics%29)
* Depth-First Search (DFS) — [https://en.wikipedia.org/wiki/Depth-first_search](https://en.wikipedia.org/wiki/Depth-first_search)
* Breadth-First Search (BFS) — [https://en.wikipedia.org/wiki/Breadth-first_search](https://en.wikipedia.org/wiki/Breadth-first_search)
* Maze Generation Algorithms — [https://en.wikipedia.org/wiki/Maze_generation_algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm)

---

### Use of AI

AI tools were used as a support system during the development of this project. Their usage was limited to guidance and conceptual clarification, not direct code generation.

Specifically, AI was used for:

* Understanding and refining algorithmic concepts (DFS, BFS, graph modeling)
* Reviewing architectural decisions (modular design, separation of concerns)
* Identifying potential edge cases and validation strategies
* Improving documentation quality (README structure, clarity, formatting)

AI was **not used to generate final implementation code**. All core logic, algorithms, and design decisions were implemented and validated independently.

---

This approach ensured that the project remains a genuine demonstration of problem-solving, system design, and programming skills while leveraging AI as a learning and review tool.

---

## Project Structure

The project follows a modular architecture, separating responsibilities across components:

```text
mazegen/
├── config_parser.py   # Configuration validation and parsing
├── generate_maze.py   # Maze generation logic (DFS)
├── draw_maze.py       # Maze rendering
├── maze2hex.py        # Hexadecimal encoding and output
├── solver.py          # Pathfinding logic (BFS)
```

---

## Usage Example

Example workflow:

```bash
make run
```

This will:

* Parse the configuration file
* Generate a valid maze
* Compute the shortest path
* Save the output in hexadecimal format

---

## Technical Choices

* **DFS (Depth-First Search)** was used for maze generation to produce perfect mazes with a single unique path between cells.
* **BFS (Breadth-First Search)** was chosen for pathfinding to guarantee the shortest path.
* **Bitmask Encoding** allows compact and efficient representation of maze walls.
* **Poetry** was used for dependency management and packaging to ensure reproducibility.

---

## Design Principles

* **Separation of Concerns**: Each module has a single responsibility.
* **Determinism**: Optional seed ensures reproducible maze generation.
* **Robust Validation**: Configuration is strictly validated before execution.
* **Extensibility**: Modular design allows easy feature extension.
