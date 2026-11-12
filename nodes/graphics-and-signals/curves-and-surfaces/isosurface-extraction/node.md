---
tag: VFC7VT
kind: problem
slug: isosurface-extraction
name: Isosurface extraction
aliases:
- isocontour extraction
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Given samples of a scalar field on a grid and a value c, build a mesh of the surface f = c (or the curves f = c in 2D) that is closed, has no cracks and is close to the level set.
prereqs: [implicit-surface, polygon-mesh]
see_also: [marching-squares, marching-cubes, marching-tetrahedra, dual-contouring, signed-distance-function, interval-tree, surface-reconstruction, octree]
sources:
  - paper: doi:10.1145/37401.37422
    title: William E. Lorensen and Harvey E. Cline, Marching cubes, a high resolution 3D surface construction algorithm, Computer Graphics (SIGGRAPH 87 Proceedings) 21(4), 163 to 169, 1987
    locator: the whole paper (the problem of surfaces from CT and MR volumes, and the cell by cell solution)
  - paper: doi:10.1109/VISUAL.1991.175782
    title: Gregory M. Nielson and Bernd Hamann, The asymptotic decider, resolving the ambiguity in marching cubes, Proceedings of Visualization 91, IEEE, 83 to 91, 1991
    locator: the whole paper (the ambiguous faces and the bilinear saddle value)
  - paper: doi:10.1016/j.cag.2006.07.021
    title: Timothy S. Newman and Hong Yi, A survey of the marching cubes algorithm, Computers and Graphics 30(5), 854 to 879, 2006
    locator: the whole survey (topology, ambiguity, tetrahedral, dual and adaptive methods, and speedups by value range indexes)
  - book: isbn:9781558602335
    title: Jules Bloomenthal (editor), Introduction to Implicit Surfaces, Morgan Kaufmann, 1997
    locator: Chapter 4, Surface Tiling (polygonization of implicit surfaces by spatial partitioning)
---

Isosurface extraction is the problem of turning a sampled scalar field into a mesh of one of its level sets. The input is a grid of numbers, for example the densities of a CT scan or the values of an [implicit surface](/implicit-surface/) function, and a value $c$. The output is a [polygon mesh](/polygon-mesh/) of the surface $f = c$ in 3D, or a set of polylines, the isolines, in 2D. The samples do not fix the surface between the nodes, so the problem has no single right answer: each method chooses an interpolant, or a rule, and the quality measures are that the mesh is closed and without cracks, has the right topology for the chosen interpolant, and is close to the level set. The standard methods are [marching squares](/marching-squares/), [marching cubes](/marching-cubes/), [marching tetrahedra](/marching-tetrahedra/) and [dual contouring](/dual-contouring/).

## In plain words

Think of a block of numbers, one number at each point of a grid, such as the density of tissue in a medical scan. Pick one number, say the density of bone. Some grid points are above it and some are below. Somewhere between them is the surface of the bone.

The task is to draw that surface with triangles. Each small cube of the grid has eight corners. If some are above and some below, the surface cuts the cube, and you place a few triangles in it. Where the surface crosses an edge of the cube, a guess from the two end values says how far along the edge it is.

The hard part is to make the pieces from all the cubes fit together without gaps, and to decide what to do when the corner values allow two different shapes.

## Definition

**Input.** A grid of $N$ cells with nodes $x_{ijk} = o + h (i, j, k)$ and values $f_{ijk}$, or an unstructured grid of tetrahedra; a value $c$; and, for some methods, the gradients at the nodes or at the edge crossings (Hermite data). A node is inside when $f_{ijk} < c$ and outside otherwise; with the opposite sign, inside and outside exchange. A cell is active when it has nodes on both sides.

**Output.** A mesh $M$ with these properties, in order of importance:

1. **No cracks.** Each edge of $M$ that is not on the border of the grid is in exactly two faces. Two cells that share a face must agree on how the surface crosses it.
2. **Manifold and oriented.** $M$ is a 2-manifold with a consistent orientation, with the outside of each face toward $f > c$. Where the level set leaves the grid, $M$ has a border on the grid boundary; otherwise $M$ is closed.
3. **Topology.** The connected parts, holes and handles of $M$ are those of the level set of a stated interpolant of the samples, such as the trilinear interpolant in each cell or the linear interpolant on a [tetrahedralization](/tetrahedralization/).
4. **Geometry.** The vertices of $M$ are on or near the level set, for example on the edge crossings found by linear interpolation, and the faces are not too thin.

**What is not defined.** The samples fix the field only at the nodes. Any surface that separates the inside nodes from the outside nodes fits the data, and features smaller than the spacing $h$ can be missed entirely. A method is correct relative to its interpolant, not relative to the unknown true surface.

## Variants

- **2D contours.** The level curves $f(x, y) = c$ of an image or a height map, as polylines; this is the problem of [marching squares](/marching-squares/). The contour lines of a map are the main example.
- **Topologically correct extraction.** The output must have the topology of the trilinear interpolant, including inside each cell. Ambiguous faces are decided by the bilinear saddle value (the asymptotic decider), and ambiguous cell interiors need more subcases.
- **Sharp features.** With Hermite data, the mesh should keep the edges and corners of the solid, as CAD models need. [Dual contouring](/dual-contouring/) places one vertex per cell by a quadratic error function for this.
- **Adaptive grids.** The field is on an [octree](/octree/), refined near the surface or where the surface is curved. Cells of different sizes must still agree on their shared faces.
- **Unstructured grids.** The input is a tetrahedral or mixed mesh from a simulation, and [marching tetrahedra](/marching-tetrahedra/) applies directly.
- **Many queries.** The same field is contoured for many values $c$, so an index over the value ranges of the cells is built once.
- **Functions, not samples.** The field is a function that can be evaluated anywhere, such as a [signed distance function](/signed-distance-function/). The method may choose where to sample, by a uniform grid, an adaptive one, or by continuation from a seed cell along the surface.

## Examples

**One square cell.** Take corner values $f_{00} = 2$, $f_{10} = -1$, $f_{01} = -1$, $f_{11} = 1$ and $c = 0$. The crossing on the edge from $(0,0)$ to $(1,0)$ is at $t = (c - f_{00}) / (f_{10} - f_{00}) = 2/3$, and the same holds for the edge from $(0,0)$ to $(0,1)$; the crossings on the two edges at $(1,1)$ are at $1/2$ from it. The two positive corners are on one diagonal and the two negative ones on the other, so there are two ways to join the four crossings by two segments. The bilinear interpolant has its saddle point value at
$$\frac{f_{00} f_{11} - f_{10} f_{01}}{f_{00} + f_{11} - f_{10} - f_{01}} = \frac{2 - 1}{2 + 1 + 1 + 1} = \frac15 > c,$$
so the positive region is connected through the center, and the two segments separate the negative corners from it. This is the rule of the asymptotic decider.

**Counts of cases.** A square cell has $2^4 = 16$ sign cases, of which 2 are ambiguous like the one above. A cube has $2^8 = 256$ cases; under the 24 rotations they fall into 23 classes, and with the exchange of inside and outside into the 15 patterns of Lorensen and Cline. A tetrahedron has $2^4 = 16$ cases, with 0, 1 or 2 triangles, and none is ambiguous, because the linear interpolant on a tetrahedron has no saddle.

**A sphere.** Sample $f(x) = \lVert x \rVert^2 - 1$ at spacing $h$ on a grid around the unit ball, and take $c = 0$. If no node value is exactly 0, marching cubes with a consistent table and marching tetrahedra both give a closed oriented mesh. On a fine grid it has $V - E + F = 2$, the value of a sphere, and every vertex lies on a grid edge that the sphere crosses, so it is at most $h$ from the true sphere. The pages of the methods test this case.

## Known algorithms

- **[Marching squares](/marching-squares/).** The 2D version: a table of the 16 cases per cell, and a choice for the 2 ambiguous ones.
- **[Marching cubes](/marching-cubes/).** Lorensen and Cline, 1987: a table of triangles for each of the 256 cases of a cube, with vertices on the edges by linear interpolation. The original table can leave holes at ambiguous faces; consistent face rules or the asymptotic decider fix this.
- **[Marching tetrahedra](/marching-tetrahedra/).** Doi and Koide, 1991: split each cube into tetrahedra and contour each one. It has no ambiguous cases and gives a closed manifold, at the cost of more triangles and a bias from the choice of diagonals.
- **[Dual contouring](/dual-contouring/).** Ju, Losasso, Schaefer and Warren, 2002: one vertex per active cell at the minimum of a quadratic error function of the Hermite data, and one quadrilateral per crossed edge. It keeps sharp features and works on octrees, but the output can be non-manifold.
- **Polygonization by continuation.** Start from one active cell and visit only the active cells next to it, as in the implicit surface polygonizers of Bloomenthal. It does work proportional to the surface, not to the volume, but it finds only the parts that are connected to a seed.
- **Indexes over cell ranges.** Store the interval $[\min f, \max f]$ of each cell in an [interval tree](/interval-tree/); the active cells for a value $c$ are the intervals that contain $c$, found in $O(\log N + k)$ time for $k$ active cells.

## Bounds

**Output size.** A cell-by-cell method makes $O(1)$ faces per active cell, so $O(k)$ faces for $k$ active cells. For a smooth closed surface of area $A$ sampled at spacing $h$, $k = \Theta(A / h^2)$, against $N = \Theta(1/h^3)$ cells in a unit box.

**Time.** A scan of all cells takes $\Theta(N)$ time. Without preprocessing this is optimal in the worst case, because a method that skips a node cannot tell whether that one value changes the surface. With an index built in $O(N \log N)$ time, each query takes $O(\log N + k)$.

**Guarantees.** If no node value equals $c$, marching tetrahedra gives a closed 2-manifold that is exactly the level set of the piecewise linear interpolant, and marching cubes with a consistent rule on each face gives a mesh without cracks. Beyond the interpolant there is no guarantee: two different fields with the same samples have different level sets, and a feature thinner than $h$ can vanish. The geometric error of a vertex placed by linear interpolation on an edge is $O(h^2)$ for a smooth field whose derivative along the edge is bounded away from zero.

## Reductions

- **To root finding on edges.** The vertex on an edge is the root of the interpolant of $f - c$ along the edge, found in closed form for linear interpolation, or by the [bisection method](/bisection-method/) when $f$ can be evaluated.
- **To piecewise linear interpolation.** Marching tetrahedra reduces the problem to the exact level set of the [piecewise linear interpolant](/piecewise-linear-interpolation/) on a tetrahedralization of the grid.
- **From surface reconstruction.** Many methods of [surface reconstruction](/surface-reconstruction/) fit an implicit function to points, such as a signed distance or an indicator function, and then extract its level set. [Poisson surface reconstruction](/poisson-surface-reconstruction/) is one.
- **From the level set method.** A surface moved by the [level set method](/level-set-method/) is stored as a grid of values, and is extracted for display at each time step.

## Applications

- **Medical imaging.** Surfaces of bone, organs and vessels from CT and MRI volumes, the original use of marching cubes.
- **Scientific visualization.** Surfaces of equal pressure, temperature or density in simulations, often for many values $c$.
- **Modeling with implicit surfaces.** Blobby objects, sums of distance fields and Boolean combinations are converted to meshes for display and for printing.
- **Maps and images.** Contour lines of terrain heights, and the boundaries of thresholded image regions.
- **Fluids and reconstruction.** The free surface of a fluid stored as a level set, and the output step of implicit reconstruction from scans.

## References
