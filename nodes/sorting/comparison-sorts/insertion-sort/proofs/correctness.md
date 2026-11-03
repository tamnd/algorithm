---
title: Insertion sort sorts the array and keeps its items
proves: [correctness]
status: full
---

Let $A_0$ be the array at the start. We prove the invariant of the outer loop:

> **(I)** Before the step for $i$, the part $A[0 \ldots i-1]$ is a permutation of $A_0[0 \ldots i-1]$ in non-decreasing order, and $A[i \ldots n-1] = A_0[i \ldots n-1]$.

**Start.** For $i = 1$, the part $A[0 \ldots 0]$ has one item, so it is sorted. No item has moved yet.

**Step.** Assume (I) before the step for $i$. Line L2 sets $key = A[i] = A_0[i]$. For the inner loop we use this invariant:

> **(J)** $-1 \le j \le i-1$. The part $A[0 \ldots j]$ is not changed. The part $A[j+2 \ldots i]$ is the old $A[j+1 \ldots i-1]$, moved one place right. Each item of $A[j+2 \ldots i]$ is larger than $key$.

Before the first test of line L4, $j = i - 1$ and $A[j+2 \ldots i]$ is empty, so (J) is true. If the test of line L4 is true, then $A[j] > key$. Line L5 copies $A[j]$ to $A[j+1]$, and line L6 makes $j$ one less. So (J) is true again. The value $j$ becomes smaller in each step and $j \ge -1$, so the inner loop stops.

When the inner loop stops, $j = -1$ or $A[j] \le key$. Line L7 puts $key$ at $A[j+1]$. Now:

- each item of $A[0 \ldots j]$ is at most $key$, because the old part was sorted and $A[j] \le key$, or the part is empty;
- $A[j+1] = key$;
- each item of $A[j+2 \ldots i]$ is larger than $key$, by (J), and these items are in the old order.

So $A[0 \ldots i]$ is sorted. It holds the old $A[0 \ldots i-1]$ and $A_0[i]$, so it is a permutation of $A_0[0 \ldots i]$. The items after $i$ did not change. This is (I) for $i + 1$.

**End.** The loop stops with $i = n$. By (I), $A[0 \ldots n-1]$ is a permutation of $A_0$ in non-decreasing order. $\blacksquare$

**Stability.** An item moves right in line L5 only past an item that is larger than $key$. So $key$ never moves before an item that is equal to it and that was before it in $A_0$.
