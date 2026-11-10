---
tag: 7N315T
kind: algorithm
slug: frequency-rounding-set-cover
name: Frequency-based set cover rounding
aliases:
- f-approximation for set cover
- Hochbaum set cover rounding
- deterministic LP rounding for set cover
area: approximation/lp-rounding
level: core
summary: Solve the set cover LP and take each set with LP value at least 1/f, where f is the largest element frequency; the cover costs at most f times the optimum.
solves: [set-cover]
model: word-ram
complexity:
  vars: {n: the number of elements, m: the number of sets, s: the total size of all sets}
  time: {worst: poly(n + m)}
  space: {extra: Θ(n + m + s)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1982
  people: [Dorit S. Hochbaum]
  note: Hochbaum (1982) gave the f-approximation for weighted set cover by rounding the LP at 1/f, and also by rounding an optimal dual.
prereqs: [set-cover, element-frequency, lp-relaxation, threshold-rounding]
see_also: [lp-rounding-vertex-cover, set-cover-primal-dual, lp-rounding-set-cover, greedy-set-cover, hitting-set, integrality-gap, complementary-slackness, set-cover-inapproximability]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 1, Section 1.3 (a deterministic rounding algorithm) and Section 1.4 (rounding a dual solution)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 14, Section 14.1 (a simple rounding algorithm)
  - paper: doi:10.1137/0211045
    title: Dorit S. Hochbaum, Approximation algorithms for the set covering and vertex cover problems, SIAM Journal on Computing 11(3), 1982
    locator: pages 555 to 556
  - paper: doi:10.1016/j.jcss.2007.06.019
    title: Subhash Khot and Oded Regev, Vertex cover might be hard to approximate to within 2 − ε, Journal of Computer and System Sciences 74(3), 2008
    locator: the result for k-uniform hypergraph vertex cover (hardness k − ε under the Unique Games Conjecture)
---

Frequency rounding for [set cover](/set-cover/) solves the [LP relaxation](/lp-relaxation/) and takes each set whose LP value is at least $1/f$, where $f$ is the largest [element frequency](/element-frequency/), the largest number of sets that contain one element. The result is a cover of cost at most $f \cdot \text{LP}^* \le f \cdot \text{OPT}$ in the worst case, found in polynomial time. It is the general form of [LP rounding for vertex cover](/lp-rounding-vertex-cover/), which is the case $f = 2$, and the standard example of [threshold rounding](/threshold-rounding/). The ratio $f$ is tight for the LP, and under the [Unique Games Conjecture](/unique-games-conjecture/) no polynomial-time algorithm has ratio $f - \varepsilon$ for fixed $f \ge 2$.

## In plain words

You must buy some of the offered bundles so that each item is in a bought bundle, and you want to pay little. No item is in more than a few bundles; call the most bundles that share one item the crowd size. First solve the easier problem where you may buy a fraction of a bundle, with the fractions of each item adding to at least one.

Each item sits in at most the crowd size of bundles, so one of its bundles carries at least one share of that size. Buy each bundle whose fraction is at least that share. Each item is then covered, and each bought bundle costs at most the crowd size times what the fractional answer pays for it.

## The problem

The input is a universe $U$ of $n$ elements, sets $S_1, \ldots, S_m \subseteq U$ whose union is $U$, and costs $c_j \ge 0$. The output is a set of indices $I \subseteq \{1, \ldots, m\}$ with $\bigcup_{j \in I} S_j = U$. The goal is a small cost $c(I) = \sum_{j \in I} c_j$. The frequency of an element is $f_e = |\{j : e \in S_j\}|$, and $f = \max_e f_e$. The LP relaxation is

$$\text{LP}^* = \min \sum_{j=1}^m c_j x_j \quad \text{subject to} \quad \sum_{j : e \in S_j} x_j \ge 1 \text{ for each } e \in U, \qquad x \ge 0.$$

The indicator vector of each cover is feasible, so $\text{LP}^* \le \text{OPT}$; this is the lower bound of the analysis. The ratio convention is ALG $\le \rho \cdot$ OPT with $\rho \ge 1$.

## The algorithm

```pseudo id=main
FREQ-ROUND-SC(U, S_1, ..., S_m, c)
L1  f ← max over e in U of |{j : e ∈ S_j}|
L2  x ← an optimal solution of the set cover LP       ▷ ellipsoid or interior point method
L3  I ← ∅
L4  for j ← 1 to m do
L5      if x_j ≥ 1/f then I ← I ∪ {j}
L6  return I
```

Line L1 counts the frequencies in one pass over the sets. Line L2 solves an LP with $m$ variables and $n$ constraints, so of polynomial size, without a separation oracle. Lines L3 to L5 round at the threshold $1/f$. As for vertex cover, the proof works for each feasible $x$, so line L2 may return any optimal solution.

## Example

The universe is $\{1, \ldots, 7\}$, with five sets.

| set | elements | cost $c_j$ | LP value $x_j$ | $x_j \ge 1/3$? |
|---|---|---|---|---|
| $S_1$ | 4, 5, 7 | 1 | 1/3 | yes |
| $S_2$ | 1, 2, 3, 4, 6, 7 | 4 | 2/3 | yes |
| $S_3$ | 6, 7 | 3 | 0 | no |
| $S_4$ | 1, 3, 4, 5 | 3 | 1/3 | yes |
| $S_5$ | 1, 2, 5, 6 | 2 | 1/3 | yes |

The elements 2 and 3 are in two sets, and the others are in three, so $f = 3$. The table shows an optimal vertex of the LP, of value $\tfrac13 + \tfrac83 + 0 + 1 + \tfrac23 = \tfrac{14}{3}$. The dual solution $y_2 = 4/3$, $y_3 = 7/3$, $y_5 = 2/3$, $y_7 = 1/3$ and $y_e = 0$ for the other elements keeps the load of each set within its cost and has the same value, so LP* $= 14/3$.

The rounding takes $I = \{1, 2, 4, 5\}$ with cost $1 + 4 + 3 + 2 = 10$, which is at most $3 \cdot 14/3 = 14$. The optimum is $\{S_1, S_2\}$ with cost 5. The run has ratio 2 against OPT and $15/7 \approx 2.14$ against LP*.

## Correctness

**Theorem (Hochbaum 1982).** For each feasible solution $x$ of the set cover LP, the index set $I = \{j : x_j \ge 1/f\}$ is a cover with $c(I) \le f \sum_j c_j x_j$. With an optimal $x$, $c(I) \le f \cdot \text{LP}^* \le f \cdot \text{OPT}$.

Each element $e$ has $f_e \le f$ sets, and their values add up to at least 1, so the largest of them is at least $1/f_e \ge 1/f$, and that set is in $I$. For $j \in I$, $1 \le f x_j$, so $c_j \le f c_j x_j$. The full proof is in the proof file below.

**Tight examples.** Take $k > f$ sets and let the elements be all the $f$-element subsets of $\{1, \ldots, k\}$, with element $T$ in the sets $S_j$ for $j \in T$ and unit costs. Each element has frequency $f$. The point $x = (1/f, \ldots, 1/f)$ is the unique optimum of the LP, with value $k/f$: summing all constraints gives $\binom{k-1}{f-1} \sum_j x_j \ge \binom{k}{f}$, so $\sum_j x_j \ge k/f$, with equality only when all constraints are tight, and that forces all $x_j$ to be equal. The rounding takes all $k$ sets. A cover must miss fewer than $f$ sets, so OPT $= k - f + 1$. The ratio $k/(k - f + 1)$ of the algorithm and the [integrality gap](/integrality-gap/) $(k - f + 1)/(k/f)$ both tend to $f$ as $k$ grows.

**Hardness.** Set cover with frequency $f$ is the vertex cover problem of an $f$-uniform hypergraph. It is NP-hard to approximate within $f - 1 - \varepsilon$ (Dinur, Guruswami, Khot and Regev 2005), and within $f - \varepsilon$ under the Unique Games Conjecture (Khot and Regev 2008). When $f$ is not bounded, the $\ln n$ bound of [greedy set cover](/greedy-set-cover/) is the better one; see [set cover inapproximability](/set-cover-inapproximability/).

## Complexity

- **Time.** Line L1 takes $\Theta(n + m + s)$ time. The LP has $m$ variables, $n$ constraints and $s$ nonzero coefficients, all equal to 1; the [ellipsoid method](/ellipsoid-method/) or an [interior point method](/interior-point-method/) solves it in time polynomial in $n + m$ and the bit size of the costs, in the worst case. Lines L3 to L5 take $\Theta(m)$ time. The total is poly$(n + m)$.
- **Space.** The sets, the frequencies and the solution take $\Theta(n + m + s)$ space, besides the work space of the LP solver.

## Properties

- **Deterministic.** The output depends only on the LP solution.
- **A certificate.** LP* bounds OPT from below, so each run reports its own ratio, at most $f$.
- **Per element.** The proof gives more: each element $e$ is covered already by the sets with $x_j \ge 1/f_e$, so a threshold that depends on the element works too.
- **Sparse vertex solutions.** A vertex of the LP has at most $n$ nonzero coordinates, by the rank argument of [fractional solutions](/fractional-solution/), so the rounding picks at most $n$ sets.

## Variants and improvements

- **Dual rounding.** Solve the dual LP $\max \sum_e y_e$ subject to $\sum_{e \in S_j} y_e \le c_j$ and $y \ge 0$, and take each set whose dual constraint is tight. By [complementary slackness](/complementary-slackness/), each set with $x_j > 0$ in an optimal primal is tight, so this cover contains the cover of the primal rounding. Its cost is $\sum_{j \in I'} \sum_{e \in S_j} y_e \le f \sum_e y_e = f \cdot \text{LP}^*$ (Hochbaum 1982).
- **No LP solve.** The [primal-dual algorithm](/set-cover-primal-dual/) builds a feasible dual greedily and takes the tight sets. It has ratio $f$ and runs in time linear in the input size.
- **Vertex cover.** The case $f = 2$ is [LP rounding for vertex cover](/lp-rounding-vertex-cover/).
- **Large frequencies.** When $f$ is large, randomized rounding gives $O(\log n)$ instead of $f$; see [LP rounding for set cover](/lp-rounding-set-cover/).

## When to use it

Use frequency rounding when $f$ is small, for example $f = 2$ (vertex cover) or $f = 3$ (vertex cover of a 3-uniform hypergraph, triangle hitting), and when an LP solver is at hand. The primal-dual algorithm gives the same ratio $f$ much faster. When $f$ is larger than about $\ln n$, use [greedy set cover](/greedy-set-cover/) or randomized rounding, whose ratios grow with $\ln n$ and not with $f$.

## Pitfalls

- **The wrong $f$.** The threshold uses the largest frequency of an element, not the size of the largest set. With the set size in line L1, the threshold can be too low or too high; if it is too high, an element whose sets all have small values stays uncovered. In the example the largest set has 6 elements, but $f = 3$.
- **A strict test.** The test $x_j > 1/f$ in line L5 fails on the tight family above, where every value equals $1/f$: it takes no set. Use $x_j \ge 1/f$.
- **Floating-point values.** A solver may return $0.33333$ for $1/3$, which is below the threshold. Use exact arithmetic, or a tolerance and a final check that $I$ is a cover.
- **An element in no set.** Then no cover exists and the LP is infeasible. Check this before line L2.

## Implementations

The Python code solves the LP with a small exact simplex method in rational arithmetic, which is for small instances only.

## History

Hochbaum (1982) gave both forms of the $f$-approximation for weighted set cover: rounding the LP at $1/f$, and taking the sets that are tight in an optimal dual solution. Bar-Yehuda and Even (1981) gave a linear-time algorithm with the same ratio that needs no LP. Williamson and Shmoys use this algorithm to open their book, as the first example of deterministic rounding.

## References
