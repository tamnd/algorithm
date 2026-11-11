# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pkcs7-padding/. The authors are listed in prov/TD8JXS.jsonl.
"""PKCS #7 padding (RFC 5652, Section 6.3) with a strict unpad.

For study only. Python code is not constant time, and pkcs7_unpad stops at the
first bad byte, so its running time and its error tell an attacker about the
plaintext. Never let a decryptor report padding errors: use an AEAD from a FIPS
140 validated module or libsodium instead.
"""


class PaddingError(ValueError):
    """The input is not the PKCS #7 padding of any message."""


def pkcs7_pad(m: bytes, b: int) -> bytes:
    """Append k bytes of value k, where k = b - (len(m) mod b), so 1 <= k <= b."""
    if not 1 <= b <= 255:
        raise ValueError("PKCS #7 needs a block length of 1 to 255 bytes")
    k = b - len(m) % b  # @line L1
    return m + bytes([k]) * k  # @line L2


def pkcs7_unpad(x: bytes, b: int) -> bytes:
    """Strict unpad: accept x only if x = pkcs7_pad(m, b) for some m, and return that m."""
    if not 1 <= b <= 255:
        raise ValueError("PKCS #7 needs a block length of 1 to 255 bytes")
    if len(x) == 0 or len(x) % b != 0:  # @line L3
        raise PaddingError("the length is not a positive multiple of the block length")
    k = x[-1]  # @line L4
    if k == 0 or k > b:  # @line L5
        raise PaddingError("the last byte is not a valid pad length")
    for i in range(1, k + 1):  # @line L6
        if x[-i] != k:
            raise PaddingError("a pad byte has the wrong value")
    return x[:-k]  # @line L7


def pkcs7_check_masked(x: bytes, b: int) -> bool:
    """The same test as pkcs7_unpad, written without branches on the data.

    It reads all of the last b bytes and folds the result with bit masks. This is
    the shape of a constant-time check in C; in Python it is only an illustration.
    """
    if len(x) == 0 or len(x) % b != 0:
        return False  # the length is public
    k = x[-1]
    bad = ((k - 1) >> 8) & 1  # 1 if k == 0
    bad |= ((b - k) >> 8) & 1  # 1 if k > b
    for i in range(1, b + 1):
        in_pad = ((i - k - 1) >> 8) & 1  # 1 if i <= k
        bad |= in_pad & (((x[-i] ^ k) + 255) >> 8)  # 1 if x[-i] != k
    return bad == 0


def pkcs7_unpad_lenient(x: bytes) -> bytes:
    """A common bug: trust the last byte and check nothing. Shown only to be tested against."""
    return x[: -x[-1]] if x and x[-1] else x
