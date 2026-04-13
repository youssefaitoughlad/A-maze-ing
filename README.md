*This project has been created as part of the 42 curriculum by yait-oug, ilhakam*


# A-Maze-ing 🧠

A-Maze-ing is a Python-based maze generation and solving system that builds, validates, and visualizes mazes using graph algorithms.

The project implements a complete pipeline:

* Parsing structured configuration files
* Generating valid mazes using depth-first search (DFS)
* Solving mazes with shortest-path algorithms (BFS)
* Exporting mazes in a compact hexadecimal format
* Rendering mazes visually with optional features

This project focuses on algorithmic correctness, data validation, and modular system design, making it both a practical tool and a demonstration of software engineering principles.


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

### Output

The program generates a maze file containing:

* A hexadecimal representation of the maze grid
* Entry and exit coordinates
* The computed shortest path


## Resources

### Documentation & References
[Build a Maze Generator in Python](https://www.youtube.com/watch?v=p2ki8bcGOXs&list=PL035-0hqH89VibCntmdk744lJUufi6nZw&index=10) — Youtube/@Code_with_Afif

[BFS vs DFS: Algorithms and Complexities](https://www.scribd.com/presentation/31345233/BFS-DFS) — [SCRIBD]

[Graph Theory Basics](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)) — Wikipedia 

---

### Use of AI

AI tools were used as a support system during the development of this project. Their usage was limited to guidance and conceptual clarification.

Specifically, AI was used for:

* Understanding and refining algorithmic concepts (DFS, BFS, graph modeling)
* Reviewing architectural decisions (modular design, separation of concerns)
* Identifying potential edge cases and validation strategies
* Improving documentation quality (README structure, clarity, formatting)


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


## Configuration File Format

The configuration file uses `KEY=VALUE` syntax. Lines starting with `#` are ignored as comments.

## Configuration File Format

The configuration file uses `KEY=VALUE` syntax. Lines starting with `#` are ignored as comments.

