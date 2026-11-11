# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yao-millionaires-problem/. The authors are listed in prov/3E3WQE.jsonl.
"""Yao's 1982 protocol for the millionaires' problem, with toy RSA.

Alice has i and Bob has j, both in 1..n. At the end Bob knows whether
i >= j, and he tells Alice. The protocol, from Section 2 of Yao's FOCS 1982
paper, uses Alice's public-key trapdoor permutation E_A with inverse D_A:

  1. Bob picks a random x, computes k = E_A(x) and sends k - j + 1.
  2. Alice computes y_u = D_A(k - j + u) for u = 1..n.
  3. Alice picks a random prime p of about half the bit length of the
     modulus, such that the values z_u = y_u mod p differ pairwise by at
     least 2 (mod p) and 0 < z_u < p - 1.
  4. Alice sends p and z_1, ..., z_i, z_{i+1} + 1, ..., z_n + 1.
  5. Bob looks at the j-th number: it equals x mod p iff i >= j.

Alice does n private-key operations and sends n + 1 numbers, so the cost is
linear in the size n of the range, which is exponential in the bit length
of the inputs. Secure only for semi-honest parties.

For study only. The RSA key is a toy, the code is not constant time, and
Python's random module is used for coins.
"""

import random
from dataclasses import dataclass, field

# ---------------------------------------------------------------- toy RSA


def is_probable_prime(n: int) -> bool:
    """Deterministic Miller-Rabin for n < 3.3 * 10^24 (bases 2 to 41)."""
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
    for q in small:
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in small:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def random_prime(bits: int, rng: random.Random) -> int:
    while True:
        c = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(c):
            return c


@dataclass(frozen=True)
class RSAKey:
    n: int
    e: int
    d: int

    def encrypt(self, m: int) -> int:
        return pow(m, self.e, self.n)

    def decrypt(self, c: int) -> int:
        return pow(c, self.d, self.n)


def rsa_keygen(bits: int, rng: random.Random, e: int = 65537) -> RSAKey:
    """Toy RSA key; the modulus has about 2 * bits binary digits."""
    while True:
        p, q = random_prime(bits, rng), random_prime(bits, rng)
        phi = (p - 1) * (q - 1)
        if p != q and phi % e != 0:
            return RSAKey(p * q, e, pow(e, -1, phi))


# ---------------------------------------------------------------- the protocol


@dataclass
class Run:
    """What happened in one run, for the tests."""

    bob_message: int = 0                 # k - j + 1
    p: int = 0                           # Alice's prime
    alice_values: list[int] = field(default_factory=list)
    decryptions: int = 0                 # private-key operations by Alice
    primes_tried: int = 0
    result: bool = False                 # Bob's conclusion: i >= j


def well_spread(z: list[int], p: int) -> bool:
    """Yao's condition: 0 < z_u < p - 1 and |z_u - z_v| >= 2 mod p for u != v."""
    if any(not 0 < v < p - 1 for v in z):
        return False
    s = sorted(z)
    gaps = [b - a for a, b in zip(s, s[1:])] + [s[0] + p - s[-1]]
    return all(g >= 2 for g in gaps)


def millionaires(i: int, j: int, n: int, key: RSAKey, rng: random.Random) -> Run:
    """Run Yao's protocol; return Bob's view and the answer to i >= j."""
    if not (1 <= i <= n and 1 <= j <= n):
        raise ValueError("inputs must be in 1..n")
    run = Run()
    big = key.n
    # Step 1 (Bob).
    x = rng.randrange(big)
    k = key.encrypt(x)
    run.bob_message = (k - j + 1) % big
    # Step 2 (Alice): y_u = D_A(k - j + u), u = 1..n.
    y = [key.decrypt((run.bob_message + u - 1) % big) for u in range(1, n + 1)]
    run.decryptions = n
    # Step 3 (Alice): a prime of about half the length of N.
    half = max(big.bit_length() // 2, 8)
    while True:
        p = random_prime(half, rng)
        run.primes_tried += 1
        z = [v % p for v in y]
        if well_spread(z, p):
            break
    # Step 4 (Alice).
    run.p = p
    run.alice_values = [z[u - 1] if u <= i else (z[u - 1] + 1) % p for u in range(1, n + 1)]
    # Step 5 (Bob).
    run.result = run.alice_values[j - 1] == x % p
    return run


def richer_than(a: int, b: int, n: int, key: RSAKey, rng: random.Random) -> bool:
    """Decide a > b for a, b in 0..n-1, as i >= j with i = a + 1, j = b + 2.

    The range for the protocol is then 1..n + 1."""
    return millionaires(a + 1, b + 2, n + 1, key, rng).result


def message_bits(run: Run, key: RSAKey) -> int:
    """Bits sent: Bob's one number mod N, then p and n numbers mod p."""
    return key.n.bit_length() + run.p.bit_length() * (1 + len(run.alice_values))
