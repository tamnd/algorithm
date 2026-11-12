---
title: LSTD solves the sample TD equations, and recursive LSTD equals batch LSTD
proves: [correctness]
status: full
---

We use the notation of the page. A transition $t$ has state $s_t$, reward $r_t$ and next state $s'_t$, with $\phi(s'_t) = 0$ when the episode ends. Write $\phi_t = \phi(s_t)$, $\phi'_t = \phi(s'_t)$ and $v_t = \phi_t - \gamma\phi'_t$. After $T$ transitions, lines L1 to L6 give

$$\hat{A}_T = \epsilon I + \sum_{t<T} z_t v_t^\top, \qquad \hat{b}_T = \sum_{t<T} r_t z_t,$$

where $z_t = \gamma\lambda z_{t-1} + \phi_t$, and $z_{t-1} = 0$ at the start of the data and after a terminal transition (line L7). Line L8 returns $\hat{\theta}_T = \hat{A}_T^{-1}\hat{b}_T$ when $\hat{A}_T$ is invertible.

**Lemma 1 (the sample equation).** Let $\lambda = 0$ and $\epsilon = 0$. Then $\hat{\theta}_T$ is the unique $\theta$ with $\sum_{t<T} \phi_t\,\delta_t(\theta) = 0$, where $\delta_t(\theta) = r_t + \gamma\phi_t'^\top\theta - \phi_t^\top\theta$ is the TD error.

*Proof.* With $\lambda = 0$, $z_t = \phi_t$. So $\sum_t \phi_t\delta_t(\theta) = \sum_t r_t\phi_t - \sum_t \phi_t(\phi_t - \gamma\phi'_t)^\top\theta = \hat{b}_T - \hat{A}_T\theta$. This is zero exactly when $\hat{A}_T\theta = \hat{b}_T$. $\square$

The sum $\sum_t \phi_t\delta_t(\theta)$ is $T$ times the mean TD(0) update over the data. So LSTD returns the point where the TD(0) updates over the batch cancel, which is the point that TD(0) would approach if it swept the batch many times with small steps.

**Lemma 2 (exact data gives the TD fixed point).** Let the chain have transition matrix $P$, stationary distribution $\mu$ and expected reward $r(s)$, and let $A = \Phi^\top D(I - \gamma P)\Phi$ and $b = \Phi^\top D r$. Suppose that in the data each pair $(s, s')$ occurs exactly $T\mu(s)P(s, s')$ times, each with reward $r(s)$. Then with $\lambda = 0$ and $\epsilon = 0$, $\hat{A}_T = TA$, $\hat{b}_T = Tb$, and $\hat{\theta}_T = A^{-1}b$ is the TD fixed point.

*Proof.* Group the terms of $\hat{A}_T$ by the pair $(s, s')$:

$$\hat{A}_T = \sum_{s, s'} T\mu(s)P(s, s')\,\phi(s)\bigl(\phi(s) - \gamma\phi(s')\bigr)^\top = T\sum_s \mu(s)\phi(s)\Bigl(\phi(s) - \gamma\sum_{s'}P(s, s')\phi(s')\Bigr)^\top = T\,\Phi^\top D(I - \gamma P)\Phi.$$

In the same way $\hat{b}_T = T\sum_s \mu(s)r(s)\phi(s) = T\Phi^\top D r$. The factor $T$ cancels in $\hat{A}_T^{-1}\hat{b}_T$. $\square$

**Theorem 1 (consistency).** Let the data be one trajectory of an irreducible, aperiodic finite chain, with $\lambda = 0$, $\epsilon = 0$, bounded rewards and $\Phi$ of full column rank. Then $\hat{\theta}_T \to A^{-1}b$ with probability one.

*Proof.* By the [ergodic theorem](/ergodic-theorem/) for finite Markov chains, the fraction of transitions from $s$ to $s'$ tends to $\mu(s)P(s, s')$, and the mean reward on those transitions tends to $r(s)$, with probability one. The computation of Lemma 2 then gives $\hat{A}_T/T \to A$ and $\hat{b}_T/T \to b$. The matrix $A$ is invertible: for $x \ne 0$, $x^\top Ax \ge (1 - \gamma)\lVert\Phi x\rVert_D^2 > 0$ (see [value function approximation](/value-function-approximation/)). Matrix inversion is continuous at an invertible matrix, so $\hat{\theta}_T = (\hat{A}_T/T)^{-1}(\hat{b}_T/T) \to A^{-1}b$. $\blacksquare$

For $\lambda > 0$ the same argument, with $z_t$ in place of $\phi_t$, gives the limit $A_\lambda = \Phi^\top D(I - \gamma\lambda P)^{-1}(I - \gamma P)\Phi$ and $b_\lambda = \Phi^\top D(I - \gamma\lambda P)^{-1}r$, whose solution is the fixed point of $\Pi T^{(\lambda)}$ of Tsitsiklis and Van Roy. We do not prove this case here.

**Theorem 2 (recursive LSTD equals batch LSTD).** Let $\epsilon > 0$ and $B_0 = \epsilon^{-1}I$. For each transition set $u = B_{t}z_t$, $w^\top = v_t^\top B_t$ and

$$B_{t+1} = B_t - \frac{u\,w^\top}{1 + v_t^\top B_t z_t}.$$

If every denominator is nonzero, then $B_T = \hat{A}_T^{-1}$, and $B_T\hat{b}_T$ equals the output of batch LSTD with the same $\epsilon$.

*Proof.* By induction on $T$. At $T = 0$, $\hat{A}_0 = \epsilon I$ and $B_0 = \epsilon^{-1}I$. Suppose $B_t = \hat{A}_t^{-1}$. Then $\hat{A}_{t+1} = \hat{A}_t + z_t v_t^\top$, a rank one change. The [Sherman-Morrison formula](/sherman-morrison-formula/) says that if $M$ is invertible and $1 + v^\top M^{-1}z \ne 0$, then $M + zv^\top$ is invertible and

$$(M + zv^\top)^{-1} = M^{-1} - \frac{M^{-1}z\,v^\top M^{-1}}{1 + v^\top M^{-1}z}.$$

With $M = \hat{A}_t$, the right side is the update above, so $B_{t+1} = \hat{A}_{t+1}^{-1}$. The vector $\hat{b}_t$ is built in the same way in both versions. So $B_T\hat{b}_T = \hat{A}_T^{-1}\hat{b}_T$. $\blacksquare$

If a denominator is $0$, then $\hat{A}_{t+1}$ is singular, by the matrix determinant lemma $\det(M + zv^\top) = (1 + v^\top M^{-1}z)\det M$. The implementation raises an error in this case.

**Theorem 3 (LSTD(1) fits the returns).** Let $\lambda = 1$, $\epsilon = 0$, and let the data be complete episodes. Let $G_t = \sum_{k \ge t} \gamma^{k-t}r_k$, summed to the end of the episode of $t$. Then $\hat{A}_T = \sum_t \phi_t\phi_t^\top$ and $\hat{b}_T = \sum_t G_t\phi_t$, so $\hat{\theta}_T$ is the ordinary least-squares fit of the returns $G_t$ on the features $\phi_t$.

*Proof.* Take one episode with transitions $0, \ldots, L - 1$, so $\phi'_{t} = \phi_{t+1}$ for $t < L - 1$ and $\phi'_{L-1} = 0$. With $\lambda = 1$, $z_t = \sum_{k \le t}\gamma^{t-k}\phi_k$. Exchange the sums:

$$\sum_{t<L} z_t v_t^\top = \sum_{k<L}\phi_k\sum_{t=k}^{L-1}\gamma^{t-k}(\phi_t - \gamma\phi'_t)^\top = \sum_{k<L}\phi_k\phi_k^\top,$$

because the inner sum telescopes to $\phi_k - \gamma^{L-k}\phi'_{L-1} = \phi_k$. In the same way $\sum_t r_t z_t = \sum_k \phi_k\sum_{t \ge k}\gamma^{t-k}r_t = \sum_k G_k\phi_k$. The trace is reset between episodes, so the totals add over episodes. $\blacksquare$
