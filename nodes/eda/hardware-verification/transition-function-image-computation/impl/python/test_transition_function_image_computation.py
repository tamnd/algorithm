# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transition-function-image-computation/. The authors are listed in prov/H8PR83.jsonl.

import random

import pytest

from bdd import BDD
from transition_function_image_computation import constrain, image, range_of


def from_table(bdd: BDD, table: list[int], vars_: list[int]) -> int:
    """The BDD of the function whose value at index sum(b_j 2^j) is table[index], for b_j the value of vars_[j]."""
    f = 0
    for idx, bit in enumerate(table):
        if bit:
            term = 1
            for j, v in enumerate(vars_):
                lit = bdd.var(v) if (idx >> j) & 1 else bdd.neg(bdd.var(v))
                term = bdd.conj(term, lit)
            f = bdd.disj(f, term)
    return f


def states_of(bdd: BDD, f: int, vars_: list[int]) -> set[int]:
    """Oracle helper: the set of codes sum(b_j 2^j) of the points where f is 1."""
    out = set()
    for code in range(1 << len(vars_)):
        if bdd.evaluate(f, {v: (code >> j) & 1 for j, v in enumerate(vars_)}):
            out.add(code)
    return out


def explicit_image(tables: list[list[int]], n: int, k: int, s: set[int]) -> set[int]:
    """Oracle: apply the next-state tables to every state of s and every input."""
    out = set()
    for st in s:
        for x in range(1 << k):
            idx = st | (x << n)
            out.add(sum(tables[i][idx] << i for i in range(n)))
    return out


def page_example():
    """State bits s1 s2 s3 (variables 0, 1, 2), input x (variable 3), next-state variables 4, 5, 6."""
    bdd = BDD()
    s1, s2, s3, x = (bdd.var(i) for i in range(4))
    delta = [bdd.xor(s1, x), bdd.conj(s1, s2), bdd.disj(x, s2)]
    states = bdd.conj(bdd.xor(s1, s2), bdd.neg(s3))  # {100, 010} as s1 s2 s3
    return bdd, delta, states


def test_page_example():
    bdd, delta, states = page_example()
    s1, x = bdd.var(0), bdd.var(3)
    g = [constrain(bdd, d, states) for d in delta]
    assert g == [bdd.xor(s1, x), 0, bdd.disj(bdd.neg(s1), x)]
    assert [constrain(bdd, h, g[0]) for h in g[1:]] == [0, bdd.neg(s1)]
    assert [constrain(bdd, h, bdd.neg(g[0])) for h in g[1:]] == [0, 1]
    img = image(bdd, delta, states, [4, 5, 6])
    # Codes are s1 + 2 s2 + 4 s3; the image is {100, 001, 101} as s1 s2 s3.
    assert states_of(bdd, img, [4, 5, 6]) == {0b001, 0b100, 0b101}
    assert img == bdd.disj(bdd.conj(bdd.var(4), bdd.neg(bdd.var(5))), bdd.conj(bdd.neg(bdd.var(5)), bdd.var(6)))


def test_empty_and_full_state_sets():
    bdd, delta, _ = page_example()
    assert image(bdd, delta, 0, [4, 5, 6]) == 0
    full = states_of(bdd, image(bdd, delta, 1, [4, 5, 6]), [4, 5, 6])
    tables = [[bdd.evaluate(d, {j: (i >> j) & 1 for j in range(4)}) for i in range(16)] for d in delta]
    assert full == explicit_image(tables, 3, 1, set(range(8)))
    assert len(full) == 6


def test_constant_functions_and_constrain_by_zero():
    bdd = BDD()
    assert range_of(bdd, [], []) == 1
    r = range_of(bdd, [1, 0], [5, 6])
    assert states_of(bdd, r, [5, 6]) == {0b01}
    with pytest.raises(ValueError):
        constrain(bdd, bdd.var(0), 0)


def test_random_against_explicit_image_and_relational_product():
    rng = random.Random(1990)
    for case in range(600):
        n = rng.randint(1, 4)
        k = rng.randint(0, 2)
        order = list(range(2 * n + k))
        rng.shuffle(order)
        svars, xvars, yvars = order[:n], order[n : n + k], order[n + k :]
        bdd = BDD()
        rows = 1 << (n + k)
        tables = [[rng.randrange(2) for _ in range(rows)] for _ in range(n)]
        if case % 5 == 0:
            tables[0] = [tables[-1][r] for r in range(rows)]
        delta = [from_table(bdd, t, svars + xvars) for t in tables]
        s_codes = [c for c in range(1 << n) if rng.random() < 0.4]
        s_table = [1 if c in s_codes else 0 for c in range(1 << n)]
        states = from_table(bdd, s_table, svars)
        img = image(bdd, delta, states, yvars)
        expect = explicit_image(tables, n, k, set(s_codes))
        assert states_of(bdd, img, yvars) == expect
        assert bdd.support(img) <= set(yvars)
        rel = 1
        for d, y in zip(delta, yvars):
            rel = bdd.conj(rel, bdd.xnor(bdd.var(y), d))
        assert img == bdd.exists(bdd.conj(states, rel), frozenset(svars + xvars))
