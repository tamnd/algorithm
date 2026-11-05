---
title: Exponential search returns the first index of x, or NIL, with at most 2 floor(lg l) + 3 comparisons
proves: [correctness, termination, complexity]
status: full
---

Let $A[0 \ldots n-1]$ be sorted in non-decreasing order, $n \ge 0$, and let $x$ be a key. Let $\ell = |\{\, j : A[j] < x \,\}|$ be the lower bound of $x$. Because $A$ is sorted, $A[j] < x$ exactly for $j < \ell$. The copies of $x$, if any, are at the indices $\ell, \ell + 1, \ldots$, so the answer is $\ell$ when $\ell < n$ and $A[\ell] = x$, and NIL otherwise.

**The doubling loop.** Before each test of line L2:

1. $b = 2^k$ for an integer $k \ge 0$;
2. $A[j] < x$ for each $j < \lfloor b/2 \rfloor$, that is, $\lfloor b/2 \rfloor \le \ell$;
3. $b \le \ell$ when $b \ge 2$, that is, the test at $b/2$ passed.

At the start $b = 1$, $\lfloor b/2 \rfloor = 0$, and statements 2 and 3 say nothing. A pass runs only when $b \le n$ and $A[b - 1] < x$, so $b - 1 < \ell$ and $b \le \ell$. For the new value $b' = 2b$ we get $\lfloor b'/2 \rfloor = b \le \ell$, which is statement 2, and statement 3 holds for $b'$ as well.

*Termination.* Each pass doubles $b$, and a pass runs only when $b \le n$, so there are at most $\lfloor \lg n \rfloor + 1$ passes when $n \ge 1$, and none when $n = 0$.

*Exit.* The loop stops when $b > n$ or $A[b - 1] \ge x$. In the first case $\ell \le n$. In the second case $b \le n$, and $A[b-1] \ge x$ gives $\ell \le b - 1$. In both cases $\ell \le \min(b - 1, n)$. Line L4 sets $lo = \lfloor b/2 \rfloor$ and $hi = \min(b - 1, n)$, so with statement 2,

$$ lo \le \ell \le hi. $$

**The binary search.** Before each test of line L5, $lo \le \ell \le hi$. A pass has $lo < hi$, so $lo \le mid < hi$. If $A[mid] < x$ then $mid < \ell$ and the new $lo = mid + 1 \le \ell$. Otherwise $A[mid] \ge x$, so $\ell \le mid$, and the new $hi = mid \ge \ell$. In both cases the invariant holds and $hi - lo$ drops by at least 1, since the new size is $\lfloor (hi - lo)/2 \rfloor$ or $\lceil (hi - lo)/2 \rceil - 1$. So the loop stops, with $lo \ge hi$, and then $lo = \ell = hi$.

**Result.** Line L9 runs with $lo = \ell$ and returns $\ell$ exactly when $\ell < n$ and $A[\ell] = x$, which is the answer. Otherwise line L10 returns NIL, which is the answer. $\blacksquare$

**The number of comparisons.** If $\ell = 0$ and $n \ge 1$, the first test fails, $lo = hi = 0$, and with line L9 there are 2 comparisons. If $n = 0$ there are none.

Let $\ell \ge 1$ and $k = \lfloor \lg \ell \rfloor$, so $2^k \le \ell < 2^{k+1}$. A test at $b$ can pass only when $b \le \ell$, by statement 3 for the next value, so the passes are at $b = 1, 2, \ldots, 2^j$ with $j \le k$, and there is at most one more test, a failing one. So the doubling makes at most $k + 2$ tests, and it stops with $b \le 2^{k+1}$. The interval of line L4 then has $s = hi - lo \le b - 1 - b/2 = b/2 - 1 \le 2^k - 1$ positions. The binary search makes at most $\lceil \lg(s + 1) \rceil \le k$ tests, because each test leaves at most $\lfloor s/2 \rfloor$ positions and $\lfloor (2^k - 1)/2 \rfloor = 2^{k-1} - 1$. With the one test of line L9 the total is at most $(k + 2) + k + 1 = 2\lfloor \lg \ell \rfloor + 3$.
