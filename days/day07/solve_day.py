from collections import Counter, Dict
from typing import List, Tuple

from solver import Solver


class Day07(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

        self.CARD_STRENGTH_ORDER = [x for x in "AKQJT98765432"]

    def __get_class_of_hand(self, hand: str) -> int:
        """
        0: high card
        1: pair
        2: two pair
        3: three of a kind
        4: full house
        5: four of a kind
        6: five of a kind
        """
        hand_comps = Counter(hand)

        if len(hand_comps) == 5:
            return 0

        if max(hand_comps.values()) == 2:
            if len(hand_comps) == 3:
                # This must be 2 pair
                return 2
            return 1

        if max(hand_comps.values()) == 3:
            if len(hand_comps) == 2:
                # This must be a full house
                return 4
            return 3

        if max(hand_comps.values()) == 4:
            return 5

        if len(hand_comps) == 1:
            return 6

    def __compare_hands(self, hand1: Dict, hand2: Dict) -> Tuple[str]:
        if hand1["hand_class"] == hand2["hand_class"]:
            for h1, h2 in zip(hand1["hand"], hand2["hand"]):
                print(h1, h2)

        return hand1["hand_class"] - hand2["hand_class"]

    def part1(self, data: List[str]) -> None:
        cards_breakdown = []
        for idx, line in enumerate(data):
            hand, bid = line.split(" ")
            cards_breakdown.append(
                {
                    "hand": hand,
                    "bid": int(bid),
                    "original_index": idx,
                    "hand_class": self.__get_class_of_hand(hand),
                }
            )

        print(
            self.__compare_hands(
                {"hand": "T55J5", "hand_class": 3}, {"hand": "QQQJA", "hand_class": 3}
            )
        )

    def part2(self, data: List[str]) -> None:
        pass


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day07(day, use_sample, run_each)
    solver.solve()
