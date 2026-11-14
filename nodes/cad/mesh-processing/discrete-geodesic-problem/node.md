---
tag: ZR3ZZJ
kind: problem
slug: discrete-geodesic-problem
name: Discrete geodesic problem
aliases:
- geodesics on polyhedral surfaces
area: cad/mesh-processing
level: core
summary: Find shortest paths or the geodesic distance field on the surface of a polyhedron, where paths may cross faces and unfold over edges.
prereqs: [polygon-mesh, shortest-path]
see_also: [mmp-geodesic-algorithm, heat-method, fast-marching-method, euclidean-shortest-path, visibility-graph, eikonal-equation, steiner-points, single-source-shortest-paths]
sources:
  - paper: doi:10.1137/0216045
    title: Joseph S. B. Mitchell, David M. Mount and Christos H. Papadimitriou, The discrete geodesic problem, SIAM Journal on Computing 16(4), 1987, 647 to 668
    locator: the statement of the problem for a source on a polyhedral surface, the structure of shortest paths, and the exact O(n^2 log n) algorithm
  - paper: doi:10.1137/0215014
    title: Micha Sharir and Amir Schorr, On shortest paths in polyhedral spaces, SIAM Journal on Computing 15(1), 1986, 193 to 215
    locator: shortest paths on the surface of a convex polytope
  - paper: doi:10.1007/s00454-007-9031-0
    title: Yevgeny Schreiber and Micha Sharir, An optimal-time algorithm for shortest paths on a convex polytope in three dimensions, Discrete and Computational Geometry 39, 2008
    locator: the O(n log n) time bound for convex polytopes (general locator, the pages were not checked)
  - paper: doi:10.1145/1073204.1073228
    title: Vitaly Surazhsky, Tatiana Surazhsky, Danil Kirsanov, Steven J. Gortler and Hugues Hoppe, Fast exact and approximate geodesics on meshes, ACM Transactions on Graphics 24(3) (SIGGRAPH 2005), 553 to 560
    locator: the practical exact method and its comparison with approximate methods on meshes
  - paper: doi:10.1073/pnas.95.15.8431
    title: Ron Kimmel and James A. Sethian, Computing geodesic paths on manifolds, Proceedings of the National Academy of Sciences 95(15), 1998, 8431 to 8435
    locator: fast marching on triangulated surfaces, with the correction for obtuse triangles
  - paper: doi:10.1145/2516971.2516977
    title: Keenan Crane, Clarisse Weischedel and Max Wardetzky, Geodesics in heat, a new approach to computing distance based on heat flow, ACM Transactions on Graphics 32(5), 2013, article 152
    locator: the heat method and its comparison with exact and fast marching distances
---

The discrete geodesic problem asks for shortest paths on the surface of a polyhedron, usually a triangle mesh. A path may go anywhere on the surface: straight across a face, over an edge into the next face, and around a vertex. Its length is its Euclidean length. The *geodesic distance* from a source to a point is the length of a shortest such path, and the *distance field* gives it for every point or every vertex. The problem is not a graph problem. A shortest path along the edges of the mesh is in general longer than the geodesic, and it does not get closer when the mesh is refined. Mitchell, Mount and Papadimitriou named the problem and gave the first exact polynomial method for general surfaces in 1987.

## In plain words

An ant on a box wants the shortest walk to the far corner. It can walk across the sides, not only along the edges. Cut the box open and lay two sides flat, and the best walk is a straight line on the flat sheet. The question is which sides to lay flat, and in what order, because each choice gives a different line.

The problem is to find these shortest walks, or just their lengths, from one start point to every point of a surface made of flat triangles. On a smooth curved surface the answer is a curve. On a surface of triangles it is a chain of straight pieces that bend only at edges, in a way that is straight when unfolded, or at special corners.

## Definition

**Input.** A connected manifold triangle mesh $M$ with vertices in $\mathbb{R}^3$, possibly with border, and a source point $s$ on it, usually a vertex. Variants use a set of sources.

**Paths.** A path is a continuous curve on the union of the closed faces. Its length is its Euclidean length in $\mathbb{R}^3$.

**Output.** The geodesic distance $d(x) = \inf \{\operatorname{length}(\gamma) : \gamma \text{ a path from } s \text{ to } x\}$, either at every vertex, or as a description of $d$ on the whole surface, or a shortest path to a given target.

**Structure of solutions.** A shortest path exists. Inside a face it is a straight segment. Where it crosses the inside of an edge, the two faces can be unfolded into one plane, and in that plane the path is straight. It can pass through a vertex only if the vertex is on the border or its face angles sum to at least $2\pi$. At such a vertex the path may bend, but the angles on both sides must be at least $\pi$. At a vertex with angle sum below $2\pi$, such as a corner of a cube, a shortest path never passes. So a shortest path is a straight line in the unfolding of the faces that it crosses, broken only at border vertices and at vertices of negative [discrete Gaussian curvature](/discrete-gaussian-curvature/). A path with these local properties is a *geodesic*, but it need not be shortest.

## Variants

- **Single source, all vertices.** The common form, which gives a distance field on the mesh.
- **Point to point.** One source and one target, with the path as output.
- **Several sources.** The distance to the nearest source, which gives the geodesic Voronoi diagram of the sources on the surface.
- **All pairs.** The distance between every two vertices, an $n \times n$ table.
- **Approximate.** A distance within a factor $1 + \varepsilon$, or a field that converges to the true distance as the mesh is refined.
- **Convex surfaces.** The surface of a convex polytope, where no vertex can be passed through, and faster exact methods exist.
- **Flat domains.** A flat mesh with holes is a polygonal domain in the plane, and the problem is the [Euclidean shortest path](/euclidean-shortest-path/) among obstacles.
- **Paths in space.** Shortest paths in $\mathbb{R}^3$ among polyhedral obstacles, not on a surface, form a different and harder problem, which Canny and Reif showed to be NP-hard.
- **Weighted regions.** Each face has a cost per unit length, and paths refract at edges as light does.

## Examples

**Edges are not enough.** On a flat grid of unit squares, each cut by a diagonal in the same direction, the distance from $(0, 0)$ to $(2, 1)$ is $\sqrt{5} \approx 2.236$, the straight line. The shortest path along edges is one diagonal and one side, $1 + \sqrt{2} \approx 2.414$. If the grid is refined by a factor of $k$, the same point is reached by $k$ diagonals and $k$ sides, so the error of $8$ percent stays.

**The cube.** On the unit cube, from one corner to the opposite corner, unfolding two sides into a $1 \times 2$ rectangle gives $\sqrt{5}$. There are six such shortest paths, one for each pair of sides that meet along an edge at neither corner. Along edges the best is $1 + \sqrt{2}$ with a face diagonal, or $3$ with the cube edges only.

**A box.** On the box $1 \times 2 \times 3$, the three unfoldings between opposite corners give $\sqrt{(1 + 2)^2 + 3^2} = \sqrt{18}$, $\sqrt{(1 + 3)^2 + 2^2} = \sqrt{20}$ and $\sqrt{(2 + 3)^2 + 1^2} = \sqrt{26}$. The distance is the smallest, $\sqrt{18} \approx 4.243$. The choice of unfolding is a combinatorial part of the problem.

**Bending at a corner.** On the flat L-shaped region $[0, 2]^2$ without the square $(1, 2] \times (1, 2]$, the shortest path from $(2, 0)$ to $(\frac{1}{2}, 2)$ cannot be straight. It goes to the inner corner $(1, 1)$, a border vertex with angle $\frac{3\pi}{2}$, and bends there, with length $\sqrt{2} + \frac{\sqrt{5}}{2} \approx 2.532$.

## Known algorithms

| method | answer | time |
|---|---|---|
| [Mitchell, Mount and Papadimitriou](/mmp-geodesic-algorithm/), 1987, and its window form by Surazhsky and coauthors, 2005 | exact, the whole distance field | $O(n^2 \log n)$ worst case, measured much less in practice |
| Chen and Han, 1990, a tree of unfoldings | exact | $O(n^2)$ time, $O(n)$ space |
| Sharir and Schorr, 1986, then Schreiber and Sharir, 2008, for convex polytopes | exact | $O(n \log n)$ for the second |
| graph search over [Steiner points](/steiner-points/) on the edges, with [Dijkstra's algorithm](/dijkstra/) | an upper bound, within a factor that shrinks as more points are added | the cost of Dijkstra on the larger graph |
| [fast marching](/fast-marching-method/) on the triangles, Kimmel and Sethian, 1998 | an approximation that converges as the mesh is refined | $O(n \log n)$ |
| [heat method](/heat-method/), Crane, Weischedel and Wardetzky, 2013 | an approximation from two sparse linear solves | the cost of two solves, with a factorization reused for new sources |

The exact methods give the reference values against which the approximate ones are measured. The approximate ones are faster in practice and easier to use on large meshes, and they also work on other kinds of domain, such as grids and point clouds.

## Bounds

- **Exact, general surfaces.** $O(n^2 \log n)$ time and $O(n^2)$ space by Mitchell, Mount and Papadimitriou, and $O(n^2)$ time and $O(n)$ space by Chen and Han. A faster exact method for general nonconvex surfaces is not confirmed here.
- **Exact, convex surfaces.** $O(n \log n)$ time by Schreiber and Sharir, which they show to be optimal.
- **Output size.** A single shortest path can cross $\Theta(n)$ faces, so writing out the paths to all vertices can take $\Theta(n^2)$ space even when the $n$ distances alone take $\Theta(n)$.
- **Graphs with a fixed spacing are not exact.** A Steiner graph gives the geodesic distance to a vertex only if it contains the points where a shortest path crosses the edges. These points depend on the source and the target, so a graph with evenly spaced points gives in general only an upper bound.

## Reductions

- **From planar shortest paths.** Triangulate a polygonal domain with holes. The result is a flat mesh with border, and its geodesic distance is the Euclidean shortest path distance among the holes. So the planar problem is a special case.
- **To graph shortest paths, approximately.** Put Steiner points on the edges and join the points of each face by straight segments. Every graph path is a real path on the surface, so graph distances are upper bounds, and with enough points they come within any factor $1 + \varepsilon$.
- **To a partial differential equation.** The distance field solves the [eikonal equation](/eikonal-equation/) $|\nabla d| = 1$ with $d = 0$ at the source, which is the base of fast marching, and by Varadhan's formula it is the short-time limit of the [heat equation](/heat-equation/), which is the base of the heat method.

## Applications

- **Geometry processing.** Geodesic distances drive remeshing, mesh segmentation, geodesic Voronoi diagrams, and the placement of samples on a surface.
- **Parameterization and texturing.** Geodesic polar coordinates around a point place decals and local texture patches.
- **Shape analysis.** Distance distributions on a surface are invariant to bending, so they serve as shape descriptors and for matching.
- **Path planning.** Shortest routes over a terrain model for robots and vehicles.
- **Manufacturing.** Tool paths at equal geodesic distance on a curved part.

## References
