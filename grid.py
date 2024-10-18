import pygame
from helpers.constant import COLORS, EXPANDED_DELAY, SCREEN_DELAY
from helpers.utils import get_move_from_direction


class Grid:
    def __init__(self, rows, columns, cell_size, initial_state, goal_states, barriers):
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
        self.initial_state = initial_state
        self.goal_states = goal_states
        self.barriers = barriers

    def reset(self, screen):
        rects = []
        for i in range(self.rows):
            for j in range(self.columns):
                color = COLORS['WHITE']
                if (i, j) == self.initial_state:
                    color = COLORS['RED']
                elif (i, j) in self.goal_states:
                    color = COLORS['GREEN']

                rect = pygame.Rect(j * self.cell_size, i *
                                   self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, color, rect)
                rects.append(rect)

        for barrier in self.barriers:
            x, y, width, height = barrier
            rect = pygame.Rect(x * self.cell_size, y * self.cell_size,
                               width * self.cell_size, height * self.cell_size)
            pygame.draw.rect(screen, COLORS['GRAY'], rect)
            rects.append(rect)

        for i in range(self.rows):
            for j in range(self.columns):
                rect = pygame.Rect(j * self.cell_size, i *
                                   self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, COLORS['BLACK'], rect, 1)
                rects.append(rect)

        return rects

    def draw_paths(self, screen, paths, expanded_nodes, delay=EXPANDED_DELAY, nodes_per_iteration=1):
        rects = self.reset(screen)
        pygame.display.update(rects)

        visited_nodes = set()
        search_surface = pygame.Surface(
            (self.columns * self.cell_size, self.rows * self.cell_size), pygame.SRCALPHA)

        while expanded_nodes:
            updated_rects = []

            chunk, expanded_nodes = expanded_nodes[:
                                                   nodes_per_iteration], expanded_nodes[nodes_per_iteration:]

            for node in chunk:
                if node in visited_nodes:
                    continue

                if node == self.initial_state:
                    continue  # Skip coloring the initial state

                visited_nodes.add(node)

                vx, vy = node
                rect = pygame.Rect(vy * self.cell_size, vx *
                                   self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(search_surface, COLORS['ORANGE'], rect)
                updated_rects.append(rect)

                # Update the display and delay after each node is explored
                screen.blit(search_surface, (0, 0))
                pygame.display.update(updated_rects)
                pygame.time.delay(delay)

        # Delay before drawing the paths (solutions)
        pygame.time.delay(SCREEN_DELAY)

        # Reset
        rects = self.reset(screen)
        pygame.display.update(rects)

        # Start Drawing Paths
        previous_path = []
        for path in paths:
            current_position = self.initial_state

            # Find the divergence point
            for i, direction in enumerate(path):
                if i < len(previous_path) and direction == previous_path[i]:
                    move = get_move_from_direction(direction)
                    if move:
                        current_position = (
                            current_position[0] + move[0], current_position[1] + move[1])
                else:
                    break

            # Draw the remaining path from the divergence point
            for direction in path[i:]:
                move = get_move_from_direction(direction)
                if move:
                    current_position = (
                        current_position[0] + move[0], current_position[1] + move[1])
                    rect = pygame.Rect(
                        current_position[1] * self.cell_size, current_position[0] * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, COLORS['BLUE'], rect)
                    pygame.display.update([rect])
                    pygame.time.delay(delay)

            previous_path = path
