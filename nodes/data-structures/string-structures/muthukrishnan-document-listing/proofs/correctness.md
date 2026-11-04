---
title: Muthukrishnan's listing procedure reports each document of the range once, with at most 2d + 1 range-minimum queries
proves: [correctness, complexity]
status: full
---

We use the pseudocode and the notation of the page. Fix a query with range $[lo, hi)$, and let $R = \{ r : lo \le r < hi \}$. For a document $j$ with a row in $R$, let $f_j$ be the smallest row of $R$ with $D[f_j] = j$.

**Lemma 1 (first rows).** For $r \in R$, $C[r] < lo$ if and only if $r = f_{D[r]}$.

*Proof.* By definition $C[r]$ is the largest row $r' < r$ of the same document, or $-1$. If $r = f_{D[r]}$, no row of $R$ before $r$ has document $D[r]$, so $C[r] < lo$. If $r \ne f_{D[r]}$, then $f_{D[r]}$ is a row of $R$ before $r$ with the same document, so $C[r] \ge f_{D[r]} \ge lo$. $\square$

So the documents of the answer are in bijection with the set $F = \{ r \in R : C[r] < lo \}$. By the choice of separators, a suffix starts with $p$ exactly when it is an occurrence of $p$ inside its document, so the documents with a row in $R$ are exactly the documents that contain $p$.

**Invariant of lines L5 to L8.** The intervals on the stack are pairwise disjoint subintervals of $R$; every row of $F$ is either in an interval of the stack or already reported, as $D[r]$; and no row outside $F$ has been reported.

At the start the stack holds $R$ and nothing is reported. Pop an interval $[a, b]$. If it is empty, it holds no row. Otherwise line L6 returns a row $r$ with $C[r] = \min C[a \ldots b]$. If $C[r] \ge lo$, then every row of $[a, b]$ has $C \ge lo$, so $[a, b] \cap F$ is empty and dropping it keeps the invariant. If $C[r] < lo$, then $r \in F$, and line L8 reports $D[r]$ and pushes $[a, r-1]$ and $[r+1, b]$, which are disjoint, cover $[a, b]$ except $r$, and are disjoint from the other intervals of the stack. So the invariant holds.

When the stack is empty, every row of $F$ has been reported, and only rows of $F$, each once since each row leaves the stack at most once (the intervals are disjoint and $r$ is not pushed again). By Lemma 1 and the bijection, LIST reports each document that contains $p$ exactly once.

**Number of queries.** Consider the tree of the nonempty popped intervals, where an interval that reports has the at most two nonempty intervals it pushes as children. Each reporting interval is an internal node with at most two children, and each failing interval is a leaf. A tree with $d$ internal nodes of degree at most 2 has at most $d + 1$ leaves, so there are at most $2d + 1$ nonempty intervals, and line L6 runs at most $2d + 1$ times. If $d = 0$, the one query on $R$ fails, or $R$ is empty and no query runs. With an $O(1)$ range-minimum structure, the listing time is $O(d + 1)$, and with the range found in $O(m)$ by a suffix tree, the query time is $O(m + d)$. $\blacksquare$
