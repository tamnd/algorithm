# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dali/. The authors are listed in prov/YVJ262.jsonl.

"""DALI (Holm and Sander 1993): structure alignment by comparison of
intramolecular distance matrices, C-alpha only, distances in angstrom.

The elastic similarity score of a residue matching M = {(i, j)} is

  S(M) = sum over (i, j) in M and (i', j') in M of phi(i, i', j, j'),
  phi = theta_E                                   if (i, j) == (i', j'),
  phi = (theta_E - |dA - dB| / d*) * exp(-(d*/alpha)^2)   otherwise,

with dA = |a_i - a_i'|, dB = |b_j - b_j'|, d* = (dA + dB) / 2,
theta_E = 0.2 and alpha = 20 angstrom.

The search follows the outline of the paper: compare all pairs of fragments
of w residues (w = 6, hexapeptides, in the paper) to get a list of candidate
fragment pairs, then run a Metropolis Monte Carlo search from the best
candidates. A move adds a candidate fragment pair, and removes the pairs that
conflict with it, or deletes one fragment. The best alignment seen is kept.
This implementation keeps the alignment sequential (order preserving).

The result is a heuristic optimum, a lower bound of the true maximum of S.
Standard library only, random numbers from random.Random(seed).
"""

import math
import random

Vec = tuple[float, float, float]
Pair = tuple[int, int]

THETA_E = 0.2
ALPHA = 20.0


def distance_matrix(pts: list[Vec]) -> list[list[float]]:
    return [[math.dist(p, q) for q in pts] for p in pts]


def phi(da: float, db: float) -> float:
    """The elastic similarity of one pair of distances (off the diagonal)."""
    dstar = 0.5 * (da + db)
    if dstar == 0.0:
        return THETA_E
    return (THETA_E - abs(da - db) / dstar) * math.exp(-(dstar / ALPHA) ** 2)


def elastic_score(m: list[Pair], dA: list[list[float]], dB: list[list[float]]) -> float:
    """S(M), summed over all ordered pairs of matched pairs, the diagonal included."""
    s = THETA_E * len(m)
    for x in range(len(m)):
        i, j = m[x]
        for y in range(x + 1, len(m)):
            i2, j2 = m[y]
            s += 2.0 * phi(dA[i][i2], dB[j][j2])
    return s


def _consistent(m: list[Pair], new: list[Pair]) -> list[Pair]:
    """Insert the fragment `new` and drop each old pair that uses one of its residues
    or breaks the order of residues in A and B."""
    keep = []
    for p in m:
        ok = True
        for q in new:
            if p[0] == q[0] or p[1] == q[1] or (p[0] < q[0]) != (p[1] < q[1]):
                ok = False
                break
        if ok:
            keep.append(p)
    return sorted(keep + new)


def _segments(m: list[Pair]) -> list[list[Pair]]:
    """Split a sequential alignment into maximal runs without gaps."""
    segs: list[list[Pair]] = []
    for p in m:
        if segs and p[0] == segs[-1][-1][0] + 1 and p[1] == segs[-1][-1][1] + 1:
            segs[-1].append(p)
        else:
            segs.append([p])
    return segs


def candidate_fragments(dA: list[list[float]], dB: list[list[float]], w: int) -> list[tuple[float, int, int]]:
    """All fragment pairs (i, j) of length w with a positive score, best first."""
    n, m = len(dA), len(dB)
    out = []
    for i in range(n - w + 1):
        for j in range(m - w + 1):
            frag = [(i + k, j + k) for k in range(w)]
            s = elastic_score(frag, dA, dB)
            if s > 0:
                out.append((s, i, j))
    out.sort(key=lambda c: (-c[0], c[1], c[2]))
    return out


def refine(m: list[Pair], s: float, cands: list[tuple[float, int, int]], w: int,
           dA: list[list[float]], dB: list[list[float]]) -> tuple[float, list[Pair]]:
    """Expansion and trimming cycles: add any candidate fragment, or delete any
    segment, whenever this raises S, until no such move is left."""
    improved = True
    while improved:
        improved = False
        for _, i, j in cands:  # expansion: test each candidate of the pair list
            nxt = _consistent(m, [(i + k, j + k) for k in range(w)])
            ns = elastic_score(nxt, dA, dB)
            if ns > s + 1e-12:
                m, s, improved = nxt, ns, True
        for seg in _segments(m):  # trimming: test the removal of each segment
            drop = set(seg)
            nxt = [p for p in m if p not in drop]
            ns = elastic_score(nxt, dA, dB)
            if ns > s + 1e-12:
                m, s, improved = nxt, ns, True
                break
    return s, m


def dali(a: list[Vec], b: list[Vec], w: int = 6, seeds: int = 5, steps: int = 400,
         beta0: float = 2.0, growth: float = 1.02, seed: int = 0) -> tuple[float, list[Pair]]:
    """Return (S, M): the best elastic score found and its sequential alignment."""
    rng = random.Random(seed)
    dA, dB = distance_matrix(a), distance_matrix(b)  # @line L1
    w = max(1, min(w, len(a), len(b)))
    cands = candidate_fragments(dA, dB, w)  # @line L2
    best_s, best_m = 0.0, []  # @line L3
    for s0, i0, j0 in cands[:seeds]:  # @line L4
        cur = [(i0 + k, j0 + k) for k in range(w)]  # @line L5
        cur_s, beta = s0, beta0
        traj_s, traj_m = cur_s, list(cur)
        for _ in range(steps):  # @line L6
            if cur and rng.random() < 0.5:  # @line L7
                segs = _segments(cur)
                drop = set(segs[rng.randrange(len(segs))])
                nxt = [p for p in cur if p not in drop]
            else:
                _, i, j = cands[rng.randrange(len(cands))]
                nxt = _consistent(cur, [(i + k, j + k) for k in range(w)])
            nxt_s = elastic_score(nxt, dA, dB)
            if nxt_s >= cur_s or rng.random() < math.exp(beta * (nxt_s - cur_s)):  # @line L8
                cur, cur_s = nxt, nxt_s
            if cur_s > traj_s:  # @line L9
                traj_s, traj_m = cur_s, list(cur)
            beta *= growth  # @line L10
        traj_s, traj_m = refine(traj_m, traj_s, cands, w, dA, dB)  # @line L11
        if traj_s > best_s:  # @line L12
            best_s, best_m = traj_s, traj_m
    return best_s, best_m  # @line L13
