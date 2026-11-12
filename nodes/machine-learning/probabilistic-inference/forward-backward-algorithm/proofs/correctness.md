---
title: The forward-backward algorithm computes the state and pair posteriors
proves: [correctness]
status: full
---

Fix the model $\lambda = (\pi, A, B)$ and the observations $O = o_1 \ldots o_T$ with $P(O) > 0$. For a path $Q = q_1 \ldots q_T$ the HMM gives the joint

$$P(Q, O) = \pi_{q_1} B_{q_1}(o_1) \prod_{s=2}^{T} A_{q_{s-1} q_s} B_{q_s}(o_s).$$

For $1 \le t \le T$ define the head and the tail of this product:

$$H_t(q_1, \ldots, q_t) = \pi_{q_1} B_{q_1}(o_1) \prod_{s=2}^{t} A_{q_{s-1} q_s} B_{q_s}(o_s), \qquad R_t(q_t, \ldots, q_T) = \prod_{s=t+1}^{T} A_{q_{s-1} q_s} B_{q_s}(o_s),$$

with $R_T = 1$ (an empty product). Then $P(Q, O) = H_t(q_1, \ldots, q_t) \, R_t(q_t, \ldots, q_T)$ for each $t$.

**Lemma 1 (forward).** $\alpha_t(i) = \sum H_t(q_1, \ldots, q_{t-1}, i)$, the sum over all $q_1, \ldots, q_{t-1}$.

*Proof.* The forward algorithm page proves that the forward recursion gives $\alpha_t(i) = P(o_{1:t}, q_t = i)$. Summing the joint over $q_{t+1}, \ldots, q_T$ and over $o_{t+1}, \ldots, o_T$ removes the tail, since each row of $A$ and of $B$ sums to 1, so $P(o_{1:t}, q_t = i)$ is the stated sum of heads. $\square$

**Lemma 2 (backward).** After lines L2 to L5, $\beta_t(i) = \sum R_t(i, q_{t+1}, \ldots, q_T)$, the sum over all $q_{t+1}, \ldots, q_T$.

*Proof.* By induction on $t$ from $T$ down to 1. For $t = T$, the sum has the single empty product 1, which is line L2. For $t < T$, split off the first factor of the tail:

$$R_t(i, q_{t+1}, \ldots, q_T) = A_{i q_{t+1}} B_{q_{t+1}}(o_{t+1}) \, R_{t+1}(q_{t+1}, \ldots, q_T).$$

Sum over $q_{t+2}, \ldots, q_T$ first; by the induction hypothesis this gives $A_{i j} B_j(o_{t+1}) \beta_{t+1}(j)$ with $j = q_{t+1}$. Then sum over $j$. This is line L5. $\square$

**Theorem 1.** Line L6 gives $\gamma_t(i) = P(q_t = i \mid O)$.

*Proof.* The sum of $P(Q, O)$ over the paths with $q_t = i$ is

$$\sum_{q_1, \ldots, q_{t-1}} \; \sum_{q_{t+1}, \ldots, q_T} H_t(q_1, \ldots, q_{t-1}, i) \, R_t(i, q_{t+1}, \ldots, q_T).$$

The first factor does not depend on the second group of variables and the second factor does not depend on the first group. By the distributive law the double sum is the product of the two single sums, which is $\alpha_t(i) \beta_t(i)$ by Lemmas 1 and 2. So $P(q_t = i, O) = \alpha_t(i) \beta_t(i)$. Line L1 computes $P = \sum_j \alpha_T(j) = P(O)$, and the definition of conditional probability gives $\gamma_t(i) = \alpha_t(i) \beta_t(i) / P(O)$. $\square$

**Theorem 2.** Line L7 gives $\xi_t(i, j) = P(q_t = i, q_{t+1} = j \mid O)$ for $1 \le t < T$.

*Proof.* For paths with $q_t = i$ and $q_{t+1} = j$, the joint splits into three factors:

$$P(Q, O) = H_t(q_1, \ldots, q_{t-1}, i) \cdot A_{ij} B_j(o_{t+1}) \cdot R_{t+1}(j, q_{t+2}, \ldots, q_T).$$

The middle factor is a constant, and the outer factors depend on disjoint groups of variables. The sum over both groups is $\alpha_t(i) \, A_{ij} B_j(o_{t+1}) \, \beta_{t+1}(j)$ by Lemmas 1 and 2. Divide by $P(O)$. $\square$

**Theorem 3 (scaled form).** Let $n_t = P(o_{1:t}) / P(o_{1:t-1})$ with $P(o_{1:0}) = 1$, and let $\hat\alpha_t(i) = \alpha_t(i) / P(o_{1:t})$ as on the forward algorithm page. Define $\hat\beta_T(i) = 1$ and $\hat\beta_t(i) = \frac{1}{n_{t+1}} \sum_j A_{ij} B_j(o_{t+1}) \hat\beta_{t+1}(j)$. Then $\hat\alpha_t(i) \hat\beta_t(i) = \gamma_t(i)$ and $\hat\alpha_t(i) A_{ij} B_j(o_{t+1}) \hat\beta_{t+1}(j) / n_{t+1} = \xi_t(i, j)$.

*Proof.* First, $\hat\beta_t(i) = \beta_t(i) / \prod_{s=t+1}^{T} n_s$ by induction from $t = T$ down: the case $t = T$ is the empty product, and the step follows from Lemma 2 and the linearity of line L5. The product of all the $n_s$ telescopes to $P(O)$, and $\prod_{s \le t} n_s = P(o_{1:t})$. So

$$\hat\alpha_t(i) \hat\beta_t(i) = \frac{\alpha_t(i) \beta_t(i)}{\prod_{s \le t} n_s \prod_{s > t} n_s} = \frac{\alpha_t(i) \beta_t(i)}{P(O)} = \gamma_t(i).$$

For the pairs, $\hat\alpha_t(i) \hat\beta_{t+1}(j) = \alpha_t(i) \beta_{t+1}(j) / \bigl(P(O) / n_{t+1}\bigr)$, since the denominator misses only $n_{t+1}$. Dividing by $n_{t+1}$ gives $\alpha_t(i) \beta_{t+1}(j) / P(O)$, and Theorem 2 finishes the proof. Each $n_t$ is positive because $P(o_{1:t}) \ge P(O) > 0$. $\blacksquare$
