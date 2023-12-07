from collections import Counter
from copy import deepcopy
from functools import cmp_to_key
from itertools import product
from typing import List, Tuple, Dict

from solver import Solver


class Day07(Solver):
    def __init__(self, day: int, use_sample: bool, run_each: List[bool]) -> None:
        super().__init__(use_sample, run_each)
        self.my_base_path = __file__
        self.day = day

        self.CARD_STRENGTH_P1: List[str] = [x for x in "AKQJT98765432"]
        self.CARD_STRENGTH_P2: List[str] = [x for x in "AKQT98765432J"]

    def __get_class_of_hand(self, hand: str) -> int:
        """Here, make assessments about the number of unique cards in a hand
        and basically do a match case. The maximum number of uniques can bin
        these (the specials cases are 2, which can either be a pair or two
        pair, and 3 which can either be three of a kind or a full house). We
        then give them a numerical strength we can use in our custom sorting
        function.

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

    def __compare_hands(self, hand1: Dict, hand2: Dict, include_jokers: bool = False) -> Tuple[str]:
        """This is the core of the custom sorting algorithm we need for this.
        Given there is complexity in the object being sorted (dictionary), non
        numerical properties of the object (arbitrary string), and a fallback
        sort method, we need to pass a custom "key" to sorted(), which is
        defined here.

        First, we need to choose the card strength rating to use for this (as
        Jacks get reclassified to Jokers), and then check if the hand classes
        are different. If they are, we need to use the fallback method of the
        individual card strength in the hand. Otherwise, just return the
        relative difference. If the first hand is weaker, the result will be
        negative and the sorted() function will put it earlier in the list.
        """
        card_strength = self.CARD_STRENGTH_P2 if include_jokers else self.CARD_STRENGTH_P1
        if hand1["hand_class"] == hand2["hand_class"]:
            for h1, h2 in zip(hand1["original_hand"], hand2["original_hand"]):
                rel_strength = card_strength.index(h2) - card_strength.index(h1)
                if rel_strength != 0:
                    return rel_strength
            return 0

        return hand1["hand_class"] - hand2["hand_class"]

    def __make_hands(self, data: List[str]) -> None:
        """We need a couple of special properties other than the hand and the
        bid - first, we need to determine the class (see __get_class_of_hand())
        so we can do easy comparisons, and secondly we need the original hand.
        This is important for part 2, which relies on the original hand, not
        the new one with jokers replaced, for tiebreaks.
        """
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

    def __make_best_hand(self, hand_spec: Dict) -> Dict:
        """Simply, any time there is a 'J' present, we instead substitute it
        for a list of all the unique cards in the hand (as well as the
        strongest possible card). This way, we guarantee that the we will
        generate the strongest hand while also not testing all possibilities.

        By taking the product of these lists and combining them, we can
        generate a new possible list, and use the existing sorting mechanism
        to isolate the strongest.

        Obviously, if J is not present, we can return early.
        """

        if "J" not in hand_spec["hand"]:
            return deepcopy(hand_spec)

        other_candidate_cards = [self.CARD_STRENGTH_P2[0]] + [
            x for x in Counter(hand_spec["hand"]).keys() if x != "J"
        ]

        card_pos_possibilities = [
            [x] if x != "J" else deepcopy(other_candidate_cards) for x in hand_spec["hand"]
        ]
        all_possible_cards = list(product(*card_pos_possibilities))
        all_possible_card_specs = [
            {
                "hand": "".join(x),
                "original_hand": hand_spec["original_hand"],
                "bid": hand_spec["bid"],
                "hand_class": self.__get_class_of_hand("".join(x)),
            }
            for x in all_possible_cards
        ]

        all_possible_card_specs = sorted(
            all_possible_card_specs, key=cmp_to_key(lambda x, y: self.__compare_hands(x, y, True))
        )

        return all_possible_card_specs[-1]

    def part1(self, data: List[str]) -> None:
        """The most complicated part here is the custom sort (see
        __compare_hands())
        """
        self.__make_hands(data)

        res_sum = 0
        for idx, hand_spec in enumerate(self.cards_breakdown):
            res_sum += hand_spec["bid"] * (idx + 1)

        return res_sum

    def part2(self, data: List[str]) -> None:
        """The custom sort from earlier helps us twofold here - instead, we
        need to rebuild the hands with the choices, which can be seen in
        __make_best_hand().
        """
        self.__make_hands(data)

        updated_cards = []
        for hand_spec in self.cards_breakdown:
            updated_cards.append(self.__make_best_hand(hand_spec))

        updated_cards = sorted(
            updated_cards, key=cmp_to_key(lambda x, y: self.__compare_hands(x, y, True))
        )

        res_sum = 0
        for idx, hand_spec in enumerate(updated_cards):
            res_sum += hand_spec["bid"] * (idx + 1)

        return res_sum


def solve_day(day: int, use_sample: bool, run_each: List[bool]):
    solver = Day07(day, use_sample, run_each)
    solver.solve()
