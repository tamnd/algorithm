---
tag: 0GY28M
kind: definition
slug: isomorphism-invariant
name: Isomorphism invariant
aliases:
- graph invariant
area: graphs/graph-isomorphism
level: intro
summary: A graph property or value equal for all isomorphic graphs; unequal values prove non-isomorphism.
prereqs: [graph-isomorphism-definition]
see_also: [graph-isomorphism-problem, canonical-labeling, weisfeiler-leman, equitable-partition, degree, eigenvalue, cai-furer-immerman-construction]
sources:
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 7, Computing isomorphism (invariants and certificates, and their use to split graphs into classes before a full test)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.1, Graphs (graph invariants)
  - paper: doi:10.1002/jgt.3190010410
    title: Ronald C. Read and Derek G. Corneil, The graph isomorphism disease, Journal of Graph Theory 1(4), 339 to 363 (1977)
    locator: the sections on invariants and on the failure of each known invariant to be complete
---

An isomorphism invariant is a function on graphs that takes the same value on any two [isomorphic graphs](/graph-isomorphism-definition/). If two graphs have different values, they are not isomorphic; if they have the same value, nothing follows unless the invariant is complete. The number of edges, the degree sequence, the spectrum and the output of [color refinement](/weisfeiler-leman/) are invariants. Cheap invariants are the first step of almost every isomorphism test, because they reject most non-isomorphic pairs at once.

## Definition

Let $\mathcal G$ be a class of graphs closed under isomorphism (for example all finite simple graphs) and let $S$ be any set. A function $f : \mathcal G \to S$ is an **isomorphism invariant** (a *graph invariant*) when

$$G \cong H \implies f(G) = f(H) \qquad \text{for all } G, H \in \mathcal G.$$

An invariant with values in $\{\text{true}, \text{false}\}$ is a *graph property*, such as "connected" or "planar". The invariant is **complete** when the converse also holds:

$$f(G) = f(H) \implies G \cong H.$$

A complete invariant whose value is itself a graph isomorphic to the input is a [canonical form](/canonical-labeling/).

A **vertex invariant** gives a value to each vertex: a function $f(G, v)$ with $f(G, v) = f(H, \varphi(v))$ for each isomorphism $\varphi : G \to H$. The degree of a vertex and the number of triangles through it are vertex invariants. The multiset $\{\!\{ f(G, v) : v \in V \}\!\}$ of a vertex invariant is a graph invariant, and an isomorphism can only map $v$ to a vertex with the same value, which cuts the search.

For directed, colored or labeled graphs the definition is the same, with the isomorphism notion of that class: an invariant of vertex-colored graphs must agree on graphs that are isomorphic by a color-preserving map.

**Use.** The contrapositive is the rule used in practice: $f(G) \ne f(H) \implies G \not\cong H$. An invariant can prove non-isomorphism but never isomorphism, unless it is complete. Every complete invariant that can be computed in polynomial time solves the [graph isomorphism problem](/graph-isomorphism-problem/) in polynomial time, so no such invariant is known for all graphs.

## Examples and non-examples

**Common invariants.**

| invariant | cost to compute | complete for |
|---|---|---|
| number of vertices and of edges | $O(n + m)$ | nothing beyond small cases |
| sorted degree sequence | $O(n + m)$ | nothing beyond small cases |
| number of connected components, of triangles | $O(n + m)$, $O(m^{3/2})$ | nothing beyond small cases |
| spectrum of the adjacency matrix | $O(n^3)$ numerically | not complete |
| stable coloring of [color refinement](/weisfeiler-leman/), as a multiset of colors | $O((n + m) \log n)$ | trees, and almost all graphs |
| stable coloring of [$k$-WL](/k-dimensional-weisfeiler-leman/) | $O(n^{k+1} \log n)$ | graphs of bounded treewidth or genus for some $k$, but no fixed $k$ for all graphs |
| [AHU code](/ahu-algorithm/) of a rooted tree | $O(n)$ | rooted trees |
| canonical form of [nauty](/nauty/) or [bliss](/bliss/) | exponential in the worst case | all graphs |

**Degree sequence separates, edge count does not.** The path $P_4$ and the star $K_{1,3}$ have 4 vertices and 3 edges each. Their degree sequences are $(1, 1, 2, 2)$ and $(1, 1, 1, 3)$, so they are not isomorphic.

**Degree sequence fails, connectivity separates.** The cycle $C_6$ and two disjoint triangles $2K_3$ both have the degree sequence $(2, 2, 2, 2, 2, 2)$. The first has 1 component and 0 triangles, the second has 2 components and 2 triangles.

**Spectrum fails.** The star $K_{1,4}$ and the 4-cycle plus an isolated vertex, $C_4 \cup K_1$, both have the adjacency eigenvalues $-2, 0, 0, 0, 2$. They are not isomorphic, since only the first is connected. Such pairs are called cospectral.

**Many invariants fail together.** The $4 \times 4$ rook's graph (the 16 squares of a $4 \times 4$ board, adjacent when in the same row or column) and the Shrikhande graph (the Cayley graph on $\mathbb Z_4 \times \mathbb Z_4$ with the connection set $\pm(0,1), \pm(1,0), \pm(1,1)$) both have 16 vertices, 48 edges, all degrees 6, 32 triangles, and the spectrum $6^1, 2^6, (-2)^9$. Both are strongly regular with the parameters $(16, 6, 2, 2)$, and color refinement and 2-dimensional Weisfeiler-Leman give them the same colors. The number of 4-cliques separates them: 8 for the rook's graph (its rows and columns) and 0 for the Shrikhande graph.

**Non-example: a labeling-dependent value.** The adjacency matrix itself, or "the degree of vertex 0", is not an invariant: relabeling the vertices changes it while the graph stays in the same class. The lexicographically smallest adjacency matrix over all labelings is an invariant, and a complete one, but computing it naively takes $n!$ steps.

**Non-example: an invariant that is not complete is not a test.** Equal values of any invariant that is not complete never prove isomorphism. [Cai, Fürer and Immerman](/cai-furer-immerman-construction/) built non-isomorphic pairs on which every fixed level of the Weisfeiler-Leman hierarchy gives equal values.

## Related definitions

- [Isomorphic graphs](/graph-isomorphism-definition/): the relation that an invariant must respect.
- [Canonical labeling](/canonical-labeling/): a complete invariant whose value is a graph of the class.
- [Equitable partition](/equitable-partition/): the vertex partition found by color refinement, a vertex invariant.
- [Automorphism orbit](/automorphism-orbit/): vertices in one orbit have equal values of every vertex invariant; the converse fails in general.
- [Degree](/degree/) and [eigenvalue](/eigenvalue/): the most common numeric invariants.

## References
