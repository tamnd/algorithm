---
title: The expected reward of a walk is the drop at its start node
proves: [correctness]
status: full
---

**Setting.** The grid has nodes $1, \ldots, N$, wire conductances $g_{mj} = g_{jm} \ge 0$, pad conductances $g^{\mathrm{pad}}_m \ge 0$ and loads $i_m \ge 0$. Every connected part of the wire graph has a node with $g^{\mathrm{pad}}_m > 0$, and every node has $D_m = \sum_j g_{mj} + g^{\mathrm{pad}}_m > 0$. The drop $x$ solves $G x = i$ with $G_{mm} = D_m$ and $G_{mj} = -g_{mj}$ for $j \ne m$; the [power grid analysis](/power-grid-analysis/) page shows that $G$ is nonsingular. Let $Q_{mj} = g_{mj}/D_m$, let $r_m = i_m/D_m$, and let $\Delta = \mathrm{diag}(D)$, so that $G = \Delta (I - Q)$.

The walk of lines L3 to L7 is a Markov chain on the nodes plus one stopping state $\star$. From node $m$ it moves to $j$ with probability $Q_{mj}$ and to $\star$ with probability $g^{\mathrm{pad}}_m / D_m = 1 - \sum_j Q_{mj}$. Let $X_0 = k, X_1, \ldots$ be the nodes visited and $\tau$ the number of node visits before $\star$. The reward is $R = \sum_{t=0}^{\tau - 1} r_{X_t}$.

**Lemma 1 (the walk stops).** There are $n_0 \le N$ and $\delta > 0$ such that from every node the walk reaches $\star$ within $n_0$ steps with probability at least $\delta$. Hence $P(\tau > t\, n_0) \le (1 - \delta)^t$, the walk stops with probability 1, and $\tau$ has finite moments of every order.

*Proof.* From node $m$, take a shortest path of wires to a node with a pad, of length at most $N - 1$, and then the step to $\star$. Each step of this path has positive probability, so the probability $\delta_m$ of following it is positive. Let $n_0 = N$ and $\delta = \min_m \delta_m$. The bound on $P(\tau > t n_0)$ follows by the Markov property, applied at the times $n_0, 2 n_0, \ldots$. A geometric tail gives finite moments. $\square$

**Lemma 2 (spectral radius).** $Q^t \to 0$ as $t \to \infty$, so $\rho(Q) < 1$, $I - Q$ is nonsingular, and $(I - Q)^{-1} = \sum_{t \ge 0} Q^t$ with nonnegative entries.

*Proof.* $(Q^t)_{kj}$ is the probability that the walk from $k$ is at node $j$ at step $t$ without having stopped, which is at most $P(\tau > t)$, and this tends to 0 by Lemma 1. A matrix whose powers tend to 0 has [spectral radius](/spectral-radius/) below 1, and then the [Neumann series](/neumann-series/) converges to $(I - Q)^{-1}$. $\square$

**Theorem 1 (unbiased).** $E[R] = x_k$.

*Proof.* All rewards are nonnegative, so we may exchange the sum and the expectation:

$$ E[R] = \sum_{t \ge 0} E\big[r_{X_t} [\tau > t]\big] = \sum_{t \ge 0} \sum_m (Q^t)_{km} r_m = \big((I - Q)^{-1} r\big)_k , $$

by Lemma 2. Now $(I - Q)^{-1} r = (I - Q)^{-1} \Delta^{-1} i = (\Delta (I - Q))^{-1} i = G^{-1} i = x$. $\square$

**Theorem 2 (discrete harmonic property).** For every node $m$, $x_m = r_m + \sum_j Q_{mj} x_j$, and $x$ is the only vector with this property.

*Proof.* The identity is row $m$ of $G x = i$ divided by $D_m$. It can be read as a first-step analysis: the walk from $m$ collects $r_m$ and then, with probability $Q_{mj}$, starts afresh at $j$, or stops with payoff 0. The system $(I - Q) z = r$ has the unique solution $z = x$ by Lemma 2. $\square$

**Theorem 3 (finite variance).** $E[R^2] < \infty$. So the mean of $W$ independent walks has variance $\mathrm{Var}(R)/W$, it converges to $x_k$ with probability 1, and $\sqrt{W}$ times its error tends in distribution to a normal law with variance $\mathrm{Var}(R)$.

*Proof.* $0 \le R \le \tau \max_m r_m$, and $E[\tau^2] < \infty$ by Lemma 1. The rest is the [law of large numbers](/law-of-large-numbers/) and the [central limit theorem](/central-limit-theorem/) for independent copies of $R$. $\square$

**Corollary (length of the walks).** The expected number of visits from $k$ is $E[\tau] = y_k$, where $y$ solves $G y = D$, with $D$ the vector of the $D_m$.

*Proof.* Apply Theorem 1 with the reward 1 at each visit, that is $r = \mathbf{1}$ and $i = \Delta \mathbf{1} = D$. $\square$

In the example of the page, $G y = D$ gives $y = (3, 6, 7)$, so a walk from node 2 makes 7 visits and 6 steps on average. The tests check Theorem 1 within 5 standard errors on a chain and on random meshes, Theorem 2 exactly in rational arithmetic, and the corollary against the mean length of the walks.
