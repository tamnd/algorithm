---
tag: 7TY98V
kind: algorithm
slug: horizon-based-ambient-occlusion
name: Horizon-based ambient occlusion
aliases:
- HBAO
area: graphics-and-signals/real-time-rendering
level: advanced
summary: March the depth buffer in several screen directions to find the horizon angle in each, and integrate the visible part of the hemisphere.
model: real-ram
complexity:
  vars: {p: the number of pixels, m: the number of directions per pixel, s: the number of steps per direction}
  time: {worst: O(p m s)}
  space: {extra: O(p)}
properties: {deterministic: true, recursive: false, online: false, in_place: false}
history:
  year: 2008
  people: [Louis Bavoil, Miguel Sainz, Rouslan Dimitrov]
  note: Bavoil, Sainz and Dimitrov presented image-space horizon-based ambient occlusion at SIGGRAPH 2008, with the integral of the sine of the horizon angle over screen directions.
prereqs: [screen-space-ambient-occlusion, ambient-occlusion]
see_also: [ground-truth-ambient-occlusion, ray-marching, digital-differential-analyzer, bilateral-filter, g-buffer, monte-carlo-integration, deferred-shading, screen-space-reflections]
sources:
  - paper: doi:10.1145/1401032.1401061
    title: "Louis Bavoil, Miguel Sainz and Rouslan Dimitrov, Image-space horizon-based ambient occlusion, SIGGRAPH 2008 talks"
    locator: Equation 3, the integral of (sin h - sin t) W over the screen directions, and the march in screen space with an attenuation per step
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 11.3, Ambient Occlusion (the part on horizon-based methods)
  - paper: doi:10.1145/1281500.1281671
    title: "Martin Mittring, Finding next gen: CryEngine 2, SIGGRAPH 2007 course Advanced Real-Time Rendering in 3D Graphics and Games"
    locator: the screen-space ambient occlusion with point samples that horizon-based methods replace
---

Horizon-based ambient occlusion is a screen-space method that treats the depth buffer as a height field seen from the camera. For each pixel, it picks a few directions in the screen and marches along each one, reading the depth buffer at each step. In each direction it keeps the highest elevation angle of the surface seen from the pixel, the horizon, and it assumes that everything below the horizon is blocked. The blocked part of a direction is the sine of the horizon angle minus the sine of the tangent angle of the surface, and the mean over the directions is the occlusion. Bavoil, Sainz and Dimitrov presented it in 2008. It replaces the random points of [SSAO](/screen-space-ambient-occlusion/) by a search along lines, and with no falloff it measures the blocked solid angle exactly, for what the depth buffer shows.

## In plain words

Stand in a field next to a wall and look in all directions. The wall hides part of the sky. In each direction, the sky starts above the top of the wall, at some angle above the ground: the horizon. HBAO does this for every pixel of the depth buffer. It walks away from the pixel along a few lines on the screen, looks at how high the surface rises along each line, and remembers the highest angle. A high horizon in many directions means a deep crease. The occluded part of each direction follows from the horizon angle by a simple formula, so a few directions with a few steps each give a smooth answer.

## The problem

The input is a depth buffer $D$ of $p$ pixels with the view depth of the visible surface, and the normals, from a [G-buffer](/g-buffer/) or from differences of $D$. The output is the visibility $A \in [0, 1]$ per pixel, 1 for open, to darken the ambient light. The integral that HBAO approximates is, in the paper's form,

$$A = 1 - \frac{1}{2\pi} \int_{-\pi}^{\pi} \int_{t(\theta)}^{h(\theta)} W(\omega) \cos\alpha \, d\alpha \, d\theta = 1 - \frac{1}{2\pi} \int_{-\pi}^{\pi} \big(\sin h(\theta) - \sin t(\theta)\big) W(\theta) \, d\theta,$$

where $\theta$ is the screen direction, $\alpha$ the elevation above the view plane, $t(\theta)$ the elevation of the tangent plane and $h(\theta)$ the elevation of the horizon. The second form is for a falloff $W$ that depends only on $\theta$.

This page and its code use an orthographic camera that looks along $-z$, so that the view vector is $(0, 0, 1)$ everywhere and the tests can use height fields. In a perspective camera, the method reconstructs the view-space point of each step from its depth and the slopes of the pixel, $P = d\,(u, v, -1)$, and measures the angles from the view-space vectors.

## The algorithm

$m$ directions with a per-pixel offset $\xi$, $s$ steps of length $\ell$ per direction, a radius $R$ and a falloff $W$. The code uses $W(r) = 1 - r^2 / R^2$, which is tuning.

```pseudo id=main
HBAO(D, q, n, m, s, ℓ, R, W, ξ)
L1  occ ← 0;  P ← the point of q
L2  for k ← 0 to m - 1:  θ ← 2π (k + ξ) / m;  c ← (cos θ, sin θ)
L3      h ← t ← the elevation of the tangent plane of n in the direction c
L4      for i ← 1 to s:  S ← the point of D at the screen position of P plus i ℓ c
L5          r ← |S - P|;  if r > R then skip this step
L6          α ← the elevation of S - P above the view plane
L7          if α > h then occ ← occ + W(r) (sin α - sin h);  h ← α
L8  return A ← 1 - occ / m
```

**The tangent (line L3).** With the normal $n$, the tangent plane rises in the direction $c$ by $\tan t = -(n_x c_x + n_y c_y) / n_z$. Starting the horizon at $t$ ignores everything below the tangent plane, which cannot occlude the pixel.

**The march (lines L4 to L7).** Each step reads one depth. If its elevation is above the current horizon, the increase of the sine is added, weighted by the falloff at that distance, and the horizon moves up. With $W \equiv 1$ the sum of a direction is $\sin h - \sin t$ for the highest horizon $h$. With a falloff, near occluders count fully and far ones less, which hides the cut at the radius $R$.

**Noise and blur.** The offset $\xi$ and the step offsets are random per pixel, from a small tile of values, and a [bilateral filter](/bilateral-filter/) removes the noise. The paper also adds a small angle bias to the tangent to hide the facets of a coarse mesh; this is tuning.

## Example

A frontal floor meets a block that rises by $H = 8$ units toward the camera along a straight line. A point of the floor at the distance $\delta$ from the foot of the block, with $W \equiv 1$ and no radius, has the exact value $A = 1 - \arctan(H / \delta) / \pi$ (proved in the proofs folder). The march uses steps of 0.25 units.

| $\delta$ | exact | $m = 64$, no radius | $m = 8$, no radius | $m = 64$, $R = 16$ | $m = 64$, $R = 16$, falloff |
|---|---|---|---|---|---|
| 2.5 | 0.596 | 0.599 | 0.573 | 0.617 | 0.743 |
| 4.5 | 0.663 | 0.669 | 0.649 | 0.689 | 0.824 |
| 8.5 | 0.760 | 0.763 | 0.752 | 0.824 | 0.937 |

With 64 directions the code is within 0.006 of the exact value; the rest is the step length, which misses the edge of the block by up to one step. With 8 directions the rectangle rule is coarser. A radius of 16 cuts off the far part of the block and opens the point, and the falloff opens it more. The last two columns are not errors of the method but choices of the look, and the cut of a radius is tuning.

## Correctness

The proofs are in the proofs folder. Write a direction as an azimuth $\theta$ in the screen plane and an elevation $\alpha$ above the view plane, so that the element of solid angle is $\cos\alpha \, d\alpha \, d\theta$. A direction is above the tangent plane exactly when $\alpha > t(\theta)$, so the hemisphere of the normal is the set above the tangent angles, with the solid angle $2\pi$. If the depth buffer is read as a height field, the blocked directions are those between $t(\theta)$ and $h(\theta)$, and their solid angle is $\int (\sin h - \sin t)\, d\theta$. So with $W \equiv 1$, $1 - A$ is the blocked share of the solid angle, and the code is the rectangle rule for it with the inner sums telescoping to $\sin h - \sin t$. Three more statements are proved and tested: a plane gives $A = 1$ for any falloff, the wall gives $\arctan(H/\delta)/\pi$, and a falloff between 0 and 1 can only raise $A$, which stays in $[0, 1]$ for an even number of directions. The value is not cosine-weighted, so it is not the [ambient occlusion](/ambient-occlusion/) integral, and it is right only for the one layer of the depth buffer.

## Complexity

The model is the real RAM. Each pixel does $m$ directions of $s$ steps with one depth lookup each: $O(p m s)$ in total, with $O(p)$ memory for the result. With 8 directions of 6 steps at 1920 by 1080 pixels, this is about 100 million lookups per frame, which is why HBAO is often run at half resolution and upsampled. The lookups along a line are close to each other in the texture, so they cache better than the scattered points of SSAO.

## Properties

- **Solid angle.** With no falloff it measures the blocked share of the solid angle above the tangent plane.
- **Height field.** The depth buffer is read as a surface of infinite thickness: everything below the horizon counts as blocked.
- **Open planes.** A plane is fully open, unlike the sphere form of SSAO.
- **Smooth.** A few directions give a smooth result, because each direction integrates over all elevations at once.
- **Screen space.** Surfaces off screen or hidden behind the first layer do not count.
- **Tuning.** The radius, the falloff, the angle bias and the step count change the look.

## Variants and improvements

- **Cosine weighting.** Weight each direction by the cosine to the normal and integrate it in closed form per slice, see [ground-truth ambient occlusion](/ground-truth-ambient-occlusion/).
- **Hierarchical depth.** March on a depth pyramid with larger steps far from the pixel.
- **Deinterleaved rendering.** Split the screen into sub-images with the same random offsets, so that each sub-image reads the texture coherently, then merge.
- **Temporal accumulation.** Change the offsets each frame and blend with the reprojected history.
- **Thickness heuristics.** Treat thin objects as having finite thickness, to reduce the over-darkening behind them.

## When to use it

Use HBAO when SSAO looks too noisy or too gray and the frame can afford a few directions with a few steps per pixel. It gives the smooth contact shadows of a height field. When the look should match the cosine-weighted ambient occlusion of a ray tracer more closely, use ground-truth ambient occlusion, which costs about the same.

## Pitfalls

- **Halos around near objects.** A near object counts as a tall wall for the pixels around its silhouette. The radius and falloff limit the band.
- **Facets.** Coarse triangles have slightly wrong normals, so the march finds the neighboring triangles above the tangent plane. An angle bias hides this.
- **Thin objects.** A pole or a leaf blocks the whole space behind it in the depth buffer, so the floor under it gets too dark.
- **Radius in pixels.** In a perspective camera, the radius in the scene maps to fewer pixels far away. Clamp the march length in pixels for near pixels, where it becomes very large.
- **Screen borders.** The march leaves the screen and reads clamped depths. Stop at the border.

## Implementations

## History

Screen-space ambient occlusion with point samples appeared in 2007. Bavoil, Sainz and Dimitrov presented image-space horizon-based ambient occlusion at SIGGRAPH 2008. They wrote the occlusion as an integral over the screen directions of the sine of the horizon angle minus the sine of the tangent angle, with a falloff, and computed the horizon by marching the depth buffer. The method shipped in many games through the HBAO and HBAO+ libraries of NVIDIA. Jimenez, Wu, Pesce and Jarabo (2016) added the cosine weight in their ground-truth ambient occlusion.

## References
