---
tag: TE6F11
kind: algorithm
slug: tiled-shading
name: Tiled shading
aliases:
- tiled light culling
- Forward+
area: graphics-and-signals/real-time-rendering
level: advanced
summary: Cut the screen into tiles, keep for each tile the lights whose volume can reach its frustum between the nearest and farthest depth, and shade each pixel with the lights of its tile only.
model: real-ram
complexity:
  vars: {p: the number of pixels, l: the number of lights, t: the number of tiles, k: the average number of lights kept per pixel}
  time: {culling: O(p + t l), shading: O(p k), worst: O(p l)}
  space: {lists: O(t l)}
properties: {deterministic: true, recursive: false, online: false, in_place: false}
history:
  year: 2011
  people: [Ola Olsson, Ulf Assarsson, Takahiro Harada, Jay McKee, Jason C. Yang]
  note: Olsson and Assarsson described tiled deferred and tiled forward shading and their costs in 2011. Harada, McKee and Yang presented a tiled forward renderer at Eurographics 2012.
prereqs: [deferred-shading, frustum-culling]
see_also: [clustered-shading, deferred-shading, g-buffer, hierarchical-z-buffer, tiled-rasterization, simt-model, prefix-sums, visibility-culling]
sources:
  - paper: doi:10.1080/2151237X.2011.621761
    title: "Ola Olsson and Ulf Assarsson, Tiled shading, Journal of Graphics, GPU, and Game Tools 15(4), 235-251, 2011"
    locator: the tile grid, the per-tile depth range and light lists, and tiled deferred and tiled forward shading
  - paper: doi:10.2312/conf/EG2012/short/005-008
    title: "Takahiro Harada, Jay McKee and Jason C. Yang, Forward+: bringing deferred lighting to the next level, Eurographics 2012 Short Papers, 5-8"
    locator: the depth pre-pass, the light culling per tile in a compute shader, and the forward shading pass that reads the tile lists
  - paper: doi:10.2312/EGGH/HPG12/087-096
    title: "Ola Olsson, Markus Billeter and Ulf Assarsson, Clustered deferred and forward shading, High-Performance Graphics 2012, 87-96"
    locator: Section 3.3 (light assignment), which notes that tiled methods test all lights per tile by brute force
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 20, Efficient Shading (the part on tiled shading)
---

Tiled shading is a light culling method for scenes with many local lights. It cuts the screen into square tiles, often 16 by 16 pixels. For each tile it finds the nearest and the farthest depth of its pixels, builds the frustum that these bounds cut out of the view, and keeps the lights whose sphere of influence is not outside it. Each pixel then shades only the lights in the list of its tile. With [deferred shading](/deferred-shading/), the culling and the shading run in one compute pass over the [G-buffer](/g-buffer/), and each pixel reads its G-buffer record once. In tiled forward shading, a depth pre-pass gives the tile depths and the forward pass reads the lists. Olsson and Assarsson described both forms in 2011. [Clustered shading](/clustered-shading/) is the successor that also cuts the depth range into slices.

## In plain words

A scene has hundreds of small lights, but each one lights only a small part of the screen. Testing every light at every pixel wastes almost all the work. So the screen is cut into small squares. For each square, the method looks at how near and how far the visible surfaces are, and asks of each light: can its light reach anything in this box? If the answer is no, the light is left out of the list of that square. Then every pixel goes only through the short list of its square. The test is careful in one direction: it can keep a light that does not reach any pixel, but it never leaves out a light that does.

## The problem

The input is a depth buffer $D$ of $p = W H$ pixels with the view depth $d > 0$ of the visible surface (or none for the background), the surface attributes of each pixel, and $l$ point lights. Light $j$ has a center $c_j$, a radius $r_j$ and an intensity. It reaches a point $P$ only if $\lVert P - c_j \rVert < r_j$, and its contribution is exactly 0 elsewhere. The output is the shaded image: for each pixel, the sum of the contributions of all lights. The brute-force method costs $\Theta(p l)$ light evaluations. The goal is a list of lights per tile that contains every light that reaches a pixel of the tile and as few other lights as possible.

The camera looks along $-z$, and the page stores the linear view depth $d = -z$. The pixel $(i, j)$ has its center at $(i + 1/2, j + 1/2)$, with $j$ counted from the bottom. With the aspect ratio $a = W / H$ and the vertical field of view $2\theta$, a screen position $s_x$ in pixels has the slope $u(s_x) = (2 s_x / W - 1)\, a \tan\theta$, and $v(s_y) = (2 s_y / H - 1) \tan\theta$; the pixel at depth $d$ is at $P = d\,(u, v, -1)$. The radius of a light is part of the light model. Real lights fall off without end, so the radius cuts them, and that cut is tuning.

## The algorithm

$t$ is the number of tiles. Lines L1 to L6 build the lists and lines L7 to L10 shade. SPHERE-IN-TILE is the conservative test of a sphere against the four side planes of the tile, which pass through the eye, and against the depth range.

```pseudo id=main
TILED-SHADING(D, G, lights, T)
L1  for each tile τ of T × T pixels                    ▷ one thread group per tile
L2      (dmin, dmax) ← the smallest and largest D over the pixels of τ
L3      F ← the inward unit normals of the four side planes of τ
L4      list[τ] ← empty
L5      for each light j                                  ▷ the threads of the group share this loop
L6          if SPHERE-IN-TILE(F, dmin, dmax, cj, rj) then append j to list[τ]
L7  for each pixel q with geometry, in tile τ
L8      P ← the view position of q;  c ← 0
L9      for each j in list[τ]: c ← c + SHADE(G[q], P, light j)
L10     out[q] ← c

SPHERE-IN-TILE(F, dmin, dmax, c, r)
L11 for each m in F: if m · c < -r then return false
L12 if -cz + r < dmin or -cz - r > dmax then return false
L13 return true
```

**The planes (line L3).** The tile covers the pixel rectangle $[x_0, x_1] \times [y_0, y_1]$. Its left plane holds the points with $x / d \ge u(x_0)$, which is $x + u(x_0) z \ge 0$, so its normal is $(1, 0, u(x_0))$ after normalizing. The right plane has $(-1, 0, -u(x_1))$, and the two planes in $y$ are the same with $v$. The planes depend only on the tile, so they can be computed once per frame.

**The depth range (line L2).** On a GPU, the threads of a tile read one pixel each and reduce the depth with atomic min and max in shared memory. Background pixels do not take part. A tile with no geometry gets an empty list.

**The light loop (lines L5 and L6).** The threads of the group take the lights in steps of the group size and append the kept ones to a list in shared memory with an atomic add on its length. The order in the list then depends on the timing of the threads. The code of this page keeps the index order, which makes the floating-point sum equal to the brute-force sum.

**The test (lines L11 to L13).** A sphere that is fully outside one plane, or fully nearer than $d_{\min}$ or farther than $d_{\max}$, cannot reach a point in the tile. The test does not catch every miss. A sphere near the corner of two planes can be outside the frustum but not outside either plane.

## Example

**The test by hand.** The screen is 32 by 32 pixels with $\tan\theta = 1$ and 16-pixel tiles. The tile in the lower left covers $u, v \in [-1, 0]$. Its four normals are $(1, 0, -1)/\sqrt 2$, $(-1, 0, 0)$, $(0, 1, -1)/\sqrt 2$ and $(0, -1, 0)$. Say its pixels have the depth range $[3, 12]$.

| light | center | $r$ | the test | result |
|---|---|---|---|---|
| A | $(0.5, -0.5, -5)$ | 1 | right plane $-0.5 \ge -1$, the other planes positive, $[d_c - r, d_c + r] = [4, 6]$ meets $[3, 12]$ | kept |
| B | $(2, -1, -5)$ | 1 | right plane $(-1, 0, 0) \cdot c = -2 < -1$ | culled |
| C | $(-1, -1, -20)$ | 2 | $d_c - r = 18 > 12$ | culled |
| D | $(-0.5, -0.5, -7)$ | 0.5 | all planes pass, $7 \in [3, 12]$ | kept |

If the tile shows a box face at depth 3 and a wall at depth 12 and nothing between, light D reaches no pixel but stays in the list. This is a false positive caused by the depth gap.

**A measured scene.** The tests render a room of 32 by 32 pixels: a floor, two side walls, a back wall at depth 12 with an open window, and a box face at depth 3. 994 pixels have geometry, and there are 60 random lights with radii between 0.3 and 0.8. Brute force evaluates $994 \cdot 60 = 59\,640$ (pixel, light) pairs. Tiled shading with 8-pixel tiles evaluates 5246 pairs, and only 63 pairs have a nonzero contribution. Clustered shading on the same scene evaluates 2374 pairs. The image is the same in all three cases, value for value. These counts are a measurement on one scene.

## Correctness

The proofs are in the proofs folder. The pixel center of a tile lies on the inner side of all four planes at every depth, because the slope $u$ is an increasing function of the screen position. If a light reaches a pixel, then $\lVert P - c \rVert < r$, and for each unit normal $m$ the Cauchy-Schwarz inequality gives $m \cdot c \ge m \cdot P - \lVert P - c \rVert > -r$. The depth of the pixel is in $[d_{\min}, d_{\max}]$ and differs from $-c_z$ by less than $r$. So no line of the test rejects the light: culling never drops a light that reaches a pixel. Since a dropped light contributes exactly 0, the tiled image equals the brute-force image, and with the lights visited in index order the two floating-point sums are equal too. The tests check both claims at every pixel, with the exact distance test as the reference.

## Complexity

The model is the real RAM, with $p$ pixels, $l$ lights, $t$ tiles and an average of $k$ kept lights per pixel. The depth ranges cost $O(p)$, the culling $O(t l)$ sphere tests, and the shading $O(p k)$ light evaluations. In the worst case every light reaches every tile, and the cost is the $O(p l)$ of brute force. The lists take $O(t l)$ space in the worst case; GPUs reserve a fixed maximum per tile. At 1920 by 1080 pixels with 16-pixel tiles, $t = 120 \cdot 68 = 8160$, so 1000 lights cost about 8.2 million sphere tests per frame.

On a GPU, the gain is also in memory traffic. Each pixel reads its G-buffer record once instead of once per light volume, and all pixels of a tile read the same list, which is good for the [SIMT model](/simt-model/): the threads of a warp run the same loop with the same lights, and their branches agree.

## Properties

- **Conservative.** No light that reaches a pixel is dropped. False positives cost time, not correctness.
- **Sensitive to depth range.** A tile that holds a near object and a far background gets every light between them.
- **Brute force per tile.** Each tile tests every light. With very many lights, the $O(t l)$ term dominates, and a hierarchy over the lights helps.
- **Screen-space only.** The lists depend on the view and are built again each frame.
- **Shared lists.** The pixels of a tile run the same light loop, so the work is coherent on SIMT hardware.

## Variants and improvements

- **Tiled deferred shading.** The lists and the shading are built in one compute pass that reads the G-buffer.
- **Tiled forward shading.** A depth pre-pass gives $d_{\min}$ and $d_{\max}$. The forward pass reads the list of the tile of each fragment. It supports MSAA and transparent surfaces; for transparent fragments, the tile range must reach from the near plane to $d_{\max}$, since they lie in front of the opaque depth. Harada, McKee and Yang (2012) published a renderer of this kind.
- **2.5D culling.** The depth range of the tile is cut into a fixed number of bins, and a bit mask records which bins hold geometry. A light is kept only if its depth range meets an occupied bin. This removes most of the false positives of depth gaps.
- **Tighter tests.** Test the sphere against the bounding box of the tile frustum, or the cone of the tile, to remove corner false positives.
- **Clusters.** Cut the depth into slices as well, and build lists per cluster, see [clustered shading](/clustered-shading/).
- **Other light shapes.** Spot lights use a cone test, and area lights a bounding volume of their range.

## When to use it

Use tiled shading when a scene has tens to thousands of local lights with a limited range, and the depth inside a tile is mostly continuous, as in most indoor scenes and top-down views. Use the forward form when MSAA, transparency or many material types matter. Use clustered shading when tiles often hold a large depth range, for example in first-person views with foliage or long views, or when transparent surfaces need light lists at their own depth.

## Pitfalls

- **No slack in the test.** A plane test in floating point can drop a light that touches the frustum by a rounding error. Add a small slack to the radius.
- **Depth in the wrong space.** The range must be in the same depth as the test. Convert a nonlinear depth buffer value to view depth before the min and max.
- **Background pixels.** Exclude them from the depth range, or the far plane makes the range of every border tile huge.
- **List overflow.** A fixed maximum per tile drops lights when it is full, which breaks the guarantee. Size the list for the worst case or fall back to all lights.
- **Transparent surfaces.** In tiled forward shading, the opaque depth range does not cover them.
- **Lights with no range.** A light with an infinite falloff cannot be culled. Give every local light a radius, and accept the cut as tuning.

## Implementations

## History

Light volumes in deferred shading draw one bounding shape per light and blend the results, which reads the G-buffer once per light. Tiles replace this with one pass that reads the G-buffer once per pixel, which became practical with compute shaders and shared memory on GPUs. Olsson and Assarsson (2011) described tiled deferred and tiled forward shading in a journal paper and studied their cost. Harada, McKee and Yang (2012) showed a forward renderer with a depth pre-pass and per-tile light culling, and argued that it keeps the material freedom of forward shading. Olsson, Billeter and Assarsson (2012) then added depth slices and built clustered shading, noting that the tiled methods test every light against every tile.

## References
