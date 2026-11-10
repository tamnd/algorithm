---
tag: VJB6HH
kind: problem
slug: set-cover
name: Set cover problem
aliases:
- minimum set cover
- weighted set cover
- set covering problem
area: approximation/covering-and-packing
level: core
summary: Choose the fewest sets, or the sets of least total cost, whose union covers the universe.
prereqs: [np-hard, linear-programming-problem, lp-relaxation, approximation-ratio]
see_also: [greedy-set-cover, set-cover-primal-dual, element-frequency, hitting-set, max-coverage, vertex-cover, dominating-set, set-cover-inapproximability]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 35, Section 35.3 (the set-covering problem)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 1, Sections 1.2 to 1.7 (set cover as the running example of the main techniques)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 2 (set cover, greedy and layering), Chapters 13 to 15 (dual fitting, rounding, primal-dual)
  - paper: doi:10.1016/S0022-0000(74)80044-9
    title: David S. Johnson, Approximation algorithms for combinatorial problems, Journal of Computer and System Sciences 9(3), 1974
    locator: pages 256 to 278
  - paper: doi:10.1016/0012-365X(75)90058-8
    title: László Lovász, On the ratio of optimal integral and fractional covers, Discrete Mathematics 13(4), 1975
    locator: pages 383 to 390
  - paper: doi:10.1137/0211045
    title: Dorit S. Hochbaum, Approximation algorithms for the set covering and vertex cover problems, SIAM Journal on Computing 11(3), 1982
    locator: pages 555 to 556
  - paper: doi:10.1016/0196-6774(81)90020-1
    title: Reuven Bar-Yehuda and Shimon Even, A linear-time approximation algorithm for the weighted vertex cover problem, Journal of Algorithms 2(2), 1981
    locator: pages 198 to 203
  - paper: doi:10.1137/S0097539704443057
    title: Irit Dinur, Venkatesan Guruswami, Subhash Khot and Oded Regev, A new multilayered PCP and the hardness of hypergraph vertex cover, SIAM Journal on Computing 34(5), 2005
    locator: pages 1129 to 1146
  - paper: doi:10.1016/j.jcss.2007.06.019
    title: Subhash Khot and Oded Regev, Vertex cover might be hard to approximate to within 2 − ε, Journal of Computer and System Sciences 74(3), 2008
    locator: pages 335 to 349
  - paper: doi:10.1287/moor.4.3.233
    title: Vašek Chvátal, A greedy heuristic for the set-covering problem, Mathematics of Operations Research 4(3), 1979
    locator: pages 233 to 235
  - paper: doi:10.1145/285055.285059
    title: Uriel Feige, A threshold of ln n for approximating set cover, Journal of the ACM 45(4), 1998
    locator: pages 634 to 652
  - paper: doi:10.1145/2591796.2591884
    title: Irit Dinur and David Steurer, Analytical approach to parallel repetition, STOC 2014
    locator: the corollary on set cover
---

The set cover problem gives a universe of elements and a family of subsets with costs, and asks for a subfamily of least total cost whose union is the whole universe. It is [NP-hard](/np-hard/), and it is the standard example of a problem with a logarithmic [approximation ratio](/approximation-ratio/): the [greedy algorithm](/greedy-set-cover/) is within a factor $H_n \le \ln n + 1$ of the optimum, and no polynomial-time algorithm does better than $(1 - \varepsilon) \ln n$ unless P = NP. Many covering problems, such as [vertex cover](/vertex-cover/), [dominating set](/dominating-set/) and [hitting set](/hitting-set/), are special cases or equivalent forms of it.

## In plain words

You must hire a team that knows a list of skills. Each candidate knows some of the skills and asks for a salary. You want every skill to be known by at least one person in the team, and you want to pay as little as possible.

There is no fast method known that always finds the cheapest team, and most experts believe that none exists. But a simple rule works well: hire the candidate who costs the least for each new skill they bring, and repeat. The team you get never costs more than a small factor above the best team. The factor grows only very slowly with the number of skills, and for large lists no fast method can promise a much smaller factor.

## Definition

**Notation.** On this page $n$ is the number of elements and $m$ is the number of sets. OPT is the cost of an optimal cover, and ALG is the cost of the cover that an algorithm returns. Set cover is a minimization problem, so a $\rho$-approximation returns a cover with ALG $\le \rho \cdot$ OPT, with $\rho \ge 1$, on each instance.

**Input.** A finite universe $U$ with $|U| = n$, a family $\mathcal{S} = \{S_1, \ldots, S_m\}$ of subsets of $U$, and a cost $c_j \ge 0$ for each set $S_j$. The family must cover $U$: $S_1 \cup \cdots \cup S_m = U$. In the unweighted version, each $c_j = 1$.

**Output.** A set of indices $C \subseteq \{1, \ldots, m\}$ such that

$$\bigcup_{j \in C} S_j = U,$$

and the cost $c(C) = \sum_{j \in C} c_j$ is as small as possible.

**Integer program.** With a 0-1 variable $x_j$ for each set, set cover is the [integer program](/binary-integer-programming/)

$$\text{minimize } \sum_{j=1}^m c_j x_j \quad \text{subject to} \quad \sum_{j : e \in S_j} x_j \ge 1 \text{ for each } e \in U, \qquad x_j \in \{0, 1\}.$$

The [LP relaxation](/lp-relaxation/) replaces $x_j \in \{0, 1\}$ by $x_j \ge 0$. Its optimum LP* is a lower bound: LP* $\le$ OPT. The [dual linear program](/dual-linear-program/) has a variable $y_e \ge 0$ for each element:

$$\text{maximize } \sum_{e \in U} y_e \quad \text{subject to} \quad \sum_{e \in S_j} y_e \le c_j \text{ for each } j.$$

By [weak duality](/weak-duality/), each feasible $y$ has $\sum_e y_e \le$ LP* $\le$ OPT. Most analyses of set cover algorithms compare ALG with LP* or with such a dual solution.

**Two parameters.** Let $d = \max_j |S_j|$ be the size of the largest set, and let $f$ be the largest number of sets that contain one element, the [element frequency](/element-frequency/). The two known ratios are $H_d$ and $f$, where $H_d = 1 + 1/2 + \cdots + 1/d$ is the [harmonic number](/harmonic-series/).

## Variants

- **Decision version.** Given $U$, $\mathcal{S}$ and an integer $k$, is there a cover with at most $k$ sets? It is one of [Karp's 21 NP-complete problems](/karps-21-np-complete-problems/).
- **Unweighted and weighted.** The greedy ratio and the hardness bounds are the same for both.
- **Bounded set size.** If each set has at most $d$ elements, greedy gives $H_d$. For $d = 2$ and unit costs, the 2-element sets are the edges of a graph, and an optimal cover is a maximum [matching](/maximum-matching/) of this graph plus one set for each element that the matching misses, as for the [minimum edge cover](/minimum-edge-cover/). So this case is in P. For $d = 3$ the problem is NP-hard, because [exact cover by 3-sets](/exact-cover-by-3-sets/) is a special case: $3q$ elements have a cover by $q$ sets of size 3 only if the sets are disjoint.
- **Bounded frequency.** If each element is in at most $f$ sets, LP rounding and the primal-dual method give $f$. For $f = 2$ the problem is weighted [vertex cover](/vertex-cover/).
- **Partial cover.** Cover at least a given number of elements at least cost. The budgeted dual of this is [maximum coverage](/max-coverage/).
- **Multicover.** Element $e$ must be covered $r_e$ times. This is a [covering integer program](/covering-integer-program/).
- **Set partitioning.** Each element must be covered exactly once. The packing counterpart, with disjoint sets of greatest total value, is [set packing](/set-packing/).
- **Online set cover.** The elements arrive one by one, and a chosen set cannot be dropped. See [online set cover](/online-set-cover-problem/).

## Examples

**A weighted instance.** Let $U = \{1, \ldots, 7\}$ and

| set | elements | cost |
|---|---|---|
| $S_1$ | 1, 2, 3, 5 | 3 |
| $S_2$ | 3, 4, 6, 7 | 4 |
| $S_3$ | 2, 5, 6 | 4 |
| $S_4$ | 3, 7 | 2 |
| $S_5$ | 1, 2, 4, 7 | 1 |

The optimal cover is $\{S_1, S_2\}$, with OPT $= 7$. No cover costs less: a cover must contain a set with element 6, so $S_2$ or $S_3$. With $S_3$ (cost 4), the elements 3 and 4 still need covering, and the cheapest way is $S_5$ plus $S_4$ or $S_1$, for a total of at least 7. With $S_2$ (cost 4), the elements 1, 2 and 5 still need covering, and only $S_1$ or $S_3$ covers 5, so the total is again at least 7. The LP optimum is LP* $= 6$, at $x_1 = x_2 = x_3 = x_5 = 1/2$ and $x_4 = 0$: each element is in exactly two of these four sets. So this instance has a gap between the LP and the integer optimum. The [greedy algorithm](/greedy-set-cover/) picks $S_5$, $S_1$, $S_2$ and pays 8. The largest set has $d = 4$ elements, and the largest frequency is $f = 3$.

**An integrality gap.** Fix $k \ge 2$. Let $U$ be the $n = 2^k - 1$ non-zero vectors of $\{0,1\}^k$, and for each non-zero $v$ let $S_v = \{u : u \cdot v \equiv 1 \pmod 2\}$, with cost 1. Each set has $2^{k-1}$ elements, and each element is in $2^{k-1}$ sets. Putting $x_v = 1/2^{k-1}$ on each set is feasible, and putting $y_u = 1/2^{k-1}$ on each element is dual feasible, so LP* $= (2^k - 1)/2^{k-1} < 2$. But OPT $= k$. If fewer than $k$ sets $S_{v_1}, \ldots, S_{v_t}$ are chosen, then some non-zero $u$ has $u \cdot v_i = 0$ for each $i$, because $t < k$ linear equations over the field with two elements have a non-zero solution, so $u$ is not covered. The $k$ unit vectors give a cover. For $k = 3$ this is the Fano plane: LP* $= 7/4$ and OPT $= 3$. So the ratio OPT/LP* is at least $k/2 = \Omega(\log n)$, and no algorithm that compares only with LP* can prove a constant ratio.

## Known algorithms

| algorithm | ratio | lower bound used |
|---|---|---|
| [Greedy set cover](/greedy-set-cover/) | $H_d \le \ln n + 1$ | a dual solution (dual fitting) |
| [Primal-dual f-approximation](/set-cover-primal-dual/) | $f$ | a dual solution built by the algorithm |
| [Frequency rounding](/frequency-rounding-set-cover/) | $f$ | LP* |
| [LP rounding for set cover](/lp-rounding-set-cover/) | $f$, or $O(\log n)$ with [randomized rounding](/randomized-rounding/) | LP* |
| Exact dynamic programming over subsets of $U$ | 1, in $O(2^n m n)$ time | none |

All ratios hold in the worst case. The LP methods solve the LP in polynomial time with the ellipsoid method or an interior point method. The LP has one row for each element, so no separation oracle is needed.

## Bounds

- **Upper bound.** Greedy gives $H_d$. Johnson (1974) and Lovász (1975) proved this for unit costs, and Chvátal (1979) for arbitrary costs. The analysis is tight for greedy: the [greedy page](/greedy-set-cover/) gives a weighted family with ratio exactly $H_n/(1 + \varepsilon)$.
- **A second upper bound.** The $f$-approximation of Hochbaum (1982) and of Bar-Yehuda and Even (1981) is better when each element is in few sets.
- **Hardness in $n$.** For each $\varepsilon > 0$, no polynomial-time $(1 - \varepsilon)\ln n$ approximation exists unless P = NP (Dinur and Steurer 2014). Feige (1998) proved the same threshold under the stronger assumption NP $\not\subseteq$ DTIME$(n^{O(\log \log n)})$. See [set cover inapproximability](/set-cover-inapproximability/).
- **Hardness in $f$.** For each fixed $f \ge 3$, the problem is NP-hard to approximate within $f - 1 - \varepsilon$ (Dinur, Guruswami, Khot and Regev 2005), and within $f - \varepsilon$ under the [Unique Games Conjecture](/unique-games-conjecture/) (Khot and Regev 2008).
- **Exact time.** The subset dynamic program takes $O^*(2^n)$ time. The [set cover conjecture](/set-cover-conjecture/) says that no $O^*((2 - \varepsilon)^n)$ algorithm exists for unbounded set sizes.

So the greedy ratio $\ln n + O(1)$ is the best possible up to the lower-order term, under P $\ne$ NP.

## Reductions

- **From vertex cover.** A graph $G = (V, E)$ gives the instance with $U = E$ and one set $S_v$ of the edges at $v$ for each vertex. A cover of $U$ is a vertex cover, at the same cost. Here $f = 2$.
- **To and from hitting set.** Exchange the roles of elements and sets. The [hitting set](/hitting-set/) page proves that the two problems are the same, with $d$ and $f$ exchanged.
- **To and from dominating set.** A graph gives a set cover instance with the closed neighbourhoods $N[v]$ as the sets. The other direction builds a graph from a set system. Both maps keep the cost, so the $\ln n$ bounds carry over to [dominating set](/dominating-set/).
- **To maximum coverage.** A cover with $k$ sets exists if and only if the [maximum coverage](/max-coverage/) optimum with budget $k$ is $n$. The hardness of maximum coverage comes from the same reduction as the hardness of set cover.

## Applications

- Choosing a smallest set of tests that exercises each requirement or each line of code.
- Placing facilities, sensors or fire stations so that each customer or area is within reach of one of them.
- Crew scheduling in airlines, where each flight leg must be covered by a crew pairing; this is usually solved as set partitioning with integer programming.
- Choosing a small set of features, probes or signatures that separates or detects all cases, as in virus signature selection.
- As a subroutine in other approximation algorithms, for example for the shortest common superstring (Vazirani, Section 2.3).

## References
