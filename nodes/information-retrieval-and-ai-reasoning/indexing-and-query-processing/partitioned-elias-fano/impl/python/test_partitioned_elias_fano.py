# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partitioned-elias-fano/. The authors are listed in prov/PX2K2C.jsonl.

import bisect
import math
import random

from partitioned_elias_fano import (
    BITMAP,
    EF,
    RUN,
    PartitionedEliasFano,
    chunk_bits,
    ef_bits,
    ef_encode,
    optimal_partition,
    partition_cost,
    uniform_partition,
)

EXAMPLE = [0, 1, 2, 3, 4, 5, 6, 7, 40, 100, 160, 220, 300, 301, 303, 304, 306, 307, 309, 310]


def brute_force_best(x: list[int], fixed: int) -> int:
    """Try every set of cut points between 1 and n - 1."""
    n = len(x)
    best = None
    for mask in range(1 << (n - 1)):
        cuts = [0] + [i for i in range(1, n) if mask >> (i - 1) & 1] + [n]
        c = partition_cost(x, cuts, fixed)
        best = c if best is None or c < best else best
    return best


def check_structure(p: PartitionedEliasFano, x: list[int]) -> None:
    assert p.decode() == x and len(p) == len(x)
    total = 0
    for (kind, base, u, b, payload), i, j in zip(p.chunks, p.cuts, p.cuts[1:]):
        assert b == j - i and base == (0 if i == 0 else x[i - 1] + 1) and u == x[j - 1] - base + 1
        if kind == RUN:
            assert b == u and payload == ""
        elif kind == BITMAP:
            assert len(payload) == u <= ef_bits(b, u) and payload.count("1") == b
        else:
            assert kind == EF and len(payload) == ef_bits(b, u) < u
        assert len(payload) == chunk_bits(b, u)
        total += p.fixed + len(payload)
    assert p.bits() == total == partition_cost(x, p.cuts, p.fixed)


def test_ef_bits_formula() -> None:
    for b in range(1, 40):
        for u in range(b, 300):
            lw = math.floor(math.log2(u / b)) if u > b else 0
            while (b << (lw + 1)) <= u:
                lw += 1
            while lw > 0 and (b << lw) > u:
                lw -= 1
            want = b * lw + b + (u - 1) // (1 << lw) + 1
            assert ef_bits(b, u) == want
            vals = sorted(random.Random(b * 1000 + u).sample(range(u), b))
            assert len(ef_encode(vals, u)) == want


def test_example() -> None:
    p = PartitionedEliasFano(EXAMPLE, fixed=10)
    assert p.cuts == [0, 8, 13, 20]
    assert [c[0] for c in p.chunks] == [RUN, EF, BITMAP]
    assert [len(c[4]) for c in p.chunks] == [0, 40, 10]
    assert p.chunks[1][4] == "0000011100110001010000100010100100100010"
    assert p.bits() == 80
    assert partition_cost(EXAMPLE, [0, 20], 10) == 129
    assert partition_cost(EXAMPLE, uniform_partition(20, 4), 10) == 113
    assert partition_cost(EXAMPLE, uniform_partition(20, 5), 10) == 115
    assert p.access(10) == 160 and p.next_geq(150) == 10 and p.next_geq(302) == 14 and p.next_geq(311) == 20
    check_structure(p, EXAMPLE)


def test_edge_cases() -> None:
    p = PartitionedEliasFano([])
    assert len(p) == 0 and p.decode() == [] and p.next_geq(0) == 0 and p.bits() == 0
    p = PartitionedEliasFano([0])
    assert p.chunks[0][0] == RUN and p.access(0) == 0 and p.next_geq(1) == 1
    p = PartitionedEliasFano([5])
    assert p.decode() == [5] and p.next_geq(0) == 0
    big = [0, 1, 2, 10 ** 9, 10 ** 9 + 1, 2 ** 40]
    p = PartitionedEliasFano(big)
    check_structure(p, big)
    dense = list(range(100, 200))
    p = PartitionedEliasFano(dense)
    check_structure(p, dense)
    for bad in ([1, 1], [3, 2], [-1, 4]):
        try:
            PartitionedEliasFano(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("bad input was accepted")
    try:
        PartitionedEliasFano([1, 2]).access(2)
    except IndexError:
        pass
    else:
        raise AssertionError("access out of range was accepted")


def test_dp_against_brute_force() -> None:
    rng = random.Random(20261120)
    for _ in range(250):
        n = rng.randint(1, 12)
        u = rng.choice([n, n + 3, 2 * n, 10 * n, 1000])
        x = sorted(rng.sample(range(u), n))
        fixed = rng.choice([0, 1, 4, 10, 30])
        cost, cuts = optimal_partition(x, fixed)
        assert cuts[0] == 0 and cuts[-1] == n and cuts == sorted(set(cuts))
        assert partition_cost(x, cuts, fixed) == cost == brute_force_best(x, fixed)


def test_random_lists() -> None:
    rng = random.Random(20261121)
    for _ in range(300):
        n = rng.randint(1, 120)
        # mix dense runs and sparse stretches
        x: list[int] = []
        v = rng.randint(0, 5)
        while len(x) < n:
            x.append(v)
            v += 1 if rng.random() < 0.5 else rng.randint(2, rng.choice([4, 50, 5000]))
        size = rng.choice([None, 1, 3, 8, 128])
        p = PartitionedEliasFano(x, chunk_size=size)
        check_structure(p, x)
        if size is None:
            for s in (1, 4, 16, n):
                assert p.bits() <= partition_cost(x, uniform_partition(n, s), p.fixed)
        for q in range(n):
            assert p.access(q) == x[q]
        for y in rng.sample(range(-2, x[-1] + 3), min(30, x[-1] + 5)):
            assert p.next_geq(y) == bisect.bisect_left(x, y)
