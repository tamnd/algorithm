---
tag: 82B7J9
kind: algorithm
slug: clustered-shading
name: Clustered shading
aliases:
- clustered light culling
area: graphics-and-signals/real-time-rendering
level: advanced
summary: Group pixels into clusters by screen tile and exponential depth slice, keep a light list for each occupied cluster, and shade each pixel with the lights of its cluster.
model: real-ram
complexity:
  vars: {p: the number of pixels, l: the number of lights, t: the number of occupied clusters, k: the average number of lights kept per pixel}
  time: {keys: O(p), assignment: O(t l), shading: O(p k)}
  space: {lists: O(t l), keys: O(p)}
properties: {deterministic: true, recursive: false, online: false, in_place: false}
history:
  year: 2012
  people: [Ola Olsson, Markus Billeter, Ulf Assarsson]
  note: Olsson, Billeter and Assarsson extended tiled shading with depth slices, and optionally normal cones, in their HPG 2012 paper on clustered deferred and forward shading.
prereqs: [tiled-shading]
see_also: [tiled-shading, deferred-shading, g-buffer, frustum-culling, bounding-volume-hierarchy, morton-encoding, radix-sort, uniform-grid]
sources:
  - paper: doi:10.2312/EGGH/HPG12/087-096
    title: "Ola Olsson, Markus Billeter and Ulf Assarsson, Clustered deferred and forward shading, High-Performance Graphics 2012, 87-96"
    locator: Section 3 (the five steps), Equations 1 and 2 (the exponential depth slices), and Section 3.3 (light assignment with a hierarchy over the lights)
  - paper: doi:10.1080/2151237X.2011.621761
    title: "Ola Olsson and Ulf Assarsson, Tiled shading, Journal of Graphics, GPU, and Game Tools 15(4), 235-251, 2011"
    locator: the tiled method that clustered shading extends, and the effect of the depth range of a tile
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 20, Efficient Shading (the part on clustered shading)
---

Clustered shading is a light culling method that groups the pixels of the screen into clusters in view space. A cluster is a screen tile cut along the depth into one slice of an exponential sequence, so that each cluster is about as deep as it is wide. The method finds the clusters that hold at least one pixel, builds a list of lights for each of them, and shades each pixel with the lights of its cluster. It is the successor of [tiled shading](/tiled-shading/), whose lists cover the whole depth range of a tile: a tile with a near object and a far wall gets every light between them. Clusters cut that range into pieces. Olsson, Billeter and Assarsson published it in 2012 for both [deferred shading](/deferred-shading/) and forward shading.

## In plain words

Tiled shading cuts the screen into squares and gives each square one list of lights. If a square shows a close object and a far wall, the list must hold all lights between them, even the ones that light nothing visible. Clustered shading also cuts the space behind each square into layers, like the floors of a building that gets wider with distance. The layers get thicker farther away, so that each piece is about as deep as it is wide. Only pieces that contain a visible surface get a list. Each pixel then looks up the piece it falls into and uses that list, which is usually shorter.

## The problem

The input is the same as for tiled shading: a depth buffer of $p$ pixels with the view depth $d$ of the visible surface, the surface attributes of each pixel, and $l$ point lights with centers $c_j$ and radii $r_j$. A light reaches a point only if the distance is below its radius. The output is the image with the full sum of light contributions at each pixel, and the goal is short light lists that never miss a light that reaches a pixel.

The camera looks along $-z$, and the page stores the view depth $d = -z$. Pixel centers are at $(i + 1/2, j + 1/2)$. The screen has $S_x \times S_y$ tiles of $T \times T$ pixels, the vertical field of view is $2\theta$ and the near plane is at the depth $n_0$. The paper defines the slices by

$$n_k = n_0 \Big(1 + \frac{2 \tan\theta}{S_y}\Big)^k, \qquad k = \Big\lfloor \frac{\log(d / n_0)}{\log(1 + 2 \tan\theta / S_y)} \Big\rfloor,$$

its Equations 1 and 2. Slice $k$ covers the depths $[n_k, n_{k+1})$.

## The algorithm

The paper gives five steps: render the G-buffer, assign clusters, find the unique clusters, assign lights to clusters, and shade. Lines L1 to L3 are steps 2 and 3, lines L4 to L6 are step 4 and lines L7 to L9 are step 5. $q = 1 + 2 \tan\theta / S_y$. SPHERE-IN-CLUSTER is the test of the tiled shading page with the slab $[n_k, n_{k+1}]$ in place of the depth range of the tile.

```pseudo id=main
CLUSTERED-SHADING(D, G, lights, T)
L1  for each pixel q with geometry
L2      key[q] ← (⌊qx / T⌋, ⌊qy / T⌋, ⌊log(D[q] / n0) / log q⌋)
L3  C ← the set of distinct keys                        ▷ sort, hash, or a flag per cluster
L4  for each cluster κ = (i, j, k) in C
L5      F ← the side planes of tile (i, j);  the slab is [nk, nk+1]
L6      list[κ] ← the lights j with SPHERE-IN-CLUSTER(F, nk, nk+1, cj, rj)
L7  for each pixel q with geometry
L8      c ← the sum of SHADE(G[q], Pq, light j) over j in list[key[q]]
L9      out[q] ← c
```

**The slices (line L2).** The ratio $q$ makes the slices self-similar. A tile is $2 x \tan\theta / S_y$ high at the depth $x$, and slice $k$ has the depth extent $n_{k+1} - n_k = n_k (q - 1)$, which is exactly the tile height at $n_k$. So the clusters are as close to cubes as a frustum cell allows. The number of slices from $n_0$ to the far depth $f$ is $\lceil \log(f / n_0) / \log q \rceil$. With a small $n_0$, many thin slices are spent near the camera, and implementations often start the exponential slices at a larger depth.

**The unique clusters (line L3).** Most of the $S_x S_y$ times (number of slices) clusters hold no pixel. The occupied ones can be found by sorting the keys, or by marking a flag per cluster in a grid and compacting the flags with a [prefix sum](/prefix-sums/). Only these get a list, so the light assignment is not spent on empty space.

**The light assignment (lines L4 to L6).** The simple form tests every light against every occupied cluster, at $O(t l)$ cost. The paper builds a [bounding volume hierarchy](/bounding-volume-hierarchy/) over the lights each frame, sorted by their [Morton codes](/morton-encoding/), and walks it for each cluster, which replaces the brute-force loop over all lights.

**Normals (an option).** The paper can add a quantized normal direction to the key, so that the pixels of a cluster also face about the same way. A light behind all these surfaces can then be culled with a normal cone test. The code of this page does not do this.

## Example

**The slices.** Take $\tan\theta = 1$, $S_y = 4$ tiles in $y$ and $n_0 = 0.5$. Then $q = 1.5$, and the slices start at $0.5$, $0.75$, $1.125$, $1.6875$, $2.531$, $3.797$, $5.695$, $8.543$ and $12.81$. A pixel at depth 3 gets $k = \lfloor \log 6 / \log 1.5 \rfloor = \lfloor 4.42 \rfloor = 4$, the slice $[2.531, 3.797)$. A pixel at depth 12 gets $k = \lfloor \log 24 / \log 1.5 \rfloor = 7$, the slice $[8.543, 12.81)$.

**A depth gap.** A tile shows a box face at depth 3 and a wall at depth 12. Tiled shading gives the tile the range $[3, 12]$. A light at depth 7 with radius $0.5$ covers $[6.5, 7.5]$ and stays in the tile list, though it lights nothing that the tile shows. Here the tile has two occupied clusters, slices 4 and 7. The light meets neither $[2.531, 3.797]$ nor $[8.543, 12.81]$, so both cluster lists drop it.

**A measured scene.** The room of the tests has 32 by 32 pixels, 994 of them with geometry, 60 random lights with radii between $0.3$ and $0.8$, and 8-pixel tiles. Brute force evaluates 59 640 (pixel, light) pairs, tiled shading 5246 and clustered shading 2374, of which 63 give a nonzero contribution. 48 clusters are occupied. All three images are equal value for value. These numbers are a measurement on one scene.

## Correctness

The proofs are in the proofs folder. Equation 2 gives the unique $k$ with $n_k \le d < n_{k+1}$, because $\log q > 0$ and the slice bounds increase with $k$. So the position of a pixel lies in the slab of its cluster, and inside the four side planes of its tile. If a light reaches the pixel, its sphere is not fully outside any of these six boundaries, by the same Cauchy-Schwarz step as in tiled shading. So the list of the cluster holds the light: clustered culling never drops a light that reaches a pixel. A dropped light contributes exactly 0, so the image equals the brute-force image, and with the lights in index order the floating-point sums are equal. The code corrects the slice index of a depth that rounding puts one slice off, so that the claim holds for the computed slices too. The tests check both claims at every pixel.

## Complexity

The model is the real RAM, with $p$ pixels, $l$ lights, $t$ occupied clusters and an average of $k$ kept lights per pixel. The keys cost $O(p)$. The unique clusters cost $O(p)$ expected time with a hash or a flag grid and a prefix sum, or $O(p \log p)$ with a comparison sort ([radix sort](/radix-sort/) on GPUs). The assignment by brute force costs $O(t l)$, and with a hierarchy over the lights it costs $O(l \log l)$ to build plus a walk per cluster whose cost depends on the overlap of lights. The shading costs $O(p k)$. Always $t \le p$, and $t \le S_x S_y \lceil \log(f / n_0) / \log q \rceil$.

The number $t$ is usually a small multiple of the number of tiles, because the visible surfaces in a tile cover few slices. The lists take $O(t l)$ space in the worst case.

## Properties

- **Conservative.** No light that reaches a pixel is dropped.
- **Robust to depth gaps.** A tile with far apart depths gets separate clusters for its surfaces, so lights in the gap are culled.
- **View dependent.** The clusters follow the view frustum and are built each frame. A cluster grid fixed in view space can also be filled without a depth buffer, which forward renderers and transparent surfaces use.
- **Self-similar cells.** With the ratio of Equation 1, each cluster is as deep as it is high at its near face.
- **Indirection.** Each pixel finds its list through its key, which costs a lookup that tiled shading does not need.

## Variants and improvements

- **Clustered forward shading.** The cluster key of a fragment is computed from its own depth, so transparent fragments and MSAA work, and the lists are built for all clusters of a fixed grid or for the clusters a depth pre-pass marks.
- **Tighter bounds.** The real minimum and maximum depth of the pixels inside a cluster can replace the slab bounds, and the side planes can be replaced by the bounding box of the pixel positions.
- **Normal clusters.** A quantized normal in the key, with a cone test against the light, as in the paper.
- **Linear or mixed slices.** Fewer slices near the camera and exponential slices farther away, a common change for wide depth ranges.
- **Light hierarchies.** A hierarchy over the lights, as in the paper, or a [uniform grid](/uniform-grid/) over the lights in view space.

## When to use it

Use clustered shading when tiles often hold surfaces at very different depths, as in first-person views, foliage and long views, or when transparent surfaces and forward materials need light lists at their own depth. Use plain tiled shading when the depth is mostly continuous inside tiles and the extra lookup and the cluster search do not pay. With few lights, neither is needed.

## Pitfalls

- **Slices near the camera.** With a small $n_0$, Equation 1 spends many slices on the first meter. Start the exponential slices at a larger depth and put the near region into one slice.
- **Rounding at slice borders.** The logarithm can put a depth that lies on a slice border into the wrong slice, which can drop a light. Check $k$ against $n_k$ and $n_{k+1}$.
- **Depth space.** Equation 2 needs the linear view depth, not the value of a nonlinear depth buffer.
- **List storage.** The total length of all lists varies by frame. Build it with a count, a [prefix sum](/prefix-sums/) and a fill, or a fixed budget per cluster that can overflow.
- **Cluster grid size.** A finer grid gives shorter lists but more clusters to cull and more memory. The tile size and the number of slices are tuning.

## Implementations

## History

Tiled shading (Olsson and Assarsson 2011) keeps one list per screen tile over the depth range of the tile. Olsson, Billeter and Assarsson (2012) added the depth slices of Equation 1 and the optional normal direction, found only the occupied clusters, and assigned the lights with a hierarchy over the lights in place of the brute-force test of every light against every tile. They showed both a deferred and a forward form. The forward form gives light lists at any depth, which is what transparent surfaces need.

## References
