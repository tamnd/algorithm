---
tag: K1P3D1
kind: algorithm
slug: shadow-volume-algorithm
name: Shadow volume algorithm
aliases:
- Crow's shadow volumes
- stencil shadow volumes
- z-pass and z-fail shadow volumes
area: graphics-and-signals/visibility
level: core
summary: Extrude each occluder's silhouette away from the light into a closed volume. Count how often each eye ray enters and leaves the volumes; a nonzero count means shadow.
solves: [shadow-determination]
model: real-ram
complexity:
  vars: {t: the number of occluder triangles, A: the number of pixels}
  time: {worst: O(t A), average: O(t A), best: Θ(t + A)}
  space: {extra: Θ(t + A)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1977
  people: [Franklin C. Crow]
  note: Crow defined the shadow volume of an object as the region behind it from the light, bounded by planes through the light and the silhouette edges. Heidmann in 1991 counted the crossings with the stencil buffer; the z-fail count came about 1999 to 2000.
prereqs: [silhouette-edge, back-face-culling, stencil-buffer, z-buffer]
see_also: [shadow-mapping, shadow-determination, stencil-buffer, silhouette-edge, back-face-culling, ray-casting, any-hit-query, hidden-surface-removal]
sources:
  - paper: doi:10.1145/563858.563901
    title: Franklin C. Crow, Shadow algorithms for computer graphics, Proceedings of SIGGRAPH 1977, Computer Graphics 11(2), pages 242 to 248
    locator: the whole paper (the shadow volume method)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, 2018
    locator: Chapter 7, Section 7.3 (Shadow Volumes), pages 230 to 234
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, 1990
    locator: Chapter 16, Section 16.4 (shadows, the shadow volume method)
---

The shadow volume algorithm decides, for each visible point of an image, whether a point light reaches it. For each occluder it builds a closed *shadow volume*: the region behind the occluder as seen from the light, bounded by the occluder's faces that face the light, by quads that extend its [silhouette edges](/silhouette-edge/) away from the light, and by a far cap. A point is in shadow exactly when it is inside some volume. The renderer finds this by counting, along each eye ray, how often the ray enters and leaves the volumes. Real-time renderers do the count in the [stencil buffer](/stencil-buffer/), one pixel at a time. There are two ways to count. *z-pass* counts the volume faces in front of the visible point and fails when the eye is in shadow. *z-fail* counts the faces behind it and is correct for each eye position. The method solves [shadow determination](/shadow-determination/) exactly, to the pixel, for point lights; [shadow mapping](/shadow-mapping/) is the common image-based alternative.

## In plain words

Hold a box under a lamp. Behind the box there is a dark region of space that grows wider away from the lamp. That region is the shadow volume. To build it, take the edges where the box turns from lit to unlit, and pull each edge straight away from the lamp into a long wall.

To decide whether a point on the floor is in shadow, walk from your eye to that point. Add one each time you go into a volume, and take one away each time you come out. If the count is not zero, the point is in shadow.

This walk must start outside all volumes. If your eye is in a shadow, the count is off by one. The z-fail trick walks from the point out to far away, which is surely outside all volumes. That count is right wherever the eye is.

## The problem

The light is a point $L$. The occluders are closed triangle meshes with outward normals, and $L$ is outside each of them. The eye is a point $C$, and each pixel holds the visible point $P$ that a [z-buffer](/z-buffer/) finds on its eye ray. The output, for each $P$, is whether $P$ is in shadow: whether the closed segment from $P$ to $L$ meets an occluder. The coordinates are real numbers; the implementation uses integers and exact fractions.

The implementation does the count by exact ray casting, not by rasterizing. For each visible point it intersects the segment or the ray from $C$ through $P$ with each triangle of each volume. This is the same count that the stencil buffer makes, with one sample per pixel. The proof assumes general position: no eye ray passes through an edge of a volume, and no $P$ is on a volume face.

## The algorithm

For a face $f$ with outward normal $n$ and a vertex $v_0$, $f$ *faces the light* when $n \cdot (L - v_0) > 0$; this is the [back-face test](/back-face-culling/) with the light in place of the eye. Let $v' = v + k (v - L)$ be the point $v$ moved away from the light by the factor $1 + k$. The constant $k$ is large enough that each visible point is nearer to $L$ than the far cap.

```pseudo id=main
SHADOW-VOLUMES(occluders, light L, eye C, visible points P[1 .. m], method)
L1  for each occluder O do
L2      classify each face of O: it faces L or it does not
L3      for each edge u → v of a face that faces L whose other face does not face L do
L4          add the quad (v, u, u′, v′)                          ▷ a side of the volume
        add the faces that face L (near cap) and the moved faces that do not (far cap)
L5  for each visible point P do
L6      count ← 0
L7      for each volume triangle that the line from C through P crosses, at parameter t do
L8          z-pass: if 0 < t < 1 then count ← count + 1 if the triangle faces C, else count − 1
L9          z-fail: if t > 1 then count ← count − 1 if the triangle faces C, else count + 1
L10     shadow[P] ← (count ≠ 0)
L11 return shadow
```

Lines L2 to L4 build each volume. The edges of line L3 are the silhouette edges of $O$ seen from the light. The near cap, the side quads and the far cap form a closed surface. Its faces are oriented consistently, with their normals pointing out of the volume. Lines L7 to L9 are what the stencil buffer does. A volume face that faces the eye is a front face, and the eye ray *enters* the volume there; at a back face it *leaves*. With z-pass, the faces that pass the depth test, in front of $P$, change the count. With z-fail, the faces that fail it, behind $P$, change the count with the opposite signs. The implementation decides crossings with signed volumes of the ray and each triangle edge, as in the [Plücker ray-triangle test](/plucker-ray-triangle-test/), and breaks a zero by the order of the two endpoints. So two triangles that share an edge never both count one crossing.

On a GPU, line L4 is done in a vertex shader or a geometry shader, and line L7 is a rasterization pass of the volumes with depth writes off and color writes off. The stencil operations are increment and decrement with wrap. A last pass draws the lit image where the stencil value is zero.

## Example

The occluder is the tetrahedron with vertices $(2, 2, 2)$, $(6, 2, 2)$, $(2, 6, 2)$, $(2, 2, 4)$, above the ground $z = 0$. The light is $L = (3, 3, 12)$. Only the slanted face, on the plane $x + y + 2z = 12$, faces the light: $3 + 3 + 24 = 30 > 12$. The base and the faces $x = 2$ and $y = 2$ face away. So the silhouette is the triangle of the slanted face. The volume has 1 near cap triangle, 3 side quads (6 triangles) and 3 far cap triangles. The eye is $C = (19, 13, 16)$, outside the shadow.

| ground point $P$ | ray to light | crossings of the eye line, $t$ and kind | z-pass | z-fail |
|---|---|---|---|---|
| $(1, 7, 0)$ | lit | none | 0 | 0 |
| $(3, 4, 0)$ | in shadow | enter at $\tfrac{134}{141}$, leave at $\tfrac{254}{231}$ | 1 | 1 |
| $(5, 4, 0)$ | lit | enter at $\tfrac{134}{131}$, leave at $\tfrac{254}{197}$ | 0 | 0 |
| $(9, 1, 0)$ | lit | none | 0 | 0 |

The point $(3, 4, 0)$ is behind the side wall at $t = \tfrac{134}{141} < 1$, so z-pass counts the entry. For z-fail, the exit at $t > 1$ is behind $P$ and counts $+1$. The point $(5, 4, 0)$ is in front of the volume: the eye line enters and leaves it only behind $P$, so both counts are 0.

Now put the eye at $C = (3, 4, 1)$, under the occluder and inside its shadow. For $P = (4, 3, 0)$, which is in shadow, the eye line meets the volume at $t = -\tfrac{21}{20}$, behind the eye, and leaves it at $t = \tfrac{39}{16}$, behind $P$. z-pass sees no face between $C$ and $P$ and gives 0, which says "lit"; z-fail counts the exit behind $P$ and gives 1. For $P = (9, 1, 0)$, which is lit, the eye leaves the volume at $t = \tfrac37$, in front of $P$: z-pass gives $-1$, which says "shadow", and z-fail gives 0. The tests check these numbers.

## Correctness

The volume $\Pi_O$ of a closed occluder mesh $O$ is a closed, consistently oriented surface. At a point $X$ nearer than the far cap, its winding number is the number of times the segment from $L$ to $X$ enters $O$; for a convex occluder, $\Pi_O$ is, on each ray from $L$ that meets $O$, the part from the entry point into $O$ to the far cap. So the winding number at $P$ is nonzero exactly when the segment from $P$ to $L$ meets $O$. Let $w(X)$ be the sum of the winding numbers of all the volumes at $X$. Along a segment in general position, each crossing of a volume face changes $w$ by $+1$ at a front face and by $-1$ at a back face. So the z-pass count is $w(P) - w(C)$, which equals $w(P)$ when the eye is lit. The z-fail count is $w(P) - w(\infty) = w(P)$, because the volumes are bounded. In both cases the count is nonzero exactly when $P$ is in shadow. The full proofs are below. The tests compare both counts with an exact segment-to-light test with fractions on random scenes of one to three tetrahedra. They also check that z-fail stays right, and z-pass goes wrong, when the eye is in shadow.

## Complexity

Building the volumes takes $\Theta(t)$ time for $t$ occluder triangles, with a table of edges. A volume has $O(t)$ triangles. In the stencil form, each volume triangle is rasterized, and the cost is the *fill*: the number of pixels covered by volume faces, summed over the faces. That is $O(tA)$ in the worst case, for $A$ pixels. Large volumes close to the eye cover the whole screen many times, and this fill is the main cost of the method in practice. The best case is $\Theta(t + A)$, when the volumes cover few pixels. The ray casting form of the implementation costs $O(t)$ per visible point. The extra space is the volume, $\Theta(t)$, and the stencil buffer, $\Theta(A)$.

## Properties

- **Exact per sample.** For a point light, the result at each visible point is the exact answer of the segment-to-light test, with no resolution or bias parameter. Compare [shadow mapping](/shadow-mapping/), which samples the depth from the light on a grid.
- **Hard shadows.** A point light gives sharp edges. Soft shadows need many lights or other methods.
- **Needs closed occluders.** The volume is closed only if each occluder mesh is closed. An open mesh gives a volume with holes, and the counts are wrong behind the holes.
- **Geometry dependent cost.** The cost grows with the silhouette and the screen area of the volumes, not with the light's view resolution.
- **Order independent.** The count is a sum, so the volume faces can be drawn in any order.

## Variants and improvements

- **Stencil buffer counting.** Heidmann in 1991 used the stencil buffer to count the front faces and the back faces of the volumes in front of the visible surface: the z-pass method.
- **z-fail.** Count the faces behind the visible surface, with the signs reversed, and close the volumes with the near and the far cap. The answer no longer depends on the eye. This was found by Bilodeau and Songy in 1999 and by Carmack in 2000, and it is often called *Carmack's reverse*. Everitt and Kilgard in 2002 described the robust form.
- **Infinite volumes.** Extrude the silhouette to points at infinity, with $w = 0$ in homogeneous coordinates, and use a projection with an infinite far plane. Then the far plane never cuts the volume, and the far cap of a point light is empty or degenerate.
- **Silhouette extraction.** Only the [silhouette edges](/silhouette-edge/) from the light need side quads. Find them on the CPU with a table of edges, or on the GPU with a geometry shader or by extruding the vertices of degenerate quads on each edge.
- **Two-sided stencil.** Modern hardware updates the stencil for front faces and back faces in one pass, with different operations.
- **Fill reduction.** Clip the volumes to the view frustum and to the receivers' bounds, or use only z-pass when the eye is surely lit.

## When to use it

Use shadow volumes when you need exact, sharp shadows from a few point lights. Examples are a scene with self-shadowing and no bias problems, or an engine where the occluders are closed, low-polygon meshes. Games of the early 2000s, for example Doom 3 (2004), used it for unified per-pixel lighting. Today [shadow mapping](/shadow-mapping/) is more common, because its cost does not depend on the silhouettes, it works for any geometry, and it filters to soft edges. For offline rendering, a ray to the light, as an [any-hit query](/any-hit-query/), is simpler.

## Pitfalls

- **z-pass with the eye in shadow.** If the eye is inside a volume, or the near clip plane cuts a volume, z-pass counts are off by one, and the shadow inverts in parts of the screen. The example shows both kinds of error. Use z-fail, or test that the eye is lit.
- **z-fail without caps.** z-fail needs both caps. Without the far cap, a ray from a point in shadow can leave the volume through the open end, with no crossing that counts, and the point is shown as lit. Without the near cap, the same thing happens at the occluder side. Use infinite extrusion so that the far plane never cuts the volume.
- **Open or broken meshes.** A hole or a non-manifold edge leaves the volume open. Then a ray can leave the volume without a crossing that counts, and the count is wrong behind the hole.
- **The lit faces of the occluder.** The faces that face the light lie on the boundary of their own volume, so the depth test at those pixels compares equal depths. Shade those faces with the lighting term $n \cdot (L - P) > 0$ alone, or offset the volume slightly.
- **Stencil overflow.** Many overlapping volumes can exceed the range of the stencil buffer. Use wrapping increment and decrement, so that only the value modulo $2^s$ matters.
- **Huge fill.** Long volumes of small, near objects cover the whole screen. Limit the extrusion distance or cull the volumes that do not reach visible receivers.

## Implementations

## History

Crow in 1977 described shadow volumes in his survey of shadow algorithms. The volume of an object is bounded by the planes through the light and the silhouette edges, and a point is in shadow when it is inside such a volume. He counted the volume faces along the eye ray in a scan-line renderer. Heidmann in 1991 showed how to do the count in the stencil buffer of graphics hardware: the z-pass method. Bilodeau and Songy in 1999, and Carmack independently in 2000, reversed the count to the faces behind the visible surface: the z-fail method. Everitt and Kilgard in 2002 combined z-fail with infinite extrusion and an infinite far plane into a robust method. Shadow volumes were then used for the unified lighting of several games of that period, before shadow maps became dominant.

## References
