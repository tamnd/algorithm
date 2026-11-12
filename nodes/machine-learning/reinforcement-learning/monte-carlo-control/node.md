---
tag: VZ2NZH
kind: algorithm
slug: monte-carlo-control
name: Monte Carlo control
aliases:
- Monte Carlo with exploring starts
- Monte Carlo ES
- on-policy first-visit Monte Carlo control
- off-policy Monte Carlo control
area: machine-learning/reinforcement-learning
level: intro
summary: "Find a good policy from complete episodes: average the returns after each state action pair to estimate Q, and make the policy greedy (or epsilon-greedy) in Q."
solves: [rl-control]
model: real-ram
complexity:
  vars: {T: the total number of steps in all episodes, A: the largest number of actions in a state, S: the number of states, L: the length of the longest episode}
  time: {worst: "O(A T)"}
  space: {extra: "O(S A + L)"}
properties: {deterministic: false, online: false, exact: false, recursive: false}
history:
  year: 1998
  people: [Richard S. Sutton, Andrew G. Barto]
  note: The first edition of their book presented Monte Carlo control with exploring starts and the on-policy and off-policy forms as generalized policy iteration with sample returns.
prereqs: [monte-carlo-policy-evaluation, action-value-function, policy-iteration, epsilon-greedy]
see_also: [sarsa, q-learning, importance-sampling-off-policy, policy-improvement-theorem, exploration-exploitation-tradeoff, tabular-q-learning-convergence, monte-carlo-algorithm, monte-carlo-tree-search]
sources:
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 5.3 (Monte Carlo ES and the open question of its convergence), Section 5.4 (on-policy control with epsilon-soft policies) and Section 5.7 (off-policy Monte Carlo control with weighted importance sampling)
  - paper: "John N. Tsitsiklis, On the convergence of optimistic policy iteration, Journal of Machine Learning Research 3, 2002, pages 59 to 72"
    locator: convergence of a form of optimistic policy iteration with Monte Carlo estimates of Q, in which all pairs are updated at the same rate
  - paper: "Che Wang, Shuhan Yuan, Kai Shao and Keith Ross, On the convergence of the Monte Carlo exploring starts algorithm for reinforcement learning, International Conference on Learning Representations (ICLR), 2022"
    locator: convergence of Monte Carlo ES for optimal policy feed-forward MDPs, in which no optimal policy visits a state twice in an episode
  - paper: "Satinder P. Singh and Richard S. Sutton, Reinforcement learning with replacing eligibility traces, Machine Learning 22, 1996, pages 123 to 158"
    locator: the first-visit and every-visit Monte Carlo estimators
---

Monte Carlo control finds a good policy for an unknown MDP from complete episodes, with no model. It estimates the [action values](/action-value-function/) $Q(s, a)$ by averaging the returns that follow the visits to each pair, as in [Monte Carlo policy evaluation](/monte-carlo-policy-evaluation/), and after each episode it makes the policy greedy in $Q$ at the states of the episode. This is [policy iteration](/policy-iteration/) with sample returns in place of exact evaluation, and with improvement after every episode. Every pair must keep being tried, and there are three standard ways to get this: exploring starts (Monte Carlo ES), $\varepsilon$-soft policies (on-policy), and a separate soft behavior policy with [importance sampling](/importance-sampling-off-policy/) (off-policy) (Sutton and Barto, Sections 5.3 to 5.7). Whether Monte Carlo ES always converges to an optimal policy is an open question in general (Sutton and Barto, Section 5.3).

## In plain words

You want to learn the best way to play a game, but you have no rule book. So you play whole games, and after each game you look back: for each move you made in each position, you note the total score that followed it. The average of these scores is your estimate of how good that move is in that position.

After each game you change your plan: in each position you saw, you now choose the move with the best average so far. Then you play again with the new plan.

There is one catch. If you always play your best known move, you never learn about the others. So you must sometimes try other moves: start some games with a random move, play a random move now and then, or learn from games that someone else plays at random.

## The problem

The input is an episodic MDP that the algorithm can only sample: from a pair $(s, a)$ it can draw a reward and a next state. The discount is $0 \le \gamma \le 1$. The goal is an optimal policy $\pi_*$ and its action values $q_*$, the problem of [RL control](/rl-control/). Monte Carlo methods need every episode to end. With $\gamma = 1$ we assume that every policy ends each episode with probability 1. An episode is $S_0, A_0, R_1, S_1, A_1, \ldots, R_T$, and the return after time $t$ is $G_t = R_{t+1} + \gamma G_{t+1}$ with $G_T = 0$.

## The algorithm

Monte Carlo with exploring starts, with first-visit sample averages:

```pseudo id=main
MC-ES(n, γ)
L1  Q(s, a) ← 0, N(s, a) ← 0 for all pairs; π(s) ← any action, for all s
L2  repeat n times
L3      choose a start pair (S_0, A_0) at random, each pair with probability > 0
L4      generate an episode S_0, A_0, R_1, ..., S_{T−1}, A_{T−1}, R_T from (S_0, A_0), then following π
L5      G ← 0
L6      for t ← T − 1 down to 0 do
L7          G ← γ G + R_{t+1}
L8          if (S_t, A_t) occurs at an earlier time of the episode then skip to the next t
L9          N(S_t, A_t) ← N(S_t, A_t) + 1;  Q(S_t, A_t) ← Q(S_t, A_t) + (G − Q(S_t, A_t)) / N(S_t, A_t)
L10         π(S_t) ← an action a with the largest Q(S_t, a)
L11 return π, Q
```

Line L3 is the exploring start: the first pair is random, so every pair keeps getting new returns even when $\pi$ never chooses it. Line L4 then follows the current deterministic policy. The backward loop of lines L6 and L7 computes each return in $O(1)$. Line L8 keeps only the first visit of each pair in the episode. Line L9 is the running mean of the returns, and line L10 is the greedy improvement, done at once for the state just updated.

When exploring starts are not possible, as in a real system that always starts in the same state, use one of these forms:

- **On-policy, ε-soft.** Drop line L3: start from the given start state, and in line L4 follow the [ε-greedy](/epsilon-greedy/) policy for $Q$. Line L10 then makes the policy ε-greedy in $Q$ (Sutton and Barto, Section 5.4).
- **Off-policy, weighted importance sampling.** Generate episodes with a soft behavior policy $b$, for example uniform. Go backward with a weight $W = 1$: add $W$ to a cumulative weight $C(S_t, A_t)$, move $Q(S_t, A_t)$ toward $G$ by $W / C(S_t, A_t)$, set $\pi(S_t)$ greedy, stop the episode at the first $A_t \ne \pi(S_t)$, and else multiply $W$ by $1 / b(A_t \mid S_t)$ (Sutton and Barto, Section 5.7). The weighting is explained on the [off-policy importance sampling](/importance-sampling-off-policy/) page.

## Example

A small MDP with $\gamma = 1$ and three states. In state a, action 0 gives reward 0 and moves to b or c with probability 1/2 each, and action 1 gives reward 1 and moves to c. In b, action 0 gives 0 or 4 with probability 1/2 each, and action 1 gives 1; both end the episode. In c, action 0 gives $-1$, and action 1 gives 0 or 1 with probability 1/2 each; both end. The optimal values are $q_*(\mathrm{b}, 0) = 2$, $q_*(\mathrm{b}, 1) = 1$, $q_*(\mathrm{c}, 0) = -1$, $q_*(\mathrm{c}, 1) = 1/2$, $q_*(\mathrm{a}, 0) = \tfrac12 \cdot 2 + \tfrac12 \cdot \tfrac12 = 5/4$ and $q_*(\mathrm{a}, 1) = 1 + 1/2 = 3/2$, so $\pi_*$ chooses 1 in a, 0 in b and 1 in c.

Start with $\pi = 0$ everywhere and $Q = 0$, and break ties toward action 0. Four episodes of MC ES:

| episode | start pair | episode | updates (backward) | $\pi$ after |
| --- | --- | --- | --- | --- |
| 1 | (a, 1) | a, 1, $+1$, c, 0, $-1$ | $Q(\mathrm{c},0) = -1$, $Q(\mathrm{a},1) = 0$ | a 0, c 1 |
| 2 | (b, 0) | b, 0, $+4$ | $Q(\mathrm{b},0) = 4$ | b 0 |
| 3 | (a, 0) | a, 0, $0$, c, 1, $+1$ | $Q(\mathrm{c},1) = 1$, $Q(\mathrm{a},0) = 1$ | a 0, c 1 |
| 4 | (a, 1) | a, 1, $+1$, c, 1, $0$ | $Q(\mathrm{c},1) = 1/2$, $Q(\mathrm{a},1) = 1/2$ | a 0 |

In episode 1 the policy took action 0 in c, got $-1$, and switched c to action 1 at once. In episode 4, $Q(\mathrm{a}, 1)$ is the mean of the returns 0 and 1, which is still below $Q(\mathrm{a}, 0) = 1$, so a still chooses 0. Its early return 0 came from the bad action in c, before the policy changed. Such old returns stay in the average. With 20,000 episodes, the policy is $\pi_*$ and all $Q$ values are within 0.1 of $q_*$ for the seeds 0, 1 and 2 of the tests. The on-policy form with $\varepsilon = 0.1$ and the off-policy form with a uniform behavior policy also find $\pi_*$ on this MDP.

## Correctness

**What the algorithm keeps.** After each episode, $Q(s, a)$ is the mean of all first-visit returns observed after $(s, a)$ so far, and $\pi(s)$ is greedy in $Q(s, \cdot)$ at every state that was updated. Both follow from lines L9 and L10, and the proofs section proves them.

**The only stable points are optimal.** If $Q = q_\pi$ and $\pi$ is greedy in $Q$, then $v_\pi(s) = \max_a q_\pi(s, a)$ for every state, which is the [Bellman optimality equation](/bellman-optimality-equation/); its solution is unique, so $\pi$ is optimal. In the same way, if $\pi$ is ε-greedy in $q_\pi$, then $\pi$ is best among all ε-soft policies (Sutton and Barto, Section 5.4). Each improvement step is justified by the [policy improvement theorem](/policy-improvement-theorem/), which the proofs section applies to the ε-greedy step.

**Convergence is open in general.** These facts do not show that MC ES reaches a stable point. The estimate $Q(s, a)$ averages returns from many different policies, so it is not $q_\pi$ for any one $\pi$. Sutton and Barto (Section 5.3) state that convergence of MC ES to the optimal policy has not been proved and call it one of the most basic open theoretical questions of reinforcement learning. Tsitsiklis (2002) proved convergence for a related form of optimistic policy iteration in which all pairs are updated at the same rate, which the random starts of MC ES do not ensure. Wang, Yuan, Shao and Ross (2022) proved convergence for MDPs in which no optimal policy can visit a state twice in an episode, a class that contains all MDPs in which no policy can. A 2026 preprint reports counterexamples in which first-visit MC ES with sample averages converges to a policy that is not optimal; it had not been through peer review when this page was written.

For the off-policy form, with a fixed target policy and a behavior policy that tries every pair, the weighted importance sampling estimates converge to the target's action values ([off-policy importance sampling](/importance-sampling-off-policy/)). The control loop changes the target after each episode, so this fact alone does not prove convergence either; the stable points are again optimal.

## Complexity

An episode of $T$ steps costs $O(T)$ to generate (with one call to the environment per step), $O(T)$ for the first-visit table, and $O(T A)$ for the updates, since line L10 compares the $A$ actions of the state. So $n$ episodes with $T$ steps in total cost $O(A T)$ time. The memory is $O(SA)$ for $Q$, $N$ and $\pi$, plus $O(L)$ for the episode in progress, with $L$ the length of the longest episode. The time to learn a good policy depends on the MDP and on how often the rare pairs are tried; no general bound is known for MC ES.

## Properties

- **No bootstrapping.** The targets are sample returns, not estimates, so the method does not need the Markov property for its estimates of $Q$ to be meaningful, and errors in one value do not spread to others.
- **Model-free.** It uses $Q$, not $V$, because choosing a greedy action from $V$ would need the transition probabilities.
- **Episodic only.** Updates wait until the end of the episode. In a task without episodes, or with a policy that never ends an episode, the method cannot update.
- **Randomized.** The start pairs, the exploration and the environment are random, so the result is a random policy.
- **High variance.** Each target is a full return, a sum of many random rewards. [SARSA](/sarsa/) and [Q-learning](/q-learning/) bootstrap and usually learn faster.

## Variants and improvements

- **Every-visit MC control.** Remove line L8. The estimates are biased within a finite sample but still consistent for a fixed policy.
- **Constant step size.** Replace $1/N$ by a constant $\alpha$, which forgets the returns of old policies. This often helps, because the policy keeps changing.
- **GLIE on-policy control.** Decrease $\varepsilon$ over the episodes, for example $\varepsilon_k = 1/k$, so the policy becomes greedy in the limit while every action is still tried infinitely often.
- **Off-policy with ordinary importance sampling.** Use weights $W$ without normalization: unbiased for a fixed target, but with much higher, possibly infinite, variance ([off-policy importance sampling](/importance-sampling-off-policy/)).
- **Monte Carlo tree search.** [MCTS](/monte-carlo-tree-search/) uses Monte Carlo returns with a model, to choose one action from the current state.

## When to use it

Use Monte Carlo control for short episodic tasks with no model, where full returns are cheap to get and the Markov property may not hold, such as card games like blackjack (Sutton and Barto, Example 5.3). Use exploring starts only in a simulator that can start from any pair. Use the on-policy ε-soft form when you must learn from the policy you run. For long episodes or continuing tasks, prefer [SARSA](/sarsa/) or [Q-learning](/q-learning/), which update at every step.

## Pitfalls

- **No exploration.** Without exploring starts, ε-soft policies or a soft behavior policy, a deterministic greedy policy never tries some pairs, and their estimates never change. The method can then stay on a bad policy forever.
- **Policies that never end the episode.** With $\gamma = 1$, a greedy policy can loop forever, for example in a maze where it walks into a wall. Line L4 then never returns. Cap the length of an episode or use a method that updates during the episode.
- **Ties in line L10.** Breaking ties always toward the first action is safe for MC ES, but a policy that breaks ties at random keeps changing among equal actions, which can hide whether it has settled.
- **Treating the result as $q_*$.** The on-policy form learns the values of the best ε-soft policy, not $q_*$, and the greedy policy for these values can differ from the optimal one when risky actions are close to danger.
- **Off-policy stops early.** The off-policy form learns only from the tails of episodes after the last non-greedy action. With a uniform behavior policy on long episodes, these tails are short, and the early states learn very slowly.

## Implementations

## History

Monte Carlo estimation of values is old; its use for control as a form of policy iteration with sample returns was set out in the first edition of the book of Sutton and Barto (1998), with exploring starts, ε-soft policies and the off-policy form. Singh and Sutton (1996) named the first-visit and every-visit estimators. Tsitsiklis (2002) proved convergence for a form of optimistic policy iteration, and the general question for MC ES remains open in Sutton and Barto (2018, Section 5.3), with a positive result for optimal policy feed-forward MDPs by Wang, Yuan, Shao and Ross (2022).

## References
