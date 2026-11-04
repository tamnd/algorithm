---
title: Pancake sort sorts the array with prefix reversals
proves: [correctness]
status: full
---

FLIP$(A, m)$ reverses $A[0 \ldots m]$. It permutes the items of $A[0 \ldots m]$ and changes no other index. So each step of the algorithm keeps the multiset of the items of the array.

**Invariant.** Before the step of line L1 for $k$, with $2 \le k \le n$, and also when the loop ends with $k = 1$:

> **(S)** $A[k \ldots n-1]$ is sorted, and each item of $A[0 \ldots k-1]$ is at most each item of $A[k \ldots n-1]$.

*Start.* For $k = n$ the part $A[n \ldots n-1]$ is empty, so (S) holds.

*Step.* Assume (S) before the step for $k \ge 2$. Line L2 sets $m$ to the index of a largest item $x$ of $A[0 \ldots k-1]$, so $0 \le m \le k - 1$.

- If $m = k - 1$, nothing changes, and $x = A[k-1]$.
- If $m = 0$, line L4 is skipped, and line L5 reverses $A[0 \ldots k-1]$, which moves $A[0] = x$ to index $k - 1$.
- If $0 < m < k - 1$, line L4 reverses $A[0 \ldots m]$, which moves $x$ to index 0 and keeps the items of $A[0 \ldots k-1]$, since $m < k$. Then line L5 moves $x$ to index $k - 1$.

In each case, the flips are of prefixes that end at an index less than $k$, so $A[k \ldots n-1]$ does not change, and $A[0 \ldots k-1]$ holds the same items as before, with $A[k-1] = x$. Since $x$ is a largest item of this prefix, each item of $A[0 \ldots k-2]$ is at most $x$. By (S), $x$ is at most each item of $A[k \ldots n-1]$, so $A[k-1 \ldots n-1]$ is sorted. Each item of $A[0 \ldots k-2]$ was in $A[0 \ldots k-1]$, so it is at most each item of $A[k \ldots n-1]$, and at most $x$. So (S) holds for $k - 1$.

**Theorem.** PANCAKE-SORT$(A)$ stops, changes $A$ only by prefix reversals, and leaves $A$ sorted, with the same items.

*Proof.* The loop runs for $k = n, n-1, \ldots, 2$, and each step does a scan of $k - 1$ items and at most two flips, so the algorithm stops. All changes are flips, so the items are kept. If $n \le 1$, the loop does not run, and the array is sorted. Otherwise, at the end (S) holds for $k = 1$: $A[1 \ldots n-1]$ is sorted, and $A[0]$ is at most each of its items. So $A$ is sorted. $\blacksquare$

**The number of flips.** Each step makes at most 2 flips, and the step for $k = 2$ makes at most one, because then $m \in \{0, 1\}$: for $m = 1$ there is no flip, and for $m = 0$ only line L5 runs. So for $n \ge 2$ there are at most $2(n - 2) + 1 = 2n - 3$ flips.
