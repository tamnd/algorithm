# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chase-sequence/. The authors are listed in prov/BN89EB.jsonl.

import itertools
import random
from functools import lru_cache
from math import comb

import pytest

from chase_sequence import chase, chase_combinations, chase_strings


@lru_cache(maxsize=None)
def ref_a(s: int, t: int) -> tuple[str, ...]:
    """A_st = 1 B_s(t-1), 0 A^R_(s-1)t, from Knuth (35)."""
    if s < 0 or t < 0:
        return ()
    if s == 0 and t == 0:
        return ("",)
    return tuple("1" + x for x in ref_b(s, t - 1)) + tuple("0" + x for x in reversed(ref_a(s - 1, t)))


@lru_cache(maxsize=None)
def ref_b(s: int, t: int) -> tuple[str, ...]:
    """B_st = 1 A_s(t-1), 0 A_(s-1)t, from Knuth (35)."""
    if s < 0 or t < 0:
        return ()
    if s == 0 and t == 0:
        return ("",)
    return tuple("1" + x for x in ref_a(s, t - 1)) + tuple("0" + x for x in ref_a(s - 1, t))


def reference(s: int, t: int) -> list[str]:
    return list(ref_a(s, t) if (s + t) % 2 else ref_b(s, t))


def near_perfect_step(u: str, v: str) -> bool:
    d = [i for i in range(len(u)) if u[i] != v[i]]
    if len(d) != 2 or u[d[0]] == u[d[1]]:
        return False
    if d[1] - d[0] == 1:
        return True
    return d[1] - d[0] == 2 and u[d[0] + 1] == "0"


def test_knuth_table() -> None:
    # Knuth, Section 7.2.1.3, Table 2: C_33 = B_33 in index form c3 c2 c1.
    want = "543 542 540 541 521 520 510 530 531 532 432 430 431 421 420 410 210 310 320 321".split()
    got = ["".join(map(str, c)) for c in chase_combinations(6, 3)]
    assert got == want


def test_small_lists() -> None:
    assert chase_strings(2, 2) == ["1100", "1001", "1010", "0110", "0101", "0011"]
    assert chase_strings(2, 1) == ["100", "001", "010"]


def test_edges() -> None:
    assert chase_strings(0, 0) == [""]
    assert chase_strings(3, 0) == ["000"]
    assert chase_strings(0, 3) == ["111"]
    assert chase_combinations(4, 5) == []
    assert chase_combinations(4, -1) == []
    assert chase_combinations(0, 0) == [()]
    with pytest.raises(ValueError):
        list(chase(-1, 2))
    with pytest.raises(ValueError):
        chase_combinations(-1, 0)


def test_against_reference_and_near_perfect() -> None:
    for s in range(0, 9):
        for t in range(0, 9):
            got = chase_strings(s, t)
            assert got == reference(s, t)
            n = s + t
            assert len(got) == comb(n, t) == len(set(got))
            every = {"".join("1" if i in c else "0" for i in range(n)) for c in itertools.combinations(range(n), t)}
            assert set(got) == every
            for u, v in zip(got, got[1:]):
                assert near_perfect_step(u, v)
            assert got[0] == "1" * t + "0" * s
            if t > 0:
                q = min(s, 1 if n % 2 else 2)
                assert got[-1] == "0" * q + "1" * t + "0" * (s - q)


def test_random_sizes_index_form() -> None:
    rng = random.Random(7)
    for _ in range(20):
        n = rng.randrange(0, 15)
        k = rng.randrange(0, n + 1)
        lst = chase_combinations(n, k)
        assert len(lst) == comb(n, k)
        for u, v in zip(lst, lst[1:]):
            changed = [i for i in range(k) if u[i] != v[i]]
            assert len(changed) == 1
            assert abs(u[changed[0]] - v[changed[0]]) in (1, 2)
