---
tag: AMABKP
kind: algorithm
slug: gyo-reduction
name: GYO reduction
aliases:
- Graham-Yu-Ozsoyoglu reduction
- GYO algorithm
- Graham reduction
area: databases/relational-theory
level: core
summary: Test whether a hypergraph is alpha-acyclic by repeatedly deleting vertices in one edge only and edges contained in another edge.
model: word-ram
complexity:
  vars: {m: the number of edges, v: the number of vertices}
  time: {worst: O(m^3 v^2)}
  space: {extra: O(m v)}
prereqs: [hypergraph, acyclic-hypergraph]
see_also: [acyclic-join-evaluation, yannakakis-algorithm, semijoin, hypertree-width, chordal-graph, maximum-cardinality-search, tree-structured-csp, conjunctive-query]
sources:
  - paper: "M. H. Graham, On the universal relation, Technical report, University of Toronto (1979)"
    locator: the reduction by the two deletion rules
  - paper: doi:10.1109/CMPSAC.1979.762509
    title: "Clement T. Yu and M. Zehra Ozsoyoglu, An algorithm for tree-query membership of a distributed query, Proceedings of COMPSAC 79, IEEE Computer Society, 306 to 312 (1979)"
    locator: the reduction used to decide whether a query is a tree query
  - paper: doi:10.1145/2402.322389
    title: Catriel Beeri, Ronald Fagin, David Maier and Mihalis Yannakakis, On the desirability of acyclic database schemes, Journal of the ACM 30(3), 479 to 513 (1983)
    locator: the theorem that a hypergraph is acyclic if and only if the Graham reduction ends with an empty hypergraph, among the other equivalent conditions
  - paper: doi:10.1137/0213035
    title: Robert E. Tarjan and Mihalis Yannakakis, Simple linear-time algorithms to test chordality of graphs, test acyclicity of hypergraphs, and selectively reduce acyclic hypergraphs, SIAM Journal on Computing 13(3), 566 to 579 (1984)
    locator: the linear-time acyclicity test by maximum cardinality search
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 6 (static analysis and optimization), the section on acyclic joins, with the GYO algorithm and join trees
---

The GYO reduction decides whether a [hypergraph](/hypergraph/) is [alpha-acyclic](/acyclic-hypergraph/). It applies two deletion rules while one of them applies: delete a vertex that is in only one edge, and delete an edge that is a subset of another edge. The hypergraph is alpha-acyclic if and only if at most one edge is left at the end, and the edge deletions then give a *join tree*. In databases the vertices are the attributes or variables of a query and the edges are its relations, so the test tells whether a [join](/relational-join/) can be evaluated by the [Yannakakis algorithm](/yannakakis-algorithm/) without first combining relations. The name comes from Graham, and from Yu and Ozsoyoglu, who found the reduction independently in 1979.

## In plain words

Think of each table of a query as a set of column names. Some columns occur in only one table. They do not connect that table to any other table, so you can forget them. Some tables, after this, have only columns that another table also has. Such a table hangs off the other table like a leaf off a branch, so you can put it aside and remember where it hangs.

Do these two steps again and again. If everything goes away except one table, the tables fit together like a tree, and the remembered "hangs off" links are that tree. If you get stuck with two or more tables, the tables form a real cycle, such as three tables that each share one column with the next one.

## The problem

A hypergraph $H = (V, E)$ has a finite set $V$ of vertices and a finite list $E = (e_1, \ldots, e_m)$ of edges, each a subset of $V$. Equal edges and empty edges are allowed. A *join tree* of $H$ is a tree $T$ whose nodes are the indices $1, \ldots, m$, such that for each vertex $x$ the set $\{ i : x \in e_i \}$ induces a connected subtree of $T$ (the *running intersection property*). $H$ is *alpha-acyclic* if it has a join tree. The hypergraph with no edges is alpha-acyclic.

**Input.** A hypergraph $H$. **Output.** Whether $H$ is alpha-acyclic, and if it is, a join tree.

For a [conjunctive query](/conjunctive-query/) $Q(\bar x) \mathbin{:\!-} R_1(\bar u_1), \ldots, R_m(\bar u_m)$, the hypergraph has the variables as vertices and one edge $\mathrm{var}(\bar u_i)$ per atom. For a natural join of relations $R_1, \ldots, R_m$, the edges are the attribute sets $\mathrm{att}(R_i)$.

## The algorithm

The algorithm changes a copy $c_i$ of each edge and keeps a set $A$ of the edges that are still there.

```pseudo id=main
GYO(e_1, ..., e_m)
L1  c_i ← e_i for each i;  A ← {1, ..., m};  parent ← empty map
L2  loop
L3      if some vertex x is in c_i for exactly one i in A then
L4          c_i ← c_i − {x}                         ▷ ear rule
L5      else if there are i ≠ j in A with c_i ⊆ c_j then
L6          A ← A − {i};  parent[i] ← j               ▷ containment rule
L7      else exit the loop
L8  return (|A| ≤ 1, parent)
```

Line L4 is the *ear rule*: the vertex $x$ connects $e_i$ to no other edge. Line L6 is the *containment rule*: after the deletions, every vertex of $c_i$ is also in $c_j$, so $e_i$ can hang from $e_j$ in the tree. An empty $c_i$ is a subset of any other edge, so it goes too. When one edge is left, line L4 empties it, and the loop stops. The pairs $\{i, \mathit{parent}[i]\}$ are the edges of the join tree, and the last edge of $A$ is its root.

Either rule may be applied first, and the choice does not change the answer (see Correctness). Two equal edges are a case of line L5: one of them goes.

## Example

The query $Q \mathbin{:\!-} R_1(A, B, C), R_2(B, C, D), R_3(C, D, E), R_4(D, F), R_5(A, B)$ has the edges $e_1 = ABC$, $e_2 = BCD$, $e_3 = CDE$, $e_4 = DF$ and $e_5 = AB$. The run below always takes the ear rule first, with the smallest vertex, and else the containment pair $(i, j)$ with the smallest $i$, then the smallest $j$.

| step | rule | the edges after the step |
|---|---|---|
| 1 | ear: $E$ only in $e_3$ | $e_1 = ABC$, $e_2 = BCD$, $e_3 = CD$, $e_4 = DF$, $e_5 = AB$ |
| 2 | ear: $F$ only in $e_4$ | $e_1 = ABC$, $e_2 = BCD$, $e_3 = CD$, $e_4 = D$, $e_5 = AB$ |
| 3 | containment: $e_3 \subseteq e_2$, parent 2 | $e_1 = ABC$, $e_2 = BCD$, $e_4 = D$, $e_5 = AB$ |
| 4 | containment: $e_4 \subseteq e_2$, parent 2 | $e_1 = ABC$, $e_2 = BCD$, $e_5 = AB$ |
| 5 | ear: $D$ only in $e_2$ | $e_1 = ABC$, $e_2 = BC$, $e_5 = AB$ |
| 6 | containment: $e_2 \subseteq e_1$, parent 1 | $e_1 = ABC$, $e_5 = AB$ |
| 7 | ear: $C$ only in $e_1$ | $e_1 = AB$, $e_5 = AB$ |
| 8 | containment: $e_1 \subseteq e_5$, parent 5 | $e_5 = AB$ |
| 9, 10 | ear: $A$, then $B$ | $e_5 = \emptyset$ |

One edge is left, so the hypergraph is alpha-acyclic. The join tree has the edges $e_3 - e_2$, $e_4 - e_2$, $e_2 - e_1$ and $e_1 - e_5$. The check for $D$: it is in $e_2$, $e_3$ and $e_4$, and these three nodes are connected through $e_2$.

Now add the atom $R_6(A, D)$, an edge $e_6 = AD$. Steps 1 to 4 are the same, and then $e_5 = AB$ goes into $e_1 = ABC$. The edges left are $ABC$, $BCD$ and $AD$. Each vertex is in two of them, and no edge is inside another one, so both rules stop with three edges. The hypergraph is not alpha-acyclic: $ABC$ and $BCD$ share $B$ and $C$, $BCD$ and $AD$ share $D$, and $AD$ and $ABC$ share $A$, and no edge holds all of $A$, $C$ and $D$. The smallest cyclic case is the triangle $AB$, $BC$, $CA$, where no rule applies at all.

## Correctness

Let $D$ be the set of vertices that the ear rule has deleted so far. The run keeps the invariant that $c_i = e_i \setminus D$ for each $i \in A$, and that no vertex of $D$ is in any $c_i$ with $i \in A$. A vertex is deleted only when it is in one remaining edge, so after that it is in none.

- **If at most one edge is left, the parent links form a join tree.** Take the edges in the reverse order of their deletion. When $e_i$ is deleted into $e_j$, each vertex of $e_i$ that is also in a later edge is not yet in $D$, so it is in $c_i \subseteq c_j \subseteq e_j$. So $e_i$ hangs from an edge that holds all the vertices that it shares with the rest of the tree, and the running intersection property holds.
- **If $H$ has a join tree, the run ends with at most one edge, in any order of the rules.** While two or more edges are left, take a leaf $\ell$ of a join tree and its neighbor $p$. Each vertex of $c_\ell$ that is also in another edge is in $c_p$, by the running intersection property. So either some vertex of $c_\ell$ is in no other edge (line L4 applies) or $c_\ell \subseteq c_p$ (line L5 applies). Each rule keeps a join tree: after line L4 the same tree works, and after line L6 the neighbors of $i$ are joined to $j$.

The loop stops, because each step deletes one vertex occurrence or one edge, so there are at most $\sum_i |e_i| + m$ steps. The full proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

The bounds are in the [word RAM](/word-ram/) model, for a hypergraph with $m$ edges and $v$ vertices, given as lists of vertices. Let $s = \sum_i |e_i| \le m v$ be its size.

- **Number of steps.** At most $s + m$, since each step deletes a vertex from an edge or an edge from $A$.
- **The plain implementation.** Before each step, count the occurrences of each vertex in $O(s)$ time with a dictionary, and if there is no ear, test all pairs for containment in $O(m^2 v)$ time with sets. That is $O(s + m^2 v)$ per step and $O((s + m)(s + m^2 v)) = O(m^3 v^2)$ in total. The code of this page does this. It keeps the copies $c_i$ and the parent map, in $O(m v)$ extra space.
- **Linear time.** Tarjan and Yannakakis (1984) test alpha-acyclicity in $O(s + v + m)$ time. They order the vertices by [maximum cardinality search](/maximum-cardinality-search/) and check the order, a method that also tests whether a graph is [chordal](/chordal-graph/). A join tree comes out of the same pass.

## Properties

- **The order of the rules does not matter.** Every order of the rules gives the same yes or no answer, by the two parts of the proof above. The join tree can differ.
- **Certificate in both cases.** A yes answer comes with a join tree. A no answer leaves a reduced hypergraph with at least two edges, in which every vertex is in at least two edges and no edge is inside another. These edges show the part of the query that is cyclic.
- **Deterministic and exact.** No heuristic is involved. It decides alpha-acyclicity, not the stronger beta or gamma forms (see [acyclic hypergraph](/acyclic-hypergraph/)).

## Variants and improvements

- **Ears of whole edges.** Some books state one rule: delete an *ear*, an edge $e$ for which some other edge $f$ contains every vertex of $e$ that is also in an edge other than $e$. This deletes the ear vertices of $e$ and the edge $e$ in one step, and it gives the same answer.
- **Join tree output.** Record $\mathit{parent}[i] \leftarrow j$ at line L6, as above. The [Yannakakis algorithm](/yannakakis-algorithm/) then runs its [semijoin](/semijoin/) passes along this tree. The deletion order is a bottom-up order of the tree: each edge is deleted before its parent.
- **Linear-time test.** Use the Tarjan and Yannakakis method when the hypergraph is large.
- **Width measures.** When GYO fails, [hypertree width](/hypertree-width/) and [fractional hypertree width](/fractional-hypertree-width/) measure how far the hypergraph is from acyclic. Acyclic hypergraphs are exactly those with hypertree width 1.

## When to use it

Use GYO in a query optimizer to detect acyclic [conjunctive queries](/conjunctive-query/), which have polynomial evaluation by the Yannakakis algorithm, and to build their join tree. For queries of a few dozen relations the plain version is fast and easy to check. Use the linear-time test of Tarjan and Yannakakis when the hypergraph has thousands of edges, for example in a [constraint satisfaction](/tree-structured-csp/) solver.

## Pitfalls

- **Deleting a vertex too soon.** Line L3 asks for a vertex in exactly one remaining edge. A vertex in two edges that are both still in $A$ must stay; deleting it can make a cyclic hypergraph look acyclic.
- **Containment against the original edges.** Line L5 compares the reduced copies $c_i$ and $c_j$, not the original $e_i$ and $e_j$. In the example, $e_3 = CDE$ is not a subset of $e_2 = BCD$. Only after the ear rule deletes $E$ is $c_3 = CD \subseteq c_2$. A test on the original edges stops there and rejects an acyclic hypergraph.
- **A spanning tree is not a join tree.** A tree that connects the relations that share attributes need not have the running intersection property. Build the tree from the parent links, not from a plain spanning tree of the "shares an attribute" graph.
- **Alpha-acyclicity is not closed under subsets of edges.** The triangle $AB$, $BC$, $CA$ is cyclic, but with the extra edge $ABC$ it is alpha-acyclic. Removing a relation from an acyclic query can make it cyclic.

## Implementations

## History

Graham described the reduction in a 1979 technical report on the universal relation at the University of Toronto. Yu and Ozsoyoglu gave the same reduction at COMPSAC 1979 to decide whether a distributed query is a tree query. Beeri, Fagin, Maier and Yannakakis (1983) proved that the reduction ends with an empty hypergraph exactly when the schema has a join tree, and that this is equivalent to several other conditions, such as the existence of a semijoin full reducer. Tarjan and Yannakakis (1984) gave the linear-time test.

## References
