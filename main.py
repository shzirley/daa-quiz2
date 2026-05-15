import random
from collections import deque
import time
import pygame
import csv
import os

# --- Konstanta Arah ---
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# --- Konstanta Pygame ---
BLOCK_SIZE = 20
(W_PAD, H_PAD) = (0, 0)

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 200, 0)
COLOR_GREEN_DARK = (0, 150, 0)
COLOR_RED = (200, 0, 0)
COLOR_GRAY = (100, 100, 100)
COLOR_GRAY_DYNAMIC = (160, 160, 160)

class SnakeGame:
    def __init__(self, width, height, static_obstacles=None, food_trigger=0, obstacle_spawn_count=(0,0)):
        self.width = width
        self.height = height

        self.static_obstacles = set(static_obstacles) if static_obstacles else set()
        self.dynamic_obstacles = set()

        self.food_trigger_threshold = food_trigger
        self.obstacle_spawn_min = obstacle_spawn_count[0]
        self.obstacle_spawn_max = obstacle_spawn_count[1]
        self.food_eaten_counter = 0

        start_pos = (1, 1)
        self.snake = deque([start_pos])
        self.snake_body_set = {start_pos}

        self.food = None
        self.place_food()

        self.game_over = False
        self.score = 0
        self.steps = 0
        self.max_steps = 1000
        self.game_over_reason = ""

    def place_food(self):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            pos = (x, y)
            if (pos not in self.snake_body_set and
                pos not in self.static_obstacles and
                pos not in self.dynamic_obstacles):
                self.food = pos
                return

    def place_dynamic_obstacle(self):
        max_attempts = 50
        for _ in range(max_attempts):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            pos = (x, y)
            if pos not in self.snake_body_set and \
               pos not in self.static_obstacles and \
               pos not in self.dynamic_obstacles and \
               pos != self.food:
                self.dynamic_obstacles.add(pos)
                return True
        return False

    def get_valid_neighbors(self, pos):
        neighbors = []
        x, y = pos
        for dx, dy in [UP, DOWN, LEFT, RIGHT]:
            nx, ny = x + dx, y + dy
            new_pos = (nx, ny)
            if 0 <= nx < self.width and 0 <= ny < self.height and \
               new_pos not in self.static_obstacles and \
               new_pos not in self.dynamic_obstacles:
                if new_pos not in self.snake_body_set:
                    neighbors.append(new_pos)
                elif len(self.snake) > 2 and new_pos == self.snake[-1] and new_pos != self.food:
                    neighbors.append(new_pos)
        return neighbors

    def move(self, direction):
        if self.game_over:
            return

        current_head = self.snake[0]
        dx, dy = direction
        new_head = (current_head[0] + dx, current_head[1] + dy)

        self.steps += 1

        if (
           (new_head in self.snake_body_set) or
           (new_head in self.static_obstacles) or
           (new_head in self.dynamic_obstacles) or
           (not (0 <= new_head[0] < self.width and 0 <= new_head[1] < self.height)) or
           (self.steps >= self.max_steps)
        ):
            if new_head in self.snake_body_set: self.game_over_reason = "Self-collision"
            elif new_head in self.static_obstacles: self.game_over_reason = "Hit Static Obstacle"
            elif new_head in self.dynamic_obstacles: self.game_over_reason = "Hit Dynamic Obstacle"
            elif not (0 <= new_head[0] < self.width and 0 <= new_head[1] < self.height): self.game_over_reason = "Hit Wall"
            elif self.steps >= self.max_steps: self.game_over_reason = "Step Limit Reached"
            self.game_over = True
            return

        self.snake.appendleft(new_head)
        self.snake_body_set.add(new_head)

        if new_head == self.food:
            self.score += 1
            self.place_food()

            if self.food_trigger_threshold > 0:
                self.food_eaten_counter += 1
                if self.food_eaten_counter >= self.food_trigger_threshold:
                    num_to_spawn = random.randint(self.obstacle_spawn_min, self.obstacle_spawn_max)
                    for _ in range(num_to_spawn):
                        if not self.place_dynamic_obstacle():
                            break
                    self.food_eaten_counter = 0
        else:
            tail = self.snake.pop()
            self.snake_body_set.remove(tail)


# --- ALGORITMA PATHFINDING ---

def find_path_bfs(game, goal):
    """BFS: Menjamin jalur terpendek, eksplorasi level per level."""
    start = game.snake[0]

    queue = deque([(start, [start])])
    visited = {start}
    nodes_expanded = 0

    while queue:
        nodes_expanded += 1
        current_pos, path = queue.popleft()

        if current_pos == goal:
            return path, nodes_expanded

        for neighbor in game.get_valid_neighbors(current_pos):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))

    return None, nodes_expanded


def find_path_dfs(game, goal):
    """DFS: Tidak menjamin jalur terpendek, eksplorasi secara mendalam (stack-based)."""
    start = game.snake[0]

    stack = [(start, [start])]
    visited = {start}
    nodes_expanded = 0

    while stack:
        nodes_expanded += 1
        current_pos, path = stack.pop()

        if current_pos == goal:
            return path, nodes_expanded

        for neighbor in game.get_valid_neighbors(current_pos):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [neighbor]
                stack.append((neighbor, new_path))

    return None, nodes_expanded


def get_direction_from_path(head, next_step):
    """Mendapatkan vektor arah (dx, dy) dari dua titik."""
    dx = next_step[0] - head[0]
    dy = next_step[1] - head[1]
    return (dx, dy)


def draw_game(screen, game, block_size):
    screen.fill(COLOR_BLACK)

    for (x, y) in game.static_obstacles:
        rect = pygame.Rect(x * block_size + W_PAD, y * block_size + H_PAD,
                           block_size, block_size)
        pygame.draw.rect(screen, COLOR_GRAY, rect)

    for (x, y) in game.dynamic_obstacles:
        rect = pygame.Rect(x * block_size + W_PAD, y * block_size + H_PAD,
                           block_size, block_size)
        pygame.draw.rect(screen, COLOR_GRAY_DYNAMIC, rect)

    if game.food:
        (x, y) = game.food
        rect = pygame.Rect(x * block_size + W_PAD, y * block_size + H_PAD,
                           block_size, block_size)
        pygame.draw.rect(screen, COLOR_RED, rect)

    for (x, y) in list(game.snake)[1:]:
        rect = pygame.Rect(x * block_size + W_PAD, y * block_size + H_PAD,
                           block_size, block_size)
        pygame.draw.rect(screen, COLOR_GREEN, rect)
        pygame.draw.rect(screen, COLOR_GREEN_DARK, rect, 1)

    (x, y) = game.snake[0]
    rect = pygame.Rect(x * block_size + W_PAD, y * block_size + H_PAD,
                       block_size, block_size)
    pygame.draw.rect(screen, COLOR_GREEN_DARK, rect)


def run_simulation(LEVEL, ALGO, config, game_speed_fps=30):

    W, H = config[LEVEL]["size"]
    OBSTACLES = config[LEVEL]["obstacles"]
    FOOD_TRIGGER = config[LEVEL]["food_trigger"]
    SPAWN_COUNT = config[LEVEL]["obstacle_spawn_count"]
    game = SnakeGame(W, H, OBSTACLES, food_trigger=FOOD_TRIGGER, obstacle_spawn_count=SPAWN_COUNT)

    pygame.init()
    SCREEN_WIDTH = W * BLOCK_SIZE + (W_PAD * 2)
    SCREEN_HEIGHT = H * BLOCK_SIZE + (H_PAD * 2)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f"Snake Pathfinding - {ALGO} on {LEVEL} Level")
    clock = pygame.time.Clock()

    total_decision_time = 0
    total_nodes_expanded = 0
    decision_count = 0

    running = True
    current_path_deque = deque()

    while running and not game.game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game.game_over = True
                game.game_over_reason = "User Interruption"

        if not current_path_deque:
            nodes_expanded = 0
            start_time = time.perf_counter()

            if ALGO == "BFS":
                path_to_food, nodes = find_path_bfs(game, game.food)
                nodes_expanded += nodes
                if path_to_food:
                    current_path_deque = deque(path_to_food[1:])
                else:
                    game.game_over = True
                    game.game_over_reason = "No Path Found (Trapped)"

            elif ALGO == "DFS":
                path_to_food, nodes = find_path_dfs(game, game.food)
                nodes_expanded += nodes
                if path_to_food:
                    current_path_deque = deque(path_to_food[1:])
                else:
                    game.game_over = True
                    game.game_over_reason = "No Path Found (Trapped)"

            end_time = time.perf_counter()
            total_decision_time += (end_time - start_time)
            total_nodes_expanded += nodes_expanded
            decision_count += 1

        if current_path_deque:
            next_step = current_path_deque.popleft()
            direction = get_direction_from_path(game.snake[0], next_step)
            game.move(direction)

            if game.game_over_reason == "Hit Dynamic Obstacle":
                current_path_deque.clear()
                game.game_over = False
                game.game_over_reason = ""

        elif not game.game_over:
            game.game_over = True
            game.game_over_reason = "Pathfinding Logic Error"

        draw_game(screen, game, BLOCK_SIZE)
        pygame.display.flip()
        clock.tick(game_speed_fps)

    print(f" Selesai. Makanan: {game.score:<3} | Langkah: {game.steps:<4} | Alasan: {game.game_over_reason}")

    avg_time = 0.0
    avg_expansion = 0.0
    if decision_count > 0:
        avg_time = (total_decision_time / decision_count) * 1000
        avg_expansion = total_nodes_expanded / decision_count

    log_file = 'snake_experiment_log.csv'
    file_exists = os.path.isfile(log_file)
    header = ['Algorithm', 'Level', 'Total Food', 'Total Steps',
              'Average Time (ms)', 'Average Expansion', 'Replans', 'Game Over Reason']
    data_row = [ALGO, LEVEL, game.score, game.steps, f"{avg_time:.4f}",
                f"{avg_expansion:.2f}", decision_count, game.game_over_reason]

    try:
        with open(log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(header)
            writer.writerow(data_row)
    except IOError as e:
        print(f"\n[ERROR] Gagal mencatat data ke CSV: {e}")

    font = pygame.font.SysFont(None, 40)
    text_str = f"GAME OVER: {game.game_over_reason}"
    text = font.render(text_str, True, COLOR_WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    pygame.time.wait(250)
    pygame.quit()

    return game.score, game.steps, avg_time, avg_expansion


def print_comparison(bfs_stats, dfs_stats):
    """Cetak tabel perbandingan BFS vs DFS dan umumkan pemenang tiap kategori."""
    bfs_food  = [s[0] for s in bfs_stats]
    bfs_steps = [s[1] for s in bfs_stats]
    bfs_time  = [s[2] for s in bfs_stats]
    bfs_exp   = [s[3] for s in bfs_stats]

    dfs_food  = [s[0] for s in dfs_stats]
    dfs_steps = [s[1] for s in dfs_stats]
    dfs_time  = [s[2] for s in dfs_stats]
    dfs_exp   = [s[3] for s in dfs_stats]

    avg = lambda lst: sum(lst) / len(lst) if lst else 0

    bfs_avg_food  = avg(bfs_food)
    dfs_avg_food  = avg(dfs_food)
    bfs_avg_steps = avg(bfs_steps)
    dfs_avg_steps = avg(dfs_steps)
    bfs_avg_time  = avg(bfs_time)
    dfs_avg_time  = avg(dfs_time)
    bfs_avg_exp   = avg(bfs_exp)
    dfs_avg_exp   = avg(dfs_exp)

    winner_food  = "BFS" if bfs_avg_food  > dfs_avg_food  else ("DFS" if dfs_avg_food  > bfs_avg_food  else "DRAW")
    winner_steps = "BFS" if bfs_avg_steps < dfs_avg_steps else ("DFS" if dfs_avg_steps < bfs_avg_steps else "DRAW")
    winner_time  = "BFS" if bfs_avg_time  < dfs_avg_time  else ("DFS" if dfs_avg_time  < bfs_avg_time  else "DRAW")
    winner_exp   = "BFS" if bfs_avg_exp   < dfs_avg_exp   else ("DFS" if dfs_avg_exp   < bfs_avg_exp   else "DRAW")

    score_bfs = [winner_food, winner_steps, winner_time, winner_exp].count("BFS")
    score_dfs = [winner_food, winner_steps, winner_time, winner_exp].count("DFS")
    overall   = "BFS" if score_bfs > score_dfs else ("DFS" if score_dfs > score_bfs else "DRAW")

    sep = "=" * 62
    print(f"\n{sep}")
    print(f"{'  HASIL PERBANDINGAN BFS vs DFS':^62}")
    print(sep)
    print(f"  {'Metrik':<22} {'BFS':>10} {'DFS':>10} {'Pemenang':>12}")
    print("-" * 62)
    print(f"  {'Rata-rata Makanan':<22} {bfs_avg_food:>10.1f} {dfs_avg_food:>10.1f} {winner_food:>12}")
    print(f"  {'Rata-rata Langkah':<22} {bfs_avg_steps:>10.1f} {dfs_avg_steps:>10.1f} {winner_steps:>12}")
    print(f"  {'Rata-rata Waktu (ms)':<22} {bfs_avg_time:>10.4f} {dfs_avg_time:>10.4f} {winner_time:>12}")
    print(f"  {'Rata-rata Ekspansi':<22} {bfs_avg_exp:>10.1f} {dfs_avg_exp:>10.1f} {winner_exp:>12}")
    print("-" * 62)
    print(f"  {'Poin Kategori':<22} {score_bfs:>10} {score_dfs:>10}")
    print(sep)
    if overall == "DRAW":
        print(f"  >>> HASIL IMBANG! BFS dan DFS seimbang di batch ini.")
    else:
        print(f"  >>> PEMENANG BATCH INI: *** {overall} *** ({score_bfs if overall=='BFS' else score_dfs}/4 kategori)")
    print(sep + "\n")


if __name__ == "__main__":

    valid_levels = ["Easy", "Medium", "Hard"]
    while True:
        level_input = input(f"Pilih Level Eksperimen ({'/'.join(valid_levels)}): ").capitalize()
        if level_input in valid_levels:
            LEVEL = level_input
            break
        print(f"Input tidak valid. Harap pilih salah satu dari: {', '.join(valid_levels)}")

    # Level Easy: Tanpa obstacle
    W_easy = 15
    obs_easy = set()

    # Level Medium: Dua Pilar Vertikal
    obs_medium = set()
    x_kiri, x_kanan = 6, 13
    y_start, y_end = 5, 14
    for i in range(y_start, y_end + 1):
        obs_medium.add((x_kiri, i))
        obs_medium.add((x_kanan, i))

    # Level Hard: Plus (+) shape, arm length 6
    obs_hard = set()
    center_h, arm_h = 12, 6
    obs_hard.add((center_h, center_h))
    for i in range(1, arm_h + 1):
        obs_hard.add((center_h, center_h - i))
        obs_hard.add((center_h, center_h + i))
        obs_hard.add((center_h - i, center_h))
        obs_hard.add((center_h + i, center_h))

    config = {
        "Easy": {
            "size": (W_easy, W_easy),
            "obstacles": obs_easy,
            "food_trigger": 0,
            "obstacle_spawn_count": (0, 0)
        },
        "Medium": {
            "size": (20, 20),
            "obstacles": obs_medium,
            "food_trigger": 7,
            "obstacle_spawn_count": (1, 2)
        },
        "Hard": {
            "size": (25, 25),
            "obstacles": obs_hard,
            "food_trigger": 5,
            "obstacle_spawn_count": (1, 5)
        }
    }

    while True:
        print("\n" + "="*30)
        print(f"Menjalankan Batch (Level: {LEVEL})")
        print("="*30)

        bfs_stats = []
        print("Menjalankan 5x BFS...")
        for i in range(5):
            print(f"  [BFS Run {i+1}/5]...", end="", flush=True)
            bfs_stats.append(run_simulation(LEVEL, "BFS", config, game_speed_fps=70))

        dfs_stats = []
        print("\nMenjalankan 5x DFS...")
        for i in range(5):
            print(f"  [DFS Run {i+1}/5]...", end="", flush=True)
            dfs_stats.append(run_simulation(LEVEL, "DFS", config, game_speed_fps=70))

        print("="*30)
        print_comparison(bfs_stats, dfs_stats)

        lanjut = ""
        while lanjut not in ['y', 'n']:
            lanjut = input("Batch 10 run selesai. Lanjut 10 run lagi? (y/n): ").lower()

        if lanjut == 'n':
            break

    print("\nSimulasi selesai.")
