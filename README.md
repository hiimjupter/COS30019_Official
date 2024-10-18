# COS30019_Official 

# Assignment 1: Robot Navigation Program

## Instructions

### Setup

Ensure you have `python` and `pygame` installed on your system. For more details, please visit:

- [Python](https://www.python.org)
- [Pygame](https://www.pygame.org)

### Upload your test file (.txt)

Please do as instructed in test.txt file located in `root/maps` folder.

### Running the Program

1. Navigate to the directory containing the `main.py` file.
2. Run the main script using the following command:

   ```bash
   python main.py
3. You can test your test file by choosing the `test` button when choosing maze.

### Algorithm Selection

After selecting a maze, choose the search algorithm to use:

- BFS (Breadth-first Search)
- DFS (Depth-first Search)
- GBFS (Greedy Best-first Search)
- A* (A-star Search)
- CUS_1 (Iterative Deepening Search)
- CUS_2 (Iterative Deepening A\* Search)

Alternatively, select `Evaluate` to run all algorithms and generate a comparative report.

### Viewing Results

The robot's exploration and pathfinding process will be visualized on the GUI with:

- Orange: `expanded_nodes`.
- Blue: Solution (shortest path from `initial_state` to `goal_state(s)`).

Results, including paths found and performance metrics, will be displayed in the console or saved in `evaluation_results.csv` if using the `Evaluate` option.

## Exiting the Program

- Use the `Return` button to go back to the maze selection screen.
- Click `Quit` to exit the application.
