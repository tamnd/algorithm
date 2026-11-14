# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cop-testability-measure/. The authors are listed in prov/ZPFC9R.jsonl.
"""COP (Brglez 1984): probabilistic controllability and observability of every line.

C[k] is the estimated probability that line k is 1 under random input
vectors, and O[k] the estimated probability that a change of k reaches a
primary output. Both treat all signals as independent. The detection
probability of k/0 is then C[k] O[k] and that of k/1 is (1 - C[k]) O[k].
Values are Fractions, so the code computes the COP numbers exactly; on a word
RAM with floating point numbers the cost is O(L + P) operations.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Optional, Sequence

from td2net import Circuit, Fault, controlling, inversion

ONE = Fraction(1)


def controllability(c: Circuit, p: Optional[Sequence[Fraction]] = None) -> list[Fraction]:
    """C[k] for every line, from the input probabilities p (1/2 each by default)."""
    if p is None:
        p = [Fraction(1, 2)] * len(c.pi)
    cc = [Fraction(0)] * c.n_lines
    k_in = 0
    for k in range(c.n_lines):  # @line L1
        op, ins = c.op[k], c.fanin[k]
        if c.kind[k] == "pi":  # @line L2
            cc[k] = Fraction(p[k_in])
            k_in += 1
            continue
        if c.kind[k] == "branch":  # @line L3
            cc[k] = cc[ins[0]]
            continue
        if op in ("AND", "NAND"):  # @line L4
            v = ONE
            for j in ins:
                v *= cc[j]
        elif op in ("OR", "NOR"):  # @line L5
            v = ONE
            for j in ins:
                v *= ONE - cc[j]
            v = ONE - v
        elif op in ("XOR", "XNOR"):  # @line L6
            v = Fraction(0)
            for j in ins:
                v = v * (ONE - cc[j]) + (ONE - v) * cc[j]
        else:  # NOT, BUF
            v = cc[ins[0]]
        cc[k] = ONE - v if inversion(op) else v  # @line L7
    return cc


def sensitizing(op: str, cj: Fraction) -> Fraction:
    """S_g(j): the probability that side input j of a gate of type op lets a change through."""
    cv = controlling(op)
    if cv is None:
        return ONE
    return cj if cv == 0 else ONE - cj


def observability(c: Circuit, cc: Sequence[Fraction]) -> list[Fraction]:
    """O[k] for every line, by one sweep in reverse topological order."""
    obs = [Fraction(0)] * c.n_lines
    is_po = set(c.po)
    for k in range(c.n_lines - 1, -1, -1):  # @line L8
        outs = c.fanout[k]
        if k in is_po:  # @line L9
            obs[k] = ONE
        elif len(outs) > 1:  # @line L10: a stem and its branches
            miss = ONE
            for b in outs:
                miss *= ONE - obs[b]
            obs[k] = ONE - miss
        elif len(outs) == 1:  # @line L11
            g = outs[0]
            v = obs[g]
            for j in c.fanin[g]:
                if j != k:
                    v *= sensitizing(c.op[g], cc[j])  # @line L12
            obs[k] = v
    return obs


def cop(c: Circuit, p: Optional[Sequence[Fraction]] = None) -> tuple[list[Fraction], list[Fraction]]:
    """The COP controllability and observability of every line."""
    cc = controllability(c, p)
    return cc, observability(c, cc)


def detection_probability(cc: Sequence[Fraction], obs: Sequence[Fraction], fault: Fault) -> Fraction:
    """COP estimate of the probability that a random vector detects the fault."""
    k, s = fault
    return (cc[k] if s == 0 else ONE - cc[k]) * obs[k]  # @line L13
