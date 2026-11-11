# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/threshold-cryptography/. The authors are listed in prov/HRY17J.jsonl.
"""Threshold ElGamal decryption (Desmedt and Frankel 1989) with Shamir
shares and Lagrange interpolation in the exponent.

* The group is the subgroup of prime order q of the integers modulo the
  safe prime p = 2q + 1 = 2**127 + 8799, with generator g = 4. A 128-bit
  group is a toy: real systems use elliptic curves of 256 bits or more.
* A dealer, or a distributed key generation (DKG) in the style of Pedersen
  (1991) with Feldman commitments, gives each of n servers a Shamir share
  x_i of the secret key x, and publishes y = g^x and y_i = g^(x_i).
* To decrypt (c1, c2), each server in a set S of at least t servers sends
  d_i = c1^(x_i) and proves with an interactive Chaum-Pedersen proof that
  log_g y_i = log_c1 d_i. The combiner computes c1^x as the product of
  d_i^(lambda_i), with lambda_i the Lagrange coefficients of S at zero.

For study only. The code is not constant time and must not protect real
data. Use a reviewed threshold library, for example the threshold modes of
a maintained MPC or threshold signing library.
"""

import itertools
import secrets
from typing import Dict, Iterable, List, Optional, Tuple

P = 2**127 + 8799  # a safe prime
Q = (P - 1) // 2  # prime
G = 4  # a square, so it has order Q


# ---------------------------------------------------------------- Shamir secret sharing, local copy


def poly_eval(coeffs: List[int], x: int) -> int:
    acc = 0
    for c in reversed(coeffs):
        acc = (acc * x + c) % Q
    return acc


def shamir_split(secret: int, t: int, n: int) -> Tuple[Dict[int, int], List[int]]:
    """Shares f(1), ..., f(n) of a random polynomial of degree t - 1 with f(0) = secret."""
    coeffs = [secret % Q] + [secrets.randbelow(Q) for _ in range(t - 1)]
    return {i: poly_eval(coeffs, i) for i in range(1, n + 1)}, coeffs


def lagrange_at_zero(xs: Iterable[int], i: int) -> int:
    """lambda_i = prod over j != i of j / (j - i), modulo Q."""
    num, den = 1, 1
    for j in xs:
        if j != i:
            num = num * j % Q
            den = den * (j - i) % Q
    return num * pow(den, -1, Q) % Q


def shamir_combine(shares: Dict[int, int]) -> int:
    return sum(s * lagrange_at_zero(shares, i) for i, s in shares.items()) % Q


# ---------------------------------------------------------------- messages as group elements


def encode(m: int) -> int:
    """Map 1 <= m <= Q into the subgroup: m or P - m, whichever is a square (P = 3 mod 4)."""
    assert 1 <= m <= Q
    return m if pow(m, Q, P) == 1 else P - m


def decode(e: int) -> int:
    return e if e <= Q else P - e


# ---------------------------------------------------------------- keys, encryption and partial decryption


class Server:
    def __init__(self, index: int, share: int) -> None:
        self.index, self.share = index, share

    def partial(self, c1: int) -> int:
        return pow(c1, self.share, P)

    def prove(self, c1: int):
        """Chaum-Pedersen: an interactive proof that log_G(y_i) = log_c1(d_i). Yields the
        commitment, takes the challenge, returns the response."""
        w = secrets.randbelow(Q)
        e = yield (pow(G, w, P), pow(c1, w, P))
        yield (w + e * self.share) % Q


class PublicKey:
    def __init__(self, y: int, verification: Dict[int, int], t: int) -> None:
        self.y, self.verification, self.t = y, verification, t


def deal(t: int, n: int) -> Tuple[PublicKey, List[Server]]:
    """A trusted dealer picks x and hands out Shamir shares; then it must forget x."""
    x = secrets.randbelow(Q - 1) + 1
    shares, _ = shamir_split(x, t, n)
    pk = PublicKey(pow(G, x, P), {i: pow(G, s, P) for i, s in shares.items()}, t)
    return pk, [Server(i, s) for i, s in shares.items()]


def encrypt(pk: PublicKey, m: int) -> Tuple[int, int]:
    r = secrets.randbelow(Q - 1) + 1
    return pow(G, r, P), encode(m) * pow(pk.y, r, P) % P


def check_partial(pk: PublicKey, server: Server, c1: int, d: int) -> bool:
    """Run the Chaum-Pedersen proof with server as the prover and a random challenge."""
    proof = server.prove(c1)
    a1, a2 = next(proof)
    e = secrets.randbelow(Q)
    z = proof.send(e)
    yi = pk.verification[server.index]
    return pow(G, z, P) == a1 * pow(yi, e, P) % P and pow(c1, z, P) == a2 * pow(d, e, P) % P


def combine(c: Tuple[int, int], partials: Dict[int, int]) -> int:
    """c1^x from the partial decryptions of a set S, then m = c2 / c1^x."""
    c1, c2 = c
    s = 1
    for i, d in partials.items():
        s = s * pow(d, lagrange_at_zero(partials, i), P) % P
    return decode(c2 * pow(s, -1, P) % P)


def threshold_decrypt(pk: PublicKey, servers: List[Server], c: Tuple[int, int]) -> int:
    """Collect partial decryptions, drop those whose proof fails, and combine any t good ones."""
    good: Dict[int, int] = {}
    for srv in servers:
        d = srv.partial(c[0])
        if check_partial(pk, srv, c[0], d):
            good[srv.index] = d
        if len(good) == pk.t:
            return combine(c, good)
    raise ValueError("fewer than t valid partial decryptions")


# ---------------------------------------------------------------- distributed key generation (Pedersen 1991, Feldman commitments)


def feldman_check(commitments: List[int], i: int, share: int) -> bool:
    """g^share must equal the product of C_k^(i^k)."""
    rhs = 1
    for k, ck in enumerate(commitments):
        rhs = rhs * pow(ck, pow(i, k, Q), P) % P
    return pow(G, share, P) == rhs


def dkg(t: int, n: int, cheater: Optional[int] = None) -> Tuple[PublicKey, List[Server], List[int]]:
    """Each party deals a random secret with Feldman commitments; a party whose
    share fails the check is disqualified. The key share of party j is the sum
    of the shares it got from the qualified dealers. cheater sends one bad share."""
    deals = {}
    for d in range(1, n + 1):
        shares, coeffs = shamir_split(secrets.randbelow(Q), t, n)
        if d == cheater:
            shares[1 if d != 1 else 2] = (shares[1 if d != 1 else 2] + 1) % Q
        deals[d] = (shares, [pow(G, c, P) for c in coeffs])
    disqualified = sorted(d for d, (sh, cm) in deals.items() if not all(feldman_check(cm, j, sh[j]) for j in sh))
    qual = [d for d in deals if d not in disqualified]
    servers = [Server(j, sum(deals[d][0][j] for d in qual) % Q) for j in range(1, n + 1)]
    y = 1
    verification = {j: 1 for j in range(1, n + 1)}
    for d in qual:
        cm = deals[d][1]
        y = y * cm[0] % P
        for j in verification:  # g^(x_j) from public values only
            for k, ck in enumerate(cm):
                verification[j] = verification[j] * pow(ck, pow(j, k, Q), P) % P
    return PublicKey(y, verification, t), servers, disqualified


def subsets(servers: List[Server], k: int):
    return itertools.combinations(servers, k)
