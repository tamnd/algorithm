# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quotient-filter/. The authors are listed in prov/44MVA2.jsonl.

"""Quotient filter (Bender et al. 2012, after Cleary 1984)."""

import hashlib

Key = str | bytes | int


class QuotientFilter:
    """2^q slots, each with an r-bit remainder and three metadata bits.

    A key's fingerprint has q + r bits: the top q bits are its quotient fq,
    the canonical slot, and the low r bits are its remainder fr. The table
    is circular. It holds at most 2^q - 1 fingerprints, so one slot is
    always empty. lookup follows the metadata bits; insert and delete decode
    the part of the cluster from the nearest unshifted slot, change it, and
    write it back.
    """

    def __init__(self, q: int, r: int, seed: int = 0) -> None:
        if q < 1 or r < 1:
            raise ValueError("q and r must be positive")
        self.q, self.r, self.seed = q, r, seed
        self.m = 1 << q
        self.occupied = [False] * self.m  # some fingerprint has quotient j
        self.continuation = [False] * self.m  # slot is in a run, not its first slot
        self.shifted = [False] * self.m  # slot holds a fingerprint with another quotient
        self.remainder = [0] * self.m
        self.n = 0

    def _fp(self, key: Key) -> tuple[int, int]:
        d = hashlib.blake2b(repr(key).encode(), digest_size=8, key=self.seed.to_bytes(8, "little")).digest()
        v = int.from_bytes(d, "little") % (1 << (self.q + self.r))
        return v >> self.r, v & ((1 << self.r) - 1)

    def _is_empty(self, p: int) -> bool:
        return not (self.occupied[p] or self.continuation[p] or self.shifted[p])

    def _contains(self, fq: int, fr: int) -> bool:
        m = self.m
        if not self.occupied[fq]:  # @line L1
            return False
        b = fq
        while self.shifted[b]:  # @line L2: back to an unshifted slot
            b = (b - 1) % m
        s = b  # @line L3
        while b != fq:  # @line L4: skip one run for each occupied quotient before fq
            s = (s + 1) % m  # @line L5
            while self.continuation[s]:
                s = (s + 1) % m
            b = (b + 1) % m  # @line L6
            while not self.occupied[b]:
                b = (b + 1) % m
        while True:  # @line L7: s is the start of the run of fq
            if self.remainder[s] == fr:  # @line L8
                return True
            s = (s + 1) % m  # @line L9
            if not self.continuation[s]:
                return False  # @line L10

    def query(self, key: Key) -> bool:
        """False if key is surely absent; True if it may be present."""
        return self._contains(*self._fp(key))

    def _start(self, fq: int) -> int:
        b = fq
        while self.shifted[b]:
            b = (b - 1) % self.m
        return b

    def _decode(self, b: int) -> tuple[list[tuple[int, int]], int]:
        """The fingerprints stored from slot b to the next empty slot, and that length."""
        m, slots, p = self.m, [], b
        while not self._is_empty(p) and len(slots) < m:
            slots.append(p)
            p = (p + 1) % m
        quotients = [j for j in slots if self.occupied[j]]
        out, k = [], -1
        for p in slots:
            if not self.continuation[p]:
                k += 1
            out.append((quotients[k], self.remainder[p]))
        return out, len(slots)

    def _encode(self, b: int, elems: list[tuple[int, int]], old_len: int) -> None:
        """Write elems from slot b on in canonical order, over old_len old slots."""
        m = self.m
        for t in range(old_len):
            p = (b + t) % m
            self.occupied[p] = self.continuation[p] = self.shifted[p] = False
            self.remainder[p] = 0
        elems.sort(key=lambda e: ((e[0] - b) % m, e[1]))
        pos, i = 0, 0
        while i < len(elems):
            fq = elems[i][0]
            self.occupied[fq] = True
            pos = max(pos, (fq - b) % m)  # the run starts at fq or right after the previous run
            first = True
            while i < len(elems) and elems[i][0] == fq:
                p = (b + pos) % m
                self.remainder[p] = elems[i][1]
                self.continuation[p] = not first
                self.shifted[p] = p != fq
                first, pos, i = False, pos + 1, i + 1

    def insert(self, key: Key) -> bool:
        """Add key. False, with no change, if the table already holds 2^q - 1 fingerprints."""
        if self.n >= self.m - 1:
            return False
        fq, fr = self._fp(key)
        b = self._start(fq)  # @line L11
        elems, length = self._decode(b)  # @line L12
        elems.append((fq, fr))  # @line L13
        self._encode(b, elems, length)  # @line L14
        self.n += 1
        return True

    def delete(self, key: Key) -> bool:
        """Remove one copy of the fingerprint of key. Precondition: key is present."""
        fq, fr = self._fp(key)
        if not self._contains(fq, fr):
            return False
        b = self._start(fq)  # @line L15
        elems, length = self._decode(b)
        elems.remove((fq, fr))  # @line L16
        self._encode(b, elems, length)  # @line L17
        self.n -= 1
        return True
