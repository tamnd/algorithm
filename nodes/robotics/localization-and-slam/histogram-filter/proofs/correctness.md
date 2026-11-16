---
title: The histogram filter computes the posterior of the cell model
proves: [correctness]
status: full
---

**Setting.** A continuous state space $S$ is split into $g$ cells $X_1, \ldots, X_g$ that do not overlap and cover $S$. Cell $k$ has a representative point $c_k \in X_k$. The cell model is the hidden Markov model whose state $k_t \in \{1, \ldots, g\}$ is a cell, with

- the prior $P(k_0 = i) = p_{i,0}$,
- the transition $P(k_t = k \mid u_t, k_{t-1} = i) = T_{ki}(u_t)$, the probability that the continuous motion model started at $c_i$ ends in $X_k$,
- the measurement probability $p(z_t \mid k_t = k) = p(z_t \mid x_t = c_k)$.

The data at time $t$ are $d_t = (z_{1:t}, u_{1:t})$.

**Assumptions.**

- (T) For every control $u$ and every cell $i$, $\sum_{k=1}^{g} T_{ki}(u) = 1$ and $T_{ki}(u) \ge 0$.
- (M) The cell model satisfies the Markov assumption, and each control is chosen from the past data and from randomness independent of the state (assumptions M1, M2 and C of the proof of the Bayes filter).
- (P) Each measurement that occurs has positive probability under the predicted belief, so line L4 does not divide by zero.

**Claim.** If the input $p_i = P(k_{t-1} = i \mid d_{t-1})$ for all $i$, then the output of HISTOGRAM-FILTER$(p, u_t, z_t)$ is $P(k_t = k \mid d_t)$ for all $k$. By induction over $t$, the filter computes the posterior of the cell model at every time step.

*Proof.* First, the cell model is a valid model. The prior is a distribution by assumption. By (T), each column of the transition is a distribution over the cells, so $T(u)$ is a stochastic matrix. For the code on an interval $[a, b)$ with Gaussian noise, $T_{ki}(u) = \Phi(\beta_{k+1}) - \Phi(\beta_k)$ with $\beta_k = (e_k - c_i - u)/\sigma$, where $e_1 = -\infty$, $e_{g+1} = +\infty$ and $e_k$ is the left edge of cell $k$ for $2 \le k \le g$. The edges increase, and $\Phi$ increases, so each term is nonnegative. The sum over $k$ telescopes to $\Phi(+\infty) - \Phi(-\infty) = 1$. So (T) holds, and the end cells receive exactly the mass of the motion model that falls outside $[a, b)$.

Second, the cell model is a finite state Bayes filter model, with state $k_t$, motion model $T_{ki}(u_t)$ and measurement model $p(z_t \mid c_k)$. Lines L1 and L2 compute

$$\bar p_k = \sum_{i=1}^{g} T_{ki}(u_t)\, p_i,$$

which is line L2 of the Bayes filter for this model. Line L3 computes $q_k = p(z_t \mid c_k)\, \bar p_k$, which is line L3 of the Bayes filter. Lines L4 and L5 divide by $\sum_k q_k$, which is positive by (P). This is lines L4 and L5 of the Bayes filter. By the correctness of the Bayes filter on a finite state space under (M), the output is $P(k_t = k \mid d_t)$. $\square$

**What the claim does not say.** The claim is about the cell model. The posterior of the continuous model, integrated over cell $k$, is in general a different number, because the cell model starts the motion from $c_i$ and not from the true distribution of the state inside cell $i$, and because it reads the likelihood at $c_k$ only. The tests of the code measure this difference on a linear Gaussian model, against the Kalman filter, and show that it falls as the cells get smaller.
