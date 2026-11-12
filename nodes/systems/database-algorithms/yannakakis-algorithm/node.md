---
tag: D8JPK9
kind: algorithm
slug: yannakakis-algorithm
name: Yannakakis algorithm
aliases:
- Yannakakis join algorithm
- semijoin full reducer evaluation
area: systems/database-algorithms
level: advanced
summary: "Evaluate an acyclic join on its join tree: semijoin passes up and down remove every dangling tuple, then joins in time linear in input plus output."
solves: [acyclic-join-evaluation]
model: word-ram
complexity:
  vars: {n: the total number of input tuples, z: the number of output tuples, r: the number of relations}
  time: {expected: O(r n + r z)}
  space: {extra: O(n + z)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [semijoin, hash-join, acyclic-join-evaluation]
see_also: [multiway-join, generic-join, leapfrog-triejoin, junction-tree, tree-decomposition, join-ordering, bloom-join, query-optimization]
sources:
  - paper: "Mihalis Yannakakis, Algorithms for acyclic database schemes, Proceedings of the 7th International Conference on Very Large Data Bases (VLDB), 82 to 94 (1981)"
    locator: the full reducer by two semijoin passes over a join tree, and the evaluation of acyclic joins with projections in time polynomial in input and output
  - paper: doi:10.1145/322234.322238
    title: Philip A. Bernstein and Dah-Ming W. Chiu, Using semi-joins to solve relational queries, Journal of the ACM 28(1), 25 to 40 (1981)
    locator: semijoin programs and full reducers for tree queries
  - paper: doi:10.1145/2402.322389
    title: Catriel Beeri, Ronald Fagin, David Maier and Mihalis Yannakakis, On the desirability of acyclic database schemes, Journal of the ACM 30(3), 479 to 513 (1983)
    locator: the equivalence of acyclicity, join trees, full reducers and pairwise consistency implying global consistency
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 6, Section 6.4 (acyclic joins, full reducers and the Yannakakis algorithm)
  - paper: "Guillaume Bagan, Arnaud Durand and Etienne Grandjean, On acyclic conjunctive queries and constant delay enumeration, CSL 2007, Lecture Notes in Computer Science 4646, 208 to 222"
    locator: free-connex acyclic queries, which can be answered in time linear in input plus output
---

The Yannakakis algorithm evaluates an [acyclic join](/acyclic-join-evaluation/) in time linear in the size of the input plus the size of the output. Mihalis Yannakakis published it in 1981. It works on a join tree of the query. First, a bottom-up pass and a top-down pass of [semijoins](/semijoin/), called the *full reducer*, delete every tuple that takes part in no output tuple. Then it joins the reduced relations up the tree. After the reduction, no intermediate result is larger than the output, so a bad join order can no longer blow up.

## In plain words

You have several tables that link in a tree shape: orders link to customers, customers link to cities, and orders link to products. Some rows lead nowhere: an order whose product is not in the product table can never be part of the answer.

First, walk from the leaves of the tree to the root, and at each table drop the rows that have no partner in a child table. Then walk back from the root to the leaves, and drop the rows that have no partner in the parent table. After the two walks, each row that is left is part of at least one answer. Now join the tables in any order up the tree. Nothing is wasted, because no row is thrown away later.

## The problem

The input is a set of relations $R_1, \ldots, R_r$ whose hypergraph is alpha-acyclic, given with a *join tree*: a tree on the relations such that, for each attribute, the relations that hold it form a connected subtree (the *running intersection property*). A join tree can be found in linear time, for example by the GYO reduction (see [acyclic join evaluation](/acyclic-join-evaluation/)). The output is the natural join, or its projection on a set $O$ of output attributes. The cost model is the word RAM with hash tables; $n$ is the total number of input tuples, $z$ the number of output tuples.

## The algorithm

```pseudo id=main
YANNAKAKIS(join tree T, relations R_u, output attributes O)
L1  for each non-root u in post-order: R_parent(u) ← R_parent(u) ⋉ R_u
L2  for each non-root u in pre-order:  R_u ← R_u ⋉ R_parent(u)
L3  for each node u in post-order do
L4      J_u ← R_u
L5      for each child c of u do J_u ← J_u ⋈ J_c                 ▷ hash join
L6      J_u ← π over (attributes shared with the parent, and O) of J_u
L7  return J_root
```

Lines L1 and L2 are the full reducer. Each semijoin $R \ltimes S$ keeps the tuples of $R$ that agree with some tuple of $S$ on the shared attributes; it is a hash set build and a probe. Line L6 drops the attributes that are not output attributes and that no node above $u$ holds; for a full join it drops nothing.

## Example

The root is $R(A, B)$, with two children $S(B, C)$ and $T(A, D)$:

- $R = \{(1,1), (1,2), (2,3)\}$, $S = \{(1,5), (3,6), (4,7)\}$, $T = \{(1,8), (1,9), (3,9)\}$.

| step | semijoin | shared attribute | result |
|---|---|---|---|
| up | $R \leftarrow R \ltimes T$ | $A \in \{1, 3\}$ | $\{(1,1), (1,2)\}$ |
| up | $R \leftarrow R \ltimes S$ | $B \in \{1, 3, 4\}$ | $\{(1,1)\}$ |
| down | $S \leftarrow S \ltimes R$ | $B \in \{1\}$ | $\{(1,5)\}$ |
| down | $T \leftarrow T \ltimes R$ | $A \in \{1\}$ | $\{(1,8), (1,9)\}$ |

Each remaining tuple is part of an output tuple. The join phase gives $(A, B, C, D) = (1, 1, 5, 8)$ and $(1, 1, 5, 9)$. With $O = \{C\}$ the answer is $\{(5)\}$.

**Why the reduction matters.** Take the path $R(A, B), S(B, C), T(C, D)$ with $R = \{(i, 0) : i < m\}$, $S = \{(0, j) : j < m\}$ and $T = \{(m + 1, 0)\}$. The output is empty, but the plan $(R \bowtie S) \bowtie T$ first builds $m^2$ tuples. The full reducer empties all three relations first, so the Yannakakis algorithm builds no intermediate tuple at all.

## Correctness

Three facts give correctness. After the bottom-up pass, each $R_u$ is the projection of the join of its subtree on its own attributes: a tuple survives exactly when it extends into each child's subtree, and by running intersection the subtrees of different children share only attributes of $u$. After the top-down pass, each $R_u$ is the projection of the whole join: a tuple that survives extends into its subtree and agrees with a parent tuple that extends to the rest of the tree, and the two parts share only attributes of $u$ and its parent. Finally, the attributes dropped at line L6 occur nowhere above $u$, so dropping them early does not change the result. The full proof is in the proof file.

## Complexity

- **Full reducer.** $2(r - 1)$ semijoins, each linear in the sizes of its two relations with hashing: $O(n)$ for a fixed query, $O(r n)$ in general.
- **Full joins.** After the reduction, each partial join is a projection of the output, so it has at most $z$ tuples. Each of the $r - 1$ hash joins costs $O(|R_u| + z)$, so the join phase costs $O(n + r z)$, and the whole algorithm runs in $O(n + z)$ for a fixed query.
- **Projections.** With output attributes $O$, each partial result has at most $|R_u| \cdot z$ tuples, and the time is $O(r n z)$. This is Yannakakis's polynomial bound. For *free-connex* acyclic queries, Bagan, Durand and Grandjean (2007) showed that $O(n + z)$ time is possible. They also showed that, for self-join-free acyclic queries that are not free-connex, this needs a fast algorithm for Boolean matrix multiplication.
- **Boolean queries.** Whether the join is empty is decided by the bottom-up pass alone, in $O(n)$ time for a fixed query.

## Properties

- **No dangling tuples.** After the full reducer, every tuple of every relation takes part in the output. The relations are *globally consistent*.
- **Order free.** Any join order that follows the tree is safe after the reduction; no cost model is needed to avoid blow-up.
- **Only for acyclic queries.** A cyclic query such as the triangle has no full reducer of semijoins: pairwise consistent relations can still have an empty join.
- **Output sensitive.** The cost depends on the output size, unlike worst-case optimal joins, which pay up to the AGM bound even when the output is small.

## Variants and improvements

- **Semijoin programs.** Bernstein and Chiu (1981) studied semijoin programs for distributed queries, where semijoins cut the data shipped between sites; the full reducer is the case for tree queries.
- **[Bloom join](/bloom-join/).** Replaces exact semijoins by Bloom filter probes; some dangling tuples may survive, but the filters are small to ship. Recent systems use this to make hash join plans robust on acyclic queries.
- **Constant-delay enumeration.** For free-connex queries, after a linear preprocessing, answers can be listed with constant delay between them.
- **Cyclic queries.** Combine with a [tree decomposition](/tree-decomposition/): join the relations in each bag (for example with [generic join](/generic-join/)), then run the Yannakakis algorithm on the tree of bags. The cost is then governed by the fractional hypertree width.
- **Aggregates.** The same tree pass computes counts, sums and other semiring aggregates over the join without listing it, as in the sum-product algorithm on a [junction tree](/junction-tree/).

## When to use it

Use the Yannakakis algorithm for acyclic joins with many dangling tuples or skewed keys, where a pairwise plan can create intermediate results much larger than the output: star and snowflake schemas, path queries over graphs, and foreign-key chains with selective filters. When all joins follow foreign keys and no filter removes tuples, the reduction removes nothing and costs an extra pass.

## Pitfalls

- **The tree must have running intersection.** A spanning tree of the relations that does not satisfy it gives wrong results after the reduction; build the tree with GYO or a maximum-weight spanning tree on shared attributes.
- **Two passes are needed.** The bottom-up pass alone makes only the root consistent; the top-down pass is needed for the others.
- **Projection is not free.** With a projection, the intermediate results can be larger than both input and output, up to $|R_u| \cdot z$. Only free-connex queries avoid this.
- **Bag semantics.** Semijoins do not change multiplicities, but the join phase must keep counts if the query has bag semantics.

## Implementations

## History

Bernstein and Chiu (1981) studied semijoins as a tool for distributed queries and showed that tree queries have full reducers. Yannakakis (VLDB 1981) gave the algorithm for acyclic joins with projections, with time polynomial in input and output. Beeri, Fagin, Maier and Yannakakis (1983) showed that alpha-acyclicity is equivalent to the existence of a join tree, of a full reducer, and to the property that pairwise consistency implies global consistency. Bagan, Durand and Grandjean (2007) found the class of free-connex queries, for which linear time in input plus output is possible.

## References
