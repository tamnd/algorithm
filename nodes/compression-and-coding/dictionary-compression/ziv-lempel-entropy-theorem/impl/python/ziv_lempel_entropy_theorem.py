# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ziv-lempel-entropy-theorem/. The authors are listed in prov/X1WQQT.jsonl.

"""Numerical companion to the Ziv-Lempel asymptotic optimality theorem.

It has:
  * the LZ78 incremental parse, with a trie in a dict;
  * a real LZ78 bit code (encoder and decoder) for binary input, whose
    length is sum over phrases j = 1..c of (ceil(log2 j) + 1) bits, and the
    simpler count c (log2 c + 1) of Cover and Thomas;
  * the bound c <= n / ((1 - eps_n) log2 n) on the number of phrases of
    any distinct parsing of a binary string of length n;
  * the left side of Ziv's inequality, sum c_ls log2 c_ls, and the
    k-th order Markov log probability that it bounds;
  * samplers for Bernoulli and two-state Markov sources and their entropy rates.
"""

import math
import random


def lz78_parse(x) -> list[tuple[int, object]]:
    """Phrases as (index of the prefix phrase, last symbol); index 0 is the empty phrase.

    If the text ends inside a known phrase, the last pair is (index of that
    phrase, None): a copy of an earlier phrase, with no new symbol.
    """
    trie: dict[tuple[int, object], int] = {}
    out: list[tuple[int, object]] = []
    node = 0
    for symbol in x:
        child = trie.get((node, symbol))
        if child is None:
            out.append((node, symbol))
            trie[(node, symbol)] = len(out)
            node = 0
        else:
            node = child
    if node:
        out.append((node, None))
    return out


def phrases_as_strings(x) -> list:
    out, i = [], 0
    texts = [x[:0]]
    for prefix, symbol in lz78_parse(x):
        length = len(texts[prefix]) + (symbol is not None)
        piece = x[i:i + length]
        texts.append(piece)
        out.append(piece)
        i += length
    return out


def encode(bits: str) -> str:
    """LZ78 code of a binary string: phrase j gets ceil(log2 j) bits of pointer and one bit.

    The last phrase, if it has no new symbol, gets only its pointer. The
    decoder needs n, the length of the input, to know where to stop.
    """
    out = []
    for j, (prefix, symbol) in enumerate(lz78_parse(bits), start=1):
        width = (j - 1).bit_length()  # = ceil(log2 j): the pointer is one of 0 .. j-1
        if width:
            out.append(format(prefix, "0{}b".format(width)))
        if symbol is not None:
            out.append(symbol)
    return "".join(out)


def decode(code: str, n: int) -> str:
    phrases, out, pos, length = [""], [], 0, 0
    j = 1
    while length < n:
        width = (j - 1).bit_length()
        prefix = int(code[pos:pos + width], 2) if width else 0
        pos += width
        piece = phrases[prefix]
        if length + len(piece) < n:
            piece += code[pos]
            pos += 1
        phrases.append(piece)
        out.append(piece)
        length += len(piece)
        j += 1
    return "".join(out)


def code_length(c: int) -> int:
    """Bits of encode() when all c phrases end with a new symbol."""
    return sum((j - 1).bit_length() + 1 for j in range(1, c + 1))


def cover_thomas_length(c: int) -> float:
    """The count c (log2 c + 1) used in the proof."""
    return c * (math.log2(c) + 1) if c else 0.0


def distinct_parsing_bound(n: int) -> float:
    """n / ((1 - eps_n) log2 n) with eps_n = min(1, (log2 log2 n + 4) / log2 n), for n >= 4."""
    lg = math.log2(n)
    eps = min(1.0, (math.log2(lg) + 4) / lg)
    return n / ((1 - eps) * lg) if eps < 1 else math.inf


def max_distinct_phrases_string(n: int) -> str:
    """All binary strings of length 1, 2, 3, ... in order, cut to length n.

    Any parse of it into the strings of length at most m gives the most
    distinct phrases for its length; it is the case where the bound is tight.
    """
    out, m = [], 1
    while sum(map(len, out)) < n:
        out.extend(format(v, "0{}b".format(m)) for v in range(2 ** m))
        m += 1
    return "".join(out)[:n]


def ziv_sum(phrases: list[str], x: str, k: int) -> float:
    """sum over (l, s) of c_ls log2 c_ls, where s is the k symbols before the phrase."""
    counts: dict[tuple[int, str], int] = {}
    i = 0
    padded = "0" * k + x  # the state before the text is k zeros
    for p in phrases:
        state = padded[i:i + k]
        counts[(len(p), state)] = counts.get((len(p), state), 0) + 1
        i += len(p)
    return sum(c * math.log2(c) for c in counts.values())


def markov_log2_prob(x: str, k: int, q: dict[str, float]) -> float:
    """log2 Q_k(x | k zeros before x), where q[s] = P(next symbol = '1' | previous k symbols s)."""
    padded = "0" * k + x
    total = 0.0
    for i, symbol in enumerate(x):
        p1 = q[padded[i:i + k]]
        p = p1 if symbol == "1" else 1 - p1
        if p == 0:
            return -math.inf
        total += math.log2(p)
    return total


def binary_entropy(p: float) -> float:
    if p in (0.0, 1.0):
        return 0.0
    return -(p * math.log2(p) + (1 - p) * math.log2(1 - p))


def bernoulli(n: int, p: float, rng: random.Random) -> str:
    return "".join("1" if rng.random() < p else "0" for _ in range(n))


def markov(n: int, a: float, b: float, rng: random.Random) -> str:
    """Two states: P(0 -> 1) = a, P(1 -> 0) = b, started in the stationary law."""
    state = "1" if rng.random() < a / (a + b) else "0"
    out = []
    for _ in range(n):
        out.append(state)
        flip = a if state == "0" else b
        if rng.random() < flip:
            state = "1" if state == "0" else "0"
    return "".join(out)


def markov_entropy_rate(a: float, b: float) -> float:
    pi0 = b / (a + b)
    return pi0 * binary_entropy(a) + (1 - pi0) * binary_entropy(b)
