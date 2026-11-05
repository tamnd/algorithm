---
title: Uniform binary search returns the first index of x, or NIL, with exactly floor(lg n) + 1 order comparisons
proves: [correctness, termination, complexity]
status: full
---

Let $A[0 \ldots n-1]$ be sorted in non-decreasing order, $n \ge 0$, and let $x$ be a key. For the argument only, extend $A$ with $A[-1] = -\infty$ and $A[n] = +\infty$. Let $\ell = |\{\, j : 0 \le j < n,\ A[j] < x \,\}|$ be the lower bound of $x$. Since $A$ is sorted, $A[j] < x$ for $-1 \le j < \ell$ and $A[j] \ge x$ for $\ell \le j \le n$. We prove that UNIFORM-BINARY-SEARCH$(A, x)$ returns $\ell$ when $\ell < n$ and $A[\ell] = x$, and NIL otherwise, that it reads only cells $A[0], \ldots, A[n-1]$, and that it makes exactly $\lfloor \lg n \rfloor + 1$ order comparisons when $n \ge 1$.

If $n = 0$, line L1 returns NIL, which is correct. Assume $n \ge 1$. Line L2 sets $p = 2^k$ with $k = \lfloor \lg n \rfloor$, so $p \le n < 2p$. Line L4 reads $A[p - 1]$, a real cell since $1 \le p \le n$.

**Invariant.** Before each test of line L6:

1. $s$ is a power of 2 with $1 \le s \le p$.
2. $-1 \le b$ and $b + s \le n$.
3. $A[b] < x \le A[b + s]$, that is, $b < \ell \le b + s$.

*Start.* Line L5 sets $s = p$, so statement 1 holds. There are two cases for line L4.

- If $A[p - 1] \ge x$, then $b = -1$, and $b + s = p - 1 \le n - 1$. Also $A[-1] = -\infty < x \le A[p - 1]$.
- If $A[p - 1] < x$, then $b = n - p$. From $n < 2p$ we get $b \le p - 1$, so $A[b] \le A[p - 1] < x$, and $b \ge 0$. Also $b + s = n$ and $x \le A[n] = +\infty$.

*Step.* A pass runs only when $s > 1$, so $s \ge 2$ and $s' = s / 2$ is a power of 2 with $1 \le s' < s$. The pass reads $A[b + s']$. Since $b \ge -1$ and $s' \ge 1$, the index is at least $0$; since $b + s \le n$ and $s' < s$, it is at most $n - 1$. So it is a real cell.

- If $A[b + s'] < x$, the new value is $b' = b + s'$. Then $A[b'] < x$, and $b' + s' = b + s$, so $b' + s' \le n$ and $x \le A[b' + s']$.
- Otherwise $b' = b$, $A[b] < x$, and $x \le A[b + s']$, with $b + s' < b + s \le n$.

In both cases the three statements hold for $(b', s')$.

**Termination and the count.** Each pass halves $s$, which starts at $p = 2^k$, so the loop makes exactly $k$ passes and stops with $s = 1$. Each pass makes one order comparison, and line L4 makes one, so the total is $k + 1 = \lfloor \lg n \rfloor + 1$ for every key.

**The result.** At the end $s = 1$, and statement 3 gives $b < \ell \le b + 1$, so $\ell = b + 1$. If $b + 1 < n$ and $A[b + 1] = x$, line L9 returns $\ell$; since every index $j < \ell$ has $A[j] < x$, this is the smallest index of $x$. Otherwise, either $\ell = n$, so every item is $< x$, or $A[\ell] > x$, so every item from $\ell$ on is $> x$ and every item before is $< x$. In both cases $x$ is not in $A$, and line L10 returns NIL, which is correct. $\blacksquare$
