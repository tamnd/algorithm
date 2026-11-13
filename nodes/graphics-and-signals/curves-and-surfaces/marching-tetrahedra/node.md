---
tag: 2FMDJR
kind: algorithm
slug: marching-tetrahedra
name: Marching tetrahedra
aliases:
- marching tets
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Extracts an isosurface mesh by cutting each grid cube into tetrahedra and contouring the linear interpolant in each one; there are no ambiguous cases.
solves: [isosurface-extraction]
model: real-ram
complexity:
  vars: {n: the number of cells of the grid, t: the number of output triangles}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: O(t)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1991
  people: [Akio Doi, Akio Koide]
  note: Doi and Koide, at IBM Japan, triangulated equi-valued surfaces with tetrahedral cells, which removes the ambiguous cases of the cube table.
prereqs: [isosurface-extraction, marching-squares, tetrahedralization]
see_also: [marching-cubes, dual-contouring, triangulation, piecewise-linear-interpolation, implicit-surface, polygon-mesh, mesh-simplification]
sources:
  - paper: "Akio Doi and Akio Koide, An efficient method of triangulating equi-valued surfaces by using tetrahedral cells, IEICE Transactions on Information and Systems E74-D(1), 214 to 224, 1991"
    locator: the whole paper (the division of the cube into tetrahedra, the cases of one tetrahedron and the shared vertices)
  - paper: doi:10.1145/37401.37422
    title: William E. Lorensen and Harvey E. Cline, Marching cubes, a high resolution 3D surface construction algorithm, Computer Graphics (SIGGRAPH 87 Proceedings) 21(4), 163 to 169, 1987
    locator: the whole paper (the cube method that marching tetrahedra refines)
  - paper: doi:10.1016/j.cag.2006.07.021
    title: Timothy S. Newman and Hong Yi, A survey of the marching cubes algorithm, Computers and Graphics 30(5), 854 to 879, 2006
    locator: the section on tetrahedral decompositions (5 and 6 tetrahedra per cube, the extra triangles, the dependence on the diagonals)
  - book: isbn:9781930934191
    title: Will Schroeder, Ken Martin and Bill Lorensen, The Visualization Toolkit, An Object-Oriented Approach to 3D Graphics, fourth edition, Kitware, 2006
    locator: Chapter 6, Fundamental Algorithms, Section 6.2, Scalar Algorithms (marching tetrahedra as the way to avoid the ambiguous cases)
---

Marching tetrahedra builds a triangle mesh of the surface $f = c$ from a 3D grid of samples, like [marching cubes](/marching-cubes/), but it first cuts each cube into tetrahedra. On a tetrahedron, the [piecewise linear interpolant](/piecewise-linear-interpolation/) of the four corner samples is a linear function, so its level set is a flat triangle, a flat quadrilateral, or empty. There are only 16 sign patterns, and none of them is ambiguous: a face of a tetrahedron is a triangle and is always cut by at most one segment. The output is exactly the level set of the piecewise linear interpolant, and it is closed when the field is outside on the border. The price is more triangles than marching cubes, and a result that depends on which diagonals the cut uses.

## In plain words

A cube has square faces, and on a square face the low corners can sit on a diagonal. Then the surface could cut the face in two ways, and two cubes must agree. A triangle does not have this problem: if one or two of its three corners are low, there is only one way to cut it.

So cut each cube of the grid into six tetrahedra, pyramids with four triangular faces, all around the long diagonal of the cube. In each tetrahedron, a flat cut separates the low corners from the others. With one low corner (or one high corner) the cut is a triangle. With two low corners it is a four-sided piece, split into two triangles. The cut crosses each edge where a straight-line guess between the two ends gives the target value. Neighbors share these points.

## The problem

The input is a grid of samples $f[z][y][x]$, $0 \le x < X$, $0 \le y < Y$, $0 \le z < Z$, with $X, Y, Z \ge 2$, and an iso value $c$, as for [marching cubes](/marching-cubes/). A sample is inside when its value is less than $c$. Each of the $n = (X - 1)(Y - 1)(Z - 1)$ cells is cut into the 6 tetrahedra of the Kuhn (or Freudenthal) [tetrahedralization](/tetrahedralization/): with corner $k$ of the cell at offset $(k \bmod 2, \lfloor k/2 \rfloor \bmod 2, \lfloor k/4 \rfloor)$, they are the 6 monotone paths from corner 0 to corner 7 that change one coordinate at a time,

$$\{0,1,3,7\},\ \{0,2,3,7\},\ \{0,2,6,7\},\ \{0,4,6,7\},\ \{0,4,5,7\},\ \{0,1,5,7\}.$$

The tetrahedron of the path that adds the axes in the order $a, b, d$ is the set of points of the cell with $u_a \ge u_b \ge u_d$ in local coordinates. Every cube face is cut along the diagonal from its lowest corner to its highest one, the same way for the two cells that share it, so the tetrahedra of the whole grid meet face to face. The output is a [polygon mesh](/polygon-mesh/) that is the level set $\{\ell = c\}$ of the interpolant $\ell$ that is linear on each tetrahedron and equals $f$ at the samples.

## The algorithm

A table over the 16 sign patterns of one tetrahedron is built once, from vertices 0 to 3 of a reference tetrahedron.

```pseudo id=main
MARCHING-TETRAHEDRA(f, c)
L1  V ← empty list, T ← empty list, index ← empty map
L2  for each cell (x, y, z) do
L3      for each of the 6 tetrahedra τ = (τ_0, τ_1, τ_2, τ_3) of the cell do
L4          m ← Σ_i 2^i · [f(τ_i) < c]
L5          for each triangle ((i_1, j_1), (i_2, j_2), (i_3, j_3)) in TET-TABLE[m] do
L6              for each pair (i, j): key ← the grid points τ_i, τ_j as a sorted pair
L7                  if key is not in index then index[key] ← |V|; append CROSS(τ_i, τ_j) to V
L8              append the three indices to T
L9  return (V, T)

BUILD-TET-TABLE()
L10 for m ← 0 to 15 do                    ▷ I = the inside vertices of the pattern m, O = the others
L11     if |I| = 1 or |I| = 3 then one triangle on the 3 edges at the vertex that is alone on its side
L12     else if |I| = 2, I = {a, b}, O = {c, d} then the quadrilateral ac, ad, bd, bc, as the triangles (ac, ad, bd) and (ac, bd, bc)
L13     orient each triangle so that its normal points toward an outside vertex
```

Lines L11 and L12 are all the cases: with 0 or 4 inside vertices the level set misses the tetrahedron. In the quadrilateral, consecutive vertices lie on a common face of the tetrahedron (for example $ac$ and $ad$ on the face $acd$), so the four points are in cyclic order, and the chord from $ac$ to $bd$ joins two edges that share no face; it lies inside the tetrahedron. Line L13 makes the orientation test once, on the reference tetrahedron with the vertices at edge midpoints, where the level set is a plane between the inside and the outside vertices; the result carries over to every tetrahedron of the grid, because line L3 lists the 6 tetrahedra with positive orientation, as $(0,1,3,7), (0,3,2,7), (0,2,6,7), (0,6,4,7), (0,4,5,7), (0,5,1,7)$; every second path of the list above has its two middle vertices swapped, since in path order it is negatively oriented. So the map from the reference keeps orientation. CROSS is the linear interpolation $p_u + \frac{c - f_u}{f_v - f_u}(p_v - p_u)$ along the tetrahedron edge, which can be a cell edge, a face diagonal or the body diagonal.

## Example

Take the cell of the [marching cubes](/marching-cubes/) example: $f_0 = 0$, $f_7 = 1$, the other six corners equal to 4, and $c = 2$. Corners 0 and 7 are in all 6 tetrahedra, so each tetrahedron has the pattern with its first and last vertex inside, and line L12 gives a quadrilateral, as 2 triangles.

| crossings at $t = 1/2$ from corner 0 | crossings at $1/3$ of the way from corner 7 |
| --- | --- |
| $(\tfrac12, 0, 0)$, $(0, \tfrac12, 0)$, $(0, 0, \tfrac12)$ | $(1, 1, \tfrac23)$, $(1, \tfrac23, 1)$, $(\tfrac23, 1, 1)$ |
| $(\tfrac12, \tfrac12, 0)$, $(\tfrac12, 0, \tfrac12)$, $(0, \tfrac12, \tfrac12)$ | $(1, \tfrac23, \tfrac23)$, $(\tfrac23, 1, \tfrac23)$, $(\tfrac23, \tfrac23, 1)$ |

The mesh has 12 vertices, one on each of the 12 tetrahedron edges with a sign change, and 12 triangles. It is a tube around the diagonal from corner 0 to corner 7: along that diagonal the interpolant runs from 0 to 1 and stays below $c = 2$, so in this tetrahedralization the two inside corners are joined. Marching cubes gives 2 separate triangles for the same cell, one around each corner. Both answers fit the 8 samples; they differ in the interpolant between them. With the other diagonal (from corner 1 to corner 6, whose values are 4), the tetrahedra would separate the two corners.

For the two cells with an ambiguous shared face of the second marching cubes example, marching tetrahedra gives 13 vertices and 12 triangles, and there is no choice to make: the face is cut along its diagonal from $(1, 0, 0)$ to $(1, 1, 1)$, both inside, so the two inside corners of the face are joined.

## Correctness

**Claim.** Assume no sample equals $c$. In each tetrahedron, the triangles of the output cover exactly the set $\{\ell = c\}$. Every mesh edge that is not on the border of the box is in exactly two triangles, once in each direction, and the link of each such vertex is one cycle. So, if every border sample is outside, the mesh is a closed, oriented 2-manifold, and it is the exact level set of the piecewise linear interpolant.

On a tetrahedron, $\ell$ is linear, so $\{\ell = c\}$ is the intersection of a plane with the tetrahedron, the convex hull of the crossing points on its edges, which is the triangle or the quadrilateral of lines L11 and L12. On a triangular face with a sign change, the plane cuts exactly one segment, which depends only on the three samples of the face. So two tetrahedra that share a face cut it in the same segment, and they see it in opposite orientations. The argument for edges and vertex links is then the same as for marching cubes, with tetrahedra in place of cubes. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the [real RAM](/real-ram/), or exact rational arithmetic on numbers of bounded size, with a [hash table](/hash-table/) for the vertex map ($O(1)$ expected time per operation).

- **Time.** Each cell costs $O(1)$: 6 tetrahedra with at most 2 triangles each. The time is $\Theta(n)$ in all cases.
- **Output size.** At most 12 triangles per cell, so $t \le 12 n$. The vertices lie on up to 7 kinds of edges per grid point (3 cell edges, 3 face diagonals, 1 body diagonal) instead of 3, and a smooth surface typically gets about twice as many triangles as with marching cubes or more, depending on the surface and the grid.
- **Space.** $\Theta(V + t)$ for the output and the vertex map.

## Properties

- **No ambiguity.** Each face is a triangle, so the cut of a face is determined by its three signs, and no table entry is a choice.
- **Exact level set.** The mesh is the level set of a well defined interpolant, the piecewise linear one, not just a surface with the right edge crossings. A [linear field](/piecewise-linear-interpolation/) gives a mesh exactly on its plane.
- **Topology depends on the diagonals.** The interpolant, and so the topology, depends on the tetrahedralization. The 6-tetrahedra cut used here favors the diagonal from corner 0 to corner 7 in every cell, so the output is not invariant under rotations of the grid.
- **Many thin triangles.** The triangles are smaller and often thinner than with marching cubes. [Mesh simplification](/mesh-simplification/) usually follows.
- **Works on any tetrahedral mesh.** The same per-tetrahedron step contours a field given on an unstructured tetrahedral mesh, as in finite element output.

## Variants and improvements

- **Five tetrahedra per cube.** A cube can be cut into 5 tetrahedra, one central one and four at the corners. Neighboring cubes must then alternate between the two mirror images, or the face diagonals do not match.
- **Body centered grids.** Adding a sample at each cube center and using the tetrahedra between neighboring centers and corners gives a more symmetric result.
- **Unstructured meshes.** For data on a [tetrahedralization](/tetrahedralization/), skip lines L2 and L3 and run lines L4 to L8 on each tetrahedron.
- **Interval search.** Skip tetrahedra whose min and max do not bracket $c$, with a tree on the intervals, which makes the cost depend on the number of cut tetrahedra; see [isosurface extraction](/isosurface-extraction/).
- **Cube methods.** [Marching cubes](/marching-cubes/) gives fewer triangles with a case table, and [dual contouring](/dual-contouring/) gives one vertex per cell and sharp features.

## When to use it

Use marching tetrahedra when the data is already on tetrahedra, when you want a mesh that is the exact level set of a known interpolant, or when you want closed output with no case table to get right. It is a good reference method for testing a marching cubes table, because it has no choices. Use marching cubes when the triangle count matters, and dual contouring when sharp features matter.

## Pitfalls

- **Inconsistent diagonals.** Cutting neighboring cubes so that a shared face gets different diagonals leaves cracks along that face. With the 6-tetrahedra cut of line L3, every face is cut from its lowest corner to its highest; with 5 tetrahedra, alternate the two forms in a checkerboard pattern.
- **Mixed orientations.** Building the table on a reference tetrahedron and applying it to tetrahedra listed with negative orientation flips their triangles, and the mesh has inconsistent normals. List every tetrahedron of line L3 with a positive determinant, or test the orientation on its real coordinates.
- **The quad split.** Splitting the quadrilateral of line L12 as $(ac, ad, bc)$ and $(ad, bd, bc)$ is also valid, but splitting it with the vertices out of cyclic order, as $(ac, bd, ad)$ and $(ad, bc, bd)$, gives overlapping triangles and a hole. Keep the cyclic order $ac, ad, bd, bc$.
- **Ties.** A sample equal to $c$ puts vertices of several edges at one point and gives triangles of area zero. Use one strict test, $f < c$, in line L4 everywhere.
- **Diagonal vertices not shared.** The vertex key of line L6 must cover face and body diagonals as well as cell edges, or the diagonals get duplicate vertices and the mesh opens.

## Implementations

## History

Doi and Koide published the method in 1991, in the IEICE Transactions on Information and Systems, as an efficient way to triangulate equi-valued surfaces with tetrahedral cells. It removes the ambiguous faces that Dürst had pointed out in the marching cubes table in 1988. The Kuhn triangulation of the cube into 6 simplices along the main diagonal is much older and is the standard simplicial subdivision of a cube in any dimension.

## References
