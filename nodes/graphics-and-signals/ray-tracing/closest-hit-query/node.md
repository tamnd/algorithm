---
tag: Q9V10R
kind: problem
slug: closest-hit-query
name: Closest-hit query
aliases:
- nearest-intersection query
area: graphics-and-signals/ray-tracing
level: intro
summary: Given a scene of objects and a ray with an interval of its parameter, find the object hit at the smallest parameter in the interval, with that parameter, or report that nothing is hit.
model: real-ram
complexity:
  vars: {n: the number of objects in the scene}
  time: {worst: O(n)}
prereqs: [ray-object-intersection]
see_also: [any-hit-query, ray-casting, bounding-volume-hierarchy, bvh-traversal, kd-tree-traversal, uniform-grid, hidden-surface-removal, vertical-ray-shooting]
sources:
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Chapter 4, Primitives and Intersection Acceleration (the Intersect and IntersectP interfaces, and bounding volume hierarchies)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 26, Real-Time Ray Tracing (closest-hit and any-hit shaders of ray tracing interfaces)
  - paper: doi:10.1137/0222051
    title: Pankaj K. Agarwal and Jiří Matoušek, Ray shooting and parametric search, SIAM Journal on Computing 22(4), 1993, 794 to 806
    locator: ray shooting queries with preprocessing, by a reduction to emptiness queries
---

The closest-hit query asks which object of a scene a ray hits first: among all hits with a parameter in the interval $(t_{\min}, t_{\max})$, the one with the smallest parameter. It is the query of visibility in ray tracing, because the first object along the ray from the eye through a pixel is the one seen at that pixel, and of every bounce of a path tracer. Ray tracing interfaces for graphics hardware name it after the shader that runs on the closest hit. It is built on per-object [ray-object intersection](/ray-object-intersection/) tests and differs from the [any-hit query](/any-hit-query/), which only asks whether some hit exists and can stop at the first one it finds. It is also different from an occlusion query of rasterization, which counts the visible samples of drawn geometry on the GPU; see [occlusion query](/occlusion-query/).

## In plain words

Shine a laser pointer into a room full of objects. Many objects may lie on the line of the beam, but the beam stops at the first one. The closest-hit query finds that one, and how far away it is.

A distance range comes with the question: hits closer than the near limit or farther than the far limit do not count. The near limit keeps a ray that leaves a surface from finding that same surface again, and the far limit lets a renderer ask for something closer than a hit it already has.

## Definition

**Input.** A scene of $n$ objects $S_1, \ldots, S_n$, each a closed set in $\mathbb{R}^3$ with a ray intersection test, a ray $o + t\,d$ with $d \ne 0$, and an open interval $I = (t_{\min}, t_{\max})$.

**Output.** With the hit sets $H_k = \{\, t \in I : o + t\,d \in S_k \,\}$, let $t^* = \inf \bigcup_k H_k$. If the union is empty, the answer is NONE. Otherwise the answer is a pair $(t^*, k)$ with $t^* \in H_k$, together with the hit data of $S_k$ at $o + t^* d$ (the point, the normal, the surface coordinates). For the objects of graphics, closed sets of bounded description, the infimum is attained when it is greater than $t_{\min}$.

When several objects are hit at the same $t^*$, any of them is a correct answer; an implementation usually returns the first one in scene order, so that the answer is deterministic.

## Variants

- **With a filter.** A callback can reject a hit, for example where an alpha texture makes a leaf transparent; then the query asks for the smallest accepted hit.
- **The $k$ closest hits, or all hits in order.** For transparency and for volumes, a renderer may need several hits sorted by $t$.
- **Ray packets and streams.** Many rays are queried together against one scene, to share the work of traversal; see [ray packet tracing](/ray-packet-tracing/).
- **The decision version.** Is there any hit in $I$? This is the [any-hit query](/any-hit-query/).
- **Segments.** A segment from $a$ to $b$ is the ray $d = b - a$ on $I = (0, 1)$.
- **In the plane.** Ray shooting among segments in 2D, and [vertical ray shooting](/vertical-ray-shooting/) in a planar subdivision, which point location answers in $O(\log n)$ time.

## Examples

Two triangles parallel to the $xy$ plane, $S_1$ with the vertices $(0, 0, 1)$, $(4, 0, 1)$, $(0, 4, 1)$ and $S_2$ with the same $x$ and $y$ at $z = 2$, and the ray from $o = (1, 1, 5)$ with $d = (0, 0, -1)$. The ray hits $S_2$ at $t = 3$ and $S_1$ at $t = 4$.

| interval $I$ | answer |
|---|---|
| $(0, \infty)$ | $(3, S_2)$ |
| $(3, \infty)$ | $(4, S_1)$: the interval is open, so the hit at $t = 3$ does not count |
| $(0, 3)$ | NONE |
| $(0, 3.5)$ | $(3, S_2)$ |

## Known algorithms

| method | cost per query |
|---|---|
| linear scan: test every object, and shrink $t_{\max}$ to each hit found | $\Theta(n)$ tests |
| [bounding volume hierarchy](/bounding-volume-hierarchy/) with [BVH traversal](/bvh-traversal/), nearest child first, skipping boxes entered after the best hit | nodes visited plus objects tested; $O(n)$ in the worst case |
| kd-tree with [kd-tree traversal](/kd-tree-traversal/), front to back, stopping at the first cell with a hit | $O(n)$ in the worst case |
| [uniform grid](/uniform-grid/), traversed cell by cell along the ray | $O(n)$ objects plus the cells passed in the worst case |
| ray shooting structures of computational geometry with superlinear preprocessing (Agarwal and Matoušek) | sublinear; not used in practice |

The per-object tests are the algorithms of [ray-object intersection](/ray-object-intersection/), for example the [Möller-Trumbore](/moller-trumbore/) and [watertight](/watertight-ray-triangle-intersection/) tests for triangles.

## Bounds

**Without preprocessing.** In a model where the objects are only accessed through their intersection tests, every algorithm needs $n$ tests in the worst case: if some object is not tested, an adversary can make that object the one with the closest hit. The linear scan meets this bound, so the query costs $\Theta(n)$.

**With preprocessing.** Acceleration structures cost $O(n \log n)$ or so to build, and on typical scenes a query then visits a number of nodes and objects that grows slowly with $n$, often close to logarithmic. That behavior is observed, not proved: for a [bounding volume hierarchy](/bounding-volume-hierarchy/), a ray that passes close to many objects whose boxes overlap visits $\Omega(n)$ nodes, so the worst case is $O(n)$ per ray, as for the scan. The surface area heuristic, which guides the construction of good trees, is a cost model with assumptions about the distribution of rays, not a bound. In computational geometry, ray shooting among $n$ triangles in space can be answered in sublinear worst-case time with superlinear space, through the reduction of Agarwal and Matoušek to emptiness queries.

**In floating point.** The answer can differ from the exact one when two hits have nearly equal $t$, and an object can be missed at an edge if the triangle test is not watertight.

## Reductions

- **Any-hit reduces to closest-hit.** A closest hit answers the decision version; the converse does not hold, which is why the any-hit query is cheaper.
- **Hidden-surface removal by ray casting reduces to closest-hit queries**, one per pixel sample; see [ray casting](/ray-casting/) and [hidden-surface removal](/hidden-surface-removal/).
- **The closest hit over a union of scenes** is the closest of the closest hits over the parts, with the far limit of each query set to the best hit so far; this is how a traversal combines subtrees, and how instanced scenes combine instances.
- **Transformed objects** reduce to their untransformed form by the inverse map applied to the ray, with the same $t$; see [object instancing](/object-instancing/).

## Applications

- **Visibility.** The primary rays of [ray casting](/ray-casting/), and every reflected and refracted ray of [Whitted ray tracing](/whitted-ray-tracing/).
- **Global illumination.** Each bounce of a [path tracer](/path-tracing/) is a closest-hit query.
- **Picking.** The object under the cursor is the closest hit of the ray through the cursor.
- **Physics and games.** Line-of-sight, projectile and sensor queries ask for the first object along a segment.

## References
