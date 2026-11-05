---
tag: HSJ5WG
kind: concept
slug: planar-dual-graph
name: Planar dual graph
aliases:
- dual graph
area: graphs/planar-graphs
level: core
summary: Graph with a vertex per face and an edge per primal edge joining the two faces it separates.
prereqs: [planar-face, rotation-system]
see_also: [planar-face-finding, euler-formula, four-color-theorem, min-cut-problem, spanning-tree, planar-shortest-paths, cut, multigraph]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 4.6, Plane duality (the dual of a plane multigraph, and the duality of cycles and bonds)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 6.1, Embeddings and Euler's formula (dual graphs, the dependence on the embedding, and the duality of cycles and bonds)
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 10, Planar graphs (the section on duality)
  - paper: "Hassler Whitney, Non-separable and planar graphs, Transactions of the American Mathematical Society 34(2), 339 to 362 (1932)"
    locator: the combinatorial dual and the planarity criterion by duals
---

The planar dual $G^*$ of a plane graph $G$ has one vertex for each [face](/planar-face/) of $G$ and one edge $e^*$ for each edge $e$ of $G$; the edge $e^*$ joins the two faces on the two sides of $e$, crossing $e$ once. It is a [multigraph](/multigraph/) in general: a bridge gives a loop, and two faces that share several edges are joined by parallel edges. The dual depends on the embedding, not only on the graph. Duality turns faces into vertices, cycles into minimal cuts, and spanning trees into the complements of spanning trees, which makes many planar problems easier.

## In plain words

Take a map of countries. Put a capital in each country, and for each stretch of border between two countries, draw a road from one capital to the other that crosses that border once. The capitals and roads form a new graph, the dual of the border graph. The sea around the map counts as a country too.

Coloring countries so that neighbours differ is the same as coloring capitals so that the ends of each road differ. A closed loop of borders in the old graph cuts the capitals into an inside group and an outside group, and the roads that cross the loop are exactly the roads between the two groups.

## The idea

**Definition (drawing form).** Let $G$ be a connected plane graph. Put a point $f^*$ in each face $f$. For each edge $e$, with faces $f_1$ and $f_2$ on its two sides, draw an arc $e^*$ from $f_1^*$ to $f_2^*$ that crosses $e$ once and meets no other part of $G$. The arcs can be chosen so that they do not cross each other, so $G^*$ is again a plane graph. If $f_1 = f_2$, which happens exactly when $e$ is a bridge, then $e^*$ is a loop. The counts are

$$n^* = f, \qquad m^* = m, \qquad f^* = n,$$

and the degree of $f^*$ is the length of the facial walk of $f$.

**Definition (combinatorial form).** An algorithm gets $G$ as a [rotation system](/rotation-system/) on the set $D$ of $2m$ darts, with the rotation $\sigma$, the twin map $\theta$ and the face map $\varphi = \sigma^{-1}\theta$. Let each dart $d$ also stand for the dual dart that crosses it. Then the dual is the rotation system with

$$\sigma^* = \varphi, \qquad \theta^* = \theta .$$

The vertices of $G^*$ are the cycles of $\varphi$, the faces of $G$. The face map of the dual is $\varphi^* = (\sigma^*)^{-1}\theta = \varphi^{-1}\theta = \theta\sigma\theta$, which is $\sigma$ conjugated by $\theta$. So the faces of $G^*$ correspond one to one to the vertices of $G$, and $G^{**} \cong G$. [Planar face finding](/planar-face-finding/) computes $G^*$ in $\Theta(n + m)$ time: number the faces, then for each edge join the faces of its two darts.

**Cycles and bonds.** A *bond* is a minimal nonempty edge [cut](/cut/). For a connected plane graph $G$ and $C \subseteq E(G)$:

$$C \text{ is the edge set of a cycle of } G \iff C^* = \{e^* : e \in C\} \text{ is a bond of } G^*.$$

*Proof of the forward direction.* A cycle is drawn as a simple closed curve, which by the [Jordan curve theorem](/jordan-curve-theorem/) splits the faces of $G$ into those inside and those outside, both nonempty. A dual edge $e^*$ joins an inside face to an outside face exactly when it crosses the curve, that is, when $e \in C$. So $C^*$ is the cut between the two sets. The inside faces induce a connected subgraph of $G^* - C^*$, and so do the outside faces (Diestel, Section 4.6). A cut whose two sides are both connected is minimal, so $C^*$ is a bond. The converse is in Diestel, Section 4.6. $\square$

**Spanning trees.** If $T$ is a [spanning tree](/spanning-tree/) of a connected plane graph $G$, then the duals of the other edges, $(E \setminus T)^*$, form a spanning tree of $G^*$. *Proof.* If $(E \setminus T)^*$ contained a cycle, its dual set would be a bond of $G$ (apply the theorem above to $G^*$, using $G^{**} = G$) disjoint from $T$; removing it would disconnect $G$ but not $T$, a contradiction. So $(E \setminus T)^*$ is acyclic, and it has $m - (n - 1) = f - 1$ edges on the $f$ vertices of $G^*$, by Euler's formula, so it is a spanning tree. $\square$ The pair is a *tree-cotree decomposition*, and $G$ and $G^*$ have the same number of spanning trees.

**The dual depends on the embedding.** Different embeddings of one planar graph can have non-isomorphic duals. For a 3-connected planar graph the embedding is unique (Whitney), so the dual is determined by the graph.

**Whitney's criterion.** A graph $G$ is planar if and only if it has an *abstract dual*: a graph $H$ with a bijection $E(G) \to E(H)$ that maps the cycles of $G$ exactly to the bonds of $H$ (Whitney, 1932).

## Examples

| plane graph $G$ | $n, m, f$ | dual $G^*$ |
|---|---|---|
| a single vertex | 1, 0, 1 | a single vertex |
| a tree with $n$ vertices | $n$, $n - 1$, 1 | one vertex with $n - 1$ loops |
| the cycle $C_k$ | $k$, $k$, 2 | two vertices joined by $k$ parallel edges |
| $K_4$ | 4, 6, 4 | $K_4$ (self-dual) |
| the cube $Q_3$ | 8, 12, 6 | the octahedron: 6 vertices of degree 4 |
| the octahedron | 6, 12, 8 | the cube |
| the icosahedron | 12, 30, 20 | the dodecahedron |
| a triangle with a pendant edge inside | 4, 4, 2 | 2 vertices, 3 parallel edges, and a loop at the inner face |
| the wheel $W_k$ (a $k$-cycle and a hub) | $k + 1$, $2k$, $k + 1$ | $W_k$ again (self-dual) |

**Two embeddings, two duals.** Let $G$ have the vertices $0, \ldots, 4$ and the triangles $012$, $123$ and $014$ (7 edges). Draw the edge $12$ with 0 on one side and 3 on the other. If 4 is drawn outside the triangle $012$, the faces have lengths 3, 3, 3, 5 ($014$, $012$, $123$, and the outer walk $0, 4, 1, 3, 2$). If 4 is drawn inside the triangle $012$, the faces have lengths 3, 3, 4, 4 ($014$, $0412$, $123$, and the outer $0231$). The two duals have the degree sequences $(3, 3, 3, 5)$ and $(3, 3, 4, 4)$, so they are not isomorphic. Both embeddings are planar: each has $5 - 7 + 4 = 2$.

**A cycle and a bond in $K_4$.** In the drawing of $K_4$ with 3 inside the triangle $0, 1, 2$, the cycle $0, 1, 2$ is the outer triangle. It separates the outer face from the three inner faces, and the dual edges of $01$, $12$, $20$ are the three edges from the outer-face vertex of $K_4^*$ to the others: the bond that isolates one vertex.

## Where it is used

- **Map coloring.** Coloring the faces of a plane graph is coloring the vertices of its dual. The [four color theorem](/four-color-theorem/) is usually stated for maps and proved for the duals, which are planar graphs; see [planar graph coloring](/planar-graph-coloring/).
- **Cuts as paths.** A minimum $s$-$t$ cut in a planar graph is a shortest cycle in the dual that separates the faces of $s$ and $t$, and a global [minimum cut](/min-cut-problem/) is a shortest cycle in the dual. So planar cut and flow problems reduce to [planar shortest paths](/planar-shortest-paths/) in the dual.
- **Euler's formula.** The tree-cotree split above gives a proof of [Euler's formula](/euler-formula/): $(n - 1) + (f - 1) = m$.
- **Separators.** The [Lipton-Tarjan separator](/lipton-tarjan-separator/) algorithm and [r-divisions](/r-division/) walk the dual to grow the inside of a fundamental cycle face by face.
- **Geometry.** The dual of a [Delaunay triangulation](/delaunay-triangulation/), with the outer face removed, is the [Voronoi diagram](/voronoi-diagram/) graph, and the dual of a triangulated polygon is a tree ([triangulation dual tree](/triangulation-dual-tree/)).
- **Planarization.** Inserting an edge with few crossings is a [shortest path](/shortest-path/) problem in the dual ([planarization heuristic](/planarization-heuristic/)).

## References
