---
title: The Retrace operator is a gamma-contraction with fixed point Q^pi
proves: [correctness]
status: full
---

We use the notation of the page. The MDP has finitely many states and actions and $\gamma < 1$. A trajectory $x_0, a_0, r_0, x_1, a_1, r_1, \ldots$ starts from a pair $(x_0, a_0)$ and then follows the behavior policy $\mu$. Write $\mathbb{E}_\pi Q(x, \cdot) = \sum_b \pi(b \mid x)Q(x, b)$, $\delta_t = r_t + \gamma\mathbb{E}_\pi Q(x_{t+1}, \cdot) - Q(x_t, a_t)$, and $c_s = c(x_s, a_s)$ for a trace function $c \ge 0$. The general operator is

$$\mathcal{R}Q(x, a) = Q(x, a) + \mathbb{E}_\mu\Big[\sum_{t \ge 0}\gamma^t\Big(\prod_{s=1}^{t}c_s\Big)\delta_t \;\Big|\; x_0 = x, a_0 = a\Big].$$

Retrace is the case $c(x, a) = \lambda\min(1, \pi(a \mid x)/\mu(a \mid x))$ with $\lambda \in [0, 1]$.

**Lemma 1 (the sample target).** For a trajectory that ends at step $T$, the backward recursion of lines L1 to L5 gives $y_t = Q(x_t, a_t) + \sum_{s=t}^{T-1}\gamma^{s-t}\big(\prod_{i=t+1}^{s}c_i\big)\delta_s$, where $\delta_{T-1}$ uses $\mathbb{E}_\pi Q(x_T, \cdot)$, or $0$ if $x_T$ is terminal.

*Proof.* Line L5 sets $g_t = \mathbb{E}_\pi Q(x_t, \cdot) + c_t(y_t - Q(x_t, a_t))$, and line L3 sets $y_{t-1} = r_{t-1} + \gamma g_t$. So $y_{t-1} - Q(x_{t-1}, a_{t-1}) = \delta_{t-1} + \gamma c_t(y_t - Q(x_t, a_t))$. At the last step, $y_{T-1} - Q(x_{T-1}, a_{T-1}) = \delta_{T-1}$ by line L1. Unrolling the recursion gives the sum. $\square$

So the mean of $y_0$ over trajectories from $(x, a)$ is $\mathcal{R}Q(x, a)$; for episodic tasks the sum stops at the end of the episode. In matrix form, with $P^{c\mu}((x, a), (y, b)) = P(y \mid x, a)\mu(b \mid y)c(y, b)$ and $T^\pi Q = r + \gamma P^\pi Q$,

$$\mathcal{R}Q = Q + (I - \gamma P^{c\mu})^{-1}(T^\pi Q - Q).$$

**Theorem 1 (Munos, Stepleton, Harutyunyan and Bellemare 2016).** If $0 \le c(x, a) \le \pi(a \mid x)/\mu(a \mid x)$ for all $(x, a)$ with $\mu(a \mid x) > 0$, then $\|\mathcal{R}Q - Q^\pi\|_\infty \le \gamma\|Q - Q^\pi\|_\infty$ for every $Q$. So $Q^\pi$ is the unique fixed point of $\mathcal{R}$, and the iterates $\mathcal{R}^kQ$ converge to it at rate $\gamma^k$.

*Proof.* The condition gives $\sum_b \mu(b \mid x)c(x, b) \le \sum_b \pi(b \mid x) = 1$ at every $x$. So $e_t = \mathbb{E}_\mu[c_1 \cdots c_t] \le 1$ for all $t$, with $e_0 = 1$, and the series in $\mathcal{R}Q$ converges absolutely.

Let $\Delta = Q - Q^\pi$. The Bellman equation $Q^\pi(x_t, a_t) = \mathbb{E}[r_t + \gamma\mathbb{E}_\pi Q^\pi(x_{t+1}, \cdot) \mid x_t, a_t]$ gives

$$\mathbb{E}[\delta_t \mid x_0, a_0, \ldots, x_t, a_t] = \mathbb{E}[\gamma\mathbb{E}_\pi\Delta(x_{t+1}, \cdot) \mid x_t, a_t] - \Delta(x_t, a_t).$$

The products $c_1 \cdots c_t$ depend only on the history up to $(x_t, a_t)$, so

$$\mathcal{R}Q - Q^\pi = \Delta + \sum_{t \ge 0}\gamma^t\,\mathbb{E}_\mu\Big[c_1 \cdots c_t\big(\gamma\mathbb{E}_\pi\Delta(x_{t+1}, \cdot) - \Delta(x_t, a_t)\big)\Big].$$

The term $-\Delta(x_0, a_0)$ for $t = 0$ cancels the first $\Delta$. Shift the index of the positive terms by one and condition on $x_t$:

$$\mathcal{R}Q - Q^\pi = \sum_{t \ge 1}\gamma^t\,\mathbb{E}_\mu\Big[c_1 \cdots c_{t-1}\sum_b\big(\pi(b \mid x_t) - \mu(b \mid x_t)c(x_t, b)\big)\Delta(x_t, b)\Big].$$

The condition on $c$ makes every weight $\pi(b \mid x_t) - \mu(b \mid x_t)c(x_t, b)$ nonnegative, so $|\mathcal{R}Q - Q^\pi|$ is at most $\|\Delta\|_\infty$ times the sum of the weights:

$$\sum_{t \ge 1}\gamma^t\,\mathbb{E}_\mu\big[c_1 \cdots c_{t-1}(1 - c_t)\big] = \sum_{t \ge 1}\gamma^t(e_{t-1} - e_t) = \gamma - (1 - \gamma)\sum_{t \ge 1}\gamma^t e_t \le \gamma.$$

So $\|\mathcal{R}Q - Q^\pi\|_\infty \le \gamma\|\Delta\|_\infty$. If $Q'$ is a fixed point, then $\|Q' - Q^\pi\|_\infty \le \gamma\|Q' - Q^\pi\|_\infty$, so $Q' = Q^\pi$. $\square$

The proof gives a sharper rate, $\gamma - (1 - \gamma)\sum_{t \ge 1}\gamma^te_t$: the longer the traces, the faster the contraction. On-policy with $\lambda = 1$, Retrace has $c = 1$, so $e_t = 1$ and the rate is $\gamma - \gamma = 0$: one application of $\mathcal{R}$ gives $Q^\pi$.

**Corollary (the three trace choices).** Retrace satisfies the condition, since $\lambda\min(1, \pi/\mu) \le \pi/\mu$. Tree Backup, $c = \lambda\pi(a \mid x)$, satisfies it because $\mu \le 1$. Importance sampling, $c = \lambda\pi/\mu$, satisfies it, but the products $c_1 \cdots c_t$ are unbounded, so the sample targets can have very large variance. $Q^\pi(\lambda)$, $c = \lambda$, violates it wherever $\mu(a \mid x)\lambda > \pi(a \mid x)$; then some weights are negative and the bound fails. Harutyunyan, Bellemare, Stepleton and Munos (2016) prove that $Q^\pi(\lambda)$ is still a contraction when $\lambda < (1 - \gamma)/(\gamma\epsilon)$ with $\epsilon = \max_x\|\pi(\cdot \mid x) - \mu(\cdot \mid x)\|_1$, and the example on the page shows that it can diverge when $\lambda$ is large.
