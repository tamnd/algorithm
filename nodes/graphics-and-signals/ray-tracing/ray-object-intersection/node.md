---
tag: J1XKQ6
kind: problem
slug: ray-object-intersection
name: Ray-object intersection
aliases:
- ray intersection
- ray-primitive intersection
area: graphics-and-signals/ray-tracing
level: intro
summary: Given a ray, an interval of its parameter and one geometric object, find the parameters at which the ray meets the object, with the hit point and its surface data.
model: real-ram
complexity:
  time: {worst: O(1)}
prereqs: [dot-product, cross-product]
see_also: [closest-hit-query, any-hit-query, ray-plane-intersection, ray-sphere-intersection, moller-trumbore, slab-method, vertical-ray-shooting, line-line-intersection]
sources:
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 22, Intersection Test Methods (Sections 22.6 to 22.8 for spheres, boxes and triangles)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Chapter 3, Shapes (the interface of an intersection routine and the shapes that implement it)
  - book: isbn:9780122861604
    title: Andrew S. Glassner (editor), An Introduction to Ray Tracing, Academic Press, 1989
    locator: Chapter 2, Essential Ray Tracing Algorithms, by Eric Haines
  - paper: doi:10.1137/0222051
    title: Pankaj K. Agarwal and Jiří Matoušek, Ray shooting and parametric search, SIAM Journal on Computing 22(4), 1993, 794 to 806
    locator: the reduction of ray shooting queries to emptiness queries by parametric search
---

Ray-object intersection asks where a ray meets one geometric object: for which parameters $t$ in an interval the point $o + t\,d$ lies on the object, and what the surface is like there. It is the basic operation of ray tracing. Every ray tracer is a loop over such tests, one per object that a ray may hit, organized by a scene query such as the [closest-hit query](/closest-hit-query/) or the [any-hit query](/any-hit-query/). Each kind of object, from planes and spheres to triangles, boxes and implicit surfaces, has its own algorithm, and most of them cost a constant number of arithmetic operations in exact arithmetic. The hard part in practice is floating point: a hit can be lost at an edge, or found at the wrong side of a surface.

## In plain words

A ray is a half line: a start point and a direction. Picture a laser pointer and one object in the room. The question is whether the beam touches the object, and if so, how far along the beam, at which point, and which way the surface faces there.

The answer can be no point (a miss), one point (a plane or a triangle), two points (the beam enters and leaves a ball), or more for curved or complex shapes. A renderer usually needs only the nearest hit in a range of distances, but some tasks need all of them, such as finding the inside of a solid.

## Definition

**Input.** A ray $r(t) = o + t\,d$ with an origin $o \in \mathbb{R}^3$ and a direction $d \in \mathbb{R}^3 \setminus \{0\}$, an interval $I = (t_{\min}, t_{\max})$ with $0 \le t_{\min} < t_{\max} \le \infty$, and an object, a closed set $S \subset \mathbb{R}^3$ given by a finite description (a plane, a sphere, a triangle, a box, a polynomial equation).

**Output.** The hit set $H = \{\, t \in I : o + t\,d \in S \,\}$, in one of the forms of the variants below. For the first-hit form the answer is

$$t^* = \min H \quad (\text{or MISS if } H = \emptyset),$$

together with the hit data: the point $p = o + t^* d$, the surface normal $n(p)$, and the surface coordinates of $p$, for example the barycentric coordinates in a triangle or $(u, v)$ in a parametric patch.

The direction need not have unit length; then $t$ measures distance in units of $|d|$, and a ray segment from $a$ to $b$ is the ray $o = a$, $d = b - a$ on $I = (0, 1)$.

## Variants

- **Decision.** Is $H$ empty? This is the test of shadow rays and of culling.
- **First hit.** The smallest $t \in H$ with its hit data; the usual form.
- **All hits, as intervals.** For a solid $S$, the set $H$ is a union of intervals, and set operations on solids (unions, intersections, differences) combine these intervals; Roth's ray casting of solids works in this form.
- **One-sided tests.** Only hits where the ray enters the surface from the front, $d \cdot n < 0$, count; this is back-face culling.
- **Special objects.** Planes, spheres, quadrics, triangles, convex polygons, axis-aligned and oriented boxes, cylinders, tori (a quartic in $t$), parametric patches and implicit surfaces.
- **Scenes.** With many objects, the problem becomes a query on a scene: the [closest-hit query](/closest-hit-query/) asks for the smallest $t$ over all objects, and the [any-hit query](/any-hit-query/) for any hit in $I$.
- **In the plane.** In 2D, a ray against segments is [line-line intersection](/line-line-intersection/) restricted to the segment and the ray, and ray shooting in a planar subdivision has its own data structures, for example [vertical ray shooting](/vertical-ray-shooting/).

## Examples

| object | ray $o$, $d$ | hit set $H$ on $(0, \infty)$ |
|---|---|---|
| plane $z = 0$ | $(0, 0, 3)$, $(1, 0, -2)$ | $\{1.5\}$, at $(1.5, 0, 0)$ |
| unit sphere at the origin | $(0, 0, -5)$, $(0, 0, 1)$ | $\{4, 6\}$, entry at $(0, 0, -1)$ and exit at $(0, 0, 1)$ |
| triangle $(0,0,0), (1,0,0), (0,1,0)$ | $(\tfrac14, \tfrac14, 1)$, $(0, 0, -1)$ | $\{1\}$, barycentric coordinates $(\tfrac12, \tfrac14, \tfrac14)$ |
| unit sphere at the origin | $(0, 2, -5)$, $(0, 0, 1)$ | empty: the line passes at distance 2 from the center |
| plane $z = 0$ | $(0, 0, 3)$, $(1, 0, 0)$ | empty: the ray is parallel to the plane |
| unit cube $[0, 1]^3$ | $(-1, \tfrac12, \tfrac12)$, $(1, 0, 0)$ | the interval $[1, 2]$, entry at $t = 1$ |

## Known algorithms

| object | algorithm | cost |
|---|---|---|
| plane | [ray-plane intersection](/ray-plane-intersection/) | $\Theta(1)$, one division |
| sphere | [ray-sphere intersection](/ray-sphere-intersection/), with stable roots | $\Theta(1)$, one square root |
| triangle | [Möller-Trumbore](/moller-trumbore/), by Cramer's rule | $\Theta(1)$, not watertight in floating point |
| triangle | [watertight ray-triangle intersection](/watertight-ray-triangle-intersection/) | $\Theta(1)$, watertight on meshes |
| triangle | [Plücker ray-triangle test](/plucker-ray-triangle-test/) | $\Theta(1)$, watertight along edges |
| axis-aligned box | the [slab method](/slab-method/) | $\Theta(k)$ for $k$ axes |
| implicit surface with a distance bound | [sphere tracing](/sphere-tracing/) of a [signed distance function](/signed-distance-function/) | iterative; no fixed bound |
| general implicit or heightfield | [ray marching](/ray-marching/) | iterative; no fixed bound |

## Bounds

For each object of bounded description, such as a plane, a quadric, a triangle or a box, the hit set is found with $O(1)$ arithmetic operations in the [real RAM](/real-ram/), since it is the set of roots in $I$ of a polynomial of bounded degree, restricted by a bounded number of sign conditions. Reading the input takes $\Omega(1)$, so this is tight. For surfaces of degree up to 4, such as tori, the roots have closed forms; for higher degree and for general implicit surfaces, a numerical root finder is needed, and its cost depends on the accuracy.

In floating point, the exact answer for the rounded inputs can be decided with exact predicates, using [error-free transformations](/error-free-transformations/), [Shewchuk's expansions](/shewchuk-expansion-sum/) or [interval arithmetic](/interval-arithmetic/) as a filter. The usual fast tests are not exact: they are only usually correct near edges and tangent rays, and the [watertight test](/watertight-ray-triangle-intersection/) guarantees a weaker but sufficient property for meshes.

For a scene of $n$ objects, a query by a linear scan costs $\Theta(n)$ tests. Acceleration structures such as the [bounding volume hierarchy](/bounding-volume-hierarchy/) are fast on typical scenes but cost $O(n)$ per ray in the worst case. With superlinear preprocessing, ray shooting among triangles in space can answer each query in sublinear time; Agarwal and Matoušek reduced ray shooting to emptiness queries by [parametric search](/parametric-search/). These structures are of theoretical interest and are not used in renderers.

## Reductions

- **Segment queries** reduce to ray queries on the interval $(0, 1)$, with $d = b - a$.
- **Ray-triangle reduces to a $3 \times 3$ linear system**, solved by [Cramer's rule](/cramers-rule/), with three sign conditions on the solution.
- **Ray-polygon reduces to ray-plane** followed by a 2D [point in polygon](/point-in-polygon/) test.
- **Ray-box reduces to ray-plane** for three pairs of parallel planes, followed by an intersection of intervals.
- **Transformed objects.** A ray against an object under an affine map $M$ reduces to the ray $(M^{-1} o, M^{-1} d)$ against the untransformed object, with the same $t$; this is [object instancing](/object-instancing/).
- **Point in a closed mesh reduces to ray-mesh crossings**: the point is inside if a ray from it crosses the surface an odd number of times, which needs a watertight test.

## Applications

- **Rendering.** [Ray casting](/ray-casting/), [Whitted ray tracing](/whitted-ray-tracing/), [path tracing](/path-tracing/) and [ambient occlusion](/ambient-occlusion/) are built from ray-object tests.
- **Visibility and shadows.** A shadow ray is a decision query on a segment; see [shadow determination](/shadow-determination/).
- **Picking.** The object under the mouse is the first hit of the ray through the cursor.
- **Collision detection and physics.** Fast objects are tested by rays or segments along their motion, and line-of-sight tests in games are segment queries.
- **Acoustics and radio.** Sound and radio propagation are simulated by tracing rays among walls.
- **Geometry processing.** Inside and outside tests of meshes, and the distance from a point to a surface along a direction.

## References
