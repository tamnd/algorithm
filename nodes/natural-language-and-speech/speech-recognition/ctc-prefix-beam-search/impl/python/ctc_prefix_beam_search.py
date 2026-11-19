# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ctc-prefix-beam-search/. The authors are listed in prov/NXHD7B.jsonl.

"""CTC prefix beam search, in log space.

The input is a T x K matrix of log outputs ln y_t(k) of a CTC network. Symbol 0
is the blank, written ∅ on the page and "_" in its examples. A prefix is a
tuple of labels (symbols 1..K-1). For each prefix l the search keeps two log
probabilities:

    b(l)   the total probability of the frame paths so far that collapse to l
           and end in a blank,
    nb(l)  the same for the paths that end in a label (the last label of l).

Their log_add is the probability of l given the frames read so far. A
repeated label needs a blank between its two copies, so extending l by its own
last label uses only b(l), while the paths of nb(l) that read the same label
again stay in l.

An optional language model hook lm(prefix, c) returns the log weight added when
label c is appended to prefix (for example alpha * ln p_LM(c | prefix) + beta).
The search ranks the prefixes by b + nb (log_add) with the weights included.
Every probability is accumulated with log_add. Hannun et al. (2014), Algorithm 1,
write some of these updates as plain assignments, which loses probability.

The code takes the network outputs as given. All logs are natural logs.
"""

import itertools
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from nlslog import NEG_INF, log_add, log_sum

BLANK = 0
Prefix = Tuple[int, ...]


def _no_lm(prefix: Prefix, c: int) -> float:
    return 0.0


def prefix_beam_search(
    log_y: Sequence[Sequence[float]],
    beam: int,
    lm: Optional[Callable[[Prefix, int], float]] = None,
    blank: int = BLANK,
    recover: bool = False,
) -> Tuple[Prefix, float, List[Tuple[Prefix, float]]]:
    """Return (best prefix, its log score, the final beam as (prefix, log score) pairs).

    beam is the number of prefixes kept after each frame. Ties are broken by the
    smaller prefix tuple, so the result does not depend on the order of a dict.

    With recover=True, a prefix l+ that was scored at the previous frame but
    pruned, and is now made again from its parent l, also gets the paths that
    continue its old b and nb (a blank, or its own last label again). This is
    the "l+ not in A_prev" step of Hannun et al. (2014), Algorithm 1. With a
    beam that keeps everything it changes nothing.
    """
    if beam < 1:
        raise ValueError("the beam must keep at least one prefix")
    if len(log_y) == 0:
        raise ValueError("need at least one frame")
    lm = lm or _no_lm
    K = len(log_y[0])
    labels = [c for c in range(K) if c != blank]
    A: Dict[Prefix, Tuple[float, float]] = {(): (0.0, NEG_INF)}  # @line L1
    scored: Dict[Prefix, List[float]] = {}  # every prefix of the previous frame, before pruning
    for row in log_y:  # @line L2
        N: Dict[Prefix, List[float]] = {}  # @line L3

        def acc(p: Prefix, which: int, v: float) -> None:
            cell = N.setdefault(p, [NEG_INF, NEG_INF])
            cell[which] = log_add(cell[which], v)

        for l, (b, nb) in A.items():  # @line L4
            acc(l, 0, row[blank] + log_add(b, nb))  # @line L5
            if l:
                acc(l, 1, row[l[-1]] + nb)  # @line L6
            for c in labels:  # @line L7
                s = b if (l and c == l[-1]) else log_add(b, nb)  # @line L8
                acc(l + (c,), 1, row[c] + s + lm(l, c))  # @line L9
                lp = l + (c,)
                if recover and lp not in A and lp in scored:
                    ob, onb = scored[lp]
                    acc(lp, 0, row[blank] + log_add(ob, onb))
                    acc(lp, 1, row[c] + onb)
        scored = N
        ranked = sorted(N.items(), key=lambda kv: (-log_add(kv[1][0], kv[1][1]), kv[0]))
        A = {p: (v[0], v[1]) for p, v in ranked[:beam]}  # @line L10
    final = sorted(((p, log_add(b, nb)) for p, (b, nb) in A.items()), key=lambda x: (-x[1], x[0]))
    best, score = final[0]  # @line L11
    return best, score, final


def collapse(path: Sequence[int], blank: int = BLANK) -> Prefix:
    """The CTC map B: merge runs of equal symbols, then drop blanks."""
    out = []
    prev = None
    for k in path:
        if k != prev and k != blank:
            out.append(k)
        prev = k
    return tuple(out)


def greedy_decode(log_y: Sequence[Sequence[float]], blank: int = BLANK) -> Prefix:
    """Best path decoding: the best symbol per frame (first on ties), then B."""
    return collapse([max(range(len(r)), key=lambda k: (r[k], -k)) for r in log_y], blank)


def lm_log_weight(prefix: Prefix, lm: Optional[Callable[[Prefix, int], float]] = None) -> float:
    """The sum of the hook weights for building prefix label by label."""
    if lm is None:
        return 0.0
    return sum(lm(prefix[:i], prefix[i]) for i in range(len(prefix)))


def exhaustive_scores(
    log_y: Sequence[Sequence[float]],
    lm: Optional[Callable[[Prefix, int], float]] = None,
    blank: int = BLANK,
) -> Dict[Prefix, float]:
    """Every labeling with nonzero probability and its log score
    ln p(l | x) + lm_log_weight(l), by summing over all K^T frame paths.
    Only for small T and K."""
    T, K = len(log_y), len(log_y[0])
    terms: Dict[Prefix, List[float]] = {}
    for path in itertools.product(range(K), repeat=T):
        terms.setdefault(collapse(path, blank), []).append(sum(log_y[t][k] for t, k in enumerate(path)))
    return {l: log_sum(v) + lm_log_weight(l, lm) for l, v in terms.items()}


def exhaustive_best(
    log_y: Sequence[Sequence[float]],
    lm: Optional[Callable[[Prefix, int], float]] = None,
    blank: int = BLANK,
) -> Tuple[Prefix, float]:
    """The labeling with the largest score, by exhaustive search (ties: smaller tuple)."""
    scores = exhaustive_scores(log_y, lm, blank)
    best = min(scores, key=lambda l: (-scores[l], l))
    return best, scores[best]
