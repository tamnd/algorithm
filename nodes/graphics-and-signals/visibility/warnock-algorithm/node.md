---
tag: NST03R
kind: algorithm
slug: warnock-algorithm
name: Warnock's algorithm
aliases:
- area subdivision algorithm
area: graphics-and-signals/visibility
level: core
summary: Hidden surface removal by recursive subdivision of the screen into four squares, until each square is empty, is covered by one front polygon, or is one pixel.
solves: [hidden-surface-removal]
model: real-ram
complexity:
  vars: {n: the number of polygons, W: the image width in pixels, H: the image height in pixels}
  time: {worst: O(n W H)}
  space: {extra: O(n log(W + H))}
properties: {stable: true, in_place: false, adaptive: true, online: false, deterministic: true, comparison: true, recursive: true}
history:
  year: 1969
  people: [John E. Warnock]
  note: Warnock described the method in a 1969 University of Utah technical report, which was also his PhD thesis. It made halftone pictures of polygon scenes on a raster.
prereqs: [hidden-surface-removal, quadtree, divide-and-conquer-paradigm]
see_also: [z-buffer, watkins-scanline-algorithm, object-space-vs-image-space, visibility-coherence, separating-axis-theorem, weiler-atherton-algorithm, hierarchical-z-buffer]
sources:
  - paper: "John E. Warnock, A Hidden Surface Algorithm for Computer Generated Halftone Pictures, University of Utah Computer Science Department, Technical Report 4-15, June 1969 (PhD thesis)"
    locator: the whole report (the subdivision of the screen into squares and the tests on each square)
  - paper: doi:10.1145/356625.356626
    title: Ivan E. Sutherland, Robert F. Sproull and Robert A. Schumacker, A characterization of ten hidden-surface algorithms, ACM Computing Surveys 6(1), 1974, pages 1 to 55
    locator: the section on the Warnock algorithm
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 15, the section on area-subdivision algorithms (the four relations of a polygon to a window and the four cases)
---

Warnock's algorithm solves [hidden surface removal](/hidden-surface-removal/) by splitting the screen into four squares, and each square again, until the picture in a square is simple. A square is simple when no polygon meets it, when only one polygon meets it, when one polygon covers it and is in front of all the others there, or when it is one [pixel](/pixel/). It is an image-space [divide and conquer](/divide-and-conquer-paradigm/) method, and the squares form a [quadtree](/quadtree/). It does work only where the picture is complex, near edges and where surfaces cross.

## In plain words

Look at a square part of the picture. If nothing is in it, paint it with the background. If one shape covers the whole square and is in front of everything else there, paint it with that shape. If only one shape is in it, draw that shape there. These cases are easy.

If the square is not easy, cut it into four smaller squares and look at each one in the same way. Large parts of the picture, such as the sky or the middle of a wall, are easy at once. Only the squares near edges get cut again and again.

When a square is as small as one dot of the screen, stop cutting. Find the nearest shape at the center of the dot, and paint the dot with it.

## The problem

The input is a list of $n$ triangles in screen space and an image of $W \times H$ pixels. A vertex is $(x, y, z)$ with $x$ to the right and $y$ down in pixel units, and $z$ the depth after the perspective divide, smaller nearer; $z$ is affine in $x$ and $y$ on each triangle. Pixel $(i, j)$ is the point sample at $(i + \tfrac12, j + \tfrac12)$, and the [top-left fill rule](/top-left-fill-rule/) decides the centers on edges. The output at each pixel is the covering triangle with the least depth at the center, the first one on a tie, or the background. This is the same output as the [z-buffer](/z-buffer/) gives.

A *window* is a square $[x, x + s] \times [y, y + s]$ with integer corners and a side $s$ that is a power of 2. The first window has the least side $s \ge \max(W, H)$. A part of a window outside the screen is not drawn. A triangle $t$ has one of three relations to a window:

- *disjoint*: $t$ meets no point of the open window;
- *surrounding*: $t$ contains the closed window;
- *other*: $t$ meets the window but does not contain it (it is inside the window or crosses its border).

## The algorithm

The *corner depths* of a triangle are the depths of its plane at the four corners of the window. Since the depth is affine, its least and greatest values on the window are at corners.

```pseudo id=main
WARNOCK(W, H, T)
L1  push (0, 0, s, T) on a stack S, with s the least power of 2 ≥ max(W, H)
L2  while S is not empty do
        pop (x, y, s, L) from S; skip it if the window is outside the screen
L3      R ← the triangles of L that are not disjoint from the window
        U ← the triangles of R that surround the window
L4      if R is empty then fill the window with the background; continue
L5      if R = {t} and t is not in U then draw t at each pixel center of the window; continue
L6      if some t in U has max corner depth < min corner depth of each other triangle of R then
L7          fill the window with t; continue
L8      if s = 1 then give the pixel the nearest triangle of R that covers its center; continue
L9      push the four quarters of side s/2 on S, each with the list R
```

Line L3 decides *disjoint* with the [separating axis theorem](/separating-axis-theorem/): a triangle and a square are disjoint if and only if their projections are disjoint on the $x$ axis, on the $y$ axis, or on the normal of one of the three triangle edges. It decides *surrounding* by the four corners: the closed square is in the triangle if and only if each corner is. Each child gets only the list $R$ of its parent, so a triangle that is disjoint from a window is never tested again below it. The stack replaces the recursion of the usual description.

## Example

The scene on an $8 \times 8$ image has a far triangle $F = ((-1,-1,9), (20,-1,9), (-1,20,9))$, which surrounds the screen, and a near triangle $N = ((0,0,1), (6,0,1), (0,6,1))$, whose long edge is the line $x + y = 6$. The output is

```
NNNNNFFF
NNNNFFFF
NNNFFFFF
NNFFFFFF
NFFFFFFF
FFFFFFFF
FFFFFFFF
FFFFFFFF
```

The algorithm visits 29 windows:

| side | windows | split (L9) | filled with $F$ (L7) | filled with $N$ (L7) | pixel decision (L8) |
|---|---|---|---|---|---|
| 8 | 1 | 1 | 0 | 0 | 0 |
| 4 | 4 | 3 | 1 | 0 | 0 |
| 2 | 12 | 3 | 6 | 3 | 0 |
| 1 | 12 | 0 | 3 | 3 | 6 |

The window of side 4 at $(4, 4)$ has $x + y \ge 8$, so $N$ is disjoint from it, $F$ surrounds it, and line L7 fills it. The window of side 2 at $(2, 0)$ has its corners on or below the line $x + y = 6$, so $N$ surrounds it; its corner depths are all 1 and those of $F$ are all 9, so line L7 fills it with $N$. The six pixel decisions are the pixels that the edge $x + y = 6$ crosses, two in each of the three windows of side 2 on the edge. At the pixel $(5, 0)$ the center $(5.5, 0.5)$ is on that edge, which is not a top or left edge of $N$, so $F$ wins.

## Correctness

Each window that the algorithm fills or draws gets the right pixels, and the windows that it finishes cover the screen without overlap. In case L4 no triangle meets the open window, and each pixel center of the window is in the open window. In case L5 only $t$ can cover a center. In case L7, $t$ covers each center, and its depth there is at most its greatest corner depth; each other triangle that covers a center has its plane depth there at least its least corner depth, which is larger. Case L8 is the definition. Each split halves the side, so after at most $\log_2 s$ splits a window is a pixel, and the loop ends. The full proof is in the proof file.

## Complexity

Let $s < 2 \max(W, H)$ be the first side. A window of side $h$ that meets the screen is one of at most $(\lceil W/h \rceil)(\lceil H/h \rceil)$, so the number of windows over all levels is $O(W H + \log s)$. Each window costs $O(|L|) \le O(n)$ for line L3, and the fills and draws cost $O(1)$ per pixel of a finished window. The finished windows are disjoint, so all fills cost $O(W H)$ together. The worst-case time is $O(n W H)$.

The actual cost depends on the picture: windows are split only where the picture is not simple, which is near the projected edges, near lines where two surfaces cross, and where the corner test of line L6 is too weak. Inside a large uniform region one window of large size ends the work. This is *area coherence*. For the example, 29 windows decide 64 pixels.

The stack holds at most $3$ windows per level plus one, so at most $3 \log_2 s + 1$ entries, each with a list of at most $n$ triangles. The extra space is $O(n \log(W + H))$, besides the image.

## Properties

- **Image space, with object-space tests.** The tests on a window use the exact geometry, but the recursion stops at pixels. See [object space and image space](/object-space-vs-image-space/).
- **No depth buffer.** The memory is the stack and the image, not a depth per pixel.
- **Adaptive.** The work follows the complexity of the visible picture, not the size of the screen.
- **Exact.** With rational coordinates each test is an exact sign test, and the output equals the brute-force answer at each center. The corner test of line L6 is conservative: it can fail when $t$ is in front, and then the window is split further, which costs time but never gives a wrong pixel.
- **Antialiasing.** Running the subdivision below pixel size gives the area of each polygon inside a pixel, up to the size of the smallest window.

## Variants and improvements

- **Polygon-shaped windows.** Weiler and Atherton (1977) split the screen along the edges of the front polygon, not into squares, so that fewer windows are needed; their clipping method is on the [Weiler-Atherton algorithm](/weiler-atherton-algorithm/) page.
- **A depth sort first.** Sort the polygons by their nearest depth, so that the front polygon of line L6 is found early in each list.
- **Stopping at subpixels.** Split to $\tfrac14$ or $\tfrac18$ of a pixel and average, for antialiasing.
- **Hierarchical depth.** The [hierarchical z-buffer](/hierarchical-z-buffer/) uses the same quadtree over the screen, but stores depths in it and tests objects against it.

## When to use it

Use it to study the idea of area coherence, or when memory for a depth buffer is not available and the scene has large uniform regions. A hardware depth buffer is faster for almost every real-time scene. The subdivision itself is the base of many later methods: quadtree image coding, hierarchical depth culling and adaptive sampling.

## Pitfalls

- **Recursion depth.** The recursion has only $\log_2 s$ levels, but a naive version copies a list at each level. Pass only the list $R$, as line L9 does.
- **A weak disjoint test.** A test by bounding boxes alone keeps triangles that are disjoint from a window near their long diagonal edge. The result stays correct, but more windows are split. Use the edge normals too.
- **The front test.** Comparing the depths of the triangles only at the window center is wrong when two surfaces cross inside the window. Use the corner depths of the planes, as line L6 does.
- **Pixels and windows.** The pixel decision of line L8 must use the same center and the same fill rule as the rest of the renderer, or edges show gaps and double pixels between this method and a z-buffer.

## Implementations

## History

Warnock described the method in 1969 in a University of Utah technical report, which was his PhD thesis. Sutherland, Sproull and Schumacker included it among the ten algorithms of their 1974 survey, as an image-space method that sorts by area. The form with four relations and four cases is the one that Foley, van Dam, Feiner and Hughes give.
## References
