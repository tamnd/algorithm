# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cut-and-choose/. The authors are listed in prov/QC3Y6Z.jsonl.
"""Cut-and-choose for garbled circuits against a cheating garbler.

The garbler makes s circuits and corrupts k of them. The evaluator opens
and checks a random set of them, and evaluates the rest. Two rules for the
evaluated circuits are modelled:

  "majority": a fixed number c of circuits is checked, and the evaluator
      outputs the majority of the e = s - c evaluated outputs (the style of
      Lindell and Pinkas 2007). The garbler wins if no bad circuit is checked
      and the bad circuits are more than half of the evaluated ones.
  "lindell13": each circuit is checked on its own with probability q
      (q = 1/2 in Lindell 2013). If two evaluated circuits disagree, the
      evaluator learns the garbler's input and computes the right output
      itself, so one good evaluated circuit suffices. The garbler wins only
      if every checked circuit is good and every evaluated circuit is bad.

A circuit here is only a flag: good or bad. The simulation counts the
events; it does not garble real circuits (see the Yao garbled circuits page
for that). The selective failure attack on the evaluator's input OTs is
modelled the same way.

For study only. Uses Python's random module and is not constant time. Use a
maintained framework such as EMP-toolkit for real malicious 2PC.
"""

import random
from fractions import Fraction
from math import comb
from typing import Callable, Sequence

CAUGHT, WRONG, CORRECT = "caught", "wrong", "correct"


# ---------------------------------------------------------------- the template


def cut_and_choose(good: Sequence[bool], pick_check: Callable[[int], set[int]],
                   combine: Callable[[list[bool]], bool]) -> str:
    """One run of the template on s instances, each good or bad.

    pick_check(s) returns the check set. combine(flags of evaluated
    instances) says whether the combined result is right. Returns CAUGHT if a
    checked instance is bad, else CORRECT or WRONG."""
    s = len(good)                                   # @line L1
    check = pick_check(s)                           # @line L2
    for i in check:
        if not good[i]:                             # @line L3
            return CAUGHT
    used = [good[i] for i in range(s) if i not in check]   # @line L4
    return CORRECT if combine(used) else WRONG      # @line L5


def majority_ok(used: list[bool]) -> bool:
    """Majority output: right unless more than half of the evaluated are bad."""
    return 2 * sum(1 for g in used if not g) <= len(used)


def any_good_ok(used: list[bool]) -> bool:
    """Lindell 2013: right if at least one evaluated circuit is good."""
    return any(used)


def fixed_check(c: int, rng: random.Random) -> Callable[[int], set[int]]:
    return lambda s: set(rng.sample(range(s), c))


def coin_check(q: float, rng: random.Random) -> Callable[[int], set[int]]:
    return lambda s: {i for i in range(s) if rng.random() < q}


# ---------------------------------------------------------------- exact formulas


def escape_majority(s: int, c: int, k: int) -> Fraction:
    """Probability that k bad circuits out of s give a wrong majority unseen,
    when a uniform set of c circuits is checked."""
    e = s - c
    if k == 0 or k > e or 2 * k <= e:
        return Fraction(0)
    return Fraction(comb(s - k, c), comb(s, c))      # no bad circuit in the check set


def best_majority(s: int, c: int) -> tuple[int, Fraction]:
    """The garbler's best k and its escape probability."""
    return max(((k, escape_majority(s, c, k)) for k in range(s + 1)), key=lambda kp: kp[1])


def escape_lindell13(s: int, k: int, q: Fraction = Fraction(1, 2)) -> Fraction:
    """Each circuit is checked with probability q. The garbler wins only if
    the evaluated set is exactly the bad set: all s - k good ones checked and
    all k bad ones evaluated."""
    if k == 0:
        return Fraction(0)
    return q ** (s - k) * (1 - q) ** k


def min_circuits(target_log2: int, rule: str, check_fraction: Fraction = Fraction(3, 5)) -> int:
    """Smallest s whose best escape probability is at most 2^-target_log2."""
    s = 1
    while True:
        if rule == "lindell13":
            p = max(escape_lindell13(s, k) for k in range(s + 1))
        else:
            c = round(check_fraction * s)
            if c == 0 or c == s:          # nothing checked, or nothing to evaluate
                s += 1
                continue
            p = best_majority(s, c)[1]
        if p <= Fraction(1, 2 ** target_log2):
            return s
        s += 1


# ---------------------------------------------------------------- Monte Carlo


def monte_carlo(s: int, k: int, rule: str, trials: int, rng: random.Random,
                c: int = 0, q: float = 0.5) -> float:
    """Fraction of runs in which a garbler with k bad circuits escapes."""
    wins = 0
    for _ in range(trials):
        bad = set(rng.sample(range(s), k))
        good = [i not in bad for i in range(s)]
        if rule == "majority":
            res = cut_and_choose(good, fixed_check(c, rng), majority_ok)
        else:
            res = cut_and_choose(good, coin_check(q, rng), any_good_ok)
        wins += res == WRONG
    return wins / trials


# ---------------------------------------------------------------- selective failure


def abort_probability(y: int, corrupted: set[int], s: int) -> Fraction:
    """Selective failure on the evaluator's input bit y.

    The input bit is encoded as s random bits y_1..y_s with XOR y (the
    encoding of Lindell and Pinkas 2007; s = 1 is no encoding). The garbler
    gives a bad key for value 1 on the encoded wires in 'corrupted', so the
    evaluator aborts if some y_i with i in corrupted is 1. Exact abort
    probability, by counting the 2^(s-1) encodings of y."""
    total = abort = 0
    for bits in range(1 << s):
        if bin(bits).count("1") % 2 != y:
            continue
        total += 1
        abort += any((bits >> i) & 1 for i in corrupted)
    return Fraction(abort, total)


def selective_failure_run(y: int, corrupted: set[int], s: int, rng: random.Random) -> bool:
    """One run: encode y at random and report whether the evaluator aborts."""
    bits = [rng.getrandbits(1) for _ in range(s - 1)]
    last = y
    for b in bits:
        last ^= b
    bits.append(last)
    return any(bits[i] for i in corrupted)
