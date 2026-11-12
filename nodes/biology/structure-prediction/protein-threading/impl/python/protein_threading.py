# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/protein-threading/. The authors are listed in prov/K6H9KW.jsonl.

"""Protein threading onto one core template (the model of Lathrop and Smith).

The template has m core segments, of lengths c[0], ..., c[m-1], in order
along the chain. The core positions are numbered 0 .. C-1 over all segments,
C = sum(c). Between segment k and segment k + 1 the sequence must skip at
least gap_min[k] residues (the loop); the loops have no upper bound here.

A threading of a sequence a of length n is a list of start positions
t[0] < t[1] < ... with t[k+1] >= t[k] + c[k] + gap_min[k] and
t[m-1] + c[m-1] <= n. Residue a[t[k] + l] then sits at core position
(the l-th position of segment k). The energy is

    sum over core positions u of single(u, residue at u)
  + sum over template contacts (u, v) of pair(residue at u, residue at v).

Lower energy is better. With no contacts the problem is a dynamic program;
with contacts it is NP-hard (Lathrop 1994), and brute force is the reference.
"""

from itertools import accumulate
from typing import Callable, List, Optional, Sequence, Tuple

Single = Callable[[int, str], object]
Pair = Callable[[str, str], object]


def segment_offsets(c: Sequence[int]) -> List[int]:
    """offsets[k] is the number of the first core position of segment k."""
    return [0] + list(accumulate(c))[:-1]


def threading_energy(
    a: str, c: Sequence[int], t: Sequence[int], single: Single,
    contacts: Sequence[Tuple[int, int]] = (), pair: Optional[Pair] = None,
):
    """The energy of the threading t of the sequence a."""
    residue = {}
    for k, off in enumerate(segment_offsets(c)):
        for l in range(c[k]):
            residue[off + l] = a[t[k] + l]
    e = sum(single(u, x) for u, x in residue.items())
    for u, v in contacts:
        e += pair(residue[u], residue[v])
    return e


def all_threadings(n: int, c: Sequence[int], gap_min: Sequence[int]):
    """Every valid threading, as a tuple of start positions (explicit stack, no recursion)."""
    m = len(c)
    stack: List[Tuple[int, ...]] = [()]
    while stack:
        t = stack.pop()
        k = len(t)
        if k == m:
            yield t
            continue
        lo = 0 if k == 0 else t[-1] + c[k - 1] + gap_min[k - 1]
        rest = sum(c[k:]) + sum(gap_min[k:m - 1])  # room the later segments need
        for s in range(n - rest, lo - 1, -1):
            stack.append(t + (s,))


def brute_force(
    a: str, c: Sequence[int], gap_min: Sequence[int], single: Single,
    contacts: Sequence[Tuple[int, int]] = (), pair: Optional[Pair] = None,
):
    """(least energy, a threading that reaches it), or (None, None) if no threading fits."""
    best, arg = None, None
    for t in all_threadings(len(a), c, gap_min):
        e = threading_energy(a, c, t, single, contacts, pair)
        if best is None or e < best or (e == best and t < arg):
            best, arg = e, t
    return best, arg


def thread_singleton(a: str, c: Sequence[int], gap_min: Sequence[int], single: Single):
    """Optimal threading when the energy has only singleton terms. O(n C) time for C = sum(c).

    Returns (least energy, one optimal threading), or (None, None) if the
    segments do not fit into the sequence. Recursion-free: two nested loops
    and a backward pass over the back pointers.
    """
    n, m = len(a), len(c)
    offs = segment_offsets(c)
    if m == 0:
        return 0, ()
    if sum(c) + sum(gap_min[:m - 1]) > n:
        return None, None
    # S[k][s]: cost of segment k at start s.
    S = [[sum(single(offs[k] + l, a[s + l]) for l in range(c[k])) if s + c[k] <= n else None
          for s in range(n)] for k in range(m)]  # @line L1
    F: List[List[object]] = [[None] * n for _ in range(m)]
    B: List[List[int]] = [[-1] * n for _ in range(m)]  # B[k][s]: best start of segment k - 1
    for s in range(n):  # @line L2
        F[0][s] = S[0][s]  # @line L3
    for k in range(1, m):  # @line L4
        best, arg = None, -1  # prefix minimum of F[k-1][0 .. s - c[k-1] - gap_min[k-1]]
        for s in range(n):  # @line L5
            q = s - c[k - 1] - gap_min[k - 1]
            if q >= 0 and F[k - 1][q] is not None and (best is None or F[k - 1][q] < best):  # @line L6
                best, arg = F[k - 1][q], q
            if best is not None and S[k][s] is not None:
                F[k][s] = S[k][s] + best  # @line L7
                B[k][s] = arg
    end = min((s for s in range(n) if F[m - 1][s] is not None), key=lambda s: (F[m - 1][s], s))  # @line L8
    t = [end]
    for k in range(m - 1, 0, -1):  # @line L9
        t.append(B[k][t[-1]])
    t.reverse()
    return F[m - 1][end], tuple(t)  # @line L10
