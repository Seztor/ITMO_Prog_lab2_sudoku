import pathlib
import typing as tp
import random
import copy

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i:i+n] for i in range(0,len(values),n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [grid[i][pos[1]] for i in range(len(grid))]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    i_block = pos[0]//3*3
    j_block = pos[1]//3*3

    return [grid[i][j] for i in range(i_block, i_block + 3) for j in range(j_block, j_block + 3) ]


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    n = len(grid)
    for i in range(n):
        if '.' in set(grid[i]):
            for j in range(n):
                if grid[i][j] == '.':
                    return i, j
    return -1,-1


def find_arr_empty_positions(grid: tp.List[tp.List[str]]) -> tp.List[tp.Tuple[int, int]]:
    n = len(grid)
    arr = []
    for i in range(3):
        for j in range(3):
            temp_arr = get_block(grid, (i*3,j*3))
            arr.extend([(i*3+g//3,j*3+g%3) for g in range(9) if temp_arr[g] == '.'])
    arr.append((-1,-1))
    return arr


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    return set(str(i) for i in range(1,10) if str(i) not in set(get_row(grid, pos)) | set(get_col(grid, pos)) | set(get_block(grid, pos)))


def solve_recursion(grid: tp.List[tp.List[str]], ind_arr_pos: int):
    '''Рекурсивная функция решения судоку'''
    global solution_grid_global, arr_empty_positions, solution_found
    if solution_found:
        return
    y, x = arr_empty_positions[ind_arr_pos]
    if not(y == -1 and x == -1):
        possible_values = sorted(find_possible_values(grid, (y,x)))
        if not possible_values:
            return
        max_from_block = max(get_block(grid, (y,x)))
        max_from_block = '0' if max_from_block == '.' else max_from_block
        possible_values = [i for i in possible_values if i > max_from_block] + [i for i in possible_values if i <= max_from_block]
        for i in possible_values:
            grid[y][x] = i
            solve_recursion(grid, ind_arr_pos+1)
            grid[y][x] = '.'

    else:
        solution_grid_global = copy.deepcopy(grid)
        solution_found = True


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Как решать Судоку?
        >>> grid = read_sudoku('puzzle1.txt')
        >>> solve(grid)
        [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    global solution_grid_global, arr_empty_positions, solution_found
    arr_empty_positions = find_arr_empty_positions(grid)
    solution_grid_global = []
    solution_found = False
    solve_recursion(grid, 0)
    return solution_grid_global


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = read_sudoku('puzzle_false.txt')
    >>> check_solution(grid)
    False
    """
    if not solution:
        return False
    for i in range(len(solution)):
        row_nums = set(get_row(solution, (i, 0)))
        col_nums = set(get_col(solution, (0, i)))
        block_nums = set(get_block(solution, (i//3*3, i%3*3)))
        if '.' in row_nums:
            return False
        if not (len(row_nums) == len(col_nums) == len(block_nums) == len(solution)):
            return False
    return True

def transpon(grid: tp.List[tp.List[str]]) -> tp.List[tp.List[str]]:
    '''Транспонирование матрицы'''
    grid_temp = [['.']*len(grid) for _ in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid)):
            grid_temp[i][j] = grid[j][i]
    return grid_temp

def swap_row(grid: tp.List[tp.List[str]], n_row_1, n_row_2) -> tp.List[tp.List[str]]:
    grid_temp = []
    for i in range(len(grid)):
        if i == n_row_2:
            grid_temp.append(grid[n_row_1][:])
        elif i == n_row_1:
            grid_temp.append(grid[n_row_2][:])
        else:
            grid_temp.append(grid[i][:])
    return grid_temp

def swap_col(grid: tp.List[tp.List[str]], n_col_1, n_col_2) -> tp.List[tp.List[str]]:
    grid_temp = []
    for i in range(len(grid)):
        arr_temp = grid[i][:]
        arr_temp[n_col_1], arr_temp[n_col_2] = arr_temp[n_col_2], arr_temp[n_col_1]
        grid_temp.append(arr_temp)
    return grid_temp

def swap_cols_area(grid: tp.List[tp.List[str]], n_col_area_1, n_col_area_2) -> tp.List[tp.List[str]]:
    grid_temp = []
    for i in range(len(grid)):
        arr_temp = grid[i][:]
        (arr_temp[n_col_area_1*3], arr_temp[n_col_area_1*3+1], arr_temp[n_col_area_1*3+2],
         arr_temp[n_col_area_2*3], arr_temp[n_col_area_2*3+1], arr_temp[n_col_area_2*3+2]) \
        =\
        (arr_temp[n_col_area_2*3], arr_temp[n_col_area_2*3+1], arr_temp[n_col_area_2*3+2],
         arr_temp[n_col_area_1*3], arr_temp[n_col_area_1*3+1], arr_temp[n_col_area_1*3+2])
        grid_temp.append(arr_temp)
    return grid_temp

def swap_rows_area(grid: tp.List[tp.List[str]], n_row_area_1, n_row_area_2) -> tp.List[tp.List[str]]:
    grid_temp = []
    for i in range(0, len(grid), 3):
        if i // 3 == n_row_area_1:
            grid_temp.append(grid[n_row_area_2 * 3][:])
            grid_temp.append(grid[n_row_area_2 * 3 + 1][:])
            grid_temp.append(grid[n_row_area_2 * 3 + 2][:])
        elif i // 3 == n_row_area_2:
            grid_temp.append(grid[n_row_area_1 * 3][:])
            grid_temp.append(grid[n_row_area_1 * 3 + 1][:])
            grid_temp.append(grid[n_row_area_1 * 3 + 2][:])
        else:
            grid_temp.append(grid[i][:])
            grid_temp.append(grid[i + 1][:])
            grid_temp.append(grid[i + 2][:])
    return grid_temp

def two_random_nums(fr: int,to: int) -> tp.Tuple[int,int]:
    num_1 = random.randint(fr, to)
    num_2 = random.randint(fr, to)
    while num_1 == num_2:
        num_2 = random.randint(fr, to)
    return num_1, num_2

def two_random_nums_row_or_col(num_row_or_col: int) -> tp.Tuple[int,int]:
    num_1 = random.randint(num_row_or_col*3, num_row_or_col*3+2)
    num_2 = random.randint(num_row_or_col*3, num_row_or_col*3+2)
    while num_1 == num_2:
        num_2 = random.randint(num_row_or_col*3, num_row_or_col*3+2)
    return num_1, num_2

def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    arr_pos_to_gen = [(i,j) for i in range(9) for j in range(9)]
    random.shuffle(arr_pos_to_gen)

    gen_sudoku_grid = create_grid('123456789 456789123 789123456'
                         '234567891 567891234 891234567'
                         '345678912 678912345 912345678')
    for i in range(100):
        op_num = random.randint(0,4)
        if op_num == 0:
            gen_sudoku_grid = transpon(gen_sudoku_grid)
            #print(gen_sudoku_grid)
        elif op_num == 1:
            num_row_1, num_row_2 = two_random_nums_row_or_col(random.randint(0, 2))
            gen_sudoku_grid = swap_row(gen_sudoku_grid, num_row_1, num_row_2)
        elif op_num == 2:
            num_col_1, num_col_2 = two_random_nums_row_or_col(random.randint(0, 2))
            gen_sudoku_grid = swap_col(gen_sudoku_grid, num_col_1, num_col_2)
        elif op_num == 3:
            num_row_area_1, num_row_area_2 = two_random_nums(0, 2)
            gen_sudoku_grid = swap_rows_area(gen_sudoku_grid, num_row_area_1, num_row_area_2)
        elif op_num == 4:
            num_col_area_1, num_col_area_2 = two_random_nums(0, 2)
            gen_sudoku_grid = swap_cols_area(gen_sudoku_grid, num_col_area_1, num_col_area_2)

    for i in range(81-N):
        y, x = arr_pos_to_gen[i]
        gen_sudoku_grid[y][x] = '.'

    return gen_sudoku_grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt","puzzle_full_clear.txt","puzzle_hardest.txt", "puzzle_false.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
        print('#-#-#-#-#-#-#-#-#-#')
        print()
