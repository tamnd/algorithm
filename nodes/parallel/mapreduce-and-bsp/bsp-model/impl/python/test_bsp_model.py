# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bsp-model/. The authors are listed in prov/C7AB2T.jsonl.

import itertools
import random

import pytest

from bsp_model import (BSP, broadcast_direct, broadcast_tree, broadcast_two_phase, ceil_log2,
                       prefix_sums, sort_regular_sampling)

PS = [1, 2, 3, 4, 5, 7, 8, 9, 16]


def split_blocks(a, p):
    n = len(a)
    return [a[(i * n) // p:((i + 1) * n) // p] for i in range(p)]


def test_barrier_hides_messages_of_the_same_superstep():
    m = BSP(3)

    def step(i, st, inbox):
        st["seen"] = list(inbox)
        return 1, [((i + 1) % 3, i)]

    m.superstep(step)
    assert all(st["seen"] == [] for st in m.state)
    m.superstep(step)
    assert [st["seen"] for st in m.state] == [[(2, 2)], [(0, 0)], [(1, 1)]]
    assert [(s.w, s.h) for s in m.log] == [(1, 1), (1, 1)]
    assert m.cost(g=3, L=10) == 2 * (1 + 3 + 10)


def test_broadcast_direct_and_tree():
    for p in PS:
        for root in {0, p - 1, p // 2}:
            out, m = broadcast_direct(p, "x", root)
            assert out == ["x"] * p
            W, H, S = m.totals()
            assert (W, H, S) == (0, p - 1, 1)
            assert m.cost(4, 50) == 4 * (p - 1) + 50
            out, m = broadcast_tree(p, 7, root)
            assert out == [7] * p
            assert len(m.log) == ceil_log2(p)
            assert all(s.h == 1 for s in m.log)
            assert m.cost(4, 50) == ceil_log2(p) * (4 + 50)


def test_broadcast_two_phase():
    rng = random.Random(3)
    for p in PS:
        for n in [0, 1, p - 1, p, p + 1, 3 * p, 50]:
            data = [rng.randint(0, 99) for _ in range(n)]
            out, m = broadcast_two_phase(p, data, root=rng.randrange(p))
            assert out == [data] * p
            assert len(m.log) == 2
            bound = (p - 1) * -(-n // p)
            assert all(s.h <= bound for s in m.log)
            if p > 1 and n % p == 0:
                assert all(s.h == bound for s in m.log)  # equal pieces: the bound is exact


def test_prefix_sums():
    rng = random.Random(5)
    for p in PS:
        for n in [0, 1, p, p + 3, 4 * p, 37]:
            a = [rng.randint(-9, 9) for _ in range(n)]
            blocks = split_blocks(a, p)
            out, m = prefix_sums(blocks)
            assert sum(out, []) == list(itertools.accumulate(a))
            s1, s2 = m.log
            assert s1.h == (p - 1)
            assert s2.h == 0
            assert s1.w == max(len(b) for b in blocks)
            assert s2.w == max(i + len(b) for i, b in enumerate(blocks))
            W, H, S = m.totals()
            assert W <= 2 * -(-n // p) + p - 1 and H == p - 1 and S == 2
            assert m.cost(2, 9) == W + 2 * H + 2 * 9


def test_sort_regular_sampling_result_and_costs():
    rng = random.Random(11)
    for p in PS:
        for m_items in sorted({p, p + 1, 2 * p, p * p, 3 * p + 2}):
            for top in (3, 10 ** 6):  # many equal keys, and few
                a = [rng.randint(0, top) for _ in range(p * m_items)]
                blocks = split_blocks(a, p)
                out, mach = sort_regular_sampling(blocks)
                assert sum(out, []) == sorted(a)
                s1, s2, s3, s4 = mach.log
                assert s1.h == p * (p - 1)
                assert s2.h == (p - 1) ** 2
                assert s4.h == 0
                assert s1.w <= m_items * ceil_log2(m_items)
                assert s2.w <= p * p * ceil_log2(p * p)
                assert s3.w <= m_items + p - 1
                biggest = max(len(b) for b in out)
                assert s4.w <= biggest * ceil_log2(p)
                if m_items % p == 0:
                    bound = 2 * m_items - m_items // p - p + 1  # the bucket bound proved on the page
                    assert biggest <= bound
                    assert s3.h <= bound
                assert mach.cost(3, 20) == sum(s.w + 3 * s.h + 20 for s in mach.log)


def test_sort_rejects_unequal_or_small_blocks():
    with pytest.raises(ValueError):
        sort_regular_sampling([[1, 2], [3]])
    with pytest.raises(ValueError):
        sort_regular_sampling([[1], [2], [3]])


def test_bucket_bound_is_reached():
    # p = 2, m = 4: the bound 2m - m/p - p + 1 = 5 is reached, over all inputs.
    best = 0
    for perm in itertools.permutations(range(8)):
        if perm[:4] != tuple(sorted(perm[:4])) or perm[4:] != tuple(sorted(perm[4:])):
            continue
        out, _ = sort_regular_sampling([list(perm[:4]), list(perm[4:])])
        best = max(best, max(len(b) for b in out))
    assert best == 5
    out, _ = sort_regular_sampling([[0, 1, 2, 6], [3, 4, 5, 7]])
    assert [len(b) for b in out] == [5, 3]
