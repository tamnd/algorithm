---
title: Pascal's triangle dynamic programming returns C(n, k) mod m
proves: [correctness]
status: full
---

We use the pseudocode of the page. The input is an integer $n \ge 0$, an integer $k$ and a modulus $m \ge 1$ or $m = \infty$, where $x \bmod \infty = x$. For integers $i \ge 0$ and $j$, $\binom{i}{j}$ is the number of $j$-subsets of $[i]$, which is $0$ when $j < 0$ or $j > i$.

**Facts used.**

1. *Pascal's rule.* For $i \ge 1$ and every integer $j$, $\binom{i}{j} = \binom{i-1}{j-1} + \binom{i-1}{j}$. (Fix the element $i$: the $j$-subsets of $[i]$ that contain it correspond to the $(j-1)$-subsets of $[i-1]$, and those that do not are the $j$-subsets of $[i-1]$.)
2. *Symmetry.* For $0 \le k \le n$, $\binom{n}{k} = \binom{n}{n-k}$, by taking complements.
3. *Reduction.* $(a \bmod m + b \bmod m) \bmod m = (a + b) \bmod m$ for integers $a, b \ge 0$; for $m = \infty$ this is trivial.

**Claim.** PASCAL-TRIANGLE-DP$(n, k, m)$ returns $\binom{n}{k} \bmod m$.

*Proof.* If $k < 0$ or $k > n$, line L1 returns $0 = \binom{n}{k} \bmod m$. Otherwise $0 \le k \le n$, and line L2 replaces $k$ by $k' = \min(k, n - k)$, with $0 \le k' \le n$ and $\binom{n}{k'} = \binom{n}{k}$ by fact 2. From now on write $k$ for $k'$. Lines L3 and L4 create $R[0 \ldots k]$ with $R[0] = 1 \bmod m$ and $R[j] = 0$ for $j \ge 1$.

*Outer invariant.* For $1 \le i \le n + 1$:

> **(O)** before the iteration of line L5 for $i$ (or after the loop when $i = n + 1$), $R[j] = \binom{i-1}{j} \bmod m$ for every $0 \le j \le k$.

*Initialization.* For $i = 1$: $\binom{0}{0} = 1$ and $\binom{0}{j} = 0$ for $j \ge 1$, which is what lines L3 and L4 store.

*Maintenance.* Assume (O) for some $i \le n$, and let $t = \min(i, k)$. The inner loop of line L6 runs $j = t, t - 1, \ldots, 1$. We show this inner invariant:

> **(I)** when the inner loop is about to process $j$ (or has finished, with $j = 0$), $R[\ell] = \binom{i}{\ell} \bmod m$ for $j < \ell \le t$, and $R[\ell] = \binom{i-1}{\ell} \bmod m$ for $0 \le \ell \le j$ and for $t < \ell \le k$.

Before the first step, $j = t$, and (I) is (O). Assume (I) before the step for $j \ge 1$. Line L7 reads $R[j]$ and $R[j-1]$; both have index at most $j$, so they hold $\binom{i-1}{j} \bmod m$ and $\binom{i-1}{j-1} \bmod m$. By facts 3 and 1, line L7 stores $\bigl(\binom{i-1}{j} + \binom{i-1}{j-1}\bigr) \bmod m = \binom{i}{j} \bmod m$ in $R[j]$. No other entry changes, so (I) holds with $j - 1$ in place of $j$.

When the inner loop ends, $j = 0$, so $R[\ell] = \binom{i}{\ell} \bmod m$ for $1 \le \ell \le t$, and the other entries are unchanged. They are also right for row $i$:

- $R[0] = \binom{i-1}{0} \bmod m = 1 \bmod m = \binom{i}{0} \bmod m$.
- If $t = i < k$, the entries $R[\ell]$ with $i < \ell \le k$ hold $\binom{i-1}{\ell} = 0$, since $\ell > i - 1$, and $\binom{i}{\ell} = 0$ too, since $\ell > i$.

So (O) holds for $i + 1$.

*Termination.* The outer loop ends after $i = n$, and (O) for $i = n + 1$ gives $R[k] = \binom{n}{k} \bmod m$, which line L8 returns. When $n = 0$, the loop body never runs, $k = 0$, and line L8 returns $R[0] = 1 \bmod m = \binom{0}{0} \bmod m$, which agrees with (O) for $i = 1$. Both loops have fixed bounds, so the algorithm stops. $\square$

**Number of additions.** For $0 \le k \le n$ (after line L2), line L7 runs $\sum_{i=1}^{n} \min(i, k) = \sum_{i=1}^{k} i + (n - k)k = \frac{k(k+1)}{2} + nk - k^2 = nk - \frac{k(k-1)}{2}$ times. Since $k - 1 \le n$, this lies between $nk/2$ and $nk$.

**Size of the numbers.** For $0 \le j \le k \le n/2$ and $i \le n$, $\binom{i}{j} \le \binom{n}{j} \le \binom{n}{k}$: the first inequality holds because $\binom{i}{j}$ counts $j$-subsets of $[i] \subseteq [n]$, and the second because a row increases up to its middle. So in exact arithmetic, every value stored in $R$ is at most the answer. $\blacksquare$
