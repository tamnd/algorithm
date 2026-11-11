# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lzma/. The authors are listed in prov/KBKFC6.jsonl.
"""LZMA: the range coder, the literal coder, the 12-state machine and the
four repeated distances of Igor Pavlov's LZMA, and the .lzma ("alone") file
header. This module does not read .xz files or LZMA2 chunks.

The names follow the LZMA specification of the LZMA SDK
(DOC/lzma-specification.txt).
"""

N_BITS = 11                  # probabilities are 11-bit numbers
P_INIT = 1 << (N_BITS - 1)   # 1024: the probability one half
MOVE = 5                     # adaptation shift
TOP = 1 << 24
N_STATES = 12
POS_BITS_MAX = 4
END_POS_MODEL = 14
FULL_DISTANCES = 1 << (END_POS_MODEL >> 1)   # 128
ALIGN_BITS = 4
MATCH_MIN = 2
MATCH_MAX = 273
UNKNOWN_SIZE = (1 << 64) - 1


class LZMAError(ValueError):
    """The input is not a valid LZMA stream."""


def _next_literal(state):
    return 0 if state < 4 else state - 3 if state < 10 else state - 6


# ---------------------------------------------------------------- model

class _LenModel:
    def __init__(self):
        self.choice = [P_INIT, P_INIT]                # Choice, Choice2
        self.low = [P_INIT] * (16 << 3)               # 16 trees of 3 bits
        self.mid = [P_INIT] * (16 << 3)
        self.high = [P_INIT] * (1 << 8)


class _Model:
    """All adaptive probabilities, set to one half."""

    def __init__(self, lc, lp, pb):
        self.lc, self.lp, self.pb = lc, lp, pb
        self.literal = [P_INIT] * (0x300 << (lc + lp))
        self.is_match = [P_INIT] * (N_STATES << POS_BITS_MAX)
        self.is_rep = [P_INIT] * N_STATES
        self.is_rep_g0 = [P_INIT] * N_STATES
        self.is_rep_g1 = [P_INIT] * N_STATES
        self.is_rep_g2 = [P_INIT] * N_STATES
        self.is_rep0_long = [P_INIT] * (N_STATES << POS_BITS_MAX)
        self.pos_slot = [P_INIT] * (4 << 6)           # 4 trees of 6 bits
        self.pos = [P_INIT] * (1 + FULL_DISTANCES - END_POS_MODEL)
        self.align = [P_INIT] * (1 << ALIGN_BITS)
        self.length = _LenModel()
        self.rep_length = _LenModel()

    def literal_base(self, pos, prev):
        lit_state = ((pos & ((1 << self.lp) - 1)) << self.lc) + (prev >> (8 - self.lc))
        return 0x300 * lit_state


# ---------------------------------------------------------------- range decoder

class _RangeDecoder:
    def __init__(self, data, pos):
        if pos + 5 > len(data):
            raise LZMAError("truncated range coder start")
        if data[pos] != 0:
            raise LZMAError("the first byte of the range coder is not 0")
        self.data = data
        self.pos = pos + 5
        self.range = 0xFFFFFFFF
        self.code = int.from_bytes(data[pos + 1:pos + 5], "big")
        if self.code == self.range:
            raise LZMAError("corrupt range coder start")

    def _byte(self):
        if self.pos >= len(self.data):
            raise LZMAError("truncated input")
        b = self.data[self.pos]
        self.pos += 1
        return b

    def bit(self, probs, i):
        p = probs[i]
        bound = (self.range >> N_BITS) * p
        if self.code < bound:
            self.range = bound
            probs[i] = p + (((1 << N_BITS) - p) >> MOVE)
            b = 0
        else:
            self.code -= bound
            self.range -= bound
            probs[i] = p - (p >> MOVE)
            b = 1
        if self.range < TOP:
            self.range = (self.range << 8) & 0xFFFFFFFF
            self.code = ((self.code << 8) | self._byte()) & 0xFFFFFFFF
        return b

    def direct(self, nbits):
        res = 0
        for _ in range(nbits):
            self.range >>= 1
            if self.code >= self.range:
                self.code -= self.range
                res = (res << 1) | 1
            else:
                res <<= 1
            if self.range < TOP:
                self.range = (self.range << 8) & 0xFFFFFFFF
                self.code = ((self.code << 8) | self._byte()) & 0xFFFFFFFF
        return res

    def tree(self, probs, base, nbits):
        m = 1
        for _ in range(nbits):
            m = (m << 1) | self.bit(probs, base + m)
        return m - (1 << nbits)

    def reverse_tree(self, probs, base, nbits):
        m, sym = 1, 0
        for i in range(nbits):
            b = self.bit(probs, base + m)
            m = (m << 1) | b
            sym |= b << i
        return sym

    def length(self, lm, pos_state):
        if self.bit(lm.choice, 0) == 0:
            return self.tree(lm.low, pos_state << 3, 3)
        if self.bit(lm.choice, 1) == 0:
            return 8 + self.tree(lm.mid, pos_state << 3, 3)
        return 16 + self.tree(lm.high, 0, 8)

    def distance(self, model, ln):
        slot = self.tree(model.pos_slot, min(ln, 3) << 6, 6)
        if slot < 4:
            return slot
        nd = (slot >> 1) - 1
        dist = (2 | (slot & 1)) << nd
        if slot < END_POS_MODEL:
            return dist + self.reverse_tree(model.pos, dist - slot, nd)
        dist += self.direct(nd - ALIGN_BITS) << ALIGN_BITS
        return dist + self.reverse_tree(model.align, 0, ALIGN_BITS)


# ---------------------------------------------------------------- decoder

def parse_properties(b):
    if b >= 9 * 5 * 5:
        raise LZMAError("bad properties byte")
    return b % 9, (b // 9) % 5, b // 45          # lc, lp, pb


def decompress(data):
    """Decode a .lzma file: the 13-byte header, then the LZMA stream."""
    if len(data) < 13:                                           # @line L1
        raise LZMAError("truncated header")
    lc, lp, pb = parse_properties(data[0])
    dict_size = max(int.from_bytes(data[1:5], "little"), 1 << 12)
    n = int.from_bytes(data[5:13], "little")
    known = n != UNKNOWN_SIZE
    rc = _RangeDecoder(data, 13)
    m = _Model(lc, lp, pb)
    state, rep0, rep1, rep2, rep3 = 0, 0, 0, 0, 0                 # @line L2
    out = bytearray()
    while True:                                                  # @line L3
        if known and len(out) == n and rc.code == 0:             # @line L4
            return bytes(out)
        pos_state = len(out) & ((1 << pb) - 1)
        s2 = (state << POS_BITS_MAX) + pos_state
        if rc.bit(m.is_match, s2) == 0:                          # @line L5
            if known and len(out) >= n:
                raise LZMAError("data after the end")
            prev = out[-1] if out else 0                         # @line L6
            base = m.literal_base(len(out), prev)
            sym = 1
            if state >= 7:
                match_byte = out[-rep0 - 1]
                while sym < 0x100:
                    mb = (match_byte >> 7) & 1
                    match_byte <<= 1
                    b = rc.bit(m.literal, base + ((1 + mb) << 8) + sym)
                    sym = (sym << 1) | b
                    if mb != b:
                        break
            while sym < 0x100:
                sym = (sym << 1) | rc.bit(m.literal, base + sym)
            out.append(sym - 0x100)
            state = _next_literal(state)
            continue
        if rc.bit(m.is_rep, state) == 0:                         # @line L7
            rep3, rep2, rep1 = rep2, rep1, rep0                  # @line L8
            ln = rc.length(m.length, pos_state)
            state = 7 if state < 7 else 10
            rep0 = rc.distance(m, ln)                            # @line L9
            if rep0 == 0xFFFFFFFF:
                if rc.code != 0 or (known and len(out) != n):
                    raise LZMAError("bad end marker")
                return bytes(out)
            if rep0 >= dict_size:
                raise LZMAError("distance beyond the dictionary")
        else:
            if not out:
                raise LZMAError("repeated match at the start")
            if rc.bit(m.is_rep_g0, state) == 0:                  # @line L10
                if rc.bit(m.is_rep0_long, s2) == 0:              # @line L11
                    if (known and len(out) >= n) or rep0 >= len(out):
                        raise LZMAError("bad short repeated match")
                    state = 9 if state < 7 else 11
                    out.append(out[-rep0 - 1])
                    continue
            else:                                                # @line L12
                if rc.bit(m.is_rep_g1, state) == 0:
                    rep0, rep1 = rep1, rep0
                elif rc.bit(m.is_rep_g2, state) == 0:
                    rep0, rep1, rep2 = rep2, rep0, rep1
                else:
                    rep0, rep1, rep2, rep3 = rep3, rep0, rep1, rep2
            ln = rc.length(m.rep_length, pos_state)              # @line L13
            state = 8 if state < 7 else 11
        if rep0 >= len(out):                                     # @line L14
            raise LZMAError("distance before the start")
        ln += MATCH_MIN                                          # @line L15
        if known and len(out) + ln > n:
            raise LZMAError("match runs past the end")
        s = len(out) - rep0 - 1
        if rep0 + 1 >= ln:
            out += out[s:s + ln]
        else:
            for _ in range(ln):
                out.append(out[-rep0 - 1])


# ---------------------------------------------------------------- range encoder

class _RangeEncoder:
    def __init__(self):
        self.low = 0
        self.range = 0xFFFFFFFF
        self.cache = 0
        self.cache_size = 1
        self.out = bytearray()

    def _shift_low(self):
        if self.low < 0xFF000000 or self.low >= 1 << 32:
            carry = self.low >> 32
            temp = self.cache
            while True:
                self.out.append((temp + carry) & 0xFF)
                temp = 0xFF
                self.cache_size -= 1
                if self.cache_size == 0:
                    break
            self.cache = (self.low >> 24) & 0xFF
        self.cache_size += 1
        self.low = (self.low & 0x00FFFFFF) << 8

    def bit(self, probs, i, b):
        p = probs[i]
        bound = (self.range >> N_BITS) * p
        if b == 0:
            self.range = bound
            probs[i] = p + (((1 << N_BITS) - p) >> MOVE)
        else:
            self.low += bound
            self.range -= bound
            probs[i] = p - (p >> MOVE)
        while self.range < TOP:
            self.range = (self.range << 8) & 0xFFFFFFFF
            self._shift_low()

    def direct(self, value, nbits):
        for i in range(nbits - 1, -1, -1):
            self.range >>= 1
            if (value >> i) & 1:
                self.low += self.range
            while self.range < TOP:
                self.range = (self.range << 8) & 0xFFFFFFFF
                self._shift_low()

    def tree(self, probs, base, nbits, value):
        m = 1
        for i in range(nbits - 1, -1, -1):
            b = (value >> i) & 1
            self.bit(probs, base + m, b)
            m = (m << 1) | b

    def reverse_tree(self, probs, base, nbits, value):
        m = 1
        for i in range(nbits):
            b = (value >> i) & 1
            self.bit(probs, base + m, b)
            m = (m << 1) | b

    def length(self, lm, pos_state, ln):
        if ln < 8:
            self.bit(lm.choice, 0, 0)
            self.tree(lm.low, pos_state << 3, 3, ln)
        elif ln < 16:
            self.bit(lm.choice, 0, 1)
            self.bit(lm.choice, 1, 0)
            self.tree(lm.mid, pos_state << 3, 3, ln - 8)
        else:
            self.bit(lm.choice, 0, 1)
            self.bit(lm.choice, 1, 1)
            self.tree(lm.high, 0, 8, ln - 16)

    def distance(self, model, ln, dist):
        if dist < 4:
            slot = dist
        else:
            nb = dist.bit_length()
            slot = 2 * (nb - 1) + ((dist >> (nb - 2)) & 1)
        self.tree(model.pos_slot, min(ln, 3) << 6, 6, slot)
        if slot < 4:
            return
        nd = (slot >> 1) - 1
        base = (2 | (slot & 1)) << nd
        rem = dist - base
        if slot < END_POS_MODEL:
            self.reverse_tree(model.pos, base - slot, nd, rem)
        else:
            self.direct(rem >> ALIGN_BITS, nd - ALIGN_BITS)
            self.reverse_tree(model.align, 0, ALIGN_BITS, rem & 15)

    def finish(self):
        for _ in range(5):
            self._shift_low()
        return bytes(self.out)


# ---------------------------------------------------------------- encoder

def _match_length(buf, a, b, limit):
    k = 8
    while k < limit and buf[a:a + k] == buf[b:b + k]:
        k *= 2
    lo = k // 2 if k > 8 else 0
    if k >= limit:
        if buf[a:a + limit] == buf[b:b + limit]:
            return limit
        k = limit
    hi = k - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if buf[a:a + mid] == buf[b:b + mid]:
            lo = mid
        else:
            hi = mid - 1
    return lo


def compress(data, lc=3, lp=0, pb=2, dict_size=1 << 20, end_marker=False,
             chain=24):
    """Encode data as a .lzma file with a greedy parse.

    The parse tries the four repeated distances and a hash chain of 3-byte
    strings at each position, and takes the longest choice.
    """
    if not (0 <= lc <= 8 and 0 <= lp <= 4 and 0 <= pb <= 4):
        raise ValueError("lc, lp, pb out of range")
    data = bytes(data)
    n = len(data)
    header = bytes([(pb * 5 + lp) * 9 + lc]) + dict_size.to_bytes(4, "little")
    header += (UNKNOWN_SIZE if end_marker else n).to_bytes(8, "little")
    rc = _RangeEncoder()
    m = _Model(lc, lp, pb)
    state, reps = 0, [0, 0, 0, 0]
    head, prev = {}, [0] * n
    window = min(dict_size, 1 << 32) - 1

    def insert(q):
        if q + 3 <= n:
            key = data[q:q + 3]
            prev[q] = head.get(key, -1)
            head[key] = q

    p = 0
    while p < n:
        pos_state = p & ((1 << pb) - 1)
        s2 = (state << POS_BITS_MAX) + pos_state
        limit = min(MATCH_MAX, n - p)
        rep_len, rep_i = 0, 0
        if p > 0 and limit >= 2:
            for i in range(4):
                if reps[i] < p:
                    ln = _match_length(data, p - reps[i] - 1, p, limit)
                    if ln > rep_len:
                        rep_len, rep_i = ln, i
        main_len, main_dist = 0, 0
        if limit >= 3:
            c = head.get(data[p:p + 3], -1)
            for _ in range(chain):
                if c < 0 or p - c - 1 > window:
                    break
                ln = _match_length(data, c, p, limit)
                if ln > main_len:
                    main_len, main_dist = ln, p - c - 1
                    if ln == limit:
                        break
                c = prev[c]
        if rep_len >= 2 and rep_len + 1 >= main_len:
            rc.bit(m.is_match, s2, 1)
            rc.bit(m.is_rep, state, 1)
            if rep_i == 0:
                rc.bit(m.is_rep_g0, state, 0)
                rc.bit(m.is_rep0_long, s2, 1)
            else:
                rc.bit(m.is_rep_g0, state, 1)
                if rep_i == 1:
                    rc.bit(m.is_rep_g1, state, 0)
                else:
                    rc.bit(m.is_rep_g1, state, 1)
                    rc.bit(m.is_rep_g2, state, rep_i - 2)
                d = reps.pop(rep_i)
                reps.insert(0, d)
            rc.length(m.rep_length, pos_state, rep_len - MATCH_MIN)
            state = 8 if state < 7 else 11
            step = rep_len
        elif main_len >= 3:
            rc.bit(m.is_match, s2, 1)
            rc.bit(m.is_rep, state, 0)
            rc.length(m.length, pos_state, main_len - MATCH_MIN)
            state = 7 if state < 7 else 10
            rc.distance(m, main_len - MATCH_MIN, main_dist)
            reps = [main_dist] + reps[:3]
            step = main_len
        elif p > reps[0] and data[p] == data[p - reps[0] - 1]:
            rc.bit(m.is_match, s2, 1)                  # short rep: one byte
            rc.bit(m.is_rep, state, 1)
            rc.bit(m.is_rep_g0, state, 0)
            rc.bit(m.is_rep0_long, s2, 0)
            state = 9 if state < 7 else 11
            step = 1
        else:
            rc.bit(m.is_match, s2, 0)
            base = m.literal_base(p, data[p - 1] if p else 0)
            sym = data[p] | 0x100
            ctx = 1
            i = 7
            if state >= 7:
                match_byte = data[p - reps[0] - 1]
                while i >= 0:
                    mb = (match_byte >> i) & 1
                    b = (sym >> i) & 1
                    rc.bit(m.literal, base + ((1 + mb) << 8) + ctx, b)
                    ctx = (ctx << 1) | b
                    i -= 1
                    if mb != b:
                        break
            while i >= 0:
                b = (sym >> i) & 1
                rc.bit(m.literal, base + ctx, b)
                ctx = (ctx << 1) | b
                i -= 1
            state = _next_literal(state)
            step = 1
        for q in range(p, p + step):
            insert(q)
        p += step
    if end_marker:
        pos_state = p & ((1 << pb) - 1)
        rc.bit(m.is_match, (state << POS_BITS_MAX) + pos_state, 1)
        rc.bit(m.is_rep, state, 0)
        rc.length(m.length, pos_state, 0)
        rc.distance(m, 0, 0xFFFFFFFF)
    return header + rc.finish()
