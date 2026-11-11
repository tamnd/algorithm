# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/context-tree-weighting/. The authors are listed in prov/4VCC2M.jsonl.

import math
import random
from fractions import Fraction

import pytest

from context_tree_weighting import (CTW, block_probability, best_tree_cost, decode, encode, ideal_length,
                                    kt_exact, kt_log2, redundancy_bound, source_length, tree_source_sample)


def test_page_example() -> None:
    bits = [0, 1, 1, 0, 1, 0, 0]
    model = CTW(1)
    probs = []
    for x in bits:
        p1 = model.prob_one()
        probs.append(p1 if x else 1 - p1)
        model.update(x)
    assert probs == pytest.approx([1 / 2, 1 / 4, 1 / 2, 5 / 16, 1 / 2, 9 / 20, 4 / 9])
    assert block_probability(bits, 1) == Fraction(1, 512)
    assert kt_exact(4, 3) == Fraction(5, 2048)
    assert kt_exact(2, 2) == Fraction(3, 128)
    assert kt_exact(2, 1) == Fraction(1, 16)
    assert model.log_pw() == pytest.approx(-9.0)


def test_sequential_equals_exact() -> None:
    rng = random.Random(1995)
    for _ in range(40):
        depth = rng.randint(0, 4)
        n = rng.randint(0, 40)
        bits = [rng.randint(0, 1) for _ in range(n)]
        exact = block_probability(bits, depth)
        assert ideal_length(bits, depth) == pytest.approx(-math.log2(exact), abs=1e-9)
        model = CTW(depth)
        for x in bits:
            assert 0 < model.prob_one() < 1
            model.update(x)
    for a in range(6):
        for b in range(6):
            assert kt_log2(a, b) == pytest.approx(math.log2(kt_exact(a, b)))


def test_kt_bound() -> None:
    # log2 P_e(a, b) >= log2 of the ML probability - 1/2 lg(a + b) - 1.
    for a in range(0, 150):
        for b in range(0, 150 - a):
            n = a + b
            if n == 0:
                continue
            ml = (a * math.log2(a / n) if a else 0.0) + (b * math.log2(b / n) if b else 0.0)
            assert kt_log2(a, b) >= ml - 0.5 * math.log2(n) - 1 - 1e-9


def test_roundtrip() -> None:
    rng = random.Random(7)
    for _ in range(30):
        depth = rng.randint(0, 5)
        n = rng.randint(0, 300)
        bias = rng.random()
        bits = [1 if rng.random() < bias else 0 for _ in range(n)]
        assert decode(encode(bits, depth), n, depth) == bits
    with pytest.raises(ValueError):
        encode([2], 1)


LEAVES = {(1,): 0.1, (0, 0): 0.8, (0, 1): 0.4}


@pytest.mark.parametrize("depth", [2, 3, 5])
def test_redundancy_bound_on_tree_source(depth: int) -> None:
    n = 3000
    bits = tree_source_sample(LEAVES, n, seed=1995)
    ideal = ideal_length(bits, depth)
    bound = redundancy_bound(LEAVES, depth, n)
    # The bound holds against the true parameters and against the best (ML) parameters for S.
    assert ideal - source_length(bits, LEAVES) <= bound
    assert ideal - source_length(bits, LEAVES, ml=True) <= bound
    # CTW is never worse than the best pruned tree with its description cost.
    assert ideal <= best_tree_cost(bits, depth) + 1e-6
    code = encode(bits, depth)
    assert decode(code, n, depth) == bits
    assert ideal <= 8 * len(code) <= ideal + 2 + 8 + 0.001 * n


def test_deeper_tree_costs_little() -> None:
    n = 3000
    bits = tree_source_sample(LEAVES, n, seed=11)
    shallow = ideal_length(bits, 2)
    deep = ideal_length(bits, 8)
    assert shallow <= deep <= shallow + 8
    # A depth too small for the source loses a lot.
    assert ideal_length(bits, 1) > shallow + 50
