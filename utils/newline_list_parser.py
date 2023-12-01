from typing import List


class NewLineListParser:
    def __init__(self, data: List[str]) -> None:
        self.data = data

    def parse(self) -> List[str]:
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
