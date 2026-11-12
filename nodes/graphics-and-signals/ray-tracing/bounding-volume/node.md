---
tag: R4901A
kind: concept
slug: bounding-volume
name: Bounding volume
aliases: [bounding volume test]
area: graphics-and-signals/ray-tracing
level: intro
summary: A simple shape, such as a box or a sphere, that contains a complex object. A query that misses the simple shape misses the object, so one cheap test can reject a costly one.
prereqs: [convex-hull]
see_also: [axis-aligned-bounding-box, bounding-volume-hierarchy, slab-method, minimum-bounding-rectangle, minimum-enclosing-ball, separating-axis-theorem, collision-detection, frustum-culling]
sources:
  - paper: doi:10.1145/360349.360354
    title: James H. Clark, Hierarchical geometric models for visible surface algorithms, Communications of the ACM 19(10), 1976, 547 to 554
    locator: bounding volumes around objects and their hierarchy, used to reject invisible parts of a scene
  - paper: doi:10.1145/15886.15916
    title: Timothy L. Kay and James T. Kajiya, Ray tracing complex scenes, SIGGRAPH 1986, Computer Graphics 20(4), 269 to 278
    locator: the slab volumes with a fixed set of normals and their fit compared with boxes and spheres
  - paper: doi:10.1145/237170.237244
    title: Stefan Gottschalk, Ming C. Lin and Dinesh Manocha, OBBTree, a hierarchical structure for rapid interference detection, SIGGRAPH 1996, 171 to 180
    locator: oriented bounding boxes, their fit by the covariance of the hull, and the overlap test with 15 separating axes
  - paper: doi:10.1109/2945.675649
    title: James T. Klosowski, Martin Held, Joseph S. B. Mitchell, Henry Sowizral and Karel Zikan, Efficient collision detection using bounding volume hierarchies of k-DOPs, IEEE Transactions on Visualization and Computer Graphics 4(1), 1998, 21 to 36
    locator: discrete orientation polytopes with k fixed normals and their overlap test
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 4, Bounding Volumes (desired properties, AABBs, spheres, OBBs, sphere-swept volumes and k-DOPs)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Chapter 4, Primitives and Intersection Acceleration, Section 4.3 Bounding Volume Hierarchies (the surface area ratio as the probability that a ray meets a child box)
---

A bounding volume of an object is a simple shape that contains it, such as a box, a sphere or an intersection of a few slabs. Any query that misses the bounding volume also misses the object, so one cheap test can replace a costly one in most cases. The test is conservative: a hit on the volume does not mean a hit on the object, and the exact test must then follow. Bounding volumes are the nodes of a [bounding volume hierarchy](/bounding-volume-hierarchy/) and the first test in ray tracing, culling and collision detection.

## In plain words

Before you check if a thrown ball hits a statue with all its fine detail, check if it hits the crate that the statue came in. A miss on the crate is a miss on the statue, and the crate is easy to check. Only when the ball hits the crate do you look at the statue itself.

The crate can be a box, a ball, or a tighter shape. A tight shape gives fewer false alarms, where the crate is hit but the statue is not. A simple shape is quicker to check. A good bounding volume is a balance of the two, and the best choice depends on how often you test and how much a false alarm costs.

## The idea

Let $X \subset \mathbb{R}^3$ be a bounded object. A *bounding volume* of $X$ is a set $V$ from a fixed family of simple shapes with $X \subseteq V$. For a query set $Q$, such as a ray, a view frustum or another object, $Q \cap V = \emptyset$ implies $Q \cap X = \emptyset$. The converse is false, and $Q \cap V \ne \emptyset$ with $Q \cap X = \emptyset$ is a false positive.

**Cost.** Let $c_V$ be the cost of the volume test, $c_X$ the cost of the exact test, and $p$ the probability that a query meets $V$. The test with the volume costs $c_V + p\,c_X$ on average, against $c_X$ without it, so the volume pays off when $p < 1 - c_V / c_X$. Weghorst, Hooper and Greenberg (1984) used this kind of balance to choose volumes for ray tracing, and the same terms appear in the cost of a hierarchy.

**Fit under random rays.** For convex sets $X \subseteq V$ and a uniform random line, the probability that the line meets $X$, given that it meets $V$, is $S(X)/S(V)$, the ratio of the surface areas. This is the Cauchy and Crofton result from integral geometry: the measure of the lines that meet a convex body is proportional to its surface area. For a flat convex set, $S$ counts both sides, so it is twice the area. This ratio is the base of the [surface area heuristic](/surface-area-heuristic/). For a nonconvex $X$ it bounds the probability for the [convex hull](/convex-hull/) of $X$, which is the tightest convex volume.

**The families.** Each family trades fit against the cost of the tests and of the fit.

| volume | storage | ray test | overlap test | fit | under rotation |
|---|---|---|---|---|---|
| sphere | center, radius: 4 numbers | one quadratic | distance of centers against the sum of radii | poor for long or flat objects | unchanged |
| [axis-aligned box](/axis-aligned-bounding-box/) | 6 numbers | [slab method](/slab-method/) | 3 interval tests | good for axis-aligned parts | must be refit or grows |
| oriented box (OBB) | center, 3 axes, 3 half extents: 15 numbers | slab method in the box frame | 15 separating axes | good for long objects at any angle | rotates exactly |
| k-DOP, slab volume | $k$ numbers for $k/2$ fixed normals | $k/2$ slabs | $k/2$ interval tests | tighter as $k$ grows | must be refit |
| [convex hull](/convex-hull/) | all hull faces | clip against each face | [GJK](/gjk-algorithm/) or [separating axes](/separating-axis-theorem/) | tightest convex | rotates exactly |

The box is the 6-DOP with the three coordinate normals, and the slab volumes of Kay and Kajiya (1986) are the same idea for ray tracing. Spheres for a set of points come from the [minimum enclosing ball](/minimum-enclosing-ball/), or from a fast approximate fit. Gottschalk, Lin and Manocha (1996) fit an OBB with the axes of the covariance of the convex hull, and test two OBBs for overlap with the 15 candidate axes of the [separating axis theorem](/separating-axis-theorem/). Klosowski et al. (1998) used k-DOPs with $k = 6, 14, 18, 26$ for collision detection.

**Requirements for a hierarchy.** A node volume must contain the objects below it. The union of two boxes or two k-DOPs with the same normals is computed per coordinate in $O(k)$, and the result is the tightest of its family. The tight sphere around two spheres is also cheap, but the tight sphere around a set of objects is not the sphere around the spheres of its parts, so sphere trees are looser.

## Examples

- **A right triangle.** The triangle with corners $(0, 0, 0)$, $(4, 0, 0)$ and $(0, 3, 0)$ has area 6, so $S(X) = 12$ counting both sides. Its box $[0, 4] \times [0, 3] \times [0, 0]$ is flat with $S = 2 \cdot 4 \cdot 3 = 24$. Its smallest sphere has its center at the middle of the hypotenuse, $(2, 1.5, 0)$, and radius 2.5, so $S = 4\pi \cdot 2.5^2 = 25\pi \approx 78.54$. A uniform random line that meets the box meets the triangle with probability $12/24 = 0.5$; one that meets the sphere does so with probability $12/(25\pi) \approx 0.153$. Here the box rejects far more false positives.
- **A rotated cube.** A unit cube has $S = 6$, and its box is itself. Rotate it by 45 degrees about the z axis. Its box becomes $\sqrt 2 \times \sqrt 2 \times 1$ with $S = 2(2 + 2\sqrt 2) = 4 + 4\sqrt 2 \approx 9.657$, so the probability of a true hit after a box hit drops to $6/9.657 \approx 0.621$. Its smallest sphere has radius $\sqrt 3/2$ and $S = 3\pi \approx 9.425$ before and after the rotation, which gives $6/(3\pi) \approx 0.637$. An OBB stays the cube, with probability 1.
- **A long diagonal rod.** A thin rod from $(0, 0, 0)$ to $(10, 10, 10)$ has a box that is the full cube $[0, 10]^3$, with $S = 600$, while the rod itself has almost no area. An OBB along the rod fits it well. This is the case for which oriented boxes were made.
- **A false positive.** The ray from $(3, 2.5, 1)$ in the direction $(0, 0, -1)$ meets the box of the triangle above at $(3, 2.5, 0)$, but $3/4 + 2.5/3 > 1$, so it misses the triangle. The box test passes, and the exact test must run.

## Where it is used

- [Bounding volume hierarchy](/bounding-volume-hierarchy/): a tree of volumes, the main use in ray tracing, with [BVH traversal](/bvh-traversal/).
- [Slab method](/slab-method/): the ray test for boxes and slab volumes.
- [Collision detection](/collision-detection/): a broad phase on boxes or spheres, then a narrow phase on the exact shapes, often with [GJK](/gjk-algorithm/).
- [Frustum culling](/frustum-culling/) and [occlusion culling](/occlusion-culling/): a box or sphere outside the view, or behind an occluder, removes its whole object.
- [Minimum bounding rectangle](/minimum-bounding-rectangle/) and the [R-tree](/r-tree/): the same idea in spatial databases, with axis-aligned boxes in the plane or in space.
- [Loose octree](/loose-octree/) and [uniform grid](/uniform-grid/): objects are put in cells by the boxes that bound them.

## References
