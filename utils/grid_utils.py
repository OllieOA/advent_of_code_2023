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
    pos: Tuple[int],
    arr_shape: Tuple[int],
    include_diagonals: bool = True,
    direction: Tuple = None,
) -> List[Tuple]:
    """Get all adjacent positions ()

    Args:
        pos (Tuple[int]): start pos
        arr_shape (Tuple[int]): shape of the array
        include_diagonals (bool): include diagonals from pos

    Returns:
        List[Tuple]: _description_
    """
    if direction:
        positions = [(pos[0] + direction[0], pos[1] + direction[1])]
    else:
        positions = [
            (pos[0] + 1, pos[1]),
            (pos[0] - 1, pos[1]),
            (pos[0], pos[1] + 1),
            (pos[0], pos[1] - 1),
        ]

    if include_diagonals and not direction:
        diag_positions = [
            (pos[0] - 1, pos[1] - 1),
            (pos[0] - 1, pos[1] + 1),
            (pos[0] + 1, pos[1] - 1),
            (pos[0] + 1, pos[1] + 1),
        ]
        positions.extend(diag_positions)

    if include_diagonals and direction:
        raise ValueError("Cannot consider both diagonals and a given direction")

    filtered_positions = []
    for pos in positions:
        x, y = pos
        if x < 0 or x >= arr_shape[0] or y < 0 or y >= arr_shape[1]:
            continue
        filtered_positions.append(pos)
    return filtered_positions
