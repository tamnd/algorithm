# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prediction-by-partial-matching/. The authors are listed in prov/3NN434.jsonl.

"""PPMC of order k with full exclusion, over a small arithmetic coder.

For each symbol, the coder starts at the longest context (the k symbols before
it) and goes down to shorter ones. In each context, after removing the symbols
already excluded, a seen symbol gets probability c / (n + q) and the escape
gets q / (n + q), where n is the sum of the counts and q the number of
distinct symbols (escape method C). After an escape, every symbol of that
context is excluded from the shorter ones. Below order 0 is an order -1 model
that is uniform over the symbols not excluded. After coding, the count of the
symbol is increased in the context where it was found and in all longer ones
(update exclusion).

The arithmetic coder is the integer coder of Witten, Neal and Cleary with
32-bit registers; totals stay below 2^16.
"""

import math

CODE_BITS = 32
TOP = (1 << CODE_BITS) - 1
QTR = 1 << (CODE_BITS - 2)
HALF = 2 * QTR
MAX_TOTAL = 1 << 16


class _Encoder:
    def __init__(self) -> None:
        self.low, self.high, self.pending = 0, TOP, 0
        self.bits: list[int] = []

    def _emit(self, b: int) -> None:
        self.bits.append(b)
        self.bits.extend([1 - b] * self.pending)
        self.pending = 0

    def encode(self, lo: int, hi: int, total: int) -> None:
        r = self.high - self.low + 1
        self.high = self.low + r * hi // total - 1
        self.low = self.low + r * lo // total
        while True:
            if self.high < HALF:
                self._emit(0)
            elif self.low >= HALF:
                self._emit(1)
                self.low -= HALF
                self.high -= HALF
            elif self.low >= QTR and self.high < HALF + QTR:
                self.pending += 1
                self.low -= QTR
                self.high -= QTR
            else:
                break
            self.low = 2 * self.low
            self.high = 2 * self.high + 1

    def finish(self) -> bytes:
        self.pending += 1
        self._emit(0 if self.low < QTR else 1)
        bits = self.bits + [0] * (-len(self.bits) % 8)
        return bytes(int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8))


class _Decoder:
    def __init__(self, data: bytes) -> None:
        self.data, self.pos = data, 0
        self.low, self.high, self.value = 0, TOP, 0
        for _ in range(CODE_BITS):
            self.value = 2 * self.value + self._bit()

    def _bit(self) -> int:
        i = self.pos
        self.pos += 1
        return (self.data[i >> 3] >> (7 - (i & 7))) & 1 if i < 8 * len(self.data) else 0

    def target(self, total: int) -> int:
        r = self.high - self.low + 1
        return ((self.value - self.low + 1) * total - 1) // r

    def consume(self, lo: int, hi: int, total: int) -> None:
        r = self.high - self.low + 1
        self.high = self.low + r * hi // total - 1
        self.low = self.low + r * lo // total
        while True:
            if self.high < HALF:
                pass
            elif self.low >= HALF:
                self.low -= HALF
                self.high -= HALF
                self.value -= HALF
            elif self.low >= QTR and self.high < HALF + QTR:
                self.low -= QTR
                self.high -= QTR
                self.value -= QTR
            else:
                break
            self.low = 2 * self.low
            self.high = 2 * self.high + 1
            self.value = 2 * self.value + self._bit()


class _Model:
    """The context tables of PPMC: context tuple -> {symbol: count}."""

    def __init__(self, k: int, sigma: int) -> None:
        self.k, self.sigma = k, sigma
        self.tables: dict[tuple, dict[int, int]] = {}

    def candidates(self, ctx: tuple, excluded: set) -> list[tuple[int, int]]:
        table = self.tables.get(ctx, {})
        return sorted((s, c) for s, c in table.items() if s not in excluded)  # @line L4

    def update(self, history: list[int], s: int, found_order: int) -> None:
        top = min(self.k, len(history))
        for j in range(max(found_order, 0), top + 1):  # @line L11
            ctx = tuple(history[len(history) - j:])
            table = self.tables.setdefault(ctx, {})
            table[s] = table.get(s, 0) + 1
            if sum(table.values()) + len(table) >= MAX_TOTAL:
                for t in list(table):
                    table[t] = (table[t] + 1) // 2


def encode(data: list[int], k: int, sigma: int = 256) -> bytes:
    enc = _Encoder()
    model = _Model(k, sigma)
    for i, s in enumerate(data):  # @line L1
        if not 0 <= s < sigma:
            raise ValueError("symbol out of range")
        excluded: set[int] = set()
        o = min(k, i)  # @line L2
        while o >= 0:  # @line L3
            cand = model.candidates(tuple(data[i - o:i]), excluded)
            if not cand:  # @line L5
                o -= 1
                continue
            n = sum(c for _, c in cand)  # @line L6
            q = len(cand)
            lo = 0
            for t, c in cand:
                if t == s:
                    break
                lo += c
            else:
                enc.encode(n, n + q, n + q)  # @line L8
                excluded.update(t for t, _ in cand)  # @line L9
                o -= 1
                continue
            enc.encode(lo, lo + dict(cand)[s], n + q)  # @line L7
            break
        if o < 0:  # @line L10
            rank = sum(1 for t in range(s) if t not in excluded)
            enc.encode(rank, rank + 1, sigma - len(excluded))
        model.update(data[:i] if i <= k else data[i - k:i], s, o)
    return enc.finish()


def decode(code: bytes, n: int, k: int, sigma: int = 256) -> list[int]:
    dec = _Decoder(code)
    model = _Model(k, sigma)
    out: list[int] = []
    for i in range(n):  # @line L12
        excluded: set[int] = set()
        o = min(k, i)  # @line L13
        s = -1
        while o >= 0:  # @line L14
            cand = model.candidates(tuple(out[i - o:i]), excluded)
            if not cand:
                o -= 1
                continue
            tot = sum(c for _, c in cand)
            q = len(cand)
            t = dec.target(tot + q)
            if t < tot:
                lo = 0
                for sym, c in cand:
                    if t < lo + c:
                        s = sym
                        dec.consume(lo, lo + c, tot + q)
                        break
                    lo += c
                break
            dec.consume(tot, tot + q, tot + q)
            excluded.update(sym for sym, _ in cand)
            o -= 1
        if o < 0:  # @line L15
            rest = [t for t in range(sigma) if t not in excluded]
            rank = dec.target(len(rest))
            s = rest[rank]
            dec.consume(rank, rank + 1, len(rest))
        out.append(s)
        model.update(out[:i] if i <= k else out[i - k:i], s, o)  # @line L16
    return out


def ideal_length(data: list[int], k: int, sigma: int = 256) -> float:
    """The sum of -lg of the probabilities PPMC gives the symbols, escapes included."""
    model = _Model(k, sigma)
    bits = 0.0
    for i, s in enumerate(data):
        excluded: set[int] = set()
        o = min(k, i)
        while o >= 0:
            cand = model.candidates(tuple(data[i - o:i]), excluded)
            if not cand:
                o -= 1
                continue
            n = sum(c for _, c in cand)
            q = len(cand)
            counts = dict(cand)
            if s in counts:
                bits -= math.log2(counts[s] / (n + q))
                break
            bits -= math.log2(q / (n + q))
            excluded.update(counts)
            o -= 1
        if o < 0:
            bits += math.log2(sigma - len(excluded))
        model.update(data[:i] if i <= k else data[i - k:i], s, o)
    return bits


def probabilities(data: list[int], k: int, sigma: int = 256) -> list[list[tuple[str, float]]]:
    """For each symbol, the list of (event, probability) that PPMC codes, for the worked example."""
    model = _Model(k, sigma)
    steps = []
    for i, s in enumerate(data):
        events = []
        excluded: set[int] = set()
        o = min(k, i)
        while o >= 0:
            cand = model.candidates(tuple(data[i - o:i]), excluded)
            if not cand:
                o -= 1
                continue
            n = sum(c for _, c in cand)
            q = len(cand)
            counts = dict(cand)
            if s in counts:
                events.append((f"order {o}", counts[s] / (n + q)))
                break
            events.append((f"escape from order {o}", q / (n + q)))
            excluded.update(counts)
            o -= 1
        if o < 0:
            events.append(("order -1", 1 / (sigma - len(excluded))))
        steps.append(events)
        model.update(data[:i] if i <= k else data[i - k:i], s, o)
    return steps
