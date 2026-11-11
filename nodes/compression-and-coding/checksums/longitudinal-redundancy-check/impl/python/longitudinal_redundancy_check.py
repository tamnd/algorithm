# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/longitudinal-redundancy-check/. The authors are listed in prov/QJA1A5.jsonl.

"""Longitudinal redundancy check in its two common forms: the XOR of the
bytes (longitudinal parity, as in ISO 1155) and the two's complement of the
byte sum (Modbus ASCII mode)."""


def lrc_xor(msg: bytes) -> int:
    x = 0  # @line L1
    for b in msg:  # @line L2
        x ^= b  # @line L3
    return x  # @line L4


def lrc_modbus(msg: bytes) -> int:
    s = 0  # @line L5
    for b in msg:  # @line L6
        s = (s + b) & 0xFF  # @line L7
    return (256 - s) & 0xFF  # @line L8


def check_xor(msg: bytes, lrc: int) -> bool:
    return lrc_xor(msg) ^ lrc == 0  # @line L9


def check_modbus(msg: bytes, lrc: int) -> bool:
    return (sum(msg) + lrc) & 0xFF == 0  # @line L10


def modbus_ascii_frame(msg: bytes) -> bytes:
    """A Modbus ASCII frame: ':', the bytes and the LRC as upper-case hex
    pairs, then CR LF. The LRC covers the bytes, not the hex characters."""
    return b":" + (msg + bytes([lrc_modbus(msg)])).hex().upper().encode() + b"\r\n"


def parse_modbus_ascii(frame: bytes) -> bytes:
    """Return the message bytes of a frame, or raise ValueError when the
    frame is malformed or the LRC is wrong."""
    if not (frame.startswith(b":") and frame.endswith(b"\r\n")):
        raise ValueError("bad framing")
    body = bytes.fromhex(frame[1:-2].decode("ascii"))
    if len(body) < 2:
        raise ValueError("too short")
    msg, lrc = body[:-1], body[-1]
    if not check_modbus(msg, lrc):
        raise ValueError("LRC mismatch")
    return msg
