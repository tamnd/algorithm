---
title: The frozen Wang-Landau walk has a flat energy histogram exactly when ĝ ∝ g, and ln g is the only and stable fixed point of the mean motion
proves: [correctness]
status: full
---

**Setting.** $\mathcal{X}$ is a finite set of states, $E : \mathcal{X} \to \{e_1, \dots, e_N\}$ takes every level, and $g(e) = |\{x : E(x) = e\}| > 0$. The proposal $q$ is symmetric, $q(x, y) = q(y, x)$, and the graph of its positive entries is connected. For $\theta \in \mathbb{R}^N$ (the current $\ln\hat g$) write $\pi_\theta(x) = e^{-\theta_{E(x)}}/Z_\theta$ with $Z_\theta = \sum_jg(e_j)e^{-\theta_j}$.

**Step 1: the frozen walk is Metropolis for $\pi_\theta$.** With $\theta$ fixed, lines L3 and L4 move from $x$ to $y \ne x$ with probability $P(x, y) = q(x, y)\min(1, e^{\theta_{E(x)} - \theta_{E(y)}})$. Then

$$\pi_\theta(x)P(x, y) = \frac{q(x, y)}{Z_\theta}\min\big(e^{-\theta_{E(x)}}, e^{-\theta_{E(y)}}\big),$$

which is symmetric in $x$ and $y$ because $q$ is. So $P$ satisfies detailed balance and keeps $\pi_\theta$. It is irreducible, because $q$ connects all states and every acceptance probability is positive.

**Step 2: the law of the energy.** Under $\pi_\theta$,

$$p_\theta(e_j) = \pi_\theta(E = e_j) = \frac{g(e_j)e^{-\theta_j}}{Z_\theta}.$$

This equals $1/N$ for every $j$ if and only if $g(e_j)e^{-\theta_j}$ is the same for all $j$, that is, $\theta_j = \ln g(e_j) + c$ for one constant $c$. So the frozen walk has a flat energy histogram in the long run if and only if $\hat g$ is proportional to $g$. The ergodic theorem for the irreducible chain of Step 1 turns this into a statement about visit frequencies.

**Step 3: the mean motion.** In line L5 the level $e_j$ gets the increment $\ln f$ with frequency close to $p_\theta(e_j)$ while $\theta$ changes slowly. A common shift of all $\theta_j$ does not change $\pi_\theta$, so we remove it and study

$$\dot\theta_j = h_j(\theta) = p_\theta(e_j) - \frac1N.$$

By Step 2, $h(\theta) = 0$ if and only if $\theta = \ln g + c\mathbf 1$.

**Step 4: a Lyapunov function.** Let $V(\theta) = \ln Z_\theta + \frac1N\sum_j\theta_j$. Then

$$\frac{\partial V}{\partial\theta_j} = -\frac{g(e_j)e^{-\theta_j}}{Z_\theta} + \frac1N = -h_j(\theta).$$

Along a solution, $\frac{d}{dt}V(\theta(t)) = \sum_j\frac{\partial V}{\partial\theta_j}h_j = -\sum_jh_j(\theta)^2 \le 0$, with equality only at the fixed points. $V$ is convex, because $\ln Z_\theta$ is a log-sum-exp of linear functions of $\theta$, and it does not change under $\theta \mapsto \theta + c\mathbf 1$. On the subspace $\sum_j\theta_j = 0$ it is strictly convex and tends to $+\infty$ as $|\theta| \to \infty$: if $\max_j\theta_j - \min_j\theta_j \to \infty$, then $\ln Z_\theta \ge \ln g(e_i) - \theta_i$ for the index $i$ of the smallest $\theta_i$, and $-\min_j\theta_j$ grows at least like $(\max_j\theta_j - \min_j\theta_j)/N$. So every solution stays bounded, $V$ decreases to its minimum, and by LaSalle's principle every solution converges to the unique fixed point with $\sum_j\theta_j = 0$, which is $\ln g$ shifted to mean zero.

**Step 5: the halving schedule freezes.** Let $\gamma_t$ be the value of $\ln f$ at step $t$. Each step changes $\theta$ by $\gamma_t$ in one coordinate. If $\sum_t\gamma_t < \infty$, then $\theta_t$ is a Cauchy sequence and converges to a limit $\theta_\infty$, for every path. With the halving schedule, $\gamma_t = 2^{-i}$ during stage $i$, so $\sum_t\gamma_t = \sum_iL_i2^{-i}$, where $L_i$ is the length of stage $i$. This sum is finite whenever $L_i$ grows more slowly than $2^i$, which is what happens in practice. The limit $\theta_\infty$ depends on the random path, so it is a random vector, and nothing forces it to equal $\ln g + c$. With $\gamma_t \propto 1/t$, $\sum\gamma_t = \infty$ and $\sum\gamma_t^2 < \infty$, which are the classical conditions under which a stochastic approximation follows the mean motion of Step 3 to its stable fixed point. For the Wang-Landau algorithm itself, this last step is the theorem of Fort, Jourdain, Kuhn, Lelièvre and Stoltz (2015), under their conditions, and it is not proved here. $\blacksquare$
