---
tag: 1XFX5C
kind: algorithm
slug: a-buffer
name: A-buffer
aliases:
- anti-aliased z-buffer
area: graphics-and-signals/visibility
level: advanced
summary: A z-buffer that keeps a list of fragments per pixel, each with a subpixel coverage mask, and resolves the list in depth order for antialiased edges and transparency.
solves: [hidden-surface-removal]
model: real-ram
complexity:
  vars: {n: the number of triangles, W: the image width in pixels, H: the image height in pixels, F: "the number of pairs of a triangle and a pixel that it meets, at least the number of fragments", s: the number of subpixel cells per pixel, m: the largest number of fragments in one pixel}
  time: {worst: O(W H + n + F (s + log m))}
  space: {extra: O(W H + F)}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1984
  people: [Loren Carpenter]
  note: Carpenter described the A-buffer in 1984 as the hidden surface method of the REYES renderer at Lucasfilm, with a 4 by 8 bit mask per fragment.
prereqs: [z-buffer, alpha-blending, antialiasing]
see_also: [depth-peeling, multisample-antialiasing, supersampling-antialiasing, porter-duff-compositing, image-compositing, linked-list, object-space-vs-image-space, warnock-algorithm]
sources:
  - paper: doi:10.1145/964965.808585
    title: Loren Carpenter, The A-buffer, an antialiased hidden surface method, Computer Graphics 18(3), SIGGRAPH 1984, pages 103 to 108
    locator: the whole paper (the pixel structure, the fragment with its 4 by 8 bit mask, opacity, area, object tag and depth range, and the recursive packing procedure that resolves a pixel)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Section 5.5 (transparency, order-independent methods and per-pixel fragment lists)
---

The A-buffer extends the [z-buffer](/z-buffer/) from one depth per pixel to a list of *fragments* per pixel. A fragment is the part of one surface inside one pixel: its depth, its color, its opacity and a bit mask of the subpixel cells it covers. When all surfaces are in the lists, each pixel is resolved front to back: the masks tell which part of the pixel each fragment covers, and the opacities tell how much of what is behind shows through. So one pass gives [antialiased](/antialiasing/) edges and correct transparency in any draw order, at the cost of memory that grows with the depth complexity of the scene.

## In plain words

A normal depth buffer keeps one thing for each dot of the screen: the nearest surface. That gives jagged edges, because a dot on an edge is all one color, and it cannot show glass, because only the nearest surface is kept.

The A-buffer keeps a short list for each dot. Each item in the list says: this surface is here, at this distance, with this color, it covers these small parts of the dot, and it is this clear. At the end, for each dot, it sorts the list from near to far and works out the color. A surface that covers half of the dot gives half of the color. A clear surface lets some of the color behind it come through.

## The problem

The input is a list of $n$ triangles in screen space, each with a color and an opacity $\alpha \in [0, 1]$, an image of $W \times H$ pixels and a background color. A vertex is $(x, y, z)$ with $x$ to the right and $y$ down in pixel units, and $z$ the depth, smaller nearer, affine in $x$ and $y$ on each triangle. Pixel $(i, j)$ is the square $[i, i + 1] \times [j, j + 1]$, split into $s = s_x s_y$ cells; cell $(a, b)$ has center $(i + \tfrac{2a + 1}{2 s_x}, j + \tfrac{2b + 1}{2 s_y})$, and bit $a + s_x b$ of a mask stands for it. A triangle covers a cell when it covers its center under the [top-left fill rule](/top-left-fill-rule/). Carpenter used $s_x = 8$ and $s_y = 4$, a 32-bit mask.

The output at a pixel is the mean over its cells of the front-to-back [over](/alpha-blending/) composite, at the center of the cell, of the triangles that cover the cell, then the background. The A-buffer gives each fragment one depth, the depth of its plane at the pixel center $(i + \tfrac12, j + \tfrac12)$, and orders the fragments by this depth and then by index. So the output is exact in this sense: it equals the mean over the cells of the composite in the order of the pixel-center depths. It equals the true per-cell composite when the order of the surfaces does not change inside a pixel, for example when the triangles are parallel to the screen.

## The algorithm

Each pixel holds a list of fragments and at most one *full* fragment: the nearest opaque fragment that covers all $s$ cells. Nothing behind the full fragment can be seen, so it is not stored.

```pseudo id=main
A-BUFFER(W, H, T, s)
L1  for each pixel: full ← none, list ← empty
L2  for each triangle t (index k) in T do
L3      for each pixel where t covers a cell: f ← (depth at the pixel center, k, mask, color, α); INSERT(f)

INSERT(f)                                          ▷ into the list of its pixel
L4  if full ≠ none and (f.z, f.k) > (full.z, full.k) then return       ▷ hidden
L5  if f.α = 1 and f.mask covers all cells then
L6      full ← f; remove from the list each fragment behind f
L7  else append f to the list

RESOLVE(pixel)
L8  order ← the list sorted by (z, k), then full if it exists
L9  G ← {(all cells, 1)}                ▷ disjoint cell sets, each with its transmittance τ
L10 for each fragment f in order do
L11     split each (M, τ) in G into M ∩ f.mask and M \ f.mask
L12     add τ · f.α · |M ∩ f.mask| · f.color to the sum
L13     keep (M ∩ f.mask, τ (1 − f.α)) if f.α < 1, and keep (M \ f.mask, τ)
L14 for each (M, τ) left in G: add τ · |M| · background to the sum
L15 return the sum / s
```

Lines L1 to L7 are the first pass, in any order of the triangles. Lines L8 to L15 resolve one pixel, after all triangles are in. The sets in $G$ are disjoint, and each holds cells that the same nearer fragments cover, so they share one transmittance $\tau$. A set with $\tau = 0$ is dropped, since nothing behind it shows. This loop is an iterative form of Carpenter's recursive packing procedure, which calls itself on the inside and the outside mask of each fragment.

## Example

One pixel with $8 \times 4$ cells. Two opaque red triangles at depth 1 cover its left half, the 16 cells with $x < \tfrac12$. An opaque blue triangle at depth 2 covers the 16 cells below the line $x + y = 1$; 4 of them are in the right half. The background is black. Red is nearer, so 16 cells are red, 4 are blue and 12 are black, and the pixel is
$$\left(\tfrac{16 \cdot 255}{32}, 0, \tfrac{4 \cdot 255}{32}\right) = (127.5, 0, 31.875).$$

Now add a green triangle with $\alpha = \tfrac12$ at depth $\tfrac12$, in front of all, that covers 12 cells: 1 red cell, the 4 blue cells of the right half and 7 black cells. Line L12 adds $\tfrac12 \cdot 12$ cells of green. The red set splits into 1 cell with $\tau = \tfrac12$ and 15 cells with $\tau = 1$, and the blue cells get $\tau = \tfrac12$. The result is
$$\left(\tfrac{(15 + \frac12) \cdot 255}{32}, \tfrac{12 \cdot \frac12 \cdot 255}{32}, \tfrac{4 \cdot \frac12 \cdot 255}{32}\right) = \left(\tfrac{7905}{64}, \tfrac{765}{16}, \tfrac{255}{16}\right).$$

**One depth per fragment.** Two opaque surfaces that cross at $x = \tfrac12$ inside one pixel should each show in half of it. Both fragments get the depth at the pixel center, so one of them wins in all cells that both cover. Carpenter's fragments keep a least and a greatest depth to estimate this case; see the variants.

## Correctness

Fix a cell $c$ of a pixel. The fragments whose masks contain $c$ are those of the triangles that cover $c$ (line L3), less those behind the full fragment, which add nothing at $c$ because the full fragment is opaque and covers $c$. The loop of lines L10 to L13 keeps this invariant: the sets of $G$ are disjoint, the cell $c$ is in a set of $G$ exactly when the fragments before the current one let light through at $c$, and the $\tau$ of that set is the product of $1 - \alpha$ over those fragments that contain $c$. So line L12 adds at $c$ the term $\tau \alpha$ times the color, which is the over operator in front-to-back form, and line L14 adds the background term. Summing over the cells and dividing by $s$ gives the mean. The proof file gives the details.

## Complexity

Take $s$ at most the word size, so that a mask operation costs $O(1)$, as with Carpenter's 32-bit masks. Line L1 costs $O(W H)$. Line L3 visits, for each triangle, the pixels it meets, and computes a mask with $s$ cell tests per pixel: $O(n + F s)$ in total, where $F$ counts the pairs of a triangle and a pixel it meets. Lines L4 to L7 cost $O(1)$ each, except the removal of line L6, which costs $O(1)$ per fragment removed. Resolving a pixel with $f$ fragments costs $O(f \log f)$ for the sort and $O(f \min(s, f))$ for the mask splits, since $G$ never holds more than $s$ nonempty disjoint sets. Over the image this is $O(W H + F (s + \log m))$. The lists take $O(F)$ space in total, and the pixel headers $O(W H)$.

## Properties

- **Order independent.** The output does not depend on the order of the triangles, since each pixel is sorted before it is resolved and ties are broken by index.
- **Antialiasing at edges.** Coverage is computed at $s$ cells, so an edge pixel gets the fraction of the cells each surface covers, but the shading is done once per fragment, not once per cell. This is the idea of [multisample antialiasing](/multisample-antialiasing/), which keeps a fixed number of samples in place of lists.
- **Transparency.** Transparent surfaces are composited in depth order without a sort of the scene, as needed for [alpha blending](/alpha-blending/) to be correct.
- **Memory grows with the scene.** A pixel holds as many fragments as there are visible or transparent surfaces in it. The full fragment bounds this for opaque interiors: an opaque surface that covers a pixel removes all fragments behind it.
- **Image space.** The answers are per cell; see [object space and image space](/object-space-vs-image-space/).

## Variants and improvements

- **Depth ranges.** Carpenter's fragment holds the least and greatest depth of the surface in the pixel, and the resolve step estimates the visible part of two fragments whose depth ranges overlap, from these ranges. This handles surfaces that cross in a pixel better than one depth, but it is still an estimate.
- **Merging fragments.** Carpenter's fragments also carry an object tag and the area of coverage; fragments of the same surface in one pixel can be combined, which saves memory at the shared edges of a mesh.
- **Per-pixel linked lists on GPUs.** A fragment shader appends each fragment to a [linked list](/linked-list/) per pixel in a global buffer, with an atomic counter, and a second pass sorts and resolves each list. This is the A-buffer with point samples in place of masks.
- **Fixed-size buffers.** The k-buffer and similar methods keep only the $k$ nearest fragments per pixel and merge the rest, which bounds the memory but gives an approximation.
- **Multiple passes in place of lists.** [Depth peeling](/depth-peeling/) gets the layers in depth order with one ordinary z-buffer per pass, and needs no lists, at the cost of one pass per layer.

## When to use it

Use it in an offline renderer that needs antialiased edges and correct transparency in one pass over unsorted geometry, as REYES did. On GPUs use per-pixel lists when the number of transparent layers is moderate and memory is available; with an unbounded number of layers, the memory is not bounded, and [depth peeling](/depth-peeling/) or approximate order-independent methods are safer.

## Pitfalls

- **Interpenetration.** One depth per fragment gives one winner across a whole pixel where two surfaces cross. Keep depth ranges, or split the fragment.
- **The full fragment.** A fragment can replace the full fragment only if it is opaque and covers all cells; a transparent fragment that covers the pixel must stay in the list, or what is behind it is lost.
- **Ties.** Fragments with equal depth must be ordered by a fixed key, such as the index, or the result depends on the draw order, the same problem as [z-fighting](/z-fighting/).
- **Overflow.** A fixed pool of fragments can run out in pixels of high depth complexity. A renderer must detect this and fall back, not drop fragments without notice.
- **Mask sampling and the fill rule.** Two triangles that share an edge must not both cover a cell on it, or the coverage of the pixel adds up to more than 1. The top-left rule at the cell centers prevents this.

## Implementations

## History

Carpenter described the A-buffer in 1984 as the hidden surface method of the REYES renderer at Lucasfilm. The name stands for an anti-aliased, area-averaged, accumulation buffer. It joined three ideas in one structure: the depth test of the z-buffer, subpixel coverage masks and depth-ordered compositing. On GPUs, per-pixel fragment lists became practical when shaders got atomic counters and writes to buffers.

## References
