# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cpg-island-detection/. The authors are listed in prov/0S3A9K.jsonl.
"""CpG island detection with a two-state HMM and with a sliding window rule.

The HMM has the states "+" (island) and "-" (background). Each state emits
the next base with a probability that may depend on the previous base, so it
is the two-state form of the eight-state CpG model of Durbin, Eddy, Krogh and
Mitchison (1998, chapter 3). A model is CpgModel(start, trans, first, cond):
- start[k] is the probability that the first base is in state k;
- trans[j][k] is the probability of the step from state j to state k;
- first[k][b] is the probability that state k emits b as the first base;
- cond[k][p][b] is the probability that state k emits b after the base p.

viterbi_cpg works in log space, so long sequences do not underflow. Ties go to
the state that comes first in STATES.

window_islands is the rule of Gardiner-Garden and Frommer (1987): every window
of w bases with GC fraction above min_gc and observed over expected CpG above
min_oe is marked, and overlapping marked windows are joined.

All intervals are 0-based and half-open.
"""

from __future__ import annotations

import math
from collections import namedtuple
from typing import Dict, List, Tuple

STATES = ("+", "-")
BASES = "ACGT"

CpgModel = namedtuple("CpgModel", ["start", "trans", "first", "cond"])


def _log(p: float) -> float:
    return math.log(p) if p > 0 else -math.inf


def composition_model(gc_plus: float = 0.65, gc_minus: float = 0.4, cg_minus: float = 0.25,
                      stay_plus: float = 0.999, stay_minus: float = 0.9999) -> CpgModel:
    """A simple model for tests and examples, not fitted to any genome.

    The island state emits C and G with probability gc_plus/2 each. The
    background state emits C and G with probability gc_minus/2 each, but after
    a C it multiplies the probability of G by cg_minus and renormalizes, which
    makes CG rare in the background, as in vertebrate DNA.
    """
    def comp(gc):
        return {"A": (1 - gc) / 2, "C": gc / 2, "G": gc / 2, "T": (1 - gc) / 2}

    plus, minus = comp(gc_plus), comp(gc_minus)
    after_c = dict(minus)
    after_c["G"] *= cg_minus
    z = sum(after_c.values())
    after_c = {b: v / z for b, v in after_c.items()}
    cond = {"+": {p: dict(plus) for p in BASES},
            "-": {p: (after_c if p == "C" else dict(minus)) for p in BASES}}
    trans = {"+": {"+": stay_plus, "-": 1 - stay_plus}, "-": {"+": 1 - stay_minus, "-": stay_minus}}
    return CpgModel({"+": 0.5, "-": 0.5}, trans, {"+": plus, "-": minus}, cond)


def path_log_prob(seq: str, path: str, model: CpgModel) -> float:
    """ln P(seq, path) under the model."""
    lp = _log(model.start[path[0]]) + _log(model.first[path[0]][seq[0]])
    for i in range(1, len(seq)):
        lp += _log(model.trans[path[i - 1]][path[i]]) + _log(model.cond[path[i]][seq[i - 1]][seq[i]])
    return lp


def viterbi_cpg(seq: str, model: CpgModel) -> Tuple[float, str]:
    """The most probable state path, as (ln P(seq, path), path string over "+-")."""
    s = seq.upper()
    if not s or any(c not in BASES for c in s):
        raise ValueError("seq must be a non-empty string over ACGT")
    lt = {j: {k: _log(model.trans[j][k]) for k in STATES} for j in STATES}
    V = {k: _log(model.start[k]) + _log(model.first[k][s[0]]) for k in STATES}  # @line L1
    ptr: List[Dict[str, str]] = [{}]
    for i in range(1, len(s)):  # @line L2
        new, back = {}, {}
        for k in STATES:  # @line L3
            best = max(STATES, key=lambda j: (V[j] + lt[j][k], -STATES.index(j)))  # @line L4
            back[k] = best
            new[k] = V[best] + lt[best][k] + _log(model.cond[k][s[i - 1]][s[i]])  # @line L5
        V = new  # @line L6
        ptr.append(back)
    q = max(STATES, key=lambda k: (V[k], -STATES.index(k)))  # @line L7
    score = V[q]
    path = [q]
    for i in range(len(s) - 1, 0, -1):  # @line L8
        q = ptr[i][q]
        path.append(q)
    path.reverse()
    return score, "".join(path)


def runs(path: str, state: str = "+") -> List[Tuple[int, int]]:
    """The maximal runs of state in path, as half-open intervals."""
    out, i = [], 0
    while i < len(path):
        if path[i] == state:
            j = i
            while j < len(path) and path[j] == state:
                j += 1
            out.append((i, j))
            i = j
        else:
            i += 1
    return out


def hmm_islands(seq: str, model: CpgModel, min_len: int = 1) -> List[Tuple[int, int]]:
    """The islands of the Viterbi path that have at least min_len bases."""
    _, path = viterbi_cpg(seq, model)
    return [r for r in runs(path) if r[1] - r[0] >= min_len]  # @line L9


def obs_exp_cpg(c: int, g: int, cg: int, n: int) -> float:
    """Observed over expected CpG, CG * n / (C * G); 0.0 if C or G is 0."""
    return cg * n / (c * g) if c and g else 0.0


def window_flags(seq: str, w: int = 200, min_gc: float = 0.5, min_oe: float = 0.6) -> List[bool]:
    """flags[i] is True if the window seq[i:i + w] passes both tests."""
    s = seq.upper()
    if w < 2 or w > len(s):
        return []
    c, g = s[:w].count("C"), s[:w].count("G")
    cg = sum(1 for j in range(w - 1) if s[j] == "C" and s[j + 1] == "G")
    flags = []
    for i in range(len(s) - w + 1):  # @line L10
        if i > 0:
            out, inn = s[i - 1], s[i + w - 1]
            c += (inn == "C") - (out == "C")
            g += (inn == "G") - (out == "G")
            cg += (s[i + w - 2] == "C" and inn == "G") - (out == "C" and s[i] == "G")
        flags.append((c + g) / w > min_gc and obs_exp_cpg(c, g, cg, w) > min_oe)  # @line L11
    return flags


def window_islands(seq: str, w: int = 200, min_gc: float = 0.5,
                   min_oe: float = 0.6) -> List[Tuple[int, int]]:
    """The unions of overlapping marked windows, as half-open intervals."""
    out: List[Tuple[int, int]] = []
    for i, ok in enumerate(window_flags(seq, w, min_gc, min_oe)):
        if ok:
            if out and i <= out[-1][1]:
                out[-1] = (out[-1][0], i + w)
            else:
                out.append((i, i + w))
    return out  # @line L12
