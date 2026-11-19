---
title: LexRank has a unique stationary distribution, and the power method converges to it at rate 1 - d
proves: [correctness]
status: full
---

Let $A$ be the $n \times n$ matrix of lines L1 to L3, with $A_{ij} \ge 0$ and $A_{ii} = 1$, and let $B$ be $A$ with each row divided by its sum (line L4). The rows of $B$ are probability vectors, because each row sum of $A$ is at least $A_{ii} = 1 > 0$. Fix $0 < d \le 1$, let $U$ be the matrix of ones and $M = \frac{d}{n}U + (1 - d)B$. Line L7 computes $q = M^{\mathsf T} p$ when $\sum_i p_i = 1$, since $(\frac{d}{n}U^{\mathsf T} p)_j = \frac{d}{n}\sum_i p_i = \frac{d}{n}$. The norm is $\|x\|_1 = \sum_i |x_i|$, and $\Delta = \{p \ge 0 : \sum_i p_i = 1\}$.

**Lemma 1.** If $p \in \Delta$ then $M^{\mathsf T} p \in \Delta$.

*Proof.* $M \ge 0$, so $M^{\mathsf T}p \ge 0$. Its sum is $\sum_j \sum_i M_{ij} p_i = \sum_i p_i \sum_j M_{ij} = \sum_i p_i = 1$, because each row of $M$ sums to $\frac{d}{n} \cdot n + (1 - d) \cdot 1 = 1$. $\square$

**Lemma 2.** For every $y$ with $\sum_i y_i = 0$, $M^{\mathsf T} y = (1 - d) B^{\mathsf T} y$ and $\|M^{\mathsf T} y\|_1 \le (1 - d)\|y\|_1$.

*Proof.* $U^{\mathsf T} y$ has every entry equal to $\sum_i y_i = 0$, which gives the first claim. For the second, $\|B^{\mathsf T}y\|_1 = \sum_j |\sum_i B_{ij} y_i| \le \sum_i |y_i| \sum_j B_{ij} = \|y\|_1$. $\square$

**Theorem 1 (existence and uniqueness).** There is exactly one $p^* \in \Delta$ with $M^{\mathsf T} p^* = p^*$.

*Proof.* Let $T(p) = M^{\mathsf T}p$. By Lemma 1, $T$ maps $\Delta$ into itself. For $p, p' \in \Delta$, $y = p - p'$ has sum 0, so by Lemma 2 $\|T(p) - T(p')\|_1 \le (1 - d)\|p - p'\|_1$. Since $d > 0$, $T$ is a contraction of the closed set $\Delta$, and the Banach fixed point theorem gives exactly one fixed point. (Equivalently: all entries of $M$ are positive, so the chain is irreducible and aperiodic, and the Perron-Frobenius theorem gives the same conclusion. This is the argument of the paper.) $\square$

**Theorem 2 (rate and stopping rule).** Let $p_0 = (1/n, \ldots, 1/n)$ and $p_{t+1} = M^{\mathsf T}p_t$. Then $\|p_t - p^*\|_1 \le (1 - d)^t \|p_0 - p^*\|_1 \le 2(1 - d)^t$. If line L9 stops with $\delta = \|p_{t+1} - p_t\|_1$, then $\|p_{t+1} - p^*\|_1 \le \frac{1 - d}{d}\,\delta$.

*Proof.* Each $p_t \in \Delta$ by Lemma 1, so $p_t - p^*$ has sum 0, and Lemma 2 gives $\|p_{t+1} - p^*\|_1 = \|M^{\mathsf T}(p_t - p^*)\|_1 \le (1 - d)\|p_t - p^*\|_1$. Induction gives the first bound, and two distributions are at distance at most 2. For the second, let $e = \|p_{t+1} - p^*\|_1$; then $e \le (1 - d)\|p_t - p^*\|_1 \le (1 - d)(\delta + e)$, so $e\,d \le (1 - d)\delta$. $\square$

**Theorem 3 (degree centrality).** Let $A$ be symmetric and $d = 0$. Then $\pi_i = \deg_i / \sum_k \deg_k$, with $\deg_i = \sum_j A_{ij}$, satisfies $B^{\mathsf T}\pi = \pi$. If the graph of the nonzero entries of $A$ is connected, $\pi$ is the only stationary distribution, and the power method converges to it.

*Proof.* Let $D = \sum_k \deg_k$. Then $(B^{\mathsf T}\pi)_j = \sum_i \frac{A_{ij}}{\deg_i}\cdot\frac{\deg_i}{D} = \frac{1}{D}\sum_i A_{ji} = \frac{\deg_j}{D} = \pi_j$, using $A_{ij} = A_{ji}$. If the graph is connected, the chain $B$ is irreducible, and it is aperiodic because $B_{ii} > 0$. A finite irreducible aperiodic chain has a unique stationary distribution, and $B^{\mathsf T}$ applied $t$ times to any distribution tends to it as $t \to \infty$. $\blacksquare$

**Remark (isolated vertex).** If row $i$ of $A$ has only its diagonal entry and column $i$ has only its diagonal entry, the fixed point equation gives $p^*_i = \frac{d}{n} + (1 - d)p^*_i$, so $p^*_i = 1/n$ for any $d > 0$.

**Remark (output).** By Theorem 2 the returned vector is within $(1 - d)\delta/d$ of $p^*$ in the 1-norm, so two sentences whose exact scores differ by more than that bound are returned in the right order.
