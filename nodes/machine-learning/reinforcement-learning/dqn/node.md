---
tag: 5J3KX3
kind: algorithm
slug: dqn
name: Deep Q-network
aliases:
- DQN
- deep Q-learning with experience replay
area: machine-learning/reinforcement-learning
level: core
summary: "Q-learning with a neural network Q(s, a; theta), trained by SGD on minibatches from a replay buffer against targets from a target network that is copied every C steps. No convergence guarantee."
solves: [rl-control]
model: real-ram
complexity:
  vars: {T: the number of environment steps, B: the minibatch size, W: the cost of one forward and backward pass of the network, N: the replay capacity}
  time: {worst: "O(T B W)"}
  space: {extra: "O(N)"}
properties: {deterministic: false, online: true, exact: false, recursive: false}
history:
  year: 2013
  people: [Volodymyr Mnih, Koray Kavukcuoglu, David Silver]
  note: "Mnih et al. trained a convolutional Q-network with experience replay on seven Atari games in 2013, and added the target network for the 49-game Nature paper of 2015."
prereqs: [q-learning, experience-replay, value-function-approximation]
see_also: [double-dqn, dueling-network, prioritized-experience-replay, fitted-q-iteration, deadly-triad, double-q-learning, conservative-q-learning, td-error]
sources:
  - paper: "Volodymyr Mnih, Koray Kavukcuoglu, David Silver, Alex Graves, Ioannis Antonoglou, Daan Wierstra and Martin Riedmiller, Playing Atari with deep reinforcement learning, NIPS Deep Learning Workshop, 2013, arXiv:1312.5602"
    locator: Section 4 and Algorithm 1 (deep Q-learning with experience replay), Section 5 (the Atari experiments)
  - paper: doi:10.1038/nature14236
    title: "Volodymyr Mnih and others, Human-level control through deep reinforcement learning, Nature 518(7540), 2015, pages 529 to 533"
    locator: the main text, the Methods section (network, target network every C steps, error clipping, hyperparameters) and Algorithm 1
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 16.5 (human-level video game play) and Section 11.3 (the deadly triad)
  - paper: doi:10.1007/11564096_32
    title: "Martin Riedmiller, Neural fitted Q iteration, first experiences with a data efficient neural reinforcement learning method, ECML 2005, LNCS 3720, pages 317 to 328"
    locator: the NFQ algorithm (a Q-network refitted on all stored transitions against fixed targets)
  - paper: doi:10.1007/BF00992699
    title: "Long-Ji Lin, Self-improving reactive agents based on reinforcement learning, planning and teaching, Machine Learning 8(3-4), 1992, pages 293 to 321"
    locator: the section on experience replay
  - paper: doi:10.1109/9.580874
    title: "John N. Tsitsiklis and Benjamin Van Roy, An analysis of temporal-difference learning with function approximation, IEEE Transactions on Automatic Control 42(5), 1997, pages 674 to 690"
    locator: the divergence example for off-policy TD with linear function approximation
---

The deep Q-network (DQN) of Mnih et al. (2013, 2015) is [Q-learning](/q-learning/) with a neural network $Q(s, a; \theta)$ as the action-value function. Two changes make the training stable enough in practice: an [experience replay](/experience-replay/) buffer from which each update draws a uniform minibatch, and a *target network* $\theta^-$, a copy of $\theta$ that is refreshed only every $C$ steps and gives the bootstrap targets $y = r + \gamma \max_{a'} Q(s', a'; \theta^-)$. The loss is the Huber loss of $y - Q(s, a; \theta)$, which is the same as clipping the error to $[-1, 1]$ in the gradient. With one network, one set of hyperparameters and the raw screen as input, DQN reached the level of a professional human tester on many of 49 Atari 2600 games. It has no convergence guarantee: it combines function approximation, bootstrapping and off-policy data, the [deadly triad](/deadly-triad/).

## In plain words

Q-learning keeps a table with one number for each pair of a situation and an action: how much reward you can still get if you take that action there and act well later. When the situations are screen images, the table would be far too large. DQN replaces the table by a neural network that takes the situation and outputs one number per action.

Training such a network on the stream of play goes wrong in two ways. Consecutive frames look almost the same, so the network overfits to the latest few. And the network chases its own tail: each update changes the targets that the next update aims at. DQN fixes the first problem with a memory of past moves, from which it picks random batches. It fixes the second with a frozen copy of the network that supplies the targets, and refreshes the copy only now and then.

## The problem

The setting is [reinforcement learning control](/rl-control/) in an unknown MDP $(S, A, P, R, \gamma)$ with a finite action set $A$, under the discounted criterion with $0 \le \gamma < 1$. The agent sees samples $(s, a, r, s')$ and episode ends, not $P$ and $R$. The goal is a policy with a high expected discounted return; DQN aims at the optimal action-value function $Q^*$, the fixed point of the Bellman optimality operator, and acts greedily with respect to its estimate. The state may be large or continuous (an image), so $Q$ is a parametric function $Q(\cdot, \cdot; \theta)$, usually a network with one output per action, so that one forward pass gives $Q(s, a; \theta)$ for all $a$.

## The algorithm

Notation: $\theta$ are the online parameters, $\theta^-$ the target parameters, $D$ the replay buffer of capacity $N$, $B$ the minibatch size, $C$ the sync period, $\eta$ the step size, $\epsilon_t$ the exploration rate at step $t$. The Huber loss with threshold 1 is $h(\delta) = \tfrac12 \delta^2$ for $|\delta| \le 1$ and $|\delta| - \tfrac12$ otherwise, so $h'(\delta) = \mathrm{clip}(\delta, -1, 1)$.

```pseudo id=main
DQN(env, T, N, B, C, γ, η)
L1  D ← empty buffer of capacity N; θ ← random; θ⁻ ← θ
L2  for t ← 1 to T do
L3      a ← random action with probability ε_t, else argmax_a Q(s, a; θ)
L4      do a, observe r, s′, done; store (s, a, r, s′, done) in D
L5      draw a minibatch (s_j, a_j, r_j, s′_j, done_j), j = 1..B, uniformly from D
L6      y_j ← r_j if done_j, else r_j + γ max_a′ Q(s′_j, a′; θ⁻)
L7      θ ← θ − η ∇_θ (1/B) Σ_j h(y_j − Q(s_j, a_j; θ))       ▷ y_j is a constant
L8      if t mod C = 0 then θ⁻ ← θ
L9      s ← s′, or a new start state if done
```

Line L3 is $\epsilon$-greedy exploration; DQN anneals $\epsilon$ from 1 to 0.1 over the first part of training. Line L4 stores the transition, and the buffer drops its oldest transition when full. Line L5 starts after a warm-up period in practice. Line L6 computes the targets with the *target* network, and line L7 treats them as constants: the gradient flows only through $Q(s_j, a_j; \theta)$. Since $h'(\delta) = \mathrm{clip}(\delta, -1, 1)$, the step on one example is $\eta\, \mathrm{clip}(y_j - Q, -1, 1)\, \nabla_\theta Q(s_j, a_j; \theta)$, which is the "error clipping" of the Nature paper. Line L8 copies the online network into the target network every $C$ steps; between two copies the targets do not move.

**The Atari setup (history).** The Nature agent took the last four $84 \times 84$ grey frames as the state, used three convolutional layers and one hidden layer of 512 units, repeated each action for 4 frames, clipped rewards to $[-1, 1]$, and used RMSProp with minibatches of 32, a buffer of $10^6$ transitions, $C = 10^4$ updates and $\gamma = 0.99$. It trained for 50 million frames per game.

## Example

The chain has states $0, \ldots, 5$ and actions left and right. Moving right from state 5 ends the episode with reward 1; every other move gives 0, and left from state 0 stays there. With $\gamma = 0.9$, $Q^*(s, \text{right}) = 0.9^{5-s}$ and $Q^*(s, \text{left}) = 0.9^{6 - \max(s-1, 0)}$, so the optimal greedy policy goes right in every state.

**One update.** Suppose the target network gives $Q(4, \cdot; \theta^-) = (0.60, 0.85)$ and $Q(0, \cdot; \theta^-) = (0.50, 0.55)$ for (left, right), and the minibatch holds three transitions:

| transition | target $y$ | online $Q(s, a; \theta)$ | error $\delta = y - Q$ | $h'(\delta)$ |
|---|---|---|---|---|
| $(3, \text{right}, 0, 4)$ | $0.9 \cdot 0.85 = 0.765$ | 0.70 | 0.065 | 0.065 |
| $(5, \text{right}, 1, \text{end})$ | $1$ | $-0.40$ | 1.40 | 1 |
| $(0, \text{left}, 0, 0)$ | $0.9 \cdot 0.55 = 0.495$ | 0.52 | $-0.025$ | $-0.025$ |

The second error is clipped to 1, so one bad estimate cannot produce a huge step. The third target uses the maximum over the target network's values at state 0, not the online network's.

**A full run.** A one-hidden-layer network with 16 ReLU units on a one-hot state, trained by plain SGD with $\eta = 0.05$, $N = 1000$, $B = 16$, $C = 50$, a warm-up of 100 transitions, $\epsilon$ annealed from 1 to 0.1 over 1000 steps and 3000 steps in total (seed 0 of the implementation below), gives:

| state | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| learned $Q(s, \text{right})$ | 0.590 | 0.656 | 0.729 | 0.810 | 0.900 | 1.000 |
| $Q^*(s, \text{right})$ | 0.590 | 0.656 | 0.729 | 0.810 | 0.900 | 1.000 |
| learned $Q(s, \text{left})$ | 0.530 | 0.530 | 0.591 | 0.657 | 0.717 | 0.818 |
| $Q^*(s, \text{left})$ | 0.531 | 0.531 | 0.590 | 0.656 | 0.729 | 0.810 |

The greedy policy is optimal. The left values in states 4 and 5 are off by about 0.01, because the $\epsilon$-greedy agent rarely tries left there late in training.

## Correctness

DQN has no convergence guarantee for nonlinear networks, and none is claimed: off-policy bootstrapping with function approximation can diverge (Tsitsiklis and Van Roy, 1997; the [deadly triad](/deadly-triad/)). What does hold is the following, proved in full below.

1. Between two syncs, $\theta^-$ is fixed, so line L7 is a stochastic gradient step on the fixed regression loss $L(\theta) = \frac{1}{|D|} \sum_{i \in D} h(y_i - Q(s_i, a_i; \theta))$ of the current buffer: the minibatch gradient is an unbiased estimate of $\nabla L$. Without a target network the "loss" changes with every step and is not a fixed objective.
2. The gradient of the Huber loss is the error clipped to $[-1, 1]$.
3. In the tabular limit (one parameter per pair $(s, a)$, a fixed buffer that contains every pair, the regression solved exactly between syncs with the squared loss), the sequence of target networks is value iteration on the empirical MDP of the buffer, so it converges to that MDP's $Q^*$ at the rate $\gamma^k$ in the max norm. This is [fitted Q-iteration](/fitted-q-iteration/) with a lookup table.

## Complexity

Let $W$ be the cost of one forward and one backward pass of the network. Each step does one forward pass to act (line L3), $B$ forward passes of the target network (line L6) and $B$ forward and backward passes of the online network (line L7). So $T$ steps cost $O(T B W)$ arithmetic operations, in the worst case. A sync costs $O(|\theta|)$, which is at most $W$, once every $C$ steps. The buffer holds $N$ transitions, and the two networks hold $2|\theta|$ parameters. For the Nature agent, the memory of the buffer dominates: about $10^6$ frames of $84 \times 84$ bytes. The number of steps needed to reach a good policy has no known bound for this algorithm; the 50 million frames per game are an observed budget.

## Properties

- **Off-policy.** The targets use $\max_{a'}$, so transitions from older, more exploratory policies are valid training data. This is what allows replay.
- **Model-free and value-based.** It learns $Q$ and acts greedily; it needs a finite action set for the maximum of line L6. Continuous actions need [DDPG](/ddpg/) or similar methods.
- **Biased upward.** The maximum over noisy estimates overestimates in expectation ([double Q-learning](/double-q-learning/) gives the argument); [Double DQN](/double-dqn/) changes line L6 to reduce it.
- **Not convergent in general.** See Correctness.
- **Randomized.** Exploration, replay sampling and initialization use random numbers.

## Variants and improvements

- **[Double DQN](/double-dqn/).** Choose $\arg\max_{a'}$ with $\theta$ and evaluate it with $\theta^-$ in line L6.
- **[Dueling network](/dueling-network/).** Split the head into a state value and centered advantages.
- **[Prioritized experience replay](/prioritized-experience-replay/).** Draw line L5 in proportion to a power of the TD error, with importance weights.
- **Soft target updates.** Replace line L8 by $\theta^- \leftarrow \tau \theta + (1 - \tau)\theta^-$ at every step, as in [DDPG](/ddpg/).
- **Multi-step targets.** Use $n$-step returns in line L6 ([n-step TD](/n-step-td/)).
- **Distributional and combined agents.** C51 learns a distribution of returns instead of its mean; Rainbow combines six extensions. Recurrent replay (R2D2) stores sequences for partially observed games.
- **Offline use.** Run on a fixed buffer, DQN overestimates actions the data does not contain; [conservative Q-learning](/conservative-q-learning/) adds a penalty for this.

## When to use it

Use DQN, or one of its extensions, for control problems with a small discrete action set and large observations, where a simulator gives many cheap samples. For small finite MDPs, tabular [Q-learning](/q-learning/) is simpler and has a convergence proof. For a known model, use planning ([value iteration](/value-iteration/)). For continuous actions use actor-critic methods such as [DDPG](/ddpg/), [TD3](/td3/) or [soft actor-critic](/soft-actor-critic/). When samples are very expensive, model-based methods or [fitted Q-iteration](/fitted-q-iteration/) on all the data usually use them better.

## Pitfalls

- **Gradient through the target.** If line L7 also differentiates $y_j$ with respect to $\theta$ (a "full gradient" through $\max_{a'} Q(s', a'; \theta)$), the method becomes a residual gradient method with a different fixed point. Stop the gradient at $y_j$.
- **Clipping the loss instead of the gradient.** Clipping $(y - Q)^2$ to at most 1 makes the gradient zero for large errors. Clip the error $y - Q$ in the gradient, or use the Huber loss.
- **Bootstrapping at a time limit.** If an episode is cut by a step limit, the last state is not terminal; line L6 must bootstrap there. Treating the cut as terminal teaches the network that the reward stops.
- **Target sync too often.** With $C = 1$ the target network is the online network, and the training is the unstable plain semi-gradient Q-learning with a network.
- **Reward scale.** Clipping rewards to $[-1, 1]$, as in the Atari agent, changes the task: the agent cannot tell a small reward from a large one. Use it as a deliberate choice, not a default.
- **Too little exploration.** With $\epsilon$ annealed too fast, actions that were never tried keep their random initial values; the example above shows the small version of this in the left values.

## Implementations

## History

Neural networks for Q-values go back to Lin (1992), who also introduced experience replay, and to Riedmiller's neural fitted Q-iteration (2005), which refit a network on all stored transitions with targets fixed per iteration. Mnih et al. (2013) trained a convolutional Q-network from pixels with experience replay on seven Atari games. The Nature paper (Mnih et al., 2015) added the periodically updated target network and error clipping and reported results on 49 games with one architecture and one set of hyperparameters. Its success started the field of deep reinforcement learning and a long line of extensions (Double DQN, dueling networks, prioritized replay, distributional agents).

## References
