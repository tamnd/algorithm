# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chang-lawler-algorithm/. The authors are listed in prov/K5VMHF.jsonl.

import random

import pytest
from chang_lawler_algorithm import SuffixAutomaton, chang_lawler, live_blocks


def edit_distance(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def brute(pattern: str, text: str, k: int) -> list[int]:
    return [
        j for j in range(len(text) + 1)
        if min(edit_distance(pattern, text[h:j]) for h in range(j + 1)) <= k
    ]


def test_example() -> None:
    assert chang_lawler("GATAA", "CAGATAAGAGAA", 1) == [6, 7, 8, 12]
    assert chang_lawler("survey", "surgery", 2) == [5, 6, 7]
    assert chang_lawler("abc", "xxabcxx", 0) == [5]


def test_edges() -> None:
    assert chang_lawler("", "", 0) == [0]
    assert chang_lawler("", "ab", 0) == [0, 1, 2]
    assert chang_lawler("ab", "", 1) == []
    assert chang_lawler("ab", "", 2) == [0]
    assert chang_lawler("abcd", "", 0) == []
    with pytest.raises(ValueError):
        chang_lawler("a", "a", -1)


def test_suffix_automaton() -> None:
    rng = random.Random(3)
    for _ in range(300):
        p = "".join(rng.choice("acgt") for _ in range(rng.randint(0, 12)))
        t = "".join(rng.choice("acgt") for _ in range(rng.randint(0, 20)))
        sa = SuffixAutomaton(p)
        for i in range(len(t) + 1):
            best = max(L for L in range(len(t) - i + 1) if t[i:i + L] in p)
            assert sa.longest_prefix(t, i) == best


@pytest.mark.parametrize("alphabet", ["ab", "acgt"])
def test_random_against_brute_force(alphabet: str) -> None:
    rng = random.Random(1106 + len(alphabet))
    pruned = 0
    for _ in range(800):
        m = rng.randint(0, 12)
        n = rng.randint(0, 28)
        pattern = "".join(rng.choice(alphabet) for _ in range(m))
        text = "".join(rng.choice(alphabet) for _ in range(n))
        if m and rng.random() < 0.3 and n >= m:
            i = rng.randint(0, n - m)
            text = text[:i] + pattern + text[i + m:]
        k = rng.randint(0, max(0, m // 2))
        if m - k >= 2 and n // ((m - k) // 2) > len(live_blocks(pattern, text, k)):
            pruned += 1
        assert chang_lawler(pattern, text, k) == brute(pattern, text, k)
    assert pruned > 50


def test_long_random_text() -> None:
    rng = random.Random(11)
    for _ in range(40):
        pattern = "".join(rng.choice("acgt") for _ in range(30))
        text = "".join(rng.choice("acgt") for _ in range(300))
        for _ in range(3):
            i = rng.randint(0, 270)
            piece = list(pattern)
            for _ in range(rng.randint(0, 3)):
                piece[rng.randrange(30)] = rng.choice("acgt")
            text = text[:i] + "".join(piece) + text[i + 30:]
        for k in (0, 2, 4):
            from chang_lawler_algorithm import sellers
            assert chang_lawler(pattern, text, k) == sellers(pattern, text, k)
