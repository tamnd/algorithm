---
title: Markov localization computes p(x_t | z_1:t, u_1:t, m)
proves: [correctness]
status: full
---

**Setting.** The set $X$ of poses is finite. The map $m$ is fixed and known. The data at time $t \ge 1$ are a control $u_t$ and a reading $z_t$, and $d_t = (z_{1:t}, u_{1:t})$. All probabilities below are conditioned on $m$; we write $m$ only where the models use it.

**Assumptions.**

- (M1) $p(x_t \mid x_{0:t-1}, d_{t-1}, u_t, m) = p(x_t \mid u_t, x_{t-1}, m)$.
- (M2) $p(z_t \mid x_{0:t}, d_{t-1}, u_t, m) = p(z_t \mid x_t, m)$.
- (C) $p(x_{t-1} \mid d_{t-1}, u_t, m) = p(x_{t-1} \mid d_{t-1}, m)$: the control depends only on past data and on randomness that is independent of the pose.
- (P) $p(z_t \mid d_{t-1}, u_t, m) > 0$ for each reading that occurs.

**Claim.** If $\mathrm{bel}(x) = p(x_{t-1} = x \mid d_{t-1}, m)$ for all $x \in X$, then MARKOV-LOCALIZATION$(\mathrm{bel}, u_t, z_t, m)$ returns $p(x_t = x \mid d_t, m)$ for all $x \in X$. By induction from $\mathrm{bel}_0 = p(x_0 \mid m)$, this holds at every time step.

*Proof.* Write $T(x, x') = p(x_t = x \mid u_t, x_{t-1} = x', m)$.

*Prediction.* Line L1 sets every entry of $\mathrm{bel\_bar}$ to zero. Lines L2 to L4 add the term $T(x, x')\,\mathrm{bel}(x')$ to the entry $x$, once for each pair $(x', x)$ with $\mathrm{bel}(x') > 0$ and $T(x, x') > 0$, and for no other pair. A pair with $\mathrm{bel}(x') = 0$ or $T(x, x') = 0$ has a zero term. So when line L4 has run for all pairs,

$$\mathrm{bel\_bar}(x) = \sum_{x' \in X} T(x, x')\,\mathrm{bel}(x') \quad \text{for every } x \in X.$$

By the law of total probability and the product rule,

$$p(x_t = x \mid d_{t-1}, u_t, m) = \sum_{x'} p(x_t = x \mid x_{t-1} = x', d_{t-1}, u_t, m)\; p(x_{t-1} = x' \mid d_{t-1}, u_t, m).$$

Summing (M1) over $x_{0:t-2}$ shows that the first factor is $T(x, x')$. By (C) and the hypothesis of the claim, the second factor is $\mathrm{bel}(x')$. So $\mathrm{bel\_bar}(x) = p(x_t = x \mid d_{t-1}, u_t, m)$.

*Correction.* By Bayes' rule with the data $d_{t-1}, u_t$ held fixed,

$$p(x_t = x \mid d_t, m) = \frac{p(z_t \mid x_t = x, d_{t-1}, u_t, m)\; p(x_t = x \mid d_{t-1}, u_t, m)}{p(z_t \mid d_{t-1}, u_t, m)}.$$

Summing (M2) over $x_{0:t-1}$ shows that the first factor of the numerator is $p(z_t \mid x_t = x, m)$. The second factor is $\mathrm{bel\_bar}(x)$. So the numerator is $\mathrm{bel}'(x)$ of line L5. The denominator is $\sum_x \mathrm{bel}'(x)$ by the law of total probability, and it is positive by (P). Lines L6 and L7 divide by it. So the output is $p(x_t = x \mid d_t, m)$. $\square$

**Remarks.** The proof does not use the order of the loops in lines L2 and L3, only that every nonzero term is added exactly once. If the motion model gives zero probability to the true move (a kidnapping), the claim still holds for the model, but the model is wrong, and the posterior can be zero at the true pose. If the readings of the beams of one scan are not independent given the pose, (M2) is false, and the output is not the posterior.
