# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/utf-16/. The authors are listed in prov/7HJ2KD.jsonl.

"""UTF-16 encoding and decoding, as in The Unicode Standard 16.0.0, section 3.9 (D91), and RFC 2781.

The core works on 16-bit code units. The byte layer (UTF-16BE and UTF-16LE) puts each code
unit in two bytes. An unpaired surrogate code unit is ill-formed; the decoder replaces each
one with U+FFFD, as Python's bytes.decode("utf-16-be", "replace") does.
"""

REPLACEMENT = 0xFFFD


class UTF16Error(ValueError):
    """Raised by strict decoding. start and end are offsets in the input (code units or bytes)."""

    def __init__(self, start: int, end: int) -> None:
        super().__init__(f"ill-formed UTF-16 at {start}..{end - 1}")
        self.start = start
        self.end = end


def is_high(u: int) -> bool:
    return 0xD800 <= u <= 0xDBFF


def is_low(u: int) -> bool:
    return 0xDC00 <= u <= 0xDFFF


def encode_code_point(c: int) -> list[int]:
    """Return the UTF-16 code units of the scalar value c."""
    if not 0 <= c <= 0x10FFFF or 0xD800 <= c <= 0xDFFF:
        raise ValueError(f"{c:#x} is not a scalar value")
    if c < 0x10000:  # @line L1
        return [c]
    v = c - 0x10000  # @line L2
    return [0xD800 + (v >> 10), 0xDC00 + (v & 0x3FF)]  # @line L3


def encode_units(s: str) -> list[int]:
    """Encode a str of scalar values as a list of code units."""
    out: list[int] = []
    for ch in s:
        out.extend(encode_code_point(ord(ch)))
    return out


def decode_units(units: list[int], errors: str = "replace") -> list[int]:
    """Decode code units to code points; each unpaired surrogate gives one U+FFFD."""
    out: list[int] = []
    n = len(units)
    i = 0  # @line L4
    while i < n:  # @line L5
        u = units[i]  # @line L6
        if not 0xD800 <= u <= 0xDFFF:  # @line L7
            out.append(u)
            i += 1
        elif is_high(u) and i + 1 < n and is_low(units[i + 1]):  # @line L8
            out.append(0x10000 + ((u - 0xD800) << 10) + (units[i + 1] - 0xDC00))  # @line L9
            i += 2
        else:  # @line L10
            if errors == "strict":
                raise UTF16Error(i, i + 1)
            out.append(REPLACEMENT)
            i += 1
    return out  # @line L11


def encode(s: str, byteorder: str = "big") -> bytes:
    """Encode s as UTF-16BE (byteorder "big") or UTF-16LE ("little"), with no byte order mark."""
    return b"".join(u.to_bytes(2, byteorder) for u in encode_units(s))


def decode(data: bytes, errors: str = "replace", byteorder: str = "big") -> str:
    """Decode UTF-16BE or UTF-16LE bytes.

    A final odd byte is a truncated code unit and gives one U+FFFD. Like Python, a high
    surrogate followed only by such a byte gives one U+FFFD for the 3 bytes.
    """
    n = len(data)
    units = [int.from_bytes(data[k:k + 2], byteorder) for k in range(0, n - 1, 2)]
    # A final high surrogate is never part of a pair. If an odd byte follows it, the
    # 3 bytes are one truncated sequence.
    merge_tail = n % 2 == 1 and len(units) > 0 and is_high(units[-1])
    body = units[:-1] if merge_tail else units
    try:
        out = decode_units(body, errors)
    except UTF16Error as e:
        raise UTF16Error(2 * e.start, 2 * e.end) from None
    if n % 2 == 1:
        start = n - 3 if merge_tail else n - 1
        if errors == "strict":
            raise UTF16Error(start, n)
        out.append(REPLACEMENT)
    return "".join(map(chr, out))


def length_in_code_units(s: str) -> int:
    """The length that Java and JavaScript report: 2 for each supplementary code point."""
    return sum(2 if ord(ch) >= 0x10000 else 1 for ch in s)
