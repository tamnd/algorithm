# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-hmm-gene-finder/. The authors are listed in prov/FHW813.jsonl.
"""Viterbi decoding of a generalized HMM (GHMM), and a small gene model for it.

A GHMM explains x[0:n] as a parse: a list of segments (q, a, b) that cover
0..n in order, where state q emits the whole segment x[a:b]. A model is a
Ghmm with these fields (all probabilities are given as natural logarithms,
and -math.inf means "impossible"):
- states: the names of the states, indexed 0..K-1;
- log_start[q]: ln of the probability that the first segment has state q;
- log_trans[p][q]: ln of the probability that a segment of state p is
  followed by a segment of state q;
- log_end[q]: ln of the weight of a parse whose last segment has state q
  (use 0.0 for every state to let any state end the sequence);
- max_dur[q]: the largest segment length of state q;
- log_dur(q, l): ln of the probability that a segment of state q has length l;
- log_seg(q, a, b): ln of the probability that state q emits x[a:b] as a
  segment of length b - a.

The score of a parse is log_start of its first state, plus log_trans of each
step, plus log_dur and log_seg of each segment, plus log_end of its last
state. ghmm_viterbi returns a parse of largest score. Ties go to the smaller
length, then to the smaller state index.

toy_gene_model(x) builds a GHMM with the states N (intergenic), E (exon,
three-periodic composition) and I (intron, GT at the start and AG at the
end) whose log_seg takes O(1) time by prefix sums.
"""

from __future__ import annotations

import math
from collections import namedtuple
from typing import Callable, Dict, List, Optional, Sequence, Tuple

NEG = -math.inf

Ghmm = namedtuple("Ghmm", ["states", "log_start", "log_trans", "log_end",
                           "max_dur", "log_dur", "log_seg"])

Segment = Tuple[str, int, int]


def parse_score(model: Ghmm, parse: Sequence[Segment]) -> float:
    """The score of a parse given as (state name, a, b) segments."""
    idx = {s: i for i, s in enumerate(model.states)}
    total, prev = 0.0, None
    for name, a, b in parse:
        q = idx[name]
        if b - a < 1 or b - a > model.max_dur[q]:
            return NEG
        total += model.log_start[q] if prev is None else model.log_trans[prev][q]
        total += model.log_dur(q, b - a) + model.log_seg(q, a, b)
        prev = q
    return total + model.log_end[prev]


def ghmm_viterbi(model: Ghmm, n: int) -> Tuple[float, Optional[List[Segment]]]:
    """A parse of x[0:n] of largest score, as (score, segments), or (-inf, None)."""
    K = len(model.states)
    gamma = [[NEG] * K for _ in range(n + 1)]  # best parse of x[0:b] whose last segment is q
    back_len = [[0] * K for _ in range(n + 1)]
    delta = [[NEG] * K for _ in range(n + 1)]  # best way to start a segment of q at b
    delta_arg = [[-1] * K for _ in range(n + 1)]
    for b in range(1, n + 1):  # @line L1
        for q in range(K):  # @line L2
            best, best_l = NEG, 0  # @line L3
            for l in range(1, min(model.max_dur[q], b) + 1):  # @line L4
                enter = model.log_start[q] if l == b else delta[b - l][q]  # @line L5
                if enter == NEG:
                    continue
                s = enter + model.log_dur(q, l) + model.log_seg(q, b - l, b)  # @line L6
                if s > best:  # @line L7
                    best, best_l = s, l
            gamma[b][q], back_len[b][q] = best, best_l
        for q in range(K):  # @line L8
            bp, bv = -1, NEG
            for p in range(K):
                v = gamma[b][p] + model.log_trans[p][q]
                if v > bv:
                    bp, bv = p, v
            delta[b][q], delta_arg[b][q] = bv, bp
    end_q, end_v = -1, NEG
    for q in range(K):  # @line L9
        v = gamma[n][q] + model.log_end[q]
        if v > end_v:
            end_q, end_v = q, v
    if end_q < 0:
        return NEG, None
    parse: List[Segment] = []
    b, q = n, end_q
    while b > 0:  # @line L10
        l = back_len[b][q]
        parse.append((model.states[q], b - l, b))
        b, q = b - l, (delta_arg[b - l][q] if b - l > 0 else -1)
    parse.reverse()
    return end_v, parse  # @line L11


# ---------------------------------------------------------------- a toy gene model


def _logs(dist: Dict[str, float]) -> Dict[str, float]:
    return {k: (math.log(v) if v > 0 else NEG) for k, v in dist.items()}


def _prefix(x: str, logp: Callable[[int, str], float]) -> List[float]:
    out = [0.0]
    for i, c in enumerate(x):
        out.append(out[-1] + logp(i, c))
    return out


def toy_gene_model(x: str, intergenic: Dict[str, float], intron: Dict[str, float],
                   exon_phases: Sequence[Dict[str, float]], max_dur: int = 200,
                   min_exon: int = 3, min_intron: int = 4,
                   p_exon_to_intron: float = 0.5) -> Ghmm:
    """A forward-strand gene model with the states N, E and I.

    - N emits bases independently with the probabilities intergenic.
    - E emits base j of the segment with exon_phases[j % 3] (three-periodic,
      the phase restarts at each exon), and has length at least min_exon.
    - I emits bases with intron, must start with GT and end with AG, and has
      length at least min_intron.
    Every state has a uniform length distribution on its allowed lengths up to
    max_dur. A parse starts and ends in N, and goes N -> E -> (I -> E)* -> N.
    """
    s = x.upper()
    ln_n, ln_i = _logs(intergenic), _logs(intron)
    ln_e = [_logs(d) for d in exon_phases]
    pre_n = _prefix(s, lambda i, c: ln_n[c])
    pre_i = _prefix(s, lambda i, c: ln_i[c])
    # pre_e[r][i] sums the exon log probabilities of x[0:i] for an exon that starts at a position = r mod 3.
    pre_e = [_prefix(s, lambda i, c, r=r: ln_e[(i - r) % 3][c]) for r in range(3)]
    lo = [1, min_exon, min_intron]

    def log_seg(q: int, a: int, b: int) -> float:
        if q == 0:
            return pre_n[b] - pre_n[a]
        if q == 1:
            return pre_e[a % 3][b] - pre_e[a % 3][a]
        if s[a:a + 2] != "GT" or s[b - 2:b] != "AG":
            return NEG
        return pre_i[b] - pre_i[a]

    def log_dur(q: int, l: int) -> float:
        if l < lo[q]:
            return NEG
        return -math.log(max_dur - lo[q] + 1)

    ln = lambda p: math.log(p) if p > 0 else NEG
    trans = [[NEG, 0.0, NEG],
             [ln(1 - p_exon_to_intron), NEG, ln(p_exon_to_intron)],
             [NEG, 0.0, NEG]]
    return Ghmm(("N", "E", "I"), [0.0, NEG, NEG], trans, [0.0, NEG, NEG],
                [max_dur] * 3, log_dur, log_seg)
