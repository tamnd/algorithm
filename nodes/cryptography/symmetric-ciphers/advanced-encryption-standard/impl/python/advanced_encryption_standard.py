# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/advanced-encryption-standard/. The authors are listed in prov/4E36FN.jsonl.
"""AES (FIPS 197): the cipher, the inverse cipher and the key expansion.

For study only. This code is not constant time: the S-box is a table indexed
by secret bytes, and Python itself leaks timing. Do not use it to protect real
data. Use a FIPS 140 validated module, or a library such as OpenSSL or
libsodium, instead.

The state is a list of 16 bytes in the order of FIPS 197 Section 3.4: the
byte in row r and column c is state[r + 4 * c]. A word is a list of 4 bytes.
Cost: Nr rounds, each with 16 S-box lookups, 4 column mixes and 16 XORs of
key bytes, where Nr is 10, 12 or 14 for a key of 16, 24 or 32 bytes.
"""


def gf_mul(a: int, b: int) -> int:
    """Multiply two bytes in GF(2^8) modulo m(x) = x^8 + x^4 + x^3 + x + 1."""
    p = 0
    while b:
        if b & 1:
            p ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11B
        b >>= 1
    return p


def gf_inv(a: int) -> int:
    """The inverse of a in GF(2^8), with 0 mapped to 0. It is a^254."""
    r, e, x = 1, 254, a
    while e:
        if e & 1:
            r = gf_mul(r, x)
        x = gf_mul(x, x)
        e >>= 1
    return r if a else 0


def _affine(b: int) -> int:
    """The affine map of FIPS 197 equation (5.3), with the constant c = 0x63."""
    out = 0
    for i in range(8):
        bit = (b >> i) ^ (b >> ((i + 4) % 8)) ^ (b >> ((i + 5) % 8)) ^ (b >> ((i + 6) % 8)) ^ (b >> ((i + 7) % 8)) ^ (0x63 >> i)
        out |= (bit & 1) << i
    return out


SBOX = [_affine(gf_inv(b)) for b in range(256)]
INV_SBOX = [0] * 256
for _i, _s in enumerate(SBOX):
    INV_SBOX[_s] = _i
RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]


def sub_word(w: list[int]) -> list[int]:
    return [SBOX[b] for b in w]


def rot_word(w: list[int]) -> list[int]:
    return w[1:] + w[:1]


def key_expansion(key: bytes) -> list[list[int]]:
    """Expand a 16, 24 or 32 byte key into 4 * (Nr + 1) words (FIPS 197 Section 5.2)."""
    if len(key) not in (16, 24, 32):
        raise ValueError("an AES key has 16, 24 or 32 bytes")
    nk = len(key) // 4
    nr = nk + 6
    w = [list(key[4 * i:4 * i + 4]) for i in range(nk)]  # @line L13
    for i in range(nk, 4 * nr + 4):  # @line L14
        temp = list(w[i - 1])  # @line L15
        if i % nk == 0:  # @line L16
            temp = sub_word(rot_word(temp))
            temp[0] ^= RCON[i // nk - 1]
        elif nk > 6 and i % nk == 4:  # @line L17
            temp = sub_word(temp)
        w.append([w[i - nk][j] ^ temp[j] for j in range(4)])  # @line L18
    return w  # @line L19


def add_round_key(state: list[int], w: list[list[int]], rnd: int) -> list[int]:
    """XOR the words w[4 rnd .. 4 rnd + 3] into the four columns."""
    return [state[i] ^ w[4 * rnd + i // 4][i % 4] for i in range(16)]


def sub_bytes(state: list[int]) -> list[int]:
    return [SBOX[b] for b in state]


def inv_sub_bytes(state: list[int]) -> list[int]:
    return [INV_SBOX[b] for b in state]


def shift_rows(state: list[int]) -> list[int]:
    """Row r moves r places to the left: s'[r, c] = s[r, (c + r) mod 4]."""
    return [state[r + 4 * ((c + r) % 4)] for c in range(4) for r in range(4)]


def inv_shift_rows(state: list[int]) -> list[int]:
    return [state[r + 4 * ((c - r) % 4)] for c in range(4) for r in range(4)]


def _mix(state: list[int], m: tuple[int, int, int, int]) -> list[int]:
    out = []
    for c in range(4):
        col = state[4 * c:4 * c + 4]
        for r in range(4):
            v = 0
            for j in range(4):
                v ^= gf_mul(m[(j - r) % 4], col[j])
            out.append(v)
    return out


def mix_columns(state: list[int]) -> list[int]:
    """Multiply each column by the circulant matrix with first row (02, 03, 01, 01)."""
    return _mix(state, (2, 3, 1, 1))


def inv_mix_columns(state: list[int]) -> list[int]:
    """Multiply each column by the circulant matrix with first row (0e, 0b, 0d, 09)."""
    return _mix(state, (0x0E, 0x0B, 0x0D, 0x09))


def encrypt_block(key: bytes, block: bytes, rounds: int | None = None) -> bytes:
    """Encrypt one 16-byte block. The argument rounds is for study of reduced-round AES only."""
    if len(block) != 16:
        raise ValueError("an AES block has 16 bytes")
    nr = len(key) // 4 + 6  # @line L1
    w = key_expansion(key)  # @line L2
    if rounds is not None:
        nr = rounds
    state = add_round_key(list(block), w, 0)  # @line L3
    for rnd in range(1, nr):  # @line L4
        state = sub_bytes(state)  # @line L5
        state = shift_rows(state)  # @line L6
        state = mix_columns(state)  # @line L7
        state = add_round_key(state, w, rnd)  # @line L8
    state = sub_bytes(state)  # @line L9
    state = shift_rows(state)  # @line L10
    state = add_round_key(state, w, nr)  # @line L11
    return bytes(state)  # @line L12


def decrypt_block(key: bytes, block: bytes) -> bytes:
    """The inverse cipher of FIPS 197 Section 5.3: the steps of encrypt_block in reverse order."""
    if len(block) != 16:
        raise ValueError("an AES block has 16 bytes")
    nr = len(key) // 4 + 6
    w = key_expansion(key)
    state = add_round_key(list(block), w, nr)
    for rnd in range(nr - 1, 0, -1):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, w, rnd)
        state = inv_mix_columns(state)
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    state = add_round_key(state, w, 0)
    return bytes(state)
