---
title: Pigeonhole sort sorts the items and is stable
proves: [correctness, stability, termination]
status: full
---

Let $n \ge 1$ (for $n = 0$ line L1 returns, and the empty array is sorted). Let $\kappa_i = \mathrm{key}(A[i])$ for the input array, $lo = \min_i \kappa_i$, $hi = \max_i \kappa_i$ and $k = hi - lo + 1 \ge 1$.

**Step 1 (the holes exist).** For each $i$, $lo \le \kappa_i \le hi$, so $0 \le \kappa_i - lo \le k - 1$. So line L6 appends to one of the $k$ holes made by line L4.

**Step 2 (the scatter).** At the test of line L5 with index $i$, for each $h$, the hole $H[h]$ holds the items $A[j]$ with $j < i$ and $\kappa_j = lo + h$, in increasing order of $j$. For $i = 0$ all holes are empty. Step $i$ appends $A[i]$ at the end of $H[\kappa_i - lo]$ and changes no other hole, so the claim holds for $i + 1$. At $i = n$, hole $h$ holds all items with key $lo + h$, in input order. The array $A$ is not written in this loop, so it still holds the input.

**Step 3 (the gather).** At the start of the step of line L8 with index $h$, $j = |H[0]| + \cdots + |H[h-1]|$, and $A[0 \ldots j-1]$ holds the items of $H[0], \ldots, H[h-1]$, each hole in its order, one hole after the other. For $h = 0$, $j = 0$ by line L7. The loop of lines L9 and L10 writes the $|H[h]|$ items of $H[h]$ to $A[j], A[j+1], \ldots$ in order and adds $|H[h]|$ to $j$, so the claim holds for $h + 1$. The writes do not lose data, because all items are in the holes after Step 2.

**Step 4 (the result).** At the end, $h = k$ and $j = \sum_h |H[h]| = n$. So $A$ holds each input item exactly once. Its keys are non-decreasing, because the holes are written in increasing order of $h$ and hole $h$ holds only the key $lo + h$. Two items with the same key are in the same hole, in input order by Step 2, and they are written in that order. So the sort is stable. $\blacksquare$

**Termination.** Each loop has a fixed number of steps: $n$ for line L5, $k$ for line L8, and $|H[h]|$ for line L9, with $\sum_h |H[h]| = n$.
