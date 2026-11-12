---
tag: PHHMGW
kind: algorithm
slug: epsilon-greedy
name: Epsilon-greedy
aliases:
- epsilon-greedy policy
- epsilon_n-greedy
- epsilon-greedy action selection
area: machine-learning/reinforcement-learning
level: intro
summary: "Pull a uniformly random arm with probability epsilon and the arm with the best mean otherwise. Constant epsilon gives linear regret; epsilon_t = cK/(d^2 t) gives log regret."
solves: [multi-armed-bandit]
model: real-ram
complexity:
  vars: {n: the number of rounds, K: the number of arms, d: a lower bound on the smallest positive gap}
  time: {worst: "Θ(n·K)"}
  space: {extra: "Θ(K)"}
  regret: {expected: "O(K log(n) / d^2)"}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 2002
  people: [Peter Auer, Nicolo Cesa-Bianchi, Paul Fischer]
  note: The constant rule is an old heuristic of reinforcement learning. Auer, Cesa-Bianchi and Fischer gave the decaying schedule and its first finite time log n bound.
prereqs: [multi-armed-bandit]
see_also: [exploration-exploitation-tradeoff, ucb1, thompson-sampling, q-learning, sarsa, lai-robbins-lower-bound]
sources:
  - paper: doi:10.1023/A:1013689704352
    title: Peter Auer, Nicolo Cesa-Bianchi and Paul Fischer, Finite-time analysis of the multiarmed bandit problem, Machine Learning 47(2-3), 2002
    locator: pp. 235 to 256; Section 2, Figure 3 (the epsilon_n-GREEDY policy) and Theorem 3 with the remark on c > 5; Section 3 (its proof); Section 4 (experiments)
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Chapter 2, Sections 2.2 to 2.4 (action-value methods, the 10-armed testbed and the incremental update)
  - book: isbn:9781108486828
    title: Tor Lattimore and Csaba Szepesvari, Bandit Algorithms, Cambridge University Press, 2020
    locator: Chapter 6 (explore-then-commit) and its notes on epsilon-greedy
---

Epsilon-greedy is the simplest exploration rule for the [multi-armed bandit](/multi-armed-bandit/): in round $t$, with probability $\varepsilon_t$ it pulls an arm chosen uniformly at random, and otherwise it pulls the arm with the largest empirical mean. With a constant $\varepsilon$ its [regret](/regret/) grows linearly in the horizon $n$. With the decaying rate $\varepsilon_t = \min(1, cK/(d^2 t))$ of Auer, Cesa-Bianchi and Fischer (2002), where $d$ is a lower bound on the smallest positive gap, the regret is $O(\log n)$. The same rule chooses actions in [Q-learning](/q-learning/), [SARSA](/sarsa/) and [DQN](/dqn/).

## In plain words

Keep the average payout of each machine so far. Before each play, flip a biased coin. On a rare result, play a machine chosen at random. Otherwise play the machine with the best average so far.

The random plays make sure that each machine keeps being tried, so a machine that was unlucky at the start can show its true value later. But if the share of random plays stays fixed, you keep wasting the same share of plays on bad machines for ever. So the better version lowers the share over time: many random plays at the start, few later.

## The problem

The input is a stochastic bandit with $K$ arms and rewards in $[0,1]$, a horizon $n$, and a schedule $\varepsilon_1, \varepsilon_2, \ldots$ in $[0,1]$. The output is a sequence of pulls $A_1, \ldots, A_n$, chosen online. The goal is small regret $R_n = \sum_i \Delta_i \mathbb{E}[T_i(n)]$, with the notation of the [multi-armed bandit](/multi-armed-bandit/) page: $\mu_i$ the means, $\Delta_i = \mu^* - \mu_i$ the gaps, $T_i(n)$ the number of pulls of arm $i$.

## The algorithm

```pseudo id=main
EPSILON-GREEDY(K, n, ε_1 .. ε_n)
L1  for i ← 1 to K do N[i] ← 0, S[i] ← 0
L2  for t ← 1 to n do
L3      draw U uniformly from [0, 1); if U < ε_t then
L4          A ← an arm drawn uniformly from 1 .. K       ▷ explore
L5      else A ← argmax_i Q[i], with Q[i] = S[i] / N[i], and Q[i] = +∞ if N[i] = 0, ties to the smallest i
L6      pull arm A and observe the reward X
L7      N[A] ← N[A] + 1, S[A] ← S[A] + X
```

$N[i]$ counts the pulls of arm $i$ and $S[i]$ sums its rewards, so $Q[i]$ is the empirical mean. The value $+\infty$ for an arm never pulled makes the greedy branch try each arm once. Three schedules matter:

- $\varepsilon_t = 0$: the pure greedy rule.
- $\varepsilon_t = \varepsilon$, a constant: the rule of most RL code.
- $\varepsilon_t = \min(1, cK/(d^2 t))$ with $c > 0$ and $0 < d < 1$: the $\varepsilon_n$-GREEDY rule of Auer, Cesa-Bianchi and Fischer (Figure 3 of their paper). Its Theorem 3 needs $d \le \min_{i : \Delta_i > 0} \Delta_i$. For the first $cK/d^2$ rounds the rate is 1, so the rule starts with uniform exploration.

## Example

Take three Bernoulli arms with means $(0.7, 0.5, 0.3)$ and a constant $\varepsilon = 0.2$. The policy uses `random.Random(5)` and the arms use `random.Random(105)`. The column $S/N$ lists $S[i]/N[i]$ after the round.

| $t$ | $U$ | branch | arm | reward | $S/N$ for arms 1, 2, 3 |
|---|---|---|---|---|---|
| 1 | 0.623 | greedy | 1 | 0 | 0/1, 0/0, 0/0 |
| 2 | 0.742 | greedy | 2 | 1 | 0/1, 1/1, 0/0 |
| 3 | 0.795 | greedy | 3 | 0 | 0/1, 1/1, 0/1 |
| 4 | 0.942 | greedy | 2 | 0 | 0/1, 1/2, 0/1 |
| 5 | 0.740 | greedy | 2 | 1 | 0/1, 2/3, 0/1 |
| 6 | 0.922 | greedy | 2 | 0 | 0/1, 2/4, 0/1 |
| 7 | 0.029 | explore | 2 | 1 | 0/1, 3/5, 0/1 |
| 8 | 0.776 | greedy | 2 | 1 | 0/1, 4/6, 0/1 |
| 9 | 0.249 | greedy | 2 | 1 | 0/1, 5/7, 0/1 |
| 10 | 0.052 | explore | 1 | 0 | 0/2, 5/7, 0/1 |

Rounds 1 to 3 pull each arm once. The best arm, arm 1, pays 0 on its first pull, so the greedy branch keeps pulling arm 2. Only the exploration of round 10 pulls arm 1 again, and it pays 0 again. Without exploration, arm 1 would never be pulled again in this run, because $Q[2] > 0 = Q[1]$ for ever.

**Regret over many runs.** On the means $(0.9, 0.6, 0.5)$, averaged over the seeds 0 to 19, constant $\varepsilon = 0.1$ has regret 28.2, 98.9 and 379.7 at $n = 1000$, 4000 and 16000: linear growth, just above the lower bound $\varepsilon n \sum_i \Delta_i / K$, which is 23.3, 93.3 and 373.3. The schedule with $c = 5$ and $d = 0.3$ (the true smallest gap) has regret 106.4, 159.6 and 213.9 at the same horizons: each factor of 4 in $n$ adds about 54, which is growth in $\log n$. At small $n$ the decaying rule is worse, since it explores uniformly for its first $cK/d^2 \approx 167$ rounds.

## Correctness

The estimates are right: before round $t$, $N[i] = T_i(t-1)$ and $S[i]$ is the sum of the rewards of arm $i$ so far, by induction on $t$. The regret claims are:

- **Constant rate, linear regret.** Each round pulls each arm with probability at least $\varepsilon/K$, so $R_n \ge \frac{\varepsilon n}{K}\sum_i \Delta_i$.
- **Greedy, linear regret.** For two Bernoulli arms with $\mu_1 > \mu_2 > 0$, with probability $(1-\mu_1)\mu_2$ the first pull of arm 1 pays 0 and the first pull of arm 2 pays 1. Then arm 1 is never pulled again, so $R_n \ge (1-\mu_1)\mu_2(\mu_1 - \mu_2)(n-2)$.
- **Decaying rate, logarithmic regret** (Auer, Cesa-Bianchi and Fischer 2002, Theorem 3). For all $K > 1$ and rewards in $[0,1]$, if $0 < d \le \min_{i:\Delta_i>0}\Delta_i$, then for $t \ge cK/d$ the probability that round $t$ pulls a given suboptimal arm $j$ is at most $\frac{c}{d^2 t}$ plus two terms that are $o(1/t)$ when $c > 5$. Summing over $t$ gives $\mathbb{E}[T_j(n)] \le \frac{c}{d^2}\ln n + O(1)$.

The [proof page](proofs/correctness.md) proves the first three claims in full, proves the exploration part of the fourth, and sketches the greedy part with a pointer to the paper.

## Complexity

- **Time.** Each round draws one or two random numbers and, in the greedy branch, scans $K$ means, so the time is $\Theta(K)$ per round and $\Theta(nK)$ in total. A heap keyed by $Q$ gives $O(\log K)$ per round.
- **Space.** $\Theta(K)$ for $N$ and $S$.
- **Regret, constant rate.** $\Theta(n)$ in expectation whenever some gap is positive.
- **Regret, decaying rate.** $\mathbb{E}[T_j(n)] \le \frac{c}{d^2}\ln n + O(1)$ for each suboptimal arm $j$ when $c > 5$, so $R_n \le \frac{c}{d^2}\sum_j \Delta_j \ln n + O(1) = O(K \log(n) / d^2)$. This is worse than [UCB1](/ucb1/), whose bound has $1/\Delta_j$ in place of $\Delta_j / d^2$, and much worse when $d$ is small.

## Properties

- **Randomized.** The exploration needs random bits even when the rewards are deterministic.
- **Explores without direction.** A random pull is as likely to go to an arm that is clearly bad as to an arm that is still uncertain. [UCB1](/ucb1/) and [Thompson sampling](/thompson-sampling/) direct their exploration to the uncertain arms.
- **Needs knowledge for the guarantee.** The logarithmic bound needs $d$ below the smallest gap. The gap is unknown in practice; a guess that is too large voids the theorem.
- **Works with any value estimate.** Line L5 only needs an estimate of each action's value, so the rule works with action values from a learned function in RL.

## Variants and improvements

- **Explore-then-commit.** Pull each arm $m$ times, then commit to the best. It is epsilon-greedy with $\varepsilon_t = 1$ for $t \le mK$ and 0 after. With $m$ tuned to the gap it has $O(\log n)$ regret for two arms (Lattimore and Szepesvari, Chapter 6).
- **Optimistic initial values.** Set $Q[i]$ to a large value at the start, with $\varepsilon = 0$ (Sutton and Barto, Section 2.6). It explores at the start only.
- **Softmax or Boltzmann exploration.** Pull arm $i$ with probability proportional to $e^{Q[i]/\tau}$. Bad arms get fewer random pulls than good ones.
- **Decay by episodes in RL.** In [Q-learning](/q-learning/) and [DQN](/dqn/), $\varepsilon$ falls linearly from 1 to a small floor such as 0.1 or 0.01 over a fixed number of steps. There is no regret guarantee for this rule.

## When to use it

Use a constant epsilon-greedy rule as a baseline, or in RL with function approximation where a confidence bound is hard to compute. Use the decaying schedule when a lower bound on the gap is known. When the rewards are bounded and the arms are few, [UCB1](/ucb1/) needs no gap and has a better bound, and [Thompson sampling](/thompson-sampling/) is usually better in practice.

## Pitfalls

- **A constant epsilon in a long run.** The regret grows like $\varepsilon n \sum_i \Delta_i / K$. Lower $\varepsilon$ over time, as in the schedule of line L3.
- **A decay that is too fast.** With $\varepsilon_t = 1/t^2$ the total number of random pulls is finite, so the greedy lock-in of the example happens with positive probability and the regret is linear again. The $1/t$ rate is what makes the random pulls grow like $\log n$.
- **Unpulled arms with $Q = 0$.** If line L5 sets $Q[i] = 0$ for an arm never pulled, the greedy branch may never try it. Use $+\infty$, or pull each arm once first.
- **Ties broken to the first arm with real valued $Q$.** With Bernoulli rewards many means are equal at the start. A fixed tie rule is fine for analysis, but random tie breaking is less biased in practice.

## Implementations

## History

The rule with a constant rate is part of the folklore of reinforcement learning, and Sutton and Barto teach it in Chapter 2 of their book. Auer, Cesa-Bianchi and Fischer (2002) showed that a constant rate gives linear regret, introduced the $1/t$ schedule $\varepsilon_n$-GREEDY, and proved its logarithmic bound in the same paper as [UCB1](/ucb1/). In their experiments on Bernoulli arms, against UCB1-TUNED and UCB2, an $\varepsilon_n$-GREEDY with the best $c$ was almost always the best policy, but its performance fell quickly when $c$ was not tuned.

## References
