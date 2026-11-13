# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mastermind-problem/. The authors are listed in prov/EHS84T.jsonl.

import random
from collections import Counter

from mastermind_problem import (all_codes, knuth_strategy, largest_class, most_codes_solvable, score,
                                score_by_definition, score_table)


def test_score_formula_matches_definition() -> None:
    for pegs, colors in [(2, 3), (3, 3), (3, 4)]:
        codes = all_codes(pegs, colors)
        for g in codes:
            for s in codes:
                assert score(g, s, colors) == score_by_definition(g, s)
    rng = random.Random(11)
    codes = all_codes(4, 6)
    for _ in range(3000):
        g, s = rng.choice(codes), rng.choice(codes)
        assert score(g, s) == score_by_definition(g, s)


def test_fast_table_matches_formula() -> None:
    codes = all_codes(4, 6)
    table = score_table(codes, 6)
    rng = random.Random(12)
    for _ in range(5000):
        i, j = rng.randrange(1296), rng.randrange(1296)
        b, w = score(codes[i], codes[j])
        assert table[i][j] == b * 5 + w
    assert len(set(table[0])) == 5  # 1111 against anything: black only
    assert len({x for row in table for x in row}) == 14  # (3, 1) never occurs


def test_worked_score() -> None:
    # secret 1123, guess 1312 in colors 1..6 written as 0..5
    assert score((0, 2, 0, 1), (0, 0, 1, 2)) == (1, 3)
    assert score((0, 0, 1, 1), (0, 0, 1, 1)) == (4, 0)


def test_knuth_worst_case_five() -> None:
    used = knuth_strategy()
    dist = Counter(used)
    assert max(used) == 5
    assert sorted(dist.items()) == [(1, 1), (2, 6), (3, 62), (4, 533), (5, 694)]
    assert sum(used) == 5801


def test_four_guesses_are_not_enough() -> None:
    # the best first guesses, one from each class up to symmetry
    sizes = {code: largest_class(code) for code in
             [(0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 1, 1), (0, 0, 1, 2), (0, 1, 2, 3)]}
    assert sizes == {(0, 0, 0, 0): 625, (0, 0, 0, 1): 317, (0, 0, 1, 1): 256,
                     (0, 0, 1, 2): 276, (0, 1, 2, 3): 312}
    # after a wrong first guess, three more guesses solve at most 183 codes
    assert most_codes_solvable(3, 14) == 183
    assert min(sizes.values()) > most_codes_solvable(3, 14)
