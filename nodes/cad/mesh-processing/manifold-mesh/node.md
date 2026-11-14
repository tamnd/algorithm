---
tag: Q6E1QG
kind: definition
slug: manifold-mesh
name: Manifold mesh
aliases:
- two-manifold mesh
area: cad/mesh-processing
level: intro
summary: A mesh in which each edge has one or two faces and the faces around each vertex form one fan, so it is locally like a disk or a half disk.
prereqs: [polygon-mesh, indexed-face-set]
see_also: [manifold-solid, consistent-mesh-orientation, euler-poincare-formula, mesh-repair-problem, mesh-self-intersection, doubly-connected-edge-list, corner-table, radial-edge-data-structure]
sources:
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 8, Model Repair, Section 8.1, Types of Artifacts (non-manifold edges and vertices)
  - book: isbn:9780821849255
    title: Herbert Edelsbrunner and John Harer, Computational Topology, An Introduction, American Mathematical Society, 2010
    locator: Chapter II, Surfaces, Section II.1, Two-dimensional Manifolds (triangulated surfaces, links of vertices, orientability)
  - paper: doi:10.1145/2431211.2431214
    title: Marco Attene, Marcel Campen and Leif Kobbelt, Polygon mesh repairing, an application perspective, ACM Computing Surveys 45(2), Article 15, 2013
    locator: the section on the types of defects (singular edges and vertices, borders, orientation)
---

A manifold mesh is a [polygon mesh](/polygon-mesh/) in which each edge lies in one or two faces and the faces around each vertex form a single fan. These two local conditions make each point of the surface have a neighbourhood like a disk, or like a half disk on the border. The first condition alone gives an edge-manifold mesh, which is weaker: two cones that touch at their tips satisfy it, but the tip is not like a disk. Most mesh algorithms and mesh data structures need a manifold mesh as input, so testing and repairing this property comes first in a mesh pipeline.

## Definition

A mesh is a set of vertices $\{0, \ldots, n-1\}$ and a set of faces, where each face is a cyclic sequence of at least three distinct vertices, as in an [indexed face set](/indexed-face-set/). An edge is a pair $\{u, v\}$ of vertices that follow each other in some face. The number of faces that contain an edge, counted with their uses, is its *valence*.

**Link of a vertex.** For a vertex $v$, the link $\mathrm{Lk}(v)$ is the graph whose nodes are the neighbours $w$ of $v$ (the vertices with an edge $\{v, w\}$), with one link edge for each face $f$ that contains $v$. The link edge of $f$ joins the two neighbours of $v$ in $f$, the vertex before $v$ and the vertex after $v$. So the link edges are the faces around $v$, and two of them touch where two faces share an edge at $v$.

**Manifold mesh.** A mesh is a *manifold mesh* (a combinatorial 2-manifold, possibly with border) if these two conditions hold:

1. **Edge condition.** Each edge has valence 1 or 2.
2. **Vertex condition.** For each vertex $v$ that some face uses, $\mathrm{Lk}(v)$ is one cycle or one simple path.

The degree of a node $w$ in $\mathrm{Lk}(v)$ is the valence of the edge $\{v, w\}$. So under the edge condition, each link is a disjoint union of paths and cycles, and the vertex condition asks only that the link is connected: the faces around $v$ form one fan. An edge with valence 1 is a *border edge*. A vertex with a cycle as its link is an *inner vertex*, and a vertex with a path is a *border vertex*. The mesh is *closed*, or watertight, if it has no border edge.

**Edge-manifold mesh.** A mesh that satisfies only the edge condition is *edge-manifold*. A vertex that breaks the vertex condition, while all its edges have valence 1 or 2, is a *non-manifold vertex*. An edge with valence at least 3 is a *non-manifold edge*.

**Why the name.** If the mesh is a manifold mesh and its faces are drawn as flat polygons that meet only along shared edges and vertices, the union of the faces is a compact topological surface with boundary: the fan around an inner vertex is a disk, and the fan around a border vertex is a half disk. The border edges then form disjoint closed loops, the *border loops*. The definition is combinatorial. It says nothing about the positions of the vertices, so a manifold mesh can still cross itself in space, see [mesh self-intersection](/mesh-self-intersection/).

**Orientation.** A manifold mesh is *consistently oriented* if the two faces of each inner edge use it in opposite directions, and *orientable* if some choice of the vertex order of each face makes it so. With the convention of this encyclopedia, the outward normal of each face follows the right-hand rule for its vertex order. For a connected, orientable manifold mesh with genus $g$ and $b$ border loops, the [Euler-Poincaré formula](/euler-poincare-formula/) gives $\chi = V - E + F = 2 - 2g - b$.

## Examples and non-examples

**Examples.**

- **A tetrahedron** with faces $(0, 2, 1), (0, 1, 3), (1, 2, 3), (0, 3, 2)$. Each edge has valence 2. The link of vertex 0 has the nodes 1, 2 and 3 and the link edges $\{2, 1\}$, $\{1, 3\}$, $\{3, 2\}$, which form one cycle. The mesh is closed, consistently oriented, and $\chi = 4 - 6 + 4 = 2$.
- **A single triangle.** Each edge has valence 1, and each link is one link edge, a path. It is a disk with one border loop, $\chi = 1$.
- **An open box**, a cube without its top face. The four top edges are border edges, and they form one border loop. The top vertices have a path of two link edges as their link. $\chi = 8 - 12 + 5 = 1 = 2 - 0 - 1$.
- **A Möbius strip** made of triangles. It is a manifold mesh, but it is not orientable: each choice of face orders leaves some inner edge used twice in the same direction.

**Non-examples.**

- **Two cones that meet at their tips.** Let vertex 0 be the common tip, with the upper rim $1, 2, 3, 4$ and the lower rim $5, 6, 7, 8$, and the faces $(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1)$ and $(0, 6, 5), (0, 7, 6), (0, 8, 7), (0, 5, 8)$. Each edge has valence 1 or 2, so the mesh is edge-manifold. But $\mathrm{Lk}(0)$ is two disjoint cycles, $1, 2, 3, 4$ and $5, 6, 7, 8$. So vertex 0 is a non-manifold vertex: a small ball around the tip meets the surface in two disks that share one point, which is not a disk. Here $\chi = 9 - 16 + 8 = 1$, and this is not $2 - 2g - b$ for the two border loops and any $g \ge 0$.
- **A bow tie.** The triangles $(0, 1, 2)$ and $(0, 3, 4)$ share only the vertex 0. All edges have valence 1, but $\mathrm{Lk}(0)$ is two disjoint paths, so vertex 0 is non-manifold. This is the border form of the two cones.
- **Three triangles on one edge**, $(0, 1, 2)$, $(1, 0, 3)$ and $(0, 1, 4)$. The edge $\{0, 1\}$ has valence 3, and node 1 has degree 3 in $\mathrm{Lk}(0)$. This is a non-manifold edge. Such edges come up where two closed solids touch along an edge, or where a wall is attached to a closed shell.
- **A triangle soup**, where each face has its own copies of its vertices. Each face is a separate disk, so the mesh is manifold, but it is not the surface it shows: every edge is a border edge. [Vertex welding](/vertex-welding/) merges the copies. It can also create non-manifold edges and vertices where two parts only touch.

## Related definitions

- **[Polygon mesh](/polygon-mesh/).** The general mesh, with the Euler characteristic and the half-edge structure. This page makes its 2-manifold condition precise with the link.
- **[Manifold solid](/manifold-solid/).** A solid whose boundary is a closed, orientable 2-manifold. A closed, orientable manifold mesh without self-intersections bounds such a solid.
- **[Consistent mesh orientation](/consistent-mesh-orientation/).** The algorithm that orients a manifold mesh, or reports that it is not orientable.
- **[Euler-Poincaré formula](/euler-poincare-formula/).** The relation $\chi = 2 - 2g - b$ for each connected, orientable manifold mesh.
- **[Mesh repair](/mesh-repair-problem/).** The problem of turning a mesh with non-manifold edges and vertices, holes and self-intersections into a manifold mesh.
- **[Doubly connected edge list](/doubly-connected-edge-list/)** and **[corner table](/corner-table/).** Structures that store only manifold meshes. The [radial edge structure](/radial-edge-data-structure/) stores non-manifold meshes as well.

## References
