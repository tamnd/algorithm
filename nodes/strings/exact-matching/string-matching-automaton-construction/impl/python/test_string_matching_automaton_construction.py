# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/string-matching-automaton-construction/. The authors are listed in prov/HCTKVB.jsonl.

import random

from string_matching_automaton_construction import (
    automaton_search,
    compute_transition_function,
    compute_transition_function_naive,
)


def oracle(t: list[int], p: list[int]) -> list[int]:
    return [s for s in range(len(t) - len(p) + 1) if t[s : s + len(p)] == p]


def enc(s: str) -> list[int]:
    return [ord(ch) - ord("a") for ch in s]


def test_example() -> None:
    delta = compute_transition_function(enc("ababaca"), 3)
    assert delta == [
        [1, 0, 0],
        [1, 2, 0],
        [3, 0, 0],
        [1, 4, 0],
        [5, 0, 0],
        [1, 4, 6],
        [7, 0, 0],
        [1, 2, 0],
    ]
    assert automaton_search(enc("abababacaba"), enc("ababaca"), 3) == [2]


def test_edges() -> None:
    assert compute_transition_function([], 2) == [[0, 0]]
    assert automaton_search(enc("abc"), [], 3) == [0, 1, 2, 3]
    assert automaton_search([], [], 1) == [0]
    assert automaton_search([], [0], 1) == []
    assert automaton_search(enc("ab"), enc("abc"), 3) == []
    assert automaton_search([0] * 10, [0] * 4, 1) == list(range(7))
    assert automaton_search([0] * 10, enc("aaab"), 2) == []


def test_table_against_naive() -> None:
    rng = random.Random(5)
    for sigma in (1, 2, 4):
        for _ in range(300):
            p = [rng.randrange(sigma) for _ in range(rng.randint(0, 9))]
            assert compute_transition_function(p, sigma) == compute_transition_function_naive(p, sigma)


def test_random_against_oracle() -> None:
    rng = random.Random(1990)
    for sigma in (1, 2, 4):
        for _ in range(700):
            t = [rng.randrange(sigma) for _ in range(rng.randint(0, 40))]
            p = [rng.randrange(sigma) for _ in range(rng.randint(0, 7))]
            assert automaton_search(t, p, sigma) == oracle(t, p)
