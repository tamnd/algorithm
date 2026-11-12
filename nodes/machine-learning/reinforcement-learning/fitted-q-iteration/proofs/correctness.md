---
title: Tabular FQI is value iteration on the empirical MDP, and FQI with an averager converges
proves: [correctness]
status: full
---

We use the notation of the page. The data are $n$ transitions $(s_i, a_i, r_i, s'_i)$, with $s'_i$ terminal when the episode ends there. For a function $Q$ define the target $y_i(Q) = r_i$ if $s'_i$ is terminal and $y_i(Q) = r_i + \gamma\max_b Q(s'_i, b)$ otherwise. Line L5 computes $y_i(Q_{k-1})$, and line L7 sets $Q_k = \text{REGRESS}(\{((s_i, a_i), y_i(Q_{k-1}))\})$.

**Theorem 1 (tabular regressor).** Let REGRESS return, at each pair $(s, a)$ that occurs in the data, the mean of the targets with input $(s, a)$, and $0$ at other pairs. Let $n(s, a)$ be the number of transitions from $(s, a)$, and define the empirical MDP by $\hat{R}(s, a) = \frac{1}{n(s, a)}\sum_{i : (s_i, a_i) = (s, a)} r_i$ and $\hat{P}(s' \mid s, a) = \frac{1}{n(s, a)}\#\{i : (s_i, a_i) = (s, a), s'_i = s'\}$ for nonterminal $s'$. Let $\hat{Q}_0 = 0$ and $\hat{Q}_k(s, a) = \hat{R}(s, a) + \gamma\sum_{s'}\hat{P}(s' \mid s, a)\max_b\hat{Q}_{k-1}(s', b)$ at pairs in the data, and $\hat{Q}_k = 0$ at other pairs. Then $Q_k = \hat{Q}_k$ for every $k$.

*Proof.* By induction on $k$. Both are $0$ at $k = 0$ (line L1). Assume $Q_{k-1} = \hat{Q}_{k-1}$. At a pair $(s, a)$ that is not in the data, both are $0$ by definition. At a pair in the data,

$$Q_k(s, a) = \frac{1}{n(s, a)}\sum_{i : (s_i, a_i) = (s, a)} y_i(Q_{k-1}) = \hat{R}(s, a) + \frac{\gamma}{n(s, a)}\sum_{i : (s_i, a_i) = (s, a),\ s'_i \text{ not terminal}}\max_b Q_{k-1}(s'_i, b).$$

Group the last sum by the value of $s'_i$. Each nonterminal $s'$ appears $n(s, a)\hat{P}(s' \mid s, a)$ times, so the sum is $\gamma\sum_{s'}\hat{P}(s' \mid s, a)\max_b Q_{k-1}(s', b) = \gamma\sum_{s'}\hat{P}(s' \mid s, a)\max_b\hat{Q}_{k-1}(s', b)$. So $Q_k(s, a) = \hat{Q}_k(s, a)$. $\square$

So tabular FQI is [value iteration](/value-iteration/) on the maximum likelihood model, and it converges to the optimal $Q$ of that model at rate $\gamma^k$ by the [Bellman contraction](/bellman-contraction/).

**Theorem 2 (averagers).** Call REGRESS an averager if for every input $x$ there are weights $w_i(x) \ge 0$ with $\sum_i w_i(x) = 1$, which depend on $x$ and on the inputs $(s_i, a_i)$ but not on the targets, such that $\text{REGRESS}(\{((s_i, a_i), y_i)\})(x) = \sum_i w_i(x) y_i$. The $k$-nearest-neighbor average, kernel averages with nonnegative kernels, and a regression tree whose structure is fixed are averagers. If REGRESS is an averager, the map $H$ with $Q_k = H Q_{k-1}$ satisfies $\|HQ - HQ'\|_\infty \le \gamma\|Q - Q'\|_\infty$. So $Q_k$ converges to the unique fixed point $Q_H$ of $H$, and $\|Q_k - Q_H\|_\infty \le \gamma^k\|Q_0 - Q_H\|_\infty$.

*Proof.* For each $i$, $|y_i(Q) - y_i(Q')| \le \gamma|\max_b Q(s'_i, b) - \max_b Q'(s'_i, b)| \le \gamma\max_b|Q(s'_i, b) - Q'(s'_i, b)| \le \gamma\|Q - Q'\|_\infty$, and it is $0$ for terminal $s'_i$. At any $x$,

$$|HQ(x) - HQ'(x)| = \Big|\sum_i w_i(x)\big(y_i(Q) - y_i(Q')\big)\Big| \le \sum_i w_i(x)\,\gamma\|Q - Q'\|_\infty = \gamma\|Q - Q'\|_\infty.$$

The space of bounded functions with the sup norm is complete, so the Banach fixed point theorem gives the fixed point and the rate. $\square$

**Theorem 3 (approximate value iteration).** Let $T$ be the Bellman optimality operator of the true MDP, with fixed point $Q^*$. If $\|Q_k - TQ_{k-1}\|_\infty \le \epsilon$ for every $k \le K$, then

$$\|Q_K - Q^*\|_\infty \le \gamma^K\|Q_0 - Q^*\|_\infty + \frac{\epsilon}{1 - \gamma},$$

and the greedy policy $\pi_K$ of $Q_K$ satisfies $\|V^* - V^{\pi_K}\|_\infty \le \frac{2}{1 - \gamma}\|Q_K - Q^*\|_\infty$.

*Proof.* $\|Q_k - Q^*\|_\infty \le \|Q_k - TQ_{k-1}\|_\infty + \|TQ_{k-1} - TQ^*\|_\infty \le \epsilon + \gamma\|Q_{k-1} - Q^*\|_\infty$, since $T$ is a $\gamma$-contraction and $TQ^* = Q^*$. Unrolling $K$ times gives $\gamma^K\|Q_0 - Q^*\|_\infty + \epsilon(1 + \gamma + \cdots + \gamma^{K-1})$, which is at most the bound.

For the policy, let $\delta = \|Q_K - Q^*\|_\infty$ and $a = \pi_K(s)$. Then $Q^*(s, a) \ge Q_K(s, a) - \delta \ge Q_K(s, a^*) - \delta \ge Q^*(s, a^*) - 2\delta = V^*(s) - 2\delta$ for an optimal action $a^*$. Let $T^{\pi_K}$ be the Bellman expectation operator of $\pi_K$ on state values. Then $T^{\pi_K}V^*(s) = Q^*(s, \pi_K(s)) \ge V^*(s) - 2\delta$. So $V^* - V^{\pi_K} = V^* - T^{\pi_K}V^* + T^{\pi_K}V^* - T^{\pi_K}V^{\pi_K}$, and its sup norm is at most $2\delta + \gamma\|V^* - V^{\pi_K}\|_\infty$, which gives $\|V^* - V^{\pi_K}\|_\infty \le 2\delta/(1 - \gamma)$. $\square$

The error $\epsilon$ in Theorem 3 combines the sampling error, which shrinks as the data grow, and the bias of the function class, which does not. Munos and Szepesvári (2008) give bounds of this kind in weighted $L^p$ norms with sample sizes.
