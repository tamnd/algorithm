---
tag: QPWQ6K
kind: algorithm
slug: z-buffer
name: Z-buffer algorithm
aliases:
- Z-buffer
- depth buffer
- depth buffer algorithm
- z-buffering
area: graphics-and-signals/visibility
level: core
summary: Keep one depth value per pixel. Draw the primitives in any order, and write a fragment only if it is nearer than the stored depth.
solves: [hidden-surface-removal]
model: real-ram
complexity:
  vars: {n: the number of triangles, W: the image width in pixels, H: the image height in pixels, P: "the number of covered pixel centers, summed over all triangles"}
  time: {worst: Θ(W H + n + P), average: Θ(W H + n + P), best: Θ(W H + n + P)}
  space: {extra: Θ(W H)}
properties: {stable: true, in_place: false, adaptive: false, online: true, deterministic: true, comparison: true, recursive: false}
history:
  year: 1974
  people: [Edwin Catmull]
  note: Catmull described the depth buffer in his 1974 PhD thesis at the University of Utah. Memory was expensive, and the method became the standard only when memory for a full depth image was cheap.
prereqs: [hidden-surface-removal, triangle-rasterization, frame-buffer]
see_also: [z-fighting, painters-algorithm, a-buffer, depth-peeling, early-depth-test, hierarchical-z-buffer, shadow-mapping, object-space-vs-image-space]
sources:
  - paper: "Edwin Catmull, A Subdivision Algorithm for Computer Display of Curved Surfaces, PhD thesis, Department of Computer Science, University of Utah, December 1974"
    locator: the chapter on hidden surfaces (the depth value kept per picture element)
  - paper: doi:10.1145/356625.356626
    title: Ivan E. Sutherland, Robert F. Sproull and Robert A. Schumacker, A characterization of ten hidden-surface algorithms, ACM Computing Surveys 6(1), 1974, pages 1 to 55
    locator: the discussion of image-space methods and of the memory cost of a full depth buffer
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 15, the section on the z-buffer algorithm
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 4.7 (projections and the depth after the divide) and Section 23.7 (depth culling, testing and buffering)
---

The z-buffer algorithm solves [hidden surface removal](/hidden-surface-removal/) with one depth value per [pixel](/pixel/). It draws the primitives in any order, and at each covered pixel it keeps the fragment only if it is nearer than the depth already stored. It needs no sort and handles surfaces that pass through each other, and it takes $\Theta(WH + n + P)$ time for $n$ triangles that cover $P$ pixel centers in total. Every GPU does hidden surface removal this way.

## In plain words

Think of a wall of small boxes, one box for each dot of the picture. Each box holds a color and a number: the distance of the thing that the box shows now. At the start each box shows the background and holds the distance "very far".

Now draw the shapes of the scene, one at a time, in any order. For each dot that a shape covers, find the distance of the shape at that dot. If it is less than the number in the box, the shape is in front: put its color and its distance in the box. If not, something nearer is already there, so do nothing.

When all shapes are drawn, each box shows the nearest shape at its dot. No shape had to be compared with another shape, only with one number per dot.

## The problem

The input is a list of $n$ triangles $t_0, \ldots, t_{n-1}$ in screen space and an image of $W \times H$ pixels. A vertex is $(x, y, z)$: $x$ and $y$ are in pixel units, with $x$ to the right and $y$ down, and $z$ is the depth after the perspective divide, where a smaller $z$ is nearer. On each triangle, $z$ is an affine function of $x$ and $y$; this holds for the depth after a perspective divide, but not for the distance to the eye (see [perspective-correct interpolation](/perspective-correct-interpolation/)).

Pixel $(i, j)$ is a point sample at its center $c = (i + \tfrac12, j + \tfrac12)$, not a small square. A triangle covers $c$ when $c$ is inside it or on an edge that the [top-left fill rule](/top-left-fill-rule/) gives to it, so a center on an edge shared by two triangles goes to exactly one of them. A pixel center outside the screen is not sampled, so the screen border clips each triangle. The output at each pixel is the color of the covering triangle with the least depth at $c$; of two equal depths, the triangle that comes first in the list wins. A pixel that no triangle covers gets the background.

## The algorithm

$D$ is the depth buffer and $C$ is the color buffer, both $W \times H$.

```pseudo id=main
Z-BUFFER(W, H, t[0 .. n − 1])
L1  for each pixel (i, j) do D[i, j] ← +∞, C[i, j] ← background
L2  for k ← 0 to n − 1 do                        ▷ any order gives the same depths
L3      for each pixel center c = (i + ½, j + ½) that t[k] covers do
L4          z ← the depth of the plane of t[k] at c
L5          if z < D[i, j] then                      ▷ strict: the earlier triangle keeps a tie
L6              D[i, j] ← z, C[i, j] ← color of t[k]
L7  return C, D
```

Lines L3 and L4 are [triangle rasterization](/triangle-rasterization/). The implementation uses three [edge functions](/edge-function/) $w_0, w_1, w_2$ at $c$, with $w_0 + w_1 + w_2 = A$, twice the area. The center is covered when each $w_k$ is positive, or zero on a top or left edge. The depth is the barycentric mix $z = (w_0 z_0 + w_1 z_1 + w_2 z_2)/A$. From one pixel to the next one on the right, each $w_k$ changes by a constant, so line L3 costs a few additions per pixel.

## Example

Two triangles pass through each other on an $8 \times 6$ image. Triangle $a = ((0,0,0), (8,0,0), (4,6,12))$ has its base at the top and depth $z = 2y$. Triangle $b = ((0,6,0), (8,6,0), (4,0,12))$ has its base at the bottom and depth $z = 12 - 2y$. They meet on the line $y = 3$.

| row $j$ | $y$ at the centers | $a$ covers | $b$ covers | result | depth in column 3 |
|---|---|---|---|---|---|
| 0 | 0.5 | 8 pixels | none | `AAAAAAAA` | 1 |
| 1 | 1.5 | 6 pixels | 2 pixels | `.AAAAAA.` | 3 |
| 2 | 2.5 | 4 pixels | 4 pixels | `..AAAA..` | 5 |
| 3 | 3.5 | 4 pixels | 4 pixels | `..BBBB..` | 5 |
| 4 | 4.5 | 2 pixels | 6 pixels | `.BBBBBB.` | 3 |
| 5 | 5.5 | none | 8 pixels | `BBBBBBBB` | 1 |

In row 1, $b$ covers pixels 3 and 4, but $a$ is at depth 3 there and $b$ at depth 9, so $a$ stays. At pixel $(3, 2)$ the depth of $a$ is 5 and the depth of $b$ is 7, so $a$ stays. At pixel $(3, 3)$ the depth of $a$ is 7 and of $b$ is 5, so $b$ replaces $a$. The image is the same if $b$ is drawn first. A [painter's algorithm](/painters-algorithm/) cannot draw this scene with one order of the two triangles, because each is in front of the other in some rows.

## Correctness

The invariant of the loop of line L2 is: after the triangles $t_0, \ldots, t_{k-1}$, $D[i, j]$ is the least depth at $c$ over those of them that cover $c$ (or $+\infty$), and $C[i, j]$ is the color of the first of them with that depth. Line L5 keeps it, because the new $D$ is $\min(D, z)$, and the strict test keeps the earlier triangle on a tie. At $k = n$ the invariant is the output. The depths do not depend on the order, because the minimum does not. The full proof is in the proof file.

## Complexity

Line L1 takes $\Theta(WH)$ time. Each triangle costs $O(1)$ for its setup, plus $O(1)$ for each pixel center it covers, so the loop takes $\Theta(n + P)$ when the rasterizer visits only covered centers. The total is $\Theta(WH + n + P)$ in each case, with no sort. The implementation scans the bounding box of each triangle, which costs the area of the box: for a long thin triangle on a diagonal, this is much more than the pixels it covers. Tiled and hierarchical rasterizers skip the empty parts of the box (see [tiled rasterization](/tiled-rasterization/)).

$P$ is at most $nWH$. The ratio $P/(WH)$ is the average *depth complexity*: the number of surfaces on the ray through a pixel. Each covered center is tested, even if it is later overwritten, so the work grows with the depth complexity, not with the visible part. The [hierarchical z-buffer](/hierarchical-z-buffer/) and the [early depth test](/early-depth-test/) reduce this work.

The extra space is $\Theta(WH)$ depth values. In hardware the depth is often a 24-bit fixed-point number or a 32-bit float per sample, and with [multisample antialiasing](/multisample-antialiasing/) there is one depth per sample.

## Properties

- **Image space.** The decision is made per pixel center, not per polygon. See [object space and image space](/object-space-vs-image-space/).
- **Any order, any shape.** The primitives arrive as a stream, and each needs only a depth at each covered center. Surfaces that pass through each other are drawn right, as in the example.
- **Order independent.** The final depth does not depend on the order. The final color depends on it only at exact ties, which the strict test of line L5 gives to the first triangle.
- **Exact or not.** With integer or rational coordinates each decision is exact. With floating point the coverage test and the depth compare can both fail near ties: a pixel on a shared edge can be drawn twice or not at all, and nearly equal depths produce [z-fighting](/z-fighting/). GPUs snap the vertices to a fixed-point grid, which makes the edge functions exact.
- **One sample per pixel.** The image has [aliasing](/aliasing/) at the edges. Antialiasing needs more samples, or the coverage masks of the [A-buffer](/a-buffer/).
- **Opaque only.** A blend of transparent surfaces needs the surfaces in depth order, which the depth buffer does not keep.

## Variants and improvements

- **Scanline z-buffer.** Keep a depth buffer for one row only, and draw the scene row by row. This needs $\Theta(W)$ depth memory, but each primitive must be found for each of its rows.
- **Early depth test.** Test the depth before the fragment shader runs, so that hidden fragments cost no shading. See [early depth test](/early-depth-test/).
- **Hierarchical z-buffer.** Keep a pyramid of the farthest depths, and reject a whole object that lies behind it. See [hierarchical z-buffer](/hierarchical-z-buffer/).
- **A-buffer.** Keep a list of fragments with coverage masks per pixel, for antialiasing and transparency. See [A-buffer](/a-buffer/).
- **Depth peeling.** Run the z-buffer several times, each time for the next layer behind the last one. See [depth peeling](/depth-peeling/).
- **Reversed depth.** Map the near plane to 1 and the far plane to 0, with a floating-point buffer. This spreads the precision more evenly. See [z-fighting](/z-fighting/).
- **Shadow maps.** A z-buffer drawn from the light gives the nearest surface on each light ray. See [shadow mapping](/shadow-mapping/).
- **Occlusion queries.** Count the samples that pass the depth test. See [occlusion query](/occlusion-query/).

## When to use it

Use the z-buffer for opaque scenes of many triangles, in particular when they arrive as a stream, are not sorted, or pass through each other. It is the default on GPUs, where the depth test is fixed hardware. Use another method when memory for a depth per pixel is not available, when the surfaces are transparent (sort them, or use [depth peeling](/depth-peeling/) or the [A-buffer](/a-buffer/)), or when the output must be exact polygons and not pixels, as for a plotter (an object-space method, for example a [BSP tree](/bsp-tree-visibility/)).

## Pitfalls

- **Depth in the wrong space.** The affine interpolation of line L4 is right for the depth after the perspective divide. Interpolating the view distance linearly in screen space gives wrong depths, and wrong visibility where two surfaces cross.
- **Precision.** After a perspective projection most of the depth values lie near the near plane. Far surfaces that are close together get the same depth value and flicker. See [z-fighting](/z-fighting/).
- **The test operator.** With $\le$ in place of $<$, the last of two equal depths wins. Both are correct, but a renderer that draws a second pass over the same geometry (for example a pass of lights) needs $\le$ or an equal test, and a renderer that relies on the first-wins rule needs $<$.
- **Transparency.** Drawing a transparent surface with depth writes on hides all that is drawn after it behind it. Draw the opaque surfaces first, then the transparent ones in back to front order with depth writes off.
- **Clear the buffer.** Each frame must start with $D = +\infty$ (or the far value). A buffer that keeps the last frame hides the new one.

## Implementations

## History

Catmull described the depth buffer in his 1974 PhD thesis at the University of Utah, as a side result of his subdivision method for curved surfaces. In the survey of the same year, Sutherland, Sproull and Schumacker list it among image-space methods and point to the large memory it needs. When memory became cheap, the z-buffer became the standard method, and graphics hardware since the 1980s has a depth test in fixed function.

## References
