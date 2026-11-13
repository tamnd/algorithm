---
tag: E6W632
kind: problem
slug: surface-reconstruction
name: Surface reconstruction
aliases:
- mesh reconstruction from point clouds
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Given points sampled from an unknown surface, possibly with normals and noise, build a mesh close to that surface with the same topology. Guarantees exist only under sampling conditions.
prereqs: [polygon-mesh, hausdorff-distance, medial-axis]
see_also: [ball-pivoting-algorithm, poisson-surface-reconstruction, alpha-shape, delaunay-triangulation, isosurface-extraction, signed-distance-function, principal-component-analysis, minimum-spanning-tree]
sources:
  - paper: doi:10.1145/142920.134011
    title: Hugues Hoppe, Tony DeRose, Tom Duchamp, John McDonald and Werner Stuetzle, Surface reconstruction from unorganized points, Computer Graphics (SIGGRAPH 92 Proceedings) 26(2), 71 to 78, 1992
    locator: the whole paper (the problem statement, tangent planes from neighbors, normal orientation along a spanning tree, the signed distance and the contouring)
  - paper: doi:10.1007/PL00009475
    title: Nina Amenta and Marshall Bern, Surface reconstruction by Voronoi filtering, Discrete and Computational Geometry 22(4), 481 to 504, 1999
    locator: the local feature size, the sampling condition relative to it, the crust, and the proof that the output is topologically valid and converges to the surface with its normals
  - paper: doi:10.1111/cgf.12802
    title: Matthew Berger, Andrea Tagliasacchi, Lee M. Seversky, Pierre Alliez, Gaël Guennebaud, Joshua A. Levine, Andrei Sharf and Cláudio T. Silva, A survey of surface reconstruction from point clouds, Computer Graphics Forum 36(1), 301 to 329, 2017
    locator: the whole survey (the kinds of input imperfections, the priors, and the families of methods)
  - paper: doi:10.1109/2945.817351
    title: Fausto Bernardini, Joshua Mittleman, Holly Rushmeier, Cláudio Silva and Gabriel Taubin, The ball-pivoting algorithm for surface reconstruction, IEEE Transactions on Visualization and Computer Graphics 5(4), 349 to 359, 1999
    locator: the introduction (interpolating reconstruction of large scans)
---

Surface reconstruction is the problem of building a surface from a finite set of points that were measured on it, such as the output of a laser scanner, a depth camera or photogrammetry. The output is usually a [polygon mesh](/polygon-mesh/), sometimes an [implicit surface](/implicit-surface/) that is meshed later. The problem is ill posed: many surfaces pass through or near any finite set of points, so a method must assume something about the unknown surface and about the sampling. The theory gives guarantees, such as a mesh homeomorphic to the surface and close to it, only when the samples are dense relative to the local feature size. Real scans have noise, holes and sharp edges and do not meet these conditions everywhere. For them there is no worst case guarantee on the quality of the result, and methods are compared by experiments.

## In plain words

A scanner gives you a cloud of dots on the skin of an object, and nothing else: no lines between the dots, and no record of which dots are neighbors on the surface. You want the skin back, as a sheet of triangles.

If the dots are close together compared with the size of the details, the answer looks obvious: join each dot to its near neighbors. But two dots that are close in space can be on two different sides of a thin wall. Where the scanner missed a part, there is a hole, and you must decide whether to close it. Noise moves the dots off the skin. So each method makes a guess about what the surface is like, and it works well when the guess is right.

## Definition

**Input.** A finite set $P = \{p_1, \ldots, p_n\} \subset \mathbb{R}^3$, assumed to lie on or near an unknown surface $S$, usually a compact 2-manifold, closed or with a border. Some inputs also give a normal $\nu_i$ at each point, from the scanner position or from the scan lines; some give several registered scans with their viewpoints.

**Output.** A mesh $M$ (or a function whose level set is $M$) that is close to $S$. The usual measures are the [Hausdorff distance](/hausdorff-distance/) between $M$ and $S$, the angle between their normals, and the topology: $M$ should be homeomorphic to $S$, or isotopic to it, which also fixes how it sits in space.

**Sampling condition.** The local feature size $\operatorname{lfs}(x)$ of a point $x \in S$ is its distance to the [medial axis](/medial-axis/) of $S$. It is small where $S$ is curved or where two parts of $S$ come close. $P$ is an $\varepsilon$-sample of $S$ if every $x \in S$ has a point of $P$ within distance $\varepsilon \cdot \operatorname{lfs}(x)$. Amenta and Bern proved that for a small enough $\varepsilon$, the crust of an $\varepsilon$-sample is topologically valid and converges to $S$, with its normals. At a sharp edge or corner $\operatorname{lfs} = 0$, so no finite set is an $\varepsilon$-sample of a surface with sharp features, and the theory says nothing there.

**Two families.** An interpolating method uses the input points as the vertices of $M$, as [ball pivoting](/ball-pivoting-algorithm/) and the Delaunay based methods do. An approximating method fits a smooth function to the points and extracts a level set, as Hoppe et al. and [Poisson surface reconstruction](/poisson-surface-reconstruction/) do; its vertices are new points, and it can smooth noise and fill holes.

## Variants

- **Curve reconstruction.** The same problem in the plane: join points sampled from closed curves into polygons. The 2D crust and its relatives have guarantees under the same kind of sampling condition.
- **With or without normals.** Normals make the problem much easier, because they tell the inside from the outside. Without them, a method first estimates the tangent plane at each point from its neighbors, for example by [principal component analysis](/principal-component-analysis/), and then orients the normals consistently.
- **Noise and outliers.** The points are off the surface by a random error, or some points are not on it at all. Interpolating methods keep the noise; approximating methods average it.
- **Holes and borders.** Parts of the surface have no samples. A method can leave a hole, close it smoothly, or must keep a real border, such as the edge of a sheet.
- **Watertight output.** The mesh must be closed, for 3D printing or for volume computations.
- **Priors.** The surface is assumed to be smooth, or piecewise planar, or made of known primitives such as planes, cylinders and spheres, as for buildings and machine parts.
- **Large data.** Scans of hundreds of millions of points, which call for out of core or streaming methods.

## Examples

**A sphere with normals.** Take $n$ points spread evenly on the unit sphere, with the outward normals. Ball pivoting with a radius a little above the spacing, and Poisson reconstruction, both give a closed mesh with $V - E + F = 2$; the pages of the two methods test this. With $\rho$ below half the spacing, ball pivoting gives nothing, and with a cap of points removed it leaves a hole, while Poisson closes the hole.

**Two thin walls.** Sample both faces of a slab of thickness $t$ at spacing $s$. If $s \ll t$, a good sample, the methods find two separate sheets joined at the rim. If $s > t$, the points of the two faces are nearer to each other than to their neighbors on the same face. The sample is not an $\varepsilon$-sample for a small $\varepsilon$ (the local feature size is about $t/2$), and a method that joins near neighbors builds triangles across the slab.

**Ambiguity in the plane.** The four points $(0, 0)$, $(2, 0)$, $(2, 2)$, $(0, 2)$ with the extra point $(1, 1 + \delta)$ can be one closed curve that dents in to the extra point, or a square plus an isolated point, or a curve through the points in another order. Nothing in the points chooses among them; a sampling condition does, by forbidding the cases where the curve passes between near points.

## Known algorithms

- **Tangent planes and signed distance.** Hoppe, DeRose, Duchamp, McDonald and Stuetzle, 1992: estimate a tangent plane at each point from its neighbors, orient the normals by propagation along a [minimum spanning tree](/minimum-spanning-tree/) of a neighbor graph, define a [signed distance](/signed-distance-function/) to the planes, and contour it with [marching cubes](/marching-cubes/).
- **[Alpha shapes](/alpha-shape/).** Edelsbrunner and Mücke: the simplices of the [Delaunay triangulation](/delaunay-triangulation/) that have an empty ball of radius $\alpha$. It needs one radius for the whole set.
- **Delaunay filtering.** The crust of Amenta and Bern keeps the Delaunay triangles that survive when the poles, far Voronoi vertices, are added; the cocone and the power crust are later methods of the same family with proofs of homeomorphism for $\varepsilon$-samples.
- **[Ball-pivoting algorithm](/ball-pivoting-algorithm/).** Bernardini et al., 1999: roll a ball of radius $\rho$ over the points; the output is a subset of the alpha shape for $\alpha = \rho$. Fast and small in memory, but it leaves holes where the sampling is sparse.
- **[Poisson surface reconstruction](/poisson-surface-reconstruction/).** Kazhdan, Bolitho and Hoppe, 2006: solve a Poisson equation for an indicator function whose gradient matches the normals, on an octree, and extract a level set. It is robust to noise and always closed, and it smooths fine detail.
- **Other implicit fits.** Radial basis functions, moving least squares surfaces, and volumetric merging of range images with signed distances along the lines of sight, each followed by [isosurface extraction](/isosurface-extraction/).

## Bounds

**No general guarantee.** For an arbitrary finite set there is no right answer, so there is no worst case bound on quality. The proven results are conditional: for an $\varepsilon$-sample of a smooth closed surface with $\varepsilon$ small enough, the crust and the cocone give a mesh homeomorphic to $S$, within $O(\varepsilon) \cdot \operatorname{lfs}$ of it, with normals within $O(\varepsilon)$. For Poisson reconstruction and ball pivoting on real data, quality is measured by experiment.

**Time.** Methods based on the 3D Delaunay triangulation take time proportional to its size, which is $\Theta(n^2)$ in the worst case for $n$ points in space, but much smaller for points that sample a surface well. Grid and octree methods take time proportional to the number of cells near the points; ball pivoting is linear for points of bounded density.

**Lower bound.** Even in the plane, with a sampling condition, reconstruction takes $\Omega(n \log n)$ time in the [algebraic decision tree](/algebraic-decision-tree/) model. To sort numbers $x_1, \ldots, x_n$ in $[0, 1)$, put each on the unit circle at the point $\left((1 - x_i^2)/(1 + x_i^2),\ 2 x_i/(1 + x_i^2)\right)$, which needs only arithmetic and lies at the angle $2 \arctan x_i$, an increasing function of $x_i$, and add the $n$ points at the angles $2 \pi k / n$, which are constants for a given $n$, so that the gaps are at most $2 \pi / n$. For large $n$ this is a dense sample of the circle, whose local feature size is 1 everywhere, so a correct method must return the polygon of the points in angular order. Reading the $x_i$ from it in $O(n)$ time sorts them, and sorting takes $\Omega(n \log n)$; see the [comparison sort lower bound](/comparison-sort-lower-bound/).

## Reductions

- **To isosurface extraction.** Approximating methods reduce the problem to fitting a function and then to [isosurface extraction](/isosurface-extraction/) of its level set.
- **To a Delaunay triangulation.** Interpolating methods with guarantees choose a subset of the triangles of the [Delaunay triangulation](/delaunay-triangulation/), using the [Voronoi diagram](/voronoi-diagram/) to estimate normals and the medial axis.
- **Normal orientation to a graph problem.** Orienting estimated normals consistently is done by propagation over a spanning tree of the neighbor graph, with edge weights that prefer nearly parallel tangent planes.
- **To mesh simplification.** The output is usually much larger than needed and is passed to [mesh simplification](/mesh-simplification/).

## Applications

- **3D scanning.** Digital models of sculptures, buildings and archaeological finds from laser and structured light scans.
- **Reverse engineering.** CAD models of machine parts from measurements, often with planes and cylinders as priors.
- **Robotics and mapping.** Surfaces of rooms and terrain from depth cameras and lidar, often in real time.
- **Medicine.** Surfaces of organs and teeth from scans and from contours drawn on image slices.
- **Film and games.** Models of actors and objects captured by photogrammetry.

## References
