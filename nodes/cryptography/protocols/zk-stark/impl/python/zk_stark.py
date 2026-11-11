# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zk-stark/. The authors are listed in prov/7RSZSV.jsonl.
"""FRI, the low-degree test at the core of a zk-STARK.

This file implements FRI (Fast Reed-Solomon Interactive Oracle Proof of
Proximity, Ben-Sasson, Bentov, Horesh and Riabzev, ICALP 2018), made
non-interactive with the Fiat-Shamir transform over a SHA-256 transcript.
It is NOT a full STARK: there is no AIR (algebraic intermediate
representation), no execution trace, no constraint composition and no
zero-knowledge masking. It proves only that a committed function on a domain
is close to a polynomial of degree below a bound d.

  field   p = 3 * 2^30 + 1 = 3221225473, generator 5 of the multiplicative group
  domain  the subgroup of order N = 8 d (blowup factor 8, rate 1/8)
  commit  a SHA-256 Merkle tree over the N values
  fold    f'(x^2) = (f(x) + f(-x)) / 2 + alpha (f(x) - f(-x)) / (2 x)

For study only. It is not constant time and not for real data. Use a
reviewed STARK library such as Winterfell, Plonky2 or Stone for real proofs.
"""

import hashlib
import secrets

P = 3 * 2**30 + 1
GENERATOR = 5
BLOWUP = 8
INV2 = pow(2, -1, P)


def root_of_unity(n):
    """A generator of the subgroup of order n (n divides 2^30)."""
    assert (P - 1) % n == 0
    return pow(GENERATOR, (P - 1) // n, P)


def evaluate(coeffs, xs):
    out = []
    for x in xs:
        acc = 0
        for c in reversed(coeffs):
            acc = (acc * x + c) % P
        out.append(acc)
    return out


def domain(n):
    w = root_of_unity(n)
    return [pow(w, j, P) for j in range(n)]


# ------------------------------------------------------------ Merkle tree
def leaf_hash(value):
    return hashlib.sha256(b"\x00" + value.to_bytes(4, "big")).digest()


def node_hash(left, right):
    return hashlib.sha256(b"\x01" + left + right).digest()


class MerkleTree:
    def __init__(self, values):
        n = len(values)
        assert n & (n - 1) == 0
        self.levels = [[leaf_hash(v) for v in values]]
        while len(self.levels[-1]) > 1:
            low = self.levels[-1]
            self.levels.append([node_hash(low[k], low[k + 1]) for k in range(0, len(low), 2)])

    @property
    def root(self):
        return self.levels[-1][0]

    def path(self, index):
        out = []
        for level in self.levels[:-1]:
            out.append(level[index ^ 1])
            index //= 2
        return out


def merkle_verify(root, index, value, path):
    h = leaf_hash(value)
    for sibling in path:
        h = node_hash(h, sibling) if index % 2 == 0 else node_hash(sibling, h)
        index //= 2
    return h == root


# ------------------------------------------------------------ transcript
class Transcript:
    """Fiat-Shamir: each challenge is a hash of the salt and all earlier messages."""

    def __init__(self, salt):
        self.state = hashlib.sha256(b"FRI" + salt).digest()

    def absorb(self, data):
        self.state = hashlib.sha256(self.state + data).digest()

    def challenge(self, bound):
        self.state = hashlib.sha256(self.state + b"challenge").digest()
        return int.from_bytes(self.state, "big") % bound   # bias below 2^-220


# ------------------------------------------------------------ FRI
def fold(values, alpha):
    """One FRI round: from f on a domain of size n to f' on its squares, of size n/2."""
    n = len(values)
    half = n // 2
    w = root_of_unity(n)
    out = []
    x = 1
    for j in range(half):
        a, b = values[j], values[j + half]                         # f(x), f(-x)
        even = (a + b) * INV2 % P
        odd = (a - b) * INV2 * pow(x, -1, P) % P
        out.append((even + alpha * odd) % P)                       # @line L3
        x = x * w % P
    return out


def fold_at(a, b, alpha, n, j):
    """The fold of the pair at index j of a domain of size n."""
    x = pow(root_of_unity(n), j, P)
    return ((a + b) * INV2 + alpha * (a - b) * INV2 * pow(x, -1, P)) % P


def prove(values, degree_bound, queries, salt=None, shadow=None):
    """FRI proof that `values` (on the domain of size N) has degree < degree_bound.

    For the attack test only: with `shadow`, layer 0 commits `values` but the
    later layers are the honest folds of `shadow` (a cheating prover).
    """
    salt = secrets.token_bytes(16) if salt is None else salt
    rounds = degree_bound.bit_length() - 1
    assert degree_bound == 1 << rounds
    transcript = Transcript(salt)
    funcs = [list(values)]
    source = list(values) if shadow is None else list(shadow)
    trees = [MerkleTree(funcs[0])]                                 # @line L1
    transcript.absorb(trees[0].root)
    for i in range(rounds):
        alpha = transcript.challenge(P)                            # @line L2
        source = fold(source, alpha)                               # the fold of line L3
        funcs.append(source)
        if i < rounds - 1:
            trees.append(MerkleTree(source))                       # @line L4
            transcript.absorb(trees[-1].root)
    final = funcs[-1]                                              # @line L5
    transcript.absorb(b"".join(v.to_bytes(4, "big") for v in final))
    openings = []
    n0 = len(values)
    for _ in range(queries):
        j = transcript.challenge(n0 // 2)                          # @line L6
        rows = []
        for i in range(rounds):
            n = len(funcs[i])
            k = j % (n // 2)
            rows.append((funcs[i][k], trees[i].path(k), funcs[i][k + n // 2], trees[i].path(k + n // 2)))  # @line L7
        openings.append(rows)
    return {
        "salt": salt,
        "roots": [t.root for t in trees],
        "final": final,
        "openings": openings,
    }


def replay(proof, n0, rounds, queries):
    """The verifier's copy of the transcript: the alphas and the query indices."""
    roots = proof["roots"]
    transcript = Transcript(proof["salt"])
    transcript.absorb(roots[0])
    alphas = []
    for i in range(rounds):
        alphas.append(transcript.challenge(P))
        if i < rounds - 1:
            transcript.absorb(roots[i + 1])
    transcript.absorb(b"".join(v.to_bytes(4, "big") for v in proof["final"]))
    return alphas, [transcript.challenge(n0 // 2) for _ in range(queries)]


def verify(proof, n0, degree_bound, queries):
    rounds = degree_bound.bit_length() - 1
    roots, final, openings = proof["roots"], proof["final"], proof["openings"]
    if len(roots) != rounds or len(final) != n0 >> rounds or len(openings) != queries:
        return False
    alphas, indices = replay(proof, n0, rounds, queries)          # @line L8
    if any(v != final[0] for v in final):                          # @line L11
        return False
    for j, rows in zip(indices, openings):
        for i in range(rounds):
            n = n0 >> i
            k = j % (n // 2)
            a, path_a, b, path_b = rows[i]
            if not (merkle_verify(roots[i], k, a, path_a) and merkle_verify(roots[i], k + n // 2, b, path_b)):  # @line L9
                return False
            want = fold_at(a, b, alphas[i], n, k)                  # @line L10
            m = n // 2
            if i + 1 < rounds:
                na, _, nb, _ = rows[i + 1]
                got = na if k < m // 2 else nb
            else:
                got = final[k]
            if got != want:
                return False
    return True


def proof_size(proof):
    """Bytes: 32 per hash and 4 per field element."""
    size = 32 * len(proof["roots"]) + 4 * len(proof["final"]) + len(proof["salt"])
    for rows in proof["openings"]:
        for a, pa, b, pb in rows:
            size += 8 + 32 * (len(pa) + len(pb))
    return size
