---
tag: 0ECWZS
kind: algorithm
slug: dpccp
name: DPccp
aliases:
- dynamic programming over connected subgraph complement pairs
- csg-cmp pair enumeration
area: databases/query-planning
level: advanced
summary: Dynamic programming for join ordering that enumerates exactly the connected subgraph and complement pairs of the query graph.
solves: [join-ordering]
model: word-ram
complexity:
  vars: {n: the number of relations, c: the number of csg-cmp pairs of the query graph}
  time: {worst: "O(n c)"}
  space: {extra: "O(2^n)"}
properties: {deterministic: true, exact: true, recursive: true}
history:
  year: 2006
  people: [Guido Moerkotte, Thomas Neumann]
  note: Introduced at VLDB 2006 together with an analysis of the older DPsize and DPsub.
prereqs: [selinger-join-enumeration, left-deep-and-bushy-join-trees, connected-components]
see_also: [dphyp, join-ordering, ikkbz-algorithm, greedy-operator-ordering, matrix-chain-multiplication, principle-of-optimality, query-plan, cascades-framework]
sources:
  - paper: "Guido Moerkotte and Thomas Neumann, Analysis of two existing and one new dynamic programming algorithm for the generation of optimal bushy join trees without cross products, Proceedings of VLDB 2006, 930 to 941"
    title: Analysis of two existing and one new dynamic programming algorithm for the generation of optimal bushy join trees without cross products
    locator: "the algorithms DPsize, DPsub and DPccp, the procedures EnumerateCsg, EnumerateCsgRec and EnumerateCmp, and the number of csg-cmp pairs for chain, cycle, star and clique queries"
  - paper: "doi:10.1145/582095.582099"
    title: "P. Griffiths Selinger, M. M. Astrahan, D. D. Chamberlin, R. A. Lorie and T. G. Price, Access path selection in a relational database management system, Proceedings of ACM SIGMOD 1979, 23 to 34"
    locator: "Section 5, the dynamic program over subsets of relations that DPsize generalizes"
  - paper: "Guido Moerkotte and Thomas Neumann, Dynamic programming strikes back, Proceedings of ACM SIGMOD 2008, 539 to 552"
    title: Dynamic programming strikes back
    locator: "the extension of DPccp to hypergraphs (DPhyp), which builds on the same csg and cmp enumeration"
---

DPccp is a dynamic program that finds the cheapest bushy join tree without cross products for a connected query graph. Like the [Selinger enumeration](/selinger-join-enumeration/), it keeps the best plan for each set of relations and builds larger plans from smaller ones. The difference is in which pairs of sets it tries. Every join in a plan without cross products combines two disjoint connected sets of relations that a join predicate links: a *csg-cmp pair* (connected subgraph and connected complement). DPccp enumerates exactly these pairs, each once, in an order where the plans of both halves are already final. So its work grows with the number of such pairs, which is $(n^3 - n)/6$ for a chain query, and not with the number of all subsets. Moerkotte and Neumann gave it in 2006.

## In plain words

A dynamic program for join ordering keeps the cheapest plan for each group of tables and joins two groups to make a larger one. Older versions try many pairs of groups that are useless: groups whose tables are not linked by any predicate, or two groups with no predicate between them. On a long chain of tables almost every pair they try is useless.

DPccp only makes useful pairs. It grows each group from its smallest table, one ring of neighbors at a time, so every group it makes is linked. For each group, it grows the partners the same way, starting from the neighbors of the group. It never makes a pair twice, and it makes the smaller pieces of a group before the group itself, so their best plans are ready when it needs them.

## The problem

The input is a connected query graph on relations $v_0, \ldots, v_{n-1}$, with the size of each relation and a selectivity on each edge, and a cost function. The cost of a join tree is the sum of a join cost over its inner nodes, where the join cost of $P_1 \bowtie P_2$ depends only on the sets of relations of $P_1$ and $P_2$, for example $C_{out}$, the size of the result. The output is a cheapest [bushy](/left-deep-and-bushy-join-trees/) join tree in which each join has a predicate between its two inputs. This is the [join ordering](/join-ordering/) problem for bushy trees without cross products.

$N(S)$ is the *neighborhood* of a set $S$: the relations outside $S$ with an edge into $S$. $B_i = \{v_0, \ldots, v_i\}$.

## The algorithm

```pseudo id=main
DPCCP(query graph G)
L1  number the relations v_0, ..., v_(n-1) in breadth-first order
L2  for each relation v do best[{v}] ← the scan of v
L3  for each csg S1 from ENUMERATE-CSG do
L4      for each S2 from ENUMERATE-CMP(S1) do
L5          S ← S1 ∪ S2
L6          for (P1, P2) in (best[S1], best[S2]) and (best[S2], best[S1]) do
L7              if best[S] is empty or cost(P1 ⋈ P2) < cost(best[S]) then best[S] ← P1 ⋈ P2
L8  return best[all relations]
```

```pseudo id=enum
ENUMERATE-CSG
L9  for i ← n-1 down to 0 do
L10     emit {v_i}
L11     ENUMERATE-CSG-REC({v_i}, B_i)

ENUMERATE-CSG-REC(S, X)
L12 N ← N(S) - X
L13 for each nonempty subset S' of N, smaller subsets first do emit S ∪ S'
L14 for each nonempty subset S' of N, smaller subsets first do ENUMERATE-CSG-REC(S ∪ S', X ∪ N)

ENUMERATE-CMP(S1)
L15 X ← B_min(S1) ∪ S1
L16 N ← N(S1) - X
L17 for each v_i in N, by decreasing i do
L18     emit {v_i}
L19     ENUMERATE-CSG-REC({v_i}, X ∪ (B_i ∩ N))
```

ENUMERATE-CSG starts a new set from each relation $v_i$ and only lets it grow into relations with a larger index, so $v_i$ is the smallest member of every set it makes in that iteration. ENUMERATE-CSG-REC grows a connected set $S$ by any nonempty subset of its neighborhood. The set $X$ holds the relations that this branch must not add, either because they have a smaller index or because another branch adds them; this is what makes every set appear only once. ENUMERATE-CMP grows the partners of $S_1$ from its neighbors, in the same way, but only with relations above the smallest index of $S_1$, so each unordered pair appears once, with $S_1$ as the half that holds the smaller index. Line L6 tries both orders of the inputs, which matters when the join cost is not symmetric, as for a hash join with a build side.

## Example

Four relations form a chain $A$-$B$-$C$-$D$, with 50, 1000, 200 and 10 tuples and the selectivities 1/100, 1/50 and 1/2 on the three edges. The cost is $C_{out}$. The table lists the pairs in the order that DPccp uses them, with the size of the union, the cost of the new candidate, and the best plan stored for the union after the pair.

| $S_1$ | $S_2$ | size of the union | candidate cost | best plan after the pair |
|---|---|---|---|---|
| $C$ | $D$ | 1000 | 1000 | $C \bowtie D$, 1000 |
| $B$ | $C$ | 4000 | 4000 | $B \bowtie C$, 4000 |
| $B$ | $CD$ | 20 000 | 21 000 | $B \bowtie (C \bowtie D)$, 21 000 |
| $BC$ | $D$ | 20 000 | 24 000 | unchanged, 21 000 |
| $A$ | $B$ | 500 | 500 | $A \bowtie B$, 500 |
| $A$ | $BC$ | 2000 | 6000 | $A \bowtie (B \bowtie C)$, 6000 |
| $A$ | $BCD$ | 10 000 | 31 000 | $A \bowtie (B \bowtie (C \bowtie D))$, 31 000 |
| $AB$ | $C$ | 2000 | 2500 | $(A \bowtie B) \bowtie C$, 2500 |
| $AB$ | $CD$ | 10 000 | 11 500 | $(A \bowtie B) \bowtie (C \bowtie D)$, 11 500 |
| $ABC$ | $D$ | 10 000 | 12 500 | unchanged, 11 500 |

There are 10 pairs, which is $(4^3 - 4)/6$. The pairs for $\{B, C, D\}$ come before $B C D$ is used as a half, and $ABC$ has its final plan before the last row. The result is the bushy tree $(A \bowtie B) \bowtie (C \bowtie D)$ with cost 11 500; the cheapest left-deep tree, $((A \bowtie B) \bowtie C) \bowtie D$, costs 12 500. A dynamic program over all subsets with all their splits would look at 50 ordered splits for these four relations, most of them with a disconnected half.

## Correctness

There are three facts to show. First, ENUMERATE-CSG emits each connected set exactly once: a set with smallest member $v_i$ is made only in the iteration for $i$, and inside it the set $X$ decides in which branch each relation is added. Second, ENUMERATE-CMP($S_1$) emits exactly the connected sets that are disjoint from $S_1$, linked to it by an edge, and above its smallest index, each once; with the first fact, every csg-cmp pair is used exactly once. Third, when a pair is used, all pairs with union $S_1$ or $S_2$ have been used: the halves of $S_2$ have a larger smallest index, so they come in an earlier iteration of line L9, and the halves of $S_1$ are smaller sets with the same smallest member, which line L13 emits first because it takes smaller subsets first. Then the usual argument applies: the last join of an optimal plan combines a csg-cmp pair, and the best plans of its halves are optimal. The proof file has the details; the argument does not need the breadth-first numbering.

## Complexity

Let $c$ be the number of csg-cmp pairs. Every call of ENUMERATE-CSG-REC belongs to a set that was just emitted, and costs $O(n)$ to compute a neighborhood with bit operations, so the enumeration takes $O(n c)$ time; there are at most $c + n$ connected sets, and each pair costs $O(1)$ at lines L5 to L7 when the sizes are stored per set. The table holds one plan per connected set, at most $2^n$.

| query graph | csg-cmp pairs $c$ | $n = 5$ | $n = 10$ | $n = 20$ |
|---|---|---|---|---|
| chain | $(n^3 - n)/6$ | 20 | 165 | 1330 |
| star | $(n - 1)\, 2^{n-2}$ | 32 | 2304 | 4 980 736 |
| clique | $(3^n - 2^{n+1} + 1)/2$ | 90 | 28 501 | 1 742 343 625 |

Any dynamic program that considers every csg-cmp pair must do at least $c$ steps, so DPccp is within a factor $n$ of that bound, and its work adapts to the shape of the graph. DPsub, which tries every split of every subset, does $\Theta(3^n)$ steps on every graph, including a chain.

## Properties

- **Exact.** The result is a cheapest bushy tree without cross products for any cost that adds a join term which depends only on the sets of the two inputs.
- **No wasted pairs.** Every pair it builds is a legal join, and no pair is built twice.
- **Needs a connected graph.** If the graph is not connected, there is no plan without a cross product; a system must add cross product edges first.
- **Simple predicates only.** Each edge links two relations. Predicates over three or more relations, and the ordering limits of outer joins, need hyperedges, which is what [DPhyp](/dphyp/) adds.

## Variants and improvements

- **DPsize and DPsub.** The older dynamic programs enumerate pairs by the sizes of the sets, or by the subsets of each set, and test each pair for connectivity and for an edge. They find the same optimum but test many pairs that fail. Moerkotte and Neumann analyze both.
- **DPhyp.** Moerkotte and Neumann (2008) generalize the neighborhood and the enumeration to hypergraphs. For a graph without hyperedges it enumerates the same pairs.
- **Physical properties.** Keeping one plan per (set, interesting order) pair, as in the Selinger enumeration, adds sort orders without changing the enumeration.
- **Cross products.** To allow cross products, add an edge with selectivity 1 between every pair of relations; the graph becomes a clique and DPccp then behaves like DPsub.

## When to use it

Use it as the exact bushy join enumerator of an optimizer for queries with up to 10 to 20 relations, when cross products are not wanted. It is most useful for sparse graphs (chains, stars, snowflakes with few joins), where it avoids most of the work of DPsub. For a star with 20 relations or a large clique it is still exponential; then use a heuristic such as [greedy operator ordering](/greedy-operator-ordering/) or, for tree queries and left-deep plans, the [IKKBZ algorithm](/ikkbz-algorithm/).

## Pitfalls

- **Subset order in ENUMERATE-CSG-REC.** The proof needs smaller subsets of $N$ before their supersets at lines L13 and L14. Enumerating them in another order, for example from the largest down, can use a set as a half before its best plan is final.
- **Asymmetric costs.** Each unordered pair appears once, so the code must try both orders of the inputs at line L6 when the join cost is not symmetric.
- **Equivalent predicates.** The graph should contain the edges implied by equalities, such as $A.x = C.x$ from $A.x = B.x$ and $B.x = C.x$. Without them, the graph has fewer edges and the search misses plans.
- **Estimates.** The plan is optimal for the estimated sizes; see [cardinality estimation](/cardinality-estimation/).

## Implementations

## History

The Selinger optimizer of System R (1979) introduced dynamic programming for join ordering, over left-deep trees. Later optimizers extended it to bushy trees with DPsize, which enumerates by the size of the sets, and DPsub, which enumerates the subsets of each set. In 2006 Moerkotte and Neumann analyzed these two, showed how far each is from the number of csg-cmp pairs, and gave DPccp, which enumerates the pairs directly. In 2008 they extended it to hypergraphs as DPhyp, which is used for queries with complex predicates and outer joins.

## References
