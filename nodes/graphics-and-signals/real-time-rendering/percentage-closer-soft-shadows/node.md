---
tag: EXXNC3
kind: algorithm
slug: percentage-closer-soft-shadows
name: Percentage-closer soft shadows
aliases:
- PCSS
area: graphics-and-signals/real-time-rendering
level: advanced
summary: Estimate the penumbra width from the average blocker depth found in the shadow map and use it as the kernel size of percentage-closer filtering.
solves: [shadow-determination]
model: real-ram
complexity:
  vars: {q: the number of shadow lookups, m: the number of texels in the blocker search region, k: the number of texels in the filter region}
  time: {worst: Θ(q (m + k))}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: false, adaptive: true, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 2005
  people: [Randima Fernando]
  note: Fernando presented the method at SIGGRAPH 2005 as a sketch, and NVIDIA showed it at I3D 2005. It uses one ordinary shadow map from the center of the light.
prereqs: [shadow-mapping, percentage-closer-filtering]
see_also: [variance-shadow-maps, moment-shadow-mapping, cascaded-shadow-maps, shadow-volume-algorithm, temporal-antialiasing, gaussian-filter]
sources:
  - paper: doi:10.1145/1187112.1187153
    title: Randima Fernando, Percentage-closer soft shadows, ACM SIGGRAPH 2005 Sketches, article 35, 2005
    locator: the three steps (blocker search, penumbra estimation from parallel planes, filtering) and the penumbra formula (general locator)
  - url: "http://download.nvidia.com/developer/presentations/2005/I3D/I3D_05_Percentage_Closer_Soft_Shadows.pdf"
    title: Randima Fernando, Percentage-closer soft shadows, NVIDIA presentation at I3D 2005
    locator: the slides on the blocker search, the penumbra estimate and the filter step (general locator)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 7, the part on percentage-closer soft shadows (general locator)
---

Percentage-closer soft shadows add two steps before [percentage-closer filtering](/percentage-closer-filtering/): a search of the shadow map for blockers near the lookup point, and an estimate of the penumbra width from their average depth. The PCF kernel then has that width, so a shadow is sharp where the occluder touches the receiver and soft far from it. Plain PCF has one kernel width everywhere. The map is the ordinary map of [shadow mapping](/shadow-mapping/), rendered from the center of an area light, so the method costs no extra pass but more lookups.

## In plain words

A large lamp makes shadows with soft edges. The edge is narrow where the object is close to the floor, and wide where the object is high above it.

The method first looks in the shadow map around the point and finds the things that are nearer to the lamp than the point. It takes their average distance from the lamp. With that distance, the size of the lamp and the distance of the point, a rule of similar triangles gives the width of the soft edge.

Then it does the usual blur of yes or no answers, with a blur as wide as that edge. If it finds nothing in the way, the point is lit and no blur is needed.

## The problem

The light is a square of side $w$ in the plane at depth 0 of the light frame. The shadow map is a perspective view from its center with the near plane at depth $n$, and each texel is a square of side $h$ on the near plane. Unlike the [PCF](/percentage-closer-filtering/) page, the map stores linear depth $d$, the distance along the light axis, because the steps below do arithmetic on depths. A receiver point has the map position $(x, y)$ in texels and the depth $d_r$. The output is an estimate of the fraction of the light that the point sees. The reference answer is the exact visible fraction of the area light, which is known in closed form for a blocker plane parallel to a receiver plane.

## The algorithm

```pseudo id=main
PCSS(S, x, y, d_r, w, n, h, bias)
L1  r_s ← w (d_r - n) / (2 d_r h)                 ▷ half-width of the search region, in texels
L2  B ← the depths S[i, j] < d_r - bias of the texels in the square of half-width r_s around (x, y)
L3  if B is empty then return 1                    ▷ no blocker: the point is lit
L4  d_b ← the mean of B                           ▷ the average blocker depth
L5  w_p ← (d_r - d_b) w / d_b                     ▷ the penumbra width at the receiver
L6  r_f ← w_p n / (2 d_r h)                       ▷ the half-width of the filter on the map, in texels
L7  return the box PCF of half-width r_f around (x, y), with the depth d_r and the bias
```

Line L1 sets the search region. A blocker that hides some part of the light from the receiver lies in the pyramid from the receiver point to the light, and its depth is at least $n$. The pyramid is widest on the map at depth $n$, where it covers $w (d_r - n)/d_r$ on the near plane; the proof file derives this. Fernando's paper uses a search size that is set by the light size; this bound is the size that misses no blocker.

Line L5 is similar triangles for a blocker edge at depth $d_b$ parallel to the receiver: the light of width $w$ at distance $d_b$ from the edge throws a penumbra of width $w (d_r - d_b)/d_b$ at the receiver. Line L6 projects half of it onto the near plane (the factor $n / d_r$) and converts it to texels.

## Example

Take $n = 1$, a blocker half-plane at $d_b = 2$, a receiver plane at $d_r = 4$, a light of width $w = 1$, and texels of side $h = 0.05$ on the near plane in a map 64 texels wide. The blocker covers the map columns 0 to 31 (the world $x < 0$).

- Line L1: $r_s = 1 \cdot (4 - 1)/(2 \cdot 4 \cdot 0.05) = 7.5$ texels.
- Line L2 at the point that maps to column 32 on a map of 3 rows: the search square covers the columns 24 to 39 of all 3 rows, and the columns 24 to 31 hold the blocker, so $|B| = 24$.
- Line L4: $d_b = 2.0$.
- Line L5: $w_p = (4 - 2) \cdot 1 / 2 = 1$, in world units at the receiver.
- Line L6: $r_f = 1 \cdot 1 / (2 \cdot 4 \cdot 0.05) = 2.5$ texels.

At five receiver points, given by the world $x_w$ of the point:

| $x_w$ | PCSS | exact visible fraction |
|---|---|---|
| $-0.5$ | 0 | 0 |
| $-0.25$ | 0.2 | 0.25 |
| $0$ | 0.5 | 0.5 |
| $0.25$ | 0.8 | 0.75 |
| $0.5$ | 1.0 | 1 |

The exact fraction is $\mathrm{clamp}(1/2 + x_w / w_p)$, a ramp of width $w_p = 1$. PCSS gets the width right, and its error, at most 0.05 here, comes from the count of whole texels in a filter of half-width 2.5. With a blocker at $d_b = 3.5$ the same formula gives $w_p = 1/7$, a much sharper edge.

## Correctness

PCSS is exact for no scene with a penumbra, because it replaces the occluders by one plane at their mean depth. The proof file shows what holds in the model of parallel planes, and the tests check each claim.

- **The ramp.** For a half-plane blocker at $d_b$ and a receiver plane at $d_r$, the exact visible fraction of a light of width $w$ is $\mathrm{clamp}(1/2 + x_w / w_p)$ with $w_p$ of line L5 (similar triangles).
- **The search region.** Every map texel that can hold a blocker of the receiver point lies in the square of line L1 (the bound is reached at depth $n$).
- **The limits.** With no blocker in the region the result is 1, and with $w = 0$ the filter has half-width 0 and PCSS is the hard test of shadow mapping.
- **The error bound.** In flatland, with the filter inside the map and $r_f \ge 1$, the result differs from the exact fraction by at most $1/(2 r_f)$. The tests check this on random parallel-plane scenes.

For several blockers at different depths, the mean depth of line L4 is a heuristic. It gives a wrong width where a near and a far occluder overlap in the search region.

## Complexity

Line L2 reads the $m \approx (2 r_s)^2$ texels of the search region, and line L7 reads the $k \approx (2 r_f)^2$ texels of the filter, so one lookup costs $\Theta(m + k)$ and $q$ lookups cost $\Theta(q (m + k))$ in the worst case. Both regions grow with the light size, and $r_f$ grows as the blocker gets nearer to the light. Renderers bound the cost with a fixed number of taps in each step, for example a Poisson disk of taps scaled to the region, which makes the cost $\Theta(q)$ with a fixed constant but adds noise. The extra space is $\Theta(1)$.

## Properties

- **Contact hardening.** The penumbra is narrow at contact and wide far from it, as with an area light (a proved property of the parallel-plane model, and a heuristic elsewhere).
- **One map.** It needs no extra pass and works with any map that stores linear depth.
- **Not a visibility integral.** The result is a PCF value with a chosen width, not the visible fraction of the light. Overlapping occluders and receivers that are not planes give a wrong width.
- **Adaptive cost.** The cost per pixel follows the blocker distance, which makes the frame time depend on the scene.

## Variants and improvements

- **Fixed tap counts.** Sample both regions with a fixed Poisson disk scaled to $r_s$ and $r_f$, rotated per pixel, and clean the noise with [temporal antialiasing](/temporal-antialiasing/).
- **Min and max depth maps.** Search a mip chain of the minimum and the maximum depths to find the blockers in fewer reads, or to skip points that are fully lit or fully shadowed.
- **Filterable blocker search.** With [variance shadow maps](/variance-shadow-maps/) or [moment shadow mapping](/moment-shadow-mapping/), both the blocker average and the filter come from moments over a box, which a summed-area table or a mip chain gives in $O(1)$ per lookup.
- **Several maps.** With [cascaded shadow maps](/cascaded-shadow-maps/), the light size in texels differs from cascade to cascade, so $r_s$ and $r_f$ are computed per cascade.

## When to use it

Use PCSS when soft shadows of a small area light must sharpen at contact and the light is not too large. For large lights, the search and filter regions become large and slow. Then a filterable map with a box filter of variable size, or ray-traced shadows, gives a more even cost. For hard shadows, plain [PCF](/percentage-closer-filtering/) is cheaper.

## Pitfalls

- **A search region that is too small.** If line L1 uses a fixed size smaller than $w (d_r - n)/(2 d_r h)$, a blocker far from the point is not found, the point returns 1 at line L3, and the penumbra has lit holes.
- **No bias in the search.** Without the bias in line L2, the receiver's own depth in the map counts as a blocker, $d_b$ moves toward $d_r$, and the penumbra becomes too narrow.
- **Clip depth in place of linear depth.** Lines L4 and L5 need linear depth. With the nonlinear depth of a perspective light, the mean and the ratio are wrong, and the penumbra width changes with the near plane.
- **Forgetting the projection.** If line L6 omits the factor $n / d_r$, the filter is larger than the penumbra by $d_r / n$.
- **Dividing by zero.** Line L5 divides by $d_b$, which is at least $n > 0$ only when the map stores depths from the near plane on.

## Implementations

## History

Fernando presented percentage-closer soft shadows in 2005, as a SIGGRAPH sketch and in NVIDIA material for developers. It used the PCF filter that hardware already supported and needed only one ordinary shadow map, so it fit into existing renderers. Later work replaced its search and filter by filterable moment maps and fixed tap patterns, and the name stayed for the class of contact-hardening shadow filters.

## References
