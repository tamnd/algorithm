---
title: The biweight reweighting step never increases the objective and never divides by zero
proves: [correctness]
status: full
---

**Setting.** $x_1, \ldots, x_n$ are real, $c > q$ where $q = \Phi^{-1}(3/4)$, and $\sigma = \mathrm{MAD}/q > 0$ (the case $\sigma = 0$ ends at line L1). Write $r_i(\theta) = (x_i - \theta)/\sigma$, $Q(\theta) = \sum_i \rho_c(r_i(\theta))$, and let $T(\theta)$ be the value $\theta'$ of line L5.

**Lemma 1.** Put $g(s) = \frac{c^2}{6}\bigl[1 - (1 - s/c^2)^3\bigr]$ for $0 \le s \le c^2$ and $g(s) = c^2/6$ for $s > c^2$. Then $\rho_c(u) = g(u^2)$, $g$ is concave and nondecreasing on $[0, \infty)$, it is differentiable, and $2g'(u^2) = w_c(u)$.

*Proof.* The identity $\rho_c(u) = g(u^2)$ is the definition. For $s < c^2$, $g'(s) = \frac12(1 - s/c^2)^2$, and for $s > c^2$, $g'(s) = 0$. Both one-sided derivatives at $s = c^2$ are 0, so $g$ is differentiable with $g'(s) = \frac12\max(0, 1 - s/c^2)^2$. This function is nonnegative and nonincreasing, so $g$ is nondecreasing and concave. Finally $2g'(u^2) = (1 - u^2/c^2)^2 = w_c(u)$ for $|u| < c$, and both sides are 0 for $|u| \ge c$. $\square$

**Lemma 2 (descent).** If $S(\theta) = \sum_i w_c(r_i(\theta)) > 0$, then $Q(T(\theta)) \le Q(\theta)$, with equality only if $T(\theta) = \theta$.

*Proof.* Fix $\theta_0$ with $S(\theta_0) > 0$, and put $s_i = r_i(\theta_0)^2$ and $w_i = w_c(r_i(\theta_0)) = 2g'(s_i)$. A concave differentiable function lies below its tangent lines, so for every $\theta$
$$Q(\theta) = \sum_i g(r_i(\theta)^2) \le \sum_i \Bigl[g(s_i) + \tfrac12 w_i\bigl(r_i(\theta)^2 - s_i\bigr)\Bigr] =: M(\theta),$$
with equality at $\theta = \theta_0$. $M$ is a quadratic in $\theta$ with leading coefficient $\frac{1}{2\sigma^2}\sum_i w_i > 0$. Its derivative is $-\frac{1}{\sigma^2}\sum_i w_i(x_i - \theta)$, which is 0 at $\theta = \sum_i w_i x_i / \sum_i w_i = T(\theta_0)$. So $T(\theta_0)$ is the unique minimizer of $M$, and
$$Q(T(\theta_0)) \le M(T(\theta_0)) \le M(\theta_0) = Q(\theta_0).$$
The second inequality is strict if $T(\theta_0) \ne \theta_0$, because the minimizer of $M$ is unique. $\square$

**Lemma 3 (positive weights).** Let $\theta_0$ be the median. Then $Q(\theta_0) < nc^2/6$, and every iterate $\theta_t$ has $S(\theta_t) > 0$.

*Proof.* By the definition of the MAD, at least half of the points, and so at least one, satisfy $|x_i - \theta_0| \le \mathrm{MAD} = q\sigma$, that is $|r_i(\theta_0)| \le q < c$. For such a point $\rho_c(r_i) < c^2/6$, and all other terms are at most $c^2/6$. So $Q(\theta_0) < nc^2/6$. For any $\theta$, $S(\theta) = 0$ means $|r_i(\theta)| \ge c$ for all $i$, so $Q(\theta) = nc^2/6$. By induction on $t$: if $S(\theta_0), \ldots, S(\theta_{t-1})$ are positive, Lemma 2 gives $Q(\theta_t) \le Q(\theta_0) < nc^2/6$, so $S(\theta_t) > 0$. $\square$

**Theorem.** The iterates of lines L2 to L7 are well defined, $Q(\theta_t)$ is nonincreasing, and every limit point $\theta^*$ of $(\theta_t)$ satisfies $\sum_i \psi_c(r_i(\theta^*)) = 0$.

*Proof.* Lemma 3 shows that line L5 never divides by 0, and Lemma 2 gives the monotonicity. Each $\theta_{t+1}$ is a weighted mean of the $x_i$, so the iterates lie in $[\min x_i, \max x_i]$, a compact set, and limit points exist. $Q$ is bounded below by 0, so $Q(\theta_t)$ converges to some $Q^*$. Let $\theta_{t_j} \to \theta^*$. $Q$ is continuous, so $Q(\theta^*) = Q^*$, and $Q^* \le Q(\theta_0) < nc^2/6$, so $S(\theta^*) > 0$. $w_c$ is continuous (it is 0 at $\pm c$), so $T$ is continuous at $\theta^*$, and $T(\theta_{t_j}) = \theta_{t_j + 1} \to T(\theta^*)$. Then $Q(T(\theta^*)) = \lim Q(\theta_{t_j + 1}) = Q^* = Q(\theta^*)$. By Lemma 2, $T(\theta^*) = \theta^*$, that is $\sum_i w_c(r_i(\theta^*))(x_i - \theta^*) = 0$. Since $w_c(u)\,u = \psi_c(u)$, this is $\sigma\sum_i \psi_c(r_i(\theta^*)) = 0$. $\square$

**What is not claimed.** The limit is a stationary point of $Q$. It need not be the global minimizer, because $Q$ is not convex. The stopping rule of line L6 bounds the last step, not the distance to the limit.
