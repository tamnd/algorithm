---
title: The Li Chao tree keeps a lowest line on every root path
proves: [correctness, complexity]
status: full
---

The domain is the index range $[0, C)$ with $C \ge 1$; a line is a function $f(i) = a x_i + b$ of the index, and for two lines $f, g$ the difference $f - g$ is a linear function of $x_i$, so it is monotone in $i$. For a node $v$ over $[lo, hi)$ write $P(i)$ for the path from the root to the leaf of $i$.

**Invariant (LC).** (a) If a node holds no line, none of its descendants holds one. (b) For every inserted line $f$ and every index $i$, some line $g$ stored on $P(i)$ has $g(i) \le f(i)$.

**Lemma 1 (one step).** Let $g$ and $f$ be the node line and the carried line at a node over $[lo, hi)$ after line L5, so $g(mid) \le f(mid)$.

1. If the walk stops at line L9, then $g(i) \le f(i)$ for all $i \in [lo, hi)$.
2. If it goes left at line L7, then $g(i) \le f(i)$ for all $i \in [mid, hi)$.
3. If it goes right at line L8, then $g(i) \le f(i)$ for all $i \in [lo, mid]$.

*Proof.* Let $d = f - g$, monotone in $i$. (1) $d(lo) \ge 0$ and $d(hi - 1) \ge 0$, so $d \ge 0$ between them. (2) $d(lo) < 0 \le d(mid)$, so $d$ is non-decreasing, and $d(i) \ge d(mid) \ge 0$ for $i \ge mid$. (3) $d(lo) \ge 0$ and $d(mid) \ge 0$, so $d \ge 0$ on $[lo, mid]$. $\square$

**Lemma 2 (INSERT keeps (LC)).** After INSERT$(f_0)$, (LC) holds for the old lines and $f_0$.

*Proof.* (a) INSERT places a line only at the first empty node of its path, whose parent holds a line, and it never empties a node. For (b), consider the walk, with the carried line $c_t$ at the $t$-th node $v_t$. The lines that are "in flight" are those stored in the nodes and the carried line. We show the claim: after each step, for each line $h$ that is stored or carried at the start of the step and each index $i$, either some stored line on $P(i)$ is $\le h$ at $i$, or $i$ lies in the range of the next node and the carried line is $\le h$ at $i$.

At a swap on line L5 the two lines change places, so both are still stored or carried, at the same node. Then by Lemma 1, at the indices of $[lo, hi)$ that the walk leaves behind, the stored line $g$ is at most the carried line, and $g$ lies on $P(i)$ for all of them. Indices outside $[lo, hi)$ are not affected: the carried line was carried into this node only for indices of its range. When the walk ends at line L3, the carried line is stored at a node whose range contains all its remaining indices. At line L6 the range has one index, which is $mid$, where $g \le f$ after line L5. Lines stored below the path are not moved. By induction over the steps, every line, old or new, is covered on every index. $\square$

**Theorem.** QUERY$(i)$ returns $\min_f f(i)$ over all inserted lines, or $+\infty$ if there are none.

*Proof.* QUERY reads the stored lines on $P(i)$ from the root down; by (a) it can stop at the first empty node, since none below holds a line. Every value it takes is the value of an inserted line, so the result is at least the minimum. By (b), for the line $f^*$ that attains the minimum at $i$, some stored line on $P(i)$ is at most $f^*(i)$, so the result is at most the minimum. $\square$

**Cost.** The tree over $[0, C)$ has at most $\lceil \lg C \rceil + 1$ levels. INSERT and QUERY visit one node per level and evaluate at most four lines per node, so both take $O(\log C)$ time. Each INSERT fills at most one empty node, so at most $\min(n, 2C - 1)$ nodes hold lines.
