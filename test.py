import unittest
from algorithm import Search
from grid import Grid

# test_algorithm.py


class MockGrid:
    def __init__(self, rows, columns, initial_state, goal_states, barriers):
        self.rows = rows
        self.columns = columns
        self.cell_size = 10
        self.barriers = barriers
        self.initial_state = initial_state
        self.goal_states = goal_states


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.grid = MockGrid(
            rows=5,
            columns=11,
            initial_state=(1, 0),  # (row, column)
            goal_states=[(0, 7)],  # (row, column)
            barriers=[
                (2, 0, 2, 2),
                (8, 0, 1, 2),
                (10, 0, 1, 1),
                (2, 3, 1, 2),
                (3, 4, 3, 1),
                (9, 3, 1, 1),
                (8, 4, 2, 1)
            ]
        )

        self.search = Search(self.grid)

    def transform_path(self, path):
        result = path.strip(";").split("; ")
        return result

    def test_bfs(self):
        path = self.transform_path(self.search.search('bfs'))
        expected_path = ['down', 'right', 'right', 'right',
                         'right', 'up', 'up', 'right', 'right', 'right']
        self.assertEqual(path, expected_path)

    def test_dfs(self):
        path = self.transform_path(self.search.search('dfs'))
        expected_path = ['up', 'right', 'down', 'down', 'right', 'right', 'down', 'right',
                         'up', 'up', 'up', 'right', 'down', 'down', 'down', 'right', 'up', 'up', 'up', 'right']
        self.assertEqual(path, expected_path)

    def test_astar(self):
        path = self.transform_path(self.search.search('a_star'))
        expected_path = ['down', 'right', 'right', 'right',
                         'right', 'up', 'up', 'right', 'right', 'right']
        self.assertEqual(path, expected_path)

    def test_gbfs(self):
        path = self.transform_path(self.search.search('gbfs'))
        expected_path = ['right', 'down', 'right', 'right',
                         'right', 'up', 'up', 'right', 'right', 'right']
        self.assertEqual(path, expected_path)

    def test_cus_1(self):
        path = self.transform_path(self.search.search('cus_1'))
        expected_path = ['down', 'right', 'right', 'right',
                         'right', 'up', 'up', 'right', 'right', 'right']
        self.assertEqual(path, expected_path)

    def test_cus_2(self):
        path = self.transform_path(self.search.search('cus_2'))
        expected_path = ['down', 'right', 'right', 'right',
                         'right', 'up', 'up', 'right', 'right', 'right']
        self.assertEqual(path, expected_path)


class TestNoPath(unittest.TestCase):
    def setUp(self):
        self.grid = MockGrid(
            rows=5,
            columns=11,
            initial_state=(1, 0),  # (row, column)
            goal_states=[(0, 2)],  # (row, column)
            barriers=[
                (2, 0, 2, 2),
                (8, 0, 1, 2),
                (10, 0, 1, 1),
                (2, 3, 1, 2),
                (3, 4, 3, 1),
                (9, 3, 1, 1),
                (8, 4, 2, 1)
            ]
        )

        self.search = Search(self.grid)

    def test_bfs(self):
        path = self.search.search('bfs')
        expected_path = 'No path found.'
        self.assertEqual(path, expected_path)

    def test_dfs(self):
        path = self.search.search('dfs')
        expected_path = 'No path found.'
        self.assertEqual(path, expected_path)

    def test_astar(self):
        path = self.search.search('a_star')
        expected_path = 'No path found.'
        self.assertEqual(path, expected_path)

    def test_gbfs(self):
        path = self.search.search('gbfs')
        expected_path = 'No path found.'
        self.assertEqual(path, expected_path)

    def test_cus_1(self):
        path = self.search.search('cus_1')
        expected_path = 'No path found.'
        self.assertEqual(path, expected_path)

    def test_cus_2(self):
        path = self.search.search('cus_2')
        expected_path = 'No path found.'
        self.assertEqual(path, expected_path)


if __name__ == '__main__':
    unittest.main()
