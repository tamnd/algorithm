# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partial-trace/. The authors are listed in prov/Z8AWR0.jsonl.
"""Partial trace of an operator on a tensor product of several systems.

The systems are listed in dims from the most significant to the least
significant part of the basis index: the space is H_0 tensor H_1 tensor ...,
and the index of |a_0>|a_1>... is the mixed-radix number a_0 a_1 ... .
For n qubits with qubit 0 as the least significant bit (see qsim.py), qubit q
is the system at position n - 1 - q.
"""

import math
from typing import List, Sequence

from qsim import Matrix, matmul, zeros


def _digits(index: int, dims: Sequence[int]) -> List[int]:
    out = [0] * len(dims)
    for pos in range(len(dims) - 1, -1, -1):
        index, out[pos] = divmod(index, dims[pos])
    return out


def _number(digits: Sequence[int], dims: Sequence[int]) -> int:
    index = 0
    for digit, dim in zip(digits, dims):
        index = index * dim + digit
    return index


def partial_trace(rho: Matrix, dims: Sequence[int], keep: Sequence[int]) -> Matrix:
    """Trace out every system whose position is not in keep.

    Entry (i, j) of rho adds to entry (i_K, j_K) of the result when the digits
    of i and j agree on every traced system. Cost O(D^2) for D = prod(dims).
    """
    keep = sorted(keep)
    traced = [p for p in range(len(dims)) if p not in keep]
    kdims = [dims[p] for p in keep]
    out = zeros(math.prod(kdims))
    total = len(rho)
    digits = [_digits(i, dims) for i in range(total)]
    for i in range(total):
        di = digits[i]
        ri = _number([di[p] for p in keep], kdims)
        for j in range(total):
            dj = digits[j]
            if all(di[p] == dj[p] for p in traced):
                out[ri][_number([dj[p] for p in keep], kdims)] += rho[i][j]
    return out


def trace_out_qubits(rho: Matrix, n: int, qubits: Sequence[int]) -> Matrix:
    """Trace out the listed qubits of an n-qubit operator (qubit 0 is the least significant bit)."""
    gone = {n - 1 - q for q in qubits}
    return partial_trace(rho, [2] * n, [p for p in range(n) if p not in gone])


def trace_out_second_by_sandwich(rho: Matrix, da: int, db: int) -> Matrix:
    """Tr_B rho = sum_j (I_A tensor <j|) rho (I_A tensor |j>), the definition by a basis of B."""
    out = zeros(da)
    for j in range(db):
        bra = [[1 if col == a * db + j else 0 for col in range(da * db)] for a in range(da)]  # I tensor <j|
        ket = [[bra[a][row] for a in range(da)] for row in range(da * db)]  # I tensor |j>
        term = matmul(matmul(bra, rho), ket)
        out = [[out[r][c] + term[r][c] for c in range(da)] for r in range(da)]
    return out
