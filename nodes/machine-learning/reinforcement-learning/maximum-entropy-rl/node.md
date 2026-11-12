---
tag: X97YP9
kind: concept
slug: maximum-entropy-rl
name: Maximum entropy reinforcement learning
aliases:
- entropy-regularized RL
- MaxEnt RL
- soft reinforcement learning
area: machine-learning/reinforcement-learning
level: advanced
summary: "Reinforcement learning whose objective adds alpha times the policy entropy to every reward. The soft Bellman equation uses a log-sum-exp, and the best policy is a softmax of Q / alpha."
prereqs: [markov-decision-process, shannon-entropy, bellman-optimality-equation]
see_also: [soft-actor-critic, log-sum-exp-trick, value-iteration, bellman-contraction, softmax-regression, mirror-descent, a3c, ppo]
sources:
  - paper: "Brian D. Ziebart, Andrew Maas, J. Andrew Bagnell and Anind K. Dey, Maximum entropy inverse reinforcement learning, Proceedings of the 23rd AAAI Conference on Artificial Intelligence, 2008, pages 1433 to 1438"
    locator: Sections 3 and 4 (the maximum entropy distribution over paths and the soft value recursion)
  - paper: "Tuomas Haarnoja, Haoran Tang, Pieter Abbeel and Sergey Levine, Reinforcement learning with deep energy-based policies, Proceedings of the 34th International Conference on Machine Learning, PMLR 70, 2017, arXiv:1702.08165"
    locator: Section 2 (the maximum entropy objective), Section 3 (soft value functions, the optimal energy-based policy, soft Q-iteration), Appendix A (proofs)
  - paper: "Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel and Sergey Levine, Soft actor-critic: off-policy maximum entropy deep reinforcement learning with a stochastic actor, Proceedings of the 35th International Conference on Machine Learning, PMLR 80, 2018, arXiv:1801.01290"
    locator: Section 3.1 (the maximum entropy objective and its discounted form)
  - paper: "Sergey Levine, Reinforcement learning and control as probabilistic inference: tutorial and review, arXiv:1805.00909, 2018"
    locator: Sections 2 and 3 (control as inference, the soft Bellman backup, the variational view)
  - paper: "Roy Fox, Ari Pakman and Naftali Tishby, Taming the noise in reinforcement learning via soft updates, Proceedings of the 32nd Conference on Uncertainty in Artificial Intelligence, 2016, arXiv:1512.08562"
    locator: Section 3 (G-learning, the soft backup with a prior policy)
---

Maximum entropy reinforcement learning changes the goal of an agent in a [Markov decision process](/markov-decision-process/): the agent maximizes $J_\alpha(\pi) = \mathbb{E}_\pi\big[\sum_{t \ge 0} \gamma^t \big(r_t + \alpha \mathcal{H}(\pi(\cdot \mid s_t))\big)\big]$, the expected return plus $\alpha > 0$ times the [Shannon entropy](/shannon-entropy/) of the policy in each state it visits. The best policy is then stochastic: $\pi^*(a \mid s) = \exp\big((Q_{\text{soft}}(s, a) - V_{\text{soft}}(s)) / \alpha\big)$, a softmax of the soft action values, and the values satisfy the soft Bellman equation $V_{\text{soft}}(s) = \alpha \log \sum_a \exp(Q_{\text{soft}}(s, a) / \alpha)$, in which the maximum of the [Bellman optimality equation](/bellman-optimality-equation/) becomes a [log-sum-exp](/log-sum-exp-trick/). The temperature $\alpha$ sets the balance: as $\alpha \to 0$ the soft values tend to the ordinary optimal values. The objective gives exploration, robustness and a policy that keeps all good actions; it is the basis of soft Q-learning and [soft actor-critic](/soft-actor-critic/).

## In plain words

An ordinary agent only wants the most reward. A maximum entropy agent also wants to stay as random as it can while it still earns reward. It pays itself a small bonus for being unsure. So when two actions are almost equally good, it keeps both and tries each often, in place of picking one at random and forgetting the other. A temperature knob sets the size of the bonus. With a high temperature the agent acts almost at random. With the knob near zero it acts like an ordinary agent that only wants reward.

## The idea

Take a finite discounted MDP with states $S$, actions $A$, rewards $R(s, a)$, transitions $P(s' \mid s, a)$ and $0 \le \gamma < 1$. For a stationary [policy](/policy/) $\pi$, the soft action value and soft state value satisfy

$$Q^\pi(s, a) = R(s, a) + \gamma \sum_{s'} P(s' \mid s, a) V^\pi(s'), \qquad V^\pi(s) = \sum_a \pi(a \mid s) Q^\pi(s, a) + \alpha \mathcal{H}(\pi(\cdot \mid s)).$$

**One state.** The key fact is the Gibbs variational principle: for any vector $q \in \mathbb{R}^A$ and $\alpha > 0$,

$$\max_{p \in \Delta(A)} \Big(\sum_a p_a q_a + \alpha \mathcal{H}(p)\Big) = \alpha \log \sum_a e^{q_a / \alpha},$$

and the maximum is attained only at $p_a = e^{q_a / \alpha} / \sum_b e^{q_b / \alpha}$. To see it, write $L = \alpha \log \sum_b e^{q_b/\alpha}$ and $g_a = e^{(q_a - L)/\alpha}$; then $\sum_a p_a q_a + \alpha \mathcal{H}(p) = L - \alpha \sum_a p_a \log(p_a / g_a) = L - \alpha\, \mathrm{KL}(p \,\|\, g)$, and the Kullback-Leibler divergence is zero only at $p = g$.

**Soft Bellman equation.** Applying the principle in every state gives the soft optimality equation

$$Q^*(s, a) = R(s, a) + \gamma \sum_{s'} P(s' \mid s, a) V^*(s'), \qquad V^*(s) = \alpha \log \sum_a e^{Q^*(s, a)/\alpha},$$

with the optimal policy $\pi^*(a \mid s) = e^{(Q^*(s, a) - V^*(s))/\alpha}$. The soft backup $V \mapsto \alpha \log \sum_a e^{Q_V(s, a)/\alpha}$ is monotone and moves by exactly $\gamma c$ when $V$ moves by a constant $c$, so it is a $\gamma$-contraction in the maximum norm, just like the hard backup ([Bellman contraction](/bellman-contraction/)). Soft value iteration therefore converges from any start to the unique fixed point, which is the soft optimal value. In code, $\alpha \log \sum_a e^{q_a/\alpha}$ must be evaluated as $m + \alpha \log \sum_a e^{(q_a - m)/\alpha}$ with $m = \max_a q_a$, or the exponentials overflow when $q / \alpha$ is large, which is the common case for small $\alpha$.

**Small temperature.** For any $q$, $\max_a q_a \le \alpha \log \sum_a e^{q_a/\alpha} \le \max_a q_a + \alpha \log |A|$. Carried through the contraction, this gives $V^*_{\text{hard}}(s) \le V^*_\alpha(s) \le V^*_{\text{hard}}(s) + \alpha \log |A| / (1 - \gamma)$. So as $\alpha \to 0$ the soft values tend to the hard optimal values, and the soft optimal policy puts its mass on the greedy actions.

**Continuous actions.** The sum becomes an integral, $V(s) = \alpha \log \int \exp(Q(s, a)/\alpha)\, da$, which has no closed form for a general $Q$; soft Q-learning samples from the energy-based policy, and soft actor-critic fits a Gaussian policy by minimizing a Kullback-Leibler divergence to it.

**Inference view.** If optimality at each step is a binary event with probability proportional to $e^{r_t/\alpha}$, then, for a finite horizon without discount and with deterministic dynamics, the posterior over trajectories given optimality at all steps is the trajectory law of the soft optimal policy; with stochastic dynamics the exact posterior is too optimistic, and the variational approximation that fixes the dynamics gives exactly the maximum entropy objective (Levine 2018).

## Examples

**One step.** One state, two actions, rewards $0$ and $\log 2$, and the episode ends after one step. With $\alpha = 1$ the soft value is $\log(e^0 + e^{\log 2}) = \log 3$, and the optimal policy is $(\tfrac13, \tfrac23)$. Its expected reward is $\tfrac23 \log 2$ and its entropy is $\log 3 - \tfrac23 \log 2$; the sum is $\log 3$, as the principle says. The greedy policy earns $\log 2 < \log 3$ in this objective.

**Two states.** In the two-state MDP with $P = [[[1/2, 1/4], [0, 3/4]], [[1/2, 0], [0, 0]]]$ (missing mass ends the episode), $R = [[1, 0], [0, 3]]$ and $\gamma = \tfrac12$, the hard optimal values are $V^* = (\tfrac{11}6, 3)$. Soft value iteration gives:

| $\alpha$ | $V_\alpha(0)$ | $V_\alpha(1)$ | $\pi^*(a_0 \mid 0)$ | $\pi^*(a_1 \mid 1)$ |
|---|---|---|---|---|
| 2 | 3.2371 | 3.5770 | 0.6124 | 0.7494 |
| 1 | 2.3371 | 3.0855 | 0.6927 | 0.9180 |
| 0.5 | 1.9702 | 3.0033 | 0.8151 | 0.9934 |
| 0.1 | 1.8334 | 3.0000 | 0.9992 | 1.0000 |
| hard | 1.8333 | 3 | 1 | 1 |

Each value lies between $V^*$ and $V^* + 2\alpha \log 2$. The policy approaches the greedy policy as $\alpha$ falls, and state 1, whose best action is clearly better, becomes nearly deterministic first.

## Where it is used

- **Soft Q-learning and soft actor-critic.** Haarnoja et al. learn soft values with neural networks; [soft actor-critic](/soft-actor-critic/) adds an actor and is a standard method for continuous control.
- **Maximum entropy inverse reinforcement learning.** Ziebart et al. model expert behaviour as the soft optimal policy for an unknown reward and fit the reward by maximum likelihood.
- **Entropy bonuses in policy gradient methods.** [A3C](/a3c/) and [PPO](/ppo/) add $\beta \mathcal{H}(\pi(\cdot \mid s_t))$ to the loss at sampled states to delay premature convergence. This regularizes only the current state, not the future entropy, so it is a weaker form of the same idea.
- **KL-regularized control.** Replacing the entropy by $-\mathrm{KL}(\pi \,\|\, \pi_0)$ to a prior policy gives G-learning and the policy updates of [mirror descent](/mirror-descent/) style methods; the soft backup becomes $\alpha \log \sum_a \pi_0(a \mid s) e^{Q(s, a)/\alpha}$.
- **Linearly solvable control and control as inference**, where the exponentiated soft value solves a linear equation in some problem classes.

## References
