# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eades-mckay-algorithm/. The authors are listed in prov/W2DJTJ.jsonl.

import itertools
import random
from functools import lru_cache
from math import comb

import pytest

from eades_mckay_algorithm import eades_mckay, eades_mckay_combinations, eades_mckay_strings


@lru_cache(maxsize=None)
def ref_k(s: int, t: int) -> tuple[str, ...]:
    """K_st from Knuth (31): 0 K_(s-1)t, 10 K^R_(s-1)(t-1), 11 K_s(t-2)."""
    if s < 0 or t < 0:
        return ()
    if t == 0:
        return ("0" * s,)
    if s == 0:
        return ("1" * t,)
    return (
        tuple("0" + x for x in ref_k(s - 1, t))
        + tuple("10" + x for x in reversed(ref_k(s - 1, t - 1)))
        + tuple("11" + x for x in ref_k(s, t - 2))
    )


@lru_cache(maxsize=None)
def ref_e(n: int, k: int) -> tuple[str, ...]:
    """E(n, k) of Ruskey (5.5) with Algorithm 5.8, strings b_1 ... b_n."""
    if k == 0:
        return ("0" * n,)
    if k == n:
        return ("1" * n,)
    if k == 1:
        return tuple("0" * i + "1" + "0" * (n - 1 - i) for i in range(n))
    return (
        tuple(x + "0" for x in ref_e(n - 1, k))
        + tuple(x + "01" for x in reversed(ref_e(n - 2, k - 1)))
        + tuple(x + "11" for x in ref_e(n - 2, k - 2))
    )


def homogeneous_step(u: str, v: str) -> bool:
    d = [i for i in range(len(u)) if u[i] != v[i]]
    if len(d) != 2 or u[d[0]] == u[d[1]]:
        return False
    return all(u[i] == "0" for i in range(d[0] + 1, d[1]))


def test_knuth_list() -> None:
    # Knuth, Section 7.2.1.3, (32) and (33): K_33 as bit strings and finger patterns.
    bits = (
        "000111 001011 001101 001110 010110 010101 010011 011001 011010 011100 "
        "101100 101001 101010 100110 100101 100011 110001 110010 110100 111000"
    ).split()
    assert eades_mckay_strings(3, 3) == bits
    fingers = "210 310 320 321 421 420 410 430 431 432 532 530 531 521 520 510 540 541 542 543".split()
    assert ["".join(map(str, c)) for c in eades_mckay_combinations(6, 3)] == fingers


def test_edges() -> None:
    assert eades_mckay_strings(0, 0) == [""]
    assert eades_mckay_strings(4, 0) == ["0000"]
    assert eades_mckay_strings(0, 4) == ["1111"]
    assert eades_mckay_strings(3, 1) == ["0001", "0010", "0100", "1000"]
    assert eades_mckay_strings(1, 2) == ["011", "101", "110"]
    assert eades_mckay_combinations(3, 4) == []
    assert eades_mckay_combinations(3, -1) == []
    with pytest.raises(ValueError):
        list(eades_mckay(0, -1))
    with pytest.raises(ValueError):
        eades_mckay_combinations(-2, 0)


def test_against_references() -> None:
    for s in range(0, 9):
        for t in range(0, 9):
            got = eades_mckay_strings(s, t)
            assert got == list(ref_k(s, t))
            n = s + t
            if n:
                assert [x[::-1] for x in got] == list(ref_e(n, t))
            assert len(got) == comb(n, t) == len(set(got))
            every = {"".join("1" if i in c else "0" for i in range(n)) for c in itertools.combinations(range(n), t)}
            assert set(got) == every
            for u, v in zip(got, got[1:]):
                assert homogeneous_step(u, v)
            assert got[0] == "0" * s + "1" * t
            assert got[-1] == "1" * t + "0" * s


def test_random_sizes_one_index_changes() -> None:
    rng = random.Random(11)
    for _ in range(20):
        n = rng.randrange(0, 15)
        k = rng.randrange(0, n + 1)
        lst = eades_mckay_combinations(n, k)
        assert len(lst) == comb(n, k)
        for u, v in zip(lst, lst[1:]):
            assert sum(1 for i in range(k) if u[i] != v[i]) == 1
