---
tag: SFEHPC
kind: algorithm
slug: cascaded-shadow-maps
name: Cascaded shadow maps
aliases:
- CSM
- parallel-split shadow maps
area: graphics-and-signals/real-time-rendering
level: core
summary: Split the view frustum into depth ranges and render one shadow map per range, so that shadow resolution follows the distance to the eye.
solves: [shadow-determination]
model: real-ram
complexity:
  vars: {m: the number of cascades, N: the map side in texels, t: the number of triangles, P: "the number of covered texel centers, summed over all triangles and cascades", q: the number of shadow lookups}
  time: {worst: Θ(m N^2 + m t + P + q)}
  space: {extra: Θ(m N^2)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 2006
  people: [Wolfgang Engel, Fan Zhang, Hanqiu Sun, Leilei Xu, Lee Kit Lun]
  note: Engel described cascaded shadow maps in ShaderX5 in 2006, and Zhang, Sun, Xu and Lun published a split scheme that blends logarithmic and uniform splits in the same year.
prereqs: [shadow-mapping, frustum-culling]
see_also: [percentage-closer-filtering, variance-shadow-maps, moment-shadow-mapping, percentage-closer-soft-shadows, level-of-detail, texture-clipmap, z-fighting]
sources:
  - book: isbn:9781584504993
    title: Wolfgang Engel (editor), ShaderX5, Advanced Rendering Techniques, Charles River Media, 2006, Wolfgang Engel, Cascaded Shadow Maps, 197 to 206
    locator: the whole chapter (the slices of the view frustum, one map per slice, and the choice of the map per pixel)
  - paper: doi:10.1145/1128923.1128975
    title: Fan Zhang, Hanqiu Sun, Leilei Xu and Lee Kit Lun, Parallel-split shadow maps for large-scale virtual environments, Proceedings of the 2006 ACM International Conference on Virtual Reality Continuum and Its Applications (VRCIA 2006), 311 to 318
    locator: the practical split scheme (the blend of the logarithmic and the uniform split) and the fit of each map to its slice
  - book: isbn:9780321515261
    title: Hubert Nguyen (editor), GPU Gems 3, Addison-Wesley, 2007, Chapter 10, Fan Zhang, Hanqiu Sun and Oskari Nyman, Parallel-Split Shadow Maps on Programmable GPUs
    locator: the split scheme with lambda = 0.5, the logarithmic split as the split that distributes the perspective aliasing evenly, and the crop matrix of each slice
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 7.4 (the part on cascaded shadow maps)
---

Cascaded shadow maps cut the view frustum of the camera into $m$ slices by depth and give each slice its own [shadow map](/shadow-mapping/), cropped to the slice as seen from the light. A pixel uses the map of its slice. Near slices are small, so their texels are small, and the shadow resolution falls with the distance from the camera, as the pixel size of the camera grows. The test per pixel is the test of plain shadow mapping; only the choice of map and the crop are new. This is a [level of detail](/level-of-detail/) scheme for shadows, close to the [texture clipmap](/texture-clipmap/), which also keeps finer data near the viewer.

## In plain words

One shadow map for a whole landscape has the same dots everywhere. Near the camera, one dot of the map covers many screen pixels, and the shadow edges look like steps. Far away, many dots fall on one pixel and are wasted.

So cut the space in front of the camera into a few slabs: a thin one near the camera, then thicker ones. Make one shadow map for each slab, and fit it tightly around that slab as the sun sees it. The near map covers a small area, so its dots are small. The far map covers a large area with large dots, where the camera cannot see the difference.

When you draw a point, find out which slab it is in, and look in that map.

## The problem

The camera has the near plane at view depth $n$ and the far plane at $f$, and it looks along $-z$ of its frame, with $y$ up in the world. The light is directional, with an orthonormal frame $R$; a point $p$ has the light coordinates $q = R p$, and $-q_z$ is its light depth, larger farther from the light. The input is the scene, the camera, the light, the number of cascades $m$, a blend $\lambda \in [0, 1]$ and a map size of $N \times N$ texels. The output is, for each visible point, the shadow mapping answer from a map whose texels are small where the camera is close. Each map is a z-buffer of the scene from the light, cropped to the light $(x, y)$ rectangle of one slice of the view frustum, and it stores linear light depth.

## The algorithm

```pseudo id=main
CSM-RENDER(camera, R, scene, n, f, m, λ, N)
L1  C_i ← λ n (f/n)^(i/m) + (1 - λ)(n + (f - n) i/m) for i = 0, ..., m   ▷ the split depths
L2  for i ← 0 to m - 1 do
L3      Q ← the 8 corners of the view slice between depths C_i and C_(i+1), mapped by R
L4      lo_i, hi_i ← the least and the greatest light (x, y) over Q; texel_i ← (hi_i - lo_i) / N
L5      S_i ← the light depth map of the scene over the rectangle [lo_i, hi_i], at N x N texel centers

CSM-SHADOWED(p, bias)
L6  i ← the cascade with C_i ≤ depth(p) < C_(i+1)          ▷ none: p is lit
L7  q ← R p; (a, b) ← (⌊(q_x - lo_x) / texel_x⌋, ⌊(q_y - lo_y) / texel_y⌋)   ▷ outside the map: lit
L8  return S_i[a, b] < -q_z - bias                        ▷ the test of shadow mapping
```

Line L1 is the split scheme of Zhang and coauthors. With $\lambda = 1$ the split is logarithmic: every slice has the same ratio $C_{i+1}/C_i$. With $\lambda = 0$ it is uniform. The value $\lambda = 0.5$ of GPU Gems 3 is a tuning. Lines L3 and L4 are the crop: the slice is a convex box with 8 corners, so the rectangle of its corners in the light plane holds the light $(x, y)$ of every point of the slice. Line L5 must still draw all shadow casters between the light and the slice, also those outside the view frustum, so its depth range extends toward the light; only $x$ and $y$ are cropped.

A renderer often uses a *stable fit* in place of lines L3 and L4. It fits a square around a sphere that holds the slice, rounds the radius up to a multiple of a quantum, and snaps the lower corner to whole texels. The texels then keep their size and their grid in the world when the camera turns or moves, and shadow edges do not crawl. The quantum, $1/64$ in the code, is a tuning.

## Example

Take $n = 1$, $f = 100$ and $m = 4$.

| scheme | $C_0$ | $C_1$ | $C_2$ | $C_3$ | $C_4$ |
|---|---|---|---|---|---|
| logarithmic, $\lambda = 1$ | 1 | 3.162 | 10 | 31.62 | 100 |
| practical, $\lambda = 0.5$ | 1 | 14.456 | 30.25 | 53.436 | 100 |
| uniform, $\lambda = 0$ | 1 | 25.75 | 50.5 | 75.25 | 100 |

The logarithmic split makes the first slice very thin, and the uniform split puts most of the resolution far away; the blend lies between them, slice by slice.

Now a camera at $(0, 3, 0)$ looks along $(0, -0.3, -1)$ with a vertical field of view of $60°$ and the aspect ratio 1, with $n = 0.5$ and $f = 40$. The light comes from the direction $(0.3, -1, 0.2)$, and each map has $64 \times 64$ texels. The splits for $\lambda = 0.5$ are 0.5, 5.935, 12.361, 21.75 and 40. The texel sizes in world units are:

| map | texel $x$ | texel $y$ | stable fit |
|---|---|---|---|
| cascade 0 | 0.132 | 0.0938 | 0.1766 |
| cascade 1 | 0.275 | 0.1267 | 0.3363 |
| cascade 2 | 0.4839 | 0.196 | 0.5833 |
| cascade 3 | 0.8899 | 0.3742 | 1.0769 |
| one map for all of $[0.5, 40]$ | 0.8899 | 0.6724 | |

The first cascade has texels 6.7 times smaller in $x$ and 7.2 times smaller in $y$ than one map of the same size for the whole frustum. The stable fit costs a factor of 1.21 to 1.34 in texel size here, and it removes the crawl of the edges.

## Correctness

The proof file shows four claims, and the tests check them.

- **The splits.** $C_0 = n$, $C_m = f$, and the $C_i$ increase strictly, so each view depth in $[n, f)$ has exactly one cascade in line L6. The test checks this and that the practical split lies between the logarithmic and the uniform split.
- **Why logarithmic.** In a model in which the texel size of a slice is proportional to its length and the pixel footprint to the depth, the logarithmic split gives the smallest largest ratio of the two. This is a model, not a theorem on scenes.
- **Containment.** Every point of slice $i$ maps into the rectangle of map $i$, for the tight fit and for the stable fit. The test samples points of each slice.
- **The lookup.** Lines L6 to L8 are the test of shadow mapping against one map, so its correctness result applies: at a texel center with bias 0 the answer is exact, and away from shadow edges by more than half a texel diagonal it is exact as well. The test compares the lookup with ray casting against the spheres of a scene at such points.

The proof file also shows that the stable fit keeps the texel size and the texel grid fixed when the camera moves.

## Complexity

Each cascade is a depth pass over the scene: $\Theta(N^2)$ to clear, $\Theta(t)$ for the triangles and the covered texel centers, so the $m$ passes cost $\Theta(m N^2 + m t + P)$, with [frustum culling](/frustum-culling/) per cascade to reduce $t$. A lookup costs $O(m)$ to find the cascade by a scan, or $O(1)$ with a compare against the split depths in a vector, plus the cost of the filter. The total is $\Theta(m N^2 + m t + P + q)$ in the worst case, and the maps take $\Theta(m N^2)$ space, often as the layers of one texture array.

## Properties

- **Resolution follows the depth.** The texel size grows with the slice, as the pixel size of the camera grows with the depth (a measured effect in the example, and a model argument in the proof file).
- **Perspective aliasing reduced, projective aliasing not.** The slices fix the mismatch caused by the camera's perspective. Surfaces almost parallel to the light still get stretched texels.
- **Seams.** At a split depth, the texel size jumps, and a filtered shadow edge can change its look.
- **Cost grows with $m$.** Each cascade draws the scene again from the light, and the casters near the light are drawn into several maps.

## Variants and improvements

- **Stable fit.** Fit to a bounding sphere, round the radius and snap to texels, as described above, at the cost of larger texels.
- **Tighter crops.** Fit each map to the visible receivers in the slice, found from the depth buffer of the camera, in place of the whole slice (sample distribution shadow maps).
- **Blending at the splits.** Look in two maps near a split and blend the answers, to hide the seam.
- **Filtering per cascade.** Use [PCF](/percentage-closer-filtering/), [variance shadow maps](/variance-shadow-maps/) or [moment shadow mapping](/moment-shadow-mapping/) per map, with a filter width scaled by the texel size of the cascade.
- **Warped maps.** Perspective and light space perspective shadow maps warp one map in place of several; they can be combined with slices.

## When to use it

Use cascaded shadow maps for a directional light, such as the sun, over a large scene with a view that reaches far: outdoor games, flight and driving views, terrain. For a small scene or a spot light, one map is usually enough. For very large views, combine them with a coarse map for the distance, or with baked shadows.

## Pitfalls

- **Radial distance in place of depth.** If line L6 picks the cascade by the distance $|p - \text{eye}|$, a point near the edge of the screen in slice $i$ can get cascade $i + 1$, whose map does not hold it, and the point is called lit.
- **Cropping the light depth.** If line L5 also clips the light depth to the slice, casters outside the view frustum (a tall building behind the camera) cast no shadow into it.
- **One bias for all cascades.** The bias of line L8 must grow with the texel size of the cascade; a bias set for cascade 0 gives acne in cascade 3, and a bias set for cascade 3 gives peter panning near the camera.
- **Tight fit with a moving camera.** Lines L3 and L4 change the size and the position of the texels in every frame, so the shadow edges shimmer when the camera turns. Use the stable fit.
- **Too thin a first slice.** With $\lambda$ near 1 in line L1 and a small $n$, the first slice is very thin, and most pixels near the camera fall in the second one.

## Implementations

## History

Engel described cascaded shadow maps in ShaderX5 in 2006, as a set of maps for slices of the view frustum. In the same year Zhang, Sun, Xu and Lun published their method with the split scheme that blends a logarithmic and a uniform split, and Zhang, Sun and Nyman described its GPU form in GPU Gems 3 in 2007. Later work added the stable fit, cascades fit to the visible samples, and the blend between cascades. The method became the standard way to draw sun shadows in games.

## References
