# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fixed-parameter-mec/. The authors are listed in prov/W2Z7FH.jsonl.
"""The dynamic program of WhatsHap for weighted minimum error correction (wMEC).

A fragment is a dict {column: allele}, with columns 0-based (0 to m - 1) and
alleles 0 or 1. A column that is not in the dict is a hole. The weights have the
same shape, {column: weight}; with no weights every entry costs 1 to flip.

A fragment is active in every column from its leftmost to its rightmost
non-hole column, so the internal segment of a paired read counts as covered.
The coverage c of a column is the number of active fragments. The table of
column j has one entry for each bipartition (R, S) of the active fragments,
encoded as a bit mask: bit t is 1 when the t-th active fragment is in S.

The cost is O(2^c m) time for maximum coverage c and m columns, after an
O(n + total number of entries) pass to find the active fragments. Patterson
et al. (2015) store only half of the masks, because (R, S) and (S, R) have the
same cost; this code keeps all of them, which costs a factor 2.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

Fragment = Dict[int, int]


def _subset_sums(vals: Sequence[int]) -> List[int]:
    """sums[mask] = the sum of vals[t] over the bits t of mask, in O(2^len) time."""
    sums = [0] * (1 << len(vals))
    for mask in range(1, len(sums)):
        low = mask & -mask
        sums[mask] = sums[mask ^ low] + vals[low.bit_length() - 1]
    return sums


def _bit_map(src: Sequence[int], dst: Sequence[int]) -> List[int]:
    """proj[mask] maps a mask over the list src to a mask over the list dst.

    A bit of an item of src that is not in dst is dropped.
    """
    where = {f: t for t, f in enumerate(dst)}
    bit = [1 << where[f] if f in where else 0 for f in src]
    proj = [0] * (1 << len(src))
    for mask in range(1, len(proj)):
        low = mask & -mask
        proj[mask] = proj[mask ^ low] | bit[low.bit_length() - 1]
    return proj


def active_sets(fragments: Sequence[Fragment], m: int) -> List[List[int]]:
    """A[j] = the indices of the fragments active at column j, in increasing order."""
    A: List[List[int]] = [[] for _ in range(m)]
    for i, f in enumerate(fragments):  # @line L1
        if f:
            for j in range(min(f), max(f) + 1):
                A[j].append(i)
    return A


def column_costs(fragments: Sequence[Fragment], weights, active: Sequence[int], j: int,
                 all_het: bool) -> Tuple[List[int], List[int], List[int]]:
    """Return delta, w0 and w1 for every mask over the active fragments of column j.

    w0[mask] is the cost to set column j of every fragment in mask to 0, and
    w1[mask] the cost to set it to 1. delta[mask] is the least cost to make
    column j conflict free when mask is S and the other active fragments are R.
    """
    to0, to1 = [], []
    for i in active:
        a = fragments[i].get(j)
        wt = 0 if a is None else (1 if weights is None else weights[i][j])
        to0.append(wt if a == 1 else 0)
        to1.append(wt if a == 0 else 0)
    w0, w1 = _subset_sums(to0), _subset_sums(to1)
    full = (1 << len(active)) - 1
    delta = []
    for s in range(full + 1):  # @line L4
        r = full ^ s
        if all_het:  # @line L5
            delta.append(min(w0[r] + w1[s], w1[r] + w0[s]))
        else:
            delta.append(min(w0[r], w1[r]) + min(w0[s], w1[s]))
    return delta, w0, w1


def whatshap_mec(fragments: Sequence[Fragment], m: int, weights: Optional[Sequence[Dict[int, int]]] = None,
                 all_het: bool = False) -> Tuple[int, List[int], List[int], List[int]]:
    """Solve wMEC exactly.

    Returns (cost, h1, h2, side): the least total weight of flips, two haplotypes
    as lists of 0 and 1, and side[i] = 0 if fragment i is in the part of h1 and 1
    if it is in the part of h2. A column with no active fragment gets 0 in both
    haplotypes (0 and 1 under all_het). A fragment with no entries gets side 0.
    """
    if m == 0:
        return 0, [], [], [0] * len(fragments)
    A = active_sets(fragments, m)
    back: List[List[int]] = []  # back[j][mask over A[j] & A[j+1]] = best mask over A[j]
    prev_bar: Optional[List[int]] = None
    for j in range(m):  # @line L2
        cur = A[j]  # @line L3
        delta, _, _ = column_costs(fragments, weights, cur, j, all_het)
        if j == 0:  # @line L6
            C = delta
        else:  # @line L7
            proj_in = _bit_map(cur, inter)
            C = [delta[s] + prev_bar[proj_in[s]] for s in range(len(delta))]
        if j + 1 < m:  # @line L8
            inter = [f for f in cur if f in set(A[j + 1])]
            proj_out = _bit_map(cur, inter)
            bar = [None] * (1 << len(inter))
            arg = [0] * (1 << len(inter))
            for s, cost in enumerate(C):
                p = proj_out[s]
                if bar[p] is None or cost < bar[p]:
                    bar[p], arg[p] = cost, s
            back.append(arg)
            prev_bar = bar
    best = min(range(len(C)), key=lambda s: (C[s], s))  # @line L9
    cost = C[best]
    masks = [0] * m
    masks[m - 1] = best
    for j in range(m - 2, -1, -1):  # @line L10
        inter = [f for f in A[j] if f in set(A[j + 1])]
        masks[j] = back[j][_bit_map(A[j + 1], inter)[masks[j + 1]]]
    side = [0] * len(fragments)
    h1, h2 = [0] * m, [0] * m
    for j in range(m):  # @line L11
        for t, i in enumerate(A[j]):
            side[i] = (masks[j] >> t) & 1
        _, w0, w1 = column_costs(fragments, weights, A[j], j, all_het)
        s = masks[j]
        r = ((1 << len(A[j])) - 1) ^ s
        if all_het:
            h1[j] = 0 if w0[r] + w1[s] <= w1[r] + w0[s] else 1
            h2[j] = 1 - h1[j]
        else:
            h1[j] = 0 if w0[r] <= w1[r] else 1
            h2[j] = 0 if w0[s] <= w1[s] else 1
    return cost, h1, h2, side  # @line L12


def flip_cost(fragment: Fragment, hap: Sequence[int], weight: Optional[Dict[int, int]] = None) -> int:
    """The weight of the entries of fragment that differ from hap."""
    return sum((1 if weight is None else weight[j]) for j, a in fragment.items() if hap[j] != a)


def mec_cost(fragments: Sequence[Fragment], h1: Sequence[int], h2: Sequence[int],
             weights: Optional[Sequence[Dict[int, int]]] = None) -> int:
    """The MEC objective of a haplotype pair: each fragment goes to the closer haplotype."""
    total = 0
    for i, f in enumerate(fragments):
        wt = None if weights is None else weights[i]
        total += min(flip_cost(f, h1, wt), flip_cost(f, h2, wt))
    return total
