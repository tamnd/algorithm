# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/a5-1/. The authors are listed in prov/6XMTK8.jsonl.

"""The A5/1 keystream generator of GSM, as in the 1999 pedagogical implementation, for study only.

A5/1 is broken. The code is not constant time as Python runs it (it uses
data-dependent branches) and must not protect real data.
"""

# (length, feedback tap mask, clocking bit, output bit) for R1, R2 and R3.
REGISTERS = [
    (19, (1 << 18) | (1 << 17) | (1 << 16) | (1 << 13), 8, 18),
    (22, (1 << 21) | (1 << 20), 10, 21),
    (23, (1 << 22) | (1 << 21) | (1 << 20) | (1 << 7), 10, 22),
]


def _step(r: int, j: int) -> int:
    """Shift register j left by one and put the parity of its taps in bit 0."""
    length, taps, _, _ = REGISTERS[j]
    t = bin(r & taps).count("1") & 1  # @line L8
    return ((r << 1) & ((1 << length) - 1)) | t  # @line L8


def _majority_clock(regs: list[int]) -> None:
    """Clock each register whose clocking bit agrees with the majority of the three."""
    bits = [(regs[j] >> REGISTERS[j][2]) & 1 for j in range(3)]
    m = 1 if sum(bits) >= 2 else 0  # @line L6
    for j in range(3):
        if bits[j] == m:  # @line L7
            regs[j] = _step(regs[j], j)  # @line L7


def _output_bit(regs: list[int]) -> int:
    return ((regs[0] >> 18) ^ (regs[1] >> 21) ^ (regs[2] >> 22)) & 1


def a5_1_setup(key: bytes, frame: int) -> list[int]:
    """Return the three registers after key loading, frame loading and the 100 mixing clocks.

    Precondition: an 8-byte key and a 22-bit frame number. Key bit i is bit i mod 8
    of byte i // 8 (least significant bit first), as in the pedagogical code.
    """
    if len(key) != 8 or not 0 <= frame < (1 << 22):
        raise ValueError("A5/1 needs a 64-bit key and a 22-bit frame number")
    regs = [0, 0, 0]  # @line L1
    for i in range(64):  # @line L2
        bit = (key[i // 8] >> (i % 8)) & 1
        regs = [_step(regs[j], j) ^ bit for j in range(3)]  # @line L2
    for i in range(22):  # @line L3
        bit = (frame >> i) & 1
        regs = [_step(regs[j], j) ^ bit for j in range(3)]  # @line L3
    for _ in range(100):  # @line L4
        _majority_clock(regs)  # @line L4
    return regs


def a5_1_keystream_bits(key: bytes, frame: int, n: int = 228) -> list[int]:
    """Return n keystream bits. The first 114 encrypt A to B and the next 114 B to A.

    Cost: Theta(186 + n) clocks of three short registers.
    """
    regs = a5_1_setup(key, frame)
    out = []
    for _ in range(n):  # @line L5
        _majority_clock(regs)  # @line L5
        out.append(_output_bit(regs))  # @line L5
    return out


def pack_bits(bits: list[int]) -> bytes:
    """Pack bits most significant first, padding the last byte with zeros."""
    out = bytearray((len(bits) + 7) // 8)
    for i, b in enumerate(bits):
        out[i // 8] |= b << (7 - i % 8)
    return bytes(out)


def a5_1_frame_keystreams(key: bytes, frame: int) -> tuple[bytes, bytes]:
    """Return the two 114-bit keystreams (A to B, B to A) of one GSM frame, packed in 15 bytes each."""
    bits = a5_1_keystream_bits(key, frame, 228)
    return pack_bits(bits[:114]), pack_bits(bits[114:])
