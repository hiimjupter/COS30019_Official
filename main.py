import pygame
import time
import math
from grid import Grid
from algorithm import Search
from helpers.constant import COLORS, SCREEN_DELAY, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, BUTTON_WIDTH, BUTTON_HEIGHT, SMALL_FONT, MEDIUM_FONT, LARGE_FONT
from helpers.button import Button
from helpers.utils import get_move_from_direction, get_algorithm_name, load_map


def initialize_game():
    pygame.init()
    pygame.display.set_caption("Robot Navigation Problem")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    return screen


def render_title(screen):
    title = LARGE_FONT.render("Robot Navigation", True, COLORS['WHITE'])
    title_rect = title.get_rect(center=((SCREEN_WIDTH / 2), 50))
    screen.blit(title, title_rect)


def execute_search(search, algorithm):
    start_time = time.time()
    result = search.search(algorithm=algorithm)
    end_time = time.time()
    duration = round(end_time - start_time, 5)

    path = result.strip(";").split("; ")

    if not path or all(x.isspace() for x in path):
        path_output = "No Path Found"
    else:
        path_output = ', '.join(path)

    expanded_nodes = search.get_expanded_movement()
    num_expanded_nodes = len(expanded_nodes)

    return path, path_output, duration, expanded_nodes, num_expanded_nodes


def navigate_path(screen, grid, num_expanded_nodes, expanded_nodes, path, algorithm, goal_states):
    path_drawn = False
    goal_found = set()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(COLORS['WHITE'])

        if not path_drawn:
            grid.draw_path(screen, path, expanded_nodes)
            path_drawn = True
            pygame.time.delay(SCREEN_DELAY)

            goal_found = get_goal(grid, path)
            if goal_found:
                running = False

        pygame.display.flip()

    return get_algorithm_name(algorithm), goal_found


def get_goal(grid, path):
    current_position = grid.initial_state
    for direction in path:
        move = get_move_from_direction(direction)
        if move:
            current_position = (
                current_position[0] + move[0], current_position[1] + move[1])
    if current_position in grid.goal_states:
        return (current_position[1], current_position[0])


def main():
    # Initialize the game
    pygame.init()
    pygame.display.set_caption("Robot Navigation Problem")

    running = True
    while running:
        # Create screen for maze selection
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Create maze selection buttons
        Maze1_button = Button(screen, (((SCREEN_WIDTH // 2) - BUTTON_WIDTH * 2),
                                       (SCREEN_HEIGHT // 2), BUTTON_WIDTH, BUTTON_HEIGHT), "Maze 1")
        Maze2_button = Button(screen, (((SCREEN_WIDTH // 2) - BUTTON_WIDTH // 2),
                                       (SCREEN_HEIGHT // 2), BUTTON_WIDTH, BUTTON_HEIGHT), "Maze 2")
        Maze3_button = Button(screen, (((SCREEN_WIDTH // 2) + BUTTON_WIDTH),
                                       (SCREEN_HEIGHT // 2), BUTTON_WIDTH, BUTTON_HEIGHT), "Maze 3")
        Quit_button = Button(screen, (((SCREEN_WIDTH // 2) - BUTTON_WIDTH // 2),
                                      (SCREEN_HEIGHT // 2) + BUTTON_HEIGHT * 2, BUTTON_WIDTH, BUTTON_HEIGHT), "Quit")

        screen.fill(COLORS['BLUE'])
        render_title(screen)
        Maze1_button.render()
        Maze2_button.render()
        Maze3_button.render()
        Quit_button.render()
        pygame.display.flip()

        choosing_maze = True
        MAZE = None

        while choosing_maze:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    choosing_maze = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if Maze1_button.is_clicked(mouse_pos):
                        MAZE = 'maps/maze1.txt'
                        choosing_maze = False
                    elif Maze2_button.is_clicked(mouse_pos):
                        MAZE = 'maps/maze2.txt'
                        choosing_maze = False
                    elif Maze3_button.is_clicked(mouse_pos):
                        MAZE = 'maps/maze3.txt'
                        choosing_maze = False
                    elif Quit_button.is_clicked(mouse_pos):
                        running = False
                        choosing_maze = False

        if not running:
            break  # exit the main loop

        # Load map and get initial data
        dimension, initial_state, goal_states, barriers = load_map(MAZE)
        rows, columns = dimension

        # Reset grid and search
        grid = Grid(rows, columns, CELL_SIZE,
                    initial_state, goal_states, barriers)
        search = Search(grid)

        # Reset screen to initial screen size
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Initialize buttons with the current screen
        BFS_button = Button(screen, (((SCREEN_WIDTH // 2) - BUTTON_WIDTH * 2),
                                     (SCREEN_HEIGHT // 2) - BUTTON_HEIGHT * 2, BUTTON_WIDTH, BUTTON_HEIGHT), "BFS")
        DFS_button = Button(screen, (((SCREEN_WIDTH // 2) - BUTTON_WIDTH // 2),
                                     (SCREEN_HEIGHT // 2) - BUTTON_HEIGHT * 2, BUTTON_WIDTH, BUTTON_HEIGHT), "DFS")
        CUS_1_button = Button(screen, (((SCREEN_WIDTH // 2) + BUTTON_WIDTH),
                                       (SCREEN_HEIGHT // 2) - BUTTON_HEIGHT * 2, BUTTON_WIDTH, BUTTON_HEIGHT), "CUS_1")

        GBFS_button = Button(screen, (((SCREEN_WIDTH // 2) - BUTTON_WIDTH * 2),
                                      (SCREEN_HEIGHT // 2), BUTTON_WIDTH, BUTTON_HEIGHT), "GBFS")
        A_STAR_button = Button(screen, (((SCREEN_WIDTH // 2) - BUTTON_WIDTH // 2),
                                        (SCREEN_HEIGHT // 2), BUTTON_WIDTH, BUTTON_HEIGHT), "A*")
        CUS_2_button = Button(screen, (((SCREEN_WIDTH // 2) + BUTTON_WIDTH),
                                       (SCREEN_HEIGHT // 2), BUTTON_WIDTH, BUTTON_HEIGHT), "CUS_2")

        Evaluate_button = Button(screen, (((SCREEN_WIDTH // 2) - BUTTON_WIDTH // 2),
                                          (SCREEN_HEIGHT // 2) + BUTTON_HEIGHT * 4, BUTTON_WIDTH, BUTTON_HEIGHT), "Evaluate")

        Return_button = Button(screen, (((SCREEN_WIDTH // 2) - BUTTON_WIDTH // 2),
                                        (SCREEN_HEIGHT // 2) + BUTTON_HEIGHT * 2, BUTTON_WIDTH, BUTTON_HEIGHT), "Return")

        screen.fill(COLORS['BLUE'])
        render_title(screen)
        BFS_button.render()
        DFS_button.render()
        CUS_1_button.render()
        GBFS_button.render()
        A_STAR_button.render()
        CUS_2_button.render()
        Evaluate_button.render()
        Return_button.render()
        pygame.display.flip()

        choose = True
        algorithm = None

        while choose:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    choose = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if BFS_button.is_clicked(mouse_pos):
                        algorithm = 'bfs'
                        choose = False
                    elif DFS_button.is_clicked(mouse_pos):
                        algorithm = 'dfs'
                        choose = False
                    elif CUS_1_button.is_clicked(mouse_pos):
                        algorithm = 'cus_1'
                        choose = False
                    elif GBFS_button.is_clicked(mouse_pos):
                        algorithm = 'gbfs'
                        choose = False
                    elif A_STAR_button.is_clicked(mouse_pos):
                        algorithm = 'a_star'
                        choose = False
                    elif CUS_2_button.is_clicked(mouse_pos):
                        algorithm = 'cus_2'
                        choose = False
                    elif Evaluate_button.is_clicked(mouse_pos):
                        algorithms = ['bfs', 'dfs', 'cus_1',
                                      'gbfs', 'a_star', 'cus_2']
                        results = []
                        for algo in algorithms:
                            path, path_output, duration, expanded_nodes, num_expanded_nodes = execute_search(
                                search, algo)
                            goal_found = get_goal(grid, path)
                            results.append(
                                [get_algorithm_name(algo), goal_found, len(path_output), duration, num_expanded_nodes])
                        with open('evaluation_results.csv', 'w') as f:
                            f.write(
                                'Algorithm,Goal,Solution Steps,Duration,Memory\n')
                            for result in results:
                                f.write(','.join(map(str, result)) + '\n')
                        print('Evaluation results saved to evaluation_results.csv')
                        choose = False
                    elif Return_button.is_clicked(mouse_pos):
                        choose = False
                        choosing_maze = True

        if algorithm:
            path, path_output, duration, expanded_nodes, num_expanded_nodes = execute_search(
                search, algorithm)
            DISPLAY_WIDTH, DISPLAY_HEIGHT = columns * CELL_SIZE, rows * CELL_SIZE
            screen = pygame.display.set_mode(
                (DISPLAY_WIDTH, DISPLAY_HEIGHT))
            algorithm, goal_found = navigate_path(screen, grid, num_expanded_nodes, expanded_nodes, path,
                                                  algorithm, goal_states)

            print('--------Results---------')
            print(f'Algorithm: {algorithm}')
            print(f'Goals Found: {goal_found}')
            print(f'Path: {path_output}')
            print(f'Duration: {duration} seconds')
            print(f'Memory: {num_expanded_nodes} nodes')

    pygame.quit()


if __name__ == "__main__":
    main()
