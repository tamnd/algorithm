# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-error-correction/. The authors are listed in prov/8PQV2E.jsonl.
"""Forward error correction with a binary linear block code on BPSK over the AWGN channel,
hard decisions and syndrome decoding, and the coding gain at a target bit error rate.

Words are Python integers (bit i is position i). The code is systematic: positions 0 .. k-1
carry the message.
"""

import math
import random
from typing import Dict, List, Sequence


def q_function(x: float) -> float:
    """Tail probability of the standard normal distribution."""
    return 0.5 * math.erfc(x / math.sqrt(2.0))


def db(x: float) -> float:
    return 10.0 * math.log10(x)


def from_db(x_db: float) -> float:
    return 10.0 ** (x_db / 10.0)


def uncoded_ber(ebn0_db: float) -> float:
    """Bit error rate of uncoded BPSK: Q(sqrt(2 Eb/N0))."""
    return q_function(math.sqrt(2.0 * from_db(ebn0_db)))


def crossover(ebn0_db: float, rate: float) -> float:
    """Channel bit error probability of coded BPSK: each code bit has energy R Eb."""
    return q_function(math.sqrt(2.0 * rate * from_db(ebn0_db)))


def encode(rows: Sequence[int], message: int) -> int:
    word = 0
    for i, r in enumerate(rows):
        if message >> i & 1:
            word ^= r
    return word


def syndrome_table(checks: Sequence[int], n: int) -> Dict[int, int]:
    """Coset leaders: for each syndrome, a least-weight error pattern with that syndrome.

    checks are the rows of a parity-check matrix; the syndrome bit j is the parity of word & checks[j].
    """
    table: Dict[int, int] = {}
    for e in sorted(range(1 << n), key=lambda v: (v.bit_count(), v)):
        s = syndrome(checks, e)
        if s not in table:
            table[s] = e
    return table


def syndrome(checks: Sequence[int], word: int) -> int:
    s = 0
    for j, h in enumerate(checks):
        s |= ((word & h).bit_count() & 1) << j
    return s


def decode(checks: Sequence[int], table: Dict[int, int], received: int, k: int) -> int:
    """Hard-decision syndrome decoding; returns the k message bits."""
    word = received ^ table[syndrome(checks, received)]
    return word & ((1 << k) - 1)


def decoded_ber(checks: Sequence[int], n: int, k: int, p: float) -> float:
    """Exact message bit error rate of syndrome decoding on BSC(p).

    For a linear code the decoding error does not depend on the codeword sent, so it is enough
    to send the zero word and sum over all 2^n error patterns.
    """
    table = syndrome_table(checks, n)
    total = 0.0
    for e in range(1 << n):
        w = e.bit_count()
        wrong = decode(checks, table, e, k).bit_count()
        if wrong:
            total += wrong * p ** w * (1 - p) ** (n - w)
    return total / k


def coded_ber(checks: Sequence[int], n: int, k: int, ebn0_db: float) -> float:
    return decoded_ber(checks, n, k, crossover(ebn0_db, k / n))


def required_ebn0_db(ber_of, target: float, lo: float = -5.0, hi: float = 20.0) -> float:
    """Least Eb/N0 in dB with ber_of(Eb/N0) <= target, by bisection (ber_of is decreasing)."""
    for _ in range(100):
        mid = (lo + hi) / 2
        if ber_of(mid) <= target:
            hi = mid
        else:
            lo = mid
    return hi


def coding_gain_db(checks: Sequence[int], n: int, k: int, target: float) -> float:
    """Coding gain at a target bit error rate: the Eb/N0 that uncoded BPSK needs minus the Eb/N0
    that the coded system needs, both per information bit."""
    uncoded = required_ebn0_db(uncoded_ber, target)
    coded = required_ebn0_db(lambda x: coded_ber(checks, n, k, x), target)
    return uncoded - coded


def asymptotic_gain_soft_db(n: int, k: int, d: int) -> float:
    """10 log10(R d): the gain of soft-decision maximum likelihood decoding as Eb/N0 grows."""
    return db(k / n * d)


def asymptotic_gain_hard_db(n: int, k: int, d: int) -> float:
    """10 log10(R (t + 1)) with t = floor((d - 1) / 2), for hard decisions."""
    return db(k / n * ((d - 1) // 2 + 1))


def simulate_ber(rows: Sequence[int], checks: Sequence[int], n: int, k: int, ebn0_db: float,
                 trials: int, rng: random.Random) -> float:
    """Monte Carlo: random messages, BPSK with Gaussian noise, hard decisions, syndrome decoding."""
    table = syndrome_table(checks, n)
    sigma = math.sqrt(1.0 / (2.0 * (k / n) * from_db(ebn0_db)))
    errors = 0
    for _ in range(trials):
        m = rng.getrandbits(k)
        c = encode(rows, m)
        r = 0
        for i in range(n):
            x = 1.0 - 2.0 * (c >> i & 1)
            if x + rng.gauss(0.0, sigma) < 0:
                r |= 1 << i
        errors += (decode(checks, table, r, k) ^ m).bit_count()
    return errors / (trials * k)


# The [7, 4, 3] Hamming code in systematic form: message bits 0..3, parity bits 4..6.
HAMMING_ROWS: List[int] = [0b0110001, 0b1010010, 0b1100100, 0b1111000]
HAMMING_CHECKS: List[int] = [0b0011011, 0b0101101, 0b1001110]
