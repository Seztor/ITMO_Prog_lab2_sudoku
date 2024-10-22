'''
КОД взят с сайта habr для проверки
https://habr.com/ru/articles/192102/
'''

from itertools import product

def solve_sudoku(size, grid):
    R, C = size
    N = R * C
    X = ([("rc", rc) for rc in product(range(N), range(N))] +
         [("rn", rn) for rn in product(range(N), range(1, N + 1))] +
         [("cn", cn) for cn in product(range(N), range(1, N + 1))] +
         [("bn", bn) for bn in product(range(N), range(1, N + 1))])
    Y = dict()
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        b = (r // R) * R + (c // C) # Box number
        Y[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n)),
            ("bn", (b, n))]
    X, Y = exact_cover(X, Y)
    for i, row in enumerate(grid):
        for j, n in enumerate(row):
            if n:
                select(X, Y, (i, j, n))
    for solution in solve(X, Y, []):
        for (r, c, n) in solution:
            grid[r][c] = n
        yield grid

def exact_cover(X, Y):
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)
    return X, Y

def solve(X, Y, solution):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()

def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols

def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)



import typing as tp
T = tp.TypeVar("T")
import pathlib


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[int]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)

def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    # """
    # Сгруппировать значения values в список, состоящий из списков по n элементов
    # >>> group([1,2,3,4], 2)
    # [[1, 2], [3, 4]]
    # >>> group([1,2,3,4,5,6,7,8,9], 3)
    # [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # """
    return [values[i:i+n] for i in range(0,len(values),n)]

def create_grid(puzzle: str) -> tp.List[tp.List[int]]:
    digits = [int(c.replace('.','0',1)) for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


#
# grid = read_sudoku('puzzle_false.txt')
# print(grid)

# for i in solve_sudoku((3,3), grid):
#     print(i)
#     break