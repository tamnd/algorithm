---
title: Sift-down restores the heap property in a subtree
proves: [correctness, termination]
status: full
---

The children of $j$ are $2j+1$ and $2j+2$ when they are less than $n$. Let $T(j)$ be the set of indices in the subtree of $j$. An *edge* $(q, c)$ is a pair with $c$ a child of $q$. It is *right* when $A[q] \le A[c]$. Let $i_0$ be the input index.

**Theorem.** Assume $0 \le i_0 < n$ and that each edge of $T(i_0)$ whose parent is not $i_0$ is right. Then SIFT-DOWN$(A, i_0, n)$ ends after at most $h(i_0) + 1$ iterations, where $h(i_0)$ is the number of levels below $i_0$. At the end, all edges of $T(i_0)$ are right, the items of $T(i_0)$ are a permutation of the old ones, and no cell outside $T(i_0)$ has changed.

*Proof.* We show that this invariant holds each time line L2 starts:

> **(I)** $i \in T(i_0)$. (D1) Each edge of $T(i_0)$ whose parent is not $i$ is right. (D2) If $i \ne i_0$ and $q$ is the parent of $i$, then $A[q] \le A[d]$ for each child $d$ of $i$. Only cells of $T(i_0)$ have changed, by swaps.

**Initialization.** At the first iteration, $i = i_0$. Then (D1) is the hypothesis, (D2) does not apply, and nothing has changed.

**Maintenance.** Assume (I). If line L3 or line L6 returns, we treat it under termination. Else $i$ has a child, lines L4 and L5 set $c$ to a child of $i$ with $A[c] \le A[d]$ for each child $d$ of $i$, and $A[c] < A[i]$. Write $a = A[i]$ and $b = A[c]$ before line L7, so $b < a$. After line L7, $A[i] = b$ and $A[c] = a$. We check each edge with an end at $i$ or $c$. All other edges keep both values.

1. The edge $(i, c)$: $A[i] = b < a = A[c]$, so it is right.
2. The edge $(i, s)$ to the other child $s$ of $i$, if there is one: $b \le A[s]$ by the choice of $c$, so it is right.
3. The edge $(q, i)$ from the parent $q$ of $i$, if $i \ne i_0$: by (D2), $A[q] \le b$, because $c$ is a child of $i$. So it is right. If $i = i_0$, this edge is not in $T(i_0)$, and we do not need it.
4. The edges $(c, d)$ for the children $d$ of $c$: these are the edges that (D1) for the new index $c$ leaves out.

So each edge of $T(i_0)$ whose parent is not $c$ is right, which is (D1) for $c$. For (D2) with the new index $c$, whose parent is $i$: before the swap, each edge $(c, d)$ was right by (D1), since $c \ne i$, so $b \le A[d]$. The new value at $i$ is $b$, so $A[i] \le A[d]$ for each child $d$ of $c$. A swap of two cells of $T(i_0)$ keeps the multiset of $T(i_0)$, and $c \in T(i_0)$. Line L8 sets $i \leftarrow c$, so (I) holds at the next iteration.

**Termination.** Each iteration that does not return moves $i$ to a child, so the number of levels below $i$ drops by exactly 1. The number of levels below $i_0$ is $h(i_0)$, and a node with no level below it is a leaf, at which line L3 returns. So there are at most $h(i_0)$ iterations that do not return, and one more that returns.

If line L3 returns, $i$ is a leaf, so there is no edge with parent $i$, and (D1) covers all edges of $T(i_0)$. If line L6 returns, then $A[i] \le A[c] \le A[d]$ for each child $d$ of $i$, so the edges with parent $i$ are right, and with (D1) all edges of $T(i_0)$ are right. By (I), only cells of $T(i_0)$ changed, and their items are a permutation of the old ones. $\blacksquare$

**EXTRACT-MIN.** Let $A[0 \ldots n-1]$ be a min-heap with $n \ge 1$. Line L9 saves the root, which is a smallest item because each item is reached from the root by right edges. After line L10 the heap has $n - 1$ items, and each edge whose parent is not $0$ joins two cells that did not change, so it is right. If $n - 1 > 0$, the theorem with $i_0 = 0$ makes the whole array a min-heap. The items are the old items less one copy of the returned minimum.

**Increase-key.** If $A$ is a min-heap and the value at $i$ grows, each edge of $T(i)$ whose parent is not $i$ keeps both values, so the theorem applies to $T(i)$. The edge from the parent $q$ of $i$ stays right: the final value at $i$ is the new value, which is larger than the old one, or a value from $T(i)$, which was at least the old $A[i] \ge A[q]$.

**Floyd's construction.** Call SIFT-DOWN$(A, i, n)$ for $i = \lfloor n/2 \rfloor - 1, \ldots, 0$. Claim: after the call for $i$, the subtrees of $i, i+1, \ldots, n-1$ are min-heaps. The indices $j \ge \lfloor n/2 \rfloor$ are leaves, so the claim holds before the first call. When the call for $i$ starts, its children are larger indices, so their subtrees are heaps, which is the hypothesis of the theorem. The call changes only cells of $T(i)$, and for $j > i$ the subtree $T(j)$ is either inside $T(i)$, where the call leaves all edges right, or disjoint from it, where nothing changes. So the claim holds after the call, and after the call for $0$ the whole array is a heap.
