# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/agm-bound/. The authors are listed in prov/79KBSS.jsonl.

"""The AGM bound of a join query, computed exactly.

A query is a list of edges (tuples of attribute names). A fractional edge cover
is x >= 0 with sum of x_e over the edges e that hold v at least 1, for each
attribute v. The AGM bound for relation sizes N_e and a cover x is
prod N_e^(x_e). The best bound minimizes sum x_e log N_e, a linear program.
The cover polyhedron is pointed (x >= 0), so a minimum is at a vertex; this
module lists the vertices exactly with Fractions, which is fine for the small
queries of the tests. Bounds are compared exactly by raising both sides to a
common denominator.
"""

from collections.abc import Sequence
from fractions import Fraction
from itertools import combinations, product
from math import lcm, prod


def _solve(rows: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction] | None:
    """Solve a square system by Gaussian elimination; None if it is singular."""
    k = len(rows)
    a = [r[:] + [b] for r, b in zip(rows, rhs)]
    for col in range(k):
        piv = next((i for i in range(col, k) if a[i][col] != 0), None)
        if piv is None:
            return None
        a[col], a[piv] = a[piv], a[col]
        for i in range(k):
            if i != col and a[i][col] != 0:
                f = a[i][col] / a[col][col]
                a[i] = [u - f * w for u, w in zip(a[i], a[col])]
    return [a[i][k] / a[i][i] for i in range(k)]


def polyhedron_vertices(cons: list[tuple[list[Fraction], Fraction]], dim: int) -> list[tuple[Fraction, ...]]:
    """All vertices of {z : a.z >= b for each (a, b) in cons} in dimension dim."""
    found = set()
    for pick in combinations(range(len(cons)), dim):
        z = _solve([list(cons[i][0]) for i in pick], [cons[i][1] for i in pick])
        if z is not None and all(sum(c * v for c, v in zip(a, z)) >= b for a, b in cons):
            found.add(tuple(z))
    return sorted(found)


def attributes(edges: Sequence[Sequence[str]]) -> list[str]:
    return sorted({v for e in edges for v in e})


def cover_vertices(edges: Sequence[Sequence[str]]) -> list[tuple[Fraction, ...]]:
    """Vertices of the fractional edge cover polyhedron of the query."""
    m = len(edges)
    cons = [([Fraction(int(v in e)) for e in edges], Fraction(1)) for v in attributes(edges)]
    cons += [([Fraction(int(i == j)) for j in range(m)], Fraction(0)) for i in range(m)]
    return polyhedron_vertices(cons, m)


def packing_vertices(edges: Sequence[Sequence[str]]) -> list[tuple[Fraction, ...]]:
    """Vertices of the fractional vertex packing polytope (the dual LP)."""
    vs = attributes(edges)
    cons = [([Fraction(-int(v in e)) for v in vs], Fraction(-1)) for e in edges]
    cons += [([Fraction(int(i == j)) for j in range(len(vs))], Fraction(0)) for i in range(len(vs))]
    return polyhedron_vertices(cons, len(vs))


def rho_star(edges: Sequence[Sequence[str]]) -> Fraction:
    """The fractional edge cover number: the minimum of sum x_e."""
    return min(sum(x) for x in cover_vertices(edges))


def _power(sizes: Sequence[int], x: Sequence[Fraction], d: int) -> int:
    """prod N_e^(d x_e), an integer when d is a multiple of each denominator."""
    return prod(n ** int(d * w) for n, w in zip(sizes, x))


def bound_le(a: Sequence[int], x: Sequence[Fraction], b: Sequence[int], y: Sequence[Fraction]) -> bool:
    """Exactly decide prod a_e^(x_e) <= prod b_e^(y_e) (all a_e, b_e >= 1)."""
    d = lcm(*(w.denominator for w in list(x) + list(y)))
    return _power(a, x, d) <= _power(b, y, d)


def count_le_bound(count: int, sizes: Sequence[int], x: Sequence[Fraction]) -> bool:
    """Exactly decide count <= prod N_e^(x_e)."""
    if 0 in sizes:
        return count == 0
    return bound_le([count], [Fraction(1)], sizes, x)


def optimal_cover(edges: Sequence[Sequence[str]], sizes: Sequence[int]) -> tuple[Fraction, ...]:
    """A cover x that minimizes prod N_e^(x_e); sizes must be at least 1."""
    best = None
    for x in cover_vertices(edges):
        if best is None or bound_le(sizes, x, sizes, best) and not bound_le(sizes, best, sizes, x):
            best = x
    return best


def join_size(edges: Sequence[Sequence[str]], rels: Sequence[set[tuple]]) -> int:
    """|Q| by backtracking over relations: each output tuple is one consistent
    choice of one tuple per relation. Used only on small instances."""
    count = 0
    stack = [(0, {})]
    while stack:
        i, asg = stack.pop()
        if i == len(edges):
            count += 1
            continue
        for t in rels[i]:
            if all(asg.get(v, a) == a for v, a in zip(edges[i], t)):
                nxt = dict(asg)
                nxt.update(zip(edges[i], t))
                stack.append((i + 1, nxt))
    return count


def product_instance(edges: Sequence[Sequence[str]], y: Sequence[Fraction], n: int) -> list[set[tuple]]:
    """The instance where attribute v has the domain range(n^(y_v)) and each
    relation is the product of the domains of its attributes."""
    vs = attributes(edges)
    dom = {}
    for v, w in zip(vs, y):
        r = round(n ** float(w))
        if Fraction(r) ** w.denominator != Fraction(n) ** w.numerator:
            raise ValueError("n^(y_v) must be an integer")
        dom[v] = range(r)
    return [set(product(*(dom[v] for v in e))) for e in edges]
