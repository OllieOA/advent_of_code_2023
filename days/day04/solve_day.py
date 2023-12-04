from typing import Dict, List, Tuple, Set

from solver import Solver


class Day04(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

    def __get_card_spec(self, nums_str: str) -> List[int]:
        """Just split up the numbers that are space delimeted (remember that
        they are also tab-aligned, so need to consider the empty string)
        """
        num_list = []
        for num in nums_str.split(" "):
            if num == "":
                continue
            num_list.append(int(num))
        return num_list

    def __get_card(self, data: List[str]) -> List[int]:
        """We don't actually care about the content of each card, just the
        result, so we can throw that away and just consider the number of
        winning numbers using the length of a set intersection
        """
        cards = []
        for line in data:
            card_spec = line.split(": ")[-1]
            winning_nums_str, all_nums_str = card_spec.split(" | ")

            winning_nums = set(self.__get_card_spec(winning_nums_str))
            all_nums = set(self.__get_card_spec(all_nums_str))

            cards.append(len(winning_nums.intersection(all_nums)))
        return cards

    def part1(self, data: List[str]) -> None:
        """Simply get all the card results and raise 2 to the power of result-1
        recalling that the result is a double, though if 1 number is present,
        it is worth one. Anything**0 = 1, so we just need a special handler for
        when it is worth nothing to discard it
        """
        self.cards = self.__get_card(data)

        points = []
        for card in self.cards:
            total_nums = card
            if total_nums == 0:
                continue
            points.append(2 ** (total_nums - 1))
        return sum(points)

    def __get_total_num_cards_won(self, card_idx: int) -> int:
        """This is a recursive function to return the winning numbers from
        a given index, and then continue recursing until all winnings are
        tabulated. Note that the range considers a +1 offset to ensure we are
        getting the next value only.
        """
        cards_won = self.cards[card_idx]
        for idx in range(card_idx + 1, card_idx + self.cards[card_idx] + 1):
            cards_won += self.__get_total_num_cards_won(idx)
        return cards_won

    def part2(self, data: List[str]) -> None:
        """Iterate over the cards and find the result. Note here that we will
        be recursing, starting with the treatment of each index card first.
        This is not worded the same as the puzzle, as we do NOT consider every
        instance of the card at once, but instead consider only the copies won
        by a given card. The sum is equivalent.
        """
        self.cards = self.__get_card(data)

        total_cards = 0
        for idx in range(len(self.cards)):
            total_cards += 1 + self.__get_total_num_cards_won(idx)

        return total_cards


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day04(day, use_sample, run_each)
    solver.solve()
