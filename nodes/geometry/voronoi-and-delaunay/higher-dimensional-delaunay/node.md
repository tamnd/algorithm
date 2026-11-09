---
tag: G18482
kind: concept
slug: higher-dimensional-delaunay
name: Higher-dimensional Delaunay triangulation
aliases:
- Delaunay tetrahedralization
- Delaunay triangulation in d dimensions
- Delaunay tessellation
area: geometry/voronoi-and-delaunay
level: advanced
summary: Generalization of Delaunay triangulation to d dimensions via the lifting map and convex hulls in d+1 dimensions.
prereqs: [paraboloid-lifting-map, convex-polytope, delaunay-triangulation]
see_also: [convex-hull-3d, bowyer-watson-algorithm, regular-triangulation, power-diagram, dwyer-algorithm, general-position-delaunay, voronoi-complexity-theorem, mesh-generation]
sources:
  - paper: "H. Edelsbrunner and R. Seidel, Voronoi diagrams and arrangements, Discrete and Computational Geometry 1, 1986, 25-44"
    locator: Voronoi diagrams and Delaunay subdivisions in d dimensions through the paraboloid in d+1 dimensions
  - paper: "K. L. Clarkson and P. W. Shor, Applications of random sampling in computational geometry, II, Discrete and Computational Geometry 4, 1989, 387-421"
    locator: the randomized incremental convex hull in any fixed dimension and its expected time bound
  - paper: "B. Joe, Construction of three-dimensional Delaunay triangulations using local transformations, Computer Aided Geometric Design 8(2), 1991, 123-142"
    locator: insertion of a point followed by 2-3 and 3-2 flips always reaches the Delaunay tetrahedralization
  - book: isbn:9781584887300
    title: S.-W. Cheng, T. K. Dey and J. R. Shewchuk, Delaunay Mesh Generation, CRC Press, 2013
    locator: Chapter 4 (three-dimensional Delaunay triangulations, the lifting map, flips, slivers and the size bounds)
---

The Delaunay triangulation of a finite point set in $\mathbb{R}^d$ cuts its convex hull into $d$-simplices, triangles for $d = 2$ and tetrahedra for $d = 3$, whose circumscribed spheres hold no point of the set inside. The [paraboloid lifting map](/paraboloid-lifting-map/) works in every dimension: lift each point $p$ to $(p, |p|^2)$ in $\mathbb{R}^{d+1}$, and the lower faces of the [convex hull](/convex-polytope/) of the lifted points project to the Delaunay simplices. So it always exists, it is unique when no $d + 2$ points lie on one sphere, and any convex hull algorithm in $d + 1$ dimensions computes it. Unlike the plane, its size can grow faster than linearly: up to $\Theta(n^{\lceil d/2 \rceil})$ simplices, already $\Theta(n^2)$ tetrahedra in space.

## In plain words

In the plane, the Delaunay method joins points into triangles so that the circle through the corners of each triangle has no other point inside. In space, it joins points into four-cornered solids, and the ball through the four corners of each solid has no other point inside. The same works in any number of dimensions.

The same trick as in the plane builds it. Add one more coordinate, the squared distance from the origin, and take the bottom of the convex shape around the raised points.

Two things change in space. First, the number of solids can be much larger than the number of points. Second, the best-shape promise of the plane is lost: very flat solids can still pass the empty-ball test.

## The idea

Notation: $P$ is a finite set of $n$ points in $\mathbb{R}^d$ whose affine hull is all of $\mathbb{R}^d$, $h$ is the number of points on the boundary of $\mathrm{conv}(P)$, and $|p|^2$ is the squared length of $p$. In the plane a point is $p = (x, y)$; there $\mathrm{orient}(a, b, c)$ is positive when $a, b, c$ turn counterclockwise, and $\mathrm{incircle}$ is the [in-circle test](/in-circle-test/). General position is not assumed.

**Definitions.** A $d$-simplex with vertices $a_0, \ldots, a_d \in P$, affinely independent, has a unique circumsphere. It is **Delaunay** when no point of $P$ is in the open ball of that sphere. A **triangulation** of $P$ is a set of $d$-simplices with vertices in $P$ that cover $\mathrm{conv}(P)$, meet face to face, and use every point of $P$ as a vertex. It is a **Delaunay triangulation** when all its simplices are Delaunay.

**The in-sphere test.** Let $g$ be the affine function on $\mathbb{R}^d$ with $g(a_i) = |a_i|^2$ for $i = 0, \ldots, d$. Writing $g(q) = 2 o \cdot q + c$, the identity $g(q) - |q|^2 = (c + |o|^2) - |q - o|^2$ shows that $o$ is the circumcenter, $c + |o|^2$ is the squared radius, and $q$ is strictly inside the sphere exactly when $|q|^2 < g(q)$, that is, when the lifted $q$ is strictly below the hyperplane through the lifted $a_i$. As a determinant, this is the sign of the $(d+1) \times (d+1)$ matrix with rows $(a_i - q, |a_i - q|^2)$, multiplied by the orientation of $a_0, \ldots, a_d$ and by a sign that depends only on $d$. For integer input it is computed exactly with integers of degree $d + 2$ in the coordinates.

**Theorem.** (1) A simplex with vertices in $P$ is Delaunay exactly when its lifted copy lies in a face of the lower boundary of $K = \mathrm{conv}\{(p, |p|^2) : p \in P\}$. (2) The Delaunay triangulations of $P$ are exactly the triangulations of $P$ in which every simplex lies in the projection of one lower face of $K$. (3) A Delaunay triangulation of $P$ exists. (4) If no $d + 2$ points of $P$ lie on one sphere, every lower face of $K$ is a simplex and the Delaunay triangulation is unique.

*Proof.* (1) and (2): the proof of the theorem on the [lifting map](/paraboloid-lifting-map/) page uses only the convexity of the lower boundary function $F$, the tangent functions $q \mapsto 2 p \cdot q - |p|^2$, and the identity of Lemma 1 there. All of them hold in $\mathbb{R}^d$, with triangles replaced by $d$-simplices and circles by spheres. (3): in the plane, any cutting of each lower face works, because two faces share at most an edge with two points. In $\mathbb{R}^3$ two faces can share a polygon, and their cuttings must agree on it, so take the symbolic perturbation of [general position](/general-position-delaunay/): lift $p_i$ to $|p_i|^2 + \varepsilon^i$. For small $\varepsilon > 0$, every lifted point stays a vertex of the lower hull (the tangent hyperplane argument), and every lower facet is a simplex: a facet with $d + 2$ or more vertices has $d + 1$ of them affinely independent in projection, and then the perturbed in-sphere value of these and one more vertex has a nonzero coefficient of the power of $\varepsilon$ that belongs to the extra vertex, so it is not zero. These simplices meet face to face, since they are the facets of one convex polytope, and each is Delaunay for $P$, because an exact positive in-sphere value keeps its sign for small $\varepsilon$. (4): a lower face lies in a non-vertical hyperplane, and by the identity above the points of $P$ whose lifted points lie on it are on one sphere. A face with $d + 2$ or more vertices would put $d + 2$ points on one sphere. So every face is a simplex, and by (2) the only Delaunay triangulation is the set of these simplices. $\square$

**Size.** The lower boundary of $K$ is part of the boundary of a polytope with at most $n$ vertices in $\mathbb{R}^{d+1}$. By the upper bound theorem for polytopes, such a polytope has $O(n^{\lfloor (d+1)/2 \rfloor}) = O(n^{\lceil d/2 \rceil})$ faces. For $d = 2$ this gives $O(n)$, as in the [Voronoi complexity theorem](/voronoi-complexity-theorem/); for $d = 3$ it gives $O(n^2)$. The bound is reached in $d = 3$:

> **Two skew lines.** Let $a_i = (i, 0, 0)$ and $b_j = (0, j, 1)$ for $i, j = 0, \ldots, m - 1$, so $n = 2m$. Every tetrahedron $a_i a_{i+1} b_j b_{j+1}$ is Delaunay with no other point on its sphere, so all $(m - 1)^2 = (n/2 - 1)^2$ of them are in every Delaunay triangulation.

*Proof.* The two lines are skew, so the four points are affinely independent. A sphere meets a line in at most two points, so the sphere through $a_i$ and $a_{i+1}$ meets the first line only there, and the open ball meets that line in the open segment between them, which holds no $a_k$. The same holds for the second line. So no point is inside or on the sphere except the four corners. By (1) the lifted tetrahedron is in a lower face, and since every other lifted point is strictly above its hyperplane, that face is the tetrahedron itself, so by (2) it is a simplex of every Delaunay triangulation. $\square$

By duality, the Voronoi diagram of these points has $\Theta(n^2)$ vertices. For points drawn uniformly at random from a ball or cube, the expected size is $O(n)$ in every fixed dimension; [Dwyer's algorithm](/dwyer-algorithm/) uses this.

**Algorithms.**

- **Through convex hulls.** Any algorithm for the convex hull in $\mathbb{R}^{d+1}$ gives the Delaunay triangulation. The randomized incremental hull of Clarkson and Shor runs in $O(n \log n + n^{\lceil d/2 \rceil})$ expected time, which is $O(n^2)$ expected for $d = 3$; this matches the worst-case size.
- **Bowyer-Watson.** The [Bowyer-Watson algorithm](/bowyer-watson-algorithm/) works in any dimension: delete the simplices whose spheres hold the new point, and join the new point to the boundary of the hole. It is the usual method in 3D mesh codes.
- **Flips.** In 3D, the 2-3 and 3-2 flips replace two tetrahedra by three on the same five points, or the reverse. Starting from an arbitrary tetrahedralization, flips can get stuck before they reach the Delaunay one. After the insertion of one point into a Delaunay tetrahedralization, flips always succeed (Joe).
- **Weights.** With heights $|p|^2 - w_p$ the same constructions give the [regular triangulation](/regular-triangulation/) and the [power diagram](/power-diagram/) in $\mathbb{R}^d$.

**What does not carry over.** In the plane, the Delaunay triangulation maximizes the smallest angle. In space, no such statement holds for dihedral angles: a **sliver** is a tetrahedron whose four vertices are close to one circle, with volume close to zero and dihedral angles close to $0$ and $\pi$, and it can be Delaunay.

## Examples

**One in-sphere test.** For the tetrahedron $(0,0,0)$, $(2,0,0)$, $(0,2,0)$, $(0,0,2)$, the lifted hyperplane is $w = 2x + 2y + 2z$: it passes through $(0,0,0,0)$, $(2,0,0,4)$, $(0,2,0,4)$, $(0,0,2,4)$. So the circumcenter is $(1,1,1)$ and the squared radius is $0 + 3 = 3$.

| point $q$ | $|q|^2$ | $2x + 2y + 2z$ | position |
| --- | --- | --- | --- |
| $(1,1,1)$ | $3$ | $6$ | inside |
| $(2,2,0)$ | $8$ | $8$ | on the sphere |
| $(2,2,2)$ | $12$ | $12$ | on the sphere |
| $(3,0,0)$ | $9$ | $6$ | outside |

**A cube.** The eight corners of a cube are on one sphere, so every triangulation of the cube with its own corners is Delaunay. There are several: one with five tetrahedra (a regular tetrahedron and four corners), and others with six tetrahedra around a main diagonal. A grid of cubes gives many cospherical groups at once and is the standard hard test.

**A sliver.** The points $(1,0,\varepsilon)$, $(0,1,-\varepsilon)$, $(-1,0,\varepsilon)$, $(0,-1,-\varepsilon)$ for small $\varepsilon > 0$ form a tetrahedron of volume $\frac{4}{3} \varepsilon$. Alone, they are their own Delaunay triangulation, although the tetrahedron is almost flat.

**Two skew lines.** For $m = 5$ the set above has $10$ points and its Delaunay triangulation has $(5 - 1)^2 = 16$ tetrahedra, all of equal volume, filling the tetrahedron with corners $a_0$, $a_4$, $b_0$, $b_4$.

## Where it is used

- **Mesh generation.** Tetrahedral meshes for finite element methods start from a 3D Delaunay triangulation and then remove slivers and refine ([mesh generation](/mesh-generation/)).
- **Surface reconstruction.** Methods that rebuild a surface from a point cloud select faces of the 3D Delaunay triangulation, for example through [alpha shapes](/alpha-shape/) in space.
- **Interpolation.** Natural neighbour interpolation and piecewise linear interpolation of scattered data in $\mathbb{R}^d$ use the Delaunay simplices.
- **Molecular and materials science.** Weighted 3D diagrams describe the space around atoms, and 3D Voronoi cells describe grains and cells in materials.

## References
