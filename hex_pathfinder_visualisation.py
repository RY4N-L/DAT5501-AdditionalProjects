import math
import sys
import pygame
from collections import deque
import heapq

# ------------------------------
# Config
# ------------------------------
WIDTH, HEIGHT = 1000, 800
BG_COLOR = (25, 28, 35)
GRID_MARGIN = 30

HEX_SIZE = 22  # radius of hex
GRID_COLS = 24  # axial q range
GRID_ROWS = 16  # axial r range
POINTY_TOP = True  # hex orientation

# Colors
COLOR_EMPTY = (210, 214, 220)
COLOR_WALL = (60, 65, 75)
COLOR_START = (80, 200, 120)
COLOR_END = (255, 120, 120)
COLOR_FRONTIER = (255, 198, 109)
COLOR_VISITED = (120, 160, 255)
COLOR_PATH = (255, 255, 120)
COLOR_TEXT = (220, 225, 235)
COLOR_GRID = (80, 85, 95)

# ------------------------------
# Hex math (axial coordinates)
# ------------------------------
# Axial coord: (q, r)
NEIGHBOR_DIRS = [(+1, 0), (+1, -1), (0, -1), (-1, 0), (-1, +1), (0, +1)]

def axial_to_pixel(q, r, size, origin=(0, 0), pointy=True):
    if pointy:
        x = size * (math.sqrt(3) * q + math.sqrt(3)/2 * r)
        y = size * (3/2 * r)
    else:
        x = size * (3/2 * q)
        y = size * (math.sqrt(3)/2 * q + math.sqrt(3) * r)
    return (origin[0] + x, origin[1] + y)

def polygon_corners(q, r, size, origin=(0, 0), pointy=True):
    center = axial_to_pixel(q, r, size, origin, pointy)
    corners = []
    for i in range(6):
        angle = math.pi/180 * (60 * i - (30 if pointy else 0))
        x = center[0] + size * math.cos(angle)
        y = center[1] + size * math.sin(angle)
        corners.append((x, y))
    return corners

def hex_distance(a, b):
    aq, ar = a
    bq, br = b
    # convert axial to cube: x=q, z=r, y=-x-z
    ax, az = aq, ar
    ay = -ax - az
    bx, bz = bq, br
    by = -bx - bz
    return max(abs(ax - bx), abs(ay - by), abs(az - bz))

# ------------------------------
# Grid and cell types
# ------------------------------
EMPTY, WALL, START, END = "empty", "wall", "start", "end"

class HexGrid:
    def __init__(self, cols, rows, size, margin, pointy=True):
        self.cols = cols
        self.rows = rows
        self.size = size
        self.pointy = pointy
        self.margin = margin

        # compute origin to center grid
        self.origin = self.compute_origin()

        # grid state: dict[(q, r)] -> type
        self.cells = {}
        for q in range(cols):
            for r in range(rows):
                self.cells[(q, r)] = EMPTY

        self.start = None
        self.end = None

        # algorithm state
        self.frontier = set()
        self.visited = set()
        self.path = []

    def compute_origin(self):
        # approximate grid bounding box and center it
        if self.pointy:
            width_px = self.size * (math.sqrt(3) * self.cols + math.sqrt(3)/2 * (self.rows - 1))
            height_px = self.size * (3/2 * (self.rows - 1)) + 2*self.size
        else:
            width_px = self.size * (3/2 * (self.cols - 1)) + 2*self.size
            height_px = self.size * (math.sqrt(3)/2 * (self.cols - 1) + math.sqrt(3) * self.rows)
        ox = (WIDTH - width_px) / 2
        oy = (HEIGHT - height_px) / 2
        return (ox, oy)

    def in_bounds(self, q, r):
        return 0 <= q < self.cols and 0 <= r < self.rows

    def neighbors(self, q, r):
        for dq, dr in NEIGHBOR_DIRS:
            nq, nr = q + dq, r + dr
            if self.in_bounds(nq, nr) and self.cells[(nq, nr)] != WALL:
                yield (nq, nr)

    def reset_algo_state(self):
        self.frontier.clear()
        self.visited.clear()
        self.path = []

    def reset_all(self):
        for k in list(self.cells.keys()):
            self.cells[k] = EMPTY
        self.start = None
        self.end = None
        self.reset_algo_state()

    def set_start_or_end(self, q, r):
        if self.cells[(q, r)] == WALL:
            return
        if self.start is None:
            self.start = (q, r)
            self.cells[(q, r)] = START
        elif self.end is None and (q, r) != self.start:
            self.end = (q, r)
            self.cells[(q, r)] = END
        else:
            # toggle wall after both set
            self.toggle_wall(q, r)

    def toggle_wall(self, q, r):
        if (q, r) == self.start or (q, r) == self.end:
            return
        self.cells[(q, r)] = WALL if self.cells[(q, r)] != WALL else EMPTY

    def clear_cell(self, q, r):
        if (q, r) == self.start:
            self.start = None
        if (q, r) == self.end:
            self.end = None
        self.cells[(q, r)] = EMPTY

    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(current)
        path.reverse()
        return path

    def draw(self, screen, font):
        screen.fill(BG_COLOR)
        # draw grid
        for (q, r), state in self.cells.items():
            corners = polygon_corners(q, r, self.size, self.origin, self.pointy)
            color = COLOR_EMPTY
            if state == WALL:
                color = COLOR_WALL
            elif state == START:
                color = COLOR_START
            elif state == END:
                color = COLOR_END

            # overlay states
            if (q, r) in self.visited and state not in (START, END):
                color = COLOR_VISITED
            if (q, r) in self.frontier and state not in (START, END):
                color = COLOR_FRONTIER
            if (q, r) in self.path and state not in (START, END):
                color = COLOR_PATH

            pygame.draw.polygon(screen, color, corners)
            pygame.draw.polygon(screen, COLOR_GRID, corners, width=1)

        # HUD text
        lines = [
            "Left click: set start then end; then toggle walls",
            "Right click: toggle wall | Middle click: clear cell",
            "A: A* | D: Dijkstra | F: DFS | C: Clear algo | R: Reset | Esc/Q: Quit",
        ]
        y = 6
        for s in lines:
            text = font.render(s, True, COLOR_TEXT)
            screen.blit(text, (10, y))
            y += text.get_height() + 2

# ------------------------------
# Algorithms (generators for visualization)
# ------------------------------
def algo_astar(grid: HexGrid):
    if grid.start is None or grid.end is None:
        return
    start, goal = grid.start, grid.end
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {start: 0}
    seen_frontier = set([start])
    grid.reset_algo_state()

    while frontier:
        _, current = heapq.heappop(frontier)
        seen_frontier.discard(current)

        if current == goal:
            grid.path = grid.reconstruct_path(came_from, current)
            yield "done"
            return

        grid.visited.add(current)
        grid.frontier = set(seen_frontier)
        yield current

        cq, cr = current
        for nq, nr in grid.neighbors(cq, cr):
            new_cost = cost_so_far[current] + 1  # uniform cost
            if (nq, nr) not in cost_so_far or new_cost < cost_so_far[(nq, nr)]:
                cost_so_far[(nq, nr)] = new_cost
                priority = new_cost + hex_distance((nq, nr), goal)
                heapq.heappush(frontier, (priority, (nq, nr)))
                seen_frontier.add((nq, nr))
                came_from[(nq, nr)] = current

    yield "fail"

def algo_dijkstra(grid: HexGrid):
    if grid.start is None or grid.end is None:
        return
    start, goal = grid.start, grid.end
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {start: 0}
    seen_frontier = set([start])
    grid.reset_algo_state()

    while frontier:
        cost, current = heapq.heappop(frontier)
        seen_frontier.discard(current)

        if current == goal:
            grid.path = grid.reconstruct_path(came_from, current)
            yield "done"
            return

        grid.visited.add(current)
        grid.frontier = set(seen_frontier)
        yield current

        cq, cr = current
        for nq, nr in grid.neighbors(cq, cr):
            new_cost = cost + 1  # uniform weight
            if (nq, nr) not in cost_so_far or new_cost < cost_so_far[(nq, nr)]:
                cost_so_far[(nq, nr)] = new_cost
                heapq.heappush(frontier, (new_cost, (nq, nr)))
                seen_frontier.add((nq, nr))
                came_from[(nq, nr)] = current

    yield "fail"

def algo_dfs(grid: HexGrid):
    if grid.start is None or grid.end is None:
        return
    start, goal = grid.start, grid.end
    stack = [start]
    came_from = {}
    seen = set([start])
    grid.reset_algo_state()

    while stack:
        current = stack.pop()
        if current == goal:
            grid.path = grid.reconstruct_path(came_from, current)
            yield "done"
            return

        grid.visited.add(current)
        grid.frontier = set(stack)
        yield current

        cq, cr = current
        for nq, nr in grid.neighbors(cq, cr):
            if (nq, nr) not in seen:
                seen.add((nq, nr))
                came_from[(nq, nr)] = current
                stack.append((nq, nr))

    yield "fail"

# ------------------------------
# Picking hex from mouse position
# ------------------------------
def pixel_to_axial(x, y, size, origin, pointy=True):
    # inverse of axial_to_pixel using standard formulas
    # Convert screen pixel to local coordinates
    lx = x - origin[0]
    ly = y - origin[1]
    if pointy:
        q = (math.sqrt(3)/3 * lx - 1/3 * ly) / size
        r = (2/3 * ly) / size
    else:
        q = (2/3 * lx) / size
        r = (-1/3 * lx + math.sqrt(3)/3 * ly) / size

    # round to nearest hex (cube rounding)
    x_c = q
    z_c = r
    y_c = -x_c - z_c

    rx = round(x_c)
    ry = round(y_c)
    rz = round(z_c)

    x_diff = abs(rx - x_c)
    y_diff = abs(ry - y_c)
    z_diff = abs(rz - z_c)

    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry - rz
    elif y_diff > z_diff:
        ry = -rx - rz
    else:
        rz = -rx - ry

    q_hex, r_hex = int(rx), int(rz)
    return (q_hex, r_hex)

# ------------------------------
# Main app
# ------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hex Pathfinding Visualizer (A*, Dijkstra, DFS)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 18)

    grid = HexGrid(GRID_COLS, GRID_ROWS, HEX_SIZE, GRID_MARGIN, POINTY_TOP)

    running_algo = None  # generator
    algo_speed_ms = 25   # delay between steps

    last_step_time = 0

    while True:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    running_algo = None
                    grid.reset_all()
                elif event.key == pygame.K_c:
                    running_algo = None
                    grid.reset_algo_state()
                elif event.key == pygame.K_a:
                    running_algo = algo_astar(grid)
                elif event.key == pygame.K_d:
                    running_algo = algo_dijkstra(grid)
                elif event.key == pygame.K_f:
                    running_algo = algo_dfs(grid)

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                q, r = pixel_to_axial(x, y, grid.size, grid.origin, grid.pointy)
                if grid.in_bounds(q, r):
                    if event.button == 1:
                        grid.set_start_or_end(q, r)
                        running_algo = None
                        grid.reset_algo_state()
                    elif event.button == 3:
                        grid.toggle_wall(q, r)
                        running_algo = None
                        grid.reset_algo_state()
                    elif event.button == 2:
                        grid.clear_cell(q, r)
                        running_algo = None
                        grid.reset_algo_state()

        # step algorithm
        if running_algo is not None:
            now = pygame.time.get_ticks()
            if now - last_step_time >= algo_speed_ms:
                last_step_time = now
                try:
                    next(running_algo)
                except StopIteration:
                    running_algo = None

        grid.draw(screen, font)
        pygame.display.flip()

if __name__ == "__main__":
    main()

