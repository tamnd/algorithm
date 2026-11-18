---
tag: CD2W8Y
kind: algorithm
slug: dphyp
name: DPhyp
aliases:
- hypergraph-based join enumeration
- DPhyp join enumeration
area: databases/query-planning
level: research
summary: "An extension of DPccp to query hypergraphs, which handles complex join predicates and the reordering of outer joins."
solves: [join-ordering]
model: word-ram
complexity:
  vars: {n: the number of relations, m: the number of hyperedges}
  time: {worst: "O(3^n m^2)"}
  space: {extra: "O(2^n)"}
properties: {deterministic: true, exact: true, recursive: true}
history:
  year: 2008
  people: [Guido Moerkotte, Thomas Neumann]
  note: Introduced at SIGMOD 2008 in the paper Dynamic programming strikes back.
prereqs: [hypergraph, dpccp]
see_also: [join-ordering, selinger-join-enumeration, left-deep-and-bushy-join-trees, greedy-operator-ordering, cascades-framework, relational-algebra-equivalences, subquery-unnesting, cost-model]
sources:
  - paper: "Guido Moerkotte and Thomas Neumann, Dynamic programming strikes back, Proceedings of ACM SIGMOD 2008, 539 to 552"
    title: Dynamic programming strikes back
    locator: "the query hypergraph, the neighborhood of a set, the procedures Solve, EmitCsg, EnumerateCsgRec, EnumerateCmpRec and EmitCsgCmp, and the treatment of non-inner joins"
  - paper: "Guido Moerkotte and Thomas Neumann, Analysis of two existing and one new dynamic programming algorithm for the generation of optimal bushy join trees without cross products, Proceedings of VLDB 2006, 930 to 941"
    title: Analysis of two existing and one new dynamic programming algorithm for the generation of optimal bushy join trees without cross products
    locator: "the algorithm DPccp for simple query graphs, which DPhyp generalizes"
---

DPhyp is a dynamic program that finds the cheapest bushy join tree without cross products when the join predicates form a *hypergraph*. A simple join predicate such as $R.a = S.b$ links two relations. A complex one, such as $R.a + S.b = T.c$, needs $R$ and $S$ on one side of the join and $T$ on the other: it is a hyperedge $\{\{R, S\}, \{T\}\}$. [DPccp](/dpccp/) cannot use such a predicate, and a system that drops it may see a query graph that is not connected. DPhyp extends the enumeration of DPccp to hyperedges. It emits every pair of disjoint connected sets that a hyperedge links, each once, in an order where the best plans of both halves are already final. Moerkotte and Neumann gave it in 2008, and they also showed how to encode the reordering limits of outer joins and antijoins as hyperedges.

## In plain words

Some join conditions need three or more tables at once. Such a condition can only be checked when the join puts one group of its tables on the left and the other group on the right. The query then is not a simple graph of tables but a graph whose edges connect groups of tables.

DPhyp keeps the cheapest plan for each group of tables, as other dynamic programs for join order do. It grows groups from their smallest table, and it grows partners for each group, so that it only tries joins that can check a condition. When an edge leads to a whole group of tables, it steps into one table of that group and keeps growing from there. Some groups it reaches this way are not linked yet. It skips those, because no plan for them is in its table.

## The problem

The input is a query hypergraph on relations $v_0, \ldots, v_{n-1}$, with the size of each relation, and a set of hyperedges. A hyperedge is a pair $\{u, w\}$ of disjoint nonempty sets of relations with a selectivity. A hyperedge *links* two disjoint sets $A$ and $B$ if one of its sides is inside $A$ and the other is inside $B$. A set is *connected* if it has one relation, or if it splits into two disjoint connected sets that a hyperedge links. The cost of a join tree is the sum of a join cost over its inner nodes, where the join cost depends only on the sets of the two inputs, for example $C_{out}$, the size of the result. The size of a set is the product of the sizes of its relations and of the selectivities of the hyperedges inside it. The output is a cheapest [bushy](/left-deep-and-bushy-join-trees/) join tree in which a hyperedge links the two inputs of every join. A simple graph is the case where every side has one relation; then this is the problem that DPccp solves.

For sets $S$ and $X$, $N(S, X)$ is the *neighborhood*: take every side $w$ of a hyperedge whose other side is inside $S$ and which is disjoint from $S$ and $X$, keep the sides $w$ that contain no other such side, and take the member with the smallest index of each. $B_i = \{v_0, \ldots, v_i\}$.

## The algorithm

```pseudo id=main
DPHYP(hypergraph H with relations v_0, ..., v_(n-1))
L1  for each relation v do best[{v}] ← the scan of v
L2  for i ← n-1 down to 0 do
L3      EMIT-CSG({v_i})
L4      ENUMERATE-CSG-REC({v_i}, B_i)
L5  return best[all relations]
```

```pseudo id=enum
ENUMERATE-CSG-REC(S1, X)
L6  N ← N(S1, X)
L7  for each nonempty subset S' of N, smaller subsets first do
L8      if best[S1 ∪ S'] is not empty then EMIT-CSG(S1 ∪ S')
L9  for each nonempty subset S' of N, smaller subsets first do ENUMERATE-CSG-REC(S1 ∪ S', X ∪ N)

EMIT-CSG(S1)
L10 X ← S1 ∪ B_min(S1)
L11 N ← N(S1, X)
L12 for each v_i in N, by decreasing i do
L13     if a hyperedge links S1 and {v_i} then EMIT-CSG-CMP(S1, {v_i})
L14     ENUMERATE-CMP-REC(S1, {v_i}, X ∪ (B_i ∩ N))

ENUMERATE-CMP-REC(S1, S2, X)
L15 N ← N(S2, X)
L16 for each nonempty subset S' of N, smaller subsets first do
L17     if best[S2 ∪ S'] is not empty and a hyperedge links S1 and S2 ∪ S' then EMIT-CSG-CMP(S1, S2 ∪ S')
L18 for each nonempty subset S' of N, smaller subsets first do ENUMERATE-CMP-REC(S1, S2 ∪ S', X ∪ N)

EMIT-CSG-CMP(S1, S2)
L19 S ← S1 ∪ S2
L20 for (P1, P2) in (best[S1], best[S2]) and (best[S2], best[S1]) do
L21     if best[S] is empty or cost(P1 ⋈ P2) < cost(best[S]) then best[S] ← P1 ⋈ P2
```

The structure is that of DPccp. The main loop starts a search from each relation $v_i$ and only lets it grow into relations with a larger index. ENUMERATE-CSG-REC grows a set by subsets of its neighborhood, and the set $X$ keeps two branches from making the same set. EMIT-CSG looks for partners of a set $S_1$, only above its smallest index, so each unordered pair appears once. There are two changes. First, the neighborhood holds one representative relation of each hyperedge side, so a step can reach a set that is not connected yet; line L8 skips such a set, because it has no plan in the table, and line L9 keeps growing it. Second, line L17 tests that a hyperedge really links the two halves, because a partner can be connected but meet a hyperedge with only part of a side.

## Example

Four relations $A$, $B$, $C$ and $D$ have 10, 20, 30 and 40 tuples. The predicates are $A.k = B.k$ with selectivity 1/10, $C.k = D.k$ with selectivity 1/10, and $A.x + B.y = C.z + D.w$ with selectivity 1/100, which is the hyperedge $\{\{A, B\}, \{C, D\}\}$. The cost is $C_{out}$.

| step | set | what happens |
|---|---|---|
| $i = 3$ | $D$ | no neighbors above it |
| $i = 2$ | $C$ | partner $D$: pair $(C, D)$, $\mathrm{best}[CD]$ costs 120 |
| | $CD$ | visited at line L8; no partners above index 2 |
| $i = 1$ | $B$ | its only simple neighbor $A$ is below it, and the hyperedge needs $A$ too, so nothing grows |
| $i = 0$ | $A$ | partner $B$: pair $(A, B)$, $\mathrm{best}[AB]$ costs 20 |
| | $AB$ | the hyperedge gives the representative $C$; $\{C\}$ alone is not linked to $AB$, but the search grows it to $CD$: pair $(AB, CD)$, $\mathrm{best}[ABCD]$ costs $120 + 20 + 24 = 164$ |
| | $ABC$ | reached from $AB$ through the representative $C$; not connected, so line L8 skips it |
| | $ABCD$ | reached from $ABC$; it has a plan, so EMIT-CSG runs and finds no partner |

The result is $(A \bowtie B) \bowtie (C \bowtie D)$ with cost 164. There are three csg-cmp pairs in all. A join such as $A \bowtie C$ is never tried, because no predicate links $A$ and $C$, and $ABC$ is reached but never planned. If the hyperedge were split into the simple edges $A$-$C$, $A$-$D$, $B$-$C$ and $B$-$D$, a simple enumerator would also try joins such as $A \bowtie C$, where the predicate cannot be checked yet.

## Correctness

The proof follows that of DPccp, with three changes. Connectivity has the recursive definition above. One lemma replaces the edge argument: if a set $T$ is connected, every split of $T$ into two nonempty parts is crossed by a hyperedge, so a search from inside $T$ always has a representative in $T$ to step into. The searches then visit every connected set with the right smallest index exactly once, and never visit a set before its subsets. The table test at line L8 makes this enough: by induction over the run, when a set is visited, all pairs with that union have been used, so the set is in the table exactly when it is connected. Each csg-cmp pair is then used exactly once, with final plans for both halves, and the usual argument shows that the plan for all relations is optimal. The proof file has the details.

## Complexity

With the sets stored as bitmasks, each set is visited at most once in the main search, and for each $S_1$ each set disjoint from it is tested at most once in the partner search. So there are fewer than $3^n$ tests, and each costs one neighborhood, which this page computes in $O(m^2)$ steps for $m$ hyperedges. That gives $O(3^n m^2)$ time in the worst case and $O(2^n)$ space for the table. The bound is loose for sparse hypergraphs. For a simple graph, DPhyp makes the same calls as DPccp and does $O(n c)$ work for $c$ csg-cmp pairs, which is $(n^3 - n)/6$ pairs for a chain.

## Properties

- **Exact.** The result is a cheapest bushy plan without cross products for any cost that adds a join term which depends only on the sets of the two inputs.
- **Each pair once.** Every csg-cmp pair is used exactly once. Some sets that are not connected are reached on the way and skipped.
- **Same as DPccp on graphs.** On a simple graph it enumerates the same pairs in the same order.
- **Needs a connected hypergraph.** If the hypergraph is not connected, there is no plan without a cross product, and the table never holds the set of all relations.

## Variants and improvements

- **Non-inner joins.** For an outer join or an antijoin, some orders give a different result. The 2008 paper encodes these limits in the hyperedges: the sides of the hyperedge for such a join hold the relations that must be present on each side, so that the enumeration only builds valid orders.
- **Conflict detection.** Later work studies which reorderings of non-inner joins are valid and how to detect the conflicts during the enumeration, without changing the enumeration itself.
- **Physical properties.** As in the [Selinger enumeration](/selinger-join-enumeration/), the table can keep one plan per set and [interesting order](/interesting-orders/) without a change to the enumeration.
- **Large queries.** For queries too large for exact enumeration, a heuristic such as [greedy operator ordering](/greedy-operator-ordering/) can build a plan from the same hypergraph.

## When to use it

Use it as the exact bushy join enumerator of an optimizer when the query has predicates over three or more relations, or outer joins, semijoins and antijoins whose order is limited. For a query with only simple equality predicates and inner joins, DPccp does the same work. As with any exact join enumerator, it is practical for queries with up to about 10 to 20 relations, depending on the shape of the hypergraph.

## Pitfalls

- **Skipping the table test.** Line L8 must test that the set has a plan. Without the test, EMIT-CSG runs for sets that are not connected.
- **Skipping the link test.** Line L17 must test that a hyperedge links $S_1$ and the partner. A partner that is connected and next to $S_1$ through a representative may not hold a whole side of any hyperedge into $S_1$.
- **Subset order.** As in DPccp, the subsets of $N$ must come smaller first, or a set can be used as a half before its best plan is final.
- **Asymmetric costs.** Each unordered pair appears once, so line L20 must try both orders of the inputs when the join cost is not symmetric.
- **Selectivities of hyperedges.** A hyperedge applies to a set only when both of its sides are inside the set; its selectivity must not be applied to a join that has only part of a side.

## Implementations

## History

The dynamic programs for join order since System R used simple query graphs. In 2006 Moerkotte and Neumann gave DPccp, which enumerates only the connected subgraph and complement pairs of such a graph. In 2008, in the paper Dynamic programming strikes back, they extended it to hypergraphs, so that complex predicates and the reordering limits of non-inner joins fit in the same enumeration. Later work refined the way that these reordering limits are turned into hyperedges.

## References
