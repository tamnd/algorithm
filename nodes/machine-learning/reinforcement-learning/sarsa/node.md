---
tag: 568W6N
kind: algorithm
slug: sarsa
name: SARSA
aliases:
- SARSA(0)
- modified connectionist Q-learning
area: machine-learning/reinforcement-learning
level: intro
summary: "On-policy TD control: after each step, move Q(S,A) toward R + gamma Q(S',A'), where A' is the next action the epsilon-greedy policy really takes."
solves: [rl-control]
model: real-ram
complexity:
  vars: {T: the total number of steps, A: the largest number of actions in a state, S: the number of states}
  time: {worst: "O(A T)"}
  space: {extra: "O(S A)"}
properties: {deterministic: false, online: true, exact: false, recursive: false}
history:
  year: 1994
  people: [Gavin A. Rummery, Mahesan Niranjan]
  note: Rummery and Niranjan introduced the update as modified connectionist Q-learning; Sutton (1996) gave it the name SARSA.
prereqs: [temporal-difference-learning, action-value-function, epsilon-greedy]
see_also: [q-learning, expected-sarsa, monte-carlo-control, td-lambda, eligibility-traces, robbins-monro-conditions, exploration-exploitation-tradeoff, actor-critic]
sources:
  - paper: "Gavin A. Rummery and Mahesan Niranjan, On-line Q-learning using connectionist systems, Technical Report CUED/F-INFENG/TR 166, Cambridge University Engineering Department, 1994"
    locator: the update called modified connectionist Q-learning
  - paper: "Richard S. Sutton, Generalization in reinforcement learning, successful examples using sparse coarse coding, Advances in Neural Information Processing Systems 8 (NIPS 1995), MIT Press, 1996"
    locator: the name Sarsa for the on-policy TD control update
  - paper: "Satinder Singh, Tommi Jaakkola, Michael L. Littman and Csaba Szepesvari, Convergence results for single-step on-policy reinforcement-learning algorithms, Machine Learning 38(3), 2000, pages 287 to 308"
    locator: the convergence of SARSA(0) to the optimal action values under GLIE exploration and Robbins-Monro step sizes
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 6.4 (Sarsa) and Example 6.6 in Section 6.5 (cliff walking, Sarsa against Q-learning)
---

SARSA is the on-policy [temporal-difference](/temporal-difference-learning/) control algorithm. It learns the [action values](/action-value-function/) $Q(s, a)$ of the policy it follows, usually [ε-greedy](/epsilon-greedy/) in $Q$, and so improves the policy as it learns. After each step it uses the five values $S_t, A_t, R_{t+1}, S_{t+1}, A_{t+1}$, which give it its name, and moves $Q(S_t, A_t)$ toward $R_{t+1} + \gamma Q(S_{t+1}, A_{t+1})$. Rummery and Niranjan (1994) introduced it as "modified connectionist Q-learning", and Sutton (1996) named it. With exploration that becomes greedy in the limit (GLIE) and [Robbins-Monro](/robbins-monro-conditions/) step sizes, tabular SARSA converges to the optimal action values with probability 1 (Singh, Jaakkola, Littman and Szepesvari 2000). Because it learns the value of the policy that explores, it prefers safe paths when exploration is costly, as in the cliff walking task.

## In plain words

You learn a score for each move in each place, while you play. After every move, you see the reward and the next place, and you also pick your next move. Then you update the score of the move you just made toward the reward plus the score of the next move you picked.

You pick moves by a simple rule: usually the move with the best score, and now and then a random move, to keep learning. The scores learn what really happens when you play this way, random moves included. So if a random move near a cliff could make you fall, the moves near the cliff get bad scores, and you learn to keep away from the edge.

## The problem

The input is an MDP that the algorithm can only sample, with a discount $0 \le \gamma \le 1$. Episodes start in a start state and may end in a terminal state, whose value is 0. The goal is a good policy and its action values; with exploration that fades, the goal is an optimal policy and $q_*$, the problem of [RL control](/rl-control/). SARSA learns online, one step at a time, with no model.

## The algorithm

```pseudo id=main
SARSA(episodes, α, γ, ε)
L1  Q(s, a) ← 0 for all pairs                       ▷ Q(terminal, ·) = 0
L2  for each episode do
L3      S ← the start state;  A ← ε-greedy action for Q in S
L4      repeat until S is terminal
L5          take A, observe R and S′
L6          if S′ is terminal then y ← R else A′ ← ε-greedy action for Q in S′;  y ← R + γ Q(S′, A′)
L7          Q(S, A) ← Q(S, A) + α (y − Q(S, A))
L8          S ← S′;  A ← A′
L9  return Q
```

Line L6 chooses the next action *before* the update, from the same ε-greedy policy that will then take it in line L5 of the next step. This is what makes SARSA on-policy: the target uses the action the agent really takes. Line L7 is the [TD error](/td-error/) update for action values. The step $\alpha$ may depend on the number of updates of the pair, and $\varepsilon$ may decrease over the episodes. A random tie-break in the greedy choice is common; the implementation takes the first best action, so that runs repeat exactly.

## Example

**The first updates.** Take cliff walking (Sutton and Barto, Example 6.6): a 4 by 12 grid, the start in the bottom left corner $(3, 0)$, the goal in the bottom right corner $(3, 11)$, and the cells between them in the bottom row are a cliff. Each step gives $-1$, a step into the cliff gives $-100$ and sends the agent back to the start, and moves into a wall leave the agent in place. Let $Q = 0$, $\alpha = 1/2$, $\gamma = 1$, the actions in the order up, right, down, left, with ties broken toward the first, and suppose that no random action is drawn.

| step | $S$ | $A$ | $R$ | $S'$ | $A'$ | new $Q(S, A)$ |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | $(3, 0)$ | up | $-1$ | $(2, 0)$ | up | $-1/2$ |
| 2 | $(2, 0)$ | up | $-1$ | $(1, 0)$ | up | $-1/2$ |
| 3 | $(1, 0)$ | up | $-1$ | $(0, 0)$ | up | $-1/2$ |
| 4 | $(0, 0)$ | up | $-1$ | $(0, 0)$ | up | $-1/2$ |
| 5 | $(0, 0)$ | up | $-1$ | $(0, 0)$ | right | $-1/2 + \tfrac12(-1 + 0 + \tfrac12) = -3/4$ |

In step 4 the agent hits the top wall, and the value of "up" in $(0, 0)$ becomes negative. So in step 5 the greedy next action is "right", whose value is still 0, and the target uses it. Initial values of 0 are optimistic here, since every true value is negative, so the greedy policy keeps trying actions it has not yet tried.

**Safe path against optimal path.** With $\varepsilon = 0.1$ and $\alpha = 1/2$ fixed, after 500 episodes, seed 0 of the tests:

| | greedy path | its length | mean return of the last 100 episodes |
| --- | --- | --- | --- |
| SARSA | up to the top row, across, down | 17 steps | about $-25$ |
| [Q-learning](/q-learning/) | along the row next to the cliff | 13 steps (optimal) | about $-52$ |

Q-learning learns the values of the greedy policy, so it finds the shortest path next to the cliff, but its ε-greedy behavior falls into the cliff now and then. SARSA learns the values of the ε-greedy policy it runs, for which cells next to the cliff are dangerous, so it learns the longer, safe path and earns more while it explores. Over seeds 0 to 9, Q-learning always found the 13-step path, and the mean return of SARSA over the last 100 episodes was always higher. With constant $\varepsilon$ and $\alpha$, the greedy path of SARSA did not always end: for 2 of the 10 seeds it looped. If $\varepsilon$ decreases to 0, both methods tend to the optimal path.

## Correctness

**For a fixed policy.** If $\varepsilon$ is fixed and the policy $\pi$ that chooses the actions were fixed, the expected target of line L6, given $S_t = s$ and $A_t = a$, would be $(T^\pi Q)(s, a) = r(s, a) + \gamma\sum_{s'} p(s' \mid s, a) \sum_{a'} \pi(a' \mid s')\, Q(s', a')$, the [Bellman expectation operator](/bellman-expectation-equation/) for action values. It is a $\gamma$-contraction in the max norm with the unique fixed point $q_\pi$, so line L7 is a [stochastic approximation](/stochastic-approximation/) of $q_\pi$, exactly as [TD(0)](/temporal-difference-learning/) is for $v_\pi$.

**Convergence to the optimum.** The policy of SARSA changes with $Q$, so the target operator also changes. Singh, Jaakkola, Littman and Szepesvari (2000) proved: in a finite MDP with bounded rewards and $\gamma < 1$, if the step sizes of each pair satisfy the Robbins-Monro conditions and the policy is **GLIE**, then $Q$ converges to $q_*$ with probability 1. GLIE (greedy in the limit with infinite exploration) means that every pair is tried infinitely often and that the policy becomes greedy in $Q$ in the limit. For example, ε-greedy with $\varepsilon_t(s) = c / n_t(s)$, $0 < c < 1$, where $n_t(s)$ counts the visits to $s$, is GLIE. The proof writes the target as the [Q-learning](/q-learning/) target plus the term $\gamma(Q(S', A') - \max_{a'} Q(S', a'))$. Under GLIE this term tends to 0, and a stochastic approximation lemma with a vanishing extra term then gives the same limit as [tabular Q-learning](/tabular-q-learning-convergence/). The proofs section proves the contraction and the decomposition and cites the lemma. With fixed $\varepsilon > 0$, SARSA instead tends to the values of the best ε-soft policies, not to $q_*$; this is why it finds the safe path in the example.

## Complexity

Each step costs one call to the environment and $O(A)$ time for the ε-greedy choice of line L6, which scans the actions of $S'$. So $T$ steps cost $O(AT)$ time. The table takes $O(SA)$ memory; nothing else grows with time. The number of steps needed for a given accuracy depends on the MDP and on the exploration; finite-sample bounds exist for related methods but not in a simple general form for SARSA.

## Properties

- **On-policy.** SARSA evaluates and improves the policy it runs, exploration included. Its values account for the cost of exploring.
- **Online and incremental.** It updates after every step and needs no episode to end, so it works for continuing tasks.
- **Model-free.** It uses only samples of transitions.
- **Bootstrapping.** The target uses the estimate $Q(S', A')$, so errors spread between pairs, and the method is biased while it learns.
- **Variance from the next action.** The target depends on the random choice of $A'$. [Expected SARSA](/expected-sarsa/) removes this source of variance.

## Variants and improvements

- **Expected SARSA.** Replace $Q(S', A')$ by $\sum_{a'} \pi(a' \mid S') Q(S', a')$: [Expected SARSA](/expected-sarsa/), with lower variance.
- **Q-learning.** Replace it by $\max_{a'} Q(S', a')$: the off-policy [Q-learning](/q-learning/).
- **n-step SARSA.** Use the [n-step](/n-step-td/) return $R_{t+1} + \cdots + \gamma^{n-1} R_{t+n} + \gamma^n Q(S_{t+n}, A_{t+n})$ (Sutton and Barto, Section 7.2).
- **SARSA(λ).** Use [eligibility traces](/eligibility-traces/) on the pairs, so that each TD error updates all recent pairs (Sutton and Barto, Section 12.7). Rummery and Niranjan used traces from the start.
- **Function approximation.** Semi-gradient SARSA with linear features, as in Sutton (1996) and Sutton and Barto (Chapter 10), or with a neural network ([value function approximation](/value-function-approximation/)).
- **Actor-critic.** A critic learned with SARSA-like targets drives a separate policy ([actor-critic](/actor-critic/)).

## When to use it

Use SARSA when the agent must learn while it acts and mistakes during learning have a real cost, so that the values of the exploring policy are the right ones to optimize: robots, online systems, or any task like cliff walking. When only the final greedy policy matters and the data may come from any policy, such as a replay buffer, use [Q-learning](/q-learning/). When the variance of the target is a problem, use [Expected SARSA](/expected-sarsa/).

## Pitfalls

- **Choosing A′ after the update, from the new Q.** Line L6 must choose $A'$ and use it both in the target and as the next action. Choosing the next action again after line L7 gives a target action that is not the one taken, and the algorithm is no longer SARSA.
- **Bootstrapping from the terminal state.** At a terminal $S'$, the target is $R$ alone. Using a stored $Q(S', \cdot)$ there adds a value that should be 0.
- **Fixed ε and a claim of optimality.** With constant $\varepsilon$, SARSA converges at best to the values of an ε-soft policy. To reach $q_*$, $\varepsilon$ must fall to 0 while every pair is still tried infinitely often.
- **A step size that is too large.** In stochastic tasks, a constant $\alpha$ near 1 keeps $Q$ noisy. With constant $\alpha$, $Q$ only fluctuates around its target.
- **Initial values.** Optimistic initial values cause early exploration; pessimistic ones can make the greedy policy stick with the first action that gave a reward.

## Implementations

## History

Rummery and Niranjan (1994) proposed the update, with eligibility traces and neural networks, under the name modified connectionist Q-learning. Sutton (1996) introduced the name Sarsa and used it with tile coding on control tasks. Singh, Jaakkola, Littman and Szepesvari (2000) proved convergence of tabular SARSA(0) under GLIE exploration. Sutton and Barto (2018, Example 6.6) use cliff walking to contrast SARSA with Q-learning.

## References
