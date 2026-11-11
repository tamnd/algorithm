# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forking-lemma/. The authors are listed in prov/WQ62KQ.jsonl.
"""The general forking algorithm of Bellare and Neven, and its use on Schnorr.

general_fork runs an algorithm A two times with the same coins and the same
first oracle answers, and new answers from the fork point on. The Schnorr
part builds a toy forger in a small group, runs the fork, and extracts the
secret key from the two forgeries, as in the proof of security of the Schnorr
signature in the random oracle model.

For study only. The group has order 1019 and offers no security, and the code
is not constant time. The forger here finds the key by brute force, which is
possible only because the group is tiny; the reduction does not look inside it.
"""

import random
from typing import Callable

# An algorithm A for the lemma: A(x, answers, coins) -> (J, output), J in 0..q.
Algorithm = Callable[[object, list[int], int], tuple[int, object]]


def general_fork(algo: Algorithm, x: object, q: int, h: int, rng: random.Random):
    """The forking algorithm F_A of Bellare and Neven.

    Returns (J, h_J, out1, h2_J, out2) on success and None on failure.
    """
    coins = rng.getrandbits(64)  # @line L1
    answers = [rng.randrange(h) for _ in range(q)]  # @line L2
    j, out1 = algo(x, answers, coins)  # @line L3
    if j == 0:  # @line L4
        return None
    answers2 = answers[: j - 1] + [rng.randrange(h) for _ in range(q - j + 1)]  # @line L5
    j2, out2 = algo(x, answers2, coins)  # @line L6
    if j2 == j and answers[j - 1] != answers2[j - 1]:  # @line L7
        return j, answers[j - 1], out1, answers2[j - 1], out2
    return None  # @line L8


def fork_bound(acc: float, q: int, h: int) -> float:
    """The lower bound acc * (acc / q - 1 / h) of the general forking lemma."""
    return acc * (acc / q - 1 / h)


# ------------------------------------------------------------ Schnorr part
P = 2039
Q = 1019
G = 4


class ProgrammedOracle:
    """A random oracle whose i-th new query gets answers[i - 1]. It logs the queries."""

    def __init__(self, answers: list[int]) -> None:
        self.answers = answers
        self.table: dict[tuple, int] = {}
        self.order: list[tuple] = []

    def __call__(self, r_elem: int, msg: bytes) -> int:
        key = (r_elem, msg)
        if key not in self.table:
            if len(self.order) == len(self.answers):
                raise RuntimeError("the forger asked more than q queries")
            self.table[key] = self.answers[len(self.order)]
            self.order.append(key)
        return self.table[key]


def schnorr_verify(y: int, msg: bytes, sig: tuple[int, int], oracle: ProgrammedOracle) -> bool:
    r_elem, s = sig
    return pow(G, s, P) == r_elem * pow(y, oracle(r_elem, msg), P) % P


def toy_forger(y: int, oracle: ProgrammedOracle, coins: int, q: int) -> tuple[int, bytes, int] | None:
    """A forger that makes q hash queries and forges with probability about 1/2.

    It solves the discrete log by brute force (the group is tiny), picks the
    query index of its forgery from its coins, and gives up when the answer
    to that query is odd, so that its success depends on the oracle.
    """
    rnd = random.Random(coins)
    x, acc = 0, 1
    while acc != y:
        acc, x = acc * G % P, x + 1
    target = rnd.randrange(q)
    forgery = None
    for i in range(q):
        k = rnd.randrange(1, Q)
        r_elem = pow(G, k, P)
        msg = b"message %d" % i
        e = oracle(r_elem, msg)
        if i == target and e % 2 == 0:
            forgery = (r_elem, msg, (k + e * x) % Q)
    return forgery


def schnorr_as_algorithm(q: int) -> Algorithm:
    """Wrap the forger as an algorithm A for the lemma: J is the index of the forgery query."""

    def algo(y: object, answers: list[int], coins: int) -> tuple[int, object]:
        oracle = ProgrammedOracle(answers)
        out = toy_forger(int(y), oracle, coins, q)  # type: ignore[arg-type]
        if out is None:
            return 0, None
        r_elem, msg, s = out
        if not schnorr_verify(int(y), msg, (r_elem, s), oracle):  # type: ignore[arg-type]
            return 0, None
        return oracle.order.index((r_elem, msg)) + 1, out

    return algo


def extract_key(y: int, q: int, rng: random.Random, tries: int = 50) -> int | None:
    """The reduction: fork the forger until two forgeries share R, then solve for x."""
    algo = schnorr_as_algorithm(q)
    for _ in range(tries):
        res = general_fork(algo, y, q, Q, rng)
        if res is None:
            continue
        _, e1, (r1, m1, s1), e2, (r2, m2, s2) = res
        assert (r1, m1) == (r2, m2)  # the same query at the fork point
        x = (s1 - s2) * pow(e1 - e2, -1, Q) % Q
        if pow(G, x, P) == y:
            return x
    return None
