# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/banerjee-test/. The authors are listed in prov/PS0MQH.jsonl.
"""The Banerjee test with direction vectors, for rectangular loop nests.

A loop nest has depth k, and loop l runs over the integers L_l..U_l, given as
bounds = [(L_1, U_1), ..., (L_k, U_k)]. A subscript is a tuple
(c0, c1, ..., ck) for c0 + c1*i1 + ... + ck*ik. The source reference uses
the indices i and the sink reference the indices j; a reference to an array
of m dimensions is a list of m subscripts.

The direction psi_l relates i_l and j_l: "<" is i_l < j_l, "=" is i_l = j_l,
">" is i_l > j_l and "*" is no constraint (Wolfe's notation).

banerjee_test returns "independent" when, for some subscript, the equation
sum(a_l i_l) - sum(b_l j_l) = b0 - a0 has no real solution in the region of
the bounds and the directions, and "maybe" otherwise.
"""

from fractions import Fraction


def pos(x: int) -> int:
    """The positive part x+ = max(x, 0)."""
    return x if x > 0 else 0


def neg(x: int) -> int:
    """The negative part x- = max(-x, 0); x = x+ - x-."""
    return -x if x < 0 else 0


def level_bounds(a: int, b: int, lo: int, hi: int, d: str):
    """Min and max of a*x - b*y over the real region of one level, or None.

    The region is lo <= x, y <= hi with x = y for "=", x + 1 <= y for "<",
    y + 1 <= x for ">" and no relation for "*". It is empty for "<" and ">"
    when hi - lo < 1.
    """
    n = hi - lo
    if d == "*":
        return (pos(a) * lo - neg(a) * hi - pos(b) * hi + neg(b) * lo,  # @line L10
                pos(a) * hi - neg(a) * lo - pos(b) * lo + neg(b) * hi)
    if d == "=":
        c = a - b
        return (pos(c) * lo - neg(c) * hi, pos(c) * hi - neg(c) * lo)  # @line L11
    if n < 1:
        return None
    if d == "<":
        v0 = (a - b) * lo - b
        return (v0 - pos(neg(a) + b) * (n - 1), v0 + pos(pos(a) - b) * (n - 1))  # @line L12
    v0 = (a - b) * lo + a
    return (v0 - pos(pos(b) - a) * (n - 1), v0 + pos(a + neg(b)) * (n - 1))  # @line L13


def subscript_bounds(src, snk, bounds, psi=None):
    """Min and max of the left side of the dependence equation, or None."""
    lo_sum, hi_sum = 0, 0  # @line L3
    for l, (lo, hi) in enumerate(bounds):  # @line L4
        d = "*" if psi is None else psi[l]
        r = level_bounds(src[l + 1], snk[l + 1], lo, hi, d)  # @line L5
        if r is None:
            return None  # @line L6
        lo_sum += r[0]  # @line L7
        hi_sum += r[1]
    return lo_sum, hi_sum


def banerjee_test(src, snk, bounds, psi=None) -> str:
    """The Banerjee test for two references and an optional direction vector."""
    for f, g in zip(src, snk):  # @line L1
        c = g[0] - f[0]  # @line L2
        r = subscript_bounds(f, g, bounds, psi)
        if r is None or c < r[0] or c > r[1]:  # @line L8
            return "independent"
    return "maybe"  # @line L9


def direction_vectors(src, snk, bounds) -> set:
    """All plain direction vectors that the Banerjee test does not rule out.

    The search refines one "*" at a time, from the outermost level, and cuts
    a branch as soon as the test says "independent".
    """
    k = len(bounds)
    out = set()

    def refine(psi: tuple) -> None:
        if banerjee_test(src, snk, bounds, psi) == "independent":
            return
        if "*" not in psi:
            out.add(psi)
            return
        l = psi.index("*")
        for d in "<=>":
            refine(psi[:l] + (d,) + psi[l + 1:])

    refine(("*",) * k)
    return out


def level_vertices(lo: int, hi: int, d: str) -> list:
    """The vertices of the real region of one level, as (x, y) pairs."""
    if d == "*":
        return [(lo, lo), (lo, hi), (hi, lo), (hi, hi)]
    if d == "=":
        return [(lo, lo), (hi, hi)]
    if hi - lo < 1:
        return []
    if d == "<":
        return [(lo, lo + 1), (lo, hi), (hi - 1, hi)]
    return [(lo + 1, lo), (hi, lo), (hi, hi - 1)]


def real_witness(src, snk, bounds, psi=None):
    """A real solution (x, y) of one subscript equation in the region, or None.

    It joins the vertex that gives the minimum with the vertex that gives the
    maximum at each level; the segment between the two points stays in the
    region, and the left side runs over [lo, hi] along it.
    """
    k = len(bounds)
    c = snk[0] - src[0]
    pmin, pmax = [], []
    for l, (lo, hi) in enumerate(bounds):
        d = "*" if psi is None else psi[l]
        vs = level_vertices(lo, hi, d)
        if not vs:
            return None
        val = lambda p: src[l + 1] * p[0] - snk[l + 1] * p[1]  # noqa: E731
        pmin.append(min(vs, key=val))
        pmax.append(max(vs, key=val))
    left = lambda ps: sum(src[l + 1] * ps[l][0] - snk[l + 1] * ps[l][1] for l in range(k))  # noqa: E731
    lo_v, hi_v = left(pmin), left(pmax)
    if c < lo_v or c > hi_v:
        return None
    t = Fraction(0) if hi_v == lo_v else Fraction(c - lo_v, hi_v - lo_v)
    x = [pmin[l][0] + t * (pmax[l][0] - pmin[l][0]) for l in range(k)]
    y = [pmin[l][1] + t * (pmax[l][1] - pmin[l][1]) for l in range(k)]
    return x, y


if __name__ == "__main__":
    # for i = 1 to 5: A[i] = A[i + 10]: the range of i - j is [-4, 4].
    print(banerjee_test([(0, 1)], [(10, 1)], [(1, 5)]))  # independent
    # for i = 1 to 3: A[2*i] = A[3*i + 2]: maybe, only with ">".
    print(banerjee_test([(0, 2)], [(2, 3)], [(1, 3)]))  # maybe
    print(sorted(direction_vectors([(0, 2)], [(2, 3)], [(1, 3)])))  # [('>',)]
