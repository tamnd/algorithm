---
title: A DSM table returns record i from the i-th entry of every column, and a scan of J columns reads only the pages of those columns
proves: [correctness]
status: full
---

We use the notation of the page. The table has $k$ columns and $N$ records. Column $j$ is a list of pages $P_{j,0}, P_{j,1}, \ldots$, and $first_j(q)$ is the position of the first value of page $P_{j,q}$. A page holds a header $(n, e)$, then $n$ entries of the same size, and the texts of a text column in $[e, p)$.

**Invariant.** For every column $j$:

1. $first_j(0) = 0$, and $first_j(q + 1) = first_j(q) + n(P_{j,q})$, where every page has $n \ge 1$; the last page ends at $N$.
2. Entry $x$ of page $P_{j,q}$ is the value of attribute $j$ of the record at position $first_j(q) + x$ (and its id, if ids are stored).
3. In each page, the entries $[4, 4 + E n)$, with $E$ the entry size, and the texts $[e, p)$ do not overlap, and the texts of different entries do not overlap.

**Lemma 1.** APPEND keeps the invariant.

*Proof.* Line L1 gives the new record the position $i = N$. For column $j$, the value goes to the last page if its entry and its text fit (line L4), and to a new page with $first = i$ otherwise (line L5). In the first case the last page gets entry $n$, at position $first + n = i$ by part 1, and $n$ grows by one, so the last page now ends at $N + 1$. In the second case the new page starts at $i$, which is where the old last page ended, and holds one entry. The test of line L4 is $4 + E(n + 1) + |text| \le e$, so the new entry lies below the new text, and the new text lies below the old texts. The value of each column is checked to fit in an empty page before line L1, so a new page always takes it. $\square$

**Theorem 1 (reconstruction).** FETCH$(i, J)$ returns the attributes $J$ of the record at position $i$.

*Proof.* By part 1, the pages of column $j$ cover the positions $[first_j(q), first_j(q + 1))$ in order, so the page with the largest $first_j(q) \le i$, found by binary search at line L9, is the one that holds position $i$. By part 2, its entry $i - first_j(q)$ is attribute $j$ of record $i$. $\square$

**Theorem 2 (scan).** SCAN$(J)$ outputs, for $i = 0, \ldots, N - 1$ in order, the attributes $J$ of record $i$. It reads only the pages of the columns in $J$, each page once, in order.

*Proof.* Each cursor starts before the first page of its column and moves to the next page exactly when it has used all $n$ entries of the current page. By part 1, the entry it reads for row $i$ is entry $i - first_j(q)$ of the page that holds position $i$, and by part 2 that is attribute $j$ of record $i$. Every value read comes from a column in $J$. $\square$

**Theorem 3 (pages and lines).** For an int column with entries of $E$ bytes ($E = 8$, or 16 with ids), each page holds $m = \lfloor (p - 4) / E \rfloor$ values, so the column has $\lceil N / m \rceil$ pages and a scan of $J$ int columns reads $|J| \lceil N / m \rceil$ pages. A page with $c$ values costs $\lceil (4 + Ec) / L \rceil$ cache lines of $L$ bytes.

*Proof.* An int column has no texts, so a page with $n$ entries takes another one if and only if $4 + E(n + 1) \le p$, that is, $n + 1 \le m$. So every page but the last holds $m$ values, which gives the page count, and Theorem 2 gives the pages of the scan. The scan reads the header and every entry of a page, which are the bytes $[0, 4 + Ec)$, a range that meets $\lceil (4 + Ec) / L \rceil$ lines of $L$ bytes. $\square$

For a table of $k$ int attributes stored in NSM, every page holds $\lfloor (p - 4)/(8k + 4) \rfloor$ records, and a scan reads all $\lceil N / \lfloor (p - 4)/(8k + 4) \rfloor \rceil$ pages whatever $J$ is. Theorem 3 shows that DSM without ids reads about $|J| / k$ of that, slightly less because it needs no slots.
