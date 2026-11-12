---
title: The forward algorithm computes the likelihood of the observations
proves: [correctness]
status: full
---

We write $o_{1:t}$ for $o_1, \ldots, o_t$, and all probabilities are under the fixed model $\lambda = (\pi, A, B)$. The HMM has two conditional independences, which hold for each $t \ge 1$:

> **(H1)** $P(q_{t+1} = j \mid q_1, \ldots, q_t, o_{1:t}) = A_{q_t j}$: the next state depends only on the current state.
>
> **(H2)** $P(o_t = k \mid q_1, \ldots, q_t, o_{1:t-1}) = B_{q_t}(k)$: an observation depends only on the state at the same time.

**Lemma.** After line L1 and after the pass of line L2 for each $t$, $\alpha_t(j) = P(o_{1:t}, q_t = j)$ for each state $j$.

*Proof.* By induction on $t$.

*Base, $t = 1$.* Line L1 sets $\alpha_1(j) = \pi_j B_j(o_1)$. By the definition of $\pi$ and by (H2) with $t = 1$, $P(o_1, q_1 = j) = P(q_1 = j) P(o_1 \mid q_1 = j) = \pi_j B_j(o_1)$.

*Step.* Let $t \ge 2$ and assume the claim for $t - 1$. The events $\{q_{t-1} = i\}$ for $i = 1, \ldots, N$ partition the sample space, so

$$P(o_{1:t}, q_t = j) = \sum_{i=1}^{N} P(o_{1:t-1}, q_{t-1} = i, q_t = j, o_t).$$

By the chain rule each term is

$$P(o_{1:t-1}, q_{t-1} = i) \cdot P(q_t = j \mid q_{t-1} = i, o_{1:t-1}) \cdot P(o_t \mid q_t = j, q_{t-1} = i, o_{1:t-1}).$$

By (H1) at time $t - 1$, the probability of $q_t = j$ given $q_1, \ldots, q_{t-1}$ and $o_{1:t-1}$ is $A_{ij}$ for each value of $q_1, \ldots, q_{t-2}$ when $q_{t-1} = i$. The middle factor conditions on less information, so it is a weighted average of these equal numbers, and it is $A_{ij}$. In the same way, (H2) gives that the last factor is $B_j(o_t)$. By the induction hypothesis the first factor is $\alpha_{t-1}(i)$. So

$$P(o_{1:t}, q_t = j) = B_j(o_t) \sum_{i=1}^{N} \alpha_{t-1}(i) A_{ij}.$$

Lines L4 and L5 compute the sum in $s$, and line L6 multiplies it by $B_j(o_t)$, so $\alpha_t(j)$ has this value. $\square$

**Theorem.** FORWARD returns $P(O \mid \lambda)$.

*Proof.* The loop of line L2 runs for $t = 2, \ldots, T$ and stops, since each loop has a fixed range. By the lemma with $t = T$, $\alpha_T(j) = P(o_{1:T}, q_T = j)$. The events $\{q_T = j\}$ partition the sample space, so line L7 returns $\sum_j P(O, q_T = j) = P(O)$. $\square$

**Theorem (scaled form).** Assume $P(o_{1:t}) > 0$ for all $t \le T$. After step $t$ of FORWARD-SCALED, $\hat\alpha_t(j) = \alpha_t(j) / P(o_{1:t})$, $n_t = P(o_{1:t}) / P(o_{1:t-1})$ with $P(o_{1:0}) = 1$, and $\ell = \log P(o_{1:t})$.

*Proof.* By induction on $t$. For $t = 1$, line L9 gives $a(j) = \alpha_1(j)$, line L11 gives $n_1 = \sum_j \alpha_1(j) = P(o_1)$, and line L12 gives $\hat\alpha_1(j) = \alpha_1(j) / P(o_1)$. Line L13 sets $\ell = \log P(o_1)$.

For $t \ge 2$, the hypothesis gives $\hat\alpha_{t-1}(i) = \alpha_{t-1}(i) / P(o_{1:t-1})$. Line L10 is linear in $\hat\alpha_{t-1}$, so by the lemma

$$a(j) = \frac{1}{P(o_{1:t-1})} B_j(o_t) \sum_i \alpha_{t-1}(i) A_{ij} = \frac{\alpha_t(j)}{P(o_{1:t-1})}.$$

Line L11 gives $n_t = \sum_j \alpha_t(j) / P(o_{1:t-1}) = P(o_{1:t}) / P(o_{1:t-1})$, which is positive by the assumption. Line L12 gives $\hat\alpha_t(j) = a(j) / n_t = \alpha_t(j) / P(o_{1:t})$. Line L13 adds $\log n_t$ to $\ell = \log P(o_{1:t-1})$, which gives $\log P(o_{1:t})$. $\square$

With $t = T$, the scaled form returns $\log P(O)$. The value $\hat\alpha_t(j) = P(q_t = j \mid o_{1:t})$ is the filtered distribution, by the definition of conditional probability. If some $P(o_{1:t}) = 0$, then $n_t = 0$ at the first such $t$, and the implementation stops with $\log P(O) = -\infty$, which is correct because $P(O) \le P(o_{1:t}) = 0$. $\blacksquare$
