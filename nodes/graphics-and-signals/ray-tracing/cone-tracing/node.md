---
tag: 7SNYXJ
kind: algorithm
slug: cone-tracing
name: Cone tracing
area: graphics-and-signals/ray-tracing
level: advanced
summary: Trace a cone instead of a ray. Test each object against the cone, compute the fraction of the cone that it blocks, and mix the nearest objects by that coverage.
solves: [antialiasing]
model: real-ram
complexity:
  vars: {n: "the number of objects tested by one cone"}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: O(1)}
properties: {deterministic: true, exact: false, recursive: false, one-cone-per-pixel: true}
history:
  year: 1984
  people: [John Amanatides]
  note: Amanatides extended the ray with a spread angle and a virtual origin, computed the fractional coverage of spheres, planes and polygons in the cone, and used it for antialiasing, fuzzy shadows, dull reflections and the level of detail.
prereqs: [ray-casting, ray-sphere-intersection, antialiasing]
see_also: [beam-tracing, ray-differentials, supersampling-antialiasing, distributed-ray-tracing, porter-duff-compositing, a-buffer, mipmap, warnock-algorithm]
sources:
  - paper: doi:10.1145/964965.808589
    title: John Amanatides, Ray tracing with cones, Computer Graphics 18(3) (SIGGRAPH 84), 1984, pages 129 to 135
    locator: the sections An Approximation, Cones (spread angle, virtual origin, the list of the eight closest objects), Intersection Calculations (the test D = T tan A + R/cos A, the circle intersections for spheres, planes and polygons), and the sections on fuzzy shadows, dull reflections and reducing intersection calculations
  - paper: doi:10.1145/800031.808588
    title: Paul S. Heckbert and Pat Hanrahan, Beam tracing polygonal objects, Computer Graphics 18(3) (SIGGRAPH 84), 1984, pages 119 to 127
    locator: the exact alternative with polygonal beams, published in the same proceedings
  - paper: doi:10.1111/j.1467-8659.2011.02063.x
    title: Cyril Crassin, Fabrice Neyret, Miguel Sainz, Simon Green and Elmar Eisemann, Interactive indirect illumination using voxel cone tracing, Computer Graphics Forum 30(7), 2011, pages 1921 to 1930
    locator: the modern use of cones, sampled along their axis in a prefiltered voxel octree for indirect light
---

Cone tracing replaces each ray of a ray tracer by a cone: an apex, an axis and a spread angle $A$, the angle between the axis and the boundary. For a primary ray the spread angle is chosen so that the cone's radius at the virtual screen is one pixel width. Each object first gets a fast in or out test against the cone. If the cone meets the object, the tracer computes the *fractional coverage*: the part of the cone's circular cross-section that the object blocks. For a sphere this is the area of intersection of two circles, and for a plane it is the area of a circle on one side of a line. The tracer keeps a list of the eight nearest objects with nonzero coverage and mixes their colors front to back with these fractions, so that a pixel on an edge gets a blend of the two sides from one cone. John Amanatides introduced the method in 1984. With wider cones, the same idea gives fuzzy shadows from spherical lights, dull reflections and the level of detail for textures, each at the cost of one cone instead of many rays.

## In plain words

A ray tracer usually sends one thin line of sight through the middle of each pixel. If an object's edge crosses the pixel, the line either hits the object or misses it, and the edge looks jagged.

Cone tracing makes the line of sight thick. It sends a cone that is as wide as the pixel. When the cone touches an object, the tracer computes how much of the cone's round cross-section the object hides, for example 62 percent. It then mixes the object's color and the color behind it in that ratio. One cone per pixel gives smooth edges.

A wider cone sees a wider part of the world at once. A shadow cone as wide as a lamp sees how much of the lamp is hidden and gives a soft shadow edge.

## The problem

Given a scene of spheres and planes (and, by extension, polygons), a cone with apex $O$, unit axis $D$ and spread angle $A$ with $0 < A < 90°$, and a color for each object, compute an approximation of the average color of the rays of the cone. The average is over the rays uniformly distributed in a cross-section of the cone perpendicular to its axis, which is the same at every depth, because the cross-sections are scaled copies of each other. This is [antialiasing](/antialiasing/) by an area estimate instead of by many samples.

## The algorithm

```pseudo id=main
TRACE-CONE(apex O, unit axis D, spread angle A, scene)
L1  list ← empty; compute tan A, cos A and sin A once
L2  for each object X of the scene:
L3      if the fast test shows that the cone misses X then skip X
L4      (f, t) ← the fractional coverage and the depth of X in the cone
L5      if f > 0 then insert (t, f, X) into list by depth, and keep only the 8 nearest
L6  color ← 0; left ← 1
L7  for each (t, f, X) in list, nearest first:
L8      color ← color + left · f · SHADE(X, t)
L9      left ← left · (1 − f)
L10 return color + left · background
```

**Spheres.** Let $CP$ be the point of the axis nearest to the center $C$, $T = (C - O) \cdot D$ its distance from the apex, and $SEP = \lVert C - CP\rVert$. A ray tracer already computes $T$ and $SEP$ for the ray-sphere test of [ray-sphere intersection](/ray-sphere-intersection/), and rejects the sphere if $SEP \ge R$. The cone test of line L3 rejects it if

$$SEP \ge T \tan A + \frac{R}{\cos A}.$$

The trigonometric values depend only on $A$, so the test costs a few more operations than the ray test. For the coverage of line L4, the plane through $C$ perpendicular to the axis cuts the cone in a disk of radius $r_c = T \tan A$ around $CP$ and the sphere in its great circle, a disk of radius $R$ around $C$. The coverage is the area of the lens of the two disks, divided by $\pi r_c^2$:

$$\text{lens}(r_1, r_2, s) = r_1^2 \arccos\frac{s^2 + r_1^2 - r_2^2}{2 s r_1} + r_2^2 \arccos\frac{s^2 + r_2^2 - r_1^2}{2 s r_2} - \tfrac12 \sqrt{(-s + r_1 + r_2)(s + r_1 - r_2)(s - r_1 + r_2)(s + r_1 + r_2)}$$

for $|r_1 - r_2| < s < r_1 + r_2$, with $0$ beyond and $\pi \min(r_1, r_2)^2$ for nested disks. The depth is the distance to the front of the sphere along the axis, or $T$ if the axis misses.

**Planes.** Put the cross-section at distance 1 from the apex, so that the cone's disk has radius $\tan A$. A ray $D + u$ hits a plane with normal $n$ (on the apex's side) when $(D + u) \cdot n < 0$, and in the cross-section this is a half-plane bounded by a line at signed distance $-(D \cdot n)/\sin\theta$ from the center, where $\theta$ is the angle between $D$ and $n$. The coverage is the fraction of the disk on the hit side:

$$f(h) = \frac{1}{\pi}\Bigl(\arcsin h + h\sqrt{1 - h^2} + \frac{\pi}{2}\Bigr), \qquad h = \frac{-(D \cdot n)}{\sin\theta \tan A},$$

clamped to $0$ for $h \le -1$ and $1$ for $h \ge 1$. So the fast test is the comparison of the angle $\theta$ with the spread angle. The depth is the distance to the plane along the axis, or infinity if the axis points above the horizon.

**Polygons.** Amanatides projects the vertices onto a plane perpendicular to the axis, where the cone's section is a circle, and estimates the coverage from the distances of the circle's center to the edges with the circle and half-plane formula.

**Mixing.** Lines L6 to L10 mix front to back: each object gets the fraction $f$ of what the nearer objects left uncovered. The paper says only that the next object in the list contributes if the nearest one does not fill the cone, and that only the coverage values are used in the mixing. The product form of line L9 is the choice of this implementation. It is the "over" operator of [Porter-Duff compositing](/porter-duff-compositing/) with coverage as alpha.

**Reflection and refraction.** The new axis is the reflected or refracted axis. The new spread angle and virtual origin come from the curvature of the surface at the hit, which the paper takes as constant over the footprint, with the optics of spherical mirrors and lenses without the paraxial approximation. A flat mirror keeps the spread angle and moves the virtual origin to the mirror image of the apex.

## Example

**A silhouette.** The eye is at the origin, the virtual screen at distance 1, the pixel width $w = 0.02$, so the spread angle of a pixel cone is about $\arctan 0.02$. A sphere of radius 2 at $(0, 0, 10)$ has its silhouette at screen coordinate $x = \tan(\arcsin 0.2) \approx 0.2041$. Along the row $y = 0$:

| pixel center $x$ | one ray through the center | cone coverage | fast test |
|---|---|---|---|
| 0.16 | hit | 1 | meets |
| 0.18 | hit | 1 | meets |
| 0.20 | hit | 0.618 | meets |
| 0.22 | miss | 0.058 | meets |
| 0.24 | miss | 0 | misses |

A single ray gives a hard step from 1 to 0 between $x = 0.20$ and $x = 0.22$. The cone gives a ramp over two pixels, because its radius is one pixel width, so its footprint is two pixels wide. For the two partial pixels, supersampling the cone with $300 \times 300$ rays gives $0.6179$ and $0.0582$.

**A sphere in front of the floor.** A cone with spread $5°$ has the axis $(0, -0.15, 1)$. A white sphere (color 1) of radius 0.5 at $(0.3, -1.2, 8)$ has $T = 8.09$ and $SEP = 0.3$, so the cone's section there has radius $0.708$ and the sphere covers $f = 0.462$ of it, at depth $7.69$. The gray floor $y = -3$ (color 0.25) covers the whole cone at depth $20.2$. Lines L6 to L10 give $0.462 \cdot 1 + 0.538 \cdot 0.25 = 0.597$. Supersampling with $300 \times 300$ rays gives $0.5974$.

**Abutting objects.** Two white spheres of radius 0.8 at $(\pm 1, 0, 10)$ lie side by side inside the section of radius 2 of a cone along the $z$ axis with $\tan A = 0.2$. Each covers $0.64/4 = 0.16$, and their disks do not overlap, so together they cover $0.32$. The mixing of line L9 assumes that the second sphere covers 16 percent of what the first left uncovered and gives $0.16 + 0.84 \cdot 0.16 = 0.2944$. The paper notes this limitation: overlapping surfaces are mixed correctly, abutting surfaces are not.

The tests check the fast test against a dense sampling of the cone's boundary and against rays of the cone, the lens and half-plane formulas against grid sampling, the sphere coverage against the rays that hit, the three examples above, and the list of the eight nearest.

## Correctness

The fast test is exact. By rotational symmetry about the axis, the distance from $C$ to the solid cone is a distance in the half-plane through the axis and $C$, where the cone is the wedge $\{(x, y) : x \ge 0, |y| \le x \tan A\}$ and $C$ is the point $(T, SEP)$. If $T \cos A + SEP \sin A \ge 0$, which holds whenever $T \ge 0$, the nearest point of the wedge's boundary is on its edge line, at distance $SEP \cos A - T \sin A$, and this is less than $R$ exactly when $SEP < T \tan A + R/\cos A$. Otherwise the nearest point is the apex, and the implementation compares $T^2 + SEP^2$ with $R^2$.

The coverage formulas are the exact areas of a lens and of a circular segment. For a plane the coverage is exact: it is the fraction of rays of the cone that hit the plane. For a sphere it is a lower bound: every point of the great circle's disk in the section is hit by the ray of the cone through it, but rays near the silhouette can hit the sphere in front of that plane and miss the disk. The mixing weights $f_i \prod_{j < i} (1 - f_j)$ and the background weight $\prod_j (1 - f_j)$ are nonnegative and sum to 1, so the color is a convex combination of the object colors and the background. It is the exact average when each object's covered region is independent of the union of the nearer ones, which holds in particular when a nearer region is nested in a farther one, as in the floor example. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

One cone makes the fast test for each of the $n$ objects, $\Theta(n)$ in total, plus the coverage for the objects that pass. The list has at most 8 entries, so each insertion and the mixing take constant time, and the extra space is $O(1)$. A ray costs $\Theta(n)$ in the same scene without an acceleration structure, so a cone costs a constant factor more than one ray, while [supersampling](/supersampling-antialiasing/) with $k$ rays per pixel costs $\Theta(k n)$. Acceleration structures need the cone version of their bounding volume tests, and a wide cone passes more of them than a ray does.

## Properties

- **One cone per pixel.** The edge of every object gets a coverage value, and nothing small can fall between the samples, because the cones of neighboring pixels overlap.
- **Approximate.** The coverage is an area estimate. The sphere coverage is a lower bound, the polygon coverage is estimated edge by edge, and the mixing is exact only when the covered regions are independent.
- **Abutting surfaces.** Two objects that share an edge in the cone are mixed as if they overlapped, which lets the background show through the seam.
- **A filter of fixed shape.** The coverage weights the cross-section uniformly, a box filter on a disk of radius one pixel width.
- **Footprint for free.** The cone's radius at a hit gives the size of the footprint, which selects the level of a [mipmap](/mipmap/) or the level of detail of a procedural model.
- **Paper's approximations.** Amanatides evaluates the lens and segment areas with polynomial approximations. The implementation uses the exact formulas.

## Variants and improvements

- **Fuzzy shadows.** The shadow ray toward a spherical light is broadened to the size of the light, and the coverage of the blockers estimates how much of the light is hidden. This gives penumbras from one cone. The paper notes that the shadows of transparent objects are still wrong.
- **Dull reflections and translucency.** A reflected or transmitted cone with a larger spread averages a larger part of the scene, which gives blurred reflections with one cone instead of many rays, as in [distributed ray tracing](/distributed-ray-tracing/).
- **Culling by subdivision.** Firing cones of decreasing size at the screen and testing objects against the larger cones first is a [Warnock](/warnock-algorithm/) style subdivision. Amanatides reports an order of magnitude fewer intersection calculations on a test scene of six spheres; this is a measurement, not a bound.
- **Beam tracing.** [Beam tracing](/beam-tracing/) uses pyramids with polygonal cross-sections and computes exact visible fragments, for polygons and flat mirrors only.
- **Ray differentials.** [Ray differentials](/ray-differentials/) track a first-order parallelogram footprint instead of a circle, and see the stretching of grazing views and the effect of curvature in two directions.
- **Ray cones in real-time ray tracers.** GPU ray tracers keep a cone width and spread angle per ray only to choose texture levels, without coverage.
- **Voxel cone tracing.** Crassin et al. (2011) march cones through a prefiltered voxel octree and accumulate its values front to back, with the radius of the cone choosing the level of the octree, for indirect light and ambient occlusion in real time.

## When to use it

Use cone tracing when one sample per pixel must give smooth edges, soft shadows or blurred reflections, and the scene is made of objects with simple cone tests, such as spheres, planes and polygons. Use it for its footprint alone, to choose texture or geometry levels, in any ray tracer. Prefer [supersampling](/supersampling-antialiasing/) or stochastic sampling when the scene has many abutting surfaces, complex objects without a cone test, or when an unbiased average is needed, because the coverage estimates do not converge to the exact pixel value. Prefer [beam tracing](/beam-tracing/) for exact visibility in polygonal scenes with flat mirrors.

## Pitfalls

- **Abutting surfaces.** Product mixing lets the background show through the seam between two objects that share an edge, as in the third example. The paper suggests using more of the information in the sorted list to fix this. Coverage masks, as in the [A-buffer](/a-buffer/), solve it.
- **A cone radius of one pixel width.** The paper chooses the spread so that the radius, not the diameter, is one pixel width. The footprint then covers neighbor pixels and the image is slightly blurred. A radius of half a pixel width gives a sharper image with less antialiasing.
- **The representative point.** When the cone covers a plane only near the horizon, the point of the plane nearest the axis is at infinity, and shading it with distance attenuation gives black. Choose the sample point inside the covered part.
- **Specular highlights.** A highlight that varies strongly inside the cone aliases even with correct coverage. The paper suggests clamping the Phong exponent where the normal varies a lot in the footprint.
- **A full list.** If more than eight objects with nonzero coverage meet the cone, the farthest are dropped, and their weight goes to the background.
- **Spheres behind or around the apex.** The coverage formula needs $T > 0$. Objects behind the apex, or a sphere that contains it, need a separate rule.
- **Wide cones near silhouettes.** The great circle used for the sphere coverage is smaller in the view than the silhouette. For small spread angles the difference is negligible, as in the examples, but for wide shadow or reflection cones it underestimates the coverage.

## Implementations

## History

Whitted's ray tracer of 1980 had considered widening rays but gave up because of the intersection calculations, as Amanatides reports. In 1984 two papers in the same SIGGRAPH proceedings replaced the ray by a volume: Heckbert and Hanrahan used pyramids with polygonal sections in [beam tracing](/beam-tracing/), and Amanatides used circular cones. Amanatides defined the cone by a spread angle and a virtual origin, gave intersection and coverage calculations for spheres, planes and polygons, and applied cones to antialiasing, level of detail, texture filtering, fuzzy shadows, dull reflections and a Warnock style culling. Igehy's ray differentials of 1999 replaced the circular footprint by a first-order one. From 2011 on, voxel cone tracing by Crassin and others brought cones to real-time indirect illumination.

## References
