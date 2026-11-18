# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/word-aligned-hybrid-compression/. The authors are listed in prov/KZ8EQQ.jsonl.

"""Word-aligned hybrid (WAH) compression of bitmaps, with 32-bit words.

A bitmap is a list of bits (0 or 1). It is cut into groups of 31 bits. The
first bit of a group is the highest of its 31 bits, as in Fig. 2 of Wu, Otoo
and Shoshani (2006). A literal word has top bit 0 and holds one group. A fill
word has top bit 1, then the fill bit, then a 30-bit count of groups. The last
N mod 31 bits stay in the active word.
"""

from typing import Callable, List, Sequence, Tuple

W = 32
GROUP = W - 1                    # 31 bits per group
ALL_ONES = (1 << GROUP) - 1      # a group of 31 ones
FILL_FLAG = 1 << (W - 1)         # the top bit of a fill word
FILL_BIT = 1 << (W - 2)          # the fill bit of a fill word
MAX_COUNT = (1 << (W - 2)) - 1   # the largest count of a fill word


class WAH:
    """A compressed bitmap: regular words, the active word and its length."""

    def __init__(self, words: List[int], active: int, nbits: int):
        self.words = words
        self.active = active
        self.nbits = nbits

    def __eq__(self, other):
        return (self.words, self.active, self.nbits) == (other.words, other.active, other.nbits)

    def __repr__(self):
        return "WAH(%s, active=0x%08X, nbits=%d)" % (
            ", ".join("0x%08X" % x for x in self.words), self.active, self.nbits)

    def size(self) -> int:
        """The number of regular words."""
        return len(self.words)

    def groups(self) -> int:
        """The number of full groups, M."""
        return sum(word_count(x) for x in self.words)


def is_fill(word: int) -> bool:
    return bool(word & FILL_FLAG)


def fill_bit(word: int) -> int:
    return 1 if word & FILL_BIT else 0


def word_count(word: int) -> int:
    """The number of groups that a word covers: the count of a fill, 1 for a literal."""
    return word & MAX_COUNT if is_fill(word) else 1


def append_fill(z: List[int], f: int, k: int) -> None:
    """Append k groups of bit f to z, merging with a last fill of the same bit."""
    while k > 0:
        if z and is_fill(z[-1]) and fill_bit(z[-1]) == f and word_count(z[-1]) < MAX_COUNT:  # @line L11
            add = min(k, MAX_COUNT - word_count(z[-1]))
            z[-1] += add                                                      # @line L12
        else:
            add = min(k, MAX_COUNT)
            z.append(FILL_FLAG | (FILL_BIT if f else 0) | add)               # @line L13
        k -= add


def append_literal(z: List[int], g: int) -> None:
    """Append one group g; an all-zero or all-one group becomes a fill."""
    if g == 0:                                                               # @line L8
        append_fill(z, 0, 1)
    elif g == ALL_ONES:                                                      # @line L9
        append_fill(z, 1, 1)
    else:
        z.append(g)                                                          # @line L10


def bits_to_int(bits: Sequence[int]) -> int:
    """The bits as an integer, the first bit highest."""
    v = 0
    for b in bits:
        v = (v << 1) | (1 if b else 0)
    return v


def int_to_bits(v: int, length: int) -> List[int]:
    return [(v >> (length - 1 - i)) & 1 for i in range(length)]


def compress(bits: Sequence[int]) -> WAH:
    """COMPRESS: the WAH form of a bit sequence."""
    z: List[int] = []                                                        # @line L1
    n = len(bits)
    m = n // GROUP                                                           # @line L2
    for i in range(m):                                                       # @line L3
        g = bits_to_int(bits[GROUP * i: GROUP * i + GROUP])                  # @line L4
        append_literal(z, g)                                                 # @line L5
    nbits = n - GROUP * m                                                    # @line L6
    active = bits_to_int(bits[GROUP * m:])                                   # @line L6
    return WAH(z, active, nbits)                                             # @line L7


def decompress(x: WAH) -> List[int]:
    out: List[int] = []
    for word in x.words:
        if is_fill(word):
            out.extend([fill_bit(word)] * (GROUP * word_count(word)))
        else:
            out.extend(int_to_bits(word, GROUP))
    out.extend(int_to_bits(x.active, x.nbits))
    return out


def _run(words: List[int], i: int) -> Tuple[int, int]:
    """RUN: the 31-bit group value of word i and the number of groups it covers."""
    if i >= len(words):
        return 0, 0
    word = words[i]
    if is_fill(word):
        return (ALL_ONES if fill_bit(word) else 0), word_count(word)
    return word, 1


def wah_op(x: WAH, y: WAH, op: Callable[[int, int], int], stats=None) -> WAH:
    """WAH-OP: a bitwise operation on two compressed bitmaps of the same length.

    op works on 31-bit integers (for example lambda a, b: a & b). If stats is a
    dict, the number of loop steps is stored in stats["steps"].
    """
    if x.nbits != y.nbits or x.groups() != y.groups():
        raise ValueError("operands must cover the same number of bits")
    z: List[int] = []                                                        # @line L14
    i = j = 0                                                                # @line L14
    a, na = _run(x.words, 0)                                                 # @line L15
    b, nb = _run(y.words, 0)                                                 # @line L15
    steps = 0
    while i < len(x.words) and j < len(y.words):                             # @line L16
        steps += 1
        k = min(na, nb)                                                      # @line L17
        r = op(a, b) & ALL_ONES
        if is_fill(x.words[i]) and is_fill(y.words[j]):                      # @line L18
            append_fill(z, 1 if r else 0, k)                                 # @line L18
        else:
            append_literal(z, r)                                             # @line L19
        na -= k                                                              # @line L20
        nb -= k                                                              # @line L20
        if na == 0:                                                          # @line L21
            i += 1                                                           # @line L21
            a, na = _run(x.words, i)                                         # @line L21
        if nb == 0:                                                          # @line L22
            j += 1                                                           # @line L22
            b, nb = _run(y.words, j)                                         # @line L22
    mask = (1 << x.nbits) - 1
    active = op(x.active, y.active) & mask                                   # @line L23
    if stats is not None:
        stats["steps"] = steps
    return WAH(z, active, x.nbits)                                           # @line L24


def wah_and(x: WAH, y: WAH, stats=None) -> WAH:
    return wah_op(x, y, lambda a, b: a & b, stats)


def wah_or(x: WAH, y: WAH, stats=None) -> WAH:
    return wah_op(x, y, lambda a, b: a | b, stats)


def wah_xor(x: WAH, y: WAH, stats=None) -> WAH:
    return wah_op(x, y, lambda a, b: a ^ b, stats)


def counting_group_fills(bits: Sequence[int]) -> int:
    """G of Theorem 3: the pairs of consecutive full groups that are both all 0 or both all 1."""
    m = len(bits) // GROUP
    kinds = []
    for i in range(m):
        g = bits_to_int(bits[GROUP * i: GROUP * i + GROUP])
        kinds.append(0 if g == 0 else (1 if g == ALL_ONES else None))
    return sum(1 for i in range(m - 1) if kinds[i] is not None and kinds[i] == kinds[i + 1])
