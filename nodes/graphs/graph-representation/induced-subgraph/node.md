---
tag: V5XE2Q
kind: definition
slug: induced-subgraph
name: Induced subgraph
aliases:
- vertex-induced subgraph
area: graphs/graph-representation
level: intro
summary: Subgraph containing all edges of the original graph between its chosen vertices.
prereqs: [subgraph, graph]
see_also: [subgraph, clique, independent-set, chordal-graph, perfect-graph, line-graph, k-core, subgraph-isomorphism]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4 (Graphs), the subgraph of G induced by a vertex set V'
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 1, Section 1.1 (Graphs), induced subgraphs G[U] and the notation G − U
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.2, the induced subgraph G[T]; Section 7.1, the characterization of line graphs by nine forbidden induced subgraphs (Beineke)
---

The induced subgraph $G[S]$ of a [graph](/graph/) $G$ on a set $S$ of [vertices](/vertex/) has the vertex set $S$ and every [edge](/edge/) of $G$ whose two ends are both in $S$. It is the [subgraph](/subgraph/) you see when you delete all the other vertices and nothing else. Many central objects are induced subgraphs: a [clique](/clique/) is an induced complete graph, an [independent set](/independent-set/) is an induced graph with no edges, and the [k-core](/k-core/) is an induced subgraph. Many graph classes, such as [chordal](/chordal-graph/), [perfect](/perfect-graph/) and [line graphs](/line-graph/), are defined by the induced subgraphs they do not contain.

## Definition

Let $G = (V, E)$ be a [directed](/directed-graph/) or [undirected](/undirected-graph/) graph and $S \subseteq V$. The **subgraph induced by $S$** is

$$G[S] = \big(S,\ \{e \in E : \text{both ends of } e \text{ lie in } S\}\big).$$

For a directed graph, the edge set is $E \cap (S \times S)$. For an undirected graph, it is $\{\{u, v\} \in E : u, v \in S\}$. A [self-loop](/self-loop/) at $v$ belongs to $G[S]$ when $v \in S$. In a [multigraph](/multigraph/), $G[S]$ keeps every parallel edge between vertices of $S$.

A graph $H$ is an **induced subgraph** of $G$ if $H = G[S]$ for some $S \subseteq V$. Equivalently, $H \subseteq G$ and each edge of $G$ between two vertices of $H$ is an edge of $H$. We also write $G - U = G[V \setminus U]$ for the graph left after deleting the vertex set $U$.

**$G$ contains $H$ as an induced subgraph** (for graphs given up to isomorphism) if there is an injective map $f : V(H) \to V(G)$ such that for all distinct $x, y \in V(H)$,

$$(x, y) \in E(H) \iff (f(x), f(y)) \in E(G).$$

The "if" direction is what separates this from the plain subgraph relation, which needs only "$\Rightarrow$". A graph is **$H$-free** if it has no induced subgraph isomorphic to $H$.

**Basic facts.**

- There are exactly $2^n$ induced subgraphs of a graph with $n$ vertices, one for each $S \subseteq V$, because $S$ determines the edges.
- $G[S][T] = G[T]$ for $T \subseteq S$: inducing twice is inducing once.
- $\overline{G[S]} = \overline{G}[S]$: the [complement](/complement-graph/) of an induced subgraph is the induced subgraph of the complement. So $S$ is a clique of $G$ if and only if it is an independent set of $\overline{G}$.
- A graph property is **hereditary** if each induced subgraph of a graph with the property has it too. Being a forest, bipartite, planar, chordal, perfect or a line graph are all hereditary. Each hereditary property is the class of graphs with no induced subgraph in some set of forbidden graphs: take the minimal graphs that lack the property.

**Computing $G[S]$.** From an [adjacency list](/adjacency-list/): mark the vertices of $S$ in an array of $n$ flags, give them the new names $0, \ldots, |S| - 1$, and for each $u \in S$ copy the neighbours $v$ of $u$ that are marked. The time is $\Theta(|S| + \sum_{u \in S} d(u))$ plus $O(n)$ to clear the flags, or $O(1)$ for them with a [hash-based](/hash-based-adjacency/) set. From an [adjacency matrix](/adjacency-matrix/), $G[S]$ is the submatrix on the rows and columns of $S$, in $\Theta(|S|^2)$ time.

## Examples and non-examples

Let $G$ have $V = \{1, 2, 3, 4, 5\}$ and $E = \{12, 13, 23, 24, 34, 45\}$.

| $S$ | edges of $G[S]$ | what it is |
|---|---|---|
| $\{1, 2, 3\}$ | $12, 13, 23$ | a triangle, so $\{1, 2, 3\}$ is a clique |
| $\{1, 4\}$ | none | an independent set |
| $\{1, 5\}$ | none | an independent set |
| $\{1, 2, 4, 5\}$ | $12, 24, 45$ | an induced path on 4 vertices |
| $\{2, 3, 4, 5\}$ | $23, 24, 34, 45$ | a triangle with a pendant edge |
| $V$ | all six | $G$ itself |

**Non-example.** The path $(\{1, 2, 3, 4\}, \{12, 23, 34\})$ is a subgraph of $G$, but not an induced one: $13$ and $24$ are edges of $G$ between its vertices. The graph $G$ still contains a path on 4 vertices as an induced subgraph, on $\{1, 2, 4, 5\}$, and also on $\{1, 3, 4, 5\}$.

**A characterization by one forbidden graph.** A graph has no induced path $P_3$ (three vertices $u, v, w$ with $uv, vw \in E$ and $uw \notin E$) if and only if each of its components is a complete graph. *Proof.* If each component is complete, any two vertices of a component are adjacent, so no induced $P_3$ exists. Conversely, let $G$ be $P_3$-free, and let $u$ and $w$ be distinct vertices of one component, joined by a shortest path $u = x_0, x_1, \ldots, x_k = w$. If $k \ge 2$, then $x_0 x_1, x_1 x_2 \in E$ and $x_0 \ne x_2$; with no induced $P_3$, $x_0 x_2 \in E$, which gives a shorter path. So $k = 1$, and $u$ and $w$ are adjacent. $\square$

**Graph classes defined this way.**

- A graph is [chordal](/chordal-graph/) if it has no induced cycle of length 4 or more.
- A graph is a [line graph](/line-graph/) if and only if it has none of nine graphs, one of them the claw $K_{1,3}$, as an induced subgraph (Beineke).
- A graph is [perfect](/perfect-graph/) if each induced subgraph $H$ has chromatic number equal to its clique number. The [strong perfect graph theorem](/strong-perfect-graph-theorem/) says: exactly when it has no induced odd cycle of length at least 5 and no complement of one.
- A graph is a forest if and only if it has no cycle as a subgraph, and then no induced cycle either; here the two relations agree, because a shortest cycle in a graph is always induced.

## Related definitions

- **Subgraph.** The weaker notion, which may drop edges between kept vertices. See [subgraph](/subgraph/).
- **Clique and independent set.** A set $S$ with $G[S]$ complete, or with $G[S]$ edgeless. See [clique](/clique/) and [independent set](/independent-set/).
- **Induced subgraph isomorphism.** Deciding whether $G$ contains $H$ as an induced subgraph is NP-complete when $H$ is part of the input, since $H = K_k$ is the [clique problem](/clique-problem/). It is a variant of [subgraph isomorphism](/subgraph-isomorphism/).
- **k-core.** The [k-core](/k-core/) is $G[S]$ for the largest $S$ such that each vertex has at least $k$ neighbours in $S$.
- **Edge-induced subgraph.** The dual notion: fix an edge set and take all of its ends. See [subgraph](/subgraph/).

## References
