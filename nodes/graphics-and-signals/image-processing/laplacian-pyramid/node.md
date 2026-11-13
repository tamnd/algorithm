---
tag: KYWMGX
kind: data-structure
slug: laplacian-pyramid
name: Laplacian pyramid
area: graphics-and-signals/image-processing
level: advanced
summary: The bands L_l = G_l - EXPAND(G_(l+1)) of a Gaussian pyramid, with the coarsest level on top. Adding the bands back from the top rebuilds the image exactly, for any kernel.
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels}
  time: {build: Θ(W H), reconstruct: Θ(W H), band: O(1)}
  space: {total: Θ(W H)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1983
  people: [Peter J. Burt, Edward H. Adelson]
  note: Burt and Adelson defined the Laplacian pyramid as a sequence of prediction error images for image coding, and in the same year used it to blend images band by band.
prereqs: [gaussian-pyramid, image-pyramid]
see_also: [discrete-wavelet-transform, perfect-reconstruction, filter-bank, laplacian-of-gaussian, image-compositing, mipmap, polyphase-decomposition, transform-coding]
sources:
  - paper: doi:10.1109/TCOM.1983.1095851
    title: Peter J. Burt and Edward H. Adelson, The Laplacian pyramid as a compact image code, IEEE Transactions on Communications 31(4), 1983, 532 to 540
    locator: page 534 (EXPAND and its factor 4), page 535 (the definition L_l = g_l - EXPAND(g_l+1), L_N = g_N, the band-pass view and the exact decoding), and pages 536 to 539 (quantization and entropy coding of the levels)
  - paper: doi:10.1145/245.247
    title: Peter J. Burt and Edward H. Adelson, A multiresolution spline with application to image mosaics, ACM Transactions on Graphics 2(4), 1983, 217 to 236
    locator: the whole paper (the blend of two images by mixing their Laplacian levels with a Gaussian pyramid of the mask)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 3, Section 3.5, Pyramids and wavelets (the Laplacian pyramid and pyramid blending)
---

A Laplacian pyramid stores an image as a stack of band-pass images $L_0, \ldots, L_{N-1}$ and one low-pass image $L_N$ on top. Each band is the difference $L_l = G_l - \mathrm{EXPAND}(G_{l+1})$ between a level of the [Gaussian pyramid](/gaussian-pyramid/) and the next coarser level, upsampled and interpolated back to the finer size; the top is $L_N = G_N$. The image comes back exactly from $g_N = L_N$ and $g_l = L_l + \mathrm{EXPAND}(g_{l+1})$, whatever the kernel. Burt and Adelson built it as an image code, since most band values are near zero, and it is the standard tool for blending images without seams.

## In plain words

Make the stack of smaller and smaller blurred copies of a picture. Now take the second copy, blow it up to the size of the first, and subtract it from the first. What is left is only the fine detail, the part that the smaller copy could not hold: edges, texture and noise. Do the same for every pair of neighbors in the stack, and keep the smallest copy as it is. You now have a stack of detail layers, from fine to coarse, plus one tiny picture. To get the picture back, blow up the tiny picture, add the coarsest detail layer, blow up again, add the next layer, and so on. Each addition undoes one subtraction, so the result is the original picture, with no loss. In a smooth region most detail values are close to zero, which makes the layers easy to compress.

## The abstract type

The structure holds the arrays $L_0, \ldots, L_N$, where $L_l$ has the size $W_l \times H_l$ of level $l$ of the Gaussian pyramid of the image, and a kernel $\hat w$. The operations are:

- **Build** $(I, \hat w)$: make the Gaussian levels $G_0, \ldots, G_N$ of $I$ and the bands.
- **Band** $(l)$: return $L_l$.
- **Reconstruct**: return the image from the bands.
- **Combine**: apply an operation to each band, for example a weighted sum of the bands of two images, and then reconstruct.

The invariant is $L_l = G_l - \mathrm{EXPAND}(G_{l+1})$ for $l < N$ and $L_N = G_N$. EXPAND maps an array of size $\lceil W_l / 2 \rceil \times \lceil H_l / 2 \rceil$ to one of size $W_l \times H_l$. Burt and Adelson define it as

$$
\mathrm{EXPAND}(g)(x, y) = 4 \sum_{m=-2}^{2} \sum_{n=-2}^{2} \hat w(m)\, \hat w(n)\, g\Big(\frac{x - m}{2}, \frac{y - n}{2}\Big),
$$

where only the terms with integer coordinates are kept. Equivalently, place the coarse samples on the even positions of a zero grid of the fine size and filter it with $2 \hat w$ along each axis. The factor 4 makes up for the three zero samples in each $2 \times 2$ block.

**Model.** One channel of real values, pixel centers at $(x + 1/2, y + 1/2)$, the coarse sample $(i, j)$ on the fine sample $(2i, 2j)$, sizes that round up, and the reflect-101 border, as on the [Gaussian pyramid](/gaussian-pyramid/) page. EXPAND uses the same border on the fine grid. An axis of length 1 has no zeros to fill, so EXPAND leaves it as it is. The bands hold signed values even when the image does not.

## Representation

The bands have the same sizes as the Gaussian levels, so they can share the packed layout and offset table of the Gaussian pyramid: one buffer of $S = \sum_l W_l H_l$ signed samples. The Gaussian levels are not kept after the build; the bands and the kernel determine them. With 8-bit input and a dyadic kernel such as $\frac{1}{16}(1, 4, 6, 4, 1)$, a band fits a signed fixed-point type with a few fraction bits per level, or a float type.

## Operations

```pseudo id=main
EXPAND(g, W, H, ŵ)                          ▷ g has ⌈W/2⌉ × ⌈H/2⌉ samples
L1  z ← a W × H array of zeros;  z[2j][2i] ← g[j][i] for each sample of g
L2  r[y][x] ← Σ_{m = −2..2} 2ŵ(m) · z[y][ρ_W(x − m)]   for each y < H, x < W
L3  e[y][x] ← Σ_{n = −2..2} 2ŵ(n) · r[ρ_H(y − n)][x]   for each y < H, x < W
L4  return e

BUILD(I, ŵ)
L5  G_0, …, G_N ← the Gaussian pyramid of I with kernel ŵ
L6  for l ← 0 to N − 1 do L_l ← G_l − EXPAND(G_{l+1}, W_l, H_l, ŵ)
L7  L_N ← G_N
L8  return L_0, …, L_N

RECONSTRUCT(L_0, …, L_N, ŵ)
L9  g ← L_N
L10 for l ← N − 1 down to 0 do g ← L_l + EXPAND(g, W_l, H_l, ŵ)
L11 return g
```

Line L1 is the zero insertion. Lines L2 and L3 filter along the rows and then the columns with $2\hat w$, so the two factors of 2 give the 4 of the definition. A faster EXPAND skips the zeros: each output reads only the 2 or 3 taps that land on coarse samples, which is the [polyphase](/polyphase-decomposition/) form of the same filter.

**Combine** is the reason for the structure. The multiresolution spline of Burt and Adelson blends images $A$ and $B$ with a mask $M$ (1 where $A$ is wanted, 0 where $B$ is wanted): build the bands $L^A$, $L^B$ and the Gaussian pyramid $G^M$ of the mask, set $L_l = G^M_l L^A_l + (1 - G^M_l) L^B_l$ sample by sample, and reconstruct. The coarse bands get a wide, soft transition and the fine bands a sharp one, so the seam does not show. This is a multiscale form of [image compositing](/image-compositing/).

## Example

Take the $5 \times 5$ image with every row $0, 0, 16, 16, 16$ and the binomial kernel $\frac{1}{16}(1, 4, 6, 4, 1)$. Its Gaussian levels have the rows $G_1 = (2, 11, 16)$, $G_2 = (33/4, 47/4)$ and $G_3 = (10)$ (see the [Gaussian pyramid](/gaussian-pyramid/) example). Every row of every array below is the same, so one row each is shown.

| step | row |
|---|---|
| $\mathrm{EXPAND}(G_1)$, size 5 | $17/4, 13/2, 21/2, 27/2, 59/4$ |
| $L_0 = G_0 - \mathrm{EXPAND}(G_1)$ | $-17/4, -13/2, 11/2, 5/2, 5/4$ |
| $\mathrm{EXPAND}(G_2)$, size 3 | $73/8, 10, 87/8$ |
| $L_1 = G_1 - \mathrm{EXPAND}(G_2)$ | $-57/8, 1, 41/8$ |
| $\mathrm{EXPAND}(G_3)$, size 2 | $10, 10$ |
| $L_2 = G_2 - \mathrm{EXPAND}(G_3)$ | $-7/4, 7/4$ |
| $L_3 = G_3$ | $10$ |

Take the first value of $\mathrm{EXPAND}(G_1)$. The zero-inserted row is $2, 0, 11, 0, 16$. At $x = 0$ the taps $x - m$ are $2, 1, 0, -1, -2$, which the border maps to $2, 1, 0, 1, 2$, with values $11, 0, 2, 0, 11$. So the value is $2 \cdot (1 \cdot 11 + 6 \cdot 2 + 1 \cdot 11)/16 = 68/16 = 17/4$. The band $L_0$ is negative on the dark side of the edge and positive on the bright side, the typical signed response of a band-pass filter to a step.

Reconstruction runs the table upward. $g_3 = 10$; $g_2 = (-7/4, 7/4) + (10, 10) = (33/4, 47/4)$; $g_1 = (-57/8, 1, 41/8) + (73/8, 10, 87/8) = (2, 11, 16)$; and $g_0 = L_0 + \mathrm{EXPAND}(g_1) = (0, 0, 16, 16, 16)$, the image.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The main claim is exact reconstruction: by downward induction, the value $g$ after the pass of line L10 for level $l$ equals $G_l$, since $L_l + \mathrm{EXPAND}(G_{l+1}) = G_l - \mathrm{EXPAND}(G_{l+1}) + \mathrm{EXPAND}(G_{l+1})$. The proof uses only that BUILD and RECONSTRUCT call the same deterministic EXPAND on the same arrays. So it holds for every kernel, including ones that are not Gaussian or not of equal contribution, and for an EXPAND that rounds to integers, as long as the arithmetic of the subtraction and the addition is exact.

The proof also shows when the bands are true band-pass images, with zero response to a constant. EXPAND maps a constant $c$ to $c$ exactly when each parity class of the kernel sums to $1/2$, $\hat w(-2) + \hat w(0) + \hat w(2) = \hat w(-1) + \hat w(1) = 1/2$, which for a normalized kernel is the equal contribution rule. The kernel $\frac{1}{9}(1, 2, 3, 2, 1)$ fails it: EXPAND of the constant 9 gives $100/9$, $80/9$ and $64/9$ in a checkerboard, so the bands of a flat image are not zero. The reconstruction is still exact.

## Complexity

- **Space.** The bands have exactly the sizes of the Gaussian levels, so the pyramid holds $S = \sum_l W_l H_l$ samples, which is $(4WH - 1)/3$ for $W = H = 2^N$ and $\frac{4}{3}WH + O(W + H + \log \max(W, H))$ in general (the count is on the [Gaussian pyramid](/gaussian-pyramid/) page). It is overcomplete: about $WH/3$ more numbers than the image, against none for a [discrete wavelet transform](/discrete-wavelet-transform/).
- **Build.** The Gaussian levels cost $\Theta(WH)$. EXPAND to $W_l \times H_l$ costs $10 W_l H_l$ multiply-adds as written, or about $2.5$ per pass and pixel in the polyphase form. Summed over the levels this is $\Theta(S) = \Theta(WH)$ in the [real RAM](/real-ram/).
- **Reconstruct.** One EXPAND and one addition per level, so $\Theta(WH)$.
- **Band access.** $O(1)$ through the offset table.

## Variants

- **Coding.** Burt and Adelson quantize each band and code the result by its entropy. The decoder adds the bands back as usual, and a quantization error $q_l$ in band $l$ reaches the output as $l$ applications of EXPAND to $q_l$, so the errors of the bands add up and do not stay in their band.
- **Blending.** The multiresolution spline above, the classic use in image mosaics and panoramas.
- **Difference of Gaussians.** Burt and Adelson describe each band as the difference of the image filtered with two equivalent weighting functions, which is similar to a filter with a scaled Laplacian weighting function (see [Laplacian of Gaussian](/laplacian-of-gaussian/)). This gives the name. Burt and Adelson note that the center frequency of the passband drops by an octave from level to level. Scale-space detectors such as [SIFT](/sift/) use differences of Gaussians without the upsampling step.
- **Critically sampled transforms.** A [discrete wavelet transform](/discrete-wavelet-transform/) splits each level into one coarse and three detail subbands of a quarter size each, with a [filter bank](/filter-bank/) that has [perfect reconstruction](/perfect-reconstruction/), so it stores exactly $WH$ numbers. The Laplacian pyramid needs no conditions on the filters for exactness, at the cost of the extra third.
- **Oriented pyramids.** Later designs split each band further into orientations, for texture analysis and denoising.

## When to use it

Use a Laplacian pyramid to blend or mosaic images, to edit or enhance the detail of an image band by band, to denoise by shrinking the fine bands, and as a simple multiscale code. Use a [Gaussian pyramid](/gaussian-pyramid/) alone when only the coarse copies are needed, as in coarse-to-fine search. Use a [discrete wavelet transform](/discrete-wavelet-transform/) or a [transform code](/transform-coding/) when the number of coefficients must equal the number of pixels.

## Pitfalls

- **EXPAND without the factor 4.** A blur of the zero-inserted grid with $\hat w$ instead of $2\hat w$ per axis gives a level a quarter as bright, and the bands then hold most of the image.
- **Two different EXPANDs.** The build and the reconstruction must use the same EXPAND, the same border and the same output size. With a different one, the reconstruction is wrong by the difference of the two at each level.
- **Odd sizes.** EXPAND must produce exactly $W_l \times H_l$ samples. Doubling $\lceil W_l / 2 \rceil$ gives $W_l + 1$ when $W_l$ is odd; crop or, better, pass the target size, as in line L6.
- **Floating point.** Exact reconstruction needs exact arithmetic. In binary floating point, $(0.1 - 0.7) + 0.7$ is $0.09999999999999998$, so the rebuilt image can differ in the last bits. Use integers, a fixed-point type, or rounding at the end when bit-exact output matters.
- **Integer bands.** If the bands are stored as integers, the EXPAND inside BUILD must round in the same way as the one inside RECONSTRUCT, or the identity of line L10 fails.
- **Edits that break the invariant.** After the bands are changed, for example by blending or by quantization, the result is the reconstruction of the new bands, not a Laplacian pyramid of any image. Building the pyramid of that result again does not in general return the edited bands.

## Implementations

## History

Burt and Adelson introduced the Laplacian pyramid in 1983 in IEEE Transactions on Communications, as a compact image code. They saw the reduced image $g_1$ as a prediction of $g_0$, coded the prediction error, and repeated the step on $g_1$. They defined REDUCE, EXPAND and the bands, showed that decoding by repeated expansion and addition is exact, and quantized the bands for compression. In the same year, in ACM Transactions on Graphics, they used the structure to join images into mosaics with the multiresolution spline.

## References
