---
title: Sorted dynamic programming finds an optimal pair matching on one score
proves: [correctness]
status: full
---

After line L1, the treated scores are $s_1 \le \cdots \le s_m$ and the control scores are $c_1 \le \cdots \le c_n$, with $m \le n$; renaming the units does not change any cost. A *matching* is an injective map $\sigma : \{1, \ldots, m\} \to \{1, \ldots, n\}$, and $\operatorname{cost}(\sigma) = \sum_i |s_i - c_{\sigma(i)}|$. A matching is *monotone* if $\sigma(1) < \sigma(2) < \cdots < \sigma(m)$.

**Lemma 1 (convex exchange).** Let $\varphi$ be convex on the real line. If $x \le u \le y$, $x \le v \le y$ and $u + v = x + y$, then $\varphi(u) + \varphi(v) \le \varphi(x) + \varphi(y)$.

*Proof.* If $x = y$, all four numbers are equal. Otherwise put $\lambda = (y - u)/(y - x) \in [0, 1]$. Then $u = \lambda x + (1 - \lambda)y$ and $v = x + y - u = (1 - \lambda)x + \lambda y$. By convexity, $\varphi(u) \le \lambda\varphi(x) + (1 - \lambda)\varphi(y)$ and $\varphi(v) \le (1 - \lambda)\varphi(x) + \lambda\varphi(y)$. Add the two. $\square$

**Lemma 2 (uncrossing).** If $a \le b$ and $p \le q$ are reals, then $|a - p| + |b - q| \le |a - q| + |b - p|$.

*Proof.* Put $x = a - q$, $y = b - p$, $u = a - p$ and $v = b - q$. Then $x \le u \le y$ and $x \le v \le y$, because $p \le q$ and $a \le b$, and $u + v = x + y$. Apply Lemma 1 with $\varphi = |\cdot|$. $\square$

**Lemma 3 (a monotone optimum exists).** There is an optimal matching that is monotone.

*Proof.* There are finitely many matchings, so an optimal one exists. Among the optimal matchings, take one, $\sigma$, with the fewest *inversions*, pairs $a < b$ with $\sigma(a) > \sigma(b)$. Suppose it has an inversion $a < b$. Then $s_a \le s_b$ and $c_{\sigma(b)} \le c_{\sigma(a)}$. Let $\sigma'$ be $\sigma$ with the values at $a$ and $b$ swapped. By Lemma 2 with $p = c_{\sigma(b)}$ and $q = c_{\sigma(a)}$, $\operatorname{cost}(\sigma') \le \operatorname{cost}(\sigma)$, so $\sigma'$ is also optimal. Swapping the two values of an inverted pair in a sequence lowers the number of inversions by at least one: the pair $(a, b)$ is no longer inverted, and for each $k$ strictly between $a$ and $b$, the number of inversions among $\{a, k, b\}$ does not increase. This contradicts the choice of $\sigma$. So $\sigma$ has no inversion, and since it is injective, it is strictly increasing. $\square$

**Lemma 4 (the table).** For $0 \le i \le m$ and $0 \le j \le n$, let $\mathrm{OPT}(i, j)$ be the least cost of a monotone matching of $s_1, \ldots, s_i$ into $c_1, \ldots, c_j$, with $\mathrm{OPT}(i, j) = \infty$ when $j < i$ (no injection exists) and $\mathrm{OPT}(0, j) = 0$. After lines L2 to L5, $D[i][j] = \mathrm{OPT}(i, j)$ for all $i, j$.

*Proof.* By induction on $i + j$. Line L2 sets the cases $i = 0$ and $j < i$ correctly, and lines L3 and L4 never write to them. Let $1 \le i \le j$. Line L5 runs after $D[i][j - 1]$ (the same row, previous column, or the value $\infty$ from line L2 when $j = i$) and $D[i - 1][j - 1]$ (the previous row) are final, so by induction it sets $D[i][j] = \min(\mathrm{OPT}(i, j - 1), \mathrm{OPT}(i - 1, j - 1) + |s_i - c_j|)$. Take a monotone matching $\sigma$ of the first $i$ treated into the first $j$ controls. If $c_j$ is unused, $\sigma$ is a monotone matching into the first $j - 1$ controls, so its cost is at least $\mathrm{OPT}(i, j - 1)$. If $c_j$ is used, then $\sigma(i) = j$, since $\sigma(i)$ is the largest value of $\sigma$ and is at most $j$; then $\sigma$ restricted to $1, \ldots, i - 1$ is a monotone matching into the first $j - 1$ controls, and the cost is at least $\mathrm{OPT}(i - 1, j - 1) + |s_i - c_j|$. So $\mathrm{OPT}(i, j)$ is at least the minimum of the two. Conversely, both values are reached: an optimal matching for $(i, j - 1)$ is one for $(i, j)$ that leaves $c_j$ unused, and an optimal matching for $(i - 1, j - 1)$ extended by $i \mapsto j$ is monotone. So $D[i][j] = \mathrm{OPT}(i, j)$. $\square$

**Lemma 5 (the trace back).** Line L6 returns a monotone matching of cost $D[m][n]$.

*Proof.* The trace back keeps the invariant that the pairs found so far have total cost $D[m][n] - D[i][j]$, and that their treated indices are $i + 1, \ldots, m$ and their control indices are larger than $j$ and increasing in the treated index. At the start, $(i, j) = (m, n)$ and no pairs are found. If $j > i$ and $D[i][j - 1] = D[i][j]$, the step to $(i, j - 1)$ keeps the invariant. Otherwise, if $j = i$ then $D[i][j - 1] = \infty$, and if $j > i$ then $D[i][j - 1] \ne D[i][j]$; in both cases line L5 took the second term, so $D[i][j] = D[i - 1][j - 1] + |s_i - c_j|$, and adding the pair $(i, j)$ and moving to $(i - 1, j - 1)$ keeps the invariant. When $i \ge 1$ the table value is finite, since $j \ge i$ holds throughout (the first move needs $j > i$, the second lowers both). Each step lowers $i + j$, and the loop stops at $i = 0$, where $D[0][j] = 0$. Then the pairs cover every treated unit, use distinct controls, and cost $D[m][n]$. $\square$

**Theorem 6 (optimality).** OPTIMAL-PAIR-MATCH returns a matching $\sigma$ with $\operatorname{cost}(\sigma) = \min_\tau \operatorname{cost}(\tau)$ over all matchings $\tau$, and returns that cost.

*Proof.* By Lemma 4, $D[m][n]$ is the least cost over monotone matchings. Every monotone matching is a matching, and by Lemma 3 some optimal matching is monotone, so $D[m][n]$ is the least cost over all matchings. By Lemma 5 the returned pairs reach it. Mapping the sorted positions back to the original indices does not change any distance. $\square$

The proof used only Lemma 1 for $\varphi = |\cdot|$, so the same algorithm, with $|s_i - c_j|$ replaced by $\varphi(s_i - c_j)$ in line L5, is optimal for every convex $\varphi$.

**Cost.** Line L1 sorts in $\Theta(m\log m + n\log n)$ time. Line L5 runs $\sum_{i=1}^m (n - i + 1) = m(n + 1) - m(m - 1)/2$ times, which lies between $m(n + 1)/2$ and $m(n + 1)$ since $m \le n$, and each run takes constant time. Line L6 takes at most $m + n$ steps. So the time is $\Theta(mn + n\log n)$, and the table uses $\Theta(mn)$ space. All loops have finite ranges and the trace back lowers $i + j$ at each step, so the procedure terminates. $\blacksquare$
