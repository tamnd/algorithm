# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/meme-algorithm/. The authors are listed in prov/FD26PV.jsonl.
"""The EM core of MEME (Bailey and Elkan 1994) for one motif: a two-component
mixture of a motif model and a background model over all windows of length L,
fit by expectation maximization from many starting points.

This code leaves out the parts of MEME that find several motifs (erasing),
the smoothing of z over overlapping windows and the search over lambda.

Positions are 0-based in this code; the page numbers them from 1.
"""

import math
from typing import List, NamedTuple, Optional, Sequence, Tuple

from bioseq import DNA, kmers

_INDEX = {a: k for k, a in enumerate(DNA)}


class MemeResult(NamedTuple):
    """The fitted model and the run history.

    theta[j][a] is the motif letter probability, theta0[a] the background one,
    lam the mixing weight, z the posterior motif probability of each window in
    the order of windows(), start the start string chosen, and objective the
    log posterior after each iteration of the main run.
    """

    theta: Tuple[Tuple[float, ...], ...]
    theta0: Tuple[float, ...]
    lam: float
    z: Tuple[float, ...]
    start: str
    objective: Tuple[float, ...]
    iterations: int


def windows(seqs: Sequence[str], L: int) -> List[Tuple[int, int]]:
    """All windows as (sequence index, 0-based start), sequence by sequence."""
    return [(i, q) for i, s in enumerate(seqs) for q in range(len(s) - L + 1)]


def letter_frequencies(seqs: Sequence[str]) -> List[float]:
    """mu[a]: the frequency of each letter over all sequences."""
    total = sum(len(s) for s in seqs)
    return [sum(s.count(a) for s in seqs) / total for a in DNA]


def _encode(seqs, L):
    return [tuple(_INDEX[a] for a in w) for s in seqs for w in kmers(s, L)]


def objective(X, theta, theta0, lam, beta, mu) -> float:
    """The log posterior that MEME's EM increases: the mixture log likelihood
    plus beta * sum mu(a) log of the motif and background probabilities."""
    lt = [[math.log(p) for p in row] for row in theta]
    l0 = [math.log(p) for p in theta0]
    ll = 0.0
    for x in X:
        a1 = math.log(lam) + sum(lt[j][c] for j, c in enumerate(x))
        a0 = math.log(1 - lam) + sum(l0[c] for c in x)
        m = max(a1, a0)
        ll += m + math.log(math.exp(a1 - m) + math.exp(a0 - m))
    prior = sum(beta * mu[a] * lt[j][a] for j in range(len(theta)) for a in range(4))
    prior += sum(beta * mu[a] * l0[a] for a in range(4))
    return ll + prior


def e_step(X, theta, theta0, lam) -> List[float]:
    """z_k = lam P(X_k | theta) / (lam P(X_k | theta) + (1 - lam) P(X_k | theta0))."""
    lt = [[math.log(p) for p in row] for row in theta]
    l0 = [math.log(p) for p in theta0]
    cut = math.log((1 - lam) / lam)
    z = []
    for x in X:
        r = sum(lt[j][c] - l0[c] for j, c in enumerate(x)) - cut
        z.append(1 / (1 + math.exp(-r)) if r >= 0 else math.exp(r) / (1 + math.exp(r)))
    return z


def m_step(X, z, L, beta, mu):
    """lam = sum z / N, theta_j(a) = (c_j(a) + beta mu(a)) / (sum_a c_j(a) + beta), and the same for theta0."""
    lam = sum(z) / len(X)  # @line L8
    c = [[0.0] * 4 for _ in range(L)]
    c0 = [0.0] * 4
    for x, zk in zip(X, z):
        for j, a in enumerate(x):
            c[j][a] += zk
            c0[a] += 1 - zk
    theta = [[(c[j][a] + beta * mu[a]) / (sum(c[j]) + beta) for a in range(4)] for j in range(L)]  # @line L9
    theta0 = [(c0[a] + beta * mu[a]) / (sum(c0) + beta) for a in range(4)]
    lam = min(max(lam, 1e-12), 1 - 1e-12)
    return theta, theta0, lam


def start_model(u: str, m: float) -> List[List[float]]:
    """The starting motif model of the string u: probability m for its letter, (1 - m) / 3 for the others."""
    return [[m if a == _INDEX[x] else (1 - m) / 3 for a in range(4)] for x in u]


def meme(seqs: Sequence[str], L: int, beta: float = 0.1, m: float = 0.7,
         starts: Optional[Sequence[str]] = None, tol: float = 1e-6, max_iter: int = 200) -> MemeResult:
    """Fit the motif and background mixture by EM and return the fitted model.

    starts are the start strings; by default the distinct windows of the first
    sequence, in order of first occurrence. Each start gets one EM iteration
    from lambda = n / N; the start with the largest objective after it is run
    to convergence (the largest change of a motif probability below tol, or
    max_iter iterations). The defaults m = 0.7 and beta = 0.1 are the choice
    of this code, picked on planted test data. Cost:
    O(N L) per iteration for the N windows.
    """
    if L <= 0:
        raise ValueError("L must be positive")
    if not seqs:
        raise ValueError("need at least one sequence")
    for s in seqs:
        if len(s) < L or set(s) - set(DNA):
            raise ValueError("sequences must be over ACGT with length at least L")
    if beta <= 0 or not 0.25 < m < 1:
        raise ValueError("beta must be positive and m in (0.25, 1)")
    X = _encode(seqs, L)  # @line L1
    N = len(X)
    mu = letter_frequencies(seqs)
    if min(mu) == 0:
        raise ValueError("every letter must occur in the input")
    if starts is None:
        starts = list(dict.fromkeys(kmers(seqs[0], L)))
    lam0 = min(len(seqs) / N, 0.5)
    best = None
    for u in starts:  # @line L2
        if len(u) != L or set(u) - set(DNA):
            raise ValueError("start strings must be over ACGT with length L")
        theta, theta0, lam = start_model(u, m), list(mu), lam0  # @line L3
        z = e_step(X, theta, theta0, lam)  # @line L4
        theta, theta0, lam = m_step(X, z, L, beta, mu)
        f = objective(X, theta, theta0, lam, beta, mu)
        if best is None or f > best[0]:
            best = (f, u, theta, theta0, lam)
    f, u, theta, theta0, lam = best  # @line L5
    history = [f]
    it = 1
    while True:  # @line L6
        z = e_step(X, theta, theta0, lam)  # @line L7
        new_theta, theta0, lam = m_step(X, z, L, beta, mu)
        change = max(abs(p - r) for row, nrow in zip(theta, new_theta) for p, r in zip(row, nrow))
        theta = new_theta
        history.append(objective(X, theta, theta0, lam, beta, mu))
        it += 1
        if change < tol or it >= max_iter:  # @line L10
            break
    z = e_step(X, theta, theta0, lam)
    return MemeResult(tuple(map(tuple, theta)), tuple(theta0), lam, tuple(z), u, tuple(history), it)  # @line L11


def consensus(theta) -> str:
    """The most probable letter of each column (the first in ACGT order on a tie)."""
    return "".join(DNA[max(range(4), key=lambda a: (row[a], -a))] for row in theta)


def best_sites(seqs: Sequence[str], L: int, z: Sequence[float]) -> Tuple[int, ...]:
    """For each sequence, the 0-based start of its window with the largest z (the first on a tie)."""
    out, k = [], 0
    for s in seqs:
        w = len(s) - L + 1
        row = z[k:k + w]
        out.append(max(range(w), key=lambda q: (row[q], -q)))
        k += w
    return tuple(out)
