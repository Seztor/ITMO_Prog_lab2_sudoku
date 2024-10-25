import unittest
import src.lab3.sudoku as sud



class SudokuTestCase(unittest.TestCase):

    # Тест для проверки работы, можно удалить
    def test_create_grid(self):
        string_sudoku = '8..4.6..7\n......4..\n.1....65.\n5.9.3.78.\n....7....\n.48.2.1.3\n.52....9.\n..1......\n3..9.2..5'
        alr_created_grid = [['8', '.', '.', '4', '.', '6', '.', '.', '7'], ['.', '.', '.', '.', '.', '.', '4', '.', '.'], ['.', '1', '.', '.', '.', '.', '6', '5', '.'], ['5', '.', '9', '.', '3', '.', '7', '8', '.'], ['.', '.', '.', '.', '7', '.', '.', '.', '.'], ['.', '4', '8', '.', '2', '.', '1', '.', '3'], ['.', '5', '2', '.', '.', '.', '.', '9', '.'], ['.', '.', '1', '.', '.', '.', '.', '.', '.'], ['3', '.', '.', '9', '.', '2', '.', '.', '5']]
        self.assertEqual(sud.create_grid(string_sudoku), alr_created_grid)

    def test_group(self):
        test1 = [1,2,3,4]
        n1 = 2
        self.assertEqual(sud.group(test1,n1),[[1, 2], [3, 4]])
        test2 = [1,2,3,4,5,6,7,8,9]
        n2 = 3
        self.assertEqual(sud.group(test2, n2), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    def test_get_row(self):
        test1 = [['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']]
        pos1 = (0,2)
        self.assertEqual(sud.get_row(test1, pos1), ['1', '2', '.'])
        test2 = [['4', '7', '2'], ['3', '1', '.'], ['6', '9', '5']]
        pos2 = (1, 1)
        self.assertEqual(sud.get_row(test2, pos2), ['3', '1', '.'])

    def test_get_col(self):
        test1 = [['4', '7', '2'], ['3', '1', '.'], ['6', '9', '5']]
        pos1 = (1, 2)
        self.assertEqual(sud.get_col(test1, pos1), ['2', '.', '5'])
        test2 = [['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']]
        pos2 = (0, 1)
        self.assertEqual(sud.get_col(test2, pos2), ['2', '.', '8'])

    def test_get_block(self):
        test1 = sud.read_sudoku('src/lab3/puzzle1.txt')
        pos1 = (1, 2)
        pos2 = (7, 7)
        self.assertEqual(sud.get_block(test1, pos1), ['5', '3', '.', '6', '.', '.', '.', '9', '8'])
        self.assertEqual(sud.get_block(test1, pos2), ['2', '8', '.', '.', '.', '5', '.', '7', '9'])

    def test_find_empty_position(self):
        test1 = [['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']]
        self.assertEqual(sud.find_empty_positions(test1), (0, 2))
        test2 = [['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']]
        self.assertEqual(sud.find_empty_positions(test2), (2, 0))

    def test_possible_values(self):
        test1 = sud.read_sudoku('src/lab3/puzzle1.txt')
        pos1 = (0,2)
        self.assertEqual(sud.find_possible_values(test1, pos1), {'1', '2', '4'})
        pos2 = (4,7)
        self.assertEqual(sud.find_possible_values(test1, pos2), {'2', '5', '9'})

    def test_solve(self):
        test1 = sud.read_sudoku('src/lab3/puzzle1.txt')
        self.assertEqual(sud.solve(test1), [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']])

    def test_check_solution(self):
        test1 = sud.solve(sud.read_sudoku('src/lab3/puzzle1.txt'))
        self.assertEqual(sud.check_solution(test1), True)
        test2 = sud.read_sudoku('src/lab3/puzzle1.txt')
        self.assertEqual(sud.check_solution(test2), False)




