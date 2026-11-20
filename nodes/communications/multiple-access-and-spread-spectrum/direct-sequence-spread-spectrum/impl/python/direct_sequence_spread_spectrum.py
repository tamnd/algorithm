# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-sequence-spread-spectrum/. The authors are listed in prov/5PQ8PD.jsonl.

"""Direct-sequence spreading and despreading with a +1/-1 chip code.

Each symbol d[i] in {+1, -1} is sent as d[i] c[0], ..., d[i] c[N - 1], where c
is a chip code of length N (here usually one period of an m-sequence). The
receiver correlates each block of N chips with c and takes the sign.
"""


def mseq_chips(exps: list[int]) -> list[int]:
    """One period of an m-sequence as chips: bit 0 -> +1 and bit 1 -> -1.

    The polynomial is the list of its exponents, for example [3, 1, 0] for
    x^3 + x + 1, and s[k + n] = XOR over the exponents i < n of s[k + i].
    """
    n = max(exps)
    s = [1] + [0] * (n - 1)
    taps = [i for i in exps if i < n]
    while len(s) < (1 << n) - 1:
        k = len(s) - n
        bit = 0
        for i in taps:
            bit ^= s[k + i]
        s.append(bit)
    return [1 - 2 * b for b in s]


def spread(symbols: list[int], code: list[int]) -> list[int]:
    """The chip stream: each symbol times the whole code."""
    chips = []
    for d in symbols:  # @line L1
        chips.extend(d * c for c in code)  # @line L2
    return chips


def despread(received: list[float], code: list[int]) -> list[float]:
    """The correlator outputs z[i] = sum over n of r[i N + n] c[n]."""
    n = len(code)
    if len(received) % n:
        raise ValueError("length must be a multiple of the code length")
    return [sum(received[i + j] * code[j] for j in range(n)) for i in range(0, len(received), n)]  # @line L3


def decide(z: list[float]) -> list[int]:
    """Hard decisions: +1 if z >= 0, else -1."""
    return [1 if v >= 0 else -1 for v in z]  # @line L4
