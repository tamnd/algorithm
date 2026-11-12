---
tag: 5FR13Q
kind: algorithm
slug: painters-algorithm
name: Painter's algorithm
aliases:
- depth sort
- depth-sorting algorithm
area: graphics-and-signals/visibility
level: intro
summary: Sort the polygons by depth and paint them farthest first, so that nearer polygons overwrite farther ones. Correct when the order is a valid visibility order.
solves: [hidden-surface-removal]
model: real-ram
complexity:
  vars: {n: the number of polygons, P: "the number of covered pixels, summed over all polygons"}
  time: {worst: Θ(n log n + P), average: Θ(n log n + P), best: Θ(n log n + P)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1972
  people: [Martin E. Newell, Richard G. Newell, Tom L. Sancha]
  note: The idea of painting far objects first is old. Newell, Newell and Sancha made the depth sort a hidden surface method in 1972, with extra tests and splits that repair the order where the simple sort fails.
prereqs: [hidden-surface-removal, sorting-problem, polygon]
see_also: [newell-newell-sancha-algorithm, bsp-tree-visibility, bsp-tree, z-buffer, object-space-vs-image-space, topological-sort, a-buffer, depth-peeling]
sources:
  - paper: doi:10.1145/356625.356626
    title: Ivan E. Sutherland, Robert F. Sproull and Robert A. Schumacker, A characterization of ten hidden-surface algorithms, ACM Computing Surveys 6(1), 1974, pages 1 to 55
    locator: the sections on priority (list) algorithms and on the Newell, Newell and Sancha algorithm
  - paper: doi:10.1145/800193.569954
    title: M. E. Newell, R. G. Newell and T. L. Sancha, A solution to the hidden surface problem, Proceedings of the ACM Annual Conference 1972, pages 443 to 450
    locator: the whole paper
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, 1990
    locator: Chapter 15, Section 15.5 (list-priority algorithms, the depth-sort algorithm)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, 2008
    locator: Chapter 12, the introduction (the painter's algorithm and why a depth order can fail)
---

The painter's algorithm draws a scene of polygons by sorting them by depth and painting them from the farthest to the nearest, so that each polygon overwrites what lies behind it. It solves [hidden surface removal](/hidden-surface-removal/) with no depth value per pixel, unlike the [z-buffer](/z-buffer/). The result is correct when the order is a *valid visibility order*, for example when the depth ranges of the polygons do not overlap. When the ranges overlap the sort can be wrong, and for cyclic overlap no order is correct. The [Newell-Newell-Sancha algorithm](/newell-newell-sancha-algorithm/) and [BSP tree visibility](/bsp-tree-visibility/) repair this by tests and splits.

## In plain words

A painter who paints a landscape first paints the sky, then the hills, then the trees, and last the house at the front. Each new layer of paint covers the old paint where they overlap. So the painter never has to decide which parts of the hills are hidden. The new paint hides them.

The computer does the same with the flat pieces of a scene. It sorts the pieces from far to near and draws them in that order. A near piece drawn later covers a far piece drawn earlier.

The method fails when no piece is wholly behind the other. Two long planks that cross, or three that overlap in a ring, have no correct order. One sort key per piece cannot tell which part of a piece is in front.

## The problem

The input is a list of $n$ planar [convex polygons](/convex-polygon/) $p_0, \ldots, p_{n-1}$ in screen space, and an image of $W \times H$ [pixels](/pixel/). The viewer looks down the $z$ axis from $z = +\infty$, so a larger $z$ is nearer. This is an orthographic view; a perspective view is first changed to this form by the projection. The plane of each polygon is not parallel to the $z$ axis, so it has a depth $z_p(x, y)$ at each point $(x, y)$ of its projection.

Pixel $(i, j)$ is a point sample at its center $c = (i + \tfrac12, j + \tfrac12)$. A polygon *covers* the pixel when $c$ lies in the closed projection of the polygon onto the $xy$ plane. The output is, at each pixel, the polygon with the largest depth $z_p(c)$ among those that cover it, or the background if none covers it. If two polygons tie for the largest depth, either answer is acceptable.

An order of the polygons is a *valid visibility order* when, for each pixel $c$ and each two polygons $p$ before $q$ that both cover $c$, $z_p(c) \le z_q(c)$. Thus no polygon hides a part of a polygon that comes later.

## The algorithm

```pseudo id=main
PAINTER(p[0 .. n − 1], W, H)
L1  for each polygon p do key[p] ← the least z of a vertex of p      ▷ its farthest point
L2  order ← the indices sorted by key, ascending, with a stable sort
L3  fill the image with the background
L4  for each p in order do
L5      for each pixel (i, j) whose center (i + 1/2, j + 1/2) is in the projection of p do
L6          image[j][i] ← p                                          ▷ overwrite
L7  return image
```

Line L1 computes the sort key of each polygon. Here the key is the depth of its farthest point; other choices, such as the centroid depth, are also common, and each fails in some cases. Line L2 sorts the polygons from far to near. Lines L4 to L6 paint each polygon over the image. In practice line L5 is a [scan conversion](/polygon-scan-conversion/) of the polygon, which visits only the covered pixels. The implementation on this page tests each pixel center, which is slower but simpler to check.

## Example

Take an image of $8 \times 6$ pixels and three polygons parallel to the screen. $A$ is the rectangle with corners $(0, 0)$ and $(6, 4)$ at $z = 1$. $B$ is the triangle $(3, 1), (8, 1), (5, 6)$ at $z = 3$. $C$ is the triangle $(1, 2), (5, 2), (1, 6)$ at $z = 5$. The keys are 1, 3 and 5, so the order is $A, B, C$.

| step | polygon | pixels covered | pixels overwritten | pixels of A, B, C, background after the step |
|---|---|---|---|---|
| start | | | | 0, 0, 0, 48 |
| 1 | A | 24 | 0 | 24, 0, 0, 24 |
| 2 | B | 13 | 7 | 17, 13, 0, 18 |
| 3 | C | 10 | 7 | 11, 12, 10, 15 |

Step 2 overwrites 7 pixels of $A$ and step 3 overwrites 7 pixels of $A$ and $B$. The final image, with row $j = 5$ at the top and `.` for the background, is:

```
.C......
.CC.BB..
ACCCBBB.
ACCCCBB.
AAABBBBB
AAAAAA..
```

A per-pixel depth test gives the same image, because the depth ranges $[1, 1]$, $[3, 3]$ and $[5, 5]$ are disjoint.

**A failure.** Let $D$ be the rectangle $(0, 0)$ to $(8, 6)$ on the tilted plane $z = x$, so its depth goes from 0 at the left edge to 8 at the right edge. Let $E$ be the small square $(5, 1)$ to $(7, 3)$ at $z = 5$. The keys are 0 for $D$ and 5 for $E$, so the sort paints $D$ first and $E$ last. But at the four pixels with $i \in \{5, 6\}$ and $j \in \{1, 2\}$, $D$ has depth 5.5 or 6.5, which is nearer than 5. The image shows $E$ there, and these four pixels are wrong. The order $E, D$ is correct, so a valid order exists here, but the sort by key does not find it.

**A cycle.** Three thin quadrilaterals can each lie in front of the next one where they cross: $s_1$ in front of $s_2$, $s_2$ in front of $s_3$ and $s_3$ in front of $s_1$. The tests of this page check all six orders of such a scene against a per-pixel depth test, and each order gives a wrong pixel. No sort key can work; a polygon must be split.

## Correctness

The image at a pixel is the last polygon in the order that covers it. If the order is a valid visibility order, the last such polygon has the largest depth among them, so the image is correct. The sort by key gives a valid order when the polygons have pairwise disjoint depth ranges: if $p$ sorts before $q$, then each depth of $p$ is less than each depth of $q$. Conversely, a wrong pixel needs two polygons whose depth ranges overlap. The proofs are below.

## Complexity

Line L1 takes $\Theta(k)$ time for a polygon with $k$ vertices, and line L2 takes $\Theta(n \log n)$ time with a comparison sort. With scan conversion, lines L4 to L6 take time proportional to $P$, the number of covered pixels summed over all polygons, plus the number of edges. So the time is $\Theta(n \log n + P)$ in each case. The overdraw $P$ can be much larger than $WH$: a stack of $n$ full-screen polygons gives $P = nWH$, and the method writes each pixel $n$ times. The extra space is $\Theta(n)$ for the keys and the order, and no depth buffer is necessary.

The implementation tests all $WH$ pixel centers for each polygon, so its time is $\Theta(n \log n + nWHk)$ for polygons with at most $k$ vertices.

## Properties

- **Object space order, image space output.** The sort works on polygons, and the painting works on pixels. See [object space and image space](/object-space-vs-image-space/).
- **Not exact.** The output can be wrong when depth ranges overlap. No choice of one key per polygon removes the error, because cyclic overlap has no valid order.
- **No depth buffer.** The memory is the image and the order. This was important when memory was expensive.
- **Overdraw.** Each covered pixel is written once per polygon, even if a later polygon hides it.
- **Transparency.** Because the order is back to front, the method can blend translucent polygons with the *over* operator. The [z-buffer](/z-buffer/) cannot do this without an order.

## Variants and improvements

- **Newell-Newell-Sancha.** After the sort, test each polygon against the polygons that overlap it in depth, reorder them, and split polygons where no order exists. See [the Newell-Newell-Sancha algorithm](/newell-newell-sancha-algorithm/).
- **BSP order.** Build a [BSP tree](/bsp-tree/) of the polygons once. A traversal of the tree gives a valid order for each viewpoint. See [BSP tree visibility](/bsp-tree-visibility/).
- **Fixed priority.** For a scene that does not change, compute a priority order of clusters once, as in early flight simulators.
- **Reverse painter's algorithm.** Draw front to back, and write a pixel only if it is still empty. This gives the same image for a valid order, and it can stop when all pixels are full.
- **Depth sort of transparent objects.** Renderers draw the opaque part with a z-buffer, then sort the transparent polygons back to front. Exact methods for transparency, such as [depth peeling](/depth-peeling/) and the [A-buffer](/a-buffer/), avoid the sort.

## When to use it

Use the painter's algorithm when the scene is small or its depth order is known, for example layers in 2D graphics, sprites, or a terrain drawn from a height map in a fixed direction. Use it for translucent polygons that you blend. For a general 3D scene, use the [z-buffer](/z-buffer/), which is correct for each input, or a [BSP tree](/bsp-tree-visibility/) if you need a correct order.

## Pitfalls

- **Assuming that a sort is enough.** The sort of line L2 does not give a valid order when depth ranges overlap. The failure example above has a valid order that the sort misses, and a cycle has no valid order. Use a repair step, a BSP tree or a z-buffer when the scene is general.
- **Sorting in the wrong direction.** If line L2 sorts with the nearest polygon first, far polygons overwrite near ones. With the convention that a larger $z$ is nearer, sort by ascending key. Many systems use the opposite convention, with a larger depth farther away; then sort by descending depth.
- **Trusting a better key.** The centroid depth or the nearest vertex depth does not fix the failure. In the example, $D$ has its centroid at depth 4, which is still before $E$ at depth 5. Only tests between pairs of polygons can find the right order.
- **Polygons that cross.** Two polygons that cut through each other have no valid order. Split one of them along the line where they meet.

## Implementations

## History

The idea of painting far objects first is as old as painting. Early flight simulators at General Electric drew scenes in a priority order of clusters of faces that was computed before the flight. Newell, Newell and Sancha described a full depth sort method in 1972: they sort the polygons by depth, test pairs whose depth ranges overlap, and split polygons that no order can handle. Sutherland, Sproull and Schumacker in 1974 classified the depth sort as a *list priority* algorithm that works in object space before it paints in image space. Fuchs, Kedem and Naylor in 1980 gave the [BSP tree](/bsp-tree/), which gives a correct order for each viewpoint after one preprocessing step.

## References
