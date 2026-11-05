# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cole-hariharan-algorithm/. The authors are listed in prov/5Z7RCS.jsonl.

"""The sparse case of the Cole-Hariharan algorithm for k-differences matching.

Edit model: unit-cost insertion, deletion and substitution (Levenshtein),
no transpositions. Indices are 0-based. The result is the sorted list of
start positions s in 0..len(text) such that some substring text[s:j] has edit
distance at most k to the pattern.

The pattern is scanned for 2k disjoint aperiodic substrings of length k*k
(breaks). If they exist, an exact search for the breaks marks the windows of
k consecutive start positions where a match can begin, and a Landau-Vishkin
computation restricted to a band of diagonals checks each window that gets
marks from at least k breaks. If they do not exist (the pattern is mostly
periodic) or k = 0, this file runs the Landau-Vishkin algorithm on all
diagonals; the paper's O(k^4) procedure for mostly periodic patterns is not
implemented here. Start positions are ends in the reversed strings, so all
diagonal work runs on the reversed pattern and text. All loops are iterative.
"""

NONE = -(10**18)  # stands for "no cell of the diagonal has a value <= e"


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


def period(s: str) -> int:
    """Smallest p >= 1 with s[i] == s[i + p] for all valid i (len(s) for s == '')."""
    fail = [0] * (len(s) + 1)  # fail[i] = longest proper border of s[:i]
    for i in range(1, len(s)):
        b = fail[i]
        while b and s[i] != s[b]:
            b = fail[b]
        fail[i + 1] = b + 1 if s[i] == s[b] else 0
    return len(s) - fail[len(s)]


def find_breaks(pattern: str, length: int, want: int) -> list[int]:
    """Start offsets of up to `want` disjoint aperiodic substrings of the given length.

    Greedy left-to-right scan: a window that is periodic with period p is
    extended until the first character that breaks the period; the last
    `length` characters then form an aperiodic string.
    """
    m = len(pattern)
    out: list[int] = []
    c = 0
    while len(out) < want and c + length <= m:
        p = period(pattern[c:c + length])
        if 2 * p > length:
            out.append(c)
            c += length
            continue
        i = c + length
        while i < m and pattern[i] == pattern[i - p]:
            i += 1
        if i == m:
            break
        out.append(i - length + 1)
        c = i + 1
    return out


def find_occurrences(words: list[str], text: str) -> dict[str, list[int]]:
    """Start positions in text of each distinct word; all words have one common length."""
    length = len(words[0])
    goto: list[dict[str, int]] = [{}]
    depth = [0]
    for w in words:  # trie
        v = 0
        for ch in w:
            nxt = goto[v].get(ch)
            if nxt is None:
                nxt = len(goto)
                goto[v][ch] = nxt
                goto.append({})
                depth.append(depth[v] + 1)
            v = nxt
    fail = [0] * len(goto)
    queue = list(goto[0].values())
    head = 0
    while head < len(queue):  # breadth-first failure links
        v = queue[head]
        head += 1
        for ch, u in goto[v].items():
            f = fail[v]
            while f and ch not in goto[f]:
                f = fail[f]
            fail[u] = goto[f][ch] if ch in goto[f] and goto[f][ch] != u else 0
            queue.append(u)
    occ: dict[str, list[int]] = {w: [] for w in words}
    v = 0
    for i, ch in enumerate(text):
        while v and ch not in goto[v]:
            v = fail[v]
        v = goto[v].get(ch, 0)
        if depth[v] == length:  # equal lengths: only full-depth nodes are words
            occ[text[i - length + 1:i + 1]].append(i - length + 1)
    return occ


def band_matches(lce: LCE, m: int, n: int, k: int, dlo: int, dhi: int) -> list[int]:
    """Diagonals d in [dlo, dhi] with L[d][k] == m, computed on diagonals dlo - k .. dhi + k."""
    blo, bhi = max(dlo - k, -m), min(dhi + k, n)
    if blo > bhi:
        return []
    prev: list[int] = []
    for e in range(k + 1):
        cur = [NONE] * (bhi - blo + 1)
        for d in range(max(blo, -e), bhi + 1):
            x = d - blo
            r = max(0, -d)
            if e > 0:
                if prev[x] != NONE:
                    r = max(r, prev[x] + 1)
                if x > 0 and prev[x - 1] != NONE:
                    r = max(r, prev[x - 1])
                if x + 1 < len(prev) and prev[x + 1] != NONE:
                    r = max(r, prev[x + 1] + 1)
            r = min(r, m, n - d)
            if r < m and r + d < n:
                r += lce.query(r, r + d)
            cur[x] = r
        prev = cur
    return [d for d in range(max(dlo, blo), min(dhi, bhi) + 1) if prev[d - blo] == m]


def plan(pattern: str, k: int) -> list[int] | None:
    """Break offsets of the sparse case, or None when the fallback runs."""
    if k == 0:
        return None
    breaks = find_breaks(pattern, k * k, 2 * k)
    return breaks if len(breaks) == 2 * k else None


def candidate_windows(pattern: str, text: str, k: int, breaks: list[int]) -> list[int]:
    """Indices w of the windows [w k, w k + k) of start positions marked by at least k breaks."""
    n, length = len(text), k * k
    words = [pattern[o:o + length] for o in breaks]
    occ = find_occurrences(words, text)  # @line L4
    count = [0] * (n // k + 1)
    stamp = [-1] * (n // k + 1)
    for b, o in enumerate(breaks):  # @line L5
        for q in occ[words[b]]:
            lo, hi = max(0, q - o - k), min(n, q - o + k)
            for w in range(lo // k, hi // k + 1) if lo <= hi else ():
                if stamp[w] != b:
                    stamp[w] = b
                    count[w] += 1
    return [w for w in range(n // k + 1) if count[w] >= k]  # @line L6


def cole_hariharan(pattern: str, text: str, k: int) -> list[int]:
    """Return the sorted start positions of the approximate matches of pattern in text."""
    if k < 0:
        raise ValueError("k must be at least 0")
    m, n = len(pattern), len(text)
    lce = LCE(pattern[::-1], text[::-1])  # start s in text is end n - s in reverse
    breaks = plan(pattern, k)  # @line L1
    if breaks is None:  # @line L2
        return sorted(n - (m + d) for d in band_matches(lce, m, n, k, -m, n - m))  # @line L3
    out: list[int] = []
    for w in candidate_windows(pattern, text, k, breaks):  # @line L7
        s0, s1 = w * k, min(w * k + k - 1, n)
        out.extend(n - (m + d) for d in band_matches(lce, m, n, k, n - m - s1, n - m - s0))
    return sorted(out)  # @line L8
