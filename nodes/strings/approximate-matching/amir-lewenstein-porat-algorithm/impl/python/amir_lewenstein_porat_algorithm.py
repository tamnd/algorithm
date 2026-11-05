# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/amir-lewenstein-porat-algorithm/. The authors are listed in prov/EGHY1F.jsonl.

"""The Amir-Lewenstein-Porat algorithm for the k-mismatch problem.

Edit model: Hamming distance (substitutions only). Indices are 0-based.
The result is the sorted list of start positions i in 0..len(text)-len(pattern)
such that pattern and text[i:i+len(pattern)] differ in at most k places.

Symbols that occur at least f = ceil(sqrt(k * ceil(log2 m))) times in the
pattern are frequent. With many frequent symbols, 2k marks of the pattern
filter the alignments and a kangaroo check with longest common extensions
verifies the few that remain. With few frequent symbols, one convolution per
frequent symbol and direct counting for the other symbols give every
Hamming distance. Convolutions use a number-theoretic transform modulo the
prime 998244353, exact because every count is at most m. All loops are
iterative.
"""

from math import isqrt

MOD = 998244353
ROOT = 3  # a primitive root modulo MOD


def ntt(a: list[int], invert: bool) -> None:
    """Transform a in place; len(a) is a power of two that divides 2**23."""
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        w = pow(ROOT, (MOD - 1) // length, MOD)
        if invert:
            w = pow(w, MOD - 2, MOD)
        half = length >> 1
        for start in range(0, n, length):
            wn = 1
            for k in range(start, start + half):
                u = a[k]
                v = a[k + half] * wn % MOD
                a[k] = (u + v) % MOD
                a[k + half] = (u - v) % MOD
                wn = wn * w % MOD
        length <<= 1
    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD


class LCE:
    """Longest common extension of a suffix of a and a suffix of b."""

    def __init__(self, a: str, b: str) -> None:
        syms = sorted(set(a) | set(b))
        code = {c: r + 2 for r, c in enumerate(syms)}
        s = [code[c] for c in a] + [1] + [code[c] for c in b] + [0]
        self.off = len(a) + 1
        n = len(s)
        rank = s[:]
        sa = list(range(n))
        h = 1
        while True:  # prefix doubling: sort by (rank[i], rank[i + h])
            key = [rank[i] * (n + 2) + (rank[i + h] + 1 if i + h < n else 0) for i in range(n)]
            sa.sort(key=key.__getitem__)
            new = [0] * n
            for t in range(1, n):
                new[sa[t]] = new[sa[t - 1]] + (key[sa[t]] != key[sa[t - 1]])
            rank = new
            if rank[sa[-1]] == n - 1:
                break
            h *= 2
        self.rank = rank
        lcp = [0] * n  # lcp[t] = lcp of suffixes sa[t - 1] and sa[t]
        q = 0
        for i in range(n):
            if rank[i] == 0:
                q = 0
                continue
            j = sa[rank[i] - 1]
            while i + q < n and j + q < n and s[i + q] == s[j + q]:
                q += 1
            lcp[rank[i]] = q
            if q:
                q -= 1
        self.table = [lcp]
        w = 1
        while 2 * w <= n:
            prev = self.table[-1]
            self.table.append([min(prev[t], prev[t + w]) for t in range(n - 2 * w + 1)])
            w *= 2

    def query(self, i: int, j: int) -> int:
        """Length of the longest common prefix of a[i:] and b[j:]."""
        x, y = self.rank[i], self.rank[self.off + j]
        if x > y:
            x, y = y, x
        x += 1  # minimum of lcp[x..y]
        lev = (y - x + 1).bit_length() - 1
        row = self.table[lev]
        return min(row[x], row[y - (1 << lev) + 1])


def parameters(m: int, k: int) -> tuple[int, int]:
    """Return (f, g): the frequency threshold and the number of mark symbols."""
    lam = (m - 1).bit_length() if m > 1 else 0  # ceil(log2 m)
    x = k * lam
    f = isqrt(x)
    if f * f < x:
        f += 1  # f = ceil(sqrt(k * lam))
    f = max(1, f)
    return f, -(-2 * k // f)  # g = ceil(2k / f)


def kangaroo(lce: LCE, m: int, i: int, k: int) -> bool:
    """Return True when the window at i has at most k mismatches."""
    q, e = 0, 0
    while q < m:
        q += lce.query(q, i + q)  # jump over a run of equal symbols
        if q < m:
            e += 1
            if e > k:
                return False
            q += 1
    return True


def correlate(pattern: str, text: str, c: str, out: list[int]) -> None:
    """Add to out[i] the number of q with pattern[q] = text[i + q] = c."""
    m, n = len(pattern), len(text)
    size = 1
    while size < 3 * m - 2:
        size <<= 1
    x = [0] * size
    for q in range(m):
        if pattern[m - 1 - q] == c:
            x[q] = 1
    ntt(x, False)
    for b in range(0, n - m + 1, m):  # text blocks of length 2m - 1
        y = [0] * size
        for j, t in enumerate(text[b:b + 2 * m - 1]):
            if t == c:
                y[j] = 1
        ntt(y, False)
        z = [u * v % MOD for u, v in zip(x, y)]
        ntt(z, True)
        for t in range(min(m, n - m + 1 - b)):
            out[b + t] += z[t + m - 1]


def alp_k_mismatch(pattern: str, text: str, k: int) -> list[int]:
    """Return the start positions with at most k mismatches.

    Precondition: k >= 0. Cost: O(n + n * sqrt(k log m)) time after the
    longest common extension structure, O(n + m) extra space.
    """
    if k < 0:
        raise ValueError("k must be at least 0")
    m, n = len(pattern), len(text)
    if m > n:
        return []
    if k >= m:  # @line L1
        return list(range(n - m + 1))
    f, g = parameters(m, k)  # @line L2
    occ: dict[str, list[int]] = {}
    for q, c in enumerate(pattern):
        occ.setdefault(c, []).append(q)
    freq = sorted(c for c in occ if len(occ[c]) >= f)
    if len(freq) >= g:  # @line L3
        marks = {c: occ[c][:f] for c in freq[:g]}  # @line L4
        count = [0] * (n - m + 1)
        for j, t in enumerate(text):  # @line L5
            for q in marks.get(t, ()):
                if 0 <= j - q <= n - m:
                    count[j - q] += 1
        lce = LCE(pattern, text)
        need = g * f - k
        return [i for i in range(n - m + 1) if count[i] >= need and kangaroo(lce, m, i, k)]  # @line L6
    match = [0] * (n - m + 1)  # @line L7
    for c in freq:  # @line L8
        correlate(pattern, text, c, match)
    frequent = set(freq)
    for j, t in enumerate(text):  # @line L9
        if t not in frequent:
            for q in occ.get(t, ()):
                if 0 <= j - q <= n - m:
                    match[j - q] += 1
    return [i for i in range(n - m + 1) if m - match[i] <= k]  # @line L10


def case_of(pattern: str, k: int) -> str:
    """Return "A" (marks and kangaroo) or "B" (convolutions), for tests."""
    m = len(pattern)
    f, g = parameters(m, k)
    counts: dict[str, int] = {}
    for c in pattern:
        counts[c] = counts.get(c, 0) + 1
    return "A" if sum(1 for v in counts.values() if v >= f) >= g else "B"
