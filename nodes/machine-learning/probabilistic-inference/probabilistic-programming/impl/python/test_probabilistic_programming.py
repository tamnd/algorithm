# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/probabilistic-programming/. The authors are listed in prov/KGYEAS.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from probabilistic_programming import (acceptance, enumerate_posterior, enumerate_traces,
                                       evidence_estimate, flip, flips_until_heads,
                                       likelihood_weighting, lmh, lmh_kernel_exact, run,
                                       sprinkler, trick_coin, uniform_draw, weighted_posterior)

MODELS = [trick_coin, flips_until_heads, sprinkler]


def chain_model(ctx):
    """A random Bayesian network as a program: three binary variables in a chain, with the
    last one observed, and a choice whose existence depends on the first."""
    a = ctx.sample("a", flip(Fraction(2, 7)))
    b = ctx.sample("b", flip(Fraction(3, 5) if a else Fraction(1, 4)))
    if a:
        extra = ctx.sample("extra", uniform_draw([0, 1, 2]))
    else:
        extra = 0
    ctx.observe(flip(Fraction(5, 6) if b else Fraction(1, 9)), True)
    ctx.observe(uniform_draw([0, 1, 2]) if a else flip(Fraction(1, 2)), extra if a else True)
    return (a, b)


def stationary(model):
    traces = [t for t in enumerate_traces(model) if t.joint() > 0]
    z = sum(t.joint() for t in traces)
    return {t.key(): t.joint() / z for t in traces}, traces


def test_enumeration_on_the_page_models():
    post, z = enumerate_posterior(trick_coin)
    assert post[True] == Fraction(84, 209) and z == Fraction(1881, 10000)
    post, z = enumerate_posterior(flips_until_heads)
    assert post == {2: Fraction(1, 3), 3: Fraction(2, 9), 4: Fraction(4, 9)} and z == Fraction(2, 3)
    post, z = enumerate_posterior(sprinkler)
    assert post[True] == Fraction(202, 207) and z == Fraction(1863, 5000)


def test_enumeration_visits_each_trace_once():
    keys = [t.key() for t in enumerate_traces(flips_until_heads)]
    assert len(keys) == len(set(keys)) == 5
    assert sum(t.prior() for t in enumerate_traces(flips_until_heads)) == 1


def test_enumeration_matches_a_direct_sum():
    direct = {}
    for a, b, extra in itertools.product([True, False], [True, False], [0, 1, 2]):
        if not a and extra:
            continue
        p = (Fraction(2, 7) if a else Fraction(5, 7))
        pb = Fraction(3, 5) if a else Fraction(1, 4)
        p *= pb if b else 1 - pb
        p *= Fraction(1, 3) * Fraction(1, 3) if a else Fraction(1, 2)
        p *= Fraction(5, 6) if b else Fraction(1, 9)
        direct[(a, b)] = direct.get((a, b), 0) + p
    z = sum(direct.values())
    post, z2 = enumerate_posterior(chain_model)
    assert z2 == z and post == {k: v / z for k, v in direct.items()}


def test_zero_evidence_is_reported():
    def impossible(ctx):
        ctx.condition(ctx.sample("x", flip(Fraction(1, 2))) and False)
    with pytest.raises(ValueError):
        enumerate_posterior(impossible)


def test_repeated_address_is_an_error():
    def bad(ctx):
        ctx.sample("x", flip(Fraction(1, 2)))
        ctx.sample("x", flip(Fraction(1, 2)))
    with pytest.raises(ValueError):
        run(bad, lambda a, d: True)


@pytest.mark.parametrize("model", MODELS + [chain_model])
def test_lmh_kernel_is_exactly_reversible(model):
    pi, traces = stationary(model)
    kernel = {t.key(): lmh_kernel_exact(model, t)[0] for t in traces}
    for x in pi:
        assert sum(kernel[x].values()) == 1
        assert {y for y, p in kernel[x].items() if p} <= set(pi)
    for x in pi:
        for y in pi:
            assert pi[x] * kernel[x].get(y, 0) == pi[y] * kernel[y].get(x, 0)
    for y in pi:
        assert sum(pi[x] * kernel[x].get(y, 0) for x in pi) == pi[y]


def test_dropping_the_trace_correction_breaks_invariance():
    def naive(old, new, site):
        return min(1, new.joint() / old.joint())
    pi, traces = stationary(trick_coin)
    kernel = {t.key(): lmh_kernel_exact(trick_coin, t, naive)[0] for t in traces}
    assert any(sum(pi[x] * kernel[x].get(y, 0) for x in pi) != pi[y] for y in pi)


def test_page_example_of_one_move():
    start = next(t for t in enumerate_traces(trick_coin) if t.key() == (("trick", False),))
    kernel, traces = lmh_kernel_exact(trick_coin, start)
    for key, p in kernel.items():
        assert p == (Fraction(9, 10) if key == start.key() else Fraction(1, 20))
    to_four_fifths = traces[(("trick", True), ("bias", Fraction(4, 5)))]
    assert acceptance(start, to_four_fifths, "trick") == 1
    assert acceptance(to_four_fifths, start, "trick") == Fraction(125, 256)
    samples = likelihood_weighting(trick_coin, 10000, random.Random(1))
    assert abs(float(weighted_posterior(samples)[True]) - 0.4046) < 1e-4
    assert abs(float(evidence_estimate(samples)) - 0.1885) < 1e-4
    values = lmh(trick_coin, 10000, random.Random(1), burn=1000)
    assert abs(sum(values) / len(values) - 0.3888) < 1e-4


@pytest.mark.parametrize("model", MODELS + [chain_model])
def test_likelihood_weighting_agrees_with_enumeration(model):
    post, z = enumerate_posterior(model)
    samples = likelihood_weighting(model, 20000, random.Random(5))
    est = weighted_posterior(samples)
    for v, p in post.items():
        assert abs(float(est.get(v, 0)) - float(p)) < 0.02
    assert abs(float(evidence_estimate(samples)) - float(z)) / float(z) < 0.05


@pytest.mark.parametrize("model", MODELS + [chain_model])
def test_lmh_agrees_with_enumeration(model):
    post, _ = enumerate_posterior(model)
    values = lmh(model, 30000, random.Random(6), burn=1000)
    for v, p in post.items():
        assert abs(values.count(v) / len(values) - float(p)) < 0.03
