---
tag: H7XRK4
kind: concept
slug: advantage-function
name: Advantage function
aliases:
area: machine-learning/reinforcement-learning
level: core
summary: "A^pi(s, a) = Q^pi(s, a) - V^pi(s): how much better action a is than the average action of the policy pi in state s. Its mean under pi is zero."
prereqs: [action-value-function]
see_also: [policy-improvement-theorem, policy-gradient-theorem, actor-critic, a2c, generalized-advantage-estimation, dueling-network, td-error, trpo]
sources:
  - paper: "Leemon C. Baird III, Advantage Updating, Technical Report WL-TR-93-1146, Wright Laboratory, Wright-Patterson Air Force Base, 1993"
    title: Advantage Updating
    locator: "the definition of the advantage and the small time step argument"
  - paper: "Sham Kakade and John Langford, Approximately Optimal Approximate Reinforcement Learning, Proceedings of the 19th International Conference on Machine Learning (ICML), 2002"
    title: Approximately Optimal Approximate Reinforcement Learning
    locator: "Section 6 (the performance difference lemma)"
  - paper: "John Schulman, Philipp Moritz, Sergey Levine, Michael I. Jordan and Pieter Abbeel, High-Dimensional Continuous Control Using Generalized Advantage Estimation, ICLR 2016, arXiv:1506.02438"
    title: High-Dimensional Continuous Control Using Generalized Advantage Estimation
    locator: "Section 2 (advantage in the policy gradient), Section 3 (the estimator)"
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: "Section 13.4 (REINFORCE with a baseline), Section 13.5 (actor-critic methods)"
---

The advantage function of a [policy](/policy/) $\pi$ is $A^\pi(s, a) = Q^\pi(s, a) - V^\pi(s)$, the [action value](/action-value-function/) minus the [state value](/state-value-function/). It tells how much better it is to take action $a$ once in state $s$, and then follow $\pi$, than to follow $\pi$ from $s$ at once. Policy improvement, the performance difference lemma and most policy gradient methods are stated in terms of $A^\pi$.

## In plain words

An agent follows a fixed way of acting. In some situation it can try one particular choice and then go back to its usual way. The advantage of that choice is the gain in expected long term reward compared with the usual way. A positive advantage marks a choice that is better than the usual one. A negative advantage marks a worse one. If the agent picks its choices in its usual way, the mean advantage is zero, because the usual way is the reference. An optimal agent has no choice with a positive advantage. Learning methods use the advantage to make good choices more likely and bad choices less likely. It is a better signal than the raw reward, because it removes the part of the reward that comes from the situation and not from the choice.

## The idea

Fix a finite discounted MDP $(S, A, P, R, \gamma)$ with $0 \le \gamma < 1$ and a stationary policy $\pi$. Define

$$A^\pi(s, a) = Q^\pi(s, a) - V^\pi(s) = R(s, a) + \gamma \sum_{s'} P(s' \mid s, a) V^\pi(s') - V^\pi(s).$$

**Zero mean under $\pi$.** Because $V^\pi(s) = \sum_a \pi(a \mid s) Q^\pi(s, a)$,

$$\sum_a \pi(a \mid s)\, A^\pi(s, a) = 0 \quad \text{for every } s.$$

So $A^\pi(s, \cdot)$ always has some entries $\ge 0$ on the support of $\pi(\cdot \mid s)$.

**The expected TD error.** Let $\delta_t = R_{t+1} + \gamma V^\pi(S_{t+1}) - V^\pi(S_t)$, the [TD error](/td-error/) for the true value. Then $\mathbb{E}[\delta_t \mid S_t = s, A_t = a] = A^\pi(s, a)$. So $\delta_t$ is an unbiased one-sample estimate of the advantage of the action that was taken, if $V^\pi$ is known.

**The optimal advantage.** For an optimal policy, $A^*(s, a) = Q^*(s, a) - V^*(s) \le 0$, with $\max_a A^*(s, a) = 0$. An action is optimal in $s$ exactly when its optimal advantage is 0.

**The performance difference lemma** (Kakade and Langford 2002). For any two stationary policies $\pi, \pi'$ and a start distribution $\mu$,

$$\mathbb{E}_{s_0 \sim \mu}\left[V^{\pi'}(s_0) - V^\pi(s_0)\right] = \frac{1}{1-\gamma}\, \mathbb{E}_{s \sim d^{\pi'}_\mu}\, \mathbb{E}_{a \sim \pi'(\cdot \mid s)}\left[A^\pi(s, a)\right],$$

where $d^{\pi'}_\mu(s) = (1-\gamma) \sum_t \gamma^t \Pr^{\pi'}_\mu(S_t = s)$ is the discounted occupancy of $\pi'$.

*Proof.* Run $\pi'$ from $S_0 \sim \mu$. Since $V^\pi$ is bounded and $\gamma^t \to 0$, the sum $\sum_{t \ge 0} \gamma^t \left(\gamma V^\pi(S_{t+1}) - V^\pi(S_t)\right)$ telescopes to $-V^\pi(S_0)$. Add it to the return of $\pi'$:

$$V^{\pi'}(S_0) - V^\pi(S_0) = \mathbb{E}^{\pi'}\left[\sum_{t \ge 0} \gamma^t \left(R_{t+1} + \gamma V^\pi(S_{t+1}) - V^\pi(S_t)\right) \,\middle|\, S_0\right].$$

The term at step $t$ has the conditional mean $A^\pi(S_t, A_t)$ given $(S_t, A_t)$, by the TD error identity, because the dynamics do not depend on the policy. Sum over $t$ and use the definition of $d^{\pi'}_\mu$. $\blacksquare$

**Policy improvement.** If $\sum_a \pi'(a \mid s) A^\pi(s, a) \ge 0$ in every state, the lemma with $\mu$ a point mass gives $V^{\pi'} \ge V^\pi$ in every state. The greedy policy $\pi'(s) \in \arg\max_a A^\pi(s, a)$ meets this condition, since the max is at least the mean 0. This is the [policy improvement theorem](/policy-improvement-theorem/). The weights $d^{\pi'}$ come from the new policy. Methods such as [TRPO](/trpo/) replace them with $d^\pi$, and bound the error of that change.

**A baseline in the policy gradient.** The [policy gradient theorem](/policy-gradient-theorem/) gives $\nabla_\theta J = \frac{1}{1-\gamma} \mathbb{E}_{s \sim d^\pi, a \sim \pi}\left[\nabla_\theta \log \pi_\theta(a \mid s)\, Q^\pi(s, a)\right]$. Since $\sum_a \pi \nabla \log \pi = \nabla \sum_a \pi = 0$, any function of $s$ alone can be subtracted from $Q^\pi$ without bias. With $V^\pi$ subtracted, the weight is $A^\pi$. This often lowers the variance of the sampled gradient, but it is not the variance-minimizing baseline in general.

**Estimators.** In practice $V^\pi$ is an estimate $\hat V$. Then $\delta_t$ has bias, and the Monte Carlo return minus $\hat V(S_t)$ has high variance. [Generalized advantage estimation](/generalized-advantage-estimation/) mixes the two: $\hat A_t = \sum_{l \ge 0} (\gamma\lambda)^l \delta_{t+l}$, with $\lambda = 0$ giving $\delta_t$ and $\lambda = 1$ giving the return minus $\hat V(S_t)$.

## Examples

Take the two-state example of the [MDP page](/markov-decision-process/) with $\gamma = 9/10$: in $s_1$, *stay* gives 1 and stays, *switch* gives 0 and moves to $s_2$ with probability 1/2; in $s_2$, *stay* gives 2 and stays with probability 3/4, *switch* gives 3 and moves to $s_1$.

- **The uniform policy.** $V^\pi = (715/71, 875/71)$ and the advantages are

  | | stay | switch |
  |---|---|---|
  | $s_1$ | $-1/142$ | $1/142$ |
  | $s_2$ | $37/142$ | $-37/142$ |

  Each row has mean 0 under the uniform policy. The positive entries pick (switch, stay).
- **Performance difference.** Take $\pi'$ = (switch, stay) and start in $s_1$. The discounted occupancy of $\pi'$ from $s_1$ is $(13/31, 18/31)$. The lemma gives $10 \cdot \left(\frac{13}{31} \cdot \frac{1}{142} + \frac{18}{31} \cdot \frac{37}{142}\right) = 3395/2201$, and $V^{\pi'}(s_1) - V^\pi(s_1) = 360/31 - 715/71 = 3395/2201$.
- **The optimal advantage.** For (switch, stay), $A^*(s_1, \cdot) = (-5/31, 0)$ and $A^*(s_2, \cdot) = (0, -23/31)$. Each row has max 0 at the optimal action.
- **Small time steps.** Baird's motivation for advantage updating: if a control step lasts $\Delta t$, then $Q(s, a)$ and $Q(s, b)$ differ by $O(\Delta t)$, while $V$ is $O(1)$. A function approximator of $Q$ must then resolve tiny differences on top of a large value. Learning $A$ scaled by $1/\Delta t$ keeps the action differences at a usable size.

## Where it is used

- **Policy iteration.** The improvement step picks a greedy action of $A^\pi$, the same as a greedy action of $Q^\pi$ ([policy iteration](/policy-iteration/)).
- **Actor-critic methods.** [Actor-critic](/actor-critic/), [A2C](/a2c/), [A3C](/a3c/) and [PPO](/ppo/) weight $\nabla \log \pi$ by an advantage estimate, often from [GAE](/generalized-advantage-estimation/).
- **Trust region methods.** [TRPO](/trpo/) and conservative policy iteration build on the performance difference lemma.
- **Dueling networks.** A [dueling network](/dueling-network/) writes $Q(s, a) = V(s) + A(s, a)$ with two heads, and subtracts the mean (or the max) of $A$ over actions, because $V$ and $A$ are not identifiable from $Q$ alone.
- **Analysis.** Regret and suboptimality bounds often write the gap of a policy as a sum of $-A^*(s, a)$ along its occupancy, by the lemma with $\pi = \pi^*$.

## References
