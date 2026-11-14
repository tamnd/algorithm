---
tag: 7H7VSS
kind: definition
slug: cut-graph
name: Cut graph
aliases:
- seam graph
- mesh cut to a disk
area: cad/mesh-processing
level: core
summary: A set of edges whose removal opens a closed mesh of genus g into a topological disk, needed before flattening, found from a spanning tree and cotree.
prereqs: [manifold-mesh, spanning-tree, euler-poincare-formula]
see_also: [mesh-parameterization, graph-genus, fundamental-cycle, cycle-basis, euler-formula, breadth-first-search, mixed-integer-quadrangulation, discrete-conformal-equivalence]
sources:
  - paper: doi:10.1007/s00454-003-2948-z
    title: Jeff Erickson and Sariel Har-Peled, Optimally cutting a surface into a disk, Discrete and Computational Geometry 31(1), 37-59, 2004
    locator: the definition of a cut graph, the count of its cycles from the Euler characteristic, and the NP-hardness of a shortest cut graph
  - paper: arxiv:cs/0207082
    title: David Eppstein, Dynamic generators of topologically embedded graphs, Proceedings of the 14th ACM-SIAM Symposium on Discrete Algorithms, 599-608, 2003
    locator: the tree-cotree decomposition into a spanning tree, a dual spanning tree and 2g leftover edges
  - book: isbn:9780821849255
    title: Herbert Edelsbrunner and John Harer, Computational Topology, An Introduction, American Mathematical Society, 2010
    locator: Chapter II, Surfaces (triangulated surfaces, the Euler characteristic and the classification of surfaces)
---

A cut graph of a closed surface mesh is a set of edges such that cutting the surface along them leaves one piece that is a topological disk. Flattening methods such as [mesh parameterization](/mesh-parameterization/) and quad meshing work on disks, so a sphere, a torus or a surface with more handles must first be cut open, and the cut is the seam of the texture map. By the Euler characteristic, a cut graph of a surface of genus $g$ always has exactly $2g$ independent cycles, so a torus needs two loops and a sphere needs none. A cut graph is easy to find with a spanning tree of the mesh and a spanning tree of its dual; a shortest cut graph is NP-hard to find.

## Definition

Let $M$ be a connected, closed, orientable [manifold mesh](/manifold-mesh/) with $V$ vertices, $E$ edges and $F$ triangles, oriented by the right-hand rule. Its Euler characteristic is $\chi = V - E + F = 2 - 2g$, where $g$ is the genus, the number of handles. This is the [Euler-Poincaré formula](/euler-poincare-formula/) for a closed surface.

A **cut graph** of $M$ is a subgraph $G$ of the edge graph of $M$ such that $M \setminus G$, the surface with the points of $G$ removed, is homeomorphic to an open disk. *Cutting $M$ along $G$* means making two copies of each edge of $G$, one for each side, and enough copies of each vertex of $G$ to separate the fans of triangles between the cut edges. The result is a closed disk $D$, and its boundary walks along each edge of $G$ twice, once on each side.

A cut graph is **reduced** if it has no vertex of degree 1. A vertex of degree 1 ends a branch that can be glued shut again without changing the disk, so every cut graph can be reduced by removing such branches, except on the sphere, where the reduced cut graph can be a single vertex.

**Theorem (the number of loops).** Let $G$ be a cut graph of $M$ with $V_G$ vertices and $E_G \ge 1$ edges. Then $G$ is connected, and

$$E_G - V_G + 1 = 2g,$$

that is, $G$ has exactly $2g$ independent cycles, its cycle rank.

*Proof.* The boundary of $D$ is one closed walk that covers each edge of $G$ twice, so it has $2E_G$ edges and $2E_G$ corners. Each corner is a copy of a vertex of $G$, and every edge of $G$ is on the walk, so $G$ is the image of one connected walk and is connected. The vertices of $D$ are the $V - V_G$ vertices not on $G$ and the $2E_G$ corners of the boundary. The edges of $D$ are the $E - E_G$ edges not on $G$ and the $2E_G$ copies. The triangles are the $F$ triangles of $M$. A closed disk has Euler characteristic 1, so

$$1 = (V - V_G + 2E_G) - (E - E_G + 2E_G) + F = \chi - V_G + E_G = 2 - 2g - V_G + E_G,$$

which gives $E_G - V_G + 1 = 2g$. $\blacksquare$

**Corollary (the size of a reduced cut graph).** For $g \ge 1$, write a reduced cut graph as $P$ paths between the $B$ vertices of degree at least 3, with the vertices of degree 2 inside the paths. Then $P - B = E_G - V_G = 2g - 1$ and $2P = \sum \deg \ge 3B$, so $B \le 4g - 2$ and $P \le 6g - 3$. If the graph has only one vertex of degree more than 2, it consists of $2g$ loops through that vertex, and cutting along them gives the classical $4g$-gon of the classification of surfaces. For $g = 1$ these are the two loops that open a torus to a square.

**Construction by tree and cotree.** Pick a [spanning tree](/spanning-tree/) $T$ of the vertices and edges of $M$, for example by [breadth-first search](/breadth-first-search/). Then pick a spanning tree $C$ of the *dual graph*, which has a node for each triangle and an arc across each edge, using only edges not in $T$. Such a tree exists because a tree on a surface has a small neighbourhood that is a disk, and removing a disk from a connected surface leaves it connected, so the triangles stay connected across the edges not in $T$. The edges in neither tree are the leftover set $X$, and

$$|X| = E - (V - 1) - (F - 1) = 2 - \chi = 2g.$$

The edges of $T \cup X$ are a cut graph. *Reason:* the triangles glued along the $F - 1$ edges of the tree $C$ form a disk, because gluing a triangle to a disk along one boundary edge gives a disk again. The edges not in $C$ are exactly the edges of $T \cup X$, and they are the boundary of this disk. So $M$ cut along $T \cup X$ is that disk. Each edge of $X$ closes a cycle in $T$, its [fundamental cycle](/fundamental-cycle/); the $2g$ cycles are the loops of the cut graph, and removing the branches of $T$ that lead nowhere reduces it. This is Eppstein's tree-cotree decomposition. Each step takes $O(V + E + F)$ time.

**Surfaces with boundary.** If $M$ has $b \ge 1$ boundary loops, the boundary already counts as cut, and $G$ is a set of inner edges such that cutting along $G$ gives a disk. The same count, with the boundary edges walked once, gives a cycle rank of $2g + b$ for the graph $G \cup \partial M$. A disk needs no cut, and a cylinder ($g = 0$, $b = 2$) needs one path from one boundary loop to the other.

## Examples and non-examples

- **Tetrahedron, $g = 0$.** $V = 4$, $E = 6$, $F = 4$, $\chi = 2$. The three edges at one vertex form a cut graph: a tree, with $E_G - V_G + 1 = 3 - 4 + 1 = 0$. Cutting along them unfolds the tetrahedron into a triangle made of four triangles. Any spanning tree of a convex polyhedron is a cut graph in the same way; an edge unfolding of a polyhedron cuts along a spanning tree.
- **Torus, $g = 1$.** Take a $3 \times 3$ grid of vertices with opposite sides identified and each square split into two triangles: $V = 9$, $E = 27$, $F = 18$, $\chi = 0$. One horizontal loop of 3 edges and one vertical loop of 3 edges through a common vertex form a cut graph with $V_G = 5$ and $E_G = 6$, so $E_G - V_G + 1 = 2$. Cutting along them gives the square, made of 18 triangles. The tree-cotree count gives $|X| = 27 - 8 - 17 = 2$ leftover edges.
- **Genus 2.** A reduced cut graph has cycle rank 4. It can be four loops at one vertex, which open the surface to an octagon, or up to $4g - 2 = 6$ vertices of degree 3 joined by $6g - 3 = 9$ paths.
- **Non-example: one loop on a torus.** Cutting along one meridian gives a cylinder, which is not a disk. Its cycle rank is $1 < 2$.
- **Non-example: the right count in the wrong place.** Two parallel meridians of a torus, joined by a path, have cycle rank 2. Cutting along the two meridians gives two cylinders, and the path cuts only one of them into a disk, so the result is a disk and a cylinder, not one disk. The two loops fail because they go around the same handle in the same way. So the count $E_G - V_G + 1 = 2g$ is necessary but not sufficient.
- **Non-example: a loop on a sphere.** A closed loop of edges on a sphere cuts it into two disks, not one, so a cut graph of a sphere has no cycle, as the theorem says.

## Related definitions

- **Cut graph and parameterization.** The [discrete conformal](/discrete-conformal-equivalence/) and other flattening methods lay out triangles across edges, which works only on a disk. The cut graph is the seam, and in a texture map the two sides of each seam edge get different texture coordinates. Methods for seamless maps, such as [mixed-integer quadrangulation](/mixed-integer-quadrangulation/), require that the two sides match up to a rotation by a multiple of $90°$ and an integer translation.
- **Homology basis.** A homology basis is a set of $2g$ loops such that every loop on the surface is, up to deformation and cancellation, a combination of them in exactly one way, counted with integer multiples. The $2g$ fundamental cycles of a cut graph are a homology basis: the surface is the cut graph with one disk glued on, and the boundary of the disk walks each edge once in each direction, so gluing it adds no relation between the cycles. The two parallel meridians of the non-example are not a basis, because they are the same loop up to deformation.
- **Graph genus.** The [genus of a graph](/graph-genus/) is the smallest genus of a surface on which the graph embeds without crossings. The genus of a mesh is fixed by its Euler characteristic; the [Euler formula](/euler-formula/) is the case $g = 0$.
- **Cycle basis.** The fundamental cycles of a spanning tree are a [cycle basis](/cycle-basis/) of the graph. The tree-cotree construction keeps only the $2g$ of them that come from the leftover edges.
- **Shortest cut graph.** Erickson and Har-Peled showed that finding a cut graph of least total length is NP-hard, and gave an approximation with factor $O(\log^2 g)$. In practice, cuts are made short and placed along regions of high distortion or low visibility.

## References
