---
tag: SB0VDK
kind: algorithm
slug: shapley-value-sampling
name: Monte Carlo Shapley value estimation
aliases:
- permutation sampling for the Shapley value
area: algorithmic-game-theory/cooperative-games
level: core
summary: Estimates Shapley values by averaging marginal contributions over random orders of the players, with Hoeffding error bounds.
model: real-ram
complexity:
  vars: {n: the number of players, m: the number of sampled orders, t: the time of one query of v}
  time: {worst: O(m n t)}
  space: {extra: O(n)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 1960
  people: [Irwin Mann, Lloyd S. Shapley, Javier Castro, Daniel Gomez, Juan Tejada]
  note: Mann and Shapley estimated the Shapley-Shubik index of the Electoral College by Monte Carlo sampling in 1960. Castro, Gomez and Tejada gave the general method with an error analysis in 2009.
prereqs: [shapley-value, hoeffding-inequality, fisher-yates-shuffle]
see_also: [union-bound, stratified-sampling, monte-carlo-integration, central-limit-theorem, owen-multilinear-extension, marginal-contribution-nets, power-index-dynamic-programming, power-index-hardness]
sources:
  - paper: doi:10.1016/j.cor.2008.04.004
    title: "Javier Castro, Daniel Gomez and Juan Tejada, Polynomial calculation of the Shapley value based on sampling, Computers and Operations Research 36(5) (2009), 1726-1730"
    locator: the estimator by sampling orders, its unbiasedness, and the sample size from the central limit theorem
  - url: https://www.rand.org/pubs/research_memoranda/RM2651.html
    title: "Irwin Mann and Lloyd S. Shapley, Values of large games, IV: Evaluating the Electoral College by Monte Carlo techniques, RAND Corporation, Research Memorandum RM-2651, 1960"
    locator: the Monte Carlo estimate of the Shapley-Shubik index of the states in the Electoral College
  - url: https://arxiv.org/abs/1306.4265
    title: "Sasan Maleki, Long Tran-Thanh, Greg Hines, Talal Rahwan and Alex Rogers, Bounding the estimation error of sampling-based Shapley value approximation, arXiv 1306.4265, 2013"
    locator: the finite-sample bounds from the Hoeffding and Bernstein inequalities, and the stratified version
  - paper: doi:10.1080/01621459.1963.10500830
    title: "Wassily Hoeffding, Probability inequalities for sums of bounded random variables, Journal of the American Statistical Association 58(301) (1963), 13-30"
    locator: the tail bound for the mean of independent bounded variables
  - book: isbn:9781608456529
    title: Georgios Chalkiadakis, Edith Elkind and Michael Wooldridge, Computational Aspects of Cooperative Game Theory, Morgan and Claypool, 2011
    locator: Chapter 2, Basic concepts (the Shapley value as an average over orders), and Chapter 4, Weighted voting games (the hardness that motivates approximation)
---

Monte Carlo Shapley value estimation draws $m$ random orders of the players, walks along each order, and pays each player the amount that it adds to the coalition of the players before it. The mean of these payments over the $m$ orders is an unbiased estimate of the [Shapley value](/shapley-value/). It needs only an oracle for $v$, and it uses $n$ queries per order. If each marginal contribution lies in an interval of length $r$, then $m = \lceil r^2 \ln(2n/\delta) / (2\varepsilon^2) \rceil$ orders put every player within $\varepsilon$ of its value with probability at least $1 - \delta$, by the [Hoeffding inequality](/hoeffding-inequality/). The exact value is #P-hard already for weighted voting games ([hardness of power indices](/power-index-hardness/)), so for large general games this estimate is often the only option.

## In plain words

The Shapley value of a player is what it adds to the group when the players arrive one at a time in a random order, averaged over all orders. There are too many orders to try them all. So we try some of them. For each sampled order, we let the players arrive, and we write down what each one adds when it comes in. At the end we take the average for each player. With more orders the averages come closer to the true values. A standard bound tells us how many orders are enough for a given accuracy and a given chance of failure.

## The problem

The input is a TU game $(N, v)$ with $N = \{1, \ldots, n\}$ and $v(\emptyset) = 0$, given as an oracle that returns $v(S)$ for a coalition $S$, and two numbers $\varepsilon > 0$ and $0 < \delta < 1$. The output is a vector $\hat\varphi$ with $|\hat\varphi_i - \varphi_i(v)| < \varepsilon$ for every player $i$, with probability at least $1 - \delta$. The guarantee needs a bound $r$ on the range of the marginal contributions: for each player $i$, the numbers $v(S \cup \{i\}) - v(S)$ lie in an interval of length at most $r$. For a monotone game with values in $[0, 1]$, such as a simple game, $r = 1$.

## The algorithm

Let $P_i^\pi$ be the set of the players before $i$ in the order $\pi$. The Shapley value is the mean of $\Delta_i(\pi) = v(P_i^\pi \cup \{i\}) - v(P_i^\pi)$ over a uniform random order $\pi$. The algorithm takes the sample mean.

```pseudo id=main
SHAPLEY-SAMPLING(N, v, m)
L1  total[i] ← 0 for each player i
L2  repeat m times
L3      π ← a uniform random order of N           ▷ Fisher-Yates shuffle
L4      S ← ∅; prev ← 0                          ▷ prev = v(S)
L5      for each player i, in the order π do
L6          S ← S ∪ {i}
L7          cur ← v(S)
L8          total[i] ← total[i] + cur - prev       ▷ the marginal contribution of i
L9          prev ← cur
L10 return total[i] / m for each player i
```

Choose $m$ by the bound of the section on correctness: $m = \lceil r^2 \ln(2n/\delta) / (2\varepsilon^2) \rceil$ for all $n$ players at once, or $\lceil r^2 \ln(2/\delta) / (2\varepsilon^2) \rceil$ for one player. The walk along one order reuses each value: $v(S)$ is queried once and serves as $cur$ for one player and as $prev$ for the next, so one order costs $n$ queries, not $2n$.

## Example

Take the weighted voting game $[51; 50, 49, 1]$: players 1, 2 and 3 have the weights 50, 49 and 1, and a coalition wins ($v(S) = 1$) if its weight is at least 51. The exact Shapley values are $(2/3, 1/6, 1/6)$. Each marginal contribution is 1 for the pivot, the player whose arrival makes the coalition win, and 0 for the others.

Run the algorithm with $m = 4$ and these orders:

| order | weights so far | pivot | marginal contributions |
| --- | --- | --- | --- |
| 2, 1, 3 | 49, 99 | 1 | (1, 0, 0) |
| 3, 2, 1 | 1, 50, 100 | 1 | (1, 0, 0) |
| 1, 3, 2 | 50, 51 | 3 | (0, 0, 1) |
| 2, 3, 1 | 49, 50, 100 | 1 | (1, 0, 0) |

The totals are $(3, 0, 1)$ and the estimate is $(3/4, 0, 1/4)$. It sums to $v(N) = 1$, as every estimate does, but player 2 is off by $1/6$. Four orders are far too few.

Here $r = 1$. For $\varepsilon = 0.05$ and $\delta = 0.01$ for all three players, the bound asks for $m = \lceil \ln(600) / 0.005 \rceil = 1280$ orders, which is 3840 queries. For one player with $\varepsilon = 0.05$ and $\delta = 0.05$ the bound gives $m = 738$; for all of $n = 10$ players with the same numbers it gives $m = 1199$. The union bound over the players costs only a logarithmic factor.

## Correctness

For each order, lines L4 to L9 keep the invariant that $S$ holds the players already handled and $prev = v(S)$. So line L8 adds exactly $\Delta_i(\pi)$ to $total[i]$, and the additions of one order telescope to $v(N)$. Hence the output sums to $v(N)$ for every run (efficiency holds exactly, not only in expectation). If the orders are independent and uniform, each $\Delta_i(\pi_k)$ has the expected value $\varphi_i(v)$, so the estimate is unbiased. The terms for one player are independent and lie in an interval of length at most $r$, so Hoeffding's inequality gives
$$\Pr\big[|\hat\varphi_i - \varphi_i(v)| \ge \varepsilon\big] \le 2 \exp\!\left(-\frac{2 m \varepsilon^2}{r^2}\right),$$
and the [union bound](/union-bound/) over the $n$ players gives the choice of $m$ above. The full proofs are in [the proof file](proofs/correctness.md).

## Complexity

Let $t$ be the time of one query of $v$, including the time to pass the coalition.

- **Queries.** Exactly $m n$ queries of $v$. With the Hoeffding choice of $m$, this is $O(n\, r^2 \log(n/\delta) / \varepsilon^2)$ queries, polynomial in $n$, $1/\varepsilon$ and $\log(1/\delta)$.
- **Time.** $O(m n)$ for the shuffles (each Fisher-Yates shuffle is $O(n)$) and the additions, plus $O(m n t)$ for the queries.
- **Space.** $O(n)$ for the totals, the order and the coalition, plus the space of the oracle.

The cost per accuracy is the usual Monte Carlo rate: halving $\varepsilon$ costs four times as many orders. The error decreases as $1/\sqrt{m}$, so the method cannot give many exact digits.

## Properties

- **Unbiased.** $\mathbb{E}[\hat\varphi_i] = \varphi_i(v)$ for each player and each $m \ge 1$.
- **Efficient for every sample.** $\sum_i \hat\varphi_i = v(N)$ exactly, because each order divides $v(N)$.
- **Symmetric and null in expectation only.** Two symmetric players have the same expected estimate, but in one run their estimates differ. A null player gets exactly 0 in every run, since all its marginal contributions are 0.
- **Additive error, not relative.** The bound controls $|\hat\varphi_i - \varphi_i|$. A player with a tiny value can get the estimate 0 or a value many times too large.
- **Variance.** $\mathrm{Var}(\hat\varphi_i) = \sigma_i^2 / m$, where $\sigma_i^2$ is the variance of $\Delta_i(\pi)$ over a uniform order. Since the terms lie in an interval of length $r$, $\sigma_i^2 \le r^2/4$.

## Variants and improvements

- **Sampling by the subset formula.** Pick a size $s$ uniformly from $\{0, \ldots, n-1\}$, then a uniform $S \subseteq N \setminus \{i\}$ with $|S| = s$, and average $v(S \cup \{i\}) - v(S)$. This is also unbiased, because the weight $s!\,(n-s-1)!/n!$ equals $\frac{1}{n} \binom{n-1}{s}^{-1}$. It costs two queries per sample and per player, so it is better only when one wants a few players.
- **Stratified sampling.** Split the samples of player $i$ by the size of $P_i^\pi$ (its position in the order) and sample each stratum separately, as in [stratified sampling](/stratified-sampling/). Maleki et al. (2013) give bounds for this version. It helps when the marginal contributions vary much more between sizes than within a size, which is typical for voting games.
- **Bounds from the variance.** Castro, Gomez and Tejada (2009) choose $m$ by the [central limit theorem](/central-limit-theorem/), with an estimated or a bounded variance. This gives a smaller $m$ than Hoeffding when $\sigma_i$ is small, but only an asymptotic guarantee. The Bernstein inequality gives a finite-sample bound that also uses the variance.
- **Through the multilinear extension.** The Shapley value is the integral over $t \in [0, 1]$ of the gradient of [Owen's multilinear extension](/owen-multilinear-extension/) on the diagonal. One can sample $t$, then a random coalition with each player present with probability $t$. This is the [Monte Carlo integration](/monte-carlo-integration/) of that integral.
- **Exact methods for compact games.** For a [marginal contribution net](/marginal-contribution-nets/) the exact value takes linear time, and for a weighted voting game with small integer weights the exact index takes pseudo-polynomial time by [dynamic programming](/power-index-dynamic-programming/). Prefer them when they apply.

## When to use it

Use sampling when $n$ is too large for the $2^{n-1}$ terms of the subset formula (about $n > 25$ with a fast oracle), when $v$ is only available as an oracle, and when an additive error such as $0.01$ is good enough. Typical cases are cost allocation in large games with a cheap value function, power indices of large voting bodies with large weights, and feature attributions in machine learning, where $v(S)$ is the output of a model on a subset of its inputs. Do not use it when you need the exact value, a ranking of players with nearly equal values, or a relative error for small values.

## Pitfalls

- **The range $r$ must be a real bound.** The Hoeffding sample size is only valid if every marginal contribution lies in an interval of length $r$. If $v$ can take values in $[0, 10]$ and is not monotone, the marginal contributions lie in $[-10, 10]$, so $r = 20$, not 10.
- **Small values.** No sampling method gives a relative error for all players in polynomial time for weighted voting games: deciding whether an index is positive is NP-complete ([hardness of power indices](/power-index-hardness/)), and an estimate within a factor would decide it. An additive estimate of 0 does not prove that a player is a dummy.
- **Correlated estimates.** One order gives a term to every player, so the estimates of different players are not independent. The union bound does not need independence, but a test that compares two players must account for it.
- **Uniform orders.** Use a correct [Fisher-Yates shuffle](/fisher-yates-shuffle/). A naive shuffle that swaps each item with any position gives a biased order and a biased estimate. A pseudo-random generator with a period smaller than $n!$ cannot produce all orders (for Python's generator, this is the case for $n$ above about 2080); this does not break the bound for a mean of $m$ samples in practice, but it is a reason not to claim exact uniformity.
- **Floating point.** Accumulate in floating point only after you know the scale of $v$. For integer games, accumulate integers and divide once at the end, as line L10 does.

## Implementations

The Python version takes the generator as an argument (a `random.Random` with a fixed seed gives a repeatable run) and also computes the Hoeffding sample size and the Hoeffding failure bound.

## History

Mann and Shapley (1960) estimated the Shapley-Shubik index of the states in the United States Electoral College by Monte Carlo sampling of orders at RAND, and in a later memorandum (1962) they computed the values exactly. Castro, Gomez and Tejada (2009) described the sampling of orders for general games, proved that it is unbiased and gave the sample size from the central limit theorem. Maleki, Tran-Thanh, Hines, Rahwan and Rogers (2013) gave bounds for a finite number of samples from the Hoeffding and Bernstein inequalities and studied stratified sampling.

## References
