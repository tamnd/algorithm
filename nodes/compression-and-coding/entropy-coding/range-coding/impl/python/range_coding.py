# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/range-coding/. The authors are listed in prov/3GVCEG.jsonl.

"""The binary range coder of LZMA, as in lzma-specification.txt of the LZMA SDK.

A probability is an 11-bit integer prob, the chance of a 0 bit times 2048.
After each bit it moves 1/32 of the way to the bit that came (shift 5).
The encoder keeps low (33 bits are enough) and range (32 bits). It writes
bytes, and it handles a carry out of low with one cached byte and a count of
0xFF bytes that wait behind it. The decoder keeps range and code, 32 bits each.

Cost: O(1) word operations per bit, plus O(1) per output byte.
"""

import math

NUM_BIT_MODEL_TOTAL_BITS = 11
BIT_MODEL_TOTAL = 1 << NUM_BIT_MODEL_TOTAL_BITS  # 2048
PROB_INIT = BIT_MODEL_TOTAL // 2  # 1024, both bits equally likely
NUM_MOVE_BITS = 5
TOP_VALUE = 1 << 24
MASK32 = 0xFFFFFFFF


class RangeEncoder:
    def __init__(self) -> None:
        self.low = 0  # @line L1
        self.range = MASK32
        self.cache = 0
        self.cache_size = 1
        self.out = bytearray()

    def _shift_low(self) -> None:
        """Move the top byte of low out, through the cache, with any carry."""
        if self.low < 0xFF000000 or self.low >= (1 << 32):  # @line L12
            carry = self.low >> 32
            temp = self.cache
            while True:  # @line L13
                self.out.append((temp + carry) & 0xFF)
                temp = 0xFF
                self.cache_size -= 1
                if self.cache_size == 0:
                    break
            self.cache = (self.low >> 24) & 0xFF  # @line L14
        self.cache_size += 1  # @line L15
        self.low = (self.low & 0x00FFFFFF) << 8  # @line L16

    def encode_bit(self, probs: list[int], i: int, bit: int) -> None:
        """Encode bit with the adaptive probability probs[i], and update it."""
        prob = probs[i]
        bound = (self.range >> NUM_BIT_MODEL_TOTAL_BITS) * prob  # @line L2
        if bit == 0:  # @line L3
            self.range = bound
            probs[i] = prob + ((BIT_MODEL_TOTAL - prob) >> NUM_MOVE_BITS)  # @line L4
        else:
            self.low += bound  # @line L5
            self.range -= bound
            probs[i] = prob - (prob >> NUM_MOVE_BITS)  # @line L6
        while self.range < TOP_VALUE:  # @line L7
            self.range = (self.range << 8) & MASK32
            self._shift_low()

    def encode_direct_bits(self, value: int, num_bits: int) -> None:
        """Encode the low num_bits bits of value, top bit first, each with probability 1/2."""
        for k in range(num_bits - 1, -1, -1):
            self.range >>= 1
            if (value >> k) & 1:
                self.low += self.range
            while self.range < TOP_VALUE:
                self.range = (self.range << 8) & MASK32
                self._shift_low()

    def finish(self) -> bytes:
        for _ in range(5):  # @line L8
            self._shift_low()
        return bytes(self.out)


class RangeDecoder:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.pos = 0
        self.range = MASK32  # @line L17
        self.code = 0
        first = self._byte()
        for _ in range(4):
            self.code = (self.code << 8) | self._byte()
        if first != 0 or self.code == self.range:
            raise ValueError("corrupted range coder stream")

    def _byte(self) -> int:
        b = self.data[self.pos] if self.pos < len(self.data) else 0
        self.pos += 1
        return b

    def decode_bit(self, probs: list[int], i: int) -> int:
        prob = probs[i]
        bound = (self.range >> NUM_BIT_MODEL_TOTAL_BITS) * prob  # @line L18
        if self.code < bound:  # @line L19
            self.range = bound
            probs[i] = prob + ((BIT_MODEL_TOTAL - prob) >> NUM_MOVE_BITS)
            bit = 0
        else:
            self.code -= bound  # @line L20
            self.range -= bound
            probs[i] = prob - (prob >> NUM_MOVE_BITS)
            bit = 1
        if self.range < TOP_VALUE:  # @line L21
            self.range = (self.range << 8) & MASK32
            self.code = ((self.code << 8) | self._byte()) & MASK32
        return bit

    def decode_direct_bits(self, num_bits: int) -> int:
        res = 0
        for _ in range(num_bits):
            self.range >>= 1
            if self.code >= self.range:
                self.code -= self.range
                bit = 1
            else:
                bit = 0
            if self.range < TOP_VALUE:
                self.range = (self.range << 8) & MASK32
                self.code = ((self.code << 8) | self._byte()) & MASK32
            res = (res << 1) | bit
        return res

    def finished_ok(self) -> bool:
        return self.code == 0


def encode_bits(bits: list[int], num_contexts: int, contexts: list[int]) -> bytes:
    """Encode bits[i] with the adaptive probability of context contexts[i]."""
    probs = [PROB_INIT] * num_contexts
    enc = RangeEncoder()
    for bit, ctx in zip(bits, contexts):
        enc.encode_bit(probs, ctx, bit)  # @line L9
    return enc.finish()


def decode_bits(data: bytes, num_contexts: int, contexts: list[int]) -> list[int]:
    probs = [PROB_INIT] * num_contexts
    dec = RangeDecoder(data)
    return [dec.decode_bit(probs, ctx) for ctx in contexts]  # @line L22


def model_cost_bytes(data: bytes) -> float:
    """The sum of -lg p over all binary decisions of encode_bytes, with p from the adaptive model."""
    probs = [PROB_INIT] * 256
    cost = 0.0
    for byte in data:
        node = 1
        for k in range(7, -1, -1):
            bit = (byte >> k) & 1
            p0 = probs[node] / BIT_MODEL_TOTAL
            cost -= math.log2(p0 if bit == 0 else 1 - p0)
            if bit == 0:
                probs[node] += (BIT_MODEL_TOTAL - probs[node]) >> NUM_MOVE_BITS
            else:
                probs[node] -= probs[node] >> NUM_MOVE_BITS
            node = (node << 1) | bit
    return cost


def encode_bytes(data: bytes) -> bytes:
    """Order-0 byte coder: each byte is 8 binary decisions down a bit tree of 255 probabilities."""
    probs = [PROB_INIT] * 256
    enc = RangeEncoder()
    for byte in data:
        node = 1
        for k in range(7, -1, -1):  # @line L10
            bit = (byte >> k) & 1
            enc.encode_bit(probs, node, bit)
            node = (node << 1) | bit  # @line L11
    return enc.finish()


def decode_bytes(code: bytes, n: int) -> bytes:
    probs = [PROB_INIT] * 256
    dec = RangeDecoder(code)
    out = bytearray()
    for _ in range(n):
        node = 1
        while node < 256:  # @line L23
            node = (node << 1) | dec.decode_bit(probs, node)
        out.append(node - 256)  # @line L24
    return bytes(out)


def decode_lzma_literals(raw: bytes, n: int, lc: int = 3, lp: int = 0, pb: int = 2) -> bytes:
    """Decode the first n symbols of a raw LZMA1 stream, all of which must be literals.

    This uses only the parts of the LZMA decoder that a stream of literals
    needs: the IsMatch probabilities in state 0 and the literal coder with the
    previous byte as context. It raises ValueError if a match appears.
    """
    dec = RangeDecoder(raw)
    is_match = [PROB_INIT] * (12 << 4)
    literal = [PROB_INIT] * (0x300 << (lc + lp))
    state, prev, out = 0, 0, bytearray()
    for pos in range(n):
        pos_state = pos & ((1 << pb) - 1)
        if dec.decode_bit(is_match, (state << 4) + pos_state):
            raise ValueError("a match, not a literal")
        lit_state = ((pos & ((1 << lp) - 1)) << lc) + (prev >> (8 - lc))
        base = 0x300 * lit_state
        node = 1
        while node < 0x100:
            node = (node << 1) | dec.decode_bit(literal, base + node)
        prev = node - 0x100
        out.append(prev)
        state = 0  # after a literal, state < 4 goes to 0
    return bytes(out)
