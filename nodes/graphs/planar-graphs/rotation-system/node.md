---
tag: K5A9W6
kind: concept
slug: rotation-system
name: Rotation system
aliases:
- combinatorial embedding description
area: graphs/planar-graphs
level: core
summary: For each vertex, the cyclic order of its incident edges, which encodes a combinatorial embedding.
prereqs: [planar-graph, planar-face]
see_also: [planar-embedding, planar-face-finding, euler-formula, doubly-connected-edge-list, graph-genus, planar-dual-graph, planarity-testing, graph-genus-computation]
sources:
  - book: isbn:9780801866890
    title: Bojan Mohar and Carsten Thomassen, Graphs on Surfaces, Johns Hopkins University Press, 2001
    locator: Chapters 3 and 4 (rotation systems, embedding schemes with signatures, and the face tracing procedure)
  - book: isbn:9780486417417
    title: Jonathan L. Gross and Thomas W. Tucker, Topological Graph Theory, Dover edition, 2001
    locator: Chapter 3, Surfaces and graph imbeddings (pure rotation systems and the face tracing algorithm)
  - paper: "Jack Edmonds, A combinatorial representation for polyhedral surfaces, Notices of the American Mathematical Society 7, 646 (1960)"
    locator: the whole abstract (every rotation system of a connected graph defines an embedding in an orientable surface)
  - paper: "Lothar Heffter, Über das Problem der Nachbargebiete, Mathematische Annalen 38, 477 to 508 (1891)"
    locator: the description of embeddings by cyclic orders of neighbours
---

A rotation system of a [graph](/graph/) assigns to each vertex a cyclic order of the edges at that vertex. For a connected graph it describes an embedding in an orientable surface completely: the [faces](/planar-face/) are the orbits of one permutation of the half-edges, and the surface is the sphere exactly when [Euler's formula](/euler-formula/) $n - m + f = 2$ holds. It is the standard way to give a [planar embedding](/planar-embedding/) to an algorithm, because it is finite, exact and has no coordinates.

## In plain words

In a drawing with no crossings, stand on a vertex and turn around once, counterclockwise. You meet the edges of the vertex one after another, in a circle. A rotation system writes down this circle for every vertex, and nothing else.

That is enough to recover the regions of the drawing. Walk along an edge to its far end, then turn to the next edge in the circle there, and keep going. You walk around one region and come back to the start. Doing this from every side of every edge finds every region. No positions or angles are needed.

## The idea

**Darts.** Each edge $e = uv$ of $G = (V, E)$ has two *darts* (half-edges, arcs), $(u, v)$ leaving $u$ and $(v, u)$ leaving $v$. Let $D$ be the set of $2m$ darts. Two permutations of $D$ describe the embedding:

- the **involution** $\theta(u, v) = (v, u)$, which swaps the two darts of each edge;
- the **rotation** $\sigma$, whose cycles are the darts leaving each vertex, in counterclockwise order. So $\sigma(u, v) = (u, v')$, where $v'$ follows $v$ in the cyclic order $\rho_u$ at $u$.

A **rotation system** is the family $\rho = (\rho_v)_{v \in V}$, or equivalently the permutation $\sigma$. With parallel edges the cyclic order is on darts, not on neighbours.

**Faces.** The face permutation is

$$\varphi = \sigma^{-1} \circ \theta, \qquad \varphi(u, v) = (v, w), \quad w = \text{the neighbour just before } u \text{ in } \rho_v .$$

Its cycles are the facial walks. In a plane drawing with counterclockwise rotations, each walk keeps its face on the left; using $\sigma$ in place of $\sigma^{-1}$ walks the same faces in the other direction. Let $f$ be the number of cycles of $\varphi$.

**The rotation principle (Heffter, Edmonds).** Let $G$ be connected. For every rotation system $\rho$ there is an embedding of $G$ in a closed orientable surface $S$ such that each face is an open disc and the counterclockwise order at each vertex is $\rho$; $S$ and the embedding are unique up to homeomorphism. Conversely each such *cellular* embedding has a rotation system. The faces of the embedding are the cycles of $\varphi$, so the Euler characteristic gives

$$n - m + f = 2 - 2g,$$

where $g \ge 0$ is the genus of $S$. In particular:

> **$\rho$ is planar if and only if $n - m + f = 2$.**

For a graph with $c$ components, apply this to each component: $\rho$ is planar if and only if $n - m + f = 2c$. The rotation system says nothing about which face of one component contains another component.

**Mirror image.** Reversing every $\rho_v$ gives the mirror embedding. It has the same faces as vertex sets, walked in the opposite direction.

**How many rotation systems.** A vertex of degree $d \ge 1$ has $(d-1)!$ cyclic orders, so $G$ has $\prod_v (\deg v - 1)!$ rotation systems. The minimum genus over all of them is the [genus](/graph-genus/) of $G$.

**Adding an edge.** Insert a new edge $uw$ into a corner at $u$ (between two consecutive darts of $\rho_u$) and a corner at $w$. Each corner lies on one face. If both corners lie on the same face, that face splits in two: $f$ grows by 1 and $g$ does not change. If they lie on different faces, the two faces merge into one: $f$ drops by 1, and when $G$ was connected, $g$ grows by 1. (In terms of permutations, $\varphi$ is multiplied by a transposition, which splits one cycle or joins two.) So a planar embedding stays planar exactly when each new edge is put into two corners of one face. This is the step used by path addition [planarity tests](/planarity-testing/) and by [planarization](/planarization-heuristic/).

**Stored as a data structure.** For each dart keep its twin $\theta$, its next dart $\sigma$ around the tail, and its previous dart $\sigma^{-1}$. These are exactly the pointers of a half-edge structure, the [doubly connected edge list](/doubly-connected-edge-list/) of computational geometry, which also stores the face of each dart. With arrays indexed by dart, $\varphi$ costs $O(1)$ per step, and all faces are found in $O(n + m)$ time ([planar face finding](/planar-face-finding/)).

**Other forms of the same data.** A *combinatorial map* is the triple $(D, \sigma, \theta)$ with $\theta$ a fixed-point-free involution and $\langle \sigma, \theta \rangle$ transitive. For a straight-line drawing given by coordinates, $\rho_v$ is the order of the neighbours of $v$ by angle around $v$, which takes $O(\deg v \log \deg v)$ time per vertex to sort. Non-orientable surfaces need one more bit per edge, a *signature*, which says whether the edge reverses the local orientation (Mohar and Thomassen).

## Examples

**$K_4$, planar.** The rotation system $\rho_0 = (1, 3, 2)$, $\rho_1 = (2, 3, 0)$, $\rho_2 = (0, 3, 1)$, $\rho_3 = (0, 1, 2)$ comes from the drawing with 3 inside the triangle $0, 1, 2$. Its face permutation has 4 cycles, $(0, 1, 3)$, $(0, 3, 2)$, $(1, 2, 3)$, $(0, 2, 1)$, and $4 - 6 + 4 = 2$, so $g = 0$.

**$K_4$, toroidal.** With every $\rho_v$ in increasing order, $\varphi$ has 2 cycles, of lengths 4 and 8, so $4 - 6 + 2 = 0$ and $g = 1$. The same graph, a different rotation system, a different surface.

**Counts by brute force.** The table gives the number of rotation systems, how many are planar, and the face counts that occur.

| graph | rotation systems | planar | values of $f$ | genus of $G$ |
|---|---|---|---|---|
| a single vertex | 1 | 1 | 1 | 0 |
| a star with 3 leaves | 2 | 2 | 1 | 0 |
| $K_4$ | 16 | 2 | 2, 4 | 0 |
| $K_5$ | 7776 | 0 | 1, 3, 5 | 1 |
| $K_{3,3}$ | 64 | 0 | 1, 3 | 1 |

For $K_5$, $f = 5$ gives $5 - 10 + 5 = 0$, so the best surface is the torus. For $K_{3,3}$, $f = 3$ gives $6 - 9 + 3 = 0$.

**A tree.** Every rotation system of a tree on $n$ vertices has a single face of length $2(n - 1)$, and $n - (n-1) + 1 = 2$. So all rotation systems of a tree are planar, which matches the fact that the order of the children of each node can be chosen freely in a drawing.

**Inserting an edge.** In the planar $K_4$ above, delete nothing and add a new vertex 4 in the face $(0, 1, 3)$ joined to 0, 1 and 3, with each new edge put in the corner of that face. Each insertion splits the face it uses, and the result has $n = 5$, $m = 9$, $f = 6$, so $5 - 9 + 6 = 2$: a planar $K_5 - e$, missing the edge 24. Any attempt to add the edge 24 now joins two corners on different faces, since 2 and 4 share no face, and the genus becomes 1.

## Where it is used

- As the output of [planarity testing](/planarity-testing/) and [planar embedding](/planar-embedding/) algorithms, and as the input of almost every algorithm on embedded planar graphs: [face finding](/planar-face-finding/), the [planar dual](/planar-dual-graph/), [separators](/lipton-tarjan-separator/), [Schnyder woods](/schnyder-woods/) and [straight-line drawing](/planar-straight-line-drawing/).
- In [graph genus](/graph-genus/) and [graph genus computation](/graph-genus-computation/): the genus of $G$ is the minimum genus over all rotation systems.
- In computational geometry as the [doubly connected edge list](/doubly-connected-edge-list/) of a [planar subdivision](/planar-subdivision/), and in mesh processing as half-edge meshes.
- In topological graph theory to construct embeddings, such as the triangular embeddings of complete graphs used in the proof of the Heawood map-coloring formula.

## References
