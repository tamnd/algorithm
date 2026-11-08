---
tag: XQFAEY
kind: problem
slug: convex-hull-3d
name: 3D convex hull problem
aliases:
- convex hull in three dimensions
- convex hull in d dimensions
- higher-dimensional convex hull
- facet enumeration
area: geometry/convex-hulls
level: core
summary: Given n points in R^3 (or R^d), compute the facets of their convex hull.
prereqs: [convex-hull-problem, convex-polytope, orientation-test]
see_also: [beneath-beyond, chan-algorithm, convex-hull-lower-bound, euler-formula, paraboloid-lifting-map, higher-dimensional-delaunay, vertex-enumeration, randomized-incremental-construction]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, 3rd edition, Springer, 2008
    locator: Chapter 11, Convex Hulls (the size of a 3D hull, the randomized incremental algorithm with a conflict graph, and the relation to half-space intersection and Voronoi diagrams)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 3, Convex hulls, the sections on hulls in more than two dimensions (gift wrapping, beneath-beyond and the 3D divide-and-conquer algorithm)
  - paper: doi:10.1145/321556.321564
    title: Donald R. Chand and Sham S. Kapur, An algorithm for convex polytopes, Journal of the ACM 17(1), 1970
    locator: the gift-wrapping method in d dimensions, which walks from facet to facet across ridges
  - paper: doi:10.1145/359423.359430
    title: Franco P. Preparata and Se June Hong, Convex hulls of finite sets of points in two and three dimensions, Communications of the ACM 20(2), 1977
    locator: the O(n log n) divide-and-conquer algorithm in three dimensions
  - paper: doi:10.1007/BF02187740
    title: Kenneth L. Clarkson and Peter W. Shor, Applications of random sampling in computational geometry, II, Discrete and Computational Geometry 4(5), 1989
    locator: the randomized incremental hull in expected O(n log n) time in 3D and O(n^(d/2)), with d/2 rounded down, for d at least 4
  - paper: doi:10.1007/BF02573985
    title: Bernard Chazelle, An optimal convex hull algorithm in any fixed dimension, Discrete and Computational Geometry 10(4), 1993
    locator: the deterministic O(n log n + n^(d/2)) algorithm, with d/2 rounded down
  - paper: doi:10.1007/BF02712873
    title: Timothy M. Chan, Optimal output-sensitive convex hull algorithms in two and three dimensions, Discrete and Computational Geometry 16(4), 1996
    locator: the 3D algorithm in O(n log h) time
---

The 3D convex hull problem asks for the boundary of the [convex hull](/convex-hull/) of $n$ points in space: the list of its facets, with the vertices of each facet in order and the adjacency between facets. The $d$-dimensional problem asks the same for points in $\mathbb{R}^d$. In three dimensions the output has linear size, at most $2n - 4$ facets, and the best algorithms take $O(n \log n)$ time, as in the plane. In higher dimensions the output itself can have $\Theta(n^{\lfloor d/2 \rfloor})$ facets by the Upper Bound Theorem, and that size, not the sorting cost, sets the running time. The problem matters beyond geometry because the [Delaunay triangulation](/delaunay-triangulation/) of points in $\mathbb{R}^{d-1}$ is the lower hull of the lifted points in $\mathbb{R}^d$.

## In plain words

Imagine a cloud of points floating in a room, and shrink-wrap plastic pulled tight around all of them. The plastic forms a solid with flat faces, like a gem. The problem is to describe that gem: which points are its corners, and which corners form each flat face.

In the plane the answer is a single loop of corners. In space it is a whole surface, made of triangles in the simplest case, and each triangle must know its neighbours. The surface has at most about twice as many faces as there are points, so a fast method can still afford to list it all. In four or more dimensions the wrapping can have many more faces than there are points, and just writing them down takes most of the time.

## Definition

**Input.** A finite set $S$ of $n$ points in $\mathbb{R}^3$ (or $\mathbb{R}^d$ for a fixed $d$), usually with integer or rational coordinates.

**Output.** The facets of the [polytope](/convex-polytope/) $P = \mathrm{conv}(S)$. In 3D each facet is a convex polygon given by its vertices in counterclockwise order seen from outside, and the output also records, for each edge, the two facets that share it. A [doubly connected edge list](/doubly-connected-edge-list/) is the usual structure. Many implementations output a triangulated surface instead: a list of triangles with vertices in $S$, each oriented outward, whose union is the boundary of $P$. If the points are in general position (no four on a plane), the two outputs are the same.

In $\mathbb{R}^d$ the output is the list of facets, each given by its vertex set and its outward normal, together with the facet adjacency across ridges. Some applications also want the full face lattice.

**Degenerate inputs.** If $S$ lies in a plane, $P$ has no interior and the problem reduces to the [planar problem](/convex-hull-problem/) in that plane. An algorithm must detect this case, for example by searching for four affinely independent points with the [affine hull](/affine-hull/) test, before it builds a starting tetrahedron.

**Model.** The [real RAM](/real-ram/) with exact arithmetic. With integer coordinates every decision is the sign of the 3D orientation determinant $\mathrm{orient}(a, b, c, d) = ((b - a) \times (c - a)) \cdot (d - a)$, which is exact with integers of about three times the input size. In $\mathbb{R}^d$ the test is a $(d + 1) \times (d + 1)$ [determinant](/determinant/).

**The size of the output.** For a 3-polytope with $v \le n$ vertices, $e$ edges and $f$ facets, [Euler's formula](/euler-formula/) $v - e + f = 2$ and the count $2e \ge 3f$ (each facet has at least three edges, each edge is on two facets) give

$$f \le 2v - 4 \le 2n - 4 \qquad\text{and}\qquad e \le 3v - 6 \le 3n - 6,$$

with equality when every facet is a triangle. In $\mathbb{R}^d$ the Upper Bound Theorem gives the exact maximum number of facets of a $d$-polytope with $n$ vertices; it is reached by the cyclic polytope and has order $\Theta(n^{\lfloor d/2 \rfloor})$. For $d = 4$ the maximum is $n(n - 3)/2$, and for $d = 5$ it is $(n - 3)(n - 4)$. The exact formula is on the [convex polytope](/convex-polytope/) page.

## Variants

- **Triangulated or merged facets.** Output each facet as one polygon, or as a set of triangles. Merging coplanar triangles needs an exact coplanarity test.
- **Vertices only.** Report the extreme points. In 3D this is no easier than the full hull in the comparison-based models, since the lower bounds hold for it.
- **Lower hull.** Only the facets whose outward normal points downward. This is the version used for Delaunay triangulations through the [paraboloid lifting map](/paraboloid-lifting-map/).
- **Half-space intersection.** Given $n$ half-spaces that contain a known interior point, compute their intersection. By polar duality this is the hull problem on the dual points, and in 3D it costs the same.
- **Vertex enumeration.** Given an H-description $\{x : Ax \le b\}$, list the vertices. This is the dual problem, studied for polytopes in high dimension, where output-sensitive bounds matter. See [vertex enumeration](/vertex-enumeration/).
- **Dynamic 3D hulls.** Insertions and deletions in 3D are much harder than in the plane; the known bounds are polylogarithmic amortized per update and come from more complex structures.

## Examples

**Seven points.** Let $a = (0,0,0)$, $b = (6,0,0)$, $c = (0,6,0)$, $d = (0,0,6)$, $e = (1,2,1)$, $f = (4,3,2)$ and $g = (6,5,-1)$. No four of them are on a plane. The point $e$ is inside the tetrahedron $abcd$, and $f$ and $g$ are outside. The hull has the 8 triangular facets

$$abd,\ adc,\ cdf,\ dbf,\ acg,\ bag,\ cfg,\ fbg,$$

with 6 vertices, 12 edges and $6 - 12 + 8 = 2$. Since all facets are triangles, $f = 2 \cdot 6 - 4 = 8$ and $e = 3 \cdot 6 - 6 = 12$, the maximum for 6 vertices. A brute-force check confirms each facet: for a triple $(u, v, w)$, compute $\mathrm{orient}(u, v, w, x)$ for every other point $x$, and the triple is a facet exactly when all values are negative. The [beneath-beyond](/beneath-beyond/) page traces how the incremental algorithm finds this list.

**A cube.** The 8 corners of $[0, 2]^3$ have 6 square facets, 12 edges, and $8 - 12 + 6 = 2$. A triangulated output has 12 triangles, two per square, and the choice of diagonals is arbitrary. Adding the 6 face centers, such as $(1, 1, 2)$, does not change the hull, but a correct algorithm must not report them as vertices.

**Many facets in four dimensions.** The 8 points $(t, t^2, t^3, t^4)$ for $t = 1, \ldots, 8$ span a 4-polytope with 20 facets, and every pair of the 8 points is an edge. A brute-force check over all $\binom{8}{4} = 70$ quadruples with exact integer determinants confirms the count $8 \cdot 5 / 2 = 20$.

## Known algorithms

Bounds are on the real RAM, in 3D unless stated. $f$ is the number of facets of the output, and $h$ the number of hull vertices.

| algorithm | time | notes |
| --- | --- | --- |
| brute force | $O(n^4)$ | test each triple against all points |
| gift wrapping (Chand and Kapur, 1970) | $O(nf)$ | from a facet, find the neighbour across each edge by a scan over all points; works in any dimension |
| divide and conquer (Preparata and Hong, 1977) | $O(n \log n)$ | split by $x$, merge two hulls by wrapping a band of triangles around them |
| randomized incremental with a conflict graph (Clarkson and Shor, 1989) | $O(n \log n)$ expected | random insertion order; see [beneath-beyond](/beneath-beyond/) and [randomized incremental construction](/randomized-incremental-construction/) |
| beneath-beyond in $\mathbb{R}^d$ (Kallay; Seidel, 1981) | $O(n \log n + n^{\lceil d/2 \rceil})$ | deterministic incremental; optimal for even $d$ |
| randomized incremental in $\mathbb{R}^d$ | $O(n \log n + n^{\lfloor d/2 \rfloor})$ expected | the same Clarkson-Shor analysis |
| Chazelle (1993) | $O(n \log n + n^{\lfloor d/2 \rfloor})$ | deterministic and worst-case optimal in every fixed dimension |
| Chan (1996) | $O(n \log h)$ | output-sensitive in 3D, by grouping and wrapping, as in the [planar version](/chan-algorithm/) |

The expected bounds hold for every input; the expectation is over the random insertion order only.

## Bounds

- **Lower bound in 3D.** The planar problem reduces to the 3D one: put the planar points at height 0 and add one apex point above them. The side facets through the apex are triangles over the edges of the planar hull, in order. So the $\Omega(n \log n)$ bound of the [convex hull lower bound](/convex-hull-lower-bound/) and the $\Omega(n \log h)$ bound of the [output-sensitive lower bound](/convex-hull-output-sensitive-lower-bound/) hold in 3D, in the same algebraic decision or computation tree models.
- **Upper bound in 3D.** $O(n \log n)$ in the worst case (Preparata and Hong) and expected (randomized incremental), and $O(n \log h)$ (Chan), all matching the lower bounds.
- **Higher dimensions.** For fixed $d \ge 4$, any algorithm that lists the facets needs $\Omega(n^{\lfloor d/2 \rfloor})$ time on the cyclic polytope just to write the output, and $\Omega(n \log n)$ by the planar reduction. Chazelle's algorithm reaches $O(n \log n + n^{\lfloor d/2 \rfloor})$, so the worst-case complexity is settled. Output-sensitive bounds in high dimension, in terms of $n$ and $f$, are still open in general.
- **Dependence on $d$.** The constants hidden in these bounds grow quickly with $d$, and the bounds treat $d$ as fixed. For $d$ part of the input, the number of facets can be exponential in $d$.

## Reductions

- **Delaunay triangulation and Voronoi diagram.** Lift each planar point $(x, y)$ to $(x, y, x^2 + y^2)$. The downward facets of the 3D hull project to the triangles of the [Delaunay triangulation](/delaunay-triangulation/), so a 3D hull algorithm gives the Delaunay triangulation and, by duality, the [Voronoi diagram](/voronoi-diagram/) in $O(n \log n)$ time. In general the Delaunay triangulation in $\mathbb{R}^{d-1}$ is a lower hull in $\mathbb{R}^d$; see [higher-dimensional Delaunay](/higher-dimensional-delaunay/).
- **Half-space intersection.** By polarity about an interior point, intersecting half-spaces is the hull problem on dual points, and conversely.
- **The planar problem.** A special case, as in the lower bound above.
- **Linear programming.** The vertices of a feasible region $\{x : Ax \le b\}$ are the dual of a hull, so [vertex enumeration](/vertex-enumeration/) and hull computation solve each other, while [linear programming](/linear-programming-problem/) needs only one optimal vertex and is much cheaper.

## Applications

- **Mesh generation and surface reconstruction.** Delaunay triangulations and tetrahedralizations through the lifting map.
- **Collision detection and physics engines.** Objects are often replaced by the convex hulls of their vertices, and tests between convex polyhedra such as [convex polyhedra intersection](/convex-polyhedra-intersection/) work on hulls.
- **Robotics and motion planning.** Configuration-space obstacles of convex objects are Minkowski sums, which are hulls of sums of vertices.
- **Computational biology and chemistry.** Hulls and their alpha-shape refinements describe the shape of molecules.
- **Polyhedral combinatorics and optimization.** Computing the facets of the hull of a set of 0-1 points (the integer points of a combinatorial problem) gives the inequalities of an exact LP formulation; tools for this are hull codes in high dimension.

## References
