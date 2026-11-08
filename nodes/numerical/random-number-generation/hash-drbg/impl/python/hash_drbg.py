# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hash-drbg/. The authors are listed in prov/XX9PAT.jsonl.

"""Hash_DRBG from NIST SP 800-90A Rev. 1, Section 10.1.1, with Hash_df from Section 10.3.1."""

import hashlib
from typing import Optional

# seedlen in bits and highest security strength for each approved hash (SP 800-90A Table 2)
PARAMS = {
    "sha1": (440, 128),
    "sha224": (440, 192),
    "sha512_224": (440, 192),
    "sha256": (440, 256),
    "sha512_256": (440, 256),
    "sha384": (888, 256),
    "sha512": (888, 256),
}
RESEED_INTERVAL = 2 ** 48
MAX_REQUEST_BITS = 2 ** 19


class ReseedRequired(Exception):
    pass


def hash_df(name: str, data: bytes, nbits: int) -> bytes:
    """Hash_df: Hash(counter || nbits as 32-bit || data) for counter = 1, 2, ..., truncated to nbits."""
    if nbits % 8:
        raise ValueError("this implementation works in whole bytes")
    out = b""
    counter = 1
    while 8 * len(out) < nbits:
        out += hashlib.new(name, bytes([counter]) + nbits.to_bytes(4, "big") + data).digest()
        counter += 1
    return out[: nbits // 8]


class HashDRBG:
    def __init__(self, name: str, entropy: bytes, nonce: bytes, personalization: bytes = b"",
                 reseed_interval: int = RESEED_INTERVAL) -> None:
        if name not in PARAMS:
            raise ValueError("unsupported hash function")
        self.name = name
        self.seedlen, self.strength = PARAMS[name]
        self.mod = 1 << self.seedlen
        self.reseed_interval = reseed_interval
        if 8 * len(entropy) < self.strength:
            raise ValueError("entropy input shorter than the security strength")
        seed = hash_df(name, entropy + nonce + personalization, self.seedlen)
        self.V = int.from_bytes(seed, "big")
        self.C = self._derive_c()
        self.reseed_counter = 1

    def _hash(self, data: bytes) -> bytes:
        return hashlib.new(self.name, data).digest()

    def _vbytes(self, v: int) -> bytes:
        return v.to_bytes(self.seedlen // 8, "big")

    def _derive_c(self) -> int:
        return int.from_bytes(hash_df(self.name, b"\x00" + self._vbytes(self.V), self.seedlen), "big")

    def reseed(self, entropy: bytes, additional: bytes = b"") -> None:
        if 8 * len(entropy) < self.strength:
            raise ValueError("entropy input shorter than the security strength")
        seed = hash_df(self.name, b"\x01" + self._vbytes(self.V) + entropy + additional, self.seedlen)
        self.V = int.from_bytes(seed, "big")
        self.C = self._derive_c()
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
            w = int.from_bytes(self._hash(b"\x02" + self._vbytes(self.V) + additional), "big")
            self.V = (self.V + w) % self.mod
        data, W = self.V, b""  # @line L3
        while len(W) < nbytes:  # @line L4
            W += self._hash(self._vbytes(data))  # @line L5
            data = (data + 1) % self.mod  # @line L5
        H = int.from_bytes(self._hash(b"\x03" + self._vbytes(self.V)), "big")  # @line L6
        self.V = (self.V + H + self.C + self.reseed_counter) % self.mod  # @line L7
        self.reseed_counter += 1  # @line L8
        return W[:nbytes]  # @line L9
