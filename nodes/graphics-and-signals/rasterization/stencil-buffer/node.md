---
tag: A59S6S
kind: data-structure
slug: stencil-buffer
name: Stencil buffer
aliases:
- stencil test buffer
area: graphics-and-signals/rasterization
level: advanced
summary: An s-bit integer per pixel that a fixed test reads and fixed operations update for each fragment, used to mask drawing and to count windings or shadow volumes.
model: word-ram
prereqs: [pixel, nonzero-winding-rule]
see_also: [z-buffer, shadow-volume-algorithm, even-odd-fill-rule, triangle-rasterization, top-left-fill-rule, polygon-scan-conversion, scanline-polygon-fill, graphics-pipeline]
sources:
  - url: https://registry.khronos.org/OpenGL-Refpages/gl4/html/glStencilFunc.xhtml
    title: Khronos Group, OpenGL 4 Reference Pages, glStencilFunc
    locator: the comparison of the masked reference with the masked stored value, the eight functions, and the clamp of the reference value
  - url: https://registry.khronos.org/OpenGL-Refpages/gl4/html/glStencilOp.xhtml
    title: Khronos Group, OpenGL 4 Reference Pages, glStencilOp
    locator: the three cases sfail, dpfail and dppass, and the eight operations, with INCR and DECR saturating and INCR_WRAP and DECR_WRAP wrapping
  - paper: "Mark J. Kilgard and Jeff Bolz, GPU-accelerated path rendering, ACM Transactions on Graphics 31(6), article 172 (2012)"
    locator: the stencil, then cover method for filled paths under the nonzero and even-odd rules
  - book: isbn:9781138627000
    title: Tomas Akenine-Moller, Eric Haines, Naty Hoffman, Angelo Pesce, Michal Iwanicki and Sebastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 7.3, Shadow Volumes (the count of entries and exits in the stencil buffer)
---

A stencil buffer holds one small unsigned integer of $s$ bits, most often 8, for each pixel of a frame buffer, next to the color and the [z-buffer](/z-buffer/). Each fragment that the rasterizer makes at a pixel first goes through the stencil test, which compares a reference value with the stored value under a mask, and then one of three fixed operations updates the stored value, chosen by whether the stencil test and the depth test passed. With these few rules a renderer can limit drawing to a region of any shape, count how many times a path winds around each pixel to fill it under the [nonzero winding rule](/nonzero-winding-rule/), or count how many [shadow volumes](/shadow-volume-algorithm/) contain the visible point. The count is kept modulo $2^s$, which is the main limit of the method.

## In plain words

Think of a sheet of numbers laid over the screen, one number for each pixel. Each number starts at zero. When the program draws a shape, it can tell the hardware what to do with the number at each pixel that the shape covers: add one, take one away, set it to zero, and so on.

Later, the program draws another shape and says: draw only where the number is not zero, or only where it equals five. So the numbers act like a stencil cut from card, and the program can cut it into any form.

The numbers are small. With eight bits, a count goes from 0 to 255 and then starts at 0 again.

## The abstract type

The buffer is a $W$ by $H$ array $S$ of values in $\{0, \dots, 2^s - 1\}$, with a state that the program sets:

- a **function** FUNC, one of NEVER, LESS, LEQUAL, GREATER, GEQUAL, EQUAL, NOTEQUAL, ALWAYS, with a **reference** value $r$ and a **read mask** $m$;
- three **operations** for each face, front and back: sfail when the stencil test fails, dpfail when the stencil test passes and the depth test fails, dppass when both pass;
- a **write mask** $w$, the bits that an update may change.

The operations are KEEP, ZERO, REPLACE (store $r$), INCR and DECR (add or take away one, and stop at $2^s - 1$ or at 0), INCR_WRAP and DECR_WRAP (add or take away one modulo $2^s$), and INVERT (flip all bits). These are the names and the rules of OpenGL, and Direct3D and Vulkan have the same set.

The type has two operations:

- **TEST(i, j)** returns $(r \mathbin{\&} m)$ FUNC $(S[j][i] \mathbin{\&} m)$. The reference is on the left: LESS passes when $r < S$, after the masks.
- **FRAGMENT(i, j, face, depth pass)** runs one fragment at pixel $(i, j)$: it calls TEST, picks one of the three operations of the face, and writes the result through the write mask. It returns whether the fragment passed both tests and may write color.

The fragments come from the rasterizer, so the pixel model is the one of [triangle rasterization](/triangle-rasterization/): a pixel is a point sample at its center $(i + 1/2, j + 1/2)$, as in OpenGL and Direct3D 10, not a little square, and a center on an edge goes to one triangle by the [top-left fill rule](/top-left-fill-rule/).

## Representation

The buffer is an array of $WH$ words of $s$ bits each, often packed with a 24-bit depth value into one 32-bit word per pixel. The state is a few registers: FUNC, $r$, $m$, $w$, and three operations for each of the two faces. In the model of the [word RAM](/word-ram/) with words of at least $s$ bits, each test and each update is $O(1)$ bitwise and integer operations. The implementation here keeps the values as Python integers in a list of rows, and it takes the vertex coordinates of the triangles as exact fractions, so the decision of which pixels a triangle covers is exact. In hardware, vertices are snapped to a grid of subpixel steps and the edge tests are integer tests; with vertices in [IEEE 754](/ieee-754/) floating point and no snap, a pixel center on a shared edge can go to both triangles or to neither, and the counts are then off by one.

## Operations

```pseudo id=main
TEST(i, j)
L1  return (r & m) FUNC (S[j][i] & m)

FRAGMENT(i, j, face, depthPass)
    passed ← TEST(i, j); (sfail, dpfail, dppass) ← the operations of face
L2  op ← sfail if not passed, else dppass if depthPass, else dpfail
L3  S[j][i] ← (S[j][i] & ¬w) | (op(S[j][i]) & w)
    return passed and depthPass

FILL-PATH(rings, rule)                                   ▷ stencil, then cover
L4  FUNC ← ALWAYS; if rule is nonzero then dppass ← INCR_WRAP for front faces, DECR_WRAP for back faces
                    else dppass ← INVERT for both faces, w ← 1
L5  for each ring (v0, ..., v(m−1)) and each k from 1 to m − 2, let T ← (v0, vk, vk+1), front when orient(T) > 0
L6      for each pixel (i, j) that T covers do FRAGMENT(i, j, the face of T, true)
L7  FUNC ← NOTEQUAL, r ← 0, m ← all bits (nonzero) or 1 (even-odd); w ← all bits; all three operations ← ZERO
L8  for each pixel (i, j) do if FRAGMENT(i, j, front, true) then cover (i, j)
```

FILL-PATH is the standard use that shows the whole type. The stencil pass on lines L4 to L6 writes no color. It draws a fan of triangles from the first vertex of each ring, and each covered pixel counts $+1$ for a front-facing triangle and $-1$ for a back-facing one. The cover pass on lines L7 and L8 draws one shape over the path, in practice its bounding box, and writes color where the count is not zero. It also resets the count to zero for the next path.

## Example

Fill the five-point star with the vertices $(5, 0)$, $(8, 10)$, $(0, 4)$, $(10, 4)$, $(2, 10)$ on an 11 by 11 buffer of 8 bits. The fan from $(5, 0)$ has three triangles.

| Triangle | orient | Face | Pixels covered |
|---|---|---|---|
| $(5, 0)$, $(8, 10)$, $(0, 4)$ | $62$ | front, INCR_WRAP | 31 |
| $(5, 0)$, $(0, 4)$, $(10, 4)$ | $-40$ | back, DECR_WRAP | 20 |
| $(5, 0)$, $(10, 4)$, $(2, 10)$ | $62$ | front, INCR_WRAP | 31 |

After the 82 fragments of the stencil pass the buffer holds these values, with `.` for 0 and row 0 at the top.

```text
...........
...........
....11.....
....11.....
.11122111..
..122221...
...2222....
...1111....
..11..11...
..1....1...
...........
```

The middle triangle runs the other way around and takes one away in rows 0 to 3. Each of its 20 pixels is also covered by one or two front-facing triangles, so these pixels end at 0 or 1, and only the top tip stays filled. The pentagon in the middle holds 2, which is its winding number. The cover pass with NOTEQUAL 0 and mask all ones covers each nonzero pixel, which is the nonzero fill. With INVERT and write mask 1, bit 0 holds the parity, the pixels with value 2 are left out, and the cover pass with mask 1 gives the even-odd fill. Both pictures are on the page of [polygon scan conversion](/polygon-scan-conversion/). The values do not depend on the order of the 82 fragments.

## Correctness

The fan of a ring $v_0, \dots, v_{m-1}$ has the triangles $T_k = (v_0, v_k, v_{k+1})$. As closed chains, the boundaries of the $T_k$ add up to the ring, because each diagonal $v_0 v_k$ appears once in each direction. Winding numbers add over chains, so for each point $p$ on no line through two vertices, $w(p) = \sum_k \sigma_k [p \in T_k]$, where $\sigma_k$ is the sign of the orientation of $T_k$. The rasterizer covers a pixel for $T_k$ exactly when the shifted center $c + (\varepsilon, \varepsilon^2)$ is inside $T_k$, and this point is on no such line. INCR_WRAP and DECR_WRAP are $+1$ and $-1$ modulo $2^s$, which commute, so after the stencil pass each pixel holds $w \bmod 2^s$ at its shifted center, in any order of the fragments. With INVERT and write mask 1, bit 0 holds $w \bmod 2$. The cover test NOTEQUAL 0 under the mask then selects $w \not\equiv 0 \pmod{2^s}$, or $w$ odd. The full proof is below.

## Complexity

| Operation | Time | Notes |
|---|---|---|
| TEST | $O(1)$ | two masks and one comparison |
| FRAGMENT | $O(1)$ | one test, one operation, one masked write |
| clear | $O(W H)$ | in hardware, often a fast clear of tiles |
| FILL-PATH | $O(n + F + B)$ | $F$ fragments in the stencil pass, $B$ pixels in the cover shape |

Here $n$ is the number of vertices, $F$ is the total number of pixels that the fan triangles cover, and $B$ is the number of pixels of the cover shape, at most $W H$. The fan can cover the same pixel many times, so $F$ can be as large as $\Theta(n W H)$ for a long path that crosses itself, and $F$ does not depend on how many pixels end up filled. The space is $s W H$ bits. The implementation tests each pixel center of the image for each triangle, so it takes $O(n W H)$ time for the stencil pass; a rasterizer that walks the bounding box or the spans of each triangle takes the bound of the table.

## Variants

- **Two-sided stencil.** Separate operations for front and back faces let one pass do both the increments and the decrements. OpenGL has had this since version 2.0, as `glStencilOpSeparate`. Without it, the path is drawn twice with face culling.
- **Wrapping or saturating.** INCR and DECR stop at the ends of the range. The wrapping forms came later (OpenGL 1.4) and are the ones that counting needs.
- **Shadow volumes.** The [shadow volume algorithm](/shadow-volume-algorithm/) uses the same counting: it draws the faces of the shadow volumes and counts, at each pixel, how many volumes the visible point is inside. The z-pass form counts on dppass, and the z-fail form counts on dpfail. That page covers the method; this page covers the buffer.
- **Masks and portals.** REPLACE with ALWAYS writes a shape into the buffer, and a later EQUAL test draws only inside it, as for mirrors, portals and cut-outs in user interfaces.
- **Stencil export.** Some newer GPUs let a fragment shader write the reference value per fragment, so one pass can write many different values.

## When to use it

Use it on a GPU to fill paths of any shape under the nonzero or even-odd rule, with no sorting of edges and no tessellation into non-overlapping triangles; to clip drawing to a region of any shape; and to count shadow volumes. On a CPU, or when the winding numbers can be large, [scanline polygon fill](/scanline-polygon-fill/) computes the exact winding sum along each row and needs no buffer of counts. For triangles that do not overlap, plain [triangle rasterization](/triangle-rasterization/) needs no stencil at all.

## Pitfalls

- **Saturating counts.** INCR and DECR do not commute: from 0, DECR then INCR gives 1, but the true count is 0. A fill that counts with them depends on the order of the triangles and covers wrong pixels. Use INCR_WRAP and DECR_WRAP.
- **Too few bits.** The count is kept modulo $2^s$. A pixel that the path winds around $2^s$ times looks outside. With one bit, the nonzero pass gives the even-odd fill.
- **The order of the comparison.** The test is $(r \mathbin{\&} m)$ FUNC $(S \mathbin{\&} m)$, so LESS passes when the reference is smaller than the stored value, not the other way around.
- **The reference is clamped.** OpenGL clamps $r$ to $[0, 2^s - 1]$ before the test, so a reference of 256 on an 8-bit buffer acts as 255.
- **The write mask also limits clears.** In OpenGL the stencil write mask applies to the clear of the buffer, so a mask left at 1 clears only bit 0.
- **Shared edges counted twice.** Each fan triangle must follow the [top-left fill rule](/top-left-fill-rule/), so a pixel center on a diagonal $v_0 v_k$ goes to exactly one of the two triangles next to it. Without it, the count is off by one along the diagonals.
- **Which face is front.** The sign of the count depends on which face is called front, but the nonzero test and the parity do not, so this choice does not matter as long as it is the same for all triangles of a path.

## Implementations

## History

Stencil planes appeared in the graphics workstations of the 1980s, and OpenGL 1.0 in 1992 defined the stencil test and the operations KEEP, ZERO, REPLACE, INCR, DECR and INVERT. Heidmann in 1991 showed how to count shadow volumes in the stencil buffer, which made the method of Crow practical on such hardware. The fill of concave polygons by a fan of triangles with INVERT is an old OpenGL technique. The wrapping operations entered the core of OpenGL in version 1.4, and two-sided stencil in version 2.0. Kilgard and Bolz in 2012 built GPU path rendering on the two steps of stencil, then cover, for both fill rules.

## References
