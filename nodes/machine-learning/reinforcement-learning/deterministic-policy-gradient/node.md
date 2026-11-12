---
tag: KFKT3Y
kind: theorem
slug: deterministic-policy-gradient
name: Deterministic policy gradient theorem
aliases:
- DPG theorem
- deterministic policy gradient theorem of Silver et al.
area: machine-learning/reinforcement-learning
level: advanced
summary: "For a deterministic policy a = mu_theta(s), the gradient of the return is E over discounted visits of grad mu_theta(s) times grad_a Q(s, a) at a = mu_theta(s). No integral over actions is needed."
prereqs: [policy-gradient-theorem, action-value-function]
see_also: [ddpg, td3, actor-critic, soft-actor-critic, natural-policy-gradient, importance-sampling-off-policy, q-learning, markov-decision-process]
sources:
  - paper: "David Silver, Guy Lever, Nicolas Heess, Thomas Degris, Daan Wierstra and Martin Riedmiller, Deterministic policy gradient algorithms, Proceedings of the 31st International Conference on Machine Learning, PMLR 32(1), 2014, pages 387 to 395"
    locator: Section 3.1 Theorem 1 (the deterministic policy gradient theorem), Section 3.3 Theorem 2 (the limit of stochastic policy gradients), Section 4.2 (off-policy deterministic actor-critic), Section 4.3 Theorem 3 (compatible function approximation), supplementary material (regularity conditions and proofs)
  - paper: "Richard S. Sutton, David McAllester, Satinder Singh and Yishay Mansour, Policy gradient methods for reinforcement learning with function approximation, Advances in Neural Information Processing Systems 12 (NIPS 1999), MIT Press, 2000, pages 1057 to 1063"
    locator: Theorem 1 (the stochastic policy gradient theorem that the deterministic theorem parallels)
  - paper: "Timothy P. Lillicrap, Jonathan J. Hunt, Alexander Pritzel, Nicolas Heess, Tom Erez, Yuval Tassa, David Silver and Daan Wierstra, Continuous control with deep reinforcement learning, International Conference on Learning Representations, 2016, arXiv:1509.02971"
    locator: Section 3 (the actor update by the deterministic policy gradient with a deep critic)
---

The deterministic policy gradient (DPG) theorem of Silver, Lever, Heess, Degris, Wierstra and Riedmiller (2014) gives the gradient of the expected return of a deterministic policy $a = \mu_\theta(s)$ over a continuous action space:

$$\nabla_\theta J(\mu_\theta) = \mathbb{E}_{s \sim \rho^\mu}\left[\nabla_\theta \mu_\theta(s)\, \nabla_a Q^\mu(s, a)\big|_{a = \mu_\theta(s)}\right].$$

It is the deterministic counterpart of the stochastic [policy gradient theorem](/policy-gradient-theorem/): as there, the gradient of the state distribution does not appear. Unlike there, the expectation is over states only, because a deterministic policy has no action distribution to integrate over. The formula is a chain rule: move the action in the direction in which the [action value](/action-value-function/) $Q^\mu$ increases, and move the parameters so that the action moves that way. It is the base of off-policy actor-critic methods for continuous control: [DDPG](/ddpg/), [TD3](/td3/) and, through the reparameterized gradient, [soft actor-critic](/soft-actor-critic/).

## Statement

**Setting.** A [Markov decision process](/markov-decision-process/) with state space $\mathcal{S}$, action space $\mathcal{A} = \mathbb{R}^n$, transition kernel $p(s' \mid s, a)$, reward $r(s, a)$, start law $p_1$ and discount $0 \le \gamma < 1$. A deterministic policy $\mu_\theta : \mathcal{S} \to \mathcal{A}$ with $\theta \in \mathbb{R}^m$. Write $\nabla_\theta \mu_\theta(s)$ for the $m \times n$ matrix whose column $j$ is the gradient of the $j$-th action coordinate. The objective is $J(\mu_\theta) = \mathbb{E}[\sum_{t \ge 0} \gamma^t r(S_t, \mu_\theta(S_t))]$ with $S_0 \sim p_1$. The discounted state visitation is

$$\rho^\mu(B) = \sum_{t \ge 0} \gamma^t \Pr(S_t \in B \mid S_0 \sim p_1, \mu_\theta),$$

a measure of total mass $1/(1 - \gamma)$, not a probability. $V^\mu(s) = Q^\mu(s, \mu_\theta(s))$ and $Q^\mu(s, a) = r(s, a) + \gamma \int V^\mu(s')\, p(ds' \mid s, a)$.

**Regularity.** Assume that (R1) $Q^{\mu}(s, a)$ is differentiable in $a$ and $\mu_\theta(s)$ is differentiable in $\theta$; (R2) $V^{\mu_\theta}(s)$ is differentiable in $\theta$, with $\sup_s \|\nabla_\theta V^{\mu_\theta}(s)\| < \infty$; (R3) derivatives in $\theta$ and $a$ may be taken inside the integrals over $s'$ and $S_0$. Silver et al. derive these from continuity and boundedness conditions on $p$, $\nabla_a p$, $r$, $\nabla_a r$, $\mu_\theta$, $\nabla_\theta \mu_\theta$ and $p_1$ (their supplementary material).

**Theorem 1 (deterministic policy gradient).** Under (R1) to (R3),

$$\nabla_\theta J(\mu_\theta) = \int_{\mathcal{S}} \nabla_\theta \mu_\theta(s)\, \nabla_a Q^\mu(s, a)\big|_{a = \mu_\theta(s)}\, \rho^\mu(ds).$$

**Theorem 2 (limit of stochastic policy gradients).** Let $\pi_{\theta, \sigma}$ be a family of stochastic policies such that $\pi_{\theta, 0} = \mu_\theta$, for example $a = \mu_\theta(s) + \sigma \xi$ with $\xi$ standard normal. Under conditions on the family (Silver et al., Section 3.3), $\lim_{\sigma \downarrow 0} \nabla_\theta J(\pi_{\theta, \sigma}) = \nabla_\theta J(\mu_\theta)$, where the left side is the stochastic policy gradient.

**Theorem 3 (compatible function approximation).** A critic $Q^w(s, a)$ with $\nabla_a Q^w(s, a)|_{a = \mu_\theta(s)} = \nabla_\theta \mu_\theta(s)^\top w$, whose $w$ minimizes $\int \|\nabla_a Q^w(s, \mu_\theta(s)) - \nabla_a Q^\mu(s, \mu_\theta(s))\|^2 \rho^\mu(ds)$, gives the exact gradient when it replaces $Q^\mu$ in Theorem 1. An example is $Q^w(s, a) = (a - \mu_\theta(s))^\top \nabla_\theta \mu_\theta(s)^\top w + V^v(s)$ for any baseline $V^v$.

## In plain words

A deterministic rule picks one exact action in each situation, such as how hard to push a pedal. To improve the rule, ask in each situation the agent meets: if the push were a little harder, would the long-run reward go up or down, and by how much? Then turn the knobs of the rule so that the push changes in that direction. Average this over the situations the agent meets, counting later ones less. That is the exact direction of improvement. As with stochastic rules, the knobs also change which situations the agent reaches later, but this effect does not need to be measured.

## Proof

Fix $\theta$ and write $\mu = \mu_\theta$, $V = V^\mu$, $Q = Q^\mu$ and $g(s) = \nabla_\theta \mu_\theta(s)\, \nabla_a Q(s, a)|_{a = \mu_\theta(s)}$.

**Step 1 (one-step recursion).** $V(s) = Q_\theta(s, \mu_\theta(s))$, where $Q_\theta(s, a) = r(s, a) + \gamma \int V^{\mu_\theta}(s')\, p(ds' \mid s, a)$ depends on $\theta$ in two ways: through the action argument and through $V^{\mu_\theta}$ inside the integral. By (R1) to (R3) and the chain rule,

$$\nabla_\theta V(s) = \nabla_\theta \mu_\theta(s)\, \nabla_a Q(s, a)\big|_{a = \mu(s)} + \gamma \int \nabla_\theta V(s')\, p(ds' \mid s, \mu(s)) = g(s) + \gamma\, \mathbb{E}[\nabla_\theta V(S_1) \mid S_0 = s].$$

The first term holds $V^{\mu_\theta}$ inside $Q$ fixed and moves the action; the second holds the action fixed at $\mu(s)$ and moves $V^{\mu_\theta}$.

**Step 2 (unrolling).** Apply Step 1 to $\nabla_\theta V(S_1)$, then to $\nabla_\theta V(S_2)$, and so on, with the trajectory of $\mu$. After $n$ steps,

$$\nabla_\theta V(s) = \sum_{t=0}^{n-1} \gamma^t\, \mathbb{E}[g(S_t) \mid S_0 = s] + \gamma^n\, \mathbb{E}[\nabla_\theta V(S_n) \mid S_0 = s].$$

By (R2) the last term is at most $\gamma^n \sup_{s'} \|\nabla_\theta V(s')\|$, which tends to 0. So $\nabla_\theta V(s) = \sum_{t \ge 0} \gamma^t\, \mathbb{E}[g(S_t) \mid S_0 = s]$; the series converges because its partial sums converge.

**Step 3 (start law).** $J(\mu_\theta) = \int V^{\mu_\theta}(s)\, p_1(ds)$, and $p_1$ does not depend on $\theta$. By (R3), $\nabla_\theta J = \int \nabla_\theta V(s)\, p_1(ds) = \sum_{t \ge 0} \gamma^t\, \mathbb{E}[g(S_t)] = \int g(s)\, \rho^\mu(ds)$, which is Theorem 1.

**Theorem 2, one-step Gaussian case.** Let $\gamma = 0$, one state, a scalar action and $a = \theta + \sigma \xi$ with $\xi \sim N(0, 1)$; let $r$ be continuously differentiable with $|r'(a)| \le C(1 + |a|^k)$. Then $J(\pi_{\theta, \sigma}) = \mathbb{E}[r(\theta + \sigma \xi)]$, and differentiation under the expectation gives $\nabla_\theta J(\pi_{\theta, \sigma}) = \mathbb{E}[r'(\theta + \sigma\xi)]$. This equals the score function form $\mathbb{E}[\frac{\xi}{\sigma} r(\theta + \sigma\xi)]$ by Gaussian integration by parts ($\mathbb{E}[\xi f(\xi)] = \mathbb{E}[f'(\xi)]$). As $\sigma \downarrow 0$, $r'(\theta + \sigma\xi) \to r'(\theta)$ for every $\xi$, and the bound $C(1 + (|\theta| + |\xi|)^k)$ is integrable, so dominated convergence gives the limit $r'(\theta)$, the deterministic gradient. The general case follows the same pattern with the conditions of Silver et al.

**Theorem 3.** By the minimizing property, the derivative of the error in $w$ is zero: $\int \nabla_\theta \mu_\theta(s) \left(\nabla_a Q^w(s, \mu(s)) - \nabla_a Q(s, \mu(s))\right) \rho^\mu(ds) = 0$, using $\nabla_w [\nabla_a Q^w(s, \mu(s))] = \nabla_\theta \mu_\theta(s)^\top$ by compatibility. So $\int \nabla_\theta \mu_\theta\, \nabla_a Q^w\, \rho^\mu(ds) = \int \nabla_\theta \mu_\theta\, \nabla_a Q\, \rho^\mu(ds) = \nabla_\theta J$ by Theorem 1. For the example critic, $\nabla_a Q^w(s, a) = \nabla_\theta \mu_\theta(s)^\top w$ for every $a$, so it is compatible. $\blacksquare$

## Consequences

- **Worked example.** Take the scalar system $s' = s + a + w$ with $w = \pm\tfrac12$ with equal probability, reward $r(s, a) = -(s^2 + a^2)$, $\gamma = \tfrac12$, start state $s_0 = 1$, and the linear policy $\mu(s) = k s + c$ at $(k, c) = (-\tfrac12, 0)$. Then $V^\mu(s) = -\tfrac{10}{7} s^2 - \tfrac{5}{14}$, $J = -\tfrac{25}{14}$, and $\nabla_a Q^\mu(s, a) = -2a - \tfrac{10}{7}(s + a)$. Theorem 1 gives $\nabla J = (\tfrac{20}{49}, \tfrac{8}{21})$, which matches the derivative of the closed-form return. The positive first coordinate says that the feedback gain $-\tfrac12$ is too strong: the best gain with $c = 0$ is near $-0.414$.
- **Lower variance with many action dimensions.** The stochastic gradient integrates over actions, and its score function estimate has variance that grows as the policy's noise shrinks. The deterministic gradient has no action integral, which Silver et al. found to help most in high-dimensional action spaces.
- **Off-policy learning without importance weights on actions.** Since no action is sampled from $\mu$, an actor can follow the gradient $\int \nabla_\theta \mu_\theta\, \nabla_a Q^\mu\, \rho^\beta(ds)$ under the states of an exploratory behaviour policy $\beta$, with a critic learned by [Q-learning](/q-learning/)-style targets. This off-policy gradient drops a term, as in the off-policy actor-critic of Degris et al., and is the update of [DDPG](/ddpg/) and [TD3](/td3/).
- **Reparameterized policies.** For $a = f_\theta(s, \xi)$ with fixed noise $\xi$, the same chain rule gives $\mathbb{E}[\nabla_\theta f_\theta(s, \xi)\, \nabla_a Q(s, a)]$, the actor update of [soft actor-critic](/soft-actor-critic/).
- **Linear quadratic control.** For linear dynamics, quadratic costs and a linear policy, $Q^\mu$ is quadratic and the theorem gives the gradient of the cost with respect to the feedback gain in closed form.

## Tightness

**Differentiability in the action is needed.** For discrete actions, or a reward with a kink such as $r(s, a) = -|a|$ at the policy's action, $\nabla_a Q^\mu$ does not exist and the theorem does not apply; the stochastic theorem still does.

**The limit in Theorem 2 is not an identity.** For one step with $r(a) = -(a - 2)^4$ and $a \sim N(\theta, \sigma^2)$, the stochastic gradient is $-(4x^3 + 12 x \sigma^2)$ with $x = \theta - 2$, and the deterministic gradient is $-4x^3$. The gap $12 x \sigma^2$ vanishes only as $\sigma \to 0$. For a reward quadratic in $a$, Gaussian noise only adds a constant to the return and the two gradients agree for every $\sigma$.

**No exploration.** The on-policy deterministic gradient uses only the actions $\mu_\theta(s)$, so its critic never sees other actions and $\nabla_a Q^\mu$ must be learned from off-policy data or extrapolated. This is why practical methods are off-policy with exploration noise.

**The off-policy form is an approximation.** With states from $\rho^\beta$ instead of $\rho^\mu$, the formula is not the gradient of $J(\mu_\theta)$ nor of the return under $\beta$ in general.

## History

Sutton, McAllester, Singh and Mansour (2000) proved the stochastic policy gradient theorem. It had been widely believed that a deterministic policy gradient did not exist, or could only be obtained with a model of the environment. Silver, Lever, Heess, Degris, Wierstra and Riedmiller (ICML 2014) proved Theorem 1, showed that it is the limit of the stochastic theorem, gave compatible critics, and built on-policy and off-policy deterministic actor-critic algorithms, including COPDAC-Q. Lillicrap et al. (2016) combined the theorem with deep networks, replay and target networks in [DDPG](/ddpg/), and Fujimoto, van Hoof and Meger (2018) improved that in [TD3](/td3/).

## References
