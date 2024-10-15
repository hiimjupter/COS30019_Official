def navigate_path(screen, grid, num_expanded_nodes, expanded_nodes, path, algorithm, goal_states, barriers):
    path_drawn = False
    running = True
    goals_found = []
    total_duration = 0
    total_expanded_nodes = num_expanded_nodes
    total_path_output = ', '.join(path)
    current_position = grid.initial_state

    while running and goal_states:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(COLORS['WHITE'])

        if not path_drawn:
            grid.draw_path(screen, path, expanded_nodes)
            path_drawn = True
            pygame.time.delay(5000)

            for direction in path:
                move = get_move_from_direction(direction)
                if move:
                    current_position = (
                        current_position[0] + move[0], current_position[1] + move[1])

            if current_position in goal_states:
                goals_found.append(current_position)
                goal_states.remove(current_position)
                grid.initial_state = current_position  # Update the initial state
                path_drawn = False

                if not goal_states:
                    # All goals found
                    running = False
                    break

                # Continue searching for the next goal without resetting
                search = Search(grid)
                try:
                    path, path_output, duration, expanded_nodes, num_expanded_nodes = execute_search(
                        search, algorithm)
                    total_duration += duration
                    total_expanded_nodes += num_expanded_nodes
                    total_path_output += '; ' + path_output
                except IndexError:
                    running = False
            else:
                print("Goal not found in the path.")
                running = False

        pygame.display.flip()

    # Reswap to match map format
    goals_found = [(goal[1], goal[0]) for goal in goals_found]

    return get_algorithm_name(algorithm), goals_found, total_duration, total_expanded_nodes, total_path_output


if algorithm:
    # Execute the initial search
    path, path_output, duration, expanded_nodes, num_expanded_nodes = execute_search(
        search, algorithm)
    DISPLAY_WIDTH, DISPLAY_HEIGHT = columns * CELL_SIZE, rows * CELL_SIZE
    screen = pygame.display.set_mode(
        (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    # Receive the collected information from navigate_path
    algorithm_used, goals_found, total_duration, total_expanded_nodes, total_path_output = navigate_path(
        screen, grid, num_expanded_nodes, expanded_nodes, path, algorithm, goal_states, barriers)

    # Print the required information
    print(f"Algorithm Used: {algorithm_used}")
    print(f"Goals Found: {goals_found}")
    print(f"Total Number of Expanded Nodes: {total_expanded_nodes}")
    print(f"Total Path Output: {total_path_output}")
    print(f"Total Time Taken: {total_duration} seconds")
