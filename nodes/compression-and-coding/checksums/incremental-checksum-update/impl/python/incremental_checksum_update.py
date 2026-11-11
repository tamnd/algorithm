# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-checksum-update/. The authors are listed in prov/RGZ1Q3.jsonl.

"""Incremental update of the Internet checksum after one 16-bit field changes.

HC is the checksum stored in the header, m the old value of a 16-bit word of
the header and m2 its new value (m' in the RFCs). All arithmetic is ones'
complement on 16 bits.

- update_rfc1624 is Eqn. 3 of RFC 1624: HC' = ~(~HC + ~m + m').
- update_rfc1141 is Eqn. 2 of RFC 1624, the formula of RFC 1141:
  HC' = HC + m + ~m'. It gives 0xFFFF where a full recompute gives 0x0000.
- update_rfc1624_eqn4 is Eqn. 4 of RFC 1624: HC' = HC - ~m - m', with ones'
  complement subtraction (subtract with end-around borrow).

Cost: O(1) per changed word, independent of the length of the header.
"""

MASK16 = 0xFFFF


def _add(a: int, b: int) -> int:
    s = a + b
    return (s & MASK16) + (s >> 16)


def _sub(a: int, b: int) -> int:
    """Ones' complement subtraction a - b with an end-around borrow."""
    d = a - b
    if d < 0:
        d = (d - 1) & MASK16  # the borrow out of bit 15 is taken from bit 0
    return d


def update_rfc1624(hc: int, m: int, m2: int) -> int:
    """New header checksum by RFC 1624 Eqn. 3: HC' = ~(~HC + ~m + m')."""
    c = ~hc & MASK16  # @line L1
    c = _add(c, ~m & MASK16)  # @line L2
    c = _add(c, m2)  # @line L3
    return ~c & MASK16  # @line L4


def update_rfc1141(hc: int, m: int, m2: int) -> int:
    """New header checksum by RFC 1141 (Eqn. 2 of RFC 1624): HC' = HC + m + ~m'."""
    return _add(_add(hc, m), ~m2 & MASK16)


def update_rfc1624_eqn4(hc: int, m: int, m2: int) -> int:
    """New header checksum by RFC 1624 Eqn. 4: HC' = HC - ~m - m'."""
    return _sub(_sub(hc, ~m & MASK16), m2)


def update_word(header: bytearray, offset: int, new_word: int, rule=update_rfc1624, field: int = 10) -> None:
    """Replace the 16-bit word at an even offset and patch the checksum at offset field in place."""
    if offset % 2 or field % 2 or offset == field:
        raise ValueError("offsets must be even, and the word must not be the checksum field")
    m = (header[offset] << 8) | header[offset + 1]
    hc = (header[field] << 8) | header[field + 1]
    header[offset : offset + 2] = new_word.to_bytes(2, "big")
    header[field : field + 2] = rule(hc, m, new_word).to_bytes(2, "big")


def decrement_ttl(header: bytearray, rule=update_rfc1624) -> None:
    """Decrement the TTL of an IPv4 header (byte 8) and update its checksum incrementally."""
    if header[8] == 0:
        raise ValueError("the TTL is already zero")
    new_word = ((header[8] - 1) << 8) | header[9]
    update_word(header, 8, new_word, rule)
