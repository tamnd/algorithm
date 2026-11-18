---
tag: CF3C6M
kind: algorithm
slug: percentage-closer-filtering
name: Percentage-closer filtering
aliases:
- PCF
area: graphics-and-signals/real-time-rendering
level: core
summary: Soften shadow map edges by comparing several depth samples near the lookup point with the receiver depth and averaging the binary results.
solves: [shadow-determination]
model: real-ram
complexity:
  vars: {q: the number of shadow lookups, k: the number of kernel taps}
  time: {worst: Θ(q k)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1987
  people: [William T. Reeves, David H. Salesin, Robert L. Cook]
  note: Reeves, Salesin and Cook introduced the method in 1987 for antialiased shadows in film rendering. Graphics hardware later added the 2 x 2 bilinear form to the depth texture lookup.
prereqs: [shadow-mapping]
see_also: [percentage-closer-soft-shadows, variance-shadow-maps, moment-shadow-mapping, bilinear-filtering, gaussian-filter, prefix-sums, temporal-antialiasing, z-fighting]
sources:
  - paper: doi:10.1145/37401.37435
    title: William T. Reeves, David H. Salesin and Robert L. Cook, Rendering antialiased shadows with depth maps, Computer Graphics 21(4), SIGGRAPH 1987, pages 283 to 291
    locator: the sections on percentage-closer filtering (compare first, then filter) and on the bias
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 7.5 (percentage-closer filtering and its kernels)
---

Percentage-closer filtering changes the lookup step of [shadow mapping](/shadow-mapping/): it compares the receiver depth with every depth in a small neighborhood of the shadow map and returns the weighted mean of the binary results. The map and its first pass do not change. The result is a lit fraction between 0 and 1, so the shadow edge is smooth, but its width is set by the kernel and not by the size of the light; [percentage-closer soft shadows](/percentage-closer-soft-shadows/) choose the kernel from the scene, and [variance shadow maps](/variance-shadow-maps/) change what the map stores so that it can be filtered before the test.

## In plain words

A shadow map gives a yes or no answer for each point: lit or not lit. Where the shadow edge crosses the dots of the map, the yes and no answers make a staircase.

Ask the same question at several dots near the point, and count how many say lit. If 6 of 9 say lit, call the point two thirds lit. Points near the edge then get values between dark and bright, and the staircase becomes a soft ramp.

The order matters. You must ask the question at each dot first and then take the average. If you take the average of the stored distances first and ask once, you still get only yes or no, and the edge stays hard.

## The problem

The input is a shadow map $S$ of $W \times H$ texels from the first pass of [shadow mapping](/shadow-mapping/), a lookup point with the light space position $(x, y, z)$, a bias $b \ge 0$, and a kernel $K$ that gives a weight $\omega \ge 0$ to each offset $(u, v)$. As on the shadow mapping page, $x$ and $y$ are in texel units, texel $(i, j)$ has its center at $(i + \tfrac12, j + \tfrac12)$, and $z$ is the light depth in the Direct3D range $[0, 1]$, smaller nearer. A tap $(i, j)$ is *lit* when $z - b \le S[i, j]$, and a tap outside the map is lit (the border rule of that page). The output is the weighted mean of the lit taps over the kernel, placed at the texel that holds $(x, y)$. The shadow mapping page returns the shadowed fraction; this page returns the lit fraction, which is 1 minus it.

## The algorithm

```pseudo id=main
LIT-TAP(S, i, j, z, b)
    if (i, j) is outside the map then return 1
    if z - b ≤ S[i, j] then return 1 else return 0

PCF(S, x, y, z, b, K)                           ▷ K maps an offset (u, v) to a weight ω
L1  (i, j) ← (⌊x⌋, ⌊y⌋)                         ▷ the texel that holds (x, y)
L2  acc ← 0, wsum ← 0
L3  for each offset (u, v) with weight ω > 0 in K do
L4      t ← LIT-TAP(S, i + u, j + v, z, b)      ▷ compare first
L5      acc ← acc + ω t                         ▷ then filter
L6      wsum ← wsum + ω
L7  return acc / wsum                           ▷ the lit fraction

PCF-BILINEAR(S, x, y, z, b)                      ▷ the 2 x 2 form of the hardware
L8  (i, j) ← (⌊x - 1/2⌋, ⌊y - 1/2⌋), f ← x - 1/2 - i, g ← y - 1/2 - j
L9  c00, c10, c01, c11 ← LIT-TAP at (i, j), (i + 1, j), (i, j + 1), (i + 1, j + 1)
L10 return (1 - f)(1 - g) c00 + f (1 - g) c10 + (1 - f) g c01 + f g c11
```

The box kernel of radius $r$ gives the weight 1 to each offset in $[-r, r]^2$, which is the filter of the shadow mapping page. The tent kernel gives the weight $(r + 1 - |u|)(r + 1 - |v|)$, which makes the ramp smoother. PCF-BILINEAR places the four taps around $(x, y)$ and weights them by the distances to their centers. Graphics hardware does this in one lookup of a depth texture with a compare mode. Larger kernels in a renderer are often sums of several such bilinear lookups.

## Example

The $8 \times 8$ map has a floor at depth 0.8 and the top of a box at depth 0.3 over the texels with $2 \le i, j \le 5$. The receiver is the floor, $z = 0.8$, with $b = 0$, and the kernel is the $3 \times 3$ box. Each lookup is at the center of the texel in the table.

| texel | shadowed taps | lit fraction |
|---|---|---|
| $(6, 3)$ | column 5, rows 2 to 4 | $6/9 = 2/3$ |
| $(6, 6)$ | $(5, 5)$ only | $8/9$ |
| $(5, 5)$ | columns 4 and 5, rows 4 and 5 | $5/9$ |
| $(5, 3)$ | columns 4 and 5, rows 2 to 4 | $3/9 = 1/3$ |

At $(6, 3)$ the floor is outside the box, but the box is one texel away, so a third of the kernel is shadowed. Without PCF the four lookups return 1, 1, 0 and 0.

The bilinear form at $(x, y) = (6.25, 3.5)$ has $(i, j) = (5, 3)$, $f = 0.75$ and $g = 0$. The tap $(5, 3)$ is shadowed and $(6, 3)$ is lit, so L10 returns $0.75$. As $x$ moves from 5.5 to 6.5, the value goes from 0 to 1 along a straight line.

**Filtering the depths first.** At $(6, 3)$ the mean of the nine stored depths is $(3 \cdot 0.3 + 6 \cdot 0.8)/9 = 0.6333$, and $0.8 > 0.6333$, so one compare says shadowed (0). PCF says $2/3$. At $(5, 3)$ the mean is $(6 \cdot 0.3 + 3 \cdot 0.8)/9 = 0.4667$, and the one compare also says 0. The mean of the depths is a depth that no surface has, and the compare with it is still binary.

## Correctness

The proof file shows three claims, and the tests check each one against a second method.

- **The weighted mean.** For any kernel with nonnegative weights and a positive sum, lines L1 to L7 return $\sum \omega\, t / \sum \omega$ over the taps, a value in $[0, 1]$ that does not increase when $z$ grows. With one tap it is the binary test of shadow mapping. For the box, the count of lit taps equals the count from a [prefix sum](/prefix-sums/) table of the binary image of lit texels, which is how the test checks it.
- **The bilinear form.** Line L10 equals the mean of the nearest texel test over the unit square centered at $(x, y)$: the square overlaps the four texels in the areas $(1 - f)(1 - g)$, $f(1 - g)$, $(1 - f) g$ and $f g$. At a texel center $f = g = 0$, and the result is the binary test. The tests compare L10 with this integral, computed on a $16 \times 16$ grid of sample points, exactly.
- **The wrong order.** Filtering the depths and then comparing once gives only 0 or 1. The example shows this.

What PCF does not do is give the true visibility of an area light: the mean is over the taps of a point light test, so it is an image filter of the binary shadow, not a penumbra.

## Complexity

One lookup with a kernel of $k$ taps makes $k$ texel reads and compares, so it costs $\Theta(k)$, and $q$ lookups cost $\Theta(q k)$ in the worst case. The box of radius $r$ has $k = (2r + 1)^2$. The bilinear form is $k = 4$. The extra space is $\Theta(1)$ beyond the map. The cost cannot drop to $O(1)$ per lookup with a [prefix sum](/prefix-sums/) table of the map, because the binary image depends on the receiver depth $z$ of each lookup. This is the reason for the filterable maps of the variants.

## Properties

- **Compare, then filter.** The filter acts on the binary results, so the output is a fraction of lit taps (a proved property).
- **Linear in the weights, not in the depths.** For a fixed receiver depth, PCF is a linear filter of the binary image. It is not a linear filter of the stored depths, so the map cannot be [mipmapped](/mipmap/) or blurred in advance.
- **Fixed penumbra.** The width of the soft edge is the kernel width in texels, the same for a contact shadow and for a shadow far from its occluder. This is a heuristic softening, not the shadow of an area light.
- **Bias per tap.** One bias serves all taps, but the receiver depth changes across the kernel, so a large kernel needs a larger bias or a bias that follows the receiver plane.

## Variants and improvements

- **Kernel shapes.** Box, tent and Gaussian kernels; a Poisson disk of taps with a rotation per pixel trades the regular pattern for noise, which [temporal antialiasing](/temporal-antialiasing/) can then average.
- **Bilinear taps.** A kernel of $(2r)^2$ texels can be read with $r^2$ bilinear lookups, each with its own weights.
- **Receiver plane depth bias.** Compute the depth slope of the receiver in light space and compare each tap with the receiver depth moved to that tap, in place of one constant bias.
- **Soft shadows.** [Percentage-closer soft shadows](/percentage-closer-soft-shadows/) estimate the penumbra width from a blocker search and set the kernel from it.
- **Filterable maps.** [Variance shadow maps](/variance-shadow-maps/) and [moment shadow mapping](/moment-shadow-mapping/) store moments of the depth, which can be filtered in advance, and bound the lit fraction from them.

## When to use it

Use PCF as the default filter of a shadow map. The $2 \times 2$ hardware form costs about one texture lookup, and a few bilinear lookups give a good edge at a low cost. Use a filterable map when the kernel must be large, when the map should be mipmapped, or when the shadow must be blurred over many texels, because the cost of PCF grows with the kernel area.

## Pitfalls

- **Filtering the depths first.** Replacing lines L4 and L5 by a mean of $S$ and one compare after L7 gives 0 or 1 at every point, as the example shows: 0 at $(6, 3)$ in place of $2/3$.
- **Dividing by the kernel size.** If line L7 divides by the number of taps in place of `wsum`, a weighted kernel returns a value outside $[0, 1]$.
- **No half texel shift.** If line L8 takes $\lfloor x \rfloor$ in place of $\lfloor x - 1/2 \rfloor$, the four taps are not the four nearest centers, and the shadow moves by half a texel.
- **A constant bias with a large kernel.** In line L4 the same $z - b$ is compared at taps several texels away, where a sloped receiver has a different depth, so a wide kernel on a sloped floor shadows the floor itself (acne) unless $b$ grows with the kernel.
- **Clamp at the border.** Treating taps outside the map as the nearest edge texel in place of lit (line L4) stretches a shadow at the map border across the scene.

## Implementations

## History

Reeves, Salesin and Cook described percentage-closer filtering in 1987, at Pixar, for shadows in film rendering. Their point was that the depth map cannot be filtered like a color texture, because the result of interest is the outcome of a compare. They filtered the binary results over a region of the map with stochastic samples. Depth textures with a compare mode and bilinear filtering of the results came to graphics hardware later and made the $2 \times 2$ form a standard part of real-time shadows.

## References
