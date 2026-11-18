# SPDX-License-Identifier: MIT
# Shared helper of the natural-language-and-speech pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Log-space arithmetic and semirings for the natural-language-and-speech pages.

Every log is the natural log. A probability of 0 is NEG_INF (float("-inf")),
never a large negative number. A cost is -log p, so a probability of 0 is a
cost of POS_INF.

The semirings are (K, plus, times, zero, one) as on the weighted-automaton page:

    PROB      probabilities         plus = +        times = *   zero = 0       one = 1
    LOG       log probabilities     plus = log_add  times = +   zero = -inf    one = 0
    VITERBI   log probabilities     plus = max      times = +   zero = -inf    one = 0
    TROPICAL  costs -log p          plus = min      times = +   zero = +inf    one = 0
    LOG_COST  costs -log p          plus = -log_add(-a, -b), times = +, zero = +inf, one = 0
    BOOLEAN   truth values          plus = or       times = and zero = False   one = True
    COUNTING  path counts           plus = +        times = *   zero = 0       one = 1

This module holds no algorithm of any page: no forward, Viterbi, CKY, Eisner,
CTC or DTW recursion. The pages build their dynamic programs on top of it.
"""

import math
from dataclasses import dataclass
from typing import Any, Callable, Iterable, List, Sequence

NEG_INF = float("-inf")
POS_INF = float("inf")


def safe_log(p) -> float:
    """Return log p, and NEG_INF for p = 0. Raise ValueError for p < 0."""
    if p < 0:
        raise ValueError("log of a negative number")
    if p == 0:
        return NEG_INF
    return math.log(p)


def log_add(a: float, b: float) -> float:
    """Return log(exp(a) + exp(b)) = max(a, b) + log(1 + exp(-|a - b|)).

    log_add(NEG_INF, NEG_INF) is NEG_INF. No exp of a large number is taken.
    """
    if a < b:
        a, b = b, a
    if b == NEG_INF or a == POS_INF:
        return a
    return a + math.log1p(math.exp(b - a))


def log_sum(xs: Iterable[float]) -> float:
    """Return log(sum of exp(x)) over xs. An empty input gives NEG_INF."""
    xs = list(xs)
    if not xs:
        return NEG_INF
    m = max(xs)
    if m == NEG_INF or m == POS_INF:
        return m
    return m + math.log(math.fsum(math.exp(x - m) for x in xs))


def log_normalize(xs: Sequence[float]) -> List[float]:
    """Return the list x - log_sum(xs): log values whose exps sum to 1.

    Raise ValueError if every value is NEG_INF (nothing to normalize).
    """
    z = log_sum(xs)
    if z == NEG_INF:
        raise ValueError("every weight is zero")
    return [x - z for x in xs]


def log_softmax(xs: Sequence[float]) -> List[float]:
    """Return log softmax(xs): the logits xs turned into log probabilities."""
    return log_normalize(xs)


def softmax(xs: Sequence[float], temperature: float = 1.0) -> List[float]:
    """Return the probabilities exp(x / temperature) / sum, computed stably.

    The temperature must be positive. Logits of NEG_INF get probability 0.
    """
    if not temperature > 0:
        raise ValueError("the temperature must be positive")
    m = max(xs)
    if m == NEG_INF:
        raise ValueError("every logit is -inf")
    es = [math.exp((x - m) / temperature) for x in xs]
    s = math.fsum(es)
    return [e / s for e in es]


def argmax(xs: Sequence[Any]) -> int:
    """Return the first index of a largest value. Raise ValueError if xs is empty."""
    if len(xs) == 0:
        raise ValueError("argmax of an empty sequence")
    best = 0
    for i in range(1, len(xs)):
        if xs[i] > xs[best]:
            best = i
    return best


@dataclass(frozen=True)
class Semiring:
    """A semiring (K, plus, times, zero, one). idempotent is True when a plus a = a."""

    name: str
    plus: Callable[[Any, Any], Any]
    times: Callable[[Any, Any], Any]
    zero: Any
    one: Any
    idempotent: bool


def _add(a, b):
    return a + b


def _mul(a, b):
    return a * b


def _log_add_cost(a: float, b: float) -> float:
    return -log_add(-a, -b)


PROB = Semiring("probability", _add, _mul, 0, 1, False)
LOG = Semiring("log", log_add, _add, NEG_INF, 0.0, False)
VITERBI = Semiring("viterbi", max, _add, NEG_INF, 0.0, True)
TROPICAL = Semiring("tropical", min, _add, POS_INF, 0.0, True)
LOG_COST = Semiring("log-cost", _log_add_cost, _add, POS_INF, 0.0, False)
BOOLEAN = Semiring("boolean", lambda a, b: a or b, lambda a, b: a and b, False, True, True)
COUNTING = Semiring("counting", _add, _mul, 0, 1, False)


def sr_sum(sr: Semiring, xs: Iterable[Any]) -> Any:
    """Return the semiring sum of xs, and sr.zero for an empty input."""
    acc = sr.zero
    for x in xs:
        acc = sr.plus(acc, x)
    return acc


def sr_prod(sr: Semiring, xs: Iterable[Any]) -> Any:
    """Return the semiring product of xs, and sr.one for an empty input."""
    acc = sr.one
    for x in xs:
        acc = sr.times(acc, x)
    return acc
