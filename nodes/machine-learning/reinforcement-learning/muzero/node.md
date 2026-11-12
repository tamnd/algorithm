---
tag: RGAS70
kind: algorithm
slug: muzero
name: MuZero
area: machine-learning/reinforcement-learning
level: research
summary: "Learn a model that predicts rewards, values and policies in a hidden state space, and choose actions by Monte Carlo tree search with the pUCT rule over that model."
solves: [rl-control]
model: real-ram
complexity:
  vars: {N: the number of simulations of one search, D: the largest depth of the search tree, A: the number of actions, M: the cost of one call of the dynamics and prediction functions}
  time: {worst: "O(N (D A + M))"}
  space: {extra: "O(N A)"}
properties: {deterministic: true, online: true, exact: false, recursive: false}
history:
  year: 2020
  people: [Julian Schrittwieser, Ioannis Antonoglou, Thomas Hubert, David Silver]
  note: The MuZero paper appeared on arXiv in 2019 and in Nature in 2020. It matched AlphaZero in Go, chess and shogi without being given the rules.
prereqs: [monte-carlo-tree-search, model-based-reinforcement-learning]
see_also: [uct, dyna-q, policy-iteration, prioritized-experience-replay, dqn, temporal-difference-learning, offline-reinforcement-learning, rl-control]
sources:
  - paper: doi:10.1038/s41586-020-03051-4
    title: "Julian Schrittwieser, Ioannis Antonoglou, Thomas Hubert, Karen Simonyan, Laurent Sifre, Simon Schmitt, Arthur Guez, Edward Lockhart, Demis Hassabis, Thore Graepel, Timothy Lillicrap and David Silver, Mastering Atari, Go, chess and shogi by planning with a learned model, Nature 588, 2020, pages 604 to 609"
    locator: the description of the model (representation, dynamics and prediction functions), the search, the training targets and the results
  - paper: arxiv:1911.08265
    title: "Julian Schrittwieser and others, Mastering Atari, Go, chess and shogi by planning with a learned model, arXiv preprint, 2019"
    locator: Appendix B (the search, the pUCT rule with c1 = 1.25 and c2 = 19652, and the min-max normalization of Q values) and the published pseudocode
---

MuZero is a reinforcement learning agent that plans with a model it learns. The model has three parts. A representation function $h$ turns the past observations into a hidden state. A dynamics function $g$ takes a hidden state and an action and predicts the reward and the next hidden state. A prediction function $f$ takes a hidden state and predicts a policy, the prior probabilities of the actions, and a value. The hidden state does not have to describe the real world. It only has to make these three predictions correct. To choose an action, MuZero runs Monte Carlo tree search over the model, using the pUCT rule to balance the prior, the value estimates and the visit counts. It acts by the visit counts at the root, and it trains $f$ to predict these counts and the observed returns. **The code on this page implements only the search: tree search with pUCT over a given model, stored as tables.** It does not learn the model.

## In plain words

To plan, an agent needs to imagine what happens after each action. Chess programs use the rules of the game for this. MuZero is not given the rules. It learns its own small imagined world. In that world it can predict three things: how much reward an action gives, how good a situation is, and which actions look worth trying.

Before each move, MuZero imagines many short futures. It starts with the actions that look promising, tries others now and then, and keeps track of how good each imagined future was. It then plays the action that it explored most. After the game, it trains its imagined world so that its predictions agree with what really happened and with what the search found.

## The problem

The agent acts in an environment with observations $o_t$, actions $a_t$ from a finite set and rewards $u_t$, and it wants a policy with a large expected discounted return. This is [the control problem](/rl-control/). The rules of the environment are not given. MuZero is a [model-based](/model-based-reinforcement-learning/) method, but unlike [Dyna-Q](/dyna-q/) it does not predict the next observation. It learns only the quantities that the search needs: rewards, values and policies.

For the search alone, the input is a model $(h, g, f)$, an observation, a discount $\gamma$ and a number $N$ of simulations. The output is a visit count for each action at the root, and the action with the most visits.

## The algorithm

**Search.** Each node of the tree holds a hidden state $s$, the reward $r$ that the model predicted for the edge into it, a prior $P$, a visit count $N$ and a sum of returns $W$. For a child $c$ of a node $u$ with action $a$, the estimate of the action value is $Q(u, a) = r(c) + \gamma W(c)/N(c)$. The search selects the action that maximizes

$$\bar Q(u, a) + P(u, a)\,\frac{\sqrt{N(u)}}{1 + N(c)}\Big(c_1 + \log\frac{N(u) + c_2 + 1}{c_2}\Big),$$

with $c_1 = 1.25$ and $c_2 = 19652$. Here $\bar Q$ is $Q$ scaled to $[0, 1]$ by the smallest and largest $Q$ values seen so far in the tree, and $\bar Q = 0$ for an unvisited child.

```pseudo id=main
MUZERO-SEARCH(h, g, f, observation, γ, N)
L1  root ← a node with hidden state h(observation); (p, v) ← f(root state); give root a child for each action a, with prior p(a)
L2  for i ← 1 to N do
L3      node ← root; path ← [root]
L4      while node has children do
L5          a ← the action that maximizes the pUCT score; node ← child(node, a); append node to path
L6      (r, s) ← g(state of the parent of node, a); store r and s in node
L7      (p, v) ← f(s); give node a child for each action, with prior p; G ← v
L8      for each node u on path, from the leaf to the root do
L9          W(u) ← W(u) + G; N(u) ← N(u) + 1; update the min and max with r(u) + γ W(u)/N(u); G ← r(u) + γ G
L10 return the visit counts N(child(root, a)) and the action with the most visits
```

Each simulation goes down the tree by the pUCT rule until it reaches a node that has not been expanded (lines L3 to L5), calls the dynamics function once to get its reward and hidden state (line L6), and calls the prediction function to get its priors and value (line L7). The backup in lines L8 and L9 adds to each node on the path the discounted sum of the predicted rewards below it plus the discounted leaf value. So every simulation gives an $n$-step estimate of the return with a bootstrap from $f$. In the paper, the search also adds Dirichlet noise to the root priors during self-play. The code leaves this out.

**Training (not in the code).** Actors play with the search and store the trajectories in a replay buffer. The learner samples a position and unrolls the model for $K$ steps along the actions that were really taken: $s^0 = h(o_1, \ldots, o_t)$ and $(r^k, s^k) = g(s^{k-1}, a_{t+k})$. At each step it trains $f(s^k)$ to predict the visit distribution of the search at time $t + k$ and a value target, and $r^k$ to predict the observed reward. The value target is the game result in board games, and an $n$-step return that bootstraps from the search value in Atari. The loss sums these three terms over the $K + 1$ steps, plus weight decay. All three functions are trained together through the unrolled model.

## Example

Take a deterministic MDP with three states and $\gamma = 0.9$. In state 0, action 0 pays 1 and leads to a dead end, state 1, where every action pays 0 forever. Action 1 pays 0 and leads to state 2, where action 0 pays 2 and stays. So $Q^*(0, 0) = 1$ and $Q^*(0, 1) = 0.9 \cdot 2/(1 - 0.9) = 18$. The search gets the exact rewards and transitions as $g$, the value 0 for every state as $f$, and the same priors in every state. The tests give these counts at the root:

| priors (action 0, action 1) | simulations | visits | chosen action | $Q$ of action 1 at the root |
| --- | --- | --- | --- | --- |
| 0.5, 0.5 | 10 | 9, 1 | 0 | 0 |
| 0.5, 0.5 | 50 | 13, 37 | 1 | 6.08 |
| 0.5, 0.5 | 800 | 21, 779 | 1 | 14.15 |
| 0.9, 0.1 | 200 | 199, 1 | 0 | 0 |
| 0.9, 0.1 | 400 | 285, 115 | 0 | 15.13 |
| 0.9, 0.1 | 800 | 285, 515 | 1 | 16.95 |

With few simulations, the search sees only the reward of 1 for action 0, because the value of every leaf is 0. As the tree grows deeper below action 1, its estimate rises toward 18 and the visits move to it. A wrong prior delays this: with prior 0.1 on the good action, the search needs between 400 and 800 simulations. This is the reason why MuZero trains $f$ to predict the visit counts. A good prior makes a small search strong.

On 500 random deterministic MDPs with up to 5 states, where the best action at the root is better than the others by at least 1, the search with an exact model, exact values and uniform priors finds the best action in every case with 100 simulations.

## Correctness

The search terminates: each simulation goes down at most as many levels as there are nodes, and adds one node. The output is a heuristic choice, not a proved optimal action. What can be proved about the search is in the proofs section:

- After every simulation, $N(u)$ is the number of simulations that passed through $u$, and $W(u)$ is the sum of their returns, each of which is the discounted predicted reward below $u$ plus the discounted leaf value.
- If all priors are positive, every child of the root, and in fact every node of the infinite tree, is visited infinitely often as $N$ grows. The bonus of a rarely visited child grows like $\sqrt{N}$, while the bonus of the most visited child goes to 0.
- With an exact model and exact values $V^*$, every estimate $Q(\text{root}, a)$ is at most $Q^*(\text{root}, a)$, and it equals $Q^*(\text{root}, a)$ after the first visit to $a$. Later visits that explore poor actions below $a$ pull the mean down, so the most visited action is not always the best one when the gaps are small.

The quality of a real MuZero agent depends on how well $h$, $g$ and $f$ are learned, which no theorem here covers. The original paper supports it by experiments.

## Complexity

A simulation goes down $d \le D$ levels and scores $A$ children at each level, so the selection costs $O(dA)$. Each simulation makes one call to $g$ and one to $f$, and the backup costs $O(d)$. So a search costs $O(N(DA + M))$ time, where $M$ is the cost of one call of $g$ and $f$, and $D \le N$. Each simulation creates $A$ children, so the tree has $O(NA)$ nodes. In practice the network calls dominate the cost. The paper used 800 simulations per move for the board games and 50 for Atari.

## Properties

- **Deterministic search.** For a fixed model and number of simulations, the search returns the same counts. The randomness of self-play comes from the root noise and from sampling the action by the visit counts.
- **Anytime.** The search can stop after any number of simulations and return the counts so far.
- **Uses only values, rewards and policies.** The model is never asked to predict an observation, so it can ignore the parts of the world that do not matter for the return.
- **Policy improvement.** The visit distribution at the root usually puts more weight on good actions than the prior does, and training $f$ toward it is a form of [policy iteration](/policy-iteration/) with search as the improvement step.
- **Scale invariance.** The min-max normalization makes the pUCT rule work with rewards of any size, as in Atari, without knowing their range.

## Variants and improvements

- **AlphaZero.** The direct predecessor uses the same search, but with the true rules of the game as the dynamics and the true state as the hidden state.
- **MuZero Reanalyze and MuZero Unplugged.** Rerun the search on old trajectories with the newest network to make fresh training targets. This also lets MuZero learn from a fixed dataset, as in [offline reinforcement learning](/offline-reinforcement-learning/).
- **Sampled MuZero.** Hubert and others (2021) search over a sample of actions, which allows large or continuous action spaces.
- **Stochastic MuZero.** Antonoglou and others (2022) add chance nodes to the model, for environments with random transitions, such as backgammon.
- **EfficientZero.** Ye and others (2021) add a consistency loss between predicted and encoded hidden states and other changes, and reach strong Atari results with far less data.
- **Gumbel MuZero.** Danihelka and others (2022) replace the root selection by sampling without replacement with Gumbel noise and sequential halving, which improves the policy even with very few simulations.

## When to use it

Use MuZero when good decisions need planning, the environment can be simulated for many episodes but its rules are unknown or too costly to model in detail, and large compute for training is available. It was designed for board games and Atari, and later versions were applied to video compression and other control tasks. For small tabular problems, a [count model](/model-based-reinforcement-learning/) with exact planning or [Dyna-Q](/dyna-q/) is far simpler. When search at decision time is too slow, a model-free agent such as [DQN](/dqn/) may be the better choice.

## Pitfalls

- **Pessimistic unvisited children.** The score gives an unvisited child $\bar Q = 0$, which is the lowest possible normalized value. With a confident wrong prior, as in the example, the good action can stay almost unvisited for hundreds of simulations.
- **Normalization before the range exists.** Until two different $Q$ values are seen, the min-max normalization cannot scale, and the implementation uses the raw value. The pseudocode of the paper does the same.
- **Errors of the model compound.** The learned dynamics is trained for $K$ unrolled steps, but the search can go deeper. Predictions far below the root can be poor.
- **The most visited action is not the highest valued one.** The visit counts mix value and prior. With small gaps or few simulations they can pick an action that is not optimal even with an exact model.
- **Off-policy targets.** The value targets come from old trajectories, made by older policies. Reanalyze or shorter $n$-step returns reduce the bias.

## Implementations

## History

AlphaGo (2016), AlphaGo Zero (2017) and AlphaZero (2018) combined tree search with a network that predicts policies and values, and they used the known rules to simulate the game. The pUCT selection rule comes from this line of work, with roots in the predictor-plus-UCB rule of Rosin (2011) and in [UCT](/uct/) (Kocsis and Szepesvári 2006). Schrittwieser and others posted MuZero on arXiv in November 2019 and published it in Nature in December 2020. It replaced the rules by a learned model in a hidden state space, matched AlphaZero in Go, chess and shogi, and, as reported by the paper, set a new state of the art on the 57 Atari games of the Arcade Learning Environment. Later work extended it to stochastic environments, large action spaces, offline data and better sample efficiency.

## References
