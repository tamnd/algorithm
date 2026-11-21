---
title: What OSEM guarantees and what it does not
proves: [correctness]
status: full
---

We use the notation of the page. $A$ is an $m \times N$ matrix with $a_{ij} \ge 0$, $b \ge 0$ is the known background, $y \ge 0$ holds the counts, and the bins are split into disjoint subsets $S_1, \ldots, S_T$ whose union is all bins. For a subset $t$ put $s^t_j = \sum_{i \in S_t} a_{ij}$ and
$$L_t(x) = \sum_{i \in S_t} \big[y_i \log \bar y_i - \bar y_i\big], \qquad \bar y = A x + b,$$
so the full log-likelihood is $L = \sum_t L_t$. Sub-iteration $t$ (lines L5 to L8) maps $x$ to
$$x'_j = \frac{x_j}{s^t_j} \sum_{i \in S_t} a_{ij} \frac{y_i}{\bar y_i} \quad \text{if } s^t_j > 0, \qquad x'_j = x_j \quad \text{if } s^t_j = 0, \tag{1}$$
where the sum runs over the bins of $S_t$ with $y_i > 0$. We assume that $\bar y_i > 0$ for every bin with $y_i > 0$, as on the MLEM page. We work in exact arithmetic.

**Theorem 1 (one sub-iteration).** For every subset $t$, $L_t(x') \ge L_t(x)$, with equality only if $x' = x$, and $x' \ge 0$.

*Proof.* Let $A_t$ be the rows of $A$ in $S_t$, and remove the pixels with $s^t_j = 0$: they do not enter $L_t$, because their column in $A_t$ is zero, and (1) does not change them. On the other pixels, (1) is exactly one MLEM iteration for the matrix $A_t$, the counts $y_i$, $i \in S_t$, and the background $b_i$, $i \in S_t$. Theorem 1 of the MLEM proof (the Jensen surrogate) gives $L_t(x') \ge L_t(x)$ with equality only if $x' = x$. Every factor in (1) is nonnegative. $\square$

So OSEM is a cycle of $T$ maps, and map $t$ climbs its own likelihood $L_t$. It does not climb $L$: a step that raises $L_t$ can lower $L_s$ for $s \ne t$ by more.

**Theorem 2 (the subset count).** If $b = 0$, then after sub-iteration $t$, $\sum_j s^t_j x'_j = \sum_{i \in S_t} y_i$.

*Proof.* Sum (1) times $s^t_j$ over the pixels with $s^t_j > 0$ and swap the sums: $\sum_{i \in S_t} (y_i / \bar y_i) \sum_j a_{ij} x_j = \sum_{i \in S_t} y_i$, because $\bar y_i = \sum_j a_{ij} x_j$ for $b = 0$. The pixels with $s^t_j = 0$ add nothing. $\square$

**Theorem 3 (consistent data).** If $x \ge 0$ satisfies $A x + b = y$, then $x$ is a fixed point of every sub-iteration, so OSEM started at $x$ stays at $x$.

*Proof.* For every $i$ with $y_i > 0$, $y_i / \bar y_i = 1$. So for $s^t_j > 0$, (1) gives $x'_j = (x_j / s^t_j) \sum_{i \in S_t, y_i > 0} a_{ij}$. A bin with $y_i = 0$ has $\bar y_i = 0$, so $a_{ij} x_j = 0$ for all $j$ in that bin. Hence $x_j \sum_{i \in S_t, y_i > 0} a_{ij} = x_j s^t_j$, and $x'_j = x_j$. $\square$

**Theorem 4 (no convergence in general).** There are data for which the OSEM iterates do not converge, and for which the end points of the passes converge to a point that is not a maximizer of $L$.

*Proof.* Take one pixel, two bins with $a_{11} = a_{21} = 1$, $b = 0$, counts $y = (1, 3)$, and the subsets $S_1 = \{1\}$, $S_2 = \{2\}$. Both subsets have $s^t_1 = 1$, so they are balanced. Sub-iteration 1 gives $x' = x \cdot 1/x = 1$, and sub-iteration 2 gives $x' = x \cdot 3/x = 3$, from every positive start. So the sub-iterates are $1, 3, 1, 3, \ldots$ and do not converge. The end point of each pass is 3. The maximizer of $L(x) = \log x - x + 3 \log x - x$ is $x = 2$, because $L'(x) = 4/x - 2$. $\square$

The example has inconsistent data: no $x$ has $x = 1$ and $x = 3$. Real counts are always inconsistent with the model in this sense, because of the noise. So in practice OSEM does not converge to the maximum likelihood image. Its passes approach a limit cycle near it. The page shows a second example on a $2 \times 2$ image.

**What is known about convergence (cited, not proved here).** Hudson and Larkin (1994) proved that if the data are exact, so that a nonnegative solution of $A x + b = y$ exists, and the subsets are balanced, that is $s^t_j$ does not depend on $t$, then OSEM converges to such a solution. Methods that converge with noisy data change the update: they make the step size go to 0, as in RAMLA, or they keep a running sum of all subset gradients, as in COSEM. They are not the plain OSEM of this page.
