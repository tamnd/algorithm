# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/markov-password-model/. The authors are listed in prov/Q34M2V.jsonl.

"""A character Markov model of passwords, used to estimate password strength.

The model of order k predicts each character from the k characters before it,
with k start symbols in front of the password and an end symbol after it. It
is trained on a list of passwords by counting, with additive smoothing delta,
and it scores a password by its probability P(w) or by -log2 P(w) bits. A
low probability means a strong password under this model. The guess number
of w is 1 plus the number of strings with a higher probability: the place of
w in a guessing order by decreasing probability. It is an estimate under the
model and its training list, not a property of the password alone.

All probabilities are exact fractions.
"""

import math
import random
from fractions import Fraction
from typing import NamedTuple

START = "\x02"
END = "\x03"


class MarkovModel(NamedTuple):
    k: int  # the order: the number of characters of context
    alphabet: tuple[str, ...]  # the characters a password may use, sorted
    delta: Fraction  # the additive smoothing constant
    counts: dict  # (context, symbol) -> count, symbol in alphabet or END
    totals: dict  # context -> count


def shift(ctx: str, a: str, k: int) -> str:
    """The last k symbols of ctx followed by a."""
    return (ctx + a)[len(ctx) + 1 - k :] if k else ""


def _check(w: str, alphabet: tuple[str, ...]) -> None:
    for ch in w:
        if ch not in alphabet:
            raise ValueError(f"character {ch!r} is not in the alphabet")


def train(passwords: list[str], k: int, alphabet: str, delta: Fraction = Fraction(1)) -> MarkovModel:
    """Count the transitions of the padded passwords.

    Precondition: k >= 0, delta >= 0, each password uses only the alphabet.
    Cost: O(N k) time for N characters in the list, O(N k) space.
    """
    if k < 0 or delta < 0:
        raise ValueError("need k >= 0 and delta >= 0")
    alpha = tuple(sorted(set(alphabet)))
    if START in alpha or END in alpha:
        raise ValueError("the start and end symbols are reserved")
    counts: dict = {}
    totals: dict = {}
    for w in passwords:
        _check(w, alpha)
        ctx = START * k
        for a in list(w) + [END]:
            counts[(ctx, a)] = counts.get((ctx, a), 0) + 1
            totals[ctx] = totals.get(ctx, 0) + 1
            ctx = shift(ctx, a, k)
    return MarkovModel(k, alpha, Fraction(delta), counts, totals)


def next_prob(m: MarkovModel, ctx: str, a: str) -> Fraction:
    """P(a | ctx) with additive smoothing over the alphabet and END."""
    sigma = len(m.alphabet) + 1
    den = m.totals.get(ctx, 0) + m.delta * sigma
    if den == 0:
        return Fraction(0)  # no smoothing and an unseen context
    return (m.counts.get((ctx, a), 0) + m.delta) / den


def probability(m: MarkovModel, w: str) -> Fraction:
    """MARKOV-SCORE of the page, as an exact probability. Cost: O(|w| k)."""
    _check(w, m.alphabet)
    ctx = START * m.k  # @line L1
    p = Fraction(1)
    for i in range(len(w) + 1):  # @line L2
        a = w[i] if i < len(w) else END  # @line L3
        p *= next_prob(m, ctx, a)  # @line L4
        ctx = shift(ctx, a, m.k)  # @line L5
    return p


def strength_bits(m: MarkovModel, w: str) -> float:
    """-log2 P(w), the strength in bits (L6). Infinite when P(w) = 0."""
    p = probability(m, w)
    if p == 0:
        return math.inf
    return math.log2(p.denominator) - math.log2(p.numerator)  # @line L6


def guess_number(m: MarkovModel, w: str, max_len: int) -> int:
    """1 + the number of strings of length at most max_len whose probability
    is higher than P(w). It counts and never lists the strings.

    A prefix has probability at least that of each string that extends it, so
    the search stops at each prefix whose probability is at most P(w).
    Cost: O(G |alphabet| k) for G strings counted, plus the pruned prefixes.
    """
    target = probability(m, w)
    count = 0
    stack = [("", START * m.k, Fraction(1))]
    while stack:
        prefix, ctx, p = stack.pop()
        if p <= target:
            continue
        if p * next_prob(m, ctx, END) > target:
            count += 1
        if len(prefix) == max_len:
            continue
        for a in m.alphabet:
            q = p * next_prob(m, ctx, a)
            stack.append((prefix + a, shift(ctx, a, m.k), q))
    return count + 1


def sample_probabilities(m: MarkovModel, rng: random.Random, count: int, max_len: int) -> list[Fraction]:
    """The probabilities of count strings drawn from the model, cut at max_len.
    Only the probabilities are returned. Precondition: delta > 0.
    Cost: O(count max_len |alphabet|)."""
    if m.delta <= 0:
        raise ValueError("sampling needs delta > 0")
    symbols = list(m.alphabet) + [END]
    out = []
    for _ in range(count):
        ctx = START * m.k
        p = Fraction(1)
        for _ in range(max_len + 1):
            probs = [next_prob(m, ctx, a) for a in symbols]
            u = Fraction(rng.random())
            j = 0
            acc = probs[0]
            while u >= acc and j + 1 < len(symbols):
                j += 1
                acc += probs[j]
            p *= probs[j]
            if symbols[j] == END:
                break
            ctx = shift(ctx, symbols[j], m.k)
        else:
            p = Fraction(0)  # cut at max_len: counted as probability 0
        out.append(p)
    return out


def estimate_guess_number(target: Fraction, sample_probs: list[Fraction]) -> float:
    """The Monte Carlo estimate of Dell'Amico and Filippone (2015): each sample
    s with P(s) > target stands for 1 / (m P(s)) strings above the target.
    The estimate of the count is unbiased; the result adds 1 for the rank."""
    m = len(sample_probs)
    total = sum((1 / (m * p) for p in sample_probs if p > target), Fraction(0))
    return float(total) + 1
