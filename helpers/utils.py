def load_map(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        dimension = eval(lines[0].strip())
        initial_state = eval(lines[1].strip())
        goal_states = [eval(goal.strip()) for goal in lines[2].split('|')]
        barriers = [eval(barrier.strip()) for barrier in lines[3:]]

    # Swap row and column for initial_state
    initial_state = (initial_state[1], initial_state[0])

    # Swap row and column for each goal_state
    goal_states = [(goal[1], goal[0]) for goal in goal_states]

    return dimension, initial_state, goal_states, barriers


def get_move_from_direction(direction):
    if direction == 'up':
        return (-1, 0)
    elif direction == 'left':
        return (0, -1)
    elif direction == 'down':
        return (1, 0)
    elif direction == 'right':
        return (0, 1)
    return None


def get_algorithm_name(algorithm):
    if algorithm == 'bfs':
        return 'Breadth First Search'
    elif algorithm == 'dfs':
        return 'Depth First Search'
    elif algorithm == 'cus_1':
        return 'Custom 1'
    elif algorithm == 'gbfs':
        return 'Greedy Best-first Search'
    elif algorithm == 'a_star':
        return 'A* Search'
    elif algorithm == 'cus_2':
        return 'Custom 2'
    return None
