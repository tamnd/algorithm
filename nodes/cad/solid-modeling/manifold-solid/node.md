---
tag: QDAAFS
kind: definition
slug: manifold-solid
name: Manifold solid
aliases:
- two-manifold solid
area: cad/solid-modeling
level: core
summary: A solid whose boundary is a closed 2-manifold surface, so each edge bounds exactly two faces and each boundary point has a neighborhood like a disk.
prereqs: [r-set, polygon-mesh]
see_also: [boundary-representation, radial-edge-data-structure, manifold-mesh, euler-poincare-formula, graph-genus, regularized-set-operations, vertex-neighborhood-classification]
sources:
  - book: isbn:9780881751086
    title: Martti Mäntylä, An Introduction to Solid Modeling, Computer Science Press, 1988
    locator: Section 3.5, Surface-based models (Section 3.5.1, 2-Manifolds, p. 35, and Section 3.5.6, Euler characteristic, p. 43), and Section 6.3, Validity of boundary models (p. 110)
  - paper: doi:10.1145/356827.356833
    title: Aristides A. G. Requicha, Representations for rigid solids, theory, methods, and systems, ACM Computing Surveys 12(4), 437 to 464, 1980
    locator: the boundary of an r-set and the validity of boundary representations
  - paper: "Kevin J. Weiler, Topological structures for geometric modeling, PhD thesis, Rensselaer Polytechnic Institute, 1986"
    locator: the manifold and non-manifold conditions and the cases that a manifold boundary model cannot store
---

A manifold solid is an [r-set](/r-set/) whose boundary is a closed 2-manifold: near each point of its skin, the skin looks like a flat disk. For a solid with flat faces this means that each edge bounds exactly two faces and that the faces around each vertex make one cycle. Most [boundary representations](/boundary-representation/), and the [winged-edge](/winged-edge-data-structure/) and half-edge structures, can store only manifold solids. The class is smaller than the r-sets, and it is not closed under the [regularized set operations](/regularized-set-operations/), which is why non-manifold modelers exist.

## Definition

Let $S \subseteq E^3$ be an r-set, and let $\partial S$ be its boundary.

**Manifold solid.** $S$ is a manifold solid if $\partial S$ is a 2-manifold: each point $p \in \partial S$ has a neighborhood in $\partial S$ that is homeomorphic to an open disk of the plane. The boundary is then a closed surface: it is compact, because $\partial S$ is closed and bounded, and it has no border, because every point has a full disk around it.

**Shells and genus.** The connected components of $\partial S$ are the *shells* of $S$. Each shell is a closed surface in $E^3$. A closed surface that lies in $E^3$ is orientable, so by the classification of surfaces each shell is a sphere with $g$ handles for some $g \ge 0$, its genus. The number of holes $H$ of the solid is the sum of the genera of its shells. A cube has one shell of genus 0. A solid torus has one shell of genus 1. A cube with an inner cavity has two shells of genus 0.

**Orientation.** Each shell separates $E^3$, so at each point of $\partial S$ one side is in $S$ and the other side is not. The outward normal points to the side that is not in $S$. On this page and on the other solid modeling pages, a face loop is oriented by the right-hand rule: when the fingers of the right hand follow the loop, the thumb points along the outward normal. So the outer loop of a face runs counterclockwise when one looks at the face from outside the solid.

**The combinatorial test for polyhedra.** Let the boundary of $S$ be split into planar faces, each a polygon that may have holes, with the edges and vertices that the faces share. Then $\partial S$ is a 2-manifold if and only if:

1. **Edge condition.** Each edge lies on exactly two faces, and near each point inside the edge the two faces are the only part of $\partial S$.
2. **Vertex condition.** At each vertex $v$, the faces that contain $v$ can be put in one cyclic order $f_1, f_2, \ldots, f_d$ so that $f_i$ and $f_{i+1}$ (and $f_d$ and $f_1$) share an edge at $v$. Then a small sphere around $v$ cuts $\partial S$ in one closed polygon, its *link*.

The reason is local. Near a point inside a face, $\partial S$ is a flat disk. Near a point inside an edge with $k$ faces, $\partial S$ is $k$ half-planes that meet along a line, and this is a disk exactly when $k = 2$. Near a vertex, $\partial S$ is the cone over the link, and the cone over a set is a disk exactly when the set is one circle. These are the same conditions as for a closed [2-manifold mesh](/manifold-mesh/), and the [polygon mesh](/polygon-mesh/) page states them for meshes.

**Neighborhoods in the solid.** For a polyhedral r-set, the boundary is a 2-manifold if and only if each point of $\partial S$ has a neighborhood in $S$ that is homeomorphic to a closed half-ball. A disk of $\partial S$ cuts a small ball around $p$ into two parts, and only one of them is in $S$, since $p$ would be an interior point otherwise. So $S$ is a compact 3-manifold with boundary, and some texts use that as the definition.

## Examples and non-examples

Each example gives the faces at an edge and the link at a vertex, which is enough by the combinatorial test.

- **A cube** $[0, 1]^3$. Each of the 12 edges is on 2 faces. At each of the 8 corners, 3 squares meet, and they form one cycle, so the link is a triangle. It is a manifold solid with one shell of genus 0.
- **A square frame**, the box $[0, 3] \times [0, 3] \times [0, 1]$ minus the hole $(1, 2) \times (1, 2) \times [0, 1]$. As a polyhedron whose top and bottom faces are square rings, it has 16 vertices, 24 edges and 10 faces (top, bottom, 4 outer sides and 4 inner sides). Each edge is on 2 faces, and at each vertex 3 faces meet in one cycle. It is a manifold solid with one shell of genus 1, so $H = 1$. The page on the [Euler-Poincaré formula for solids](/euler-poincare-formula/) checks its counts.
- **A cube with a cavity**, $[0, 3]^3$ minus the open cube $(1, 2)^3$. Each shell passes the test on its own. It is a manifold solid with two shells, both of genus 0.
- **Two disjoint cubes.** A manifold solid with two shells. A manifold solid does not need to be connected.

Non-examples:

- **Two cubes that share an edge**, $[0, 1]^3 \cup [1, 2] \times [1, 2] \times [0, 1]$. It is an r-set. The shared edge $\{1\} \times \{1\} \times [0, 1]$ lies on four faces, two of each cube. Near a point inside it, $\partial S$ is four half-planes on one line, which is not a disk. So it is not a manifold solid.
- **Two cubes that share a vertex**, $[0, 1]^3 \cup [1, 2]^3$. Each edge is on two faces, so the edge test passes. At the vertex $(1, 1, 1)$ there are 6 faces, which form two cycles of 3, one per cube. The link is two triangles, and the neighborhood of the vertex in $\partial S$ is two cones that touch at one point, not a disk.
- **A cube with a dangling face** is not even an r-set, so the question does not arise. A boundary model that stores it fails the edge test, because the edges of the dangling square are on 1 or 3 faces.

**The class is not closed under the regularized operations.** Two cubes $[0, 1]^3$ and $[1, 2] \times [1, 2] \times [0, 1]$ are manifold solids, and their regularized union is the non-manifold solid above. A difference gives the same result: take the L-shaped prism $L = ([0, 1] \times [0, 2] \cup [0, 2] \times [1, 2]) \times [0, 1]$, which is a manifold solid, and the box $B = [-1, 1] \times [1, 3] \times [-1, 2]$. Then $L -^* B = ([0, 1] \times [0, 1] \cup [1, 2] \times [1, 2]) \times [0, 1]$, which is again two boxes that share the edge over $(1, 1)$. A modeler that stores only manifold solids must reject these results or move the shapes apart, and a modeler that accepts them needs a structure such as the [radial edge data structure](/radial-edge-data-structure/).

## Related definitions

- An [r-set](/r-set/) is the general model of a solid. Every manifold solid is an r-set, and the two cube examples show that the converse is false.
- A [manifold mesh](/manifold-mesh/) is the same local condition for a surface given as faces, with borders allowed. The boundary of a polyhedral manifold solid is a closed, oriented manifold mesh.
- The [Euler-Poincaré formula for solids](/euler-poincare-formula/) relates the counts of vertices, edges, faces, rings, shells and holes of a manifold solid. The number of holes is the sum of the genera of the shells; see [graph genus](/graph-genus/) for the genus of a graph, which is at most the genus of a surface on which it is drawn.
- [Vertex neighborhood classification](/vertex-neighborhood-classification/) decides, at a vertex of a Boolean result, which sectors are in the solid. It is the step that finds the non-manifold vertices and edges.
- The [radial edge data structure](/radial-edge-data-structure/) stores non-manifold r-sets, with any number of faces around an edge in their angular order.

## References
