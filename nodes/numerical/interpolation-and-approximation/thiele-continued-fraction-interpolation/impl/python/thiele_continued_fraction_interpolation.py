# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thiele-continued-fraction-interpolation/. The authors are listed in prov/D0H64Z.jsonl.

"""Thiele continued-fraction (rational) interpolation by inverse differences.

R(t) = b0 + (t - x0) / (b1 + (t - x1) / (b2 + ... + (t - x[m-2]) / b[m-1]))

Inverse differences may be infinite; INF stands for the point at infinity
of the projective line and is handled exactly. Nodes are reordered so that
every b_k is finite, and the fraction stops early once it already matches
all remaining data. Works with floats or with fractions.Fraction.
"""

INF = None  # the point at infinity in projective arithmetic


def thiele_fit(x, y):
    """Return a model (nodes, coefficients) for thiele_eval.

    Raises ValueError for empty input, unequal lengths or repeated nodes.
    """
    n = len(x)
    if n == 0 or n != len(y):
        raise ValueError("need equally many nodes and values, at least one")
    if len(set(x)) != n:
        raise ValueError("repeated nodes")
    xs = list(x)
    a = list(y)                                                  # @line L1
    m = n
    for k in range(1, n):
        px, pa = xs[k - 1], a[k - 1]          # pivot, always finite
        for i in range(k, n):
            if a[i] is INF:
                a[i] = 0 * pa                 # (x_i - px) / (inf - pa) = 0
            elif a[i] == pa:
                a[i] = INF                    # R_(k-1) already matches x_i
            else:
                a[i] = (xs[i] - px) / (a[i] - pa)                # @line L2
        j = next((i for i in range(k, n) if a[i] is not INF), None)
        if j is None:
            m = k                             # all remaining points matched
            break
        xs[k], xs[j] = xs[j], xs[k]
        a[k], a[j] = a[j], a[k]
    return (xs[:m], a[:m])                    # @line L3


def thiele_eval(model, t):
    """Evaluate the continued fraction at t as A(t) / B(t).

    A and B come from the three-term (Wallis) recurrence, so a node t
    needs no special case. Returns INF (None) at a pole, and raises
    ValueError when A(t) = B(t) = 0, which at a node means that the
    node is unattainable.
    """
    xs, b = model
    a_prev, a_cur = 1, b[0]
    b_prev, b_cur = 0, 1
    for k in range(1, len(b)):
        d = t - xs[k - 1]
        a_prev, a_cur = a_cur, b[k] * a_cur + d * a_prev        # @line L4
        b_prev, b_cur = b_cur, b[k] * b_cur + d * b_prev
        big = max(abs(a_cur), abs(b_cur))
        if isinstance(big, float) and big > 1e150:   # rescale floats only
            a_prev, a_cur = a_prev / big, a_cur / big
            b_prev, b_cur = b_prev / big, b_cur / big
    if b_cur == 0:
        if a_cur == 0:
            raise ValueError("0/0 at t: unattainable point or degenerate data")
        return INF
    return a_cur / b_cur                                         # @line L5


def thiele_type(model):
    """Return the type (numerator degree bound, denominator degree bound)."""
    m = len(model[1]) - 1
    return ((m + 1) // 2, m // 2)
