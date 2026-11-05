# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/string-matching-automaton/. The authors are listed in prov/3VKE1X.jsonl.

import random

from string_matching_automaton import StringMatchingAutomaton, automaton_search


def oracle(t: str, p: str) -> list[int]:
    return [s for s in range(len(t) - len(p) + 1) if t.startswith(p, s)]


def sigma_oracle(p: str, w: str) -> int:
    return max(k for k in range(min(len(p), len(w)) + 1) if w.endswith(p[:k]))


def test_example() -> None:
    a = StringMatchingAutomaton("ababaca")
    table = [[a.step(q, ch) for ch in "abc"] for q in range(8)]
    assert table == [[1, 0, 0], [1, 2, 0], [3, 0, 0], [1, 4, 0], [5, 0, 0], [1, 4, 6], [7, 0, 0], [1, 2, 0]]
    assert a.search("abababacaba") == [2]
    assert a.step(5, "z") == 0


def test_edges() -> None:
    assert automaton_search("abc", "") == [0, 1, 2, 3]
    assert automaton_search("", "") == [0]
    assert automaton_search("", "a") == []
    assert automaton_search("ab", "abc") == []
    assert automaton_search("a" * 10, "a" * 4) == list(range(7))
    assert automaton_search("a" * 10, "aaab") == []


def test_states_are_sigma() -> None:
    rng = random.Random(11)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(200):
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 8)))
            t = "".join(rng.choice(alphabet + "z") for _ in range(rng.randint(0, 25)))
            a = StringMatchingAutomaton(p)
            q = 0
            for i, ch in enumerate(t):
                q = a.step(q, ch)
                assert q == sigma_oracle(p, t[: i + 1])


def test_random_against_oracle() -> None:
    rng = random.Random(1968)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(700):
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 40)))
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 7)))
            assert automaton_search(t, p) == oracle(t, p)
