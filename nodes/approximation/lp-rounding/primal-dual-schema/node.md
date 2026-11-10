---
tag: WPDFM8
kind: technique
slug: primal-dual-schema
name: Primal-dual schema
aliases:
- primal-dual method
- relaxed complementary slackness
area: approximation/lp-rounding
level: core
summary: Build an integral primal and a feasible dual together; if the two complementary slackness conditions hold up to factors alpha and beta, the primal costs at most alpha beta times the dual.
prereqs: [lp-duality, complementary-slackness, weak-duality, lp-relaxation]
see_also: [primal-dual-approximation, set-cover-primal-dual, primal-dual-weighted-vertex-cover, goemans-williamson-steiner-forest, jain-vazirani-facility-location, dual-fitting, local-ratio-technique, integrality-gap]
sources:
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 15 (set cover via the primal-dual schema; Section 15.1 states the schema and the bound alpha times beta), and Chapters 22 and 24 for Steiner forest and facility location
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 7 (the primal-dual method), Section 7.6 (facility location)
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems
    locator: Chapter 4, by Michel X. Goemans and David P. Williamson (the primal-dual method for approximation algorithms and its application to network design problems)
  - paper: doi:10.1137/S0097539793242618
    title: Michel X. Goemans and David P. Williamson, A general approximation technique for constrained forest problems, SIAM Journal on Computing 24(2), 1995
    locator: pages 296 to 317
  - paper: doi:10.1145/375827.375845
    title: Kamal Jain and Vijay V. Vazirani, Approximation algorithms for metric facility location and k-median problems using the primal-dual schema and Lagrangian relaxation, Journal of the ACM 48(2), 2001
    locator: pages 274 to 296
  - paper: doi:10.1007/BF02523685
    title: Naveen Garg, Vijay V. Vazirani and Mihalis Yannakakis, Primal-dual approximation algorithms for integral flow and multicut in trees, Algorithmica 18(1), 1997
    locator: pages 3 to 20
  - paper: doi:10.1002/nav.3800020109
    title: Harold W. Kuhn, The Hungarian method for the assignment problem, Naval Research Logistics Quarterly 2, 1955
    locator: pages 83 to 97
  - title: George B. Dantzig, Lester R. Ford and Delbert R. Fulkerson, A primal-dual algorithm for linear programs, in Linear Inequalities and Related Systems (H. W. Kuhn and A. W. Tucker, editors), Princeton University Press, 1956
    locator: pages 171 to 181
---

The primal-dual schema is a general way to design approximation algorithms from a pair of [dual](/dual-linear-program/) linear programs. The algorithm keeps an integral primal solution and a feasible dual solution, and it improves both until the primal is feasible. The analysis needs only two inequalities: the [complementary slackness](/complementary-slackness/) conditions, each relaxed by a factor. If the primal conditions hold up to $\alpha$ and the dual conditions up to $\beta$, the primal costs at most $\alpha\beta$ times the dual value, and so at most $\alpha\beta \cdot$ OPT. This page gives the general schema and its theorem; the [primal-dual method](/primal-dual-approximation/) page covers the common special case for covering problems, with $\alpha = 1$.

## In plain words

An optimization problem often comes with a second problem, its dual, whose solutions give lower bounds on the best answer. The schema builds an answer and a bound together, in small steps.

Two simple rules say when an answer and a bound match exactly. The first rule asks that each item that the answer uses is paid for in full by the bound. The second rule asks that each part of the bound that is used is met exactly once by the answer. If both rules hold, the answer is the best one.

The schema asks only that the rules hold roughly: each used item is paid for at least partly, and each used part of the bound is met only a few times. The answer then costs at most a fixed factor more than the bound, and so at most that factor more than the best answer.

## When it applies

**Convention.** The primal LP is a minimization with nonnegative variables, and the dual is its LP dual:

$$\text{(P)} \ \min \sum_{j=1}^{n} c_j x_j \ \text{ s.t. } \sum_{j} a_{ij} x_j \ge b_i \ (i = 1, \ldots, m),\ x \ge 0. \qquad \text{(D)} \ \max \sum_{i=1}^{m} b_i y_i \ \text{ s.t. } \sum_{i} a_{ij} y_i \le c_j \ (j = 1, \ldots, n),\ y \ge 0.$$

The problem is an integer program with this LP as its [relaxation](/lp-relaxation/), so OPT is at least the LP optimum LP*. The ratio convention is ALG $\le \rho \cdot$ OPT.

**Exact complementary slackness.** A feasible $x$ and a feasible $y$ are both optimal if and only if the following hold:

- *primal conditions:* for each $j$, $x_j > 0$ implies $\sum_i a_{ij} y_i = c_j$;
- *dual conditions:* for each $i$, $y_i > 0$ implies $\sum_j a_{ij} x_j = b_i$.

**Relaxed complementary slackness.** Fix $\alpha \ge 1$ and $\beta \ge 1$. The relaxed conditions are

- *primal conditions relaxed by $\alpha$:* for each $j$, $x_j > 0$ implies $c_j / \alpha \le \sum_i a_{ij} y_i \le c_j$;
- *dual conditions relaxed by $\beta$:* for each $i$, $y_i > 0$ implies $b_i \le \sum_j a_{ij} x_j \le \beta b_i$.

The upper bound in the first condition and the lower bound in the second are dual and primal feasibility.

**Theorem (the schema).** Let $x$ be feasible for (P) and $y$ feasible for (D), and let them satisfy the primal conditions relaxed by $\alpha$ and the dual conditions relaxed by $\beta$. Then

$$\sum_j c_j x_j \le \alpha \beta \sum_i b_i y_i \le \alpha \beta \cdot \text{LP}^*.$$

If $x$ is integral, it is an $\alpha\beta$-approximation: $\sum_j c_j x_j \le \alpha\beta \cdot \text{OPT}$.

*Proof.* Each term with $x_j = 0$ is zero, and for $x_j > 0$ the primal condition gives $c_j \le \alpha \sum_i a_{ij} y_i$. So, with $x \ge 0$,

$$\sum_j c_j x_j \le \alpha \sum_j \Big( \sum_i a_{ij} y_i \Big) x_j = \alpha \sum_i \Big( \sum_j a_{ij} x_j \Big) y_i.$$

The middle step only exchanges the order of summation. Each term with $y_i = 0$ is zero, and for $y_i > 0$ the dual condition gives $\sum_j a_{ij} x_j \le \beta b_i$. So, with $y \ge 0$, the right side is at most $\alpha \beta \sum_i b_i y_i$. [Weak duality](/weak-duality/) gives $\sum_i b_i y_i \le \text{LP}^*$, and LP* $\le$ OPT because each integral solution is feasible for (P). $\square$

With $\alpha = \beta = 1$ the proof shows $c \cdot x \le b \cdot y$, so both are optimal. This is the easy direction of the exact theorem. The bound $\alpha\beta \cdot \text{LP}^*$ cannot beat the [integrality gap](/integrality-gap/) of (P): if the gap is $g$, then each analysis of this kind has $\alpha\beta \ge g$.

**An averaged form.** The proof uses the dual conditions only through the sum $\sum_i y_i \sum_j a_{ij} x_j \le \beta \sum_i b_i y_i$. It is enough that this sum inequality holds, even if some single constraint has $\sum_j a_{ij} x_j > \beta b_i$. The Steiner forest algorithm needs this form, and it proves the sum bound one phase of the dual growth at a time.

Use the schema when:

- the problem has an integer program whose LP relaxation and dual have a clear meaning, such as cuts and the paths that cross them, or clients and the facilities that serve them;
- you want a combinatorial algorithm that never solves the LP, and that returns a lower bound with each answer;
- an LP solution is too costly, for example when (P) has exponentially many constraints, but a violated constraint is easy to find.

## The template

The input is the data $(A, b, c)$ of (P) and (D), often given implicitly. The output is an integral feasible $x$ and a feasible $y$.

```pseudo id=main
PRIMAL-DUAL-SCHEMA(A, b, c)
L1  x ← 0;  y ← 0
L2  while x is not feasible for (P) do
L3      V ← a nonempty set of primal constraints that x violates
L4      raise y_i for all i ∈ V, at rates fixed by the design, until some dual constraint j goes tight
L5      raise x_j for the tight j to the next integer value
L6  x ← CLEANUP(x), for example reverse delete;  adjust y if the design asks for it
L7  return x, y
```

Line L4 keeps $y$ feasible for (D), because it stops at the first tight dual constraint. Line L5 raises only a variable whose dual constraint is tight, so the primal conditions hold with $\alpha = 1$. The factor $\beta$ is the hard part: it bounds how often the final $x$ meets each constraint that got dual money, and it comes from the structure of the problem and from line L6. A design with $\alpha > 1$ lets line L5 raise some $x_j$ whose dual constraint is only nearly tight, or lets line L6 connect clients along a path of tight edges, as in the facility location algorithm below.

There are two common choices for line L3. One violated constraint at a time gives simple algorithms with a local bound, as for set cover. All minimal violated constraints at once, raised at the same rate, is the key idea for network design: the bound $\beta$ then holds on average over the constraints raised in one step, which is all that the averaged form needs.

## Classic examples

| problem | (P) has a row for each | $\alpha$ | $\beta$ | ratio |
|---|---|---|---|---|
| [Shortest path](/shortest-path/), as [Dijkstra's algorithm](/dijkstra/) | $s$-$t$ cut | 1 | 1 | 1 (exact) |
| [Assignment problem](/assignment-problem/), as the [Hungarian algorithm](/hungarian-algorithm/) (Kuhn 1955) | worker and job | 1 | 1 | 1 (exact) |
| [Set cover](/set-cover-primal-dual/) with frequency $f$ | element | 1 | $f$ | $f$ |
| [Weighted vertex cover](/primal-dual-weighted-vertex-cover/) | edge | 1 | 2 | 2 |
| [Multicut in trees](/multicut-problem/) (Garg, Vazirani and Yannakakis 1997) | path of a terminal pair | 1 | 2 | 2 |
| [Steiner forest](/goemans-williamson-steiner-forest/) (Goemans and Williamson 1995) | cut that separates a pair | 1 | 2, on average | $2 - 2/k$ |
| [Metric facility location](/jain-vazirani-facility-location/) (Jain and Vazirani 2001) | client and client-facility pair | 3 | 1 | 3 |

The exact algorithms of the first two rows are older than the approximation schema. The primal-dual algorithm of Dantzig, Ford and Fulkerson (1956) for general LPs follows the same plan with $\alpha = \beta = 1$. For facility location, the dual conditions hold exactly, because each client is connected to exactly one open facility. The primal conditions hold exactly for the clients that are connected to a facility they paid for, and up to $\alpha = 3$ for the other clients, whose connection cost is at most three times their dual.

## Variations

- **Averaged slackness.** As above, the dual conditions may hold only in sum over the constraints raised in one step. This is the form behind the factor 2 for Steiner forest and for many [constrained forest problems](/goemans-williamson-steiner-forest/).
- **Lagrangian preserving bounds.** The facility location algorithm proves the stronger bound $C + 3F \le 3 \sum_j \alpha_j$, with connection cost $C$ and facility cost $F$. This form survives the [Lagrangian relaxation](/lagrangian-relaxation/) of a side constraint, and it gives the ratio 6 for [k-median](/k-median-problem/).
- **Dual fitting.** A greedy algorithm builds a dual that is not feasible, and the analysis scales it down by a factor until it is feasible. This is [dual fitting](/dual-fitting/); it fits the same theorem with $y$ replaced by the scaled dual.
- **Local ratio.** The [local ratio technique](/local-ratio-technique/) describes many of the same algorithms without LPs. Each raise of a dual variable is a weight function that is subtracted from the costs.
- **LP rounding with a dual.** Some algorithms solve the LP first and then use exact complementary slackness of the optimal pair to analyze a rounding; this is the *dual rounding* view of [set cover](/set-cover/) by Hochbaum (1982).

## Pitfalls

- **The integrality gap.** The ratio $\alpha\beta$ is a bound against the LP, so it is at least the integrality gap. A weak LP gives a weak schema, whatever the design of the dual growth.
- **Raising a satisfied constraint.** If line L4 raises $y_i$ for a constraint that $x$ already meets, the final $x$ can meet that constraint many times, and $\beta$ grows. Raise only violated constraints.
- **Forgetting cleanup.** For Steiner forest, the bound $\beta = 2$ on average holds only for the forest after reverse delete. Without line L6, the ratio can be as large as the number of terminals.
- **Dual feasibility after cleanup.** Line L6 removes primal variables, which can only help the dual conditions, but a design that changes $y$ there must check that $y$ stays feasible.
- **Reading $\beta$ as a constant per constraint.** For averaged designs, a single constraint can have $\sum_j a_{ij} x_j$ much larger than $\beta b_i$. The proof must use the sum, phase by phase.

## Exercises

1. Show the converse of the easy direction: if $x$ and $y$ are optimal for (P) and (D), then the exact conditions hold. *Answer:* by [strong duality](/strong-duality/), $c \cdot x = b \cdot y$, so the chain in the proof with $\alpha = \beta = 1$ holds with equality. Each step is a sum of nonnegative terms $(c_j - \sum_i a_{ij} y_i) x_j \ge 0$ and $(\sum_j a_{ij} x_j - b_i) y_i \ge 0$, so each term is zero.
2. State $\alpha$ and $\beta$ for the primal-dual vertex cover algorithm and prove the ratio 2 from the theorem. *Answer:* a vertex is taken only when it is tight, so $\alpha = 1$; an edge meets at most its two ends, so $\sum_{v \in e} x_v \le 2 = 2 b_e$ and $\beta = 2$.
3. Run the template on shortest $s$-$t$ path: the rows are the sets $S$ with $s \in S$ and $t \notin S$, line L3 takes the set $S$ of vertices that the tight edges join to $s$, and line L6 keeps only the $s$-$t$ path in the tight edges. Show that $\beta = 1$. *Answer:* each raised set $S$ is joined to $s$ by tight edges, so the final path, which is the path from $s$ in a tree of tight edges, leaves $S$ once and never comes back. So the path crosses each raised cut exactly once, $\beta = 1$, and the path is a shortest path. The sets are the balls of Dijkstra's algorithm.
4. Give an LP where a valid primal-dual pair with $\alpha = 1$ and $\beta = 2$ has cost exactly twice the dual. *Answer:* vertex cover on one edge $uv$ with unit weights: raise $y_{uv}$ to 1, take both $u$ and $v$. The cost is 2 and the dual value 1.

## References
