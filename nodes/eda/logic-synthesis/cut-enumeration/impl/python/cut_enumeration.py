# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cut-enumeration/. The authors are listed in prov/B4M940.jsonl.

"""Bottom-up enumeration of all k-feasible cuts of every node of a DAG.

The network is a list `fanins`: node v has the fanin list fanins[v], and
every fanin of v is a smaller number than v, so the list order is a
topological order. A node with no fanins is a primary input. A cut is a
frozenset of node numbers.

For a primary input v the only cut is the trivial cut {v}. For an inner
node v with fanins u_1, ..., u_d, a cut is the union of one cut of each
fanin, kept when it has at most k leaves, plus the trivial cut {v}.
With pruning, a cut that holds another cut of the same node is dropped,
and the result is exactly the set of minimal k-feasible cuts.
"""

from typing import Sequence

Cut = frozenset


def merge(a: frozenset, b: frozenset, k: int):
    """The union of two cuts, or None when it has more than k leaves."""
    u = a | b
    return u if len(u) <= k else None


def drop_dominated(cuts: set) -> list:
    """Keep the cuts that contain no other cut of the set."""
    by_size = sorted(cuts, key=lambda c: (len(c), sorted(c)))
    kept: list = []
    for c in by_size:
        if not any(d <= c for d in kept):
            kept.append(c)
    return kept


def enumerate_cuts(fanins: Sequence[Sequence[int]], k: int, prune: bool = True) -> list:
    """All k-feasible cuts of every node, as a list of lists of frozensets.

    With prune=True the cuts of each node are its minimal k-feasible cuts.
    With prune=False they are all unions that the merge produces, which
    are cuts but not always minimal ones.
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    cuts: list = []
    for v, fi in enumerate(fanins):  # @line L1
        if any(u >= v for u in fi):
            raise ValueError("fanins must come before the node")
        if not fi:  # @line L2
            cuts.append([frozenset([v])])  # @line L3
            continue
        # @line L4: v is a gate
        acc = {frozenset()}  # @line L5
        for u in fi:  # @line L6
            nxt = set()
            for a in acc:
                for c in cuts[u]:
                    m = merge(a, c, k)  # @line L7
                    if m is not None:
                        nxt.add(m)
            acc = nxt
        if prune:
            mine = drop_dominated(acc)  # @line L8
        else:
            mine = sorted(acc, key=lambda c: (len(c), sorted(c)))
        cuts.append([frozenset([v])] + mine)  # @line L9
    return cuts  # @line L10


def cut_function(fanins: Sequence[Sequence[int]], ops: Sequence, v: int, cut: Sequence[int]) -> int:
    """Truth table of node v over the ordered leaves of a cut.

    ops[w] is a function from the list of fanin values to 0 or 1. The
    table is an integer of 2^|cut| bits; bit m is the value of v when
    leaf i has the value of bit (|cut| - 1 - i) of m, so the first leaf
    is the high bit.
    """
    n = len(cut)
    full = (1 << (1 << n)) - 1
    val: dict = {}
    for i, leaf in enumerate(cut):
        t = 0
        for m in range(1 << n):
            if (m >> (n - 1 - i)) & 1:
                t |= 1 << m
        val[leaf] = t

    def table(w: int) -> int:
        if w in val:
            return val[w]
        if not fanins[w]:
            raise ValueError("the set is not a cut of the node")
        ins = [table(u) for u in fanins[w]]
        t = 0
        for m in range(1 << n):
            if ops[w]([(x >> m) & 1 for x in ins]):
                t |= 1 << m
        val[w] = t & full
        return val[w]

    return table(v)
