---
tag: 57DPX1
kind: theorem
slug: policy-gradient-theorem
name: Policy gradient theorem
aliases:
- policy gradient theorem of Sutton et al.
area: machine-learning/reinforcement-learning
level: core
summary: "The gradient of the expected return of a policy pi_theta is sum_s d(s) sum_a grad pi(a | s) Q(s, a), with d the discounted state visits. It needs no derivative of the state distribution."
prereqs: [markov-decision-process, policy, action-value-function, gradient]
see_also: [reinforce, actor-critic, natural-policy-gradient, deterministic-policy-gradient, advantage-function, generalized-advantage-estimation, black-box-variational-inference, variational-autoencoder]
sources:
  - paper: "Richard S. Sutton, David McAllester, Satinder Singh and Yishay Mansour, Policy gradient methods for reinforcement learning with function approximation, Advances in Neural Information Processing Systems 12 (NIPS 1999), MIT Press, 2000, pages 1057 to 1063"
    locator: Theorem 1 (the policy gradient for the average reward and the start state formulations), Theorem 2 (compatible function approximation), Theorem 3 (convergence of policy iteration with function approximation)
  - paper: "Peter Marbach and John N. Tsitsiklis, Simulation-based optimization of Markov reward processes, IEEE Transactions on Automatic Control 46(2), 2001, pages 191 to 209"
    locator: the gradient formula of the average reward in terms of the stationary distribution and the differential values, and the simulation-based estimate
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 13.2 (the theorem and its proof for the episodic case), Section 13.4 (baselines), Section 13.6 (the continuing case)
  - paper: "Philip S. Thomas, Bias in natural actor-critic algorithms, Proceedings of the 31st International Conference on Machine Learning, PMLR 32(1), 2014, pages 441 to 448"
    locator: the discounted state weighting that common actor-critic algorithms drop, and the bias that results
  - paper: "Chris Nota and Philip S. Thomas, Is the policy gradient a gradient?, Proceedings of AAMAS 2020, pages 939 to 947"
    locator: the update without the gamma^t factor is not the gradient of any function
---

The policy gradient theorem gives the gradient of the expected return $J(\theta)$ of a parameterized [policy](/policy/) $\pi_\theta$ in a [Markov decision process](/markov-decision-process/). The gradient is a sum over states, weighted by how often the policy visits each state, of $\sum_a \nabla\pi(a \mid s)\, Q^\pi(s, a)$, where $Q^\pi$ is the [action value function](/action-value-function/). The visit frequencies depend on $\theta$, but their [gradient](/gradient/) does not appear. This is why the gradient can be estimated from sampled episodes, and it is the base of [REINFORCE](/reinforce/), [actor-critic](/actor-critic/) methods and their successors.

## Statement

**Setting.** A finite MDP $(S, A, P, R, \gamma)$ with a start distribution $\mu$. $P(s' \mid s, a)$ may sum to less than 1 over $s'$; the missing mass is the probability that the episode ends. For each $\theta \in \mathbb{R}^m$, $\pi_\theta(a \mid s)$ is a policy that is differentiable in $\theta$. Write $P_\pi(s, s') = \sum_a \pi(a \mid s) P(s' \mid s, a)$ and $r_\pi(s) = \sum_a \pi(a \mid s) R(s, a)$. Assume that $\sum_{t \ge 0} \gamma^t P_\pi^t$ converges for each $\theta$. This holds when $\gamma < 1$, and when $\gamma = 1$ in an episodic MDP where each policy ends the episode with probability 1.

**Start state formulation.** Let $J(\theta) = \sum_s \mu(s) V^{\pi_\theta}(s)$, the expected [discounted return](/discounted-return/), and let

$$d^\pi(s) = \sum_{t=0}^{\infty} \gamma^t \Pr(S_t = s \mid S_0 \sim \mu, \pi)$$

be the discounted state visitation. It is not normalized: $\sum_s d^\pi(s) = 1/(1-\gamma)$ when no episode ends. Then

$$\nabla J(\theta) = \sum_{s} d^{\pi}(s) \sum_{a} \nabla_\theta \pi_\theta(a \mid s)\, Q^{\pi}(s, a).$$

**Average reward formulation.** Assume instead that no episode ends and that $P_{\pi_\theta}$ has a unique stationary distribution $d^\pi$ for each $\theta$. Let $\rho(\theta) = \sum_s d^\pi(s) r_\pi(s)$ be the average reward, and let $Q^\pi(s, a) = R(s, a) - \rho + \sum_{s'} P(s' \mid s, a) h(s')$ be the differential action values, where $h$ solves $h = r_\pi - \rho \mathbf{1} + P_\pi h$ with $\sum_s d^\pi(s) h(s) = 0$. Then

$$\nabla \rho(\theta) = \sum_{s} d^{\pi}(s) \sum_{a} \nabla_\theta \pi_\theta(a \mid s)\, Q^{\pi}(s, a).$$

**Baselines.** For any function $b(s)$ that does not depend on $a$, the formulas stay true with $Q^\pi(s, a) - b(s)$ in place of $Q^\pi(s, a)$.

**Score function form.** Since $\nabla\pi = \pi\,\nabla\log\pi$, the start state formula is an expectation over episodes:

$$\nabla J(\theta) = \mathbb{E}\Big[\sum_{t \ge 0} \gamma^t\, \nabla_\theta \log \pi_\theta(A_t \mid S_t)\, Q^\pi(S_t, A_t)\Big].$$

This is the "log-derivative trick" applied to the policy. The same score function estimator appears in [black-box variational inference](/black-box-variational-inference/); the [variational autoencoder](/variational-autoencoder/) uses the reparameterization estimator instead, which needs a differentiable sample path.

**Compatible function approximation** (Theorem 2 of Sutton et al.). Let $f_w(s, a)$ be differentiable in $w$ with $\nabla_w f_w(s, a) = \nabla_\theta \log \pi_\theta(a \mid s)$ for all $s, a$. If $w$ is a stationary point of $\sum_s d^\pi(s) \sum_a \pi(a \mid s) (Q^\pi(s, a) - f_w(s, a))^2$, then

$$\nabla J(\theta) = \sum_s d^\pi(s) \sum_a \nabla_\theta \pi_\theta(a \mid s)\, f_w(s, a).$$

### A worked example

Two states, two actions, $\gamma = 1/2$, start in state 0, and a tabular softmax policy $\pi(a \mid s) = e^{\theta_{s,a}} / \sum_b e^{\theta_{s,b}}$ at $\theta = 0$, so each action has probability $1/2$. Then $\partial \pi(a \mid s) / \partial\theta_{s,b} = \pi(a \mid s)(1[a = b] - \pi(b \mid s))$, the softmax Jacobian of [softmax regression](/softmax-regression/).

| state | action | reward | to state 0 | to state 1 | end |
|---|---|---|---|---|---|
| 0 | 1 | 1 | 1/2 | 1/4 | 1/4 |
| 0 | 2 | 0 | 0 | 3/4 | 1/4 |
| 1 | 1 | 0 | 1/2 | 0 | 1/2 |
| 1 | 2 | 3 | 0 | 0 | 1 |

The Bellman equations give $V = (28/27, 44/27)$, so $J = 28/27$, and $Q(0, \cdot) = (79/54, 11/18)$, $Q(1, \cdot) = (7/27, 3)$. The equations $d = \mu + \gamma P_\pi^\top d$ give $d = (32/27, 8/27)$. The theorem gives

$$\frac{\partial J}{\partial \theta_{0,1}} = d(0) \cdot \tfrac14 \big(Q(0,1) - Q(0,2)\big) = \frac{184}{729}, \qquad \frac{\partial J}{\partial \theta_{1,1}} = d(1) \cdot \tfrac14 \big(Q(1,1) - Q(1,2)\big) = -\frac{148}{729},$$

and $\partial J / \partial\theta_{s,2} = -\partial J / \partial\theta_{s,1}$. These values equal the derivatives of the closed form of $J$, obtained by differentiating the linear system $(I - \gamma P_\pi)V = r_\pi$, and central differences of $J$ in floating point agree to $10^{-7}$.

## In plain words

An agent acts by a rule with adjustable knobs. We want to know which way to turn each knob to collect more reward. Turning a knob changes two things: the choices in each situation, and which situations the agent reaches later. The second effect looks hard to measure. The theorem says that we do not need to measure it. It is enough to look at each situation the agent visits, count later visits less, and ask: how much does this knob make each choice more likely, and how good is that choice? Add these up and you get the exact direction. You can also subtract any fixed amount from the value of the choices in a situation, and the answer stays the same, because the probabilities of all choices always sum to one.

## Proof

**Start state formulation.** The values solve $(I - \gamma P_\pi) V = r_\pi$. By the hypothesis, $I - \gamma P_\pi$ is invertible with inverse $\sum_t \gamma^t P_\pi^t$. Its entries are differentiable in $\theta$, so $V = (I - \gamma P_\pi)^{-1} r_\pi$ is differentiable, and so is $Q^\pi(s, a) = R(s, a) + \gamma \sum_{s'} P(s' \mid s, a) V(s')$. Fix one parameter coordinate and write $\nabla$ for the derivative in it. Since $R$ and $P$ do not depend on $\theta$, $\nabla Q^\pi(s, a) = \gamma \sum_{s'} P(s' \mid s, a) \nabla V(s')$. Differentiate $V(s) = \sum_a \pi(a \mid s) Q^\pi(s, a)$ with the product rule:

$$\nabla V(s) = \underbrace{\sum_a \nabla\pi(a \mid s)\, Q^\pi(s, a)}_{\phi(s)} + \gamma \sum_{s'} P_\pi(s, s')\, \nabla V(s').$$

In vector form, $(I - \gamma P_\pi)\nabla V = \phi$, so $\nabla V = \sum_{t \ge 0} \gamma^t P_\pi^t \phi$. Then

$$\nabla J = \mu^\top \nabla V = \sum_{t \ge 0} \gamma^t \mu^\top P_\pi^t \phi = \sum_s \Big(\sum_{t \ge 0} \gamma^t \Pr(S_t = s)\Big) \phi(s) = \sum_s d^\pi(s) \phi(s),$$

because $(\mu^\top P_\pi^t)(s) = \Pr(S_t = s)$ under $\pi$. The sums are finite or absolutely convergent, so the order of summation can change.

**Average reward formulation.** Assume that $\rho$ and $h$ are differentiable in $\theta$. (For a finite MDP with a unique stationary distribution for each $\theta$, they are rational functions of the entries of $\pi_\theta$, because they solve a nonsingular linear system together with the normalizations.) Let $V(s) = \sum_a \pi(a \mid s) Q^\pi(s, a) = h(s)$. Differentiate, using $\nabla Q^\pi(s, a) = -\nabla\rho + \sum_{s'} P(s' \mid s, a) \nabla h(s')$:

$$\nabla h(s) = \sum_a \nabla\pi(a \mid s) Q^\pi(s, a) - \nabla\rho + \sum_{s'} P_\pi(s, s') \nabla h(s').$$

Solve for $\nabla\rho$, multiply by $d^\pi(s)$ and sum over $s$. Since $\sum_s d^\pi(s) = 1$ and $\sum_s d^\pi(s) P_\pi(s, s') = d^\pi(s')$, the two terms in $\nabla h$ cancel:

$$\nabla\rho = \sum_s d^\pi(s) \sum_a \nabla\pi(a \mid s) Q^\pi(s, a) + \sum_{s'} d^\pi(s') \nabla h(s') - \sum_s d^\pi(s) \nabla h(s) = \sum_s d^\pi(s) \sum_a \nabla\pi(a \mid s) Q^\pi(s, a).$$

**Baselines.** $\sum_a \nabla\pi(a \mid s)\, b(s) = b(s)\, \nabla \sum_a \pi(a \mid s) = b(s)\, \nabla 1 = 0$, for each $s$.

**Score function form.** $\sum_s d^\pi(s) \sum_a \pi(a \mid s) \nabla\log\pi(a \mid s) Q^\pi(s, a) = \sum_t \gamma^t \sum_{s, a} \Pr(S_t = s, A_t = a) \nabla\log\pi(a \mid s) Q^\pi(s, a)$, which is the expectation stated above.

**Compatible function approximation.** The gradient of the weighted error in $w$ is zero at a stationary point:

$$\sum_s d^\pi(s) \sum_a \pi(a \mid s) \big(Q^\pi(s, a) - f_w(s, a)\big) \nabla_w f_w(s, a) = 0.$$

Replace $\nabla_w f_w$ by $\nabla_\theta \log\pi = \nabla_\theta\pi / \pi$. This gives $\sum_s d^\pi(s) \sum_a \nabla_\theta\pi(a \mid s)(Q^\pi(s, a) - f_w(s, a)) = 0$. Subtract it from the start state formula. $\blacksquare$

## Consequences

- **Sampled gradients.** The score function form is an expectation over episodes of the current policy. Replace $Q^\pi(S_t, A_t)$ by the return $G_t$ and you get [REINFORCE](/reinforce/). Replace it by a [TD error](/td-error/) of a learned critic and you get [actor-critic](/actor-critic/). The baseline result lets both subtract a value estimate, which turns $Q^\pi$ into the [advantage function](/advantage-function/) $A^\pi = Q^\pi - V^\pi$ and lowers the variance. [Generalized advantage estimation](/generalized-advantage-estimation/) trades bias for variance in this estimate.
- **Natural gradients.** With compatible features $\psi = \nabla\log\pi$, the compatible weights are the [natural policy gradient](/natural-policy-gradient/) $F^{-1}\nabla J$ (Kakade 2001), which leads to [TRPO](/trpo/) and [PPO](/ppo/).
- **Deterministic policies.** The [deterministic policy gradient](/deterministic-policy-gradient/) theorem is the limit of this theorem when the policy's variance goes to zero.
- **Convergence with function approximation.** Theorem 3 of Sutton et al. uses the compatible result for policy iteration with a compatible critic: with bounded rewards, bounded second derivatives of $\pi_\theta$ and step sizes $\alpha_k$ with $\sum_k \alpha_k = \infty$ and $\sum_k \alpha_k^2 < \infty$, the gradient of the objective tends to zero.
- **Stationary points.** $J$ is not concave in $\theta$ in general, so gradient ascent finds stationary points, not optima. For the tabular softmax policy the theorem gives $\partial J / \partial\theta_{s,a} = d^\pi(s)\, \pi(a \mid s)\, A^\pi(s, a)$. So if $d^\pi(s) > 0$ in every state, a stationary point with finite $\theta$ has $A^\pi = 0$ everywhere, which is the [Bellman optimality equation](/bellman-optimality-equation/) for $V^\pi$, and the policy is optimal.

## Tightness

**The factor $\gamma^t$ cannot be dropped.** Many implementations weight the states by the undiscounted visitation $\sum_t \Pr(S_t = s)$, or sample states from the on-policy distribution, while they keep the discounted $Q^\pi$. This is not the gradient of $J$ when $\gamma < 1$ (Thomas 2014), and Nota and Thomas (2020) showed that the resulting update is in general not the gradient of any function. In the worked example the undiscounted visits are $(8/5, 4/5)$, and the per state blocks become $46/135$ and $-74/135$ instead of $184/729$ and $-148/729$. Now let one parameter $\omega$ play the role of $\theta_{0,1}$ and $\theta_{1,1}$ at the same time (with $\theta_{s,2} = 0$). The true derivative is $dJ/d\omega = 184/729 - 148/729 = 4/81 > 0$, but the undiscounted weighting gives $46/135 - 74/135 = -28/135 < 0$. So the common update moves $\omega$ in the direction that lowers $J$. With $\gamma = 1$ in an episodic task the two weightings are equal.

**The baseline must not depend on the action.** With $b(s, a)$ the term $\sum_a \nabla\pi(a \mid s)\, b(s, a)$ is not zero in general. A state-dependent baseline is the most that the identity allows without a correction term.

**Compatibility is needed for Theorem 2.** For features that are not $\nabla\log\pi$, the best least squares fit of $Q^\pi$ does not in general give the true gradient, since the residual is then orthogonal to the features but not to $\nabla\log\pi$.

## History

Williams (1992) gave the likelihood ratio estimator for episodic tasks in the REINFORCE algorithms. Sutton, McAllester, Singh and Mansour stated the theorem in both the average reward and the start state forms at NIPS 1999, published in 2000, together with the compatible function approximation result and a convergence proof for policy iteration with function approximation. Marbach and Tsitsiklis (2001) derived the same gradient formula for the average reward of parameterized Markov reward processes, with simulation-based estimates. Konda and Tsitsiklis found the compatible features at the same time in their work on actor-critic methods. Thomas (2014) pointed out that common discounted actor-critic algorithms drop the $\gamma^t$ weighting, and Nota and Thomas (2020) studied what these updates compute.

## References
