---
tag: MW0BS7
kind: technique
slug: tiled-rasterization
name: Tiled rasterization
aliases:
- tile-based rendering
area: graphics-and-signals/rasterization
level: advanced
summary: Split the screen into square tiles, test each tile against the edges of a triangle as a whole, and test single pixels only in the tiles that an edge cuts.
prereqs: [pineda-rasterization, triangle-rasterization]
see_also: [sort-middle-rendering, conservative-rasterization, hierarchical-z-buffer, edge-function, frame-buffer, memory-coalescing, uniform-grid, graphics-pipeline]
sources:
  - paper: "Joel McCormack and Robert McNamara, Tiled polygon traversal using half-plane edge functions, Graphics Hardware 2000"
    title: Joel McCormack and Robert McNamara, Tiled polygon traversal using half-plane edge functions, Proceedings of the ACM SIGGRAPH/EUROGRAPHICS Workshop on Graphics Hardware, 2000
    locator: the whole paper (the order of tiles, and the visit of the pixels of a tile with edge functions)
  - paper: "Tomas Akenine-Möller and Timo Aila, Conservative and tiled rasterization using a modified triangle setup, Journal of Graphics Tools 10(3), 2005"
    title: Tomas Akenine-Möller and Timo Aila, Conservative and tiled rasterization using a modified triangle setup, Journal of Graphics Tools 10(3), 1 to 8, 2005
    locator: the whole paper (the test of a tile against an edge at the tile corner that is farthest along the edge normal)
  - paper: doi:10.1145/378456.378457
    title: Juan Pineda, A parallel algorithm for polygon rasterization, Computer Graphics (SIGGRAPH 88 Proceedings) 22(4), 17 to 20, 1988
    locator: the whole paper (edge functions evaluated in parallel over a block of pixels)
  - paper: doi:10.1109/38.291528
    title: Steven Molnar, Michael Cox, David Ellsworth and Henry Fuchs, A sorting classification of parallel rendering, IEEE Computer Graphics and Applications 14(4), 23 to 32, 1994
    locator: the whole paper (screen regions, the sort to regions after geometry processing, and the overlap of primitives with regions)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 23, Efficiency and Hardware (tiled traversal in the rasterizer, and tile-based GPU architectures)
---

Tiled rasterization is the technique of splitting the screen into square tiles of $t \times t$ pixels and deciding coverage one tile at a time. For a triangle, each tile is first tested as a whole against the three [edge functions](/edge-function/): it is rejected if one edge excludes all its pixel centers, accepted if no edge excludes any, and only otherwise are its pixels tested one by one. The tile test costs $O(1)$, because an edge function is affine and its extreme value over the tile is at one corner. The same tiles are also the unit of work of tile-based GPUs, which first sort the triangles into lists per tile and then render each tile with its color and depth in on-chip memory ([sort-middle rendering](/sort-middle-rendering/)). In both forms the result is the same set of pixels as plain [Pineda rasterization](/pineda-rasterization/).

## In plain words

Think of the screen as a floor of tiles, each tile a small square of dots. To draw a triangle, we do not ask each dot whether it is inside. We first ask each tile.

A tile that lies fully outside one side of the triangle is skipped at once. A tile that lies fully inside all three sides is filled at once. Only the tiles that a side of the triangle cuts through are checked dot by dot. For a large triangle these are few, so most of the work goes away.

The tiles help in a second way. A graphics chip can first sort all triangles by the tiles they touch, and then draw one tile at a time in a small, fast memory on the chip. Each tile is then written to the slow main memory only once.

## When it applies

- The coverage test is a set of half-plane tests with affine functions, as with the edge functions of a triangle under the [top-left fill rule](/top-left-fill-rule/). The pixels are point samples at the centers $(i + \tfrac12, j + \tfrac12)$, as in the Direct3D 10 and OpenGL rules; a pixel is a point, not a little square, and the tile test uses the extreme centers of the tile, not the corners of its square.
- The triangles are large compared with a tile, so that many tiles are fully inside or fully outside. For triangles of a few pixels, the tile test is extra work.
- The pixels of a tile are processed together: in parallel lanes, in one block of cache, or in an on-chip buffer. This is where the speed of the technique comes from in hardware.

## The template

```pseudo id=main
TILED-RASTERIZE(T, t)
L1  set up the edge functions E_0, E_1, E_2 of T with the top-left bias, and the pixel bounding box B
L2  for each tile R of t × t pixels that meets B do
L3      let C_R be the pixel centers of R ∩ B
L4      for k ← 0 to 2 do
L5          hi_k ← the largest value of E_k on C_R      ▷ at the corner center chosen by the signs of the coefficients
L6          lo_k ← the smallest value of E_k on C_R     ▷ at the opposite corner center
L7      if hi_k < 0 for some k then skip R               ▷ rejected: one edge excludes each center
L8      else if lo_k ≥ 0 for each k then output each pixel of R ∩ B      ▷ accepted
L9      else for each center p in C_R do
L10         if E_k(p) ≥ 0 for each k then output the pixel of p
```

An edge function $E(x, y) = A x + B y + C$ is affine, so on the rectangle of centers its largest value is at the corner with the largest $x$ if $A \ge 0$ (the smallest $x$ otherwise) and the largest $y$ if $B \ge 0$; the smallest value is at the opposite corner. Lines L5 and L6 are four multiplications and additions per edge, or two additions with steps from tile to tile. Line L7 is exact: if the largest value is negative, each center fails that edge. Line L8 is exact: if each smallest value is at least 0, each center passes each edge. Line L9 is the loop of [Pineda rasterization](/pineda-rasterization/) on one tile. So the output equals the untiled output, with the same tie rule.

**The cost bound.** Let the bounding box have $w \times h$ pixels and the triangle cover $c$ of them. The tests of lines L2 to L8 cost $O(1)$ per tile, and at most $(\lceil w/t \rceil + 1)(\lceil h/t \rceil + 1) \le wh/t^2 + 2(w + h)/t + 4$ tiles meet $B$, since $B$ need not start at a tile boundary. A tile that line L9 visits has a center that fails an edge and a center that passes it, so the line of that edge passes through the square spanned by its centers. A line in $B$ crosses at most $w/t + 1$ vertical and $h/t + 1$ horizontal tile boundaries, and meets one more tile than the number of boundaries it crosses, so each of the three edges meets at most $(w + h)/t + 3$ tiles. A cut tile has at most $t^2$ centers, and at most $t \min(w, h)$ because it lies in $B$, so the cut tiles cost $O\big(((w + h)/t)\,t^2 + t \min(w, h)\big) = O(t(w + h))$. The accepted tiles of line L8 cost $O(1)$ per output pixel. In total the time is

$$O\!\left(\frac{wh}{t^2} + t\,(w + h) + c\right),$$

against $\Theta(wh)$ for Pineda's loop over the whole box. For a square box with $w = h = n$, the sum $n^2/t^2 + 2tn$ is smallest at $t = n^{1/3}$; in practice $t$ is fixed by the hardware, often 8 or 16. A hierarchy of tile sizes, tested from large to small, brings the cut tiles down further.

## Classic examples

- **Tile traversal in GPU rasterizers.** The rasterizer walks the tiles of a triangle in a fixed order and tests the pixels of a cut tile in parallel lanes, as in McCormack and McNamara (2000), with the edge functions of [Pineda rasterization](/pineda-rasterization/) (1988).
- **Tile-based rendering.** Mobile GPUs and the sort-middle machines described by Molnar, Cox, Ellsworth and Fuchs (1994) first sort each triangle into the lists of the screen tiles it may touch, and then render each tile with its color and depth buffers on chip, which saves most of the traffic to the [frame buffer](/frame-buffer/) ([sort-middle rendering](/sort-middle-rendering/)).
- **Conservative tile tests.** The test of line L7, made at the corner of the tile square instead of the corner center and joined with a test of the bounding box, is the overestimate of [conservative rasterization](/conservative-rasterization/) at tile resolution; Akenine-Möller and Aila (2005) use one modified setup for both.
- **Depth culling per tile.** A [hierarchical z-buffer](/hierarchical-z-buffer/) keeps the farthest depth of each tile and rejects a whole tile of a triangle that is behind it.

**A worked example.** On a $64 \times 64$ screen with 16 subpixel steps, the triangle $(2.5, 3.25)$, $(60.75, 10.5)$, $(20.25, 58.5)$ has a pixel box of $59 \times 56 = 3304$ centers and covers 1547 of them. Pineda's loop tests all 3304. The tiled loop gives:

| tile size $t$ | tiles that meet $B$ | rejected | accepted | cut | pixel tests in cut tiles |
| --- | --- | --- | --- | --- | --- |
| 4 | 240 | 121 | 76 | 43 | 638 |
| 8 | 64 | 26 | 13 | 25 | 1374 |
| 16 | 16 | 4 | 1 | 11 | 2367 |

In each case the output is the same 1547 pixels as Pineda's loop. Smaller tiles mean more tile tests and fewer pixel tests; at $t = 4$ the work is $240$ tile tests and $638$ pixel tests, against $3304$ pixel tests untiled.

## Variations

- **Tile order.** Tiles are visited in rows, in a zigzag, or along a space-filling curve, to keep the texture and frame buffer accesses of nearby pixels in the same cache lines ([memory coalescing](/memory-coalescing/)).
- **Hierarchical tiles.** Test tiles of $64 \times 64$, then their $8 \times 8$ parts, then pixels. The rejected and accepted parts stop early, and only the cut parts go down.
- **Sorting into tile lists.** In a first pass, each triangle goes into the list of each tile that its bounding box meets, or each tile that passes the test of line L7, like a [uniform grid](/uniform-grid/) for points. In a second pass, each tile renders its list. The number of list entries is the overlap that [sort-middle rendering](/sort-middle-rendering/) measures.
- **Coarse coverage masks.** The result of line L8 for a group of tiles can be stored as one bit per tile and combined with the depth or stencil state of the tile.

## Pitfalls

- **The wrong corner.** Taking in line L5 the corner chosen by the signs of $-A$ and $-B$ gives the smallest value, not the largest, and line L7 then rejects tiles that hold covered centers, which leaves holes in the triangle. Line L5 must take the largest $x$ when $A \ge 0$ and the largest $y$ when $B \ge 0$, and line L6 the opposite corner. Testing at the corners of the tile square instead of the corner centers is still correct, since the square contains the centers, but it rejects and accepts fewer tiles.
- **Bias left out of the tile test.** The top-left bias must be in the constant of each edge function before lines L5 and L6. A tile test without it accepts tiles whose border centers lie on a right or bottom edge, and the pixels of a shared edge are drawn twice.
- **Output outside the screen.** A tile at the border of a screen whose size is not a multiple of $t$ reaches past the screen. Line L8 must output the pixels of $R \cap B$, with $B$ clipped to the screen, not all $t^2$ pixels of $R$.
- **Overflow at corners outside the box.** If the tiles are not clipped to $B$ as in line L3, a corner center can lie up to $t - 1$ pixels outside the box, and $E_k$ there can exceed the range that property 7 of the [edge function](/edge-function/) page gives for the box. Clip to $B$, or give the integers a few more binary digits.
- **Small triangles.** A triangle of a few pixels meets 1 to 4 tiles, and the tile tests only add work. Hardware handles such triangles on a separate fast path.

## Exercises

1. Prove that the largest value of $A x + B y + C$ on a rectangle of points is at the corner chosen by the signs of $A$ and $B$.
2. Show that the intersection of the three inner half-planes of a triangle with nonzero area is the triangle, so the accept test of line L8 needs no bounding box. Explain why the overestimate of conservative rasterization does need one.
3. For $w = h = 1024$ and a triangle that covers half its box, compute the bound of the template for $t = 4, 8, 16, 32$ and find the best $t$.
4. Give the cost of a two-level hierarchy with tile sizes $T$ and $t$, and find when it beats one level.
5. A triangle is sorted into tile lists by its bounding box. Give a thin diagonal triangle whose box meets $\Theta(n^2)$ tiles of an $n \times n$ grid while the triangle meets only $O(n)$, and say which test fixes it.

## References
