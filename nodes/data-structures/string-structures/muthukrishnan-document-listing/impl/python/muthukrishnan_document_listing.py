# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/muthukrishnan-document-listing/. The authors are listed in prov/QK2HK3.jsonl.

SEP = "\x01"


class DocumentListing:
    """Muthukrishnan's document listing over a collection of strings.

    The documents are concatenated with a separator after each one. D is the document
    array (the document of each suffix in suffix array order) and C[r] is the largest
    r' < r with D[r'] = D[r], or -1. A range minimum structure on C lists the distinct
    documents of a suffix array range with one query per document reported.
    """

    def __init__(self, docs: list[str]) -> None:
        for d in docs:
            if SEP in d:
                raise ValueError("documents must not contain the separator")
        self.docs = docs
        self.text = "".join(d + SEP for d in docs)
        t = self.text
        self.sa = sorted(range(len(t)), key=lambda i: t[i:])
        owner: list[int] = []
        for k, d in enumerate(docs):
            owner += [k] * (len(d) + 1)
        self.d = [owner[p] for p in self.sa]  # @line L1
        last: dict[int, int] = {}
        self.c: list[int] = []
        for r, k in enumerate(self.d):  # @line L2
            self.c.append(last.get(k, -1))
            last[k] = r
        self._build_rmq()  # @line L3
        self.rmq_calls = 0

    def _build_rmq(self) -> None:
        """A sparse table: table[j][i] is the position of the minimum of C[i .. i + 2^j - 1]."""
        c = self.c
        self.table: list[list[int]] = [list(range(len(c)))]
        j = 1
        while (1 << j) <= len(c):
            prev, half = self.table[-1], 1 << (j - 1)
            row = []
            for i in range(len(c) - (1 << j) + 1):
                a, b = prev[i], prev[i + half]
                row.append(a if c[a] <= c[b] else b)
            self.table.append(row)
            j += 1

    def _rmq(self, a: int, b: int) -> int:
        self.rmq_calls += 1
        j = (b - a + 1).bit_length() - 1
        x, y = self.table[j][a], self.table[j][b - (1 << j) + 1]
        return x if self.c[x] <= self.c[y] else y

    def sa_range(self, p: str) -> tuple[int, int]:
        """The suffix array range [lo, hi) of the suffixes that start with p."""
        t, sa, m = self.text, self.sa, len(p)
        lo, hi = 0, len(sa)
        while lo < hi:
            mid = (lo + hi) // 2
            if t[sa[mid]: sa[mid] + m] < p:
                lo = mid + 1
            else:
                hi = mid
        start, hi = lo, len(sa)
        while lo < hi:
            mid = (lo + hi) // 2
            if t[sa[mid]: sa[mid] + m] <= p:
                lo = mid + 1
            else:
                hi = mid
        return start, lo

    def list_documents(self, p: str) -> list[int]:
        """The documents that contain p, each once, in the order they are found."""
        if p == "" or SEP in p:
            raise ValueError("the pattern must be nonempty and must not contain the separator")
        lo, hi = self.sa_range(p)  # @line L4
        left = lo
        out: list[int] = []
        stack = [(lo, hi - 1)]
        while stack:  # @line L5
            a, b = stack.pop()
            if a > b:
                continue
            m = self._rmq(a, b)  # @line L6
            if self.c[m] >= left:  # @line L7
                continue
            out.append(self.d[m])  # @line L8
            stack.append((m + 1, b))
            stack.append((a, m - 1))
        return out
