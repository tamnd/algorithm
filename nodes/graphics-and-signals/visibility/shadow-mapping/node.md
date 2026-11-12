---
tag: 4VKYK3
kind: algorithm
slug: shadow-mapping
name: Shadow mapping
aliases:
- depth-map shadows
- Williams shadow mapping
area: graphics-and-signals/visibility
level: core
summary: Draw a depth buffer from the light. A point is in shadow when its depth from the light is greater than the depth stored at its place in that map.
solves: [shadow-determination]
model: real-ram
complexity:
  vars: {n: the number of triangles, W: the map width in texels, H: the map height in texels, P: "the number of covered texel centers, summed over all triangles", q: the number of shadow lookups, r: the filter radius in texels}
  time: {worst: Θ(W H + n + P + q (r + 1)^2)}
  space: {extra: Θ(W H)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1978
  people: [Lance Williams]
  note: Williams described shadows from a depth map in 1978. Reeves, Salesin and Cook added percentage-closer filtering in 1987.
prereqs: [z-buffer]
see_also: [shadow-volume-algorithm, z-fighting, mipmap, texture-mapping, silhouette-edge, perspective-correct-interpolation]
sources:
  - paper: doi:10.1145/965139.807402
    title: Lance Williams, Casting curved shadows on curved surfaces, Computer Graphics 12(3), SIGGRAPH 1978, pages 270 to 274
    locator: the whole paper (the depth image from the light and the comparison of each visible point with it)
  - paper: doi:10.1145/37401.37435
    title: William T. Reeves, David H. Salesin and Robert L. Cook, Rendering antialiased shadows with depth maps, Computer Graphics 21(4), SIGGRAPH 1987, pages 283 to 291
    locator: the sections on percentage-closer filtering and on the bias
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 7.4 (shadow maps, the bias and the aliasing) and Section 7.5 (percentage-closer filtering)
---

Shadow mapping solves [shadow determination](/shadow-determination/) with a [z-buffer](/z-buffer/) drawn from the light. The first pass stores, at each texel of the map, the depth of the nearest surface as seen from the light. The second pass maps each visible point into the light's view and calls it shadowed when its depth is greater than the stored depth there. It works for any geometry that can be rasterized, but it needs a depth bias against false self-shadowing, and the finite resolution of the map causes aliasing at the shadow edges.

## In plain words

Put a camera where the lamp is, and take a picture of the scene. At each dot keep only how far away the nearest thing is. That is the shadow map: the things in it are lit.

Now draw the scene from the real camera. For each point you draw, ask: how far is this point from the lamp, and what distance did the lamp's picture store in that direction? If the point is farther than the stored distance, something nearer to the lamp is in the way, and the point is in shadow. If not, the point is lit.

The map has a limited number of dots, so the edge of a shadow can look like steps. A point also compares with a stored value that is a little off, so it can shadow itself. A small extra distance in the test fixes this.

## The problem

The input is a list of $n$ triangles in world space, a point light or a directional light, and a set of $q$ query points (the points that the camera sees). The output is, for each query point $p$, whether the segment from $p$ to the light meets a surface nearer to the light. This is [shadow determination](/shadow-determination/) for one light, sampled at the light's texels.

The *light transform* $M$ is a $4 \times 4$ matrix. For a world point $p$, $M (p, 1)^T = (h_x, h_y, h_z, h_w)$, and $(x, y, z) = (h_x, h_y, h_z)/h_w$. Here $x$ and $y$ are texel coordinates of a $W \times H$ map, with $x$ to the right and $y$ down, and $z$ is the depth from the light, smaller nearer. An orthographic light (a directional light) has last row $(0, 0, 0, 1)$; a perspective light (a spot light) divides by the distance along its axis. Every point is in front of the light, $h_w > 0$, so no clipping is needed. On each triangle, $z$ is affine in $x$ and $y$, as the depth after a perspective divide is.

Texel $(i, j)$ is the point sample at its center $(i + \tfrac12, j + \tfrac12)$, under the [top-left fill rule](/top-left-fill-rule/). A query point whose $(x, y)$ is outside the map is lit: this is the border rule. The answer is exact when the query point is at a texel center and the bias is 0, as the correctness proof shows; elsewhere it is an approximation of the true answer.

## The algorithm

```pseudo id=main
SHADOW-MAP(W, H, T, M)                          ▷ pass 1, from the light
L1  for each texel (i, j) do S[i, j] ← +∞
L2  for each triangle t in T do
L3      t' ← t with each vertex mapped by M and divided by h_w
L4      for each texel center that t' covers, with depth z do S[i, j] ← min(S[i, j], z)
    return S

SHADOWED(S, M, p, b)                             ▷ pass 2, for a point p, with bias b
L5  (x, y, z) ← M (p, 1) divided by h_w
L6  (i, j) ← (⌊x⌋, ⌊y⌋)                          ▷ the texel that holds (x, y)
L7  return z − b > S[i, j]                        ▷ false outside the map

PCF(S, M, p, b, r)                               ▷ percentage-closer filtering
L8  (x, y, z) ← M (p, 1) divided by h_w, (i, j) ← (⌊x⌋, ⌊y⌋)
L9  h ← the number of (u, v) in [−r, r]^2 with z − b > S[i + u, j + v]
L10 return h / (2r + 1)^2                         ▷ the fraction in shadow
```

Pass 1 is the [z-buffer](/z-buffer/) without the color buffer. In a renderer, pass 2 runs in the fragment shader of the camera pass: each fragment computes its light-space position by [perspective-correct interpolation](/perspective-correct-interpolation/), and the shadow test is a [texture](/texture-mapping/) lookup with a compare. PCF filters the results of the comparison. Filtering the depths first and comparing once gives a value that is not the fraction of shadowed samples, as Reeves, Salesin and Cook show; this is why the method compares first.

## Example

An orthographic light looks along $+z$ at a floor $z = 5$ that covers the $8 \times 8$ map, and at the top of a box, $z = 2$, over the square $[2, 6] \times [2, 6]$.

| texel | stored depth |
|---|---|
| $(0, 0)$ | 5 |
| $(2, 2)$ | 2 |
| $(5, 5)$ | 2 |
| $(6, 6)$ | 5 |

The floor point $(4, 4, 5)$ maps to texel $(4, 4)$, where 2 is stored; $5 > 2$, so it is in shadow. The floor point $(1, 1, 5)$ maps to texel $(1, 1)$, where 5 is stored; $5 > 5$ is false, so it is lit, and the strict test lets a surface not shadow itself at a texel center. The box top $(4, 4, 2)$ is lit. With $r = 1$, PCF at the floor point $(2.5, 2.5, 5)$ looks at texels 1 to 3 in each direction; 4 of the 9 hold 2, so it returns $4/9$, a soft edge.

**Shadow acne.** Tilt the floor to depth $5 + x/2$, with no box. Texel $(1, 1)$ stores the depth at its center, $5 + 1.5/2 = 5.75$. The floor point $(1.9, 1.2, 5.95)$ maps to that texel, and $5.95 > 5.75$, so the floor shadows itself there. With $b = 0$, each floor point to the right of its texel center is shadowed, which is half of the floor, in stripes. The depth slope is $\tfrac12$ per texel and a point is at most half a texel from the center in $x$, so with $b = \tfrac14$ no floor point is shadowed.

**Peter panning.** A thin sheet at depth $5.875$ lies $\tfrac18$ above a floor at depth 6. The floor point under the sheet is in shadow with $b = 0$, but lit with $b = \tfrac14$: a bias larger than the gap removes the contact shadow, and the object seems to float.

## Correctness

Pass 1 is a z-buffer from the light, so $S[i, j]$ is the least depth at the center of texel $(i, j)$ over the triangles that cover it, by the [z-buffer](/z-buffer/) proof. The light transform is a projective map with $h_w > 0$, so it takes the segment from a point to the light to the set of points with the same $(x, y)$ and a smaller depth. So for a query point $p$ that maps to a texel center with depth $z$, the test $z > S[i, j]$ holds exactly when some surface meets that segment strictly nearer to the light. At other points the test compares with the depth at the nearest texel center, which is the source of both acne and aliasing. The proof file gives the details and the bound on the bias for a planar receiver.

## Complexity

Pass 1 costs $\Theta(W H + n + P)$, as a z-buffer of $W \times H$ texels. Each lookup costs $O(1)$ for a point, and PCF costs $\Theta((2r + 1)^2)$. The total for $q$ lookups is $\Theta(W H + n + P + q (r + 1)^2)$. The map takes $\Theta(W H)$ space. A point light that shines in all directions needs six maps (a cube), and each light needs its own map.

## Properties

- **Image space from the light.** The method samples the light's view, so its error is in units of texels, not of the scene. See [object space and image space](/object-space-vs-image-space/).
- **Any geometry.** Whatever the rasterizer can draw casts and receives shadows, with no silhouette edges and no closed meshes. This is the main difference from the [shadow volume algorithm](/shadow-volume-algorithm/), which builds volumes from the [silhouette edges](/silhouette-edge/) and is exact per pixel, but needs closed meshes and much fill rate.
- **Hard shadows.** The test is binary, for a point light. PCF smooths the edge, but the width of the soft edge is set by $r$, not by the size of the light.
- **Aliasing.** When a texel of the map covers many pixels of the camera image, the shadow edge shows steps. This happens near the camera with a directional light (perspective aliasing) and on surfaces almost parallel to the light (projective aliasing).
- **Bias.** The bias $b$ must be at least the depth change across half a texel on the receiver, or the receiver shadows itself; a larger $b$ removes contact shadows. The same precision problem as [z-fighting](/z-fighting/).

## Variants and improvements

- **Percentage-closer filtering.** Reeves, Salesin and Cook (1987): average the binary tests over a neighborhood, as in lines L8 to L10. GPUs do a $2 \times 2$ bilinear PCF in one lookup.
- **Slope-scaled bias.** Make the bias grow with the depth slope of the receiver in light space, so that steep surfaces get more bias and flat ones less.
- **Normal offset.** Move the query point a little along the surface normal before the lookup, in place of a depth bias.
- **Cascaded maps.** Use several maps for ranges of distance from the camera, so that near surfaces get more texels.
- **Warped maps.** Perspective shadow maps (Stamminger and Drettakis, 2002) draw the map in the camera's post-perspective space, which puts more texels near the camera.
- **Filterable maps.** Variance shadow maps (Donnelly and Lauritzen, 2006) store the depth and its square, so the map can be filtered and [mipmapped](/mipmap/), and estimate the shadowed fraction with Chebyshev's inequality. They leak light where depths vary a lot.
- **Exact shadows from a light view.** The irregular z-buffer stores the exact query points in the light's grid and rasterizes the occluders against them, which removes the aliasing.

## When to use it

Use shadow maps for real-time shadows of large, complex or animated scenes, in particular with geometry that is not closed (foliage, alpha-tested textures). They are the default in games. Use [shadow volumes](/shadow-volume-algorithm/) or ray-traced shadows when the shadows must be exact at each pixel, and ray-traced or filtered soft-shadow methods for area lights.

## Pitfalls

- **No bias.** With $b = 0$, a lit surface compares with its own depth at a texel center and shadows itself in a pattern of stripes (shadow acne).
- **Too much bias.** A large bias removes the shadow where an object touches the floor (peter panning).
- **Filtering the depths.** Bilinear filtering of the depth map, then one compare, is wrong at depth edges. Compare first, then filter (PCF).
- **The map border.** A point outside the map must have a defined answer: lit, as here, or the value of the nearest edge texel (clamp). With clamp, a shadow at the border of the map is stretched across the scene.
- **Near and far planes of the light.** The light's depth precision follows the same rules as the camera's: a near plane too close to the light wastes the depth range. See [z-fighting](/z-fighting/).
- **Back faces.** Drawing only the back faces into the map moves the stored depth away from the lit front faces, which reduces acne for closed meshes, but fails for thin open geometry.

## Implementations

## History

Williams described the method in 1978, for curved surfaces in a software renderer: a depth image from the light, then a test of each visible point against it. Reeves, Salesin and Cook added percentage-closer filtering in 1987, for antialiased shadows in film rendering. With depth textures and hardware compare in GPUs, shadow maps became the standard method of real-time shadows.

## References
