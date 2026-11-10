# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sidney-decomposition/. The authors are listed in prov/YXCAK6.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from sidney_decomposition import (
    cost,
    max_ratio_initial_set,
    ratio,
    sidney_decomposition,
    sidney_order,
)


def feasible(order, prec):
    pos = {j: i for i, j in enumerate(order)}
    return all(pos[i] < pos[j] for i, j in prec)


def is_initial(S, prec):
    return all(i in S for i, j in prec if j in S)


def random_instance(rng, n):
    p = [rng.randint(1, 5) for _ in range(n)]
    w = [rng.randint(0, 6) for _ in range(n)]
    label = list(range(n))
    rng.shuffle(label)
    prec = [(label[i], label[j]) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.35]
    return p, w, prec


def respects(order, pieces):
    idx = {j: k for k, S in enumerate(pieces) for j in S}
    ks = [idx[j] for j in order]
    return ks == sorted(ks)


def test_page_example() -> None:
    p, w, prec = [3, 1, 2, 1, 2], [1, 6, 4, 1, 3], [(0, 1), (3, 4)]
    assert sidney_decomposition(p, w, prec) == [[2], [0, 1], [3, 4]]
    order = sidney_order(p, w, prec)
    assert order == [2, 0, 1, 3, 4] and cost(p, w, order) == 83
    opt = min(cost(p, w, o) for o in itertools.permutations(range(5)) if feasible(o, prec))
    assert opt == 83


def test_gap_example() -> None:
    p, w, prec = [3, 1, 2, 4], [0, 3, 0, 3], [(0, 1), (0, 3), (1, 2)]
    assert cost(p, w, [0, 1, 3, 2]) == 36 and cost(p, w, [0, 3, 1, 2]) == 45
    assert ratio(p, w, [0, 1]) == ratio(p, w, [0, 1, 3]) == Fraction(3, 4)


def test_pieces_are_max_ratio_initial_sets() -> None:
    rng = random.Random(61)
    for _ in range(150):
        n = rng.randint(1, 7)
        p, w, prec = random_instance(rng, n)
        pieces = sidney_decomposition(p, w, prec)
        assert sorted(j for S in pieces for j in S) == list(range(n))
        rest = set(range(n))
        last = None
        for S in pieces:
            best = max(
                ratio(p, w, T)
                for k in range(1, len(rest) + 1)
                for T in itertools.combinations(sorted(rest), k)
                if is_initial(set(T), [(i, j) for i, j in prec if i in rest and j in rest])
            )
            assert is_initial(set(S), [(i, j) for i, j in prec if i in rest and j in rest])
            assert ratio(p, w, S) == best
            assert last is None or best <= last
            last = best
            rest -= set(S)


def test_some_optimal_order_respects_the_pieces_and_every_such_order_is_within_2() -> None:
    rng = random.Random(62)
    for _ in range(120):
        n = rng.randint(1, 6)
        p, w, prec = random_instance(rng, n)
        pieces = sidney_decomposition(p, w, prec)
        orders = [o for o in itertools.permutations(range(n)) if feasible(o, prec)]
        opt = min(cost(p, w, o) for o in orders)
        inside = [cost(p, w, o) for o in orders if respects(o, pieces)]
        assert min(inside) == opt
        assert max(inside) <= 2 * opt
        order = sidney_order(p, w, prec)
        assert feasible(order, prec) and respects(order, pieces)


def test_without_precedence_it_is_smiths_rule() -> None:
    rng = random.Random(63)
    for _ in range(100):
        n = rng.randint(1, 7)
        p = [rng.randint(1, 5) for _ in range(n)]
        w = [rng.randint(0, 6) for _ in range(n)]
        opt = min(cost(p, w, o) for o in itertools.permutations(range(n)))
        assert cost(p, w, sidney_order(p, w, [])) == opt


def test_max_ratio_set_on_a_chain() -> None:
    # a chain 0 -> 1 -> 2: the initial sets are the prefixes {0}, {0,1}, {0,1,2}
    p, w, prec = [2, 1, 1], [1, 5, 0], [(0, 1), (1, 2)]
    assert max_ratio_initial_set(p, w, prec, [0, 1, 2]) == {0, 1}


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        sidney_decomposition([0, 1], [1, 1], [])
    with pytest.raises(ValueError):
        sidney_order([1, 1], [1, 1], [(0, 1), (1, 0)])
