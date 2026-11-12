# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/error-detection/. The authors are listed in prov/CXD68V.jsonl.
"""Error detection with a binary linear code, its undetected error probability, and ARQ throughput.

Words are Python integers (bit i is position i). A binary linear code is given by the rows of a
generator matrix; a received word passes the check when it is a codeword, which for a linear
code means that its syndrome is zero.
"""

import random
from typing import Dict, List, Sequence


def codewords(rows: Sequence[int]) -> List[int]:
    """All 2^k codewords spanned by the generator rows (assumed independent)."""
    words = [0]
    for r in rows:
        words += [w ^ r for w in words]
    return words


def weight_distribution(rows: Sequence[int], n: int) -> List[int]:
    """A_0, ..., A_n: the number of codewords of each weight."""
    a = [0] * (n + 1)
    for c in codewords(rows):
        a[c.bit_count()] += 1
    return a


def passes_check(code: set, received: int) -> bool:
    """The detector: accept the word if and only if it is a codeword."""
    return received in code


def undetected_error_probability(a: Sequence[int], p: float) -> float:
    """P_ud = sum_{w >= 1} A_w p^w (1 - p)^(n - w) for a linear code on BSC(p).

    The error pattern e is missed exactly when e is a nonzero codeword, because c + e is then
    a codeword for every codeword c.
    """
    n = len(a) - 1
    return sum(a[w] * p ** w * (1 - p) ** (n - w) for w in range(1, n + 1))


def undetected_by_enumeration(rows: Sequence[int], n: int, p: float) -> float:
    """The same probability by brute force over all 2^n error patterns and a fixed codeword."""
    code = set(codewords(rows))
    sent = max(code)  # any codeword gives the same value for a linear code
    total = 0.0
    for e in range(1, 1 << n):
        if passes_check(code, sent ^ e):
            w = e.bit_count()
            total += p ** w * (1 - p) ** (n - w)
    return total


def even_parity_rows(k: int) -> List[int]:
    """Generator rows of the [k + 1, k, 2] single parity check code: bit k is the parity bit."""
    return [(1 << i) | (1 << k) for i in range(k)]


def throughput_selective_repeat(p_retx: float, k: int, n: int) -> float:
    """Information bits delivered per channel bit: (1 - P) k / n."""
    return (1 - p_retx) * k / n


def throughput_go_back_n(p_retx: float, window: int, k: int, n: int) -> float:
    """Each detected error costs the block and the window - 1 blocks sent after it:
    (1 - P) / (1 - P + N P) * k / n."""
    return (1 - p_retx) / (1 - p_retx + window * p_retx) * k / n


def throughput_stop_and_wait(p_retx: float, idle_bits: int, k: int, n: int) -> float:
    """Each transmission costs n + s bit times (s: the idle time for the acknowledgment):
    (1 - P) k / (n + s)."""
    return (1 - p_retx) * k / (n + idle_bits)


def simulate_arq(scheme: str, p_retx: float, blocks: int, window: int = 1, idle_bits: int = 0,
                 n: int = 1, seed: int = 1) -> float:
    """Channel bit times per delivered block, by Monte Carlo of the three ARQ schemes.

    Each transmission of a block fails (is detected in error) with probability P, independently.
    Stop-and-wait spends n + s bit times per transmission; selective repeat spends n per
    transmission; go-back-N spends n per success and N n per failure (the failed block and
    the blocks behind it in the window are sent again).
    """
    rng = random.Random(seed)
    time = 0
    for _ in range(blocks):
        while True:
            ok = rng.random() >= p_retx
            if scheme == "stop-and-wait":
                time += n + idle_bits
            elif scheme == "selective-repeat":
                time += n
            elif scheme == "go-back-n":
                time += n if ok else window * n
            else:
                raise ValueError(scheme)
            if ok:
                break
    return time / blocks
