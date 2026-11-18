---
tag: ZKFGDY
kind: algorithm
slug: ikkbz-algorithm
name: IKKBZ algorithm
aliases:
- Ibaraki-Kameda-Krishnamurthy-Boral-Zaniolo algorithm
- KBZ algorithm
- IKKBZ
- rank-based join ordering for tree queries
area: databases/query-planning
level: advanced
summary: "Find the optimal left-deep join order without cross products for an acyclic query graph and an ASI cost, in polynomial time."
solves: [join-ordering]
model: word-ram
complexity:
  vars: {n: the number of relations}
  time: {worst: "O(n^2 log n)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: true, recursive: true}
history:
  year: 1984
  people: [Toshihide Ibaraki, Tiko Kameda, Ravi Krishnamurthy, Haran Boral, Carlo Zaniolo]
  note: "Ibaraki and Kameda gave the algorithm for tree queries in TODS 1984; Krishnamurthy, Boral and Zaniolo generalized it to ASI costs at VLDB 1986."
prereqs: [join-ordering, left-deep-and-bushy-join-trees, cost-model]
see_also: [selinger-join-enumeration, dpccp, greedy-operator-ordering, join-ordering-np-hardness, smiths-rule, weighted-completion-time, predicate-pushdown, cardinality-estimation]
sources:
  - paper: "doi:10.1145/1270.1498"
    title: "Toshihide Ibaraki and Tiko Kameda, On the optimal nesting order for computing N-relational joins, ACM Transactions on Database Systems 9(3) (1984), 482 to 502"
    locator: "the algorithm for tree queries with the nested loop cost, which tries each relation as the first one and orders the rest by rank, in O(n^2 log n) time"
  - paper: "Ravi Krishnamurthy, Haran Boral and Carlo Zaniolo, Optimization of nonrecursive queries, Proceedings of VLDB 1986, 128 to 137"
    title: Optimization of nonrecursive queries
    locator: the O(n^2) algorithm for tree queries with cost functions that have the adjacent sequence interchange (ASI) property
  - paper: "Clyde L. Monma and Jeffrey B. Sidney, Sequencing with series-parallel precedence constraints, Mathematics of Operations Research 4(3) (1979)"
    title: Sequencing with series-parallel precedence constraints
    locator: "the adjacent sequence interchange property and the optimal sequencing of jobs under series-parallel precedence constraints, on which the join algorithm is based"
  - paper: "Michael Steinbrunn, Guido Moerkotte and Alfons Kemper, Heuristic and randomized optimization for the join ordering problem, The VLDB Journal 6(3) (1997), 191 to 208"
    title: Heuristic and randomized optimization for the join ordering problem
    locator: "the KBZ algorithm as one of the compared methods on large join queries, applied to a spanning tree of the query graph"
---

The IKKBZ algorithm finds the cheapest left-deep join order without cross products when the query graph is a tree and the cost function has the *adjacent sequence interchange* (ASI) property, such as the sum of the intermediate result sizes. It runs in polynomial time, although [join ordering](/join-ordering/) is NP-hard in general. It fixes the first relation, which turns the query tree into a precedence order: each relation must come after its parent. Then it gives every relation and every group of relations a *rank*, and sorts by rank. Where the precedence order forbids the sorted position, it glues a parent to its child into one block. It tries every relation as the first one and keeps the best order. The name comes from Ibaraki and Kameda (1984) and Krishnamurthy, Boral and Zaniolo (1986).

## In plain words

A plan that joins tables one at a time should first add the tables that shrink the result, and late the tables that make it grow. A good number for this is the rank of a table: how much it makes the result grow, against how much work it adds. Sorting the tables by rank gives the best order when the tables can come in any order.

But a table can only join a table that is already in the result. When a good table must wait for a poor table, the algorithm glues the two into one block and gives the block its own rank. The block is then sorted like a single table. This needs no search, so it is fast. The algorithm does this once for each possible first table and keeps the cheapest order.

## The problem

The input is a set of relations $R_0, \ldots, R_{n-1}$ with sizes $|R_i| > 0$ and a query graph that is a tree, with a selectivity $f_{ij} > 0$ on each edge. Under the independence assumption, the join of a set $S$ has $|R_S| = \prod_{i \in S} |R_i| \prod_{\{i,j\} \subseteq S} f_{ij}$ tuples. The output is a [left-deep](/left-deep-and-bushy-join-trees/) order $R_{v_1}, \ldots, R_{v_n}$ in which each relation after the first has an edge to an earlier one (no cross product), with the least cost $C_{out} = \sum_{k=2}^{n} |R_{\{v_1, \ldots, v_k\}}|$.

Fix the first relation $r$ and hang the tree from it. For $v \ne r$ with parent $p(v)$, let $T(v) = f_{v p(v)} |R_v|$: the factor by which $R_v$ multiplies the result when it is joined. For a sequence $s$ of non-root relations, $T(s)$ is the product of the factors, and the cost is defined by

$$C(v) = T(v), \qquad C(s_1 s_2) = C(s_1) + T(s_1)\, C(s_2), \qquad \mathrm{rank}(s) = \frac{T(s) - 1}{C(s)}.$$

Then $C_{out}(r\, s) = |R_r| \cdot C(s)$. A cost with this form has the ASI property: exchanging two adjacent blocks $A$ and $B$ changes the cost by $T(U)\, C(A)\, C(B)\, (\mathrm{rank}(A) - \mathrm{rank}(B))$, where $U$ is the part before them. So the block with the smaller rank should come first.

## The algorithm

A *module* is a sequence of relations that stays together, with its $T$ and $C$.

```pseudo id=main
IKKBZ(relations, tree of predicates)
L1  best ← none
L2  for each relation r do
L3      hang the tree from r; p(v) is the parent of v
L4      for each v ≠ r do T(v) ← f(v, p(v)) · |R_v|
L5      mods ← LINEARIZE(r)
L6      cost ← |R_r| · C(concatenation of mods)
L7      if best = none or cost < cost(best) then best ← (cost, r followed by mods)
L8  return best
```

```pseudo id=linearize
LINEARIZE(v)
L9  merged ← the modules of LINEARIZE(c) for all children c of v, merged by rank
L10 if v = r then return merged
L11 head ← the module (v), with T = C = T(v)
L12 while merged is not empty and rank(head) > rank(first module of merged) do
L13     head ← head followed by the first module of merged, which is removed
L14 return head followed by merged
```

Line L9 merges lists that are already sorted by rank, so each child list keeps its own order and the precedence order inside each subtree holds. Lines L11 to L13 handle the case where a child block has a smaller rank than its parent: it should come before the parent, but it cannot, so the best place for it is directly after the parent, and the two become one module. The new module has a rank between the two old ranks, so it may also absorb the next module. Line L14 returns a list whose ranks do not decrease, which is what the parent needs for its own merge. On equal ranks the order of the merge does not change the cost.

## Example

Five relations: $A$ with 100 tuples, $B$ with 1000, $C$ with 200, $D$ with 50 and $E$ with 10. The query tree has the edges $A$-$B$ (selectivity 1/100), $A$-$C$ (1/50), $C$-$D$ (1/10) and $C$-$E$ (1/2).

With $A$ first, $T(B) = 10$, $T(C) = 4$, $T(D) = 5$ and $T(E) = 5$, so the ranks of the single relations are 9/10, 3/4, 4/5 and 4/5. $C$ has a smaller rank than its children, so LINEARIZE($C$) returns $C$, $D$, $E$ unchanged, and the root merges this list with $B$: the order is $A C D E B$. Its cost is $100 \cdot (4 + 4 \cdot 5 + 20 \cdot 5 + 100 \cdot 10) = 112\,400$.

With $D$ first, the tree hangs as $D$-$C$, and $C$ has the children $A$ and $E$. Now $T(C) = 20$ and $T(A) = 2$, so $\mathrm{rank}(C) = 19/20$ is larger than $\mathrm{rank}(A) = 1/2$, but $A$ must come after $C$. Line L13 glues them into the module $CA$ with $T = 40$ and $C = 20 + 20 \cdot 2 = 60$, so its rank is $39/60 = 13/20$. That is below $\mathrm{rank}(E) = 4/5$, so the loop stops.

| first relation | modules after LINEARIZE | order | $C_{out}$ |
|---|---|---|---|
| $A$ | $C$, $D$, $E$, $B$ | $A C D E B$ | 112 400 |
| $B$ | $A$, $C$, $D$, $E$ | $B A C D E$ | 125 000 |
| $C$ | $A$, $D$, $E$, $B$ | $C A D E B$ | 112 400 |
| $D$ | $CA$, $E$, $B$ | $D C A E B$ | 113 000 |
| $E$ | $CA$, $D$, $B$ | $E C A D B$ | 113 000 |

Line L7 keeps the first order of cost 112 400. Of the 120 orders of five relations, 28 have no cross product; their costs range from 112 400 to 125 000, and four of them reach the minimum. Starting with the largest relation $B$ gives the worst choice of first relation here.

## Correctness

Fix the first relation. The orders without cross products are exactly the sequences in which each relation comes after its parent, and the cost of such an order is $|R_r| \cdot C(s)$, because the edges inside a prefix are exactly the parent edges of its relations. The proof turns any such sequence into the output of the algorithm without raising the cost, from the leaves up. At each node, two child modules that are in the wrong order are brought together by moving one of them past the unrelated relations between them, and then exchanged; by the ASI identity no step raises the cost. A child module that follows its parent block with a smaller rank is brought next to it the same way, which is the gluing of line L13. At the root, the result is the order of line L10, so it is optimal for that first relation, and line L2 tries all first relations. The proof file has the details.

## Complexity

The algorithm runs once for each of the $n$ first relations. Ibaraki and Kameda do one run in $O(n \log n)$ time, so the total is $O(n^2 \log n)$; Krishnamurthy, Boral and Zaniolo reduce the total to $O(n^2)$. The version on this page sorts all modules of a subtree at every node, which costs $O(n^2 \log n)$ for one run on a path-shaped tree and $O(n^3 \log n)$ in total; it is simpler to check. The extra space is $O(n)$ for the tree and the module lists. This is polynomial, against $2^{n-1}$ orders without cross products for a chain query and $2(n-1)!$ for a star (see [query plan](/query-plan/)).

## Properties

- **Exact for its space.** The result is a cheapest left-deep order without cross products for a tree query under an ASI cost. It says nothing about bushy trees or about orders with cross products, which can be cheaper.
- **Needs the ASI form.** The cost of a sequence must be $C(s_1) + T(s_1) C(s_2)$ for some positive $T$. $C_{out}$ and the nested loop cost of Ibaraki and Kameda have this form.
- **Deterministic and simple.** There is no table over subsets; the work is sorting and gluing.

## Variants and improvements

- **KBZ.** Krishnamurthy, Boral and Zaniolo (1986) state the algorithm for every ASI cost and bring the total time for all first relations to $O(n^2)$.
- **A fixed first relation.** When the first relation is given, for example because it is the only one with a useful index, one run of lines L3 to L6 is enough.
- **Cyclic query graphs.** A common heuristic keeps only a spanning tree of the query graph, for example one that keeps the most selective predicates, runs IKKBZ on the tree and applies the other predicates where their relations are present. The result is then not guaranteed to be optimal; Steinbrunn, Moerkotte and Kemper (1997) compare this use of KBZ with randomized methods on large queries.

## When to use it

Use it for tree queries (chains, stars, snowflakes) with many relations, where the dynamic programs over subsets are too slow, and when left-deep plans without cross products are acceptable. For up to about a dozen relations, the exact [Selinger enumeration](/selinger-join-enumeration/) or [DPccp](/dpccp/) can also choose bushy trees and physical operators. For large cyclic graphs, [greedy operator ordering](/greedy-operator-ordering/) or IKKBZ on a spanning tree are both heuristics.

## Pitfalls

- **Trying one first relation only.** The root changes the precedence order and the result. In the example, starting with $B$ costs 125 000 against 112 400.
- **Zero sizes.** A relation with no tuples gives $T = 0$ and a module with $C = 0$, and the rank is not defined. An empty relation makes the whole join empty, so the order hardly matters; handle it before the algorithm.
- **Floating point ranks.** Ranks that are equal in exact arithmetic can compare unequal in floating point, which changes the merge order. That does not change the cost, but it can make plans differ between runs on different machines. Exact fractions or a stable tie rule avoid this.
- **Costs without the ASI form.** A cost that depends on the physical join method per step, such as the choice between a hash join and an index nested loop join, is usually not of this form, and then the result is a heuristic.
- **Independence.** The sizes come from the product of the selectivities. The order is optimal for those estimates; see [cardinality estimation](/cardinality-estimation/).

## Implementations

## History

The problem is a form of job sequencing with precedence constraints: order jobs on one machine to minimize a weighted cost, where some jobs must wait for others. Monma and Sidney (1979) solved it for series-parallel precedence orders and costs with the adjacent sequence interchange property. Ibaraki and Kameda (1984) used this approach for join orders, with the nested loop cost and tree queries, and showed in the same paper that the general problem is NP-complete. Krishnamurthy, Boral and Zaniolo (1986) extended it to every ASI cost and brought the time to $O(n^2)$. The algorithm is known as IKKBZ after the five authors.

## References
