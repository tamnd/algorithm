# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/connectionist-temporal-classification/. The authors are listed in prov/7KBK03.jsonl.

"""Connectionist temporal classification (CTC): the loss, its gradient and greedy decoding.

A network gives, at each of T frames, logits u[t][k] over K symbols. Symbol 0
is the blank, written ∅ in the formulas of the page and "_" in its examples.
The symbols 1..K-1 are the labels. A path is one symbol per frame. The collapse
map B removes repeated symbols first and blanks second, so B("aa_ab_") = "aab".
The probability of a label sequence l is the sum, over all paths pi with
B(pi) = l, of the product of y_t(pi_t), where y_t = softmax(u_t).

The code follows Graves et al. (2006), Section 4, in log space. alpha_t(s)
includes the output of frame t. beta_t(s) here does NOT include the output of
frame t, so alpha_t(s) + beta_t(s) is the log of the total probability of the
paths that are in state s at frame t, and the gradient of -log p with respect
to u_t(k) is y_t(k) - (1/p) sum over s with l'_s = k of alpha_t(s) beta_t(s).
Graves defines beta with y_t inside, which puts an extra 1/y_t(k) in his
eq. (16).

Frames and states are numbered from 0 in the code and from 1 on the page.
The code takes the network outputs as given. It does not train a network.
All logs are natural logs.
"""

import itertools
import math
from typing import List, Sequence, Tuple

from nlslog import NEG_INF, POS_INF, Semiring, argmax, log_add, log_softmax, log_sum

BLANK = 0


def collapse(path: Sequence[int], blank: int = BLANK) -> Tuple[int, ...]:
    """The map B: merge runs of equal symbols, then drop blanks."""
    out = []
    prev = None
    for k in path:
        if k != prev and k != blank:
            out.append(k)
        prev = k
    return tuple(out)


def extend_labels(labels: Sequence[int], blank: int = BLANK) -> List[int]:
    """Return l' = blank, l_1, blank, l_2, ..., l_U, blank, of length 2U + 1."""
    ext = [blank]
    for k in labels:
        if k == blank:
            raise ValueError("a label sequence may not hold the blank")
        ext += [k, blank]
    return ext


def min_frames(labels: Sequence[int]) -> int:
    """The fewest frames that can produce l: |l| plus the number of adjacent repeats."""
    return len(labels) + sum(1 for i in range(1, len(labels)) if labels[i] == labels[i - 1])


def _can_skip(ext: Sequence[int], s: int, blank: int) -> bool:
    """True if a path may jump from state s - 2 to state s (skip the blank between)."""
    return s >= 2 and ext[s] != blank and ext[s] != ext[s - 2]


def ctc_forward(sr: Semiring, weights: Sequence[Sequence], labels: Sequence[int], blank: int = BLANK):
    """The forward sum in any semiring: the semiring sum, over paths with B(path) = l,
    of the semiring product of weights[t][path_t].

    With PROB and probabilities it gives p(l | x), with LOG and log probabilities
    it gives log p(l | x), with VITERBI it gives the log probability of the best
    path, and with COUNTING and weights of 1 it counts the paths.
    """
    ext = extend_labels(labels, blank)
    S = len(ext)
    T = len(weights)
    if T == 0:
        return sr.one if S == 1 else sr.zero
    a = [sr.zero] * S
    a[0] = weights[0][ext[0]]
    if S > 1:
        a[1] = weights[0][ext[1]]
    for t in range(1, T):
        new = [sr.zero] * S
        for s in range(S):
            acc = a[s]
            if s >= 1:
                acc = sr.plus(acc, a[s - 1])
            if _can_skip(ext, s, blank):
                acc = sr.plus(acc, a[s - 2])
            new[s] = sr.times(acc, weights[t][ext[s]])
        a = new
    return a[S - 1] if S == 1 else sr.plus(a[S - 1], a[S - 2])


def log_alpha(log_y: Sequence[Sequence[float]], ext: Sequence[int], blank: int = BLANK) -> List[List[float]]:
    """alpha[t][s]: log of the summed probability of the path prefixes 0..t that
    are in state s of l' at frame t and can be read as the start of l. Includes y_t."""
    T, S = len(log_y), len(ext)
    alpha = [[NEG_INF] * S for _ in range(T)]
    alpha[0][0] = log_y[0][ext[0]]  # @line L2
    if S > 1:
        alpha[0][1] = log_y[0][ext[1]]
    for t in range(1, T):  # @line L3
        prev = alpha[t - 1]
        for s in range(S):
            acc = prev[s]  # @line L4
            if s >= 1:
                acc = log_add(acc, prev[s - 1])
            if _can_skip(ext, s, blank):
                acc = log_add(acc, prev[s - 2])
            alpha[t][s] = acc + log_y[t][ext[s]]  # @line L5
    return alpha


def log_beta(log_y: Sequence[Sequence[float]], ext: Sequence[int], blank: int = BLANK) -> List[List[float]]:
    """beta[t][s]: log of the summed probability of the frames t+1..T-1 for paths
    that are in state s at frame t and end in one of the two last states. Does
    NOT include y_t."""
    T, S = len(log_y), len(ext)
    beta = [[NEG_INF] * S for _ in range(T)]
    beta[T - 1][S - 1] = 0.0  # @line L7
    if S > 1:
        beta[T - 1][S - 2] = 0.0
    for t in range(T - 2, -1, -1):
        nxt = beta[t + 1]
        for s in range(S):
            acc = nxt[s] + log_y[t + 1][ext[s]]
            if s + 1 < S:
                acc = log_add(acc, nxt[s + 1] + log_y[t + 1][ext[s + 1]])
            if s + 2 < S and _can_skip(ext, s + 2, blank):
                acc = log_add(acc, nxt[s + 2] + log_y[t + 1][ext[s + 2]])
            beta[t][s] = acc
    return beta


def ctc_loss_and_grad(logits: Sequence[Sequence[float]], labels: Sequence[int], blank: int = BLANK):
    """Return (loss, grad): loss = -log p(l | x) in nats, grad[t][k] = d loss / d u_t(k).

    Raise ValueError if no path produces l (T < min_frames(l)), since then the
    loss is infinite and has no gradient.
    """
    T = len(logits)
    if T == 0:
        raise ValueError("need at least one frame")
    log_y = [log_softmax(u) for u in logits]  # @line L1
    ext = extend_labels(labels, blank)
    S = len(ext)
    if T < min_frames(labels):
        raise ValueError("too few frames for this label sequence")
    alpha = log_alpha(log_y, ext, blank)
    log_p = alpha[T - 1][S - 1] if S == 1 else log_add(alpha[T - 1][S - 1], alpha[T - 1][S - 2])  # @line L6
    beta = log_beta(log_y, ext, blank)
    K = len(logits[0])
    grad = []
    for t in range(T):  # @line L8
        occ = [[] for _ in range(K)]
        for s in range(S):
            occ[ext[s]].append(alpha[t][s] + beta[t][s])
        grad.append([math.exp(log_y[t][k]) - math.exp(log_sum(occ[k]) - log_p) for k in range(K)])
    return -log_p, grad  # @line L9


def ctc_loss(logits: Sequence[Sequence[float]], labels: Sequence[int], blank: int = BLANK) -> float:
    """Return -log p(l | x) in nats, and POS_INF if no path produces l."""
    if len(logits) == 0:
        raise ValueError("need at least one frame")
    if len(logits) < min_frames(labels):
        return POS_INF
    log_y = [log_softmax(u) for u in logits]
    ext = extend_labels(labels, blank)
    alpha = log_alpha(log_y, ext, blank)
    last = alpha[-1]
    return -(last[-1] if len(ext) == 1 else log_add(last[-1], last[-2]))


def greedy_decode(log_y: Sequence[Sequence[float]], blank: int = BLANK) -> Tuple[int, ...]:
    """Best path decoding: the most probable symbol of each frame, then B.

    This is the labeling of the most probable path. It is NOT always the most
    probable labeling.
    """
    return collapse([argmax(row) for row in log_y], blank)


def brute_force_log_prob(log_y: Sequence[Sequence[float]], labels: Sequence[int], blank: int = BLANK) -> float:
    """log p(l | x) by summing over all K^T paths. Only for small T and K."""
    T, K = len(log_y), len(log_y[0])
    target = tuple(labels)
    terms = [
        sum(log_y[t][k] for t, k in enumerate(path))
        for path in itertools.product(range(K), repeat=T)
        if collapse(path, blank) == target
    ]
    return log_sum(terms)


def labeling_posteriors(log_y: Sequence[Sequence[float]], blank: int = BLANK) -> dict:
    """Map every labeling with nonzero probability to its log probability, by
    summing over all K^T paths. Only for small T and K."""
    T, K = len(log_y), len(log_y[0])
    acc: dict = {}
    for path in itertools.product(range(K), repeat=T):
        lab = collapse(path, blank)
        acc.setdefault(lab, []).append(sum(log_y[t][k] for t, k in enumerate(path)))
    return {lab: log_sum(v) for lab, v in acc.items()}
