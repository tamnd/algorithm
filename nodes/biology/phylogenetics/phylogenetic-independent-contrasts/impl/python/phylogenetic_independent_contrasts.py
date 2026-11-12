# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phylogenetic-independent-contrasts/. The authors are listed in prov/VXSG4E.jsonl.
"""Felsenstein's phylogenetically independent contrasts.

A rooted binary tree is a parent list: parent[v] is the parent of node v and
parent[root] = -1; length[v] > 0 is the length of the edge above v. Tips are
the nodes with no children, and x[v] is the trait value of tip v. The
functions work with floats or with Fractions (exact, apart from the square
root of the standardization).
"""

import math


def children_of(parent: list) -> list:
    kids = [[] for _ in parent]
    for v, p in enumerate(parent):
        if p >= 0:
            kids[p].append(v)
    return kids


def postorder(parent: list) -> list:
    kids = children_of(parent)
    order, stack = [], [parent.index(-1)]
    while stack:
        v = stack.pop()
        order.append(v)
        stack.extend(kids[v])
    order.reverse()
    return order


def contrasts(parent: list, length: list, x: dict):
    """Return (raw, root_value, root_var).

    raw is a list of (node, c, var) with c = x_i - x_j for the two children of
    node and var = v_i + v_j, the variance of c per unit of the BM rate.
    root_value is the estimate at the root, and root_var its variance per unit
    of rate. The n - 1 contrasts are independent under Brownian motion.
    """
    kids = children_of(parent)
    value, v = dict(x), list(length)
    raw = []
    for k in postorder(parent):  # @line L1
        if not kids[k]:
            continue
        i, j = kids[k]
        raw.append((k, value[i] - value[j], v[i] + v[j]))  # @line L2
        value[k] = (value[i] / v[i] + value[j] / v[j]) / (1 / v[i] + 1 / v[j])  # @line L4
        extra = v[i] * v[j] / (v[i] + v[j])
        if parent[k] >= 0:
            v[k] = v[k] + extra  # @line L5
        else:
            root_var = extra
    root = parent.index(-1)
    return raw, value[root], root_var  # @line L6


def standardized(raw: list) -> list:
    """Each contrast divided by its standard deviation."""
    return [c / math.sqrt(var) for _, c, var in raw]  # @line L3


def contrast_weights(parent: list, length: list, tips: list) -> tuple:
    """Each contrast and the root estimate as weights on the tip values.

    Returns (rows, root_row, variances, root_var): rows[m][t] is the weight of
    tip tips[t] in contrast m. Exact when the lengths are Fractions.
    """
    unit = {t: [1 if s == t else 0 for s in tips] for t in tips}
    kids = children_of(parent)
    vec, v = dict(unit), list(length)
    rows, variances, root_var = [], [], None
    for k in postorder(parent):
        if not kids[k]:
            continue
        i, j = kids[k]
        rows.append([a - b for a, b in zip(vec[i], vec[j])])
        variances.append(v[i] + v[j])
        wi, wj = 1 / v[i], 1 / v[j]
        vec[k] = [(a * wi + b * wj) / (wi + wj) for a, b in zip(vec[i], vec[j])]
        extra = v[i] * v[j] / (v[i] + v[j])
        if parent[k] >= 0:
            v[k] += extra
        else:
            root_var = extra
    return rows, vec[parent.index(-1)], variances, root_var


def regression_through_origin(cx: list, cy: list):
    """The slope of y on x from paired contrasts, fitted through the origin."""
    return sum(a * b for a, b in zip(cx, cy)) / sum(a * a for a in cx)
