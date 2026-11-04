---
title: Dijkstra's three-way partition is correct and inspects each item exactly once
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. Let $A_0$ be the input array, of length $n \ge 0$, and $p$ the pivot value. Write $X < p$ for "every item of the range $X$ is less than $p$", and the same for $=$ and $>$; an empty range satisfies each of these.

**Claim.** THREE-WAY-PARTITION$(A, p)$ runs the loop of line L2 exactly $n$ times. On return, $A$ is a permutation of $A_0$, and the returned pair $(lt, gt)$ satisfies $A[0 \ldots lt-1] < p$, $A[lt \ldots gt-1] = p$ and $A[gt \ldots n-1] > p$.

*Proof.* We show that this invariant holds at each test of line L2:

> **(F)** $0 \le lo \le mid \le hi + 1 \le n$; $A$ is a permutation of $A_0$; $A[0 \ldots lo-1] < p$; $A[lo \ldots mid-1] = p$; $A[hi+1 \ldots n-1] > p$.

*Initialization.* Line L1 sets $lo = mid = 0$ and $hi = n - 1$. Then $0 \le 0 \le 0 \le n \le n$, $A = A_0$, and the three ranges $A[0 \ldots -1]$, $A[0 \ldots -1]$ and $A[n \ldots n-1]$ are empty.

*Maintenance.* Assume (F) and $mid \le hi$, so $0 \le mid \le n - 1$ and $A[mid]$ exists. Let $x = A[mid]$. Write primes for the values after the iteration.

- *Case $x < p$ (line L4).* If $lo < mid$, then $lo$ is in the range $[lo, mid - 1]$, so $A[lo] = p$ by (F). After the swap, $A'[lo] = x < p$ and $A'[mid] = p$. If $lo = mid$, the swap changes nothing and $A'[lo] = x < p$. In both cases the other cells do not change. Now $lo' = lo + 1$ and $mid' = mid + 1$. The range $A'[0 \ldots lo']$ minus its last cell is $A[0 \ldots lo-1] < p$, and its last cell $A'[lo] < p$, so $A'[0 \ldots lo'-1] < p$. The range $A'[lo' \ldots mid'-1] = A'[lo+1 \ldots mid]$ is the range $A[lo+1 \ldots mid-1]$, which is $= p$, plus the cell $A'[mid]$, which is $p$ when $lo < mid$; when $lo = mid$ the range is empty. The last region does not change. The bounds hold since $mid + 1 \le hi + 1$.
- *Case $x > p$ (line L6).* After the swap, $A'[hi] = x > p$, and $hi' = hi - 1$. So $A'[hi'+1 \ldots n-1] = A'[hi \ldots n-1]$ is the cell $A'[hi] > p$ followed by $A[hi+1 \ldots n-1] > p$. The cells $0 \ldots mid-1$ do not change, because $mid \le hi$ and the swap touches only $mid$ and $hi$. The bounds hold: $mid \le hi = hi' + 1$.
- *Case $x = p$ (line L7).* $mid' = mid + 1$, and $A[lo \ldots mid] = p$. Nothing else changes, and $mid + 1 \le hi + 1$.

Each case only swaps two cells, so $A'$ is still a permutation of $A_0$. So (F) holds again.

*Termination and count.* Let $u = hi - mid + 1$. By (F), $u \ge 0$, and the loop runs while $u \ge 1$. Line L4 adds 1 to $mid$, line L6 subtracts 1 from $hi$ and line L7 adds 1 to $mid$; in each case $u$ decreases by exactly 1. It starts at $n$, so the loop runs exactly $n$ times and stops with $u = 0$.

*Result.* When the loop stops, $mid = hi + 1$. Line L8 returns $lt = lo$ and $gt = hi + 1 = mid$. By (F), $A[0 \ldots lt-1] < p$, $A[lt \ldots gt-1] = A[lo \ldots mid-1] = p$, and $A[gt \ldots n-1] = A[hi+1 \ldots n-1] > p$, and $A$ is a permutation of $A_0$. $\blacksquare$

**Each item is inspected once.** The value $A[mid]$ is compared with $p$ once in each iteration. Call the cells $mid, \ldots, hi$ the unknown region. An item is compared only when it is at $mid$, inside the unknown region, and after the comparison it leaves this region in each case: by $mid + 1$ in lines L4 and L7, and by the swap to position $hi$ and $hi - 1$ in line L6. Items enter the unknown region never; the item that line L6 moves to position $mid$ was already in it. So each of the $n$ items is compared in exactly one iteration, which matches the count $n$.

**Swap count.** Line L4 runs once for each item less than $p$ and line L6 once for each item greater than $p$, since each iteration handles the item it inspects. So the number of swaps is the number of items different from $p$.
