---
tag: 4YZZK4
kind: technique
slug: threshold-rounding
name: Threshold rounding
aliases:
- deterministic rounding
- deterministic threshold rounding
- rounding up above a threshold
area: approximation/lp-rounding
level: intro
summary: Round up every variable at or above a fixed threshold and down otherwise; gives an f-approximation when each constraint has at most f variables.
prereqs: [lp-relaxation, linear-programming-rounding, covering-integer-program]
see_also: [lp-rounding-vertex-cover, frequency-rounding-set-cover, half-integrality, fractional-solution, randomized-rounding, integrality-gap, hitting-set, max-flow-min-cut-theorem]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 1.3 (a deterministic rounding algorithm for set cover)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Section 14.1 (a simple rounding algorithm)
  - paper: doi:10.1137/0211045
    title: Dorit S. Hochbaum, Approximation algorithms for the set covering and vertex cover problems, SIAM Journal on Computing 11(3), 1982
    locator: pages 555 to 556
---

Threshold rounding is the simplest way to turn a fractional solution of a covering LP into an integral one. Solve the [LP relaxation](/lp-relaxation/), fix a threshold $t \in (0, 1]$, and set each variable to 1 if its LP value is at least $t$ and to 0 otherwise. Each chosen variable has LP value at least $t$, so the cost is at most $\frac{1}{t}$ times the LP value. The result is feasible when each constraint holds a variable of value at least $t$. If each constraint has at most $f$ variables, $t = 1/f$ always works, which gives an $f$-approximation: $\text{ALG} \le f \cdot \text{LP}^* \le f \cdot \text{OPT}$ in the worst case.

## In plain words

First solve the easy version of the problem, where each item may be taken in part. Then pick a cut-off level. Take every item whose part is at or above the cut-off, and drop the rest.

Each item that you take was already paid for at the cut-off level or more, so the full price is at most one over the cut-off times what the easy version paid. If every rule says "take at least one of these few items", then one of them must carry a fair share of the total, so a cut-off of one over the number of items keeps every rule true.

## When it applies

- **A covering LP with 0-1 coefficients.** The constraints have the form $\sum_{j \in T_i} x_j \ge 1$ for sets $T_i$ of variables, with costs $c_j \ge 0$ and $0 \le x_j \le 1$. This is the shape of [vertex cover](/vertex-cover/), [set cover](/set-cover/) and [hitting set](/hitting-set/).
- **A large value in each constraint.** Some $t$ is such that each constraint has a variable with $x^*_j \ge t$. With $|T_i| \le f$, the constraint $\sum_{j \in T_i} x^*_j \ge 1$ forces $\max_{j \in T_i} x^*_j \ge 1/f$, so $t = 1/f$ is enough.
- **A deterministic answer.** The method uses no coins, so the bound holds in the worst case on every run.

## The template

```pseudo id=main
THRESHOLD-ROUND(c, T_1, ..., T_m)
L1  x* ← an optimal solution of min Σ c_j x_j, Σ_{j ∈ T_i} x_j ≥ 1, 0 ≤ x ≤ 1   ▷ polynomial time
L2  t ← THRESHOLD(x*, T_1, ..., T_m)                                     ▷ hole: 1/f, 1/2, or problem specific
L3  for each variable j
L4      x̂_j ← 1 if x*_j ≥ t, else 0
L5  return x̂
```

**Claim.** If each constraint $T_i$ has a variable with $x^*_j \ge t$, then $\hat{x}$ is feasible and $c \cdot \hat{x} \le \frac{1}{t} \, c \cdot x^* = \frac{1}{t} \text{LP}^* \le \frac{1}{t} \text{OPT}$.

*Proof.* Feasibility: each $T_i$ has a $j$ with $x^*_j \ge t$, and line L4 sets $\hat{x}_j = 1$. Cost: if $\hat{x}_j = 1$ then $x^*_j / t \ge 1 = \hat{x}_j$, and if $\hat{x}_j = 0$ then $x^*_j / t \ge 0 = \hat{x}_j$. So $c_j \hat{x}_j \le c_j x^*_j / t$ for each $j$, because $c_j \ge 0$. Sum over $j$. Each integral solution is feasible for the LP, so $\text{LP}^* \le \text{OPT}$. $\square$

The LP has polynomial size, so it is solved in polynomial time by the [ellipsoid method](/ellipsoid-method/) or an [interior point method](/interior-point-method/), with no separation oracle. Lines L3 and L4 take linear time.

**The hole.** THRESHOLD picks $t$. The largest $t$ that still meets every constraint gives the best bound from this proof, and that value is $\min_i \max_{j \in T_i} x^*_j$.

## Classic examples

- **Vertex cover, $t = 1/2$.** Each edge constraint $x_u + x_v \ge 1$ has two variables, so one of them is at least $1/2$. The result is a 2-approximation. See [LP rounding for vertex cover](/lp-rounding-vertex-cover/). By [half-integrality](/half-integrality/) a vertex solution has values in $\{0, \frac12, 1\}$, so the rounding only changes the $\frac12$ values.
- **Set cover, $t = 1/f$.** With $f$ the largest number of sets that contain one element, the result is an $f$-approximation. See [frequency rounding for set cover](/frequency-rounding-set-cover/) and [element frequency](/element-frequency/).
- **Hitting set in a $k$-uniform hypergraph, $t = 1/k$.** Each edge has $k$ vertices, so one has value at least $1/k$, and the result is a $k$-approximation. See [hitting set](/hitting-set/).
- **Minimum $s$-$t$ cut, random threshold.** From the LP with edge lengths $d_e \ge 0$ and length at least 1 on each $s$-$t$ path, let $\ell(v)$ be the shortest path distance from $s$. Pick $\theta$ uniformly in $[0, 1)$ and cut the edges that leave $\{v : \ell(v) \le \theta\}$. An edge $(u, v)$ is cut with probability at most $|\ell(u) - \ell(v)| \le d_e$, so the expected cost is at most $\text{LP}^*$, and some threshold gives an integral cut of cost at most $\text{LP}^*$. This is one proof that the LP is exact; see the [max-flow min-cut theorem](/max-flow-min-cut-theorem/).

## Variations

- **Random threshold.** Draw $t$ from a distribution in place of a fixed value. For vertex cover, $t$ uniform in $(0, \frac12]$ gives $\Pr[\hat{x}_v = 1] = \min(1, 2 x^*_v)$, so the expected cost is still at most $2 \text{LP}^*$, and each run is feasible. Random thresholds are the base of rounding for cut and metric problems.
- **Threshold on the dual.** Solve the dual LP and take each set whose dual constraint is tight. Complementary slackness gives the same ratio $f$; see [frequency rounding](/frequency-rounding-set-cover/).
- **Threshold and then repair.** When a threshold leaves some constraints open, add a cheap fix for each one. [Filtering](/filtering-technique/) uses a threshold on distances in this way.
- **Randomized rounding.** Read each value as a probability; see [randomized rounding](/randomized-rounding/). It gives $O(\log n)$ for set cover, which is better than $f$ when $f$ is large.

## Pitfalls

- **General coefficients.** With a constraint $\sum_j a_{ij} x_j \ge b_i$ and $a_{ij} \ne 1$, a variable of large value need not meet the constraint alone. For minimum knapsack the plain LP has unbounded gap, and no threshold helps.
- **A threshold that is too high.** If some constraint has all its values below $t$, the result is not feasible. With $f$ variables per constraint, values $1/f$ each are possible, so $t$ must not be above $1/f$.
- **Ties and floating point.** A value of $0.4999999$ where the exact value is $1/2$ fails the test $x^*_j \ge 1/2$. Use exact arithmetic, or compare with a small tolerance and check feasibility after rounding.
- **The bound is against the LP.** The rounding cannot beat the [integrality gap](/integrality-gap/). For vertex cover on $K_n$, all values are $1/2$, threshold rounding takes all $n$ vertices against $\text{LP}^* = n/2$, and OPT $= n - 1$.

## Exercises

1. For the complete $k$-uniform hypergraph on $n \ge k$ vertices, show that the hitting set LP has the optimum $x_v = 1/k$ with value $n/k$, that threshold rounding with $t = 1/k$ takes all $n$ vertices, and that OPT $= n - k + 1$. Conclude that the ratio $k$ of the rounding is tight against the LP.
2. Show that for vertex cover, $t$ uniform in $(0, \frac12]$ gives a feasible cover on every run with expected weight at most $2 \text{LP}^*$.
3. Prove the claim for the $s$-$t$ cut example: with $\theta$ uniform in $[0, 1)$, the set $\{v : \ell(v) \le \theta\}$ holds $s$ and not $t$, and each edge is cut with probability at most $d_e$.
4. Give a set cover instance with $f = 2$ and an optimal LP solution for which threshold rounding with $t = 1/2$ returns a cover of cost exactly $2 \text{OPT}$.

## References
