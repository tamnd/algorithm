---
tag: 68PE88
kind: algorithm
slug: online-randomized-set-cover
name: Online randomized set cover
aliases:
- Alon et al. set cover algorithm
- AAABN algorithm
- online set cover by threshold rounding
area: online-and-streaming/competitive-analysis
level: research
summary: Keeps a fractional cover by a primal-dual multiplicative update and takes each set whose value passes a random threshold; the expected cost is O(log m log n) times the optimum.
solves: [online-set-cover-problem]
model: word-ram
complexity:
  vars: {s: the total size of the sets, m: the number of sets, n: the number of elements, r: the number of arrivals, d: the largest number of sets that contain one element, b: the bisection steps per arrival}
  time: {worst: O(s + m log n + r d b)}
  space: {extra: O(s + m)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 2003
  people: [Noga Alon, Baruch Awerbuch, Yossi Azar, Niv Buchbinder, Joseph (Seffi) Naor]
  note: Alon, Awerbuch, Azar, Buchbinder and Naor gave the first online set cover algorithm with a polylogarithmic ratio at STOC 2003, by a multiplicative fractional update and threshold rounding, and also derandomized it; the journal version appeared in 2009.
prereqs: [online-set-cover-problem, online-primal-dual, randomized-rounding, competitive-ratio]
see_also: [set-cover, greedy-set-cover, lp-rounding-set-cover, oblivious-adversary, adaptive-adversary, union-bound, online-facility-location-problem, online-vertex-cover-problem]
sources:
  - paper: doi:10.1137/060661946
    title: "Noga Alon, Baruch Awerbuch, Yossi Azar, Niv Buchbinder and Joseph (Seffi) Naor, The online set cover problem, SIAM Journal on Computing 39(2) (2009), 361-370"
    locator: Section 2 (the fractional algorithm) and Section 3 (the randomized rounding with 2 log n thresholds per set and its analysis)
  - paper: doi:10.1561/0400000024
    title: "Niv Buchbinder and Joseph (Seffi) Naor, The design of competitive online algorithms via a primal-dual approach, Foundations and Trends in Theoretical Computer Science 3(2-3) (2009), 93-263"
    locator: Chapter 4 (the continuous covering update and its O(log d) bound) and Chapter 5 (rounding the fractional set cover solution)
---

Online randomized set cover is the algorithm of Alon, Awerbuch, Azar, Buchbinder and Naor for [online set cover](/online-set-cover-problem/): the sets are known in advance, the elements arrive one at a time, and each arriving element must be covered at once by a set that is bought for good. The algorithm has two layers. A fractional layer keeps a value $x_S \in [0, 1]$ for each set and raises the values of the sets that contain a new element multiplicatively, by the [online primal-dual method](/online-primal-dual/), so its cost stays within $2 \ln(1 + d)$ of the optimum. A rounding layer draws, once and for all, a random threshold for each set, the minimum of $\lceil 2 \ln n \rceil$ uniform values, and buys a set as soon as its value passes its threshold. An element that is still uncovered then gets its cheapest set. The expected cost is $O(\log m \log n)$ times the optimum against an [oblivious adversary](/oblivious-adversary/), where $m$ is the number of sets and $n$ the number of elements.

## In plain words

A city must give each new street a fire station within reach, and a station, once built, stays. All possible sites and their prices are known, but the streets appear one at a time.

The planner keeps a soft score for each site, from zero to full. When a new street appears and the sites that reach it do not add up to one full site, the planner raises their scores, faster for cheap sites and for sites that already have a high score. Before the first street, each site also gets a secret random bar. The planner builds a site as soon as its score passes its bar. A bar is rarely low, so the real stations cost only a few times the soft plan. If a street is still out of reach, which is rare, the planner builds its cheapest site.

## The problem

The input is a ground set $X$ of $n$ elements, a family $\mathcal{S}$ of $m$ subsets of $X$, and a cost $c_S > 0$ for each set, all known at the start. Then elements $j_1, j_2, \ldots$ of $X$ arrive one at a time. After each arrival, the chosen family $C$ must contain a set with the new element, and sets can be added but never removed. The cost is $c(C) = \sum_{S \in C} c_S$, and $\mathrm{OPT}$ is the cheapest family that covers the elements that arrived. The ratio is $\mathbb{E}[c(C)] \le \rho \cdot \mathrm{OPT}$ with no additive term, against an adversary that fixes the sequence before the coins are drawn. $\mathcal{S}(j)$ is the family of sets that contain $j$, and $d = \max_j \lvert \mathcal{S}(j) \rvert \le m$. The [problem page](/online-set-cover-problem/) has the models, the lower bounds and the deterministic algorithm.

## The algorithm

```pseudo id=main
ONLINE-RANDOMIZED-SET-COVER(X, 𝒮, c, σ, rng)        ▷ σ = j_1, j_2, ..., revealed one at a time
L1  x_S ← 0 for each S ∈ 𝒮;  C ← ∅;  k ← ⌈2 ln n⌉
L2  for each S ∈ 𝒮 do θ_S ← min of k independent uniform values in [0, 1]
L3  for each arriving element j do
L4      𝒮(j) ← the sets that contain j
L5      while Σ_{S ∈ 𝒮(j)} x_S < 1 do raise y_j, with dx_S/dy_j = (x_S + 1/d)/c_S for each S ∈ 𝒮(j)
L6      for each S ∈ 𝒮(j) with x_S ≥ θ_S do C ← C ∪ {S}
L7      if no set of C contains j then
L8          C ← C ∪ {a cheapest set of 𝒮(j)}
L9  return C
```

Line L5 is the continuous update of the [online primal-dual method](/online-primal-dual/). The rate of $x_S$ depends only on $x_S$, so a raise of size $t$ gives exactly $x_S \leftarrow (x_S + 1/d) e^{t/c_S} - 1/d$, and the implementation finds the $t$ that makes the sum 1 by bisection. The dual value $y_j$ is not needed to run the algorithm; it is kept only for the analysis. The fractional layer, lines L4 and L5, never reads the thresholds or $C$.

## Example

Take $X = \{1, 2, 3\}$, the sets $A = \{1, 2\}$, $B = \{2, 3\}$ and $C' = \{1, 2, 3\}$ with costs 1, 1 and 3. Then $n = 3$, $d = 3$ and $k = \lceil 2 \ln 3 \rceil = 3$. The seed 0 of the implementation draws $\theta_A = 0.4206$, $\theta_B = 0.2589$ and $\theta_{C'} = 0.3033$. Elements 1 and 3 arrive.

| step | element | $\mathcal{S}(j)$ | raise $y_j$ | $x_A$ | $x_B$ | $x_{C'}$ | sets bought |
|---|---|---|---|---|---|---|---|
| 1 | 1 | $A, C'$ | 1.2482 | 0.8280 | 0 | 0.1720 | $A$ ($0.8280 \ge 0.4206$) |
| 2 | 3 | $B, C'$ | 1.0475 | 0.8280 | 0.6168 | 0.3832 | $B$ ($0.6168 \ge 0.2589$), $C'$ ($0.3832 \ge 0.3033$) |

At step 1 the raise $t$ solves $\frac{1}{3}(e^{t} - 1) + \frac{1}{3}(e^{t/3} - 1) = 1$, that is $e^t + e^{t/3} = 5$. The cheap set $A$ grows three times as fast as $C'$. The fractional cost is $P = 0.8280 + 0.6168 + 3 \cdot 0.3832 = 2.5943$, within twice the dual value $D = 1.2482 + 1.0475 = 2.2957$. The optimum is $\{A, B\}$ with cost 2. This run is unlucky: the low threshold of $C'$ makes it pay 5. Over the coins, the expected cost of the threshold sets is $\sum_S c_S (1 - (1 - x_S)^3) = 4.2346$, and no fallback is needed with probability above 0.98. The guarantee is about the expectation and about large $n$; on tiny inputs the factor $k \ln(1+d)$ is larger than the trivial bound.

## Correctness

The [proof](proofs/correctness.md) has four parts. First, the output is a cover, because L8 covers each element that the thresholds miss. Second, the fractional layer pays at most $2 \ln(1 + d) \cdot \mathrm{OPT}_{LP}$: while $y_j$ rises, the primal cost grows at rate $\sum x_S + \lvert \mathcal{S}(j) \rvert / d < 2$, and for each set $x_S = (e^{Y_S/c_S} - 1)/d \le 1$ with $Y_S = \sum_{j \in S} y_j$, so $y / \ln(1 + d)$ is a feasible dual and [weak duality](/weak-duality/) applies. Third, $\theta_S$ is the minimum of $k$ uniform values, so $\Pr[\theta_S \le x_S] = 1 - (1 - x_S)^k \le k x_S$, and the threshold sets cost at most $k$ times the fractional cost in expectation. Fourth, an element is missed only if every set that contains it has $\theta_S > x_S$, which has probability at most $\prod (1 - x_S)^k \le e^{-k} \le 1/n^2$; the fallback set costs at most $\mathrm{OPT}$, so all fallbacks together cost at most $\mathrm{OPT}/n$ in expectation. The total is

$$\mathbb{E}[c(C)] \le 2 \lceil 2 \ln n \rceil \ln(1 + d) \cdot \mathrm{OPT} + \frac{\mathrm{OPT}}{n} = O(\log m \log n) \cdot \mathrm{OPT}.$$

The third and fourth parts need the values $x_S$ to be fixed numbers, independent of the thresholds. This holds because the fractional layer never reads the coins and the oblivious adversary fixes the input in advance.

## Complexity

- **Time.** Building the index from elements to sets costs $O(s)$, where $s = \sum_S \lvert S \rvert$, and line L2 draws $mk = O(m \log n)$ random values. Each arrival costs $O(d\,b)$ for $b$ bisection steps in L5, and $O(d)$ for L6 to L8, because $j$ is covered by $C$ exactly when some set of $\mathcal{S}(j)$ is in $C$. The total is $O(s + m \log n + r\,d\,b)$ for $r$ arrivals.
- **Space.** $O(s)$ for the index and $O(m)$ for $x$, $\theta$ and the flags of $C$. Only the minimum of the $k$ draws is kept.
- **Randomness.** All $mk$ random values are drawn before the first arrival, and the rest of the run is deterministic.

## Properties

- **Online and monotone.** $x_S$ never decreases and $C$ never loses a set. Each decision uses only the elements seen so far.
- **Always a cover.** The fallback of L8 makes the output a valid cover for every outcome of the coins; only the cost is random.
- **Oblivious adversary only.** The analysis needs the input to be independent of the thresholds. An adaptive adversary that sees $C$ can send elements in sets whose thresholds are high, and the bound does not hold.
- **The two logarithms come from two places.** $\ln(1 + d) \le \ln(1 + m)$ comes from the fractional layer, and $k = O(\log n)$ from the rounding. With unit costs, each fallback set costs $1 \le \mathrm{OPT}_{LP}$, so the whole bound holds against the fractional optimum: $O(\log d \log n) \cdot \mathrm{OPT}_{LP}$.
- **Weighted for free.** Costs enter only through the rate $1/c_S$ of L5 and the choice in L8; the bound does not depend on the ratio of the largest to the smallest cost.

## Variants and improvements

- **Discrete update.** Alon et al. raise the values in discrete steps: while the constraint of $j$ is violated, each $x_S$ with $S \in \mathcal{S}(j)$ is multiplied by a constant factor, with a small additive term so that values can leave zero. With unit costs the factor is 2. The analysis is the same with other constants. The continuous update of L5 is the form in the monograph of Buchbinder and Naor.
- **Deterministic version.** Alon et al. replace the random thresholds by a pessimistic estimator, a potential function that the algorithm keeps small when it buys sets. This gives a deterministic online algorithm with the same ratio $O(\log m \log n)$, which they also showed nearly optimal for deterministic algorithms; see [online set cover](/online-set-cover-problem/).
- **Fractional layer alone.** The fractional layer by itself is $O(\log d)$-competitive for the fractional problem, and this is optimal: the halving adversary of the [online primal-dual](/online-primal-dual/) page forces cost $1 + (\log_2 d)/2$ against $\mathrm{OPT} = 1$.
- **Other covering problems.** The same two layers, a multiplicative fractional update and a rounding step made for the problem, are the pattern of many later online algorithms, for example for non-metric facility location and for covering problems in which each element must be covered several times. The packing form of the same update gives the primal-dual analysis of the [adwords problem](/online-adwords-problem/).

## When to use it

Use it when sets must be bought as requirements appear and cannot be returned, the set system is known in advance, and the adversary cannot react to the random choices, for example when the requests come from a fixed but unknown workload. If the whole input is known, the offline [greedy set cover](/greedy-set-cover/) gives $H_n \le 1 + \ln n$, which is better by a factor $\log m$. If the adversary is adaptive, use the deterministic version.

## Pitfalls

- **Drawing new thresholds at each step.** The thresholds must be drawn once. A fresh draw at each step gives each set many chances to be bought, and the bound $\Pr[S \in C] \le k x_S$ fails.
- **Too few thresholds.** With $k$ below $2 \ln n$, the miss probability $e^{-k}$ is no longer below $1/n^2$, and the fallbacks can cost more than $\mathrm{OPT}$ in total. The value $n$ is the size of the ground set, which is known at the start.
- **A careless fallback.** L8 must take a cheapest set of $\mathcal{S}(j)$. A more expensive one can cost more than $\mathrm{OPT}$, and the bound $\mathrm{OPT}/n$ fails.
- **Reading $C$ in the fractional layer.** If the update skips sets that are already in $C$ or stops early when $j$ is already covered, the values $x_S$ depend on the coins, and the analysis of the thresholds no longer applies.
- **Floating point in L5.** The bisection must return the upper end of its interval, so that the sum is at least 1. If it returns a value with sum $1 - 10^{-12}$, the constraint of $j$ is not met, and a test that checks the constraint exactly fails.

## Implementations

## History

Online set cover with the set system known and the elements arriving was introduced by Alon, Awerbuch, Azar, Buchbinder and Naor at STOC 2003, and the journal version appeared in the SIAM Journal on Computing in 2009. The paper gave the multiplicative fractional update, the threshold rounding of this page, its derandomization and a nearly matching lower bound for deterministic algorithms. Buchbinder and Naor then turned the fractional update into a general method for online covering and packing, with the continuous form used here, in their 2005 ESA paper, their 2009 paper in Mathematics of Operations Research and their 2009 monograph.

## References
