# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crossword-filling-problem/. The authors are listed in prov/WQC6R5.jsonl.

import random
from itertools import combinations

from crossword_filling_problem import brute_force, is_filling, slots, solve

WORDS = ["BAT", "ARE", "TEN", "TAN", "ATE", "NET", "EAR", "ERA", "RAT", "TAR", "BEE", "ONE", "TOE", "OAT"]
SHORT = ["AT", "TO", "BE", "NO", "AN", "ON"]


def test_word_square() -> None:
    grid = ["...", "...", "..."]
    assert solve(grid, WORDS) == [["TAR", "ERA", "NET"], ["TEN", "ARE", "RAT"]]
    # If a word may be used twice, symmetric squares such as BAT ARE TEN also count.
    again = solve(grid, WORDS, distinct=False)
    assert len(again) == 16 and ["BAT", "ARE", "TEN"] in again
    assert all(is_filling(grid, WORDS, x, distinct=False) for x in again)


def test_blocks_and_given_letters() -> None:
    grid = ["..#", "...", "#.."]
    assert len(slots(grid)) == 6
    assert solve(grid, WORDS + SHORT) == [["AN#", "TEN", "#TO"], ["AT#", "NET", "#NO"]]
    assert solve(["..#", "T..", "#.."], WORDS + SHORT) == [["AN#", "TEN", "#TO"]]
    assert solve(["...", "...", "..."], ["ABC"]) == []


def test_is_filling() -> None:
    grid = ["..#", "...", "#.."]
    assert is_filling(grid, WORDS + SHORT, ["AN#", "TEN", "#TO"])
    assert not is_filling(grid, WORDS + SHORT, ["AN#", "TEN", "#TA"])
    assert not is_filling(grid, WORDS + SHORT, ["ANT", "TEN", "#TO"])


def from_x3c(q, triples):
    """The reduction from exact cover by 3-sets: a q by 3q open grid."""
    across = ["".join("a" if i in t else "b" for i in range(3 * q)) for t in triples]
    down = ["".join("a" if i == j else "b" for i in range(q)) for j in range(q)]
    return ["." * (3 * q)] * q, across + down


def test_reduction_from_exact_cover_by_3_sets() -> None:
    rng = random.Random(62)
    for _ in range(40):
        q = rng.randint(1, 2)
        triples = [tuple(sorted(rng.sample(range(3 * q), 3))) for _ in range(rng.randint(1, 5))]
        cover = any(sorted(i for t in pick for i in t) == list(range(3 * q))
                    for pick in combinations(triples, q))
        grid, words = from_x3c(q, triples)
        assert bool(solve(grid, words, distinct=False, limit=1)) == cover


def test_solver_against_all_assignments() -> None:
    rng = random.Random(61)
    vocab = WORDS + SHORT + ["BEAT", "RATE", "TEAR", "NEAR", "EARN", "AREA", "TOTE", "NOTE"]
    for _ in range(120):
        h, w = rng.randint(1, 3), rng.randint(1, 4)
        grid = ["".join(rng.choice("...#") for _ in range(w)) for _ in range(h)]
        words = rng.sample(vocab, rng.randint(3, 7))
        for distinct in (True, False):
            got = solve(grid, words, distinct)
            assert all(is_filling(grid, words, x, distinct) for x in got)
            assert sorted(got) == brute_force(grid, words, distinct)
