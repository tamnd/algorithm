---
tag: SSJP31
kind: problem
slug: any-hit-query
name: Any-hit query
aliases:
- shadow query
area: graphics-and-signals/ray-tracing
level: intro
summary: Given a scene and a ray with an interval of its parameter, decide whether any object is hit in the interval; a search may stop at the first hit it finds, as in shadow tests.
model: real-ram
complexity:
  vars: {n: the number of objects in the scene}
  time: {worst: O(n)}
prereqs: [ray-object-intersection]
see_also: [closest-hit-query, shadow-determination, ambient-occlusion, next-event-estimation, bvh-traversal, bounding-volume-hierarchy, ray-casting, occlusion-query]
sources:
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Chapter 4, Primitives and Intersection Acceleration (the IntersectP predicate beside Intersect)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 26, Real-Time Ray Tracing (any-hit shaders and the flag that ends a search at the first accepted hit)
  - paper: doi:10.1137/0222051
    title: Pankaj K. Agarwal and Jiří Matoušek, Ray shooting and parametric search, SIAM Journal on Computing 22(4), 1993, 794 to 806
    locator: emptiness queries for segments, and the reduction of ray shooting to them
---

The any-hit query asks whether a ray hits anything at all in an interval $(t_{\min}, t_{\max})$ of its parameter, not which object it hits first. It is the decision version of the [closest-hit query](/closest-hit-query/), and it is cheaper: a search may test the objects in any order and stop at the first hit, because every hit gives the same answer. Its main use is the shadow ray, a segment from a surface point to a light, which is blocked if any object lies on it; see [shadow determination](/shadow-determination/). Renderers have a separate entry point for it, the IntersectP predicate of PBRT beside its Intersect, and ray tracing interfaces for graphics hardware have a flag that ends the search at the first accepted hit. It is a different thing from an [occlusion query](/occlusion-query/) of rasterization, which counts on the GPU how many samples of drawn geometry pass the depth test.

## In plain words

Stand at a point on the floor and look at a lamp. Is anything in the way? You do not care what the obstacle is, or how far it is, only whether there is one. As soon as you find one obstacle, you can stop looking.

That is the any-hit query: a yes or no question about a ray, with a near limit and a far limit along it. For a shadow, the ray goes from the point to the lamp, and the far limit is the lamp itself, so objects behind the lamp do not count. A yes can come after the first object checked; a no needs every object ruled out.

## Definition

**Input.** A scene of $n$ objects $S_1, \ldots, S_n$, each a closed set in $\mathbb{R}^3$ with a ray intersection test, a ray $o + t\,d$ with $d \ne 0$, an open interval $I = (t_{\min}, t_{\max})$, and optionally a filter $\mathrm{accept}(k, t)$ that may reject a hit.

**Output.** YES if there are an object $k$ and a parameter $t \in I$ with $o + t\,d \in S_k$ (and $\mathrm{accept}(k, t)$ true, when there is a filter), and NO otherwise. An implementation may also return the index of the object it found, but any object with an accepted hit is a correct witness, not only the nearest.

**The shadow ray.** For a surface point $p$ and a point light $q$, the segment is the ray $o = p$, $d = q - p$ on $I = (\varepsilon, 1 - \varepsilon)$. The point $p$ is lit by $q$ when the answer is NO. The small $\varepsilon \ge 0$ keeps the surface at $p$, and an emitter at $q$, from blocking the ray; with exact arithmetic and the open interval, $\varepsilon = 0$ already does this.

## Variants

- **With a filter.** Alpha-tested geometry, such as a leaf drawn on a rectangle, is hit only where its texture is opaque. The filter rejects the other hits, and the search goes on after a rejected hit. In hardware ray tracing interfaces the any-hit shader plays this role: it runs on candidate hits and may ignore them, so it is the filter, not the query.
- **Transmittance.** For colored glass or participating media, the question becomes how much light passes the segment, a product of the transmittances of all hits; then a search can no longer stop at the first hit, except when it reaches an opaque one.
- **Counting.** The number of hits in $I$, for example the parity of crossings that decides whether a point is inside a closed mesh.
- **Several lights or samples.** Soft shadows and [ambient occlusion](/ambient-occlusion/) ask many any-hit queries from one point, toward samples of an area light or of the hemisphere.
- **Segments in the plane.** Is the segment between two points free of the obstacles? This is the visibility test of visibility graphs and of motion planning.

## Examples

A floor triangle $(-10, -10, 0)$, $(10, -10, 0)$, $(0, 10, 0)$, a small triangle $B$ with the vertices $(-1, -1, 2)$, $(1, -1, 2)$, $(0, 1, 2)$, and a small triangle $B'$ with the same $x$ and $y$ at $z = 6$. The point $p = (0, 0, 0)$ lies on the floor and the light is at $q = (0, 0, 4)$, so the shadow ray is $d = (0, 0, 4)$ on $I = (0, 1)$.

| scene | hits in $I$ | answer |
|---|---|---|
| floor | none: the floor is hit at $t = 0$, outside the open interval | NO, $p$ is lit |
| floor and $B$ | $B$ at $t = \tfrac12$ | YES, $p$ is in shadow |
| floor and $B'$ | none: $B'$ is at $t = \tfrac32$, behind the light | NO, $p$ is lit |

With nine parallel triangles stacked on the ray at $z = 1, \ldots, 9$, a search that tests them in that order answers YES after one test, while a closest-hit scan in the same order must test all nine to rule out a closer hit.

## Known algorithms

| method | cost per query |
|---|---|
| linear scan, stopping at the first accepted hit | between 1 and $n$ tests; $n$ for every NO answer |
| [bounding volume hierarchy](/bounding-volume-hierarchy/) with [BVH traversal](/bvh-traversal/), in any order, ending at the first accepted hit | nodes visited plus objects tested; $O(n)$ in the worst case |
| kd-tree and [uniform grid](/uniform-grid/) traversal along the ray, ending at the first accepted hit | $O(n)$ in the worst case |
| shadow caches: test first the object that blocked the last shadow ray toward the same light | one test when the guess is right |
| [ray packet tracing](/ray-packet-tracing/) of the shadow rays of nearby points | shares traversal among coherent rays |
| segment emptiness structures of computational geometry, with superlinear preprocessing | sublinear; not used in renderers |

Since every hit is a witness, a traversal need not visit children nearest first, and it does not shrink $t_{\max}$ as the closest-hit query does. Renderers often order the children by a cheap guess, such as the larger box first, or use a separate tree built for shadow rays.

## Bounds

**Without preprocessing.** When the objects are only accessed through their intersection tests, every algorithm needs $n$ tests on a NO answer: if some object is not tested, an adversary can place a hit in it. A YES answer may need only one test, but in the worst case it also needs $n$, since the only hit can be in the last object tested. The linear scan meets both, so the query costs $\Theta(n)$ in the worst case, the same as the closest-hit query; the difference is in the typical case, where shadow rays toward lights in closed rooms are often blocked early.

**With preprocessing.** A [bounding volume hierarchy](/bounding-volume-hierarchy/) is fast on typical scenes, but that is observed, not proved: the worst case is $O(n)$ per query, for example on a NO answer for a segment that passes close to many objects with overlapping boxes. The surface area heuristic is a cost model, not a bound. Agarwal and Matoušek answered emptiness queries for segments among objects in space in sublinear time with superlinear space, and reduced ray shooting, the closest-hit query, to them by parametric search.

**In floating point.** A hit near $t_{\min}$ on the surface of the origin, called shadow acne, can make a lit point dark; renderers move the origin off the surface or use $\varepsilon > 0$, and a hit lost at a mesh edge can let light leak through, which [watertight](/watertight-ray-triangle-intersection/) triangle tests prevent.

## Reductions

- **Any-hit reduces to closest-hit.** The answer is YES exactly when the closest hit exists. The converse needs a search: the closest hit is the smallest $t$ for which the any-hit query on $(t_{\min}, t)$ says YES, which is how parametric search turns emptiness queries into ray shooting.
- **The any-hit query on a union of scenes** is the OR of the queries on the parts, in any order, and stops at the first YES.
- **Shadows from a point light reduce to one any-hit query** per visible point; see [shadow determination](/shadow-determination/). Shadows from an area light reduce to many, one per light sample, as in [next-event estimation](/next-event-estimation/).
- **Transformed objects** reduce to the untransformed object with the inverse map applied to the ray, with the same interval; see [object instancing](/object-instancing/).

## Applications

- **Shadows.** The shadow rays of [ray casting](/ray-casting/) and of [Whitted ray tracing](/whitted-ray-tracing/), one per light and visible point.
- **Direct lighting in path tracing.** Each light sample of [next-event estimation](/next-event-estimation/) costs one any-hit query between the surface point and the sample on the light.
- **Ambient occlusion.** The fraction of short rays from a point that hit nothing within a radius; see [ambient occlusion](/ambient-occlusion/).
- **Line of sight.** Whether one agent in a game can see another, and visibility tests in motion planning.
- **Inside and outside tests** of closed meshes by counting crossings along a ray.

## References
