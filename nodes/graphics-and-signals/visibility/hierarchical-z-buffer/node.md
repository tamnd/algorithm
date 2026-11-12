---
tag: EAKK9Q
kind: algorithm
slug: hierarchical-z-buffer
name: Hierarchical z-buffer
aliases:
- Hi-Z
- hierarchical depth buffer
area: graphics-and-signals/visibility
level: advanced
summary: A z-buffer with a pyramid of the farthest depth per square block, so that a whole object or triangle can be proved hidden with a few lookups and skipped.
solves: [hidden-surface-removal]
model: real-ram
complexity:
  vars: {n: the number of objects and triangles tested, W: the image width in pixels, H: the image height in pixels, P: "the number of fragments drawn, after culling", B: "the total area in pixels of the rectangles tested"}
  time: {worst: O(W H + B + (n + P) log(W + H))}
  space: {extra: Θ(W H)}
properties: {stable: true, in_place: false, adaptive: true, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1993
  people: [Ned Greene, Michael Kass, Gavin Miller]
  note: Greene, Kass and Miller put a z-pyramid on the z-buffer in 1993, and used it with an octree of the scene and the visible set of the previous frame to cull hidden geometry.
prereqs: [z-buffer, quadtree]
see_also: [occlusion-culling, early-depth-test, occlusion-query, image-pyramid, octree, visibility-coherence, warnock-algorithm, mipmap]
sources:
  - paper: doi:10.1145/166117.166147
    title: Ned Greene, Michael Kass and Gavin Miller, Hierarchical Z-buffer visibility, SIGGRAPH 1993, pages 231 to 238
    locator: the whole paper (the z-pyramid, the test of a box against it, the octree of the scene and the temporal coherence)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 19.7 (occlusion culling, hierarchical z-buffering) and Section 23.7 (depth culling in hardware, HiZ with zmax and zmin per tile)
---

The hierarchical z-buffer adds a pyramid on top of the [z-buffer](/z-buffer/). Level 0 is the depth buffer. Each entry of the next level holds the *farthest* depth of the $2 \times 2$ entries below it, so the top entry is the farthest depth on the whole screen. An object whose nearest depth is at least the stored depth at every pixel of its screen rectangle cannot change the image, and the pyramid proves this by looking at a few coarse entries. Such an object, or triangle, is skipped before it is rasterized. With the scene drawn roughly front to back, most hidden geometry costs almost nothing. It is a method of [occlusion culling](/occlusion-culling/).

## In plain words

A depth buffer tells, at each dot, how far away the nearest thing drawn so far is. To learn if a new object is hidden, you would have to check every dot it covers.

The hierarchical z-buffer also keeps a coarse summary. For each block of 2 by 2 dots it keeps the farthest distance in the block; for each block of 4 by 4 dots, the farthest of those; and so on, up to one number for the whole screen.

Now if an object is behind the farthest distance of a big block, it is behind every dot of that block. One look answers the question for many dots. Only where the answer is not clear do you look at the smaller blocks. A wall in front of the camera hides everything behind it with one look at the top.

## The problem

The input is a list of objects, each a list of triangles in screen space, and an image of $W \times H$ pixels. A vertex is $(x, y, z)$ with $x$ to the right and $y$ down in pixel units, and $z$ the depth, smaller nearer, affine in $x$ and $y$ on each triangle. Pixel $(i, j)$ is the point sample at $(i + \tfrac12, j + \tfrac12)$, under the [top-left fill rule](/top-left-fill-rule/). The output is the image of the z-buffer: at each pixel, the least depth of a covering triangle and its color, with ties to the first drawn.

The pyramid has levels $0$ to $L$, with $2^L$ the least power of 2 at least $\max(W, H)$. Level $l$ is a grid of side $2^{L - l}$, and its entry $(x, y)$ stands for the block of pixels $[2^l x, 2^l (x + 1)) \times [2^l y, 2^l (y + 1))$. Pixels outside the screen hold $+\infty$. The invariant is that each entry holds the greatest level-0 depth in its block. A query asks, for a rectangle $R$ of pixels and a depth $z_{\min}$, whether $z_{\min} \ge Z_0[p]$ at every pixel $p$ of $R$. The query is exact on rectangles. It is conservative for objects: the rectangle is the bounding box of the pixel centers the object can cover, and $z_{\min}$ is the least vertex depth.

## The algorithm

```pseudo id=main
HIDDEN(R, z_min)                    ▷ is z_min ≥ Z_0 at every pixel of R?
L1  push the root (level L, entry (0, 0)) on a stack
L2  while the stack is not empty do pop an entry e of level l
L3      if the block of e misses R then continue
L4      if z_min ≥ Z_l[e] then continue                ▷ hidden in the whole block
L5      if l = 0 then return false                      ▷ a pixel where it may be visible
L6      push the four children of e
L7  return true

HZB-RENDER(objects)
L8  for each object, in increasing order of its least vertex depth do
L9      if HIDDEN(rectangle of the object, its least depth) then skip the object
L10     for each triangle t of the object: if HIDDEN(rectangle of t, least depth of t) then skip t
L11     for each fragment (p, z) of t: if z < Z_0[p] then WRITE(p, z) and set the color at p

WRITE(p, z)
L12 Z_0[p] ← z
L13 for l = 1 to L: set the entry above p at level l to the max of its four children; stop if it does not change
```

The order of line L8 replaces the octree of the paper: Greene, Kass and Miller walk an [octree](/octree/) of the scene front to back and test each cube against the pyramid before they visit its contents, so a hidden cube culls all the geometry in it. They also draw first the cubes that were visible in the last frame, so that the pyramid holds good occluders early.

## Example

On an $8 \times 8$ screen, a wall at depth 1 covers all pixels, and a box with depths 5 to 6 lies behind it in the pixels 2 to 4 in each direction. The wall has the least depth, so it is drawn first, and every entry of the pyramid becomes 1. The box has $z_{\min} = 5$. The query pops the root, whose block meets the rectangle, and $5 \ge 1$, so line L4 drops it and the stack is empty: the box is hidden after one lookup, and none of its 9 pixels is rasterized.

If the wall had a hole at pixel $(3, 3)$, the depth there would be $+\infty$. Then each entry on the path from the root to $(3, 3)$ would hold $+\infty$, the query would descend along this path, and line L5 would return false at $(3, 3)$: the box is drawn, and the z-buffer gives it that one pixel.

## Correctness

The invariant holds after each write: WRITE changes one level-0 entry and recomputes the max on the path above it, and an entry off the path has an unchanged block. If one recomputed entry does not change, its ancestors do not either. With the invariant, HIDDEN returns true exactly when no level-0 entry in $R$ is greater than $z_{\min}$: line L4 drops a block only when its greatest depth is at most $z_{\min}$, and line L5 finds a pixel of $R$ where the depth is greater. A skipped triangle has every fragment with depth at least $z_{\min}$, which is at least the stored depth at its pixel, and the stored depths only decrease later, so the test $z < Z_0[p]$ would reject every such fragment. So the output equals the z-buffer of all triangles in the order drawn. The proof file gives the details.

## Complexity

A write costs $O(1)$ plus the path above it, $O(\log(W + H))$. A query on a rectangle of $a \times b$ pixels visits at most the entries that meet the rectangle at each level, which is $O(a b + L)$ in total, since the counts form a geometric series with $O(1)$ extra entries per level at the border. When the object is hidden behind a large uniform occluder, the query ends at a coarse level after $O(L)$ visits, independent of $a b$. The total is $O(W H + B + (n + P) \log(W + H))$: clearing, the queries, and the writes with their paths. The pyramid adds a third of the depth buffer, since $\sum_{l \ge 1} 4^{-l} = \tfrac13$.

The gain is in the fragments not drawn. The worst case is a scene with no hidden geometry, where every query fails and the pyramid only adds cost.

## Properties

- **Exact output.** Culling is conservative, so the image is the z-buffer image.
- **Order dependent cost.** The output does not depend on the order, but the culling does: drawn back to front, nothing is culled. A front-to-back order, from a spatial structure or from the last frame, makes it effective.
- **Image-space occlusion.** The occluders are whatever has been drawn, with no special occluder models; this is a property that object-space culling methods do not have.
- **Far depths, not near ones.** The pyramid keeps the farthest depth, because a block hides an object only if all its pixels are nearer. A pyramid of the nearest depths answers the other question: whether an object is in front of everything in a block.

## Variants and improvements

- **Hardware Hi-Z.** GPUs keep, for each tile of pixels, the farthest depth (and often the nearest) in on-chip memory, and test each tile of a triangle against it before the per-pixel [early depth test](/early-depth-test/). With the nearest depth per tile, a tile that is wholly in front can also skip the depth reads. These are one or two levels, not a full pyramid.
- **Hi-Z for GPU-driven culling.** A renderer builds a full max pyramid from the depth buffer of the last frame, or of a first pass with the large occluders, like a [mipmap](/mipmap/) with max in place of the mean, and tests the bounding boxes of objects in a compute shader, choosing the level where the box covers a few texels.
- **Occlusion queries.** An [occlusion query](/occlusion-query/) counts the samples of a box that pass the depth test, which answers the same question with the rasterizer, at the cost of a round trip to the GPU.
- **Coverage masks.** Greene's later hierarchical polygon tiling uses coverage masks in the tiles, which allows conservative culling with less precision of depth.

## When to use it

Use it for scenes with high depth complexity and large occluders, such as cities and interiors, where most geometry is hidden, together with a spatial structure or the last frame to draw near objects first. For scenes where almost everything is visible, the plain z-buffer is cheaper. On modern GPUs the per-tile Hi-Z is built in, and the full pyramid is used for culling whole objects before they are sent to the rasterizer.

## Pitfalls

- **Min and max confused.** Culling needs the farthest depth of a block. Using the nearest depth culls visible objects.
- **A stale pyramid.** After a write, the levels above must be updated before the next query, or the pyramid holds a depth that is too far and culls too little, or, if depths can grow, too near and culls visible objects. Depths that only decrease, as with the test $<$, keep the pyramid conservative.
- **Strict and non-strict tests.** With the depth test $\le$, an object at exactly the stored depth can win, so the cull must use $z_{\min} > Z$, not $\ge$.
- **The last frame's depth.** A pyramid from the last frame is not conservative for the current frame when the camera or objects move; a common fix is a second pass that tests the culled objects against the new depth buffer.
- **Bounds.** The rectangle must hold all pixel centers the object can cover, and $z_{\min}$ must be the least depth after projection, or the cull is not safe.

## Implementations

## History

Greene, Kass and Miller described the hierarchical z-buffer in 1993, with three parts: an octree of the scene in object space, the z-pyramid in image space, and temporal coherence from the visible set of the previous frame. GPUs later added depth culling per tile (HiZ), and renderers that cull on the GPU build the full pyramid in software.

## References
