# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/structural-causal-model/. The authors are listed in prov/ZC6AXX.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from structural_causal_model import SCM, Equation, prob

F = Fraction
Z, X, Y = 0, 1, 2
G = {(0, 0): 6, (1, 0): 8, (0, 1): 1, (1, 1): 4}  # recovery thresholds out of 10


def treatment_model():
    """Severity Z, treatment X, recovery Y; the example of the page."""
    return SCM(
        prior=[[F(1, 2)] * 2, [F(1, 4)] * 4, [F(1, 10)] * 10],
        eqs=[
            Equation([], [0], lambda pa, u: u[0]),
            Equation([Z], [1], lambda pa, u: int(u[0] < 1 + 2 * pa[0])),
            Equation([X, Z], [2], lambda pa, u: int(u[0] < G[pa[0], pa[1]])),
        ])


def test_rung_one_and_two_differ_under_confounding():
    m = treatment_model()
    obs = m.distribution()
    assert prob(obs, {Y: 1}, {X: 1}) == F(1, 2)
    assert prob(obs, {Y: 1}, {X: 0}) == F(19, 40)
    assert prob(m.distribution({X: 1}), {Y: 1}) == F(3, 5)
    assert prob(m.distribution({X: 0}), {Y: 1}) == F(7, 20)
    # conditioning and intervening differ, but adjusting for the confounder Z recovers do
    for x in (0, 1):
        adj = sum(prob(obs, {Y: 1}, {X: x, Z: z}) * prob(obs, {Z: z}) for z in (0, 1))
        assert adj == prob(m.distribution({X: x}), {Y: 1})
        assert adj != prob(obs, {Y: 1}, {X: x})


def test_rung_three_counterfactual():
    m = treatment_model()
    # among treated patients who recovered, the share who would not have recovered untreated
    cf = m.counterfactual({X: 1, Y: 1}, {X: 0})
    assert prob(cf, {Y: 0}) == F(11, 20)
    # with monotone thresholds, a treated patient who did not recover would not have recovered untreated
    assert prob(m.counterfactual({X: 1, Y: 0}, {X: 0}), {Y: 1}) == 0
    # the posterior of the severity
    assert prob(cf, {Z: 1}) == F(3, 5)


def test_consistency_and_do_on_a_root():
    m = treatment_model()
    for x, y in itertools.product((0, 1), repeat=2):
        assert prob(m.counterfactual({X: x, Y: y}, {X: x}), {Y: y}) == 1
    # intervening on a root with its own noise is the same as conditioning on it
    obs = m.distribution()
    for z in (0, 1):
        assert prob(m.distribution({Z: z}), {Y: 1}) == prob(obs, {Y: 1}, {Z: z})


def test_rung_two_does_not_fix_rung_three():
    # Y = U and Y = X xor U agree on every observational and interventional distribution
    half = [F(1, 2)] * 2
    a = SCM([half, half], [Equation([], [0], lambda p, u: u[0]), Equation([0], [1], lambda p, u: u[0])])
    b = SCM([half, half], [Equation([], [0], lambda p, u: u[0]), Equation([0], [1], lambda p, u: p[0] ^ u[0])])
    assert a.distribution() == b.distribution()
    for x in (0, 1):
        assert a.distribution({0: x}) == b.distribution({0: x})
    assert prob(a.counterfactual({0: 1, 1: 1}, {0: 0}), {1: 1}) == 1
    assert prob(b.counterfactual({0: 1, 1: 1}, {0: 0}), {1: 1}) == 0


def random_markovian(n, rng, d=3):
    eqs = []
    for v in range(n):
        pa = sorted(rng.sample(range(v), rng.randint(0, min(v, 2))))
        table = {k: rng.randrange(2) for k in itertools.product((0, 1), repeat=len(pa) + 1)}
        # noise value u in 0 .. d - 1; the table maps (parents, u mod 2) to a value, flipped when u = d - 1
        eqs.append(Equation(pa, [v], lambda p, u, t=table, d=d: t[p + (u[0] % 2,)] ^ int(u[0] == d - 1)))
    prior = [[F(rng.randint(1, 5)) for _ in range(d)] for _ in range(n)]
    prior = [[w / sum(p) for w in p] for p in prior]
    return SCM(prior, eqs)


def test_markovian_model_factorizes_over_its_graph():
    rng = random.Random(2009)
    for _ in range(40):
        n = rng.randint(2, 5)
        m = random_markovian(n, rng)
        pj = m.distribution()
        directed, bidirected = m.graph()
        assert not bidirected
        pa = [sorted(a for a, b in directed if b == v) for v in range(n)]
        for x in itertools.product((0, 1), repeat=n):
            prod = F(1)
            for v in range(n):
                cond = {u: x[u] for u in pa[v]}
                if prob(pj, cond) == 0 if cond else False:
                    prod = F(0)
                    break
                prod *= prob(pj, {v: x[v]}, cond) if not cond or prob(pj, cond) else 0
            assert prod == pj.get(x, 0)


def test_truncated_factorization():
    # P(v | do(x)) is the product of the other conditionals, with x fixed
    rng = random.Random(4)
    m = random_markovian(4, rng)
    pj = m.distribution()
    directed, _ = m.graph()
    pa = [sorted(a for a, b in directed if b == v) for v in range(4)]
    for t, val in itertools.product(range(4), (0, 1)):
        post = m.distribution({t: val})
        for x in itertools.product((0, 1), repeat=4):
            if x[t] != val:
                assert post.get(x, 0) == 0
                continue
            p = F(1)
            for v in range(4):
                if v != t:
                    cond = {u: x[u] for u in pa[v]}
                    p *= prob(pj, {v: x[v]}, cond)
            assert post.get(x, 0) == p


def test_shared_noise_gives_a_bidirected_edge_and_evidence_must_be_possible():
    m = SCM([[F(1, 2)] * 2], [Equation([], [0], lambda p, u: u[0]), Equation([0], [0], lambda p, u: p[0] ^ u[0])])
    assert m.graph()[1] == {frozenset((0, 1))}
    with pytest.raises(ValueError):
        m.counterfactual({1: 1}, {0: 0})
    with pytest.raises(ValueError):
        SCM([[F(1)]], [Equation([0], [0], lambda p, u: 0)])
