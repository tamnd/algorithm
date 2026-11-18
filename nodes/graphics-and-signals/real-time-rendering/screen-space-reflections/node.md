---
tag: 4JP2C2
kind: algorithm
slug: screen-space-reflections
name: Screen-space reflections
aliases:
- SSR
area: graphics-and-signals/real-time-rendering
level: advanced
summary: March the reflected ray through the depth buffer in screen space, perspective correct, and reuse the shaded color at the hit. Off-screen and hidden surfaces fall back to an environment map.
model: real-ram
complexity:
  vars: {p: the number of pixels that reflect, n: the number of steps per ray}
  time: {worst: O(p n)}
  space: {extra: O(p)}
properties: {deterministic: true, recursive: false, online: false, in_place: false}
history:
  year: 2014
  people: [Morgan McGuire, Michael Mara]
  note: McGuire and Mara published in 2014 a march that projects both ends of the ray and steps one pixel at a time with perspective-correct depth, which replaced marches with equal steps in 3D.
prereqs: [g-buffer, perspective-correct-interpolation, digital-differential-analyzer]
see_also: [environment-mapping, image-based-lighting, hierarchical-z-buffer, ray-marching, fresnel-equations, microfacet-brdf, temporal-antialiasing, screen-space-ambient-occlusion]
sources:
  - url: https://jcgt.org/published/0003/04/04/
    title: "Morgan McGuire and Michael Mara, Efficient GPU screen-space ray tracing, Journal of Computer Graphics Techniques 3(4), 73-85, 2014"
    locator: the projection of both ends of the ray, the linear interpolation of the reciprocal depth and of the point divided by depth, the step along the major axis, and the thickness test against the depth buffer
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 11, the part on screen-space reflections and their fallbacks
---

Screen-space reflections find the reflected color of a pixel with the pictures that the renderer already has. These are the depth buffer and the shaded image of the current frame. From the visible point, the method follows the reflected ray across the screen and compares the depth of the ray with the depth buffer at each pixel. If the ray goes behind a surface there, that pixel is the hit, and its shaded color is the reflection. The method can only see what is on the screen. A ray that leaves the screen, or that passes behind a surface with no hit, uses a fallback, usually an [environment map](/environment-mapping/). McGuire and Mara (2014) gave the march that most renderers use. It projects both ends of the ray and steps one pixel at a time, and it gets the depth correct for perspective.

## In plain words

A wet floor shows the room above it. To draw that, start at a floor pixel, bounce the view ray off the floor and follow the bounced ray. Do not follow it through the 3D scene. Follow its picture on the screen, from one pixel to the next. At each pixel, compare two depths: the depth of the ray at that point, and the depth stored in the depth buffer. When the ray goes a little behind what the camera sees there, the ray has hit that surface, so copy its color. When the ray leaves the picture, the screen has no answer, so take the color from a sky or room map.

## The problem

The input is the depth buffer $D$ and the shaded color of a frame, and the normals of the reflecting pixels, for example from a [G-buffer](/g-buffer/). The output is, for each reflecting pixel, the color seen along the mirror direction $r = w - 2 (w \cdot n)\, n$ of the view direction $w$. The depth buffer stores one surface per pixel, so the scene is unknown behind it. The method takes every pixel as a slab of the thickness $\tau$ behind its visible surface.

The camera looks along $-z$, and a point $p$ has the depth $d = -p_z$. The pixel $(i, j)$ has its center at $(i + \tfrac12, j + \tfrac12)$ with $j$ counted from the bottom. The view ray through the screen point $(s_x, s_y)$ has the slopes $u = (2 s_x / W - 1)\, a \tan\theta$ and $v = (2 s_y / H - 1) \tan\theta$, with the aspect ratio $a = W/H$. The visible point of a pixel is $d\,(u, v, -1)$.

## The algorithm

```pseudo id=main
TRACE(D, o, r, ℓ, τ)
L1  if the end o + ℓ r is nearer than the near plane:  shorten ℓ so that it is on it
L2  (x0, y0, k0) ← project(o);  (x1, y1, k1) ← project(o + ℓ r);  Q0 ← k0 o;  Q1 ← k1 (o + ℓ r)
L3  if |y1 - y0| > |x1 - x0|:  swap the roles of x and y
L4  each step: x ← x ± 1;  y, Q, k ← y + dy, Q + dQ, k + dk
L5      if (x, y) is off the screen:  return MISS
L6      if the depth range of the ray across this step overlaps [D(x, y), D(x, y) + τ]:  return the pixel and Q / k
L7      if x is past x1:  return MISS
L8  REFLECTION(q) = the color at TRACE(D, the point of q, r, ℓ, τ), or the environment in the direction r on a MISS
```

**Project once, step in 2D (lines L2 to L4).** Both ends of the ray are projected. The march then moves one pixel along the longer screen axis per step, and the other screen coordinate grows by a constant amount. The code does not step the depth. It steps $k = 1/d$ and $Q = p/d$, because these two are affine along the screen image of a 3D line, and the depth itself is not. So each step has the exact depth of the 3D point that projects there, and the point $Q/k$ is on the ray.

**The hit test (line L6).** The depth of the ray across a step runs from its value half a step back to its value half a step on. A hit is a range that reaches the stored depth $D$ and is not more than $\tau$ behind it. A small $\tau$ lets rays pass behind thin objects. A large $\tau$ makes thin objects into walls.

**The near plane (line L1).** A ray that points toward the camera would cross $d = 0$, where the projection breaks. The ray is cut at the near plane first.

**The fallback (line L8).** A ray that misses reads an environment map in the direction $r$. Renderers also fade the reflection near the edges of the screen and for rays that point toward the camera, so that the switch to the fallback is not seen. That fade is tuning.

## Example

The camera has $64 \times 48$ pixels, $\tan\theta = 0.5$ and the near plane at 0.1. The room has a floor at $y = -1$, a back wall at the depth 12 whose top edge is at $y = 3$, and a plate that faces the camera at the depth 6 for $-1.5 \le x \le 0$ and $-1 \le y \le 0.5$. The floor is a mirror with $n = (0, 1, 0)$, and $\tau = 0.3$.

| floor pixel | its depth | the code finds | the exact reflected ray |
|---|---|---|---|
| (20, 5) | 2.595 | the plate at (-1.4375, 0.3125, -6) | meets the plate at (-1.4375, 0.3125, -6) |
| (45, 8) | 3.097 | the wall at (3.375, 1.875, -12) | meets the wall at (3.375, 1.875, -12) |
| (28, 3) | 2.341 | no hit, so the environment | passes the wall plane at $y = 3.125$, above the top edge |

Of the 1232 floor pixels, 832 reflect the wall, 144 reflect the plate and 256 go to the environment. The points are exact to the rounding of the floating-point numbers, as the proof says. For the pixel (28, 3), screen space gets the correct answer for the wrong reason. The ray goes past the top of the wall, leaves the screen and falls back. If the room had a ceiling above the screen, the screen still could not show it.

## Correctness

The proofs folder has the proofs. For a 3D segment with the ends $o$ and $e$, put $\lambda = t\, d_e / d(t)$. Then $1/d = (1 - \lambda)/d_o + \lambda/d_e$ and $p/d = (1 - \lambda)\, o/d_o + \lambda\, e/d_e$. The screen coordinates are affine in $\lambda$ too. So $k$ and $Q$ are affine in the screen coordinate of the major axis, and constant increments give their exact values at every step. The depth is monotone along the step, so the range of a step is the range between its two half-step ends, and the steps follow one another with no gaps. The result is then the first visited pixel whose slab $[D, D + \tau]$ meets the ray. A miss means that the ray left the screen or reached its end first. The march tests one pixel per unit of the major axis, so it can be one pixel off from a march that tests every pixel the ray crosses. The tests check the identities at random points. They also compare 40 reflections with a fine 3D march: hit or miss agrees every time, and the hit pixels agree to within one pixel. That the hits are the scene's true reflections is not a theorem. It is true only where the slabs match the real objects and the reflected surface is on the screen.

## Complexity

The model is the real RAM. Each step costs $O(1)$, and a ray takes at most $\max(W, H) + 1$ steps before it leaves the screen, or fewer with a step limit or a short ray. So $p$ reflecting pixels with $n$ steps each cost $O(p n)$. The extra memory is the reflection image, $O(p)$. On a GPU the cost is the number of depth reads. Renderers lower $n$ with a stride of several pixels and a refinement near the hit, or with a [hierarchical Z-buffer](/hierarchical-z-buffer/) that skips empty regions.

## Properties

- **Perspective correct.** The depth along the march is exact, because $1/d$ and $p/d$ are affine in screen space.
- **One pixel per step.** The march takes no more than one step per pixel on the major axis, and it does not skip pixels on that axis.
- **Screen bound.** The march has only what is on the screen and in front. Off-screen and hidden surfaces give misses or wrong hits.
- **Thickness is a guess.** One depth layer does not say how thick an object is. The value $\tau$ is tuning.
- **Reuses the frame.** The reflected color is the color that was already shaded, with its lighting from the view of the camera.
- **No scene data.** The method needs no acceleration structure and no geometry, only the buffers of the frame.

## Variants and improvements

- **Stride and refinement.** Step several pixels at a time, and on a hit, search back by bisection. This makes fewer reads, but the method can now jump over thin objects.
- **Hierarchical tracing.** March a min-depth pyramid of the depth buffer, and move up a level where the ray is in front of the whole cell. This takes long steps over empty space.
- **Glossy reflections.** Sample several directions from a [microfacet BRDF](/microfacet-brdf/) per pixel, or blur the hit colors by the cone width. Then filter over time and space.
- **Back-face and thickness buffers.** Render the back faces to a second depth buffer. Then each pixel has a real thickness in place of a constant $\tau$.
- **Blend with other sources.** Fall back to local reflection probes or [image-based lighting](/image-based-lighting/), and weight the result with the [Fresnel equations](/fresnel-equations/).
- **Previous frame.** Read the hit color from the last frame, reprojected. This adds one bounce and avoids a second shading pass.

## When to use it

Use screen-space reflections for floors, water and other surfaces that reflect objects which are also on the screen, at a cost close to one depth march per pixel. It fits a deferred renderer, which has the depth and normals in buffers. Do not use it alone for mirrors that face the camera, because their reflected rays point back toward the camera, out of the screen. Do not use it alone where the reflected objects are off screen or hidden. Use ray traced reflections or planar reflection passes there, and keep an environment map as the fallback in any case.

## Pitfalls

- **Self-hits.** A ray that starts exactly on a flat surface overlaps the slab of the next pixel of the same surface. Move the origin a little off the surface, or skip the first steps.
- **Linear depth in screen space.** Interpolating $d$, not $1/d$, gives wrong depths that grow with the depth range of the ray.
- **No near-plane clip.** A ray toward the camera crosses $d = 0$, and its projection wraps around the screen.
- **A ray that projects to a point.** A ray along the view ray of its own pixel has no screen length. Treat it as a miss or give it a small screen length.
- **Edges of the screen.** Reflections stop abruptly where the rays leave the screen. Fade the result near the edges and near the camera direction.
- **Stretched hits.** Behind thin objects, a large $\tau$ gives streaks of the object's color, and a small one lets rays slip through gaps between steps.
- **Rough surfaces.** One mirror ray per pixel on a rough surface gives noise, and the denoiser must respect depth edges.

## Implementations

## History

Renderers marched the depth buffer for reflections before 2014, with equal steps along the ray in 3D or in screen space. McGuire and Mara (2014) published a march that projects both ends of the ray, interpolates $1/d$ and $p/d$ linearly along the screen line, and steps one pixel at a time on the major axis as in a line [digital differential analyzer](/digital-differential-analyzer/). Later work kept the screen-space march and added hierarchical depth pyramids, stochastic glossy rays with temporal filtering, and hybrid schemes that fall back to ray tracing for the rays that leave the screen.

## References
