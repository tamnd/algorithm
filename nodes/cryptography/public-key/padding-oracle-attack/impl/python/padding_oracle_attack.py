# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/padding-oracle-attack/. The authors are listed in prov/88GNSJ.jsonl.
"""The CBC padding oracle attack of Vaudenay (Eurocrypt 2002) on a local toy server.

The file holds three parts:

1. CBC mode with PKCS #7 padding, as in the cbc-mode and pkcs7-padding pages.
2. A simulated server that decrypts a ciphertext and answers one bit: "was
   the padding valid". This is the oracle. A real server leaks the same bit
   through an error message, an alert code or a timing difference.
3. The attack, which recovers the plaintext from that bit alone, with about
   128 queries for each plaintext byte, and the matching fix.

For study only. The code is not constant time, and the attack runs only
against the simulated server in this file, on keys that the test file makes.
"""

import hashlib
from dataclasses import dataclass, field

from aes import AES

BLOCK = 16


class PaddingError(Exception):
    """Raised by the unpadding step. A real server must never report this."""


def pkcs7_pad(data: bytes, block: int = BLOCK) -> bytes:
    """Append 1 to block octets, each equal to the number of octets added."""
    count = block - len(data) % block
    return data + bytes([count]) * count


def pkcs7_unpad(data: bytes, block: int = BLOCK) -> bytes:
    """Remove the padding, or raise PaddingError."""
    if not data or len(data) % block != 0:
        raise PaddingError("bad length")
    count = data[-1]
    if count < 1 or count > block or data[-count:] != bytes([count]) * count:
        raise PaddingError("bad padding")
    return data[:-count]


def cbc_encrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    """CBC encryption with PKCS #7 padding. The output starts with the IV."""
    if len(iv) != BLOCK:
        raise ValueError("the IV has 16 bytes")
    cipher = AES(key)
    padded = pkcs7_pad(plaintext)
    out = bytearray(iv)
    previous = iv
    for start in range(0, len(padded), BLOCK):
        block = padded[start:start + BLOCK]
        previous = cipher.encrypt_block(bytes(a ^ b for a, b in zip(block, previous)))
        out.extend(previous)
    return bytes(out)


def cbc_decrypt_raw(key: bytes, ciphertext: bytes) -> bytes:
    """CBC decryption with no unpadding. The first block of the input is the IV."""
    if len(ciphertext) % BLOCK != 0 or len(ciphertext) < 2 * BLOCK:
        raise ValueError("the ciphertext must hold an IV and at least one block")
    cipher = AES(key)
    out = bytearray()
    previous = ciphertext[:BLOCK]
    for start in range(BLOCK, len(ciphertext), BLOCK):
        block = ciphertext[start:start + BLOCK]
        plain = cipher.decrypt_block(block)
        out.extend(a ^ b for a, b in zip(plain, previous))
        previous = block
    return bytes(out)


def cbc_decrypt(key: bytes, ciphertext: bytes) -> bytes:
    """CBC decryption with the padding removed."""
    return pkcs7_unpad(cbc_decrypt_raw(key, ciphertext))


@dataclass
class PaddingOracleServer:
    """A server that leaks one bit for each ciphertext: was the padding valid.

    This is the broken design. It is the "MAC-then-encrypt and report the
    padding error" shape of SSL and of TLS before the countermeasures.
    """

    key: bytes
    queries: int = 0
    limit: int = 1 << 20

    def __call__(self, ciphertext: bytes) -> bool:
        if self.queries >= self.limit:
            raise RuntimeError("the query budget is used up")
        self.queries += 1
        try:
            cbc_decrypt(self.key, ciphertext)
        except PaddingError:
            return False
        return True


@dataclass
class SafeServer:
    """The fix: encrypt-then-MAC. The MAC is checked before any unpadding.

    The server answers one bit as well, but the bit never depends on the
    padding: a forged ciphertext fails the MAC check, whatever its padding is.
    The test file shows that the attack gets no information from it.
    """

    key: bytes
    mac_key: bytes
    queries: int = 0
    log: list = field(default_factory=list)

    def tag(self, data: bytes) -> bytes:
        """A toy MAC, for the demonstration only. Use HMAC in real code."""
        return hashlib.sha256(self.mac_key + data).digest()[:16]

    def seal(self, iv: bytes, plaintext: bytes) -> bytes:
        body = cbc_encrypt(self.key, iv, plaintext)
        return body + self.tag(body)

    def __call__(self, sealed: bytes) -> bool:
        self.queries += 1
        body, tag = sealed[:-16], sealed[-16:]
        if len(sealed) < 3 * BLOCK or self.tag(body) != tag:
            return False
        try:
            cbc_decrypt(self.key, body)
        except PaddingError:
            return False
        return True


def recover_decrypted_block(oracle, block: bytes) -> bytes:
    """Recover D(block), the block cipher decryption of one ciphertext block.

    The query is a two block ciphertext forged ‖ block, where forged plays
    the role of the IV. The server computes D(block) XOR forged and checks
    the padding of the result. The cost is at most 256 queries for each of
    the 16 positions, and about 128 on average.
    """
    known = bytearray(BLOCK)  # known[i] will hold D(block)[i]
    for position in range(BLOCK - 1, -1, -1):
        target = BLOCK - position  # the padding value we aim for
        forged = bytearray(BLOCK)
        for i in range(position + 1, BLOCK):
            forged[i] = known[i] ^ target
        found = None
        for guess in range(256):
            forged[position] = guess
            if not oracle(bytes(forged) + block):
                continue
            if position == BLOCK - 1:
                # A yes for the last position can mean a longer valid padding.
                # Change the octet before it and ask again: a padding of one
                # octet stays valid, a longer one breaks.
                probe = bytearray(forged)
                probe[position - 1] ^= 0xFF
                if not oracle(bytes(probe) + block):
                    continue
            found = guess
            break
        if found is None:
            raise RuntimeError("no conforming octet; the oracle is not a padding oracle")
        known[position] = found ^ target
    return bytes(known)


def attack(oracle, ciphertext: bytes, strip_padding: bool = True) -> bytes:
    """Recover the whole plaintext of a CBC ciphertext from the padding bit.

    The input is the ciphertext as it was sent, with the IV in the first
    block. The attacker needs no key and no plaintext. The cost is about
    128 queries for each plaintext octet.
    """
    if len(ciphertext) % BLOCK != 0 or len(ciphertext) < 2 * BLOCK:
        raise ValueError("the ciphertext must hold an IV and at least one block")
    out = bytearray()
    for start in range(BLOCK, len(ciphertext), BLOCK):
        previous = ciphertext[start - BLOCK:start]
        block = ciphertext[start:start + BLOCK]
        decrypted = recover_decrypted_block(oracle, block)
        out.extend(a ^ b for a, b in zip(decrypted, previous))
    return pkcs7_unpad(bytes(out)) if strip_padding else bytes(out)
