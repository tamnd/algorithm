# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knuth-morris-pratt/. The authors are listed in prov/F0V6W1.jsonl.

import random

from knuth_morris_pratt import compute_next, compute_prefix_function, knuth_morris_pratt


def oracle(t: str, p: str) -> list[int]:
    return [s for s in range(len(t) - len(p) + 1) if t.startswith(p, s)]


def border_oracle(p: str) -> list[int]:
    return [max(k for k in range(q + 1) if p[:k] == p[q + 1 - k : q + 1]) for q in range(len(p))]


def next_oracle(p: str) -> list[int]:
    m = len(p)
    out = []
    for q in range(m):
        ks = [k for k in range(q) if p[:k] == p[q - k : q] and p[k] != p[q]]
        out.append(max(ks) if ks else -1)
    return out + [border_oracle(p)[-1]]


def test_example() -> None:
    p = "abacabab"
    assert compute_prefix_function(p) == [0, 0, 1, 0, 1, 2, 3, 2]
    assert compute_next(p) == [-1, 0, -1, 1, -1, 0, -1, 3, 2]
    assert knuth_morris_pratt("abacabcabacababa", p) == [7]


def test_edges() -> None:
    assert knuth_morris_pratt("abc", "") == [0, 1, 2, 3]
    assert knuth_morris_pratt("", "") == [0]
    assert knuth_morris_pratt("", "a") == []
    assert knuth_morris_pratt("ab", "abc") == []
    assert knuth_morris_pratt("a", "a") == [0]
    assert knuth_morris_pratt("a" * 10, "a" * 4) == list(range(7))
    assert knuth_morris_pratt("a" * 10, "aaab") == []


def test_overlap_after_match() -> None:
    # after a match the search must continue from nxt[m] = pi[m-1], not from 0
    assert knuth_morris_pratt("abababab", "abab") == [0, 2, 4]
    assert knuth_morris_pratt("aaaaa", "aa") == [0, 1, 2, 3]


def test_tables_against_definition() -> None:
    rng = random.Random(77)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(300):
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 12)))
            assert compute_prefix_function(p) == border_oracle(p)
            assert compute_next(p) == next_oracle(p)


def test_random_against_oracle() -> None:
    rng = random.Random(9001)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(700):
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 40)))
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 7)))
            assert knuth_morris_pratt(t, p) == oracle(t, p)


def test_lists() -> None:
    assert knuth_morris_pratt([0, 1, 0, 1, 0], [0, 1, 0]) == [0, 2]
