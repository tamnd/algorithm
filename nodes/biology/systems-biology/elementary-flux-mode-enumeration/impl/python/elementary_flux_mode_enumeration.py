# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elementary-flux-mode-enumeration/. The authors are listed in prov/E5TT1K.jsonl.
"""Elementary flux modes by the nullspace form of the double description method.

Input: the n x m stoichiometric matrix S and a list rev of m booleans
(rev[j] is True if reaction j is reversible). Output: every elementary flux
mode, as a tuple of coprime integers, so each mode appears once up to a
positive factor. A mode e and its negative -e are two modes when both are
sign-feasible (a cycle of reversible reactions).

Steps:
1. Split each reversible reaction j into a forward copy (column S_j) and a
   backward copy (column -S_j). Every reaction of the new matrix S' is
   irreversible, so the modes of S' are the extreme rays of the pointed cone
   C = {x : S' x = 0, x >= 0}.
2. Take a kernel basis K of S' with an identity block on the free
   coordinates F. The cone {x in ker S' : x_F >= 0} has the columns of K as
   its extreme rays.
3. Add the constraints x_p >= 0 for the other coordinates p, one at a time,
   by the double description step: keep the rays with x_p >= 0, and combine
   each adjacent pair of a ray with x_p > 0 and a ray with x_p < 0 into a
   ray with x_p = 0. Two rays are adjacent if the matrix of the processed
   constraints that both satisfy with equality has rank d - 2, where
   d = dim ker S'.
4. Drop the two-cycles (forward and backward copy of one reaction) and map
   each ray back to the original reactions.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd
from typing import List, Sequence, Tuple

from sy3lp import nullspace, rank, rref


def primitive(x: Sequence[Fraction]) -> Tuple[int, ...]:
    """Scale a rational vector to coprime integers, keeping the sign."""
    den = 1
    for v in x:
        den = den * v.denominator // gcd(den, v.denominator)
    ints = [int(v * den) for v in x]
    g = 0
    for v in ints:
        g = gcd(g, abs(v))
    return tuple(v // g for v in ints) if g else tuple(ints)


def split_reversible(S, rev):
    """Return S' and back, where back[k] = (j, +1 or -1) for column k."""
    cols = list(range(len(rev)))
    back = [(j, 1) for j in cols]
    for j in cols:
        if rev[j]:
            back.append((j, -1))
    Sp = [[row[j] * s for j, s in back] for row in S]
    return Sp, back


def efm_enumeration(S: Sequence[Sequence[int]], rev: Sequence[bool]):
    """All elementary flux modes of (S, rev), sorted."""
    m = len(rev)
    Sp, back = split_reversible(S, rev)  # @line L1
    mp = len(back)
    if Sp and any(any(x != 0 for x in row) for row in Sp):
        _, piv = rref(Sp)
    else:
        piv = []
    free = [j for j in range(mp) if j not in piv]
    basis = nullspace(Sp, mp) if Sp else nullspace([], mp)  # @line L2
    d = len(basis)
    if d == 0:
        return []
    # The kernel matrix K (mp x d): row j gives x_j as a function of t.
    K = [[basis[b][j] for b in range(d)] for j in range(mp)]
    rays = [list(v) for v in basis]  # @line L3
    done = list(free)
    for p in piv:  # @line L4
        pos = [r for r in rays if r[p] > 0]  # @line L5
        zero = [r for r in rays if r[p] == 0]
        neg = [r for r in rays if r[p] < 0]
        new = []  # @line L6
        for a in pos:  # @line L7
            za = {i for i in done if a[i] == 0}
            for b in neg:
                common = [i for i in za if b[i] == 0]
                if len(common) < d - 2:
                    continue
                if rank([K[i] for i in common]) == d - 2:  # @line L8
                    new.append([a[p] * y - b[p] * x for x, y in zip(a, b)])
        rays = pos + zero + new  # @line L9
        done.append(p)
    modes = set()  # @line L10
    for r in rays:
        supp = [k for k in range(mp) if r[k] != 0]
        if len(supp) == 2 and back[supp[0]][0] == back[supp[1]][0]:
            continue  # a two-cycle j forward + j backward
        v = [Fraction(0)] * m
        for k in supp:
            j, s = back[k]
            v[j] += s * r[k]
        modes.add(primitive(v))
    return sorted(modes)  # @line L11


def brute_force_efms(S, rev):
    """EFMs by brute force over all supports.

    A sign-feasible steady-state vector e is an EFM if and only if the
    columns of S on supp(e) have a kernel of dimension 1. So for every
    support Q: if ker S_Q has dimension 1 and its basis vector has full
    support on Q, the vector or its negative (or both) is a mode when it is
    non-negative on the irreversible reactions.
    """
    from itertools import combinations
    m = len(rev)
    out = set()
    for size in range(1, m + 1):
        for Q in combinations(range(m), size):
            SQ = [[row[j] for j in Q] for row in S]
            B = nullspace(SQ, size) if S else nullspace([], size)
            if len(B) != 1 or any(x == 0 for x in B[0]):
                continue
            for sign in (1, -1):
                e = [sign * x for x in B[0]]
                if all(rev[j] or x > 0 for j, x in zip(Q, e)):
                    v = [Fraction(0)] * m
                    for j, x in zip(Q, e):
                        v[j] = x
                    out.add(primitive(v))
    return sorted(out)


# Network E of the page: R1 -> A, R2 A -> B, R3 A <-> C, R4 B -> C,
# R5 C ->, R6 B ->. Metabolites A, B, C.
S_E = [
    [1, -1, -1, 0, 0, 0],   # A
    [0, 1, 0, -1, 0, -1],   # B
    [0, 0, 1, 1, -1, 0],    # C
]
REV_E = [False, False, True, False, False, False]


def diamond_chain(k):
    """A chain of k diamonds: 2k + 2 irreversible reactions and 2^k EFMs.

    Metabolites M_0, ..., M_k. Uptake -> M_0, two parallel reactions
    M_{i-1} -> M_i for each i, and secretion M_k ->.
    """
    n, m = k + 1, 2 * k + 2
    S = [[0] * m for _ in range(n)]
    S[0][0] = 1
    for i in range(1, k + 1):
        for c in (2 * i - 1, 2 * i):
            S[i - 1][c] = -1
            S[i][c] = 1
    S[k][m - 1] = -1
    return S, [False] * m
