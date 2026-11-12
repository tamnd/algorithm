---
tag: K0Q46K
kind: problem
slug: acyclic-join-evaluation
name: Acyclic join evaluation problem
aliases:
- acyclic conjunctive query evaluation
- alpha-acyclic join evaluation
area: systems/database-algorithms
level: advanced
summary: "Evaluate a join whose hypergraph is alpha-acyclic, that is, has a join tree. It is solvable in time linear in input plus output for full joins."
prereqs: [hypergraph, relational-join, semijoin]
see_also: [yannakakis-algorithm, multiway-join, generic-join, tree-decomposition, treewidth, chordal-graph, junction-tree, agm-bound]
sources:
  - paper: doi:10.1145/2402.322389
    title: Catriel Beeri, Ronald Fagin, David Maier and Mihalis Yannakakis, On the desirability of acyclic database schemes, Journal of the ACM 30(3), 479 to 513 (1983)
    locator: the equivalent conditions for alpha-acyclicity (join tree, GYO reduction, full reducer, pairwise consistency implies global consistency)
  - paper: doi:10.1145/2402.322390
    title: Ronald Fagin, Degrees of acyclicity for hypergraphs and relational database schemes, Journal of the ACM 30(3), 514 to 550 (1983)
    locator: the definitions of alpha-, beta- and gamma-acyclicity and the strict hierarchy between them
  - paper: "Mihalis Yannakakis, Algorithms for acyclic database schemes, Proceedings of the 7th International Conference on Very Large Data Bases (VLDB), 82 to 94 (1981)"
    locator: the evaluation of acyclic joins with semijoins, in time polynomial in input and output
  - paper: "M. H. Graham, On the universal relation, technical report, University of Toronto (1979)"
    locator: the reduction that removes lonely attributes and contained edges
  - paper: "C. T. Yu and M. Z. Ozsoyoglu, An algorithm for tree-query membership of a distributed query, Proceedings of IEEE COMPSAC 1979, 306 to 312"
    locator: the same reduction, as a test for tree queries
  - paper: doi:10.1137/0213035
    title: Robert E. Tarjan and Mihalis Yannakakis, Simple linear-time algorithms to test chordality of graphs, test acyclicity of hypergraphs, and selectively reduce acyclic hypergraphs, SIAM Journal on Computing 13(3), 566 to 579 (1984)
    locator: the linear-time acyclicity test by maximum cardinality search
  - paper: doi:10.1145/382780.382783
    title: Georg Gottlob, Nicola Leone and Francesco Scarcello, The complexity of acyclic conjunctive queries, Journal of the ACM 48(3), 431 to 498 (2001)
    locator: Boolean acyclic conjunctive queries are LOGCFL-complete in combined complexity
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 6, Section 6.4 (acyclic joins, the GYO algorithm and join trees)
---

The acyclic join evaluation problem asks for the result of a natural join, or of a conjunctive query, whose [hypergraph](/hypergraph/) is *alpha-acyclic*: the relations can be put on a tree so that, for each attribute, the relations that hold it form a connected subtree. Such a tree is called a *join tree*. Acyclic joins are the class on which joins are easy: the [Yannakakis algorithm](/yannakakis-algorithm/) evaluates a full acyclic join in time linear in the input plus the output, while cyclic joins such as the triangle cannot avoid intermediate work well beyond the output in general. Acyclicity itself is tested by the GYO reduction, in linear time with the method of Tarjan and Yannakakis.

## In plain words

Each table in a join is a group of column names. Draw the tables as boxes, and try to connect them with lines into a tree, so that for each column name, the boxes that have it are joined to each other through boxes that also have it. If you can, the join is acyclic.

A chain of tables, A to B, B to C, C to D, is acyclic. Three tables A to B, B to C and C to A, the triangle, are not: each pair shares a column, but no tree connects them correctly. An acyclic join can be done by first throwing away all rows that have no partner, which makes every step small.

## Definition

A join query is a [hypergraph](/hypergraph/) $H = (V, E)$: $V$ is the set of attributes, and each edge $e \in E$ is the attribute set of one relation $R_e$. A **join tree** of $H$ is a tree $T$ with node set $E$ such that for each $v \in V$, the set $\{ e \in E : v \in e \}$ induces a connected subtree of $T$ (the *running intersection property*). $H$ is **alpha-acyclic** if it has a join tree.

**GYO reduction.** Repeat the two rules while one of them applies: remove an attribute that occurs in only one edge; remove an edge that is contained in another edge (or is empty). $H$ is alpha-acyclic if and only if the rules reduce it to at most one empty edge (Graham 1979; Yu and Ozsoyoglu 1979). In the equivalent *ear* form, an edge $e$ is an ear with witness $f \ne e$ if every attribute of $e$ that occurs in another edge also occurs in $f$; removing ears one by one and making each witness the parent of its ear builds a join tree.

**The problem.** Given an alpha-acyclic $H$, relations $R_e$ for $e \in E$, and a set $O \subseteq V$ of output attributes, compute

$$\pi_O \Bigl( \mathop{\bowtie}_{e \in E} R_e \Bigr).$$

The case $O = V$ is the **full** join, and $O = \emptyset$ is the **Boolean** query: is the join empty? The input size is $n = \sum_e |R_e|$, and the output size is $z$.

## Variants

- **Full, projected and Boolean queries.** As above. With a projection, the query is an acyclic conjunctive query with free variables $O$.
- **Free-connex queries.** An acyclic query is free-connex if adding the edge $O$ keeps it acyclic. These are exactly the self-join-free acyclic queries that can be answered in $O(n + z)$ time, assuming that Boolean matrix multiplication needs more than quadratic time (Bagan, Durand and Grandjean 2007).
- **Counting and aggregation.** Count the output tuples, or compute a sum over them, without listing them. For acyclic queries without projection, a pass up the join tree does this in $O(n)$ time.
- **Enumeration.** List the answers with small delay after a linear preprocessing.
- **Stronger acyclicity.** Fagin (1983) defined beta-acyclicity (each subset of the edges is alpha-acyclic) and gamma-acyclicity, with Berge-acyclic $\subset$ gamma-acyclic $\subset$ beta-acyclic $\subset$ alpha-acyclic, all strict. Alpha-acyclicity is not closed under removing edges; beta-acyclicity is.

## Examples

| query | edges | acyclic? | reason |
|---|---|---|---|
| path | $AB, BC, CD$ | alpha (and Berge) | the path is a join tree |
| star | $AB, AC, AD$ | alpha (and Berge) | any edge can be the center |
| triangle | $AB, BC, CA$ | no | GYO removes nothing |
| 4-cycle | $AB, BC, CD, DA$ | no | GYO removes nothing |
| covered triangle | $ABC, AB, BC, CA$ | alpha, not beta | $ABC$ covers the triangle, whose edges are a cyclic subset |

**GYO on $AB, BC, CD, BE$.** $AB$ is an ear with witness $BC$: its only shared attribute is $B$, and $B \in BC$. After removing it, $CD$ is an ear with witness $BC$. Then $BC$ is an ear with witness $BE$, because $C$ no longer occurs elsewhere. One edge, $BE$, is left, so the query is acyclic, and the join tree has root $BE$ with child $BC$, whose children are $AB$ and $CD$.

**GYO on the triangle.** Each edge shares both of its attributes with other edges, and no edge contains another, so no rule applies.

**The covered triangle.** $AB$ and $BC$ are ears with witness $ABC$. Then $ABC$ is an ear with witness $CA$, and the query is alpha-acyclic. The subset $\{AB, BC, CA\}$ is the triangle, so the query is not beta-acyclic. Joining $ABC$ with the three binary relations is easy, while joining only the three binary relations is the triangle query.

## Known algorithms

| algorithm | task | time |
|---|---|---|
| GYO reduction (Graham 1979; Yu and Ozsoyoglu 1979) | test acyclicity, build a join tree | polynomial; $O(r^2 w)$ per removal when done directly |
| Tarjan and Yannakakis (1984) | the same, by maximum cardinality search | $O(\sum_e \lvert e \rvert)$ |
| [Yannakakis algorithm](/yannakakis-algorithm/) (1981) | Boolean and full join | $O(n)$ and $O(n + z)$ for a fixed query |
| Yannakakis algorithm with projections | acyclic conjunctive query | $O(n \cdot z)$ for a fixed query |
| Bagan, Durand and Grandjean (2007) | free-connex query | $O(n + z)$, constant delay after $O(n)$ preprocessing |
| [Generic join](/generic-join/), [leapfrog triejoin](/leapfrog-triejoin/) | any full join | within the [AGM bound](/agm-bound/), not output sensitive |

The time bounds with hashing are expected bounds; with sorting they gain a log factor.

## Bounds

- **Linear time is optimal for Boolean and full joins**, because each input tuple must be read and each output tuple written.
- **Combined complexity.** When the query is part of the input, Boolean acyclic query evaluation is LOGCFL-complete (Gottlob, Leone and Scarcello 2001), so it is highly parallelizable. For general conjunctive queries, the same problem is NP-complete (Chandra and Merlin 1977).
- **Projections.** For self-join-free acyclic queries that are not free-connex, $O(n + z)$ time would give Boolean matrix multiplication in $O(n^2)$ time.
- **Output size.** The output can be much larger than the input: $R(A, B) \bowtie S(B, C)$ with one value of $B$ has $|R| \cdot |S|$ tuples. So the right measure is input plus output, and the worst-case output size over inputs of a given size is the AGM bound, as for any join.

## Reductions

- **From bounded-width cyclic queries.** For a [tree decomposition](/tree-decomposition/) of $H$, compute the join of the relations in each bag; the bags then form an acyclic query. This gives time $O(n^w + z)$ for (generalized) hypertree width $w$, and $O(n^{w^*} + z)$ for fractional hypertree width $w^*$ with worst-case optimal joins in the bags.
- **Chordal graphs.** A hypergraph is alpha-acyclic if and only if it is conformal and its primal graph is a [chordal graph](/chordal-graph/) (Beeri, Fagin, Maier and Yannakakis 1983). The join tree of the maximal cliques of a chordal graph is a [junction tree](/junction-tree/).
- **Constraint satisfaction.** A constraint satisfaction problem whose constraint hypergraph is acyclic is a Boolean acyclic query, and is solved by the same bottom-up pass of semijoins.

## Applications

- **Query optimization.** Star and snowflake schemas, foreign-key chains and path queries are acyclic; an optimizer can use semijoin reduction or Bloom filters along the join tree to bound intermediate results.
- **Distributed queries.** Semijoin programs reduce the data shipped between sites; full reducers exist exactly for acyclic queries.
- **Probabilistic inference.** Sum-product message passing on a junction tree is the same computation, with sums and products in place of projections and joins.
- **Database design.** Acyclic schemes have good properties: pairwise consistency of relations implies global consistency, and the universal relation is well defined.

## References
