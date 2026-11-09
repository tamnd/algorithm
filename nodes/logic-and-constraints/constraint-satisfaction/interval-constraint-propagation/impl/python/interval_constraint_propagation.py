# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-constraint-propagation/. The authors are listed in prov/34RZ0J.jsonl.

"""Interval constraint propagation with the HC4 revise step.

An expression is a nested tuple:
    ("var", i)             the variable x_i
    ("const", c)           the number c (a float that is exactly the constant)
    ("add", e1, e2), ("sub", e1, e2), ("mul", e1, e2), ("sqr", e1)

A constraint is (expr, lo, hi), which means lo <= expr <= hi. Use lo == hi
for an equation and -inf or inf for a one-sided bound. A box is a list of
intervals (lo, hi), one for each variable.

Every interval operation rounds its result outward by one unit in the last
place, unless the result is an integer that floats hold exactly. Python floats
round to nearest, so one step outward covers the rounding error, and every
result interval contains the exact real result. So no real solution in the box
is ever removed.

icp(box, constraints) returns the narrowed box, or None when it proves that
the box holds no solution.
"""

import math
import sys
from collections import deque

INF = math.inf
Interval = tuple[float, float]
Expr = tuple
_BIG = 2.0**53
_MAX = sys.float_info.max


def _exact(*values: float) -> bool:
    """True when all values are integers below 2^53 in size.

    If the operands and the rounded result pass this test, the exact result is
    also below 2^53 (rounding is monotone and 2^53 is a float), so it is a float
    and the rounded result equals it.
    """
    return all(math.isfinite(v) and v.is_integer() and abs(v) < _BIG for v in values)


def _down(v: float, exact: bool) -> float:
    """A lower bound for the real number that v approximates (rounded to nearest)."""
    if v == INF:  # overflow: the real value is finite, so the largest float is below it
        return _MAX
    if exact or v == -INF:
        return v
    return math.nextafter(v, -INF)


def _up(v: float, exact: bool) -> float:
    """An upper bound for the real number that v approximates (rounded to nearest)."""
    if v == -INF:
        return -_MAX
    if exact or v == INF:
        return v
    return math.nextafter(v, INF)


def _meet(a: Interval | None, b: Interval) -> Interval | None:
    if a is None:
        return None
    lo, hi = max(a[0], b[0]), min(a[1], b[1])
    return (lo, hi) if lo <= hi else None


def _add(a: Interval, b: Interval) -> Interval:
    lo, hi = a[0] + b[0], a[1] + b[1]
    return (_down(lo, _exact(a[0], b[0], lo)), _up(hi, _exact(a[1], b[1], hi)))


def _sub(a: Interval, b: Interval) -> Interval:
    lo, hi = a[0] - b[1], a[1] - b[0]
    return (_down(lo, _exact(a[0], b[1], lo)), _up(hi, _exact(a[1], b[0], hi)))


def _times(x: float, y: float) -> float:
    return 0.0 if x == 0.0 or y == 0.0 else x * y  # 0 * inf is 0 for bounds


def _mul(a: Interval, b: Interval) -> Interval:
    los, his = [], []
    for x in a:
        for y in b:
            p = _times(x, y)
            ok = _exact(x, y, p) or x == 0.0 or y == 0.0
            los.append(_down(p, ok))
            his.append(_up(p, ok))
    return (min(los), max(his))


def _div(z: Interval, y: Interval) -> Interval:
    """An enclosure of {a / b : a in z, b in y}, used only when 0 is not in y."""
    if not (math.isfinite(z[0]) and math.isfinite(z[1])):
        return (-INF, INF)
    los, his = [], []
    for a in z:
        for b in y:
            q = a / b if math.isfinite(b) else 0.0
            ok = math.isfinite(b) and _exact(a, b, q) and q * b == a
            los.append(_down(q, ok))
            his.append(_up(q, ok))
    return (min(los), max(his))


def _sqr(a: Interval) -> Interval:
    lo, hi = a
    if lo >= 0.0:
        pair = (lo, hi)
    elif hi <= 0.0:
        pair = (-hi, -lo)
    else:
        pair = (0.0, max(-lo, hi))
    s, t = pair[0] * pair[0], pair[1] * pair[1]
    return (_down(s, _exact(pair[0], s)), _up(t, _exact(pair[1], t)))


def _sqrt_bounds(z: Interval) -> Interval:
    """[r0, r1] with sqrt of every value of z (clipped to z >= 0) inside it."""
    r0, r1 = math.sqrt(z[0]), math.sqrt(z[1])
    lo = _down(r0, _exact(r0, z[0]) and r0 * r0 == z[0])
    hi = _up(r1, _exact(r1, z[1]) and r1 * r1 == z[1])
    return (max(lo, 0.0), hi)


def _hull(a: Interval | None, b: Interval | None) -> Interval | None:
    if a is None:
        return b
    if b is None:
        return a
    return (min(a[0], b[0]), max(a[1], b[1]))


def compile_expr(expr: Expr) -> list[tuple]:
    """List the nodes of expr in post-order; a child index is smaller than its parent's."""
    nodes: list[tuple] = []
    done: list[int] = []
    stack: list[tuple[Expr, bool]] = [(expr, False)]
    while stack:
        e, expanded = stack.pop()
        op = e[0]
        if op in ("var", "const"):
            nodes.append(e)
            done.append(len(nodes) - 1)
        elif not expanded:
            stack.append((e, True))
            for child in reversed(e[1:]):
                stack.append((child, False))
        else:
            k = len(e) - 1
            kids = done[len(done) - k :]
            del done[len(done) - k :]
            nodes.append((op, *kids))
            done.append(len(nodes) - 1)
    return nodes


def hc4_revise(nodes: list[tuple], lo: float, hi: float, box: list[Interval]) -> list[Interval] | None:
    """One HC4 revise of the constraint lo <= expr <= hi. Returns a new box, or None."""
    iv: list[Interval | None] = [None] * len(nodes)
    for k, node in enumerate(nodes):  # @line L1
        op = node[0]
        if op == "var":
            iv[k] = box[node[1]]
        elif op == "const":
            iv[k] = (node[1], node[1])
        elif op == "add":
            iv[k] = _add(iv[node[1]], iv[node[2]])
        elif op == "sub":
            iv[k] = _sub(iv[node[1]], iv[node[2]])
        elif op == "mul":
            iv[k] = _mul(iv[node[1]], iv[node[2]])
        else:
            iv[k] = _sqr(iv[node[1]])
    root = len(nodes) - 1
    iv[root] = _meet(iv[root], (lo, hi))  # @line L2
    if iv[root] is None:  # @line L3
        return None
    new_box = list(box)
    for k in range(root, -1, -1):  # @line L4
        node, z = nodes[k], iv[k]
        op = node[0]
        if op == "var":  # @line L7
            new_box[node[1]] = _meet(new_box[node[1]], z)
            if new_box[node[1]] is None:
                return None
            continue
        if op == "const":
            continue
        a = node[1]
        if op == "add":  # @line L5
            iv[a] = _meet(iv[a], _sub(z, iv[node[2]]))
            if iv[a] is not None:
                iv[node[2]] = _meet(iv[node[2]], _sub(z, iv[a]))
        elif op == "sub":
            iv[a] = _meet(iv[a], _add(z, iv[node[2]]))
            if iv[a] is not None:
                iv[node[2]] = _meet(iv[node[2]], _sub(iv[a], z))
        elif op == "mul":
            b = node[2]
            if iv[b][0] > 0.0 or iv[b][1] < 0.0:
                iv[a] = _meet(iv[a], _div(z, iv[b]))
            if iv[a] is not None and (iv[a][0] > 0.0 or iv[a][1] < 0.0):
                iv[b] = _meet(iv[b], _div(z, iv[a]))
        else:
            zz = _meet(z, (0.0, INF))
            if zz is None:
                return None
            r = _sqrt_bounds(zz)
            iv[a] = _hull(_meet(iv[a], r), _meet(iv[a], (-r[1], -r[0])))
        if any(iv[c] is None for c in node[1:]):  # @line L6
            return None
    return new_box


def _narrowed(old: Interval, new: Interval, ratio: float) -> bool:
    w_old, w_new = old[1] - old[0], new[1] - new[0]
    if math.isinf(w_old):
        return math.isfinite(w_new)
    return w_new < (1.0 - ratio) * w_old


def icp(
    box: list[Interval],
    constraints: list[tuple[Expr, float, float]],
    ratio: float = 1e-3,
) -> list[Interval] | None:
    """Propagate the constraints over the box with HC4 until no width shrinks by ratio."""
    compiled = [compile_expr(e) for e, _, _ in constraints]
    scope = [sorted({nd[1] for nd in nodes if nd[0] == "var"}) for nodes in compiled]
    on_var: dict[int, list[int]] = {}
    for c, vs in enumerate(scope):
        for x in vs:
            on_var.setdefault(x, []).append(c)
    box = list(box)  # @line L8
    if any(lo > hi for lo, hi in box):
        return None
    queue = deque(range(len(constraints)))  # @line L9
    queued = [True] * len(constraints)
    while queue:  # @line L10
        c = queue.popleft()  # @line L11
        queued[c] = False
        new_box = hc4_revise(compiled[c], constraints[c][1], constraints[c][2], box)  # @line L12
        if new_box is None:  # @line L13
            return None
        for x in scope[c]:  # @line L14
            if _narrowed(box[x], new_box[x], ratio):
                for c2 in on_var[x]:
                    if not queued[c2]:
                        queued[c2] = True
                        queue.append(c2)
        box = new_box  # @line L15
    return box  # @line L16
