---
title: The sort-and-scan 3SUM algorithm reports each solution exactly once
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. After line L1, $A[0] \le A[1] \le \cdots \le A[n-1]$ is the sorted input. A *solution* is a value triple $(x, y, z)$ with $x \le y \le z$, $x + y + z = t$, such that there are positions $i < p < q$ of $A$ with $(A[i], A[p], A[q]) = (x, y, z)$. Since $A$ holds the same multiset of values as the input, this is the same set of solutions as for the input list.

**Claim.** THREE-SUM$(v, t)$ terminates, and it reports each solution exactly once and nothing else.

## Step 1: one sweep

Fix an $i$ that line L3 does not skip, and let $x = A[i]$ and $r = t - x$. Call a value pair $(y, z)$ *good* if $y \le z$, $y + z = r$, and there are positions $i < p < q$ with $A[p] = y$ and $A[q] = z$. We show that the sweep (lines L4 to L11) reports each good pair exactly once and nothing else.

Write $G$ for the set of good pairs that are not yet reported. We use this invariant at each test of line L5:

> **(Q)** $i + 1 \le lo$ and $hi \le n - 1$. (a) Each $(y, z) \in G$ has positions $p < q$ with $lo \le p < q \le hi$, $A[p] = y$ and $A[q] = z$. (b) Each pair $(y, z)$ already reported in this sweep is good, and if $lo \le hi$ it has $y < A[lo]$ and $z > A[hi]$.

*Initialization.* Line L4 sets $lo = i + 1$ and $hi = n - 1$. Nothing is reported, so $G$ is the set of all good pairs, and by definition each of them has positions $p, q$ with $i < p < q \le n - 1$. So (a) holds, and (b) holds with nothing to check.

*Maintenance.* Assume (Q) and $lo < hi$. Line L6 sets $s = x + A[lo] + A[hi]$.

- *Case $s < t$ (line L7).* Then $A[lo] + A[hi] < r$. For each $q$ with $lo < q \le hi$, $A[lo] + A[q] \le A[lo] + A[hi] < r$, so no pair of positions in $[lo, hi]$ with first position $lo$ gives a good pair. So the positions of (a) have $p \ge lo + 1$, and (a) holds for the new $lo$. Part (b) holds because $A[lo + 1] \ge A[lo]$ and $hi$ does not change.
- *Case $s > t$ (line L8).* Then $A[lo] + A[hi] > r$. For each $p$ with $lo \le p < hi$, $A[p] + A[hi] \ge A[lo] + A[hi] > r$. So the positions of (a) have $q \le hi - 1$, and (a) holds for the new $hi$. Part (b) holds because $A[hi - 1] \le A[hi]$.
- *Case $s = t$ (lines L9 to L11).* Let $y_0 = A[lo]$ and $z_0 = A[hi]$. Then $y_0 \le z_0$, $y_0 + z_0 = r$, and the positions $i < lo < hi$ show that $(y_0, z_0)$ is good. By (b), each pair reported before has $y < A[lo] = y_0$, so $(y_0, z_0)$ was not reported before: line L9 reports it for the first time, and it leaves $G$.

  Now take any $(y, z) \in G$ after this report, with positions $lo \le p < q \le hi$ from (a). Then $(y, z) \ne (y_0, z_0)$. If $y = y_0$ then $z = r - y = z_0$, which is not possible, so $y \ne y_0$. If $y < y_0$, then $A[p] < A[lo]$ with $p \ge lo$, which contradicts the sorted order. So $y > y_0$, and then $z = r - y < r - y_0 = z_0$.

  Line L10 sets $lo$ to $lo + 1$ and then moves it right while $lo < hi$ and $A[lo] = A[lo - 1]$. Every position that it passes over holds the value $y_0$. Since $A[p] = y > y_0$, position $p$ is not passed over, unless the loop stops early because $lo = hi$; we treat that below. Line L11 does the same for $hi$ with the value $z_0$, and position $q$, with $A[q] = z < z_0$, is not passed over. So if the loops stop because the next value differs, the new range still contains $p$ and $q$, and (a) holds.

  If a loop stops because $lo = hi$, then all positions from the old $lo$ to the current one hold $y_0$ (or all positions from the current $hi$ to the old one hold $z_0$). Every remaining pair $p < q$ of the old range then has $A[p] = y_0$ or $A[q] = z_0$; by the paragraph above, no pair of $G$ has this, so $G$ is empty and (a) holds trivially.

  For (b): after line L10, either $lo \ge hi$, or $A[lo] \ne y_0$ and so $A[lo] > y_0$, which is at least as large as each $y$ reported so far. After line L11, in the same way, $A[hi] < z_0$ or $lo \ge hi$. Each earlier reported pair had $z > $ the old $A[hi] = z_0$, so all reported pairs have $z > A[hi]$.

*Termination of the sweep.* Each iteration decreases $hi - lo$ by at least 1: lines L7 and L8 by exactly 1, lines L10 and L11 by at least 2. The value starts at $n - 2 - i$, and the loop runs only while it is at least 1. So the sweep stops after at most $n - 2 - i$ iterations.

*End of the sweep.* When the loop stops, $lo \ge hi$, so no pair of positions $lo \le p < q \le hi$ exists, and by (a) the set $G$ is empty: every good pair has been reported. By (b), and since each pair is reported only in the case where it was not reported before, no good pair is reported twice, and every reported pair is good.

## Step 2: the outer loop

Let $(x, y, z)$ be a solution, with positions $i < p < q$. Let $i_0$ be the smallest position with $A[i_0] = x$. Then $i_0 \le i < p < q$, so $(y, z)$ is a good pair for $i_0$. Position $i_0$ is not skipped by line L3, because $i_0 = 0$ or $A[i_0 - 1] < x$. Also $i_0 \le n - 3$, since $q \le n - 1$ and $i_0 < p < q$. By Step 1, the sweep for $i_0$ reports $(x, y, z)$.

The sweeps that line L3 does not skip are exactly the first positions of the distinct values of $A$, so no two of them have the same $x$. Each sweep reports its good pairs once, with its own $x$. So each solution is reported exactly once, and each reported triple is a solution by Step 1.

The outer loop runs $\max(n - 2, 0)$ times and each sweep terminates, so the algorithm terminates. $\blacksquare$

**Cost.** By the termination argument, the total number of iterations of line L5 is at most $\sum_{i=0}^{n-3}(n - 2 - i) = \frac{(n-1)(n-2)}{2}$, and each costs $O(1)$ besides the inner while loops of lines L10 and L11, whose steps are counted in the decrease of $hi - lo$. So the time after the sort is $O(n^2)$.
