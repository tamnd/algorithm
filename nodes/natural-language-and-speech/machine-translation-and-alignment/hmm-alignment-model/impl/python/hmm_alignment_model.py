# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hmm-alignment-model/. The authors are listed in prov/S290AK.jsonl.

"""The HMM alignment model (Vogel, Ney and Tillmann 1996) with the null word
extension of Och and Ney (2003), trained by EM with forward-backward in log space.

A pair is (f, e): the generated sentence f = f_1 .. f_m and the given sentence
e = e_1 .. e_l. An alignment a has a_j in 0 .. l, with 0 for the null word.

    p(f, a | e) = prod_j p(a_j | r_{j-1}, l) t(f_j | e_{a_j})

where r_j is the last real position aligned at or before j (r_0 = 0, a virtual
position in front of the sentence). With p0 the null probability,

    p(a_j = i | r, l) = (1 - p0) c(i - r) / sum_{i'=1..l} c(i' - r)   for i >= 1
    p(a_j = 0 | r, l) = p0

c maps a jump width d to a weight c(d) >= 0. With null=False, p0 = 0.

The hidden states are the real positions 1 .. l and, with null=True, one null
state for each remembered position r = 0 .. l. A state path with nonzero
probability is fixed by the alignment, so sums over paths are sums over alignments.
"""

import math
from collections import defaultdict
from typing import Dict, List, Sequence, Tuple

from nlslog import NEG_INF, argmax, log_sum, safe_log

NULL = "<null>"
Pair = Tuple[Sequence[str], Sequence[str]]


def uniform_t(corpus: Sequence[Pair]) -> Dict[Tuple[str, str], float]:
    vf = sorted({x for f, _ in corpus for x in f})
    ve = sorted({y for _, e in corpus for y in e}) + [NULL]
    return {(x, y): 1.0 / len(vf) for x in vf for y in ve}


def uniform_c(corpus: Sequence[Pair]) -> Dict[int, float]:
    """c(d) = 1 for every jump width d that can occur: -(L - 1) .. L for the longest e."""
    lmax = max(len(e) for _, e in corpus)
    return {d: 1.0 for d in range(-(lmax - 1), lmax + 1)}


def states(l: int, null: bool) -> List[Tuple[str, int]]:
    """('w', i) for the real positions, ('n', r) for the null states."""
    out = [("w", i) for i in range(1, l + 1)]
    if null:
        out += [("n", r) for r in range(0, l + 1)]
    return out


def log_jump_row(r: int, l: int, c: Dict[int, float], p0: float, null: bool) -> Dict[Tuple[str, int], float]:
    """ln p(next state | remembered position r): the row of the transition matrix."""
    z = sum(c.get(i - r, 0.0) for i in range(1, l + 1))
    row = {}
    for i in range(1, l + 1):
        row[("w", i)] = safe_log(1 - p0) + safe_log(c.get(i - r, 0.0)) - math.log(z) if z > 0 else NEG_INF
    if null:
        row[("n", r)] = safe_log(p0)
    return row


def _model(f, e, t, c, p0, null):
    l = len(e)
    ss = states(l, null)
    rows = {r: log_jump_row(r, l, c, p0, null) for r in range(0, l + 1)}
    es = [NULL] + list(e)

    def emit(j, s):
        word = es[s[1]] if s[0] == "w" else NULL
        return safe_log(t.get((f[j], word), 0.0))

    def trans(s_prev, s):
        return rows[s_prev[1]].get(s, NEG_INF)

    return ss, rows, emit, trans


def forward_backward(f, e, t, c, p0=0.2, null=True):
    """Log-space forward and backward tables (lists over j of dicts over states) and ln p(f | e)."""
    ss, rows, emit, trans = _model(f, e, t, c, p0, null)
    m = len(f)
    alpha = [{s: rows[0].get(s, NEG_INF) + emit(0, s) for s in ss}]  # @line L2
    for j in range(1, m):
        alpha.append({s: emit(j, s) + log_sum(alpha[j - 1][q] + trans(q, s) for q in ss) for s in ss})
    beta = [None] * m  # @line L3
    beta[m - 1] = {s: 0.0 for s in ss}
    for j in range(m - 2, -1, -1):
        beta[j] = {q: log_sum(trans(q, s) + emit(j + 1, s) + beta[j + 1][s] for s in ss) for q in ss}
    logp = log_sum(alpha[m - 1].values())  # @line L4
    return alpha, beta, logp


def log_likelihood(corpus: Sequence[Pair], t, c, p0=0.2, null=True) -> float:
    return sum(forward_backward(f, e, t, c, p0, null)[2] for f, e in corpus)


def expected_counts(corpus: Sequence[Pair], t, c, p0=0.2, null=True):
    """The E step: link counts for t and jump counts N[(r, i, l)] into real positions."""
    ct: Dict[Tuple[str, str], float] = defaultdict(float)
    nj: Dict[Tuple[int, int, int], float] = defaultdict(float)
    for f, e in corpus:  # @line L1
        l, m = len(e), len(f)
        es = [NULL] + list(e)
        alpha, beta, logp = forward_backward(f, e, t, c, p0, null)
        ss, rows, emit, trans = _model(f, e, t, c, p0, null)
        for j in range(m):
            for s in ss:
                g = math.exp(alpha[j][s] + beta[j][s] - logp)  # @line L5
                if g > 0:
                    ct[(f[j], es[s[1]] if s[0] == "w" else NULL)] += g
        for i in range(1, l + 1):  # the first word, from the virtual position 0
            g = math.exp(rows[0][("w", i)] + emit(0, ("w", i)) + beta[0][("w", i)] - logp)
            nj[(0, i, l)] += g
        for j in range(1, m):
            for q in ss:
                for i in range(1, l + 1):
                    s = ("w", i)
                    x = alpha[j - 1][q] + trans(q, s) + emit(j, s) + beta[j][s] - logp  # @line L6
                    if x > NEG_INF:
                        nj[(q[1], i, l)] += math.exp(x)
    return ct, nj


def jump_objective(nj, c) -> float:
    """The part of the expected complete-data log likelihood that depends on c."""
    total = 0.0
    for (r, i, l), n in nj.items():
        if n <= 0:
            continue
        z = sum(c.get(k - r, 0.0) for k in range(1, l + 1))
        w = c.get(i - r, 0.0)
        if w <= 0 or z <= 0:
            return NEG_INF
        total += n * (math.log(w) - math.log(z))
    return total


def count_update(nj, c) -> Dict[int, float]:
    """c(d) proportional to the expected number of jumps of width d. Simple, but not the
    exact M step, because the rows r have different normalizers."""
    cand = {d: 0.0 for d in c}
    for (r, i, l), n in nj.items():
        cand[i - r] = cand.get(i - r, 0.0) + n
    s = sum(cand.values())
    return {d: v / s for d, v in cand.items()} if s > 0 else dict(c)


def jump_m_step(nj, c, iterations: int = 40) -> Dict[int, float]:
    """Maximize jump_objective over c. In theta = ln c the objective is concave (a linear
    term minus log-sum-exp terms), so gradient ascent works; a step is kept only if it
    raises the objective, so the result is never worse than c."""
    best = dict(c)
    q_best = jump_objective(nj, best)
    cand = count_update(nj, c)  # @line L8
    q_cand = jump_objective(nj, cand)
    if q_cand > q_best:
        best, q_best = cand, q_cand
    theta = {d: (math.log(v) if v > 0 else NEG_INF) for d, v in best.items()}
    rows: Dict[Tuple[int, int], float] = defaultdict(float)
    for (r, i, l), n in nj.items():
        rows[(r, l)] += n
    for _ in range(iterations):
        grad = {d: 0.0 for d in theta}
        for (r, i, l), n in nj.items():
            grad[i - r] += n
        for (r, l), n in rows.items():
            z = log_sum(theta.get(k - r, NEG_INF) for k in range(1, l + 1))
            for k in range(1, l + 1):
                d = k - r
                if theta.get(d, NEG_INF) > NEG_INF:
                    grad[d] -= n * math.exp(theta[d] - z)
        gmax = max(abs(g) for g in grad.values())
        if gmax < 1e-10:
            break
        step = 1.0 / gmax
        for _ in range(30):
            trial = {d: (th + step * grad[d] if th > NEG_INF else th) for d, th in theta.items()}
            c_trial = {d: math.exp(th) if th > NEG_INF else 0.0 for d, th in trial.items()}
            q = jump_objective(nj, c_trial)
            if q > q_best:
                theta, best, q_best = trial, c_trial, q
                break
            step /= 2
        else:
            break
    return best


def em_step(corpus: Sequence[Pair], t, c, p0=0.2, null=True):
    """One generalized EM round. t gets the exact M step; c gets a step that does not
    lower its part of the expected complete-data log likelihood."""
    ct, nj = expected_counts(corpus, t, c, p0, null)
    tot: Dict[str, float] = defaultdict(float)
    for (x, y), v in ct.items():
        tot[y] += v
    new_t = {k: (ct.get(k, 0.0) / tot[k[1]] if tot[k[1]] > 0 else v) for k, v in t.items()}  # @line L7
    new_c = jump_m_step(nj, c)  # @line L9
    return new_t, new_c  # @line L10


def train(corpus: Sequence[Pair], rounds: int, p0=0.2, null=True, t=None, c=None):
    """EM from uniform t and c unless given. Returns t, c and the log likelihoods."""
    t = uniform_t(corpus) if t is None else t
    c = uniform_c(corpus) if c is None else c
    hist = [log_likelihood(corpus, t, c, p0, null)]
    for _ in range(rounds):
        t, c = em_step(corpus, t, c, p0, null)
        hist.append(log_likelihood(corpus, t, c, p0, null))
    return t, c, hist


def viterbi_alignment(f, e, t, c, p0=0.2, null=True) -> Tuple[List[int], float]:
    """The most probable alignment and its log probability; on ties the first state in
    the order real positions 1 .. l, then null states, wins."""
    ss, rows, emit, trans = _model(f, e, t, c, p0, null)
    m = len(f)
    delta = [[rows[0].get(s, NEG_INF) + emit(0, s) for s in ss]]
    back = []
    for j in range(1, m):
        row, bp = [], []
        for s in ss:
            cands = [delta[j - 1][k] + trans(q, s) for k, q in enumerate(ss)]
            k = argmax(cands)
            bp.append(k)
            row.append(cands[k] + emit(j, s))
        delta.append(row)
        back.append(bp)
    k = argmax(delta[m - 1])
    best = delta[m - 1][k]
    path = [k]
    for bp in reversed(back):
        k = bp[k]
        path.append(k)
    path.reverse()
    return [ss[k][1] if ss[k][0] == "w" else 0 for k in path], best
