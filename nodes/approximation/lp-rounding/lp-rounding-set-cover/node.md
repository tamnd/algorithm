---
tag: 596RD9
kind: algorithm
slug: lp-rounding-set-cover
name: LP-rounding set cover
aliases:
- randomized rounding for set cover
- randomized LP rounding for set cover
area: approximation/lp-rounding
level: core
summary: Solve the set cover LP, take each set in ceil(ln n) independent rounds with probability equal to its LP value, and repair uncovered elements; the expected cost is O(log n) times the optimum.
solves: [set-cover]
model: word-ram
complexity:
  vars: {n: the number of elements, m: the number of sets, s: the total size of all sets}
  time: {worst: poly(n + m)}
  space: {extra: Θ(n + m + s)}
properties: {deterministic: false, recursive: false, online: false}
history:
  year: 1987
  people: [Prabhakar Raghavan, Clark D. Thompson]
  note: Randomized rounding comes from Raghavan and Thompson (1987); its use for set cover with ln n rounds is a standard textbook example.
prereqs: [set-cover, lp-relaxation, randomized-rounding, linearity-of-expectation, union-bound]
see_also: [frequency-rounding-set-cover, greedy-set-cover, set-cover-primal-dual, dual-fitting, set-cover-inapproximability, integrality-gap, randomized-approximation-algorithm, pessimistic-estimators]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 1, Section 1.7 (randomized rounding for set cover)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 14, Section 14.2 (randomized rounding)
  - paper: doi:10.1007/BF02579324
    title: Prabhakar Raghavan and Clark D. Thompson, Randomized rounding, a technique for provably good algorithms and algorithmic proofs, Combinatorica 7(4), 1987
    locator: pages 365 to 374
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 4 (tail inequalities, with randomized rounding for a wiring problem)
---

LP rounding for [set cover](/set-cover/) solves the [LP relaxation](/lp-relaxation/), reads each LP value $x_j$ as a probability, and takes each set in $t = \lceil \ln n \rceil$ independent rounds with that probability. An element that is still uncovered at the end gets a cheapest set that contains it. The output is always a cover, and its expected cost is at most $(\lceil \ln n \rceil + 1) \cdot \text{LP}^* \le (\ln n + 2) \cdot \text{OPT}$. This is the standard example of [randomized rounding](/randomized-rounding/). It matches the ratio of [greedy set cover](/greedy-set-cover/) up to a constant, and by the hardness of [set cover](/set-cover-inapproximability/), no polynomial-time algorithm has ratio $(1 - \varepsilon) \ln n$ unless P = NP.

## In plain words

You must buy some of the offered bundles so that each item is in a bought bundle, and you want to pay little. First solve the easier problem where you may buy a fraction of a bundle. Then read each fraction as the chance to buy that bundle, and flip a coin with that chance for each bundle, a few times over.

One round costs, on average, what the fractional answer costs, and it covers each item with a fair chance. After a number of rounds that grows like the logarithm of the number of items, each item is missed only rarely. For each item that is still missed, buy its cheapest bundle. That fix costs little on average, because it is rare.

## The problem

The input is a universe $U$ of $n$ elements, sets $S_1, \ldots, S_m \subseteq U$ whose union is $U$, and costs $c_j \ge 0$. The output is a set of indices $I$ with $\bigcup_{j \in I} S_j = U$, and the goal is a small cost $c(I) = \sum_{j \in I} c_j$. The LP relaxation is

$$\text{LP}^* = \min \sum_{j=1}^m c_j x_j \quad \text{subject to} \quad \sum_{j : e \in S_j} x_j \ge 1 \text{ for each } e \in U, \qquad x \ge 0.$$

Each cover gives a feasible point, so $\text{LP}^* \le \text{OPT}$; this is the lower bound of the analysis. The ratio convention is ALG $\le \rho \cdot$ OPT, and here the bound holds in expectation over the coins of the algorithm.

## The algorithm

```pseudo id=main
RAND-ROUND-SC(U, S_1, ..., S_m, c)
L1  x ← an optimal solution of the set cover LP         ▷ ellipsoid or interior point method
L2  t ← max(1, ⌈ln n⌉)
L3  I ← ∅
L4  for j ← 1 to m do
L5      with probability 1 − (1 − x_j)^t, independently: I ← I ∪ {j}
L6  for each e ∈ U not covered by the sets of I do
L7      I ← I ∪ {a cheapest j with e ∈ S_j}
L8  return I
```

Line L5 is the same as $t$ independent rounds, each of which takes set $j$ with probability $x_j$: the set is taken when at least one round takes it. An optimal $x$ with $c \ge 0$ can be taken with $x_j \le 1$, so these are probabilities. Line L1 solves an LP with $m$ variables and $n$ constraints, of polynomial size, so no separation oracle is needed. Lines L6 and L7 are the repair step; without them, the output is a cover only with high probability.

## Example

Let the elements be the 7 nonzero vectors of $\mathbb{F}_2^3$, and for each nonzero $v$ let the set $S_v$ hold the vectors $u$ with $\langle u, v \rangle = 1$, with cost 1. Each set has 4 elements, and each element is in 4 sets.

- **LP.** The point $x_v = 1/4$ for each $v$ is feasible, with value $7/4$, and the dual point $y_u = 1/4$ for each element has the same value, so $\text{LP}^* = 7/4$.
- **OPT.** A family of sets $S_v$, $v \in T$, misses exactly the nonzero vectors orthogonal to all of $T$. So it is a cover if and only if $T$ spans $\mathbb{F}_2^3$, and OPT $= 3$. The integrality gap of this instance is $12/7$.
- **Rounding.** Here $n = 7$ and $t = \lceil \ln 7 \rceil = 2$, so each set is taken with probability $1 - (3/4)^2 = 7/16$, and the rounding takes $49/16 \approx 3.06$ sets on average. An element is missed by all $2 \cdot 4 = 8$ coin rounds of its sets with probability $(3/4)^8 \approx 0.100$, so about $0.70$ elements need a repair on average.
- **Result.** With the lowest index as the tie rule in line L7, the exact expected cost over all $2^7$ outcomes is $965028091 / 2^{28} \approx 3.60$. The bound is $(t + 1) \cdot \text{LP}^* = 21/4 = 5.25$.

The same construction on $\mathbb{F}_2^k$ has $n = 2^k - 1$, $\text{LP}^* = n / 2^{k-1} < 2$ and OPT $= k$, so the [integrality gap](/integrality-gap/) of the set cover LP is at least about $\tfrac12 \log_2 n$. So no rounding of this LP gives a ratio of $o(\log n)$.

## Correctness

**Theorem.** RAND-ROUND-SC always returns a cover. Its expected cost is at most $(t + 1) \cdot \text{LP}^*$, with $t = \max(1, \lceil \ln n \rceil)$, so at most $(\lceil \ln n \rceil + 1) \cdot \text{OPT}$.

Set $j$ enters in line L5 with probability $1 - (1 - x_j)^t \le t x_j$, so the rounding costs at most $t \cdot \text{LP}^*$ in expectation. An element $e$ is missed with probability $\prod_{j \ni e} (1 - x_j)^t \le e^{-t \sum_{j \ni e} x_j} \le e^{-t} \le 1/n$. Its cheapest set costs at most $\sum_{j \ni e} c_j x_j \le \text{LP}^*$, because the values $x_j$ of its sets add up to at least 1. So the repairs cost at most $n \cdot (1/n) \cdot \text{LP}^* = \text{LP}^*$ in expectation. The full proof is in the proof file below.

**From expectation to high probability.** By the [Markov inequality](/markov-inequality/), one run costs at most $2(t + 1) \cdot \text{LP}^*$ with probability at least $1/2$. The algorithm can compute $\text{LP}^*$, so it can test this and run again; $k$ runs fail with probability at most $2^{-k}$. See [randomized approximation algorithms](/randomized-approximation-algorithm/).

**Tightness.** The integrality gap of about $\tfrac12 \log_2 n$ above shows that the analysis against $\text{LP}^*$ cannot give $o(\log n)$. For the problem, Dinur and Steurer (2014) showed that a ratio of $(1 - \varepsilon) \ln n$ is NP-hard for each $\varepsilon > 0$; see [set cover inapproximability](/set-cover-inapproximability/).

## Complexity

- **Time.** Line L1 solves an LP with $m$ variables, $n$ constraints and $s$ nonzero coefficients; the [ellipsoid method](/ellipsoid-method/) or an [interior point method](/interior-point-method/) does this in time polynomial in $n + m$ and the bit size of the costs, in the worst case. Lines L4 and L5 use $m$ random draws. The repair of lines L6 and L7 takes $O(n + m + s)$ time with a list of the cheapest set of each element. The total is poly$(n + m)$.
- **Space.** $\Theta(n + m + s)$ for the input, the LP solution and the coverage marks, besides the LP solver.

## Properties

- **Randomized, with a feasible output.** The output is a cover for every outcome of the coins; only the cost is random. In the terms of [randomized approximation algorithms](/randomized-approximation-algorithm/), the ratio holds in expectation.
- **A certificate.** $\text{LP}^*$ is a lower bound on OPT, so each run knows its own ratio and can decide to run again.
- **Any feasible $x$.** The proof uses only that $x$ is feasible, with $\text{LP}^*$ replaced by $c \cdot x$. A near-optimal $x$ from a fast approximate LP solver works too.
- **Number of rounds.** With $t$ rounds, the bound is $(t + n e^{-t}) \cdot \text{LP}^*$, and $t = \lceil \ln n \rceil$ makes it at most $(\ln n + 2) \cdot \text{LP}^*$.

## Variants and improvements

- **Without repair.** Take $t = \lceil 2 \ln n \rceil$ rounds and no repair. Then each element is missed with probability at most $1/n^2$, so by the [union bound](/union-bound/) the result is a cover with probability at least $1 - 1/n$, and its expected cost is at most $\lceil 2 \ln n \rceil \cdot \text{LP}^*$. The repair makes the output always feasible and about halves the constant.
- **Derandomization.** The [method of conditional expectations](/method-of-conditional-expectations/) with the [pessimistic estimator](/pessimistic-estimators/) $\sum_j c_j \Pr[j \in I] + \sum_e \Pr[e \text{ missed}] \cdot \min_{j \ni e} c_j$ fixes the coins one at a time and gives a deterministic cover of cost at most $(t + 1) \cdot \text{LP}^*$ (Raghavan 1988).
- **Bounded frequency.** When each element is in at most $f$ sets, the [frequency rounding](/frequency-rounding-set-cover/) at threshold $1/f$ gives ratio $f$ deterministically, which is better when $f < \ln n$.
- **Greedy.** [Greedy set cover](/greedy-set-cover/) has ratio $H_d \le \ln d + 1$, with $d$ the largest set size, and needs no LP. Its analysis by [dual fitting](/dual-fitting/) uses the same LP.
- **Covering integer programs.** The same rounding, with scaling of the probabilities and a [Chernoff bound](/chernoff-bound/), gives $O(\log n)$ for general [covering integer programs](/covering-integer-program/) with multiple covering.

## When to use it

Use it to teach and to analyze LP-based covering, and as a building block when the LP has extra side constraints that greedy cannot handle, for example budgets or a few packing constraints. For plain set cover, greedy is faster and has a slightly better constant. When each element is in few sets, use frequency rounding or the [primal-dual algorithm](/set-cover-primal-dual/).

## Pitfalls

- **One round only.** Taking each set once with probability $x_j$ covers an element with probability only $1 - \prod_{j \ni e} (1 - x_j) \ge 1 - 1/e$. The bound on the expected repair cost then becomes $(n/e) \cdot \text{LP}^*$ in place of $\text{LP}^*$.
- **The wrong logarithm.** The rounds are $\lceil \ln n \rceil$ with $n$ the number of elements, not the number of sets. With $t < \ln n$, the bound $n e^{-t} \le 1$ fails.
- **The repair choice.** The repair takes one cheapest set per missed element. The bound uses that its cost is at most $\sum_{j \ni e} c_j x_j \le \text{LP}^*$; any choice whose cost is not bounded this way can break the analysis.
- **Probabilities above 1.** A solver can return $x_j > 1$ at a non-unique optimum when $c_j = 0$. Cap $x_j$ at 1 before line L5; the proof still holds.

## Implementations

The Python code solves the LP with a small exact simplex method in rational arithmetic, so the probabilities $1 - (1 - x_j)^t$ are exact fractions. It exposes the repair step and the probabilities separately, so the expected cost can be computed exactly on small instances by summing over all $2^m$ coin outcomes.

## History

Raghavan and Thompson (1987) introduced randomized rounding for routing problems, and Raghavan (1988) derandomized it with pessimistic estimators. The $O(\log n)$ analysis of set cover by rounding in $\ln n$ rounds became a standard textbook example; Vazirani and Williamson and Shmoys both present it next to the deterministic rounding of Hochbaum (1982). The ratio was known earlier for greedy (Johnson 1974, Lovász 1975, Chvátal 1979). Feige (1998) and Dinur and Steurer (2014) showed that $\ln n$ is the right ratio up to lower-order terms.

## References
