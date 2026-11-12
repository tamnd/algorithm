---
tag: WS67AB
kind: algorithm
slug: ucb1
name: UCB1
aliases:
- upper confidence bound
- UCB
- UCB1 policy
area: machine-learning/reinforcement-learning
level: core
summary: "Pull the arm with the largest empirical mean plus sqrt(2 ln t / N). The regret is at most a sum of 8 ln n / gap plus a constant, for each n."
solves: [multi-armed-bandit]
model: real-ram
complexity:
  vars: {n: the number of rounds, K: the number of arms, d: the smallest positive gap}
  time: {worst: "Θ(n·K)"}
  space: {extra: "Θ(K)"}
  regret: {expected: "O(K log(n) / d)"}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2002
  people: [Peter Auer, Nicolo Cesa-Bianchi, Paul Fischer]
  note: Agrawal (1995) gave index policies with log n regret in the limit. UCB1 made the index simple and gave a bound for each finite n.
prereqs: [multi-armed-bandit, hoeffding-inequality]
see_also: [exploration-exploitation-tradeoff, epsilon-greedy, thompson-sampling, lai-robbins-lower-bound, uct, contextual-bandit, exp3]
sources:
  - paper: doi:10.1023/A:1013689704352
    title: Peter Auer, Nicolo Cesa-Bianchi and Paul Fischer, Finite-time analysis of the multiarmed bandit problem, Machine Learning 47(2-3), 2002
    locator: pp. 235 to 256; Figure 1 (UCB1) and Theorem 1; Section 3 (proof of Theorem 1)
  - book: isbn:9781108486828
    title: Tor Lattimore and Csaba Szepesvari, Bandit Algorithms, Cambridge University Press, 2020
    locator: Chapter 7 (the upper confidence bound algorithm, Theorem 7.1) and Chapter 8 (asymptotic optimality)
  - book: isbn:9780262039246
    title: Richard S. Sutton and Andrew G. Barto, Reinforcement Learning, An Introduction, second edition, MIT Press, 2018
    locator: Section 2.7 (upper confidence bound action selection)
---

UCB1 is an index policy for the stochastic [multi-armed bandit](/multi-armed-bandit/) with rewards in $[0,1]$. It pulls each arm once, and then in each round pulls the arm with the largest upper confidence bound $\bar X_i + \sqrt{2\ln t / N_i}$, where $\bar X_i$ is the mean reward of arm $i$ so far, $N_i$ is its number of pulls and $t$ is the total number of pulls so far. Auer, Cesa-Bianchi and Fischer (2002) proved that for each horizon $n$ its [regret](/regret/) is at most $\sum_{i:\Delta_i>0} 8\ln n/\Delta_i + (1+\pi^2/3)\sum_j \Delta_j$, with no knowledge of the gaps $\Delta_i$ or of $n$. The same rule picks the moves in [UCT](/uct/).

## In plain words

For each machine, keep the average payout so far. Add a bonus to it that is large when the machine has been played only a few times, and that grows slowly as the total number of plays grows. Then play the machine whose average plus bonus is largest.

The bonus says how much better the machine could still be, given what you know. A machine is played either because it looks good or because you know little about it. Each play of a machine shrinks its bonus, so a bad machine stops being played once you are sure it is bad. But the slow growth of the bonus means that no machine is ever dropped for good.

## The problem

The input is a stochastic bandit with $K \ge 2$ arms whose rewards are independent, with values in $[0,1]$ and unknown means $\mu_i$, and a horizon $n \ge K$. The output is a sequence of pulls $A_1, \ldots, A_n$, each chosen from the rewards seen so far. The goal is small regret $R_n = \sum_i \Delta_i\,\mathbb{E}[T_i(n)]$, where $\Delta_i = \mu^* - \mu_i$ and $T_i(n)$ is the number of pulls of arm $i$ in $n$ rounds.

## The algorithm

```pseudo id=main
UCB1(K, n)
L1  for i ← 1 to K do pull arm i once; N[i] ← 1, S[i] ← the reward
L2  for t ← K + 1 to n do
L3      for i ← 1 to K do U[i] ← S[i] / N[i] + sqrt(2 ln(t − 1) / N[i])
L4      A ← argmax_i U[i], ties to the smallest i
L5      pull arm A and observe the reward X
L6      N[A] ← N[A] + 1, S[A] ← S[A] + X
```

$N[i]$ counts the pulls of arm $i$ and $S[i]$ sums its rewards. Before round $t$ there have been $t - 1$ pulls, so the bonus uses $\ln(t-1)$; the paper writes it as $\sqrt{2\ln n / n_j}$ with $n$ the number of plays so far. The bonus is the radius of a confidence interval from the [Hoeffding inequality](/hoeffding-inequality/): after $s$ pulls, $\Pr[\bar X_{i,s} \ge \mu_i + \sqrt{2\ln u / s}] \le u^{-4}$. So $U[i]$ is above $\mu_i$ with high probability, and the rule is to act greedily on these optimistic values.

## Example

Take three Bernoulli arms with means $(0.7, 0.5, 0.3)$, and draw the rewards with `random.Random(3)`. Rounds 1 to 3 pull arms 1, 2 and 3, which pay 1, 0 and 0. The table lists the three indices at the start of each later round.

| $t$ | $U[1]$ | $U[2]$ | $U[3]$ | arm | reward | $N$ after the round |
|---|---|---|---|---|---|---|
| 4 | 2.482 | 1.482 | 1.482 | 1 | 1 | 2, 1, 1 |
| 5 | 2.177 | 1.665 | 1.665 | 1 | 1 | 3, 1, 1 |
| 6 | 2.036 | 1.794 | 1.794 | 1 | 1 | 4, 1, 1 |
| 7 | 1.947 | 1.893 | 1.893 | 1 | 1 | 5, 1, 1 |
| 8 | 1.882 | 1.973 | 1.973 | 2 | 0 | 5, 2, 1 |
| 9 | 1.912 | 1.442 | 2.039 | 3 | 1 | 5, 2, 2 |
| 10 | 1.937 | 1.482 | 1.982 | 3 | 1 | 5, 2, 3 |

In round 4, arm 1 has mean 1 after one pull, so $U[1] = 1 + \sqrt{2\ln 3} \approx 2.482$, and the other two have mean 0 and the same bonus. Arm 1 keeps paying 1, so its mean stays at 1, but its bonus falls as $N[1]$ grows. The bonuses of arms 2 and 3 grow with $\ln(t-1)$, and in round 8 they pass $U[1]$. The tie between arms 2 and 3 goes to arm 2. In rounds 9 and 10 arm 3 is pulled, pays 1 twice, and its mean rises to $2/3$.

**Regret over many runs.** On means $(0.9, 0.6, 0.3)$, averaged over the seeds 0 to 19, the regret is 38.7, 49.0, 59.1, 69.0, 79.4 and 88.6 at $n = 1000$, 2000, 4000, 8000, 16000 and 32000. Each doubling of $n$ adds about 10, which is growth in $\log n$. The bound of the theorem at $n = 32000$ is about 419, so it holds with a large margin. On the harder means $(0.9, 0.8, 0.7)$ the regret is 49.0, 74.3, 105.0, 137.3 and 174.8 at $n = 1000$ to 16000, against bounds from 830 to 1163.

## Correctness

The counts are right: before round $t$, $N[i] = T_i(t-1)$ and $S[i]$ is the sum of the rewards of arm $i$ so far, by induction on $t$.

**Theorem** (Auer, Cesa-Bianchi and Fischer 2002, Theorem 1). For all $K > 1$ and all reward distributions on $[0,1]$, for each $n \ge K$ and each suboptimal arm $i$,

$$\mathbb{E}[T_i(n)] \le \frac{8\ln n}{\Delta_i^2} + 1 + \frac{\pi^2}{3}, \qquad R_n \le \sum_{i:\Delta_i>0}\frac{8\ln n}{\Delta_i} + \Big(1+\frac{\pi^2}{3}\Big)\sum_{j=1}^{K}\Delta_j.$$

The idea of the proof: once arm $i$ has $\ell = \lceil 8\ln n/\Delta_i^2\rceil$ pulls, its bonus is at most $\Delta_i/2$. Then a further pull of arm $i$ needs the index of the best arm to fall below $\mu^*$, or the mean of arm $i$ to rise more than its bonus above $\mu_i$. By Hoeffding each event has probability at most $t^{-4}$, and a union bound over the at most $t^2$ pairs of pull counts gives a sum that converges to $\pi^2/3$. The [proof page](proofs/correctness.md) gives the proof in full.

## Complexity

- **Time.** Line L3 computes $K$ indices, so each round costs $\Theta(K)$ and the run costs $\Theta(nK)$. The indices of all arms change in each round, through $\ln(t-1)$, so a heap does not help directly.
- **Space.** $\Theta(K)$ for $N$ and $S$.
- **Regret.** $O(\sum_{i:\Delta_i>0} \log(n)/\Delta_i)$, which is $O(K\log(n)/d)$ with $d$ the smallest positive gap. Without the gaps, the same proof gives the worst case bound $O(\sqrt{nK\log n})$: split the arms at gap $\delta = \sqrt{K\ln n / n}$, so arms with smaller gaps cost at most $n\delta$ and the others cost at most $8K\ln n/\delta$ plus a constant.

## Properties

- **Deterministic.** Given the rewards, the pulls are fixed. All randomness comes from the arms.
- **Anytime.** The rule does not use $n$, and the bound holds at each $n$.
- **No tuning.** It needs no gap, no horizon and no parameter, only rewards in $[0,1]$.
- **Order optimal, not constant optimal.** The [Lai-Robbins lower bound](/lai-robbins-lower-bound/) says that a consistent policy pulls arm $i$ about $\ln n / \mathrm{KL}(\mu_i, \mu^*)$ times. By Pinsker's inequality $\mathrm{KL} \ge 2\Delta_i^2$ for Bernoulli arms, so the optimal coefficient is at most $1/(2\Delta_i^2)$, against 8 in the theorem.
- **Optimism.** The rule is the optimism principle in its simplest form: act as if each arm were as good as the data still allows.

## Variants and improvements

- **UCB1-TUNED** (same paper). Replace the 2 in the bonus by a bound on the empirical variance. It does better in practice, with no proof.
- **UCB2** (same paper). Play arms in epochs of growing length; its bound has a constant close to $1/(2\Delta_i^2)$.
- **Asymptotically optimal UCB** (Lattimore and Szepesvari, Chapter 8). The bonus $\sqrt{2\ln f(t)/N_i}$ with $f(t) = 1 + t\ln^2 t$ gives $\limsup_n \mathbb{E}[T_i(n)]/\ln n \le 2/\Delta_i^2$ for 1-subgaussian rewards, which matches the lower bound for Gaussian arms.
- **KL-UCB** (Lattimore and Szepesvari, Chapter 10). Use the largest $q$ with $N_i\,\mathrm{kl}(\bar X_i, q) \le \ln f(t)$. It matches the Lai-Robbins constant for Bernoulli arms.
- **MOSS** (Lattimore and Szepesvari, Chapter 9). A bonus that uses $n$ and $K$ gives the worst case regret $O(\sqrt{nK})$, without the $\sqrt{\log n}$.
- **LinUCB.** The same optimism with a confidence ellipsoid, for the linear [contextual bandit](/contextual-bandit/).
- **UCT.** UCB1 at each node of a search tree, in [Monte Carlo tree search](/monte-carlo-tree-search/).

## When to use it

Use UCB1 when the rewards are bounded, the arms are few and a deterministic policy with a guarantee is wanted. It is a good baseline and needs no tuning. When the reward distributions are known to be Bernoulli, KL-UCB and [Thompson sampling](/thompson-sampling/) have smaller regret. When the rewards can be chosen by an adversary, use [EXP3](/exp3/). When there are features for each round, use a [contextual bandit](/contextual-bandit/) method.

## Pitfalls

- **Rewards outside $[0,1]$.** The bonus assumes this range. Scale the rewards first, or the confidence interval is wrong.
- **An unpulled arm.** The index divides by $N[i]$. Line L1 pulls each arm once so that $N[i] \ge 1$.
- **The wrong log.** The bonus uses the log of the total number of pulls, not $\ln N[i]$. With the count of the arm itself, the bonus of an arm that is not pulled never grows, and the policy can lock onto a bad arm as the greedy rule does.
- **Changing rewards.** If the means change over time, the long memory of $\bar X_i$ makes UCB1 slow to react. Use a sliding window or a discount, or an adversarial method.
- **A large constant in practice.** The bonus explores more than is needed. In practice a smaller factor than 2 often does better, but then the theorem does not hold.

## Implementations

## History

Lai and Robbins (1985) built the first policies with regret $O(\log n)$, using upper confidence bounds that needed the whole history. Agrawal (1995) gave index policies based on the sample mean whose regret is also $O(\log n)$ in the limit. Auer, Cesa-Bianchi and Fischer (2002) gave UCB1, with its simple index and the first bound that holds for each finite $n$ and for each reward distribution on $[0,1]$. Kocsis and Szepesvari (2006) applied UCB1 to tree search as UCT, which led to strong Go programs.

## References
