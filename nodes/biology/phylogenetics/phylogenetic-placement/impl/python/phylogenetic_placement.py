# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phylogenetic-placement/. The authors are listed in prov/YT5XE3.jsonl.

"""Maximum likelihood placement of one query sequence on a fixed reference tree.

The model:
- a fixed unrooted binary reference tree on n taxa 0 .. n - 1 with fixed branch lengths,
- aligned DNA sequences of length m for the taxa and for the query,
- the Jukes-Cantor (JC69) model with stationary distribution (1/4, 1/4, 1/4, 1/4).

The tree is an adjacency map: leaves have degree 1, other vertices degree 3. Branch lengths are
a map from frozenset({u, v}) to a length. To place the query on edge {u, v} of length t, cut
the edge at distance a from u, join a new vertex there to a new leaf q by a pendant edge of
length p, and compute the likelihood of the tree with n + 1 taxa. The placement of an edge is
the best (a, p) on a finite grid, and the likelihood weight ratio of an edge is its best
likelihood divided by the sum over all edges.

The fast method precomputes, for each directed edge (u, v), the partial likelihood vector of
the part of the tree on the v side, as in pplacer and EPA. Each candidate (a, p) then costs
O(m) instead of a new O(n m) pruning pass.
"""

import math
from typing import Dict, FrozenSet, List, Sequence, Set, Tuple

Tree = Dict[int, Set[int]]
Lengths = Dict[FrozenSet[int], float]
Vec = List[float]
STATES = "ACGT"


def jc_apply(t: float, vec: Vec) -> Vec:
    """Return P(t) vec for the JC69 transition matrix P(t)."""
    e = math.exp(-4.0 * t / 3.0)
    same, diff = 0.25 + 0.75 * e, 0.25 - 0.25 * e
    s = sum(vec)
    return [diff * s + (same - diff) * x for x in vec]


def leaf_vec(c: str) -> Vec:
    return [1.0 if c == x else 0.0 for x in STATES]


def directed_partials(tree: Tree, lengths: Lengths, seqs: Sequence[str]) -> Dict[Tuple[int, int], List[Vec]]:
    """For each directed edge (u, v), the per-site partial likelihood of the v side, before the edge.

    The value at (u, v) is the vector over states of v of the probability of the leaf states on
    the v side of the edge. Each directed edge is computed once from its two children edges, in an
    order where children come first, so the total cost is O(n m) for DNA.
    """
    m = len(seqs[0])
    n = len(seqs)
    done: Dict[Tuple[int, int], List[Vec]] = {}
    # Order the directed edges so that (v, w) comes before (u, v): a post-order from each root edge.
    order: List[Tuple[int, int]] = []
    seen = set()
    for start in sorted((u, v) for u in tree for v in tree[u]):
        if start in seen:
            continue
        stack = [(start, False)]
        while stack:
            (u, v), expanded = stack.pop()
            if (u, v) in seen:
                continue
            if expanded or v < n:
                seen.add((u, v))
                order.append((u, v))
                continue
            stack.append(((u, v), True))
            for w in tree[v]:
                if w != u and (v, w) not in seen:
                    stack.append(((v, w), False))
    for u, v in order:
        if v < n:
            done[(u, v)] = [leaf_vec(seqs[v][j]) for j in range(m)]
            continue
        kids = [w for w in tree[v] if w != u]
        cols = []
        for j in range(m):
            vec = [1.0] * 4
            for w in kids:
                pw = jc_apply(lengths[frozenset((v, w))], done[(v, w)][j])
                vec = [x * y for x, y in zip(vec, pw)]
            cols.append(vec)
        done[(u, v)] = cols
    return done


def edge_log_likelihood(down_v: List[Vec], down_u: List[Vec], t: float, a: float, p: float, query: str) -> float:
    """Log likelihood with the query attached at distance a from u on an edge of length t.

    down_v is the partial of the v side (directed edge (u, v)), down_u that of the u side.
    The likelihood at the new vertex x is sum_x pi_x [P(t - a) down_v]_x [P(a) down_u]_x [P(p) e_q]_x.
    """
    total = 0.0
    for j, c in enumerate(query):
        lv = jc_apply(t - a, down_v[j])
        lu = jc_apply(a, down_u[j])
        lq = jc_apply(p, leaf_vec(c))
        total += math.log(0.25 * sum(x * y * z for x, y, z in zip(lv, lu, lq)))
    return total


def edges_of(tree: Tree) -> List[Tuple[int, int]]:
    return sorted((u, v) for u in tree for v in tree[u] if u < v)


def place(tree: Tree, lengths: Lengths, seqs: Sequence[str], query: str,
          fractions: Sequence[float], pendants: Sequence[float]) -> Dict[Tuple[int, int], Tuple[float, float, float]]:
    """Best (log likelihood, a, p) on each edge, with a = f t for f in fractions and p in pendants.

    Cost: O(n m) for the partials and O(n m g) for the g = |fractions| |pendants| candidates
    on each of the 2n - 3 edges.
    """
    down = directed_partials(tree, lengths, seqs)  # @line L1
    best = {}
    for u, v in edges_of(tree):  # @line L2
        t = lengths[frozenset((u, v))]
        cand = None
        for f in fractions:  # @line L3
            for p in pendants:
                ll = edge_log_likelihood(down[(u, v)], down[(v, u)], t, f * t, p, query)  # @line L4
                if cand is None or ll > cand[0]:  # @line L5
                    cand = (ll, f * t, p)
        best[(u, v)] = cand  # @line L6
    return best  # @line L7


def likelihood_weight_ratios(best: Dict[Tuple[int, int], Tuple[float, float, float]]) -> Dict[Tuple[int, int], float]:
    """Normalize the best likelihood of each edge so that the ratios sum to 1."""
    top = max(x[0] for x in best.values())
    w = {e: math.exp(x[0] - top) for e, x in best.items()}
    z = sum(w.values())
    return {e: x / z for e, x in w.items()}
