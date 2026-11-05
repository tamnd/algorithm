---
title: The column sweep returns a maximum-sum submatrix
proves: [correctness]
status: full
---

We use the pseudocode of the page on $M[0..m-1][0..n-1]$ with $m, n \ge 1$. For $a \le b$ and $e \le d$ let $S(a, b, e, d) = \sum_{i=a}^{b} \sum_{j=e}^{d} M[i][j]$, and let $S^*$ be its maximum over all such quadruples. We use the correctness of Kadane's algorithm: on an array $C[0..n-1]$ with $n \ge 1$, KADANE returns $(s, e, d)$ with $e \le d$, $\sum_{j=e}^{d} C[j] = s$, and $s$ the largest sum of a non-empty subarray of $C$.

**Lemma 1 (band sums).** In the iteration $(a, b)$ of the inner loop, after line L5, $C[j] = \sum_{i=a}^{b} M[i][j]$ for every $j$.

*Proof.* By induction on $b$ for fixed $a$. Line L3 sets $C[j] = 0$, the empty sum. If $C[j] = \sum_{i=a}^{b-1} M[i][j]$ before line L5 (for $b = a$ the sum is empty), line L5 adds $M[b][j]$. $\blacksquare$

**Lemma 2 (one band).** In the iteration $(a, b)$, line L6 returns $s = \max_{e \le d} S(a, b, e, d)$ and columns $e \le d$ with $S(a, b, e, d) = s$.

*Proof.* By Lemma 1, $S(a, b, e, d) = \sum_{j=e}^{d} \sum_{i=a}^{b} M[i][j] = \sum_{j=e}^{d} C[j]$, after exchanging the finite sums. So the rectangles with rows $a..b$ correspond one to one, with equal sums, to the non-empty subarrays of $C$. The correctness of Kadane's algorithm gives the claim. $\blacksquare$

**Claim.** After the iteration $(a, b)$, $best = \max\{S(a', b', e, d)\}$ over all bands $(a', b')$ visited so far and all $e \le d$, and $R$ is a rectangle with this sum.

*Proof.* Before the first iteration, no band is visited and $best = -\infty$. In iteration $(a, b)$, Lemma 2 gives the best sum $s$ of the band and its columns, and line L7 replaces $(best, R)$ when $s$ is larger, so the claim holds after the iteration. $\blacksquare$

**Theorem.** COLUMN-SWEEP returns $S^*$ and a rectangle that reaches it.

*Proof.* The loops of lines L2 and L4 visit each pair $0 \le a \le b \le m - 1$ exactly once, and every rectangle has its rows in exactly one such band. By the claim after the last iteration, $best = S^*$ and $R$ reaches it. There are $m(m+1)/2$ iterations, each with $\Theta(n)$ work, so the algorithm stops after $\Theta(m^2 n)$ steps. $\blacksquare$
