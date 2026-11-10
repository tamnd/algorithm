---
tag: N0K1CG
kind: technique
slug: randomized-rounding
name: Randomized rounding
aliases:
- Raghavan-Thompson rounding
- independent randomized rounding
- probabilistic rounding of an LP
area: approximation/lp-rounding
level: core
summary: Round each variable independently with probability equal to its fractional value, then bound the failure probability with a Chernoff bound and a union bound.
prereqs: [linear-programming-rounding, chernoff-bound, union-bound, linearity-of-expectation]
see_also: [lp-rounding-set-cover, max-sat-lp-rounding, randomized-approximation-algorithm, dependent-rounding, pessimistic-estimators, packing-integer-program, edge-disjoint-paths, lovasz-local-lemma]
sources:
  - paper: doi:10.1007/BF02579324
    title: Prabhakar Raghavan and Clark D. Thompson, Randomized rounding, a technique for provably good algorithms and algorithmic proofs, Combinatorica 7(4), 1987
    locator: pages 365 to 374
  - paper: doi:10.1016/0022-0000(88)90003-7
    title: Prabhakar Raghavan, Probabilistic construction of deterministic algorithms, approximating packing integer programs, Journal of Computer and System Sciences 37(2), 1988
    locator: pages 130 to 143
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 1.7 (randomized rounding for set cover), Section 5.10 (Chernoff bounds) and Section 5.11 (integer multicommodity flows)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 4 (tail inequalities and the wiring problem)
---

Randomized rounding turns a fractional LP solution into an integral one by reading each value as a probability. Each variable, or each group of variables that must pick one option, is rounded on its own, with $\Pr[\hat{x}_j = 1] = x^*_j$. By [linearity of expectation](/linearity-of-expectation/), each linear function of $\hat{x}$ has the same expectation as at $x^*$, so the expected cost equals $\text{LP}^*$. Each constraint is a sum of independent bounded terms, so a [Chernoff bound](/chernoff-bound/) shows that it is violated by much only with small probability, and a [union bound](/union-bound/) over all constraints gives a bound for all of them at once. Raghavan and Thompson introduced the method in 1987 for routing with low congestion, where it gives a ratio of $O(\log m / \log \log m)$ with high probability on a graph with $m$ edges.

## In plain words

Solve the easy version, where each choice may be taken in part. Then read each part as a chance: a choice that the easy version took to 0.7 is taken with chance 0.7, by its own coin flip.

On average, every total comes out the same as in the easy version. A total of many small independent coin flips seldom moves far from its average. So each rule is broken by much only with a tiny chance, and when there are not too many rules, the chance that some rule is broken by much is also small. If the result is bad, flip the coins again.

## When it applies

- **Probabilities from the LP.** The relaxation has values in $[0, 1]$, or a group of variables that sum to 1 and describe a choice of one option, such as one path for each pair in a routing problem.
- **Sums of independent terms.** Each constraint, or the objective, is a sum of terms that depend on different independent coins, each term in $[0, 1]$ after scaling. Then Chernoff bounds apply.
- **Few constraints, or slack.** The union bound needs a failure probability per constraint that is small compared with the number of constraints. This works for a polynomial number of constraints, or when each constraint has enough slack. Otherwise use a repair step, as for set cover, or the [Lovász local lemma](/lovasz-local-lemma/).

## The template

```pseudo id=main
RANDOMIZED-ROUND(I)
L1  x* ← an optimal solution of the LP relaxation of I
L2  x' ← SCALE(x*)                         ▷ hole: x', or λ·x* with λ < 1 for packing, or more rounds for covering
L3  for each group g of variables, independently
L4      pick option j in g with probability x'_j, or no option with the rest
L5  if CHECK(x̂) fails, then go to L3         ▷ hole: a bound that holds with high probability
L6  return REPAIR(x̂)                        ▷ hole: fix the few broken constraints, if any
```

**The analysis.** Let $X = \sum_i X_i$ be a constraint or a load, with independent $X_i \in [0, 1]$ and $\mathbb{E}[X] \le \mu$. The Chernoff bound gives, for $\delta > 0$,

$$\Pr[X \ge (1 + \delta) \mu] \le \Big( \frac{e^{\delta}}{(1 + \delta)^{1 + \delta}} \Big)^{\mu} \le \Big( \frac{e}{1 + \delta} \Big)^{(1 + \delta) \mu}.$$

Choose $\delta$ so that each bad event has probability at most $1/(\text{number of events})^2$, and take a union bound.

**The holes.**

- **SCALE.** For packing constraints $A x \le b$, scale down by $\lambda < 1$ first so that each constraint has slack; this loses a factor $\lambda$ in the objective. For covering constraints, take more than one round of coins.
- **CHECK.** The bad events are computable, for example the largest load, so a run can be checked and repeated until it meets the bound. The expected number of runs is then at most $1/(1 - p)$, where $p$ is the failure probability.
- **REPAIR.** Fix the broken constraints at a cost that the analysis bounds, as in [LP rounding for set cover](/lp-rounding-set-cover/).

## Classic examples

- **Low congestion routing.** Given a graph with $m \ge 16$ edges and pairs $(s_i, t_i)$ for $i = 1, \ldots, k$, choose one $s_i$-$t_i$ path for each pair to minimize the congestion, the largest number of paths on one edge. The LP asks for a fractional flow $f_i$ of value 1 from $s_i$ to $t_i$ for each $i$, with $\sum_i f_i(e) \le C$ on each edge $e$, and minimizes $C$. It has polynomial size, so it is solved in polynomial time by an interior point or ellipsoid method with no separation oracle. Let $C^*$ be its optimum; then $C^* \le \text{OPT}$, and $\text{OPT} \ge 1$ when $k \ge 1$.
  1. Decompose each $f_i$ into at most $m$ paths with weights that sum to 1.
  2. For each $i$ independently, pick one path, each with probability equal to its weight.
  3. The load on $e$ is $X_e = \sum_i X_{i,e}$, where $X_{i,e}$ indicates that the path of pair $i$ uses $e$. The $X_{i,e}$ are independent across $i$, and $\mathbb{E}[X_e] = \sum_i f_i(e) \le C^* \le \mu$ with $\mu = \max(C^*, 1)$.
  4. Take $1 + \delta = 4 \ln m / \ln \ln m$, which exceeds $e$. Since $\mu \ge 1$, the bound above gives $\Pr[X_e \ge (1 + \delta) \mu] \le \exp\big( -(1 + \delta) \ln \frac{1 + \delta}{e} \big) \le m^{-2}$. The last step reduces to $\ln \ln m - 2 \ln \ln \ln m + 2 \ln 4 - 2 \ge 0$, which holds for $m \ge 16$.
  5. A union bound over the $m$ edges shows that, with probability at least $1 - 1/m$, the congestion is at most $\frac{4 \ln m}{\ln \ln m} \max(C^*, 1) \le \frac{4 \ln m}{\ln \ln m} \text{OPT}$.

  So the ratio is $O(\log m / \log \log m)$ with high probability. When $C^* \ge 9 \ln m$, the bound $\Pr[X \ge (1 + \delta) \mu] \le e^{-\delta^2 \mu / 3}$ for $\delta \le 1$ gives congestion $C^* + O(\sqrt{C^* \log m})$ instead. For directed graphs the ratio $O(\log m / \log \log m)$ is the best possible up to the constant under standard complexity assumptions (Chuzhoy, Guruswami, Khanna and Talwar, 2007).
- **Set cover.** Take each set with probability $x^*_S$ in $\lceil \ln n \rceil$ independent rounds and cover the rest with cheap sets, for $O(\log n)$ in expectation; see [LP rounding for set cover](/lp-rounding-set-cover/).
- **MAX-SAT.** Set each variable true with probability $y^*_i$; each clause is satisfied with probability at least $(1 - 1/e) z^*_j$, for a ratio $1 - 1/e$ in expectation; see [MAX-SAT LP rounding](/max-sat-lp-rounding/).
- **Packing integer programs.** Scale by $\lambda < 1$ and round; Raghavan (1988) showed that each constraint holds with high probability when $\lambda$ is chosen from the Chernoff bound, and derandomized the method with [pessimistic estimators](/pessimistic-estimators/); see [packing integer programs](/packing-integer-program/).
- **Covering integer programs.** Scale up by $O(\log m)$ and round, for an $O(\log m)$ ratio; see [covering integer programs](/covering-integer-program/).

## Variations

- **Derandomization.** The [method of conditional expectations](/method-of-conditional-expectations/) with a pessimistic estimator, such as $\sum_e \mathbb{E}[(1 + \delta)^{X_e}] / (1 + \delta)^{(1 + \delta) \mu}$, fixes the coins one at a time and keeps the bound; see [pessimistic estimators](/pessimistic-estimators/).
- **Dependent rounding.** Correlated coins keep sums or degrees exactly and still give negative correlation, so Chernoff bounds still hold; see [dependent rounding](/dependent-rounding/), [pipage rounding](/pipage-rounding/) and [swap rounding](/swap-rounding/).
- **Nonlinear rounding functions.** Round with probability $g(x^*_j)$ in place of $x^*_j$, as in the variants of [MAX-SAT LP rounding](/max-sat-lp-rounding/).
- **Rounding with the local lemma.** When each bad event depends on few others, the [Lovász local lemma](/lovasz-local-lemma/) shows that all of them can be avoided at once, even when the union bound fails.
- **Limited independence.** Chernoff-type bounds also hold with [k-wise independence](/k-wise-independence/) for a large enough $k$, which gives smaller sample spaces.
- **Rounding a vector solution.** For [semidefinite programs](/semidefinite-programming/), the rounding uses a random hyperplane in place of independent coins, as for [maximum cut](/maximum-cut/).

## Pitfalls

- **Expectation alone does not give feasibility.** $\mathbb{E}[X_e] \le C^*$ says nothing about the largest load. A tail bound for each constraint and a union bound are needed.
- **A small mean.** When $C^*$ is much less than 1, the bound $(1 + \delta) C^*$ is less than 1 and cannot hold for an integral load. Use $\mu = \max(C^*, 1)$, which is valid because the Chernoff bound holds for any $\mu \ge \mathbb{E}[X]$.
- **Dependent coins.** Inside one group, the options are not independent, because exactly one is chosen. The load on an edge is still a sum of independent terms, one for each group, each in $\{0, 1\}$, because a path uses an edge at most once. If a choice can put more than one unit on an edge, scale each term into $[0, 1]$ first.
- **Many constraints.** With exponentially many constraints the union bound fails. Either use a repair step or a method that controls the dependence.
- **Floating point probabilities.** A path decomposition from a floating point LP can have weights that do not sum to 1. Normalize the weights for each group before the coins are drawn.

## Exercises

1. Prove the second inequality of the Chernoff bound above, from $e^{\delta} \le e^{1 + \delta}$.
2. Check step 4 of the routing example: show that $(1 + \delta) \ln \frac{1 + \delta}{e} \ge 2 \ln m$ for $1 + \delta = 4 \ln m / \ln \ln m$ and $m \ge 16$.
3. Show that if $C^* \ge 9 \ln m$, then with probability at least $1 - 1/m^2$ the congestion is at most $C^* + 3 \sqrt{C^* \ln m}$.
4. Show that each fractional $s$-$t$ flow of value 1 in a graph with $m$ edges is a sum of at most $m$ weighted paths and cycles, with path weights that sum to 1, and that the cycles can be dropped without raising any load.
5. Derandomize the routing algorithm with the pessimistic estimator in the variations, and show that it gives the same congestion bound in the worst case.

## References
