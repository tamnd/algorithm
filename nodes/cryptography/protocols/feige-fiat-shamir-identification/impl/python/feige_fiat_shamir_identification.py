# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/feige-fiat-shamir-identification/. The authors are listed in prov/TZZGFT.jsonl.
"""The Feige-Fiat-Shamir identification scheme over a Blum integer.

n = p q with p = q = 3 (mod 4). The prover holds k secrets s_1..s_k and
publishes v_j = (-1)^b_j s_j^-2 mod n. A round:

    prover:   r <- Z_n^*, b <- {0, 1},  x = (-1)^b r^2 mod n
    verifier: e <- {0, 1}^k
    prover:   y = r * prod(s_j for e_j = 1) mod n
    verifier: accept iff x != 0 and y^2 * prod(v_j for e_j = 1) = +x or -x mod n

A cheating prover passes a round with probability 2^-k, so t rounds give
2^-kt. The random signs make each v_j and each x a uniform element of Jacobi
symbol +1, which hides whether v_j is a square.

For study only. The code is not constant time, the modulus is a toy and the
parties are local simulated objects. Use a reviewed library such as libsodium
or a FIPS 140 validated module for real authentication.
"""

import secrets
from math import gcd

# A toy Blum integer: 499 = 547 = 3 (mod 4), both prime.
P, Q = 499, 547
N = P * Q   # 272953


def jacobi(a: int, n: int) -> int:
    """The Jacobi symbol (a / n) for odd n > 0."""
    assert n > 0 and n % 2 == 1
    a %= n
    result = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0


def random_unit(n: int, rand=secrets.randbelow) -> int:
    while True:
        r = 1 + rand(n - 1)
        if gcd(r, n) == 1:
            return r


def prod_selected(values, bits, n):
    out = 1
    for v, e in zip(values, bits):
        if e:
            out = out * v % n
    return out


# ------------------------------------------------------------ the scheme
def keygen(k: int, n: int = N, rand=secrets.randbelow):
    s, v = [], []
    for _ in range(k):                                            # @line L1
        sj = random_unit(n, rand)
        sign = rand(2)
        vj = pow(sj, -2, n)                                       # @line L2
        v.append(n - vj if sign else vj)
        s.append(sj)
    return s, v


class Prover:
    def __init__(self, s, n: int = N, rand=secrets.randbelow):
        self.s, self.n, self.rand = s, n, rand

    def commit(self, r: int = None, sign: int = None) -> int:
        self.r = random_unit(self.n, self.rand) if r is None else r
        sign = self.rand(2) if sign is None else sign
        x = self.r * self.r % self.n                              # @line L3
        return self.n - x if sign else x

    def respond(self, e) -> int:
        return self.r * prod_selected(self.s, e, self.n) % self.n  # @line L5


def random_challenge(k: int, rand=secrets.randbelow):
    return [rand(2) for _ in range(k)]                            # @line L4


def verify_round(v, x: int, e, y: int, n: int = N) -> bool:
    if not 0 < x < n:                                             # @line L6
        return False
    w = y * y % n * prod_selected(v, e, n) % n                    # @line L7
    return w in (x, n - x)


def identify(prover: Prover, v, rounds: int, n: int = N, rand=secrets.randbelow) -> bool:
    for _ in range(rounds):
        x = prover.commit()
        e = random_challenge(len(v), rand)
        if not verify_round(v, x, e, prover.respond(e), n):
            return False
    return True


# ------------------------------------------------------------ cheating, roots, extraction
class GuessingProver:
    """No secrets. Guesses e* and sends x = y^2 prod(v_j^e*_j) for a random y."""

    def __init__(self, v, guess, y, n: int = N):
        self.v, self.guess, self.y, self.n = v, guess, y, n

    def commit(self) -> int:
        return self.y * self.y % self.n * prod_selected(self.v, self.guess, self.n) % self.n

    def respond(self, e) -> int:
        return self.y


def sqrt_mod_blum(a: int, p: int = P, q: int = Q) -> int:
    """A square root of a square a mod pq, with p = q = 3 mod 4, by CRT."""
    rp = pow(a, (p + 1) // 4, p)
    rq = pow(a, (q + 1) // 4, q)
    assert rp * rp % p == a % p and rq * rq % q == a % q
    return (rp * q * pow(q, -1, p) + rq * p * pow(p, -1, q)) % (p * q)


def secret_from_public(vj: int, p: int = P, q: int = Q) -> int:
    """With the factors, find s with s^2 vj = +1 or -1, for any vj of Jacobi symbol +1.

    Exactly one of vj^-1 and -vj^-1 is a square mod pq, because -1 is a
    non-square mod p and mod q and vj has the same character mod p and q.
    """
    n = p * q
    w = pow(vj, -1, n)
    for cand in (w, n - w):
        if pow(cand, (p - 1) // 2, p) == 1 and pow(cand, (q - 1) // 2, q) == 1:
            return sqrt_mod_blum(cand, p, q)
    raise ValueError("vj does not have Jacobi symbol +1")


def extract_secret(y1: int, y2: int, n: int = N) -> int:
    """Two answers for one x, to challenges that differ only in bit j (e_j = 1
    in the first): y1 / y2 is a secret s with s^2 v_j = +1 or -1."""
    return y1 * pow(y2, -1, n) % n


def simulate(v, e, y: int, sign: int, n: int = N) -> int:
    """Honest-verifier simulator: the x that makes (x, e, y) accepted."""
    x = y * y % n * prod_selected(v, e, n) % n
    return n - x if sign else x
