# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/encrypted-key-exchange/. The authors are listed in prov/MY9FM0.jsonl.
"""Diffie-Hellman EKE in the form EKE2 of Bellare, Pointcheval and Rogaway
(Eurocrypt 2000): each side sends its Diffie-Hellman value encrypted under
the password, and the session key is a hash of the names, the two values and
the shared key.

The group is the subgroup of quadratic residues modulo a safe prime p = 2q + 1.
The "ideal cipher" is a study stand-in: the group element y is first mapped
to an integer in [1, q] by min(y, p - y), which is a bijection on the
quadratic residues, and then enciphered by an 8-round Feistel network on
[0, q - 1] with HMAC-SHA512 round functions and cycle walking. Every
ciphertext in [0, q - 1] decrypts, under every password, to a valid group
element, so a wrong password cannot be ruled out by looking at the result.
This is a heuristic model of an ideal cipher, not a proven one.

The module also has a bad encoding (a password key stream XORed over the
full bit length of p) and the partition attack against it. The attack runs
only on toy parameters against local simulated parties.

For study only. The code is not constant time, and it must not protect real
data.

Lines marked L1 to L8 match the pseudocode on the page.
"""

import hashlib
import hmac
import secrets

# RFC 5054, Appendix A, the 1024-bit group: a safe prime. g = 4 = 2^2 generates the subgroup of order q.
P_1024 = int(
    "EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C"
    "9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE4"
    "8E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B29"
    "7BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9A"
    "FD5138FE8376435B9FC61D2FC0EB06E3",
    16,
)
# A toy safe prime of 128 bits for the attack demonstration.
P_TOY = 255211775190703847597530955573826162347
G = 4
ROUNDS = 8


class Group:
    def __init__(self, p: int, g: int = G):
        self.p, self.q, self.g = p, (p - 1) // 2, g
        self.k = (self.q.bit_length() + 1) // 2 * 2      # an even number of bits with 2^k > q
        self.nbytes = (p.bit_length() + 7) // 8

    def is_qr(self, y: int) -> bool:
        return 0 < y < self.p and pow(y, self.q, self.p) == 1


# ---------------------------------------------------------------- the careful encoding: an ideal-cipher stand-in


def _round(key: bytes, i: int, half: int, bits: int) -> int:
    nbytes = (bits + 7) // 8
    out, ctr = b"", 0
    while len(out) < nbytes:
        out += hmac.new(key, bytes([i, ctr]) + half.to_bytes(nbytes, "big"), hashlib.sha512).digest()
        ctr += 1
    return int.from_bytes(out[:nbytes], "big") & ((1 << bits) - 1)


def _feistel(key: bytes, x: int, k: int, inverse: bool) -> int:
    h = k // 2
    mask = (1 << h) - 1
    left, right = x >> h, x & mask
    if not inverse:
        for i in range(ROUNDS):
            left, right = right, left ^ _round(key, i, right, h)
    else:
        for i in reversed(range(ROUNDS)):
            left, right = right ^ _round(key, i, left, h), left
    return (left << h) | right


def _prp(key: bytes, x: int, grp: Group, inverse: bool = False) -> int:
    """A permutation of [0, q - 1]: the Feistel network on k bits with cycle walking."""
    x = _feistel(key, x, grp.k, inverse)
    while x >= grp.q:
        x = _feistel(key, x, grp.k, inverse)
    return x


def password_key(pw: bytes) -> bytes:
    return hashlib.sha256(b"EKE study key" + pw).digest()


def encrypt(pw: bytes, y: int, grp: Group) -> int:
    z = min(y, grp.p - y)                       # a quadratic residue to [1, q], one to one
    return _prp(password_key(pw), z - 1, grp)


def decrypt(pw: bytes, c: int, grp: Group) -> int:
    if not 0 <= c < grp.q:
        raise ValueError("not a ciphertext")
    z = _prp(password_key(pw), c, grp, inverse=True) + 1
    return z if grp.is_qr(z) else grp.p - z     # exactly one of z and p - z is a residue


# ---------------------------------------------------------------- EKE2


def H(*parts: bytes) -> bytes:
    return hashlib.sha256(b"".join(len(x).to_bytes(4, "big") + x for x in parts)).digest()


def i2b(x: int, grp: Group) -> bytes:
    return x.to_bytes(grp.nbytes, "big")


def start(pw: bytes, grp: Group, rng=secrets.randbelow):
    x = 1 + rng(grp.q - 1)                                      # @line L1
    X = pow(grp.g, x, grp.p)
    return x, X, encrypt(pw, X, grp)                            # @line L2


def finish(pw: bytes, me: bytes, peer: bytes, initiator: bool, x: int, X: int, peer_ct: int, grp: Group) -> bytes:
    Y = decrypt(pw, peer_ct, grp)                               # @line L5
    K = pow(Y, x, grp.p)                                        # @line L6
    if K == 1:                                                  # @line L7
        raise ValueError("degenerate key")
    a, b, ga, gb = (me, peer, X, Y) if initiator else (peer, me, Y, X)
    return H(a, b, i2b(ga, grp), i2b(gb, grp), i2b(K, grp))    # @line L8


def run(pw_a: bytes, pw_b: bytes, grp: Group, rng=secrets.randbelow):
    """One EKE2 run between A and B. Returns (sk_A, sk_B)."""
    x, X, Xc = start(pw_a, grp, rng)            # @line L3: A sends "A", Xc to B
    y, Y, Yc = start(pw_b, grp, rng)            # @line L4: B sends "B", Yc to A
    sk_b = finish(pw_b, b"B", b"A", False, y, Y, Xc, grp)
    sk_a = finish(pw_a, b"A", b"B", True, x, X, Yc, grp)
    return sk_a, sk_b


# ---------------------------------------------------------------- the bad encoding and the partition attack


def _stream(pw: bytes, nbits: int) -> int:
    nbytes = (nbits + 7) // 8
    out, ctr = b"", 0
    while len(out) < nbytes:
        out += hashlib.sha256(b"bad stream" + pw + ctr.to_bytes(4, "big")).digest()
        ctr += 1
    return int.from_bytes(out[:nbytes], "big") & ((1 << nbits) - 1)


def bad_encrypt(pw: bytes, y: int, grp: Group) -> int:
    """XOR a password key stream over the full bit length of p. This leaks."""
    return y ^ _stream(pw, grp.p.bit_length())


def bad_decrypt(pw: bytes, c: int, grp: Group) -> int:
    return c ^ _stream(pw, grp.p.bit_length())


def partition_attack(transcripts, dictionary, dec, grp: Group):
    """A passive attacker keeps only the passwords under which every seen ciphertext
    decrypts to a valid group element (in [1, p - 1] and a quadratic residue)."""
    alive = list(dictionary)
    for c in transcripts:
        keep = []
        for pw in alive:
            try:
                y = dec(pw, c, grp)
            except ValueError:
                continue
            if grp.is_qr(y):
                keep.append(pw)
        alive = keep
    return alive
