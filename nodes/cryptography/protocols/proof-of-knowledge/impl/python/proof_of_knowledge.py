# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proof-of-knowledge/. The authors are listed in prov/2JJVZ2.jsonl.
"""A knowledge extractor for Schnorr's protocol, by rewinding.

The statement is y = g^x in a group of prime order q. Every y in the group has
a discrete logarithm, so soundness alone says nothing; the useful property is
that a prover who is accepted knows x. The extractor proves this by running
the prover twice on the same random tape with two different challenges:

    g^z1 = a y^c1 and g^z2 = a y^c2   =>   x = (z1 - z2) / (c1 - c2) mod q.

A prover is a deterministic function of (tape, challenge), as a program on a
fixed random tape is. The extractor only calls it as a black box.

For study only. The code is not constant time, the group is a toy and the
parties are local simulated objects. Use a reviewed library such as libsodium
or a FIPS 140 validated module for real keys.
"""

import hashlib
import random

# Toy group: the squares mod the safe prime p = 2039 = 2 * 1019 + 1.
P, Q, G = 2039, 1019, 4


def h_int(*parts) -> int:
    d = hashlib.sha256(b"|".join(str(x).encode() for x in parts)).digest()
    return int.from_bytes(d, "big")


def verify(y, a, c, z) -> bool:
    return pow(G, z, P) == a * pow(y, c, P) % P


class PartialProver:
    """Knows x, but only answers a fraction of (tape, challenge) pairs.

    For each tape the prover answers the challenges in a fixed set chosen by
    hashing; it answers about `percent` percent of them. This models a prover
    program that is correct only some of the time.
    """

    def __init__(self, x, percent, seed=0):
        self.x, self.percent, self.seed = x, percent, seed
        self.calls = 0

    def commit(self, tape):
        return pow(G, self.k(tape), P)

    def k(self, tape):
        return h_int("nonce", self.seed, tape) % Q

    def respond(self, tape, c):
        self.calls += 1
        if h_int("ok", self.seed, tape, c) % 100 >= self.percent:
            return None                                  # gives up
        return (self.k(tape) + c * self.x) % Q


class GuessingProver:
    """Does not know x. Guesses the challenge c* from the tape in advance.

    It sets z at random and a = g^z y^-c*, so it is accepted exactly when the
    verifier's challenge equals c*: probability 1/|C| for a uniform challenge.
    """

    def __init__(self, y, challenges):
        self.y, self.challenges = y, challenges
        self.calls = 0

    def guess(self, tape):
        return self.challenges[h_int("guess", tape) % len(self.challenges)]

    def z(self, tape):
        return h_int("z", tape) % Q

    def commit(self, tape):
        return pow(G, self.z(tape), P) * pow(self.y, -self.guess(tape) % Q, P) % P

    def respond(self, tape, c):
        self.calls += 1
        return self.z(tape) if c == self.guess(tape) else None


def run(prover, y, tape, c):
    """One run of the protocol on a fixed tape. Return z if accepted, else None."""
    a = prover.commit(tape)
    z = prover.respond(tape, c)
    if z is None or not verify(y, a, c, z):
        return None
    return z


def extract(prover, y, challenges, rng, budget=20000):
    """Rewinding extractor. Return (x, number of prover runs) or (None, runs)."""
    runs = 0
    while runs < budget:
        tape = rng.getrandbits(64)                        # @line L1
        c1 = rng.choice(challenges)                       # @line L2
        z1 = run(prover, y, tape, c1)
        runs += 1
        if z1 is None:                                    # @line L3
            continue
        for _ in range(2 * len(challenges)):              # @line L4
            if runs >= budget:
                break
            c2 = rng.choice(challenges)
            if c2 == c1:
                continue
            z2 = run(prover, y, tape, c2)                 # @line L5
            runs += 1
            if z2 is not None:                            # @line L6
                x = (z1 - z2) * pow(c1 - c2, -1, Q) % Q   # @line L7
                return x, runs
    return None, runs


def accepting_challenges(prover, y, tape, challenges):
    return [c for c in challenges if run(prover, y, tape, c) is not None]


def success_probability(prover, y, challenges, tapes):
    total = ok = 0
    for tape in tapes:
        for c in challenges:
            total += 1
            ok += run(prover, y, tape, c) is not None
    return ok / total


if __name__ == "__main__":
    rng = random.Random(1)
    x = 777
    y = pow(G, x, P)
    print(extract(PartialProver(x, 30), y, list(range(Q)), rng))
