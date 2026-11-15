# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-algebra-consistency/. The authors are listed in prov/TYA2PW.jsonl.

import random
from itertools import combinations, permutations, product

from point_algebra_consistency import EQ, GT, LE, LT, point_algebra_consistency
from qcn import consistent, label, network, point_algebra

PA = point_algebra()
NE = LT | GT
ALL = LT | EQ | GT


def holds(v, net) -> bool:
    return all(r >> PA.base_of(v[i], v[j]) & 1 for (i, j), r in net.items())


def integer_solution(n, net):
    """Search all assignments with values in 0 .. n-1. Any solution can be
    renumbered into this range, so this decides consistency."""
    for v in product(range(n), repeat=n):
        if holds(v, net):
            return v
    return None


def path_consistent(n, net) -> bool:
    """Path consistency written out with the 3 x 3 table, for comparison."""
    r = {(i, j): label(PA, net, i, j) for i, j in permutations(range(n), 2)}
    changed = True
    while changed:
        changed = False
        for i, j, k in permutations(range(n), 3):
            t = r[(i, j)] & PA.compose(r[(i, k)], r[(k, j)])
            if t != r[(i, j)]:
                r[(i, j)], r[(j, i)] = t, PA.converse(t)
                changed = True
    return all(r.values())


def random_net(rng, n, density, labels):
    return {p: rng.choice(labels) for p in combinations(range(n), 2) if rng.random() < density}


def test_masks_match_qcn() -> None:
    assert (LT, EQ, GT) == (PA.rel("<"), PA.rel("="), PA.rel(">"))


def test_example() -> None:
    # x0 <= x1 <= x2 <= x0 forces x0 = x1 = x2; x3 != x2 and x3 <= x0 then give x3 < x0.
    net = {(0, 1): LE, (1, 2): LE, (0, 2): EQ | GT, (2, 3): NE, (0, 3): EQ | GT}
    v = point_algebra_consistency(4, net)
    assert v is not None and holds(v, net)
    assert v[0] == v[1] == v[2] > v[3]
    net[(1, 3)] = EQ
    assert point_algebra_consistency(4, net) is None


def test_not_equal_inside_a_cycle() -> None:
    assert point_algebra_consistency(2, {(0, 1): LE | GT}) is not None
    assert point_algebra_consistency(3, {(0, 1): LE, (1, 2): LE, (0, 2): GT | EQ}) is not None
    assert point_algebra_consistency(3, {(0, 1): LE, (1, 2): LE, (0, 2): GT}) is None
    cycle = {(0, 1): LE, (1, 2): LE, (0, 2): GT | EQ, (0, 3): EQ}
    assert point_algebra_consistency(4, cycle) is not None
    assert point_algebra_consistency(4, {**cycle, (1, 3): NE}) is None


def test_edges() -> None:
    assert point_algebra_consistency(0, {}) == []
    assert point_algebra_consistency(1, {}) == [0]
    assert point_algebra_consistency(2, {(0, 1): 0}) is None
    assert point_algebra_consistency(2, {(0, 1): ALL}) is not None
    v = point_algebra_consistency(3, {(0, 1): EQ, (1, 2): LT})
    assert v[0] == v[1] < v[2]


def test_against_brute_force_and_integers() -> None:
    rng = random.Random(21)
    labels = [LT, GT, LT, GT, EQ, LE, EQ | GT, NE, ALL]
    seen = [0, 0]
    for _ in range(600):
        n = rng.randint(1, 5)
        net = random_net(rng, n, 0.6 + 0.4 * rng.random(), labels)
        v = point_algebra_consistency(n, net)
        full = network(PA, n, [(i, j, r) for (i, j), r in net.items()])
        oracle = consistent(PA, n, full)
        ints = integer_solution(n, net) if n <= 4 else oracle
        assert (v is None) == (oracle is None) == (ints is None)
        assert (v is not None) == path_consistent(n, full)
        if v is not None:
            assert holds(v, net)
            assert sorted(set(v)) == list(range(len(set(v))))
        seen[v is None] += 1
    assert min(seen) > 100


def test_larger_networks_against_path_consistency() -> None:
    rng = random.Random(22)
    labels = [LT, LE, EQ | GT, NE, NE, ALL, EQ]
    for _ in range(40):
        n = rng.randint(6, 12)
        net = random_net(rng, n, 0.3, labels)
        v = point_algebra_consistency(n, net)
        assert (v is not None) == path_consistent(n, network(PA, n, [(i, j, r) for (i, j), r in net.items()]))
        if v is not None:
            assert holds(v, net)


def test_long_chain() -> None:
    n = 3000
    net = {(i, i + 1): LE for i in range(n - 1)}
    v = point_algebra_consistency(n, net)
    assert v == list(range(n))
    net[(0, n - 1)] = EQ | GT  # closes the cycle: all points equal
    v = point_algebra_consistency(n, net)
    assert v == [0] * n
    net[(5, 6)] = LT
    assert point_algebra_consistency(n, net) is None
