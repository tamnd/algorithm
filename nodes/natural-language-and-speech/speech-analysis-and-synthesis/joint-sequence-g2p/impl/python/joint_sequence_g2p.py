# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/joint-sequence-g2p/. The authors are listed in prov/Z0KB29.jsonl.

"""Joint-sequence (graphone) model for grapheme-to-phoneme conversion, after
Bisani and Ney (2008).

A graphone is a pair (letters, phonemes) of a chunk of 1 to lmax letters and a
chunk of 0 to pmax phonemes. A word and its pronunciation are the letter and
phoneme sides of a sequence of graphones; the same pair (g, phi) has many such
joint segmentations. The model is an M-gram model over graphones with the
history padded by M - 1 copies of "<s>" and the end symbol "</s>" predicted:

    p(q_1 .. q_K) = prod_{k=1}^{K+1} p(q_k | q_{k-M+1} .. q_{k-1}),  q_{K+1} = "</s>",
    p(g, phi)     = sum over the joint segmentations of (g, phi) of p(q_1 .. q_K).

train_em fits the model by EM over the joint segmentations (forward-backward
on the lattice of positions (i, j, history), in the log semiring). decode
returns the phonemes of the best graphone sequence whose letter side is the
word (the maximum approximation, Viterbi semiring). Every log is natural.

Restriction of this code: every graphone has at least one letter. Bisani and
Ney also allow graphones with no letters. The M step is the plain maximum
likelihood estimate; the paper smooths the M-gram model, which this code does
not do, so an unseen history or graphone has probability 0.
"""

import math
from typing import Dict, List, Sequence, Tuple

from nlslog import NEG_INF, log_add, log_sum, safe_log

BOS = "<s>"
EOS = "</s>"

Graphone = Tuple[Tuple[str, ...], Tuple[str, ...]]
Model = Dict[tuple, Dict[object, float]]  # history -> graphone or EOS -> log probability


def start_history(order: int) -> tuple:
    return tuple([BOS] * (order - 1))


def next_history(h: tuple, q, order: int) -> tuple:
    """The last order - 1 symbols of h followed by q."""
    if order == 1:
        return ()
    return (h + (q,))[-(order - 1):]


def _arcs(g: Sequence[str], phi: Sequence[str], i: int, j: int, lmax: int, pmax: int):
    """The graphones that start at letter i and phoneme j and fit inside (g, phi)."""
    for a in range(1, lmax + 1):
        if i + a > len(g):
            break
        for b in range(0, pmax + 1):
            if j + b > len(phi):
                break
            yield a, b, (tuple(g[i:i + a]), tuple(phi[j:j + b]))


def inventory(lexicon, lmax: int, pmax: int) -> List[Graphone]:
    """All graphones that occur in some joint segmentation of some pair of the lexicon."""
    seen = set()
    for g, phi in lexicon:
        n, m = len(g), len(phi)
        fwd = {(0, 0)}
        for i in range(n + 1):
            for j in range(m + 1):
                if (i, j) in fwd:
                    for a, b, q in _arcs(g, phi, i, j, lmax, pmax):
                        fwd.add((i + a, j + b))
        bwd = {(n, m)}
        for i in range(n, -1, -1):
            for j in range(m, -1, -1):
                for a, b, q in _arcs(g, phi, i, j, lmax, pmax):
                    if (i + a, j + b) in bwd:
                        bwd.add((i, j))
        for (i, j) in fwd:
            for a, b, q in _arcs(g, phi, i, j, lmax, pmax):
                if (i + a, j + b) in bwd:
                    seen.add(q)
    return sorted(seen)


def uniform_model(lexicon, order: int, lmax: int, pmax: int) -> Model:
    """p(q | h) uniform over the inventory and EOS, for every history that can occur."""
    inv = inventory(lexicon, lmax, pmax)
    events = list(inv) + [EOS]
    lp = -math.log(len(events))
    hists = {start_history(order)}
    for _ in range(order - 1):
        hists |= {next_history(h, q, order) for h in list(hists) for q in inv}
    return {h: {e: lp for e in events} for h in hists}


def _lp(model: Model, h: tuple, q) -> float:
    return model.get(h, {}).get(q, NEG_INF)


def forward(model: Model, g, phi, order: int, lmax: int, pmax: int):
    """Log semiring. alpha[(i, j, h)] is the log of the total probability of the
    graphone prefixes that cover g[:i] and phi[:j] and leave history h.
    Returns (alpha, log Z) with Z = p(g, phi)."""
    n, m = len(g), len(phi)
    cells: Dict[Tuple[int, int], Dict[tuple, float]] = {(0, 0): {start_history(order): 0.0}}  # @line L10
    for i in range(n):  # @line L11
        for j in range(m + 1):
            for h, a0 in cells.get((i, j), {}).items():
                for a, b, q in _arcs(g, phi, i, j, lmax, pmax):  # @line L12
                    w = _lp(model, h, q)
                    if w == NEG_INF:
                        continue
                    h2 = next_history(h, q, order)  # @line L13
                    cell = cells.setdefault((i + a, j + b), {})
                    cell[h2] = log_add(cell.get(h2, NEG_INF), a0 + w)  # @line L14
    alpha = {(i, j, h): v for (i, j), cell in cells.items() for h, v in cell.items()}
    z = log_sum(v + _lp(model, h, EOS) for h, v in cells.get((n, m), {}).items())  # @line L15
    return alpha, z


def backward(model: Model, g, phi, order: int, lmax: int, pmax: int, alpha):
    """Log semiring. beta[(i, j, h)] is the log of the total probability of the
    suffixes from state (i, j, h) to the end, EOS included. States are those of alpha."""
    n, m = len(g), len(phi)
    beta = {}
    for key in sorted(alpha, key=lambda k: (-k[0], -k[1])):
        i, j, h = key
        if i == n and j == m:
            beta[key] = _lp(model, h, EOS)
            continue
        acc = NEG_INF
        for a, b, q in _arcs(g, phi, i, j, lmax, pmax):
            w = _lp(model, h, q)
            nxt = (i + a, j + b, next_history(h, q, order))
            if w != NEG_INF and nxt in beta:
                acc = log_add(acc, w + beta[nxt])
        beta[key] = acc
    return beta


def joint_log_prob(model: Model, g, phi, order: int, lmax: int, pmax: int) -> float:
    """log p(g, phi), the sum over all joint segmentations."""
    return forward(model, tuple(g), tuple(phi), order, lmax, pmax)[1]


def expected_counts(model: Model, lexicon, order: int, lmax: int, pmax: int):
    """The E step. Returns (counts, log likelihood), where counts[h][q] is the
    expected number of times graphone q (or EOS) follows history h."""
    counts: Dict[tuple, Dict[object, float]] = {}  # @line L3
    total = 0.0
    for g, phi in lexicon:  # @line L4
        g, phi = tuple(g), tuple(phi)
        alpha, z = forward(model, g, phi, order, lmax, pmax)  # @line L5
        if z == NEG_INF:
            raise ValueError("the pair %r has probability 0 under the model" % ((g, phi),))
        beta = backward(model, g, phi, order, lmax, pmax, alpha)
        total += z
        n, m = len(g), len(phi)
        for (i, j, h), a0 in alpha.items():  # @line L6
            row = counts.setdefault(h, {})
            if i == n and j == m:
                w = _lp(model, h, EOS)
                if w != NEG_INF:
                    row[EOS] = row.get(EOS, 0.0) + math.exp(a0 + w - z)
                continue
            for a, b, q in _arcs(g, phi, i, j, lmax, pmax):
                w = _lp(model, h, q)
                bt = beta.get((i + a, j + b, next_history(h, q, order)), NEG_INF)
                if w == NEG_INF or bt == NEG_INF:
                    continue
                row[q] = row.get(q, 0.0) + math.exp(a0 + w + bt - z)  # @line L7
    return counts, total


def m_step(counts) -> Model:
    """Maximum likelihood estimate p(q | h) = c(h, q) / sum over q' of c(h, q')."""
    model: Model = {}
    for h, row in counts.items():  # @line L8
        s = sum(row.values())
        if s > 0:
            model[h] = {q: safe_log(c / s) for q, c in row.items() if c > 0}
    return model


def train_em(lexicon, order: int = 1, lmax: int = 2, pmax: int = 2, iterations: int = 10, model: Model = None):
    """Run EM from the uniform model (or from the given model).
    Returns (model, lls), where lls[k] is the log likelihood of the lexicon
    under the model before the (k + 1)-th M step."""
    lexicon = [(tuple(g), tuple(phi)) for g, phi in lexicon]
    if model is None:
        model = uniform_model(lexicon, order, lmax, pmax)  # @line L1
    lls = []
    for _ in range(iterations):  # @line L2
        counts, ll = expected_counts(model, lexicon, order, lmax, pmax)
        lls.append(ll)
        model = m_step(counts)
    return model, lls  # @line L9


def decode(model: Model, g, order: int, lmax: int):
    """The best graphone sequence whose letter side is g, in the Viterbi semiring.

    Returns (phonemes, graphones, log score), where the score includes EOS.
    Raises ValueError if no graphone sequence of the model spells g.
    Tie rule: candidates are tried in a fixed order and a later one replaces the
    stored one only if it is strictly better.
    """
    g = tuple(g)
    n = len(g)
    by_letters: Dict[Tuple[str, ...], set] = {}
    for row in model.values():
        for q in row:
            if q != EOS:
                by_letters.setdefault(q[0], set()).add(q)
    by_letters = {k: sorted(v) for k, v in by_letters.items()}
    cells: List[Dict[tuple, float]] = [dict() for _ in range(n + 1)]
    back: List[Dict[tuple, tuple]] = [dict() for _ in range(n + 1)]
    cells[0][start_history(order)] = 0.0  # @line L16
    for i in range(n):  # @line L17
        for h in sorted(cells[i], key=repr):
            d = cells[i][h]
            for a in range(1, min(lmax, n - i) + 1):
                for q in by_letters.get(g[i:i + a], []):  # @line L18
                    w = _lp(model, h, q)
                    if w == NEG_INF:
                        continue
                    h2 = next_history(h, q, order)
                    if d + w > cells[i + a].get(h2, NEG_INF):  # @line L19
                        cells[i + a][h2] = d + w
                        back[i + a][h2] = (i, h, q)
    best_h, best = None, NEG_INF
    for h in sorted(cells[n], key=repr):  # @line L20
        s = cells[n][h] + _lp(model, h, EOS)
        if s > best:
            best_h, best = h, s
    if best_h is None:
        raise ValueError("no graphone sequence of the model spells %r" % (g,))
    seq = []
    i, h = n, best_h
    while i > 0:
        i, h, q = back[i][h]
        seq.append(q)
    seq.reverse()
    return [p for q in seq for p in q[1]], seq, best  # @line L21
