# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bwa/. The authors are listed in prov/M5J6FC.jsonl.

"""A small model of BWA-backtrack (Li and Durbin, 2009) and of the SMEM
seeds of BWA-MEM.

BWA-backtrack searches the FM-index of the reference X for strings within
z differences (mismatches, insertions, deletions) of a read W. It reads W
from right to left by backward search and prunes with a lower bound D(i) on
the differences that W[0 .. i] needs. D comes from a greedy split of W into
pieces that do not occur in X; that test uses an FM-index of X reversed.
"""

ALPHABET = "ACGT"


class FMIndex:
    """FM-index of text + '$' with a full suffix array (small inputs)."""

    def __init__(self, text: str) -> None:
        t = text + "$"
        self.n = len(text)
        self.sa = sorted(range(len(t)), key=lambda i: t[i:])
        bwt = [t[i - 1] for i in self.sa]
        self.c = {}
        total = 1
        for a in ALPHABET:
            self.c[a] = total
            total += text.count(a)
        self.occ = {a: [0] * (len(t) + 1) for a in ALPHABET}
        for i, ch in enumerate(bwt):
            for a in ALPHABET:
                self.occ[a][i + 1] = self.occ[a][i] + (ch == a)

    def step(self, a: str, sp: int, ep: int) -> tuple[int, int]:
        if a not in self.c:
            return 0, 0
        return self.c[a] + self.occ[a][sp], self.c[a] + self.occ[a][ep]


def calculate_d(rev: FMIndex, w: str) -> list[int]:
    """D[i] = number of disjoint pieces of W[0 .. i] that do not occur in X.

    rev is the FM-index of X reversed: backward search of W[j], W[j+1], ...
    on rev tracks the rows of reverse(W[j .. i]), which occurs in reverse(X)
    exactly when W[j .. i] occurs in X.
    """
    d = []
    z = 0  # @line L1
    sp, ep = 0, rev.n + 1  # interval of the empty piece
    for ch in w:  # @line L2
        sp, ep = rev.step(ch, sp, ep)
        if sp >= ep:  # @line L3: W[j .. i] is not a substring of X
            z += 1  # @line L4
            sp, ep = 0, rev.n + 1  # @line L5: start a new piece at i + 1
        d.append(z)  # @line L6
    return d


class Counter:
    def __init__(self) -> None:
        self.states = 0


def inexact_search(fw: FMIndex, rev: FMIndex, w: str, z: int, use_d: bool = True,
                   cnt: Counter | None = None) -> set[tuple[int, int, int]]:
    """Triples (sp, ep, length) of suffix-array intervals of strings v with
    an alignment to w of at most z differences (v is aligned in full, and the
    alignment does not start with a deleted letter of v)."""
    m = len(w)
    d = calculate_d(rev, w) if use_d else [0] * m

    def bound(i: int) -> int:
        return d[i] if i >= 0 else 0

    out = set()
    seen = set()
    stack = [(m - 1, z, 0, fw.n + 1, 0)]  # @line L7
    while stack:
        i, zz, sp, ep, length = stack.pop()
        if (i, zz, sp, ep, length) in seen:
            continue
        seen.add((i, zz, sp, ep, length))
        if cnt is not None:
            cnt.states += 1
        if zz < bound(i):  # @line L8: prune by the lower bound
            continue
        if i < 0:  # @line L9
            out.add((sp, ep, length))
            continue
        if zz > 0:
            stack.append((i - 1, zz - 1, sp, ep, length))  # @line L10: W[i] is an insertion
        for b in ALPHABET:  # @line L11
            nsp, nep = fw.step(b, sp, ep)
            if nsp >= nep:
                continue
            if zz > 0:
                stack.append((i, zz - 1, nsp, nep, length + 1))  # @line L12: b is deleted from W
            if b == w[i]:
                stack.append((i - 1, zz, nsp, nep, length + 1))  # @line L13: match
            elif zz > 0:
                stack.append((i - 1, zz - 1, nsp, nep, length + 1))  # @line L14: mismatch
    return out


class BWA:
    def __init__(self, ref: str) -> None:
        self.ref = ref
        self.fw = FMIndex(ref)
        self.rev = FMIndex(ref[::-1])

    def end_positions(self, w: str, z: int, use_d: bool = True, cnt: Counter | None = None) -> set[int]:
        """End positions e (exclusive) of the occurrences found."""
        ends = set()
        for sp, ep, length in inexact_search(self.fw, self.rev, w, z, use_d, cnt):
            for row in range(sp, ep):
                ends.add(self.fw.sa[row] + length)
        return ends

    def matching_statistics(self, q: str) -> list[int]:
        """ms[a] = length of the longest prefix of q[a ..] that occurs in ref,
        by forward extension with the index of the reversed reference."""
        out = []
        for a in range(len(q)):
            sp, ep = 0, self.rev.n + 1
            length = 0
            for ch in q[a:]:
                sp, ep = self.rev.step(ch, sp, ep)
                if sp >= ep:
                    break
                length += 1
            out.append(length)
        return out

    def smems(self, q: str, min_len: int = 1) -> list[tuple[int, int]]:
        """Super-maximal exact matches of q, as query intervals [a, b)."""
        ms = self.matching_statistics(q)
        out = []
        prev_end = -1
        for a, l in enumerate(ms):
            end = a + l
            if l > 0 and end > prev_end and l >= min_len:
                out.append((a, end))
            prev_end = max(prev_end, end)
        return out


def edit_distance(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] != b[j - 1]))
        prev = cur
    return prev[-1]


def sellers_table(ref: str, w: str) -> list[list[int]]:
    """t[i][e] = min over s of ed(w[:i], ref[s:e]) (Sellers, 1980)."""
    n = len(ref)
    t = [[0] * (n + 1)]
    for i in range(1, len(w) + 1):
        prev = t[-1]
        cur = [i] + [0] * n
        for e in range(1, n + 1):
            cur[e] = min(prev[e] + 1, cur[e - 1] + 1, prev[e - 1] + (w[i - 1] != ref[e - 1]))
        t.append(cur)
    return t


def naive_ends(ref: str, w: str, z: int) -> set[int]:
    """End positions e with min over s of ed(w, ref[s:e]) <= z."""
    last = sellers_table(ref, w)[-1]
    return {e for e, v in enumerate(last) if v <= z}


def naive_smems(ref: str, q: str) -> list[tuple[int, int]]:
    occurs = [(a, b) for a in range(len(q)) for b in range(a + 1, len(q) + 1) if q[a:b] in ref]
    return sorted(x for x in occurs
                  if not any(y != x and y[0] <= x[0] and x[1] <= y[1] for y in occurs))
