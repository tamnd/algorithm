---
title: The generalized median is computed correctly, is strategyproof on single-peaked preferences, and is Pareto efficient with n - 1 phantoms
proves: [correctness]
status: full
---

The candidates are the points $0, 1, \ldots, m - 1$ of the axis. Each voter $i$ has a ranking $\succ_i$ that is single-peaked on the axis with peak $p_i$. The rule takes the multiset $V$ of the $n$ reported peaks and the $k$ phantoms $a_1, \ldots, a_k$, with $T = n + k$ odd, and returns its median: the value at position $(T + 1)/2$ when $V$ is sorted. For a value $y$ let $c(y)$ be the number of elements of $V$ that are at most $y$. The median is the smallest $y$ with $c(y) \ge (T + 1)/2$.

## The code returns the median

Lines L1 to L3 set $\mathrm{cnt}[x]$ to the number of elements of $V$ equal to $x$. Before line L6 tests $x$, line L5 has made $\mathrm{seen} = \mathrm{cnt}[0] + \cdots + \mathrm{cnt}[x] = c(x)$. The loop goes through $x = 0, 1, \ldots$ in order and stops at the first $x$ with $c(x) \ge (T + 1)/2$, which is the median by the description above. Some $x$ stops the loop, because $c(m - 1) = T$. The time is $O(n + k + m)$ and the extra space is $O(m)$.

## A fact about single-peaked rankings

If $y < z \le p_i$, then $z \succ_i y$. If $p_i \le z < y$, then $z \succ_i y$. In words, on each side of the peak a point nearer to the peak is better. This is the no-valley form of the definition applied to $y, z, p_i$, with $z = p_i$ allowed.

## Strategyproofness

Fix the reports of the other voters and the phantoms. Let $x$ be the outcome when voter $i$ reports its true peak $p_i$, and let $x'$ be the outcome when it reports some $q$. We show that $x' \succ_i x$ never holds. The rule reads only the top of each reported ranking, so a false ranking acts only through its top $q$.

If $x = p_i$, the voter gets its best point and cannot gain. Assume $x < p_i$; the case $x > p_i$ is the mirror image.

- If $q > x$: going from $p_i$ to $q$ removes a value above $x$ and adds a value above $x$, so $c(y)$ does not change for any $y \le x$. The smallest $y$ with $c(y) \ge (T + 1)/2$ is still $x$, so $x' = x$.
- If $q \le x$: the change adds one to $c(y)$ for $q \le y < p_i$ and leaves the other counts the same. No count goes down, so the smallest $y$ with a large enough count can only move left: $x' \le x$.

So $x' \le x < p_i$, and by the fact above $x \succ_i x'$ or $x' = x$. The voter cannot gain. This holds for every choice of phantoms, every $k$ with $T$ odd, and every reports of the other voters.

## Unanimity and Pareto efficiency

**With $n - 1$ phantoms**, $T = 2n - 1$ and the median is the element in position $n$. At least $n$ values, the $n$ peaks, are at most $\max_i p_i$, so $c(\max_i p_i) \ge n$ and the outcome is at most $\max_i p_i$. In the same way it is at least $\min_i p_i$. A point $x$ with $\min_i p_i \le x \le \max_i p_i$ is Pareto efficient on single-peaked rankings: for $z > x$, the voter with peak $\min_i p_i \le x$ prefers $x$ to $z$ by the fact above, and for $z < x$ the voter with peak $\max_i p_i$ prefers $x$ to $z$. So no other point is ranked above $x$ by all voters.

**With $n + 1$ phantoms.** If the phantoms include the point $0$ and the point $m - 1$, removing one copy of each from $V$ removes the smallest and the largest value and does not change the median, so the rule equals a rule with the other $n - 1$ phantoms and is Pareto efficient. If no phantom is at $0$, let every voter have peak $0$. Then $V$ has exactly $n$ values equal to $0$, fewer than $(T + 1)/2 = n + 1$, so the outcome is not $0$, while every voter prefers $0$ to it. The case with no phantom at $m - 1$ is the mirror image. So a median with $n + 1$ phantoms is Pareto efficient if and only if it has a phantom at each end of the axis.

More precisely, with $n + 1$ phantoms and all voters at the same peak $p$, the outcome is in position $n + 1$ of $2n + 1$ values. If $p < \min_j a_j$, the first $n$ values are the copies of $p$ and the outcome is $\min_j a_j$. If $p > \max_j a_j$, the first $n + 1$ values are the phantoms and the outcome is $\max_j a_j$. Otherwise it is $p$. So the outcome is $p$ moved into the interval $[\min_j a_j, \max_j a_j]$.

## The characterization

The converse, that every anonymous and strategyproof rule that depends only on the peaks is a median with $n + 1$ phantoms, is Moulin's theorem (Moulin 1980, Proposition 2; Weymark 2011, Theorem 4), and with Pareto efficiency added the rule is a median with $n - 1$ phantoms (Weymark 2011, Theorem 5). This file does not reprove it. The test `test_characterization_three_candidates_two_voters` checks it by brute force for $m = 3$ and $n = 2$: of the $3^6 = 729$ functions from multisets of two peaks to outcomes, exactly the 10 medians with 3 phantoms are strategyproof, and exactly the 3 medians with 1 phantom are strategyproof and Pareto efficient.
