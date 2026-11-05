# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/levenshtein-automaton/. The authors are listed in prov/CK7G4C.jsonl.

import itertools
import random

from levenshtein_automaton import LevenshteinAutomaton, fuzzy_lookup


def lev(a: str, b: str) -> int:
    d = [[i + j if i * j == 0 else 0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    return d[len(a)][len(b)]


def brute_ends(p: str, t: str, k: int) -> list[int]:
    return [j for j in range(len(t) + 1) if min(lev(p, t[h:j]) for h in range(j + 1)) <= k]


def bound(m: int, k: int) -> int:
    return (m + k + 1) * (k + 2) * 3 ** (2 * k) + 1


def test_example() -> None:
    a = LevenshteinAutomaton("cat", 1)
    assert a.accepts("cat") and a.accepts("cart") and a.accepts("at") and a.accepts("coat")
    assert not a.accepts("act") and not a.accepts("dog") and not a.accepts("")
    words = ["cat", "cart", "act", "at", "coat", "cut", "dog", "cats", "scat", "a", ""]
    assert fuzzy_lookup(words, "cat", 1) == ["at", "cart", "cat", "cats", "coat", "cut", "scat"]
    assert fuzzy_lookup(words, "cat", 0) == ["cat"]
    s = LevenshteinAutomaton("GATAA", 1, search=True)
    assert s.find_ends("CAGATAAGAGAA") == [6, 7, 8, 12]


def test_edges() -> None:
    a = LevenshteinAutomaton("", 0)
    assert a.accepts("") and not a.accepts("a")
    assert LevenshteinAutomaton("", 2).accepts("ab")
    assert not LevenshteinAutomaton("ab", 1).accepts("")
    assert LevenshteinAutomaton("", 0, search=True).find_ends("ab") == [0, 1, 2]
    assert LevenshteinAutomaton("ab", 0, search=True).find_ends("") == []
    assert fuzzy_lookup([], "ab", 1) == []
    assert fuzzy_lookup(["", "a"], "", 0) == [""]


def test_accepts_all_short_strings() -> None:
    rng = random.Random(1985)
    for alphabet in ("ab", "acgt"):
        for _ in range(60):
            w = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 5)))
            k = rng.randint(0, 2)
            a = LevenshteinAutomaton(w, k)
            for n in range(0, 6 if alphabet == "ab" else 4):
                for t in itertools.product(alphabet + "x", repeat=n):
                    x = "".join(t)
                    assert a.accepts(x) == (lev(w, x) <= k)
                    s = a.start
                    for ch in x:
                        s = a.step(s, ch)
                    assert a.distance(s) == min(lev(w, x), k + 1)
            assert a.build_all() <= bound(len(w), k)


def test_random_against_brute_force() -> None:
    rng = random.Random(2002)
    for alphabet in ("ab", "acgt"):
        for _ in range(300):
            w = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 6)))
            k = rng.randint(0, 3)
            words = ["".join(rng.choice(alphabet) for _ in range(rng.randint(0, 8))) for _ in range(rng.randint(0, 12))]
            assert fuzzy_lookup(words, w, k) == sorted({x for x in words if lev(w, x) <= k})
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 12)))
            assert LevenshteinAutomaton(w, k, search=True).find_ends(t) == brute_ends(w, t, k)
