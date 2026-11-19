# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lattice-free-mmi/. The authors are listed in prov/JBKG30.jsonl.

"""Lattice-free MMI (LF-MMI): the objective and gradient of the chain model.

The network gives y[t][p], one output per pdf and frame (at the reduced frame
rate). LF-MMI uses y directly as a log likelihood: there is no division by the
pdf priors and no acoustic scale. The objective of one chunk is

    F = ln Z_num - ln Z_den - (c / 2) * sum of y[t][p]^2,

where Z_num sums over the paths of the reference phone sequence (each phone
inside a window of frames around its position in a reference alignment) and
Z_den sums over the paths of a phone n-gram graph that is the same for every
chunk. The gradient is dF/dy[t][p] = gamma_num[t][p] - gamma_den[t][p] - c y[t][p].

Each phone has two pdfs: the pdf of its first frame and the pdf of its self
loop. The topology can be traversed in one frame. Here the phone language
model is a bigram; Povey et al. (2016) use a 4-gram. The numerator takes its
weights from the denominator graph, so that F <= 0.

The denominator forward-backward runs on probabilities with a scale per frame,
as on a GPU; the numerator runs in log space. All logs are natural logs.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

from nlslog import NEG_INF, log_sum


@dataclass
class Graph:
    """An HMM graph of emitting states. pdf[j] is the pdf id of state j. If window is
    given, state j may be occupied only at frames window[j][0]..window[j][1]."""

    pdf: List[int]
    arcs: List[Tuple[int, int, float]]
    init: Dict[int, float]
    final: Dict[int, float]
    window: Optional[List[Tuple[int, int]]] = None
    incoming: List[List[Tuple[int, float]]] = field(init=False)
    outgoing: List[List[Tuple[int, float]]] = field(init=False)

    def __post_init__(self):
        n = len(self.pdf)
        self.incoming = [[] for _ in range(n)]
        self.outgoing = [[] for _ in range(n)]
        for i, j, w in self.arcs:
            self.incoming[j].append((i, w))
            self.outgoing[i].append((j, w))

    def allowed(self, t: int, j: int) -> bool:
        return self.window is None or self.window[j][0] <= t <= self.window[j][1]


def first_pdf(phone: int) -> int:
    return 2 * phone


def loop_pdf(phone: int) -> int:
    return 2 * phone + 1


def numerator_graph(phones: Sequence[int], den: Graph, windows: Optional[Sequence[Tuple[int, int]]] = None) -> Graph:
    """The chain topology for a phone sequence. Phone k has a first state (pdf
    first_pdf) and a loop state (pdf loop_pdf); either may end the graph after the
    last phone. The weights are those of the same states and arcs of the
    denominator graph den (from denominator_graph), so every numerator path is a
    denominator path with the same score and F <= 0. windows[k] = (lo, hi) limits
    the frames of phone k."""
    den_arc = {(i, j): w for i, j, w in den.arcs}
    pdf: List[int] = []
    arcs: List[Tuple[int, int, float]] = []
    win: List[Tuple[int, int]] = []
    n = len(phones)
    for k, ph in enumerate(phones):
        f, s = 2 * k, 2 * k + 1
        pdf += [first_pdf(ph), loop_pdf(ph)]
        arcs += [(f, s, den_arc[(2 * ph, 2 * ph + 1)]), (s, s, den_arc[(2 * ph + 1, 2 * ph + 1)])]
        if k + 1 < n:
            nx = 2 * phones[k + 1]
            if (2 * ph, nx) not in den_arc:
                raise ValueError("the phone bigram does not allow this phone sequence")
            arcs += [(f, f + 2, den_arc[(2 * ph, nx)]), (s, f + 2, den_arc[(2 * ph + 1, nx)])]
        if windows is not None:
            win += [windows[k], windows[k]]
    if 2 * phones[0] not in den.init:
        raise ValueError("the first phone has no initial probability")
    final = {2 * n - 2: den.final[2 * phones[-1]], 2 * n - 1: den.final[2 * phones[-1] + 1]}
    return Graph(pdf, arcs, {0: den.init[2 * phones[0]]}, final, win if windows is not None else None)


def estimate_phone_bigram(sequences: Sequence[Sequence[int]], n_phones: int):
    """Unsmoothed bigram from phone sequences: (start[a], bigram[a][b]) as
    probabilities. A phone that is never followed by another gets a uniform row."""
    start = [0.0] * n_phones
    count = [[0.0] * n_phones for _ in range(n_phones)]
    for seq in sequences:
        start[seq[0]] += 1
        for a, b in zip(seq, seq[1:]):
            count[a][b] += 1
    start = [x / len(sequences) for x in start]
    bigram = []
    for row in count:
        s = sum(row)
        bigram.append([x / s for x in row] if s > 0 else [1.0 / n_phones] * n_phones)
    return start, bigram


def denominator_graph(start: Sequence[float], bigram: Sequence[Sequence[float]], steps: int = 100) -> Graph:
    """The phone bigram composed with the chain topology. State 2a is the first state
    of phone a and 2a+1 its loop state, so the state of a phone also remembers it as
    the history of the bigram. From either state of a, stay in the loop state with
    0.5, or go to the first state of b with 0.5 * bigram[a][b]. The initial
    probabilities are the average of the state distributions over the first `steps`
    frames, starting from start[]. Every final weight is 1."""
    P = len(bigram)
    pdf = [first_pdf(a) if j % 2 == 0 else loop_pdf(a) for a in range(P) for j in (0, 1)]
    prob_arcs: List[Tuple[int, int, float]] = []
    for a in range(P):
        for i in (2 * a, 2 * a + 1):
            prob_arcs.append((i, 2 * a + 1, 0.5))
            for b in range(P):
                if bigram[a][b] > 0:
                    prob_arcs.append((i, 2 * b, 0.5 * bigram[a][b]))
    dist = [0.0] * (2 * P)
    for a in range(P):
        dist[2 * a] = start[a]
    avg = [0.0] * (2 * P)
    for _ in range(steps):
        avg = [x + d / steps for x, d in zip(avg, dist)]
        nxt = [0.0] * (2 * P)
        for i, j, w in prob_arcs:
            nxt[j] += dist[i] * w
        dist = nxt
    arcs = [(i, j, math.log(w)) for i, j, w in prob_arcs]
    init = {j: math.log(x) for j, x in enumerate(avg) if x > 0}
    final = {j: 0.0 for j in range(2 * P)}
    return Graph(pdf, arcs, init, final)


def leaky_init(g: Graph) -> List[float]:
    """The initial probabilities of g as a list (0 for the states without one)."""
    return [math.exp(g.init[j]) if j in g.init else 0.0 for j in range(len(g.pdf))]


def forward_backward_log(g: Graph, y: Sequence[Sequence[float]]):
    """Log-space forward-backward (used for the numerator). Return (ln Z, gamma)."""
    T, n, P = len(y), len(g.pdf), len(y[0])
    emit = [[y[t][g.pdf[j]] if g.allowed(t, j) else NEG_INF for j in range(n)] for t in range(T)]
    alpha = [[NEG_INF] * n for _ in range(T)]
    for j, w in g.init.items():
        alpha[0][j] = w + emit[0][j]
    for t in range(1, T):
        for j in range(n):
            alpha[t][j] = log_sum([alpha[t - 1][i] + w for i, w in g.incoming[j]]) + emit[t][j]
    log_z = log_sum([alpha[T - 1][j] + w for j, w in g.final.items()])
    if log_z == NEG_INF:
        raise ValueError("the graph has no path of this length")
    beta = [[NEG_INF] * n for _ in range(T)]
    for j, w in g.final.items():
        beta[T - 1][j] = w
    for t in range(T - 2, -1, -1):
        for i in range(n):
            beta[t][i] = log_sum([w + emit[t + 1][j] + beta[t + 1][j] for j, w in g.outgoing[i]])
    gamma = [[0.0] * P for _ in range(T)]
    for t in range(T):
        for j in range(n):
            if alpha[t][j] > NEG_INF and beta[t][j] > NEG_INF:
                gamma[t][g.pdf[j]] += math.exp(alpha[t][j] + beta[t][j] - log_z)
    return log_z, gamma


def forward_backward_scaled(g: Graph, y: Sequence[Sequence[float]], leaky: float = 0.0):
    """Probability-space forward-backward with a scale per frame (used for the
    denominator). With leaky = eta > 0, each frame may also jump from any state to
    any state j with probability eta * init(j) (the leaky HMM). Return (ln Z, gamma)."""
    T, n, P = len(y), len(g.pdf), len(y[0])
    init = leaky_init(g)
    shift = [max(row) for row in y]
    e = [[math.exp(y[t][g.pdf[j]] - shift[t]) for j in range(n)] for t in range(T)]  # @line L2
    w_in = [[(i, math.exp(w)) for i, w in g.incoming[j]] for j in range(n)]
    w_out = [[(j, math.exp(w)) for j, w in g.outgoing[i]] for i in range(n)]
    final = [math.exp(g.final[j]) if j in g.final else 0.0 for j in range(n)]
    alpha = [[0.0] * n for _ in range(T)]
    c = [0.0] * T
    a = [init[j] * e[0][j] for j in range(n)]
    for t in range(T):
        if t > 0:
            total = math.fsum(alpha[t - 1])
            a = [(math.fsum(alpha[t - 1][i] * w for i, w in w_in[j]) + leaky * init[j] * total) * e[t][j] for j in range(n)]  # @line L3
        c[t] = math.fsum(a)
        if c[t] == 0.0:
            raise ValueError("the graph has no path of this length")
        alpha[t] = [x / c[t] for x in a]  # @line L4
    end = math.fsum(alpha[T - 1][j] * final[j] for j in range(n))
    if end == 0.0:
        raise ValueError("the graph has no path of this length")
    log_z = math.fsum(math.log(c[t]) + shift[t] for t in range(T)) + math.log(end)  # @line L5
    beta = [[0.0] * n for _ in range(T)]
    beta[T - 1] = final[:]
    for t in range(T - 2, -1, -1):
        nb = [e[t + 1][j] * beta[t + 1][j] for j in range(n)]
        leak = leaky * math.fsum(init[j] * nb[j] for j in range(n))
        beta[t] = [(math.fsum(w * nb[j] for j, w in w_out[i]) + leak) / c[t + 1] for i in range(n)]  # @line L6
    gamma = [[0.0] * P for _ in range(T)]
    for t in range(T):
        for j in range(n):
            gamma[t][g.pdf[j]] += alpha[t][j] * beta[t][j] / end  # @line L7
    return log_z, gamma


def lfmmi_objective_and_grad(y: Sequence[Sequence[float]], num: Graph, den: Graph, leaky: float = 0.1, l2: float = 0.0):
    """Return (F, grad, gamma_num, gamma_den) for one chunk."""
    lz_num, g_num = forward_backward_log(num, y)  # @line L1
    lz_den, g_den = forward_backward_scaled(den, y, leaky)
    T, P = len(y), len(y[0])
    F = lz_num - lz_den - 0.5 * l2 * math.fsum(v * v for row in y for v in row)  # @line L8
    grad = [[g_num[t][p] - g_den[t][p] - l2 * y[t][p] for p in range(P)] for t in range(T)]
    return F, grad, g_num, g_den  # @line L9


def lfmmi_objective(y, num, den, leaky: float = 0.1, l2: float = 0.0) -> float:
    return lfmmi_objective_and_grad(y, num, den, leaky, l2)[0]


# ---------------------------------------------------------------- reference versions for the tests


def with_leaky_arcs(g: Graph, leaky: float) -> Graph:
    """The same graph with an explicit arc i -> j of weight leaky * init(j) for every
    pair of states. It has the same Z as the leaky HMM."""
    if leaky <= 0:
        return g
    arcs = list(g.arcs)
    for i in range(len(g.pdf)):
        for j, w in g.init.items():
            arcs.append((i, j, math.log(leaky) + w))
    return Graph(list(g.pdf), arcs, dict(g.init), dict(g.final), g.window)


def brute_force_log_z(g: Graph, y: Sequence[Sequence[float]]) -> float:
    """ln Z by listing every path of T states. Only for small graphs."""
    T = len(y)
    terms: List[float] = []

    def walk(j: int, t: int, s: float) -> None:
        if not g.allowed(t, j):
            return
        s += y[t][g.pdf[j]]
        if t == T - 1:
            if j in g.final:
                terms.append(s + g.final[j])
            return
        for k, w in g.outgoing[j]:
            walk(k, t + 1, s + w)

    for j, w in g.init.items():
        walk(j, 0, w)
    return log_sum(terms)
