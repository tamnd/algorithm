---
tag: N004FS
kind: algorithm
slug: marching-cubes
name: Marching cubes
aliases:
- marching cubes algorithm
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Extracts a triangle mesh of an isosurface from a 3D grid of samples, one cube at a time, with a 256-entry table indexed by the signs of the 8 corners.
solves: [isosurface-extraction]
model: real-ram
complexity:
  vars: {n: the number of cells of the grid, t: the number of output triangles}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: O(t)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1987
  people: [William E. Lorensen, Harvey E. Cline]
  note: Lorensen and Cline, at General Electric, built surfaces from CT and MR volumes with a case table of 15 patterns; Dürst (1988) and Nielson and Hamann (1991) showed that ambiguous faces can leave holes and how to decide them.
prereqs: [isosurface-extraction, marching-squares, polygon-mesh]
see_also: [marching-tetrahedra, dual-contouring, implicit-surface, poisson-surface-reconstruction, mesh-simplification, uniform-grid, octree, signed-distance-function]
sources:
  - paper: doi:10.1145/37401.37422
    title: William E. Lorensen and Harvey E. Cline, Marching cubes, a high resolution 3D surface construction algorithm, Computer Graphics (SIGGRAPH 87 Proceedings) 21(4), 163 to 169, 1987
    locator: the whole paper (the cube, the 256 cases, the 15 patterns under rotation and complement, the edge interpolation and the normals from the gradient)
  - paper: "Martin J. Dürst, Letters: Additional reference to marching cubes, Computer Graphics 22(2), 72 to 73, 1988"
    locator: the whole letter (the ambiguous faces and the holes of the original table)
  - paper: doi:10.1109/VISUAL.1991.175782
    title: Gregory M. Nielson and Bernd Hamann, The asymptotic decider, resolving the ambiguity in marching cubes, Proceedings of Visualization 91, IEEE, 83 to 91, 1991
    locator: the whole paper (the bilinear interpolant on an ambiguous face, its saddle value, and the extra subcases of the table)
  - paper: doi:10.1016/j.cag.2006.07.021
    title: Timothy S. Newman and Hong Yi, A survey of the marching cubes algorithm, Computers and Graphics 30(5), 854 to 879, 2006
    locator: the sections on the topological problems of the original table, on the disambiguation methods and on the extensions
  - book: isbn:9781930934191
    title: Will Schroeder, Ken Martin and Bill Lorensen, The Visualization Toolkit, An Object-Oriented Approach to 3D Graphics, fourth edition, Kitware, 2006
    locator: Chapter 6, Fundamental Algorithms, Section 6.2, Scalar Algorithms (contouring, the 15 cube cases and the ambiguous cases)
---

Marching cubes builds a triangle mesh of the surface $f = c$ of a function $f$ that is known only at the points of a 3D grid. It looks at one cube of 8 samples at a time. Each corner is inside ($f < c$) or outside, which gives a case number from 0 to 255, and a table lists the triangles of the case as triples of cube edges. Each triangle vertex lies on a cube edge, at the point where linear interpolation of the two corner values gives $c$, and neighboring cubes share it. The cost is $\Theta(n)$ for a grid of $n$ cells. The table of the 1987 paper can leave holes at ambiguous faces; a table whose face cuts depend only on the face samples, as here, gives a closed surface.

## In plain words

A CT scanner gives the density of the body at the points of a 3D grid. To see the bone, you want the surface where the density crosses one value. Look at one small cube of the grid at a time. Each of its 8 corners is below the value or not. There are 256 patterns, and a table, built once, says which triangles cut the cube for each pattern. Each triangle corner lies on a cube edge where the value changes, at the point found by a straight-line guess between the two ends. Neighboring cubes put the same point on their shared edge, so their triangles join.

On some faces of the cube, the two low corners are diagonal to each other. The surface can then cut that face in two ways. Both cubes that share the face must pick the same way, or the mesh gets a hole.

## The problem

The input is a grid of samples $f[z][y][x]$, $0 \le x < X$, $0 \le y < Y$, $0 \le z < Z$, with $X, Y, Z \ge 2$, and an iso value $c$. This is [isosurface extraction](/isosurface-extraction/) on a [uniform grid](/uniform-grid/). A sample is inside when its value is less than $c$; a value equal to $c$ counts as outside. There are $n = (X - 1)(Y - 1)(Z - 1)$ cells. In a cell, corner $k \in \{0, \ldots, 7\}$ is at offset $(k \bmod 2, \lfloor k/2 \rfloor \bmod 2, \lfloor k/4 \rfloor)$, and the 12 cell edges join corners that differ in one bit. The output is a [polygon mesh](/polygon-mesh/) with $V$ vertices and $F = t$ triangles. Each vertex is on a grid edge whose two samples are on different sides of $c$, and each such edge carries exactly one vertex. When all border samples are outside, the mesh must be a closed, oriented 2-manifold, with normals that point to the outside.

## The algorithm

The table is built once. A cube face is a square cell of [marching squares](/marching-squares/), so its cut is given by the 16-case square table, with the inside on the left as seen from outside the cube. On an ambiguous face (the two inside corners on a diagonal), this implementation always takes the separated entry: it cuts off the two inside corners. Then the segments on the 6 faces close up into cycles of cube edges, and each cycle is triangulated.

```pseudo id=main
BUILD-TABLE()
L1  for case ← 0 to 255 do
L2      S ← the face segments of the 6 faces, each from the square table on its 4 signs (separated entry if ambiguous)
L3      join the segments of S into cycles of cube edges
L4      TABLE[case] ← a triangulation of each reversed cycle with no chord that lies on a cube face

MARCHING-CUBES(f, c)
L5  V ← empty list, T ← empty list, index ← empty map
L6  for each cell (x, y, z) do
L7      case ← Σ_k 2^k · [f(corner k) < c]
L8      for each triangle (e_1, e_2, e_3) in TABLE[case] do
L9          for each e_i: key ← the grid edge of e_i in this cell (its lower end and its axis)
L10             if key is not in index then
L11                 index[key] ← |V|; append CROSS(e_i) to V    ▷ as in marching squares
L12         append (index[e_1], index[e_2], index[e_3]) to T
L13 return (V, T)
```

Lines L1 to L4 make the table. The face segments go counterclockwise around the inside part of the cube surface, seen from outside, so the reversed cycle gives triangles whose normals point to the outside. A chord of a triangulation that joined two vertices on one face would lie in that face, and the cell on the other side could use the same pair; line L4 avoids such chords, and the implementation finds a valid triangulation for each of the 256 cases. No case has more than 4 cycles or more than 5 triangles. Lines L5 to L13 are the extraction. The map of lines L9 to L11 makes neighboring cells share the vertex on a shared edge. CROSS is the linear interpolation $p_u + \frac{c - f_u}{f_v - f_u}(p_v - p_u)$ of line L13 of marching squares.

Lorensen and Cline did not write out 256 cases. They grouped the cases into 15 patterns: two cases are in one pattern when a rotation of the cube maps one to the other, or maps one to the complement of the other (inside and outside exchanged). A count by the Burnside lemma over the 24 rotations gives 23 classes under rotation alone and 15 when complement is added; with reflections as well there are 14. The 15 patterns include the empty case 0.

Smooth shading needs a normal at each vertex. The 1987 paper takes the gradient of $f$ at the corners by central differences and interpolates it along the edge, as for the position.

## Example

Take one cell with $f_0 = 0$, $f_7 = 1$, the other six corners equal to 4, and $c = 2$. Corners 0 and 7 are inside, so the case is $1 + 128 = 129$. They are opposite ends of the body diagonal and share no face, so no face is ambiguous, and the table entry has two triangles, one around each corner.

| edge | from, to | values | $t$ | vertex |
| --- | --- | --- | --- | --- |
| 0 to 1 | $(0,0,0)$ to $(1,0,0)$ | 0, 4 | $1/2$ | $(\tfrac12, 0, 0)$ |
| 0 to 2 | $(0,0,0)$ to $(0,1,0)$ | 0, 4 | $1/2$ | $(0, \tfrac12, 0)$ |
| 0 to 4 | $(0,0,0)$ to $(0,0,1)$ | 0, 4 | $1/2$ | $(0, 0, \tfrac12)$ |
| 3 to 7 | $(1,1,0)$ to $(1,1,1)$ | 4, 1 | $2/3$ | $(1, 1, \tfrac23)$ |
| 5 to 7 | $(1,0,1)$ to $(1,1,1)$ | 4, 1 | $2/3$ | $(1, \tfrac23, 1)$ |
| 6 to 7 | $(0,1,1)$ to $(1,1,1)$ | 4, 1 | $2/3$ | $(\tfrac23, 1, 1)$ |

The first triangle is $(0, \tfrac12, 0), (0, 0, \tfrac12), (\tfrac12, 0, 0)$. Its normal $(B - A) \times (C - A) = (0, -\tfrac12, \tfrac12) \times (\tfrac12, -\tfrac12, 0) = (\tfrac14, \tfrac14, \tfrac14)$ points away from corner 0, to the outside.

Now take two cells side by side, with $c = 1/2$: the samples at $x = 0$ are all 9, at $x = 2$ all 0, and at $x = 1$ they are $f(1,0,0) = f(1,1,1) = 0$ and $f(1,1,0) = f(1,0,1) = 9$. The shared face $x = 1$ is ambiguous. The left cell has case 130 (corners 1 and 7 inside) and the table gives 2 triangles, which cut off the two inside corners of the face. The right cell has case 235: 6 corners inside, with the two outside corners on the shared face. Its entry cuts the shared face the same way, as two separate corner pieces, and has 4 triangles. The mesh has 8 vertices and 6 triangles, and every edge on the shared face is in one triangle of each cell. A table that treats case 235 as the complement of case 20 (2 triangles that cut off the two outside corners) cuts the shared face the other way, and the two cells leave a hole there.

## Correctness

**Claim.** Assume no sample equals $c$. The vertices are exactly the crossing points of the grid edges, one per edge with a sign change. Every edge of the mesh that is not on the border of the box is in exactly two triangles, with opposite directions, and the link of each vertex is one cycle. So, if every border sample is outside, the output is a closed, oriented combinatorial 2-manifold, and its Euler characteristic $V - E + F$ is even.

The proof has two parts. First, for each case, the boundary of the triangles of the case is the set of face segments, reversed; this is a check of the 256 entries. Second, the segments on a face depend only on the 4 samples of the face, so the two cells that share a face cut it in the same way, and they see the face with opposite orientations. The full proof, with the vertex links, is in [the correctness proof](proofs/correctness.md).

The claim is about the topology of the mesh, not about its fit to $f$. Between the samples, the mesh is one of several surfaces with the same edge crossings. With the fixed rule on ambiguous faces, it can join or split components differently from the trilinear interpolant of the cells.

## Complexity

The model is the [real RAM](/real-ram/), or exact rational arithmetic on numbers of bounded size, with unit cost per comparison and per arithmetic operation, and a [hash table](/hash-table/) for the vertex map with $O(1)$ expected time per operation. A dense array indexed by grid edge gives $O(1)$ worst case time instead.

- **Table.** The table has 256 entries and is built once, in $O(1)$ time, or copied from a constant.
- **Time.** Each of the $n$ cells reads 8 samples and emits at most 5 triangles with $O(1)$ work each. The time is $\Theta(n)$ in all cases, because every cell is visited.
- **Space.** The output takes $\Theta(V + t)$ space, and the vertex map holds one entry per vertex. A program that processes the grid one slice of cells at a time can keep the map for two slices only.
- **Output size.** $t \le 5n$. For a smooth closed surface of area $A$ in cells of side $h$, $t$ is of the order of $A/h^2$, while $n$ is of the order of the volume over $h^3$; most cells are empty, which is why the output-sensitive methods of [isosurface extraction](/isosurface-extraction/) and the [octree](/octree/) help.

## Properties

- **Local and parallel.** Each cell needs only its 8 samples and the table, so cells can be processed in any order or on many processors; only the vertex sharing needs a map or a second pass.
- **Watertight with a consistent face rule.** Any rule that cuts a face from its 4 samples only, such as the fixed separated rule here or the asymptotic decider, gives a closed mesh.
- **Vertices on edges.** Every vertex is on a grid edge. Sharp edges and corners of the true surface are cut off, and thin features between samples are lost.
- **Bad triangles.** Triangles near a sample with a value close to $c$ can be very small or very thin. The mesh often needs [mesh simplification](/mesh-simplification/) or smoothing.
- **Exact on rational input.** With integer or rational samples and a rational $c$, all vertices are exact rationals.

## Variants and improvements

- **Asymptotic decider.** Nielson and Hamann (1991) decide each ambiguous face by the saddle value of the bilinear interpolant on that face, as in [marching squares](/marching-squares/), and add subcases to the table. The face rule still reads only the face, so the mesh stays closed, and the face topology matches the trilinear interpolant.
- **Interior ambiguity.** Some cases are also ambiguous inside the cube, with a tunnel in the trilinear interpolant that the faces do not show. Chernyaev's marching cubes 33 and later work by Lewiner and others use extra tests and 33 base cases for this; see the survey of Newman and Yi.
- **Marching tetrahedra.** Cut each cube into tetrahedra and contour each one with the linear interpolant. There is no ambiguous case, at the cost of more triangles. See [marching tetrahedra](/marching-tetrahedra/).
- **Dual methods.** [Dual contouring](/dual-contouring/) puts one vertex inside each cell that the surface meets, at the point that best fits the tangent planes, and keeps sharp features.
- **Adaptive grids.** Run the method on the leaves of an [octree](/octree/), as in [Poisson surface reconstruction](/poisson-surface-reconstruction/). Leaves of different sizes create cracks that need extra patches.
- **Output sensitive search.** Skip empty cells with a min and max tree over the cells, an octree, or the span space of Livnat, Shen and Johnson.

## When to use it

Use marching cubes to turn a sampled volume into a mesh: medical CT and MR data, a level set of a simulation, or the [signed distance function](/signed-distance-function/) or other [implicit surface](/implicit-surface/) of a model sampled on a grid. It is short, fast, local and easy to run in parallel. Use a consistent face rule, as here or with the asymptotic decider, when the mesh must be closed. Use [dual contouring](/dual-contouring/) when sharp edges matter and gradients are known, and [marching tetrahedra](/marching-tetrahedra/) when you want no case table at all. To view a surface without a mesh, [ray marching](/ray-marching/) the field is an option.

## Pitfalls

- **A table with complement symmetry.** If the table takes case $255 - k$ as case $k$ with the triangles reversed, two cells that share an ambiguous face can cut it in different ways, and the mesh gets a hole, as in the second example. Build each entry from a face rule that reads only the face, as in line L2.
- **Different tie rules.** Testing $f < c$ in line L7 and $f \le c$ in another place, or in another cell, makes neighbors disagree on a sample equal to $c$. Use one test everywhere. A sample equal to $c$ also puts several vertices at one point and makes triangles of zero area.
- **Vertices not shared.** Computing CROSS in each cell and not merging the results gives a soup of triangles that look closed but have no shared vertices; with floating point, the two copies can also differ in the last bit. Key the vertex by the grid edge, as in lines L9 to L11, not by its coordinates.
- **A fan on a face.** A fan triangulation from the first vertex of a cycle can add a chord between two vertices on one ambiguous face. The neighbor cell can then add the same chord, and the edge has four triangles. Line L4 must reject chords on a face.
- **Wrong orientation.** Taking the face segments of line L2 without the reversal of line L4 points all normals to the inside. Check the signed volume of a closed mesh: it is positive when the normals point out.
- **Index order.** With $f[z][y][x]$ storage, reading corner $k$ as $f[x][y][z]$ swaps axes and gives wrong cases on any field that is not symmetric.

## Implementations

## History

Lorensen and Cline published marching cubes at SIGGRAPH 1987, for surfaces of medical volume data at General Electric; Wyvill, McPheeters and Wyvill described a similar cell method for soft objects in 1986. Dürst noted in a 1988 letter that the table has ambiguous faces and that it can leave holes. Nielson and Hamann gave the asymptotic decider in 1991. Doi and Koide gave a tetrahedral version in 1991. Chernyaev's 33 cases (1995) addressed interior ambiguity.

## References
