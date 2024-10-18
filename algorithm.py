import math
from queue import Queue


class Search:
    def __init__(self, grid):
        self.grid = grid
        self.visited = set()  # With repeated check
        self.expanded_movement = []
        self.path = []
        self.heuristic_name = "Manhattan"

    def get_visited_nodes(self):
        return self.visited

    def get_expanded_movement(self):
        return self.expanded_movement

    def is_valid(self, position):
        row, column = position

        # Check if the position is outside the bounds of the grid
        if row < 0 or row >= self.grid.rows or column < 0 or column >= self.grid.columns:
            return False

        # Check if the position is inside a wall
        for barrier in self.grid.barriers:
            x, y, width, height = barrier
            if column >= x and column < x + width and row >= y and row < y + height:
                return False

        return True

    def get_neighbors(self, position):
        row, col = position
        neighbors = [
            (row - 1, col),  # up
            (row, col - 1),  # left
            (row + 1, col),  # down
            (row, col + 1),  # right
        ]

        valid_neighbors = []
        for neighbor in neighbors:
            if self.is_valid(neighbor):
                # print("Here is the current Neighbor: ", neighbor)
                valid_neighbors.append(neighbor)

        return valid_neighbors

    def update_heuristic(self, new_heuristic):
        if new_heuristic in ['Manhattan', "Euclidean"]:
            self.heuristic_name = new_heuristic

    def heuristic(self, position, goal):
        if self.heuristic_name == "Manhattan":
            return self.manhattan_distance(position, goal)
        elif self.heuristic_name == "Euclidean":
            return self.euclidean_distance(position, goal)

    def manhattan_distance(self, position, goal):
        x = abs(position[0] - goal[0])
        y = abs(position[1] - goal[1])

        return x + y

    def euclidean_distance(self, position, goal):
        x = math.pow((position[0] - goal[0]), 2)
        y = math.pow((position[1] - goal[1]), 2)
        return math.sqrt(x + y)

    def bfs(self):
        self.visited.clear()
        self.expanded_movement.clear()
        start = self.grid.initial_state
        queue = Queue()
        queue.put((start, []))
        found_goals = set()
        paths_to_goals = []

        while not queue.empty() and len(found_goals) < len(self.grid.goal_states):
            position, path = queue.get()

            if position in self.visited:
                continue

            self.visited.add(position)
            self.expanded_movement.append(position)

            if position in self.grid.goal_states and position not in found_goals:
                found_goals.add(position)
                paths_to_goals.append(path)

            for neighbor in self.get_neighbors(position):
                direction = (neighbor[0] - position[0],
                             neighbor[1] - position[1])
                direction_map = {
                    (-1, 0): 'up',
                    (0, -1): 'left',
                    (1, 0): 'down',
                    (0, 1): 'right'
                }
                move_direction = direction_map[direction]
                queue.put((neighbor, path + [move_direction]))

        if len(found_goals) == len(self.grid.goal_states):
            self.path = paths_to_goals
            return paths_to_goals
        else:
            return "No path found."

    def dfs(self):
        self.visited.clear()
        self.expanded_movement.clear()
        start = self.grid.initial_state
        stack = [(start, [])]
        found_goals = set()
        paths_to_goals = []

        while stack and len(found_goals) < len(self.grid.goal_states):
            position, path = stack.pop()

            if position in self.visited:
                continue

            self.visited.add(position)
            self.expanded_movement.append(position)

            if position in self.grid.goal_states and position not in found_goals:
                found_goals.add(position)
                paths_to_goals.append(path)

            for neighbor in reversed(self.get_neighbors(position)):
                direction = (neighbor[0] - position[0],
                             neighbor[1] - position[1])
                direction_map = {
                    (-1, 0): 'up',
                    (0, -1): 'left',
                    (1, 0): 'down',
                    (0, 1): 'right'
                }
                move_direction = direction_map[direction]
                stack.append((neighbor, path + [move_direction]))

        if len(found_goals) == len(self.grid.goal_states):
            self.path = paths_to_goals
            return paths_to_goals
        else:
            return "No path found."

    def gbfs(self):
        self.visited.clear()
        self.expanded_movement.clear()
        start = self.grid.initial_state
        goals = self.grid.goal_states
        queue = Queue()
        queue.put((start, []))
        found_goals = set()
        paths_to_goals = []

        while not queue.empty() and len(found_goals) < len(goals):
            position, path = queue.get()

            if position in self.visited:
                continue

            self.visited.add(position)
            self.expanded_movement.append(position)

            if position in goals and position not in found_goals:
                found_goals.add(position)
                paths_to_goals.append(path)

            neighbors = self.get_neighbors(position)
            neighbors.sort(key=lambda neighbor: min(
                self.heuristic(neighbor, goal) for goal in goals))
            for neighbor in neighbors:
                direction = (neighbor[0] - position[0],
                             neighbor[1] - position[1])
                direction_map = {
                    (-1, 0): 'up',
                    (0, -1): 'left',
                    (1, 0): 'down',
                    (0, 1): 'right'
                }
                move_direction = direction_map[direction]
                queue.put((neighbor, path + [move_direction]))

        if len(found_goals) == len(goals):
            self.path = paths_to_goals
            return paths_to_goals
        else:
            return "No path found."

    def a_star(self):
        self.visited.clear()
        self.expanded_movement.clear()
        start = self.grid.initial_state
        goals = self.grid.goal_states
        open_set = Queue()
        open_set.put((start, []))
        g_costs = {start: 0}
        f_costs = {start: min(self.heuristic(start, goal) for goal in goals)}
        found_goals = set()
        paths_to_goals = []

        while not open_set.empty() and len(found_goals) < len(goals):
            current, path = open_set.get()

            if current in self.visited:
                continue

            self.visited.add(current)
            self.expanded_movement.append(current)

            if current in goals and current not in found_goals:
                found_goals.add(current)
                paths_to_goals.append(path)

            for neighbor in self.get_neighbors(current):
                tentative_g_cost = g_costs[current] + 1
                if neighbor not in g_costs or tentative_g_cost < g_costs[neighbor]:
                    g_costs[neighbor] = tentative_g_cost
                    f_costs[neighbor] = tentative_g_cost + \
                        min(self.heuristic(neighbor, goal) for goal in goals)
                    direction = (neighbor[0] - current[0],
                                 neighbor[1] - current[1])
                    direction_map = {
                        (-1, 0): 'up',
                        (0, -1): 'left',
                        (1, 0): 'down',
                        (0, 1): 'right'
                    }
                    move_direction = direction_map[direction]
                    open_set.put((neighbor, path + [move_direction]))

        if len(found_goals) == len(goals):
            self.path = paths_to_goals
            return paths_to_goals
        else:
            return "No path found."

    def ids(self):
        self.visited.clear()
        self.expanded_movement.clear()

        def dls(position, path, depth):
            if depth == 0 and position in self.grid.goal_states:
                self.path = path
                return True
            if depth > 0:
                self.visited.add(position)
                self.expanded_movement.append(position)
                for neighbor in self.get_neighbors(position):
                    if neighbor not in self.visited:
                        direction = (
                            neighbor[0] - position[0], neighbor[1] - position[1])
                        direction_map = {
                            (-1, 0): 'up',
                            (0, -1): 'left',
                            (1, 0): 'down',
                            (0, 1): 'right'
                        }
                        move_direction = direction_map[direction]
                        if dls(neighbor, path + [move_direction], depth - 1):
                            return True
                self.visited.remove(position)
            return False

        start = self.grid.initial_state
        depth = 0
        while True:
            self.visited.clear()
            self.expanded_movement.clear()
            if dls(start, [], depth):
                return '; '.join(self.path) + ';'
            depth += 1
            if depth > self.grid.rows * self.grid.columns:
                break

        return "No path found."

    def iterative_deepening_a_star(self):
        self.visited.clear()
        self.expanded_movement.clear()

        def ida_star_recursive(node, path, g_cost, threshold):
            f_cost = g_cost + min(self.heuristic(node, goal)
                                  for goal in self.grid.goal_states)
            if f_cost > threshold:
                return f_cost, None
            if node in self.grid.goal_states:
                self.path = path
                return f_cost, path
            min_threshold = float('inf')
            self.visited.add(node)
            self.expanded_movement.append(node)
            for neighbor in self.get_neighbors(node):
                if neighbor not in self.visited:
                    direction = (neighbor[0] - node[0], neighbor[1] - node[1])
                    direction_map = {
                        (-1, 0): 'up',
                        (0, -1): 'left',
                        (1, 0): 'down',
                        (0, 1): 'right'
                    }
                    move_direction = direction_map[direction]
                    temp_threshold, result_path = ida_star_recursive(
                        neighbor, path + [move_direction], g_cost + 1, threshold)
                    if result_path is not None:
                        return temp_threshold, result_path
                    min_threshold = min(min_threshold, temp_threshold)
            self.visited.remove(node)
            return min_threshold, None

        start = self.grid.initial_state
        threshold = min(self.heuristic(start, goal)
                        for goal in self.grid.goal_states)
        while True:
            self.visited.clear()
            self.expanded_movement.clear()
            temp_threshold, result_path = ida_star_recursive(
                start, [], 0, threshold)
            if result_path is not None:
                return '; '.join(result_path) + ';'
            if temp_threshold == float('inf'):
                break
            threshold = temp_threshold

        return "No path found."

    def search(self, algorithm='bfs'):
        if algorithm == 'bfs':
            return self.bfs()
        elif algorithm == 'dfs':
            return self.dfs()
        elif algorithm == 'gbfs':
            return self.gbfs()
        elif algorithm == 'a_star':
            return self.a_star()
        elif algorithm == 'cus_1':
            return self.ids()
        elif algorithm == 'cus_2':
            return self.iterative_deepening_a_star()
        return None
