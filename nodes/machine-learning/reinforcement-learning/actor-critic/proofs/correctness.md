---
title: The mean actor update of one-step actor-critic, and its bias
proves: [correctness]
status: full
---

Notation is that of the page. Fix $\theta$ and $w$ (the frozen-parameter mean update; the online algorithm is a stochastic approximation of it). Let $\pi = \pi_\theta$, $\psi(s, a) = \nabla_\theta \log \pi(a \mid s)$, $r(s, a) = \mathbb{E}[R_{t+1} \mid S_t = s, A_t = a]$, and let $P(s' \mid s, a)$ be the transition probabilities, whose missing mass is the probability that the episode ends. Write $V = V^\pi$, $Q = Q^\pi$, $e = V_w - V$ on states, and set $V_w = V = 0$ at the end. Let $T$ be the end time and $d(s) = \sum_{t \ge 0} \gamma^t \Pr(S_t = s, T > t)$. We assume that $\pi(a \mid s) > 0$, that $S$ and $A$ are finite, and that either (a) $\gamma < 1$ and $|R_{t+1}| \le R_{\max}$, or (b) the MDP has no cycles, so that $T$ is bounded and $\gamma \le 1$ is allowed.

**Theorem.** Let $u = \sum_{t=0}^{T-1} \gamma^t \delta_t \psi(S_t, A_t)$ with $\delta_t = R_{t+1} + \gamma V_w(S_{t+1}) - V_w(S_t)$, the sum of the actor changes of line L7 with $\eta_\theta = 1$. Then

$$\mathbb{E}[u] = \nabla J(\theta) + \gamma \sum_s d(s) \sum_a \nabla_\theta \pi(a \mid s) \sum_{s'} P(s' \mid s, a)\, e(s').$$

In particular $\mathbb{E}[u] = \nabla J(\theta)$ when $V_w = V^\pi$.

*Proof.* Step 1 (one step). Given $S_t = s$, $A_t = a$ and $T > t$, the next state is $s'$ with probability $P(s' \mid s, a)$, so

$$\mathbb{E}[\delta_t \mid S_t = s, A_t = a, T > t] = r(s, a) + \gamma \sum_{s'} P(s' \mid s, a) V_w(s') - V_w(s).$$

Write $V_w = V + e$ and use the Bellman equation $Q(s, a) = r(s, a) + \gamma \sum_{s'} P(s' \mid s, a) V(s')$:

$$\mathbb{E}[\delta_t \mid S_t = s, A_t = a, T > t] = Q(s, a) - V_w(s) + \gamma \sum_{s'} P(s' \mid s, a) e(s').$$

Step 2 (sum over time). The terms of $u$ are bounded: in case (a) by $\gamma^t (R_{\max} + 2 \max |V_w|) \max \lVert \psi \rVert$, whose sum over $t$ converges; in case (b) there are at most $|S|$ terms. So we may take the expectation term by term and condition each term on $(S_t, A_t)$:

$$\mathbb{E}[u] = \sum_{t \ge 0} \gamma^t \sum_{s, a} \Pr(S_t = s, T > t)\, \pi(a \mid s)\, \psi(s, a)\, \mathbb{E}[\delta_t \mid S_t = s, A_t = a, T > t],$$

because given $S_t = s$ and $T > t$, $A_t$ has the law $\pi(\cdot \mid s)$. Summing over $t$ gives the weight $d(s)$, and $\pi(a \mid s) \psi(s, a) = \nabla_\theta \pi(a \mid s)$. With Step 1,

$$\mathbb{E}[u] = \sum_s d(s) \sum_a \nabla_\theta \pi(a \mid s) \Big(Q(s, a) - V_w(s) + \gamma \sum_{s'} P(s' \mid s, a) e(s')\Big).$$

Step 3 (the three terms). By the [policy gradient theorem](/policy-gradient-theorem/) in the start-state form, $\sum_s d(s) \sum_a \nabla_\theta \pi(a \mid s) Q(s, a) = \nabla J(\theta)$, with the same unnormalized discounted weights $d$. The term with $V_w(s)$ is zero, because $\sum_a \nabla_\theta \pi(a \mid s) = \nabla_\theta \sum_a \pi(a \mid s) = \nabla_\theta 1 = 0$ and $V_w(s)$ does not depend on $a$. The last term is the stated bias. When $V_w = V^\pi$, $e = 0$ and the bias is zero. $\square$

**Corollary (which errors matter).** The bias depends on $e$ only through the vector $c(s, a) = \sum_{s'} P(s' \mid s, a) e(s')$, the expected error of the bootstrap value. An error that is the same constant $\kappa$ on all nonterminal states gives $c(s, a) = \kappa (1 - \Pr(\text{end} \mid s, a))$, so it causes no bias when no action changes the probability of ending, and it can cause bias otherwise. An error of the critic in the current state never causes bias, since it enters only through $-V_w(S_t)$. $\blacksquare$
