---
tag: ZVD2J6
kind: algorithm
slug: morphological-antialiasing
name: Morphological antialiasing
aliases:
- MLAA
area: graphics-and-signals/rasterization
level: advanced
summary: Post-process antialiasing that detects edge patterns in the final image and blends them.
solves: [antialiasing]
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels}
  time: {worst: Θ(W H), average: Θ(W H), best: Θ(W H)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, in_place: false}
history:
  year: 2009
  people: [Alexander Reshetov]
  note: Reshetov built MLAA as a post-process for ray tracers, which take one sample per pixel and have no hardware multisampling.
prereqs: [antialiasing, pixel]
see_also: [supersampling-antialiasing, multisample-antialiasing, temporal-antialiasing, edge-detection, reconstruction-filter, alpha-blending]
sources:
  - paper: doi:10.1145/1572769.1572787
    title: Alexander Reshetov, Morphological antialiasing, Proceedings of the Conference on High Performance Graphics 2009, pages 109 to 116
    locator: Section 2.1 (the three steps, the Z, U and L shapes, Figures 2 and 3, and equation 2), Section 2.2 (color images and the split positions of equation 3) and Section 3 (limitations)
  - paper: "Jorge Jimenez, Jose I. Echevarria, Tiago Sousa and Diego Gutierrez, SMAA: Enhanced Subpixel Morphological Antialiasing, Computer Graphics Forum 31(2), Eurographics 2012"
    locator: the whole paper (edge detection by local contrast, the precomputed area tables, diagonal patterns and the temporal and multisample variants)
  - paper: "Jorge Jimenez, Diego Gutierrez, Jason Yang, Alexander Reshetov and others, Filtering Approaches for Real-Time Anti-Aliasing, SIGGRAPH 2011 course"
    locator: the course notes (the survey of MLAA and its GPU versions)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, 2018
    locator: Chapter 5, Section 5.4, Aliasing and Antialiasing (the part on morphological methods)
---

Morphological antialiasing (MLAA) is a post-process that works on a finished image with one sample per [pixel](/pixel/). It finds the staircase patterns that a sampled edge leaves between pixels of different colors, guesses the straight edge that made each staircase, and blends each pixel along the staircase with its neighbor across the edge, by the area that the guessed edge cuts from the pixel. It needs no extra samples and no access to the scene, and its cost is linear in the number of pixels. It is a heuristic: it reconstructs well a long edge whose staircase it reads correctly, and it cannot restore features smaller than a pixel.

## In plain words

When a renderer takes one sample per pixel, a slanted edge turns into a staircase of whole pixels. MLAA looks at the finished picture and finds these staircases by comparing each pixel with its neighbors. Each step of a staircase has a long flat part and a short jump. MLAA draws a straight line from the middle of one jump to the middle of the next flat part, which is its best guess of where the real edge ran. Each pixel along the flat part then takes a little of the color of the pixel on the other side of the edge, as much as the guessed line cuts off from it. The steps turn into a smooth ramp. MLAA needs only the picture, so it works with any renderer, but it cannot bring back thin lines or small details that the samples missed.

## The problem

The input is an image of $W \times H$ pixels with one color per pixel, and a threshold. Pixel $(i, j)$ is a point sample at its center; MLAA treats it as the cell $[i, i+1] \times [j, j+1]$ and estimates the area that the true edge cuts from that cell. Rows grow downward. Two neighbor pixels are *different* if some channel differs by more than the threshold. Pixels outside the image repeat the border pixels, so no separation line runs along the border. The output is an image of the same size, an estimate of the box-filtered image of the [antialiasing](/antialiasing/) problem near edges. Colors should be linear values; Reshetov used a test on the 4 most significant bits of each 8-bit channel to decide whether two pixels differ.

## The algorithm

```pseudo id=main
MLAA(image)                            ▷ the pass along rows; the pass along columns is the same on the transposed image
L1  for each boundary between two neighbor rows j and j + 1 do
L2      for each separation line: a maximal run of columns a ≤ i < b where (i, j) and (i, j + 1) differ do
L3          at each end vertex, find the secondary edge: a difference between the two columns there, in row j only (up) or in row j + 1 only (down)
L4          if both ends have one then split the line in the middle into two L shapes        ▷ a Z or a U shape
L5          else if one end has one then make one L shape over the whole line
L6          for each L shape of primary length d, from its secondary edge do
L7              for each cell k along it, on the side of the secondary edge, take a ← the area under the line from height 1/2 at 0 to height 0 at d
L8                  c[cell] ← (1 − a) c[cell] + a · c₀[cell across the primary edge]
L9  return c
```

Line L2 is the first step of the paper: it finds the *separation lines*, the runs of differences along one boundary. Line L3 is the second step: it looks at the two ends of each line for an orthogonal separation segment, the *secondary edge*. If the two secondary edges point to opposite sides, the pattern is a *Z shape*; if they point to the same side, it is a *U shape*. Both are split in the middle into two *L shapes*. A line with a secondary edge at only one end, which happens mainly at the image border, is one L shape. Lines L6 to L8 are the third step. The line from the middle of the secondary edge to the far end of the L shape is the guessed edge. Each cell along the primary edge, on the side of the secondary edge, is blended with the cell on the other side of the primary edge, $c_0$ being the input color, by the area $a$ of the trapezoid between the guessed edge and the primary edge. The blends are applied one after another: first all lines between rows, then all lines between columns.

## Example

**The areas of Figure 3 of the paper.** A Z shape of length 3 splits into two L shapes of length $3/2$. The guessed edge falls from height $1/2$ to $0$ over $3/2$ pixels, so it has height $1/6$ at the end of the first cell. The first cell gets the area $(1/2 + 1/6)/2 = 1/3$, and the second cell the triangle $\frac12 \cdot \frac12 \cdot \frac16 = 1/24$. A white cell with black across the edge becomes $2/3$, and the next one $23/24$.

**A straight edge.** Sample the region below the line $y = 1/2 + x/4$ (white is 1, black is 0) on an image 16 pixels wide. The result is a staircase with steps 4 pixels long. In row 2, the columns 6 to 9 hold 1, 1, 0, 0. The separation line between rows 1 and 2 and the one between rows 2 and 3 are Z shapes of length 4, and their guessed edges lie exactly on the true line. After the pass along rows, the four pixels hold $7/8$, $5/8$, $3/8$ and $1/8$, which are their exact covered areas. The pass along columns then finds, at each step, a vertical separation line of length 1 with secondary edges on opposite sides, and blends the two pixels beside the step by $1/8$. The final values are $7/8$, $35/64$, $29/64$ and $1/8$. This is the slight blur that Reshetov describes for a line that belongs to more than one pattern.

## Correctness

MLAA has no exact guarantee for a general image: it guesses edges from a sampled picture, and many scenes give the same picture. Three properties do hold. First, each blend weight is the exact area between the guessed edge and the primary edge inside the cell; the weights of an L shape of length $d$ lie in $[0, 1/2)$ and sum to $d/4$. Second, each blend is a convex combination of the cell and an input pixel, so no channel leaves the range of the input, and for a black-and-white image the order of the blends does not matter. Third, for a straight edge of slope $1/L$ that passes through the middles of the secondary edges, the guessed edge is the true edge, and the pass along rows gives every pixel away from the left and right borders its exact covered area. The full proofs are below.

## Complexity

- **Time.** The pass along rows compares $\Theta(W H)$ pairs of neighbors. Each separation line of length $n$ makes at most $n + 1$ blends, and each pixel boundary belongs to at most one line, so there are $O(W H)$ blends. The pass along columns is the same, so the total is $\Theta(W H)$.
- **Memory.** One copy of the input image, $\Theta(W H)$, because the blends read the input colors across each edge. GPU versions store an edge texture and a blend weight texture of the same size.
- **Independent of the scene.** The cost does not depend on the number of triangles, lights or samples of the renderer.

## Properties

- **One sample per pixel.** It needs only the final colors, so it works after ray tracing, deferred shading or any other renderer.
- **No subpixel features.** A line thinner than a pixel that falls between samples is missing from the input, and MLAA cannot restore it. Reshetov shows this with rows of thin quads that MLAA cannot fix.
- **Not temporally stable.** A small motion of an edge changes the staircase and so the blend, so edges can shimmer in motion.
- **Blurs text and textures.** Any strong contrast between neighbors counts as an edge, so sharp texture detail and text get blended too.
- **Convex.** Each output value is a convex combination of input values.

## Variants and improvements

- **Color images.** For color images Reshetov does not split Z and U shapes at the middle: he chooses the split points so that the blended colors of two shapes that meet agree, by solving a small linear system, and he skips shapes whose solution lies outside $[0, 1]$.
- **GPU versions.** Jimenez and coworkers moved MLAA to the GPU in three passes: an edge texture, blend weights from a precomputed table of areas indexed by the distances to the ends of the line, and a blend pass.
- **SMAA.** Enhanced subpixel morphological antialiasing (Jimenez et al., 2012) adds an edge test by local contrast, diagonal patterns and sharp corner handling, and combines the morphological pass with a few multisamples or with temporal accumulation. It is a successor of MLAA, not the same method.
- **FXAA and CMAA.** Other post-process filters search for edges in the luminance and blend along them, with simpler rules and lower cost.
- **Depth and normal edges.** Edge detection on depth or on object identifiers in place of colors finds geometric edges only, and leaves textures alone.

## When to use it

Use MLAA or one of its successors when the renderer takes one sample per pixel and multisampling is unavailable or too expensive, for example with deferred shading, on consoles and with ray tracing. It costs a fixed time per pixel, independent of the scene. Do not rely on it for thin geometry, for text, or where temporal stability matters most; there, [temporal antialiasing](/temporal-antialiasing/) or [supersampling](/supersampling-antialiasing/) works better, and both can be combined with a morphological pass.

## Pitfalls

- **The threshold.** A low threshold blends texture detail and costs time; a high one misses low-contrast edges. Edge detection in perceived luminance is a common choice.
- **Order of the blends.** In a color image, a pixel that belongs to several shapes gets several blends, and the result depends slightly on their order. State the order, as this page does.
- **Ambiguous ends.** A vertex with separation segments on both sides of the line gives no clear secondary edge. This page treats such an end as having none; other versions pick a side.
- **Running before tone mapping or after the user interface.** MLAA should run on the final scene colors, after tone mapping and before text and user interface elements are drawn on top.
- **Expecting supersampling quality.** MLAA makes jagged edges smooth, but it does not compute coverage; its areas are guesses from the staircase.

## Implementations

## History

Reshetov (2009) introduced MLAA at High Performance Graphics as a CPU post-process for ray tracing, inspired by morphological image analysis. Within two years, GPU versions by Jimenez and coworkers, by game developers, and FXAA by Lottes made post-process antialiasing common in real-time rendering, as surveyed in a 2011 SIGGRAPH course. SMAA (2012) refined the pattern search and combined it with multisampling and temporal samples.

## References
