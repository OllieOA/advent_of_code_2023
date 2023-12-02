import math
from typing import List, Dict

from solver import Solver


BAG_CONFIG = {"red": 12, "green": 13, "blue": 14}


class Day02(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def __build_game_breakdown(self, data: List[str]) -> Dict:
        """We reduce the game to a lookup - each game number will get a
        breakdown of the occurences of each colour in each game (though we
        do not need to track the "zero" case as it is not used).
        """
        game_breakdown = {}
        for line in data:
            game_num, game_spec = line.split(": ", maxsplit=1)
            game_results = game_spec.split("; ")

            single_game_breakdown = {x: [] for x in BAG_CONFIG.keys()}
            for game_result in game_results:
                for single_result in game_result.split(", "):
                    num_str, color = single_result.split(" ")

                    single_game_breakdown[color].append(int(num_str))

            game_breakdown[int(game_num.replace("Game ", ""))] = single_game_breakdown
        return game_breakdown

    def part1(self, data: List[str]) -> None:
        """We take the game breakdown as above and iterate. First, assume the
        game will be possible, it will be marked as NOT possible if there is a
        case where an occurence is greater than what is available in the config
        (we take the negative, asserting all are <= config limit). If possible,
        add to the sum.
        """
        game_breakdown = self.__build_game_breakdown(data)
        possible_games = []
        for game_num, game_spec in game_breakdown.items():
            game_possible = True
            for color, occurences in game_spec.items():
                game_possible = game_possible and all([x <= BAG_CONFIG[color] for x in occurences])

            if game_possible:
                possible_games.append(game_num)

        return sum(possible_games)

    def part2(self, data: List[str]) -> None:
        """Here, we only care about the game's power, which is independent to
        the game number. We can discard this - but otherwise we iterate the
        same.
        Breaking into two steps, we first track the maximum occurence for any
        individual grab from the bag across all games, then after this step,
        we calculate the power by taking the product.
        """
        game_breakdown = self.__build_game_breakdown(data)
        game_powers = []
        for game_spec in game_breakdown.values():
            min_cubes = {x: 0 for x in BAG_CONFIG.keys()}

            for color, occurences in game_spec.items():
                min_cubes[color] = max(max(occurences), min_cubes[color])
            game_powers.append(math.prod(min_cubes.values()))

        return sum(game_powers)


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day02(day, use_sample, run_each)
    solver.solve()
