# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transition-density/. The authors are listed in prov/G6GC4V.jsonl.

import itertools
import random
from fractions import Fraction

from netlist import KINDS, Circuit, random_circuit, transitions
from transition_density import boolean_difference_probability, gate_probability, transition_densities

HALF = Fraction(1, 2)

# y = ab + ac, the reconvergent example of the page.
RECONV = Circuit(["a", "b", "c"], [("u", "AND", ["a", "b"]), ("v", "AND", ["a", "c"]), ("y", "OR", ["u", "v"])])


def weight(c, p, x):
    w = Fraction(1)
    for name, b in zip(c.inputs, x):
        w *= p[name] if b else 1 - p[name]
    return w


def flip(x, i):
    y = list(x)
    y[i] = 1 - y[i]
    return tuple(y)


def global_densities(c, p, d):
    """D(y) = sum_i P(dy/dx_i) D(x_i) with the Boolean differences of whole node functions, by enumeration."""
    out = {v: Fraction(0) for v in c.nodes}
    for x in itertools.product((0, 1), repeat=len(c.inputs)):
        w = weight(c, p, x)
        if w == 0:
            continue
        a = c.evaluate(x)
        for i, name in enumerate(c.inputs):
            b = c.evaluate(flip(x, i))
            for v in c.nodes:
                if a[v] != b[v]:
                    out[v] += w * d[name]
    return out


class Chain:
    """Inputs as one Markov chain: each step picks input i with probability w[i]
    and flips it with probability up[i] if it is 0 and down[i] if it is 1."""

    def __init__(self, rng, n):
        self.w = [Fraction(1, n + 1)] * n
        self.up = [Fraction(rng.randint(1, 6), 6) for _ in range(n)]
        self.down = [Fraction(rng.randint(1, 6), 6) for _ in range(n)]

    def marginal(self, i):
        return self.up[i] / (self.up[i] + self.down[i])

    def rate(self, i):
        return self.w[i] * 2 * self.up[i] * self.down[i] / (self.up[i] + self.down[i])

    def flip_prob(self, i, bit):
        return self.w[i] * (self.down[i] if bit else self.up[i])


def markov_toggles(c, ch):
    """Expected node transitions per step of the chain, from the product distribution, by enumeration."""
    p = {name: ch.marginal(i) for i, name in enumerate(c.inputs)}
    out = {v: Fraction(0) for v in c.nodes}
    for x in itertools.product((0, 1), repeat=len(c.inputs)):
        w = weight(c, p, x)
        a = c.evaluate(x)
        for i in range(len(c.inputs)):
            b = c.evaluate(flip(x, i))
            t = w * ch.flip_prob(i, x[i])
            for v in c.nodes:
                if a[v] != b[v]:
                    out[v] += t
    return out


def chain_inputs(c, ch):
    p = {name: ch.marginal(i) for i, name in enumerate(c.inputs)}
    d = {name: ch.rate(i) for i, name in enumerate(c.inputs)}
    return p, d


def test_gate_rules_against_truth_tables():
    rng = random.Random(1)
    for kind in KINDS:
        for k in ([1] if kind in ("BUF", "NOT") else [2, 3, 4]):
            c = Circuit([f"i{j}" for j in range(k)], [("o", kind, [f"i{j}" for j in range(k)])])
            for _ in range(5):
                p = {x: Fraction(rng.randint(0, 6), 6) for x in c.inputs}
                d = {x: Fraction(rng.randint(0, 9), 3) for x in c.inputs}
                q = [p[x] for x in c.inputs]
                for j in range(k):
                    one = {x: Fraction(int(x == c.inputs[j])) for x in c.inputs}
                    assert boolean_difference_probability(kind, q, j) == global_densities(c, p, one)["o"]
                P, D = transition_densities(c, p, d)
                assert D["o"] == global_densities(c, p, d)["o"]
                assert P["o"] == gate_probability(kind, q)


def test_product_distribution_is_stationary():
    rng = random.Random(2)
    for n in range(1, 5):
        ch = Chain(rng, n)
        names = [f"x{i}" for i in range(n)]
        c = Circuit(names, [])
        p = {name: ch.marginal(i) for i, name in enumerate(names)}
        states = list(itertools.product((0, 1), repeat=n))
        pi = {x: weight(c, p, x) for x in states}
        nxt = {x: Fraction(0) for x in states}
        for x in states:
            stay = Fraction(1)
            for i in range(n):
                t = ch.flip_prob(i, x[i])
                nxt[flip(x, i)] += pi[x] * t
                stay -= t
            nxt[x] += pi[x] * stay
        assert nxt == pi
        # The input rates of the chain are the transition densities D(x_i).
        for i, name in enumerate(names):
            assert markov_toggles(c, ch)[name] == ch.rate(i)


def test_page_fanout_free_example():
    c = Circuit(["a", "b", "c"], [("u", "AND", ["a", "b"]), ("y", "OR", ["u", "c"])])
    p = {"a": HALF, "b": Fraction(1, 4), "c": HALF}
    d = {"a": Fraction(2), "b": Fraction(1), "c": Fraction(4)}
    P, D = transition_densities(c, p, d)
    assert (P["u"], D["u"]) == (Fraction(1, 8), 1)
    assert (P["y"], D["y"]) == (Fraction(9, 16), 4)
    assert D == global_densities(c, p, d)


def test_page_reconvergent_example():
    p = {"a": HALF, "b": HALF, "c": HALF}
    d = {"a": Fraction(1), "b": Fraction(1), "c": Fraction(1)}
    P, D = transition_densities(RECONV, p, d)
    assert D["u"] == D["v"] == 1
    assert D["y"] == Fraction(3, 2)
    assert P["y"] == Fraction(7, 16)
    assert global_densities(RECONV, p, d)["y"] == Fraction(5, 4)


def test_exact_without_reconvergence_against_markov_chain():
    rng = random.Random(3)
    count = 0
    for _ in range(250):
        c = random_circuit(rng, rng.randint(1, 6), rng.randint(1, 8), fanout_free=rng.random() < 0.5)
        if c.has_reconvergence():
            continue
        count += 1
        ch = Chain(rng, len(c.inputs))
        p, d = chain_inputs(c, ch)
        _, D = transition_densities(c, p, d)
        assert D == markov_toggles(c, ch)
    assert count > 80


def test_global_formula_matches_markov_chain_on_every_circuit():
    rng = random.Random(4)
    for _ in range(100):
        c = random_circuit(rng, rng.randint(1, 5), rng.randint(1, 8))
        ch = Chain(rng, len(c.inputs))
        p, d = chain_inputs(c, ch)
        assert global_densities(c, p, d) == markov_toggles(c, ch)


def test_propagation_is_wrong_under_reconvergence():
    rng = random.Random(5)
    wrong = 0
    for _ in range(300):
        c = random_circuit(rng, rng.randint(2, 5), rng.randint(3, 8))
        if not c.has_reconvergence():
            continue
        ch = Chain(rng, len(c.inputs))
        p, d = chain_inputs(c, ch)
        if transition_densities(c, p, d)[1] != markov_toggles(c, ch):
            wrong += 1
    assert wrong > 50


def per_cycle(c, delay_model):
    """Expected transitions per cycle for fresh uniform vectors each cycle, over all pairs."""
    n = len(c.inputs)
    tot = {v: Fraction(0) for v in c.nodes}
    for x in itertools.product((0, 1), repeat=n):
        for y in itertools.product((0, 1), repeat=n):
            for v, k in transitions(c, x, y, delay_model).items():
                tot[v] += Fraction(k, 4**n)
    return tot


def test_simultaneous_switching():
    # Fresh uniform vectors every cycle: P = 1/2 and D = 1/2 per cycle for each input.
    same_time = Circuit(["a", "b"], [("y", "AND", ["a", "b"])])
    skewed = Circuit(["a", "b"], [("bd", "BUF", ["b"]), ("y", "AND", ["a", "bd"])])
    p = {"a": HALF, "b": HALF}
    _, D = transition_densities(same_time, p, p)
    assert D["y"] == HALF
    assert per_cycle(same_time, "zero")["y"] == Fraction(3, 8)
    assert per_cycle(skewed, "transport")["y"] == HALF


def test_glitch_of_a_and_not_a():
    c = Circuit(["a"], [("n", "NOT", ["a"]), ("y", "AND", ["a", "n"])])
    _, D = transition_densities(c, {"a": HALF}, {"a": HALF})
    assert D["y"] == HALF
    assert per_cycle(c, "zero")["y"] == 0
    assert per_cycle(c, "transport")["y"] == HALF
