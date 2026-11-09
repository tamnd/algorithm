# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/composition-generation/. The authors are listed in prov/45NXTX.jsonl.

import itertools
import math
import random

from composition_generation import compositions, extra_writes


def from_cuts(n: int, bits: tuple[int, ...]) -> tuple[int, ...]:
    """The composition of n whose cut set is {i : bits[i - 1] = 1}."""
    parts = []
    run = 1
    for b in bits:
        if b:
            parts.append(run)
            run = 1
        else:
            run += 1
    parts.append(run)
    return tuple(parts)


def brute_force(n: int) -> set[tuple[int, ...]]:
    """All compositions of n, from all sequences of positive parts, with an explicit stack."""
    out = set()
    stack = [((), n)]
    while stack:
        prefix, rest = stack.pop()
        if rest == 0:
            out.add(prefix)
            continue
        for j in range(1, rest + 1):
            stack.append((prefix + (j,), rest - j))
    return out


def test_edge_cases():
    assert list(compositions(0)) == [()]
    assert list(compositions(1)) == [(1,)]
    assert list(compositions(2)) == [(1, 1), (2,)]
    assert extra_writes(0) == 0
    assert extra_writes(1) == 0
    try:
        list(compositions(-1))
    except ValueError:
        pass
    else:
        raise AssertionError("negative n must raise ValueError")


def test_small_list():
    expected = [(1, 1, 1, 1), (1, 1, 2), (1, 2, 1), (1, 3), (2, 1, 1), (2, 2), (3, 1), (4,)]
    assert list(compositions(4)) == expected


def test_matches_brute_force():
    for n in range(0, 13):
        got = list(compositions(n))
        assert len(got) == len(set(got))
        assert set(got) == brute_force(n)


def test_counts_closed_form():
    for n in range(1, 19):
        got = list(compositions(n))
        assert len(got) == 2 ** (n - 1)
        by_length = [0] * (n + 1)
        for c in got:
            assert sum(c) == n and min(c) >= 1
            by_length[len(c)] += 1
        for k in range(1, n + 1):
            assert by_length[k] == math.comb(n - 1, k - 1)
        total_parts = (n + 1) * 2 ** (n - 2) if n >= 2 else 1
        assert sum(len(c) for c in got) == total_parts


def test_lexicographic_order():
    for n in range(0, 16):
        got = list(compositions(n))
        assert got == sorted(got)


def test_order_is_binary_countdown_of_cut_set():
    rng = random.Random(20261109)
    for n in range(1, 15):
        got = list(compositions(n))
        assert got == [from_cuts(n, bits) for bits in itertools.product((1, 0), repeat=n - 1)]
        for _ in range(20):
            bits = tuple(rng.randrange(2) for _ in range(n - 1))
            value = int("".join(map(str, bits)), 2) if bits else 0
            assert got[2 ** (n - 1) - 1 - value] == from_cuts(n, bits)


def test_successor_rule_and_extra_writes():
    for n in range(1, 17):
        got = list(compositions(n))
        total = 0
        worst = 0
        for c, d in zip(got, got[1:]):
            assert d == c[:-2] + (c[-2] + 1,) + (1,) * (c[-1] - 1)
            total += c[-1] - 1
            worst = max(worst, c[-1] - 1)
        assert total == extra_writes(n) == 2 ** (n - 1) - n
        assert worst == max(0, n - 2)


def test_larger_n_counts_only():
    assert extra_writes(22) == 2**21 - 22
