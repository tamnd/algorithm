# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-blended-oit/. The authors are listed in prov/ZP9G80.jsonl.

"""Weighted blended order-independent transparency (McGuire and Bavoil 2013).

A fragment is (c, alpha, z): a premultiplied linear RGB color c, an opacity
alpha in [0, 1] and a positive view depth z (smaller is nearer). The method
accumulates, in any order,

    A.rgb = sum c_i w_i,  A.a = sum alpha_i w_i,  R = prod (1 - alpha_i)

and returns (A.rgb / A.a) (1 - R) + C0 R. The coverage 1 - R is exact. The
color is a weighted average and is exact only in special cases.

All functions accept floats or fractions.Fraction values, so that the tests
can check the exact claims without rounding.
"""

from typing import Callable, Sequence

Color = tuple
Fragment = tuple  # (c, alpha, z)


def over_composite(fragments: Sequence[Fragment], background: Color) -> Color:
    """The exact reference: sort by depth, then c over (... over C0)."""
    result = tuple(background)
    for c, a, _ in sorted(fragments, key=lambda f: f[2], reverse=True):
        result = tuple(ci + (1 - a) * ri for ci, ri in zip(c, result))
    return result


def transmittance(fragments: Sequence[Fragment]):
    t = 1
    for _, a, _ in fragments:
        t = t * (1 - a)
    return t


def constant_weight(c: Color, a, z):
    return 1


def mcguire_blog_weight(c: Color, a: float, z: float) -> float:
    """The weight of McGuire's 2014 blog post, with c premultiplied (so the
    unpremultiplied color times alpha is c itself). Tuning, not physics: the
    constants 0.03, 200, 1e-2 and 3e3 suit a depth range of a few hundred units."""
    m = max(min(1.0, max(c)), a)
    return m * min(3e3, max(1e-2, 0.03 / (1e-5 + (z / 200.0) ** 4)))


def wboit(
    fragments: Sequence[Fragment],
    background: Color,
    weight: Callable = mcguire_blog_weight,
    eps=1e-5,
) -> Color:
    """Composite the fragments in the order given."""
    n = len(background)
    acc = [0] * n  # @line L1
    acc_a = 0
    reveal = 1
    for c, a, z in fragments:  # @line L2
        w = weight(c, a, z)  # @line L3
        for k in range(n):  # @line L4
            acc[k] = acc[k] + c[k] * w
        acc_a = acc_a + a * w
        reveal = reveal * (1 - a)  # @line L5
    denom = acc_a if acc_a > eps else eps
    avg = [x / denom for x in acc]  # @line L6
    return tuple(avg[k] * (1 - reveal) + background[k] * reveal for k in range(n))  # @line L7


def visibility_weight(fragments: Sequence[Fragment]) -> Callable:
    """The order-dependent weight that makes the method exact: the product of
    (1 - alpha) of all nearer fragments. It needs the sort that the method
    avoids, so it is not a practical weight; the tests use it to check the
    theory. The depths must be distinct."""
    table = {}
    t = 1
    for _, a, z in sorted(fragments, key=lambda f: f[2]):
        table[z] = t
        t = t * (1 - a)
    return lambda c, a, z: table[z]
