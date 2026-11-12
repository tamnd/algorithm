---
tag: APJT1C
kind: algorithm
slug: jpeg-2000
name: JPEG 2000
aliases:
- JPEG2000
- ISO/IEC 15444-1
- ITU-T T.800
area: compression-and-coding/transforms-for-compression
level: advanced
summary: "Wavelet image coder: 5/3 or 9/7 lifting DWT, dead-zone quantization, EBCOT bit-plane coding with the MQ coder, and optimal truncation. Lossless and lossy in one stream."
solves: [lossy-image-compression]
model: real-ram
complexity:
  vars: {n: the number of samples, p: the number of bit planes of the coefficients}
  time: {worst: Θ(n p), average: Θ(n p)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false, comparison: false}
history:
  year: 2000
  people: [Joint Photographic Experts Group (ISO/IEC JTC 1/SC 29/WG 1 and ITU-T)]
  note: Part 1, the core coding system, was published as ISO/IEC 15444-1 in December 2000 and approved by ITU-T as Recommendation T.800 in August 2002. Its block coder is Taubman's EBCOT.
prereqs: [discrete-wavelet-transform, lifting-scheme, bit-plane-coding, arithmetic-coding]
see_also: [jpeg-compression, lossy-image-compression, subband-coding, spiht, scalar-quantization, context-modeling, color-spaces, psnr]
sources:
  - url: https://www.itu.int/rec/T-REC-T.800/
    title: ITU-T Recommendation T.800, Information technology, JPEG 2000 image coding system, Core coding system (ISO/IEC 15444-1)
    locator: "Annex A (codestream syntax), Annex B (tiles, precincts, code blocks, packets and progression orders), Annex C (the MQ arithmetic coder), Annex D (coefficient bit modelling: the three coding passes and their contexts), Annex E (quantization), Annex F (the 5/3 and 9/7 transforms by lifting, with the 9/7 parameters in Table F.4), Annex G (DC level shift, RCT and ICT)"
  - url: https://www.iso.org/standard/27687.html
    title: ISO/IEC 15444-1:2000, JPEG 2000 image coding system, Part 1, Core coding system
    locator: the catalogue entry (first edition, published in December 2000, now withdrawn)
  - paper: doi:10.1109/83.847830
    title: David Taubman, High performance scalable image compression with EBCOT, IEEE Transactions on Image Processing 9(7), 2000
    locator: pages 1158 to 1170 (code blocks, fractional bit-plane coding passes, contexts, post-compression rate-distortion optimization, and quality layers)
  - book: isbn:9780792375197
    title: David S. Taubman and Michael W. Marcellin, JPEG2000, Image Compression Fundamentals, Standards and Practice, Kluwer, 2002
    locator: the chapters on the history of the standard, the wavelet transforms, quantization, the EBCOT block coder, the MQ coder and the codestream
  - paper: doi:10.1109/78.258085
    title: Jerome M. Shapiro, Embedded image coding using zerotrees of wavelet coefficients, IEEE Transactions on Signal Processing 41(12), 1993
    locator: pages 3445 to 3462 (the embedded zerotree wavelet coder)
  - paper: doi:10.1109/76.499834
    title: Amir Said and William A. Pearlman, A new, fast, and efficient image codec based on set partitioning in hierarchical trees, IEEE Transactions on Circuits and Systems for Video Technology 6(3), 1996
    locator: pages 243 to 250 (the SPIHT coder and its comparison with earlier coders)
  - paper: doi:10.1109/ICASSP.1988.196696
    title: Didier Le Gall and Ali Tabatabai, Sub-band coding of digital images using symmetric short kernel filters and arithmetic coding techniques, Proceedings of ICASSP 1988
    locator: the 5/3 symmetric short-kernel filter pair
  - paper: doi:10.1002/cpa.3160450502
    title: A. Cohen, I. Daubechies and J.-C. Feauveau, Biorthogonal bases of compactly supported wavelets, Communications on Pure and Applied Mathematics 45(5), 1992
    locator: the biorthogonal spline filter families, among them the 9/7 pair
  - paper: doi:10.1007/BF02476026
    title: Ingrid Daubechies and Wim Sweldens, Factoring wavelet transforms into lifting steps, Journal of Fourier Analysis and Applications 4(3), 1998
    locator: the factorization of a filter pair into lifting steps, with the 9/7 pair as an example
  - paper: doi:10.1006/acha.1997.0238
    title: A. R. Calderbank, I. Daubechies, W. Sweldens and B.-L. Yeo, Wavelet transforms that map integers to integers, Applied and Computational Harmonic Analysis 5(3), 1998
    locator: integer wavelet transforms by lifting with rounding, including the integer 5/3 transform
---

JPEG 2000 is the wavelet-based image coding standard of the Joint Photographic Experts Group, ITU-T T.800 and ISO/IEC 15444-1. It shifts the samples to be centred on zero, applies a colour transform, cuts the image into tiles, and applies several levels of a 2D [discrete wavelet transform](/discrete-wavelet-transform/), computed by [lifting](/lifting-scheme/): the integer 5/3 transform, which is exactly reversible, or the 9/7 transform in real arithmetic. The coefficients go through a [dead-zone quantizer](/scalar-quantization/) and are cut into code blocks. Each code block is coded on its own by EBCOT (Taubman 2000), a [bit-plane coder](/bit-plane-coding/) with three passes per plane and a binary [arithmetic coder](/arithmetic-coding/), the MQ coder. The encoder then picks, for each block, the cut of its stream that gives the least distortion for the target size. One code stream can be read at many qualities and resolutions, and the 5/3 path is lossless.

## In plain words

First, separate the picture into a small, blurred copy and the details that turn it back into the full picture: edges going across, edges going down, and corners. Repeat this on the small copy a few times. Smooth areas give details that are almost zero.

Then send the numbers from the most important bit down to the least important bit, in small square pieces of the picture. Each piece is coded so that its data can stop after any of many points, and stopping earlier only makes that piece less sharp.

At the end the encoder looks at all the pieces together and decides how much of each to keep to meet the file size, keeping the bits that improve the picture most. A reader can also take only the coarse levels to get a smaller picture, or read everything to get the original back exactly.

## The problem

Given an image of $H \times W$ samples with $B$ bits per sample and one or three components, and either a target size in bytes or a demand for lossless coding, produce a code stream from which a decoder rebuilds an image with small mean squared error, measured by [PSNR](/psnr/), or exactly. The same stream should also give lower qualities and lower resolutions by truncation or by skipping parts.

**The subset on this page.** The implementation covers the stages before the entropy coder for the case of tiles that start at even coordinates: the DC level shift, the reversible colour transform (RCT), tiling, the 5/3 and 9/7 lifting transforms with whole-sample symmetric extension in one and two dimensions with any number of levels, the dead-zone quantizer with the step of Annex E, and the full reversible round trip. It does not implement the irreversible colour transform (ICT), EBCOT tier 1 (code blocks, the coding passes, the contexts, the MQ coder), the rate control (PCRD), tier 2 (packets, layers and progression orders), region of interest coding, or the code stream syntax. Those parts are described below but not coded.

## The algorithm

**Level shift and colour (Annex G).** Unsigned samples get $2^{B-1}$ subtracted. For three components, the lossless path uses the RCT
$$Y = \left\lfloor \frac{R + 2G + B}{4} \right\rfloor, \quad U = B - G, \quad V = R - G,$$
which maps integers to integers and has the exact inverse $G = Y - \lfloor (U + V)/4 \rfloor$, $R = V + G$, $B = U + G$. The lossy path uses the ICT, the real YCbCr matrix of [colour spaces](/color-spaces/) for JPEG.

**Tiles.** The image is cut into rectangular tiles, often one tile for the whole image. Each tile is transformed and coded on its own, which bounds the memory and allows access to parts of the image, at the cost of seams at low rates.

**The wavelet transforms (Annex F).** One level of the 1D transform splits $x[0 \ldots n-1]$ into a low band, the even positions, and a high band, the odd positions. The samples beyond the ends come from *whole-sample symmetric extension*, $x[-i] = x[i]$ and $x[n - 1 + i] = x[n - 1 - i]$. The reversible 5/3 transform has two lifting steps:
$$y[2k+1] = x[2k+1] - \left\lfloor \frac{x[2k] + x[2k+2]}{2} \right\rfloor, \qquad y[2k] = x[2k] + \left\lfloor \frac{y[2k-1] + y[2k+1] + 2}{4} \right\rfloor.$$
The first *predicts* each odd sample from its even neighbours, so a straight line gives 0, and the second *updates* each even sample so that the low band is a smoothed half-size copy. Without the floors these are the 5-tap and 3-tap filters of Le Gall and Tabatabai (1988). The irreversible 9/7 transform has four lifting steps with the real parameters $\alpha, \beta, \gamma, \delta$ of Table F.4, and then a scaling: the low band is divided by $K = 1.230174104914001$ and the high band multiplied by it, so that the low-pass filter has gain 1 at frequency 0 and the high-pass filter gain 2 at the Nyquist frequency. Its analysis filters are the 9-tap and 7-tap filters of Cohen, Daubechies and Feauveau (1992).

In 2D, one level filters every column and then every row of the current LL band, which gives four subbands: LL, HL (high horizontally, low vertically), LH and HH. The next level splits LL again, so $N_L$ levels give $3 N_L + 1$ subbands, the dyadic tree of [subband coding](/subband-coding/).

**Quantization (Annex E).** Each subband $b$ has a step $\Delta_b = 2^{R_b - \varepsilon_b} (1 + \mu_b / 2^{11})$, where $R_b$ is the nominal dynamic range of the subband and the exponent $\varepsilon_b$ and the 11-bit mantissa $\mu_b$ are sent in the code stream. The index is $q = \mathrm{sign}(y) \lfloor |y| / \Delta_b \rfloor$, a quantizer with a dead zone twice as wide as the other cells. The decoder outputs $\mathrm{sign}(q)(|q| + r)\Delta_b$, often with $r = 1/2$. The reversible path uses no quantization, which is the same as $\Delta_b = 1$, and gets its rate control only from truncating bit planes.

**EBCOT tier 1 (Annex D).** Each subband is cut into code blocks, rectangles whose sides are powers of two, often $64 \times 64$. A block is coded by planes of the magnitudes of $q$, from the most significant plane that has a 1 bit down to plane 0. The block is scanned in stripes of four rows, column by column inside a stripe. Each plane, except the first, has three passes:

1. *Significance propagation*: code the bit of each coefficient that is not significant yet but has at least one significant neighbour among its eight neighbours, and the sign of each one that becomes significant. These bits are the most likely to be 1.
2. *Magnitude refinement*: code the bit of each coefficient that became significant in an earlier plane.
3. *Cleanup*: code the bits of all the other coefficients, with a run mode that codes four insignificant coefficients of a column with one symbol.

The first plane has only the cleanup pass. Every bit goes to the MQ coder with a context, 19 contexts in all, chosen from the significance and signs of the neighbours and the subband orientation ([context modeling](/context-modeling/)). The MQ coder (Annex C) is an adaptive binary arithmetic coder without multiplications. It estimates the probability of each context by a state machine of 47 states and renormalizes with shifts. The end of every pass is a possible truncation point of the block stream, so a block of $p$ planes has about $3p$ points.

**Rate control by PCRD.** For each block the encoder records the length $R_i^j$ of the stream up to point $j$ and the distortion $D_i^j$ that remains. Post-compression rate-distortion optimization keeps, in each block, the points on the lower convex hull of its $(R, D)$ curve, and for a slope $\lambda$ chooses the point that minimizes $D_i^j + \lambda R_i^j$. The total length falls as $\lambda$ grows, so a bisection on $\lambda$ meets the target size. For any $\lambda$ the choice minimizes the total distortion among all choices with the same total length (Taubman 2000).

**Tier 2 (Annex B).** The chosen passes go into *packets*, one for each quality layer, resolution, component and precinct (a group of code blocks). A packet header says, with tag trees, which blocks are included and how many passes and bytes each one adds. Several layers give several qualities in one stream. The *progression order*, one of LRCP, RLCP, RPCL, PCRL and CPRL, fixes the order of the packets, for example all of one resolution before the next.

```pseudo id=main
J2K-TRANSFORM(image, NL, Δ)                    ▷ the stages before tier 1
L1  s ← image − 2^(B−1)                         ▷ DC level shift
L2  (Y, U, V) ← (⌊(R + 2G + B)/4⌋, B − G, R − G)    ▷ RCT, for three components
L3  cut each component into tiles
L4  for each tile and each level 1 … NL: LIFT-53 on every column, then on every row, of the current LL band
L5  q ← sign(y) · ⌊|y| / Δb⌋ for each coefficient y of each subband b    ▷ Δb = 1 on the reversible path
L6  return the subbands of q                    ▷ tier 1, PCRD and tier 2 follow
LIFT-53(x[0 … n−1])                             ▷ symmetric extension at both ends; n = 1: return x
L7  for each odd i: y[i] ← x[i] − ⌊(x[i−1] + x[i+1]) / 2⌋        ▷ predict
L8  for each even i: y[i] ← x[i] + ⌊(y[i−1] + y[i+1] + 2) / 4⌋    ▷ update
L9  return (y at even positions, y at odd positions)
```

The decoder undoes each line in reverse order: the inverse of line L8 subtracts the same update from the even samples, and then the inverse of line L7 adds the same prediction to the odd ones.

## Example

**One level of the 5/3 transform.** For $x = (10, 12, 14, 20, 30, 31, 32, 30)$, line L7 gives the odd samples $12 - \lfloor 24/2 \rfloor = 0$, $20 - \lfloor 44/2 \rfloor = -2$, $31 - \lfloor 62/2 \rfloor = 0$ and, with $x[8] = x[6] = 32$, $30 - 32 = -2$. Line L8 gives the even samples $10 + \lfloor (0 + 0 + 2)/4 \rfloor = 10$, using $y[-1] = y[1]$, then $14 + \lfloor 0/4 \rfloor = 14$, $30 + \lfloor 0/4 \rfloor = 30$ and $32$. So the low band is $(10, 14, 30, 32)$ and the high band $(0, -2, 0, -2)$. The inverse subtracts the same updates and adds the same predictions and returns $x$ exactly. A straight line such as $(5, 7, \ldots, 17)$ gives a high band of zeros.

**A gradient in 2D.** For the $8 \times 8$ tile $x(i, j) = 4i + 2j$, one level gives zero in all three high bands except the last row and column of the image, where the symmetric extension bends the line: there the vertical high band holds 4 and the horizontal one holds 2. The LL band is
$$\begin{pmatrix} 0 & 4 & 8 & 13 \\ 8 & 12 & 16 & 21 \\ 16 & 20 & 24 & 29 \\ 25 & 29 & 33 & 38 \end{pmatrix},$$
the samples at even positions, plus 1 next to the edges, where the update step picks up those boundary values.

**Colour.** Pure red, $(255, 0, 0)$ with $B = 8$, becomes $(127, -128, -128)$ after the level shift. The RCT gives $Y = \lfloor -257/4 \rfloor = -65$, $U = 0$, $V = 255$, and the inverse gives $G = -65 - \lfloor 255/4 \rfloor = -128$, $R = 255 - 128 = 127$, $B = 0 - 128 = -128$. The floor must round toward $-\infty$.

**The 9/7 normalization.** A constant signal of ones gives a low band of ones and a high band of zeros; the signal $1, -1, 1, -1, \ldots$ gives a low band of zeros and a high band of magnitude 2. The analysis filters that the lifting steps produce have the taps $0.602949, \pm 0.266864, -0.078223, -0.016864, 0.026749$ (low-pass, centre first) and $1.115087, -0.591272, -0.057544, 0.091272$ (high-pass, centre first), and the high-pass filter gives 0 for cubic polynomials away from the ends.

**Quantization.** With $\Delta = 2$, the coefficients $-4.5, -1.9, 0, 1.9, 2.0, 5.9$ get the indices $-2, 0, 0, 0, 1, 2$. With $\varepsilon_b = 10$, $\mu_b = 1024$ and $R_b = 9$ the step is $2^{-1} \cdot 1.5 = 0.75$.

## Correctness

Each lifting step changes the samples of one parity by a function of the samples of the other parity, and symmetric extension keeps the parity of every index it mirrors. So the decoder can compute the same function, even with floors, and undo the step exactly, whatever the function is. The 5/3 transform therefore maps integers to integers and is exactly invertible, one level and then many levels and both directions of a tile. The RCT is exactly invertible because $R + 2G + B = 4G + U + V$. Tier 1 and tier 2 are lossless coders of the bit planes, so on the reversible path the decoder that reads every pass returns the image exactly. A dead-zone index has error below $\Delta_b$ in the zero cell and at most $\Delta_b / 2$ elsewhere with $r = 1/2$; each dropped bit plane doubles these bounds. The correctness proof of this page gives the details for the transform stages.

## Complexity

Each lifting step of one level of the 1D transform costs $O(1)$ per sample, and the levels of the 2D transform act on $n, n/4, n/16, \ldots$ samples, so the transform costs $\Theta(n)$ time for any number of levels; the level shift, the colour transform and the quantizer cost $\Theta(n)$ as well. Tier 1 visits every coefficient of a block in one of the three passes of every plane, so it costs $\Theta(n p)$ for $p$ planes, each visit costing $O(1)$ for the context and the MQ coder. The rate control costs $O(m \log m)$ for the convex hulls of $m$ truncation points in all, plus a bisection over $\lambda$. The whole coder takes $\Theta(n p)$ time and $\Theta(n)$ space; implementations that transform line by line and code blocks as they fill need much less memory.

## Properties

- **Lossless and lossy in one design.** The 5/3 path with the RCT is exactly reversible, and its stream truncated early is a lossy stream. The 9/7 path gives better compression at moderate and low rates but is never exact.
- **Scalable streams.** Quality layers give several rates from one stream. Dropping the subbands of the finest levels gives the image at half, a quarter, and so on of the size. Precincts and tiles give access to regions without decoding the whole image.
- **Embedded blocks, not an embedded image.** Each code block stream is embedded, and PCRD chooses the cuts after coding, so the encoder meets a target size with near-optimal quality without iterations.
- **Independent code blocks.** Errors and the context state do not cross block boundaries, which helps parallel coding and resilience to errors, at a small cost in compression.
- **No reference oracle.** The Python standard library has no JPEG 2000 codec, and the official conformance streams (ITU-T T.803) were not used here; the transform stages are checked by exact round trips, hand-computed examples and the filter taps.

## Variants and improvements

- **More options (Part 2, ISO/IEC 15444-2).** Other wavelet kernels and decompositions, more general component transforms and other quantizers.
- **Region of interest.** The maxshift method scales the coefficients of a region up by enough bit planes that all of them come before any coefficient of the background, so the region is decoded first and at higher quality.
- **High-throughput block coder.** A later part of the standard replaces the EBCOT block coder by a much faster one that is not embedded inside a block, and keeps the rest of the system.
- **Motion JPEG 2000** codes each frame of a video on its own, and digital cinema distributes films this way.
- **Embedded zerotree coders** such as EZW and [SPIHT](/spiht/) code the whole wavelet image as one embedded stream, using the trees across levels instead of independent blocks.

## When to use it

Use JPEG 2000 when the same image must serve several qualities or resolutions, when lossless and lossy versions must come from one coder, when the samples have more than 8 bits, as in medical, satellite and scientific images, or when very large images must be accessed in parts. At the same rate it usually gives better quality than [JPEG](/jpeg-compression/) at low rates, without block artefacts. Use baseline JPEG when speed and support in every program matter more, and a newer coder when the best compression of ordinary photos is the aim.

## Pitfalls

- **Rounding of negative values.** The floors must round toward $-\infty$. In C, integer division of a negative number truncates toward 0, which breaks exact reversibility with other decoders. Use an arithmetic shift for division by 2 and 4.
- **Coordinates on the canvas.** The split into even and odd samples follows the coordinates of the sample on the reference grid, not its index inside the tile. A tile or image that starts at an odd coordinate puts its first sample in the high band, and the length-1 rule differs. The implementation here assumes even starts.
- **The order of the 2D steps.** For the integer 5/3 transform, filtering rows first and columns second gives other coefficients than columns first, because the floors do not commute. Bit-exact decoders must follow Annex F.
- **The 9/7 transform is not reversible in floating point.** Its round trip has errors of the order of the machine precision, so it cannot give lossless coding even with step 1.
- **Subband names.** HL is the band that is high-pass horizontally and low-pass vertically. Other texts use the opposite order of letters.
- **Dynamic range.** Each level of the 5/3 transform can add a bit of range to the high bands. The guard bits in the code stream must be enough for the number of levels, or the coefficients overflow.
- **Tiles at low rates.** Small tiles cut the wavelet basis at their borders, and the seams become visible when the rate is low.

## Implementations

## History

Embedded wavelet coders, Shapiro's EZW (1993) and the SPIHT coder of Said and Pearlman (1996), showed that a wavelet transform with bit-plane coding beats DCT coding at low rates and gives scalable streams. The JPEG committee started work on a new standard in the late 1990s and chose a wavelet design whose block coder is Taubman's EBCOT (Taubman 2000; Taubman and Marcellin 2002). Part 1 was published as ISO/IEC 15444-1 in December 2000, and ITU-T approved the common text as Recommendation T.800 in August 2002. The 5/3 filters go back to Le Gall and Tabatabai (1988), and the 9/7 filters to Cohen, Daubechies and Feauveau (1992). The lifting form comes from Daubechies and Sweldens (1998), and the integer form with rounding from Calderbank, Daubechies, Sweldens and Yeo (1998).

## References
