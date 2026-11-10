---
tag: 24X7Z1
kind: algorithm
slug: set-cover-primal-dual
name: Primal-dual f-approximation for set cover
aliases:
- f-approximation for set cover
- Bar-Yehuda and Even set cover algorithm
area: approximation/covering-and-packing
level: advanced
summary: Raise the dual variable of each uncovered element until a set becomes tight, and take all tight sets; the cover costs at most f times the optimum, where f is the largest element frequency.
solves: [set-cover]
model: word-ram
complexity:
  vars: {n: the number of elements, m: the number of sets, s: the total size of all sets}
  time: {worst: Θ(n + m + s)}
  space: {extra: Θ(n + m + s)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1981
  people: [Reuven Bar-Yehuda, Shimon Even]
  note: Bar-Yehuda and Even gave this linear-time f-approximation for weighted set cover in 1981; Hochbaum (1982) reached the ratio f by LP rounding at about the same time.
prereqs: [set-cover, element-frequency, dual-linear-program, weak-duality, complementary-slackness]
see_also: [primal-dual-approximation, primal-dual-schema, primal-dual-weighted-vertex-cover, frequency-rounding-set-cover, greedy-set-cover, local-ratio-technique, set-cover-inapproximability]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 1, Section 1.5 (a primal-dual algorithm for set cover with ratio f)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 15 (set cover via the primal-dual schema, with a tight example)
  - paper: doi:10.1016/0196-6774(81)90020-1
    title: Reuven Bar-Yehuda and Shimon Even, A linear-time approximation algorithm for the weighted vertex cover problem, Journal of Algorithms 2(2), 1981
    locator: pages 198 to 203
  - paper: doi:10.1137/0211045
    title: Dorit S. Hochbaum, Approximation algorithms for the set covering and vertex cover problems, SIAM Journal on Computing 11(3), 1982
    locator: pages 555 to 556
  - paper: doi:10.1137/S0097539704443057
    title: Irit Dinur, Venkatesan Guruswami, Subhash Khot and Oded Regev, A new multilayered PCP and the hardness of hypergraph vertex cover, SIAM Journal on Computing 34(5), 2005
    locator: pages 1129 to 1146 (f − 1 − ε is NP-hard for each f ≥ 3)
  - paper: doi:10.1016/j.jcss.2007.06.019
    title: Subhash Khot and Oded Regev, Vertex cover might be hard to approximate to within 2 − ε, Journal of Computer and System Sciences 74(3), 2008
    locator: pages 335 to 349 (f − ε is hard under the Unique Games Conjecture)
---

The primal-dual algorithm for [set cover](/set-cover/) visits the elements one by one. For each element that is not yet covered, it raises the dual variable of that element until some set that contains it is paid for in full, and it puts each fully paid set into the cover. The cover costs at most $f \cdot$ OPT, where $f$ is the [element frequency](/element-frequency/), the largest number of sets that contain one element. It runs in linear time and never solves an LP. For $f = 2$ it is the [primal-dual algorithm for weighted vertex cover](/primal-dual-weighted-vertex-cover/). It is the simplest example of the [primal-dual method](/primal-dual-approximation/).

## In plain words

You must cover a list of items with groups, and each group has a price. Each item can put money toward the groups that hold it. Take the items in a fixed order. When an item is not yet covered, it puts the same amount of money into each of its groups, as much as it can until one of its groups is paid in full. Each group that is paid in full is bought.

Each bought group is paid only with money from its own items. An item gives money to at most as many groups as hold it. And the total money is at most the price of the best solution, because the best solution must buy a group for each item. So the total price of the bought groups is at most this number of groups times the best price.

## The problem

The input is a universe $U$ of $n$ elements, $m$ sets $S_1, \ldots, S_m \subseteq U$ with costs $c_j \ge 0$, and the union of the sets is $U$. The output is a set $C$ of indices with $\bigcup_{j \in C} S_j = U$, of small cost $c(C) = \sum_{j \in C} c_j$. The frequency of $e$ is $f_e = |\{ j : e \in S_j \}|$, and $f = \max_e f_e$. The algorithm uses the [dual](/dual-linear-program/) of the LP relaxation:

$$\max \sum_{e \in U} y_e \quad \text{subject to} \quad \sum_{e \in S_j} y_e \le c_j \text{ for each } j, \qquad y \ge 0.$$

A set $j$ is *tight* when its constraint holds with equality. OPT is the least cost of a cover, LP* is the optimum of the LP, and the ratio convention is ALG $\le \rho \cdot$ OPT.

## The algorithm

```pseudo id=main
PRIMAL-DUAL-SET-COVER(U, S[1 .. m], c[1 .. m])
L1  y[e] ← 0 for each e in U, C ← empty list
L2  for each e in U, in a fixed order do
L3      if some set in C contains e then continue
L4      δ ← min over j with e ∈ S[j] of (c[j] − Σ_{e' ∈ S[j]} y[e'])
L5      y[e] ← δ
L6      append to C each j with e ∈ S[j] that is now tight
L7  return C, y
```

Line L4 computes the largest raise of $y_e$ that keeps $y$ dual feasible: the least residual cost of a set that holds $e$. Line L5 makes at least one such set tight, and line L6 takes all of them. The algorithm never lowers a dual variable and never removes a set. The order in line L2 can be any order; it changes the output but not the bound.

## Example

The instance is the one of the [set cover](/set-cover/) page, with $U = \{1, \ldots, 7\}$, OPT $= 7$ at $\{S_1, S_2\}$, and LP* $= 6$.

| set | elements | cost |
|---|---|---|
| $S_1$ | 1, 2, 3, 5 | 3 |
| $S_2$ | 3, 4, 6, 7 | 4 |
| $S_3$ | 2, 5, 6 | 4 |
| $S_4$ | 3, 7 | 2 |
| $S_5$ | 1, 2, 4, 7 | 1 |

The elements 2, 3 and 7 are in three sets, and the others in two, so $f = 3$. The table shows the residual cost $c_j - \sum_{e \in S_j} y_e$ of each set after each visit that raises a dual variable. The visits to 2, 4, 5 and 7 are skipped by line L3, because the element is already covered.

| visit | $\delta$ | $S_1$ | $S_2$ | $S_3$ | $S_4$ | $S_5$ | added to $C$ |
|---|---|---|---|---|---|---|---|
| start | | 3 | 4 | 4 | 2 | 1 | |
| $e = 1$ | 1 | 2 | 4 | 4 | 2 | 0 | $S_5$ |
| $e = 3$ | 2 | 0 | 2 | 4 | 0 | 0 | $S_1$, $S_4$ |
| $e = 6$ | 2 | 0 | 0 | 2 | 0 | 0 | $S_2$ |

The output is $C = (S_5, S_1, S_4, S_2)$ with cost $1 + 3 + 2 + 4 = 10$, and $y_1 = 1$, $y_3 = 2$, $y_6 = 2$, all other $y_e = 0$. The dual value is $\sum_e y_e = 5 \le$ LP* $= 6$. The bound is $f \sum_e y_e = 15$, and the cost 10 is within it. The finer count of the proof is exact here: $y_1$ is paid to two sets of $C$, $y_3$ to three and $y_6$ to one, and $2 \cdot 1 + 3 \cdot 2 + 1 \cdot 2 = 10$. The cover is not minimal: $S_4$ and $S_5$ are redundant, and without them the cost is 7.

## Correctness

The algorithm keeps two invariants. First, $y$ is dual feasible, because line L4 raises $y_e$ by the least residual cost among the sets that contain $e$, and the raise changes no other set. Second, each set in $C$ is tight, because line L6 adds only tight sets, and a later raise of $y_e$ happens only for an element $e$ that is in no set of $C$. Each element is covered after its visit: either it was covered before, or the set that attains the minimum in line L4 becomes tight and enters $C$.

**Theorem (Bar-Yehuda and Even 1981).** PRIMAL-DUAL-SET-COVER returns a cover of cost at most $f \cdot \text{LP}^* \le f \cdot \text{OPT}$, in the worst case.

The proof pays each set of $C$ with the duals of its elements, because it is tight:

$$c(C) = \sum_{j \in C} \sum_{e \in S_j} y_e = \sum_{e \in U} y_e \, |\{ j \in C : e \in S_j \}| \le f \sum_{e \in U} y_e \le f \cdot \text{LP}^*.$$

The last step is [weak duality](/weak-duality/). In the language of [complementary slackness](/complementary-slackness/), the primal conditions hold exactly (each chosen set is tight) and the dual conditions hold up to the factor $f$ (each element is in at most $f$ chosen sets). The full proof is in the proof file below.

**The lower bound used.** The algorithm compares ALG with the value of the dual solution $y$ that it builds, which is at most LP* $\le$ OPT.

**Tight example.** The ratio $f$ is tight for the algorithm, even with unit costs. Take $f$ disjoint parts of $k$ vertices each. The elements are the $k^f$ tuples with one vertex from each part, and each vertex is a set of cost 1 that holds the tuples that use it. Each element is in exactly $f$ sets, and the $k$ vertices of one part form a cover, so OPT $\le k$. In any visit order, an uncovered tuple uses only vertices not yet in $C$, so its $f$ sets all have residual 1, and all $f$ become tight. Each such visit adds one vertex of each part, and a tuple stays uncovered as long as each part has a vertex not in $C$. So the algorithm takes all $fk$ vertices, and the ratio is $f$.

**Hardness.** The ratio $f$ is close to the best possible. For each fixed $f \ge 3$, an $(f - 1 - \varepsilon)$-approximation is NP-hard (Dinur, Guruswami, Khot and Regev 2005), and under the [Unique Games Conjecture](/unique-games-conjecture/) an $(f - \varepsilon)$-approximation is hard (Khot and Regev 2008). For $f = 2$ see [vertex cover](/vertex-cover/).

## Complexity

Let $s = \sum_j |S_j|$ be the total input size. The implementation keeps the residual cost of each set and a flag for each covered element.

- **Time.** Line L4 reads the residuals of the $f_e$ sets that contain $e$, and line L5 updates them, so a visit costs $O(1 + f_e)$. Line L6 runs at most once for each set, and adding set $j$ marks its $|S_j|$ elements. The total is $\Theta(n + m + s)$ in the worst case, in the [word RAM](/word-ram/) with costs that fit in a word. This is linear in the input size.
- **Space.** The lists of sets for each element, the residuals and the flags take $\Theta(n + m + s)$ extra space.

## Properties

- **Deterministic.** For a fixed visit order, the output depends only on the input.
- **Any visit order.** The bound $f$ holds for each order of line L2.
- **A certificate.** The output $y$ is a feasible dual solution, so $\sum_e y_e$ is a lower bound on OPT that comes with the cover. The ratio $c(C) / \sum_e y_e$ bounds the error of this run, and it is often well below $f$.
- **Output may be redundant.** As in the example, a set can become tight after its elements are covered by other sets.

## Variants and improvements

- **Reverse delete.** After the loop, visit the sets of $C$ in the reverse order of their addition and drop each set that is not needed. The result is a minimal cover, and the bound $f$ still holds because the cost can only fall. On the example it gives $\{S_1, S_2\}$, the optimum. For network design problems, [the primal-dual schema](/primal-dual-schema/) needs this step for its ratio.
- **Uniform raise.** Raise the duals of all uncovered elements at the same rate, and take sets as they become tight. This is the form in many texts. It has the same bound.
- **Local ratio.** The [local ratio technique](/local-ratio-technique/) gives the same algorithm in another language: subtract $\delta$ from the cost of each set that holds $e$, and take the sets of cost zero.
- **LP rounding.** Solve the LP and take each set with $x_j \ge 1/f$. This is [frequency rounding](/frequency-rounding-set-cover/). It has the same ratio but needs an LP solver.
- **Greedy.** The [greedy algorithm](/greedy-set-cover/) has ratio $H_d$, with $d$ the largest set size. It is better when $f$ is large and sets are small.

## When to use it

Use the primal-dual algorithm when each element is in few sets, so $f$ is small, for example $f = 2$ in [vertex cover](/vertex-cover/) and small $f$ in hypergraph vertex cover. It runs in linear time, is easy to implement, and gives a lower bound with each answer. When $f$ is large but sets are small, use the [greedy algorithm](/greedy-set-cover/) instead, or run both and keep the better cover. Add the reverse delete pass: it costs little and often helps a lot.

## Pitfalls

- **Raising a covered element.** Line L3 is needed for the proof that each set of $C$ is tight at the end. If a covered element raises its dual, the sets of $C$ that hold it get a load above their cost, and the dual is no longer feasible.
- **Floating-point residuals.** Exact tightness tests $c_j - \text{load} = 0$ fail with rounding errors. Use integer or rational costs, or compare with a tolerance and then check the cover.
- **Reading $f$ as an average.** The bound uses the largest frequency. One element in many sets makes the bound weak, even if most elements are in two sets. The finer bound $\sum_e f_e y_e$ of the proof can help in such cases.

## Implementations

## History

Bar-Yehuda and Even (1981) gave this algorithm, in linear time, for weighted set cover with ratio $f$, and stated it for weighted vertex cover with ratio 2. At about the same time, Hochbaum (1982) found the ratio $f$ by rounding the LP and its dual. Bar-Yehuda and Even (1985) later described the same idea as the local ratio theorem. The view of the algorithm as a primal-dual method with relaxed complementary slackness is in the books of Vazirani (2001) and Williamson and Shmoys (2011). Dinur, Guruswami, Khot and Regev (2005) and Khot and Regev (2008) showed that the ratio $f$ is close to the best possible.

## References
