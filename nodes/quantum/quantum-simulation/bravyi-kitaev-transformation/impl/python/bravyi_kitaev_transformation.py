# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bravyi-kitaev-transformation/. The authors are listed in prov/P3HDKS.jsonl.
"""The Bravyi-Kitaev transformation in its Fenwick tree form, for any number n of modes.

Qubit i stores the parity of the modes in (i - lowbit(i + 1), i], where lowbit(m) = m & -m.
For mode j the three sets are
  U(j): the qubits other than j that store n_j (the ancestors of j in the tree),
  P(j): the qubits whose sum is the parity n_0 + ... + n_{j-1} (a Fenwick prefix query),
  F(j): the qubits whose sum with n_j is the value of qubit j (the children of j), F(j) in P(j),
and R(j) = P(j) minus F(j). Then
  a_j^dagger = 1/2 X_U(j) (X_j Z_P(j) - i Y_j Z_R(j)),  a_j = 1/2 X_U(j) (X_j Z_P(j) + i Y_j Z_R(j)).
"""

from qsim import pauli_on, qop_add, qop_clean, qop_mul, qop_scale


def lowbit(m: int) -> int:
    return m & -m


def bk_matrix(n: int) -> list[list[int]]:
    """beta[i][k] = 1 when qubit i stores mode k, so b = beta f mod 2."""
    return [[1 if i - lowbit(i + 1) < k <= i else 0 for k in range(n)] for i in range(n)]


def update_set(n: int, j: int) -> list[int]:
    out = []
    i = j + 1
    i += lowbit(i)
    while i <= n:  # @line L1
        out.append(i - 1)
        i += lowbit(i)
    return out


def parity_set(n: int, j: int) -> list[int]:
    out = []
    i = j
    while i > 0:  # @line L2
        out.append(i - 1)
        i -= lowbit(i)
    return out


def flip_set(n: int, j: int) -> list[int]:
    i = j + 1
    out = []
    k = 1
    while k < lowbit(i):
        out.append(i - k - 1)
        k *= 2
    return out


def remainder_set(n: int, j: int) -> list[int]:
    f = set(flip_set(n, j))
    return [q for q in parity_set(n, j) if q not in f]  # @line L3


def bk_ladder(n: int, j: int, is_dagger: bool) -> dict:
    if not 0 <= j < n:
        raise ValueError("mode out of range")
    xu = {q: "X" for q in update_set(n, j)}
    zp = {q: "Z" for q in parity_set(n, j)}
    zr = {q: "Z" for q in remainder_set(n, j)}
    s1 = pauli_on(n, {**xu, **zp, j: "X"})
    s2 = pauli_on(n, {**xu, **zr, j: "Y"})
    return {s1: 0.5 + 0j, s2: (-0.5j if is_dagger else 0.5j)}  # @line L4


def bravyi_kitaev(n: int, terms: list) -> dict:
    """The image of a fermionic operator given as (coefficient, word) pairs."""
    out: dict = {}
    for coef, word in terms:
        w = {"I" * n: 1 + 0j}
        for j, is_dagger in word:
            w = qop_mul(w, bk_ladder(n, j, is_dagger))  # @line L5
        out = qop_add(out, qop_scale(w, coef))  # @line L6
    out = qop_clean(out)
    return out  # @line L7


def encode(n: int, x: int) -> int:
    """The BK basis index of the occupation index x: b = beta f mod 2."""
    beta = bk_matrix(n)
    b = 0
    for i in range(n):
        s = 0
        for k in range(n):
            s ^= beta[i][k] & (x >> k)
        if s & 1:
            b |= 1 << i
    return b
