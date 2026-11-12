---
title: The V-trace operator contracts to the value of pi_rho_bar, and on-policy V-trace is the n-step return
proves: [correctness]
status: full
---

We use the notation of the page. The MDP has finitely many states and actions and $\gamma < 1$. A trajectory $x_0, a_0, r_0, x_1, \ldots$ follows $\mu$. The truncated ratios are $\rho_t = \min(\bar{\rho}, \pi(a_t \mid x_t)/\mu(a_t \mid x_t))$ and $c_t = \min(\bar{c}, \pi(a_t \mid x_t)/\mu(a_t \mid x_t))$ with $\bar{c} \le \bar{\rho}$, so $c_t \le \rho_t$. Write $C_t = c_0 c_1 \cdots c_{t-1}$, with $C_0 = 1$. The V-trace operator of Espeholt et al. (2018) is

$$\mathcal{R}V(x) = V(x) + \mathbb{E}_\mu\Big[\sum_{t \ge 0}\gamma^tC_t\rho_t\big(r_t + \gamma V(x_{t+1}) - V(x_t)\big) \;\Big|\; x_0 = x\Big].$$

**Lemma 1 (the sample target).** For an $n$-step trajectory, lines L1 to L5 give $v_s = V(x_s) + \sum_{t=s}^{s+n-1}\gamma^{t-s}\big(\prod_{i=s}^{t-1}c_i\big)\delta_t$ with $\delta_t = \rho_t(r_t + \gamma V(x_{t+1}) - V(x_t))$, the definition of the $n$-step V-trace target.

*Proof.* Line L5 is $v_t - V(x_t) = \delta_t + \gamma c_t(v_{t+1} - V(x_{t+1}))$, and $v_{s+n} - V(x_{s+n}) = 0$ by line L1. Unroll the recursion from $t = s$. $\square$

So the mean of $v_0$ over infinitely long trajectories from $x$ is $\mathcal{R}V(x)$. In matrix form, $\mathcal{R}V = V + (I - \gamma P^{c})^{-1}g$ with $P^{c}(x, y) = \sum_a \mu(a \mid x)c(x, a)P(y \mid x, a)$ and $g(x) = \sum_a \mu(a \mid x)\rho(x, a)\big(\bar{r}(x, a) + \gamma\sum_y P(y \mid x, a)V(y) - V(x)\big)$.

**Theorem 1 (Espeholt et al. 2018, Theorem 1).** Let $\pi_{\bar{\rho}}(a \mid x) = \min(\bar{\rho}\mu(a \mid x), \pi(a \mid x))/\sum_b\min(\bar{\rho}\mu(b \mid x), \pi(b \mid x))$, and let $\beta = \min_x\mathbb{E}_\mu[\rho_0 \mid x_0 = x] > 0$. Then $\|\mathcal{R}V_1 - \mathcal{R}V_2\|_\infty \le (1 - (1 - \gamma)\beta)\|V_1 - V_2\|_\infty$, and the unique fixed point of $\mathcal{R}$ is $V^{\pi_{\bar{\rho}}}$. It does not depend on $\bar{c}$.

*Proof.* *Rewriting.* In the sum, the term $-\gamma^tC_t\rho_tV(x_t)$ for $t \ge 1$ pairs with the term $\gamma^{t}C_{t-1}\rho_{t-1}V(x_t)$ from step $t - 1$, and $C_t = C_{t-1}c_{t-1}$. Collecting the coefficient of each $V(x_t)$ gives

$$\mathcal{R}V(x) = \big(1 - \mathbb{E}_\mu\rho_0\big)V(x) + \mathbb{E}_\mu\Big[\sum_{t \ge 0}\gamma^tC_t\Big(\rho_tr_t + \gamma\big(\rho_t - c_t\rho_{t+1}\big)V(x_{t+1})\Big)\Big].$$

*Nonnegative weights.* Let $\Delta = V_1 - V_2$. Then

$$\mathcal{R}V_1(x) - \mathcal{R}V_2(x) = \big(1 - \mathbb{E}_\mu\rho_0\big)\Delta(x) + \sum_{t \ge 0}\gamma^{t+1}\,\mathbb{E}_\mu\big[C_t\big(\rho_t - c_t\rho_{t+1}\big)\Delta(x_{t+1})\big].$$

Since $\rho_0 \le \pi(a_0 \mid x)/\mu(a_0 \mid x)$, $\mathbb{E}_\mu\rho_0 \le \sum_a\pi(a \mid x) = 1$, so the first weight is nonnegative. Given the history up to $x_{t+1}$, the same argument gives $\mathbb{E}[\rho_{t+1} \mid x_{t+1}] \le 1$, so the conditional weight of $\Delta(x_{t+1})$ is $C_t(\rho_t - c_t\mathbb{E}[\rho_{t+1} \mid x_{t+1}]) \ge C_t(\rho_t - c_t) \ge 0$.

*The sum of the weights.* Let $b_t = \mathbb{E}_\mu[C_t\rho_t]$. Since $C_tc_t = C_{t+1}$, $\mathbb{E}_\mu[C_tc_t\rho_{t+1}] = b_{t+1}$, and the weights sum to

$$1 - b_0 + \sum_{t \ge 0}\gamma^{t+1}(b_t - b_{t+1}) = 1 - (1 - \gamma)\sum_{t \ge 0}\gamma^tb_t \le 1 - (1 - \gamma)b_0 \le 1 - (1 - \gamma)\beta.$$

So $|\mathcal{R}V_1(x) - \mathcal{R}V_2(x)| \le (1 - (1 - \gamma)\beta)\|\Delta\|_\infty$ at every $x$.

*The fixed point.* Let $N(x) = \sum_b\min(\bar{\rho}\mu(b \mid x), \pi(b \mid x))$. Since $\mu(a \mid x)\min(\bar{\rho}, \pi(a \mid x)/\mu(a \mid x)) = \min(\bar{\rho}\mu(a \mid x), \pi(a \mid x)) = N(x)\pi_{\bar{\rho}}(a \mid x)$,

$$\mathbb{E}_\mu\big[\rho_t(r_t + \gamma V(x_{t+1}) - V(x_t)) \mid x_t\big] = N(x_t)\big(T^{\pi_{\bar{\rho}}}V - V\big)(x_t),$$

where $T^{\pi_{\bar{\rho}}}$ is the Bellman expectation operator of $\pi_{\bar{\rho}}$. The factor $C_t$ depends only on the history before $a_t$, so every term of the sum has mean $0$ when $V = V^{\pi_{\bar{\rho}}}$. So $\mathcal{R}V^{\pi_{\bar{\rho}}} = V^{\pi_{\bar{\rho}}}$, and by the contraction it is the only fixed point. The traces $c_t$ never appear in this argument, so the fixed point does not depend on $\bar{c}$. $\square$

For $\bar{\rho} \ge \max_{x, a}\pi(a \mid x)/\mu(a \mid x)$, $\pi_{\bar{\rho}} = \pi$ and the fixed point is $V^\pi$. For $\bar{\rho} \le \min\pi(a \mid x)/\mu(a \mid x)$ over the pairs with $\pi > 0$, and $\pi > 0$ wherever $\mu > 0$, $\pi_{\bar{\rho}} = \mu$ and the fixed point is $V^\mu$.

**Theorem 2 (on-policy).** If $\pi = \mu$, $\bar{\rho} \ge 1$ and $\bar{c} \ge 1$, the $n$-step V-trace target is the $n$-step return: $v_s = \sum_{t=s}^{s+n-1}\gamma^{t-s}r_t + \gamma^nV(x_{s+n})$.

*Proof.* All ratios are $1$, so $\rho_t = c_t = 1$. By Lemma 1, $v_s = V(x_s) + \sum_{t=s}^{s+n-1}\gamma^{t-s}(r_t + \gamma V(x_{t+1}) - V(x_t))$. The values telescope: $\sum_{t=s}^{s+n-1}\gamma^{t-s}(\gamma V(x_{t+1}) - V(x_t)) = \gamma^nV(x_{s+n}) - V(x_s)$. $\square$

With an extra trace parameter, $c_t = \lambda\min(\bar{c}, \pi/\mu)$, the on-policy target is the truncated $\lambda$-return of [TD($\lambda$)](/td-lambda/). Espeholt et al. (2018, Theorem 2) also prove that the online tabular update converges almost surely to $V^{\pi_{\bar{\rho}}}$ under the [Robbins-Monro conditions](/robbins-monro-conditions/).
