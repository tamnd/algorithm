---
title: Deleted interpolation gives distributions, and its EM steps never lower the held-out likelihood
proves: [correctness]
status: full
---

Fix one bucket $b$ with $J$ components and its rows $p^{(1)}, \ldots, p^{(M)}$, $M \ge 1$, from line L3, where $p^{(t)}_i \ge 0$ is the value of component $i$ on held-out token $t$. The last component is the uniform one, so $p^{(t)}_J = 1/|V| > 0$ for every $t$. The buckets do not share weights, so it is enough to treat one bucket. Let $\Delta = \{\lambda \in \mathbb{R}^J : \lambda_i \ge 0, \sum_i \lambda_i = 1\}$ and

$$L(\lambda) = \sum_{t=1}^{M} \log z_t(\lambda), \qquad z_t(\lambda) = \sum_{i=1}^{J} \lambda_i p^{(t)}_i .$$

**Lemma 1 (the step stays in the simplex).** If $\lambda \in \Delta$ and $\lambda_J > 0$, then every $z_t(\lambda) > 0$, the step of lines L6 and L7 gives $\lambda' \in \Delta$, and $\lambda'_J > 0$. If $\lambda_i = 0$ then $\lambda'_i = 0$.

*Proof.* $z_t \ge \lambda_J / |V| > 0$. Let $r_{ti} = \lambda_i p^{(t)}_i / z_t \ge 0$. Then $\sum_i r_{ti} = 1$ for each $t$, and line L7 sets $\lambda'_i = \frac1M \sum_t r_{ti}$, so $\lambda'_i \ge 0$ and $\sum_i \lambda'_i = \frac1M \sum_t 1 = 1$. Also $r_{tJ} > 0$ for every $t$, so $\lambda'_J > 0$. If $\lambda_i = 0$, every $r_{ti} = 0$ and $\lambda'_i = 0$. $\square$

By Lemma 1 and line L4, which starts with all weights equal to $1/J$, every iterate has $\lambda_J > 0$ and so all $z_t > 0$ and $L$ is finite.

**Theorem 2 (monotone likelihood).** With $\lambda$ and $\lambda'$ as in Lemma 1, $L(\lambda') - L(\lambda) \ge M \, D(\lambda' \,\|\, \lambda) \ge 0$, where $D(\lambda' \| \lambda) = \sum_{i : \lambda'_i > 0} \lambda'_i \log(\lambda'_i / \lambda_i)$.

*Proof.* Fix $t$. For each $i$ with $r_{ti} > 0$ we have $\lambda_i > 0$, and

$$\frac{z_t(\lambda')}{z_t(\lambda)} = \sum_i \frac{\lambda'_i p^{(t)}_i}{z_t(\lambda)} \ge \sum_{i : r_{ti} > 0} r_{ti} \frac{\lambda'_i}{\lambda_i}.$$

The weights $r_{ti}$ over the $i$ with $r_{ti} > 0$ sum to 1, and $\log$ is concave, so by Jensen's inequality

$$\log \frac{z_t(\lambda')}{z_t(\lambda)} \ge \sum_{i : r_{ti} > 0} r_{ti} \log \frac{\lambda'_i}{\lambda_i}.$$

If $r_{ti} > 0$ then $\lambda'_i > 0$, so each logarithm is finite. Sum over $t$ and use $\sum_t r_{ti} = M \lambda'_i$:

$$L(\lambda') - L(\lambda) \ge \sum_{i : \lambda'_i > 0} M \lambda'_i \log \frac{\lambda'_i}{\lambda_i} = M \, D(\lambda' \| \lambda).$$

$D(\lambda' \| \lambda) \ge 0$ by Gibbs' inequality: $-D = \sum_{i : \lambda'_i > 0} \lambda'_i \log(\lambda_i / \lambda'_i) \le \log \sum_{i : \lambda'_i > 0} \lambda_i \le \log 1 = 0$, again by Jensen. $\square$

So the sequence $L(\lambda^{(0)}) \le L(\lambda^{(1)}) \le \cdots$ does not decrease. It is bounded above by 0, since each $z_t \le \max_i p^{(t)}_i \le 1$, so it converges, and the test of line L8 is met after finitely many steps for any positive tolerance.

**Theorem 3 (the fixed points are optima).** $L$ is concave on $\Delta$. A point $\lambda \in \Delta$ with $\lambda_J > 0$ maximizes $L$ over $\Delta$ if and only if $g_i(\lambda) = \frac1M \sum_t p^{(t)}_i / z_t(\lambda)$ equals 1 for every $i$ with $\lambda_i > 0$ and is at most 1 for every other $i$. Every fixed point of the EM step with all $\lambda_i > 0$ is such a maximum.

*Proof.* Each $z_t$ is linear in $\lambda$ and $\log$ is concave and increasing, so $\log z_t$ is concave, and so is the sum $L$. $L$ is differentiable on the open set where all $z_t > 0$, which contains $\lambda$. For a concave differentiable function on the convex set $\Delta$, the point $\lambda$ is a maximum if and only if $\nabla L(\lambda) \cdot (\mu - \lambda) \le 0$ for every $\mu \in \Delta$. The partial derivatives are $\partial L / \partial \lambda_i = M g_i$, and $\nabla L(\lambda) \cdot \lambda = \sum_t z_t / z_t = M$. Taking $\mu$ to be the vertices of $\Delta$, the condition is $M g_i \le M$, that is $g_i \le 1$, for every $i$; it then holds for every $\mu$ by linearity. Since $\sum_i \lambda_i g_i = 1$ and each $g_i \le 1$, equality $g_i = 1$ must hold for every $i$ with $\lambda_i > 0$. This is the stated condition.

The EM step can be written $\lambda'_i = \lambda_i g_i(\lambda)$. At a fixed point with all $\lambda_i > 0$, $g_i = 1$ for every $i$, which is the condition above. $\blacksquare$

**Theorem 4 (the final model).** For every history $h$, $P(\cdot \mid h)$ of line L9 is a distribution on $V$, and $P(w \mid h) > 0$ for every $w \in V$ if the bucket of $h$ has $\lambda_{b,\mathrm{u}} > 0$ or no fitted weights.

*Proof.* For $j \le m(h)$, $c(h_j) > 0$ and every token counted after $h_j$ is in $V$, so $\sum_{w \in V} c(h_j w)/c(h_j) = 1$. The uniform component sums to 1. The weights of the bucket lie in $\Delta$ by Lemma 1, or are all equal to $1/J$ for a bucket with no held-out rows. A convex combination of distributions on $V$ is a distribution on $V$, and it is positive where a component with positive weight is positive; the uniform component is positive everywhere. $\blacksquare$
