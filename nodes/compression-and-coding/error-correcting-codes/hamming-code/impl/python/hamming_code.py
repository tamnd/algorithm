# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hamming-code/. The authors are listed in prov/NYBA8H.jsonl.

"""Binary and q-ary Hamming codes, and the extended binary code used as SECDED.

Binary code of order r: n = 2^r - 1, k = n - r, d = 3. Positions are numbered
1..n as in Hamming's paper. Column j of H is j written in binary, so the
syndrome of a word with one error, read as a binary number, is the position of
the error. The check bits sit at the positions 1, 2, 4, ..., 2^(r - 1).
"""

from itertools import product

Vector = tuple[int, ...]


def parity_check_matrix(r: int) -> list[list[int]]:
    """H with column j (j = 1..2^r - 1) equal to j in binary, most significant bit in row 0."""
    n = (1 << r) - 1
    return [[(j >> (r - 1 - i)) & 1 for j in range(1, n + 1)] for i in range(r)]


def data_positions(r: int) -> list[int]:
    """The positions 1..n that are not powers of two, in increasing order."""
    n = (1 << r) - 1
    return [j for j in range(1, n + 1) if j & (j - 1)]


def encode(message: Vector, r: int) -> Vector:
    """Codeword of length 2^r - 1 for a message of 2^r - 1 - r bits. Cost: O(n r)."""
    n = (1 << r) - 1
    word = [0] * (n + 1)  # index 0 unused
    for pos, bit in zip(data_positions(r), message):
        word[pos] = bit
    for i in range(r):
        p = 1 << i
        word[p] = sum(word[j] for j in range(1, n + 1) if j & p and j != p) % 2
    return tuple(word[1:])


def syndrome_position(word: Vector) -> int:
    """The syndrome read as a number: the XOR of the positions that hold a 1."""
    s = 0
    for j, bit in enumerate(word, start=1):
        if bit:
            s ^= j
    return s


def decode(word: Vector) -> Vector:
    """Correct at most one error: flip the bit at the position the syndrome names."""
    s = syndrome_position(word)
    out = list(word)
    if s:
        out[s - 1] ^= 1
    return tuple(out)


def message_of(codeword: Vector, r: int) -> Vector:
    return tuple(codeword[j - 1] for j in data_positions(r))


def encode_extended(message: Vector, r: int) -> Vector:
    """Extended code [2^r, 2^r - 1 - r, 4]: an overall parity bit in front (position 0)."""
    c = encode(message, r)
    return (sum(c) % 2,) + c


def decode_secded(word: Vector) -> tuple[str, Vector]:
    """SECDED rule. Returns ("ok" | "corrected" | "double", word).

    s is the Hamming syndrome of positions 1..n, and p is the parity of all
    2^r bits. p = 1 means an odd number of errors, taken as one error at s
    (s = 0 points at the parity bit itself). s != 0 with p = 0 means an even,
    nonzero number of errors: two errors are detected and not corrected.
    """
    s = syndrome_position(word[1:])
    p = sum(word) % 2
    if s == 0 and p == 0:
        return "ok", word
    if p == 1:
        out = list(word)
        out[s] ^= 1
        return "corrected", tuple(out)
    return "double", word


def qary_parity_check(r: int, q: int) -> list[list[int]]:
    """H of the q-ary Hamming code (q prime): one column for each 1-dimensional subspace.

    The columns are the nonzero vectors of length r whose first nonzero entry is 1,
    so n = (q^r - 1)/(q - 1).
    """
    cols = [v for v in product(range(q), repeat=r) if any(v) and next(x for x in v if x) == 1]
    return [[c[i] for c in cols] for i in range(r)]


def qary_decode(h: list[list[int]], word: Vector, q: int) -> Vector:
    """Correct one symbol error: find column j and scalar a with H y^T = a h_j."""
    r, n = len(h), len(h[0])
    s = [sum(h[i][j] * word[j] for j in range(n)) % q for i in range(r)]
    if not any(s):
        return tuple(word)
    a = next(x for x in s if x)  # columns are normalized, so a is the first nonzero entry
    inv = pow(a, q - 2, q)
    col = [x * inv % q for x in s]
    j = next(j for j in range(n) if [h[i][j] for i in range(r)] == col)
    out = list(word)
    out[j] = (out[j] - a) % q
    return tuple(out)
