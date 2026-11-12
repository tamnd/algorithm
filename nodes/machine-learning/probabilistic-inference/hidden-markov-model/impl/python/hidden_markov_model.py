# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hidden-markov-model/. The authors are listed in prov/A7E9ZX.jsonl.

"""A discrete hidden Markov model lambda = (pi, A, B).

States are 0..N-1 and symbols are 0..M-1.
pi[i] = P(q_1 = i), A[i][j] = P(q_(t+1) = j | q_t = i), B[j][k] = P(o_t = k | q_t = j).
The numbers may be floats or fractions.Fraction (for exact checks).
"""

import random
from itertools import product
from typing import Sequence


def validate(pi: Sequence, A: Sequence[Sequence], B: Sequence[Sequence], tol: float = 1e-9) -> None:
    """Raise ValueError unless pi, every row of A and every row of B are probability vectors."""
    n = len(pi)
    if n == 0 or len(A) != n or len(B) != n:
        raise ValueError("pi, A and B must have N >= 1 rows")
    m = len(B[0])
    rows = [("pi", pi, n)] + [("A", r, n) for r in A] + [("B", r, m) for r in B]
    for name, row, size in rows:
        if len(row) != size:
            raise ValueError(f"a row of {name} has the wrong length")
        if any(x < 0 for x in row) or abs(sum(row) - 1) > tol:
            raise ValueError(f"a row of {name} is not a probability vector")


def _draw(row: Sequence, rng: random.Random) -> int:
    """Inverse-CDF draw of an index with the given probabilities."""
    u = rng.random() * float(sum(row))
    acc = 0.0
    for i, p in enumerate(row):
        acc += float(p)
        if u < acc:
            return i
    return max(i for i, p in enumerate(row) if p > 0)  # rounding at the top end


def sample(pi: Sequence, A: Sequence[Sequence], B: Sequence[Sequence], T: int, rng: random.Random):
    """Ancestral sampling: q_1 ~ pi, o_t ~ B[q_t], q_(t+1) ~ A[q_t]. Return (states, symbols). O(T (N + M))."""
    states: list[int] = []
    symbols: list[int] = []
    for t in range(T):
        q = _draw(pi, rng) if t == 0 else _draw(A[states[-1]], rng)
        states.append(q)
        symbols.append(_draw(B[q], rng))
    return states, symbols


def joint(pi: Sequence, A: Sequence[Sequence], B: Sequence[Sequence], states: Sequence[int], obs: Sequence[int]):
    """P(Q, O) = pi[q_1] B[q_1][o_1] prod_(t >= 2) A[q_(t-1)][q_t] B[q_t][o_t]. O(T)."""
    if len(states) != len(obs) or not obs:
        raise ValueError("states and obs must have the same length T >= 1")
    p = pi[states[0]] * B[states[0]][obs[0]]
    for t in range(1, len(obs)):
        p = p * A[states[t - 1]][states[t]] * B[states[t]][obs[t]]
    return p


def likelihood_by_enumeration(pi: Sequence, A: Sequence[Sequence], B: Sequence[Sequence], obs: Sequence[int]):
    """P(O) as the sum of P(Q, O) over all N^T state paths. Exponential: for checks only.
    The forward algorithm computes the same number in O(T N^2)."""
    return sum(joint(pi, A, B, q, obs) for q in product(range(len(pi)), repeat=len(obs)))


def state_marginals(pi: Sequence, A: Sequence[Sequence], T: int) -> list[list]:
    """P(q_t = i) for t = 1..T: the hidden layer alone is a Markov chain, p_(t+1) = p_t A."""
    n = len(pi)
    rows = [list(pi)]
    for _ in range(T - 1):
        rows.append([sum(rows[-1][i] * A[i][j] for i in range(n)) for j in range(n)])
    return rows
