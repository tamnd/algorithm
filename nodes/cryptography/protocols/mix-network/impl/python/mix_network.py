# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mix-network/. The authors are listed in prov/571HZE.jsonl.
"""A cascade of ElGamal re-encryption mixes.

* The group is the subgroup of prime order q of the integers modulo the
  safe prime p = 2q + 1 = 2**127 + 8799, with generator g = 4. A 128-bit
  group is a toy: real systems use elliptic curves or groups of 2048 bits
  or more.
* Trustees hold additive shares x_j of the decryption key, and the public
  key is y = g^(x_1 + ... + x_T). A sender encrypts m as (g^r, m y^r).
* Each mix of the cascade draws a random permutation, re-encrypts each
  ciphertext by multiplying it with a fresh encryption of 1, and outputs the
  results in the permuted order. No mix knows a key, and the plaintexts do
  not change.
* After the last mix, the trustees decrypt the batch together.
* A mix can prove that its output is a permuted re-encryption of its input
  with an interactive cut-and-choose proof in the style of Sako and Kilian
  (1995): it makes a shadow shuffle, and a random bit decides which of the
  two halves of the path it must open. Each round catches a cheating mix
  with probability 1/2. Neff (2001) and later proofs cost far less.
* ThresholdMix collects a batch of a fixed size before it mixes, which is
  the batching rule that the n - 1 attack exploits.

For study only. The code is not constant time and must not protect real
data. For a real election or mixnet, use a reviewed library with a proof of
shuffle, such as Verificatum or the shuffle proofs of a maintained voting
library.
"""

import secrets
from typing import List, Optional, Tuple

P = 2**127 + 8799  # a safe prime
Q = (P - 1) // 2  # prime
G = 4  # a square, so it has order Q

Ciphertext = Tuple[int, int]


def encode(m: int) -> int:
    """Map 1 <= m <= Q into the subgroup: m or P - m, whichever is a square (P = 3 mod 4)."""
    assert 1 <= m <= Q
    return m if pow(m, Q, P) == 1 else P - m


def decode(e: int) -> int:
    return e if e <= Q else P - e


# ---------------------------------------------------------------- keys, encryption, decryption


class Trustee:
    def __init__(self) -> None:
        self.x = secrets.randbelow(Q - 1) + 1  # @line L1
        self.h = pow(G, self.x, P)

    def share(self, c: Ciphertext) -> int:
        return pow(c[0], self.x, P)  # @line L8


def joint_key(trustees: List[Trustee]) -> int:
    y = 1
    for t in trustees:
        y = y * t.h % P  # @line L1
    return y


def encrypt(y: int, m: int) -> Ciphertext:
    r = secrets.randbelow(Q - 1) + 1  # @line L2
    return pow(G, r, P), encode(m) * pow(y, r, P) % P


def reencrypt(y: int, c: Ciphertext, s: int) -> Ciphertext:
    """Multiply c by the encryption (g^s, y^s) of 1."""
    return c[0] * pow(G, s, P) % P, c[1] * pow(y, s, P) % P


def decrypt_batch(trustees: List[Trustee], batch: List[Ciphertext]) -> List[int]:
    out = []
    for c in batch:
        d = 1
        for t in trustees:
            d = d * t.share(c) % P  # @line L8
        out.append(decode(c[1] * pow(d, -1, P) % P))  # @line L9
    return out


# ---------------------------------------------------------------- one mix and the cascade


def random_permutation(n: int) -> List[int]:
    """Fisher-Yates with a cryptographic random source."""
    perm = list(range(n))
    for i in range(n - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        perm[i], perm[j] = perm[j], perm[i]
    return perm


def mix(y: int, batch: List[Ciphertext], reorder: bool = True) -> Tuple[List[Ciphertext], List[int], List[int]]:
    """Return the output and the witness (pi, s): out[pi[i]] = reencrypt(batch[i], s[i]).
    reorder=False keeps the order, which is a broken mix used only for comparison."""
    n = len(batch)
    pi = random_permutation(n) if reorder else list(range(n))  # @line L3
    s = [secrets.randbelow(Q) for _ in range(n)]  # @line L4
    out: List[Ciphertext] = [(0, 0)] * n
    for i, c in enumerate(batch):
        out[pi[i]] = reencrypt(y, c, s[i])  # @line L5
    return out, pi, s  # @line L6


def cascade(y: int, batch: List[Ciphertext], k: int) -> List[List[Ciphertext]]:
    """Run k mixes in a row; return the batch after each mix (the public bulletin board)."""
    board = [batch]
    for _ in range(k):  # @line L7
        board.append(mix(y, board[-1])[0])
    return board


# ---------------------------------------------------------------- a cut-and-choose proof of shuffle


def is_shuffle(y: int, inp: List[Ciphertext], out: List[Ciphertext], perm: List[int], rand: List[int]) -> bool:
    if sorted(perm) != list(range(len(inp))) or len(out) != len(inp):
        return False
    return all(out[perm[i]] == reencrypt(y, c, rand[i]) for i, c in enumerate(inp))


def prove_shuffle(y: int, inp: List[Ciphertext], out: List[Ciphertext], pi: List[int], s: List[int], rounds: int = 20) -> bool:
    """Run the interactive proof between the mix (knows pi and s) and a verifier
    who picks a random bit in each round. Returns the verifier's verdict."""
    n = len(inp)
    for _ in range(rounds):
        sigma = random_permutation(n)  # prover: a shadow shuffle of the input
        t = [secrets.randbelow(Q) for _ in range(n)]
        shadow: List[Ciphertext] = [(0, 0)] * n
        for i, c in enumerate(inp):
            shadow[sigma[i]] = reencrypt(y, c, t[i])
        if secrets.randbelow(2) == 0:  # verifier: open input -> shadow
            ok = is_shuffle(y, inp, shadow, sigma, t)
        else:  # verifier: open shadow -> output
            phi, u = [0] * n, [0] * n
            for i in range(n):
                phi[sigma[i]] = pi[i]
                u[sigma[i]] = (s[i] - t[i]) % Q
            ok = is_shuffle(y, shadow, out, phi, u)
        if not ok:
            return False
    return True


# ---------------------------------------------------------------- a threshold mix


class ThresholdMix:
    """Wait until `size` ciphertexts have arrived, then mix and flush them all."""

    def __init__(self, y: int, size: int) -> None:
        self.y, self.size = y, size
        self.buffer: List[Ciphertext] = []

    def submit(self, c: Ciphertext) -> Optional[List[Ciphertext]]:
        self.buffer.append(c)
        if len(self.buffer) < self.size:
            return None
        out, _, _ = mix(self.y, self.buffer)
        self.buffer = []
        return out
