---
title: Proxmap sort sorts its input and is stable
proves: [correctness, stability]
status: full
---

Let $M$ be non-decreasing with values in $\{0, \ldots, m - 1\}$. Let $H[k]$ be the hit counts of line L1, $P[k] = H[0] + \cdots + H[k-1]$, and $E[k] = P[k] + H[k]$. The ranges $S_k = [P[k], E[k])$ are disjoint, in the order of $k$, and cover $[0, n)$, because $E[k] = P[k + 1]$ and $E[m-1] = n$.

**Invariant.** Before iteration $i$ of line L4, for each $k$: $0 \le F[k] \le H[k]$; the cells $B[P[k] \ldots P[k] + F[k] - 1]$ hold the $F[k]$ keys among $A[0 \ldots i-1]$ with $M(\cdot) = k$, in non-decreasing order, with equal keys in input order; and the other cells of $S_k$ are empty.

*Initialization.* $F[k] = 0$ and $B$ is empty, so the invariant holds for $i = 0$.

*Maintenance.* Let $x = A[i]$ and $k = M(x)$. The keys of $A[0 \ldots i - 1]$ with class $k$ number $F[k]$, and $x$ is one more key of class $k$, so $F[k] + 1 \le H[k]$ and the cell $j = P[k] + F[k]$ of line L5 lies in $S_k$; it is empty by the invariant. Line L6 moves $j$ down while $j > P[k]$ and $B[j - 1] > x$, and each move shifts $B[j - 1]$ one cell right into the empty cell $j$. This is one step of insertion sort on the sorted run $B[P[k] \ldots P[k] + F[k] - 1]$: when the loop stops, every key in $B[j + 1 \ldots P[k] + F[k]]$ is greater than $x$, and $j = P[k]$ or $B[j - 1] \le x$. Line L7 puts $x$ at $j$. The run is then sorted and has length $F[k] + 1$. Equal keys keep input order, since $x$ comes after all earlier keys in input order and it does not pass a key that is equal to it. No cell outside $S_k$ is read or written, because $j \ge P[k]$ at all times. With $F[k]$ increased in line L5, the invariant holds for $i + 1$.

**After the loop.** With $i = n$, each $F[k]$ equals $H[k]$, so each $S_k$ is full and holds the keys of class $k$ in sorted, stable order. Take two cells $p < q$. If they are in the same $S_k$, then $B[p] \le B[q]$. If $p \in S_k$ and $q \in S_{k'}$ with $k < k'$, then $M(B[p]) = k < k' = M(B[q])$, and since $M$ is non-decreasing, $B[p] > B[q]$ is impossible, so $B[p] \le B[q]$. Two equal keys have the same class, so they are in the same $S_k$ and in input order. Line L8 copies $B$ to $A$. $\blacksquare$
