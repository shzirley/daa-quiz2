# Snake Pathfinding — BFS vs DFS Comparison

**Course:** Design & Analysis of Algorithms (DAA) — Quiz 2  
**Language:** Python 3  
**Interface:** Pygame (game visualization) + terminal (menu & experiment report)  
**Repository:** [github.com/shzirley/daa-quiz2](https://github.com/shzirley/daa-quiz2)

---

## Project summary

This project is an **automated Snake game** where the snake moves on its own toward food using pathfinding algorithms. We compare two algorithms from the course:

| Algorithm | Role in the game |
|-----------|------------------|
| **BFS** (Breadth-First Search) | Finds a path to food; on an unweighted graph it yields the **shortest path** (minimum steps). |
| **DFS** (Depth-First Search) | Finds a path with **depth-first** exploration; does not guarantee the shortest path. |

The game map is modeled as a **grid graph**: each cell is a node; up/down/left/right moves are edges (when not blocked by walls, obstacles, or the snake body).

**Experiment goal:** Compare **score (food eaten)**, **step count**, **pathfinding decision time**, and **nodes expanded** between BFS and DFS on the same difficulty level.

---

## Quiz 2 requirements checklist

| Requirement | How we meet it |
|-------------|----------------|
| Group program (game) | Snake game with static & dynamic obstacles |
| At least one course algorithm | **BFS** and **DFS** for pathfinding |
| Any programming language | Python |

---

## Team members

| Name | Student ID | Contribution |
|------|------------|--------------|
| Jorell Ramos Sinaga | 5025241202 | BFS & DFS (`find_path_bfs`, `find_path_dfs`), replanning in `run_simulation`, time & node-expansion metrics, BFS vs DFS comparison table |
| Angela Vania Sugiyono | 5025241226 | `SnakeGame` (movement, food, collisions), level layouts, Pygame UI, README, YouTube demo, GitHub setup & push |

---

## How to run

### Prerequisites

- Python 3.10+ (tested with Python 3.13)
- Windows / Linux / macOS

### Installation

```bash
cd quiz2
pip install -r requirements.txt
```

### Run the program

```bash
python main.py
```

1. Choose a level: **Easy** / **Medium** / **Hard**
2. The program runs **5 BFS simulations** then **5 DFS simulations** (10 runs per batch)
3. Each run opens a **Pygame window**; the snake follows the path from the algorithm
4. When finished, the terminal prints a **BFS vs DFS comparison table**
5. Answer `y` / `n` to run another batch at the same level

> **Note:** In-game prompts and console messages are in Indonesian (as implemented in `main.py`).

---

## Program flow

```
Level input (terminal)
    → 5× run_simulation(..., "BFS")
    → 5× run_simulation(..., "DFS")
    → print_comparison()  (average metrics table)
    → append results to snake_experiment_log.csv
    → prompt: continue batch? (y/n)
```

Each game step:

1. When the step queue is empty → **replan**: run BFS or DFS from snake head to food
2. The path is stored in a step queue; the snake moves one cell per frame
3. When food is eaten / dynamic obstacles spawn → state changes → **replan**
4. Game ends on: collision, no path (trapped), or **1000 step** limit

---

## Difficulty levels

| Level | Grid size | Static obstacles | Dynamic obstacles |
|-------|-----------|------------------|-------------------|
| **Easy** | 15×15 | None | None |
| **Medium** | 20×20 | Two vertical pillars | After 7 food: spawn 1–2 random obstacles |
| **Hard** | 25×25 | Plus (+) shape | After 5 food: spawn 1–5 random obstacles |

**Color legend (Pygame):**

- Green — snake | Red — food  
- Dark gray — static obstacles | Light gray — dynamic obstacles  

---

## Recorded metrics

| Metric | Meaning |
|--------|---------|
| **Total Food** | Food eaten (score) |
| **Total Steps** | Steps until game over (max 1000) |
| **Average Time (ms)** | Average CPU time per pathfinding decision |
| **Average Expansion** | Average nodes expanded per replan |
| **Replans** | How many times pathfinding was rerun |
| **Game Over Reason** | End cause (e.g. trapped, step limit, collision) |

Each run is appended to **`snake_experiment_log.csv`** for documentation and further analysis.

---

## Sample terminal output

```
Pilih Level Eksperimen (Easy/Medium/Hard): Medium

==============================
Menjalankan Batch (Level: Medium)
==============================
Menjalankan 5x BFS...
  [BFS Run 1/5]... Selesai. Makanan: 40  | Langkah: 714  | Alasan: No Path Found (Trapped)
  ...

Menjalankan 5x DFS...
  [DFS Run 1/5]... Selesai. Makanan: 13  | Langkah: 1000 | Alasan: Step Limit Reached
  ...

==============================================================
                 HASIL PERBANDINGAN BFS vs DFS
==============================================================
  Metrik                        BFS        DFS     Pemenang
  ...
  >>> PEMENANG BATCH INI: *** BFS *** (3/4 kategori)
```

**Interpretation:** Results vary per batch because food placement and dynamic obstacles are **random**. BFS tends to win on food and steps because paths to food are shorter; DFS often uses more steps before hitting the 1000-step cap.

---

## File structure

```
quiz2/
├── main.py                      # Game logic, BFS, DFS, simulation, UI
├── requirements.txt             # Python dependencies
├── README.md                    # This documentation
└── snake_experiment_log.csv     # Run log (created automatically)
```

### Key sections in `main.py`

| Section | Lines (approx.) | Purpose |
|---------|-----------------|---------|
| `SnakeGame` | 26–134 | Game state, movement, obstacles, valid neighbors |
| `find_path_bfs` | 139–160 | BFS implementation |
| `find_path_dfs` | 163–184 | DFS implementation |
| `run_simulation` | 225–334 | Pygame loop + replanning |
| `print_comparison` | 337–386 | Batch comparison table |

---

## Algorithms (brief)

**Graph:** 4-directional grid; nodes are passable cells (including the tail cell when the snake can move into it).

**BFS:** `deque` queue, level-by-level visit → first path to food is shortest (in step count).

**DFS:** Stack (LIFO), depth-first visit → path found may be longer.

Both algorithms count **nodes expanded** to compare computational cost per replan.

---

## Demo video

Gameplay and BFS vs DFS experiment batch (click thumbnail to watch):

[![Demo video — Snake Pathfinding BFS vs DFS](https://img.youtube.com/vi/YCfajdwADps/hqdefault.jpg)](https://youtu.be/YCfajdwADps)

**YouTube:** [https://youtu.be/YCfajdwADps](https://youtu.be/YCfajdwADps)

The video shows the Pygame window (snake, food, obstacles) and running a simulation through to the comparison table in the terminal.

---

## License & notes

Academic project for DAA Quiz 2. Contact team members above for technical questions.
