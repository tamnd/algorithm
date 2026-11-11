# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gentry-fully-homomorphic-encryption/. The authors are listed in prov/V27SZY.jsonl.
#
# This is the somewhat homomorphic public-key scheme over the integers of van Dijk, Gentry,
# Halevi and Vaikuntanathan (DGHV, Eurocrypt 2010), which follows Gentry's blueprint. It is NOT
# Gentry's ideal lattice scheme of STOC 2009, and it does NOT bootstrap: there is no squashing
# and no homomorphic decryption, so it evaluates only circuits of small multiplicative depth.
# The parameters are toys and give no security.
# For study only. This code is not constant time and must not protect real data. Use a
# maintained library such as OpenFHE, Microsoft SEAL or TFHE-rs.

import random

# Toy parameters, far below the sizes of the paper (rho = lambda, eta about lambda^2,
# gamma about lambda^5, tau = gamma + lambda).
ETA = 192  # binary digits of the secret odd integer p
RHO = 16  # binary digits of the noise in the public key
RHO2 = 32  # binary digits of the extra noise in a fresh ciphertext (rho')
GAMMA = 2048  # binary digits of the public integers x_i
TAU = 24  # number of public integers besides x_0


def centered_mod(z: int, p: int) -> int:
    """The r in (-p/2, p/2] with r = z (mod p)."""
    r = z % p
    return r - p if r > p // 2 else r


def keygen(rng: random.Random, eta: int = ETA, rho: int = RHO, gamma: int = GAMMA, tau: int = TAU):
    p = rng.getrandbits(eta) | (1 << (eta - 1)) | 1  # @line L1
    while True:
        xs = []
        for _ in range(tau + 1):  # @line L2
            q = rng.randrange(0, (1 << gamma) // p)
            r = rng.randrange(-(1 << rho) + 1, 1 << rho)
            xs.append(p * q + r)
        xs.sort(reverse=True)  # @line L3
        if xs[0] % 2 == 1 and centered_mod(xs[0], p) % 2 == 0:
            return tuple(xs), p  # @line L4


def encrypt(pk, m: int, rng: random.Random, rho2: int = RHO2) -> int:
    if m not in (0, 1):
        raise ValueError("the message is one bit")
    x0, rest = pk[0], pk[1:]
    subset = [x for x in rest if rng.getrandbits(1)]  # @line L5
    r = rng.randrange(-(1 << rho2) + 1, 1 << rho2)
    return (m + 2 * r + 2 * sum(subset)) % x0  # @line L6


def add(c1: int, c2: int) -> int:
    """XOR of the plaintext bits. Integer addition, with no reduction."""
    return c1 + c2  # @line L7


def mul(c1: int, c2: int) -> int:
    """AND of the plaintext bits. Integer multiplication, with no reduction."""
    return c1 * c2  # @line L8


def decrypt(sk: int, c: int) -> int:
    return centered_mod(c, sk) % 2  # @line L9


def noise(sk: int, c: int) -> int:
    """The noise m + 2e of c, which only the key holder can see. Decryption is right while |noise| < p/2."""
    return centered_mod(c, sk)


def noise_bits(sk: int, c: int) -> int:
    return abs(noise(sk, c)).bit_length()


def full_adder(a: int, b: int, cin: int):
    """Sum and carry of three encrypted bits: multiplicative depth 1 for the carry."""
    s = add(add(a, b), cin)
    carry = add(mul(a, b), mul(cin, add(a, b)))
    return s, carry


def product(cs):
    """AND of many ciphertexts as a balanced tree, of depth ceil(log2(len(cs)))."""
    cs = list(cs)
    while len(cs) > 1:
        nxt = [mul(cs[i], cs[i + 1]) for i in range(0, len(cs) - 1, 2)]
        if len(cs) % 2:
            nxt.append(cs[-1])
        cs = nxt
    return cs[0]
