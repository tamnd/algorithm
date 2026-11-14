# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knot-removal-fairing/. The authors are listed in prov/GM71P6.jsonl.

"""Fairing a planar cubic B-spline curve by knot removal and reinsertion.

This is the method of Farin, Rein, Sapidis and Worsey (1987) and Farin and
Sapidis (1989). At each step it finds the inner knot where the derivative of
the curvature jumps most, removes that knot as if the curve were C3 there,
and inserts it again. The knot vector does not change, and exactly one
control point moves. After the step the curve is C3 at that knot, so the
curvature derivative is continuous there. A global tolerance bounds how far
any control point may move from its first position, which bounds how far
the curve moves.

The curve is a clamped cubic B-spline in the plane with simple inner knots.
With int or Fraction input every step is exact.
"""

from fractions import Fraction

from si3spline import check_curve, curve_point, derivative_curve, lincomb, sub

P = 3


def _check(knots, ctrl):
    check_curve(knots, P, ctrl)
    if len(ctrl[0]) != 2:
        raise ValueError("the curve must be planar")
    if knots[:P + 1] != [knots[0]] * (P + 1) or knots[-P - 1:] != [knots[-1]] * (P + 1):
        raise ValueError("the knot vector must be clamped")
    inner = knots[P + 1:len(ctrl)]
    if len(set(inner)) != len(inner) or knots[0] in inner or knots[-1] in inner:
        raise ValueError("the inner knots must be simple")


def _derivatives(knots, ctrl):
    """The first, second and third derivative curves."""
    d1 = derivative_curve(knots, P, ctrl)
    d2 = derivative_curve(*d1)
    d3 = derivative_curve(*d2)
    return d1, d2, d3


def _cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def kappa_jump(knots, ctrl, r):
    """The square of the jump of the curvature derivative at the inner knot knots[r].

    The curve is C2 at a simple knot, so only the third derivative jumps, by
    D, and the curvature derivative jumps by (c' x D) / |c'|^3. The square is
    returned, which is exact. None if c' = 0 there.
    """
    t = knots[r]
    d1, _, d3 = _derivatives(knots, ctrl)
    v = curve_point(*d1, t)
    s = _dot(v, v)
    if s == 0:
        return None
    left = curve_point(*d3, (knots[r - 1] + t) / Fraction(2))
    right = curve_point(*d3, (t + knots[r + 1]) / Fraction(2))
    j = _cross(v, sub(right, left))
    return Fraction(j * j) / (s * s * s)


def remove_and_reinsert(knots, ctrl, r):
    """Remove the inner knot knots[r] and insert it again; return the new control points.

    Boehm insertion of t into the curve without t, of span k = r - 1, keeps
    the points up to k - 3 and from k + 1 on, and makes the points k - 2, k - 1
    and k from the old points k - 3, ..., k. Solving its first equation from
    the left and its last equation from the right gives the two inner points
    of the curve without t; reinsertion then changes only point k - 1.
    """
    t = knots[r]
    k = r - 1
    K = knots[:r] + knots[r + 1:]                              # the knot vector without t

    def alpha(i):
        return (t - K[i]) / Fraction(K[i + P] - K[i])

    a0, a1, a2 = alpha(k - 2), alpha(k - 1), alpha(k)
    left = tuple((x - (1 - a0) * y) / a0 for x, y in zip(ctrl[k - 2], ctrl[k - 3]))
    right = tuple((x - a2 * y) / (1 - a2) for x, y in zip(ctrl[k], ctrl[k + 1]))
    new = list(ctrl)
    new[k - 1] = lincomb([1 - a1, a1], [left, right])
    return new


def curvature_sign_changes(knots, ctrl):
    """The exact number of sign changes of the curvature along the curve.

    On each knot interval of a cubic, f = x'y'' - y'x'' is a polynomial of
    degree at most 2 (the cubic terms cancel). Its signs at the ends of each
    interval and at its vertex, if the vertex is inside, give every sign
    change, because a quadratic is monotone on each side of its vertex.
    """
    _check(knots, ctrl)
    d1, d2, _ = _derivatives(knots, ctrl)

    def f(t):
        return _cross(curve_point(*d1, t), curve_point(*d2, t))

    signs = []
    breaks = sorted(set(knots))
    for a, b in zip(breaks, breaks[1:]):
        f0, fm, f1 = f(a), f((a + b) / Fraction(2)), f(b)
        A = 2 * f0 + 2 * f1 - 4 * fm                            # f = A s^2 + B s + f0 on s in [0, 1]
        B = f1 - f0 - A
        vals = [f0]
        if A != 0 and 0 < -B / Fraction(2 * A) < 1:
            vals.append(f0 - Fraction(B * B) / (4 * A))
        vals.append(f1)
        signs += [1 if x > 0 else -1 for x in vals if x != 0]
    return sum(1 for x, y in zip(signs, signs[1:]) if x != y)


def max_move_squared(ctrl0, ctrl1):
    """The largest squared distance between matching control points.

    On one knot vector, the curves differ by sum N_i(t) (ctrl1[i] - ctrl0[i]),
    and the N_i are non negative with sum 1, so every point of the curve moves
    by at most the square root of this number.
    """
    return max(_dot(sub(a, b), sub(a, b)) for a, b in zip(ctrl0, ctrl1))


def jumps(knots, ctrl):
    """The pairs (squared jump, r) for every inner knot index r where c' is not zero."""
    out = []
    for r in range(P + 1, len(ctrl)):
        J = kappa_jump(knots, ctrl, r)
        if J is not None:
            out.append((J, r))
    return out


def fairness(knots, ctrl):
    """The fairness measure: the sum of the squared jumps of the curvature derivative."""
    return sum((J for J, _ in jumps(knots, ctrl)), Fraction(0))


def fair_by_knot_removal(knots, ctrl, tol, rounds=50):
    """Fair the curve; return (new control points, the list of the faired knot indices).

    Each round tries the knots in the order of decreasing jump of the
    curvature derivative, and fairs the first one whose remove-and-reinsert
    step keeps every control point within tol of its first position and
    lowers the fairness measure. The loop stops when no knot qualifies or
    after the given number of rounds.
    """
    _check(knots, ctrl)
    tol2 = Fraction(tol) ** 2
    start = list(ctrl)                                           # @line L1
    E = fairness(knots, ctrl)                                    # @line L1
    done = []
    for _ in range(rounds):                                      # @line L2
        order = sorted(jumps(knots, ctrl), key=lambda x: (-x[0], x[1]))  # @line L3
        for J, r in order:                                       # @line L4
            if J == 0:
                continue
            new = remove_and_reinsert(knots, ctrl, r)            # @line L5
            if max_move_squared(start, new) > tol2:              # @line L6
                continue
            E_new = fairness(knots, new)                         # @line L6
            if E_new < E:
                ctrl, E = new, E_new                             # @line L7
                done.append(r)
                break
        else:
            break                                                # @line L8
    return ctrl, done                                            # @line L9
