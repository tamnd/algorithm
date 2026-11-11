# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/non-malleability/. The authors are listed in prov/TMD2FZ.jsonl.
"""The NM-CPA experiment of Bellare, Desai, Pointcheval and Rogaway (1998),
run against ElGamal encryption in a group of prime order.

ElGamal is IND-CPA secure under DDH, but the experiment shows that it is not
non-malleable: from a ciphertext of x the adversary makes a ciphertext of
t * x without knowing x.

For study only. The code is not constant time and runs on a toy group.
"""

import random
from typing import Callable

# The smallest safe prime above 2^63, and 4, which generates its subgroup of
# squares, a group of prime order Q.
P = 9223372036854778487
Q = (P - 1) // 2
G = 4

Ciphertext = tuple[int, int]
Relation = Callable[[int, int], bool]


def keygen(rng: random.Random) -> tuple[int, int]:
    """Return (h, x) with h = g^x. Cost: one exponentiation."""
    x = rng.randrange(Q)
    return pow(G, x, P), x


def encrypt(h: int, m: int, rng: random.Random) -> Ciphertext:
    """ElGamal encryption of a subgroup element m. Cost: two exponentiations."""
    r = rng.randrange(Q)
    return pow(G, r, P), m * pow(h, r, P) % P


def decrypt(x: int, c: Ciphertext) -> int:
    """ElGamal decryption. Cost: one exponentiation."""
    return c[1] * pow(c[0], Q - x, P) % P


def sample_message(rng: random.Random) -> int:
    """The message distribution M of the adversary: uniform on the subgroup."""
    return pow(G, rng.randrange(Q), P)


def mauling_adversary(c: Ciphertext, t: int = G) -> tuple[Relation, list[Ciphertext]]:
    """Second stage of the adversary: output R(a, b) = [b = t a] and one new
    ciphertext (c1, t * c2), which encrypts t * x if c encrypts x."""

    def relation(a: int, b: int) -> bool:
        return b == t * a % P

    return relation, [(c[0], c[1] * t % P)]


def nm_cpa_experiment(rng: random.Random, real: bool) -> bool:
    """One run of the NM-CPA experiment; returns True if R(x or x~, x') holds.

    In the real run the relation is tested on the encrypted message x; in the
    random run on an independent sample x~ from the same distribution.
    """
    h, sk = keygen(rng)
    x, x_tilde = sample_message(rng), sample_message(rng)
    y = encrypt(h, x, rng)
    relation, ys = mauling_adversary(y)
    if y in ys:  # the adversary may not copy the challenge
        return False
    xs = [decrypt(sk, c) for c in ys]
    target = x if real else x_tilde
    return all(relation(target, xp) for xp in xs)


def nm_from_ind(guess: Callable[[Ciphertext], int], m0: int, m1: int, h: int, c: Ciphertext, rng: random.Random) -> tuple[Relation, list[Ciphertext]]:
    """The proof that NM-CPA implies IND-CPA, as an adversary: with M uniform
    on {m0, m1}, re-encrypt the message that the IND-CPA guesser picks and
    use the relation 'equal'."""
    b = guess(c)
    while True:
        out = encrypt(h, (m0, m1)[b], rng)
        if out != c:
            return (lambda a, bb: a == bb), [out]
