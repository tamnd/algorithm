# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ctr-drbg/. The authors are listed in prov/D8PPZT.jsonl.

"""CTR_DRBG with AES from NIST SP 800-90A Rev. 1, Section 10.2, with Block_Cipher_df (Section 10.3.2).

The AES block cipher (FIPS 197) is implemented here in pure Python so that the module needs only the
standard library. It is for illustration and testing: it is slow and not constant time."""

from typing import Optional

# ---------------------------------------------------------------- AES (FIPS 197)


def _xtime(b: int) -> int:
    b <<= 1
    return (b ^ 0x11B) if b & 0x100 else b


def _gmul(a: int, b: int) -> int:
    r = 0
    while b:
        if b & 1:
            r ^= a
        a = _xtime(a)
        b >>= 1
    return r


def _make_sbox() -> list:
    inv = [0] * 256
    for x in range(1, 256):
        for y in range(1, 256):
            if _gmul(x, y) == 1:
                inv[x] = y
                break
    sbox = []
    for x in range(256):
        b = inv[x]
        s = b
        for k in range(1, 5):  # affine map: b xor rotl(b,1) xor ... xor rotl(b,4) xor 0x63
            s ^= ((b << k) | (b >> (8 - k))) & 0xFF
        sbox.append(s ^ 0x63)
    return sbox


SBOX = _make_sbox()
_MUL2 = [_gmul(x, 2) for x in range(256)]
_MUL3 = [_gmul(x, 3) for x in range(256)]


def aes_expand_key(key: bytes) -> list:
    """Round keys as a list of 16-byte lists (Nr + 1 of them)."""
    nk = len(key) // 4
    if len(key) not in (16, 24, 32):
        raise ValueError("AES key must have 16, 24 or 32 bytes")
    nr = nk + 6
    w = [list(key[4 * i: 4 * i + 4]) for i in range(nk)]
    rcon = 1
    for i in range(nk, 4 * (nr + 1)):
        t = list(w[i - 1])
        if i % nk == 0:
            t = [SBOX[b] for b in t[1:] + t[:1]]
            t[0] ^= rcon
            rcon = _xtime(rcon)
        elif nk > 6 and i % nk == 4:
            t = [SBOX[b] for b in t]
        w.append([a ^ b for a, b in zip(w[i - nk], t)])
    return [sum(w[4 * r: 4 * r + 4], []) for r in range(nr + 1)]


def aes_encrypt_block(round_keys: list, block: bytes) -> bytes:
    s = [b ^ k for b, k in zip(block, round_keys[0])]
    nr = len(round_keys) - 1
    for r in range(1, nr + 1):
        s = [SBOX[b] for b in s]
        # ShiftRows: byte (row i, column c) is at index 4c + i
        s = [s[(4 * (c + i) + i) % 16] for c in range(4) for i in range(4)]
        if r != nr:
            t = []
            for c in range(4):
                a0, a1, a2, a3 = s[4 * c: 4 * c + 4]
                t += [_MUL2[a0] ^ _MUL3[a1] ^ a2 ^ a3,
                      a0 ^ _MUL2[a1] ^ _MUL3[a2] ^ a3,
                      a0 ^ a1 ^ _MUL2[a2] ^ _MUL3[a3],
                      _MUL3[a0] ^ a1 ^ a2 ^ _MUL2[a3]]
            s = t
        s = [b ^ k for b, k in zip(s, round_keys[r])]
    return bytes(s)


def aes_encrypt(key: bytes, block: bytes) -> bytes:
    return aes_encrypt_block(aes_expand_key(key), block)


# ---------------------------------------------------------------- CTR_DRBG

BLOCKLEN = 16  # bytes
RESEED_INTERVAL = 2 ** 48
MAX_REQUEST_BITS = 2 ** 19


class ReseedRequired(Exception):
    pass


def _xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def bcc(round_keys: list, data: bytes) -> bytes:
    """BCC (Section 10.3.3): CBC-MAC with a zero IV over whole blocks."""
    chain = bytes(BLOCKLEN)
    for i in range(0, len(data), BLOCKLEN):
        chain = aes_encrypt_block(round_keys, _xor(chain, data[i: i + BLOCKLEN]))
    return chain


def block_cipher_df(keylen: int, data: bytes, nbytes: int) -> bytes:
    """Block_Cipher_df (Section 10.3.2) returning nbytes bytes; keylen in bytes."""
    s = len(data).to_bytes(4, "big") + nbytes.to_bytes(4, "big") + data + b"\x80"
    s += bytes(-len(s) % BLOCKLEN)
    k = aes_expand_key(bytes(range(keylen)))
    temp = b""
    i = 0
    while len(temp) < keylen + BLOCKLEN:
        iv = i.to_bytes(4, "big") + bytes(BLOCKLEN - 4)
        temp += bcc(k, iv + s)
        i += 1
    k2 = aes_expand_key(temp[:keylen])
    x = temp[keylen: keylen + BLOCKLEN]
    out = b""
    while len(out) < nbytes:
        x = aes_encrypt_block(k2, x)
        out += x
    return out[:nbytes]


class CtrDRBG:
    """CTR_DRBG with AES-128, AES-192 or AES-256, with or without the derivation function.
    The counter field is the whole block (ctr_len = blocklen), as in the CAVP vectors."""

    def __init__(self, keylen: int, entropy: bytes, nonce: bytes = b"", personalization: bytes = b"",
                 use_df: bool = True, reseed_interval: int = RESEED_INTERVAL) -> None:
        if keylen not in (16, 24, 32):
            raise ValueError("keylen must be 16, 24 or 32 bytes")
        self.keylen = keylen
        self.seedlen = keylen + BLOCKLEN
        self.strength = 8 * keylen
        self.use_df = use_df
        self.reseed_interval = reseed_interval
        if use_df:
            if 8 * len(entropy) < self.strength:
                raise ValueError("entropy input shorter than the security strength")
            seed = block_cipher_df(keylen, entropy + nonce + personalization, self.seedlen)
        else:
            if len(entropy) != self.seedlen or len(personalization) > self.seedlen:
                raise ValueError("without df, entropy must be seedlen bytes and the string at most seedlen")
            seed = _xor(entropy, personalization.ljust(self.seedlen, b"\x00"))
        self.key = bytes(keylen)
        self.V = 0
        self._rk = aes_expand_key(self.key)
        self.update(seed)
        self.reseed_counter = 1

    def _prepare(self, data: bytes) -> bytes:
        if self.use_df:
            return block_cipher_df(self.keylen, data, self.seedlen)
        if len(data) > self.seedlen:
            raise ValueError("without df, inputs are at most seedlen bytes")
        return data.ljust(self.seedlen, b"\x00")

    def _next_block(self) -> bytes:
        self.V = (self.V + 1) % (1 << (8 * BLOCKLEN))
        return aes_encrypt_block(self._rk, self.V.to_bytes(BLOCKLEN, "big"))

    def update(self, provided: bytes) -> None:
        """CTR_DRBG_Update (Section 10.2.1.2); provided has exactly seedlen bytes."""
        temp = b""
        while len(temp) < self.seedlen:
            temp += self._next_block()
        temp = _xor(temp[: self.seedlen], provided)
        self.key = temp[: self.keylen]
        self.V = int.from_bytes(temp[self.keylen:], "big")
        self._rk = aes_expand_key(self.key)

    def reseed(self, entropy: bytes, additional: bytes = b"") -> None:
        if self.use_df:
            if 8 * len(entropy) < self.strength:
                raise ValueError("entropy input shorter than the security strength")
            seed = block_cipher_df(self.keylen, entropy + additional, self.seedlen)
        else:
            if len(entropy) != self.seedlen:
                raise ValueError("without df, entropy must be seedlen bytes")
            seed = _xor(entropy, self._prepare(additional))
        self.update(seed)
        self.reseed_counter = 1

    def generate(self, nbytes: int, additional: bytes = b"", entropy: Optional[bytes] = None) -> bytes:
        """Return nbytes pseudorandom bytes. Passing entropy requests prediction resistance:
        the generator reseeds with it and the additional input first (SP 800-90A, Section 9.3.1)."""
        if 8 * nbytes > MAX_REQUEST_BITS:
            raise ValueError("request too long")
        if entropy is not None:
            self.reseed(entropy, additional)
            additional = b""
        if self.reseed_counter > self.reseed_interval:  # @line L1
            raise ReseedRequired()
        if additional:  # @line L2
            additional = self._prepare(additional)  # @line L2
            self.update(additional)  # @line L2
        else:
            additional = bytes(self.seedlen)  # @line L2
        W = b""  # @line L3
        while len(W) < nbytes:  # @line L4
            W += self._next_block()  # @line L5
        self.update(additional)  # @line L6
        self.reseed_counter += 1  # @line L7
        return W[:nbytes]  # @line L8
