---
title: Sift-up restores the heap property
proves: [correctness, termination]
status: full
---

Write $\text{par}(j) = \lfloor (j-1)/2 \rfloor$ for $j \ge 1$. An *edge* is a pair $(\text{par}(c), c)$ with $1 \le c < n$. The edge is *right* when $A[\text{par}(c)] \le A[c]$. The array is a min-heap when all edges are right.

**Theorem.** Let $A[0 \ldots n-1]$ and $0 \le i < n$ satisfy (H1) every edge $(\text{par}(c), c)$ with $c \ne i$ is right, and (H2) if $i \ge 1$, then $A[\text{par}(i)] \le A[c]$ for each child $c$ of $i$. Then SIFT-UP$(A, i)$ ends after at most $\lfloor \lg(i+1) \rfloor$ iterations. At the end, $A$ is a min-heap, it is a permutation of the input, and only the cells on the path from the input $i$ to the root have changed.

*Proof.* We show that this invariant holds before each test of line L1:

> **(I)** (H1) and (H2) hold for the current value of $i$. The array is a permutation of the input, and each changed cell is on the path from the input index to the root.

**Initialization.** Before the first test, (I) is the hypothesis of the theorem, and no cell has changed.

**Maintenance.** Assume (I) and $i > 0$. Line L2 sets $p = \text{par}(i)$. If line L3 finds $A[p] \le A[i]$, the procedure returns; we treat that case under termination. Else $A[p] > A[i]$. Write $a = A[i]$ and $b = A[p]$ before line L4, so $a < b$. After line L4, $A[p] = a$ and $A[i] = b$. We check each edge that has $p$ or $i$ as an end. All other edges keep both values, so they stay as they were.

1. The edge $(p, i)$: $A[p] = a < b = A[i]$, so it is right.
2. An edge $(i, c)$ for a child $c$ of $i$: before the swap, (H2) gave $b = A[\text{par}(i)] \le A[c]$. Now $A[i] = b$, so the edge is right.
3. The edge $(p, s)$ for the other child $s$ of $p$, if it exists: before the swap the edge was right by (H1), because $s \ne i$, so $b \le A[s]$. Now $A[p] = a < b \le A[s]$, so it is right.
4. The edge $(\text{par}(p), p)$, if $p \ge 1$: this is the one edge that (H1) for the new index $p$ leaves out.

So each edge whose child is not $p$ is right, which is (H1) for $p$. For (H2) with $p \ge 1$: the edge $(\text{par}(p), p)$ was right before the swap by (H1), because $p \ne i$, so $A[\text{par}(p)] \le b$. The children of $p$ are now $i$, with value $b$, and $s$, with $A[s] \ge b$ by step 3. Both are at least $A[\text{par}(p)]$, which did not change. So (H2) holds for $p$. A swap keeps the multiset of the items, and $p$ is on the path from the input index to the root. Line L5 sets $i \leftarrow p$, so (I) holds before the next test.

**Termination.** Each iteration that does not return replaces $i$ by $\text{par}(i)$. For $j \ge 1$, $\lfloor \lg(\text{par}(j)+1) \rfloor = \lfloor \lg(j+1) \rfloor - 1$, because $\text{par}(j) + 1 = \lfloor (j+1)/2 \rfloor$. So the depth $\lfloor \lg(i+1) \rfloor$ drops by exactly 1 in each such iteration, and it is never negative. Hence there are at most $\lfloor \lg(i+1) \rfloor$ iterations, counted from the input $i$.

The procedure stops in one of two ways. At line L3, $A[\text{par}(i)] \le A[i]$, so the edge that (H1) leaves out is right too, and all edges are right. At line L1 with $i = 0$, no edge has the child $0$, so (H1) already covers all edges. In both cases $A$ is a min-heap, and by (I) it is a permutation of the input that changed only on the path. $\blacksquare$

**HEAP-INSERT.** Before line L7, all edges of $A[0 \ldots n-1]$ are right. After line L7 the new index $n$ has no children, and all edges except $(\text{par}(n), n)$ are old edges. So (H1) and (H2) hold for $i = n$, and the theorem applies to the call of line L8.

**Decrease-key.** If $A$ is a min-heap and the value at $i$ is lowered from $b$ to $a \le b$, then each edge $(i, c)$ stays right, because $a \le b \le A[c]$, and $A[\text{par}(i)] \le b \le A[c]$ gives (H2). So the theorem applies to SIFT-UP$(A, i)$.
