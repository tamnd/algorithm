# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hadamard-code/. The authors are listed in prov/AJ00FE.jsonl.

"""Hadamard codes.

* sylvester(r): the 2^r x 2^r Sylvester Hadamard matrix with entries +1 / -1.
* encode(x, r): the linear [2^r, r, 2^(r-1)] Hadamard code, the table of a . x over all a.
* encode_augmented(x, b, r): the [2^r, r + 1, 2^(r-1)] code, the table of a . x + b
  (the rows of H and of -H, read as bits). This is the first order Reed-Muller code RM(1, r).
* decode_fwht: maximum likelihood decoding of the augmented code with the fast
  Walsh-Hadamard transform (the "Green machine"), in O(n log n) for n = 2^r.
* local_decode: the 2-query local decoder for the linear code.
* paley_code: the nonlinear (q + 1, 2(q + 1), (q + 1)/2) code from a Paley Hadamard matrix.

A codeword is a list of bits, position a for a in range(2^r).
"""

import random


def dot(a: int, x: int) -> int:
    """The inner product a . x over GF(2) of two bit vectors stored as ints."""
    return (a & x).bit_count() & 1


def sylvester(r: int) -> list[list[int]]:
    """H_1 = [1], H_{2m} = [[H, H], [H, -H]]. Entry (a, x) equals (-1)^(a . x)."""
    h = [[1]]
    for _ in range(r):
        h = [row + row for row in h] + [row + [-v for v in row] for row in h]
    return h


def is_hadamard(h: list[list[int]]) -> bool:
    """H H^T = n I and every entry is +1 or -1."""
    n = len(h)
    if any(len(row) != n or any(v not in (1, -1) for v in row) for row in h):
        return False
    return all(sum(h[i][k] * h[j][k] for k in range(n)) == (n if i == j else 0)
               for i in range(n) for j in range(n))


def encode(x: int, r: int) -> list[int]:
    """Hadamard codeword of the r-bit message x: position a holds a . x."""
    return [dot(a, x) for a in range(1 << r)]


def encode_augmented(x: int, b: int, r: int) -> list[int]:
    """Codeword of the [2^r, r + 1] code: position a holds a . x + b."""
    return [dot(a, x) ^ b for a in range(1 << r)]


def fwht(v: list[int]) -> list[int]:
    """Unnormalized fast Walsh-Hadamard transform: out[a] = sum_x (-1)^(a . x) v[x]."""
    v = list(v)
    n = len(v)
    h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                u, w = v[j], v[j + h]
                v[j], v[j + h] = u + w, u - w
        h *= 2
    return v


def decode_fwht(word: list[int]) -> tuple[int, int]:
    """Maximum likelihood decoding of the augmented Hadamard code.

    With s[x] = (-1)^word[x], the transform value F[a] = sum_x (-1)^(word[x] + a . x)
    equals n - 2 d(word, a . x). The nearest codeword is a . x + b with |F[a]| largest,
    and b = 0 when F[a] > 0. Returns (x, b). Ties go to the smallest a, then b = 0.
    """
    f = fwht([1 - 2 * bit for bit in word])
    a = max(range(len(f)), key=lambda i: (abs(f[i]), -i))
    return a, 0 if f[a] >= 0 else 1


def decode_linear(word: list[int]) -> int:
    """Nearest codeword of the linear code (b = 0 only): the a with the largest F[a]."""
    f = fwht([1 - 2 * bit for bit in word])
    return max(range(len(f)), key=lambda i: (f[i], -i))


def local_decode(word: list[int], i: int, rng: random.Random) -> int:
    """Recover bit i of the message (that is, e_i . x) from 2 queries:
    pick a random a and return word[a] + word[a xor e_i]. If at most a fraction delta of the
    word is wrong, each query is wrong with probability at most delta, so the answer is right
    with probability at least 1 - 2 delta."""
    n = len(word)
    a = rng.randrange(n)
    return word[a] ^ word[a ^ (1 << i)]


def local_decode_majority(word: list[int], i: int, reps: int, rng: random.Random) -> int:
    votes = sum(local_decode(word, i, rng) for _ in range(reps))
    return 1 if 2 * votes > reps else 0


def paley(q: int) -> list[list[int]]:
    """Paley construction of a Hadamard matrix of order q + 1 for a prime q = 3 mod 4.

    With the quadratic character chi and Q[i][j] = chi(j - i), Q is skew symmetric, and
    H = I + [[0, 1...1], [-1...-1, Q]]."""
    squares = {(x * x) % q for x in range(1, q)}

    def chi(a: int) -> int:
        a %= q
        return 0 if a == 0 else (1 if a in squares else -1)

    h = [[1] * (q + 1)]
    for i in range(q):
        h.append([-1] + [1 if i == j else chi(j - i) for j in range(q)])
    return h


def paley_code(q: int) -> list[tuple[int, ...]]:
    """Rows of H and -H for the Paley matrix of order q + 1, as bit tuples (+1 -> 0, -1 -> 1)."""
    h = paley(q)
    rows = [tuple(0 if v == 1 else 1 for v in row) for row in h]
    return rows + [tuple(1 - b for b in row) for row in rows]


def min_distance(words) -> int:
    return min(sum(a != b for a, b in zip(u, v)) for i, u in enumerate(words) for v in words[i + 1:])
