# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/no-free-lunch-theorem-learning/. The authors are listed in prov/N9KRMF.jsonl.
"""The no free lunch theorem of Shalev-Shwartz and Ben-David (Theorem 5.1), checked by exact enumeration.

The domain is C = {0, ..., 2m - 1}. For each target f : C -> {0, 1} (there are 2^(2m) of them), D_f is
the uniform distribution on C with the label f(x). A learner maps a labeled sample, a tuple of m pairs
(x, y), to a hypothesis, a tuple of 2m labels. Every probability below is an exact Fraction over the
(2m)^m equally likely sample sequences.
"""

import random
from fractions import Fraction
from itertools import product
from typing import Callable

Hyp = tuple[int, ...]
Sample = tuple[tuple[int, int], ...]
Learner = Callable[[Sample, int], Hyp]  # (labeled sample, domain size) -> hypothesis


def targets(size: int) -> list[Hyp]:
    return list(product((0, 1), repeat=size))


def sequences(m: int, size: int) -> list[tuple[int, ...]]:
    return list(product(range(size), repeat=m))


def risk(h: Hyp, f: Hyp) -> Fraction:
    """L_{D_f}(h): the fraction of C where h and f differ."""
    return Fraction(sum(a != b for a, b in zip(h, f)), len(f))


def off_sample_error(h: Hyp, f: Hyp, seen: set[int]) -> Fraction:
    """The error of h on the points of C that are not in the sample (Wolpert's off-training-set error)."""
    rest = [x for x in range(len(f)) if x not in seen]
    return Fraction(sum(h[x] != f[x] for x in rest), len(rest))


def risks(learner: Learner, m: int, f: Hyp) -> list[Fraction]:
    """L_{D_f}(A(S)) for each of the (2m)^m sample sequences S, labeled by f."""
    size = 2 * m
    return [risk(learner(tuple((x, f[x]) for x in xs), size), f) for xs in sequences(m, size)]


def expected_risk(learner: Learner, m: int, f: Hyp) -> Fraction:
    r = risks(learner, m, f)
    return sum(r, Fraction(0)) / len(r)


def prob_risk_above(learner: Learner, m: int, f: Hyp, a: Fraction) -> Fraction:
    r = risks(learner, m, f)
    return Fraction(sum(v > a for v in r), len(r))


def worst_target(learner: Learner, m: int) -> tuple[Hyp, Fraction, Fraction]:
    """The target with the largest expected risk, that risk, and P(L > 1/8) for it."""
    f = max(targets(2 * m), key=lambda g: expected_risk(learner, m, g))
    return f, expected_risk(learner, m, f), prob_risk_above(learner, m, f, Fraction(1, 8))


def mean_off_sample_error(learner: Learner, m: int, xs: tuple[int, ...]) -> Fraction:
    """For one sequence of inputs, the off-sample error averaged over all targets."""
    size = 2 * m
    seen = set(xs)
    ts = targets(size)
    total = sum((off_sample_error(learner(tuple((x, f[x]) for x in xs), size), f, seen) for f in ts), Fraction(0))
    return total / len(ts)


# A few learners. Each one is consistent with its sample unless the name says otherwise.

def memorize(default: int) -> Learner:
    def a(s: Sample, size: int) -> Hyp:
        d = dict(s)
        return tuple(d.get(x, default) for x in range(size))
    return a


def majority_fill(s: Sample, size: int) -> Hyp:
    """Seen points keep their label; unseen points get the majority label of the sample (ties: 1)."""
    d = dict(s)
    maj = int(2 * sum(y for _, y in s) >= len(s))
    return tuple(d.get(x, maj) for x in range(size))


def neighbor_fill(s: Sample, size: int) -> Hyp:
    """Unseen x gets the label of the nearest seen point below it, cyclically."""
    d = dict(s)
    out = []
    for x in range(size):
        z = x
        while z not in d:
            z = (z - 1) % size
        out.append(d[z])
    return tuple(out)


def random_table(seed: int) -> Learner:
    """A fixed but arbitrary rule: the unseen labels come from a seeded generator keyed by the sample."""
    def a(s: Sample, size: int) -> Hyp:
        d = dict(s)
        rng = random.Random(hash((seed, s)) & 0xFFFFFFFF)
        return tuple(d[x] if x in d else rng.getrandbits(1) for x in range(size))
    return a


def constant(c: int) -> Learner:
    """Not consistent: ignores the sample."""
    return lambda s, size: tuple([c] * size)


def all_learners_m1() -> list[Learner]:
    """Every deterministic learner for m = 1: a table from the 4 labeled samples to the 4 hypotheses."""
    samples = [((x, y),) for x in range(2) for y in range(2)]
    hyps = targets(2)
    out = []
    for choice in product(range(4), repeat=4):
        table = {s: hyps[c] for s, c in zip(samples, choice)}
        out.append(lambda s, size, t=table: t[s])
    return out


if __name__ == "__main__":
    for name, a in [("memorize0", memorize(0)), ("majority", majority_fill), ("neighbor", neighbor_fill),
                    ("random", random_table(3)), ("const0", constant(0))]:
        for m in (1, 2, 3):
            f, e, p = worst_target(a, m)
            print(name, m, f, e, float(e), p, float(p))
