# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gale-church-alignment/. The authors are listed in prov/TXM3A8.jsonl.

"""Gale-Church sentence alignment by sentence lengths in characters.

The input is two lists of sentence lengths, x (language L1) and y (language L2).
The output is a list of beads. A bead (i0, i1, j0, j1) joins the L1 sentences
i0+1 .. i1 with the L2 sentences j0+1 .. j1 (fencepost indices, 0 at the left
edge). The bead types are the six of Gale and Church (1993): 1-1, 1-0, 0-1,
2-1, 1-2 and 2-2.

The cost of a bead is -log(Prior(p, q) * 2 * (1 - Phi(|delta|))) in nats, with
delta = (l2 - c * l1) / sqrt(s2 * lbar) and lbar = (l1 + l2 / c) / 2, as in the
C program in the appendix of the paper. The text of the paper writes l1 in
place of lbar; that form is undefined for a 0-1 bead, where l1 = 0.

The dynamic program works in the tropical semiring (min, +) on these costs.
Tie rule: line L7 keeps the first bead type in the order of BEADS that reaches
the minimum.
"""

import math
from typing import Dict, List, Sequence, Tuple

INF = float("inf")

# The order of the bead types fixes the tie rule.
BEADS: Tuple[Tuple[int, int], ...] = ((1, 1), (1, 0), (0, 1), (2, 1), (1, 2), (2, 2))

# Table 5 of Gale and Church (1993). The category "1-0 or 0-1" (0.0099) and the
# category "2-1 or 1-2" (0.089) are used for each direction, as the C program
# does, so the six weights sum to 1.0988, not to 1.
PRIORS: Dict[Tuple[int, int], float] = {
    (1, 1): 0.89,
    (1, 0): 0.0099,
    (0, 1): 0.0099,
    (2, 1): 0.089,
    (1, 2): 0.089,
    (2, 2): 0.011,
}

C_MEAN = 1.0  # c: expected characters of L2 per character of L1
S2_VAR = 6.8  # s^2: variance of the characters of L2 per character of L1


def log_two_sided_tail(x: float) -> float:
    """Return log(2 * (1 - Phi(|x|))) = log P(|Z| >= |x|) for a standard normal Z.

    For |x| < 30 this uses math.erfc. Beyond, erfc is close to underflow, so it
    uses the asymptotic series sqrt(2 / pi) exp(-x^2 / 2) / x * (1 - 1/x^2 + 3/x^4),
    whose relative error there is below 1e-8. Cost O(1).
    """
    x = abs(x)
    if x < 30.0:
        return math.log(math.erfc(x / math.sqrt(2.0)))
    series = 1.0 - 1.0 / x**2 + 3.0 / x**4
    return 0.5 * math.log(2.0 / math.pi) - 0.5 * x * x - math.log(x) + math.log(series)


def delta(l1: float, l2: float, c: float = C_MEAN, s2: float = S2_VAR) -> float:
    """The normalized length difference of a bead with l1 and l2 characters."""
    lbar = (l1 + l2 / c) / 2.0  # @line L12
    if lbar == 0:
        return 0.0
    return (l2 - c * l1) / math.sqrt(s2 * lbar)  # @line L13


def bead_cost(l1: float, l2: float, p: int, q: int, c: float = C_MEAN, s2: float = S2_VAR,
              priors: Dict[Tuple[int, int], float] = PRIORS) -> float:
    """Return -log(Prior(p, q)) - log(2 (1 - Phi(|delta|))) in nats."""
    d = delta(l1, l2, c, s2)
    return -math.log(priors[(p, q)]) - log_two_sided_tail(d)  # @line L14


def align(x: Sequence[int], y: Sequence[int], c: float = C_MEAN, s2: float = S2_VAR,
          priors: Dict[Tuple[int, int], float] = PRIORS) -> Tuple[List[Tuple[int, int, int, int]], float]:
    """Return (beads, total cost) of the cheapest monotone alignment of x with y.

    x and y are lists of non-negative sentence lengths. Every sentence is in
    exactly one bead, and the beads keep the order of both texts. Cost:
    O(I J) time and O(I J) memory for the table and the back pointers, with
    I = len(x) and J = len(y).
    """
    nx, ny = len(x), len(y)
    px = [0] * (nx + 1)
    for i, v in enumerate(x):
        px[i + 1] = px[i] + v
    py = [0] * (ny + 1)
    for j, v in enumerate(y):
        py[j + 1] = py[j] + v
    D = [[INF] * (ny + 1) for _ in range(nx + 1)]
    B: List[List[Tuple[int, int]]] = [[(0, 0)] * (ny + 1) for _ in range(nx + 1)]
    D[0][0] = 0.0  # @line L1
    for i in range(nx + 1):  # @line L2
        for j in range(ny + 1):  # @line L3
            if i == 0 and j == 0:  # @line L4
                continue
            for p, q in BEADS:  # @line L5
                if p > i or q > j or D[i - p][j - q] == INF:
                    continue
                l1 = px[i] - px[i - p]
                l2 = py[j] - py[j - q]
                cost = D[i - p][j - q] + bead_cost(l1, l2, p, q, c, s2, priors)  # @line L6
                if cost < D[i][j]:  # @line L7
                    D[i][j] = cost
                    B[i][j] = (p, q)
    beads: List[Tuple[int, int, int, int]] = []
    i, j = nx, ny  # @line L8
    while (i, j) != (0, 0):  # @line L9
        p, q = B[i][j]  # @line L10
        beads.append((i - p, i, j - q, j))
        i, j = i - p, j - q
    beads.reverse()
    return beads, D[nx][ny]  # @line L11


def alignment_cost(x: Sequence[int], y: Sequence[int], beads: Sequence[Tuple[int, int, int, int]],
                   c: float = C_MEAN, s2: float = S2_VAR,
                   priors: Dict[Tuple[int, int], float] = PRIORS) -> float:
    """The total cost of a given list of beads (for tests and for the reader)."""
    total = 0.0
    for i0, i1, j0, j1 in beads:
        total += bead_cost(sum(x[i0:i1]), sum(y[j0:j1]), i1 - i0, j1 - j0, c, s2, priors)
    return total
