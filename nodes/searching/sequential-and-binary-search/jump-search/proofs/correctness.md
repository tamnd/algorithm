---
title: Jump search returns the first index of x, or NIL when x is not in A
proves: [correctness, termination]
status: full
---

Let $A[0 \ldots n-1]$ be sorted in non-decreasing order, $n \ge 0$, and let $x$ be a key. Let $\ell = |\{\, j : A[j] < x \,\}|$ be the lower bound of $x$. Because $A$ is sorted, $A[j] < x$ for $j < \ell$ and $A[j] \ge x$ for $\ell \le j < n$. We prove that JUMP-SEARCH$(A, x)$ stops and returns $\ell$ when $\ell < n$ and $A[\ell] = x$, and NIL otherwise. This is the smallest index of $x$ when $x$ is present, since the copies of $x$ are exactly the indices $j \ge \ell$ with $A[j] = x$, and they start at $\ell$ when there are any.

**Invariant of the jump loop.** Before each test of line L3:

1. $0 \le lo \le hi \le n$ and $hi - lo \le m$, where $m \ge 1$ is the value of line L1.
2. $A[j] < x$ for each $j < lo$, that is, $lo \le \ell$.
3. $hi = n$ or $hi = lo + m$.

*Start.* Line L2 sets $lo = 0$ and $hi = \min(m, n)$. Then $0 \le lo \le hi \le n$, $hi - lo \le m$, statement 2 is empty, and statement 3 holds.

*Step.* The body runs only when $hi < n$ and $A[hi - 1] < x$. Since $A$ is sorted, $A[j] \le A[hi - 1] < x$ for each $j < hi$. Line L4 sets $lo' = hi$ and $hi' = \min(hi + m, n)$. Then statement 2 holds for $lo'$. Also $lo' = hi < n$ gives $lo' \le hi' \le n$ and $hi' - lo' \le m$, and $hi'$ is $n$ or $lo' + m$.

*Exit.* The loop stops when $hi = n$ or $A[hi - 1] \ge x$. In the first case $\ell \le n = hi$. In the second case $hi \ge 1$ and $A[hi - 1] \ge x$, so $\ell \le hi - 1 < hi$. In both cases, with statement 2,

$$ lo \le \ell \le hi. $$

**Termination of the jump loop.** Each pass makes $hi' - hi = \min(m, n - hi) \ge 1$, since $m \ge 1$ and $hi < n$. So $hi$ grows by at least 1 in each pass and never passes $n$, and there are at most $n$ passes. More exactly, while $hi < n$, statement 3 gives $hi = lo + m$, so $hi$ grows by $m$ in each pass but the last, and there are at most $\lceil n/m \rceil - 1$ passes.

**The scan.** Line L5 sets $i = lo$. Before each test of line L6, $lo \le i \le \ell$ and $i \le hi$. This holds at the start by the exit statement. A pass runs only when $i < hi$ and $A[i] < x$, which means $i < \ell$; so the new $i + 1$ satisfies $i + 1 \le \ell$ and $i + 1 \le hi$. Each pass increases $i$ by 1 and $i \le hi \le n$, so the scan stops. When it stops, either $i = hi$, and then $\ell \le hi = i \le \ell$; or $A[i] \ge x$ with $i < hi \le n$, and then $i \ge \ell$ by the definition of $\ell$. In both cases $i = \ell$.

**Result.** Line L8 runs with $i = \ell$. If $\ell < n$ and $A[\ell] = x$, it returns $\ell$, the smallest index of $x$. Otherwise $x$ is absent: if $\ell = n$ then every item is less than $x$, and if $A[\ell] > x$ then every $j \ge \ell$ has $A[j] \ge A[\ell] > x$ and every $j < \ell$ has $A[j] < x$. So line L9 returns NIL correctly. $\blacksquare$

**The number of comparisons.** The jump loop tests $A[hi - 1]$ only while $hi < n$, and by the termination argument this happens at most $\lceil n/m \rceil - 1$ times. The scan compares at most $hi - lo \le m$ items. Line L8 makes at most one comparison. So the total is at most $\lceil n/m \rceil + m$.
