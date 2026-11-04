# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/string-b-tree/. The authors are listed in prov/EZGPK7.jsonl.

TOP = "\U0010ffff"  # a symbol above every symbol of the strings, used for prefix ranges


def _ch(s: str, i: int) -> str:
    """The symbol at position i, or the empty string past the end (smaller than every symbol)."""
    return s[i] if i < len(s) else ""


class _Node:
    """A node of the String B-tree, with the blind trie of its keys in array form.

    keys are string ids in increasing order of their strings. For an internal node the
    keys are the smallest and largest string of each child, two per child. adj[j] is the
    length of the longest common prefix of keys j - 1 and j (adj[0] = 0), and lc[j], rc[j]
    are the symbols of keys j - 1 and j at position adj[j]: the branching symbols of the
    Patricia trie of the keys.
    """

    __slots__ = ("leaf", "keys", "children", "counts", "adj", "lc", "rc")

    def __init__(self, leaf: bool) -> None:
        self.leaf = leaf
        self.keys: list[int] = []
        self.children: list[_Node] = []
        self.counts: list[int] = []
        self.adj: list[int] = []
        self.lc: list[str] = []
        self.rc: list[str] = []


class StringBTree:
    """A String B-tree over a growing list of strings, in the B+-tree form.

    Leaves hold up to b string ids; internal nodes have up to b children. Each node is
    searched with a blind search on its trie and one comparison with a string, and the
    comparison resumes at the longest common prefix found at the level above, so a search
    for a pattern P reads at most |P| + h symbols of the strings, for a tree of height h.
    The symbol U+10FFFF is reserved.
    """

    def __init__(self, b: int = 8) -> None:
        if b < 4:
            raise ValueError("b must be at least 4")
        self.b = b
        self.strings: list[str] = []
        self.root = _Node(True)
        self._rebuild(self.root)
        self.chars_read = 0  # symbols of stored strings read by comparisons
        self.nodes_read = 0

    def __len__(self) -> int:
        return len(self.strings)

    # ----- the blind trie of one node -----

    def _rebuild(self, x: _Node) -> None:
        s = self.strings
        x.adj, x.lc, x.rc = [0], [""], [""]
        for j in range(1, len(x.keys)):
            u, v = s[x.keys[j - 1]], s[x.keys[j]]
            h = 0
            while h < len(u) and h < len(v) and u[h] == v[h]:
                h += 1
            x.adj.append(h)
            x.lc.append(_ch(u, h))
            x.rc.append(_ch(v, h))

    def _blind(self, x: _Node, p: str) -> int:
        """Blind search: follow the branching symbols of p without reading any stored string."""
        lo, hi = 0, len(x.keys) - 1
        while lo < hi:  # @line L1
            d = min(x.adj[lo + 1: hi + 1])
            splits = [j for j in range(lo + 1, hi + 1) if x.adj[j] == d]
            starts = [lo] + splits
            firsts = [x.lc[splits[0]]] + [x.rc[j] for j in splits]
            c = _ch(p, d) if d < len(p) else None
            g = firsts.index(c) if c in firsts else 0  # @line L2
            lo = starts[g]
            hi = starts[g + 1] - 1 if g + 1 < len(starts) else hi
        return lo

    def _lcp_keys(self, x: _Node, i: int, j: int) -> int:
        if i == j:
            return 1 << 60
        a, b = min(i, j), max(i, j)
        return min(x.adj[a + 1: b + 1])

    def _locate(self, x: _Node, p: str, lam: int) -> tuple[int, list[int]]:
        """Return the number of keys of x that come before p, and lcp(p, key) for every key.

        p is compared with one stored string, starting at position lam, which must be at most
        the longest common prefix of p with the keys of x. A key equal to p comes before p
        unless p ends with TOP.
        """
        self.nodes_read += 1
        si = self._blind(x, p)
        s = self.strings[x.keys[si]]
        ell = lam  # @line L3
        while ell < len(p) and ell < len(s) and p[ell] == s[ell]:
            ell += 1
        self.chars_read += (ell - lam) + (1 if ell < len(s) else 0)
        pc, sc = _ch(p, ell), _ch(s, ell)
        before = 0
        lcps: list[int] = []
        for k in range(len(x.keys)):  # @line L4
            c = self._lcp_keys(x, si, k)
            lcps.append(min(c, ell))
            if c > ell:
                kc = sc
            elif c < ell:
                before += k < si
                continue
            elif k > si:
                j = k
                while x.adj[j] > c:
                    j -= 1
                kc = x.rc[j]
            else:
                j = k + 1
                while x.adj[j] > c:
                    j += 1
                kc = x.lc[j]
            before += kc <= pc
        return before, lcps

    # ----- queries -----

    def _rank(self, p: str) -> int:
        """The number of stored strings that are at most p (strictly less unless p ends in TOP)."""
        x, lam, rank = self.root, 0, 0
        if not x.keys:
            return 0
        while True:
            r, lcps = self._locate(x, p, lam)
            if x.leaf:
                return rank + r  # @line L5
            i = r // 2
            rank += sum(x.counts[:i])
            if r % 2 == 0:  # p falls between child i - 1 and child i
                return rank
            lam = max(lcps[2 * i], lcps[2 * i + 1])  # @line L6
            x = x.children[i]

    def prefix_range(self, p: str) -> tuple[int, int]:
        """Ranks [lo, hi) of the stored strings that start with p, in sorted order."""
        return self._rank_lt(p), self._rank(p + TOP)  # @line L7

    def _rank_lt(self, p: str) -> int:
        # strings < p: rank of p with a symbol below every symbol appended is the same as
        # counting strings that are at most p minus the copies equal to p
        r = self._rank(p)
        return r - (1 if self.contains(p) else 0)

    def contains(self, p: str) -> bool:
        x, lam = self.root, 0
        if not x.keys:
            return False
        while True:
            r, lcps = self._locate(x, p, lam)
            if x.leaf:
                return r > 0 and lcps[r - 1] == len(p) == len(self.strings[x.keys[r - 1]])
            i = r // 2
            if r % 2 == 0:
                return r > 0 and lcps[r - 1] == len(p) == len(self.strings[x.keys[r - 1]])
            lam = max(lcps[2 * i], lcps[2 * i + 1])
            x = x.children[i]

    def sorted_strings(self) -> list[str]:
        out: list[str] = []
        stack = [self.root]
        while stack:
            x = stack.pop()
            if x.leaf:
                out.extend(self.strings[k] for k in x.keys)
            else:
                stack.extend(reversed(x.children))
        return out

    def with_prefix(self, p: str) -> list[str]:
        lo, hi = self.prefix_range(p)
        return self.sorted_strings()[lo:hi]

    def height(self) -> int:
        h, x = 1, self.root
        while not x.leaf:
            x, h = x.children[0], h + 1
        return h

    # ----- insertion -----

    def insert(self, w: str) -> bool:
        """Insert the string w; return False if it is already stored."""
        if TOP in w:
            raise ValueError("the symbol U+10FFFF is reserved")
        if self.contains(w):
            return False
        sid = len(self.strings)
        self.strings.append(w)
        path: list[tuple[_Node, int]] = []
        x, lam = self.root, 0
        while not x.leaf:  # @line L8
            r, lcps = self._locate(x, w, lam)
            i = min(max(r - 1, 0) // 2, len(x.children) - 1)
            if r % 2 == 1:
                lam = max(lcps[2 * i], lcps[2 * i + 1])
            else:
                lam = 0
            path.append((x, i))
            x = x.children[i]
        r, _ = self._locate(x, w, 0) if x.keys else (0, [])
        x.keys.insert(r, sid)  # @line L9
        self._rebuild(x)
        child: _Node = x
        for parent, i in reversed(path):  # @line L10
            parent.counts[i] += 1
            extra = self._split(child) if self._size(child) > self.b else None
            if extra is not None:
                parent.children.insert(i + 1, extra)
                parent.counts[i] = self._count(child)
                parent.counts.insert(i + 1, self._count(extra))
            self._refresh(parent)
            child = parent
        extra = self._split(child) if self._size(child) > self.b else None
        if extra is not None:  # @line L11
            root = _Node(False)
            root.children = [child, extra]
            root.counts = [self._count(child), self._count(extra)]
            self._refresh(root)
            self.root = root
        return True

    def _size(self, x: _Node) -> int:
        return len(x.keys) if x.leaf else len(x.children)

    def _count(self, x: _Node) -> int:
        return len(x.keys) if x.leaf else sum(x.counts)

    def _split(self, x: _Node) -> _Node:
        y = _Node(x.leaf)
        if x.leaf:
            m = len(x.keys) // 2
            y.keys, x.keys = x.keys[m:], x.keys[:m]
            self._rebuild(x)
            self._rebuild(y)
        else:
            m = len(x.children) // 2
            y.children, x.children = x.children[m:], x.children[:m]
            y.counts, x.counts = x.counts[m:], x.counts[:m]
            self._refresh(x)
            self._refresh(y)
        return y

    def _first(self, x: _Node) -> int:
        return x.keys[0]

    def _last(self, x: _Node) -> int:
        return x.keys[-1]

    def _refresh(self, x: _Node) -> None:
        """Recompute the keys of an internal node from its children, and its blind trie."""
        x.keys = []
        for c in x.children:
            x.keys += [self._first(c), self._last(c)]
        self._rebuild(x)

    # ----- invariant -----

    def check_invariant(self) -> None:
        s = self.strings
        depths: set[int] = set()
        stack: list[tuple[_Node, int]] = [(self.root, 1)]
        total = 0
        while stack:
            x, d = stack.pop()
            ks = [s[k] for k in x.keys]
            assert all(ks[j - 1] <= ks[j] for j in range(1, len(ks)))
            if x.leaf:
                depths.add(d)
                assert len(x.keys) <= self.b
                assert x is self.root or len(x.keys) >= self.b // 2
                assert len(set(ks)) == len(ks)
                total += len(x.keys)
            else:
                assert 2 <= len(x.children) <= self.b
                assert x is self.root or len(x.children) >= self.b // 2
                assert x.keys == [k for c in x.children for k in (self._first(c), self._last(c))]
                assert x.counts == [self._count(c) for c in x.children]
                stack.extend((c, d + 1) for c in x.children)
            saved = (x.adj, x.lc, x.rc)
            self._rebuild(x)
            assert saved == (x.adj, x.lc, x.rc), "stale blind trie"
        assert len(depths) == 1 and total == len(s)
        assert self.sorted_strings() == sorted(s)
