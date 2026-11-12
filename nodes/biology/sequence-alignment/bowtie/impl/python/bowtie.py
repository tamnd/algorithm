# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bowtie/. The authors are listed in prov/1P62H4.jsonl.

"""A small model of Bowtie's search: an FM-index, backtracking over
substitutions, and double indexing with a mirror index.

The mirror index is the FM-index of the reversed (not complemented) text.
Backward search over the forward index matches the read from its right end,
so a search that allows substitutions only in the left half of the read
covers all hits whose substitution lies in the left half. The same search on
the reversed read over the mirror index covers the hits whose substitution
lies in the right half. Together they find every hit with at most one
mismatch, while the exact half keeps the backtracking small.
"""

ALPHABET = "ACGT"
COMP = {"A": "T", "C": "G", "G": "C", "T": "A"}


def revcomp(s: str) -> str:
    return "".join(COMP[c] for c in reversed(s))


class FMIndex:
    """FM-index of text + '$' with a full suffix array (small inputs)."""

    def __init__(self, text: str) -> None:
        t = text + "$"
        self.n = len(text)
        self.sa = sorted(range(len(t)), key=lambda i: t[i:])
        bwt = [t[i - 1] for i in self.sa]
        self.c = {}
        total = 1  # the single '$' sorts first
        for a in ALPHABET:
            self.c[a] = total
            total += text.count(a)
        # occ[a][i] = number of a in bwt[0 .. i - 1]
        self.occ = {a: [0] * (len(t) + 1) for a in ALPHABET}
        for i, ch in enumerate(bwt):
            for a in ALPHABET:
                self.occ[a][i + 1] = self.occ[a][i] + (ch == a)

    def step(self, a: str, sp: int, ep: int) -> tuple[int, int]:
        """Backward-search step: the interval of a + (current string)."""
        return self.c[a] + self.occ[a][sp], self.c[a] + self.occ[a][ep]

    def full(self) -> tuple[int, int]:
        return 0, self.n + 1

    def exact(self, p: str) -> list[int]:
        sp, ep = self.full()
        for a in reversed(p):
            if a not in self.c:
                return []
            sp, ep = self.step(a, sp, ep)
            if sp >= ep:
                return []
        return sorted(self.sa[sp:ep])


class Counter:
    def __init__(self, limit: int | None) -> None:
        self.steps = 0  # backward-search steps
        self.backtracks = 0  # substitutions tried
        self.limit = limit


def backtrack(fm: FMIndex, p: str, k: int, free_lo: int, free_hi: int, cnt: Counter) -> dict[int, int]:
    """Suffix-array rows -> mismatches, for occurrences of p with at most k
    substitutions, all at read positions in [free_lo, free_hi).

    Depth-first search from the right end of p, with an explicit stack.
    """
    out: dict[int, int] = {}
    sp0, ep0 = fm.full()
    stack = [(len(p), sp0, ep0, 0)]  # @line L1: (next position + 1, interval, mismatches)
    while stack:
        i, sp, ep, z = stack.pop()  # @line L2
        if i == 0:  # @line L3: whole read matched
            for row in range(sp, ep):
                if row not in out or out[row] > z:
                    out[row] = z
            continue
        a = p[i - 1]
        for b in ALPHABET:  # @line L4
            if b != a:
                if z >= k or not (free_lo <= i - 1 < free_hi):  # @line L5
                    continue
                if cnt.limit is not None and cnt.backtracks >= cnt.limit:  # @line L6
                    continue
                cnt.backtracks += 1
            nsp, nep = fm.step(b, sp, ep)  # @line L7
            cnt.steps += 1
            if nsp < nep:  # @line L8
                stack.append((i - 1, nsp, nep, z + (b != a)))
    return out


def positions(fm: FMIndex, rows: dict[int, int]) -> dict[int, int]:
    return {fm.sa[r]: z for r, z in rows.items()}


class Bowtie:
    def __init__(self, ref: str) -> None:
        self.ref = ref
        self.fw = FMIndex(ref)
        self.mirror = FMIndex(ref[::-1])

    def search_strand(self, p: str, k: int, double: bool, cnt: Counter) -> dict[int, int]:
        """Start positions of p in ref with at most k mismatches (k <= 1 for
        double indexing), mapped to the mismatch count."""
        m = len(p)
        if not double:
            return positions(self.fw, backtrack(self.fw, p, k, 0, m, cnt))
        if k > 1:
            raise ValueError("double indexing here handles k <= 1")
        half = m // 2
        # Phase 1: forward index, right half exact, substitutions in the left half.
        hits = positions(self.fw, backtrack(self.fw, p, k, 0, half, cnt))  # @line L9
        # Phase 2: mirror index on the reversed read. The reversed read's
        # left part is the original right half; the original left half is exact.
        rp = p[::-1]
        rows = backtrack(self.mirror, rp, k, 0, m - half, cnt)  # @line L10
        n = len(self.ref)
        for r, z in rows.items():
            start = n - self.mirror.sa[r] - m  # @line L11: position in the original text
            if start not in hits or hits[start] > z:
                hits[start] = z
        return hits  # @line L12

    def align(self, read: str, k: int = 1, double: bool = True, limit: int | None = None):
        """All hits (start, strand, mismatches) with at most k mismatches,
        on both strands, and the search counter."""
        cnt = Counter(limit)
        out = []
        for strand, p in (("+", read), ("-", revcomp(read))):
            for start, z in self.search_strand(p, k, double, cnt).items():
                out.append((start, strand, z))
        return sorted(out), cnt


def naive(ref: str, read: str, k: int) -> list[tuple[int, str, int]]:
    out = []
    for strand, p in (("+", read), ("-", revcomp(read))):
        for s in range(len(ref) - len(p) + 1):
            z = sum(1 for x, y in zip(ref[s:s + len(p)], p) if x != y)
            if z <= k:
                out.append((s, strand, z))
    return sorted(out)
