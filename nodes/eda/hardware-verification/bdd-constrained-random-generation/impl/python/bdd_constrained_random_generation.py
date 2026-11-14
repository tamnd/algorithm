# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bdd-constrained-random-generation/. The authors are listed in prov/0PZ387.jsonl.

"""Uniform and weighted random solutions of a constraint given as a reduced ordered BDD.

The constraint is a node `root` of a bdd.BDD over the variables 0 .. n-1.
Counts are exact integers and weights exact Fractions, and every random choice
is made with randrange, so the law of a sample is exactly the stated one.
"""

from fractions import Fraction

from bdd import BDD


def path_counts(bdd, root):
    """N[u] = number of assignments of the variables at levels level(u) .. n-1 that satisfy u."""
    N = {0: 0, 1: 1}
    lev = bdd.level
    for u in bdd.nodes(root):
        if u > 1:
            lo, hi = bdd.low(u), bdd.high(u)
            N[u] = (N[lo] << (lev(lo) - lev(u) - 1)) + (N[hi] << (lev(hi) - lev(u) - 1))
    return N


def model_count(bdd, root, N=None):
    """The number of models of root over all n variables."""
    if N is None:
        N = path_counts(bdd, root)
    return N[root] << bdd.level(root)


def _fill(x, start, stop, rng):
    for i in range(start, stop):
        x[i] = rng.randrange(2)


def sample(bdd, root, rng, N=None):
    """One model of root, each with probability exactly 1/#models; None if there is none."""
    if N is None:
        N = path_counts(bdd, root)  # @line L1
    if N[root] == 0:  # @line L2
        return None
    lev = bdd.level
    x = [0] * bdd.n
    u = root
    _fill(x, 0, lev(u), rng)  # @line L3
    while u > 1:  # @line L4
        lo, hi = bdd.low(u), bdd.high(u)
        c1 = N[hi] << (lev(hi) - lev(u) - 1)  # @line L5
        r = rng.randrange(N[u])  # @line L6
        if r < c1:  # @line L7
            x[lev(u)], nxt = 1, hi
        else:
            x[lev(u)], nxt = 0, lo
        _fill(x, lev(u) + 1, lev(nxt), rng)  # @line L8
        u = nxt  # @line L9
    return x  # @line L10


def probability_of(bdd, root, x, N=None):
    """The exact probability, as a Fraction, that sample returns the assignment x."""
    if N is None:
        N = path_counts(bdd, root)
    if N[root] == 0 or bdd.evaluate(root, x) == 0:
        return Fraction(0)
    lev = bdd.level
    u = root
    p = Fraction(1, 2 ** lev(u))
    while u > 1:
        nxt = bdd.high(u) if x[lev(u)] else bdd.low(u)
        p *= Fraction(N[nxt] << (lev(nxt) - lev(u) - 1), N[u])
        p /= 2 ** (lev(nxt) - lev(u) - 1)
        u = nxt
    return p


# weighted generation: variable i is 1 with bias p[i], conditioned on the constraint

def _bernoulli(q, rng):
    """1 with probability q exactly, for a Fraction q in [0, 1]."""
    return 1 if rng.randrange(q.denominator) < q.numerator else 0


def path_weights(bdd, root, p):
    """W[u] = probability under the biases that the variables at levels level(u) .. n-1 satisfy u."""
    W = {0: Fraction(0), 1: Fraction(1)}
    for u in bdd.nodes(root):
        if u > 1:
            i = bdd.level(u)
            W[u] = (1 - p[i]) * W[bdd.low(u)] + p[i] * W[bdd.high(u)]
    return W


def weighted_sample(bdd, root, p, rng, W=None):
    """A model s of root with probability w(s) / Z, where w(s) = prod p_i^s_i (1 - p_i)^(1 - s_i)."""
    p = [Fraction(q) for q in p]
    if any(not 0 < q < 1 for q in p):
        raise ValueError("each bias must lie strictly between 0 and 1")
    if W is None:
        W = path_weights(bdd, root, p)
    if W[root] == 0:
        return None
    x = [0] * bdd.n
    u = root
    for i in range(bdd.level(u)):
        x[i] = _bernoulli(p[i], rng)
    while u > 1:
        i, lo, hi = bdd.level(u), bdd.low(u), bdd.high(u)
        x[i] = _bernoulli(p[i] * W[hi] / W[u], rng)
        nxt = hi if x[i] else lo
        for k in range(i + 1, bdd.level(nxt)):
            x[k] = _bernoulli(p[k], rng)
        u = nxt
    return x


def weighted_probability_of(bdd, root, p, x, W=None):
    """The exact probability, as a Fraction, that weighted_sample returns x."""
    p = [Fraction(q) for q in p]
    if W is None:
        W = path_weights(bdd, root, p)
    if W[root] == 0 or bdd.evaluate(root, x) == 0:
        return Fraction(0)
    prob = Fraction(1)
    u = root
    for i in range(bdd.level(u)):
        prob *= p[i] if x[i] else 1 - p[i]
    while u > 1:
        i, lo, hi = bdd.level(u), bdd.low(u), bdd.high(u)
        q = p[i] * W[hi] / W[u]
        prob *= q if x[i] else 1 - q
        nxt = hi if x[i] else lo
        for k in range(i + 1, bdd.level(nxt)):
            prob *= p[k] if x[k] else 1 - p[k]
        u = nxt
    return prob


# the baseline

def rejection_sample(n, constraint, rng, max_tries=None):
    """Draw uniform assignments of n bits until constraint(x) holds; return (x, tries)."""
    tries = 0
    while max_tries is None or tries < max_tries:
        tries += 1
        x = [rng.randrange(2) for _ in range(n)]
        if constraint(x):
            return x, tries
    return None, tries


def example():
    """The constraint (x0 and x1) or x3 over four variables, the example of the page."""
    b = BDD(4)
    root = b.OR(b.AND(b.var(0), b.var(1)), b.var(3))
    return b, root


if __name__ == "__main__":
    import random

    b, root = example()
    N = path_counts(b, root)
    print("models:", model_count(b, root, N))
    rng = random.Random(1)
    print("samples:", [sample(b, root, rng, N) for _ in range(5)])
    p = [Fraction(1, 2)] * 3 + [Fraction(1, 4)]
    print("weighted:", [weighted_sample(b, root, p, rng) for _ in range(5)])
