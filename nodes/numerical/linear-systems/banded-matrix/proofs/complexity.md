---
title: Flop counts for band storage
proves: [flops.worst, time.worst, space.extra, matvec.worst]
status: full
---

**Matvec.** Row $i$ has at most $p + q + 1$ stored entries, each costing one multiplication and one addition in line M3. So at most $2 n (p + q + 1)$ flops. $\square$

**BandLU.** At step $k$ let $m_k = \min(p, n - k)$ and $s_k = \min(q, n - k)$. Lines L3 and L4 do $m_k$ divisions, and lines L5 to L7 do $m_k s_k$ multiplications and $m_k s_k$ subtractions. The total is $\sum_{k=1}^{n} m_k (2 s_k + 1) \le n p (2q + 1)$, and for $n \ge p + q$ it is at least $(n - p - q) p (2q + 1)$, so it is $\Theta(n p q + n p)$; with the $n$ pivot tests the time is $\Theta(n p q + n)$. $\square$

**Pivoted LU.** The same count with $s_k \le \min(p + q, n - k)$, plus at most $p$ comparisons and $p + q + 1$ swaps per step: at most $n p (2(p + q) + 1)$ flops, $O(n p (p + q) + n)$ time. $\square$

**Space.** The array `ab` has $p + q + 1$ rows of length $n$, and $2p + q + 1$ for the pivoted factorization, plus the $n$ pivot indices: $\Theta(n (p + q + 1))$. $\square$

$\blacksquare$
