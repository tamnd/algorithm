# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/graph-cut-stereo/. The authors are listed in prov/A0NX9X.jsonl.
"""Graph cut stereo with occlusions, after Kolmogorov and Zabih (2001).

The pair is rectified; left pixel (u, v) may match right pixel (u - d, v)
with d in [0, D). An assignment is a = (v, u, d) with u - d >= 0, and a
configuration is the set A of active assignments. Its energy is

    E(A) = sum_{a in A} Dcost(a)                         data
         + K * (pixels of either image covered by no a)  occlusion
         + sum over neighbor pairs {a1, a2} of V(a1, a2) [exactly one active]
         + infinity if a pixel is covered twice           uniqueness

Two assignments are neighbors when they have the same d and their left
pixels are 4-neighbors. Dcost(a) = min(|IL - IR|, cutoff), and V is
3 * lam when both the left and the right intensity differences of the
pair are below 8, and lam otherwise (the choice of the IPOL version).

An alpha-expansion move may drop any active assignment whose disparity is
not alpha and may switch any assignment of disparity alpha on or off. The
best move is a regular binary energy and is found by one minimum cut.
"""

from __future__ import annotations

from collections import deque
from typing import Dict, List, Optional, Sequence, Set, Tuple

Assignment = Tuple[int, int, int]  # (v, u, d)
INF = float("inf")


class Problem:
    def __init__(self, left, right, D: int, K: float, lam: float,
                 cutoff: float = 30):
        self.left, self.right, self.D = left, right, D
        self.H, self.W = len(left), len(left[0])
        self.K, self.lam, self.cutoff = K, lam, cutoff

    def valid(self, v: int, u: int, d: int) -> bool:
        return 0 <= v < self.H and 0 <= u < self.W and 0 <= u - d < self.W and 0 <= d < self.D

    def data(self, a: Assignment) -> float:
        v, u, d = a
        return min(abs(self.left[v][u] - self.right[v][u - d]), self.cutoff)

    def smooth(self, a1: Assignment, a2: Assignment) -> float:
        (v1, u1, d), (v2, u2, _) = a1, a2
        dl = abs(self.left[v1][u1] - self.left[v2][u2])
        dr = abs(self.right[v1][u1 - d] - self.right[v2][u2 - d])
        return 3 * self.lam if max(dl, dr) < 8 else self.lam

    def assignments(self) -> List[Assignment]:
        return [(v, u, d) for v in range(self.H) for u in range(self.W)
                for d in range(self.D) if u - d >= 0]

    def neighbor_pairs(self) -> List[Tuple[Assignment, Assignment]]:
        out = []
        for (v, u, d) in self.assignments():
            for (v2, u2) in ((v, u + 1), (v + 1, u)):
                if self.valid(v2, u2, d):
                    out.append(((v, u, d), (v2, u2, d)))
        return out


def energy(P: Problem, A: Set[Assignment]) -> float:
    left_cov: Dict[Tuple[int, int], int] = {}
    right_cov: Dict[Tuple[int, int], int] = {}
    e = 0.0
    for a in A:
        v, u, d = a
        left_cov[(v, u)] = left_cov.get((v, u), 0) + 1
        right_cov[(v, u - d)] = right_cov.get((v, u - d), 0) + 1
        e += P.data(a)
    if any(c > 1 for c in left_cov.values()) or any(c > 1 for c in right_cov.values()):
        return INF
    e += P.K * (2 * P.H * P.W - len(left_cov) - len(right_cov))
    for (a1, a2) in P.neighbor_pairs():
        if (a1 in A) != (a2 in A):
            e += P.smooth(a1, a2)
    return e


def _min_cut_source_side(nn: int, edges, s: int, t: int) -> List[bool]:
    """Edmonds-Karp max flow; return the nodes that s reaches at the end."""
    adj: List[List[int]] = [[] for _ in range(nn)]
    to: List[int] = []
    cap: List[float] = []
    for (u, v, c) in edges:
        adj[u].append(len(to))
        to.append(v)
        cap.append(c)
        adj[v].append(len(to))
        to.append(u)
        cap.append(0)
    while True:
        prev = [-1] * nn
        seen = [False] * nn
        seen[s] = True
        queue = deque([s])
        while queue and not seen[t]:
            u = queue.popleft()
            for e in adj[u]:
                if cap[e] > 0 and not seen[to[e]]:
                    seen[to[e]] = True
                    prev[to[e]] = e
                    queue.append(to[e])
        if not seen[t]:
            return seen
        path = []
        v = t
        while v != s:
            path.append(prev[v])
            v = to[prev[v] ^ 1]
        delta = min(cap[e] for e in path)
        for e in path:
            cap[e] -= delta
            cap[e ^ 1] += delta


def minimize_regular_binary(n: int, unary, terms) -> List[int]:
    """Minimize sum_p unary[p][x_p] + sum of terms (p, q, A, B, C, D), with
    A = theta(0,0), B = theta(0,1), C = theta(1,0), D = theta(1,1) and
    A + D <= B + C, over x in {0,1}^n, by one minimum cut (x_p = 0 is the
    source side)."""
    s, t = n, n + 1
    lin = [u1 - u0 for (u0, u1) in unary]
    edges = []
    for (p, q, A, B, C, Dd) in terms:
        k = B + C - A - Dd
        if k < 0:
            raise ValueError("nonregular term")
        lin[p] += C - A
        lin[q] += Dd - C
        if k > 0:
            edges.append((p, q, k))
    for p in range(n):
        if lin[p] > 0:
            edges.append((s, p, lin[p]))
        elif lin[p] < 0:
            edges.append((p, t, -lin[p]))
    side = _min_cut_source_side(n + 2, edges, s, t)
    return [0 if side[p] else 1 for p in range(n)]


def move_energy(P: Problem, A: Set[Assignment], alpha: int):
    """The binary energy of the alpha-expansion of A.

    Returns (variables, n_old, unary, terms, constant, big). Variable i is
    an assignment. The first n_old are the active ones with d != alpha:
    x = 0 keeps one and x = 1 drops it. The others are all assignments
    with d == alpha: x = 1 makes one active. The finite
    part of the binary energy plus the constant equals E of the result;
    `big` stands in for infinity."""
    old = sorted(a for a in A if a[2] != alpha)
    new = [a for a in P.assignments() if a[2] == alpha]
    var = old + new
    index = {a: i for i, a in enumerate(var)}
    n_old = len(old)
    big = 1 + P.K * 2 * P.H * P.W + sum(P.data(a) for a in var) \
        + sum(P.smooth(a1, a2) for (a1, a2) in P.neighbor_pairs())
    unary = [[0.0, 0.0] for _ in var]
    terms = []
    const = 0.0
    for i, a in enumerate(var):  # data
        if i < n_old:
            unary[i][0] += P.data(a)
        else:
            unary[i][1] += P.data(a)
    # each pixel: the old assignment and the alpha assignment covering it
    cover_old: Dict[Tuple[str, int, int], int] = {}
    for i, (v, u, d) in enumerate(old):
        cover_old[("L", v, u)] = i
        cover_old[("R", v, u - d)] = i
    for v in range(P.H):
        for u in range(P.W):
            for side in ("L", "R"):
                i = cover_old.get((side, v, u))
                a_new = (v, u, alpha) if side == "L" else (v, u + alpha, alpha)
                j = index.get(a_new) if P.valid(*a_new) else None
                if i is not None and j is not None:
                    # occluded if dropped and not switched on; both: forbidden
                    terms.append((i, j, 0.0, big, P.K, 0.0))
                elif i is not None:
                    unary[i][1] += P.K
                elif j is not None:
                    unary[j][0] += P.K
                else:
                    const += P.K
    for (a1, a2) in P.neighbor_pairs():  # smoothness
        w = P.smooth(a1, a2)
        i, j = index.get(a1), index.get(a2)
        if i is not None and j is not None:
            terms.append((i, j, 0.0, w, w, 0.0))
        elif i is not None:  # a2 stays inactive; pay w if a1 is active
            unary[i][0 if i < n_old else 1] += w
        elif j is not None:
            unary[j][0 if j < n_old else 1] += w
    return var, n_old, unary, terms, const, big


def result_of(var, n_old, x) -> Set[Assignment]:
    return {a for i, a in enumerate(var) if (x[i] == 0) == (i < n_old)}


def expansion_move(P: Problem, A: Set[Assignment], alpha: int) -> Set[Assignment]:
    var, n_old, unary, terms, _, _ = move_energy(P, A, alpha)  # @line L5
    x = minimize_regular_binary(len(var), unary, terms)  # @line L6
    return result_of(var, n_old, x)  # @line L6


def graph_cut_stereo(P: Problem, A: Optional[Set[Assignment]] = None,
                     order: Optional[Sequence[int]] = None
                     ) -> Tuple[Set[Assignment], int]:
    """Expansion moves over all disparities until none lowers E.
    Returns (active assignments, number of cycles)."""
    A = set() if A is None else set(A)  # @line L1
    e = energy(P, A)
    order = list(range(P.D)) if order is None else list(order)
    cycles = 0
    while True:  # @line L2
        cycles += 1
        success = False  # @line L3
        for alpha in order:  # @line L4
            A2 = expansion_move(P, A, alpha)
            e2 = energy(P, A2)
            if e2 < e:  # @line L7
                A, e, success = A2, e2, True  # @line L7
        if not success:  # @line L8
            return A, cycles


def disparity_map(P: Problem, A: Set[Assignment]) -> List[List[Optional[int]]]:
    """The disparity of each left pixel, or None where it is occluded."""
    out: List[List[Optional[int]]] = [[None] * P.W for _ in range(P.H)]
    for (v, u, d) in A:  # @line L9
        out[v][u] = d
    return out
