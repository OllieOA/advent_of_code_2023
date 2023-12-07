from collections import Counter
from copy import deepcopy
from functools import cmp_to_key
from typing import List, Tuple, Dict

from solver import Solver


class Day07(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

        self.CARD_STRENGTH_P1: List = [x for x in "AKQJT98765432"]
        self.CARD_STRENGTH_P2: List = [x for x in "AKQT98765432J"]

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
            for h1, h2 in zip(hand1["original_hand"], hand2["original_hand"]):
                rel_strength = self.CARD_STRENGTH.index(h2) - self.CARD_STRENGTH.index(h1)
                if rel_strength != 0:
                    return rel_strength
                assert "Cannot break tie!"

        return hand1["hand_class"] - hand2["hand_class"]

    def __make_hands(self, data: List[str]) -> None:
        cards_breakdown = []
        for line in data:
            hand, bid = line.split(" ")
            cards_breakdown.append(
                {
                    "hand": hand,
                    "original_hand": hand,
                    "bid": int(bid),
                    "hand_class": self.__get_class_of_hand(hand),
                }
            )
        cards_breakdown = sorted(
            cards_breakdown, key=cmp_to_key(lambda x, y: self.__compare_hands(x, y))
        )
        self.cards_breakdown = cards_breakdown

    def __make_best_hand(self, bkdown: Dict) -> Dict:
        if "J" not in bkdown["hand"]:
            return deepcopy(bkdown)

        other_candidate_cards = [x for x in Counter(bkdown["hand"]).keys() if x != "J"]

        print(other_candidate_cards)

        updated_card = {}

    def part1(self, data: List[str]) -> None:
        self.__make_hands(data)

        res_sum = 0

        for idx, bkdown in enumerate(self.cards_breakdown):
            res_sum += bkdown["bid"] * (idx + 1)

        return res_sum

    def part2(self, data: List[str]) -> None:
        self.__make_best_hand({"hand": "JJTQA", "bid": 1, "hand_class": 1})
        # updated_cards = []
        # for bkdown in self.cards_breakdown:
        #     updated_cards.append(self.__make_best_hand(bkdown))


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day07(day, use_sample, run_each)
    solver.solve()
