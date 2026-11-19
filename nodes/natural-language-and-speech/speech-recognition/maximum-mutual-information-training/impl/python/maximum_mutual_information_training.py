# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-mutual-information-training/. The authors are listed in prov/BW4ZT9.jsonl.

"""Maximum mutual information (MMI) training: the objective, its gradient and
the extended Baum-Welch update of discrete output distributions.

The acoustic model is an HMM whose emitting states carry pdf ids. The caller
gives loglik[t][p] = ln p(o_t | pdf p) for frames t = 0..T-1 (a Gaussian
mixture log density, a discrete output probability, or a scaled network output).

A graph is a set of emitting states with pdf ids, arcs (i, j, ln w), initial
log weights and final log weights. The graph weights hold the transition
probabilities, the pronunciation probabilities and the language model
probabilities. The numerator graph holds the paths of the reference
transcript, the denominator graph the paths of all competing transcripts (in
practice a lattice; here any small graph, for example the union of a list of
word sequences). With an acoustic scale kappa, the score of a state path
q_0..q_{T-1} is

    kappa * sum_t loglik[t][pdf(q_t)] + init(q_0) + sum_t ln w(q_{t-1}, q_t) + final(q_{T-1}),

Z_G is the sum of exp(score) over the paths of G, and the MMI objective of one
utterance is F = ln Z_num - ln Z_den. Its gradient with respect to
loglik[t][p] is kappa * (gamma_num[t][p] - gamma_den[t][p]), where gamma is the
posterior probability of pdf p at frame t in each graph.

All logs are natural logs. The code takes the per-frame scores as given.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Sequence, Tuple

from nlslog import NEG_INF, log_sum


@dataclass
class Graph:
    """An HMM graph of emitting states. pdf[j] is the pdf id of state j."""

    pdf: List[int]
    arcs: List[Tuple[int, int, float]]
    init: Dict[int, float]
    final: Dict[int, float]
    incoming: List[List[Tuple[int, float]]] = field(init=False)
    outgoing: List[List[Tuple[int, float]]] = field(init=False)

    def __post_init__(self):
        n = len(self.pdf)
        self.incoming = [[] for _ in range(n)]
        self.outgoing = [[] for _ in range(n)]
        for i, j, w in self.arcs:
            self.incoming[j].append((i, w))
            self.outgoing[i].append((j, w))


def word_sequence_graph(words: Sequence[str], models: Dict[str, Sequence[int]], log_self: float, log_next: float, log_lm: float = 0.0) -> Graph:
    """A left-to-right chain for one word sequence. Each word is a list of pdf ids,
    one emitting state each, with a self loop (ln weight log_self) and a move to the
    next state (log_next). log_lm is added at the start (the LM log probability of
    the whole sequence)."""
    pdf: List[int] = []
    for w in words:
        pdf.extend(models[w])
    n = len(pdf)
    arcs = [(j, j, log_self) for j in range(n)] + [(j, j + 1, log_next) for j in range(n - 1)]
    return Graph(pdf, arcs, {0: log_lm}, {n - 1: 0.0})


def union(graphs: Sequence[Graph]) -> Graph:
    """The union of graphs with disjoint state sets: a path of the union is a path of one of them."""
    pdf: List[int] = []
    arcs: List[Tuple[int, int, float]] = []
    init: Dict[int, float] = {}
    final: Dict[int, float] = {}
    for g in graphs:
        off = len(pdf)
        pdf.extend(g.pdf)
        arcs.extend((i + off, j + off, w) for i, j, w in g.arcs)
        init.update({j + off: w for j, w in g.init.items()})
        final.update({j + off: w for j, w in g.final.items()})
    return Graph(pdf, arcs, init, final)


def forward_backward(g: Graph, loglik: Sequence[Sequence[float]], kappa: float):
    """Return (ln Z, gamma) for the graph g, where gamma[t][p] is the posterior of pdf p
    at frame t. Raise ValueError if Z = 0 (no path of g has T frames)."""
    T, n = len(loglik), len(g.pdf)
    P = len(loglik[0])
    emit = [[kappa * loglik[t][g.pdf[j]] for j in range(n)] for t in range(T)]
    alpha = [[NEG_INF] * n for _ in range(T)]
    for j, w in g.init.items():
        alpha[0][j] = w + emit[0][j]  # @line L2
    for t in range(1, T):
        for j in range(n):
            alpha[t][j] = log_sum([alpha[t - 1][i] + w for i, w in g.incoming[j]]) + emit[t][j]
    log_z = log_sum([alpha[T - 1][j] + w for j, w in g.final.items()])  # @line L3
    if log_z == NEG_INF:
        raise ValueError("the graph has no path of this length")
    beta = [[NEG_INF] * n for _ in range(T)]
    for j, w in g.final.items():
        beta[T - 1][j] = w  # @line L4
    for t in range(T - 2, -1, -1):
        for i in range(n):
            beta[t][i] = log_sum([w + emit[t + 1][j] + beta[t + 1][j] for j, w in g.outgoing[i]])
    gamma = [[0.0] * P for _ in range(T)]
    for t in range(T):
        for j in range(n):
            if alpha[t][j] > NEG_INF and beta[t][j] > NEG_INF:
                gamma[t][g.pdf[j]] += math.exp(alpha[t][j] + beta[t][j] - log_z)  # @line L5
    return log_z, gamma


def mmi_objective_and_grad(loglik: Sequence[Sequence[float]], num: Graph, den: Graph, kappa: float = 1.0):
    """Return (F, grad, gamma_num, gamma_den) for one utterance. F = ln Z_num - ln Z_den,
    grad[t][p] = dF / d loglik[t][p] = kappa (gamma_num[t][p] - gamma_den[t][p])."""
    results = [forward_backward(g, loglik, kappa) for g in (num, den)]  # @line L1
    (lz_num, g_num), (lz_den, g_den) = results
    F = lz_num - lz_den  # @line L6
    P = len(loglik[0])
    grad = [[kappa * (g_num[t][p] - g_den[t][p]) for p in range(P)] for t in range(len(loglik))]  # @line L7
    return F, grad, g_num, g_den  # @line L8


def mmi_objective(loglik: Sequence[Sequence[float]], num: Graph, den: Graph, kappa: float = 1.0) -> float:
    return forward_backward(num, loglik, kappa)[0] - forward_backward(den, loglik, kappa)[0]


def brute_force_log_z(g: Graph, loglik: Sequence[Sequence[float]], kappa: float) -> float:
    """ln Z by listing every path of T states, one by one. Only for small graphs."""
    T = len(loglik)
    terms: List[float] = []

    def walk(j: int, t: int, s: float) -> None:
        s += kappa * loglik[t][g.pdf[j]]
        if t == T - 1:
            if j in g.final:
                terms.append(s + g.final[j])
            return
        for k, w in g.outgoing[j]:
            walk(k, t + 1, s + w)

    for j, w in g.init.items():
        walk(j, 0, w)
    return log_sum(terms)


# ---------------------------------------------------------------- discrete output distributions and extended Baum-Welch


def discrete_loglik(b: Sequence[Sequence[float]], obs: Sequence[int]) -> List[List[float]]:
    """loglik[t][p] = ln b[p][obs[t]] for discrete output distributions b[p][v]."""
    return [[math.log(b[p][v]) for p in range(len(b))] for v in obs]


def ebw_counts(data, b, kappa: float = 1.0):
    """Sum over the utterances (obs, num, den) of the numerator and denominator
    counts c[p][v] = sum of gamma[t][p] over the frames t with obs[t] = v, and the
    total objective."""
    P, V = len(b), len(b[0])
    c_num = [[0.0] * V for _ in range(P)]
    c_den = [[0.0] * V for _ in range(P)]
    total = 0.0
    for obs, num, den in data:
        F, _, g_num, g_den = mmi_objective_and_grad(discrete_loglik(b, obs), num, den, kappa)
        total += F
        for t, v in enumerate(obs):
            for p in range(P):
                c_num[p][v] += kappa * g_num[t][p]
                c_den[p][v] += kappa * g_den[t][p]
    return total, c_num, c_den


def ebw_update(b, c_num, c_den, D: float):
    """The extended Baum-Welch update of discrete distributions:
    b'[p][v] = (c_num[p][v] - c_den[p][v] + D b[p][v]) / (sum over v of the same).
    Raise ValueError if D is too small to keep every value positive."""
    out = []
    for p in range(len(b)):
        row = [c_num[p][v] - c_den[p][v] + D * b[p][v] for v in range(len(b[p]))]
        if min(row) <= 0:
            raise ValueError("D is too small: a probability would not be positive")
        s = math.fsum(row)
        out.append([x / s for x in row])
    return out


def smallest_safe_d(b, c_num, c_den) -> float:
    """The smallest D that keeps every updated value positive (each row separately
    would need less; this is one D for all)."""
    need = 0.0
    for p in range(len(b)):
        for v in range(len(b[p])):
            need = max(need, (c_den[p][v] - c_num[p][v]) / b[p][v])
    return need
