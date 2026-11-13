---
tag: HFMB32
kind: algorithm
slug: conservative-rasterization
name: Conservative rasterization
aliases:
- conservative triangle rasterization
area: graphics-and-signals/rasterization
level: research
summary: Find each pixel whose square a triangle touches, or each pixel whose square lies fully inside it, with the edge functions shifted by half a pixel and a grown bounding box.
solves: [triangle-rasterization]
model: word-ram
complexity:
  vars: {w: the width in pixels of the box of line L6, h: the height in pixels of that box}
  time: {worst: Θ(w h), average: Θ(w h), best: Θ(w h)}
  space: {extra: Θ(1)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 2005
  people: [Tomas Akenine-Möller, Timo Aila, Jon Hasselgren, Lennart Ohlsson]
  note: Akenine-Möller and Aila gave a modified triangle setup for conservative and tiled rasterization, and Hasselgren, Akenine-Möller and Ohlsson gave conservative rasterization on programmable GPUs, both in 2005.
prereqs: [pineda-rasterization, edge-function]
see_also: [tiled-rasterization, minkowski-sum, separating-axis-theorem, top-left-fill-rule, uniform-grid, hierarchical-z-buffer, interval-arithmetic, triangle-rasterization]
sources:
  - paper: "Tomas Akenine-Möller and Timo Aila, Conservative and tiled rasterization using a modified triangle setup, Journal of Graphics Tools 10(3), 2005"
    title: Tomas Akenine-Möller and Timo Aila, Conservative and tiled rasterization using a modified triangle setup, Journal of Graphics Tools 10(3), 1 to 8, 2005
    locator: the whole paper (the edge test at the tile corner farthest along the edge normal, the bounding box test, and the underestimate at the opposite corner)
  - book: isbn:9780321335593
    title: Matt Pharr (editor), GPU Gems 2, Addison-Wesley, 2005
    locator: Chapter 42, Conservative Rasterization, by Jon Hasselgren, Tomas Akenine-Möller and Lennart Ohlsson, pages 677 to 690
  - url: https://learn.microsoft.com/en-us/windows/win32/direct3d12/conservative-rasterization
    title: Microsoft, Conservative Rasterization, Direct3D 12 Graphics documentation
    locator: the whole page (the tiers, the uncertainty region, false positives allowed and false negatives not, inner coverage in tier 3)
  - paper: doi:10.1145/378456.378457
    title: Juan Pineda, A parallel algorithm for polygon rasterization, Computer Graphics (SIGGRAPH 88 Proceedings) 22(4), 17 to 20, 1988
    locator: the whole paper (the edge functions and their incremental evaluation)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 23, Graphics Hardware, the part on rasterization (conservative rasterization as a mode of the rasterizer)
---

Conservative rasterization is a variant of [triangle rasterization](/triangle-rasterization/) that treats each pixel as its closed square, not as the point at its center. The overestimate outputs each pixel whose square the triangle touches, so no pixel that the triangle meets is missed. The underestimate outputs only the pixels whose squares lie fully inside the triangle. The algorithm is the loop of [Pineda rasterization](/pineda-rasterization/) with one change in the setup: each [edge function](/edge-function/) is moved outward by half a pixel in the direction of its normal (inward for the underestimate), and for the overestimate the pixel box is grown by at most one pixel on each side. The moved edges and the grown box bound exactly the [Minkowski sum](/minkowski-sum/) of the triangle and a pixel square, so the decisions are exact. It is a fixed mode of the Direct3D 12 rasterizer and a building block of voxelization and of GPU visibility and collision tests.

## In plain words

Usually a dot of the screen counts as covered when its middle point is in the triangle. A thin triangle can then miss a dot even though it passes right through the dot's small square.

Some jobs cannot accept a miss. A collision test, for example, must find every square that the triangle touches, even at a corner. The conservative answer is to count each square that the triangle touches. The opposite answer counts only the squares that lie fully inside.

The trick is to push each side of the triangle outward by half a square, in the most generous direction, and then test the middle points as usual. A middle point inside the pushed sides belongs to a square that the original triangle touches. A box around the triangle stops the pushed corners from reaching too far. Pushing the sides inward instead gives the squares that lie fully inside.

## The problem

The input is a triangle $T = (v_0, v_1, v_2)$ with nonzero area, its vertices integers in units of $1/s$ pixel for an even $s$, with $y$ down, and a screen of $W \times H$ pixels. Pixel $(i, j)$ is the closed square $[i, i + 1] \times [j, j + 1]$ with the center $(i + \tfrac12, j + \tfrac12)$, the same center convention as in Direct3D 10 and OpenGL. For ordinary rasterization a pixel is a point sample, not a little square; this variant uses the square on purpose.

- **Overestimate:** the pixels with $Q_{ij} \cap T \ne \emptyset$, for the closed square $Q_{ij}$ and the closed triangle.
- **Underestimate:** the pixels with $Q_{ij} \subseteq T$.

The overestimate contains the pixels of the [top-left fill rule](/top-left-fill-rule/), which contain the underestimate. A pixel that $T$ only touches at a corner or along an edge of the square is in the overestimate here; Direct3D 12 leaves such touches to the implementation and allows extra pixels near the boundary (false positives) but no missed ones (false negatives).

## The algorithm

Write $E_k(x, y) = A_k x + B_k y + C_k$ for the edge function of edge $k$, at least 0 on the side of the triangle, and $h = s/2$ for half a pixel in subpixel units.

```pseudo id=main
CONSERVATIVE-RASTERIZE(v0, v1, v2, mode)
L1  2S ← E_{v0 v1}(v2);  if 2S = 0 then return the empty set
L2  if 2S < 0 then swap v1 and v2                       ▷ now each E_k ≥ 0 inside
L3  for k ← 0 to 2 do
L4      r_k ← (|A_k| + |B_k|)·h                         ▷ the largest change of E_k over a pixel square
L5      C_k ← C_k + r_k if mode = over, else C_k − r_k
L6  B ← the pixels whose squares meet the bounding box of T (over), or lie in it (under), clipped to the screen
L7  e_k ← E_k at the center of the first pixel of B, for k = 0, 1, 2
L8  for each row j of B do
L9      for each pixel i of the row, left to right, do
L10         if e_0 ≥ 0 and e_1 ≥ 0 and e_2 ≥ 0 then output pixel (i, j)
L11         e_k ← e_k + s·A_k for each k
L12     e_k ← the value at the start of row j, plus s·B_k, for each k
```

Lines L1 and L2 orient the triangle, as in Pineda's setup. Line L4 is the key: over the square of side $s$ around a center $p$, the edge function changes by at most $h|A_k| + h|B_k|$, and it reaches $E_k(p) + r_k$ at the corner that lies farthest in the direction $(A_k, B_k)$. So $E_k(p) + r_k \ge 0$ says that the square meets the half-plane of edge $k$, and $E_k(p) - r_k \ge 0$ says that it lies in it. Line L5 puts the shift into the constant, so the per-pixel loop of lines L7 to L12 is Pineda's loop without change.

The three shifted half-planes alone are too large for the overestimate: near a sharp vertex they meet beyond the vertex, out to where no square touches the triangle. The box of line L6 cuts this off. In subpixel units, the square of pixel $i$ meets $[x_{\min}, x_{\max}]$ if and only if $\lceil x_{\min}/s \rceil - 1 \le i \le \lfloor x_{\max}/s \rfloor$. The underestimate needs no such cut, because a triangle is the intersection of its three half-planes.

## Example

Take $T = (0.5, 0.5), (4.5, 0.5), (0.5, 4.5)$ in pixel units. In pixel units the edge functions, with $h = \tfrac12$, are:

| edge | from | to | $A$ | $B$ | $C$ | $r = (\lvert A \rvert + \lvert B \rvert)/2$ | $C$ over | $C$ under |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | $(4.5, 0.5)$ | $(0.5, 4.5)$ | $-4$ | $-4$ | $20$ | $4$ | $24$ | $16$ |
| 1 | $(0.5, 4.5)$ | $(0.5, 0.5)$ | $4$ | $0$ | $-2$ | $2$ | $0$ | $-4$ |
| 2 | $(0.5, 0.5)$ | $(4.5, 0.5)$ | $0$ | $4$ | $-2$ | $2$ | $0$ | $-4$ |

The three sets are:

- **Point samples (top-left rule):** the 10 pixels with $i + j \le 3$.
- **Overestimate:** the box of line L6 is $0 \le i, j \le 4$, and the shifted test keeps the 19 pixels with $i + j \le 5$. Pixel $(4, 1)$ has $E_0 = -4$ at its center $(4.5, 1.5)$ and $E_0 + r_0 = 0$: its square touches the hypotenuse at the single point $(4, 1)$, and it is kept. Pixel $(2, 2)$ has its center on the hypotenuse, $E_0 = 0$, which the top-left rule gives to the neighbor, but its square overlaps $T$, so it is kept here.
- **Underestimate:** the 3 pixels $(1, 1)$, $(2, 1)$ and $(1, 2)$. At $(1, 1)$ the shifted values are $E_0 - r_0 = 4$, $E_1 - r_1 = 2$ and $E_2 - r_2 = 2$. Pixel $(0, 0)$ is not inside, because its square reaches $x = 0 < 0.5$.

Without the box of line L6, the shifted edges would also accept pixels $(5, 0)$ and $(0, 5)$, 21 in all: at the center $(5.5, 0.5)$ of pixel $(5, 0)$ the three shifted values are $0$, $22$ and $2$, but the square $[5, 6] \times [0, 1]$ does not reach the triangle, whose $x$ is at most $4.5$.

## Correctness

**Claim.** For a triangle with nonzero area, the overestimate mode outputs exactly the screen pixels whose closed squares meet the closed triangle, and the underestimate mode exactly those whose closed squares lie in it.

A square $p + C$, with $C = [-h, h]^2$, meets $T$ exactly when its center $p$ lies in $T \oplus C$. The proof shows that a half-plane grown by $C$ is the half-plane with the constant of line L5, and that $T \oplus C$ is the intersection of the three grown edge half-planes and the grown bounding box, by a separation argument on the seven normal directions of the triangle and the square, the same directions as in the [separating axis theorem](/separating-axis-theorem/). The underestimate is the minimum of each edge function over the square. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the [word RAM](/word-ram/) with integer subpixel coordinates.

- **Time.** The setup of lines L1 to L7 is $O(1)$. Lines L8 to L12 visit each of the $w \times h$ pixels of the box once, with three compares and three additions. So the time is $\Theta(wh)$ in each case. For the overestimate, the box is at most one pixel larger on each side than the box of Pineda's loop for the same triangle, so at most $(w_0 + 2)(h_0 + 2)$ for a Pineda box of $w_0 \times h_0$; in the example both boxes are $5 \times 5$.
- **Space.** $\Theta(1)$ extra words besides the output.
- **Word size.** The shifted value $E_k(p) + r_k$ is the value of $E_k$ at a corner of the square of $p$, so the shifted values are no larger than the edge function over the corners of the grown box.
- **Output.** For a triangle of area $a$ and perimeter $\ell$ in pixel units, the overestimate has between $\max(a, \ell/4)$ and $a + \sqrt2\,\ell + 4$ pixels. The squares cover $T$, which gives $a$; a square holds at most length 4 of the convex boundary, which gives $\ell/4$; and the squares have disjoint interiors and lie in $T$ grown by one pixel on each side, whose area is at most $a + \sqrt2\,\ell + 4$. So even a thin triangle outputs $\Theta(\ell)$ pixels, while point sampling can output none.

## Properties

- **No false negatives.** Each pixel whose square the triangle meets is output. This is the property that the applications need.
- **Exact.** With integer subpixel vertices, each test is an integer compare. There is no uncertainty region, unlike the hardware tiers, which allow a margin.
- **Overlap on shared edges.** Two triangles that share an edge both output the pixels along it. The overestimate is not watertight in the sense of the top-left rule; it covers each pixel at least once instead of exactly once.
- **Disjoint underestimates.** The underestimates of triangles with disjoint interiors are disjoint, because a square has an interior.
- **Nested.** Underestimate, point samples and overestimate are nested sets.

## Variants and improvements

- **Hardware tiers.** Direct3D 12 has three tiers. Tier 1 allows an uncertainty region of up to half a pixel, tiers 2 and 3 of $1/256$ of a pixel, and tier 3 adds the inner coverage input, which tells a pixel shader that its square is fully inside, the underestimate.
- **A larger polygon in the vertex stage.** Hasselgren, Akenine-Möller and Ohlsson (2005) build, before the rasterizer, a polygon that contains $T \oplus C$ and rasterize it with point samples; the pixel shader then removes the pixels outside the bounding box. This was the way to get the overestimate before hardware support.
- **Tiles.** The same shifted test, with the square of a tile instead of a pixel, decides which tiles a triangle touches; [tiled rasterization](/tiled-rasterization/) uses it to sort triangles to tiles.
- **Three dimensions.** For voxelization, the test becomes a triangle and box overlap test in 3D, again by the [separating axis theorem](/separating-axis-theorem/), with 13 axes.
- **Conservative depth.** Along with the pixel, output the smallest and the largest depth of the triangle over the square, for an occlusion test in a [hierarchical z-buffer](/hierarchical-z-buffer/).

## When to use it

Use the overestimate when a missed pixel breaks a result: voxelization of a mesh into a [uniform grid](/uniform-grid/), collision tests on the GPU, lists of the lights or the triangles that touch each tile, and occlusion and visibility tests that must not drop a visible object. Use the underestimate when a pixel must certainly be inside, as for occluders that hide what is behind them. Do not use either for color: a pixel on an edge is drawn by both triangles, and blending counts it twice.

## Pitfalls

- **The box left out.** Replacing line L6 by the box of Pineda's loop, or by the whole screen, is wrong in both directions. Pineda's box is too small: it drops the squares that the triangle reaches from outside the box of the centers, such as row 0 for a triangle whose top edge is at $y = 0.75$: the center of row 0, at $y = 0.5$, is outside the box, but the square of row 0 reaches down to $y = 1$. The whole screen is too large: near a sharp vertex the shifted edges accept squares beyond the vertex, as for pixels $(5, 0)$ and $(0, 5)$ of the example. Line L6 must use the box of the squares that meet the bounding box of $T$.
- **The wrong sign in line L4.** Writing $r_k = (A_k + B_k)\,h$ instead of $(|A_k| + |B_k|)\,h$ moves an edge with a negative coefficient inward, and the overestimate misses pixels along that edge. The shift must use the absolute values, which pick the farthest corner of the square.
- **Rounding of the shift in floats.** With float vertices, $C_k + r_k$ rounds in [IEEE 754](/ieee-754/) arithmetic and can come out smaller than the exact value, which gives false negatives, the one error the method must avoid. The fix is exact integer subpixel coordinates, as here, or outward rounding of the shift with [interval arithmetic](/interval-arithmetic/), or an exact evaluation of the edge function with a [fused multiply-add](/fused-multiply-add/), [error-free transformations](/error-free-transformations/) or a [Shewchuk expansion sum](/shewchuk-expansion-sum/), as for an exact [orientation test](/orientation-test/).
- **Extrapolated attributes.** A pixel of the overestimate can have its center outside the triangle, so its barycentric coordinates are negative and the interpolated depth, color or texture coordinate lies outside the range of the vertex values. Clamp them, or compute the values at a point of the triangle inside the square.
- **Degenerate triangles.** Line L1 drops a triangle of zero area, but a segment or a point still touches pixels. If such triangles must count, as in voxelization of thin features, handle them as segments: test the Minkowski sum of the segment and the square.

## Implementations

## History

Conservative tests of a primitive against a pixel or a tile square were used in visibility and hierarchical rendering before a name was fixed for them. In 2005 Akenine-Möller and Aila gave the modified triangle setup, with the edge test at the farthest tile corner and the bounding box test, for both conservative and tiled rasterization, and Hasselgren, Akenine-Möller and Ohlsson described the overestimate and the underestimate on programmable GPUs in GPU Gems 2. Direct3D 12 made conservative rasterization a fixed function mode of the rasterizer, with tiers that bound its uncertainty.

## References
