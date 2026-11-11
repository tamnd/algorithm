# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/learning-parity-with-noise/. The authors are listed in prov/QEHHHQ.jsonl.
"""Learning parity with noise (LPN): sampling, the Gaussian elimination
attack, the HB and HB+ protocols, and the GRS man-in-the-middle attack on HB+.

For study only. The code is not constant time, uses the random module, and
the attacks run only on toy sizes. HB and HB+ are not safe protocols; use a
vetted library, for example a FIPS 140 validated module, for real
authentication.

A vector of F_2^n is a Python int (bit i is coordinate i).
"""

import random
from typing import Callable, List, Optional, Sequence, Tuple

Sample = Tuple[int, int]


def dot(a: int, s: int) -> int:
    """The inner product <a, s> over F_2."""
    return bin(a & s).count("1") & 1


def bernoulli(tau: float, rng: random.Random) -> int:
    return 1 if rng.random() < tau else 0


def lpn_sample(s: int, n: int, tau: float, rng: random.Random) -> Sample:
    """One LPN sample (a, <a, s> + e) with a uniform and e ~ Ber(tau)."""
    a = rng.getrandbits(n)
    return a, dot(a, s) ^ bernoulli(tau, rng)


def uniform_sample(n: int, rng: random.Random) -> Sample:
    return rng.getrandbits(n), rng.getrandbits(1)


# ---------------------------------------------------------------- Gaussian elimination attack

def solve(samples: Sequence[Sample], n: int) -> Optional[int]:
    """The unique s with <a_i, s> = b_i for the given n equations, or None if
    the matrix is singular. Gauss-Jordan elimination over F_2."""
    rows = [(a, b) for a, b in samples]
    pivots: List[Tuple[int, int, int]] = []    # (column, row vector, right side)
    for a, b in rows:
        for c, pa, pb in pivots:
            if (a >> c) & 1:
                a ^= pa
                b ^= pb
        if a == 0:
            continue
        c = a.bit_length() - 1
        pivots = [(c2, pa ^ a, pb ^ b) if (pa >> c) & 1 else (c2, pa, pb) for c2, pa, pb in pivots]
        pivots.append((c, a, b))
    if len(pivots) < n:
        return None
    s = 0
    for c, pa, pb in pivots:
        if pb:
            s |= 1 << c
    return s


def gauss_attack(oracle: Callable[[], Sample], n: int, tau: float,
                 check: int = 100, max_iter: int = 1 << 20) -> Tuple[Optional[int], int]:
    """Draw n fresh samples, solve, and test the candidate on `check` fresh
    samples. A round succeeds when the n samples are noise free and full rank,
    which happens with probability about 0.289 (1 - tau)^n.
    Returns (secret, rounds)."""
    limit = check * (tau + (0.5 - tau) / 2)
    for rounds in range(1, max_iter + 1):
        cand = solve([oracle() for _ in range(n)], n)
        if cand is None:
            continue
        bad = sum(dot(a, cand) != b for a, b in (oracle() for _ in range(check)))
        if bad <= limit:
            return cand, rounds
    return None, max_iter


def rank_probability(n: int) -> float:
    """The probability that a uniform n x n matrix over F_2 is invertible."""
    p = 1.0
    for i in range(1, n + 1):
        p *= 1 - 2.0 ** (-i)
    return p


# ---------------------------------------------------------------- HB and HB+

class HBTag:
    """The prover of HB: it shares x with the reader and answers <a, x> + nu."""

    def __init__(self, x: int, k: int, eta: float, rng: random.Random):
        self.x, self.k, self.eta, self.rng = x, k, eta, rng

    def answer(self, a: int) -> int:
        return dot(a, self.x) ^ bernoulli(self.eta, self.rng)


def hb_authenticate(x: int, k: int, tag_answer: Callable[[int], int], rounds: int,
                    threshold: int, rng: random.Random, transcript: Optional[list] = None) -> bool:
    """The HB reader: send `rounds` random challenges, count wrong answers,
    and accept when at most `threshold` are wrong."""
    wrong = 0
    for _ in range(rounds):
        a = rng.getrandbits(k)
        z = tag_answer(a)
        if transcript is not None:
            transcript.append((a, z))
        wrong += z != dot(a, x)
    return wrong <= threshold


class HBPlusTag:
    """The prover of HB+: it sends a blinding vector b, receives a challenge
    a, and answers <a, x> + <b, y> + nu."""

    def __init__(self, x: int, y: int, k: int, eta: float, rng: random.Random):
        self.x, self.y, self.k, self.eta, self.rng = x, y, k, eta, rng
        self.b = 0

    def commit(self) -> int:
        self.b = self.rng.getrandbits(self.k)
        return self.b

    def answer(self, a: int) -> int:
        return dot(a, self.x) ^ dot(self.b, self.y) ^ bernoulli(self.eta, self.rng)


def hb_plus_authenticate(x: int, y: int, k: int, commit: Callable[[], int],
                         answer: Callable[[int], int], rounds: int, threshold: int,
                         rng: random.Random) -> bool:
    """The HB+ reader. The challenge goes through `answer`, which a man in
    the middle may wrap."""
    wrong = 0
    for _ in range(rounds):
        b = commit()
        a = rng.getrandbits(k)
        z = answer(a)
        wrong += z != (dot(a, x) ^ dot(b, y))
    return wrong <= threshold


def grs_attack(run_session: Callable[[int], bool], k: int) -> int:
    """Gilbert, Robshaw and Sibert (2005): in session i the attacker adds the
    unit vector delta = e_i to every challenge. The answers change by
    <delta, x> = x_i, so the reader accepts when x_i = 0 and rejects when
    x_i = 1. `run_session(delta)` runs one honest reader-tag session with the
    challenges perturbed by delta and returns the reader's decision."""
    x = 0
    for i in range(k):
        if not run_session(1 << i):
            x |= 1 << i
    return x


def impersonate_hb_plus(x: int) -> Tuple[Callable[[], int], Callable[[int], int]]:
    """With x known, a fake tag chooses b = 0 and answers <a, x> exactly."""
    return (lambda: 0), (lambda a: dot(a, x))
