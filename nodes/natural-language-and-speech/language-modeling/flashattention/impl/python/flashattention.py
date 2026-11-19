# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flashattention/. The authors are listed in prov/5X6J97.jsonl.

"""FlashAttention: exact attention by blocks with an online softmax (Dao, Fu, Ermon, Rudra and Re 2022).

Shapes, with named sizes:
    Q is n x d_k, K is m x d_k, V is m x d_v.
The output is softmax(Q K^T / sqrt(d_k)) V, the same as plain attention up to
rounding. The keys are cut into T_c = ceil(m / B_c) blocks of at most B_c rows
and the queries into ceil(n / B_r) blocks of at most B_r rows. As in
Algorithm 1 of the paper, the outer loop is over key blocks and the inner
loop over query blocks; for each query row the slow memory keeps the output
row O_r, the running sum l_r and the running maximum m_r.

The function also counts the numbers moved between slow memory (HBM) and fast
memory (SRAM), under the model of the paper: every block is read from slow
memory when it is used, and O, l and m are written back after each update.

With causal=True, query i sees key j when j <= i + (m - n). A query row whose
block holds no visible key is not updated by that block.

Precondition: n, m, d_k, d_v, B_r, B_c >= 1, the shapes agree, and every
query sees at least one key.

Cost: Theta(n m (d_k + d_v)) operations, the same as plain attention.
Fast memory Theta(B_c (d_k + d_v) + B_r (d_k + d_v) + B_r B_c). Extra slow
memory Theta(n) for l and m beside the output. The number of slow-memory
transfers is io_count(n, m, d_k, d_v, B_c), which is Theta(n m d^2 / M) with
the block sizes of block_sizes(M, d).

The code takes Q, K and V as given. It does not train a network.
"""

import math
from typing import List, Sequence, Tuple

Matrix = List[List[float]]
NEG_INF = float("-inf")


def io_count(n: int, m: int, d_k: int, d_v: int, B_c: int) -> int:
    """Slow-memory transfers of flash_attention: init, K and V once, and per key block Q, O, l, m read and O, l, m written."""
    T_c = -(-m // B_c)
    return n * (d_v + 2) + m * (d_k + d_v) + T_c * n * (d_k + 2 * d_v + 4)


def standard_attention_io(n: int, m: int, d_k: int, d_v: int) -> int:
    """Slow-memory transfers of plain attention that writes S and P: read Q, K; write S; read S, write P; read P, V; write O."""
    return (n + m) * d_k + 4 * n * m + m * d_v + n * d_v


def block_sizes(M: int, d: int) -> Tuple[int, int]:
    """The block sizes (B_r, B_c) of Algorithm 1 for a fast memory of M numbers: B_c = ceil(M / 4d), B_r = min(B_c, d)."""
    if M < 1 or d < 1:
        raise ValueError("M and d must be positive")
    B_c = -(-M // (4 * d))
    return min(B_c, d), B_c


def flash_attention(
    Q: Sequence[Sequence[float]],
    K: Sequence[Sequence[float]],
    V: Sequence[Sequence[float]],
    B_r: int,
    B_c: int,
    causal: bool = False,
) -> Tuple[Matrix, int]:
    """Return (O, io): the n x d_v attention output and the number of slow-memory transfers."""
    n, m = len(Q), len(K)
    if n == 0 or m == 0 or len(V) != m:
        raise ValueError("Q and K must be non-empty and K and V must have the same number of rows")
    d_k, d_v = len(K[0]), len(V[0])
    if d_k == 0 or d_v == 0 or any(len(r) != d_k for r in Q) or any(len(r) != d_k for r in K):
        raise ValueError("the rows of Q and K must have the same positive length")
    if any(len(r) != d_v for r in V):
        raise ValueError("the rows of V must have the same length")
    if B_r < 1 or B_c < 1:
        raise ValueError("the block sizes must be positive")
    if causal and m < n:
        raise ValueError("a causal mask needs at least as many keys as queries")
    scale = 1.0 / math.sqrt(d_k)
    shift = m - n

    O = [[0.0] * d_v for _ in range(n)]  # @line L1
    ell = [0.0] * n  # @line L1
    mx = [NEG_INF] * n  # @line L1
    io = n * (d_v + 2)

    for j0 in range(0, m, B_c):  # @line L2
        cols = range(j0, min(j0 + B_c, m))
        io += len(cols) * (d_k + d_v)
        for i0 in range(0, n, B_r):  # @line L3
            rows = range(i0, min(i0 + B_r, n))
            io += len(rows) * (d_k + d_v + 2)
            for r in rows:
                S = [
                    math.fsum(Q[r][t] * K[c][t] for t in range(d_k)) * scale if not (causal and c > r + shift) else NEG_INF
                    for c in cols
                ]  # @line L4
                m_tilde = max(S)
                if m_tilde == NEG_INF:  # @line L5
                    continue
                p = [math.exp(s - m_tilde) for s in S]  # @line L6
                ell_tilde = math.fsum(p)  # @line L6
                m_new = max(mx[r], m_tilde)  # @line L7
                a = math.exp(mx[r] - m_new)  # 0 when mx[r] is -inf
                b = math.exp(m_tilde - m_new)
                ell_new = a * ell[r] + b * ell_tilde  # @line L8
                O[r] = [
                    (a * ell[r] * O[r][c] + b * math.fsum(p[k] * V[col][c] for k, col in enumerate(cols))) / ell_new
                    for c in range(d_v)
                ]  # @line L9
                mx[r], ell[r] = m_new, ell_new  # @line L10
            io += len(rows) * (d_v + 2)

    for r in range(n):
        if mx[r] == NEG_INF:
            raise ValueError(f"query {r} sees no key")
    return O, io  # @line L11
