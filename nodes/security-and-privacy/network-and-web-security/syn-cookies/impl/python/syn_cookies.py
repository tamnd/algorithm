# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/syn-cookies/. The authors are listed in prov/Z3NQ59.jsonl.

"""SYN cookies in the layout of Bernstein (RFC 4987, Appendix A).

A cookie is a 32-bit initial sequence number y for the server:
  bits 31..27  t mod 32, where t is a time counter that steps every 64 seconds
  bits 26..24  m, an index into a table of 8 MSS values
  bits 23..0   the low 24 bits of HMAC-SHA256(K, c || t), c the 4-tuple

The code works on abstract 4-tuples of strings and integers. It opens no
socket, reads no clock and sends no packet: the caller passes the counter.
"""

import hashlib
import hmac
import ipaddress

FourTuple = tuple[str, int, str, int]  # (client address, client port, server address, server port)

MSS_TABLE: tuple[int, ...] = (536, 1220, 1300, 1400, 1440, 1460, 4312, 8960)
HASH_BITS = 24
MOD32 = 1 << 32


def _encode(c: FourTuple, t: int) -> bytes:
    """Encode the 4-tuple and the full counter as a fixed layout of bytes."""
    src, sport, dst, dport = c
    a = ipaddress.ip_address(src)
    b = ipaddress.ip_address(dst)
    return (
        bytes([a.version]) + a.packed + sport.to_bytes(2, "big")
        + bytes([b.version]) + b.packed + dport.to_bytes(2, "big")
        + t.to_bytes(8, "big")
    )


def keyed_hash(key: bytes, c: FourTuple, t: int) -> int:
    """F_K(c, t) mod 2^24: the low 24 bits of HMAC-SHA256 over c and t."""
    d = hmac.new(key, _encode(c, t), hashlib.sha256).digest()
    return int.from_bytes(d[-3:], "big")


def split_cookie(y: int) -> tuple[int, int, int]:
    """Split a 32-bit value into (t mod 32, m, h)."""
    return y >> 27, (y >> 24) & 7, y & 0xFFFFFF


def make_cookie(key: bytes, c: FourTuple, t: int, m: int) -> int:
    """Return the server ISN y for a SYN from c at counter t with MSS index m.

    Precondition: t >= 0 and 0 <= m < 8. Cost: one HMAC over 45 bytes or less,
    so O(1) time and O(1) space in the word-RAM model. The server stores nothing.
    """
    h = keyed_hash(key, c, t)  # @line L1
    return ((t % 32) << 27) | (m << 24) | h  # @line L2


def check_cookie(key: bytes, c: FourTuple, a: int, now: int, max_age: int) -> int | None:
    """Check the acknowledgment number a of the final ACK from c at counter now.

    Return the MSS value if a - 1 is a cookie that make_cookie gave for c at a
    counter t with 0 <= now - t <= max_age; else return None.
    Precondition: 0 <= max_age < 32 and now >= 0. Cost: one HMAC, O(1).
    """
    y = (a - 1) % MOD32  # @line L3
    t5, m, h = split_cookie(y)  # @line L4
    t = now - ((now - t5) % 32)  # @line L5
    if now - t > max_age or t < 0:  # @line L6
        return None
    if not hmac.compare_digest(keyed_hash(key, c, t).to_bytes(3, "big"), h.to_bytes(3, "big")):  # @line L7
        return None
    return MSS_TABLE[m]  # @line L8


def mss_index(client_mss: int) -> int:
    """The largest table index whose MSS is at most the client's MSS (0 if none)."""
    best = 0
    for i, v in enumerate(MSS_TABLE):
        if v <= client_mss:
            best = i
    return best
