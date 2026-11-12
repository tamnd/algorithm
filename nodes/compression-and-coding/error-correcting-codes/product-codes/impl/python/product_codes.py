# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/product-codes/. The authors are listed in prov/XYNQ39.jsonl.

"""Binary product codes C1 (x) C2.

A codeword is an n1 x n2 array whose columns are codewords of C1 (length n1) and whose
rows are codewords of C2 (length n2). Arrays are lists of n1 row ints; bit j of a row is
column j. Component codes are given by generator rows (ints, bit j = position j).
"""

from itertools import product as cartesian


class Code:
    """A small binary linear code with bounded distance decoding by search."""

    def __init__(self, gen: list[int], n: int) -> None:
        self.gen, self.n, self.k = gen, n, len(gen)
        self.words = [self.encode(m) for m in range(1 << self.k)]
        self.d = min(w.bit_count() for w in self.words if w)
        self.t = (self.d - 1) // 2

    def encode(self, msg: int) -> int:
        out = 0
        for i, row in enumerate(self.gen):
            if (msg >> i) & 1:
                out ^= row
        return out

    def decode(self, word: int) -> int | None:
        """The codeword within distance t of word, or None (a detected failure)."""
        for c in self.words:
            if (c ^ word).bit_count() <= self.t:
                return c
        return None


def hamming74() -> Code:
    # G = [I | P], positions 0..3 information, 4..6 checks
    rows = ["1000110", "0100011", "0010111", "0001101"]
    return Code([int(r[::-1], 2) for r in rows], 7)


def repetition(n: int) -> Code:
    return Code([(1 << n) - 1], n)


def even_weight(n: int) -> Code:
    return Code([1 | (1 << (i + 1)) for i in range(n - 1)], n)


def column(arr: list[int], j: int) -> int:
    return sum(((row >> j) & 1) << i for i, row in enumerate(arr))


def set_column(arr: list[int], j: int, col: int) -> None:
    for i in range(len(arr)):
        arr[i] = (arr[i] & ~(1 << j)) | (((col >> i) & 1) << j)


def encode(msg: list[int], c1: Code, c2: Code) -> list[int]:
    """msg is a k1 x k2 array (k1 row ints of k2 bits). Encode each row with C2, then each
    of the n2 columns with C1. The result is the array M G2 encoded by G1, that is G1^T M G2."""
    rows = [c2.encode(m) for m in msg]                    # k1 x n2
    arr = [0] * c1.n
    for j in range(c2.n):
        col_msg = sum(((r >> j) & 1) << i for i, r in enumerate(rows))
        set_column(arr, j, c1.encode(col_msg))
    return arr


def encode_columns_first(msg: list[int], c1: Code, c2: Code) -> list[int]:
    """The same code word, built in the other order: columns with C1, then rows with C2."""
    k2 = c2.k
    cols = [c1.encode(sum(((msg[i] >> j) & 1) << i for i in range(c1.k))) for j in range(k2)]
    arr = []
    for i in range(c1.n):
        row_msg = sum(((cols[j] >> i) & 1) << j for j in range(k2))
        arr.append(c2.encode(row_msg))
    return arr


def is_codeword(arr: list[int], c1: Code, c2: Code) -> bool:
    words1, words2 = set(c1.words), set(c2.words)
    return all(r in words2 for r in arr) and all(column(arr, j) in words1 for j in range(c2.n))


def flatten(arr: list[int], n2: int) -> int:
    return sum(row << (i * n2) for i, row in enumerate(arr))


def all_codewords(c1: Code, c2: Code) -> list[int]:
    """Every code word as one n1 n2 bit int, from the k1 k2 generator arrays (outer
    products g1_a^T g2_b) by Gray code order."""
    gens = []
    for a in c1.gen:
        for b in c2.gen:
            gens.append(flatten([b if (a >> i) & 1 else 0 for i in range(c1.n)], c2.n))
    words, cur = [0], 0
    for x in range(1, 1 << len(gens)):
        cur ^= gens[(x & -x).bit_length() - 1]
        words.append(cur)
    return words


def row_column_decode(arr: list[int], c1: Code, c2: Code) -> list[int]:
    """Decode every column with C1, then every row with C2, each by bounded distance.
    A component decoder that fails leaves its column or row unchanged."""
    arr = list(arr)
    for j in range(c2.n):
        got = c1.decode(column(arr, j))
        if got is not None:
            set_column(arr, j, got)
    for i in range(c1.n):
        got = c2.decode(arr[i])
        if got is not None:
            arr[i] = got
    return arr


def nearest_codeword(word: int, codewords: list[int]) -> int:
    return min(codewords, key=lambda c: ((c ^ word).bit_count(), c))


def unflatten(word: int, n1: int, n2: int) -> list[int]:
    mask = (1 << n2) - 1
    return [(word >> (i * n2)) & mask for i in range(n1)]


def messages(k1: int, k2: int):
    for bits in cartesian(range(1 << k2), repeat=k1):
        yield list(bits)
