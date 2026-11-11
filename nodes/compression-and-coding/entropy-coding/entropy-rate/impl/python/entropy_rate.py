# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/entropy-rate/. The authors are listed in prov/7JPQ0Z.jsonl.
"""The entropy rate of a stationary Markov chain, and block entropies of a sampled sequence."""

import random
from collections import Counter
from math import log2
from typing import Sequence

Matrix = Sequence[Sequence[float]]


def _h(ps) -> float:
    return -sum(p * log2(p) for p in ps if p > 0)


def check_stochastic(P: Matrix) -> None:
    n = len(P)
    for row in P:
        if len(row) != n or any(v < 0 for v in row) or abs(sum(row) - 1.0) > 1e-12:
            raise ValueError("P is not a square stochastic matrix")


def stationary_distribution(P: Matrix, tol: float = 1e-15, max_iter: int = 1_000_000) -> list[float]:
    """mu with mu P = mu, by power iteration on the lazy chain (I + P) / 2.

    The lazy chain has the same stationary distributions as P and is aperiodic,
    so the iteration converges when P is irreducible.
    """
    check_stochastic(P)
    n = len(P)
    mu = [1.0 / n] * n
    for _ in range(max_iter):
        step = [sum(mu[i] * P[i][j] for i in range(n)) for j in range(n)]
        nxt = [(a + b) / 2 for a, b in zip(mu, step)]
        if max(abs(a - b) for a, b in zip(mu, nxt)) < tol:
            return nxt
        mu = nxt
    raise RuntimeError("power iteration did not converge")


def markov_entropy_rate(P: Matrix, mu: Sequence[float] | None = None) -> float:
    """H = sum_i mu_i H(P_i) bits per symbol for the stationary chain with transition matrix P."""
    if mu is None:
        mu = stationary_distribution(P)
    return sum(m * _h(row) for m, row in zip(mu, P))


def markov_block_entropy(P: Matrix, k: int) -> float:
    """H(X_1, ..., X_k) of the stationary chain: H(mu) + (k - 1) H."""
    mu = stationary_distribution(P)
    if k == 0:
        return 0.0
    return _h(mu) + (k - 1) * markov_entropy_rate(P, mu)


def sample_markov(P: Matrix, n: int, seed: int) -> list[int]:
    """n states of the chain, started from its stationary distribution."""
    rng = random.Random(seed)
    mu = stationary_distribution(P)
    states = range(len(P))
    x = rng.choices(states, weights=mu)[0]
    out = [x]
    for _ in range(n - 1):
        x = rng.choices(states, weights=P[x])[0]
        out.append(x)
    return out


def empirical_block_entropy(seq: Sequence[int], k: int) -> float:
    """The entropy of the empirical law of the overlapping k-blocks of seq, in bits."""
    if k == 0:
        return 0.0
    counts = Counter(tuple(seq[i:i + k]) for i in range(len(seq) - k + 1))
    total = sum(counts.values())
    return _h(c / total for c in counts.values())
