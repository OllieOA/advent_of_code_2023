# Using a numpy grid, here are some useful common functions

from typing import List, Tuple, Iterable, Dict


class GridVisualiser:
    def __init__(self, grid: Iterable, spec: Dict):
        self.grid = grid
        self.spec = spec

    def visualise_grid(self):
        display_grid = "\n"
        for row in self.grid:
            for col in row:
                display_grid += self.spec.get(col, self.grid[row, col])
            display_grid += "\n"
        print(display_grid)


def get_adjacent_positions(
    pos: Tuple[int], arr_shape: Tuple[int], include_diagonals: bool = True
) -> List[Tuple]:
    """Get all adjacent positions ()

    Args:
        pos (Tuple[int]): start pos
        arr_shape (Tuple[int]): shape of the array
        include_diagonals (bool): include diagonals from pos

    Returns:
        List[Tuple]: _description_
    """
    x_pos = [pos[0] - 1, pos[0], pos[0] + 1]
    y_pos = [pos[1] - 1, pos[1], pos[1] + 1]

    all_combos = []
    for x in x_pos:
        for y in y_pos:
            if x < 0 or x >= arr_shape[0] or y < 0 or y >= arr_shape[1]:
                continue
            if all([x == pos[0], y == pos[1]]):
                continue
            if not include_diagonals and (abs(x - x_pos[1]) == 1 and abs(y - y_pos[1]) == 1):
                continue
            all_combos.append((x, y))

    return all_combos
