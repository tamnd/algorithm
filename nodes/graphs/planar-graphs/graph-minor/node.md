---
tag: S27CJA
kind: definition
slug: graph-minor
name: Graph minor
aliases:
- minor
area: graphs/planar-graphs
level: core
summary: A graph obtained from another by deleting vertices, deleting edges, and contracting edges.
prereqs: [subgraph, connected-graph, simple-graph]
see_also: [wagner-theorem, kuratowski-theorem, graph-minor-theorem, minor-testing, hadwiger-conjecture, treewidth, grid-minor-theorem, planar-graph]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.7, Contraction and minors (the definitions by contraction and by branch sets, topological minors, and the proposition that minors and topological minors agree for graphs of maximum degree 3); Chapter 12, Minors, trees and WQO
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 6.2, Characterization of planar graphs (minors, subdivisions and Wagner's theorem)
  - paper: doi:10.1016/j.jctb.2004.08.001
    title: Neil Robertson and Paul D. Seymour, Graph Minors. XX. Wagner's conjecture, Journal of Combinatorial Theory, Series B 92(2), 325 to 357 (2004)
    locator: the main theorem (every minor-closed class has a finite set of forbidden minors)
---

A graph $H$ is a minor of a graph $G$ if $H$ can be obtained from a [subgraph](/subgraph/) of $G$ by contracting edges, that is, by merging the two ends of an edge into one vertex. Equivalently, $G$ contains disjoint connected pieces, one for each vertex of $H$, with an edge of $G$ between two pieces whenever the corresponding vertices of $H$ are adjacent. Minors are the order in which [planar graphs](/planar-graph/) have their cleanest description: a graph is planar exactly when neither $K_5$ nor $K_{3,3}$ is a minor of it ([Wagner's theorem](/wagner-theorem/)). The [graph minor theorem](/graph-minor-theorem/) of Robertson and Seymour extends this to every class of graphs that is closed under taking minors.

## Definition

All graphs are finite and [simple](/simple-graph/). For a graph $G = (V, E)$ and an edge $e = uv$, the **contraction** $G / e$ is the graph obtained by deleting $u$ and $v$ and adding a new vertex $w$ adjacent to every vertex of $(N(u) \cup N(v)) \setminus \{u, v\}$. Loops and parallel edges do not arise, because the neighbourhood is taken as a set.

**Definition (by operations).** A graph $H$ is a **minor** of $G$, written $H \preceq G$, if a graph isomorphic to $H$ can be obtained from $G$ by a finite sequence of vertex deletions, edge deletions and edge contractions.

**Definition (by branch sets).** A **model** of $H$ in $G$ is a family $(V_h)_{h \in V(H)}$ of pairwise disjoint nonempty sets $V_h \subseteq V(G)$, the *branch sets*, such that each induced subgraph $G[V_h]$ is [connected](/connected-graph/), and for each edge $hh'$ of $H$ some edge of $G$ joins $V_h$ to $V_{h'}$.

The two definitions agree (Diestel, Section 1.7): $H \preceq G$ exactly when $G$ has a model of $H$. Given a model, delete the vertices outside all branch sets, contract a spanning tree of each $G[V_h]$ to one vertex, and delete the edges that do not correspond to edges of $H$. Conversely, each operation keeps a model: track for each vertex of the current graph the set of original vertices merged into it; these sets are connected and pairwise disjoint, and an edge between two current vertices comes from an edge of $G$ between their sets.

A **proper** minor is a minor that is not isomorphic to $G$. A class $\mathcal{C}$ of graphs is **minor-closed** if every minor of a graph in $\mathcal{C}$ is in $\mathcal{C}$. For a set $\mathcal{F}$ of graphs, $\mathrm{Forb}(\mathcal{F})$ is the class of graphs with no minor in $\mathcal{F}$; the members of a minimal such $\mathcal{F}$ are the **forbidden minors** (or excluded minors) of the class.

**Embedded graphs.** The definition needs no embedding. If $G$ is given with a planar embedding as a [rotation system](/rotation-system/), deletion removes the edge from two rotations, and contraction of $uv$ merges the rotation of $u$ and the rotation of $v$ at the position of the edge: the neighbours of $u$ after $v$, then the neighbours of $v$ after $u$. Both operations keep the embedding plane, which is why every minor of a planar graph is planar.

## Examples and non-examples

| $G$ | $H$ | $H \preceq G$? | reason |
|---|---|---|---|
| any graph with a vertex | $K_1$ | yes | delete all other vertices |
| the cycle $C_n$, $n \ge 3$ | $K_3$ | yes | contract $n - 3$ edges of the cycle |
| a forest | $K_3$ | no | deletion and contraction of a forest give a forest |
| a path | $K_{1,3}$ | no | every minor of a path is a disjoint union of paths |
| $K_4$ | $C_4$ | yes | delete the two edges of a perfect matching |
| the Petersen graph | $K_5$ | yes | contract the five spokes; each branch set $\{i, i'\}$ meets the other four |
| the Petersen graph | $K_5$ as a topological minor | no | a subdivision of $K_5$ needs vertices of degree 4, and the Petersen graph is 3-regular |
| $K_{3,3}$ | $K_5$ | no | a minor has at most as many edges as $G$, and $9 < 10$ |
| any planar graph | $K_5$, $K_{3,3}$ | no | minors of planar graphs are planar, and these two are not |
| a large enough square grid | any planar graph | yes | every planar graph is a minor of some grid; see the [grid minor theorem](/grid-minor-theorem/) |

In the Petersen graph with outer cycle $0, 1, 2, 3, 4$, spokes $i i'$ and inner edges $i' (i+2)'$ (indices mod 5), the branch set $\{i, i'\}$ is joined to $\{i \pm 1, (i \pm 1)'\}$ by an outer edge and to $\{i \pm 2, (i \pm 2)'\}$ by an inner edge, so the five branch sets give $K_5$.

The forest row uses an invariant of the operations: deleting a vertex or an edge cannot create a cycle, and contracting an edge of a forest gives a forest, since a cycle through the new vertex $w$ would come from a cycle or a path between $u$ and $v$ other than the edge $uv$ in the forest.

## Related definitions

- **Subdivision and topological minor.** A *subdivision* of $H$ replaces edges of $H$ by paths whose inner vertices are new. $H$ is a **topological minor** of $G$ if $G$ has a subgraph that is a subdivision of $H$. Every topological minor is a minor (contract the paths). If $H$ has maximum degree at most 3, every minor $H$ of $G$ is also a topological minor (Diestel, Section 1.7). The Petersen graph shows that this fails for $K_5$. [Kuratowski's theorem](/kuratowski-theorem/) uses topological minors and [Wagner's theorem](/wagner-theorem/) uses minors; they describe the same class.
- **Induced minor.** Only vertex deletions and contractions are allowed, no edge deletions.
- **Minor order.** On isomorphism classes of finite graphs, $\preceq$ is a partial order: reflexive, transitive (compose the operations), and antisymmetric, because a proper minor has fewer vertices or fewer edges. The [graph minor theorem](/graph-minor-theorem/) says that it is a well-quasi-order: every infinite sequence $G_1, G_2, \ldots$ has $i < j$ with $G_i \preceq G_j$.
- **Minor-closed classes and their obstructions.** Forests are $\mathrm{Forb}(K_3)$. Planar graphs are $\mathrm{Forb}(K_5, K_{3,3})$. [Outerplanar graphs](/outerplanar-graph/) are $\mathrm{Forb}(K_4, K_{2,3})$. Graphs of [treewidth](/treewidth/) at most 2 are $\mathrm{Forb}(K_4)$. Graphs embeddable on a fixed surface ([graph genus](/graph-genus/) at most $g$) form a minor-closed class, so they have a finite set of forbidden minors.
- **Minor testing.** For a fixed $H$, deciding $H \preceq G$ takes polynomial time in the size of $G$ (cubic by Robertson and Seymour); with $H$ part of the input it is [NP-complete](/np-complete/). See [minor testing](/minor-testing/).
- **Hadwiger number.** The largest $k$ with $K_k \preceq G$. [Hadwiger's conjecture](/hadwiger-conjecture/) says that it is at least the [chromatic number](/chromatic-number/).

## References
