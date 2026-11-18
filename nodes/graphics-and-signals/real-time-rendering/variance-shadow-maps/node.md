---
tag: BNWA0B
kind: algorithm
slug: variance-shadow-maps
name: Variance shadow maps
aliases:
- variance shadow mapping
area: graphics-and-signals/real-time-rendering
level: advanced
summary: Store depth and squared depth, filter them like a texture, and bound the fraction of light by Chebyshev's inequality on the local depth distribution.
solves: [shadow-determination]
model: real-ram
complexity:
  vars: {w: the map width in texels, h: the map height in texels, q: the number of shadow lookups}
  time: {worst: Θ(w h + q)}
  space: {extra: Θ(w h)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: false}
history:
  year: 2006
  people: [William Donnelly, Andrew Lauritzen]
  note: Donnelly and Lauritzen published the method at I3D 2006. Lauritzen added summed-area tables, a minimum variance and a light bleeding reduction in GPU Gems 3 (2007).
prereqs: [shadow-mapping, percentage-closer-filtering, chebyshev-inequality]
see_also: [moment-shadow-mapping, percentage-closer-soft-shadows, cascaded-shadow-maps, mipmap, prefix-sums, variance, markov-inequality, separable-filter]
sources:
  - paper: doi:10.1145/1111411.1111440
    title: William Donnelly and Andrew Lauritzen, Variance shadow maps, Proceedings of the 2006 Symposium on Interactive 3D Graphics and Games (I3D 2006), 161 to 165
    locator: the moment map, the one-tailed Chebyshev bound p_max, the exactness for one planar occluder and one planar receiver, and the light bleeding example
  - book: isbn:9780321515261
    title: Hubert Nguyen (editor), GPU Gems 3, Addison-Wesley, 2007, Chapter 8, Andrew Lauritzen, Summed-Area Variance Shadow Maps
    locator: Section 8.4.2 (the minimum variance) and Section 8.4.3 (the light bleeding reduction with linstep), and the summed-area table filter
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 7, the part on filtered shadow maps (general locator)
---

Variance shadow maps store the depth and the squared depth at each texel, so the map can be blurred, [mipmapped](/mipmap/) or filtered with a summed-area table before any compare. At lookup time the filtered mean and variance give an upper bound on the lit fraction by the one-sided form of the [Chebyshev inequality](/chebyshev-inequality/). [Percentage-closer filtering](/percentage-closer-filtering/) compares first and then filters, which costs one compare per tap; here one lookup serves a filter of any size, but the bound can be too high, and the shadow then leaks light (light bleeding). [Moment shadow mapping](/moment-shadow-mapping/) stores four moments to make the bound tighter.

## In plain words

A normal shadow map stores one distance per dot, and you cannot blur it: a blurred distance is a distance that no object has.

This method stores two numbers per dot: the distance and the distance times itself. These two numbers can be blurred like the colors of an image. After the blur, each dot knows the average distance of the objects near it and how much these distances spread.

At lookup time a classic rule from statistics says: if the point is far behind the average, and the spread is small, then few of the objects near it can be behind the point. That gives a quick estimate of how lit the point is. The estimate is never too dark, but it can be too bright where objects at very different distances overlap.

## The problem

The input is a shadow map $S$ of $w \times h$ texels from the first pass of [shadow mapping](/shadow-mapping/), with depths in the Direct3D range $[0, 1]$, smaller nearer, a filter, and a set of lookups. A lookup has a texel $(i, j)$ and a receiver depth $t$. The filter gives a weight to each texel near $(i, j)$, and so a probability distribution of the depths $z$ under it. The *lit fraction* is the probability that $z \ge t$, the weighted fraction of the texels that the receiver is not behind, which is the value of PCF with the same weights and the bias 0. The output is a value that is at least the lit fraction and is exact in the simple case of one planar occluder over one planar receiver.

## The algorithm

```pseudo id=main
VSM-MAP(S, r)                                     ▷ after the depth pass, once per frame
L1  M[i, j] ← (S[i, j], S[i, j]^2) for each texel   ▷ the moments
L2  F ← the (2r + 1) x (2r + 1) box filter of M, with a summed-area table of each moment
    return F

VSM-LOOKUP(F, i, j, t, v_min, a)                   ▷ receiver depth t
L3  (m1, m2) ← F[i, j]                            ▷ the mean and the mean square
L4  if t ≤ m1 then return 1
L5  v ← max(m2 - m1^2, v_min)                      ▷ the variance, with a floor
L6  p ← v / (v + (t - m1)^2)                       ▷ the one-sided Chebyshev bound
L7  return clamp((p - a) / (1 - a), 0, 1)          ▷ light bleeding reduction; a = 0 keeps p
```

Any linear filter works in line L2: a Gaussian blur in two [separable](/separable-filter/) passes, the mip chain of the map, or anisotropic filtering of the hardware. A summed-area table, the 2D form of the [prefix sums](/prefix-sums/), gives the box mean of any size in four reads. In line L5, $m_2 - m_1^2$ is the [variance](/variance/) of the filtered distribution. The floor $v_{\min}$ is a tuning against round-off, and the amount $a$ in line L7 is a tuning that trades the bound for less bleeding.

## Example

Take the $8 \times 8$ map of the [PCF](/percentage-closer-filtering/) page: a floor at depth 0.8 and the top of a box at depth 0.3 over the texels $2 \le i, j \le 5$, with a $3 \times 3$ box filter. At texel $(6, 3)$ the filter holds three texels at 0.3 and six at 0.8.

- Line L3: $m_1 = (3 \cdot 0.3 + 6 \cdot 0.8)/9 = 19/30$ and $m_2 = (3 \cdot 0.09 + 6 \cdot 0.64)/9 = 137/300$.
- Line L5: $v = 137/300 - (19/30)^2 = 1/18$.
- Line L6 for the floor, $t = 0.8$: $t - m_1 = 1/6$, so $p = (1/18)/(1/18 + 1/36) = 2/3$.

PCF gives $2/3$ as well: with two depths, one planar occluder and one planar receiver, the bound is exact.

**Light bleeding.** Two occluders at depths 0.1 and 0.9, each over half the filter, cast a shadow on a receiver at 1.0. The true lit fraction is 0. The moments are $m_1 = 0.5$ and $v = 0.16$, so $p = 0.16/(0.16 + 0.25) = 16/41 = 0.390$: the receiver shows 39 percent of the light. With occluders at 0.1 and 0.2 over a receiver at 0.3, the moments are $m_1 = 0.15$ and $v = 0.0025$, and $p = 0.0025/(0.0025 + 0.0225) = 1/10$. The bleeding is large when the occluders are far apart and the receiver is close behind the far one.

**The reduction.** With $a = 1/5$, line L7 maps $16/41$ to $(16/41 - 1/5)/(4/5) = 39/164 = 0.238$ and $1/10$ to 0. It also maps the exact $2/3$ of the box edge to $7/12$, below the true value, so the result is no longer an upper bound.

## Correctness

The proof file shows these claims, and the tests check each against the exact lit fraction of the filtered texels.

- **The filter.** Line L2 gives the box means of $z$ and $z^2$ (inclusion and exclusion on the summed-area table). The test compares it with a direct sum over the box.
- **The bound.** For any distribution with mean $m_1$ and variance $v > 0$ and any $t > m_1$, $P(z \ge t) \le v/(v + (t - m_1)^2)$. This is the one-sided Chebyshev inequality (Cantelli's inequality). The proof applies the [Markov inequality](/markov-inequality/) to $(z - m_1 + v/(t - m_1))^2$.
- **Sharpness.** For each mean and variance there is a two-point distribution that reaches the bound, so no method that sees only $m_1$ and $m_2$ can do better.
- **Two planes.** If the filter holds only the depths $d_o < t$ and the receiver depth $t$, the bound equals the true lit fraction.
- **The tunings.** The floor $v_{\min}$ keeps the bound, because $p$ grows with $v$. The reduction of line L7 does not keep it, as the example shows.

The paper of Donnelly and Lauritzen states the inequality for $P(x \ge t)$, which is the lit fraction; its abstract calls the result a bound on the fraction occluded, which is loose wording. The occluded fraction has the lower bound $1 - p$.

## Complexity

Line L1 and the summed-area tables of line L2 take $\Theta(w h)$ time and space, and so does any fixed-size separable blur. Each lookup is $O(1)$: four reads per moment for the box mean, and a few arithmetic operations. So $q$ lookups cost $\Theta(w h + q)$ in the worst case, whatever the filter size. The map takes two values per texel in place of one.

## Properties

- **Filterable.** The stored moments are linear in the texel weights, so every linear filter, mipmapping and multisample resolve applies to them before the lookup (a proved property).
- **An upper bound.** The result is never darker than the lit fraction of the filtered texels, without line L7 (a proved property).
- **Light bleeding.** Where the depths under the filter spread widely and the receiver is close behind the far occluder, the bound is much too high (a proved property of the bound; the example gives 39 percent of the light in place of 0).
- **Precision.** The variance $m_2 - m_1^2$ is a difference of two close numbers. With 16-bit storage it loses most of its digits, so the moments need 32-bit floats or a careful offset of the depth.

## Variants and improvements

- **Summed-area variance shadow maps.** Lauritzen (GPU Gems 3, Chapter 8) uses summed-area tables so that each pixel can have its own filter size, which also serves as the filter step of soft shadows.
- **Light bleeding reduction.** Map $[a, 1]$ to $[0, 1]$ by a linear step, as in line L7. It removes bleeding below the level $a$ and darkens true penumbras.
- **Layered and exponential maps.** Split the depth range into layers, or warp the depth by an exponential before the moments are taken, so that the occluders in one layer spread less.
- **Moment shadow maps.** Store four moments and use the sharp bound for them; see [moment shadow mapping](/moment-shadow-mapping/).

## When to use it

Use variance shadow maps when the shadow must be filtered over many texels, mipmapped or blurred, and the cost per lookup must stay constant: wide soft shadows, distant [cascades](/cascaded-shadow-maps/), or shadows with anisotropic filtering at grazing angles. Use [PCF](/percentage-closer-filtering/) when the filter is small or when scenes with deep overlapping occluders make the bleeding visible.

## Pitfalls

- **No variance floor.** Without $v_{\min}$ in line L5, round-off can make $m_2 - m_1^2$ zero or negative, and line L6 then returns 0 or a value outside $[0, 1]$ at a lit surface.
- **A large variance floor.** Line L5 with a large $v_{\min}$ lights a receiver close behind a flat occluder: with $m_1 = 0.5$, no spread and $t = 0.51$, the floor $10^{-4}$ gives $p = 1/2$, but the receiver is in shadow.
- **Reduction as a free fix.** Line L7 with $a > 0$ turns the bound into an estimate that can be too dark, and it shrinks true penumbras; choose $a$ per scene.
- **Comparing with the filtered depth.** Replacing lines L4 to L6 by the test $t \le m_1$ returns 0 or 1, the error that PCF exists to avoid.
- **Too little precision.** Storing the moments of line L1 in 16 bits destroys the variance; the shadow then shows noise and acne.

## Implementations

## History

Donnelly and Lauritzen presented variance shadow maps at I3D 2006. They saw that two moments are enough for a useful bound and that the moments can be filtered with the texture hardware, which plain depth maps cannot. Lauritzen extended the method with summed-area tables and the light bleeding reduction in GPU Gems 3 in 2007. The problem of bleeding led to exponential maps and, in 2015, to [moment shadow mapping](/moment-shadow-mapping/) by Peters and Klein.

## References
