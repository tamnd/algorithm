---
title: Fibonacci search returns the first index of x, or NIL, in at most K - 2 steps
proves: [correctness, termination, complexity]
status: full
---

Let $A[0 \ldots n-1]$ be sorted in non-decreasing order, $n \ge 0$, and let $x$ be a key. Extend $A$ by $A[j] = +\infty$ for $j \ge n$; the algorithm never reads these items, because line L6 tests $mid < n$ first and then acts as if $A[mid] \ge x$. Let $\ell = |\{\, j < n : A[j] < x \,\}|$ be the lower bound of $x$, so $0 \le \ell \le n$ and, for every $j \ge 0$, $A[j] < x$ exactly when $j < \ell$. The answer is $\ell$ when $\ell < n$ and $A[\ell] = x$, and NIL otherwise. Write $F_0 = 0$, $F_1 = 1$, $F_k = F_{k-1} + F_{k-2}$.

**Line L2.** Before each test of line L2, $(g, f) = (F_{k-1}, F_k)$ for some $k \ge 1$: this holds for $(0, 1) = (F_0, F_1)$, and the step gives $(F_k, F_k + F_{k-1}) = (F_k, F_{k+1})$. Since $F_k$ grows without bound, the loop stops, at the smallest $K \ge 1$ with $F_K - 1 \ge n$ (for $n \ge 1$, the values $F_1 = F_2 = 1$ both fail and the first success has $K \ge 3$).

**The invariant.** Before each test of line L4:

1. $(g, f) = (F_{k-1}, F_k)$ for some $k \ge 1$;
2. $lo \le \ell \le lo + f - 1$.

At the start $lo = 0$ and $f - 1 \ge n \ge \ell$, so both hold with $k = K$.

*Step.* The loop runs when $f > 1$, that is $F_k \ge 2$, so $k \ge 3$ and $g = F_{k-1} \ge 1$. Line L5 gives $lo \le mid = lo + F_{k-1} - 1 \le lo + f - 1$.

- If $mid < n$ and $A[mid] < x$, then $mid < \ell$, so the new $lo' = mid + 1 \le \ell$. The new end is $lo' + F_{k-2} - 1 = lo + F_{k-1} + F_{k-2} - 1 = lo + f - 1 \ge \ell$. The new pair is $(f - g, 2g - f) = (F_{k-2}, F_{k-1} - F_{k-2}) = (F_{k-2}, F_{k-3})$, and $k - 2 \ge 1$.
- Otherwise $A[mid] \ge x$ (when $mid \ge n$ the extended item is $+\infty$), so $\ell \le mid = lo + F_{k-1} - 1$, which is the new end with the pair $(g, f - g) = (F_{k-1}, F_{k-2})$, and $k - 1 \ge 2$.

In both cases statements 1 and 2 hold for the new values.

*Termination.* Each step lowers $k$ by 1 or 2 and keeps $k \ge 1$, and the loop runs only while $k \ge 3$. So it stops after at most $K - 2$ steps (none when $K \le 2$, that is, $n = 0$). It stops with $f \le 1$, so $f = F_k = 1$ and statement 2 gives $lo \le \ell \le lo$, so $lo = \ell$.

**Result.** Line L9 runs with $lo = \ell$. It returns $\ell$ exactly when $\ell < n$ and $A[\ell] = x$, the answer, and otherwise line L10 returns NIL, the answer. $\blacksquare$

**The number of comparisons.** There are at most $K - 2$ steps, each with at most one comparison, and one more at line L9: at most $K - 1$. For $n \ge 1$, by the choice of $K$, $F_{K-1} - 1 < n$, so $F_{K-1} \le n$. The bound $F_j \ge \varphi^{j-2}$ for $j \ge 1$, with $\varphi = (1 + \sqrt{5})/2$, follows by induction from $\varphi^2 = \varphi + 1$. So $\varphi^{K-3} \le n$, and the number of steps is $K - 2 \le \log_\varphi n + 1$.
