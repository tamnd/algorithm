---
tag: GBHYW1
kind: definition
slug: graph-isomorphism-definition
name: Isomorphic graphs
aliases:
- graph isomorphism
- isomorphism of graphs
area: graphs/graph-isomorphism
level: intro
summary: Two graphs are isomorphic when a one-to-one relabeling of the vertices of one produces exactly the edges of the other.
prereqs: [graph, simple-graph, permutation]
see_also: [graph-isomorphism-problem, isomorphism-invariant, graph-automorphism-group, subgraph-isomorphism, canonical-labeling, directed-graph, labeled-graph, multigraph]
sources:
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.1, What is a graph? (the definition of an isomorphism, isomorphism as an equivalence relation, and isomorphism classes)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.1, Graphs (isomorphism, graph invariants and the convention that isomorphic graphs are the same)
  - book: isbn:9780387952208
    title: Chris Godsil and Gordon Royle, Algebraic Graph Theory, Springer, Graduate Texts in Mathematics 207, 2001
    locator: Chapter 1, Graphs (Section 1.2, Isomorphisms and automorphisms)
---

Two [graphs](/graph/) are isomorphic when there is a one-to-one map from the vertices of the first onto the vertices of the second that sends edges to edges and non-edges to non-edges. Such a map is an *isomorphism*: it renames the vertices and keeps the structure. Isomorphism is an [equivalence relation](/equivalence-relation/), and graph theory studies properties that hold for whole classes of isomorphic graphs. Deciding whether two given graphs are isomorphic is the [graph isomorphism problem](/graph-isomorphism-problem/).

## Definition

Let $G = (V, E)$ and $H = (W, F)$ be [simple](/simple-graph/) undirected graphs, so that each edge is a 2-element set of vertices. A map $\varphi : V \to W$ is an **isomorphism** from $G$ to $H$ when

1. $\varphi$ is a bijection, and
2. for all $u, v \in V$: $\{u, v\} \in E \iff \{\varphi(u), \varphi(v)\} \in F$.

$G$ and $H$ are **isomorphic**, written $G \cong H$, when at least one isomorphism from $G$ to $H$ exists. An isomorphism from $G$ to itself is an **automorphism**; the automorphisms form the [automorphism group](/graph-automorphism-group/) $\mathrm{Aut}(G)$.

In matrix form: with $V = W = \{1, \ldots, n\}$, adjacency matrices $A$ and $B$ and the permutation matrix $P$ of $\varphi$ ($P_{i, \varphi(i)} = 1$), the map $\varphi$ is an isomorphism exactly when $P^{\mathsf T} A P = B$. So $G \cong H$ when $B$ is obtained from $A$ by the same permutation of the rows and of the columns.

The same pattern defines isomorphism for the other kinds of graphs. The condition always says "the map is a bijection on vertices and keeps every piece of structure":

- **Directed graphs.** $(u, v) \in E \iff (\varphi(u), \varphi(v)) \in F$, for ordered pairs. The direction must be kept.
- **Multigraphs.** The number of edges between $u$ and $v$ equals the number between $\varphi(u)$ and $\varphi(v)$, and the number of loops at $u$ equals that at $\varphi(u)$.
- **Vertex-colored graphs.** Each vertex has a color $c(v)$, and also $c_H(\varphi(v)) = c_G(v)$ for all $v$. Colors are how algorithms force some vertices to map to some others; individualizing a vertex means giving it a color of its own.
- **Edge-labeled graphs.** The label of $\{u, v\}$ in $G$ equals the label of $\{\varphi(u), \varphi(v)\}$ in $H$.

**Properties.** The identity map shows $G \cong G$. The inverse of an isomorphism is an isomorphism, so $G \cong H$ implies $H \cong G$. The composition of isomorphisms $G \to H$ and $H \to K$ is an isomorphism $G \to K$. So $\cong$ is reflexive, symmetric and transitive, and it splits all graphs into **isomorphism classes**. A graph "up to isomorphism", or an *unlabeled graph*, means such a class.

**Counting.** Fix a vertex set $V$ with $n$ elements. The graphs on $V$ that are isomorphic to a given $G$ on $V$ are the graphs $\pi(G)$ for the $n!$ [permutations](/permutation/) $\pi$ of $V$. Two permutations give the same graph exactly when they differ by an automorphism, so the class of $G$ holds exactly $n! / |\mathrm{Aut}(G)|$ graphs on $V$.

## Examples and non-examples

**Two drawings of one cycle.** Let $G$ have vertices $0, 1, 2, 3$ and edges $01, 12, 23, 30$, and let $H$ have the same vertices and edges $02, 21, 13, 30$. The map $\varphi = (0 \mapsto 0, 1 \mapsto 2, 2 \mapsto 1, 3 \mapsto 3)$ sends $01 \mapsto 02$, $12 \mapsto 21$, $23 \mapsto 13$, $30 \mapsto 30$, so $G \cong H$; both are the 4-cycle $C_4$. There are 8 isomorphisms from $G$ to $H$, because $|\mathrm{Aut}(C_4)| = 8$ (four rotations and four reflections). On the vertex set $\{0, 1, 2, 3\}$ there are $4! / 8 = 3$ different 4-cycles.

**All graphs on 4 vertices.** There are $2^6 = 64$ graphs on the vertex set $\{0, 1, 2, 3\}$, one for each subset of the 6 possible edges. They fall into 11 isomorphism classes. For 1 to 5 vertices the numbers of classes are 1, 2, 4, 11 and 34.

**Non-example: same number of edges.** The path $P_4$ (edges $01, 12, 23$) and the star $K_{1,3}$ (edges $01, 02, 03$) both have 4 vertices and 3 edges. They are not isomorphic: an isomorphism keeps the [degree](/degree/) of each vertex, and the star has a vertex of degree 3 while the path has none.

**Non-example: same degrees.** The 6-cycle $C_6$ and the union of two disjoint triangles $2K_3$ both have 6 vertices, 6 edges and all degrees equal to 2. They are not isomorphic: an isomorphism maps a path to a path, so it keeps [connectivity](/connected-graph/), and $C_6$ is connected while $2K_3$ is not. This pair also shows that [color refinement](/weisfeiler-leman/) cannot tell all graphs apart: on a regular graph it never splits the vertices.

**Non-example: direction matters.** The directed graphs $0 \to 1 \to 2$ and $0 \to 1 \leftarrow 2$ have the same underlying undirected path, so they are isomorphic as undirected graphs. As directed graphs they are not: the second has a vertex with in-degree 2 and the first has none.

**Non-example: the bijection must be on vertices.** Two graphs with isomorphic [line graphs](/line-graph/) need not be isomorphic: the triangle $K_3$ and the star $K_{1,3}$ both have the triangle as line graph. A bijection between edge sets that keeps adjacency of edges is a different notion; by Whitney's line graph theorem, these two graphs are the only connected exception.

## Related definitions

- [Graph automorphism group](/graph-automorphism-group/): the isomorphisms from a graph to itself. A graph whose only automorphism is the identity is [asymmetric](/asymmetric-graph/).
- [Isomorphism invariant](/isomorphism-invariant/): a value that is the same on isomorphic graphs, such as the number of edges, the degree sequence or the spectrum. Different values prove non-isomorphism.
- [Canonical labeling](/canonical-labeling/): a map that picks one representative of each isomorphism class, so that $G \cong H$ exactly when the representatives are equal.
- [Subgraph isomorphism](/subgraph-isomorphism/): an injective map that sends edges to edges, but need not keep non-edges or be onto.
- [Labeled graph](/labeled-graph/): a graph whose vertices carry names. Two labeled graphs are equal only when their edge sets are equal; isomorphism forgets the names.
- [Tree isomorphism](/tree-isomorphism/): the same notion on trees, with a variant for rooted trees where the root must map to the root.

## References
