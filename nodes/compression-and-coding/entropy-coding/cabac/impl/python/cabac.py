# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cabac/. The authors are listed in prov/SYQ77C.jsonl.

"""The CABAC arithmetic coding engine of H.264/AVC (ITU-T H.264, Section 9.3).

A context holds a probability state 0..62 and the value of the most probable
symbol (MPS). The coder keeps a 9-bit range in [256, 510] and splits it with
the table RANGE_TAB_LPS (Table 9-44), indexed by the state and by two bits of
the range. The state moves by TRANS_IDX_LPS (Table 9-45) after a least
probable symbol (LPS) and by one step up after an MPS. Bypass bins are coded
with probability 1/2 and no context. A terminate bin closes the stream; the
last bit written is the rbsp_stop_one_bit of H.264.

Cost: O(1) per bin. The renormalization makes at most 7 shifts.
"""

# rangeTabLPS[state][q], q = (range >> 6) & 3 (ITU-T H.264 Table 9-44).
RANGE_TAB_LPS = (
    (128, 176, 208, 240), (128, 167, 197, 227), (128, 158, 187, 216), (123, 150, 178, 205),
    (116, 142, 169, 195), (111, 135, 160, 185), (105, 128, 152, 175), (100, 122, 144, 166),
    (95, 116, 137, 158), (90, 110, 130, 150), (85, 104, 123, 142), (81, 99, 117, 135),
    (77, 94, 111, 128), (73, 89, 105, 122), (69, 85, 100, 116), (66, 80, 95, 110),
    (62, 76, 90, 104), (59, 72, 86, 99), (56, 69, 81, 94), (53, 65, 77, 89),
    (51, 62, 73, 85), (48, 59, 69, 80), (46, 56, 66, 76), (43, 53, 63, 72),
    (41, 50, 59, 69), (39, 48, 56, 65), (37, 45, 54, 62), (35, 43, 51, 59),
    (33, 41, 48, 56), (32, 39, 46, 53), (30, 37, 43, 50), (29, 35, 41, 48),
    (27, 33, 39, 45), (26, 31, 37, 43), (24, 30, 35, 41), (23, 28, 33, 39),
    (22, 27, 32, 37), (21, 26, 30, 35), (20, 24, 29, 33), (19, 23, 27, 31),
    (18, 22, 26, 30), (17, 21, 25, 28), (16, 20, 23, 27), (15, 19, 22, 25),
    (14, 18, 21, 24), (14, 17, 20, 23), (13, 16, 19, 22), (12, 15, 18, 21),
    (12, 14, 17, 20), (11, 14, 16, 19), (11, 13, 15, 18), (10, 12, 15, 17),
    (10, 12, 14, 16), (9, 11, 13, 15), (9, 11, 12, 14), (8, 10, 12, 14),
    (8, 9, 11, 13), (7, 9, 11, 12), (7, 9, 10, 12), (7, 8, 10, 11),
    (6, 8, 9, 11), (6, 7, 9, 10), (6, 7, 8, 9), (2, 2, 2, 2),
)

# transIdxLPS[state] (ITU-T H.264 Table 9-45). transIdxMPS[state] = min(state + 1, 62).
TRANS_IDX_LPS = (
    0, 0, 1, 2, 2, 4, 4, 5, 6, 7, 8, 9, 9, 11, 11, 12,
    13, 13, 15, 15, 16, 16, 18, 18, 19, 19, 21, 21, 22, 22, 23, 24,
    24, 25, 26, 26, 27, 27, 28, 29, 29, 30, 30, 30, 31, 32, 32, 33,
    33, 33, 34, 34, 35, 35, 35, 36, 36, 36, 37, 37, 37, 38, 38, 63,
)


class Context:
    """A context variable: a probability state and the value of the MPS."""

    __slots__ = ("state", "mps")

    def __init__(self, state: int = 0, mps: int = 0) -> None:
        if not 0 <= state <= 62 or mps not in (0, 1):
            raise ValueError("bad context")
        self.state = state
        self.mps = mps


def init_context(m: int, n: int, qp: int) -> Context:
    """Section 9.3.1.1: the state of a context from its (m, n) pair and the slice QP."""
    pre = max(1, min(126, ((m * max(0, min(51, qp))) >> 4) + n))
    if pre <= 63:
        return Context(63 - pre, 0)
    return Context(pre - 64, 1)


def _update(ctx: Context, lps: bool) -> None:
    if lps:
        if ctx.state == 0:  # @line L6
            ctx.mps = 1 - ctx.mps
        ctx.state = TRANS_IDX_LPS[ctx.state]  # @line L7
    else:
        ctx.state = min(ctx.state + 1, 62)  # @line L8


class Encoder:
    def __init__(self) -> None:
        self.low, self.range, self.first, self.outstanding = 0, 510, True, 0  # @line L1
        self.bits: list[int] = []
        self.closed = False

    def _put_bit(self, b: int) -> None:
        if self.first:  # @line L15
            self.first = False
        else:
            self.bits.append(b)
        self.bits.extend([1 - b] * self.outstanding)  # @line L16
        self.outstanding = 0

    def _renorm(self) -> None:
        while self.range < 256:  # @line L10
            if self.low < 256:  # @line L11
                self._put_bit(0)
            elif self.low >= 512:  # @line L12
                self.low -= 512
                self._put_bit(1)
            else:  # @line L13
                self.low -= 256
                self.outstanding += 1
            self.range <<= 1  # @line L14
            self.low <<= 1

    def encode_decision(self, ctx: Context, b: int) -> None:
        r_lps = RANGE_TAB_LPS[ctx.state][(self.range >> 6) & 3]  # @line L2
        self.range -= r_lps  # @line L3
        if b != ctx.mps:  # @line L4
            self.low += self.range  # @line L5
            self.range = r_lps
            _update(ctx, True)
        else:
            _update(ctx, False)
        self._renorm()  # @line L9

    def encode_bypass(self, b: int) -> None:
        self.low = 2 * self.low + (self.range if b else 0)  # @line L17
        if self.low >= 1024:  # @line L18
            self.low -= 1024
            self._put_bit(1)
        elif self.low < 512:  # @line L19
            self._put_bit(0)
        else:  # @line L20
            self.low -= 512
            self.outstanding += 1

    def encode_terminate(self, b: int) -> None:
        self.range -= 2  # @line L21
        if b:  # @line L22
            self.low += self.range
            self.range = 2
            self._renorm()
            self._put_bit((self.low >> 9) & 1)
            v = ((self.low >> 7) & 3) | 1
            self.bits.extend([v >> 1, v & 1])
            self.closed = True
        else:
            self._renorm()  # @line L23

    def finish(self) -> bytes:
        """The bytes of the stream, padded with 0 bits. Call after encode_terminate(1)."""
        if not self.closed:
            raise ValueError("the stream is not terminated")
        bits = self.bits + [0] * (-len(self.bits) % 8)
        return bytes(int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8))


class Decoder:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.pos = 0
        self.range = 510  # @line L24
        self.offset = 0
        for _ in range(9):
            self.offset = (self.offset << 1) | self._bit()

    def _bit(self) -> int:
        i = self.pos
        self.pos += 1
        if i >= 8 * len(self.data):
            raise ValueError("read past the end of the stream")
        return (self.data[i >> 3] >> (7 - (i & 7))) & 1

    def decode_decision(self, ctx: Context) -> int:
        r_lps = RANGE_TAB_LPS[ctx.state][(self.range >> 6) & 3]  # @line L25
        self.range -= r_lps
        if self.offset >= self.range:  # @line L26
            b = 1 - ctx.mps
            self.offset -= self.range
            self.range = r_lps
            _update(ctx, True)
        else:  # @line L27
            b = ctx.mps
            _update(ctx, False)
        while self.range < 256:  # @line L28
            self.range <<= 1
            self.offset = (self.offset << 1) | self._bit()
        return b  # @line L29

    def decode_bypass(self) -> int:
        self.offset = (self.offset << 1) | self._bit()  # @line L30
        if self.offset >= self.range:  # @line L31
            self.offset -= self.range
            return 1
        return 0

    def decode_terminate(self) -> int:
        self.range -= 2  # @line L32
        if self.offset >= self.range:  # @line L33
            return 1
        while self.range < 256:
            self.range <<= 1
            self.offset = (self.offset << 1) | self._bit()
        return 0


def encode_ueg(enc: Encoder, ctxs: list[Context], value: int, k: int, ucoff: int) -> None:
    """UEGk binarization (Section 9.3.2.3), unsigned: a truncated unary prefix with
    cMax = ucoff in regular bins (bin i uses ctxs[min(i, len - 1)]), then an
    Exp-Golomb suffix of order k in bypass bins."""
    prefix = min(value, ucoff)
    for i in range(prefix):
        enc.encode_decision(ctxs[min(i, len(ctxs) - 1)], 1)
    if prefix < ucoff:
        enc.encode_decision(ctxs[min(prefix, len(ctxs) - 1)], 0)
        return
    suf = value - ucoff
    while suf >= (1 << k):
        enc.encode_bypass(1)
        suf -= 1 << k
        k += 1
    enc.encode_bypass(0)
    for j in range(k - 1, -1, -1):
        enc.encode_bypass((suf >> j) & 1)


def decode_ueg(dec: Decoder, ctxs: list[Context], k: int, ucoff: int) -> int:
    value = 0
    while value < ucoff and dec.decode_decision(ctxs[min(value, len(ctxs) - 1)]):
        value += 1
    if value < ucoff:
        return value
    while dec.decode_bypass():
        value += 1 << k
        k += 1
    suf = 0
    for _ in range(k):
        suf = (suf << 1) | dec.decode_bypass()
    return value + suf


def coded_probability(ctx_state: int, rng: int, is_lps: bool) -> float:
    """The probability that the coder gives a bin: rLPS/range or 1 - rLPS/range."""
    r_lps = RANGE_TAB_LPS[ctx_state][(rng >> 6) & 3]
    return r_lps / rng if is_lps else 1 - r_lps / rng
