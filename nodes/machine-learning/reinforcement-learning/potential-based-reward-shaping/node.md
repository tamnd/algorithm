---
tag: C2XHTJ
kind: technique
slug: potential-based-reward-shaping
name: Potential-based reward shaping
aliases:
- reward shaping
- PBRS
area: machine-learning/reinforcement-learning
level: advanced
summary: "Add F(s, s') = gamma Phi(s') - Phi(s) to every reward. The optimal Q-values shift by exactly -Phi(s), so the optimal policies stay the same; no other shaping of this kind is safe."
prereqs: [reward-function, action-value-function]
see_also: [q-learning, value-iteration, markov-decision-process, inverse-reinforcement-learning, markov-game, options-framework, advantage-function]
sources:
  - paper: "Andrew Y. Ng, Daishi Harada and Stuart Russell, Policy invariance under reward transformations, theory and application to reward shaping, Proceedings of the Sixteenth International Conference on Machine Learning (ICML), 1999, pages 278 to 287"
    locator: Theorem 1 (sufficiency and necessity of potential-based shaping, and Q*_M'(s, a) = Q*_M(s, a) - Phi(s)), Corollary 2 (Phi = V*), and the gridworld and mountain car experiments
  - paper: "Eric Wiewiora, Potential-based shaping and Q-value initialization are equivalent, Journal of Artificial Intelligence Research 19, 2003, pages 205 to 208"
    locator: the equivalence between Q-learning with potential-based shaping and Q-learning with the potential as initial values
  - paper: "Jette Randløv and Preben Alstrøm, Learning to drive a bicycle using reinforcement learning and shaping, Proceedings of the Fifteenth International Conference on Machine Learning (ICML), 1998, pages 463 to 471"
    locator: the shaping reward for progress toward the goal, and the agent that learned to ride in circles
  - paper: "Eric Wiewiora, Garrison Cottrell and Charles Elkan, Principled methods for advising reinforcement learning agents, Proceedings of the Twentieth International Conference on Machine Learning (ICML), 2003"
    locator: potentials over states and actions (look-ahead and look-back advice)
  - paper: "Sam Devlin and Daniel Kudenko, Theoretical considerations of potential-based reward shaping for multi-agent systems, Proceedings of the 10th International Conference on Autonomous Agents and Multiagent Systems (AAMAS), 2011"
    locator: the result that potential-based shaping keeps the Nash equilibria of a stochastic game
---

Potential-based reward shaping adds a bonus to every reward to guide a learning agent, in a form that cannot change which policies are optimal. Pick any function $\Phi$ on the states, the *potential*, and replace each reward $r$ of a transition from $s$ to $s'$ by

$$r + F(s, s'), \qquad F(s, s') = \gamma \Phi(s') - \Phi(s),$$

with $\Phi = 0$ on terminal states. Ng, Harada and Russell (1999) proved that the optimal action values of the new MDP $M'$ are $Q^*_{M'}(s, a) = Q^*_M(s, a) - \Phi(s)$, so every optimal policy of $M'$ is optimal in $M$ and the other way round. They also proved the converse: if $F$ is not of this form, some MDP exists in which the shaping changes the optimal policy.

## In plain words

Rewards that come only at the end of a long task make learning slow: the agent wanders a long time before it finds any reward. A designer can add small hints, for example a bonus for getting closer to the goal. Badly chosen hints are dangerous. An agent that gets a bonus for moving closer, and no penalty for moving away, can learn to go back and forth to collect the bonus for ever.

The safe form gives each state a score, and pays the change in score at each step. Whatever the agent gains by going up it loses again by coming down, so no loop pays. The hints change how fast the agent learns, not what the best behavior is.

## When it applies

- An MDP $(S, A, P, R, \gamma)$ with $\gamma < 1$, or $\gamma = 1$ with episodes that end with probability 1 and $\Phi = 0$ at the end.
- A learner that would find an optimal policy of the reward it gets: [Q-learning](/q-learning/), [value iteration](/value-iteration/), policy gradient methods and so on. The guarantee is about optimal policies, so it says nothing about a learner that stops early.
- Prior knowledge of which states are good, in the form of a guess $\Phi(s)$, for example the negative distance to a goal, a heuristic value, or the value of a simpler related task.
- The shaping may depend on the transition only through $s$ and $s'$ (and on $a$ in the variants below), not on the history.

## The template

The hole LEARN is any reinforcement learning algorithm. The template wraps the environment.

```pseudo id=main
SHAPE(Φ, γ, LEARN)
L1  choose Φ : S → ℝ and treat Φ as 0 on every terminal state
L2  for each transition (s, a, r, s′, done) that LEARN receives do
L3      F ← γ Φ(s′) − Φ(s)                  ▷ Φ(s′) = 0 if done
L4      r′ ← r + F
L5      pass (s, a, r′, s′, done) to LEARN in place of the original
L6  if values of M are needed, Q(s, a) ← Q′(s, a) + Φ(s)
```

**Why it is safe.** Along any trajectory $s_0, s_1, \ldots$ the shaping terms telescope:

$$\sum_{t=0}^{T-1} \gamma^t F(s_t, s_{t+1}) = \gamma^T \Phi(s_T) - \Phi(s_0),$$

which tends to $-\Phi(s_0)$ as $T \to \infty$ (bounded $\Phi$, $\gamma < 1$), or is exactly $-\Phi(s_0)$ when the episode ends in a terminal state. So the shaped return of every policy from $s_0$ is its old return minus the same constant $\Phi(s_0)$. If the first action $a$ is fixed, the same argument gives $Q^\pi_{M'}(s, a) = Q^\pi_M(s, a) - \Phi(s)$ for every policy $\pi$, and so for the optimal one. Subtracting a number that depends only on $s$ does not change the order of the actions at $s$.

**Example (a safe potential).** A corridor has states 0 to 3, actions left (at state 0 it stays) and right, and moving right from state 3 ends the episode with reward 1; all other rewards are 0 and $\gamma = 0.9$. With $\Phi(s) = s/2$, policy iteration with exact fractions gives

| state | $Q^*_M$ left | $Q^*_M$ right | $Q^*_{M'}$ left | $Q^*_{M'}$ right |
|---|---|---|---|---|
| 0 | 0.6561 | 0.729 | 0.6561 | 0.729 |
| 1 | 0.6561 | 0.81 | 0.1561 | 0.31 |
| 2 | 0.729 | 0.9 | $-0.271$ | $-0.1$ |
| 3 | 0.81 | 1 | $-0.69$ | $-0.5$ |

Each row of $M'$ is the row of $M$ minus $\Phi(s)$, and "right" is optimal in both.

**Example (an unsafe bonus).** Give a bonus $c = \tfrac12$ for every move to the right instead, and nothing for a move to the left. At state 3, finishing gives $1 + c = 1.5$. Stepping back to 2 and then right to 3 again, for ever, gives $\gamma c + \gamma^3 c + \cdots = \gamma c / (1 - \gamma^2) = 45/19 \approx 2.37$. The optimal policy of the shaped problem never finishes, and its true return is 0. The bonus is not potential-based: a loop $3 \to 2 \to 3$ earns a positive total. This is the failure that Randløv and Alstrøm (1998) saw when their bicycle learned to ride in circles near the start.

## Classic examples

- **Distance to the goal in a gridworld.** Ng, Harada and Russell used $\Phi(s) = -(\text{steps to the goal})$ scaled by the step cost. [Q-learning](/q-learning/) with this shaping learned far faster on their gridworld and on mountain car, with the same optimal policy.
- **The optimal potential.** With $\Phi = V^*_M$, the shaped optimal values satisfy $V^*_{M'} = 0$ and $Q^*_{M'}(s, a) = Q^*_M(s, a) - V^*_M(s)$, which is the optimal [advantage function](/advantage-function/). A greedy one-step learner on $M'$ is then optimal. This shows what a good potential looks like: an estimate of $V^*$, for example from [value iteration](/value-iteration/) on a simpler model.
- **Equivalence to initial values.** Wiewiora (2003) proved that tabular Q-learning with potential-based shaping and initial values $Q_0$ makes exactly the same choices as Q-learning without shaping from initial values $Q_0 + \Phi$. The implementation checks this with exact fractions over 300 transitions. So shaping in tabular Q-learning is a way to set the starting values.
- **Reward ambiguity in [inverse reinforcement learning](/inverse-reinforcement-learning/).** Two rewards that differ by a potential-based term have the same optimal policies, so no IRL method can tell them apart from optimal behavior.
- **Many agents.** In a [Markov game](/markov-game/), adding potential-based shaping to each agent's reward keeps the set of Nash equilibria (Devlin and Kudenko, 2011).

## Variations

- **Potentials on state and action.** $F(s, a, s', a') = \gamma \Phi(s', a') - \Phi(s, a)$ (look-ahead advice, Wiewiora, Cottrell and Elkan, 2003). The optimal policy is kept if the agent adds $\Phi(s, a)$ back when it chooses actions.
- **Dynamic potentials.** $\Phi$ may change over time, $F = \gamma \Phi(s', t') - \Phi(s, t)$, and the optimal policies are still kept (Devlin and Kudenko, 2012).
- **Learned potentials.** $\Phi$ can be a value estimate from an earlier task, an abstraction, a demonstration, or a model learned on line.
- **Undiscounted episodes.** With $\gamma = 1$, the terms telescope to $\Phi(s_T) - \Phi(s_0)$, so $\Phi$ must be 0 on all terminal states, or equal on all of them.

## Pitfalls

- **Bonuses for progress only.** A bonus for moving toward a goal with no matching penalty for moving away is not potential-based, and an agent can farm it, as in the corridor above.
- **Nonzero potential at the end.** If $\Phi$ is not 0 on terminal states, ending in different terminal states gives different totals, and the optimal policy can change.
- **A time limit that is not a terminal state.** If an episode is cut by a time limit, the next state is not terminal; use $\gamma \Phi(s')$, not 0, in line L3.
- **Expecting faster learning always.** The optimal policy is safe, but the learning speed is not: a poor $\Phi$ (one that is high in bad states) can make learning slower, as poor initial values do.
- **Function approximation.** The theorem is about the true optimal values. With function approximation, shaping changes the regression targets, and the learned policy can change.

## Exercises

1. Prove the telescoping identity above, and use it to prove $Q^\pi_{M'}(s, a) = Q^\pi_M(s, a) - \Phi(s)$ for every policy $\pi$.
2. Show that $F(s, a, s') = c$ for a constant $c \neq 0$ is potential-based (take $\Phi \equiv -c/(1 - \gamma)$), and so is safe. Then find what goes wrong if the episodes can end, with $\Phi$ nonzero at the end.
3. Let $\Phi = V^*_M$ in a deterministic MDP. Show that $V^*_{M'} \equiv 0$ and that the action with the largest immediate shaped reward $r'(s, a)$ is optimal in $M$.

## References
