---
title: HEAP-DELETE removes the key at index i and leaves a max-heap
proves: [correctness, termination]
status: full
---

Write $s$ for $A.\mathit{heap\text{-}size}$ after line L4, so $s = n - 1$, and $p(j) = \lfloor j/2 \rfloor$. An *edge* is a pair $(p(j), j)$ with $2 \le j \le s$, and it *holds* when $A[p(j)] \ge A[j]$. Let $C(i)$ be the set of children of $i$ with index at most $s$.

We use two lemmas whose proofs are on other pages, for a max-heap in place of a min-heap.

- **Lemma U (sift-up).** If each edge $(p(j), j)$ with $j \ne i$ holds, and, when $i \ge 2$, $A[p(i)] \ge A[c]$ for each $c \in C(i)$, then SIFT-UP$(A, i)$ stops after at most $\lfloor \lg i \rfloor$ swaps and afterwards each edge holds. This is the invariant proof of [heap increase-key](/heap-increase-key/), whose loop is lines L9 to L11.
- **Lemma D (sift-down).** If each edge $(p(j), j)$ with $p(j) \ne i$ holds, and, when $i \ge 2$, $A[p(i)] \ge A[c]$ for each $c \in C(i)$, then MAX-HEAPIFY$(A, i)$ stops after at most $\lfloor \lg(s/i) \rfloor$ swaps and afterwards each edge holds. This is the lemma of [heap extract-max](/heap-extract-max/), whose loop is lines L12 to L17.

Both only swap keys.

**Theorem.** Let $A[1 \ldots n]$ be a max-heap and $1 \le i \le n$. Then HEAP-DELETE$(A, i)$ returns the old $A[i]$, and afterwards $A[1 \ldots n - 1]$ is a max-heap whose multiset of keys is the old one with one copy of the old $A[i]$ removed. It stops. An index out of range gives an error.

*Proof.* Line L1 handles a bad index. Let $x$ be the old $A[i]$ and $y$ the old $A[n]$. Lines L2 to L4 save $x$, write $y$ into the cell $i$ and set $s = n - 1$. The keys of $A[1 \ldots s]$ are now the old keys with one copy of $x$ removed: if $i = n$, the cell $n$ was dropped; else the cell $i$ lost $x$ and got $y$, and the cell $n$, which held $y$, was dropped.

*Case $i = n$.* Then $i > s$, line L5 skips the repair, and $A[1 \ldots s]$ is the old heap without its last cell. Each of its edges is an old edge, so it holds.

*Case $i \le s$.* Each edge with no end at $i$ joins two unchanged cells, so it holds. The edges with an end at $i$ are $(p(i), i)$ when $i \ge 2$, and $(i, c)$ for $c \in C(i)$. For each $c \in C(i)$ we have $A[c] \le x$, because the edge $(i, c)$ held before, and if $i \ge 2$, then $x \le A[p(i)]$, because the edge $(p(i), i)$ held before.

- *Sub-case: line L6 calls SIFT-UP*, so $i \ge 2$ and $A[p(i)] < y$. Then for each $c \in C(i)$, $A[c] \le x \le A[p(i)] < y$, so each edge $(i, c)$ holds. Each edge $(p(j), j)$ with $j \ne i$ holds, and $A[p(i)] \ge x \ge A[c]$ for each $c \in C(i)$. So the hypothesis of Lemma U holds, and afterwards each edge holds.
- *Sub-case: line L7 calls MAX-HEAPIFY*, so $i = 1$ or $A[p(i)] \ge y$. Then the edge $(p(i), i)$ holds if $i \ge 2$, and each edge with $p(j) \ne i$ holds. If $i \ge 2$, $A[p(i)] \ge x \ge A[c]$ for each $c \in C(i)$. So the hypothesis of Lemma D holds, and afterwards each edge holds.

In each case the sift only swaps, so the multiset of keys stays the one above, and the sift stops by its lemma. Line L8 returns $x$. $\blacksquare$
