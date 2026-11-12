# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lee-visibility-polygon-algorithm/. The authors are listed in prov/V14M2Q.jsonl.

"""Visibility polygon of a point inside a simple polygon in O(n) time.

This is Lee's linear scan with the correction of Joe and Simpson (1987).
The boundary is scanned once, counterclockwise, from a point v0 that the
viewpoint z sees. A stack holds the visible chain found so far. The scan
is in one of six states:

  LEFT   the boundary moves counterclockwise around z and is visible
  RIGHT  the boundary moves clockwise around z and hides stack points
  SCANA  the boundary went behind the stack top; find where it comes out
  SCANB  the boundary crossed the ray z v0; look for the window back to v0
  SCANC  the boundary is in front of a hidden window; find its far end
  SCAND  the boundary is behind a window; find where it crosses it

All arithmetic is exact (Fraction), so the orientation tests are exact.
"""

from fractions import Fraction

LEFT, RIGHT, SCANA, SCANB, SCANC, SCAND, FINISH = range(7)
STATE_NAMES = ["LEFT", "RIGHT", "SCANA", "SCANB", "SCANC", "SCAND", "FINISH"]

CCW = 1  # left turn
CW = -1  # right turn


def orient(a, b, c):
    """Sign of the cross product (b - a) x (c - a): 1 left, -1 right, 0 collinear."""
    d = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (d > 0) - (d < 0)


def _collinear_overlap(a, b, c, d):
    """Intersection of two collinear closed segments: a point, "overlap" or None."""
    lo = max(min(a, b), min(c, d))
    hi = min(max(a, b), max(c, d))
    if lo > hi:
        return None
    if lo == hi:
        return lo
    return "overlap"


def seg_seg(a, b, c, d):
    """Intersection of closed segments ab and cd: a point, "overlap" or None."""
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    if o1 == 0 and o2 == 0 and o3 == 0 and o4 == 0:
        return _collinear_overlap(a, b, c, d)
    if o1 * o2 > 0 or o3 * o4 > 0:
        return None
    den = (b[0] - a[0]) * (d[1] - c[1]) - (b[1] - a[1]) * (d[0] - c[0])
    t = ((c[0] - a[0]) * (d[1] - c[1]) - (c[1] - a[1]) * (d[0] - c[0])) / den
    return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))


def seg_ray(a, b, o, r):
    """Intersection of the closed segment ab with the ray from o through r."""
    dx, dy = r[0] - o[0], r[1] - o[1]
    oa, ob = orient(o, r, a), orient(o, r, b)
    if oa == 0 and ob == 0:
        ta = (a[0] - o[0]) * dx + (a[1] - o[1]) * dy
        tb = (b[0] - o[0]) * dx + (b[1] - o[1]) * dy
        hi = max(ta, tb)
        if hi < 0:
            return None
        if max(min(ta, tb), 0) == hi:
            return a if ta == hi else b
        return "overlap"
    if oa * ob > 0:
        return None
    den = dx * (b[1] - a[1]) - dy * (b[0] - a[0])
    t = ((a[0] - o[0]) * (b[1] - a[1]) - (a[1] - o[1]) * (b[0] - a[0])) / den
    if t < 0:
        return None
    return (o[0] + t * dx, o[1] + t * dy)


def _between(p, q, r):
    """For collinear p, q, r: True if q lies on the closed segment pr."""
    return min(p, r) <= q <= max(p, r)


def _signed_area2(pts):
    s = 0
    for i in range(len(pts)):
        x1, y1 = pts[i - 1]
        x2, y2 = pts[i]
        s += x1 * y2 - x2 * y1
    return s


def _start_sequence(pts, z):
    """Shoot a ray up from z. Return [v0, v1, ..., v0], where v0 is the hit point.

    v0 is the boundary point nearest to z straight above it, so z sees it.
    The rest of the list is the boundary in counterclockwise order.
    """
    n = len(pts)
    best = None
    for k in range(n):
        a, b = pts[k], pts[(k + 1) % n]
        if a[0] == b[0]:
            if a[0] != z[0]:
                continue
            for j, p in ((k, a), ((k + 1) % n, b)):
                if p[1] > z[1] and (best is None or p[1] < best[0]):
                    best = (p[1], "vertex", j)
            continue
        if not (min(a[0], b[0]) <= z[0] <= max(a[0], b[0])):
            continue
        y = a[1] + (z[0] - a[0]) * (b[1] - a[1]) / (b[0] - a[0])
        if y > z[1] and (best is None or y < best[0]):
            if (z[0], y) == a:
                best = (y, "vertex", k)
            elif (z[0], y) == b:
                best = (y, "vertex", (k + 1) % n)
            else:
                best = (y, "edge", k)
    if best is None:
        raise ValueError("the viewpoint is not inside the polygon")
    y, what, k = best
    if what == "vertex":
        seq = pts[k:] + pts[:k]
        return seq + [seq[0]]
    p = (z[0], y)
    seq = pts[k + 1:] + pts[:k + 1]
    return [p] + seq + [p]


def _scan_edges(v, i, a, b, is_ray):
    """First edge v[k] v[k+1], k >= i, that meets the ray (a, b) or the segment ab.

    Returns k and the meeting point u. An edge that lies along the ray gives
    u = v[k+1].
    """
    old = CW
    for k in range(i, len(v) - 1):
        cur = orient(a, b, v[k + 1])
        if cur != old:
            if is_ray:
                hit = seg_ray(v[k], v[k + 1], a, b)
            else:
                hit = seg_seg(v[k], v[k + 1], a, b)
            if hit is not None:
                u = v[k + 1] if hit == "overlap" else hit
                return k, u
        old = cur
    raise AssertionError("scan ran off the boundary")


def lee_visibility_polygon(polygon, z, trace=None):
    """Return the visibility polygon of z inside the simple polygon.

    polygon: list of (x, y) vertices of a simple polygon, in either order.
    z: a point strictly inside the polygon.
    trace: if a list is given, a tuple (state, i, stack copy) is appended
    before each step.
    The result is the list of vertices of the visibility polygon in
    counterclockwise order, with Fraction coordinates.
    """
    pts = [(Fraction(x), Fraction(y)) for x, y in polygon]
    z = (Fraction(z[0]), Fraction(z[1]))
    if _signed_area2(pts) < 0:
        pts.reverse()
    v = _start_sequence(pts, z)  # @line L1
    last = len(v) - 1  # @line L2
    v0 = v[0]
    stack = [v0]  # @line L3
    i, w = 1, v[1]
    if orient(z, v[0], v[1]) != CW:  # @line L4
        state = LEFT
        stack.append(v[1])
    else:
        state = SCANA

    while state != FINISH:  # @line L5
        if trace is not None:
            trace.append((STATE_NAMES[state], i, list(stack)))

        if state == LEFT:  # @line L6
            if i >= last:  # @line L7
                state = FINISH
            elif orient(z, v[i], v[i + 1]) != CW:  # @line L8
                stack.append(v[i + 1])  # still visible: push
                w = v[i + 1]
                i += 1
            elif orient(stack[-2], v[i], v[i + 1]) == CW:  # @line L9
                state = SCANA  # goes behind the top
                w = v[i + 1]
                i += 1
            else:  # @line L10
                state = RIGHT  # turns back toward z
                w = v[i]
                i += 1

        elif state == RIGHT:  # @line L11
            s_prev = stack[-1]
            o2 = orient(z, s_prev, v[i])
            mode, u, s_j = 0, None, None
            while len(stack) > 1:  # @line L12
                s_j, o1 = s_prev, o2
                stack.pop()
                s_prev = stack[-1]
                o2 = orient(z, s_prev, v[i])
                if o1 != CCW and o2 != CW:  # ray z v[i] passes between s_prev and s_j
                    mode = 1
                    break
                if v[i - 1] != s_j:
                    hit = seg_seg(s_prev, s_j, v[i - 1], v[i])
                    if hit is not None:  # the edge crosses a stack segment
                        u = v[i] if hit == "overlap" else hit
                        mode = 2
                        break
            if mode == 0:
                raise AssertionError("RIGHT found no stop")
            if mode == 2:  # @line L13
                state = SCAND  # the boundary crosses the window behind it
                w = u
            elif orient(z, v[i], v[i + 1]) == CW:  # @line L14
                stack.append(s_j)  # keep moving clockwise
                w = v[i]
                i += 1
            else:
                u = seg_ray(s_prev, s_j, z, v[i])  # @line L15
                if u == "overlap":
                    u = s_j
                if stack[-1] != u:
                    stack.append(u)
                if orient(v[i - 1], v[i], v[i + 1]) == CW:  # @line L16
                    stack.append(v[i])  # visible again
                    stack.append(v[i + 1])
                    state = LEFT
                    w = v[i + 1]
                else:  # @line L17
                    state = SCANC  # a hidden window in front
                    w = v[i]
                i += 1  # @line L18

        elif state == SCANA:  # @line L19
            k, u = _scan_edges(v, i, z, stack[-1], True)  # @line L20
            i = k + 1
            if orient(z, v[k], v[k + 1]) != CW:  # @line L21
                stack.append(u)  # comes out from behind the top
                if u != v[k + 1]:
                    stack.append(v[k + 1])
                w = v[k + 1]
                state = LEFT
            elif _between(z, stack[-1], u):  # @line L22
                w = u
                state = SCAND
            else:  # @line L23
                w = u
                state = RIGHT

        elif state == SCANB:  # @line L24
            if i == last:  # @line L25
                state = FINISH
            else:
                k, u = _scan_edges(v, i, stack[-1], v0, False)  # @line L26
                if k + 1 == last and u == v0:  # @line L27
                    stack.append(v0)  # reached v0 while hidden
                    state = FINISH
                else:  # @line L28
                    i = k + 1
                    w = u
                    state = RIGHT

        else:  # @line L29
            k, u = _scan_edges(v, i, stack[-1], w, False)  # @line L30
            i = k + 1
            if state == SCANC:  # @line L31
                w = u
                state = RIGHT
            else:
                stack.append(u)
                if u != v[k + 1]:
                    stack.append(v[k + 1])
                w = v[k + 1]
                state = LEFT

        if state == LEFT:  # @line L32
            # Did the last push cross the ray z v0? Then the boundary winds
            # past the start, and the rest is hidden behind the new top.
            top = stack.pop()
            if orient(z, v0, stack[-1]) == CW and orient(z, v0, top) == CCW:
                hit = seg_ray(stack[-1], top, z, v0)
                if hit is not None and hit != "overlap":
                    top = hit  # @line L33
                    state = SCANB
            stack.append(top)

    return _clean(stack)  # @line L34


def _clean(chain):
    """Drop repeated points and points in the middle of a straight run."""
    out = []
    for p in chain:
        if not out or out[-1] != p:
            out.append(p)
    while len(out) > 1 and out[0] == out[-1]:
        out.pop()
    changed = True
    while changed and len(out) > 3:
        changed = False
        for j in range(len(out)):
            a, b, c = out[j - 1], out[j], out[(j + 1) % len(out)]
            if a == b or orient(a, b, c) == 0 and _between(a, b, c):
                out.pop(j)
                changed = True
                break
    return out


if __name__ == "__main__":
    room = [(0, 0), (8, 0), (8, 6), (5, 6), (5, 3), (3, 3), (3, 6), (0, 6)]
    for p in lee_visibility_polygon(room, (Fraction(7), Fraction(1))):
        print(p)
