---
title: The priority-sampling estimates are unbiased, with zero covariance and an unbiased variance estimate
proves: [correctness]
status: full
---

**Setting.** Items $1, \ldots, n$ have weights $w_i > 0$, and $n > k \ge 1$. Each item gets the priority $q_i = w_i / u_i$ with independent uniform $u_i \in (0, 1]$. Ties between priorities have probability 0. The sample is the set of the $k$ items of largest priority, and $\tau$ is the $(k+1)$-th largest priority. The estimate of item $i$ is $\hat w_i = \max(w_i, \tau)$ if $i$ is sampled and $\hat w_i = 0$ otherwise, and the variance estimate is $\hat v_i = \tau \max(0, \tau - w_i)$ if $i$ is sampled and $0$ otherwise. (For $n \le k$ every item is sampled with $\hat w_i = w_i$, which is exact.)

**Statement.**

1. $E[\hat w_i] = w_i$ for each $i$. Hence, for every set $I$ of items, $\sum_{i \in I} \hat w_i$ is an unbiased estimate of $\sum_{i \in I} w_i$.
2. If $k \ge 2$, then $E[\hat w_i \hat w_j] = w_i w_j$ for $i \ne j$, so the estimates have zero covariance and $\operatorname{Var}[\sum_{i \in I} \hat w_i] = \sum_{i \in I} \operatorname{Var}[\hat w_i]$.
3. $E[\hat v_i] = \operatorname{Var}[\hat w_i]$ for each $i$.

**A fact used throughout.** For a fixed $z > 0$, $\Pr[q_i > z] = \Pr[u_i < w_i / z] = \min(1, w_i / z)$.

**Proof of 1.** Fix $i$ and condition on the priorities $q_j$ of all items $j \ne i$. Let $\tau'$ be the $k$-th largest of them; there are $n - 1 \ge k$ of them, so $\tau'$ exists. Item $i$ is sampled exactly when fewer than $k$ other items have larger priority, that is, when $q_i > \tau'$. When it is sampled, the $(k+1)$-th largest priority of all items is the $k$-th largest among the others, so $\tau = \tau'$. Since $q_i$ is independent of the others,
$$E[\hat w_i \mid q_j, j \ne i] = \Pr[q_i > \tau'] \cdot \max(w_i, \tau') = \min\!\left(1, \frac{w_i}{\tau'}\right) \max(w_i, \tau') = w_i.$$
The last step checks two cases: if $w_i \ge \tau'$ both sides are $1 \cdot w_i$, and if $w_i < \tau'$ they are $\frac{w_i}{\tau'} \cdot \tau'$. Taking the expectation over the others gives $E[\hat w_i] = w_i$. Linearity of expectation gives the claim for sums.

**Proof of 2.** Fix $i \ne j$ and condition on the priorities of all other items. There are $n - 2 \ge k - 1 \ge 1$ of them. Let $\tau''$ be the $(k-1)$-th largest of them.

We claim that both $i$ and $j$ are sampled if and only if $q_i > \tau''$ and $q_j > \tau''$. If both are above $\tau''$, then above $q_i$ there are at most $k - 2$ of the other items and possibly $j$, so at most $k - 1$ items, and $i$ is sampled; the same holds for $j$. Conversely, say $q_i < \tau''$. Then $k - 1$ other items are above $q_i$. If $q_j > q_i$, then $k$ items are above $q_i$ and $i$ is not sampled. If $q_j < q_i$, then $k$ items are above $q_j$ and $j$ is not sampled. The case $q_j < \tau''$ is the same.

When both are sampled, the $(k+1)$-th largest priority of all items is the $(k-1)$-th largest of the others, so $\tau = \tau''$. Since $q_i$ and $q_j$ are independent of each other and of the others,
$$E[\hat w_i \hat w_j \mid \text{others}] = \Pr[q_i > \tau''] \max(w_i, \tau'') \cdot \Pr[q_j > \tau''] \max(w_j, \tau'') = w_i w_j,$$
by the same two cases as in part 1. Taking the expectation over the others gives $E[\hat w_i \hat w_j] = w_i w_j = E[\hat w_i]\,E[\hat w_j]$, so the covariance is 0, and the variance of a sum is the sum of the variances.

**Proof of 3.** Condition on the others as in part 1. Then
$$E[\hat w_i^2 \mid \text{others}] = \min\!\left(1, \frac{w_i}{\tau'}\right) \max(w_i, \tau')^2, \qquad E[\hat v_i \mid \text{others}] = \min\!\left(1, \frac{w_i}{\tau'}\right) \tau' \max(0, \tau' - w_i).$$
If $w_i \ge \tau'$, the first is $w_i^2$ and the second is 0. If $w_i < \tau'$, the first is $w_i \tau'$ and the second is $w_i(\tau' - w_i) = w_i \tau' - w_i^2$. In both cases $E[\hat v_i \mid \text{others}] = E[\hat w_i^2 \mid \text{others}] - w_i^2$. Taking expectations, $E[\hat v_i] = E[\hat w_i^2] - w_i^2 = \operatorname{Var}[\hat w_i]$, using part 1. $\blacksquare$
