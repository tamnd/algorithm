# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/affinity-propagation/. The authors are listed in prov/6S8D6H.jsonl.

"""Affinity propagation (Frey and Dueck, Science 2007).

S is an n x n list of similarities. S[i][k] (i != k) says how well point k fits
as the exemplar of point i, and the preference S[k][k] says how much point k
wants to be an exemplar. The messages are the responsibilities r(i, k) and the
availabilities a(i, k). Each iteration costs O(n^2). The result is a set of
exemplars and, for each point, the index of its exemplar.
"""

from typing import List, Optional, Sequence

Matrix = List[List[float]]


def squared_distance_similarity(points: Sequence[Sequence[float]], preference=None) -> Matrix:
    """s(i, k) = -||x_i - x_k||^2. The diagonal is the preference (default: the median of s)."""
    n = len(points)
    S = [[-sum((a - b) ** 2 for a, b in zip(points[i], points[k])) for k in range(n)]
         for i in range(n)]
    if preference is None:
        off = sorted(S[i][k] for i in range(n) for k in range(n) if i != k)
        m = len(off)
        preference = off[m // 2] if m % 2 else (off[m // 2 - 1] + off[m // 2]) / 2
    for k in range(n):
        S[k][k] = preference
    return S


def responsibilities(S: Matrix, A: Matrix) -> Matrix:
    """r(i, k) = s(i, k) - max over k' != k of (a(i, k') + s(i, k')). O(n^2) by the two largest values."""
    n = len(S)
    R = [[0.0] * n for _ in range(n)]
    for i in range(n):
        best, second, arg = float("-inf"), float("-inf"), -1
        for k in range(n):
            v = A[i][k] + S[i][k]
            if v > best:
                best, second, arg = v, best, k
            elif v > second:
                second = v
        for k in range(n):
            R[i][k] = S[i][k] - (second if k == arg else best)
    return R


def availabilities(R: Matrix) -> Matrix:
    """a(i, k) = min(0, r(k, k) + sum over i' not in {i, k} of max(0, r(i', k))) for i != k,
    a(k, k) = sum over i' != k of max(0, r(i', k)). O(n^2) by column sums."""
    n = len(R)
    A = [[0.0] * n for _ in range(n)]
    for k in range(n):
        pos = [max(0.0, R[i][k]) if i != k else R[k][k] for i in range(n)]
        total = sum(pos)
        for i in range(n):
            if i == k:
                A[k][k] = total - R[k][k]
            else:
                A[i][k] = min(0.0, total - pos[i])
    return A


def responsibilities_naive(S: Matrix, A: Matrix) -> Matrix:
    """The update rule of r as written, in O(n^3). For tests."""
    n = len(S)
    return [[S[i][k] - max(A[i][j] + S[i][j] for j in range(n) if j != k) for k in range(n)]
            for i in range(n)]


def availabilities_naive(R: Matrix) -> Matrix:
    """The update rule of a as written, in O(n^3). For tests."""
    n = len(R)
    A = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if i == k:
                A[i][k] = sum(max(0.0, R[j][k]) for j in range(n) if j != k)
            else:
                A[i][k] = min(0.0, R[k][k] + sum(max(0.0, R[j][k]) for j in range(n)
                                                 if j != i and j != k))
    return A


def decode(S: Matrix, A: Matrix, R: Matrix):
    """Exemplars are the k with a(k, k) + r(k, k) > 0. Each other point goes to its most
    similar exemplar. With no exemplar, return ([], [-1] * n)."""
    n = len(S)
    exemplars = [k for k in range(n) if A[k][k] + R[k][k] > 0]  # @line L9
    if not exemplars:
        return [], [-1] * n
    labels = []
    for i in range(n):  # @line L10
        if i in exemplars:
            labels.append(i)
        else:
            labels.append(max(exemplars, key=lambda k: (S[i][k], -k)))
    return exemplars, labels


def affinity_propagation(S: Matrix, damping: float = 0.5, max_iter: int = 1000,
                         convergence_iter: int = 15, tol: Optional[float] = None,
                         rng=None, noise: float = 1e-12):
    """Run affinity propagation on the similarity matrix S.

    Stops when the set of exemplars has not changed for convergence_iter iterations
    (and, if tol is given, the largest message change is at most tol), or after max_iter.
    rng (a random.Random) adds tiny noise to S to break ties, as Frey and Dueck do.
    Returns (exemplars, labels, R, A, iterations, converged).
    """
    if not 0.5 <= damping < 1:
        raise ValueError("damping must be in [0.5, 1)")
    n = len(S)
    S = [row[:] for row in S]
    if rng is not None:
        span = max(abs(x) for row in S for x in row) or 1.0
        for i in range(n):
            for k in range(n):
                S[i][k] += noise * span * rng.random()
    R = [[0.0] * n for _ in range(n)]  # @line L1
    A = [[0.0] * n for _ in range(n)]
    last, stable = None, 0
    for it in range(1, max_iter + 1):  # @line L2
        Rn = responsibilities(S, A)  # @line L3
        R2 = [[damping * R[i][k] + (1 - damping) * Rn[i][k] for k in range(n)]
              for i in range(n)]  # @line L4
        An = availabilities(R2)  # @line L5
        A2 = [[damping * A[i][k] + (1 - damping) * An[i][k] for k in range(n)]
              for i in range(n)]  # @line L6
        change = max(max(abs(R2[i][k] - R[i][k]), abs(A2[i][k] - A[i][k]))
                     for i in range(n) for k in range(n))
        R, A = R2, A2
        current = tuple(k for k in range(n) if A[k][k] + R[k][k] > 0)  # @line L7
        stable = stable + 1 if current == last else 1
        last = current
        if stable >= convergence_iter and (tol is None or change <= tol):  # @line L8
            exemplars, labels = decode(S, A, R)
            return exemplars, labels, R, A, it, True
    exemplars, labels = decode(S, A, R)
    return exemplars, labels, R, A, max_iter, False


def net_similarity(S: Matrix, labels: Sequence[int]) -> float:
    """The objective: sum of s(i, c_i), where s(k, k) is the preference of an exemplar."""
    return sum(S[i][c] for i, c in enumerate(labels))


def is_valid(labels: Sequence[int]) -> bool:
    """Each point points to an exemplar, and each exemplar points to itself."""
    return all(c >= 0 and labels[c] == c for c in labels)


def best_exemplar_set(S: Matrix):
    """The exact optimum of the net similarity over all non-empty exemplar sets. O(2^n n^2)."""
    n = len(S)
    best = (float("-inf"), None)
    for mask in range(1, 1 << n):
        E = [k for k in range(n) if mask >> k & 1]
        labels = [i if mask >> i & 1 else max(E, key=lambda k: (S[i][k], -k)) for i in range(n)]
        v = net_similarity(S, labels)
        if v > best[0]:
            best = (v, labels)
    return best
