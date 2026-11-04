---
title: The disjoint sparse table returns the product of each range
proves: [correctness, complexity]
status: full
---

Let $(S, \cdot)$ be a semigroup, $A[0 \ldots n-1]$ over $S$ with $n \ge 1$, $K = \lceil \lg n \rceil$ and $N = 2^K$. Write $A[i \ldots j] = A[i] \cdot A[i+1] \cdots A[j]$ for $i \le j$; by associativity it does not depend on the bracketing, and $A[i \ldots j] = A[i \ldots k] \cdot A[k+1 \ldots j]$ for $i \le k < j$ (the split law).

For $1 \le h \le K$ and $0 \le i < n$, let $b = 2^h \lfloor i / 2^h \rfloor$ and $m = b + 2^{h-1}$. The table entry is $T[h][i] = A[i \ldots m-1]$ if $i < m$ and $T[h][i] = A[m \ldots i]$ if $i \ge m$.

**Lemma 1 (build).** BUILD sets every $T[h][i]$ with $i < n$ to its definition.

*Proof.* Fix a block $[b, b + 2^h)$ with middle $m$. If $m - 1 < n$, line L7 sets $T[h][m-1] = A[m-1] = A[m-1 \ldots m-1]$. For $i = m-2$ down to $b$, if $T[h][i+1] = A[i+1 \ldots m-1]$, then line L8 sets $T[h][i] = A[i] \cdot A[i+1 \ldots m-1] = A[i \ldots m-1]$. So all of the left half is right when $m - 1 < n$. If $m - 1 \ge n$, no query reads the left half of this block, since a query of level $h$ in this block has $m \le r < n$ by Lemma 2, and these entries may hold anything. The right half is the same with $T[h][i] = A[m \ldots i-1] \cdot A[i] = A[m \ldots i]$; it stops being written at $i \ge n$, and later entries of the block are never read. $\square$

**Lemma 2 (level).** Let $0 \le l < r < N$ and let $h$ be the bit length of $l \oplus r$. Then $1 \le h \le K$, and with $b = 2^h \lfloor l / 2^h \rfloor$ and $m = b + 2^{h-1}$, we have $b \le l < m \le r < b + 2^h$.

*Proof.* $l \ne r$, so $l \oplus r \ne 0$ and $h \ge 1$; both are below $2^K$, so $h \le K$. The bits of $l$ and $r$ at positions $\ge h$ are equal, so $\lfloor l / 2^h \rfloor = \lfloor r / 2^h \rfloor$ and both lie in $[b, b + 2^h)$. Bit $h - 1$ is the highest bit where they differ, and $l < r$, so it is 0 in $l$ and 1 in $r$. Inside the block, bit $h - 1$ is 0 exactly on $[b, m)$ and 1 exactly on $[m, b + 2^h)$. $\square$

**Theorem.** QUERY$(l, r) = A[l \ldots r]$ for $0 \le l \le r < n$, with at most one operation of $S$.

*Proof.* If $l = r$, line L1 returns $A[l]$. Otherwise, by Lemma 2 with the level $h$ of line L2, $l < m \le r$, so by Lemma 1, $T[h][l] = A[l \ldots m-1]$ and $T[h][r] = A[m \ldots r]$, both with indices below $n$. By the split law, line L3 returns $A[l \ldots m-1] \cdot A[m \ldots r] = A[l \ldots r]$. $\square$

**Cost.** Each level of BUILD performs at most one operation per position $i < n$ and $2^{h-1}$ assignments without an operation per block, so at most $n$ operations per level and $nK$ in total; the table has at most $nK$ entries. A query is $O(1)$ word operations plus one operation of $S$.
