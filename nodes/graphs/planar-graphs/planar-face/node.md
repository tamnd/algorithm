---
tag: BSEEWC
kind: concept
slug: planar-face
name: Face of a planar embedding
aliases:
- faces
area: graphs/planar-graphs
level: intro
summary: A connected region of the plane minus the drawing of a plane graph.
prereqs: [planar-graph]
see_also: [euler-formula, rotation-system, planar-face-finding, planar-dual-graph, planar-edge-bound, maximal-planar-graph, doubly-connected-edge-list, jordan-curve-theorem]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 4.2, Plane graphs (faces, frontiers, and the lemmas on the faces of cycles and of 2-connected plane graphs)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 6.1, Embeddings and Euler's formula (faces, the length of a face, and the sum of the face lengths)
  - book: isbn:9780801866890
    title: Bojan Mohar and Carsten Thomassen, Graphs on Surfaces, Johns Hopkins University Press, 2001
    locator: Chapters 3 and 4 (embeddings described by rotation systems, and the facial walks they define)
---

A face of a [plane graph](/planar-graph/) is a connected region of the plane that remains when the points and arcs of the drawing are removed. Exactly one face is unbounded, the outer face. Each face is bounded by one or more closed walks of the graph, and the total length of these walks over all faces is $2m$, because each edge has two sides. Faces are what [Euler's formula](/euler-formula/) counts, and they are the vertices of the [planar dual](/planar-dual-graph/).

## In plain words

Draw a graph on paper with no crossing lines, then cut the paper along every line. The pieces of paper are the faces. The piece around the outside of the drawing is also a face.

You can walk around the edge of each piece. The walk follows lines of the graph and comes back to its start. Each line has two sides, and each side belongs to exactly one piece. A line that has the same piece on both sides, like a branch that sticks into a region, is walked twice by that piece.

## The idea

**Topological definition.** Let $G$ be a plane graph and let $\Gamma \subset \mathbb{R}^2$ be the union of its vertex points and edge arcs. $\Gamma$ is closed, so $\mathbb{R}^2 \setminus \Gamma$ is open, and its connected components are the **faces** of $G$. $\Gamma$ is bounded, so exactly one face contains all points far from the origin: the **outer face**. The *frontier* (boundary) of a face $f$ is the set of points of $\Gamma$ that are limits of points of $f$; it is a union of vertices and whole edges (Diestel, Section 4.2).

**Combinatorial definition.** An algorithm does not see regions. It sees the embedding as a [rotation system](/rotation-system/): for each vertex $v$, a cyclic order $\rho_v$ of the neighbours of $v$, counterclockwise in the drawing. Each edge $uv$ gives two *darts* (half-edges), $(u, v)$ and $(v, u)$. The face successor of a dart is

$$\varphi(u, v) = (v, w), \qquad w = \text{the neighbour just before } u \text{ in } \rho_v .$$

$\varphi$ is a permutation of the $2m$ darts. Its cycles are the **facial walks**, one cycle for each face of a connected plane graph. Walking along the darts of one cycle keeps the face on the same side. The page [planar face finding](/planar-face-finding/) gives the algorithm and its proof. For a graph with $c \ge 2$ components the rotation system does not say which component sits in which face of another, so the cycles of $\varphi$ are the facial walks of each component on its own.

**Length and degree.** The *length* (or degree) $\ell(f)$ of a face $f$ is the number of darts in its walk. A bridge lies on one face and is counted twice there. Each dart lies on exactly one face, so

$$\sum_{f} \ell(f) = 2m .$$

This is the face form of the [handshake lemma](/handshake-lemma/).

**What a face boundary looks like.**

- In a plane forest the only face is the outer face (an arc system with no cycle does not cut the plane), and its walk has length $2m$.
- If $G$ is 2-connected, every face is bounded by a cycle of $G$ (Diestel, Section 4.2).
- If $G$ is 3-connected, the facial cycles are exactly the induced cycles $C$ such that $G - V(C)$ is connected (Tutte; Diestel, Section 4.3). So the faces do not depend on the drawing.
- A simple plane graph with $n \ge 3$ vertices has every face of length at least 3, which gives the [edge bound](/planar-edge-bound/) $m \le 3n - 6$.

**Which face is outer is not intrinsic.** By stereographic projection, any face of a plane graph can be made the outer face of an equivalent drawing. So algorithms that need an outer face pick one and say so.

## Examples

Each row was computed by tracing $\varphi$ on a rotation system of the drawing. $f$ is the number of faces, and the last column lists the face lengths.

| plane graph | $n$ | $m$ | $f$ | face lengths |
|---|---|---|---|---|
| a single vertex | 1 | 0 | 1 | the outer face, length 0 |
| a path on 4 vertices | 4 | 3 | 1 | 6 |
| a star with 3 leaves | 4 | 3 | 1 | 6 |
| a cycle $C_5$ | 5 | 5 | 2 | 5, 5 |
| $K_4$ | 4 | 6 | 4 | 3, 3, 3, 3 |
| a triangle with a pendant edge drawn inside | 4 | 4 | 2 | 3 (outer), 5 (inner, the pendant edge twice) |
| the cube $Q_3$ | 8 | 12 | 6 | 4, 4, 4, 4, 4, 4 |
| $K_5 - e$ | 5 | 9 | 6 | 3, 3, 3, 3, 3, 3 |

In each row the face lengths sum to $2m$, and $n - m + f = 2$.

**A worked trace on $K_4$.** Put vertex 3 inside the triangle $0, 1, 2$, which is drawn counterclockwise. The counterclockwise rotations are $\rho_0 = (1, 3, 2)$, $\rho_1 = (2, 3, 0)$, $\rho_2 = (0, 3, 1)$ and $\rho_3 = (0, 1, 2)$. Start at the dart $(0, 1)$. At vertex 1 the neighbour just before 0 in $\rho_1$ is 3, so the next dart is $(1, 3)$. At vertex 3 the neighbour just before 1 is 0, so the next dart is $(3, 0)$. At vertex 0 the neighbour just before 3 is 1, which closes the walk $0 \to 1 \to 3 \to 0$, the inner triangle on the edge $01$. The four walks found this way are $(0, 1, 3)$, $(1, 2, 3)$, $(2, 0, 3)$ and the outer face $(0, 2, 1)$.

**Non-example: a rotation system that is not planar.** Give $K_4$ the rotations $\rho_0 = (1, 2, 3)$, $\rho_1 = (0, 2, 3)$, $\rho_2 = (0, 1, 3)$, $\rho_3 = (0, 1, 2)$. Tracing $\varphi$ gives only 2 walks, of lengths 4 and 8. Then $n - m + f = 4 - 6 + 2 = 0 \ne 2$: these walks bound faces of an embedding of $K_4$ on the torus, not in the plane.

## Where it is used

- [Euler's formula](/euler-formula/) $n - m + f = 2$ counts faces, and the [planar edge bound](/planar-edge-bound/) follows from it and from $\sum \ell(f) = 2m$.
- The [planar dual](/planar-dual-graph/) has one vertex for each face, and the duality of cuts and cycles is a statement about faces.
- A [maximal planar graph](/maximal-planar-graph/) is a plane graph whose faces are all triangles; an [outerplanar graph](/outerplanar-graph/) has all vertices on the outer face.
- [Planar face finding](/planar-face-finding/) lists all faces in $O(n + m)$ time, which is the first step of the [Lipton-Tarjan separator](/lipton-tarjan-separator/) algorithm, of triangulation and of many drawing algorithms.
- The [doubly connected edge list](/doubly-connected-edge-list/) of computational geometry stores a face pointer on each half-edge.
- [Planarization](/planarization-heuristic/) routes a new edge through a sequence of faces, crossing one edge between each pair of consecutive faces.

## References
