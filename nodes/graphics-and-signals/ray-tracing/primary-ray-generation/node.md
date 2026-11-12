---
tag: NCFKVH
kind: algorithm
slug: primary-ray-generation
name: Primary ray generation
aliases:
- camera ray generation
- eye ray generation
area: graphics-and-signals/ray-tracing
level: intro
summary: Turn a pixel sample into a ray from the camera, through one center for a pinhole camera or from a point of the lens through the plane of focus for a thin lens.
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, s: the number of samples per pixel}
  time: {worst: Θ(W H s)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1968
  people: [Arthur Appel]
  note: Appel cast one ray from the eye through each point of the picture plane; sampling the pixel area and the lens came with distributed ray tracing in 1984.
prereqs: [pinhole-camera-model, viewport-transform]
see_also: [thin-lens-camera, ray-casting, closest-hit-query, depth-of-field, supersampling-antialiasing, stratified-sampling, ray-differentials, ray-coherence]
sources:
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 6.2.2 The Perspective Camera, and Section 6.2.3 The Thin Lens Model and Depth of Field
  - book: isbn:9781482229394
    title: Steve Marschner and Peter Shirley, Fundamentals of Computer Graphics, fourth edition, CRC Press, 2016
    locator: Chapter 4, Ray Tracing (computing viewing rays)
  - paper: doi:10.1145/800031.808590
    title: Robert L. Cook, Thomas Porter and Loren Carpenter, Distributed ray tracing, Computer Graphics (SIGGRAPH 84 Proceedings) 18(3), 1984, 137 to 145
    locator: the sections on antialiasing by pixel samples and on depth of field by lens samples
  - paper: doi:10.1145/1468075.1468082
    title: Arthur Appel, Some techniques for shading machine renderings of solids, AFIPS Spring Joint Computer Conference, vol. 32, 1968, 37 to 45
    locator: the rays from the eye through the picture plane
---

Primary ray generation turns a sample position in a pixel into the ray that a ray tracer follows into the scene. For a [pinhole camera](/pinhole-camera-model/), the ray starts at the eye and goes through the sample point on the image plane. For a [thin-lens camera](/thin-lens-camera/), it starts at a sampled point of the lens and goes through the point of the plane of focus that the pinhole ray would reach, so that points off that plane blur. The rays of one image are the input of [ray casting](/ray-casting/) and of every ray tracer that builds on it, each one asking for a [closest hit](/closest-hit-query/).

## In plain words

Put a window one unit in front of your eye, divide it into the pixels of the image, and draw a line from your eye through the center of each pixel. That line is the primary ray of the pixel. The width of the window sets the field of view: a wider window sees more of the scene.

A real camera has a lens, not a pinhole. Light from one point in focus goes through the whole lens and meets again in one point of the film. To get that blur, the ray of a pixel starts at a random point of the lens and aims at the point that is in focus for this pixel. Several such rays per pixel, averaged, give a blurred picture away from the focus distance.

## The problem

The input is a camera and a sample. The camera has an eye point $e$, an orthonormal basis $(u, v, w)$ in which $u$ points right, $v$ points up and the view direction is $-w$, an image of $W \times H$ square pixels, and the vertical field of view $\theta$. A thin lens adds a lens radius $R$ and a focus distance $z_f$. The sample is a pixel $(i, j)$ with column $i$ and row $j$, row 0 at the top, a position $(s_x, s_y) \in [0, 1)^2$ inside the pixel, and for a lens a point $(p_x, p_y)$ of the unit disk. The output is a ray $(o, d)$: an origin and a direction, which need not have unit length.

The image plane is at distance 1 in front of the eye, from $-\tan(\theta / 2)$ to $\tan(\theta / 2)$ in height and $W / H$ times as wide. The ray of the sample is the ray from the eye through the image point of the sample, for a pinhole camera.

## The algorithm

```pseudo id=main
PRIMARY-RAY(i, j, sx, sy, px, py)
L1  x ← (2 · (i + sx) − W) / H · tan(θ/2)
L2  y ← (H − 2 · (j + sy)) / H · tan(θ/2)
L3  d ← x · u + y · v − w                      ▷ through the image point, at distance 1
L4  if R = 0 then return (e, d)                ▷ a pinhole camera
L5  lx ← R · px;  ly ← R · py                  ▷ a point of the lens disk
L6  o ← e + lx · u + ly · v
L7  pf ← e + zf · d                            ▷ the pinhole ray at the depth zf
L8  return (o, pf − o)
```

Lines L1 and L2 are the [viewport transform](/viewport-transform/) run backward: they map the sample position from pixel coordinates to the image plane. In $x$, the pixel range $[0, W]$ becomes $[-\tfrac{W}{H} \tan(\theta/2), \tfrac{W}{H} \tan(\theta/2)]$, and in $y$ the range $[0, H]$ becomes $[\tan(\theta/2), -\tan(\theta/2)]$, flipped because row 0 is at the top. Dividing both by $H$ keeps the pixels square without a separate aspect ratio. Line L3 is the image point minus the eye, in world coordinates. With $s_x = s_y = \tfrac12$, the ray goes through the pixel center.

Lines L5 to L8 are the thin lens. The point $p_f$ of line L7 lies on the pinhole ray at depth $z_f$, because the $-w$ component of $d$ is 1. All rays of the pixel sample pass through $p_f$, whatever their lens point, so points at the depth $z_f$ are sharp and others blur. The lens point usually comes from an area-preserving map of the unit square onto the disk, such as the concentric map of Shirley and Chiu, applied to a uniform or a [stratified](/stratified-sampling/) sample.

**A frame.** A renderer runs PRIMARY-RAY for each pixel and each of $s$ samples per pixel, with $(s_x, s_y)$ and $(p_x, p_y)$ drawn at random or from a stratified pattern, and averages the radiance of the $s$ rays of a pixel. This is [supersampling](/supersampling-antialiasing/) over the pixel area and the lens.

## Example

A camera at $e = (0, 0, 0)$ with $u = (1, 0, 0)$, $v = (0, 1, 0)$, $w = (0, 0, 1)$, an image of $W = 4$ by $H = 3$ pixels, and $\theta = 90^\circ$, so $\tan(\theta/2) = 1$. The pixel centers have $s_x = s_y = \tfrac12$.

| pixel $(i, j)$ | L1: $x$ | L2: $y$ | L3: $d$ |
|---|---|---|---|
| $(0, 0)$, top left | $(1 - 4) / 3 = -1$ | $(3 - 1) / 3 = \tfrac23$ | $(-1, \tfrac23, -1)$ |
| $(1, 1)$ | $(3 - 4) / 3 = -\tfrac13$ | $(3 - 3) / 3 = 0$ | $(-\tfrac13, 0, -1)$ |
| $(3, 2)$, bottom right | $(7 - 4) / 3 = 1$ | $(3 - 5) / 3 = -\tfrac23$ | $(1, -\tfrac23, -1)$ |

The image plane spans $x \in [-\tfrac43, \tfrac43]$ and $y \in [-1, 1]$, and the pixel centers are $\tfrac23$ apart in both directions, so the pixels are square.

Now give the camera a thin lens with $R = 0.1$ and $z_f = 5$, and take the lens point $(p_x, p_y) = (1, 0)$ for pixel $(0, 0)$.

| line | value |
|---|---|
| L5 | $l_x = 0.1$, $l_y = 0$ |
| L6 | $o = (0.1, 0, 0)$ |
| L7 | $p_f = 5\,(-1, \tfrac23, -1) = (-5, \tfrac{10}{3}, -5)$ |
| L8 | $d = p_f - o = (-5.1, \tfrac{10}{3}, -5)$ |

Every lens point gives a ray of this pixel through $p_f$. A point at depth $z$ on the pinhole ray is reached by rays that are spread over a disk of diameter $2 R\,|z - z_f| / z_f$ around it, measured across the view direction; that is the blur. The tests of the implementation check both facts on random samples (seeds 1968 and 1981).

## Correctness

For a pinhole camera the claim is that the ray from $e$ in the direction $d$ passes through the image point of the sample, which is the point $e + x\,u + y\,v - w$ with the $x$ and $y$ of lines L1 and L2. That holds at $t = 1$ by line L3. For a thin lens, the claim is that the ray starts on the lens disk of radius $R$ centered at $e$ in the plane spanned by $u$ and $v$, and passes through $p_f$, the point at depth $z_f$ of the pinhole ray; both hold by lines L6 and L8, at $t = 0$ and $t = 1$. The full proof is in the proofs folder, which also shows that with $R = 0$ the lens rays are the pinhole rays.

## Complexity

Lines L1 to L3 cost a constant number of operations: about 6 multiplications and divisions for $x$ and $y$, and 9 more for the combination of the basis vectors. Lines L5 to L8 add about 12 more. So one ray costs $\Theta(1)$ time and $O(1)$ extra space, and a frame of $W \times H$ pixels with $s$ samples per pixel costs $\Theta(W H s)$ time. The rays can be produced one at a time, as the tracer asks for them, so the generator needs no storage for the frame. Per ray, this cost is small next to tracing the ray, which visits nodes of an acceleration structure and tests primitives.

## Properties

- **Exact with rational inputs.** Lines L1 to L8 use only additions, multiplications and divisions, so rational inputs give exact rays.
- **Linear in the sample.** The direction of line L3 is an affine function of $(i + s_x, j + s_y)$, so neighbor pixels have nearby rays; this is the [ray coherence](/ray-coherence/) that packet tracers use.
- **Pinhole as a limit.** With $R = 0$ the thin-lens ray is the pinhole ray.
- **Focus.** All rays of one pixel sample meet at $p_f$, and only there.
- **Not normalized.** The direction has length at least 1; intersection tests that assume a unit direction need it normalized.

## Variants and improvements

- **Orthographic camera.** All rays have the direction $-w$, and the origin moves over the image plane: $o = e + x\,u + y\,v$.
- **Other projections.** Fisheye, panoramic and environment cameras map the pixel to a direction by angles instead of a plane.
- **Pixel samples.** Jittered, stratified or low-discrepancy samples for $(s_x, s_y)$ give [antialiasing](/antialiasing/) with less noise than independent random samples.
- **Ray differentials.** A ray can carry its derivatives with respect to $i$ and $j$, so that texture lookups know the footprint of the pixel; see [ray differentials](/ray-differentials/).
- **Packets.** Generating the rays of a tile of pixels together gives coherent rays for [ray packet tracing](/ray-packet-tracing/).
- **Precomputation.** The terms $\tfrac{2}{H} \tan(\theta/2)\,u$ and $\tfrac{2}{H} \tan(\theta/2)\,v$ are steps of the direction per pixel, so a scan line of rays needs one addition per ray.

## When to use it

Every ray tracer and path tracer starts here, and the pinhole form is the default. Use the thin lens when the image needs [depth of field](/depth-of-field/); use several samples per pixel for antialiasing, motion blur and depth of field, as in [distributed ray tracing](/distributed-ray-tracing/). Use the orthographic form for technical drawings and for shadow maps of directional lights.

## Pitfalls

- **The pixel corner.** Writing `x ← (2 · i − W) / H · tan(θ/2)` at line L1 shoots through the corner of the pixel, and the image shifts by half a pixel. Add the sample position, $i + s_x$, with $s_x = \tfrac12$ for the center.
- **The vertical flip.** Writing `y ← (2 · (j + sy) − H) / H · tan(θ/2)` at line L2 turns the image upside down when row 0 is at the top. Use $H - 2\,(j + s_y)$.
- **The aspect ratio.** Dividing $x$ by $W$ and $y$ by $H$ at lines L1 and L2 stretches non-square images. Divide both by $H$, as above, when $\theta$ is the vertical field of view.
- **The degrees.** Passing $\theta$ in degrees to a tangent that expects radians gives a wrong field of view. Convert first.
- **The lens ray direction.** Using the pinhole direction $d$ from the lens point at line L8 gives parallel rays that do not focus anywhere. Aim at $p_f$: the direction is $p_f - o$.
- **The lens sample.** Taking $(p_x, p_y)$ uniform in the square and scaling to radius $R$ gives a square aperture. Map the square to the disk with an area-preserving map first.

## Implementations

## History

Arthur Appel cast rays from the eye through the picture plane in 1968 to decide visibility and shadows, which is the pinhole form. Turner Whitted (1980) used one ray per pixel and added adaptive subdivision of pixels for antialiasing. Robert Cook, Thomas Porter and Loren Carpenter (1984) distributed the samples of a pixel over the pixel area, the lens and the shutter time, which gave antialiasing, depth of field and motion blur with the same rays. Peter Shirley and Kenneth Chiu published the concentric map from the square to the disk in 1997, and later texts such as PBRT use it for lens samples.

## References
