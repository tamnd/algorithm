---
tag: BSTS37
kind: algorithm
slug: fitted-q-iteration
name: Fitted Q-iteration
aliases:
- FQI
- neural fitted Q iteration
- NFQ
area: machine-learning/reinforcement-learning
level: advanced
summary: "Batch reinforcement learning: regress the targets r + gamma max Q(s', b) on a fixed set of transitions, again and again. With a tabular regressor it is value iteration on the empirical MDP."
solves: [rl-control]
model: real-ram
complexity:
  vars: {K: the number of iterations, n: the number of transitions, A: the number of actions, P: the cost of one prediction, R: the cost of one regression fit}
  time: {worst: "O(K (n A P + R))"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2005
  people: [Damien Ernst, Pierre Geurts, Louis Wehenkel, Martin Riedmiller]
  note: "Ernst, Geurts and Wehenkel named fitted Q iteration and used ensembles of regression trees. Riedmiller's neural fitted Q iteration of the same year uses a multilayer network."
prereqs: [value-iteration, value-function-approximation, action-value-function]
see_also: [q-learning, dqn, offline-reinforcement-learning, extremely-randomized-trees, k-nearest-neighbors, least-squares-td, conservative-q-learning, off-policy-evaluation]
sources:
  - paper: "Damien Ernst, Pierre Geurts and Louis Wehenkel, Tree-based batch mode reinforcement learning, Journal of Machine Learning Research 6, 2005, pages 503 to 556"
    locator: the fitted Q iteration algorithm, its convergence with kernel-based averagers, and the tree-based regressors including extremely randomized trees
  - paper: doi:10.1007/11564096_32
    title: Martin Riedmiller, Neural fitted Q iteration, first experiences with a data efficient neural reinforcement learning method, Machine Learning, ECML 2005, Lecture Notes in Computer Science 3720, pages 317 to 328
    locator: NFQ, fitted Q iteration with a multilayer perceptron trained by Rprop
  - paper: doi:10.1016/B978-1-55860-377-6.50040-2
    title: Geoffrey J. Gordon, Stable function approximation in dynamic programming, Machine Learning Proceedings 1995, pages 261 to 268
    locator: averagers, and the convergence of fitted value iteration with them
  - paper: doi:10.1023/A:1017928328829
    title: Dirk Ormoneit and Saunak Sen, Kernel-based reinforcement learning, Machine Learning 49, 2002, pages 161 to 178
    locator: fitted value iteration with kernel averagers and its consistency
  - paper: "Rémi Munos and Csaba Szepesvári, Finite-time bounds for fitted value iteration, Journal of Machine Learning Research 9, 2008, pages 815 to 857"
    locator: error bounds for fitted value iteration with general function classes
---

Fitted Q-iteration (FQI) learns an [action value function](/action-value-function/) from a fixed batch of transitions $(s, a, r, s')$ and no further contact with the environment. It runs [value iteration](/value-iteration/) on $Q$, but replaces each exact Bellman backup by a supervised regression. In round $k$ it computes the target $y = r + \gamma\max_b Q_{k-1}(s', b)$ for every transition and fits $Q_k$ to the pairs $((s, a), y)$ with any regression method. After $K$ rounds the greedy policy of $Q_K$ is the output. Ernst, Geurts and Wehenkel (2005) introduced the name and used ensembles of regression trees such as [extremely randomized trees](/extremely-randomized-trees/); Riedmiller (2005) used a neural network and called it NFQ. With a lookup table as the regressor, FQI is exactly value iteration on the empirical MDP of the data. With an averager such as [k-nearest neighbors](/k-nearest-neighbors/) it still converges. It is the batch ancestor of [DQN](/dqn/) and a base method of [offline reinforcement learning](/offline-reinforcement-learning/).

## In plain words

You have a fixed log of moves: where the agent was, what it did, what reward it got, and where it ended up. You cannot collect more. First you train a model that guesses the reward of each move. Then you train a new model on new labels: the reward plus the best guess of what can be got from the place the move led to. Then you do this again with the newest model, and again. Each round looks one step further into the future. The training method can be any regression method you like, such as trees, nearest neighbors or a neural network. In the end you act by picking the move with the highest guessed value.

## The problem

The input is a set $F$ of $n$ transitions $(s_i, a_i, r_i, s'_i)$ from a [Markov decision process](/markov-decision-process/) with a finite action set $A$ and discount $\gamma < 1$, collected by any policy; $s'_i$ is terminal when the episode ends at that step. The states may be continuous. The goal is the optimal action value function $Q^*$, the fixed point of the [Bellman optimality equation](/bellman-optimality-equation/), and a policy greedy for it: the [control problem](/rl-control/) from a batch of data. A regression method REGRESS is also given: it maps a training set of input and target pairs to a function.

## The algorithm

```pseudo id=main
FITTED-Q-ITERATION(F, A, γ, K, REGRESS)
L1  Q₀ ← 0
L2  for k ← 1 to K do
L3      TS ← empty list
L4      for each (s, a, r, s′) in F do
L5          y ← r if s′ is terminal, else r + γ max_{b ∈ A} Q_{k−1}(s′, b)
L6          append ((s, a), y) to TS
L7      Q_k ← REGRESS(TS)
L8  return Q_K          ▷ act with π(s) = argmax_a Q_K(s, a)
```

Every round refits from scratch on the same inputs $(s_i, a_i)$; only the targets change. The data are used again in every round, which makes FQI far more data-efficient than online [Q-learning](/q-learning/), which uses each transition once with a small step. The regression in line L7 is a full least-squares fit, not one gradient step.

## Example

A batch of five transitions on two states $A$ and $B$ with actions $0$ and $1$, $\gamma = 0.9$, and a tabular regressor (the mean target of each pair):

$(A, 0, 0, A)$, $(A, 1, 0, B)$, $(B, 0, 1, \text{end})$, $(B, 1, 0, A)$, $(B, 0, 0, \text{end})$.

The pair $(B, 0)$ has two transitions with rewards $1$ and $0$, so its mean is $0.5$ in every round.

| round $k$ | $Q_k(A, 0)$ | $Q_k(A, 1)$ | $Q_k(B, 0)$ | $Q_k(B, 1)$ |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0.5 | 0 |
| 2 | 0 | 0.45 | 0.5 | 0 |
| 3 | 0.405 | 0.45 | 0.5 | 0.405 |
| 4 | 0.405 | 0.45 | 0.5 | 0.405 |

Round $2$ sees that action $1$ in $A$ leads to $B$, whose best value is $0.5$, so $Q_2(A, 1) = 0.9 \cdot 0.5$. Round $3$ propagates one step further, and round $4$ changes nothing. The greedy policy takes action $1$ in $A$ and action $0$ in $B$.

**A continuous problem.** The state $x$ lies in $[0, 1)$. Action $+1$ moves it right by $0.1$ and action $-1$ moves it left by $0.1$, stopping at $0$. Reaching $1$ ends the episode with reward $1$; every other reward is $0$, and $\gamma = 0.9$. So $V^*(x) = 0.9^{m - 1}$, where $m$ is the number of right moves to reach $1$. The data are $n$ transitions from uniform random states and actions, and REGRESS is the $5$-nearest-neighbor average, fitted separately for each action. The table gives the largest error $\max_x|\max_a Q_k(x, a) - V^*(x)|$ over the ten points $x = 0.05, 0.15, \ldots, 0.95$, with seed 0.

| $n$ | after 5 rounds | after 10 rounds | after 30 rounds |
|---|---|---|---|
| 100 | 0.531 | 0.032 | 0.033 |
| 300 | 0.531 | 0.060 | 0.007 |
| 1000 | 0.590 | below 0.001 | below 0.001 |

After $5$ rounds the values are $0$ at the points that need more than $5$ moves: $Q_k$ only looks $k$ steps ahead. After $10$ rounds every point has its correct greedy action $+1$, and with $1000$ transitions the five neighbors of each test point lie in its own cell of width $0.1$, so the values are exact up to rounding.

## Correctness

The [proof](proofs/correctness.md) shows three facts. First, with the tabular regressor, $Q_k$ equals $k$ rounds of value iteration on the empirical MDP, whose rewards and transition probabilities are the sample means and frequencies of the data, with $Q = 0$ on pairs that never occur. Second, if REGRESS is an averager, that is its prediction is a convex combination of the targets with weights that depend only on the inputs, then one round of FQI is a $\gamma$-contraction in the sup norm, so $Q_k$ converges geometrically to a unique fixed point (Gordon 1995; Ernst, Geurts and Wehenkel 2005). Nearest-neighbor averages, nonnegative kernel averages and trees with a fixed structure are averagers. Third, if every round fits the true Bellman backup to within $\epsilon$ in the sup norm, then $\|Q_K - Q^*\|_\infty \le \gamma^K\|Q^*\|_\infty + \epsilon/(1 - \gamma)$, and the greedy policy loses at most $2/(1 - \gamma)$ times that.

## Complexity

Round $k$ evaluates $Q_{k-1}$ at the $nA$ pairs $(s'_i, b)$ and fits one regression on $n$ points, so $K$ rounds cost $O(K(nAP + R))$, where $P$ is the cost of one prediction and $R$ the cost of one fit. With a table, $P = O(1)$ and $R = O(n)$. With brute force $k$-nearest neighbors, $P = O(n)$, so a round costs $O(n^2A)$. With an ensemble of $M$ randomized trees, a fit costs about $O(Mn\log n)$ and a prediction $O(M\log n)$. The memory is $O(n)$ for the data and the targets, plus the regressor.

## Properties

- **Offline.** It needs only the batch, and it is off-policy: the data may come from any policy that covers the relevant actions.
- **Deterministic** for a deterministic regressor; randomized trees and neural networks add randomness.
- **Not exact.** It converges to the optimal $Q$ only for a table, or in the limit of rich function classes and many data.
- **Stable with averagers, not in general.** Least-squares linear regression and neural networks are not averagers, and FQI with them can diverge, as in the [deadly triad](/deadly-triad/).
- **Optimistic in the max.** The maximum in line L5 of noisy estimates is biased upward, and in offline data the maximum can pick actions the data never show.

## Variants and improvements

- **Neural fitted Q iteration (NFQ).** Riedmiller (2005) fits a multilayer network with the Rprop method in every round, on the whole batch.
- **DQN.** [DQN](/dqn/) is an online, stochastic version: a target network plays the role of $Q_{k-1}$, a replay buffer plays the role of $F$, and the regression is a few gradient steps instead of a full fit.
- **Fitted Q evaluation.** Replace $\max_b Q(s', b)$ with $\sum_b \pi(b \mid s')Q(s', b)$ to evaluate a fixed policy $\pi$; this is a direct method for [off-policy evaluation](/off-policy-evaluation/). With linear regression it converges to the [LSTD](/least-squares-td/) solution when it converges.
- **Fitted value iteration and kernel-based RL.** Gordon (1995) and Ormoneit and Sen (2002) fit state values with averagers and a model of the dynamics.
- **Least-squares policy iteration.** Lagoudakis and Parr (2003) alternate LSTD-Q evaluation with greedy improvement on a fixed batch.
- **Pessimistic FQI.** [Conservative Q-learning](/conservative-q-learning/) and similar methods penalize actions the batch does not cover.

## When to use it

Use FQI when you have a fixed batch of data, a small set of actions, and a good off-the-shelf regressor for the state space: tree ensembles for tabular features of moderate size, nearest neighbors for low dimensions, networks for images. It is a strong baseline for batch and [offline reinforcement learning](/offline-reinforcement-learning/). For large, growing streams of data use [DQN](/dqn/); for continuous actions the maximum in line L5 needs an actor or a search.

## Pitfalls

- **Distribution shift in the max.** In offline data, $\max_b Q(s', b)$ can choose an action never seen at states like $s'$, whose value the regressor only guesses. Errors grow over rounds.
- **Divergence with extrapolating regressors.** Linear regression and networks can extrapolate, so the map from $Q_{k-1}$ to $Q_k$ need not be a contraction.
- **Too few rounds.** $Q_K$ only plans $K$ steps ahead; choose $K$ with $\gamma^K$ small.
- **Terminal transitions.** Forgetting to drop the bootstrap term at the end of an episode adds a value that does not exist.
- **Unseen pairs.** A table predicts $0$ for pairs that never occur, which can make bad actions look good when rewards are negative.

## Implementations

## History

Fitted value iteration with averagers goes back to Gordon (1995), and Ormoneit and Sen (2002) studied kernel-based versions. Ernst, Geurts and Wehenkel (2005) gave fitted Q iteration its name and its general form with any regressor, and showed that ensembles of extremely randomized trees work well. In the same year Riedmiller (2005) introduced neural fitted Q iteration. Munos and Szepesvári (2008) gave finite-sample error bounds for fitted value iteration. The idea of a fixed target and a replay of stored data passed into [DQN](/dqn/) in 2013 and 2015.

## References
