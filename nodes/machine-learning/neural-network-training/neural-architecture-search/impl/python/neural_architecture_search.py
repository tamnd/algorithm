# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/neural-architecture-search/. The authors are listed in prov/Z1X9SG.jsonl.

"""The continuous relaxation of DARTS (Liu, Simonyan and Yang 2019).

An edge (i, j) of a cell applies one operation from a finite set O to the
feature x of node i. DARTS replaces the choice by the mixed operation

    mixed(x) = sum_o softmax(alpha)_o * o(x),

with one real architecture weight alpha_o per operation. After the search,
each edge keeps the operation with the largest weight (excluding "none"), and
each intermediate node keeps the k incoming edges whose best weight is largest.
Features are lists of floats; operations are functions from list to list.
"""

import math
from typing import Callable, Dict, List, Sequence, Tuple

Vector = List[float]


def softmax(alpha: Sequence[float]) -> Vector:
    """The mixing weights exp(alpha_o) / sum exp(alpha), with the maximum subtracted for stability."""
    m = max(alpha)
    e = [math.exp(a - m) for a in alpha]
    s = sum(e)
    return [x / s for x in e]


def mixed_op(x: Sequence[float], ops: Sequence[Callable], alpha: Sequence[float]) -> Vector:
    """sum_o softmax(alpha)_o o(x)."""
    w = softmax(alpha)
    outs = [op(list(x)) for op in ops]
    return [sum(wo * out[t] for wo, out in zip(w, outs)) for t in range(len(outs[0]))]


def mixed_op_alpha_grad(x: Sequence[float], ops: Sequence[Callable], alpha: Sequence[float],
                        upstream: Sequence[float]) -> Vector:
    """The gradient of upstream . mixed(x) with respect to alpha.

    d mixed / d alpha_o = w_o (o(x) - mixed(x)), so the gradient is
    w_o * upstream . (o(x) - mixed(x)).
    """
    w = softmax(alpha)
    outs = [op(list(x)) for op in ops]
    mix = [sum(wo * out[t] for wo, out in zip(w, outs)) for t in range(len(outs[0]))]
    return [wo * sum(u * (a - b) for u, a, b in zip(upstream, out, mix)) for wo, out in zip(w, outs)]


def discretize_edge(alpha: Sequence[float], names: Sequence[str], skip: str = "none") -> Tuple[str, float]:
    """The operation with the largest mixing weight on one edge, ignoring `skip`, and its weight."""
    w = softmax(alpha)
    best = max((i for i in range(len(names)) if names[i] != skip), key=lambda i: (w[i], -i))
    return names[best], w[best]


def discretize_cell(alphas: Dict[Tuple[int, int], Sequence[float]], names: Sequence[str], k: int = 2,
                    skip: str = "none") -> Dict[int, List[Tuple[int, str]]]:
    """For each node j, keep the k incoming edges (i, j) with the largest best weight, as in DARTS."""
    by_node: Dict[int, List[Tuple[float, int, str]]] = {}
    for (i, j), alpha in alphas.items():
        op, weight = discretize_edge(alpha, names, skip)
        by_node.setdefault(j, []).append((weight, i, op))
    out = {}
    for j, edges in by_node.items():
        edges.sort(key=lambda t: (-t[0], t[1]))
        out[j] = sorted((i, op) for _, i, op in edges[:k])
    return out
