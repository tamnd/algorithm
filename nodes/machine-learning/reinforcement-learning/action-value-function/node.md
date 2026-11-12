---
tag: VRH12A
kind: definition
slug: action-value-function
name: Action-value function
aliases:
- Q-function
- state-action value
area: machine-learning/reinforcement-learning
level: intro
summary: "Q^pi(s, a): the expected discounted return when the agent takes action a in state s and then follows the policy pi. Q* is its optimal form."
prereqs: [state-value-function]
see_also: [advantage-function, bellman-expectation-equation, bellman-optimality-equation, q-learning, sarsa, policy-iteration, dqn, value-iteration]
sources:
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: "Section 3.5 (the action value function q_pi), Section 3.6 (q_* and the greedy policy)"
  - book: isbn:9780471619772
    title: Martin L. Puterman, Markov Decision Processes, Discrete Stochastic Dynamic Programming, Wiley, 1994
    locator: "Section 6.1, Theorem 6.2.10"
  - paper: "Christopher J. C. H. Watkins, Learning from Delayed Rewards, PhD thesis, University of Cambridge, 1989"
    title: Learning from Delayed Rewards
    locator: "Chapter 5 (action values and Q-learning)"
---

The action value function $Q^\pi$ of a [policy](/policy/) $\pi$ in a [Markov decision process](/markov-decision-process/) gives, for each state $s$ and action $a$, the expected [discounted return](/discounted-return/) of an agent that takes $a$ in $s$ and then follows $\pi$. The [state value function](/state-value-function/) averages $Q^\pi(s, \cdot)$ over the actions of $\pi$. The optimal action value function $Q^*$ lets an agent act optimally with no model: in each state it takes an action that maximizes $Q^*$.

## Definition

Let $(S, A, P, R, \gamma)$ be a finite MDP with $0 \le \gamma < 1$, and let $\pi$ be a stationary policy. The action value function of $\pi$ is the map $Q^\pi : S \times A \to \mathbb{R}$,

$$Q^\pi(s, a) = \mathbb{E}^\pi\left[G_t \mid S_t = s, A_t = a\right] = \mathbb{E}^\pi\left[\sum_{k=0}^{\infty} \gamma^k R_{t+k+1} \,\middle|\, S_t = s, A_t = a\right].$$

The first action is $a$, also when $\pi(a \mid s) = 0$. From the next step on, the actions come from $\pi$. The optimal action value function is

$$Q^*(s, a) = \sup_\pi Q^\pi(s, a).$$

**Relations to $V$.** Condition on the first transition. By the Markov property the return after it has the expected value $V^\pi(S_{t+1})$, so

$$Q^\pi(s, a) = R(s, a) + \gamma \sum_{s'} P(s' \mid s, a)\, V^\pi(s'), \qquad V^\pi(s) = \sum_a \pi(a \mid s)\, Q^\pi(s, a).$$

Put the second identity into the first. Then $Q^\pi$ solves a linear system of its own on the $|S||A|$ pairs:

$$Q^\pi(s, a) = R(s, a) + \gamma \sum_{s'} P(s' \mid s, a) \sum_{a'} \pi(a' \mid s')\, Q^\pi(s', a').$$

The matrix of this system is $P \Pi$, where $P$ maps pairs to states and $\Pi$ maps states to pairs. It is a stochastic matrix, so the system has one solution, as on the [Bellman expectation equation](/bellman-expectation-equation/) page.

For the optimal values, $Q^*(s, a) = R(s, a) + \gamma \sum_{s'} P(s' \mid s, a) V^*(s')$ and $V^*(s) = \max_a Q^*(s, a)$. A policy $d$ that is greedy for $Q^*$, $d(s) \in \arg\max_a Q^*(s, a)$, is optimal ([Bellman optimality equation](/bellman-optimality-equation/)).

**Cost.** Given $V^\pi$, all of $Q^\pi$ costs $O(|S|^2|A|)$ operations. A direct solve of the system on pairs costs $O(|S|^3|A|^3)$, so in practice one solves for $V^\pi$ first.

## Examples and non-examples

Take the two-state example of the [MDP page](/markov-decision-process/) with $\gamma = 9/10$: in $s_1$, *stay* gives 1 and stays, *switch* gives 0 and moves to $s_2$ with probability 1/2; in $s_2$, *stay* gives 2 and stays with probability 3/4, *switch* gives 3 and moves to $s_1$.

- **The uniform policy.** $V^\pi = (715/71, 875/71)$. Then $Q^\pi(s_1, \text{switch}) = 0 + \frac{9}{10}\left(\frac12 \cdot \frac{715}{71} + \frac12 \cdot \frac{875}{71}\right) = 1431/142$. The full table is

  | | stay | switch |
  |---|---|---|
  | $s_1$ | 1429/142 | 1431/142 |
  | $s_2$ | 1787/142 | 1713/142 |

  The mean of each row is $V^\pi$: $(1429 + 1431)/284 = 715/71$. The system on the four pairs gives the same table.
- **The optimal values.** $V^* = (360/31, 440/31)$ gives

  | | stay | switch |
  |---|---|---|
  | $s_1$ | 355/31 | 360/31 |
  | $s_2$ | 440/31 | 417/31 |

  The row maxima are $V^*$, and the greedy policy (switch, stay) is the optimal policy found by enumeration of the four deterministic policies.
- **One greedy step.** The greedy policy for $Q^\pi$ of the uniform policy is also (switch, stay). This is one step of [policy iteration](/policy-iteration/), and here it reaches the optimum at once.
- **Non-example: $V$ alone for control.** To act greedily with $V^*$, an agent needs $P$ and $R$ to look one step ahead. With $Q^*$ it needs only a max over a row. This is why model-free control methods such as [Q-learning](/q-learning/) and [SARSA](/sarsa/) estimate $Q$ and not $V$.
- **Non-example: the immediate reward.** $R(s, a)$ is the expected next reward only. $Q^\pi(s, a)$ adds the discounted future. In the example $R(s_1, \text{switch}) = 0 < R(s_1, \text{stay}) = 1$, but $Q^*(s_1, \text{switch}) > Q^*(s_1, \text{stay})$.

## Related definitions

- [State value function](/state-value-function/) $V^\pi$, the average of $Q^\pi$ over the actions of $\pi$.
- [Advantage function](/advantage-function/) $A^\pi = Q^\pi - V^\pi$.
- [Bellman expectation equation](/bellman-expectation-equation/) and [Bellman optimality equation](/bellman-optimality-equation/) in their $Q$ forms.
- [Q-learning](/q-learning/), [SARSA](/sarsa/) and [deep Q-network](/dqn/): methods that estimate $Q^*$ or $Q^\pi$ from samples.
- [Policy iteration](/policy-iteration/) and [value iteration](/value-iteration/): planning methods that use $Q$ in the improvement step.

## References
