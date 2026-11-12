---
title: The CQL value lower bound with exact backups, and the tabular update
proves: [correctness]
status: full
---

We work with a finite MDP, discount $\gamma < 1$, a dataset $D$ with counts $n(s, a)$, $n(s) = \sum_a n(s, a)$, $N = |D|$, and the empirical behavior policy $\hat\pi_\beta(a \mid s) = n(s, a) / n(s)$. Episode ends are moves to an absorbing state of value 0, so $P^\pi$ below may be substochastic. We prove four facts used on the page.

**Claim 1 (the line L6 gradient).** For a fixed target table $\bar y$, the CQL(H) loss on the empirical distribution of $D$ is

$$J(Q) = \frac{1}{N} \sum_{i \in D} \Big[\alpha \Big(\log \sum_b e^{Q(s_i, b)} - Q(s_i, a_i)\Big) + \tfrac12 \big(Q(s_i, a_i) - y_i\big)^2\Big],$$

and $\partial J / \partial Q(s, a) = \frac{1}{N}\big[\alpha n(s) \sigma(s, a) - \alpha n(s, a) + n(s, a)(Q(s, a) - \bar y(s, a))\big]$, where $\bar y(s, a)$ is the mean of $y_i$ over the transitions at $(s, a)$.

*Proof.* The derivative of $\log \sum_b e^{Q(s, b)}$ with respect to $Q(s, a)$ is $\sigma(s, a)$; it appears once for each transition at state $s$, that is $n(s)$ times. The term $-Q(s_i, a_i)$ appears $n(s, a)$ times. The squared terms at $(s, a)$ give $\sum_{i \text{ at } (s, a)} (Q(s, a) - y_i) = n(s, a)(Q(s, a) - \bar y(s, a))$. $\square$

**Claim 2 (missing actions).** If $n(s) > 0$ and $n(s, a) = 0$, line L7 strictly lowers $Q(s, a)$ at every step, for any $\eta > 0$ and $\alpha > 0$. Tabular fitted Q-iteration never changes $Q(s, a)$ for such a pair.

*Proof.* By Claim 1, $g(s, a) = \alpha n(s) \sigma(s, a) / N$, and $\sigma(s, a) > 0$ because the softmax is positive. So $Q(s, a) - \eta g(s, a) < Q(s, a)$. Fitted Q-iteration sets each pair to the minimizer of its squared loss; a pair with no transitions has no terms in the loss, so the implementation keeps its value, and any other choice is not determined by the data. $\square$

In the example the true values of "left" are negative and its initial value is 0, so by Claim 2 fitted Q-iteration keeps an overestimate there forever, while CQL keeps lowering it.

**Claim 3 (the tabular evaluation update).** Fix a policy $\mu$ and suppose $\hat\pi_\beta(a \mid s) > 0$ for all pairs. The tabular minimizer of the equation 2 objective

$$\alpha \Big(\mathbb{E}_{s \sim D, a \sim \mu}[Q(s, a)] - \mathbb{E}_{s \sim D, a \sim \hat\pi_\beta}[Q(s, a)]\Big) + \tfrac12 \mathbb{E}_{s \sim D, a \sim \hat\pi_\beta}\big[(Q(s, a) - \hat{\mathcal B}^\mu \hat Q^k(s, a))^2\big]$$

is $Q(s, a) = \hat{\mathcal B}^\mu \hat Q^k(s, a) - \alpha \dfrac{\mu(a \mid s) - \hat\pi_\beta(a \mid s)}{\hat\pi_\beta(a \mid s)}$.

*Proof.* Write $d(s) = n(s)/N$. The objective is a sum over pairs of $d(s)\big[\alpha (\mu(a \mid s) - \hat\pi_\beta(a \mid s)) Q(s, a) + \tfrac12 \hat\pi_\beta(a \mid s) (Q(s, a) - \hat{\mathcal B}^\mu \hat Q^k(s, a))^2\big]$, a convex quadratic in each $Q(s, a)$ with positive leading coefficient. Setting the derivative to zero and dividing by $d(s) \hat\pi_\beta(a \mid s) > 0$ gives the formula. $\square$

This is the update in `cql_evaluate`, with $\mu = \pi$.

**Claim 4 (Theorem 3.2 with exact backups).** Suppose $\hat{\mathcal B}^\pi = \mathcal B^\pi$ (for example, deterministic transitions and rewards with every pair in $D$), $\hat\pi_\beta > 0$, $\mu = \pi$ and $\alpha \ge 0$. Then the update of Claim 3 has a unique fixed point $\hat Q$, and

$$\hat V(s) - V^\pi(s) = -\alpha \big[(I - \gamma P^\pi)^{-1} \Delta\big](s) \le 0, \qquad \Delta(s) = \sum_a \frac{\pi(a \mid s)^2}{\hat\pi_\beta(a \mid s)} - 1 \ge 0,$$

where $\hat V(s) = \sum_a \pi(a \mid s) \hat Q(s, a)$ and $P^\pi(s' \mid s) = \sum_a \pi(a \mid s) P(s' \mid s, a)$.

*Proof.* Let $c(s, a) = (\pi(a \mid s) - \hat\pi_\beta(a \mid s)) / \hat\pi_\beta(a \mid s)$. The update is $Q \mapsto \mathcal B^\pi Q - \alpha c$, a $\gamma$-contraction in the max norm because $\mathcal B^\pi$ is one and $\alpha c$ is a constant. So it has a unique fixed point $\hat Q$, and iterating converges to it.

Let $E = \hat Q - Q^\pi$. Since $Q^\pi = \mathcal B^\pi Q^\pi$ and $\mathcal B^\pi$ is affine with linear part $Q \mapsto \gamma P \Pi Q$, we get $E = \gamma P \Pi E - \alpha c$, where $(\Pi E)(s') = \sum_{a'} \pi(a' \mid s') E(s', a')$. Apply $\Pi$ to both sides. With $e = \Pi E = \hat V - V^\pi$, this gives $e = \gamma P^\pi e - \alpha \Pi c$, and $(\Pi c)(s) = \sum_a \pi(a \mid s)^2 / \hat\pi_\beta(a \mid s) - \sum_a \pi(a \mid s) = \Delta(s)$. The matrix $I - \gamma P^\pi$ is invertible because $P^\pi$ is substochastic and $\gamma < 1$, and $(I - \gamma P^\pi)^{-1} = \sum_{t \ge 0} \gamma^t (P^\pi)^t$ has nonnegative entries. So $e = -\alpha (I - \gamma P^\pi)^{-1} \Delta$.

It remains to show $\Delta \ge 0$. By the Cauchy-Schwarz inequality,

$$1 = \Big(\sum_a \pi(a \mid s)\Big)^2 = \Big(\sum_a \frac{\pi(a \mid s)}{\sqrt{\hat\pi_\beta(a \mid s)}} \sqrt{\hat\pi_\beta(a \mid s)}\Big)^2 \le \sum_a \frac{\pi(a \mid s)^2}{\hat\pi_\beta(a \mid s)} \cdot \sum_a \hat\pi_\beta(a \mid s) = \Delta(s) + 1.$$

Hence $\Delta(s) \ge 0$, so $e \le 0$ entrywise. $\square$

Equality holds in Cauchy-Schwarz only when $\pi(\cdot \mid s) = \hat\pi_\beta(\cdot \mid s)$, so the gap is zero exactly where the evaluated policy equals the behavior policy along its own visits, and grows with the chi-square divergence $\Delta$ between them. The single values need not be below $Q^\pi$: $E(s, a) = \gamma (P e)(s, a) - \alpha c(s, a)$, and $c(s, a) < 0$ wherever $\pi(a \mid s) < \hat\pi_\beta(a \mid s)$, so $E(s, a)$ can be positive there. This is why the paper states Theorem 3.2 for $\hat V$ only.

**What is not proved here.** The paper's Theorems 3.1 and 3.2 also cover $\hat{\mathcal B}^\pi \ne \mathcal B^\pi$, with a concentration term that needs $\alpha$ large enough; we do not reprove that term. Theorems 3.3 and 3.4 (CQL(H) with policy updates) and the safe policy improvement result of Section 3.3 are cited, not proved. For the max backup used at line L3, the inner loop converges to $Q(s, a) = \bar y(s, a) + \alpha (1 - n(s)\sigma(s, a) / n(s, a))$ on seen pairs, which can lie above the true value, as the example shows. $\blacksquare$
