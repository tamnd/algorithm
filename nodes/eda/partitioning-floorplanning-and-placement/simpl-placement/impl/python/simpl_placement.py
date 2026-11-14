# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simpl-placement/. The authors are listed in prov/S9RKW6.jsonl.

"""SimPL on a small standard cell layout.

Rows 0 .. K-1 of height 1 and S sites of width 1. Cell i has an integer width W[i].
Pins 0 .. n-1 are the cells and pins n, n+1, ... are the fixed pads (points).
A legal position is (x, r): left edge on a site x, row r, so the pin is at (x + W/2, r + 1/2).
The lower bound (LB) placement solves the quadratic program of the bound-to-bound
net model with pseudo-nets to anchors. The upper bound (UB) placement is lookahead
legalization by recursive bisection; here the bisection goes down to single rows and
packs each row, so every UB placement is legal.
"""

from fractions import Fraction


# ---------- wirelength ----------

def pin_points(x, r, W, pads):
    """Pin points of all cells (left edge x, row r) followed by the pads."""
    return [(x[i] + Fraction(W[i], 2), r[i] + Fraction(1, 2)) for i in range(len(x))] + [tuple(p) for p in pads]


def hpwl_points(pts, nets, weights):
    total = 0
    for e, w in zip(nets, weights):
        xs = [pts[p][0] for p in e]
        ys = [pts[p][1] for p in e]
        total += w * (max(xs) - min(xs) + max(ys) - min(ys))
    return total


# ---------- the lower bound: bound-to-bound model and a linear solve ----------

def b2b_edges(coord, nets, weights, eps):
    """Edges (a, b, w) of the bound-to-bound model for one coordinate.
    The two extreme pins are joined, and every inner pin is joined to both,
    each with weight 2 w_e / ((p - 1) max(|c_a - c_b|, eps))."""
    edges = []
    for e, we in zip(nets, weights):
        pins = list(dict.fromkeys(e))
        p = len(pins)
        if p < 2:
            continue
        lo = min(pins, key=lambda q: (coord[q], q))
        hi = max(pins, key=lambda q: (coord[q], -q))
        if lo == hi:
            hi = next(q for q in pins if q != lo)

        def wt(a, b):
            return 2 * we / ((p - 1) * max(abs(coord[a] - coord[b]), eps))

        edges.append((lo, hi, wt(lo, hi)))
        for q in pins:
            if q != lo and q != hi:
                edges.append((q, lo, wt(q, lo)))
                edges.append((q, hi, wt(q, hi)))
    return edges


def quadratic_cost(coord, edges):
    return sum(w * (coord[a] - coord[b]) ** 2 for a, b, w in edges)


def solve_spd(A, b, tol=1e-12):
    """Conjugate gradients for a symmetric positive definite A given as sparse rows {j: a_ij}."""
    n = len(b)
    x = [0.0] * n
    r = list(b)
    p = list(r)
    rr = sum(v * v for v in r)
    limit = tol * tol * max(rr, 1e-300)
    for _ in range(4 * n + 20):
        if rr <= limit:
            break
        Ap = [sum(a * p[j] for j, a in row.items()) for row in A]
        alpha = rr / sum(pi * qi for pi, qi in zip(p, Ap))
        x = [xi + alpha * pi for xi, pi in zip(x, p)]
        r = [ri - alpha * qi for ri, qi in zip(r, Ap)]
        rr_new = sum(v * v for v in r)
        p = [ri + rr_new / rr * pi for ri, pi in zip(r, p)]
        rr = rr_new
    return x


def lower_bound(cx, cy, n, nets, weights, pads, anchors=None, alpha=0.0, eps=0.5, rounds=3):
    """Cell centers that minimize the B2B quadratic cost plus alpha |p_i - anchor_i|^2.
    The B2B weights are rebuilt from the current centers `rounds` times."""
    cx, cy = list(cx), list(cy)
    for _ in range(rounds):
        out = []
        for k, cur in ((0, cx), (1, cy)):
            coord = [float(v) for v in cur] + [float(p[k]) for p in pads]
            A = [dict() for _ in range(n)]
            b = [0.0] * n
            for a, c, w in b2b_edges(coord, nets, weights, eps):
                for u, v in ((a, c), (c, a)):
                    if u < n:
                        A[u][u] = A[u].get(u, 0.0) + w
                        if v < n:
                            A[u][v] = A[u].get(v, 0.0) - w
                        else:
                            b[u] += w * coord[v]
            if anchors is not None and alpha > 0:
                for i in range(n):
                    A[i][i] = A[i].get(i, 0.0) + alpha
                    b[i] += alpha * float(anchors[i][k])
            out.append(solve_spd(A, b))
        cx, cy = out
    return cx, cy


# ---------- the upper bound: lookahead legalization ----------

def pack_row(cells, tx, W, s0, s1):
    """Left edges for the cells of one row segment [s0, s1), in the order of their targets.
    Each cell goes to the site nearest its target, pushed right past the previous cell;
    then a pass from the right pulls cells back inside the segment."""
    order = sorted(cells, key=lambda i: (tx[i], i))
    pos = {}
    end = s0
    for i in order:
        want = int(round(tx[i] - W[i] / 2))
        pos[i] = max(end, min(max(want, s0), s1 - W[i]))
        end = pos[i] + W[i]
    limit = s1
    for i in reversed(order):
        pos[i] = min(pos[i], limit - W[i])
        limit = pos[i]
    return pos


def lookahead_legalize(tx, ty, W, K, S):
    """Recursive bisection of the cells over the rows and sites, splitting the cells
    at the point where their area matches the capacity of the two halves.
    Returns legal (x, r), or raises ValueError if a split cannot fit both halves."""
    n = len(W)
    x, r = [0] * n, [0] * n

    def rec(cells, r0, r1, s0, s1):
        if not cells:
            return
        if r1 - r0 > 1:
            mid = (r0 + r1) // 2
            cap_lo, cap_hi = (mid - r0) * (s1 - s0), (r1 - mid) * (s1 - s0)
            order = sorted(cells, key=lambda i: (ty[i], tx[i], i))
            key = lambda i: ty[i]
        else:
            if sum(W[i] for i in cells) > s1 - s0:
                raise ValueError("a row segment has more cell width than sites")
            if len(cells) == 1 or s1 - s0 < 2:
                for i, p in pack_row(cells, tx, W, s0, s1).items():
                    x[i], r[i] = p, r0
                return
            mid = (s0 + s1) // 2
            cap_lo, cap_hi = mid - s0, s1 - mid
            order = sorted(cells, key=lambda i: (tx[i], i))
            key = lambda i: tx[i]
        total = sum(W[i] for i in order)
        want = total * cap_lo / (cap_lo + cap_hi)
        best, acc = None, 0
        for k in range(len(order) + 1):
            if k:
                acc += W[order[k - 1]]
            if acc <= cap_lo and total - acc <= cap_hi:
                if best is None or abs(acc - want) < abs(best[1] - want):
                    best = (k, acc)
        if best is None:
            if r1 - r0 == 1:  # no split fits: pack the whole segment, which fits
                for i, p in pack_row(cells, tx, W, s0, s1).items():
                    x[i], r[i] = p, r0
                return
            raise ValueError("lookahead legalization found no split that fits")
        k = best[0]
        rec(order[:k], r0, mid, s0, s1) if r1 - r0 > 1 else rec(order[:k], r0, r1, s0, mid)
        rec(order[k:], mid, r1, s0, s1) if r1 - r0 > 1 else rec(order[k:], r0, r1, mid, s1)

    rec(list(range(n)), 0, K, 0, S)
    return x, r


# ---------- SimPL ----------

def simpl(n, nets, pads, W, K, S, weights=None, iterations=12, alpha0=0.05, gap=0.05, history=None):
    """Return the legal placement (x, r) of least HPWL among the UB placements."""
    if weights is None:
        weights = [1] * len(nets)
    cx = [S / 2 + 0.01 * (i % 7) for i in range(n)]  # @line L1
    cy = [K / 2 + 0.01 * (i % 5) for i in range(n)]
    cx, cy = lower_bound(cx, cy, n, nets, weights, pads, rounds=5)  # @line L2
    best = None
    for k in range(1, iterations + 1):  # @line L3
        ux, ur = lookahead_legalize(cx, cy, W, K, S)  # @line L4
        ub = hpwl_points(pin_points(ux, ur, W, pads), nets, weights)  # @line L5
        if best is None or ub < best[0]:
            best = (ub, ux, ur)
        anchors = [(ux[i] + W[i] / 2, ur[i] + 0.5) for i in range(n)]  # @line L6
        cx, cy = lower_bound(cx, cy, n, nets, weights, pads, anchors, alpha0 * k)  # @line L7
        lb = hpwl_points(list(zip(cx, cy)) + [tuple(map(float, p)) for p in pads], nets, weights)  # @line L8
        if history is not None:
            history.append((float(lb), ub))
        if ub - lb <= gap * ub:  # @line L9
            break
    return best[1], best[2]  # @line L10
