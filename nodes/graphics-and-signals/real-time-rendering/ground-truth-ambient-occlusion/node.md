---
tag: 2H8H92
kind: algorithm
slug: ground-truth-ambient-occlusion
name: Ground-truth ambient occlusion
aliases:
- GTAO
area: graphics-and-signals/real-time-rendering
level: research
summary: A horizon-based screen-space method that integrates cosine-weighted visibility in closed form per slice. Its match with ray traced AO is a measurement, for one depth layer only.
model: real-ram
complexity:
  vars: {p: the number of pixels, m: the number of slices per pixel, s: the number of steps per side of a slice}
  time: {worst: O(p m s)}
  space: {extra: O(p)}
properties: {deterministic: true, recursive: false, online: false, in_place: false}
history:
  year: 2016
  people: [Jorge Jimenez, Xian-Chun Wu, Angelo Pesce, Adrian Jarabo]
  note: Jimenez, Wu, Pesce and Jarabo described ground-truth ambient occlusion in an Activision technical report in 2016, with slices through the view vector, two horizons per slice and a cosine-weighted inner integral in closed form.
prereqs: [horizon-based-ambient-occlusion, ambient-occlusion]
see_also: [screen-space-ambient-occlusion, lambertian-reflectance, monte-carlo-integration, temporal-antialiasing, bilateral-filter, g-buffer, global-illumination, screen-space-reflections]
sources:
  - url: https://www.activision.com/cdn/research/PracticalRealtimeStrategiesTRfinal.pdf
    title: "Jorge Jimenez, Xian-Chun Wu, Angelo Pesce and Adrian Jarabo, Practical real-time strategies for accurate indirect occlusion, Activision technical report ATVI-TR-16-01, 2016"
    locator: the slice formulation of the cosine-weighted visibility, the horizon search on both sides of a slice, the inner integral in closed form, and the comparison with ray traced references
  - paper: doi:10.1145/1401032.1401061
    title: "Louis Bavoil, Miguel Sainz and Rouslan Dimitrov, Image-space horizon-based ambient occlusion, SIGGRAPH 2008 talks"
    locator: the horizon angles found by marching the depth buffer, which GTAO keeps
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 11.3, Ambient Occlusion (the part on horizon-based methods)
---

Ground-truth ambient occlusion is a screen-space method that computes the cosine-weighted [ambient occlusion](/ambient-occlusion/) of the surface seen in the depth buffer. Like [horizon-based ambient occlusion](/horizon-based-ambient-occlusion/), it marches the depth buffer to find horizon angles. It differs in how it splits the hemisphere: into slices, planes through the view vector, each with a horizon on both sides. Inside a slice, the integral of the cosine between the normal and the direction over the open angles has a closed form, so the only numerical integration left is over the slices. Jimenez, Wu, Pesce and Jarabo described it in 2016. The name says ground truth, but the result equals ray traced ambient occlusion only for the scene that the depth buffer describes, a single layer read as a solid height field. How close it comes on real scenes is a measurement.

## In plain words

Ambient occlusion asks how much of the sky a point sees, counting directions near the normal more than directions near the ground, as a matte surface does. Horizon methods walk across the depth buffer in a few directions and find, in each, how high the surrounding surface rises. GTAO cuts the half sphere above the point into thin vertical slices, like slices of an orange around the line of sight. In each slice, it finds the horizon on the left and on the right. Between the two horizons the sky is open, and the cosine-weighted share of that open arc can be written down with a formula. So each slice costs one march and one formula, and a few slices give the answer.

## The problem

The input is a depth buffer $D$ of $p$ pixels and the normals, from a [G-buffer](/g-buffer/) or from differences of $D$. The output is the visibility

$$A = \frac{1}{\pi} \int_{n \cdot \omega > 0} V(\omega)\, (n \cdot \omega) \, d\omega \in [0, 1]$$

per pixel, where $V(\omega)$ is 1 if the direction $\omega$ is open. The depth buffer does not say what is behind the visible surface, so the method assumes that, seen from the pixel, a direction is blocked exactly when it is below the horizon of its slice.

This page and its code use an orthographic camera that looks along $-z$, so the view vector is $v = (0, 0, 1)$ at every pixel and the tests can use height fields. In a perspective camera the view vector changes from pixel to pixel; the slices are planes through it, and the points of the march are reconstructed as $P = d\,(u, v, -1)$ from the depth and the slopes of the pixel.

## The algorithm

$m$ slices with a per-pixel offset $\xi$, $s$ steps of length $\ell$ per side, and a radius $R$. A slice $\varphi$ is spanned by $v$ and the screen direction $c = (\cos\varphi, \sin\varphi, 0)$. Angles $h$ in a slice are measured from $v$, positive toward $c$.

```pseudo id=main
GTAO(D, q, n, m, s, ℓ, R, ξ)
L1  A ← 0;  P ← the point of q
L2  for k ← 0 to m - 1:  φ ← π (k + ξ) / m;  c ← (cos φ, sin φ, 0)
L3      n_p ← (n · c) c + (n · v) v;  γ ← the angle of n_p from v
L4      h2 ← the smallest angle from v of the points of D at P + i ℓ c, i = 1..s, within R, and at most γ + π/2
L5      h1 ← minus the same on the side P - i ℓ c, and at least γ - π/2
L6      â ← ¼(-cos(2h1 - γ) + cos γ + 2 h1 sin γ) + ¼(-cos(2h2 - γ) + cos γ + 2 h2 sin γ)
L7      A ← A + |n_p| â
L8  return A / m
```

**The slice (line L3).** The projected normal $n_p$ has the length $|n_p| \le 1$ and the angle $\gamma$ from $v$ in the slice. For a direction $\omega$ of the slice at the angle $h$, $n \cdot \omega = |n_p| \cos(h - \gamma)$.

**The horizons (lines L4 and L5).** Each side is marched as in HBAO, but the code keeps the largest cosine to $v$ of the vectors from $P$ to the samples, which is the smallest angle. The search starts at the tangent of the surface, $\gamma \pm \pi/2$, so that the horizons are clamped to the hemisphere of the normal.

**The inner integral (line L6).** With $d\omega = |\sin h| \, dh \, d\varphi$ in slice coordinates, the open part of a slice contributes $\int_{h_1}^{h_2} \cos(h - \gamma) |\sin h| \, dh$, and the expression of line L6 is its antiderivative evaluated at the two horizons. The proofs folder derives it. The report of Jimenez and others gives a closed form for the same integral; this page does not quote its equation.

**The rest of the frame.** The report runs few slices per pixel, rotates them per pixel and per frame, and removes the noise with spatial and temporal filters. These choices are tuning and are not in the code.

## Example

A frontal floor meets a block that rises by $H = 8$ toward the camera along a straight line. At the distance $\delta$ from its foot, the cosine-weighted visibility of the height field is $A = \tfrac12 (1 + \delta / \sqrt{\delta^2 + H^2})$, the view factor of a strip (proved in the proofs folder). The code uses 32 slices and steps of 0.25 units with no radius limit.

| $\delta$ | exact GTAO value | code | HBAO with no falloff |
|---|---|---|---|
| 2.5 | 0.649 | 0.654 | 0.596 |
| 4.5 | 0.745 | 0.750 | 0.663 |
| 8.5 | 0.864 | 0.867 | 0.760 |

The code is within 0.005 of the formula; the rest comes from the step length at the edge of the block. HBAO without falloff measures the solid angle without the cosine, so the same wall darkens the point more: directions near the ground count as much as directions near the normal.

**One layer.** Replace the block by a plate of thickness 1 that floats 4 units above the floor and is 6 units wide. The depth buffer looks the same as for a solid block 5 units high and 6 wide. At a floor point 3.5 units from the plate, the code gives $A = 0.792$. Cosine-weighted rays against the true plate, which can pass under it, give $0.828$ with 40000 rays. The method is exact for the depth buffer but not for the scene.

## Correctness

The proofs are in the proofs folder. In slice coordinates, a direction is $\omega = \cos h \, v + \sin h \, c(\varphi)$ with $\varphi \in [0, \pi)$ and $h \in (-\pi, \pi]$; this covers the sphere once, with $d\omega = |\sin h| \, dh \, d\varphi$, and $n \cdot \omega = |n_p| \cos(h - \gamma)$. Under the height-field assumption, the open directions of a slice are those between the two clamped horizons, so the cosine-weighted visibility is $\frac1\pi \int_0^\pi |n_p| \int_{h_1}^{h_2} \cos(h - \gamma) |\sin h| \, dh \, d\varphi$, and line L6 is the inner integral in closed form. An open slice gives $\cos\gamma + \gamma\sin\gamma$, and the outer integral of an open hemisphere is exactly 1, so every plane gives $A = 1$. The wall formula of the example is proved with a standard integral. The tests check the closed form against Simpson's rule, planes against 1, and the wall against both the formula and cosine-weighted rays. That the result also matches ray traced ambient occlusion is true only for the height field; for real scenes it is a measurement, as the plate shows.

## Complexity

The model is the real RAM. Each pixel marches $m$ slices with $2s$ steps each and evaluates the closed form $m$ times: $O(p m s)$ in total, and $O(p)$ memory for the result. This is the cost of HBAO with $2m$ directions. The closed form costs a few trigonometric functions per slice, which is small next to the depth reads.

## Properties

- **Cosine weighted.** The value is the ambient occlusion integral with the cosine to the normal, not the solid angle.
- **Exact for the height field.** With exact horizons and many slices, the result is the visibility of the depth buffer read as a solid surface.
- **One layer.** Space behind the visible surface counts as blocked, so thin objects over-occlude.
- **Planes are open.** Every plane gives $A = 1$, tilted or not.
- **Smooth in the slice.** The inner integral needs no samples, only the two horizons.
- **Screen space.** Off-screen geometry does not occlude.

## Variants and improvements

- **Multiple bounces.** The report maps the visibility to an approximate multi-bounce value with a function fitted to ray traced data, as a function of the visibility and the albedo. The fit is a measurement.
- **Specular occlusion.** The report also derives an occlusion term for glossy reflections from the visibility and a bent normal.
- **Thickness heuristic.** Let the horizon fall back over distance, as if objects had a finite thickness, which reduces the over-occlusion of thin objects.
- **Temporal accumulation.** One or two slices per pixel and frame, with a different rotation each frame, filtered over time as in [temporal antialiasing](/temporal-antialiasing/).
- **Bitmask visibility.** Later methods replace the two horizons by a bit mask of open sectors per slice, which can represent gaps behind thin objects.

## When to use it

Use GTAO when the ambient occlusion of a real-time renderer should look close to that of a ray tracer and the budget is that of HBAO. It needs depth and normals and a denoiser. Use ray traced ambient occlusion when thin geometry, off-screen occluders or the space behind the first layer matter.

## Pitfalls

- **Ground truth of what.** The match is for the depth buffer as a height field. Thin objects, foliage and gaps under objects come out too dark.
- **Wrong normals.** The clamp and $\gamma$ depend on the normal. Normals from depth differences tilt at edges, and normal maps give normals that do not match the depth surface.
- **Radius.** A limit on the march radius opens far occluders abruptly. Use a falloff and accept it as tuning.
- **Perspective.** In a perspective camera the view vector and the slice change per pixel. Using a constant view vector bends the slices near the edges of a wide view.
- **Noise.** Few slices need filtering, and the filter must respect depth edges, or the occlusion leaks across them.

## Implementations

## History

Horizon-based ambient occlusion of 2008 integrated the sine of the horizon angle over screen directions, which measures solid angle. Jimenez, Wu, Pesce and Jarabo (2016) reformulated the integral in slices through the view vector, with two horizons per slice and the cosine weight inside, solved the inner integral in closed form, and compared the result with ray traced references on the depth buffer. Their report also added a fitted multi-bounce term and a specular occlusion term, and it was used in a game engine of Activision. Later screen-space methods kept the slice structure and changed the horizon model, for example with bit masks of open sectors.

## References
