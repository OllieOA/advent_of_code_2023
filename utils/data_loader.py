# Example for relative common import

from typing import List


class DataLoader:
    def __init__(self, file_path) -> None:
        self.file_path = file_path

    def load_data(self) -> List:
        with open(self.file_path, "r") as f:
            lines = [x.strip("\n") for x in f.readlines()]

        assert len(lines) > 0, f"Did not load any data from {self.file_path} - check the file"
        return lines
