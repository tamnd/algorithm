# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-encoding/. The authors are listed in prov/5SF402.jsonl.
"""Block encodings as explicit unitary matrices.

A block encoding of A with normalization alpha on a ancilla qubits is a unitary U
with <0^a| U |0^a> = A / alpha. The ancillas are the high qubits, so this is the
top-left block of the matrix of U.
"""

import math

from qsim import (
    complete_unitary,
    dagger,
    householder,
    identity,
    kron,
    matmul,
    matvec,
    norm,
    pauli_matrix,
    split_registers,
)


def lcu_block_encoding(terms):
    """Block encoding of H = sum_j c_j P_j by PREP^dagger SELECT PREP. Returns (U, alpha, a)."""
    n = len(terms[0][1])
    big_l = len(terms)
    lam = sum(abs(c) for c, _ in terms)  # @line L1
    a = max(1, math.ceil(math.log2(big_l)))
    m, d = 1 << a, 1 << n
    weights = [math.sqrt(abs(c) / lam) for c, _ in terms] + [0.0] * (m - big_l)
    prep = kron(householder([complex(w) for w in weights]), identity(d))  # @line L2
    select = [[0j] * (m * d) for _ in range(m * d)]  # @line L3
    for j in range(m):
        if j < big_l:
            c, s = terms[j]
            block = pauli_matrix(s)
            sign = 1.0 if c >= 0 else -1.0
        else:
            block, sign = identity(d), 1.0
        for r in range(d):
            for k in range(d):
                select[j * d + r][j * d + k] = sign * block[r][k]
    u = matmul(dagger(prep), matmul(select, prep))  # @line L4
    return u, lam, a  # @line L5


def sparse_block_encoding(h):
    """Block encoding of a sparse matrix h (2^n x 2^n) with alpha = s * max |h_jk|, s the sparsity.

    Registers, from high to low: a flag qubit, a register r1 of n qubits and the system r2.
    W_R maps |0, 0, k> to |R_k> = s^(-1/2) sum_(j in column k) (a_jk |0> + sqrt(1 - |a_jk|^2) |1>) |j> |k>
    and W_L maps |0, 0, j> to |L_j> = s^(-1/2) sum_(k in row j) |0> |j> |k>, where a_jk = h_jk / max |h|.
    Then <L_j | R_k> = a_jk / s, and U = W_L^dagger W_R. Returns (U, alpha, a = n + 1).
    """
    d = len(h)
    n = d.bit_length() - 1
    big_x = max(abs(x) for row in h for x in row)
    rows = [[k for k in range(d) if h[j][k] != 0] for j in range(d)]
    cols = [[j for j in range(d) if h[j][k] != 0] for k in range(d)]
    s = max(max(len(r) for r in rows), max(len(c) for c in cols))
    dim = 2 * d * d

    def index(b, r1, r2):
        return (b * d + r1) * d + r2

    right, left = [], []
    for k in range(d):
        v = [0j] * dim
        for j in cols[k]:
            a_jk = h[j][k] / big_x
            v[index(0, j, k)] = a_jk / math.sqrt(s)
            v[index(1, j, k)] = math.sqrt(max(0.0, 1 - abs(a_jk) ** 2)) / math.sqrt(s)
        pad = [j for j in range(d) if j not in cols[k]][: s - len(cols[k])]
        for j in pad:  # a zero entry: the flag is |1> with certainty
            v[index(1, j, k)] = 1 / math.sqrt(s)
        right.append(v)
    for j in range(d):
        v = [0j] * dim
        chosen = rows[j] + [k for k in range(d) if k not in rows[j]][: s - len(rows[j])]
        for k in chosen:
            v[index(0, j, k)] = 1 / math.sqrt(s)
        left.append(v)
    w_r = complete_unitary(right, dim)
    w_l = complete_unitary(left, dim)
    return matmul(dagger(w_l), w_r), s * big_x, n + 1


def embed_on(u, a_u, a_skip, n, skip_low):
    """Extend U on (a_u ancillas, n system qubits) to (a_u + a_skip ancillas, system) as the identity on the other ancillas.

    With skip_low the extra ancillas sit between U's ancillas and the system, otherwise above U's ancillas.
    """
    d, mu, ms = 1 << n, 1 << a_u, 1 << a_skip
    dim = mu * ms * d
    out = [[0j] * dim for _ in range(dim)]

    def idx(i_u, i_s, x):
        return ((i_u * ms + i_s) * d + x) if skip_low else ((i_s * mu + i_u) * d + x)

    for i_s in range(ms):
        for r in range(mu * d):
            for c in range(mu * d):
                val = u[r][c]
                if val != 0:
                    out[idx(r // d, i_s, r % d)][idx(c // d, i_s, c % d)] = val
    return out


def product_block_encoding(u_a, alpha, a_a, u_b, beta, a_b, n):
    """Block encoding of A B from block encodings of A and B, with separate ancillas: (U_A (x) I)(I (x) U_B)."""
    big_a = embed_on(u_a, a_a, a_b, n, skip_low=True)
    big_b = embed_on(u_b, a_b, a_a, n, skip_low=False)
    return matmul(big_a, big_b), alpha * beta, a_a + a_b


def apply_block(u, a, psi):
    """Run U on |0^a>|psi> and keep ancilla outcome 0^a. Returns (success probability, normalized state)."""
    full = list(psi) + [0j] * (((1 << a) - 1) * len(psi))
    out = matvec(u, full)
    good = split_registers(out, len(psi).bit_length() - 1)[0]
    p = norm(good) ** 2
    return p, [x / math.sqrt(p) for x in good]
