# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hmac-drbg/. The authors are listed in prov/8PDZN0.jsonl.

"""HMAC_DRBG from NIST SP 800-90A Rev. 1, Section 10.1.2."""

import hashlib
import hmac
from typing import Optional

# highest security strength for each approved hash (SP 800-90A Table 2)
STRENGTH = {
    "sha1": 128,
    "sha224": 192,
    "sha512_224": 192,
    "sha256": 256,
    "sha512_256": 256,
    "sha384": 256,
    "sha512": 256,
}
RESEED_INTERVAL = 2 ** 48
MAX_REQUEST_BITS = 2 ** 19


class ReseedRequired(Exception):
    pass


class HmacDRBG:
    def __init__(self, name: str, entropy: bytes, nonce: bytes, personalization: bytes = b"",
                 reseed_interval: int = RESEED_INTERVAL, check_entropy: bool = True) -> None:
        if name not in STRENGTH:
            raise ValueError("unsupported hash function")
        self.name = name
        self.strength = STRENGTH[name]
        self.outlen = hashlib.new(name).digest_size
        self.reseed_interval = reseed_interval
        if check_entropy and 8 * len(entropy) < self.strength:
            raise ValueError("entropy input shorter than the security strength")
        self.K = b"\x00" * self.outlen
        self.V = b"\x01" * self.outlen
        self.update(entropy + nonce + personalization)
        self.reseed_counter = 1

    def _hmac(self, key: bytes, data: bytes) -> bytes:
        return hmac.new(key, data, self.name).digest()

    def update(self, data: bytes) -> None:
        """HMAC_DRBG_Update (Section 10.1.2.2)."""
        self.K = self._hmac(self.K, self.V + b"\x00" + data)
        self.V = self._hmac(self.K, self.V)
        if not data:
            return
        self.K = self._hmac(self.K, self.V + b"\x01" + data)
        self.V = self._hmac(self.K, self.V)

    def reseed(self, entropy: bytes, additional: bytes = b"") -> None:
        if 8 * len(entropy) < self.strength:
            raise ValueError("entropy input shorter than the security strength")
        self.update(entropy + additional)
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
            self.update(additional)  # @line L2
        W = b""  # @line L3
        while len(W) < nbytes:  # @line L4
            self.V = self._hmac(self.K, self.V)  # @line L5
            W += self.V  # @line L5
        self.update(additional)  # @line L6
        self.reseed_counter += 1  # @line L7
        return W[:nbytes]  # @line L8


# RFC 6979, Section 3.2: deterministic nonce for DSA and ECDSA, an HMAC_DRBG instance
def _bits2int(b: bytes, qlen: int) -> int:
    x = int.from_bytes(b, "big")
    blen = 8 * len(b)
    return x >> (blen - qlen) if blen > qlen else x


def rfc6979_k(q: int, x: int, message: bytes, name: str = "sha256") -> int:
    """The nonce k of RFC 6979 for private key x, group order q and the given message."""
    qlen = q.bit_length()
    rlen = (qlen + 7) // 8
    h1 = hashlib.new(name, message).digest()
    z = _bits2int(h1, qlen) % q
    drbg = HmacDRBG(name, x.to_bytes(rlen, "big"), z.to_bytes(rlen, "big"), check_entropy=False)
    while True:
        k = _bits2int(drbg.generate(rlen), qlen)
        if 1 <= k < q:
            return k
