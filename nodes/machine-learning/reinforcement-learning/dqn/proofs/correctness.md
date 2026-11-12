---
title: What is proved about DQN, and what is not
proves: [correctness]
status: full
---

DQN with a nonlinear network has no convergence theorem, and off-policy bootstrapping with function approximation can diverge (Tsitsiklis and Van Roy, 1997; Sutton and Barto, Section 11.3). We prove the three facts that the page states. Notation is that of the page: $D$ is the buffer, $\theta$ and $\theta^-$ the online and target parameters, $h$ the Huber loss with threshold 1.

**Claim 1 (fixed objective between syncs).** Let $t_0$ be a step at which line L8 runs, or $t_0 = 0$. For each step $t$ with $t_0 < t < t_0 + C$, $\theta^-$ at line L6 equals $\theta$ at the end of step $t_0$. Fix the buffer content $D_t$ after line L4 of step $t$ and write $y_i = r_i$ if $\text{done}_i$, else $y_i = r_i + \gamma \max_{a'} Q(s'_i, a'; \theta^-)$, for $i \in D_t$. Then the minibatch gradient $g = \nabla_\theta \frac{1}{B} \sum_{j} h(y_j - Q(s_j, a_j; \theta))$ of line L7 satisfies $\mathbb{E}[g] = \nabla_\theta L_t(\theta)$ with $L_t(\theta) = \frac{1}{|D_t|} \sum_{i \in D_t} h(y_i - Q(s_i, a_i; \theta))$, where the expectation is over the draw of line L5.

*Proof.* The only line that writes $\theta^-$ is L8 (and L1 before the loop). L8 writes only when $t \bmod C = 0$, so between two such steps $\theta^-$ keeps the value it got at step $t_0$. Hence each $y_i$ depends only on transition $i$ and on that fixed $\theta^-$, not on the current $\theta$, so it is a constant for the gradient of line L7. Line L5 draws each index $j_k$ uniformly from $D_t$, independently. By linearity of expectation and of the gradient,

$$\mathbb{E}[g] = \frac{1}{B} \sum_{k=1}^{B} \mathbb{E}\big[\nabla_\theta h(y_{j_k} - Q(s_{j_k}, a_{j_k}; \theta))\big] = \frac{1}{B} \sum_{k=1}^{B} \frac{1}{|D_t|} \sum_{i \in D_t} \nabla_\theta h(y_i - Q(s_i, a_i; \theta)) = \nabla_\theta L_t(\theta). \qquad \square$$

**Claim 2 (error clipping).** $h$ is differentiable, and $h'(\delta) = \mathrm{clip}(\delta, -1, 1)$. Hence the gradient of $h(y - Q(s, a; \theta))$ is $-\mathrm{clip}(y - Q(s, a; \theta), -1, 1)\, \nabla_\theta Q(s, a; \theta)$.

*Proof.* For $|\delta| < 1$, $h(\delta) = \tfrac12\delta^2$ and $h'(\delta) = \delta$. For $\delta > 1$, $h(\delta) = \delta - \tfrac12$ and $h'(\delta) = 1$; for $\delta < -1$, $h(\delta) = -\delta - \tfrac12$ and $h'(\delta) = -1$. At $\delta = 1$ both pieces have value $\tfrac12$ and slope 1, and at $\delta = -1$ both have value $\tfrac12$ and slope $-1$, so $h$ is differentiable there too. In each case $h'(\delta) = \mathrm{clip}(\delta, -1, 1)$. The chain rule gives the gradient. $\square$

**Claim 3 (the tabular limit is value iteration on the empirical MDP).** Suppose $Q(s, a; \theta) = \theta_{s,a}$ (one parameter per pair), the buffer $D$ is fixed, every pair $(s, a)$ has $n(s, a) \ge 1$ transitions in $D$, and between syncs the squared loss $\frac{1}{|D|}\sum_{i \in D} (y_i - \theta_{s_i, a_i})^2$ is minimized exactly. Define the empirical MDP $\hat M$ by $\hat P(s' \mid s, a) = $ (the fraction of the transitions at $(s, a)$ that go to $s'$ without ending) and $\hat R(s, a) = $ (the mean reward of the transitions at $(s, a)$), with episode ends as transitions to an absorbing state of value 0. Let $\theta^-_k$ be the target parameters after the $k$-th sync. Then $\theta^-_{k+1} = \hat T \theta^-_k$, where $\hat T$ is the Bellman optimality operator of $\hat M$, and $\lVert \theta^-_k - \hat Q^* \rVert_\infty \le \gamma^k \lVert \theta^-_0 - \hat Q^* \rVert_\infty$, where $\hat Q^*$ is the optimal action-value function of $\hat M$.

*Proof.* The loss is a sum of separate terms, one group for each pair $(s, a)$: $\sum_{i : (s_i, a_i) = (s, a)} (y_i - \theta_{s,a})^2$. Each group is a convex quadratic in the one number $\theta_{s,a}$ and is minimized by the mean of its targets,

$$\theta_{s,a} = \frac{1}{n(s, a)} \sum_{i : (s_i, a_i) = (s,a)} y_i = \hat R(s, a) + \gamma \sum_{s'} \hat P(s' \mid s, a) \max_{a'} \theta^-_{k, s', a'},$$

because $y_i = r_i + \gamma \max_{a'} \theta^-_{k, s'_i, a'}$ for a transition that does not end and $y_i = r_i$ for one that does, which is the same as a move to the absorbing state of value 0. The right side is $(\hat T \theta^-_k)(s, a)$. The next sync copies these values, so $\theta^-_{k+1} = \hat T \theta^-_k$. The operator $\hat T$ is a $\gamma$-contraction in the max norm with fixed point $\hat Q^*$, by the [Bellman contraction](/bellman-contraction/) applied to the finite MDP $\hat M$. Induction on $k$ gives $\lVert \theta^-_k - \hat Q^* \rVert_\infty = \lVert \hat T \theta^-_{k-1} - \hat T \hat Q^* \rVert_\infty \le \gamma \lVert \theta^-_{k-1} - \hat Q^* \rVert_\infty \le \gamma^k \lVert \theta^-_0 - \hat Q^* \rVert_\infty$. $\square$

With the Huber loss instead of the squared loss, the minimizer of each group is the Huber location estimate of its targets instead of the mean. When the rewards and transitions of the data are deterministic, all targets of a group are equal, both estimates equal that common value, and Claim 3 holds unchanged. When the transitions are deterministic and every pair is in the data, $\hat M$ is the true MDP and the limit is the true $Q^*$.

**What is not proved.** With a network that shares parameters between pairs, the minimizer of the regression is not $\hat T \theta^-$, but its projection onto the functions the network can represent. The composition of a projection and a max-norm contraction need not be a contraction in any norm, and examples with linear features diverge. DQN also takes only $C$ stochastic gradient steps between syncs, not an exact minimization, and the buffer changes. So no theorem guarantees that DQN converges, and none is claimed on the page. $\blacksquare$
