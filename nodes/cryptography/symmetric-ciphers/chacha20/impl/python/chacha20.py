# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chacha20/. The authors are listed in prov/79BC7C.jsonl.

"""ChaCha20 as in RFC 8439 (32-bit counter, 96-bit nonce), for study only.

This code is not constant time and must not protect real data. Use ChaCha20-Poly1305 from libsodium, OpenSSL or a FIPS 140 validated
module instead.
"""

M32 = 0xFFFFFFFF
CONSTANTS = (0x61707865, 0x3320646E, 0x79622D32, 0x6B206574)  # "expand 32-byte k"


def rotl32(v: int, c: int) -> int:
    """Rotate the 32-bit word v left by c places, 0 < c < 32."""
    return ((v << c) & M32) | (v >> (32 - c))


def quarter_round(x: list[int], a: int, b: int, c: int, d: int) -> None:
    """Apply the ChaCha quarter round to the words x[a], x[b], x[c], x[d] in place.

    Precondition: x holds 32-bit words. Cost: 4 additions, 4 XORs, 4 rotations.
    """
    x[a] = (x[a] + x[b]) & M32; x[d] ^= x[a]; x[d] = rotl32(x[d], 16)  # @line L1
    x[c] = (x[c] + x[d]) & M32; x[b] ^= x[c]; x[b] = rotl32(x[b], 12)  # @line L2
    x[a] = (x[a] + x[b]) & M32; x[d] ^= x[a]; x[d] = rotl32(x[d], 8)  # @line L3
    x[c] = (x[c] + x[d]) & M32; x[b] ^= x[c]; x[b] = rotl32(x[b], 7)  # @line L4


def chacha20_block(key: bytes, counter: int, nonce: bytes) -> bytes:
    """Return the 64-byte ChaCha20 block for (key, counter, nonce), RFC 8439 Section 2.3.

    Precondition: 32-byte key, 12-byte nonce, 0 <= counter < 2**32.
    Cost: 20 rounds, that is 80 quarter rounds, plus 16 additions.
    """
    if len(key) != 32 or len(nonce) != 12 or not 0 <= counter <= M32:
        raise ValueError("ChaCha20 needs a 32-byte key, a 12-byte nonce and a 32-bit counter")
    state = list(CONSTANTS)  # @line L5
    state += [int.from_bytes(key[4 * i:4 * i + 4], "little") for i in range(8)]
    state.append(counter)
    state += [int.from_bytes(nonce[4 * i:4 * i + 4], "little") for i in range(3)]
    w = list(state)  # @line L6
    for _ in range(10):  # @line L7
        quarter_round(w, 0, 4, 8, 12)  # @line L8
        quarter_round(w, 1, 5, 9, 13)
        quarter_round(w, 2, 6, 10, 14)
        quarter_round(w, 3, 7, 11, 15)
        quarter_round(w, 0, 5, 10, 15)  # @line L9
        quarter_round(w, 1, 6, 11, 12)
        quarter_round(w, 2, 7, 8, 13)
        quarter_round(w, 3, 4, 9, 14)
    return b"".join(((w[i] + state[i]) & M32).to_bytes(4, "little") for i in range(16))  # @line L10


def chacha20_encrypt(key: bytes, counter: int, nonce: bytes, data: bytes) -> bytes:
    """Encrypt or decrypt data with ChaCha20, RFC 8439 Section 2.4.

    Precondition: as for chacha20_block, and counter + ceil(len(data)/64) - 1 < 2**32.
    Cost: ceil(len(data)/64) block calls.
    """
    out = bytearray()
    for j in range((len(data) + 63) // 64):  # @line L11
        ks = chacha20_block(key, counter + j, nonce)  # @line L12
        chunk = data[64 * j:64 * j + 64]
        out += bytes(p ^ k for p, k in zip(chunk, ks))  # @line L13
    return bytes(out)
