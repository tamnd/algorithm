---
title: What each DDPG update computes
proves: [correctness]
status: full
---

Notation is that of the page. The deterministic policy gradient theorem is assumed with its regularity conditions: $\nabla_\theta J(\mu_\theta) = \int \nabla_\theta \mu_\theta(s) \nabla_a Q^\mu(s, a)|_{a = \mu_\theta(s)} \rho^\mu(ds)$, where $\rho^\mu$ has total mass $1/(1 - \gamma)$.

**Claim 1 (actor step).** Let the minibatch states be drawn independently from a law $\rho$, and let $Q_w = Q^\mu$. Then the expectation of the update direction of line L7 is $u(\rho) = \int \nabla_\theta \mu_\theta(s) \nabla_a Q^\mu(s, a)|_{a = \mu_\theta(s)} \rho(ds)$. If $\rho = (1 - \gamma) \rho^\mu$, then $u(\rho) = (1 - \gamma) \nabla_\theta J(\mu_\theta)$.

*Proof.* The update direction is the mean of $M$ terms, and each term has expectation $u(\rho)$ by the definition of $\rho$; linearity of expectation gives the first sentence. The second follows from the theorem, since $(1 - \gamma) \rho^\mu$ is a probability measure and $u$ is linear in $\rho$. $\square$

With the replay distribution in place of $(1 - \gamma)\rho^\mu$, $u$ is the off-policy deterministic gradient, which differs from $\nabla J$ in general; so line L7 follows the true gradient only when the critic is exact and the replayed states have the actor's discounted state law.

**Claim 2 (critic step).** For fixed targets $y_i$, line L6 is one gradient step on $\ell(w) = \frac1M \sum_i (Q_w(s_i, a_i) - y_i)^2$, with gradient $\frac2M \sum_i (Q_w(s_i, a_i) - y_i) \nabla_w Q_w(s_i, a_i)$. If the critic class can represent any function on the replayed pairs and $\ell$ is minimized exactly, then $Q_w(s_i, a_i) = (T Q_{w'})(s_i, a_i)$ in expectation over the next state, where $(T Q)(s, a) = \mathbb{E}[r + \gamma (1 - \text{done}) Q(s', \mu_{\theta'}(s')) \mid s, a]$.

*Proof.* The gradient formula is the chain rule. The targets in line L5 depend only on the target parameters, which line L6 does not change, so they are constants for this step. For the second sentence, the minimizer of the expected squared error $\mathbb{E}[(Q(s, a) - Y)^2 \mid s, a]$ over the value $Q(s, a)$ is the conditional mean $\mathbb{E}[Y \mid s, a]$, which is $(T Q_{w'})(s, a)$ by line L5. $\square$

**Claim 3 (soft target update).** If line L8 runs with learned weights $w_1, w_2, \ldots$, then $w'_k = (1 - \tau)^k w'_0 + \sum_{j=1}^{k} \tau (1 - \tau)^{k - j} w_j$, and the coefficients sum to 1. In particular, for fixed $w_j = w$, $w'_k = w + (1 - \tau)^k (w'_0 - w)$.

*Proof.* By induction on $k$. The case $k = 0$ is trivial. If the formula holds for $k - 1$, then $w'_k = \tau w_k + (1 - \tau) w'_{k-1} = (1 - \tau)^k w'_0 + \sum_{j=1}^{k-1} \tau (1 - \tau)^{k-j} w_j + \tau w_k$. The coefficients sum to $(1 - \tau)^k + \tau \sum_{i=0}^{k-1} (1 - \tau)^i = (1 - \tau)^k + 1 - (1 - \tau)^k = 1$. For fixed $w$, the sum of the $w_j$ terms is $(1 - (1 - \tau)^k) w$. The same holds for $\theta'$. $\square$

**Claim 4 (Ornstein-Uhlenbeck noise).** Let $x_{t+1} = x_t + c(m - x_t) + \sigma \varepsilon_t$ with $c = \theta_{\text{OU}} \, dt$, independent standard normal $\varepsilon_t$, and $0 < c < 2$. Then $\mathbb{E}[x_t] = m + (1 - c)^t (x_0 - m)$; the variance tends to $v = \sigma^2 dt / (1 - (1 - c)^2)$; and in the stationary state the correlation of $x_t$ and $x_{t+1}$ is $1 - c$. (The page and the code use $dt = 1$.)

*Proof.* Let $z_t = x_t - m$; then $z_{t+1} = (1 - c) z_t + \sigma\sqrt{dt}\, \varepsilon_t$. Taking expectations gives $\mathbb{E} z_t = (1 - c)^t z_0$. The variance satisfies $\mathrm{Var}(z_{t+1}) = (1 - c)^2 \mathrm{Var}(z_t) + \sigma^2 dt$ because $\varepsilon_t$ is independent of $z_t$; since $|1 - c| < 1$, this recursion converges to its fixed point $v$. Finally $\mathrm{Cov}(z_t, z_{t+1}) = (1 - c) \mathrm{Var}(z_t)$, so the correlation is $1 - c$ when both variances equal $v$. $\square$

Together, Claims 1 to 4 show that DDPG is an approximate off-policy actor-critic: the critic regresses on a frozen Bellman target, the actor follows the deterministic policy gradient of the critic at replayed states, the targets are moving averages of the learned parameters, and the exploration noise is mean-reverting with a known stationary scale. $\blacksquare$
