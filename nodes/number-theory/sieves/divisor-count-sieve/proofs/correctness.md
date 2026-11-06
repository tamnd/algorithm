---
title: The divisor-count sieve computes d(m) for every m up to n
proves: [correctness]
status: full
---

Fix $m$ with $1 \le m \le n$. Line L1 sets $d[m] = 0$, and line L4 is the only line that changes $d[m]$; each run adds 1. So at the end, $d[m]$ equals the number of pairs $(e, j)$ for which line L4 runs with $m = j e$, that is, with $e$ the value of the outer loop and $j \ge 1$ the step of the inner loop.

**Claim.** Line L4 runs at the index $m$ exactly once for each positive divisor $e$ of $m$, and never for any other $e$.

*Proof.* For a fixed $e$ with $1 \le e \le n$, the loop of line L3 takes the values $m' = e, 2e, 3e, \ldots$ while $m' \le n$. These values are distinct, and they are exactly the multiples of $e$ in $[1, n]$. So the index $m$ appears in the round of $e$ once if $e \mid m$, and not at all otherwise. Every positive divisor $e$ of $m$ satisfies $1 \le e \le m \le n$, so the loop of line L2 reaches it. $\square$

By the claim, $d[m]$ ends equal to the number of positive divisors of $m$, which is $d(m)$. No run of line L4 writes index 0, since $m' \ge e \ge 1$, so $d[0] = 0$. The loops terminate: the outer loop runs $n$ times, and the round of $e$ runs $\lfloor n/e \rfloor$ times. $\blacksquare$

The same argument, with line L4 adding $e^k$ instead of 1, shows that the variant computes $\sigma_k(m) = \sum_{e \mid m} e^k$.

**The count of runs.** By the claim, the total number of runs of line L4 is $\sum_{m \le n} d(m)$, and counting by $e$ instead gives $\sum_{e \le n} \lfloor n/e \rfloor$. These two sums are equal, which is the identity used in the complexity section.
