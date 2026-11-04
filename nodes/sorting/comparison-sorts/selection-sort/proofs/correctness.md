---
title: Selection sort sorts the array and keeps its items
proves: [correctness]
status: full
---

Let $A_0$ be the input array of length $n$. Items may repeat, so we treat each collection of items as a multiset.

**Theorem.** SELECTION-SORT stops, and at the end $A$ is a permutation of $A_0$ in non-decreasing order.

*Proof.* We use this invariant of the loop of line L1, before the step for $i$:

> **(I)** $A$ is a permutation of $A_0$. The part $A[0 \ldots i-1]$ is sorted. Each item of $A[0 \ldots i-1]$ is at most each item of $A[i \ldots n-1]$.

*Start.* For $i = 0$ the part $A[0 \ldots -1]$ is empty, so the last two statements hold, and no item has moved.

*The scan.* Fix a step $i \le n - 2$. For the loop of line L3 we use this invariant, before the step for $j$:

> **(J)** $i \le m \le j - 1$, and $A[m]$ is at most each item of $A[i \ldots j-1]$.

Line L2 sets $m = i$, and the first step has $j = i + 1$. The part $A[i \ldots i]$ has the one item $A[m]$, so (J) holds. In the step for $j$, if $A[j] < A[m]$, line L5 sets $m = j$. Then $A[m]$ is less than the old least item, so it is at most each item of $A[i \ldots j]$. Otherwise $A[m] \le A[j]$, and $A[m]$ is still at most each item of $A[i \ldots j]$. So (J) holds for $j + 1$. The loop runs for $j = i + 1, \ldots, n - 1$ and stops with $j = n$. Then $A[m]$ is a least item of $A[i \ldots n-1]$, and $i \le m \le n - 1$. Lines L2 to L5 do not write to $A$.

*Maintenance.* Assume (I) before the step for $i \le n - 2$, and let $y = A[m]$ at the end of the scan. Line L6 swaps $A[i]$ and $A[m]$, so $A$ is still a permutation of $A_0$. Now $A[i] = y$. Each item of the old $A[0 \ldots i-1]$ is at most $y$, by (I), because $y$ was in $A[i \ldots n-1]$. So $A[0 \ldots i]$ is sorted. The new part $A[i+1 \ldots n-1]$ holds the items of the old $A[i \ldots n-1]$ without one copy of $y$. Each of these items is at least $y$, by the scan, and at least each item of $A[0 \ldots i-1]$, by (I). So (I) holds for $i + 1$.

*End.* The loop of line L1 runs for $i = 0, \ldots, n - 2$, a finite range, so the algorithm stops. If $n \le 1$, the loop does not run, and an array of at most one item is sorted. If $n \ge 2$, (I) holds for $i = n - 1$. Then $A[0 \ldots n-2]$ is sorted, and each of its items is at most $A[n-1]$. So $A[0 \ldots n-1]$ is sorted, and by (I) it is a permutation of $A_0$. $\blacksquare$

**Comparisons.** The scan for $i$ makes one comparison for each $j$ from $i + 1$ to $n - 1$, so $n - 1 - i$ comparisons. No other line compares items. The sum over $i = 0, \ldots, n - 2$ is $(n-1) + (n-2) + \cdots + 1 = n(n-1)/2$, on each input.
