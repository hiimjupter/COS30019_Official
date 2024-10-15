# Last modified: 2024-10-15, 16:10

# import pygame
# import sys
# import time
# import math
# from grid import Grid
# from algorithm import Search
# from constant import COLORS, MAZE, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, BUTTON_WIDTH, BUTTON_HEIGHT, SMALL_FONT, MEDIUM_FONT, LARGE_FONT, MOVE_FONT
# from button import Button


# def load_map(filename):
#     with open(filename, 'r') as f:
#         lines = f.readlines()
#         dimension = eval(lines[0].strip())
#         initial_state = eval(lines[1].strip())
#         goal_states = [eval(goal.strip()) for goal in lines[2].split('|')]
#         barriers = [eval(barrier.strip()) for barrier in lines[3:]]

#     # Swap row and column for initial_state
#     initial_state = (initial_state[1], initial_state[0])

#     # Swap row and column for each goal_state
#     goal_states = [(goal[1], goal[0]) for goal in goal_states]

#     return dimension, initial_state, goal_states, barriers


# def initialize_game():
#     pygame.init()
#     pygame.display.set_caption("Robot Navigation Problem")
#     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#     return screen


# def render_title(screen):
#     title = LARGE_FONT.render("Robot Navigation", True, COLORS['WHITE'])
#     title_rect = title.get_rect(center=((SCREEN_WIDTH / 2), 50))
#     screen.blit(title, title_rect)


# def execute_search(search, algorithm):
#     start_time = time.time()
#     result = search.search(algorithm=algorithm)
#     end_time = time.time()
#     duration = end_time - start_time

#     path = result.strip(";").split("; ")

#     if not path or all(x.isspace() for x in path):
#         path_output = "No Path Found"
#     else:
#         path_output = ', '.join(path)

#     expanded_nodes = search.get_expanded_movement()
#     num_expanded_nodes = len(expanded_nodes)

#     return path, path_output, duration, expanded_nodes, num_expanded_nodes


# def navigate_path(screen, grid, num_expanded_nodes, expanded_nodes, path, algorithm, goal_states, barriers):
#     path_drawn = False
#     goal_found = set()
#     running = True

#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#         screen.fill(COLORS['WHITE'])

#         if not path_drawn:
#             grid.draw_path(screen, path, expanded_nodes)
#             path_drawn = True
#             pygame.time.delay(5000)

#             current_position = grid.initial_state
#             for direction in path:
#                 move = get_move_from_direction(direction)
#                 if move:
#                     current_position = (
#                         current_position[0] + move[0], current_position[1] + move[1])

#             if current_position in goal_states:
#                 goal_found = current_position
#                 running = False

#         pygame.display.flip()

#     # Reswap to match map format
#     goal_found = (goal_found[1], goal_found[0])

#     return get_algorithm_name(algorithm), goal_found


# def get_move_from_direction(direction):
#     if direction == 'up':
#         return (-1, 0)
#     elif direction == 'left':
#         return (0, -1)
#     elif direction == 'down':
#         return (1, 0)
#     elif direction == 'right':
#         return (0, 1)
#     return None


# def get_algorithm_name(algorithm):
#     if algorithm == 'bfs':
#         return 'Breadth First Search'
#     return None


# def main():
#     # Initialize the game
#     pygame.init()
#     pygame.display.set_caption("Robot Navigation Problem")

#     running = True
#     while running:
#         # Load map and get initial data
#         dimension, initial_state, goal_states, barriers = load_map(MAZE)
#         rows, columns = dimension

#         # Reset grid and search
#         grid = Grid(rows, columns, CELL_SIZE,
#                     initial_state, goal_states, barriers)
#         search = Search(grid)

#         # Reset screen to initial screen size
#         screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#         # Initialize buttons with the current screen
#         BFS_button = Button(screen, (((SCREEN_WIDTH // 2) - BUTTON_WIDTH * 2),
#                             (SCREEN_HEIGHT // 2), BUTTON_WIDTH, BUTTON_HEIGHT), "BFS")
#         Quit_button = Button(screen, (((SCREEN_WIDTH // 2) + BUTTON_WIDTH),
#                              (SCREEN_HEIGHT // 2), BUTTON_WIDTH, BUTTON_HEIGHT), "Quit")

#         screen.fill(COLORS['BLUE'])
#         render_title(screen)
#         BFS_button.render()
#         Quit_button.render()
#         pygame.display.flip()

#         choose = True
#         algorithm = None

#         while choose:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
#                     choose = False
#                 elif event.type == pygame.MOUSEBUTTONDOWN:
#                     mouse_pos = pygame.mouse.get_pos()
#                     if BFS_button.is_clicked(mouse_pos):
#                         algorithm = 'bfs'
#                         choose = False
#                     elif Quit_button.is_clicked(mouse_pos):
#                         running = False
#                         choose = False

#         if algorithm:
#             path, path_output, duration, expanded_nodes, num_expanded_nodes = execute_search(
#                 search, algorithm)
#             DISPLAY_WIDTH, DISPLAY_HEIGHT = columns * CELL_SIZE, rows * CELL_SIZE
#             screen = pygame.display.set_mode(
#                 (DISPLAY_WIDTH, DISPLAY_HEIGHT))
#             algorithm, goal_found = navigate_path(screen, grid, num_expanded_nodes, expanded_nodes, path,
#                                                   algorithm, goal_states, barriers)

#             print('--------Results---------')
#             print(f'Algorithm: {algorithm}')
#             print(f'Goals Found: {goal_found}')
#             print(f'Path: {path_output}')
#             print(f'Duration: {duration} seconds')

#     pygame.quit()


# if __name__ == "__main__":
#     main()
