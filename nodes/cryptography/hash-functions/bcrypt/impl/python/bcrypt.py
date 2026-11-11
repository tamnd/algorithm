# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bcrypt/. The authors are listed in prov/PKNJPH.jsonl.
"""bcrypt (Provos and Mazieres, USENIX 1999), version $2b$, with its own Blowfish.

The Blowfish tables are the hexadecimal digits of the fractional part of pi.
The code computes them with exact integer arithmetic (Machin's formula
pi = 16 arctan(1/5) - 4 arctan(1/239)) instead of copying 1042 words.

For study only. The code is not constant time and must not protect real data.
Use the bcrypt package of pyca, the crypt_blowfish code of Openwall, or better
Argon2id from libsodium or argon2-cffi, instead.
"""

M32 = 0xFFFFFFFF
ROUNDS = 16
ALPHABET = b"./ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
CTEXT = b"OrpheanBeholderScryDoubt"


def _arctan_inv(x: int, one: int) -> int:
    """arctan(1/x) * one, by the alternating Taylor series in integers."""
    total, power, n, sign = 0, one // x, 1, 1
    while power:
        total += sign * (power // n)
        power //= x * x
        n += 2
        sign = -sign
    return total


def pi_hex_words(count: int) -> list[int]:
    """The first `count` 32-bit words of the fractional part of pi in hexadecimal."""
    bits = 32 * count + 64  # 64 guard bits
    one = 1 << bits
    pi = 16 * _arctan_inv(5, one) - 4 * _arctan_inv(239, one)
    frac = (pi - 3 * one) >> 64
    return [(frac >> (32 * (count - 1 - i))) & M32 for i in range(count)]


_PI = pi_hex_words(18 + 4 * 256)
P_INIT = _PI[:18]
S_INIT = [_PI[18 + 256 * b : 18 + 256 * (b + 1)] for b in range(4)]


class Blowfish:
    """Blowfish state: the P-array of 18 words and four S-boxes of 256 words."""

    def __init__(self) -> None:
        self.p = list(P_INIT)
        self.s = [list(box) for box in S_INIT]

    def _f(self, x: int) -> int:
        s = self.s
        h = (s[0][x >> 24] + s[1][(x >> 16) & 0xFF]) & M32
        return ((h ^ s[2][(x >> 8) & 0xFF]) + s[3][x & 0xFF]) & M32

    def encrypt(self, left: int, right: int) -> tuple[int, int]:
        p = self.p
        for i in range(0, ROUNDS, 2):
            left ^= p[i]
            right ^= self._f(left)
            right ^= p[i + 1]
            left ^= self._f(right)
        return right ^ p[17], left ^ p[16]

    def expand_key(self, salt: bytes | None, key: bytes) -> None:
        """ExpandKey(state, salt, key) of the paper; salt None means the all-zero salt."""
        kpos = 0
        for i in range(18):
            word = 0
            for _ in range(4):
                word = (word << 8) | key[kpos]
                kpos = (kpos + 1) % len(key)
            self.p[i] ^= word
        spos = 0

        def salt_word() -> int:
            nonlocal spos
            if salt is None:
                return 0
            w = int.from_bytes(salt[spos : spos + 4], "big")
            spos = (spos + 4) % len(salt)
            return w

        left = right = 0
        tables = [self.p] + self.s
        for table in tables:
            for i in range(0, len(table), 2):
                left ^= salt_word()
                right ^= salt_word()
                left, right = self.encrypt(left, right)
                table[i], table[i + 1] = left, right


def blowfish_key_schedule(key: bytes) -> Blowfish:
    """The ordinary Blowfish key schedule: ExpandKey with a zero salt, once."""
    state = Blowfish()
    state.expand_key(None, key)
    return state


def eks_blowfish_setup(cost: int, salt: bytes, key: bytes) -> Blowfish:
    """EksBlowfishSetup(cost, salt, key): the expensive key schedule."""
    state = Blowfish()  # @line L5
    state.expand_key(salt, key)  # @line L6
    for _ in range(1 << cost):
        state.expand_key(None, key)  # @line L7
        state.expand_key(None, salt)  # @line L7
    return state


def b64_encode(data: bytes) -> bytes:
    """bcrypt base64: the alphabet ./A-Za-z0-9, no padding, big-endian bit groups."""
    out = bytearray()
    for i in range(0, len(data), 3):
        chunk = data[i : i + 3]
        n = int.from_bytes(chunk.ljust(3, b"\x00"), "big")
        chars = len(chunk) + 1
        for j in range(chars):
            out.append(ALPHABET[(n >> (18 - 6 * j)) & 63])
    return bytes(out)


def b64_decode(text: bytes, n_bytes: int) -> bytes:
    n = 0
    for ch in text:
        n = (n << 6) | ALPHABET.index(ch)
    total_bits = 6 * len(text)
    return (n >> (total_bits - 8 * n_bytes)).to_bytes(n_bytes, "big")


def bcrypt_raw(password: bytes, salt: bytes, cost: int) -> bytes:
    """The 23 output bytes of bcrypt version $2b$ (OpenBSD)."""
    if not 4 <= cost <= 31 or len(salt) != 16:
        raise ValueError("cost must be in 4..31 and the salt must have 16 bytes")
    key = password[:72] + b"\x00"  # @line L1
    state = eks_blowfish_setup(cost, salt, key)  # @line L2
    words = [int.from_bytes(CTEXT[i : i + 4], "big") for i in range(0, 24, 4)]
    for _ in range(64):
        for j in range(0, 6, 2):
            words[j], words[j + 1] = state.encrypt(words[j], words[j + 1])  # @line L3
    return b"".join(w.to_bytes(4, "big") for w in words)[:23]


def hashpw(password: bytes, setting: bytes) -> bytes:
    """bcrypt in modular crypt format; setting is $2b$NN$ followed by 22 salt characters."""
    prefix, cost_text, rest = setting[:4], setting[4:6], setting[7:29]
    if prefix not in (b"$2a$", b"$2b$", b"$2y$") or setting[6:7] != b"$" or len(rest) != 22:
        raise ValueError("bad bcrypt setting string")
    cost = int(cost_text)
    salt = b64_decode(rest, 16)
    raw = bcrypt_raw(password, salt, cost)
    return prefix + cost_text + b"$" + b64_encode(salt)[:22] + b64_encode(raw)  # @line L4


def checkpw(password: bytes, hashed: bytes) -> bool:
    """Recompute and compare. A real verifier compares in constant time (hmac.compare_digest)."""
    return hashpw(password, hashed[:29]) == hashed
