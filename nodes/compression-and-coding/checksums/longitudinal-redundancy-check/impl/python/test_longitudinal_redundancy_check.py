# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/longitudinal-redundancy-check/. The authors are listed in prov/QJA1A5.jsonl.

import random

import pytest

from longitudinal_redundancy_check import (
    check_modbus, check_xor, lrc_modbus, lrc_xor, modbus_ascii_frame, parse_modbus_ascii,
)

# Read 3 holding registers from address 0x006B of slave 0x11. The Modbus
# specification gives no complete frame with its LRC, so this value is
# computed by hand: 0x11 + 0x03 + 0x00 + 0x6B + 0x00 + 0x03 = 0x82, and
# 0x100 - 0x82 = 0x7E.
MSG = bytes([0x11, 0x03, 0x00, 0x6B, 0x00, 0x03])


def reference_modbus_lrc(msg: bytes) -> int:
    """Transcription of the LRC function of the Modbus serial line guide,
    Section 6.2.1: add the bytes into an unsigned char, then negate."""
    uch = 0
    for b in msg:
        uch = (uch + b) % 256
    return (-uch) % 256


def test_modbus_example() -> None:
    assert lrc_modbus(MSG) == 0x7E and lrc_xor(MSG) == 0x7A
    frame = modbus_ascii_frame(MSG)
    assert frame == b":1103006B00037E\r\n"
    assert parse_modbus_ascii(frame) == MSG
    with pytest.raises(ValueError):
        parse_modbus_ascii(b":1103006B00037F\r\n")


def test_against_reference_and_checks() -> None:
    rng = random.Random(1155)
    assert lrc_modbus(b"") == 0 and lrc_xor(b"") == 0
    for _ in range(2000):
        msg = rng.randbytes(rng.randrange(1, 40))
        assert lrc_modbus(msg) == reference_modbus_lrc(msg)
        assert check_modbus(msg, lrc_modbus(msg)) and check_xor(msg, lrc_xor(msg))


def bits_of(frame: bytes) -> int:
    return int.from_bytes(frame, "big")


def accepted(kind: str, frame_int: int, n: int) -> bool:
    frame = frame_int.to_bytes(n, "big")
    if kind == "xor":
        return check_xor(frame[:-1], frame[-1])
    return check_modbus(frame[:-1], frame[-1])


def test_double_errors_exhaustive() -> None:
    # Frames include the LRC byte; bit position 0 is the top bit of byte 0.
    for kind, make in (("xor", lrc_xor), ("modbus", lrc_modbus)):
        frame = MSG + bytes([make(MSG)])
        n = len(frame)
        x = bits_of(frame)
        total = 8 * n
        for p in range(total):
            for q in range(p + 1, total):
                y = x ^ (1 << (total - 1 - p)) ^ (1 << (total - 1 - q))
                same_col = p % 8 == q % 8
                up_p = not (x >> (total - 1 - p)) & 1
                up_q = not (x >> (total - 1 - q)) & 1
                if kind == "xor":
                    want = same_col
                else:  # opposite directions cancel; in bit 7, 128 + 128 = 256
                    want = same_col and (up_p != up_q or p % 8 == 0)
                assert accepted(kind, y, n) == want


def test_bursts_up_to_8_detected_in_both_bit_orders() -> None:
    rng = random.Random(8)
    for kind, make in (("xor", lrc_xor), ("modbus", lrc_modbus)):
        for _ in range(5):
            msg = rng.randbytes(6)
            frame = msg + bytes([make(msg)])
            n = len(frame)
            x = bits_of(frame)
            total = 8 * n
            for lsb_first in (False, True):
                # Serial position s maps to a bit of the frame int.
                def bit(s: int) -> int:
                    byte, k = divmod(s, 8)
                    within = k if lsb_first else 7 - k
                    return 1 << (8 * (n - 1 - byte) + within)

                for b in range(1, 9):
                    for start in range(total - b + 1):
                        for inner in range(1 << max(b - 2, 0)):
                            e = bit(start) | bit(start + b - 1)
                            for t in range(b - 2):
                                if (inner >> t) & 1:
                                    e |= bit(start + 1 + t)
                            assert not accepted(kind, x ^ e, n)


def test_burst_of_9_can_be_missed() -> None:
    frame = MSG + bytes([lrc_xor(MSG)])
    # Flip bit 3 of byte 1 and bit 3 of byte 2: a burst of 9 bits, one column.
    bad = bytearray(frame)
    bad[1] ^= 0x08
    bad[2] ^= 0x08
    assert check_xor(bytes(bad[:-1]), bad[-1])
