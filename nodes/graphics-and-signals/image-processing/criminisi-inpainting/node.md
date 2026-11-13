---
tag: 9PPPZC
kind: algorithm
slug: criminisi-inpainting
name: Criminisi exemplar-based inpainting
aliases:
- exemplar-based inpainting
area: graphics-and-signals/image-processing
level: advanced
summary: Copy patches from known regions, prioritized by structure along the fill front.
solves: [image-inpainting]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, m: the number of pixels to fill, a: the patch area (2r+1)^2}
  time: {worst: O(m W H a), average: O(m W H a), best: Θ(W H a)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, greedy: true, heuristic: true, keeps_known_pixels: true}
history:
  year: 2004
  people: [Antonio Criminisi, Patrick Pérez, Kentaro Toyama]
  note: Criminisi, Pérez and Toyama presented the method at CVPR 2003 and gave the full version in IEEE Transactions on Image Processing in 2004.
prereqs: [digital-image, template-matching, greedy-algorithm]
see_also: [image-inpainting, best-first-search, non-local-means, poisson-image-editing, seam-carving, fast-marching-method, nearest-neighbor-search, image-noise]
sources:
  - paper: doi:10.1109/TIP.2004.833105
    title: Antonio Criminisi, Patrick Pérez and Kentaro Toyama, Region filling and object removal by exemplar-based image inpainting, IEEE Transactions on Image Processing 13(9):1200-1212, 2004
    locator: Section III, Our region-filling algorithm (priority equation (1), exemplar equation (2), the confidence update and Table I)
  - paper: doi:10.1109/CVPR.2003.1211538
    title: Antonio Criminisi, Patrick Pérez and Kentaro Toyama, Object removal by exemplar-based inpainting, IEEE Conference on Computer Vision and Pattern Recognition, 2003
    locator: the conference version of the method
  - paper: doi:10.1109/ICCV.1999.790383
    title: Alexei A. Efros and Thomas K. Leung, Texture synthesis by non-parametric sampling, IEEE International Conference on Computer Vision, 1999, pages 1033-1038
    locator: the pixel-by-pixel synthesis from similar neighborhoods that exemplar-based filling builds on
  - paper: doi:10.1145/1531326.1531330
    title: Connelly Barnes, Eli Shechtman, Adam Finkelstein and Dan B Goldman, PatchMatch, a randomized correspondence algorithm for structural image editing, ACM Transactions on Graphics 28(3), article 24, 2009
    locator: the randomized approximate nearest-neighbor search for patches, and its use for image completion
---

Criminisi exemplar-based inpainting fills a hole $\Omega$ in an image by copying square patches from the known part of the same image. It works on the fill front, the border between filled and unfilled pixels. At each step it gives every front pixel $p$ a priority $P(p) = C(p)\,D(p)$. The confidence term $C(p)$ is the share of reliable pixels around $p$. The data term $D(p)$ is large where a strong edge of the known image meets the front. The method takes the front pixel of largest priority, finds the source patch that is nearest to the known part of its patch in sum of squared differences, and copies that source patch into the unfilled pixels. Then it updates the front and repeats. The order makes edges grow into the hole before flat texture, so lines continue across the hole. The method is a greedy heuristic for [image inpainting](/image-inpainting/): each step is exact for its own rule, but no global quality is optimized or guaranteed.

## In plain words

A part of a photo is gone, for example where a person was removed. The method fills it from the outside in, one small square at a time, using squares taken from the rest of the same photo. For each spot on the edge of the hole, it looks at the square around that spot and asks two things. How much of this square is already known and trusted? Does a strong line, such as the edge of a roof, run into the hole here? Spots with a high score are filled first, so lines grow into the hole before plain areas do. To fill a spot, the method looks through the photo for the square that best matches the known part of the square at that spot, and copies the missing pixels from it. Copied pixels are trusted a little less than the original ones.

## The problem

The input is a gray [digital image](/digital-image/) $I$ of $W \times H$ pixels, with pixel centers at integer coordinates $(x, y)$, and a target region $\Omega$ of pixels whose values are unknown. The source region $\Phi$ is the rest of the image. The patch $\Psi_p$ of radius $r$ at $p$ is the square of side $2r + 1$ centered at $p$, cut at the image border; its area is $|\Psi_p| \le a = (2r+1)^2$. A source patch is a full square $\Psi_q$ that lies inside the image and contains no pixel of $\Omega$. The output is an image equal to $I$ on $\Phi$, with a value at each pixel of $\Omega$. The method needs at least one source patch. A color image uses the same steps with a vector of channels at each pixel; the paper measures the distance in the CIE Lab color space.

## The algorithm

Every pixel carries a filled flag and a confidence $C$. A front pixel is an unfilled pixel with a filled 4-neighbor. For a front pixel $p$,

$$C(p) = \frac{1}{|\Psi_p|} \sum_{q \in \Psi_p,\ q \text{ filled}} C(q), \qquad D(p) = \frac{|\nabla I_p^{\perp} \cdot n_p|}{\alpha}, \qquad P(p) = C(p)\,D(p),$$

where $n_p$ is the unit normal to the front at $p$, $\nabla I_p^{\perp}$ is the image gradient near $p$ turned by 90 degrees (the isophote, the direction along which the image does not change), and $\alpha$ is a scale, 255 for 8-bit gray values. The distance between the patch at $\hat p$ and a source patch at $q$ is

$$d(\hat p, q) = \sum_{u \in \Psi_{\hat p} - \hat p,\ \hat p + u \text{ filled}} \big(I(\hat p + u) - I(q + u)\big)^2 .$$

```pseudo id=main
CRIMINISI-INPAINT(I, Ω, r, α)
L1  mark every pixel of Φ filled and every pixel of Ω unfilled
L2  C(p) ← 1 for p in Φ, C(p) ← 0 for p in Ω
L3  S ← the centers of the source patches
L4  repeat: δΩ ← the unfilled pixels with a filled 4-neighbor
L5      if δΩ is empty then stop
L6      for each p in δΩ compute C(p), D(p) and P(p) = C(p) D(p)
L7      p̂ ← the p in δΩ with the largest P(p)
L8      q̂ ← the q in S with the least d(p̂, q)
L9      for each offset u with p̂ + u in the image and unfilled do
L10         I(p̂ + u) ← I(q̂ + u);  mark p̂ + u filled
L11         C(p̂ + u) ← C(p̂)
L12 return I
```

Line L6 computes the confidence over the current filled pixels of the patch, so it changes as the hole shrinks. Line L11 freezes the confidence of a copied pixel at the confidence of the patch it came with. Lines L4 to L11 are steps 1, 2 and 3 of Table I of the paper.

The paper leaves some details to the implementation, and the code on this page fixes them as follows. The gradient at $p$ is the central-difference gradient of largest size among the filled pixels of $\Psi_p$, where a difference uses only filled pixels and is one-sided when one neighbor is unfilled. The normal $n_p$ is the normalized central-difference gradient of the indicator of the unfilled set, with values outside the image taken equal to the value at $p$; the paper instead smooths a list of contour points and takes the normal to the line through the neighbors of $p$ on that list. A tie in priority goes to the larger confidence, then to the first pixel in raster order; a tie in distance goes to the first source center in raster order.

## Example

Take a $9 \times 8$ image with value 40 everywhere except a bright vertical line of value 200 in column $x = 4$. The hole $\Omega$ is the $3 \times 3$ block with $3 \le x \le 5$ and $2 \le y \le 4$, shown as `?`. The patch radius is $r = 1$, and $\alpha = 255$.

```text
y=0:  40  40  40  40 200  40  40  40  40
y=1:  40  40  40  40 200  40  40  40  40
y=2:  40  40  40   ?   ?   ?  40  40  40
y=3:  40  40  40   ?   ?   ?  40  40  40
y=4:  40  40  40   ?   ?   ?  40  40  40
y=5:  40  40  40  40 200  40  40  40  40
y=6:  40  40  40  40 200  40  40  40  40
y=7:  40  40  40  40 200  40  40  40  40
```

The front at the start is the 8 pixels of the hole other than its center $(4, 3)$. At the corner $(3, 2)$, 5 of the 9 patch pixels are known, so $C = 5/9$. The largest known gradient in the patch is at $(3, 1)$, where the central difference across the line is $(200 - 40)/2 = 80$ in $x$, so the isophote is vertical with size 80. The normal at the corner is diagonal, so $D = (80/\sqrt 2)/255$. At the top middle pixel $(4, 2)$, where the line meets the hole, the normal is vertical and $D = 80/255$ is larger, but only 3 patch pixels are known. The side pixels $(3, 3)$ and $(5, 3)$ have a horizontal normal, which is at right angles to the isophote, so $D = 0$.

| front pixel | $C$ | $D$ | $P$ |
|---|---|---|---|
| $(3, 2)$, $(5, 2)$, $(3, 4)$, $(5, 4)$ | 0.55556 | 0.22184 | 0.12324 |
| $(4, 2)$, $(4, 4)$ | 0.33333 | 0.31373 | 0.10458 |
| $(3, 3)$, $(5, 3)$ | 0.33333 | 0 | 0 |

The four corners tie, and the raster rule picks $(3, 2)$. The known pixels of its patch are 40, 40, 200 in row 1 and 40, 40 in column 2, and the source patch at $(3, 6)$ matches them with distance 0. Copying fills $(3, 2)$, $(4, 2)$, $(3, 3)$ and $(4, 3)$ with 40, 200, 40, 200, so the line has grown two rows into the hole. Three more steps follow: $\hat p = (5, 2)$ with $P = 0.42605$, then $(5, 4)$ and $(3, 4)$, where every remaining front pixel has $D = 0$ and the larger confidence decides. All four exemplars have distance 0, and the output is the image without the hole, with the line unbroken.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Each pass of the loop fills $\hat p$ itself, because $\hat p$ is unfilled and the offset $u = 0$ is in its patch, so the loop stops after at most $|\Omega|$ passes. While an unfilled pixel remains, the front is not empty: there is a filled pixel, and a path in the pixel grid from it to an unfilled pixel crosses from filled to unfilled somewhere. Lines L9 and L10 write only to unfilled pixels, and a filled pixel never becomes unfilled, so the pixels of $\Phi$ keep their values. Every copied value is read from a source patch, which contains no pixel of $\Omega$, so every output value in $\Omega$ is a value of $\Phi$. Lines L7 and L8 take an exact maximum and an exact minimum, so the fill order is best first for the priority of line L6. All confidences stay in $[0, 1]$, and a copied pixel gets a confidence of at most $(a - 1)/a$, because its patch center was unfilled.

These facts are about the procedure. The result has no quality guarantee: the method does not minimize any total cost over the hole, and a different order or exemplar can give a better fill. The proof file shows one case where the output is exact: a pattern of vertical stripes with $k$ distinct column values is rebuilt without error when $r \ge 1$ and the source patches cover every column phase.

## Complexity

Let $m = |\Omega|$, $F$ the size of the front and $S \le WH$ the number of source patches. Line L3 checks $a$ pixels for each of the $WH$ centers, so it takes $\Theta(WHa)$ time. In one pass, line L4 scans the image in $\Theta(WH)$, line L6 looks at $O(a)$ pixels for each front pixel, and line L8 looks at $O(a)$ pixels for each source patch, so a pass takes $O(WH + (F + S)a) = O(WHa)$. There are at most $m$ passes, and at least $m/a$, because a pass fills at most $a$ pixels. The total is $O(mWHa)$, and the search of line L8 is the main cost. The extra space is $\Theta(WH)$ for the flags, the confidences and the list of sources.

## Properties

- Deterministic, given the tie rules.
- Greedy: a filled pixel is never changed again, even if a later patch fits better.
- Pixels outside the hole never change, and each filled value is a copy of a source pixel, so the method adds no new values and no blur.
- The confidence decays toward the inside of the hole, so the inner pixels are filled last.
- The data term is zero where the front runs along an edge, and also everywhere in a flat area, so in flat areas the order falls back on the confidence and the tie rule.
- The result depends on the patch radius, the tie rules, and the way the normal and the gradient are estimated.

## Variants and improvements

- The paper allows the source region to be the whole known image, a band around the hole, or a region that the user marks. A smaller source region makes line L8 faster.
- Color: a vector of channels per pixel, with the distance in CIE Lab, as in the paper.
- Faster search: an approximate nearest-neighbor search over patches replaces the scan of line L8. PatchMatch of Barnes, Shechtman, Finkelstein and Goldman finds good matches by random search and by passing matches to neighbors, and it is used for image completion.
- Other priorities: implementations change the product $C \cdot D$, for example by adding a small constant to $D$ or by using a sum or a weighted sum, because the product is zero in flat areas and the confidence can fall fast.
- Global methods: instead of a single greedy pass, later patch-based methods improve the whole fill in rounds, so that each filled pixel agrees with the patches that cover it.
- Diffusion-based inpainting, which follows partial differential equations such as the [heat equation](/heat-equation/), continues smooth areas and thin lines but blurs large holes and texture; the [image inpainting](/image-inpainting/) page compares the two kinds.

## When to use it

Use it to remove an object or a scratch of medium size from a photo whose background is texture or simple structure, such as grass, water, a wall or a fence, and where the same texture appears in other parts of the image. It is simple, has few parameters, and copies real texture instead of smoothing it. Do not use it for a thin scratch on a smooth image, where diffusion or a [Poisson](/poisson-image-editing/) fill is faster and smoother. Do not use it where the hole hides content that appears nowhere else in the image, such as half of a face; the method can only copy what the image already has.

## Pitfalls

- The patch radius must be a little larger than the largest repeated texture element, as the paper says; a small patch breaks texture, and a large patch copies too much.
- A source patch must lie fully in the known region. If the hole is large compared with the image, few or no source patches remain.
- Errors spread: a wrong copy becomes known data for the next steps. On a $16 \times 12$ image with value 180 where $x + y < 14$ and 60 elsewhere, a hole of $6 \times 5$ pixels at $5 \le x \le 10$, $4 \le y \le 8$, and $r = 2$, the code fills the hole in 4 steps, and 6 of the 30 filled pixels differ from the original image; the diagonal edge comes out as a vertical step in the lower rows.
- The normal from a raster mask is coarse, with only a few possible directions; the paper smooths the contour first.
- With noisy images the largest gradient in a patch comes from noise, and the data term loses its meaning; smooth the image for the gradient only.
- The brute-force search makes large images slow, because each step scans all source patches.

## Implementations

## History

Exemplar-based texture synthesis, which copies pixels or patches from a sample instead of fitting a model, goes back to Efros and Leung in 1999, who grew a texture one pixel at a time from similar neighborhoods in the sample. Inpainting by diffusion, from Bertalmio, Sapiro, Caselles and Ballester in 2000, continued edges into a hole but blurred texture. Antonio Criminisi, Patrick Pérez and Kentaro Toyama, at Microsoft Research, joined the two ideas: copy whole patches as in texture synthesis, but choose the order so that edges continue as in inpainting. They presented the method at CVPR 2003 and in IEEE Transactions on Image Processing in 2004. Later work made the patch search fast, for example PatchMatch in 2009, and moved from greedy filling to methods that improve the whole fill in rounds.

## References
