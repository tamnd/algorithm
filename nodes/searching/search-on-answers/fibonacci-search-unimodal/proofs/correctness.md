---
title: Fibonacci search finds the mode of a strictly unimodal sequence with the optimal number of evaluations
proves: [correctness]
status: full
---

We use the pseudocode of the page and the [Fibonacci numbers](/fibonacci-numbers/) $F_0 = 0$, $F_1 = 1$, $F_{k+2} = F_{k+1} + F_k$. Let $f$ be strictly unimodal for a maximum on $\{1, \ldots, n\}$ with mode $m$, and let $N \ge 1$ be the smallest number with $F_{N+2} \ge n + 1$.

**Padding.** Extend $f$ to $g$ on $\{1, \ldots, F_{N+2} - 1\}$ by $g(i) = f(i)$ for $i \le n$ and $g(i) = -M - i$ for $i > n$, where $M$ is larger than $-\min f$. Then $g$ is strictly unimodal with the same mode $m$: it increases up to $m$, decreases from $m$ to $n$, and keeps decreasing after $n$ with values below all values of $f$. Line L7 does not evaluate $g(q)$ for $q > n$; it treats $q$ as worse than $p$, which is what $g$ answers as long as $p \le n$. The invariant below shows $p \le n$, so the run is exactly the run on $g$.

**Comparison lemma.** For $x_1 < x_2$: $g(x_1) < g(x_2)$ implies $m > x_1$; $g(x_1) > g(x_2)$ implies $m < x_2$; $g(x_1) = g(x_2)$ implies $x_1 < m < x_2$. This is the lemma on the page [unimodal function](/unimodal-function/).

**Invariant.** Before each test of line L5, with $k$ the value of the counter:

1. $lo < p < hi$, and the two parts $p - lo$ and $hi - p$ are $F_{k+1}$ and $F_{k+2}$ in some order;
2. $lo < m < hi$;
3. $1 \le p \le n$ and $fp = f(p)$;
4. the number of evaluations made so far is at most $N - k$.

*Initialization.* Lines L2 to L4 set $lo = 0$, $hi = F_{N+2}$, $p = F_N$ and $k = N - 1$. The parts are $F_N = F_{k+1}$ and $F_{N+2} - F_N = F_{N+1} = F_{k+2}$. Since $1 \le m \le n < F_{N+2}$, item 2 holds. If $N = 1$, then $p = F_1 = 1 \le n$. If $N \ge 2$, minimality of $N$ gives $F_{N+1} \le n$, so $p = F_N \le F_{N+1} \le n$. One evaluation has been made, and $N - k = 1$.

*Maintenance.* Let $k \ge 1$. Then $F_{k+2} = F_{k+1} + F_k > F_{k+1}$, so the larger part is the one of length $F_{k+2}$, and line L6 picks it. Suppose it is the right part, $hi - p = F_{k+2}$, so $q = p + F_k$ with $p < q < hi$ because $1 \le F_k < F_{k+2}$. (The left case is the mirror image.)

- If $q \le n$ and $f(q) > f(p)$ (line L8), the lemma gives $m > p$, so $p < m < hi$. The new state is $lo' = p$, $p' = q$, $hi' = hi$, with parts $F_k$ and $F_{k+2} - F_k = F_{k+1}$. Also $p' = q \le n$ and $fp = f(q)$.
- Otherwise (line L9) $g(q) \le g(p)$: either $q > n$, and then $g(q) < g(p)$ by the padding, or $f(q) \le f(p)$. If $g(q) < g(p)$ the lemma gives $m < q$; if $g(q) = g(p)$ it gives $p < m < q$. In both cases $lo < m < q$. The new state is $hi' = q$ with parts $F_{k+1}$ and $F_k$, and $p$ is unchanged.

In both cases, with $k' = k - 1$, the parts are $F_{k'+1}$ and $F_{k'+2}$, and at most one evaluation was made, so item 4 holds.

*Termination and result.* Each iteration decreases $k$ by 1, so the loop stops with $k = 0$. Then the parts are $F_1 = F_2 = 1$, so $lo = p - 1$ and $hi = p + 1$. By item 2 the only integer strictly between them, $p$, is $m$. Line L11 returns $m$ after at most $N$ evaluations, by item 4. $\square$

**Optimality.** By the discrete theorem on the page [unimodal optimization](/unimodal-optimization/), no method can guarantee to find the mode of every strictly unimodal function on $n$ points with fewer than $N$ evaluations, where $N$ is the smallest number with $n \le F_{N+2} - 1$. This is the $N$ of the algorithm, so Fibonacci search is optimal in the worst case.
