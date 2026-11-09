# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fredman-khachiyan-algorithm/. The authors are listed in prov/FEAKXY.jsonl.

from collections.abc import Iterable
from fractions import Fraction

Term = frozenset[int]


def _minimize(terms: Iterable[Iterable[int]]) -> list[Term]:
    """Remove repeated terms and terms that contain another term."""
    unique = sorted({frozenset(t) for t in terms}, key=lambda t: (len(t), sorted(t)))
    kept: list[Term] = []
    for t in unique:
        if not any(k <= t for k in kept):
            kept.append(t)
    return kept


def _variables(f: list[Term], g: list[Term]) -> set[int]:
    out: set[int] = set()
    for t in f:
        out |= t
    for t in g:
        out |= t
    return out


def _both_false(f: list[Term], g: list[Term], variables: list[int]) -> Term:
    """Find x with f(x) = 0 and g(not x) = 0 when the expected count is below 1.

    For a uniform random x, a term F of f is true with probability 2^-|F|,
    and a term G of g is true on the complement of x with probability 2^-|G|.
    Fixing the variables one by one, each time to the value that does not
    raise the expected number of true terms, keeps it below 1, so at the end
    it is 0.
    """
    value: dict[int, bool] = {}

    def expected() -> Fraction:
        total = Fraction(0)
        for t in f:
            if all(value.get(v, True) for v in t):
                total += Fraction(1, 2 ** sum(1 for v in t if v not in value))
        for t in g:
            if all(not value.get(v, False) for v in t):
                total += Fraction(1, 2 ** sum(1 for v in t if v not in value))
        return total

    for v in variables:
        value[v] = True
        if_true = expected()
        value[v] = False
        if if_true < expected():
            value[v] = True
    return frozenset(v for v in variables if value[v])


def dual_witness(f: Iterable[Iterable[int]], g: Iterable[Iterable[int]]) -> Term | None:
    """Test whether the monotone DNFs f and g are dual (Fredman and Khachiyan, algorithm A).

    A DNF is a family of terms, each a set of variables. The function is true
    on an assignment x, given as the set of true variables, when some term is
    a subset of x. The DNFs are dual when f(x) != g(complement of x) for every
    x. The result is None when they are dual, and otherwise a witness x with
    f(x) = g(complement of x). The complement is taken over any set of
    variables that contains every variable of f and g.
    """
    return _dual([frozenset(t) for t in f], [frozenset(t) for t in g])


def _dual(f: list[Term], g: list[Term]) -> Term | None:
    f = _minimize(f)  # @line L1
    g = _minimize(g)
    for a in f:  # @line L2
        for b in g:
            if not (a & b):
                return a
    vf = _variables(f, [])
    vg = _variables([], g)
    for a in f:  # @line L3
        for v in sorted(a - vg):
            return a - {v}
    every = vf | vg
    for b in g:  # @line L4
        for v in sorted(b - vf):
            return frozenset(every - (b - {v}))
    weight = sum(Fraction(1, 2 ** len(t)) for t in f) + sum(Fraction(1, 2 ** len(t)) for t in g)
    if weight < 1:  # @line L5
        return _both_false(f, g, sorted(every))
    if not every:  # @line L6
        return None
    count_f = {v: sum(1 for t in f if v in t) for v in every}  # @line L7
    count_g = {v: sum(1 for t in g if v in t) for v in every}
    v = max(sorted(every), key=lambda u: max(Fraction(count_f[u], len(f)), Fraction(count_g[u], len(g))))
    f0 = [t for t in f if v not in t]  # @line L8
    f1 = [t - {v} for t in f if v in t]
    g0 = [t for t in g if v not in t]
    g1 = [t - {v} for t in g if v in t]
    y = _dual(f0 + f1, g0)  # @line L9
    if y is not None:
        return y | {v}
    y = _dual(f0, g0 + g1)  # @line L10
    if y is not None:
        return y
    return None  # @line L11


def is_dual(f: Iterable[Iterable[int]], g: Iterable[Iterable[int]]) -> bool:
    """Return True when the monotone DNFs f and g are dual."""
    return dual_witness(f, g) is None


def minimal_transversals(edges: Iterable[Iterable[int]]) -> list[list[int]]:
    """Return all minimal transversals of a hypergraph, as sorted lists in sorted order.

    Each round asks whether the transversals found so far are the dual of the
    hypergraph. A witness x is then a set that contains no edge, whose
    complement is a transversal that contains no transversal found so far,
    and a greedy pass shrinks it to a new minimal transversal.
    """
    h = _minimize(edges)
    vertices = _variables(h, [])
    found: list[Term] = []
    while True:
        x = dual_witness(h, found)
        if x is None:
            break
        t = set(vertices - x)
        for v in sorted(t):
            smaller = t - {v}
            if all(e & smaller for e in h):
                t = smaller
        found.append(frozenset(t))
    return sorted(sorted(t) for t in found)
