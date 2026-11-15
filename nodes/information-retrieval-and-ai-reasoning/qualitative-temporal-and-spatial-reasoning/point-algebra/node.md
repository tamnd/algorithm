---
tag: 2B6WT4
kind: model
slug: point-algebra
name: Point algebra
aliases:
- qualitative point algebra
- time point algebra
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: advanced
summary: The qualitative calculus of time points with the base relations <, = and >; its 8 relations include not-equal, and every network over it is decided in polynomial time.
prereqs: [qualitative-constraint-calculus]
see_also: [point-algebra-consistency, composition-table, allens-interval-algebra, ord-horn-subclass, simple-temporal-problem, algebraic-closure, total-order, cardinal-direction-calculus]
sources:
  - paper: "Marc Vilain and Henry Kautz, Constraint propagation algorithms for temporal reasoning, Proceedings of AAAI-86, 1986, pages 377 to 382"
    locator: the point algebra, polynomial propagation for it, and the translation of some interval relations to endpoints
  - paper: doi:10.1016/b978-1-4832-1447-4.50034-1
    title: Marc Vilain, Henry Kautz and Peter van Beek, Constraint propagation algorithms for temporal reasoning, a revised report, in Readings in Qualitative Reasoning about Physical Systems, Morgan Kaufmann, 1990
    locator: pages 373 to 381 (the corrected treatment of the point algebra and its propagation)
  - paper: doi:10.1016/0004-3702(92)90011-L
    title: Peter van Beek, Reasoning about qualitative temporal information, Artificial Intelligence 58(1-3), 1992
    locator: pages 297 to 326 (consistent scenarios in O(n^2) time, minimal labels in O(n^4) time, and the role of the not-equal relation)
  - paper: doi:10.1145/176584.176585
    title: Peter B. Ladkin and Roger D. Maddux, On binary constraint problems, Journal of the ACM 41(3), 1994
    locator: pages 435 to 469 (path consistency decides consistency of point algebra networks)
  - book: isbn:978-1-84821-252-7
    title: Gérard Ligozat, Qualitative Spatial and Temporal Reasoning, ISTE and Wiley, 2011
    locator: Chapter 1 (the point calculus and its relation to the interval calculus)
---

The point algebra is the simplest [qualitative constraint calculus](/qualitative-constraint-calculus/): its objects are points on a time line, and the only thing it can say about two points is whether the first is before, equal to or after the second, or a union of these. It is a model of computation in the sense that it fixes what a reasoning problem may state and what an algorithm may ask: every question is about the order of finitely many unknown points, and the answers do not depend on any numbers. Vilain and Kautz introduced it in 1986 as the tractable counterpart of [Allen's interval algebra](/allens-interval-algebra/): unlike intervals, point networks are decided in polynomial time, and the exact algorithm is on the page [point algebra consistency](/point-algebra-consistency/).

## The machine

The domain is a dense linear order without endpoints, usually $\mathbb{R}$ or $\mathbb{Q}$; for every question below, the integers give the same answers. There are 3 base relations, $<$, $=$ and $>$, and $2^3 = 8$ relations:

| relation | set | meaning |
|---|---|---|
| $\emptyset$ | $\{\}$ | impossible |
| $<$, $=$, $>$ | one base relation | known order |
| $\le$ | $\{<, =\}$ | not after |
| $\ge$ | $\{=, >\}$ | not before |
| $\ne$ | $\{<, >\}$ | different |
| ? | $\{<, =, >\}$ | no information |

The converse swaps $<$ and $>$. The [composition table](/composition-table/) is

| $\diamond$ | $<$ | $=$ | $>$ |
|---|---|---|---|
| $<$ | $<$ | $<$ | ? |
| $=$ | $<$ | $=$ | $>$ |
| $>$ | ? | $>$ | $>$ |

and it is strong, so the relations form a relation algebra. An input is a [qualitative constraint network](/qualitative-constraint-network/) on $n$ points with one of the 8 relations on each pair. The subclass without $\ne$, the 7 relations $\emptyset$, $<$, $\le$, $=$, $\ge$, $>$ and ?, is called the *convex point algebra*.

## What it counts

The cost of a reasoning algorithm is measured in the number of points $n$, and sometimes in the number $e \le \binom{n}{2}$ of pairs with a label other than ?. The standard problems are:

- **consistency:** is there an assignment of numbers that satisfies every label?
- **a solution:** an assignment, or a *consistent scenario*, the base relation of each pair under some solution;
- **minimal labels:** for each pair, the set of base relations that occur in some solution;
- **incremental versions:** the same answers after each new constraint.

## Relation to other models

- **Intervals.** An interval $(x^-, x^+)$ is two points with $x^- < x^+$, and each of the 13 base relations of [Allen's interval algebra](/allens-interval-algebra/) is a conjunction of point relations between the 4 endpoints. An interval relation is *pointisable* when it is a conjunction of point algebra relations on the endpoints; there are 188 pointisable relations, counting the empty one. Networks of them reduce to point networks on $2n$ points. The [ORD-Horn subclass](/ord-horn-subclass/) allows disjunctions of $\ne$ with one order literal on the endpoints, and is larger.
- **Metric time.** The [simple temporal problem](/simple-temporal-problem/) adds numeric bounds $a \le x_j - x_i \le b$. It covers the convex point algebra (with strict bounds for $<$), but not $\ne$.
- **Plane.** The [cardinal direction calculus](/cardinal-direction-calculus/) for points uses one point relation per axis, $3 \times 3 = 9$ base relations.
- **Orders.** A consistent scenario is a [total order](/total-order/) with ties on the points; a network of $\le$ and $<$ alone is a directed graph, and its consistency is "no cycle through a strict edge".

## Known results in the model

| problem | result | source |
|---|---|---|
| consistency and a solution, all 8 relations | $O(n^2)$, by strongly connected components | van Beek 1992 |
| consistency, all 8 relations | path consistency decides it, $O(n^3)$ | Ladkin and Maddux 1994 |
| minimal labels, convex point algebra | path consistency gives them, $O(n^3)$ | Vilain, Kautz and van Beek 1990 |
| minimal labels, all 8 relations | $O(n^4)$; path consistency is not enough | van Beek 1992 |

**Every network is decided.** Unlike the interval algebra, where consistency is NP-complete ([NP-completeness of the interval algebra](/interval-algebra-np-completeness/)), all 8 relations together form a tractable class. A consistent network on $n$ points always has a solution with integer values in $0, \ldots, n-1$, since only the order matters.

**Why $\ne$ is harder.** The network $x_0 \le x_1$, $x_0 \le x_2$, $x_1 \le x_3$, $x_2 \le x_3$, $x_1 \ne x_2$ is path consistent with the label $\le$ on $(x_0, x_3)$, but $x_0 = x_3$ would force $x_1 = x_2$, so the minimal label is $<$. Path consistency looks at three points at a time, and this reason involves all four.

## References
