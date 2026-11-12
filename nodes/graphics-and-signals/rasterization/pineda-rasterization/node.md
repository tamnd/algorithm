---
tag: JW7NSM
kind: algorithm
slug: pineda-rasterization
name: Pineda triangle rasterization
aliases:
- half-space triangle rasterization
- edge-function rasterization
area: graphics-and-signals/rasterization
level: core
summary: Rasterize a triangle by evaluating its three edge functions at each pixel center of the bounding box, with integer steps and the top-left rule.
solves: [triangle-rasterization]
model: word-ram
complexity:
  vars: {w: the width of the clipped bounding box in pixels, h: the height of the clipped bounding box in pixels}
  time: {worst: Θ(w h), average: Θ(w h), best: Θ(w h)}
  space: {extra: Θ(1)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1988
  people: [Juan Pineda]
  note: Pineda, at Apollo Computer, showed that the edge functions of a polygon can be evaluated incrementally and at many pixels in parallel.
prereqs: [edge-function, top-left-fill-rule, triangle-rasterization]
see_also: [conservative-rasterization, tiled-rasterization, scanline-polygon-fill, perspective-correct-interpolation, z-buffer, multisample-antialiasing, simt-model, digital-differential-analyzer]
sources:
  - paper: doi:10.1145/378456.378457
    title: Juan Pineda, A parallel algorithm for polygon rasterization, Computer Graphics (SIGGRAPH 88 Proceedings) 22(4), 17 to 20, 1988
    locator: the whole paper (the edge function, the incremental steps, the parallel evaluation and the traversal of the bounding region)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 23, Section 23.1, Rasterization (edge functions, fixed point vertices and the tie rule)
  - book: isbn:9781482229394
    title: Steve Marschner and Peter Shirley, Fundamentals of Computer Graphics, fourth edition, CRC Press, 2016
    locator: Chapter 8, Section 8.1.2, Triangle Rasterization (the bounding box loop over pixel centers after Pineda)
  - url: https://fgiesen.wordpress.com/2013/02/08/triangle-rasterization-in-practice/
    title: Fabian Giesen, Triangle rasterization in practice, The ryg blog, 2013
    locator: the sections on integer edge functions, the fill rule bias and incremental stepping
  - paper: "Joel McCormack and Robert McNamara, Tiled polygon traversal using half-plane edge functions, Proceedings of the ACM SIGGRAPH/Eurographics Workshop on Graphics Hardware, 2000, pages 15 to 21"
    locator: the whole paper (traversal of a triangle tile by tile with edge functions)
  - paper: doi:10.1145/258694.258723
    title: Marc Olano and Trey Greer, Triangle scan conversion using 2D homogeneous coordinates, Proceedings of the ACM SIGGRAPH/Eurographics Workshop on Graphics Hardware, 89 to 95, 1997
    locator: the whole paper (edge functions from homogeneous vertices, without clipping first)
  - url: https://learn.microsoft.com/en-us/windows/win32/direct3d11/d3d10-graphics-programming-guide-rasterizer-stage-rules
    title: Microsoft, Rasterization Rules (Direct3D 11), Direct3D 11 Graphics documentation
    locator: Triangle Rasterization Rules (the top-left rule and the pixel center convention)
---

Pineda triangle rasterization solves [triangle rasterization](/triangle-rasterization/) with [edge functions](/edge-function/): it tests each pixel center of the triangle's bounding box against the three edges, and it covers the centers where all three tests pass. Each edge function is affine, so a step to the next pixel adds a constant, and the test at one pixel does not depend on the test at any other pixel. With vertices snapped to integer subpixel coordinates, every decision is exact, and the [top-left fill rule](/top-left-fill-rule/) gives each center on a shared edge to exactly one triangle. The cost is $\Theta(wh)$ for a $w \times h$ bounding box, whatever the number of covered pixels. GPU rasterizers use this method, in a tiled and parallel form.

## In plain words

Draw a straight line through two corners of a triangle. Every point of the screen is on one side of the line or on the other. A point is in the triangle when it is on the inner side of all three lines.

The method takes the smallest rectangle of pixels around the triangle. At the center of each of its pixels, it asks "which side?" for each line. The answer to each question is a number whose sign is the side. A move of one pixel to the right changes each number by a fixed amount, so one addition updates it.

The corners are first rounded to a fine integer grid. Then the numbers are exact integers, and a center exactly on a line gets a fixed answer from a tie rule. Two triangles that share an edge then never both draw a pixel, and never both skip it.

## The problem

The screen has $W \times H$ pixels. A pixel is a point sample at its center, not a little square: pixel $(i, j)$, with $0 \le i < W$ and $0 \le j < H$, is the point $(i + \tfrac12, j + \tfrac12)$, as in the Direct3D 10 and OpenGL rules, with $y$ down. The vertices $v_0, v_1, v_2$ are integers in units of $1/s$ pixel, for an even number $s$ of subpixel steps per pixel. So the center of pixel $(i, j)$ is the integer point $c_{ij} = (s i + s/2,\ s j + s/2)$. The output is the set of pixels $(i, j)$ whose centers the triangle covers under the top-left rule. A triangle with zero area covers no pixel.

## The algorithm

The edges are numbered by the opposite vertex: edge $k$ goes from $v_{k+1}$ to $v_{k+2}$, indices modulo 3.

```pseudo id=main
PINEDA-RASTERIZE(v0, v1, v2, W, H, s)     ▷ integer vertices in units of 1/s pixel
L1  S2 ← E_{v0 v1}(v2)                     ▷ twice the signed area
L2  if S2 = 0 then return the empty set
L3  if S2 < 0 then swap v1 and v2          ▷ now E_k > 0 inside
L4  for k ← 0 to 2 do
L5      A_k ← y(v_{k+1}) − y(v_{k+2}),  B_k ← x(v_{k+2}) − x(v_{k+1}),  C_k ← x(v_{k+1}) y(v_{k+2}) − y(v_{k+1}) x(v_{k+2})
L6      bias_k ← 0 if A_k > 0 or (A_k = 0 and B_k > 0) else −1    ▷ top-left rule
L7  i0..i1, j0..j1 ← the pixels whose centers are in the bounding box of the vertices, clipped to the screen
L8  (x, y) ← (s·i0 + s/2, s·j0 + s/2)      ▷ the center of pixel (i0, j0)
L9  R_k ← A_k x + B_k y + C_k + bias_k  for k = 0, 1, 2
L10 for j ← j0 to j1 do
L11     e_k ← R_k  for k = 0, 1, 2
L12     for i ← i0 to i1 do
L13         if e_0 ≥ 0 and e_1 ≥ 0 and e_2 ≥ 0 then output pixel (i, j)
L14         e_k ← e_k + s·A_k  for k = 0, 1, 2
L15     R_k ← R_k + s·B_k  for k = 0, 1, 2
```

Lines L1 to L3 make the orientation the same for both windings, so a triangle and its mirror order give the same pixels. Lines L4 to L6 are the triangle setup: the [edge constants](/edge-function/) and the bias that turns the test "$E > 0$, or $E = 0$ on a top-left edge" into one sign test, because $E > 0$ is the same as $E - 1 \ge 0$ for integers. Line L7 finds the range of pixel indices whose centers can be inside: $i_0 = \lceil (x_{\min} - s/2)/s \rceil$, $i_1 = \lfloor (x_{\max} - s/2)/s \rfloor$, and the same for $j$, each clipped to the screen. Line L9 evaluates the three functions once, at the first center. Then a step of one pixel to the right adds $s A_k$ (line L14), and a step of one row down adds $s B_k$ (line L15). The inner loop has three additions and three sign tests and no multiplication.

The loop body for one pixel does not read the result for another pixel. Pineda's point was that hardware can therefore evaluate $A_k x + B_k y + C_k$ at many pixels at once, for example one processor per pixel of a block, and step whole blocks. The same incremental form interpolates any attribute that is affine in screen space, such as $z$ for the [z-buffer](/z-buffer/). Attributes of a perspective view need [perspective-correct interpolation](/perspective-correct-interpolation/).

## Example

Take $s = 2$ (half-pixel units), a screen of $5 \times 5$ pixels, and $v_0 = (1, 1)$, $v_1 = (9, 1)$, $v_2 = (1, 9)$. In pixel units this is the triangle $(0.5, 0.5), (4.5, 0.5), (0.5, 4.5)$, and the center of pixel $(i, j)$ is $(2i + 1, 2j + 1)$. Line L1 gives $S_2 = 64 > 0$, so there is no swap. The setup gives:

| edge | from, to | $A_k$ | $B_k$ | $C_k$ | kind | bias |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | $v_1 \to v_2$ | $-8$ | $-8$ | $80$ | right edge | $-1$ |
| 1 | $v_2 \to v_0$ | $8$ | $0$ | $-8$ | left edge | $0$ |
| 2 | $v_0 \to v_1$ | $0$ | $8$ | $-8$ | top edge | $0$ |

The bounding box is $i, j \in \{0, \ldots, 4\}$. Along a row, line L14 adds $(sA_0, sA_1, sA_2) = (-16, 16, 0)$, and down a row, line L15 adds $(sB_0, sB_1, sB_2) = (-16, 0, 16)$. The table shows $(e_0, e_1, e_2)$ at each center, with the bias included. A pixel is covered when all three values are at least 0.

| $j$ | $i = 0$ | $i = 1$ | $i = 2$ | $i = 3$ | $i = 4$ | covered $i$ |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | (63, 0, 0) | (47, 16, 0) | (31, 32, 0) | (15, 48, 0) | (−1, 64, 0) | 0, 1, 2, 3 |
| 1 | (47, 0, 16) | (31, 16, 16) | (15, 32, 16) | (−1, 48, 16) | (−17, 64, 16) | 0, 1, 2 |
| 2 | (31, 0, 32) | (15, 16, 32) | (−1, 32, 32) | (−17, 48, 32) | (−33, 64, 32) | 0, 1 |
| 3 | (15, 0, 48) | (−1, 16, 48) | (−17, 32, 48) | (−33, 48, 48) | (−49, 64, 48) | 0 |
| 4 | (−1, 0, 64) | (−17, 16, 64) | (−33, 32, 64) | (−49, 48, 64) | (−65, 64, 64) | none |

The algorithm tests 25 centers and covers 10. The zeros in the $e_1$ column are centers on the left edge, and the zeros in the $e_2$ row are centers on the top edge: both are in. The values $-1$ are centers on the diagonal, where $E_0 = 0$ on a right edge: they are out. The triangle $(9, 1), (9, 9), (1, 9)$ on the other side of the diagonal has the diagonal as a left edge. It covers the 6 pixels $(3, 1), (2, 2), (3, 2), (1, 3), (2, 3), (3, 3)$, so the two triangles cover the $4 \times 4$ block of pixels $0 \le i, j \le 3$ with each pixel once.

## Correctness

**Claim.** PINEDA-RASTERIZE outputs pixel $(i, j)$, with $0 \le i < W$ and $0 \le j < H$, if and only if the triangle covers the center $c_{ij}$ under the top-left rule. Each pixel is output at most once.

The key invariant is: when line L13 runs for pixel $(i, j)$, $e_k = E_k(c_{ij}) + \mathrm{bias}_k$ for $k = 0, 1, 2$. It holds at the first pixel by line L9 and is kept by the exact integer steps of lines L14 and L15. So line L13 tests exactly the rule. Line L7 skips only centers outside the bounding box, which no triangle covers, and centers off the screen. The full proof is in [the correctness proof](proofs/correctness.md).

That two triangles with a shared edge never both cover a center, and that a mesh leaves no gap, is the theorem on the [top-left fill rule](/top-left-fill-rule/) page.

## Complexity

The model is the [word RAM](/word-ram/) with words of at least $2q + 2$ binary digits, where the subpixel coordinates fit in $q$ binary digits as signed integers. By property 7 of the [edge function](/edge-function/), each $E_k$ at a point of the coordinate range fits in $2q + 2$ digits, and so each value of lines L9, L14 and L15 is exact.

- **Time.** Lines L1 to L9 take $O(1)$ time. The loops visit each pixel of the clipped box, $w = i_1 - i_0 + 1$ columns and $h = j_1 - j_0 + 1$ rows, with $O(1)$ work each: three sign tests and three additions. So the time is $\Theta(wh)$ in every case, plus the size of the output, which is at most $wh$.
- **Space.** The setup holds 12 integers and the loops hold 6. The extra space is $\Theta(1)$ besides the output.
- **Waste.** A triangle has at most half the area of its bounding box, so a well-shaped triangle covers about half the box or more. A thin triangle along the diagonal of a $w \times h$ box covers only $O(w + h)$ pixels, but the loops still visit all $wh$. A triangle with no covered pixel can also cost $\Theta(wh)$. [Tiled rasterization](/tiled-rasterization/) removes most of this waste: it rejects whole tiles outside an edge.

## Properties

- **Exact.** With integer subpixel vertices, every decision is a sign test on an exact integer. The same input gives the same pixels on each machine.
- **Watertight.** With the top-left rule, triangles with disjoint interiors cover each center inside their union exactly once ([top-left fill rule](/top-left-fill-rule/)).
- **Independent of the winding.** Line L3 makes both vertex orders give the same pixels. [Back-face culling](/back-face-culling/) uses the sign of $S_2$ from line L1 before this step.
- **Parallel.** The test at one pixel uses no result of another pixel, so it maps to SIMD lanes, as in the [SIMT model](/simt-model/), or to a grid of small processors.
- **Output order.** The pixels come in row-major order of the bounding box.

## Variants and improvements

- **Tiled traversal.** Test an edge function at the corners of a tile of $8 \times 8$ or $16 \times 16$ pixels to reject the tile or accept it whole, and run the loop only in tiles that the edge cuts (McCormack and McNamara 2000). This is the base of [tiled rasterization](/tiled-rasterization/).
- **Conservative coverage.** Move each $C_k$ by half a pixel along the edge normal to cover every pixel that the triangle touches, or every pixel fully inside it. See [conservative rasterization](/conservative-rasterization/).
- **Multisampling.** Evaluate the same edge functions at several sample positions per pixel and keep a coverage mask, as in [multisample antialiasing](/multisample-antialiasing/). The top-left rule applies at each sample.
- **Homogeneous edge functions.** Olano and Greer compute the edge functions from the homogeneous vertices, which rasterizes triangles that cross the eye plane without clipping them first.
- **Edge walking.** A scanline method finds the span of each row from the edges and visits only covered pixels, as in [scanline polygon fill](/scanline-polygon-fill/). It needs a division or a [DDA](/digital-differential-analyzer/) per edge, and a float DDA adds a rounded slope at each row, so its spans can be off by one pixel at shared edges.

## When to use it

Use Pineda rasterization when you need exact, watertight coverage and the work is done in parallel or in small screen tiles: it is what GPUs do, and it is short to write in software. Use a scanline method when one processor draws large triangles, because it visits only the covered pixels. For thin or very large triangles, add tiles or a hierarchical test, because the plain bounding box loop pays for each pixel of the box.

## Pitfalls

- **Float edge constants.** Computing lines L5 and L9 in floating point loses the exact zero, and the two triangles of a shared edge can both cover a center or both miss it; the [edge function](/edge-function/) page has a binary64 example. Snap the vertices to integers in units of $1/s$ pixel before line L1, and compute lines L1 to L15 in integers.
- **No bias, or the same bias on each edge.** With $\mathrm{bias}_k \leftarrow 0$ for all $k$ in line L6, centers on shared edges are drawn twice; with $-1$ for all $k$, they are drawn by neither triangle. Line L6 must test $A_k > 0$, or $A_k = 0$ and $B_k > 0$, for the orientation fixed in line L3.
- **No orientation step.** Without line L3, a triangle given in the other winding has all $E_k < 0$ inside, and line L13 covers nothing; the bias of line L6 is then also for the wrong side. Swap two vertices when $S_2 < 0$, or cull the triangle on purpose.
- **Overflow.** With 32-bit integers, the products of line L9 overflow when the subpixel coordinates need more than 15 binary digits, which with 256 steps per pixel is a range of only 128 pixels. Use 64-bit integers, or rasterize relative to the tile origin.
- **The bounding box.** In line L7, $\lfloor x_{\min}/s \rfloor$ in place of $\lceil (x_{\min} - s/2)/s \rceil$ only adds a column to test. But $\lceil x_{\min}/s \rceil$ skips the column whose center is between $x_{\min}$ and the next multiple of $s$, and loses pixels. Integer division rounds toward zero in C and down in Python, so negative coordinates need care.
- **The center convention.** Centers at integer points $(s i, s j)$ instead of $(s i + s/2, s j + s/2)$ in line L8 shift the image by half a pixel against Direct3D 10 and OpenGL.

## Implementations

## History

Pineda described the edge function method in 1988, while at Apollo Computer. He showed that the inside test of a convex polygon is the conjunction of edge function signs, that each edge function steps with one addition per pixel, and that the evaluation suits parallel hardware. McCormack and McNamara (2000) gave tiled traversal with the same functions. Olano and Greer (1997) moved the edge functions to homogeneous coordinates. Direct3D 10 fixed the top-left rule as the required tie rule, while the OpenGL specification requires only that each center on a shared edge is produced by exactly one polygon.

## References
