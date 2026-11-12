# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/structured-prediction/. The authors are listed in prov/DHVXMW.jsonl.

"""Sequence labeling as structured prediction: a first-order linear model,
exact Viterbi decoding, Hamming loss-augmented decoding, the structured
perceptron of Collins (2002) with averaging, and the structured hinge loss
with a subgradient step (the structured SVM objective).

Features of a pair (x, y), with y_0 = START:
    ("E", y_t, x_t)       emission, for each position t
    ("T", y_{t-1}, y_t)   transition, for each position t
The score is w . phi(x, y), a sum of one emission and one transition weight
per position.
"""

import itertools
from collections import Counter
from typing import Hashable, Sequence

START = "<s>"
Weights = dict


def phi(x: Sequence[Hashable], y: Sequence[Hashable]) -> Counter:
    f: Counter = Counter()
    prev = START
    for tok, lab in zip(x, y):
        f[("E", lab, tok)] += 1
        f[("T", prev, lab)] += 1
        prev = lab
    return f


def score(w: Weights, x: Sequence[Hashable], y: Sequence[Hashable]) -> float:
    return sum(w.get(k, 0) * v for k, v in phi(x, y).items())


def hamming(y: Sequence[Hashable], z: Sequence[Hashable]) -> int:
    return sum(a != b for a, b in zip(y, z))


def viterbi(w: Weights, x: Sequence[Hashable], labels: Sequence[Hashable],
            gold: Sequence[Hashable] | None = None) -> list:
    """Return a label sequence with the largest score.

    With gold given, return a sequence with the largest score + Hamming(gold, y):
    the loss-augmented decoding of the structured SVM. Ties go to the earlier
    label in `labels`.
    """
    n = len(x)
    if n == 0:
        return []

    def local(t: int, lab: Hashable) -> float:
        bonus = 1 if gold is not None and lab != gold[t] else 0
        return w.get(("E", lab, x[t]), 0) + bonus

    best = [{lab: w.get(("T", START, lab), 0) + local(0, lab) for lab in labels}]  # @line L1
    back: list[dict] = [{}]
    for t in range(1, n):  # @line L2
        row, ptr = {}, {}
        for lab in labels:  # @line L3
            arg = max(labels, key=lambda p: (best[t - 1][p] + w.get(("T", p, lab), 0), -labels.index(p)))  # @line L4
            row[lab] = best[t - 1][arg] + w.get(("T", arg, lab), 0) + local(t, lab)  # @line L5
            ptr[lab] = arg  # @line L6
        best.append(row)
        back.append(ptr)
    last = max(labels, key=lambda lab: (best[n - 1][lab], -labels.index(lab)))  # @line L7
    path = [last]
    for t in range(n - 1, 0, -1):  # @line L8
        path.append(back[t][path[-1]])  # @line L9
    return path[::-1]  # @line L10


def brute_force_decode(w: Weights, x: Sequence[Hashable], labels: Sequence[Hashable],
                       gold: Sequence[Hashable] | None = None) -> tuple[float, list]:
    """Try all |labels|^n sequences. Return the best value and one sequence that reaches it."""
    best_val, best_y = None, None
    for y in itertools.product(labels, repeat=len(x)):
        v = score(w, x, y) + (hamming(gold, y) if gold is not None else 0)
        if best_val is None or v > best_val:
            best_val, best_y = v, list(y)
    return best_val, best_y


def _add(w: Weights, f: Counter, scale: float) -> None:
    for k, v in f.items():
        w[k] = w.get(k, 0) + scale * v


def structured_perceptron(data: Sequence[tuple[Sequence, Sequence]], labels: Sequence[Hashable],
                          epochs: int, average: bool = True) -> tuple[Weights, list[int]]:
    """Collins (2002). Return the (averaged) weights and the number of mistakes per epoch.

    Training stops early after an epoch with no mistakes. The averaged weights are the
    mean of w_1, ..., w_T, the weights after each of the T = epochs_run * len(data) steps.
    An update d made at step c is in T - c + 1 of these, so the mean is w - u / T with
    u = sum of (c - 1) d over the updates.
    """
    w: Weights = {}
    u: Weights = {}
    c = 1
    mistakes = []
    for _ in range(epochs):
        m = 0
        for x, y in data:
            z = viterbi(w, x, labels)
            if list(z) != list(y):
                m += 1
                d = phi(x, y)
                d.subtract(phi(x, z))
                _add(w, d, 1)
                _add(u, d, c - 1)
            c += 1
        mistakes.append(m)
        if m == 0:
            break
    if not average:
        return w, mistakes
    steps = c - 1
    return {k: w.get(k, 0) - u.get(k, 0) / steps for k in set(w) | set(u)}, mistakes


def structured_hinge(w: Weights, x: Sequence, y: Sequence, labels: Sequence[Hashable]) -> float:
    """max_z [Hamming(y, z) + w . phi(x, z)] - w . phi(x, y), computed by loss-augmented Viterbi."""
    z = viterbi(w, x, labels, gold=y)
    return hamming(y, z) + score(w, x, z) - score(w, x, y)


def ssvm_subgradient(data: Sequence[tuple[Sequence, Sequence]], labels: Sequence[Hashable], epochs: int,
                     reg: float = 0.01, eta: float = 0.1) -> tuple[Weights, list[float]]:
    """Minimize reg/2 |w|^2 + (1/N) sum_i hinge_i(w) by full subgradient steps with step eta / sqrt(k).

    Return the weights and the objective before each step and after the last one.
    """
    w: Weights = {}
    n = len(data)

    def objective() -> float:
        return reg / 2 * sum(v * v for v in w.values()) + sum(structured_hinge(w, x, y, labels) for x, y in data) / n

    hist = [objective()]
    for k in range(1, epochs + 1):
        g: Counter = Counter()
        for x, y in data:
            z = viterbi(w, x, labels, gold=y)
            g.update(phi(x, z))
            g.subtract(phi(x, y))
        step = eta / k ** 0.5
        new = {key: (1 - step * reg) * v for key, v in w.items()}
        for key, v in g.items():
            new[key] = new.get(key, 0) - step * v / n
        w = new
        hist.append(objective())
    return w, hist
