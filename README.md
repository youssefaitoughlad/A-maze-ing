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


## Prerequisites

This project uses **Poetry** for dependency management and packaging.

### Install Poetry

If you do not have Poetry installed, you can install it using the official installer:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

After installation, ensure Poetry is available in your PATH:

```bash
poetry --version
```

If needed, add Poetry to your shell configuration (e.g., `.bashrc`, `.zshrc`).


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


## Configuration Format (Detailed)

The configuration file follows a strict `KEY=VALUE` format:

```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

### Constraints:

* `WIDTH`, `HEIGHT`: positive integers (maze dimensions)
* `ENTRY`, `EXIT`: coordinates in the form `x,y` within bounds
* `ENTRY` must not be equal to `EXIT`
* `PERFECT`: boolean (`True` or `False`)
* `SEED`: optional integer for deterministic generation

---

## Maze Generation Algorithm

The maze is generated using the **Depth-First Search (DFS) Recursive Backtracker** algorithm.

### Why DFS?

* Guarantees a **perfect maze** (fully connected, no cycles)
* Simple and efficient to implement
* Produces natural-looking maze structures
* Works well with grid-based representations

---

## Reusable Components

The project is designed as a reusable module (`mazegen`) with the following reusable parts:

* `MazeGenerator` class:

  * Can generate mazes of arbitrary sizes
  * Supports deterministic generation via seed
  * Exposes generation and solving functionality

* Configuration parser:

  * Can be reused for any structured config-based system

* Solver (BFS):

  * Generic shortest-path algorithm applicable to grid/graph problems

These components can be integrated into other projects such as games, simulations, or pathfinding systems.

---

## Team & Project Management

### Team Roles

- **👨‍💻 yait-oug** — Core algorithm design (DFS, BFS), maze generation logic, pathfinding implementation, Visual rendering (ASCII graphics), output formatting, type hints, interactive menu system, color management, banner animations ...


- **🎨 ilhakam** — Configuration parser (Pydantic validation), error handling, hexadecimal conversion, package building (Poetry), Makefile management, code quality (flake8/mypy integration)


---

### Planning & Evolution

The project started with a clear plan:

1. Build configuration parser
2. Implement maze data structure
3. Develop generation algorithm (DFS)
4. Implement solver (BFS)
5. Add output formatting and rendering

During development:

* Validation became stricter than initially planned
* Modular design was reinforced to improve maintainability
* Additional features (seed, pattern handling) were integrated progressively

---

### What Worked Well

* Strong modular architecture
* Clear separation of responsibilities
* Early focus on validation reduced bugs later
* Deterministic generation simplified debugging

---

### What Could Be Improved

* More automated testing (unit tests)
* Performance optimization for very large mazes
* Additional visualization features

---

### Tools Used

* **Poetry**: dependency management and packaging
* **flake8 / mypy**: code quality and static typing
* **Git**: version control and collaboration
* **Makefile**: task automation

---