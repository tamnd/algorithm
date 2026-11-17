---
tag: 12B9JK
kind: definition
slug: acyclic-hypergraph
name: Acyclic hypergraph
aliases:
- alpha-acyclic hypergraph
- acyclic database schema
area: databases/relational-theory
level: core
summary: A hypergraph whose edges can be arranged in a tree so that the edges that contain any vertex form a connected subtree.
prereqs: [hypergraph, tree]
see_also: [gyo-reduction, yannakakis-algorithm, acyclic-join-evaluation, semijoin, hypertree-width, chordal-graph, junction-tree, tree-structured-csp]
sources:
  - paper: doi:10.1145/2402.322389
    title: Catriel Beeri, Ronald Fagin, David Maier and Mihalis Yannakakis, On the desirability of acyclic database schemes, Journal of the ACM 30(3), 479 to 513 (1983)
    locator: the equivalence of join trees, the Graham reduction, conformal and chordal hypergraphs, full reducers, and global consistency from pairwise consistency
  - paper: doi:10.1145/2402.322390
    title: Ronald Fagin, Degrees of acyclicity for hypergraphs and relational database schemes, Journal of the ACM 30(3), 514 to 550 (1983)
    locator: alpha, beta, gamma and Berge acyclicity and the strict chain between them
  - paper: doi:10.1137/0213035
    title: Robert E. Tarjan and Mihalis Yannakakis, Simple linear-time algorithms to test chordality of graphs, test acyclicity of hypergraphs, and selectively reduce acyclic hypergraphs, SIAM Journal on Computing 13(3), 566 to 579 (1984)
    locator: the linear-time test for alpha-acyclicity
  - paper: doi:10.1006/jcss.2001.1809
    title: Georg Gottlob, Nicola Leone and Francesco Scarcello, Hypertree decompositions and tractable queries, Journal of Computer and System Sciences 64(3), 579 to 627 (2002)
    locator: a hypergraph is acyclic if and only if its hypertree width is 1
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 6 (static analysis and optimization), the section on acyclic joins
---

An acyclic hypergraph is a [hypergraph](/hypergraph/) whose edges can be placed at the nodes of a [tree](/tree/) so that, for each vertex, the edges that contain it form a connected part of the tree. Such a tree is a *join tree*. In databases the vertices are attributes or query variables and the edges are relation schemes or query atoms. Beeri, Fagin, Maier and Yannakakis (1983) showed that many good properties of a database schema are each equivalent to this one condition, and acyclic [conjunctive queries](/conjunctive-query/) can be evaluated in polynomial time by the [Yannakakis algorithm](/yannakakis-algorithm/). The [GYO reduction](/gyo-reduction/) tests the condition. The usual name in the theory is *alpha-acyclic*, since Fagin (1983) also defined the stronger beta, gamma and Berge forms.

## Definition

A hypergraph $H = (V, E)$ has a finite set $V$ of vertices and a finite list $E = (e_1, \ldots, e_m)$ of edges, each a subset of $V$.

**Definition (Beeri, Fagin, Maier and Yannakakis 1983).** A *join tree* of $H$ is a tree $T$ on the nodes $1, \ldots, m$ such that for each vertex $x \in V$ the set $\{ i : x \in e_i \}$ induces a connected subtree of $T$. This is the *running intersection property*. $H$ is *alpha-acyclic*, or simply *acyclic*, if it has a join tree. A hypergraph with no edges is acyclic.

An equal way to state the running intersection property: for any two nodes $i$ and $j$ of $T$, the set $e_i \cap e_j$ is contained in every edge on the path from $i$ to $j$.

**Equivalent conditions (Beeri, Fagin, Maier and Yannakakis 1983).** For a hypergraph $H$ the following are equivalent, among others:

1. $H$ has a join tree.
2. The [GYO reduction](/gyo-reduction/), which deletes vertices that are in one edge only and edges that are inside other edges, ends with at most one edge.
3. $H$ is *conformal* and *chordal*. The *primal graph* of $H$ has the vertices of $H$ and an edge between two vertices that share an edge of $H$. $H$ is chordal if the primal graph is a [chordal graph](/chordal-graph/), and conformal if each [clique](/clique/) of the primal graph lies inside one edge of $H$.
4. $H$ has a *full reducer*: one program of [semijoins](/semijoin/) that, on every database over the schema $H$, deletes exactly the tuples that take part in no tuple of the full join.
5. Each database over $H$ whose relations are pairwise consistent, so that each two relations agree on their common attributes, is globally consistent: each relation is the projection of the full join.

Tarjan and Yannakakis (1984) test acyclicity in linear time in the total size of the edges, with maximum cardinality search.

**Degrees of acyclicity (Fagin 1983).** Each degree below implies the next one, and none of the implications can be reversed.

- *Berge-acyclic*: the bipartite incidence graph, with one node per vertex and one per edge, has no cycle. In particular, two edges share at most one vertex.
- *Gamma-acyclic*: $H$ has no gamma-cycle, a kind of cycle that Fagin defined with a few extra conditions on the shared vertices.
- *Beta-acyclic*: every set of edges of $H$ forms an alpha-acyclic hypergraph.
- *Alpha-acyclic*: as above.

## Examples and non-examples

- **A path.** The edges $AB$, $BC$, $CD$ form a join tree $AB - BC - CD$. The hypergraph is Berge-acyclic.
- **A star.** The edges $AB$, $AC$, $AD$ form a join tree with $AB$ in the middle, or any other edge in the middle, since all of them share only $A$.
- **A chain of relations with wider overlaps.** The edges $ABC$, $BCD$, $CDE$ form the join tree $ABC - BCD - CDE$. Vertex $C$ is in all three, and the path is connected. The hypergraph is alpha-acyclic and beta-acyclic, but not Berge-acyclic, because $ABC$ and $BCD$ share two vertices.
- **Non-example: the triangle.** The edges $AB$, $BC$, $CA$ have no join tree. In any tree on the three nodes, one node, say $AB$, lies between the other two, and then $C$, which is in $BC$ and $CA$, must be in $AB$. In condition 3, the primal graph is a triangle, a chordal graph, but the clique $ABC$ is in no edge, so $H$ is not conformal.
- **Adding an edge can make a hypergraph acyclic.** The edges $AB$, $BC$, $CA$, $ABC$ have the join tree with $ABC$ in the middle and the other three edges as leaves. So the hypergraph is alpha-acyclic. It is not beta-acyclic, because the subset $AB$, $BC$, $CA$ is the triangle. Removing an edge from an alpha-acyclic hypergraph can make it cyclic.
- **Non-example: a cycle of four edges with a chord.** The edges $AB$, $BC$, $CD$, $DA$, $AC$ are cyclic. The primal graph is chordal, but the clique $ABC$ is in no edge. With the two edges $ABC$ and $ACD$ added, the hypergraph becomes acyclic.
- **Queries.** $Q(x, z) \mathbin{:\!-} R(x, y), S(y, z)$ is an acyclic query. The triangle query $Q() \mathbin{:\!-} R(x, y), S(y, z), T(z, x)$ is not.

## Related definitions

- **Join tree and GYO.** The [GYO reduction](/gyo-reduction/) builds a join tree when one exists. The order in which it deletes edges is a bottom-up order of the tree.
- **Yannakakis algorithm.** For an acyclic conjunctive query, the [Yannakakis algorithm](/yannakakis-algorithm/) runs semijoins along a join tree and then joins, in time polynomial in the input plus the output. See also [acyclic join evaluation](/acyclic-join-evaluation/).
- **Hypertree width.** Acyclic hypergraphs are exactly the hypergraphs of [hypertree width](/hypertree-width/) 1 (Gottlob, Leone and Scarcello 2002). Hypertree width and [fractional hypertree width](/fractional-hypertree-width/) measure how far a hypergraph is from acyclic.
- **Chordal graphs and junction trees.** A graph is chordal if and only if the hypergraph of its maximal cliques is acyclic, and a join tree of that hypergraph is a clique tree, the [junction tree](/junction-tree/) of probabilistic inference.
- **Tree-structured CSPs.** A [constraint satisfaction problem](/tree-structured-csp/) whose constraint hypergraph is acyclic is solved by the same semijoin passes, which are directional arc consistency on the join tree.

## References
