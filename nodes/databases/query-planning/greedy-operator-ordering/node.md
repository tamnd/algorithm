---
tag: X0F4M8
kind: algorithm
slug: greedy-operator-ordering
name: Greedy operator ordering
aliases:
- GOO
- greedy join ordering by result size
area: databases/query-planning
level: core
summary: A join ordering heuristic that repeatedly joins the two current subplans whose join has the smallest estimated result.
solves: [join-ordering]
model: word-ram
complexity:
  vars: {n: the number of relations}
  time: {worst: "O(n^3)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: false, greedy: true, recursive: false}
history:
  year: 1998
  people: [Leonidas Fegaras]
  note: Given as a heuristic for large join queries at DEXA 1998.
prereqs: [join-ordering, left-deep-and-bushy-join-trees, greedy-algorithm]
see_also: [dpccp, dphyp, ikkbz-algorithm, selinger-join-enumeration, join-ordering-np-hardness, cardinality-estimation, simulated-annealing, greedy-algorithm]
sources:
  - paper: "Leonidas Fegaras, A new heuristic for optimizing large queries, Proceedings of DEXA 1998, Lecture Notes in Computer Science 1460"
    title: A new heuristic for optimizing large queries
    locator: "the greedy operator ordering heuristic, which joins the pair of subplans with the smallest result size in each step"
  - paper: "Michael Steinbrunn, Guido Moerkotte and Alfons Kemper, Heuristic and randomized optimization for the join ordering problem, The VLDB Journal 6(3) (1997), 191 to 208"
    title: Heuristic and randomized optimization for the join ordering problem
    locator: the comparison of earlier greedy heuristics and randomized methods for large join queries
---

Greedy operator ordering (GOO) is a heuristic for [join ordering](/join-ordering/). It starts with one plan per relation. In each step it looks at every pair of current plans that a join predicate links, estimates the size of their join, and joins the pair with the smallest result. After $n - 1$ steps one bushy plan is left. GOO takes $O(n^3)$ time, so it works for queries with hundreds of relations, where exact dynamic programs such as [DPccp](/dpccp/) are too slow. The price is that the plan may cost more than the optimum. Leonidas Fegaras gave it in 1998.

## In plain words

Joining many tables in a bad order makes huge intermediate results. GOO follows a simple rule: keep the intermediate results small. At the start, every table is its own piece. At each step, look at every two pieces that a join condition connects, guess how many rows their join would give, and join the two pieces with the smallest guess. Repeat until one piece is left.

The rule can join any two pieces, not only a piece and a single table, so the plan can be bushy. The rule is fast, but it only looks one step ahead. A join that is small now can lead to large joins later, so GOO does not always find the best plan.

## The problem

The input is a query graph on relations $R_0, \ldots, R_{n-1}$ with the estimated size of each relation and a selectivity on each edge. The size of a set $S$ of relations is the product of the sizes of its relations and of the selectivities of the edges inside $S$. Two sets are *linked* if an edge has one end in each. The cost of a plan is $C_{out}$, the sum of the sizes of its joins. GOO does not solve this problem exactly; it builds some bushy plan without cross products, quickly, and tries to keep the cost low.

## The algorithm

```pseudo id=main
GOO(relations R_0, ..., R_(n-1), sizes, selectivities)
L1  T ← {R_0, ..., R_(n-1)}
L2  while T has two or more trees do
L3      among the pairs {T_i, T_j} of trees in T that an edge links (all pairs if none is linked), choose one with the smallest |T_i ⋈ T_j|
L4      T ← T - {T_i, T_j} ∪ {T_i ⋈ T_j}
L5      |T_i ⋈ T_j| ← |T_i| · |T_j| · (the product of the selectivities of the edges between T_i and T_j)
L6  return the one tree in T
```

The code stores the size of each tree and, for each pair of trees, the product of the selectivities between them. When two trees join, the value between the new tree and another tree $T_k$ is the product of the values of the two old trees with $T_k$. Each size then costs $O(1)$ to compute. The code puts the larger input on the left of each join, so that a hash join that builds on the right input builds on the smaller one. It uses a cross product only when no two trees are linked, which happens only when the query graph is not connected.

## Example

The chain $A$-$B$-$C$-$D$ has relations of 20, 10, 1000 and 20 tuples and the selectivities 1/5 on $A$-$B$, 1/100 on $B$-$C$ and 1/100 on $C$-$D$.

| step | candidate joins and their sizes | chosen |
|---|---|---|
| 1 | $A \bowtie B$: 40, $B \bowtie C$: 100, $C \bowtie D$: 200 | $A \bowtie B$, 40 |
| 2 | $(AB) \bowtie C$: 400, $C \bowtie D$: 200 | $C \bowtie D$, 200 |
| 3 | $(AB) \bowtie (CD)$: 80 | 80 |

GOO returns $(C \bowtie D) \bowtie (A \bowtie B)$ with cost $40 + 200 + 80 = 320$. The optimal plan is $A \bowtie ((B \bowtie C) \bowtie D)$, with cost $100 + 20 + 80 = 200$: it starts with a larger join, $B \bowtie C$ with 100 tuples, but then $D$ cuts the result to 20 tuples. GOO took the smallest join first and then had to pay 200 for $C \bowtie D$.

## Correctness

GOO is a heuristic, so its correctness is about what it builds, not about optimality. The invariant is that the trees in $T$ always partition the relations, and that the stored size of each tree and the stored selectivity between each two trees are exact for the estimates. So each step picks a candidate pair with the smallest estimated join size, the result is a join tree with every relation as a leaf exactly once, and its returned cost is the true $C_{out}$ of that tree. If the query graph is connected, some two trees are always linked, so no join is a cross product. With three or fewer relations GOO is optimal, because the last join has the same size in every plan. The example shows that with four relations it can cost 1.6 times the optimum. The proof file has the details.

## Complexity

There are $n - 1$ steps. With $k$ trees, a step looks at fewer than $k^2/2$ pairs in $O(1)$ each, and the update after the join takes $O(k)$. The total is $O(n^3)$ time. The table of selectivities between trees takes $O(n^2)$ space. If the query graph has few edges, it is enough to look at the linked pairs, which lowers the work of each step.

## Properties

- **Heuristic.** The plan has no guarantee of optimality, and the example shows a plan 1.6 times the optimum on four relations.
- **Bushy plans.** It can join two intermediate results, unlike a greedy rule that adds one relation at a time to a left-deep plan.
- **No cross products on connected graphs.** Every join has a predicate between its inputs when the query graph is connected.
- **Deterministic.** With a fixed tie rule, the same input gives the same plan.
- **Depends on estimates.** Every choice uses estimated sizes, so errors in [cardinality estimation](/cardinality-estimation/) change the plan directly.

## Variants and improvements

- **Other greedy criteria.** A greedy rule can pick the pair with the smallest selectivity, or the smallest cost of the join operator, instead of the smallest result. The shape of the loop is the same.
- **Cross products.** If cross products are allowed in every step, a join of two very small relations without a predicate can be chosen. The code of this page allows this with a flag.
- **Hypergraphs.** With complex predicates, two trees are linked when a hyperedge has one side in each, as in [DPhyp](/dphyp/).
- **A start for other searches.** The plan of GOO can be the start plan of a randomized search such as [simulated annealing](/simulated-annealing/), or an upper bound for a search that prunes plans by cost.

## When to use it

Use it when a query has too many relations for an exact join enumerator, for example more than about 15 to 20 relations, depending on the shape of the query graph, and a plan is needed quickly. For tree-shaped queries where a left-deep plan is acceptable, the [IKKBZ algorithm](/ikkbz-algorithm/) gives the optimal left-deep order in polynomial time. For small queries, use an exact method such as [DPccp](/dpccp/).

## Pitfalls

- **Treating it as optimal.** The result can cost more than the optimum even on four relations.
- **Stale sizes.** After a join, the size of the new tree and its selectivities to the other trees must be updated; using the old values of the inputs gives wrong choices.
- **Ties.** Many queries have joins of equal estimated size. Without a fixed tie rule, the plan can change between runs.
- **Cross products by accident.** If the code scores all pairs, a cross product of two tiny relations can look like the smallest join; restrict the candidates to linked pairs unless cross products are wanted.

## Implementations

## History

Greedy rules for join order are older than GOO. The simpler ones add one relation at a time to a left-deep plan, and in 1997 Steinbrunn, Moerkotte and Kemper compared heuristics of this kind with randomized methods for large join queries. In 1998 Leonidas Fegaras described greedy operator ordering, which applies the greedy rule to any two subplans and so builds bushy plans for large queries.

## References
