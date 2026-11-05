# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reingold-tilford-layout/. The authors are listed in prov/NB9NJR.jsonl.
"""Reingold-Tilford layout of an ordered rooted tree.

The tree has the vertices 0..n-1 and is given by children lists, in
order from left to right. It is rooted and not weighted. Each vertex gets
y = its depth and an x coordinate (a Fraction), so that two neighbours on
the same level are at least `sep` apart and each parent is centred over
its first and last child. Contours are kept as lists, deepest level first,
with a shift, so each merge costs the height of the lower of the two parts.
"""

from fractions import Fraction


def layout(children, root=0, sep=1):
    n = len(children)
    order = []
    stack = [root]
    while stack:  # preorder without recursion
        v = stack.pop()
        order.append(v)
        stack.extend(reversed(children[v]))
    rel = [Fraction(0)] * n  # x of v minus x of its parent
    left = [None] * n  # left contour: [list, shift]; level i is list[-1-i] + shift
    right = [None] * n
    for v in reversed(order):  # @line L1
        kids = children[v]
        if not kids:  # @line L2
            left[v] = [[Fraction(0)], Fraction(0)]
            right[v] = [[Fraction(0)], Fraction(0)]
            continue
        c1 = kids[0]
        fl, fr = left[c1], right[c1]  # @line L3
        off = {c1: Fraction(0)}
        for c in kids[1:]:  # @line L4
            cl, cr = left[c], right[c]
            hf, hc = len(fr[0]), len(cl[0])
            d = None
            for i in range(min(hf, hc)):  # @line L5
                gap = fr[0][hf - 1 - i] + fr[1] - (cl[0][hc - 1 - i] + cl[1])
                if d is None or gap > d:
                    d = gap
            d += sep  # @line L6
            off[c] = d
            # @line L7: merge the left contours, then the right contours
            if hc > len(fl[0]):
                hl = len(fl[0])
                for i in range(hl):
                    cl[0][hc - 1 - i] = fl[0][hl - 1 - i] + fl[1] - (cl[1] + d)
                fl = [cl[0], cl[1] + d]
            if hf > hc:
                for i in range(hc):
                    fr[0][hf - 1 - i] = cr[0][hc - 1 - i] + cr[1] + d - fr[1]
            else:
                fr = [cr[0], cr[1] + d]
        m = off[kids[-1]] / 2  # @line L8
        for c in kids:  # @line L9
            rel[c] = off[c] - m
        fl[1] -= m  # @line L10
        fl[0].append(-fl[1])
        fr[1] -= m
        fr[0].append(-fr[1])
        left[v], right[v] = fl, fr
    x = [Fraction(0)] * n
    y = [0] * n
    for v in order:  # @line L11
        for c in children[v]:
            x[c] = x[v] + rel[c]
            y[c] = y[v] + 1  # @line L12
    return x, y  # @line L13


def children_from_parents(parent):
    """Children lists in increasing order, and the root, from a parent array."""
    ch = [[] for _ in parent]
    root = 0
    for v, p in enumerate(parent):
        if p < 0:
            root = v
        else:
            ch[p].append(v)
    return ch, root
