# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/csidh/. The authors are listed in prov/QB9T1W.jsonl.

"""Toy CSIDH (Castryck, Lange, Martindale, Panny and Renes, 2018) at p = 419.

The prime is p = 4 * 3 * 5 * 7 - 1 = 419. Curves are Montgomery curves
E_A : y^2 = x^3 + A x^2 + x over F_p, given by A alone. The class group
action is computed as in Algorithm 2 of the CSIDH paper: x-only Montgomery
arithmetic, and Velu-type isogenies of odd degree in the x-only form of
Costello and Hisil (2017).

The toy prime gives only 27 curves, so every key falls to a table lookup.
This is for study only and is not constant time: the number of loop rounds
and the isogeny degrees depend on the secret. Real CSIDH-512 uses 74 primes
and a 511-bit p (see csidh512_prime), and even that size is now thought to
fall short of NIST category 1 against quantum attacks. For production key
exchange use ML-KEM from a FIPS 140 validated module.
"""

import random

TOY_P = 419
TOY_ELLS = (3, 5, 7)


def is_square(c: int, p: int) -> bool:
    """Euler's criterion: True when c is a square mod p (0 counts)."""
    c %= p
    return c == 0 or pow(c, (p - 1) // 2, p) == 1


def xdbl(P, a24: int, p: int):
    """x-only doubling on E_A in projective (X : Z), with a24 = (A + 2) / 4."""
    X, Z = P
    t1 = (X + Z) * (X + Z) % p
    t2 = (X - Z) * (X - Z) % p
    t3 = (t1 - t2) % p
    return (t1 * t2 % p, t3 * (t2 + a24 * t3) % p)


def xadd(P, Q, D, p: int):
    """x-only differential addition: x(P + Q) from x(P), x(Q) and x(P - Q) = D."""
    U = (P[0] - P[1]) * (Q[0] + Q[1]) % p
    V = (P[0] + P[1]) * (Q[0] - Q[1]) % p
    return (D[1] * (U + V) * (U + V) % p, D[0] * (U - V) * (U - V) % p)


def ladder(k: int, P, A: int, p: int):
    """The Montgomery ladder: x([k] P) in projective form."""
    a24 = (A + 2) * pow(4, -1, p) % p
    R0, R1 = (1, 0), P
    for bit in bin(k)[2:]:
        if bit == "1":
            R0, R1 = xadd(R0, R1, P, p), xdbl(R1, a24, p)
        else:
            R0, R1 = xdbl(R0, a24, p), xadd(R0, R1, P, p)
    return R0


def affine(P, p: int):
    """X / Z, or None for the point at infinity."""
    return None if P[1] % p == 0 else P[0] * pow(P[1], -1, p) % p


def isogeny(A: int, K: int, ell: int, push: list, p: int):
    """The isogeny of odd prime degree ell with kernel <K>, K given by x(K).

    Returns the new coefficient A' and the x-coordinates of the pushed points
    (None for a point in the kernel). Codomain A' = tau (A - 3 sigma) with
    tau = prod x_i^2 and sigma = 2 sum (x_i - 1 / x_i), over x_i = x([i] K) for
    i = 1, ..., (ell - 1) / 2; the map is x -> x prod ((x x_i - 1) / (x - x_i))^2.
    """
    a24 = (A + 2) * pow(4, -1, p) % p
    Kp = (K, 1)
    xs = [K]
    prev, cur = Kp, xdbl(Kp, a24, p)
    while len(xs) < (ell - 1) // 2:
        xs.append(affine(cur, p))
        prev, cur = cur, xadd(cur, Kp, prev, p)
    tau, sigma = 1, 0
    for xi in xs:
        tau = tau * xi % p
        sigma = (sigma + xi - pow(xi, -1, p)) % p
    A2 = tau * tau * (A - 6 * sigma) % p
    out = []
    for x in push:
        if x is None:
            out.append(None)
            continue
        num, den = x, 1
        for xi in xs:
            num = num * (x * xi - 1) * (x * xi - 1) % p
            den = den * (x - xi) * (x - xi) % p
        out.append(None if den == 0 else num * pow(den, -1, p) % p)
    return A2, out


def group_action(A: int, e, rng: random.Random, p: int = TOY_P, ells=TOY_ELLS) -> int:
    """[l_1^e_1 ... l_n^e_n] * E_A, by Algorithm 2 of the CSIDH paper."""
    e = list(e)
    while any(e):  # @line L1
        x = rng.randrange(1, p)  # @line L2
        s = 1 if is_square(x * x * x + A * x * x + x, p) else -1  # @line L3
        S = [i for i in range(len(ells)) if e[i] * s > 0]  # @line L4
        if not S:  # @line L4
            continue
        k = 1  # @line L5
        for i in S:
            k *= ells[i]
        Q = affine(ladder((p + 1) // k, (x, 1), A, p), p)  # @line L6
        for i in S:  # @line L7
            if Q is None:
                break
            K = affine(ladder(k // ells[i], (Q, 1), A, p), p)  # @line L8
            if K is None:  # @line L9
                continue
            A, (Q,) = isogeny(A, K, ells[i], [Q], p)  # @line L10
            k //= ells[i]  # @line L11
            e[i] -= s  # @line L11
    return A  # @line L12


def is_supersingular(A: int, rng: random.Random, p: int = TOY_P, trials: int = 8) -> bool:
    """A probabilistic check that E_A is supersingular: [p + 1] P = 0 for random P.

    Each random x gives a point on E_A or on its twist; both have p + 1
    points when E_A is supersingular. The CSIDH paper gives a better test that
    finds a point of large order; this simple one suffices for the toy.
    """
    if (A * A - 4) % p == 0:
        return False
    for _ in range(trials):
        x = rng.randrange(1, p)
        if affine(ladder(p + 1, (x, 1), A, p), p) is not None:
            return False
    return True


def keygen(rng: random.Random, bound: int = 2, p: int = TOY_P, ells=TOY_ELLS):
    """A secret exponent vector in [-bound, bound]^n and the public key A."""
    e = [rng.randint(-bound, bound) for _ in ells]
    return e, group_action(0, e, rng, p, ells)


def shared(secret, their_A: int, rng: random.Random, p: int = TOY_P, ells=TOY_ELLS) -> int:
    """The shared secret [secret] * E_B, after a check of the public key."""
    if not is_supersingular(their_A, rng, p):
        raise ValueError("public key is not a supersingular curve")
    return group_action(their_A, secret, rng, p, ells)


def csidh512_primes() -> list:
    """The 74 primes of CSIDH-512: the 73 smallest odd primes and 587."""
    out, q = [], 3
    while len(out) < 73:
        if all(q % d for d in range(3, int(q**0.5) + 1, 2)):
            out.append(q)
        q += 2
    return out + [587]


def csidh512_prime() -> int:
    """p = 4 * l_1 * ... * l_74 - 1 for CSIDH-512."""
    p = 4
    for ell in csidh512_primes():
        p *= ell
    return p - 1
