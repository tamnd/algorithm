---
tag: AXXSRR
kind: algorithm
slug: multi-band-blending
name: Multi-band blending
aliases:
- Burt-Adelson blending
- Laplacian pyramid blending
area: computer-vision/multiple-view-geometry
level: advanced
summary: Blend two images by blending each level of their Laplacian pyramids with a mask smoothed to the same level, so low frequencies mix widely and high ones narrowly.
solves: [image-stitching]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, N: the number of pyramid levels above the image}
  time: {worst: Θ(W H + N), average: Θ(W H + N), best: Θ(W H + N)}
  space: {extra: Θ(W H + N)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1983
  people: [Peter J. Burt, Edward H. Adelson]
  note: Burt and Adelson introduced the multiresolution spline, which joins two images band by band through their Laplacian pyramids. Brown and Lowe made it the blending step of their automatic panorama stitcher in 2007.
prereqs: [laplacian-pyramid, gaussian-pyramid]
see_also: [image-stitching, image-compositing, alpha-blending, poisson-image-editing, distance-transform, image-pyramid, linear-filtering]
sources:
  - paper: doi:10.1145/245.247
    title: "Peter J. Burt and Edward H. Adelson, A multiresolution spline with application to image mosaics, ACM Transactions on Graphics 2(4), 1983, 217-236"
    locator: the multiresolution spline (each Laplacian level of the result mixes the levels of the two images, with weights from the Gaussian pyramid of the region mask)
  - paper: doi:10.1007/s11263-006-0002-3
    title: "Matthew Brown and David G. Lowe, Automatic panoramic image stitching using invariant features, International Journal of Computer Vision 74(1), 2007, 59-73"
    locator: "Section 7, Multi-band blending (max-weight maps, bands of width sigma, sqrt(2k+1) sigma for the next bands, and the normalized sum over images); Figure 7"
---

Multi-band blending joins two images $A$ and $B$ along a mask $M$, which is 1 where the result should come from $A$ and 0 where it should come from $B$. It splits both images into frequency bands with a [Laplacian pyramid](/laplacian-pyramid/), mixes each band with the mask blurred to the same scale by a [Gaussian pyramid](/gaussian-pyramid/), and adds the mixed bands back. Coarse bands thus cross the seam over a wide zone and fine bands over a narrow one, so the seam shows neither as a step nor as a ghosted double edge. Plain [alpha blending](/alpha-blending/) mixes all frequencies with one weight map; [Poisson image editing](/poisson-image-editing/) mixes gradients and solves a linear system. This page gives the algorithm for two images; the whole task of making a panorama is [image stitching](/image-stitching/).

## In plain words

When you put two photos side by side, a hard cut shows a line where the brightness jumps. If you instead fade one photo into the other over a wide strip, small details from both photos show at the same time, and edges look doubled. Multi-band blending avoids both faults. It splits each photo into layers, from broad shading to fine detail. Broad shading is faded over a wide strip, so there is no visible jump in brightness. Fine detail is faded over a narrow strip, so each detail comes almost only from one photo and nothing looks doubled. At the end, the faded layers are added back into one picture. The width of each strip follows the size of the features in its layer.

## The problem

**Input.** Two images $A$ and $B$ of size $W \times H$ with real pixel values, a mask $M$ of the same size with values in $[0, 1]$, and a number of levels $N \ge 0$. For a color image, run the algorithm on each channel.

**Output.** The image $S$ obtained by collapsing the pyramid of mixed bands
$$L^S_l = G^M_l \odot L^A_l + (1 - G^M_l) \odot L^B_l, \qquad l = 0, \ldots, N,$$
where $G^M$ is the Gaussian pyramid of $M$, $L^A$ and $L^B$ are the Laplacian pyramids of $A$ and $B$, and $\odot$ is the product sample by sample. REDUCE and EXPAND are those of the [Laplacian pyramid](/laplacian-pyramid/) page: the 5-tap kernel $\frac{1}{16}(1, 4, 6, 4, 1)$, the reflect-101 border, level sizes $\lceil W_l / 2 \rceil \times \lceil H_l / 2 \rceil$, and EXPAND by zero insertion and a blur with gain 2 per axis.

## The algorithm

```pseudo id=main
MULTI-BAND-BLEND(A, B, M, N)
L1  G^M <- the Gaussian pyramid of M with levels 0 .. N
L2  G^A, G^B <- the Gaussian pyramids of A and B with levels 0 .. N
L3  L^A, L^B <- the Laplacian pyramids: L_l = G_l - EXPAND(G_(l+1)) for l < N, and L_N = G_N
L4  for l <- 0 to N
L5      L^S_l <- G^M_l * L^A_l + (1 - G^M_l) * L^B_l, sample by sample
L6  S <- L^S_N
L7  for l <- N - 1 down to 0
L8      S <- L^S_l + EXPAND(S) to the size of level l
L9  return S
```

Line L1 smooths the mask more at each level, so the weight at level $l$ changes over a zone about $2^l$ pixels wide in the original image. Lines L2 and L3 build the bands of both images. Line L5 is a plain alpha blend of one band with the matching mask level. Lines L6 to L8 are the reconstruction of the Laplacian pyramid, applied to the mixed bands. At level 0 the mask is not smoothed at all, so the finest detail switches from $A$ to $B$ at the seam of $M$; the top level $N$ holds the mean brightness and mixes it with the most smoothed mask.

## Example

One row of 8 pixels: $A = (16, 16, 16, 16, 16, 16, 16, 16)$, $B = (0, 0, 0, 0, 0, 0, 0, 0)$ and $M = (1, 1, 1, 1, 0, 0, 0, 0)$, with $N = 1$. The height is 1, so only the horizontal axis is filtered.

| line | value |
|---|---|
| L1 | $G^M_0 = (1, 1, 1, 1, 0, 0, 0, 0)$, $G^M_1 = (1, \frac{15}{16}, \frac{5}{16}, 0)$ |
| L2 | $G^A_0 = 16$ at all 8 samples, $G^A_1 = (16, 16, 16, 16)$; $G^B$ is 0 |
| L3 | $L^A_0 = 0$ at all 8 samples, $L^A_1 = (16, 16, 16, 16)$; $L^B$ is 0 |
| L4, L5 | $L^S_0 = 0$ at all 8 samples, $L^S_1 = (16, 15, 5, 0)$ |
| L6 | $S = (16, 15, 5, 0)$ |
| L7, L8 | $S = 0 + \mathrm{EXPAND}(16, 15, 5, 0) = (\frac{63}{4}, \frac{31}{2}, \frac{111}{8}, 10, \frac{45}{8}, \frac{5}{2}, \frac{5}{8}, 0)$ |
| L9 | return $S$ |

Two values in detail. In line L1, the second sample of $G^M_1$ is centered on pixel 2 and reads pixels 0 to 4, so it is $(1 + 4 + 6 + 4 + 0)/16 = 15/16$. In line L8, the zero-inserted row is $(16, 0, 15, 0, 5, 0, 0, 0)$; at $x = 0$ the taps read pixels $2, 1, 0, 1, 2$ after the border, with values $15, 0, 16, 0, 15$, so the first output is $2 \cdot (15 + 6 \cdot 16 + 15)/16 = 63/4$.

With $N = 0$ the result is the hard cut $(16, 16, 16, 16, 0, 0, 0, 0)$. With $N = 1$ the step of 16 is spread over about 7 pixels. With $N = 3$ the top level is one pixel wide, and the result is the constant $337/32$ at every pixel: the whole image is a single band, mixed with the single weight $337/512$. Too many levels for the size of the overlap remove the seam and also the difference between the two sides.

## Correctness

The specification is the formula in the problem statement. Lines L1 to L5 compute the mixed bands $L^S_l$ by definition, and lines L6 to L8 are the reconstruction of a Laplacian pyramid applied to them, so $S = \sum_{l=0}^{N} \mathrm{EXPAND}^{(l)}(L^S_l)$, where $\mathrm{EXPAND}^{(l)}$ expands from level $l$ to level 0 step by step. Because REDUCE and EXPAND are linear and collapse inverts the Laplacian pyramid exactly, the result has the properties a blend should have. If $M = 1$ everywhere, $S = A$; if $M = 0$, $S = B$; if $A = B$, $S = A$ for every mask. If $M$ is a constant $c$, then $S = cA + (1 - c)B$, since REDUCE keeps constants. With $N = 0$ the algorithm is the plain blend $M \odot A + (1 - M) \odot B$. Each level of $G^M$ lies in $[0, 1]$, because REDUCE takes weighted means with non-negative weights, so each band is a convex mix of the two input bands. The full proof is below.

## Complexity

Level $l$ has $\lceil W / 2^l \rceil \cdot \lceil H / 2^l \rceil \le (W / 2^l + 1)(H / 2^l + 1)$ samples, and each sample of REDUCE or EXPAND reads 5 values per axis. Summed over the levels, each pyramid has at most $\frac{4}{3} W H + 2(W + H) + N + 1$ samples, so the time and the extra space are $\Theta(W H + N)$ in the [real RAM](/real-ram/) model. The term $N$ counts levels that are already $1 \times 1$; in practice $N \le \log_2 \max(W, H)$, and the cost is $\Theta(W H)$. With integer or rational pixels every step is exact. In floating point the result has the small rounding errors of a few dozen additions and products per pixel.

## Properties

- **Exact on trivial masks.** $M = 1$ gives $A$, $M = 0$ gives $B$, and $A = B$ gives $A$, for any $N$.
- **Linear in the images.** For a fixed mask, $S$ is a linear function of $(A, B)$. It is not linear in $M$ jointly with the images.
- **Not a convex mix of pixels.** The bands are mixed with weights in $[0, 1]$, but the collapsed result can leave the range of the inputs. For $A = (0, 0, 0, 0, 16, 16, 16, 16)$, $B = 16$ everywhere, $M = (1, 1, 1, 1, 1, 1, 0, 0)$ and $N = 1$, the fifth pixel is $1039/64 \approx 16.23 > 16$. Clamp the result to the valid range.
- **Local.** A change of $A$, $B$ or $M$ at one pixel changes $S$ only within about $2^{N+2}$ pixels of it, since each level has a filter of 5 taps.
- **Deterministic and not iterative.** It builds three pyramids and collapses one, with no system to solve.

## Variants and improvements

- **Many images.** Give each image $I_k$ a weight map $M_k$, with $\sum_k M_k = 1$ at each pixel. Then the mixed band is $\sum_k G^{M_k}_l \odot L^{I_k}_l$. Because REDUCE is linear and keeps constants, the levels $G^{M_k}_l$ also sum to 1. If the maps do not sum to 1, divide each mixed band by $\sum_k G^{M_k}_l$.
- **Brown and Lowe.** For a panorama, each pixel of the output is given to the image whose weight, largest at its center, is the highest there. The resulting max-weight maps are the masks. Brown and Lowe form the bands with Gaussian blurs instead of a decimated pyramid: the first band is $I - I * g_\sigma$, and the next bands use blurs of width $\sigma' = \sqrt{2k + 1}\,\sigma$. Their Figure 7 uses 5 bands and $\sigma = 5$ pixels.
- **Feathering.** Mix all frequencies with one smooth weight map, for example from a [distance transform](/distance-transform/) of each image's border. It is one pass, but it gives ghosts when the images are not perfectly aligned.
- **Gradient domain blending.** [Poisson image editing](/poisson-image-editing/) keeps the gradients of each image and solves for pixel values. It removes exposure differences that a pyramid spreads only over its widest zone, at the cost of solving a large sparse system.
- **Seams first.** Choose the seam where the images agree, for example by a minimum cut, and then blend along it with a few levels.

## When to use it

Use it to hide the seams of a panorama or a photo montage after the images are aligned and their exposures are roughly matched. It is fast, simple and robust to small alignment errors, since fine detail switches quickly between the images. It does not fix a large exposure difference, parallax or a moving object; for those, compensate the gains first, place the seam with care, or use a gradient domain method.

## Pitfalls

- **Too many levels.** If the top level is smaller than the overlap, the lowest band mixes content from far away, and the mean brightness of one image leaks across the whole result. Stop the pyramid when the top level is about as large as the overlap.
- **Seam outside the overlap.** At level 0 the mask is used as it is, and the coarser levels spread it over a wide zone around the seam. Put the seam well inside the overlap, so that this zone has valid pixels of both images.
- **Invalid pixels in the pyramid.** Black borders of a warped image enter the coarse levels of its pyramid. Fill them first, for example by extending the image, or use weights normalized by the blurred valid mask.
- **Overshoot.** The result can leave the valid range; clamp it.
- **Different sizes.** $A$, $B$ and $M$ must have the same size, and REDUCE and EXPAND must use the same rounding of sizes at every level, or the bands do not line up.

## Implementations

## History

Burt and Adelson (1983) introduced the Laplacian pyramid as an image code and, in the same year, the multiresolution spline for joining images into mosaics: each band is joined over a transition zone that matches its scale. Their paper extended the method from a straight seam to regions of any shape through the Gaussian pyramid of a mask. Brown and Lowe (2007) used multi-band blending as the last step of their automatic panorama stitcher, with one weight map per image.

## References
