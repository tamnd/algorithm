# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/split-decomposition/. The authors are listed in prov/C536CB.jsonl.

import random
from fractions import Fraction
from itertools import combinations

import pytest

from split_decomposition import isolation_index, residue, split_decomposition, split_metric

F = Fraction


def metric_from_splits(n, weighted):
    return [[sum((w * split_metric(n, s, i, j) for s, w in weighted.items()), F(0)) for j in range(n)] for i in range(n)]


def brute(d):
    """Isolation index of every split of the taxa, by the definition."""
    n = len(d)
    out = {}
    for mask in range(1, 1 << n):
        if mask & 1:
            continue  # the stored side does not hold taxon 0
        side = frozenset(i for i in range(n) if mask >> i & 1)
        rest = [i for i in range(n) if i not in side]
        a = isolation_index(d, sorted(side), rest)
        if a > 0:
            out[side] = a
    return out


def weakly_compatible(n, splits):
    """No three splits and four taxa t0..t3 with t0, ti together and tj, tk apart from them in split i."""
    sides = list(splits)
    for s1, s2, s3 in combinations(sides, 3):
        for t in combinations(range(n), 4):
            for order in _orders(t):
                t0, t1, t2, t3 = order
                bad = True
                for s, ti, tj, tk in ((s1, t1, t2, t3), (s2, t2, t1, t3), (s3, t3, t1, t2)):
                    same = (t0 in s) == (ti in s)
                    other = (tj in s) == (tk in s) and (tj in s) != (t0 in s)
                    if not (same and other):
                        bad = False
                        break
                if bad:
                    return False
    return True


def _orders(t):
    from itertools import permutations
    return permutations(t)


def circular_splits(n):
    out = []
    for i in range(n):
        for j in range(i + 1, n):
            side = frozenset(range(i, j)) if i > 0 else frozenset(range(j, n))
            if 1 <= len(side) <= n - 1:
                out.append(side)
    return list(set(out))


# The page example: a circular split system on a, b, c, d, e = 0..4.
EXAMPLE = {
    frozenset([1]): F(1), frozenset([2]): F(1), frozenset([3]): F(1), frozenset([4]): F(1), frozenset([1, 2, 3, 4]): F(1),
    frozenset([2, 3, 4]): F(3), frozenset([1, 2]): F(2),
}


def test_example_from_page():
    d = metric_from_splits(5, EXAMPLE)
    assert d[0][1] == 4 and d[0][2] == 7 and d[1][3] == 7 and d[0][3] == 5
    got = split_decomposition(d)
    assert got == EXAMPLE
    assert got == brute(d)
    assert all(x == 0 for row in residue(d, got) for x in row)


def test_four_points_by_hand():
    # d(a,b)=3, d(c,d)=3, d(a,c)=d(b,d)=5, d(a,d)=d(b,c)=6
    d = [[F(0), F(3), F(5), F(6)], [F(3), F(0), F(6), F(5)], [F(5), F(6), F(0), F(3)], [F(6), F(5), F(3), F(0)]]
    got = split_decomposition(d)
    # the page trace: a|b = 3; then a|bc = 1, ab|c = 4, ac|b = 2; then six d-splits
    assert isolation_index(d, [0], [1]) == 3
    assert [isolation_index(d, a, b) for a, b in (([0], [1, 2]), ([0, 1], [2]), ([0, 2], [1]))] == [1, 4, 2]
    assert isolation_index(d, [0, 3], [1, 2]) == 0
    assert got == {frozenset([1]): 1, frozenset([2]): 1, frozenset([3]): 1, frozenset([1, 2, 3]): 1, frozenset([2, 3]): 3, frozenset([1, 3]): 1}
    assert got == brute(d)
    assert all(x == 0 for row in residue(d, got) for x in row)


def test_split_prime_residue():
    # K_{3,2} graph metric: d = 1 between the parts, 2 inside a part. It has no d-splits.
    n = 5
    part = [0, 0, 0, 1, 1]
    d = [[F(0) if i == j else (F(1) if part[i] != part[j] else F(2)) for j in range(n)] for i in range(n)]
    got = split_decomposition(d)
    assert got == brute(d)
    assert got == {}
    assert residue(d, got) == d


def test_small_inputs():
    assert split_decomposition([]) == {}
    assert split_decomposition([[F(0)]]) == {}
    assert split_decomposition([[F(0), F(2)], [F(2), F(0)]]) == {frozenset([1]): F(2)}
    with pytest.raises(ValueError):
        split_decomposition([[F(0), F(1)], [F(2), F(0)]])


@pytest.mark.parametrize("seed", range(5))
def test_random_matrices_against_definition(seed):
    rng = random.Random(seed)
    for _ in range(25):
        n = rng.randint(3, 7)
        d = [[F(0)] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                d[i][j] = d[j][i] = F(rng.randint(1, 12), rng.randint(1, 3))
        got = split_decomposition(d)
        assert got == brute(d)
        assert len(got) <= n * (n - 1) // 2
        assert weakly_compatible(n, got)


@pytest.mark.parametrize("seed", range(4))
def test_residue_is_split_prime(seed):
    rng = random.Random(40 + seed)
    for _ in range(15):
        n = rng.randint(4, 7)
        d = [[F(0)] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                d[i][j] = d[j][i] = F(rng.randint(1, 9))
        got = split_decomposition(d)
        d0 = residue(d, got)
        assert brute(d0) == {}
        assert all(d0[i][j] >= 0 for i in range(n) for j in range(n))


@pytest.mark.parametrize("seed", range(4))
def test_weighted_circular_systems_are_recovered(seed):
    rng = random.Random(80 + seed)
    for _ in range(15):
        n = rng.randint(4, 8)
        perm = list(range(n))
        rng.shuffle(perm)
        pool = circular_splits(n)
        chosen = rng.sample(pool, rng.randint(1, len(pool)))
        weighted = {}
        for s in chosen:
            side = frozenset(perm[i] for i in s)
            if 0 in side:
                side = frozenset(range(n)) - side
            weighted[side] = F(rng.randint(1, 6), rng.randint(1, 2))
        d = metric_from_splits(n, weighted)
        assert split_decomposition(d) == weighted


@pytest.mark.parametrize("seed", range(3))
def test_tree_metrics_give_the_tree(seed):
    rng = random.Random(120 + seed)
    for _ in range(15):
        n = rng.randint(3, 8)
        # random compatible system: splits of a random tree built by nesting clusters
        clusters = {frozenset([i]) for i in range(n)}
        items = [frozenset([i]) for i in range(n)]
        while len(items) > 2:
            i, j = rng.sample(range(len(items)), 2)
            c = items[i] | items[j]
            items = [x for t, x in enumerate(items) if t not in (i, j)] + [c]
            clusters.add(c)
        weighted = {}
        for c in clusters:
            side = c if 0 not in c else frozenset(range(n)) - c
            if 1 <= len(side) <= n - 1:
                weighted[side] = weighted.get(side, F(0)) + F(rng.randint(1, 5))
        d = metric_from_splits(n, weighted)
        assert split_decomposition(d) == weighted
