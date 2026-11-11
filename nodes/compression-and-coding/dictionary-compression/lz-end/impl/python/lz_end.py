# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lz-end/. The authors are listed in prov/71G02H.jsonl.

"""LZ-End parsing (Kreft and Navarro), its decoder and its random access.

Each phrase is a copy part followed by one explicit symbol. The copy part is
the longest prefix of the rest of the text (leaving room for the explicit
symbol) that is a suffix of t[0 .. E], where E is the end of an earlier
phrase. A phrase is stored as (src, length, symbol): src is the index of the
phrase at whose end the copy ends, or -1 when the copy is empty.

The parser follows Kreft and Navarro: a suffix of t[0 .. E] read backwards
is a prefix of the reversed text, so the parser keeps the suffix array
interval of the reversed copy part in an FM-index of the reversed text and
grows it by one backward step per symbol. The ranks of the reversed
prefixes that end at a phrase end are marked in a Fenwick tree, and a range
minimum structure stops the search once the copy part no longer occurs
inside t[0 .. i-1].
"""

from bisect import bisect_left


def suffix_array(s) -> list[int]:
    """Prefix doubling on a sequence of integers."""
    n = len(s)
    sa = list(range(n))
    rank = list(s)
    k = 1
    while True:
        key = [(rank[i], rank[i + k] if i + k < n else -1) for i in range(n)]
        sa.sort(key=key.__getitem__)
        new = [0] * n
        for r in range(1, n):
            new[sa[r]] = new[sa[r - 1]] + (key[sa[r]] != key[sa[r - 1]])
        rank = new
        if n == 0 or rank[sa[-1]] == n - 1:
            return sa
        k *= 2


class _Fenwick:
    """Counts of marked ranks; finds the first marked rank at or after a position."""

    def __init__(self, size: int) -> None:
        self.n = size
        self.tree = [0] * (size + 1)
        self.log = max(1, size).bit_length()

    def add(self, k: int) -> None:
        k += 1
        while k <= self.n:
            self.tree[k] += 1
            k += k & -k

    def prefix(self, k: int) -> int:
        """Number of marks in [0, k)."""
        s = 0
        while k > 0:
            s += self.tree[k]
            k -= k & -k
        return s

    def first_at_least(self, k: int) -> int:
        """Smallest marked rank >= k, or n when there is none."""
        want = self.prefix(k) + 1
        pos = 0
        for b in range(self.log, -1, -1):
            nxt = pos + (1 << b)
            if nxt <= self.n and self.tree[nxt] < want:
                pos = nxt
                want -= self.tree[nxt]
        return pos


class _ReverseFM:
    """FM-index of reverse(t) + sentinel, with a range minimum over prefix ends."""

    def __init__(self, t) -> None:
        n = len(t)
        self.n = n
        self.code = {c: k + 1 for k, c in enumerate(sorted(set(t)))}
        r = [self.code[c] for c in reversed(t)] + [0]
        m = n + 1
        sa = suffix_array(r)
        self.isa = [0] * m
        for k, p in enumerate(sa):
            self.isa[p] = k
        bwt = [r[p - 1] if p else r[m - 1] for p in sa]
        sigma = len(self.code) + 1
        counts = [0] * (sigma + 1)
        for x in r:
            counts[x + 1] += 1
        for x in range(sigma):
            counts[x + 1] += counts[x]
        self.c = counts
        self.occ = []
        for x in range(sigma):
            row = [0] * (m + 1)
            for k in range(m):
                row[k + 1] = row[k] + (bwt[k] == x)
            self.occ.append(row)
        # The suffix of r at p is t[n-1-p], ..., t[0]: a prefix of t that ends at n-1-p.
        # The sentinel suffix (p = n) ends at -1.
        ends = [n - 1 - p for p in sa]
        self.table = [ends]
        w = 1
        while 2 * w <= m:
            prev = self.table[-1]
            self.table.append([min(prev[k], prev[k + w]) for k in range(m - 2 * w + 1)])
            w *= 2

    def step(self, symbol, sp: int, ep: int) -> tuple[int, int]:
        """Backward search: prepend symbol to the reversed pattern of [sp, ep)."""
        x = self.code[symbol]
        return self.c[x] + self.occ[x][sp], self.c[x] + self.occ[x][ep]

    def min_end(self, sp: int, ep: int) -> int:
        """Smallest end of a prefix of t whose rank lies in [sp, ep), ep > sp."""
        k = (ep - sp).bit_length() - 1
        row = self.table[k]
        return min(row[sp], row[ep - (1 << k)])

    def rank_of_end(self, e: int) -> int:
        return self.isa[self.n - 1 - e]


def lz_end_parse(t) -> list[tuple[int, int, object]]:
    """Return the LZ-End phrases of t as (src, length, symbol)."""
    n = len(t)
    phrases: list[tuple[int, int, object]] = []
    if n == 0:
        return phrases
    fm = _ReverseFM(t)  # @line L1
    marks = _Fenwick(n + 1)
    phrase_at_rank: dict[int, int] = {}
    i = 0
    while i < n:  # @line L2
        sp, ep = 0, n + 1  # @line L3
        best, src = 0, -1
        j = i
        while j < n - 1:  # @line L4
            sp, ep = fm.step(t[j], sp, ep)  # @line L5
            if sp >= ep or fm.min_end(sp, ep) >= i:  # @line L6
                break
            r = marks.first_at_least(sp)  # @line L7
            if r < ep:
                best, src = j - i + 1, phrase_at_rank[r]  # @line L8
            j += 1
        phrases.append((src, best, t[i + best]))  # @line L9
        r = fm.rank_of_end(i + best)  # @line L10
        marks.add(r)
        phrase_at_rank[r] = len(phrases) - 1
        i += best + 1
    return phrases  # @line L11


def phrase_ends(phrases) -> list[int]:
    ends, e = [], -1
    for _, length, _ in phrases:
        e += length + 1
        ends.append(e)
    return ends


def decode(phrases) -> list:
    out: list = []
    ends = phrase_ends(phrases)
    for src, length, symbol in phrases:
        if length:
            e = ends[src]
            out.extend(out[e - length + 1:e + 1])
        out.append(symbol)
    return out


def extract(phrases, ends, i: int, j: int, counter=None) -> list:
    """Return t[i:j] without decoding the whole text.

    The range is first extended to the end of the phrase that holds t[j-1].
    A substring that ends at a phrase end is rebuilt right to left: the last
    symbol is explicit, and the copy part ends at the end of an earlier
    phrase, so each piece of work again ends at a phrase end. Every inner
    step writes one symbol. The optional counter list gets the step count.
    """
    if i >= j:
        return []
    e = ends[bisect_left(ends, j - 1)]
    at_end = {x: p for p, x in enumerate(ends)}
    out: list = [None] * (e - i + 1)
    stack = [(e, e - i + 1, e - i)]  # (text end, length, index in out of that end)
    steps = 0
    while stack:
        end, length, o = stack.pop()
        while length > 0:
            src, copy, symbol = phrases[at_end[end]]
            out[o] = symbol
            steps += 1
            length, o, end = length - 1, o - 1, end - 1
            k = min(length, copy)
            if k:
                stack.append((ends[src], k, o))
            length, o, end = length - k, o - k, end - k
    if counter is not None:
        counter.append(steps)
    return out[:j - i]


def lz_end_brute(t) -> list[tuple[int, object]]:
    """Oracle: (copy length, symbol) per phrase, by trying every length and every phrase end."""
    n, out, ends, i = len(t), [], [], 0
    while i < n:
        best = 0
        for length in range(1, n - i):
            piece = t[i:i + length]
            if any(e + 1 >= length and t[e - length + 1:e + 1] == piece for e in ends):
                best = length
        out.append((best, t[i + best]))
        ends.append(i + best)
        i += best + 1
    return out


def lz77_parse(t) -> list[tuple[int, object]]:
    """Greedy LZ77 with an unbounded window, as (copy length, symbol) phrases.

    The copy may overlap the phrase itself; it must start before the phrase.
    """
    n, out, i = len(t), [], 0
    while i < n:
        length = 0
        # t[i:i+L+1] starts before i exactly when it lies inside t[:i+L].
        while i + length < n - 1 and t.find(t[i:i + length + 1], 0, i + length) >= 0:
            length += 1
        out.append((length, t[i + length]))
        i += length + 1
    return out
