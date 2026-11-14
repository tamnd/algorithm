# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/a-star-bend-sequencing/. The authors are listed in prov/0RQ6RW.jsonl.

"""A* search for a cheapest bend sequence, with an admissible heuristic.

Model, as on the page (a planar profile model of a press brake):
- The part is a profile of flanges with integer lengths l[0], ..., l[n].
  Bend i (1 <= i <= n) joins flange i-1 and flange i and turns the
  profile by 90 degrees, to the left (sign +1) or to the right (sign -1)
  when you walk from flange 0 to flange n. A bend is either not done
  (the profile is straight there) or done fully.
- A tool is (punch width w, die width D, smallest flange m). Bend b can use
  tool t only if both flanges next to b have length at least m (the static
  fit) and, after the bend, no segment of the profile enters the open punch
  region or the open die region (the collision test).
- The part is turned over for a bend of sign -1, so that the punch is always
  on the inside of the bend. Two bends in a row with different signs cost
  `flip`. Two bends in a row with different tools cost `change`.

The search state is (done bends, sign of the last bend, last tool). All
geometry is on integer points, and the clipping in the collision test uses
Fraction, so it is exact.
"""

import heapq
from collections import namedtuple
from fractions import Fraction

Tool = namedtuple("Tool", ["width", "die", "min_flange"])
Plan = namedtuple("Plan", ["cost", "steps", "expanded"])
# steps: a list of (bend, tool index) in the order of the plan.


def _rot(d, e):
    """Turn the direction d by 90 degrees: to the left if e = +1, to the right if e = -1."""
    x, y = d
    return (-y, x) if e > 0 else (y, -x)


def profile_after(lengths, signs, done, b):
    """Segments of the profile after the bends in `done` and bend b, in the frame of bend b.

    In this frame bend b is at the origin and turns to the left, flange b
    runs along +x and flange b-1 along +y, so the inside of the bend is the
    open quadrant x > 0, y > 0. If bend b turns to the right, the whole
    profile is mirrored, which is the part turned over.
    """
    n = len(lengths) - 1
    mirror = signs[b]
    segs = []
    p, d = (0, 0), (1, 0)
    for j in range(b, n + 1):
        q = (p[0] + lengths[j] * d[0], p[1] + lengths[j] * d[1])
        segs.append((p, q))
        p = q
        if j < n and (j + 1) in done:
            d = _rot(d, signs[j + 1] * mirror)
    p, d = (0, 0), (0, 1)
    for j in range(b - 1, -1, -1):
        q = (p[0] + lengths[j] * d[0], p[1] + lengths[j] * d[1])
        segs.append((p, q))
        p = q
        if j > 0 and j in done:
            d = _rot(d, -signs[j] * mirror)
    return segs


def _meets_open(seg, halfplanes):
    """True if the segment meets the open set {a x + c y < k for each (a, c, k)}.

    The points of the segment are p + s (q - p) with 0 <= s <= 1. Each strict
    inequality keeps an open interval of s. The set is not empty if and only
    if the largest lower end is below the smallest upper end, or they are
    equal and both ends are closed (that is, only s = 0 or s = 1 bounds).
    """
    (px, py), (qx, qy) = seg
    lo, lo_open = Fraction(0), False
    hi, hi_open = Fraction(1), False
    for a, c, k in halfplanes:
        alpha = a * px + c * py - k
        beta = a * (qx - px) + c * (qy - py)
        if beta == 0:
            if alpha >= 0:
                return False
            continue
        r = Fraction(-alpha, beta)
        if beta > 0:
            if r < hi or (r == hi and not hi_open):
                hi, hi_open = r, True
        else:
            if r > lo or (r == lo and not lo_open):
                lo, lo_open = r, True
    if lo < hi:
        return True
    return lo == hi and not lo_open and not hi_open


def collides(lengths, signs, done, b, tool):
    """True if bend b, made with `tool` after the bends in `done`, hits the punch or the die."""
    w, die, _ = tool
    punch = [(-1, 0, 0), (0, -1, 0), (1, -1, w), (-1, 1, w)]  # x > 0, y > 0, |x - y| < w
    below = [(1, 1, 0), (1, -1, die), (-1, 1, die)]  # x + y < 0, |x - y| < die
    for seg in profile_after(lengths, signs, done, b):
        if _meets_open(seg, punch) or _meets_open(seg, below):
            return True
    return False


def fits(lengths, b, tool):
    """The static fit: both flanges next to bend b are at least the smallest flange of the tool."""
    return min(lengths[b - 1], lengths[b]) >= tool.min_flange


def heuristic(n, signs, fit_mask, state, flip, change):
    """The admissible heuristic of the page.

    flip   if some bend left has a sign other than the last sign
           (or, at the start, if the bends left have both signs);
    change if the last tool does not fit some bend left
           (or, at the start, if no one tool fits all bends left).
    """
    done, last_sign, last_tool = state
    left = [b for b in range(1, n + 1) if not done >> b & 1]
    if not left:
        return 0
    h = 0
    left_signs = {signs[b] for b in left}
    if (last_sign == 0 and len(left_signs) > 1) or (last_sign != 0 and left_signs != {last_sign}):
        h += flip
    if last_tool < 0:
        common = ~0
        for b in left:
            common &= fit_mask[b]
        if common == 0:
            h += change
    elif any(not fit_mask[b] >> last_tool & 1 for b in left):
        h += change
    return h


def a_star_bends(lengths, signs, tools, flip=1, change=1, use_h=True):
    """A cheapest feasible bend sequence, or None if there is none.

    `signs` is indexed 1..n (signs[0] is not used). Returns Plan(cost, steps,
    expanded), where `expanded` counts the states taken from the queue.
    With use_h=False the search is uniform cost search (h = 0).
    """
    n = len(lengths) - 1
    k = len(tools)
    full = sum(1 << b for b in range(1, n + 1))
    fit_mask = [0] * (n + 1)
    for b in range(1, n + 1):
        for t in range(k):
            if fits(lengths, b, tools[t]):
                fit_mask[b] |= 1 << t

    def h(state):
        return heuristic(n, signs, fit_mask, state, flip, change) if use_h else 0

    hits = {}  # (done, b, t) -> collision; it depends on the done set only, not on the last sign or tool

    def blocked(done, done_set, b, t):
        key = (done, b, t)
        if key not in hits:
            hits[key] = collides(lengths, signs, done_set, b, tools[t])
        return hits[key]

    start = (0, 0, -1)  # @line L1
    g = {start: 0}
    parent = {start: None}
    tick = 0
    queue = [(h(start), tick, start)]
    closed = set()
    expanded = 0
    while queue:  # @line L2
        _, _, u = heapq.heappop(queue)  # @line L3
        if u in closed:
            continue
        closed.add(u)
        expanded += 1
        done, last_sign, last_tool = u
        if done == full:  # @line L4
            steps = []
            while parent[u] is not None:
                p = parent[u]
                steps.append(((u[0] ^ p[0]).bit_length() - 1, u[2]))
                u = p
            steps.reverse()
            return Plan(g[(full, last_sign, last_tool)], steps, expanded)
        done_set = {b for b in range(1, n + 1) if done >> b & 1}
        for b in range(1, n + 1):  # @line L5
            if done >> b & 1:
                continue
            for t in range(k):
                if not fit_mask[b] >> t & 1:
                    continue
                if blocked(done, done_set, b, t):  # @line L6
                    continue
                v = (done | 1 << b, signs[b], t)  # @line L7
                step = (flip if last_sign not in (0, signs[b]) else 0) + (change if last_tool not in (-1, t) else 0)
                cost = g[u] + step
                if v not in g or cost < g[v]:  # @line L8
                    g[v] = cost
                    parent[v] = u
                    tick += 1
                    heapq.heappush(queue, (cost + h(v), tick, v))
    return None  # @line L9


def plan_cost(lengths, signs, tools, steps, flip=1, change=1):
    """The cost of a plan, or None if a step is not feasible. Used to check plans."""
    n = len(lengths) - 1
    if sorted(b for b, _ in steps) != list(range(1, n + 1)):
        return None
    done = set()
    cost = 0
    last_sign, last_tool = 0, -1
    for b, t in steps:
        if not fits(lengths, b, tools[t]) or collides(lengths, signs, done, b, tools[t]):
            return None
        if last_sign not in (0, signs[b]):
            cost += flip
        if last_tool not in (-1, t):
            cost += change
        last_sign, last_tool = signs[b], t
        done.add(b)
    return cost


if __name__ == "__main__":
    # The lipped channel of the page: STANDARD and GOOSENECK, flip 2, change 1.
    lengths = [1, 4, 6, 4, 1]
    signs = [0, 1, 1, 1, 1]
    tools = [Tool(3, 2, 1), Tool(1, 4, 2)]
    print(a_star_bends(lengths, signs, tools, flip=2, change=1))
