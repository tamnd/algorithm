---
tag: NXDDGG
kind: algorithm
slug: ray-casting
name: Ray casting
area: graphics-and-signals/ray-tracing
level: intro
summary: Render an image by casting one ray from the eye through each pixel, taking the closest object it hits, and shading that point with local lighting and a shadow ray.
model: real-ram
complexity:
  vars: {P: the number of pixels, n: the number of objects}
  time: {worst: Θ(P n)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 1968
  people: [Arthur Appel]
  note: Appel decided visibility and shadows by rays from the eye and to the light; Scott Roth named the method ray casting in 1982, for rendering solids.
prereqs: [primary-ray-generation, closest-hit-query, hidden-surface-removal]
see_also: [whitted-ray-tracing, any-hit-query, shadow-determination, z-buffer, lambertian-reflectance, ray-object-intersection, bounding-volume-hierarchy, ray-marching]
sources:
  - paper: doi:10.1145/1468075.1468082
    title: Arthur Appel, Some techniques for shading machine renderings of solids, AFIPS Spring Joint Computer Conference, vol. 32, 1968, 37 to 45
    locator: the rays from the eye through the picture plane for visibility, and the rays to the light for shadows
  - paper: doi:10.1016/0146-664X(82)90169-1
    title: Scott D. Roth, Ray casting for modeling solids, Computer Graphics and Image Processing 18(2), 1982, 109 to 144
    locator: the ray casting of solids built by set operations, and the name of the method
  - paper: doi:10.1145/358876.358882
    title: Turner Whitted, An improved illumination model for shaded display, Communications of the ACM 23(6), 1980, 343 to 349
    locator: the recursive extension with reflected and refracted rays
  - book: isbn:9781482229394
    title: Steve Marschner and Peter Shirley, Fundamentals of Computer Graphics, fourth edition, CRC Press, 2016
    locator: Chapter 4, Ray Tracing (the basic ray tracing algorithm, shading and shadows)
---

Ray casting renders an image by sending one ray from the eye through each pixel and asking which object the ray hits first. That object is the visible one at the pixel, so ray casting is a method of [hidden-surface removal](/hidden-surface-removal/) that works pixel by pixel instead of object by object. The color of the pixel comes from a local shading model at the hit point, usually [Lambert's cosine law](/lambertian-reflectance/) for a point light, and a second ray toward the light tells whether the point is in shadow. Ray casting stops there: it follows no reflected or refracted rays, which is what [Whitted ray tracing](/whitted-ray-tracing/) adds.

## In plain words

Look at the scene through a screen door, one hole per pixel. For each hole, ask which thing you see through it: draw a straight line from your eye through the hole and find the first object it touches. Color the hole with the color of that object.

To make the picture look solid, the color depends on how directly the surface faces the lamp: a surface that faces it is bright, a surface at a grazing angle is dark. To get shadows, draw a second line from the touched point to the lamp. If anything is in the way, the point is in shadow and gets only a little background light.

## The problem

The input is a scene of $n$ objects, each with an intersection test and a surface normal, a camera with an image of $W \times H$ pixels, $P = W H$, a point light at $\ell$, and an ambient level $k_a \in [0, 1]$. The output is, for each pixel, the index of the visible object or NONE, and a gray value in $[0, 1]$.

The visible object of a pixel is the object with the smallest positive ray parameter among the hits of the pixel's ray, a [closest-hit query](/closest-hit-query/). The gray value of a visible point $p$ with the normal $n$ facing the viewer is $k_a + (1 - k_a) \cos \alpha$ when the light is in front of the surface and the segment from $p$ to $\ell$ meets no object, with $\cos \alpha = n \cdot (\ell - p) / (|n|\,|\ell - p|)$, and $k_a$ otherwise.

## The algorithm

```pseudo id=main
RAY-CAST(objects, camera, light)
L1  for each pixel (i, j) of the image
L2      (o, d) ← PRIMARY-RAY(i, j, 1/2, 1/2)               ▷ through the pixel center
L3      best ← NONE;  tmax ← ∞
L4      for each object k:  if k hits (o, d) at some t in (0, tmax) then tmax ← t;  best ← k
L5      if best = NONE then image[i, j] ← background;  continue
L6      p ← o + tmax · d;  n ← the normal of best at p, turned to face the eye
L7      L ← light − p
L8      if n · L ≤ 0 or ANY-HIT(objects, p, L, ε, 1 − ε) then image[i, j] ← ka
L9      else image[i, j] ← ka + (1 − ka) · (n · L) / (|n| · |L|)
```

Line L2 is [primary ray generation](/primary-ray-generation/) for a [pinhole camera](/pinhole-camera-model/). Lines L3 and L4 are the [closest-hit query](/closest-hit-query/) by a linear scan: each object is tested with its own [ray-object intersection](/ray-object-intersection/), such as the [ray-sphere](/ray-sphere-intersection/) or the [Möller-Trumbore](/moller-trumbore/) test, and every hit shrinks the interval, so later objects must be closer to count. Line L5 leaves a pixel without a hit to the background.

Line L6 computes the hit point and its normal. A two-sided surface, such as a single triangle, has its normal flipped when it points away from the eye, so that $n \cdot d < 0$. Line L8 is the shadow test: the segment from $p$ to the light is the ray $p + t\,L$ with $t \in (\varepsilon, 1 - \varepsilon)$, and an [any-hit query](/any-hit-query/) on it decides whether something blocks the light; it may stop at the first blocker. The small $\varepsilon$ keeps the surface itself and the light out of the test. This is the ray form of [shadow determination](/shadow-determination/). Line L9 is Lambert's cosine law.

## Example

A sphere of radius 2 at the origin, a camera at $e = (0, 0, 10)$ looking down the $z$ axis with $\tan(\theta / 2) = 0.25$, an image of $7 \times 7$ pixels, the light at the eye and $k_a = 0.1$.

The center pixel $(3, 3)$ has the ray $o = (0, 0, 10)$, $d = (0, 0, -1)$. Line L4 finds the sphere at $t = 8$, the root of $(10 - t)^2 = 4$ that is smaller. Line L6 gives $p = (0, 0, 2)$ and $n = (0, 0, 2)$, line L7 gives $L = (0, 0, 8)$, and line L9 gives $0.1 + 0.9 \cdot 1 = 1$. The corner pixel $(1, 1)$ has the direction $(-\tfrac17, \tfrac17, -1)$, which meets the sphere farther from its center line, at a slant, and gets $0.23$. The border pixels miss.

The visible object, with # for the sphere, and the gray values of the $5 \times 5$ block of covered pixels:

| row | ids | gray values of columns 1 to 5 |
|---|---|---|
| 0 | `.......` | |
| 1 | `.#####.` | 0.23, 0.65, 0.74, 0.65, 0.23 |
| 2 | `.#####.` | 0.65, 0.88, 0.94, 0.88, 0.65 |
| 3 | `.#####.` | 0.74, 0.94, 1.00, 0.94, 0.74 |
| 4 | `.#####.` | 0.65, 0.88, 0.94, 0.88, 0.65 |
| 5 | `.#####.` | 0.23, 0.65, 0.74, 0.65, 0.23 |
| 6 | `.......` | |

With the light at the eye no visible point is in shadow. The tests of the implementation add a floor and a triangle between the floor and a light above it, and compare every pixel with the exact shadow test.

## Correctness

The invariant of the loop of line L4 is that after the objects $0, \ldots, k$ have been tested, best is the first of them with the smallest hit parameter in $(0, \infty)$, and tmax is that parameter, or best is NONE and tmax is $\infty$ if none of them is hit. So after the loop, best is the visible object of the pixel. Lines L6 to L9 then evaluate the shading formula of the problem, with the shadow decided by the any-hit query on the segment to the light. The full proof is in the proofs folder.

In floating point the visible object can differ from the exact one when two objects are hit at nearly the same $t$, and a ray through an edge of a mesh can miss it if the triangle test is not [watertight](/watertight-ray-triangle-intersection/). The shadow ray needs $\varepsilon$ larger than the error of $p$; otherwise the surface can shadow itself in speckles (shadow acne).

## Complexity

Each pixel casts one primary ray, which tests $n$ objects at line L4, and at most one shadow ray, which tests at most $n$ objects at line L8. Each test costs $O(1)$, so the time is $\Theta(P n)$ in every case for the linear scan, with $P$ primary rays and at most $P$ shadow rays. Beyond the output image, the algorithm keeps $O(1)$ values per pixel at a time.

An acceleration structure, such as a [bounding volume hierarchy](/bounding-volume-hierarchy/) traversed as in [BVH traversal](/bvh-traversal/), replaces the scan of line L4. The cost of a ray is then the number of nodes it visits plus the number of primitives it tests. That number is much smaller than $n$ on typical scenes, but a BVH ray query is still $O(n)$ in the worst case: the logarithmic behavior is observed on typical scenes, not proved. The surface area heuristic used to build such trees is a cost model, not a bound.

## Properties

- **Image order.** The outer loop runs over pixels, not objects, the opposite of the [z-buffer](/z-buffer/), so the cost per pixel depends on the scene only through the query.
- **Any primitive.** Every object with a ray intersection test can be rendered, including spheres, quadrics, implicit surfaces and solids built by set operations, without converting them to triangles.
- **Exact visibility at the sample.** At the pixel center the visible object is decided exactly, up to the precision of the tests; between samples nothing is known, which causes aliasing at edges.
- **Hard shadows.** A point light gives a shadow that is either full or empty.
- **Parallel.** Pixels are independent, so the image can be split among threads without communication.

## Variants and improvements

- **Antialiasing.** Several rays per pixel, averaged, smooth the edges; see [supersampling](/supersampling-antialiasing/).
- **Whitted ray tracing.** At the hit, also follow the reflected and refracted rays, recursively: [Whitted ray tracing](/whitted-ray-tracing/).
- **Distributed ray tracing.** Sample area lights, lenses and time with many rays for soft shadows, [depth of field](/depth-of-field/) and motion blur: [distributed ray tracing](/distributed-ray-tracing/).
- **Path tracing.** Follow random bounces to estimate the full [rendering equation](/rendering-equation/): [path tracing](/path-tracing/).
- **Volume ray casting.** Step along the ray through a volume of densities and accumulate color, as in medical imaging; the steps are a form of [ray marching](/ray-marching/).
- **Ray casting in 2D games.** Early 3D games cast one ray per screen column through a 2D grid map and drew a wall slice of height inversely proportional to the distance; this is a 2D [uniform grid](/uniform-grid/) traversal, not the 3D method here.
- **Hybrid rendering.** Rasterize the primary visibility with a z-buffer and cast only shadow or reflection rays.

## When to use it

Use ray casting for a first renderer, for scenes of exact primitives such as spheres and solids, for picking (which object is under the mouse is one primary ray), and for visibility queries in general. When the image needs mirror reflections and refractions, extend it to Whitted ray tracing; when it needs global illumination, use path tracing. For millions of triangles at interactive rates, either rasterize with a z-buffer or use an acceleration structure for the queries.

## Pitfalls

- **Taking the first hit, not the closest.** Returning the first object that the ray hits at line L4, in object order, shows objects behind others. Shrink tmax with each hit and keep the last best, as in line L4.
- **Shadow acne.** Casting the shadow ray at line L8 with the interval $(0, 1)$ lets the surface at $p$ hit itself at $t \approx 0$ through rounding, which speckles lit surfaces with shadow. Start at $\varepsilon > 0$, or offset $p$ along the normal.
- **Blockers behind the light.** Using the interval $(\varepsilon, \infty)$ at line L8 lets objects behind the light cast shadows. End the interval at the light, $1 - \varepsilon$ for the direction $L = \ell - p$.
- **The normal of a two-sided surface.** Using the stored normal without the flip of line L6 makes the back of a triangle black. Turn the normal toward the eye, or treat back faces as a separate material.
- **A light below the surface.** Without the test $n \cdot L \le 0$ at line L8, a surface lit from behind gets a negative cosine. Clamp to the ambient level.

## Implementations

## History

Arthur Appel described in 1968 how to render solids by casting a ray from the eye through each point of the picture plane, finding the first surface it meets, and casting a ray from that point to the light to decide whether it is in shadow; the images were drawn on the plotters of the time, not on a pixel display. Appel's [hidden-line algorithm](/appel-hidden-line-algorithm/) for line drawings is a different method. At MAGI in the early 1970s, rays were used to render solids built from simple shapes. Scott Roth's 1982 paper, Ray casting for modeling solids, gave the method its name and treated solids built by unions, intersections and differences. Turner Whitted had added recursive reflected and refracted rays in 1980, which is ray tracing in the narrower sense; ray casting now names the non-recursive version.

## References
