# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/compressed-suffix-tree/. The authors are listed in prov/Q61TVH.jsonl.

from collections.abc import Hashable, Sequence

INF = 1 << 62
Node = tuple[int, int]


def _suffix_array(t: list[int]) -> list[int]:
    """Suffix array by prefix doubling with library sorts; t ends with a unique smallest code."""
    n = len(t)
    sa, rank, h = list(range(n)), t[:], 1
    while n > 1:
        key = [(rank[i], rank[i + h] if i + h < n else -1) for i in range(n)]
        sa.sort(key=key.__getitem__)
        new = [0] * n
        for r in range(1, n):
            new[sa[r]] = new[sa[r - 1]] + (key[sa[r]] != key[sa[r - 1]])
        rank = new
        if rank[sa[-1]] == n - 1:
            break
        h *= 2
    return sa


class _GammaStream:
    """Positive integers written with the Elias gamma code into one growing integer."""

    def __init__(self) -> None:
        self.bits, self.length = 0, 0

    def write(self, x: int) -> None:
        k = x.bit_length()
        self.length += k - 1
        self.bits |= int(format(x, "b")[::-1], 2) << self.length
        self.length += k

    def read(self, pos: int) -> tuple[int, int]:
        zeros = 0
        while not self.bits >> (pos + zeros) & 1:
            zeros += 1
        pos += zeros
        chunk = (self.bits >> pos) & ((1 << (zeros + 1)) - 1)
        return int(format(chunk, "0%db" % (zeros + 1))[::-1], 2), pos + zeros + 1


class CompressedSuffixTree:
    """Suffix tree of T$ from a compressed suffix array, the PLCP bit vector H and range minima.

    The symbols need a total order and are coded 1 .. sigma; the sentinel $ is the
    code 0, unique and smallest. Ranks and positions are 0-based, N = n + 1. A node
    is a rank range (lb, rb): a leaf has lb == rb, the root is (0, n). Neither the
    text, nor SA, nor LCP is kept after the build: SA comes from Psi and samples,
    LCP[r] = PLCP[SA[r]] comes from H, and the minima of LCP are kept per block of
    `block` ranks in a small tree. The boundary values LCP[0] and LCP[N] are -1.
    """

    def __init__(self, text: Sequence[Hashable], step: int = 4, block: int = 8) -> None:
        self.n = n = len(text)
        self.N, self.step, self.block = n + 1, step, block
        self.symbols = sorted(set(text))
        code = {c: r + 1 for r, c in enumerate(self.symbols)}
        t = [code[c] for c in text] + [0]
        sa = _suffix_array(t)
        isa = [0] * (n + 1)
        for i, p in enumerate(sa):
            isa[p] = i
        # Psi as the increasing values F(i) * N + Psi(i), sampled and gamma coded.
        self.samples: list[tuple[int, int]] = []
        self.stream, prev = _GammaStream(), 0
        for i, p in enumerate(sa):
            value = t[p] * self.N + isa[(p + 1) % self.N]
            if i % block == 0:
                self.samples.append((value, self.stream.length))
            else:
                self.stream.write(value - prev)
            prev = value
        self.sa_sample = {i: p for i, p in enumerate(sa) if p % step == 0 or p == n}
        self.isa_sample = [isa[p] for p in range(0, self.N, step)]
        # PLCP by Kasai's method, then H with a 1 at PLCP[p] + 2p.
        plcp, h = [0] * self.N, 0
        for p in range(self.N):
            if isa[p] > 0:
                q = sa[isa[p] - 1]
                while t[p + h] == t[q + h]:
                    h += 1
                plcp[p] = h
                h = max(h - 1, 0)
            else:
                h = 0
        self.h_bits, self.h_samples = 0, []
        for p in range(self.N):
            if p % block == 0:
                self.h_samples.append(plcp[p] + 2 * p)
            self.h_bits |= 1 << (plcp[p] + 2 * p)
        # Block minima of LCP[0 .. N] in a tree of minima.
        lcp = [-1] + [plcp[sa[r]] for r in range(1, self.N)] + [-1]
        nb = (self.N + 1 + block - 1) // block
        self.size = 1
        while self.size < nb:
            self.size *= 2
        self.tree = [INF] * (2 * self.size)
        for b in range(nb):
            self.tree[self.size + b] = min(lcp[b * block:(b + 1) * block])
        for v in range(self.size - 1, 0, -1):
            self.tree[v] = min(self.tree[2 * v], self.tree[2 * v + 1])

    # ----- the compressed suffix array -----

    def _value(self, i: int) -> int:
        value, pos = self.samples[i // self.block]
        for _ in range(i % self.block):
            gap, pos = self.stream.read(pos)
            value += gap
        return value

    def psi(self, i: int) -> int:
        return self._value(i) % self.N

    def first(self, i: int) -> int:
        return self._value(i) // self.N

    def sa(self, i: int) -> int:
        t = 0
        while i not in self.sa_sample:
            i, t = self.psi(i), t + 1
        return self.sa_sample[i] - t

    def isa(self, p: int) -> int:
        i = self.isa_sample[p // self.step]
        for _ in range(p % self.step):
            i = self.psi(i)
        return i

    # ----- LCP from H, and range minima -----

    def _plcp(self, p: int) -> int:
        """PLCP[p] = select1(H, p) - 2p, by a scan from the sampled one."""
        pos, k = self.h_samples[p // self.block], p % self.block
        while k:
            pos += 1
            if self.h_bits >> pos & 1:
                k -= 1
        return pos - 2 * p

    def lcp(self, r: int) -> int:
        """LCP[r] for 0 <= r <= N, with LCP[0] = LCP[N] = -1."""
        return -1 if r <= 0 or r >= self.N else self._plcp(self.sa(r))

    def _range_min(self, a: int, b: int) -> int:
        """Minimum of LCP[a .. b]."""
        ba, bb, B = a // self.block, b // self.block, self.block
        if ba == bb:
            return min(self.lcp(r) for r in range(a, b + 1))
        best = min(min(self.lcp(r) for r in range(a, (ba + 1) * B)), min(self.lcp(r) for r in range(bb * B, b + 1)))
        lo, hi = ba + 1 + self.size, bb - 1 + self.size
        while lo <= hi:
            if lo & 1:
                best, lo = min(best, self.tree[lo]), lo + 1
            if not hi & 1:
                best, hi = min(best, self.tree[hi]), hi - 1
            lo, hi = lo >> 1, hi >> 1
        return best

    def _fwd(self, start: int, x: int) -> int:
        """The smallest r >= start with LCP[r] < x; N is a valid answer for x >= 0."""
        B = self.block
        for r in range(start, min((start // B + 1) * B, self.N + 1)):
            if self.lcp(r) < x:
                return r
        i = start // B + 1 + self.size
        while self.tree[i] >= x:
            while i & 1:
                i >>= 1
            i += 1
        while i < self.size:
            i = 2 * i if self.tree[2 * i] < x else 2 * i + 1
        return next(r for r in range((i - self.size) * B, self.N + 1) if self.lcp(r) < x)

    def _bwd(self, start: int, x: int) -> int:
        """The largest r <= start with LCP[r] < x; 0 is a valid answer for x >= 0."""
        B = self.block
        for r in range(start, (start // B) * B - 1, -1):
            if self.lcp(r) < x:
                return r
        i = start // B - 1 + self.size
        while self.tree[i] >= x:
            while not i & 1:
                i >>= 1
            i -= 1
        while i < self.size:
            i = 2 * i + 1 if self.tree[2 * i + 1] < x else 2 * i
        b = i - self.size
        return next(r for r in range(min((b + 1) * B, self.N + 1) - 1, -1, -1) if self.lcp(r) < x)

    def rmq(self, a: int, b: int) -> int:
        """The leftmost position of the minimum of LCP[a .. b]."""
        return self._fwd(a, self._range_min(a, b) + 1)

    # ----- tree operations -----

    def root(self) -> Node:
        return (0, self.n)

    def is_leaf(self, v: Node) -> bool:
        return v[0] == v[1]

    def depth(self, v: Node) -> int:
        """String depth; a leaf counts the sentinel."""
        lb, rb = v
        if lb == rb:
            return self.N - self.sa(lb)  # @line L1
        return self.lcp(self.rmq(lb + 1, rb))  # @line L2

    def _enclose(self, k: int) -> Node:
        """The node whose value is LCP[k] and whose range contains k - 1 and k."""
        h = self.lcp(k)
        return (self._bwd(k - 1, h), self._fwd(k + 1, h) - 1)

    def parent(self, v: Node) -> Node | None:
        lb, rb = v
        if v == self.root():
            return None
        k = lb if self.lcp(lb) > self.lcp(rb + 1) else rb + 1  # @line L3
        return self._enclose(k)  # @line L4

    def first_child(self, v: Node) -> Node | None:
        lb, rb = v
        if lb == rb:
            return None
        return (lb, self.rmq(lb + 1, rb) - 1)  # @line L5

    def next_sibling(self, v: Node) -> Node | None:
        lb, rb = v
        if v == self.root() or self.lcp(lb) > self.lcp(rb + 1):  # @line L6
            return None
        h = self.lcp(rb + 1)  # @line L7
        return (rb + 1, self._fwd(rb + 2, h + 1) - 1)

    def children(self, v: Node) -> list[Node]:
        out, w = [], self.first_child(v)
        while w is not None:
            out.append(w)
            w = self.next_sibling(w)
        return out

    def lca(self, u: Node, v: Node) -> Node:
        if u[0] <= v[0] and v[1] <= u[1]:
            return u
        if v[0] <= u[0] and u[1] <= v[1]:
            return v
        if u[0] > v[0]:
            u, v = v, u
        return self._enclose(self.rmq(u[1] + 1, v[0]))  # @line L8

    def suffix_link(self, v: Node) -> Node | None:
        lb, rb = v
        if v == self.root():
            return None
        if lb == rb:
            return self.root() if self.sa(lb) == self.n else (self.psi(lb),) * 2
        return self.lca((self.psi(lb),) * 2, (self.psi(rb),) * 2)  # @line L9

    def letter(self, v: Node, d: int) -> int:
        """Code of the symbol at depth d of the path label of v (0 is the sentinel)."""
        return self.first(self.isa(self.sa(v[0]) + d))  # @line L10

    def child(self, v: Node, c: Hashable) -> Node | None:
        code = {s: r + 1 for r, s in enumerate(self.symbols)}.get(c)
        d = self.depth(v)
        for w in self.children(v):
            if self.letter(w, d) == code:  # @line L11
                return w
        return None

    def find(self, pattern: Sequence[Hashable]) -> tuple[int, int]:
        """Rank range [lo, hi) of the suffixes that start with pattern."""
        code = {s: r + 1 for r, s in enumerate(self.symbols)}
        if any(c not in code for c in pattern):
            return (0, 0)
        p = [code[c] for c in pattern]
        v, d = self.root(), 0
        while d < len(p):
            if self.is_leaf(v):
                return (0, 0)
            w = next((w for w in self.children(v) if self.letter(w, d) == p[d]), None)
            if w is None:
                return (0, 0)
            e = min(self.depth(w), len(p))
            i = self.isa(self.sa(w[0]) + d + 1) if d + 1 < e else 0
            for x in p[d + 1:e]:
                if self.first(i) != x:
                    return (0, 0)
                i = self.psi(i)
            v, d = w, e
        return (v[0], v[1] + 1)

    def label(self, v: Node) -> list[Hashable]:
        """The path label of v, without the sentinel."""
        out, d = [], self.depth(v)
        i = self.isa(self.sa(v[0])) if d else 0
        for _ in range(d):
            c = self.first(i)
            if c == 0:
                break
            out.append(self.symbols[c - 1])
            i = self.psi(i)
        return out
