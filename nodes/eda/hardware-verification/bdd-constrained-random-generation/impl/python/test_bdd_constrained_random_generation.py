# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bdd-constrained-random-generation/. The authors are listed in prov/0PZ387.jsonl.

import itertools
import random
from collections import Counter
from fractions import Fraction

import pytest

from bdd import BDD
from bdd_constrained_random_generation import (
    example, model_count, path_counts, path_weights, probability_of,
    rejection_sample, sample, weighted_probability_of, weighted_sample)


# constraints as expression trees, evaluated without any BDD

def random_expr(rng, n, depth):
    if depth == 0 or rng.random() < 0.25:
        return ("var", rng.randrange(n))
    op = rng.choice(("not", "and", "and", "or", "or", "xor"))
    if op == "not":
        return ("not", random_expr(rng, n, depth - 1))
    return (op, random_expr(rng, n, depth - 1), random_expr(rng, n, depth - 1))


def eval_expr(e, x):
    op = e[0]
    if op == "var":
        return x[e[1]]
    if op == "not":
        return 1 - eval_expr(e[1], x)
    a, b = eval_expr(e[1], x), eval_expr(e[2], x)
    if op == "and":
        return a & b
    if op == "or":
        return a | b
    return a ^ b


def build(bdd, e):
    op = e[0]
    if op == "var":
        return bdd.var(e[1])
    if op == "not":
        return bdd.NOT(build(bdd, e[1]))
    f = {"and": bdd.AND, "or": bdd.OR, "xor": bdd.XOR}[op]
    return f(build(bdd, e[1]), build(bdd, e[2]))


def assignments(n):
    for bits in itertools.product((0, 1), repeat=n):
        yield list(bits)


def brute_models(n, e):
    return [tuple(x) for x in assignments(n) if eval_expr(e, x)]


def random_constraint(rng, n):
    e = random_expr(rng, n, rng.randint(1, 4))
    b = BDD(n)
    return e, b, build(b, e)


# the exact law of a sampler, by enumerating every outcome of every randrange call

class _Need(Exception):
    pass


class _ScriptRng:
    def __init__(self, script):
        self.script = script
        self.pos = 0
        self.ranges = []

    def randrange(self, m):
        if self.pos == len(self.script):
            raise _Need(m)
        r = self.script[self.pos]
        self.pos += 1
        self.ranges.append(m)
        return r


def exact_law(run):
    law = Counter()
    stack = [[]]
    while stack:
        script = stack.pop()
        rng = _ScriptRng(script)
        try:
            out = run(rng)
        except _Need as need:
            for r in range(need.args[0]):
                stack.append(script + [r])
            continue
        prob = Fraction(1)
        for m in rng.ranges:
            prob /= m
        law[None if out is None else tuple(out)] += prob
    return law


# tests

def test_example_of_the_page():
    b, root = example()
    N = path_counts(b, root)
    assert model_count(b, root, N) == 10
    assert N[root] == 10 and b.level(root) == 0
    models = [tuple(x) for x in assignments(4) if (x[0] and x[1]) or x[3]]
    law = exact_law(lambda rng: sample(b, root, rng, N))
    assert set(law) == set(models)
    assert all(law[m] == Fraction(1, 10) for m in models)
    p = [Fraction(1, 2)] * 3 + [Fraction(1, 4)]
    assert path_weights(b, root, p)[root] == Fraction(7, 16)
    wlaw = exact_law(lambda rng: weighted_sample(b, root, p, rng))
    for m in models:
        assert wlaw[m] == (Fraction(1, 14) if m[3] else Fraction(3, 14))


def test_sampler_law_is_uniform_by_enumeration():
    """The sampler itself, run on every outcome of its random draws, against the models of the expression."""
    rng = random.Random(5)
    for trial in range(150):
        n = rng.randint(1, 5)
        e, b, root = random_constraint(rng, n)
        models = brute_models(n, e)
        law = exact_law(lambda r: sample(b, root, r))
        if not models:
            assert law == {None: 1}
            continue
        assert set(law) == set(models)
        assert all(q == Fraction(1, len(models)) for q in law.values())


def test_count_and_probability_of_against_enumeration():
    rng = random.Random(17)
    for trial in range(120):
        n = rng.randint(1, 9)
        e, b, root = random_constraint(rng, n)
        models = set(brute_models(n, e))
        N = path_counts(b, root)
        assert model_count(b, root, N) == len(models)
        total = Fraction(0)
        for x in assignments(n):
            q = probability_of(b, root, x, N)
            assert q == (Fraction(1, len(models)) if tuple(x) in models else 0)
            total += q
        assert total == (1 if models else 0)


def test_weighted_law_is_the_conditioned_product_law():
    rng = random.Random(23)
    for trial in range(80):
        n = rng.randint(1, 4)
        e, b, root = random_constraint(rng, n)
        p = [Fraction(rng.randint(1, 3), 4) for _ in range(n)]
        w = {}
        for x in assignments(n):
            if eval_expr(e, x):
                wx = Fraction(1)
                for i in range(n):
                    wx *= p[i] if x[i] else 1 - p[i]
                w[tuple(x)] = wx
        Z = sum(w.values())
        law = exact_law(lambda r: weighted_sample(b, root, p, r))
        if not w:
            assert law == {None: 1}
            continue
        assert dict(law) == {s: ws / Z for s, ws in w.items()}
        for s, ws in w.items():
            assert weighted_probability_of(b, root, p, list(s)) == ws / Z


def test_chi_square_and_total_variation_on_a_sample():
    """Measured, not proved: a fixed-seed sample of a 7-variable constraint."""
    b = BDD(7)
    v = b.var
    # (x0 xor x2) and (x1 or x4) and not (x3 and x5 and x6)
    root = b.AND(b.AND(b.XOR(v(0), v(2)), b.OR(v(1), v(4))),
                 b.NOT(b.AND(b.AND(v(3), v(5)), v(6))))
    N = path_counts(b, root)
    m = model_count(b, root, N)
    assert m == 2 * 3 * 7  # x0,x2: 2 of 4; x1,x4: 3 of 4; x3,x5,x6: 7 of 8
    rng = random.Random(2026)
    draws = 21000
    hits = Counter(tuple(sample(b, root, rng, N)) for _ in range(draws))
    assert len(hits) == m
    expected = draws / m
    chi2 = sum((hits[s] - expected) ** 2 / expected for s in hits)
    # 41 degrees of freedom; the 0.999 quantile of chi-square(41) is about 74.7
    assert chi2 < 74.7
    tv = sum(abs(hits[s] / draws - 1 / m) for s in hits) / 2
    assert tv < 0.05


def naive_walk(b, root, rng):
    """The wrong sampler of the pitfall: a fair coin at every node with two live children."""
    x = [rng.randrange(2) for _ in range(b.n)]
    u = root
    while u > 1:
        lo, hi = b.low(u), b.high(u)
        if lo == 0:
            bit = 1
        elif hi == 0:
            bit = 0
        else:
            bit = rng.randrange(2)
        x[b.level(u)] = bit
        u = hi if bit else lo
    return x


def test_naive_walk_is_not_uniform():
    b, root = example()
    law = exact_law(lambda rng: naive_walk(b, root, rng))
    assert law[(0, 0, 0, 1)] == Fraction(1, 8)
    assert law[(1, 1, 0, 0)] == Fraction(1, 16)
    assert law[(1, 0, 0, 1)] == Fraction(1, 8)
    assert sum(law.values()) == 1


def test_rejection_tries_match_two_to_the_n_over_models():
    b, root = example()
    constraint = lambda x: b.evaluate(root, x) == 1
    rng = random.Random(31)
    runs = 4000
    total = 0
    hits = Counter()
    for _ in range(runs):
        x, tries = rejection_sample(4, constraint, rng)
        total += tries
        hits[tuple(x)] += 1
    mean = total / runs
    # geometric with p = 10/16: mean 1.6, standard deviation of the mean about 0.0158
    assert abs(mean - 16 / 10) < 0.07
    assert len(hits) == 10
    tv = sum(abs(c / runs - 1 / 10) for c in hits.values()) / 2
    assert tv < 0.05


def test_rejection_on_sparse_constraint():
    b = BDD(8)
    root = b.AND(b.AND(b.var(0), b.var(1)), b.AND(b.var(2), b.XOR(b.var(3), b.var(4))))
    constraint = lambda x: b.evaluate(root, x) == 1
    assert model_count(b, root) == 16  # 2^8 / 16 = 16 tries on average
    rng = random.Random(8)
    runs = 3000
    mean = sum(rejection_sample(8, constraint, rng)[1] for _ in range(runs)) / runs
    # standard deviation of the mean: sqrt(240) / sqrt(3000), about 0.28
    assert abs(mean - 16) < 1.2


def test_unsatisfiable_and_errors():
    b = BDD(3)
    root = b.AND(b.var(0), b.NOT(b.var(0)))
    assert root == 0
    assert sample(b, root, random.Random(0)) is None
    assert model_count(b, root) == 0
    assert weighted_sample(b, root, [Fraction(1, 2)] * 3, random.Random(0)) is None
    assert rejection_sample(3, lambda x: False, random.Random(0), max_tries=5) == (None, 5)
    assert sample(b, 1, random.Random(0)) is not None and model_count(b, 1) == 8
    with pytest.raises(ValueError):
        weighted_sample(b, 1, [Fraction(0)] * 3, random.Random(0))
    with pytest.raises(ValueError):
        b.mk(3, 0, 1)


def test_bdd_helper_is_canonical():
    rng = random.Random(41)
    for trial in range(60):
        n = rng.randint(1, 5)
        e1 = random_expr(rng, n, 3)
        e2 = random_expr(rng, n, 3)
        b = BDD(n)
        f, g = build(b, e1), build(b, e2)
        same = all(eval_expr(e1, x) == eval_expr(e2, x) for x in assignments(n))
        assert (f == g) == same
        for x in assignments(n):
            assert b.evaluate(f, x) == eval_expr(e1, x)
