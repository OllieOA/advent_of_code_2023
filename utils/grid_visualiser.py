from typing import Dict, Iterable


class GridVisualiser:
    def __init__(self, grid: Iterable, spec: Dict):
        self.grid = grid
        self.spec = spec

    def visualise_grid(self):
        display_grid = "\n"
        for row in self.grid:
            for col in row:
                display_grid += self.spec.get(col, ".")
            display_grid += "\n"
        print(display_grid)
