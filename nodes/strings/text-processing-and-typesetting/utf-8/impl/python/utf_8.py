# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/utf-8/. The authors are listed in prov/59B85A.jsonl.

"""UTF-8 encoding and decoding, as in The Unicode Standard 16.0.0, section 3.9 (D92, Table 3-7).

The decoder replaces each maximal subpart of an ill-formed sequence (D93b) with one
U+FFFD, the practice of section 3.9.6. Python's bytes.decode("utf-8", "replace") follows
the same practice, so the tests use it as the oracle.
"""

REPLACEMENT = 0xFFFD


class UTF8Error(ValueError):
    """Raised by strict decoding. start and end delimit the maximal subpart (bytes)."""

    def __init__(self, start: int, end: int) -> None:
        super().__init__(f"ill-formed UTF-8 at bytes {start}..{end - 1}")
        self.start = start
        self.end = end


def lead_info(b: int) -> tuple[int, int, int]:
    """Return (k, lo, hi) for a first byte b, from Table 3-7.

    k is the number of continuation bytes, and lo..hi is the range of the second byte.
    k = 0 means that b is not a legal first byte of a multi-byte sequence.
    """
    if 0xC2 <= b <= 0xDF:
        return 1, 0x80, 0xBF
    if b == 0xE0:
        return 2, 0xA0, 0xBF  # no overlong 3-byte forms
    if b == 0xED:
        return 2, 0x80, 0x9F  # no surrogates D800..DFFF
    if 0xE1 <= b <= 0xEF:
        return 2, 0x80, 0xBF
    if b == 0xF0:
        return 3, 0x90, 0xBF  # no overlong 4-byte forms
    if 0xF1 <= b <= 0xF3:
        return 3, 0x80, 0xBF
    if b == 0xF4:
        return 3, 0x80, 0x8F  # nothing above 10FFFF
    return 0, 0, 0  # 80..BF, C0, C1, F5..FF


def encode_code_point(c: int, allow_surrogates: bool = False) -> bytes:
    """Return the UTF-8 bytes of the scalar value c.

    With allow_surrogates, a surrogate code point gets the 3-byte form that the
    rest of the formula gives (ED A0 80 for D800). That is not UTF-8; it is what
    Python calls "surrogatepass".
    """
    if not 0 <= c <= 0x10FFFF:
        raise ValueError(f"{c:#x} is not a code point")
    if 0xD800 <= c <= 0xDFFF and not allow_surrogates:
        raise ValueError(f"U+{c:04X} is a surrogate, not a scalar value")
    if c < 0x80:  # @line L1
        return bytes([c])
    if c < 0x800:  # @line L2
        return bytes([0xC0 | (c >> 6), 0x80 | (c & 0x3F)])
    if c < 0x10000:  # @line L3
        return bytes([0xE0 | (c >> 12), 0x80 | ((c >> 6) & 0x3F), 0x80 | (c & 0x3F)])
    return bytes([0xF0 | (c >> 18), 0x80 | ((c >> 12) & 0x3F),  # @line L4
                  0x80 | ((c >> 6) & 0x3F), 0x80 | (c & 0x3F)])


def encode(s: str, allow_surrogates: bool = False) -> bytes:
    """Encode a Python str (a sequence of code points) as UTF-8."""
    return b"".join(encode_code_point(ord(ch), allow_surrogates) for ch in s)


def decode_code_points(data: bytes, errors: str = "replace") -> list[int]:
    """Decode data to a list of code points.

    errors="replace" puts one U+FFFD for each maximal subpart; errors="strict"
    raises UTF8Error at the first ill-formed subsequence.
    """
    out: list[int] = []
    n = len(data)
    i = 0  # @line L5
    while i < n:  # @line L6
        b = data[i]  # @line L7
        if b < 0x80:  # @line L8
            out.append(b)
            i += 1
            continue
        k, lo, hi = lead_info(b)  # @line L9
        if k == 0:  # @line L10
            if errors == "strict":
                raise UTF8Error(i, i + 1)
            out.append(REPLACEMENT)
            i += 1
            continue
        c = b & (0x7F >> (k + 1))  # @line L11
        j = 1
        while j <= k:  # @line L12
            lo2, hi2 = (lo, hi) if j == 1 else (0x80, 0xBF)  # @line L13
            if i + j >= n or not lo2 <= data[i + j] <= hi2:  # @line L14
                break
            c = (c << 6) | (data[i + j] & 0x3F)  # @line L15
            j += 1
        if j == k + 1:  # @line L16
            out.append(c)
        else:
            if errors == "strict":
                raise UTF8Error(i, i + j)
            out.append(REPLACEMENT)
        i += j  # @line L17
    return out  # @line L18


def decode(data: bytes, errors: str = "replace") -> str:
    """Decode UTF-8 bytes to a str."""
    return "".join(map(chr, decode_code_points(data, errors)))


def is_valid(data: bytes) -> bool:
    """Return True if data is well-formed UTF-8 (Table 3-7)."""
    try:
        decode_code_points(data, "strict")
    except UTF8Error:
        return False
    return True


def code_point_start(data: bytes, i: int) -> int:
    """Return the start of the code point that holds byte i of well-formed data.

    A continuation byte has the form 10xxxxxx, so at most 3 steps back are needed.
    """
    j = i
    while j > 0 and i - j < 3 and data[j] & 0xC0 == 0x80:
        j -= 1
    return j
