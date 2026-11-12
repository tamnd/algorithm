---
title: What each TD3 update computes
proves: [correctness]
status: full
---

Notation is that of the page. Expectations are over the target noise $\tilde\varepsilon$, the next state $s'$, and any randomness in the target critics, given the minibatch pair $(s, a)$ and reward $r$.

**Claim 1 (the minimum adds no upward bias).** Let $X_1, X_2$ be integrable random variables. Then $\mathbb{E}[\min(X_1, X_2)] \le \min(\mathbb{E} X_1, \mathbb{E} X_2)$. Hence, if $Q'_1(s', \tilde a)$ or $Q'_2(s', \tilde a)$ has expectation at most the true value $q$, then the expected target of line L6 is at most $r + \gamma q$ for a non-terminal transition.

*Proof.* Pointwise, $\min(X_1, X_2) \le X_1$ and $\min(X_1, X_2) \le X_2$. Expectation is monotone, so $\mathbb{E}[\min(X_1, X_2)]$ is at most $\mathbb{E} X_1$ and at most $\mathbb{E} X_2$, hence at most their minimum. For the second sentence, take $X_j = Q'_j(s', \tilde a)$; one of $\mathbb{E} X_j$ is at most $q$, so $\mathbb{E}[\min] \le q$, and $\gamma > 0$ preserves the inequality. $\square$

The inequality can be strict even when both estimates are unbiased: for independent errors uniform on $\{-1, 0, 1\}$, the expected minimum is $q - \tfrac49$. So the minimum trades the overestimation of a maximum for a bounded underestimation.

**Claim 2 (target policy smoothing).** Given $s'$ and the target parameters, the conditional expectation of the target of line L6 for a non-terminal transition is $r + \gamma \int \min_j Q'_j(s', \mu'(s') + u)\, \nu_c(du)$, where $\nu_c$ is the law of $\mathrm{clip}(\tilde\varepsilon, -c, c)$, a probability measure on $[-c, c]$. In particular, for a critic that is quadratic in the action, $Q'(s', a) = \alpha(s') + \beta(s') a + w_3 a^2$, the smoothed value is $Q'(s', \mu'(s')) + w_3\, \mathbb{E}[\mathrm{clip}(\tilde\varepsilon, -c, c)^2]$.

*Proof.* Line L5 sets $\tilde a = \mu'(s') + U$ with $U = \mathrm{clip}(\tilde\varepsilon, -c, c)$, and $|U| \le c$ by definition of the clip, so $\nu_c$ is supported on $[-c, c]$. The first formula is the definition of the expectation of a function of $U$. For the quadratic critic, expand $Q'(s', \mu'(s') + U) = Q'(s', \mu'(s')) + (\beta(s') + 2 w_3 \mu'(s')) U + w_3 U^2$. Since the law of $\tilde\varepsilon$ is symmetric about 0 and clipping is an odd map, $U$ is symmetric and $\mathbb{E} U = 0$, which leaves the stated term. $\square$

**Claim 3 (delay schedule).** Number the critic updates $k = 1, 2, \ldots$. After $K$ updates, both critics have taken $K$ steps, and the actor and each target have taken exactly $\lfloor K / d \rfloor$ steps, at the updates $k = d, 2d, \ldots$. Between two actor steps there are exactly $d$ critic steps, and every actor step uses a critic that has taken a step against the current targets.

*Proof.* Lines L7 run at every update. Lines L9 and L10 run when $k \bmod d = 0$, that is, when $k$ is a multiple of $d$; the number of multiples of $d$ in $\{1, \ldots, K\}$ is $\lfloor K / d \rfloor$, and consecutive multiples differ by $d$. Within an update, line L7 precedes line L9, so the actor uses the critic $w_1$ after that update's critic step. $\square$

**Claim 4 (actor step and target averages).** Line L9 moves $\theta$ along $\frac1M \sum_i \nabla_\theta \mu_\theta(s_i) \nabla_a Q_{w_1}(s_i, a)|_{a = \mu_\theta(s_i)}$, the sample deterministic policy gradient with critic $Q_{w_1}$. After $m$ executions of line L10, each target is $w'_m = (1 - \tau)^m w'_0 + \sum_{l=1}^{m} \tau (1 - \tau)^{m-l} w_{(l)}$, where $w_{(l)}$ is the online value at the $l$-th execution, and the coefficients sum to 1.

*Proof.* The first sentence is the chain rule applied to $\theta \mapsto Q_{w_1}(s_i, \mu_\theta(s_i))$, averaged over the minibatch; for the linear actor $\mu_\theta(s) = \theta \cdot f(s)$ the Jacobian is $f(s)$, as in the code. The second is the induction of the DDPG soft update: $w'_m = \tau w_{(m)} + (1 - \tau) w'_{m-1}$, and the coefficients sum to $(1 - \tau)^m + \tau \sum_{i=0}^{m-1} (1 - \tau)^i = 1$. $\square$

Together, Claims 1 to 4 show that TD3 is DDPG with a target that is not biased upward when one critic is accurate, that averages the critic over a bounded neighbourhood of the target action, and with an actor and targets that move once every $d$ critic steps along the deterministic policy gradient of the first critic. $\blacksquare$
