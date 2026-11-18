---
tag: EGC7ET
kind: algorithm
slug: screen-space-ambient-occlusion
name: Screen-space ambient occlusion
aliases:
- SSAO
area: graphics-and-signals/real-time-rendering
level: core
summary: Estimate ambient occlusion per pixel by testing sample points around it against the depth buffer, then blur the noisy result.
model: real-ram
complexity:
  vars: {p: the number of pixels, s: the number of samples per pixel, r: the radius of the blur in pixels}
  time: {worst: O(p s + p r^2)}
  space: {extra: O(p + s)}
properties: {deterministic: true, recursive: false, online: false, in_place: false}
history:
  year: 2007
  people: [Martin Mittring, Perumalla Shanmugam, Okan Arikan]
  note: Mittring described the SSAO of CryEngine 2 in a SIGGRAPH course in 2007, with points in a sphere tested against the depth buffer. Shanmugam and Arikan published a GPU method of the same year that also works on the depth and normal buffers.
prereqs: [ambient-occlusion, g-buffer]
see_also: [horizon-based-ambient-occlusion, ground-truth-ambient-occlusion, monte-carlo-integration, bilateral-filter, temporal-antialiasing, stratified-sampling, deferred-shading, screen-space-reflections]
sources:
  - paper: doi:10.1145/1281500.1281671
    title: "Martin Mittring, Finding next gen: CryEngine 2, SIGGRAPH 2007 course Advanced Real-Time Rendering in 3D Graphics and Games"
    locator: the part on screen-space ambient occlusion, with sample points in a sphere tested against the depth buffer and a blur of the noise
  - paper: doi:10.1145/1230100.1230113
    title: "Perumalla Shanmugam and Okan Arikan, Hardware accelerated ambient occlusion techniques on GPUs, Symposium on Interactive 3D Graphics and Games 2007"
    locator: ambient occlusion computed from the depth and normal buffers of the visible surfaces
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 11.3, Ambient Occlusion (the part on screen-space methods)
---

Screen-space ambient occlusion estimates, for each pixel, how much of the space around the visible surface is filled by other surfaces, using only the depth buffer of the frame. For a pixel at the point $P$, it places a few sample points in a small sphere or hemisphere around $P$, projects each one to the screen, and compares its depth with the depth stored there. A sample behind the stored surface counts as occluded. The share of occluded samples darkens the ambient light of the pixel, so creases, corners and contact areas get darker. The result is noisy with few samples, so a blur follows. Mittring presented it for the game Crysis in 2007. It approximates [ambient occlusion](/ambient-occlusion/), but what it computes is a volume fraction of one depth layer, not the integral over directions, and how close it comes is a measurement, not a guarantee.

## In plain words

Corners and gaps get less light from the sky than open surfaces, and it helps to darken them. A ray tracer would shoot rays from each point to see how much of the sky is blocked. That is too slow for every frame. SSAO does something cheaper with the picture that the GPU has already made. Around each point, it throws a handful of small test points, and for each one it asks the depth buffer: is there a surface in front of this test point, as seen from the camera? If yes, the test point is probably inside something. Many test points inside means the point sits in a corner. The answer is noisy, so neighboring pixels are averaged.

## The problem

The input is a depth buffer $D$ of $p$ pixels with the view depth $d$ of the visible surface, and for the hemisphere form the normals, from a [G-buffer](/g-buffer/) or from differences of $D$. The output is a visibility $A \in [0, 1]$ per pixel, 1 for open and smaller in creases, to multiply into the ambient light. The reference is the ambient occlusion of the scene, but the depth buffer holds only the nearest surface per pixel, so anything hidden behind it, and anything outside the screen, is unknown.

This page and its code use an orthographic camera that looks along $-z$, so that the tests can use height fields with known answers. The pixel $(i, j)$ has its center at $(i + 1/2, j + 1/2)$ in view units, and its point is $P = (x, y, -d)$. In a perspective camera, $P = d\,(u, v, -1)$ with the slopes of the pixel, and a sample is projected with the camera matrix; the method is otherwise the same.

## The algorithm

The kernel is a list of $s$ offsets of length at most $R$. In the sphere form they fill a ball. In the hemisphere form they fill a half ball and are turned so that its axis is the normal $n$ of the pixel. The bias $\beta$ and the range function are tuning.

```pseudo id=main
SSAO(D, kernel, R, β)
L1  for each pixel q with depth d:  P ← the point of q
L2      n ← the normal at q                                ▷ hemisphere form only
L3      occ ← 0
L4      for each offset k of the kernel:  S ← P + k, or P + ROTATE(k, n) in the hemisphere form
L5          b ← the depth of D at the screen position of S;  dS ← the depth of S
L6          if b < dS - β then occ ← occ + RANGE(R, |d - b|)
L7      A[q] ← 1 - occ / s
L8  return BLUR(A)
```

**The test (lines L5 and L6).** The sample is occluded if the surface stored at its screen position is nearer to the camera than the sample. The bias $\beta$ removes self-occlusion from depth precision and from a coarse reconstruction of the surface.

**The range check (line L6).** A surface far in front of $P$, such as a near object in front of a far wall, also passes the test. The common fix multiplies the count by a falloff in the depth gap. The code uses $\operatorname{smoothstep}(0, 1, R / |d - b|)$, a form found in many engines. The falloff is tuning.

**The kernel and the noise.** A few samples per pixel give banding. Engines rotate the kernel per pixel with a small tile of random rotations, which turns the banding into high-frequency noise, and the blur of line L8 removes most of it. A [bilateral filter](/bilateral-filter/) that does not blur across depth edges is the usual choice. The code uses a box blur.

## Example

A frontal floor at depth 40 meets a block nearer to the camera by 30 units along a line at $x = 20$. The kernel has $s = 6000$ points in the half ball of radius $R = 6$ around the normal $(0, 0, 1)$, and the lookup is nearest. A point of the floor at the distance $\delta$ from the foot of the block has the expected occluded fraction $(R - \delta)^2 (2R + \delta) / (4 R^3)$, the share of a cap of the ball.

| $\delta$ | formula | measured $1 - A$ |
|---|---|---|
| 0.5 | 0.438 | 0.471 |
| 1.5 | 0.316 | 0.313 |
| 2.5 | 0.206 | 0.204 |
| 4.5 | 0.043 | 0.044 |
| 5.5 | 0.005 | 0.004 |

The row at $\delta = 0.5$ is off by more than the noise. Its normal comes from central differences that cross the edge, so it tilts, and the hemisphere leans into the block. The other rows agree within the sampling error of about 0.006.

With a sphere kernel in antithetic pairs $k, -k$ and the bilinear lookup, every plane gives $A = 1/2$ exactly: of each pair, one point is in front of the plane and one is behind it. So a flat open floor comes out as gray as a corner. With the hemisphere kernel, every plane gives $A = 1$.

## Correctness

SSAO is an estimator, so its correctness is a statement of what it estimates, and the proofs folder proves it. With independent uniform offsets in the half ball and no bias or range check, the expected value of $1 - A$ is the fraction of the volume of the half ball that lies behind the surface seen in the depth buffer, and its variance is at most $1/(4s)$. That volume fraction is a measure of how closed the neighborhood is. It is not the cosine-weighted integral of the [ambient occlusion](/ambient-occlusion/) page. The exact cases are planes: the sphere kernel gives $1/2$ on every plane, because the test of an offset $k$ is the sign of $m \cdot k$ for the plane normal $m$ and antithetic pairs split evenly; the hemisphere kernel gives 1 on every plane, because its offsets have $m \cdot k > 0$. The wall formula of the example is proved by a cap volume. The tests check all of these, the plane cases exactly.

## Complexity

The model is the real RAM. Each pixel takes $s$ samples with one depth lookup each, so the pass costs $O(p s)$. A box blur of radius $r$ costs $O(p r^2)$, or $O(p r)$ if it is separable. The kernel takes $O(s)$ memory and the result $O(p)$. At 1920 by 1080 pixels with 16 samples, this is about 33 million depth reads per frame. Engines often run SSAO at half resolution and upsample, which cuts this by 4.

The reads of the samples are scattered around each pixel, so their cost is mostly in the texture cache. A larger radius in pixels spreads the reads and lowers the hit rate.

## Properties

- **Screen space only.** The input is one depth layer. Surfaces hidden behind it and outside the screen do not occlude.
- **Depends on the view.** The same corner gets other values from other angles, because the depth buffer changes.
- **Volume, not angle.** The value is a share of volume, not of directions weighted by the cosine.
- **Bias toward gray.** The sphere form darkens open planes to $1/2$. The hemisphere form fixes this but needs normals.
- **Noise and blur.** Few samples need a rotation pattern and a blur, or temporal accumulation.
- **Cheap and local.** The cost per pixel is fixed and independent of the scene.

## Variants and improvements

- **Sphere kernel.** The original form needs no normals. Open surfaces come out half gray, and the image is usually rescaled.
- **Hemisphere kernel.** Turn the kernel to the normal, so that open planes get $A = 1$.
- **Range check.** A falloff in the depth gap removes halos around near objects.
- **Horizon-based methods.** March the depth buffer in a few directions and integrate the angle of the horizon, see [horizon-based ambient occlusion](/horizon-based-ambient-occlusion/). The [ground-truth ambient occlusion](/ground-truth-ambient-occlusion/) method integrates the cosine-weighted visibility of each slice in closed form.
- **Temporal accumulation.** Change the kernel each frame and blend with the reprojected result of earlier frames, as in [temporal antialiasing](/temporal-antialiasing/).
- **Multiple layers.** Render a second depth layer to see behind the first, at the cost of another pass.

## When to use it

Use SSAO for cheap contact darkening in real-time rendering when the frame has a depth buffer and the budget allows a few samples per pixel. It works best with a [deferred shading](/deferred-shading/) renderer that has normals in its G-buffer. When the look must be close to ray traced ambient occlusion, use a horizon-based method or ray tracing.

## Pitfalls

- **Halos.** Without a range check, a near object darkens the far wall behind it in a band around its silhouette.
- **Self-occlusion.** Without a bias, depth precision and a coarse lookup make flat surfaces look occluded in patterns.
- **Normals from depth at edges.** Differences across a depth edge tilt the normal, as the example shows. Use G-buffer normals, or one-sided differences that pick the smaller gap.
- **Radius in the wrong space.** The radius is a distance in the scene. In a perspective camera its size on the screen shrinks with depth, so far pixels sample a few pixels only.
- **Screen borders.** Samples that leave the screen read clamped or missing depths. Fade the effect near the borders, or render a guard band.
- **Gray planes.** The sphere kernel darkens open surfaces by half. Rescale or use the hemisphere form.

## Implementations

## History

Ambient occlusion and obscurance were defined for offline rendering in the late 1990s and early 2000s, where rays are traced from each point. In 2007 Mittring described the screen-space form used in CryEngine 2 for Crysis: points in a sphere around the pixel, tested against the depth buffer, with a blur. Shanmugam and Arikan published in the same year a GPU method that also worked from the buffers of the visible surfaces. Later engines turned the kernel to the normal to remove the gray of open surfaces, added range checks, and replaced the random points by horizon searches, which led to horizon-based ambient occlusion in 2008 and ground-truth ambient occlusion in 2016.

## References
