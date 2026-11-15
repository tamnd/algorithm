# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/practical-dependence-tests/. The authors are listed in prov/B1R5XX.jsonl.
"""Subscript-wise dependence testing: ZIV, SIV and MIV tests joined by the delta test.

A rectangular loop nest has depth k, and loop l runs over L_l..U_l, given as
bounds = [(L_1, U_1), ..., (L_k, U_k)]. A subscript is a tuple
(c0, c1, ..., ck) for c0 + c1*i1 + ... + ck*ik. The source reference uses
the indices i, the sink reference the indices j. A pair of references to an
array of m dimensions is given as two lists of m subscripts.

The direction of level l is "<" when i_l < j_l, "=" when i_l = j_l and ">"
when i_l > j_l (Wolfe's notation). The result lists raw direction vectors of
the solutions: a vector whose first non-"=" entry is ">" belongs to the
dependence from the sink reference to the source reference.

The solution set of one level is kept exactly, as one of
    ("free",)                           all pairs in the box
    ("empty",)                          no pair
    ("point", i, j)                     one pair
    ("line", i0, j0, p, q, tlo, thi)    the pairs (i0 + p*t, j0 + q*t), tlo <= t <= thi
"""

from math import gcd
from itertools import product

FREE = ("free",)
EMPTY = ("empty",)
DIRS = "<=>"


def ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


def ext_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Return (g, x, y) with a*x + b*y = g = gcd(a, b) and g >= 0."""
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b != 0:
        q, r = divmod(a, b)
        a, b = b, r
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    if a < 0:
        return -a, -x0, -y0
    return a, x0, y0


def axis_range(x0: int, p: int, lo: int, hi: int):
    """The integers t with lo <= x0 + p*t <= hi, as (tmin, tmax), or None for all t."""
    if p == 0:
        return None if lo <= x0 <= hi else (1, 0)
    if p > 0:
        return ceil_div(lo - x0, p), (hi - x0) // p
    return ceil_div(hi - x0, p), (lo - x0) // p


def line_in_box(i0: int, j0: int, p: int, q: int, lo: int, hi: int):
    """The points (i0 + p*t, j0 + q*t) inside [lo, hi]^2, as a level state."""
    tlo, thi = None, None
    for x0, s in ((i0, p), (j0, q)):
        r = axis_range(x0, s, lo, hi)
        if r is None:
            continue
        tlo = r[0] if tlo is None else max(tlo, r[0])
        thi = r[1] if thi is None else min(thi, r[1])
    if tlo > thi:
        return EMPTY
    if tlo == thi:
        return ("point", i0 + p * tlo, j0 + q * tlo)
    return ("line", i0, j0, p, q, tlo, thi)


def siv_kind(a: int, b: int) -> str:
    """The name of the SIV test for a*i - b*j = c, with (a, b) != (0, 0)."""
    if a == b:
        return "strong"
    if a == 0 or b == 0:
        return "weak-zero"
    if a == -b:
        return "weak-crossing"
    return "exact"


def siv_solve(a: int, b: int, c: int, lo: int, hi: int):
    """All integer (i, j) in [lo, hi]^2 with a*i - b*j = c, as a level state."""
    kind = siv_kind(a, b)
    if kind == "strong":
        # a*i + c1 = a*j + c2: the distance j - i is (c1 - c2) / a = -c / a.
        if c % a != 0:
            return EMPTY
        d = -(c // a)
        if abs(d) > hi - lo:
            return EMPTY
        return line_in_box(0, d, 1, 1, lo, hi)
    if kind == "weak-zero":
        if b == 0:
            if c % a != 0:
                return EMPTY
            return line_in_box(c // a, 0, 0, 1, lo, hi)
        if c % b != 0:
            return EMPTY
        return line_in_box(0, -(c // b), 1, 0, lo, hi)
    if kind == "weak-crossing":
        # a*i + a*j = c: the pairs with i + j = c / a, which cross at (c / a) / 2.
        if c % a != 0:
            return EMPTY
        return line_in_box(0, c // a, 1, -1, lo, hi)
    g, x, y = ext_gcd(a, -b)
    if c % g != 0:
        return EMPTY
    p, q = b // g, a // g
    if p < 0:
        p, q = -p, -q
    return line_in_box(x * (c // g), y * (c // g), p, q, lo, hi)


def meet(state, a: int, b: int, c: int, lo: int, hi: int):
    """The level state cut by the equation a*i - b*j = c."""
    if a == 0 and b == 0:
        return state if c == 0 else EMPTY
    kind = state[0]
    if kind == "empty":
        return EMPTY
    if kind == "free":
        return siv_solve(a, b, c, lo, hi)
    if kind == "point":
        return state if a * state[1] - b * state[2] == c else EMPTY
    _, i0, j0, p, q, tlo, thi = state
    coef = a * p - b * q
    rhs = c - a * i0 + b * j0
    if coef == 0:
        return state if rhs == 0 else EMPTY
    if rhs % coef != 0:
        return EMPTY
    t = rhs // coef
    if not tlo <= t <= thi:
        return EMPTY
    return ("point", i0 + p * t, j0 + q * t)


def propagate(A: list[int], B: list[int], c: int, states: list):
    """The delta step: rewrite sum(A[l] i_l - B[l] j_l) = c with the known level facts."""
    A, B = list(A), list(B)
    for l in range(len(A)):
        if A[l] == 0 and B[l] == 0:
            continue
        st = states[l]
        if st[0] == "point":
            c -= A[l] * st[1] - B[l] * st[2]
            A[l] = B[l] = 0
        elif st[0] == "line":
            _, i0, j0, p, q, _, _ = st
            if p == 0:  # i_l is the constant i0
                c -= A[l] * i0
                A[l] = 0
            elif q == 0:  # j_l is the constant j0
                c += B[l] * j0
                B[l] = 0
            elif p == q:  # j_l = i_l + d with the distance d = j0 - i0
                c += B[l] * (j0 - i0)
                A[l] -= B[l]
                B[l] = 0
    return A, B, c


def level_view(state, d: str, lo: int, hi: int):
    """The part of a level state with direction d, or None if it is empty."""
    kind = state[0]
    if kind == "empty":
        return None
    if kind == "free":
        return None if d != "=" and hi - lo < 1 else ("free", d)
    if kind == "point":
        i, j = state[1], state[2]
        return state if direction(i, j) == d else None
    _, i0, j0, p, q, tlo, thi = state
    e0, e1 = i0 - j0, p - q  # i - j = e0 + e1*t
    if d == "=":
        if e1 == 0:
            return state if e0 == 0 else None
        if e0 % e1 != 0 or not tlo <= -(e0 // e1) <= thi:
            return None
        t = -(e0 // e1)
        return ("point", i0 + p * t, j0 + q * t)
    # "<" needs e0 + e1*t <= -1, and ">" needs e0 + e1*t >= 1.
    t1, t2 = tlo, thi
    if e1 == 0:
        ok = e0 <= -1 if d == "<" else e0 >= 1
        return state if ok else None
    if d == "<":
        bound = -1 - e0
        if e1 > 0:
            t2 = min(t2, bound // e1)
        else:
            t1 = max(t1, ceil_div(bound, e1))
    else:
        bound = 1 - e0
        if e1 > 0:
            t1 = max(t1, ceil_div(bound, e1))
        else:
            t2 = min(t2, bound // e1)
    if t1 > t2:
        return None
    return ("line", i0, j0, p, q, t1, t2)


def direction(i: int, j: int) -> str:
    return "<" if i < j else ("=" if i == j else ">")


def term_values(view, a: int, b: int, lo: int, hi: int):
    """(min, max, step, offset) for the values of a*i - b*j over a level view.

    Every value lies in [min, max] and is offset plus a multiple of step.
    """
    if view[0] == "free":
        d = view[1]
        pa, na, pb, nb = max(a, 0), max(-a, 0), max(b, 0), max(-b, 0)
        n = hi - lo
        if d == "=":
            e = a - b
            return max(e, 0) * lo - max(-e, 0) * hi, max(e, 0) * hi - max(-e, 0) * lo, e, 0
        if d == "<":
            v0 = (a - b) * lo - b
            return v0 - max(na + b, 0) * (n - 1), v0 + max(pa - b, 0) * (n - 1), gcd(a, b), 0
        v0 = (a - b) * lo + a
        return v0 - max(pb - a, 0) * (n - 1), v0 + max(a + nb, 0) * (n - 1), gcd(a, b), 0
    if view[0] == "point":
        v = a * view[1] - b * view[2]
        return v, v, 0, v
    _, i0, j0, p, q, t1, t2 = view
    k0, k1 = a * i0 - b * j0, a * p - b * q
    v1, v2 = k0 + k1 * t1, k0 + k1 * t2
    return min(v1, v2), max(v1, v2), k1, k0


def miv_allows(eq, psi_views: dict, bounds) -> bool:
    """GCD and Banerjee test of one MIV equation over the chosen level views."""
    A, B, c = eq
    lo_sum, hi_sum, g, off = 0, 0, 0, 0
    for l, view in psi_views.items():
        if A[l] == 0 and B[l] == 0:
            continue
        lo, hi, step, offset = term_values(view, A[l], B[l], *bounds[l])
        lo_sum += lo
        hi_sum += hi
        g = gcd(g, step)
        off += offset
    if not lo_sum <= c <= hi_sum:
        return False
    return (c - off) % g == 0 if g != 0 else c == off


def coupled_groups(pairs, k: int) -> list:
    """Union-find on the levels: pairs that share a level end in one group."""
    parent = list(range(k))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for f, g in pairs:
        used = [l for l in range(k) if f[l + 1] or g[l + 1]]
        for l in used[1:]:
            parent[find(l)] = find(used[0])
    groups: dict = {}
    for f, g in pairs:
        used = [l for l in range(k) if f[l + 1] or g[l + 1]]
        groups.setdefault(find(used[0]), []).append((f, g))
    return list(groups.values())


def delta_test(group, k: int, bounds):
    """Run the delta test on one coupled group.

    Returns None if the group proves independence, else (states, miv) with
    the exact solution set of each level under the SIV constraints, and the
    equations that stay MIV.
    """
    states = [FREE] * k  # @line L5
    pending = [([f[l + 1] for l in range(k)], [g[l + 1] for l in range(k)], g[0] - f[0]) for f, g in group]
    changed = True
    while changed:  # @line L6
        changed = False
        rest = []
        for A, B, c in pending:
            A, B, c = propagate(A, B, c, states)  # @line L7
            used = [l for l in range(k) if A[l] or B[l]]
            if not used:
                if c != 0:
                    return None  # @line L8
                changed = True
            elif len(used) == 1:
                l = used[0]
                states[l] = meet(states[l], A[l], B[l], c, *bounds[l])  # @line L9
                if states[l] == EMPTY:
                    return None  # @line L10
                changed = True
            else:
                rest.append((A, B, c))
        pending = rest  # @line L11
    return states, pending


def distance_of(state, lo: int, hi: int):
    """The distance j - i if it is the same for every pair of the state, else None."""
    if state[0] == "free":
        return 0 if lo == hi else None
    if state[0] == "point":
        return state[2] - state[1]
    if state[0] == "line" and state[3] == state[4]:
        return state[2] - state[1]
    return None


def dependence(src, snk, bounds) -> dict:
    """Test two references; return the directions, distances and exactness.

    The result has the keys "independent" (bool), "directions" (a set of
    tuples over the k levels), "distances" (a list with an int or None for
    each level) and "exact" (True when no MIV equation remained, so that the
    directions are exactly those of the integer solutions).
    """
    k = len(bounds)
    pairs = []
    for f, g in zip(src, snk):
        if all(f[l + 1] == 0 and g[l + 1] == 0 for l in range(k)):  # @line L1
            if f[0] != g[0]:
                return {"independent": True, "directions": set(), "distances": [None] * k, "exact": True}  # @line L2
        else:
            pairs.append((f, g))
    states = [FREE] * k
    level_dirs = [None] * k
    group_dirs = []
    exact = True
    for group in coupled_groups(pairs, k):  # @line L3
        levels = sorted({l for f, g in group for l in range(k) if f[l + 1] or g[l + 1]})
        res = delta_test(group, k, bounds)  # @line L4
        if res is None:
            return {"independent": True, "directions": set(), "distances": [None] * k, "exact": True}
        st, miv = res
        for l in levels:
            states[l] = st[l]
        options = [[d for d in DIRS if level_view(st[l], d, *bounds[l]) is not None] for l in levels]
        found = set()
        for combo in product(*options):  # @line L12
            views = {l: level_view(st[l], d, *bounds[l]) for l, d in zip(levels, combo)}
            if all(miv_allows(eq, views, bounds) for eq in miv):
                found.add(combo)
        if not found:
            return {"independent": True, "directions": set(), "distances": [None] * k, "exact": True}  # @line L13
        if miv:
            exact = False
        group_dirs.append((levels, found))
        for l in levels:
            level_dirs[l] = True
    free_options = []
    for l in range(k):
        if level_dirs[l] is None:
            free_options.append((l, [d for d in DIRS if level_view(FREE, d, *bounds[l]) is not None]))
    directions = set()
    group_choices = [sorted(found) for _, found in group_dirs]
    for picks in product(*group_choices, *[opts for _, opts in free_options]):
        vec = [None] * k
        for (levels, _), combo in zip(group_dirs, picks[: len(group_dirs)]):
            for l, d in zip(levels, combo):
                vec[l] = d
        for (l, _), d in zip(free_options, picks[len(group_dirs):]):
            vec[l] = d
        directions.add(tuple(vec))
    distances = [distance_of(states[l], *bounds[l]) for l in range(k)]
    return {"independent": False, "directions": directions, "distances": distances, "exact": exact}  # @line L14


if __name__ == "__main__":
    # for i = 1 to 8: for j = 1 to 8: A[i + 1][j] = A[i][j]
    r = dependence([(1, 1, 0), (0, 0, 1)], [(0, 1, 0), (0, 0, 1)], [(1, 8), (1, 8)])
    print(r)  # directions {("<", "=")}, distances [1, 0], exact
    # for i = 1 to 8: A[i][i] = A[i][i + 1]: the delta test proves independence
    print(dependence([(0, 1), (0, 1)], [(0, 1), (1, 1)], [(1, 8)])["independent"])
