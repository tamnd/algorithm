# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fermion-to-qubit-mapping/. The authors are listed in prov/390342.jsonl.
"""Linear fermion-to-qubit encodings: the qubit basis state of the occupation vector f is |b>, b = beta f mod 2.

For an invertible binary matrix beta, with c_j the column j of beta, r_j the row j of
beta^-1 and p_j the sum mod 2 of the rows 0, ..., j - 1 of beta^-1,
  a_j^dagger = X(c_j) Z(p_j) (I + Z(r_j)) / 2,  and a_j is its adjoint,
where X(s) and Z(s) are the products of X and Z over the qubits in the set s.
The identity is the Jordan-Wigner encoding, the all-ones lower triangle is the parity
encoding and the Fenwick tree matrix is the Bravyi-Kitaev encoding.
"""

import random

from qsim import pauli_on, qop_add, qop_clean, qop_dagger, qop_mul, qop_scale


def gf2_inverse(beta: list[list[int]]) -> list[list[int]]:
    n = len(beta)
    a = [list(row) + [1 if i == k else 0 for k in range(n)] for i, row in enumerate(beta)]
    for col in range(n):
        piv = next((r for r in range(col, n) if a[r][col]), None)
        if piv is None:
            raise ValueError("beta is not invertible over GF(2)")
        a[col], a[piv] = a[piv], a[col]
        for r in range(n):
            if r != col and a[r][col]:
                a[r] = [x ^ y for x, y in zip(a[r], a[col])]
    return [row[n:] for row in a]


def jordan_wigner_matrix(n):
    return [[1 if i == k else 0 for k in range(n)] for i in range(n)]


def parity_matrix(n):
    return [[1 if k <= i else 0 for k in range(n)] for i in range(n)]


def bravyi_kitaev_matrix(n):
    return [[1 if i - ((i + 1) & -(i + 1)) < k <= i else 0 for k in range(n)] for i in range(n)]


def random_invertible(n, rng: random.Random):
    while True:
        beta = [[rng.randrange(2) for _ in range(n)] for _ in range(n)]
        try:
            gf2_inverse(beta)
            return beta
        except ValueError:
            pass


def _x(n, qubits):
    return {pauli_on(n, {q: "X" for q in qubits}): 1 + 0j}


def _z(n, qubits):
    return {pauli_on(n, {q: "Z" for q in qubits}): 1 + 0j}


def linear_creation(beta, j: int) -> dict:
    n = len(beta)
    inv = gf2_inverse(beta)
    c = [i for i in range(n) if beta[i][j]]
    r = [k for k in range(n) if inv[j][k]]
    p = [k for k in range(n) if sum(inv[m][k] for m in range(j)) % 2]
    proj = qop_scale(qop_add({"I" * n: 1 + 0j}, _z(n, r)), 0.5)  # f_j = 0
    return qop_mul(qop_mul(_x(n, c), _z(n, p)), proj)  # sign, then flip


def linear_ladder(beta, j: int, is_dagger: bool) -> dict:
    cr = linear_creation(beta, j)
    return cr if is_dagger else qop_dagger(cr)


def linear_map(beta, terms: list) -> dict:
    n = len(beta)
    out: dict = {}
    for coef, word in terms:
        w = {"I" * n: 1 + 0j}
        for j, is_dagger in word:
            w = qop_mul(w, linear_ladder(beta, j, is_dagger))
        out = qop_add(out, qop_scale(w, coef))
    return qop_clean(out)


def encode(beta, x: int) -> int:
    n = len(beta)
    b = 0
    for i in range(n):
        if sum(beta[i][k] & (x >> k) for k in range(n)) & 1:
            b |= 1 << i
    return b
