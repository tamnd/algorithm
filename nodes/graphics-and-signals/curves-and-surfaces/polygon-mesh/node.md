---
tag: 0ZQRT2
kind: definition
slug: polygon-mesh
name: Polygon mesh
aliases:
- triangle mesh
- surface mesh
area: graphics-and-signals/curves-and-surfaces
level: intro
summary: A surface made of flat polygons that share edges and vertices, stored as vertex positions and faces; for a closed oriented mesh of genus g, V - E + F = 2 - 2g.
prereqs: [euler-formula, graph-genus]
see_also: [doubly-connected-edge-list, rotation-system, subdivision-surface, surface-tessellation, isosurface-extraction, surface-reconstruction, mesh-simplification, implicit-surface]
sources:
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, A K Peters, 2010
    locator: Chapter 1, Surface Representations, and Chapter 2, Mesh Data Structures, pages 21 to 28 (face-based, edge-based, halfedge-based and directed-edge structures)
  - paper: doi:10.1145/1499949.1500071
    title: Bruce G. Baumgart, A polyhedron representation for computer vision, Proceedings of the AFIPS National Computer Conference 44, 589 to 596, 1975
    locator: the winged-edge structure, with the vertex, edge and face records and the edge pointers
---

A polygon mesh is a surface made of flat polygons, the faces, that are glued together along shared edges and shared vertices. It is the most common way to store a shape for drawing and for geometric computation. A mesh has two parts: the geometry, a position in space for each vertex, and the connectivity, which says which vertices make each face. When all faces are triangles it is a triangle mesh; quadrilateral meshes are also common. The numbers of vertices $V$, edges $E$ and faces $F$ of a closed, oriented mesh obey the [Euler formula](/euler-formula/) $V - E + F = 2 - 2g$, where $g$ is the genus, the number of handles.

## Definition

**Mesh.** A polygon mesh is a pair of a finite set of vertices $\{1, \ldots, V\}$ with positions $p_1, \ldots, p_V \in \mathbb{R}^3$, and a finite list of faces. Each face is a cyclic sequence $(v_1, v_2, \ldots, v_k)$ of $k \ge 3$ different vertices. The edges are the unordered pairs $\{v_i, v_{i+1}\}$ of cyclically adjacent vertices of a face; the face uses the edge in the direction $v_i \to v_{i+1}$. A triangle mesh has $k = 3$ for all faces. The faces are flat polygons in the geometric meaning only when their vertices lie in a plane, which is always true for triangles.

**2-manifold.** A mesh is a 2-manifold, possibly with a border, when two conditions hold:

1. Each edge is in one or two faces. An edge in one face is a border edge; an edge in two faces is an inner edge.
2. At each vertex, the faces that contain it form one fan: they can be ordered $f_1, \ldots, f_d$ so that $f_i$ and $f_{i+1}$ share an edge at the vertex. The fan closes into a cycle at an inner vertex, and it is a path that starts and ends at border edges at a border vertex.

Then each point of the surface has a neighborhood like a disk, or like a half disk on the border. The mesh is closed, or watertight, when it has no border edges. In this encyclopedia, a mesh is a 2-manifold unless the page says otherwise.

**Orientation.** A 2-manifold mesh is consistently oriented when the two faces of each inner edge use it in opposite directions. Then the normal $(p_{v_2} - p_{v_1}) \times (p_{v_3} - p_{v_1})$ of each triangle points to the same side of the surface, and for a closed mesh the usual choice is the outside. A mesh that has a consistent orientation is orientable.

**Euler characteristic.** The Euler characteristic of a mesh is $\chi = V - E + F$. For a connected, orientable 2-manifold mesh with genus $g$ and $b$ border loops,
$$V - E + F = 2 - 2g - b.$$
So a closed sphere-like mesh has $\chi = 2$, a torus has $\chi = 0$, and a closed mesh with $g$ handles has $\chi = 2 - 2g$. The value of $\chi$ depends only on the surface, not on how it is cut into faces. For a planar graph this is the [Euler formula](/euler-formula/) $V - E + F = 2$, and the genus here is the genus of the surface, which bounds the [graph genus](/graph-genus/) of the edge graph from above. For each component, $\chi$ is added.

**Triangle meshes.** In a closed triangle mesh each face has 3 edges and each edge is in 2 faces, so $2E = 3F$. With the Euler formula this gives $F = 2V - 4 + 4g$ and $E = 3V - 6 + 6g$. So a large closed triangle mesh has about twice as many faces as vertices, and the average vertex degree $2E / V = 6 - (12 - 12g) / V$ is close to 6.

**Face-vertex lists.** The simplest storage is an array of positions and an array of faces, each face a list of indices into the positions. A triangle mesh then needs $3V$ numbers and $3F \approx 6V$ indices. This is the indexed face set of the OBJ, PLY and OFF file formats. It answers "what are the vertices of face $f$" at once, but the faces around a vertex or the neighbors across an edge need a search, or extra tables built from the list. A polygon soup is a list of faces with their own copies of the positions and no shared indices; it does not record that two faces meet.

**Half-edge structure.** Each edge is split into two half-edges with opposite directions. Each half-edge $h$ stores the vertex it points to, $\operatorname{target}(h)$; its twin $\operatorname{twin}(h)$, the other half of the same edge; the next half-edge $\operatorname{next}(h)$ of its face, in the order of the face; and its face $\operatorname{face}(h)$, or none for a half-edge on the border. Each vertex stores one outgoing half-edge, and each face stores one of its half-edges. Then the origin of $h$ is $\operatorname{target}(\operatorname{twin}(h))$; the half-edges of a face are $h, \operatorname{next}(h), \operatorname{next}^2(h), \ldots$; and the outgoing half-edges at a vertex are $h, \operatorname{next}(\operatorname{twin}(h)), \ldots$, so all neighbors of a vertex of degree $d$ are found in $O(d)$ steps. The structure can only store an oriented 2-manifold, and its updates for edge flips, splits and collapses are local. It is the [doubly connected edge list](/doubly-connected-edge-list/) of planar subdivisions, used on a surface; the next and twin pointers together are a [rotation system](/rotation-system/). The winged-edge structure of Baumgart, 1975, stores one record per edge with pointers to the four edges next to it, and the directed-edge structure is a half-edge structure for triangle meshes that finds the twin and the face from array positions.

## Examples and non-examples

**Meshes.**

- The tetrahedron with $p_0 = (0, 0, 0)$, $p_1 = (1, 0, 0)$, $p_2 = (0, 1, 0)$, $p_3 = (0, 0, 1)$ and the faces $(0, 2, 1)$, $(0, 1, 3)$, $(0, 3, 2)$, $(1, 2, 3)$. Each of the 6 edges is used once in each direction, so it is closed and consistently oriented, and the normal of $(0, 2, 1)$ is $(0, 1, 0) \times (1, 0, 0) = (0, 0, -1)$, pointing out. $V - E + F = 4 - 6 + 4 = 2$, so $g = 0$.
- The cube as 6 quadrilaterals: $8 - 12 + 6 = 2$. The same cube with each face split into 2 triangles: $8 - 18 + 12 = 2$, which also checks $2E = 3F$.
- A torus made from an $m$ by $n$ grid of quadrilaterals, $m, n \ge 3$, with opposite sides glued: $V = mn$, $E = 2mn$, $F = mn$, so $\chi = 0$ and $g = 1$.
- A single triangle: $3 - 3 + 1 = 1 = 2 - 0 - 1$, a disk with one border loop. A square ring of 8 quadrilaterals around a square hole: $V = 16$, $E = 24$, $F = 8$, $\chi = 0 = 2 - 0 - 2$, with two border loops.

**Non-examples.**

- Three triangles that share one edge. That edge is in three faces, so the mesh is not a 2-manifold; such an edge is a non-manifold edge.
- Two tetrahedra that share one vertex: $V = 7$, $E = 12$, $F = 8$, and $\chi = 3$, which is not $2 - 2g$ for any $g$. The faces at the shared vertex form two fans, not one, so the vertex is non-manifold.
- A cube stored as a polygon soup, with 4 new vertices for each face. It looks closed, but it is 6 separate squares: $V = 24$, $E = 24$, $F = 6$, and $\chi = 6$, six disks. Merging the equal positions gives the closed cube.
- A Möbius strip, for example 5 triangles in a cyclic band with a half twist. It is a 2-manifold with one border loop, but it is not orientable, so it has no consistent orientation and no half-edge structure in the sense above.
- Two triangles $(0, 1, 2)$ and $(0, 1, 3)$ that share the edge $\{0, 1\}$ in the same direction. The mesh is a 2-manifold, but it is not consistently oriented; reversing one face fixes it.

## Related definitions

- **[Doubly connected edge list](/doubly-connected-edge-list/)** and **[rotation system](/rotation-system/).** The half-edge structure for planar subdivisions, and the cyclic orders of the edges at each vertex that it encodes.
- **[Graph genus](/graph-genus/)** and the **[Euler formula](/euler-formula/).** The genus of the smallest orientable surface that holds a graph, and the relation $V - E + F = 2$ for plane graphs.
- **[Triangulation](/triangulation/)** and **[tetrahedralization](/tetrahedralization/).** Subdivisions of a planar region into triangles, or of a solid into tetrahedra; a surface mesh is the 2D analog on a curved surface.
- **[Subdivision surface](/subdivision-surface/).** The smooth limit of a mesh under repeated refinement.
- **[Implicit surface](/implicit-surface/)** and **[parametric surface](/parametric-surface/).** Other ways to describe a surface. [Isosurface extraction](/isosurface-extraction/) and [surface tessellation](/surface-tessellation/) turn them into meshes.
- **[Surface reconstruction](/surface-reconstruction/)** and **[mesh simplification](/mesh-simplification/).** Making a mesh from sampled points, and making a mesh smaller.

## References
