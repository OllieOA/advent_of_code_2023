from typing import List

import numpy as np


class BaseParser:
    def __init__(self, data: List[str]) -> None:
        self.data = data

    def parse(self) -> None:
        raise NotImplementedError("Inherit from this class and implement a `parse` method!")


class NewLineListParser(BaseParser):
    def parse(self) -> np.array:
        all_groups = []
        curr_group = []

        for line in self.data:
            if line.strip() == "":
                all_groups.append(curr_group)
                curr_group = []
                continue
            curr_group.append(line)

        if len(curr_group) > 0:
            all_groups.append(curr_group)  # Catches the last one parsed if does not end in newline
        return all_groups


class NumpyArrayParser(BaseParser):
    def parse(self) -> np.array:
        all_lines = []
        for line in self.data:
            new_line = []
            for each_char in line:
                new_line.append(each_char)
            all_lines.append(new_line)
        return np.array(all_lines)
