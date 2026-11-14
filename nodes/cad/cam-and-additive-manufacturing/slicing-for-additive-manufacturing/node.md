---
tag: HYJGRM
kind: problem
slug: slicing-for-additive-manufacturing
name: Slicing for additive manufacturing
aliases:
- layer slicing
- model slicing
area: cad/cam-and-additive-manufacturing
level: intro
summary: Cut a solid or mesh by a stack of planes into closed contours, one set per layer, as the first step of every 3D printing process.
prereqs: [polygon-mesh, polygon-with-holes]
see_also: [triangle-mesh-slicing, adaptive-slicing, staircase-effect, vertex-welding, mesh-repair-problem, simulation-of-simplicity, point-in-polygon, marching-squares]
sources:
  - paper: doi:10.1016/j.cad.2017.07.001
    title: Rodrigo Minetto, Neri Volpato, Jorge Stolfi, Rodrigo M. M. H. Gregori and Murilo V. G. da Silva, An optimal algorithm for 3D triangle mesh slicing, Computer-Aided Design 92, 2017, 1 to 10
    locator: the statement of the slicing problem for a triangle mesh and the lower bound for it
  - book: isbn:978-3-030-56126-0
    title: Ian Gibson, David Rosen, Brent Stucker and Mahyar Khorasani, Additive Manufacturing Technologies, 3rd edition, Springer, 2021
    locator: the process chain from CAD model to STL file to sliced layers (chapter not confirmed)
  - paper: doi:10.1016/0010-4485(94)90032-9
    title: Atanas Dolenc and Ismo Mäkelä, Slicing procedures for layered manufacturing techniques, Computer-Aided Design 26(2), 1994, 119 to 126
    locator: the slicing of a model into layers of chosen thickness
---

Slicing is the step of 3D printing that turns a solid into layers. The input is a solid, almost always given as a triangle mesh, and a set of heights. The output, for each height, is the cross-section of the solid with the horizontal plane at that height, as a set of closed oriented polygons: the outer boundaries and the holes of a [polygon with holes](/polygon-with-holes/). Every later step of the print, from walls and infill to supports and toolpaths, works on these contours. The problem is easy to state for a clean solid in general position. The difficulty is in the input: the usual file format, STL, is a list of separate triangles with no shared vertices and no topology, the coordinates are rounded floats, and the planes often pass exactly through vertices and horizontal faces.

## In plain words

A printer cannot print a 3D shape at once. It prints one thin flat layer, then the next one on top. So the shape must first be cut into thin flat slices, like a loaf of bread. For each slice, the printer needs the outline of the shape at that height: an outer loop and loops around each hole.

The cut is simple for a clean model. Real files are harder. They list loose triangles that only happen to touch, and some cuts pass exactly through a corner or along a flat face, where the outline is not clear.

## Definition

**Input.** A triangle mesh $M$ with $n$ triangles that is the boundary of a solid $S$: a closed, oriented [manifold mesh](/manifold-mesh/) whose faces have outward normals by the right-hand rule. The input also has heights $z_1 < z_2 < \dots < z_k$, either given or chosen from a layer thickness.

**Output.** For each $j$, the section $S \cap \{z = z_j\}$, given as a finite set of closed polygons, each oriented with the solid on its left (outer boundaries counterclockwise, holes clockwise, seen from above). The polygons are disjoint, and the region they bound with the even-odd or nonzero rule is the section.

**General position.** If no vertex of $M$ has a height $z_j$, then each plane cuts each triangle in a segment or not at all. The segments of one plane then link into disjoint simple closed polygons, because each edge of a closed manifold has exactly two triangles. Let $m$ be the total number of segments.

**Degenerate planes.** If a plane passes through a vertex, the section can have a point, an edge or a face where the solid only touches the plane, and the output is not defined by the formula above. A solution must fix a rule. The common rule treats the plane $z = z_j$ as $z = z_j - \varepsilon$ for an infinitely small $\varepsilon > 0$ (or $+\varepsilon$). This is a symbolic perturbation, see [simulation of simplicity](/simulation-of-simplicity/). With such a rule, every plane is in general position, and the output is the limit of the sections just below the plane.

## Variants

- **Uniform or adaptive layers.** The heights are equally spaced, or they are chosen from the surface slope to bound the [staircase effect](/staircase-effect/), see [adaptive slicing](/adaptive-slicing/).
- **Mesh repair first.** If the input is a polygon soup that is not closed or not oriented, the section is not defined until the mesh is repaired, see [mesh repair](/mesh-repair-problem/). Slicers often accept such input and close each contour heuristically.
- **Direct slicing.** The section is computed from the exact CAD model (a B-rep with NURBS faces), not from a mesh. The contours are then curves, which avoids the chord error of the mesh.
- **Voxel and implicit models.** For a model given as a grid of values, each layer is a 2D grid, and the contours are found with [marching squares](/marching-squares/).
- **Non-planar layers.** Some processes use curved layers or a tilting build direction. The planes are replaced by a family of surfaces.

## Examples

**A cube.** Let $M$ be the cube $[0, 2]^3$ as 12 triangles, two per face. The plane $z = 1$ meets the 8 side triangles and none of the 4 top and bottom triangles. Each side triangle gives one segment, and the 8 segments link into one counterclockwise square with corners $(0, 0)$, $(2, 0)$, $(2, 2)$, $(0, 2)$ and area 4. Here $m = 8$.

**A degenerate plane.** The plane $z = 2$ contains the top face of the same cube. With the rule $z_j - \varepsilon$, the plane is just below the top, the 8 side triangles cross it, and the section is the same square of area 4. With the rule $z_j + \varepsilon$, the plane is above the cube, nothing crosses it, and the section is empty. Both answers are limits of true sections, and a slicer must choose one. For the top layer of a print, the first one is the right choice.

**No topology.** In an STL file the same cube is 36 vertex records, three per triangle, and the segment end points of two neighbor triangles are computed from separate copies of the shared edge. With integer or exact coordinates the copies are equal. With float coordinates, two copies of an edge that were written with different rounding give end points that differ in the last digits, and a slicer that links end points by exact equality finds open chains. This is why slicers weld vertices first, see [vertex welding](/vertex-welding/).

## Known algorithms

- **One plane at a time.** Cut every triangle with every plane: $O(nk)$ time even if most triangles miss most planes.
- **[Triangle mesh slicing](/triangle-mesh-slicing/).** Minetto, Volpato, Stolfi, Gregori and da Silva (2017) find, for each triangle, the range of planes that it crosses by binary search or by direct index for uniform spacing, keep an active list of triangles per plane, and link segments by a hash table. The time is $O(n \log k + k + m)$ in general and $O(n + k + m)$ for uniform spacing or sorted input. In the corrigendum the bound of the linking step is in expected time, because of the hash table.
- **[Adaptive slicing](/adaptive-slicing/).** Chooses the heights first and then cuts as above.

## Bounds

Every algorithm must read the $n$ triangles and the $k$ heights and write the $m$ segments, so $\Omega(n + k + m)$ time is needed. The output size $m$ can be as large as $\Theta(nk)$, for example for $n$ long thin vertical triangles that span all $k$ planes. Minetto and coauthors prove a worst-case lower bound of $\Omega(n \log k + k + m)$ for general heights, where the $\log k$ term comes from locating the triangle heights among the planes. So their algorithm is asymptotically optimal in that setting.

## Reductions

- **Point membership.** A point $(x, y, z_j)$ is in the solid if and only if $(x, y)$ is inside the section polygons by the even-odd rule. So one slice turns 3D point membership at that height into [point in polygon](/point-in-polygon/).
- **Area and volume.** The area of a section follows from the [shoelace formula](/shoelace-formula/) on its oriented polygons, with holes negative. The sum of the areas times the layer thicknesses approximates the volume of the solid.
- **Contours of a height field.** Slicing a terrain mesh at equal heights gives its contour lines. It is the same problem on a surface that is not closed, so the chains can be open.

## Applications

- Every additive process: material extrusion, vat photopolymerization, powder bed fusion and binder jetting. Each prints the contours of each layer.
- Layered models in medicine and geology, where a solid is rebuilt from or cut into slices.
- Laser and water-jet cutting of stacked sheets, where each sheet is one slice.

## References
