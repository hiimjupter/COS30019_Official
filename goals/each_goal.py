def navigate_path(screen, grid, num_expanded_nodes, expanded_nodes, path, algorithm, goal_states, barriers):
    goal_index = 0
    path_drawn = False
    goals_found = []
    running = True

    while running and goal_index < len(goal_states):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(COLORS['WHITE'])

        if not path_drawn:
            if goal_index < len(goal_states):
                grid.draw_path(screen, path, expanded_nodes)
                path_drawn = True
                pygame.time.delay(5000)

                current_position = grid.initial_state
                for direction in path:
                    move = get_move_from_direction(direction)
                    if move:
                        current_position = (
                            current_position[0] + move[0], current_position[1] + move[1])

                if current_position in goal_states:
                    goals_found.append(current_position)
                    goal_states.remove(current_position)

                grid.goal_states = goal_states[goal_index:]
                grid = Grid(grid.rows, grid.columns, CELL_SIZE,
                            grid.initial_state, grid.goal_states, barriers)
                path_drawn = False

                try:
                    path, path_output, duration, expanded_nodes, num_expanded_nodes = execute_search(
                        Search(grid), algorithm)
                except IndexError:
                    running = False

        pygame.display.flip()

    # Reswap to match map format
    goals_found = [(goal[1], goal[0]) for goal in goals_found]

    return get_algorithm_name(algorithm), goals_found, duration


if algorithm:
    path, path_output, duration, expanded_nodes, num_expanded_nodes = execute_search(
        search, algorithm)
    DISPLAY_WIDTH, DISPLAY_HEIGHT = columns * CELL_SIZE, rows * CELL_SIZE
    screen = pygame.display.set_mode(
        (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    algorithm, goals_found, duration = navigate_path(screen, grid, num_expanded_nodes, expanded_nodes, path,
                                                     algorithm, goal_states, barriers)

    print('--------Results---------')
    print(f'Algorithm: {algorithm}')
    print(f'Goals Found: {goals_found}')
    print(f'Path: {path_output}')
    print(f'Duration: {duration} seconds')
