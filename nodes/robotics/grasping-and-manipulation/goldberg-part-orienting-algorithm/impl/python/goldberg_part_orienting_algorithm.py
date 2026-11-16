# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/goldberg-part-orienting-algorithm/. The authors are listed in prov/8BG41W.jsonl.

"""Goldberg's part orienting algorithm for a parallel-jaw gripper.

Model (Goldberg 1993, Section 3): a rigid planar part, a gripper with two
parallel jaws that close at the same time, no friction between the part and
the jaws, and quasi-static motion. Only the convex hull of the part matters.

Angles are floats in radians. The part orientation theta is measured relative
to the gripper. The diameter d(theta) is the distance between the jaws when
both touch the part. A squeeze turns the part to the local minimum of d that
lies between the two local maxima around theta. Steps of the squeeze function
are closed on the left and open on the right, as in the paper. A squeeze with
the gripper at the world angle alpha maps the world orientation phi of the
part to alpha + s(phi - alpha).

All comparisons of angles use the tolerance TOL. The test file states the
tolerances of its checks.
"""

import math

TOL = 1e-9


def convex_hull(points):
    """Andrew's monotone chain. Returns the hull in counterclockwise order."""
    pts = sorted(set((float(x), float(y)) for x, y in points))
    if len(pts) < 3:
        raise ValueError("the part needs at least three points not on a line")

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    hull = lower[:-1] + upper[:-1]
    if len(hull) < 3:
        raise ValueError("the part needs at least three points not on a line")
    return hull


def _u(theta):
    # The closing direction of the jaws in the frame of the part, when the
    # part is turned by theta relative to the gripper.
    return (math.sin(theta), math.cos(theta))


def diameter(hull, theta):
    """The distance between the jaws for the relative orientation theta."""
    ux, uy = _u(theta)
    proj = [x * ux + y * uy for x, y in hull]
    return max(proj) - min(proj)


def squeeze_function(hull):
    """Return (maxima, minima) on one period pi of the diameter function.

    maxima[j] < minima[j] < maxima[j + 1], with maxima[r] = maxima[0] + pi.
    The step j of the squeeze function is [maxima[j], maxima[j + 1]) and it
    maps to minima[j].
    """
    h = len(hull)
    # Breakpoints: a jaw is flush with an edge, so u is normal to the edge.
    bps = []
    for i in range(h):
        ex = hull[(i + 1) % h][0] - hull[i][0]
        ey = hull[(i + 1) % h][1] - hull[i][1]
        bps.append(math.atan2(-ey, ex) % math.pi)
    bps.sort()
    uniq = []
    for b in bps:
        if not uniq or b - uniq[-1] > TOL:
            uniq.append(b)
    if len(uniq) > 1 and uniq[0] + math.pi - uniq[-1] <= TOL:
        uniq.pop()
    K = len(uniq)
    # On piece t, d(theta) = <w_t, u(theta)> for one antipodal pair.
    pieces = []
    for t in range(K):
        lo = uniq[t]
        hi = uniq[t + 1] if t + 1 < K else uniq[0] + math.pi
        mid = 0.5 * (lo + hi)
        ux, uy = _u(mid)
        proj = [x * ux + y * uy for x, y in hull]
        i = max(range(h), key=lambda k: proj[k])
        j = min(range(h), key=lambda k: proj[k])
        w = (hull[i][0] - hull[j][0], hull[i][1] - hull[j][1])
        pieces.append((lo, hi, w))

    def slope(w, theta):
        return w[0] * math.cos(theta) - w[1] * math.sin(theta)

    maxima, minima = [], []
    for t, (lo, hi, w) in enumerate(pieces):
        # A local minimum sits at a breakpoint where d turns from down to up.
        # The left piece of piece 0 is the last piece, which ends at lo + pi.
        hl, wl = pieces[t - 1][1], pieces[t - 1][2]
        if slope(wl, hl) < 0 < slope(w, lo):
            minima.append(lo)
        # A local maximum is inside a piece, where the slope is zero.
        top = math.atan2(w[0], w[1])
        top = lo + ((top - lo) % math.pi)
        if lo + TOL < top < hi - TOL:
            maxima.append(top % math.pi)
    maxima.sort()
    minima.sort()
    if len(maxima) != len(minima) or not maxima:
        raise ValueError("degenerate diameter function")
    # Pair each step [e_j, e_(j+1)) with the minimum inside it.
    r = len(maxima)
    e = maxima + [maxima[0] + math.pi]
    m = []
    for j in range(r):
        inside = [x for x in minima + [y + math.pi for y in minima]
                  if e[j] < x < e[j + 1]]
        if len(inside) != 1:
            raise ValueError("degenerate diameter function")
        m.append(inside[0])
    return e[:r], m


def smallest_period(e, m):
    """Return (T, c): the smallest period T of s and c steps per period."""
    r = len(e)
    e2 = e + [x + math.pi for x in e]
    width = [e2[j + 1] - e2[j] for j in range(r)]
    offset = [m[j] - e[j] for j in range(r)]
    for c in range(1, r + 1):
        if r % c:
            continue
        if all(abs(width[j] - width[(j + c) % r]) < TOL and
               abs(offset[j] - offset[(j + c) % r]) < TOL for j in range(r)):
            return math.pi * c / r, c
    return math.pi, r


class Squeeze:
    """The squeeze function of a part, with its smallest period T."""

    def __init__(self, points):
        self.hull = convex_hull(points)
        e, m = squeeze_function(self.hull)
        self.T, self.r = smallest_period(e, m)
        self.e0 = e[:self.r]  # maxima in one period
        self.m0 = m[:self.r]  # minima in one period

    def e(self, j):
        """Maximum j, for any integer j (unrolled over the periods)."""
        q, k = divmod(j, self.r)
        return self.e0[k] + q * self.T

    def m(self, j):
        q, k = divmod(j, self.r)
        return self.m0[k] + q * self.T

    def step_of(self, theta):
        """The unrolled index j with e(j) <= theta < e(j + 1)."""
        q = math.floor((theta - self.e0[0]) / self.T)
        j = q * self.r
        x = theta - q * self.T
        k = 0
        while k + 1 < self.r and self.e0[k + 1] <= x:
            k += 1
        return j + k

    def s(self, theta):
        return self.m(self.step_of(theta))

    def act(self, phi, alpha):
        """World orientation after a squeeze with the gripper at alpha."""
        return alpha + self.s(phi - alpha)


def plan(points):
    """Goldberg's algorithm.

    Returns (alphas, final, S, levels). alphas are the gripper angles of the
    shortest plan, final is the world orientation of the part after the plan
    (modulo S.T), and levels is the list of s-intervals (p, q) with
    Theta_i = [e(p), e(q + 1)) and s-image [m(p), m(q)].
    """
    S = Squeeze(points)  # @line L1 @line L2 @line L3
    r, T = S.r, S.T
    j = max(range(r), key=lambda k: S.e(k + 1) - S.e(k))
    levels = [(j, j)]  # @line L4
    length = S.e(j + 1) - S.e(j)
    while length < T - TOL:  # @line L5
        best, arg = -1.0, None
        q = 0
        for p in range(r):  # @line L6
            # Two pointers: the largest q with m(q) - m(p) < length.
            q = max(q, p)
            while q + 1 < p + r and S.m(q + 1) - S.m(p) < length - TOL:
                q += 1
            w = S.e(q + 1) - S.e(p)
            if w > best + TOL:
                best, arg = w, (p, q)
        if best <= length + TOL:
            raise ArithmeticError("no progress; the tolerance hides a tie")
        levels.append(arg)  # @line L7
        length = best
    k = len(levels)  # @line L8
    alphas = [0.0]  # @line L8
    for t in range(2, k + 1):  # @line L9
        p, q = levels[k - t + 1]  # @line L10
        a, b = S.e(levels[k - t][0]), S.e(levels[k - t][1] + 1)  # @line L10
        slack = (b - a) - (S.m(q) - S.m(p))
        alphas.append(alphas[-1] + S.m(p) - a - slack / 2.0)  # @line L11
    final = alphas[-1] + S.m(levels[0][0])
    return alphas, final, S, levels  # @line L12


def run_plan(S, alphas, phi):
    """Execute a plan from the world orientation phi."""
    for alpha in alphas:
        phi = S.act(phi, alpha)
    return phi


def same_mod(x, y, T, tol=1e-7):
    d = (x - y) % T
    return min(d, T - d) < tol
