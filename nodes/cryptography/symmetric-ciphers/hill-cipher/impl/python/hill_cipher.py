# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hill-cipher/. The authors are listed in prov/G0FB2K.jsonl.
"""The Hill cipher modulo 26 and its known plaintext attack.

For study only. The cipher is linear, so a few known plaintext blocks give
the key, and the code is not constant time. Do not use it to protect real
data; use AES-GCM or ChaCha20-Poly1305 from libsodium, a FIPS 140 validated
module, or the standard library of your language.

Letters A to Z are the numbers 0 to 25. Only letters are encrypted, in upper
case; the message is padded with X to a multiple of the block size n. A key
is an n x n matrix K, given as a list of rows, and a block is a column
vector p, so the cipher block is c = K p mod 26.
"""

import math

M = 26

Matrix = list[list[int]]


def letters(text: str) -> str:
    """Keep the letters A to Z of text, in upper case."""
    return "".join(c for c in text.upper() if "A" <= c <= "Z")


def det(a: Matrix) -> int:
    """The integer determinant of a square integer matrix (Bareiss elimination, exact)."""
    n = len(a)
    if n == 0:
        return 1
    b = [row[:] for row in a]
    sign, prev = 1, 1
    for k in range(n - 1):
        if b[k][k] == 0:
            swap = next((i for i in range(k + 1, n) if b[i][k] != 0), None)
            if swap is None:
                return 0
            b[k], b[swap] = b[swap], b[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                b[i][j] = (b[i][j] * b[k][k] - b[i][k] * b[k][j]) // prev
        prev = b[k][k]
    return sign * b[n - 1][n - 1]


def det_mod(a: Matrix, m: int = M) -> int:
    return det(a) % m


def is_valid_key(k: Matrix) -> bool:
    """A key is valid exactly when its determinant is coprime to 26."""
    return math.gcd(det_mod(k), M) == 1


def inverse_mod(k: Matrix, m: int = M) -> Matrix:
    """The inverse of k modulo m, by the adjugate: k^-1 = det(k)^-1 adj(k)."""
    n = len(k)
    d = det_mod(k, m)
    if math.gcd(d, m) != 1:
        raise ValueError("the matrix is not invertible modulo m")
    d_inv = pow(d, -1, m)
    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j + 1 :] for r, row in enumerate(k) if r != i]
            adj[j][i] = (-1) ** (i + j) * det(minor)
    return [[d_inv * adj[i][j] % m for j in range(n)] for i in range(n)]


def mat_mul(a: Matrix, b: Matrix, m: int = M) -> Matrix:
    return [[sum(a[i][t] * b[t][j] for t in range(len(b))) % m for j in range(len(b[0]))] for i in range(len(a))]


def hill_encrypt(plaintext: str, k: Matrix) -> str:
    """Encrypt the letters of plaintext in blocks of n with c = K p mod 26."""
    if not is_valid_key(k):
        raise ValueError("the key matrix must be invertible modulo 26")
    n = len(k)
    t = letters(plaintext)
    t += "X" * (-len(t) % n)  # @line L1
    out = []
    for s in range(0, len(t), n):  # @line L2
        p = [ord(ch) - 65 for ch in t[s : s + n]]  # @line L3
        c = [sum(k[i][j] * p[j] for j in range(n)) % M for i in range(n)]  # @line L4
        out.extend(chr(65 + x) for x in c)
    return "".join(out)  # @line L5


def hill_decrypt(ciphertext: str, k: Matrix) -> str:
    """Decrypt with the inverse matrix. The padding X letters stay at the end."""
    return hill_encrypt(ciphertext, inverse_mod(k))


def count_keys(n: int) -> int:
    """|GL(n, Z_26)| = |GL(n, Z_2)| * |GL(n, Z_13)|, by the Chinese remainder theorem."""
    total = 1
    for p in (2, 13):
        for i in range(n):
            total *= p**n - p**i
    return total


def _solve_mod_prime(pt: Matrix, ct: Matrix, n: int, p: int) -> Matrix | None:
    """Find K mod p with K P = C (mod p), where P and C hold the blocks as columns.

    Gaussian elimination over GF(p) on the rows of P^T | C^T. Returns None
    when the plaintext blocks do not span GF(p)^n, since then K mod p is not
    unique.
    """
    rows = [[x % p for x in pt[b]] + [x % p for x in ct[b]] for b in range(len(pt))]
    r = 0
    for col in range(n):
        piv = next((i for i in range(r, len(rows)) if rows[i][col] != 0), None)
        if piv is None:
            return None
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = pow(rows[r][col], -1, p)
        rows[r] = [x * inv % p for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][col]:
                f = rows[i][col]
                rows[i] = [(x - f * y) % p for x, y in zip(rows[i], rows[r])]
        r += 1
    # Now rows[0..n-1] read I | K^T (mod p).
    return [[rows[j][n + i] for j in range(n)] for i in range(n)]


def known_plaintext_attack(plaintext: str, ciphertext: str, n: int) -> Matrix | None:
    """Recover K from matching plaintext and ciphertext, or None if they do not fix K.

    K is unique exactly when the plaintext blocks span (Z_2)^n and (Z_13)^n.
    With exactly n blocks this means that the n x n plaintext matrix is
    invertible modulo 26, and then K = C P^-1. The function solves modulo 2
    and modulo 13 and joins the results by the Chinese remainder theorem.
    """
    p, c = letters(plaintext), letters(ciphertext)
    blocks = min(len(p), len(c)) // n
    pt = [[ord(x) - 65 for x in p[b * n : (b + 1) * n]] for b in range(blocks)]
    ct = [[ord(x) - 65 for x in c[b * n : (b + 1) * n]] for b in range(blocks)]
    k2 = _solve_mod_prime(pt, ct, n, 2)
    k13 = _solve_mod_prime(pt, ct, n, 13)
    if k2 is None or k13 is None:
        return None
    # x = k2 (mod 2) and x = k13 (mod 13): x = k13 + 13 * ((k2 - k13) mod 2).
    return [[k13[i][j] + 13 * ((k2[i][j] - k13[i][j]) % 2) for j in range(n)] for i in range(n)]
