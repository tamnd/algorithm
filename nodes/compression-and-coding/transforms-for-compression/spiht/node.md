---
tag: 0AFRWT
kind: algorithm
slug: spiht
name: SPIHT
aliases:
- set partitioning in hierarchical trees
area: compression-and-coding/transforms-for-compression
level: research
summary: "Embedded wavelet image coder: plane by plane, it tests whole trees of coefficients for significance and splits only the trees that hold a significant one."
solves: [lossy-image-compression]
model: word-ram
complexity:
  vars: {N: the number of wavelet coefficients, p: the number of bit planes of the largest magnitude}
  time: {worst: Θ(N p), average: Θ(N p)}
  space: {extra: Θ(N)}
properties: {deterministic: true, recursive: false, online: false, comparison: false}
history:
  year: 1996
  people: [Amir Said, William A. Pearlman]
  note: Published in IEEE Transactions on Circuits and Systems for Video Technology in June 1996 as a faster and simpler successor of Shapiro's zerotree coder EZW (1993).
prereqs: [discrete-wavelet-transform, bit-plane-coding]
see_also: [jpeg-2000, subband-coding, lossy-image-compression, haar-wavelet, lifting-scheme, arithmetic-coding, psnr, transform-coding]
sources:
  - paper: doi:10.1109/76.499834
    title: Amir Said and William A. Pearlman, A new, fast, and efficient image codec based on set partitioning in hierarchical trees, IEEE Transactions on Circuits and Systems for Video Technology 6(3), 1996
    locator: pages 243 to 250 (the spatial orientation trees, the sets H, O, D and L, the lists LIP, LIS and LSP, the sorting and refinement passes, and the coder with and without arithmetic coding)
  - paper: doi:10.1109/78.258085
    title: Jerome M. Shapiro, Embedded image coding using zerotrees of wavelet coefficients, IEEE Transactions on Signal Processing 41(12), 1993
    locator: pages 3445 to 3462 (zerotrees, successive approximation of the coefficients, and the embedded stream)
  - paper: doi:10.1109/83.535842
    title: Amir Said and William A. Pearlman, An image multiresolution representation for lossless and lossy compression, IEEE Transactions on Image Processing 5(9), 1996
    locator: pages 1303 to 1310 (the integer S transform and the S+P transform for lossless and lossy coding)
  - paper: doi:10.1109/83.847830
    title: David Taubman, High performance scalable image compression with EBCOT, IEEE Transactions on Image Processing 9(7), 2000
    locator: pages 1158 to 1170 (embedded coding of independent code blocks, the alternative to coding trees across the levels)
---

SPIHT, set partitioning in hierarchical trees (Said and Pearlman 1996), is an embedded coder for the coefficients of a 2D [discrete wavelet transform](/discrete-wavelet-transform/). It is a [bit-plane coder](/bit-plane-coding/) that sends the planes from the most significant down. It does not send the bits of every coefficient in each plane. It asks yes or no questions about whole sets of coefficients: is any coefficient in this tree at least $2^n$? The trees join each coefficient to the four coefficients at the same place and orientation in the next finer level. In a natural image most trees are insignificant at the high planes, so one bit answers for many coefficients. A set that gives "yes" is split into smaller sets, and the parts are tested again. The decoder runs the same procedure with the bits as input, so the positions of the significant coefficients are never sent. The stream can be cut after any bit, and a longer prefix usually gives a better image. With an integer transform the full stream is lossless.

## In plain words

First turn the picture into a wavelet image: a small, blurred copy in one corner and many detail numbers, most of them near zero. The detail numbers form family trees. A number at a coarse level has four children one level finer, at the same place.

Then make passes with a threshold that is halved each time. In each pass, ask questions with yes or no answers: is this number above the threshold, and is anything in this whole tree above it? One "no" answers for a whole tree of small numbers. A "yes" splits the tree, and the parts are asked again. Numbers found earlier get one more bit each, to make them more exact.

The decoder asks itself the same questions in the same order and reads the answers, so no positions are sent. The stream can stop anywhere and still give a picture.

## The problem

Given the integer wavelet coefficients $c(i, j)$ of an $R \times C$ image, produce a bit stream such that every prefix decodes to an estimate $\hat c$, the error falls as the prefix grows, and the full stream gives $c$ exactly. The quality is measured by the mean squared error or the [PSNR](/psnr/) of the image after the inverse transform. The aim is the best quality for each prefix length, which makes the stream useful at any rate, as in [lossy image compression](/lossy-image-compression/) with a target size that is not known when the image is coded.

**The subset on this page.** The implementation is the binary coder of the paper: the significance, sign and refinement bits go out as they are, without the [arithmetic coding](/arithmetic-coding/) of the symbols that the paper also describes. The wavelet is the integer S-transform, the [Haar wavelet](/haar-wavelet/) computed by [lifting](/lifting-scheme/) with rounding (Said and Pearlman, S+P paper, 1996), on rows and then columns, with $L \ge 1$ levels in the Mallat layout. The paper uses a real biorthogonal wavelet instead. The sides $R$ and $C$ must be multiples of $2^{L+1}$, so the LL band has even sides. The header, made of $R$, $C$, $L$ and $n_{\max}$, is passed as arguments and not coded in bits. Colour images are not handled.

## The algorithm

**The trees.** The Mallat layout puts the LL band of size $R_0 \times C_0$, with $R_0 = R/2^L$ and $C_0 = C/2^L$, in the top-left corner and the detail bands of each level around it. Outside the LL band, the *offspring* $O(i, j)$ of the coefficient $(i, j)$ are the $2 \times 2$ block at $(2i, 2j)$, which is the same place and orientation one level finer, and the coefficients of the finest level have no offspring. In the LL band the roots form $2 \times 2$ groups. The top-left root of a group has no offspring, and each of the other three points to a $2 \times 2$ block in one of the three detail bands of the coarsest level. The sets are:

- $H$, the roots, which are all the coefficients of the LL band;
- $O(i, j)$, the offspring;
- $D(i, j)$, all the descendants;
- $L(i, j) = D(i, j) \setminus O(i, j)$, the descendants except the offspring.

Each coefficient outside $H$ has exactly one parent, so the trees partition the coefficients.

**Significance.** For a set $T$ and a plane $n$, $S_n(T) = 1$ if some coefficient in $T$ has $|c| \ge 2^n$, and 0 otherwise. A coefficient is *significant* at plane $n$ if $|c| \ge 2^n$.

**The lists.** The coder keeps three lists:

- the list of insignificant pixels (LIP), single coefficients not yet significant;
- the list of significant pixels (LSP), coefficients already found significant, in the order they were found;
- the list of insignificant sets (LIS), entries $(i, j)$ of type A, which stand for $D(i, j)$, or of type B, which stand for $L(i, j)$.

**The passes.** The plane starts at $n_{\max} = \lfloor \lg \max |c| \rfloor$ and falls by one after each pass. Each pass has two parts, the *sorting pass* (lines L3 to L9) and the *refinement pass* (line L10).

```pseudo id=main
SPIHT-ENCODE(c, L)                              ▷ c: integer wavelet coefficients, L levels
L1  LIP ← H;  LIS ← {(i, j, A) : (i, j) ∈ H has offspring};  LSP ← ∅;  n ← ⌊lg max |c|⌋
L2  while n ≥ 0:
L3      for each (i, j) in LIP: output S_n(i, j); if 1, output the sign and move (i, j) to LSP
L4      for each entry (i, j, type) in LIS, including entries appended during this loop:
L5          if type A: output S_n(D(i, j)); if 1:
L6              for each (k, l) ∈ O(i, j): output S_n(k, l); if 1, output the sign and append (k, l) to LSP, else append (k, l) to LIP
L7              if L(i, j) ≠ ∅ move (i, j) to the end of LIS as type B, else remove it
L8          if type B: output S_n(L(i, j)); if 1:
L9              append each (k, l) ∈ O(i, j) to LIS as type A, and remove (i, j)
L10     for each (i, j) in LSP that was there before this pass: output bit n of |c(i, j)|
L11     n ← n − 1
```

The decoder is the same procedure with "output" replaced by "input". The tests $S_n$ are not computed but read from the stream, and the test $L(i, j) \ne \emptyset$ of line L7 depends only on the geometry. When a coefficient becomes significant at plane $n$ the decoder knows $2^n \le |c| < 2^{n+1}$; each refinement bit halves the interval. The decoder of the implementation places each estimate at the middle of its interval, $\pm(K + 2^{k-1})$, where $K$ is the known part of $|c|$ and $k$ the lowest known plane.

To make each set test cost $O(1)$, the encoder first computes $\max |c|$ over $D(i, j)$ and over $L(i, j)$ for every node, from the leaves up, in $O(N)$ time.

## Example

**A small coefficient array.** Take an $8 \times 8$ array with $L = 2$, so the LL band is the $2 \times 2$ block at the top left. All coefficients are 0 except $c(0,0) = 26$, $c(0,1) = 6$, $c(1,0) = -3$ and $c(1,1) = 2$ in the LL band, $c(0,2) = 13$ and $c(0,3) = -12$ in the detail band to the right of LL at the coarsest level, and $c(0,4) = -9$ at the finest level. The root $(0,1)$ has the offspring $(0,2), (0,3), (1,2), (1,3)$, and $(0,2)$ has the offspring $(0,4), (0,5), (1,4), (1,5)$. The root $(0,0)$ has none. Here $n_{\max} = 4$.

| plane $n$ | threshold | bits of the pass | count | nonzero estimates after the pass | squared error |
|---|---|---|---|---|---|
| 4 | 16 | `10000000` | 8 | $(0,0) = 24$ | 447 |
| 3 | 8 | `00011011000011110000001` | 23 | $28$, $(0,2) = 12$, $(0,3) = -12$, $(0,4) = -12$ | 63 |
| 2 | 4 | `100000000000000110` | 18 | $26$, $(0,1) = 6$, $14$, $-14$, $-10$ | 19 |
| 1 | 2 | `1110000000000010001` | 19 | $27$, $7$, $13$, $-13$, $-9$, $(1,0) = -3$, $(1,1) = 3$ | 4 |
| 0 | 1 | `00000000000101010` | 17 | all exact | 0 |

In the pass of plane 4, the LIP holds the four roots: $(0,0)$ gives 1 and the sign 0 (positive), and the other three give 0. The LIS holds $(0,1)$, $(1,0)$ and $(1,1)$ as type A, and their trees have maxima 13, 0 and 0, all below 16, so three more 0 bits. There is nothing to refine yet. That makes 8 bits.

In the pass of plane 3, the three roots left in the LIP give `000`. The tree of $(0,1)$ gives 1, so its offspring are tested: $(0,2)$ gives `10` (significant, positive), $(0,3)$ gives `11` (significant, negative), and $(1,2)$ and $(1,3)$ give 0 and go to the LIP. $L(0,1)$ is not empty, so $(0,1)$ goes to the end of the LIS as type B. The trees of $(1,0)$ and $(1,1)$ give `00`. Then the type B entry is reached in the same pass: $L(0,1)$ holds $-9$, so it gives 1 and the four offspring of $(0,1)$ enter the LIS as type A. The tree of $(0,2)$ gives 1, its offspring give `11` for $(0,4)$ and `000` for the rest, and $L(0,2)$ is empty, so the entry is removed. The trees of $(0,3)$, $(1,2)$ and $(1,3)$ give `000`. The refinement pass sends bit 3 of 26, which is 1. That makes 23 bits.

The full stream has 85 bits. The plain bit-plane coder, which sends every bit of every plane and one sign for each nonzero coefficient, needs $64 \cdot 5 + 7 = 327$ bits for the same array. The squared error falls after each pass, but not for each coefficient: the estimate of $(0,0)$ is exact after plane 2 and is 27 after plane 1, because midpoint reconstruction is exact only by chance.

**A synthetic image.** The tests build a $64 \times 64$ image with 8-bit samples: a gradient, a bright disc, a small checkerboard patch, and Gaussian noise with standard deviation 3, with a fixed seed. With $L = 4$ levels, $n_{\max} = 7$ and the full stream has 20672 bits, 5.05 bits per pixel, and decodes to the exact image. The prefixes of 0.25, 0.5, 1 and 2 bits per pixel give a PSNR of 21.66, 28.57, 30.66 and 36.36 dB. These numbers are for this image and the integer Haar transform only. They do not compare with the published results, which use a real wavelet and photographs.

## Correctness

The trees partition the coefficients, because each coefficient outside the LL band has exactly one parent and each child lies at a larger $i + j$ than its parent. The decoder stays in step with the encoder, because every branch of the encoder depends only on the list state and the bit just sent, and the decoder reads that bit. After the sorting pass of plane $n$, the lists still partition the coefficients, every coefficient in the LIP or in a set of the LIS is below $2^n$, and the LSP holds exactly the coefficients with $|c| \ge 2^n$. So after the full pass of plane $n$ every estimate is within $2^n - 1$, a prefix cut during the pass of plane $n$ is within $2^{n+1} - 1$, and the full stream is exact. The integer S-transform is a pair of lifting steps and is exactly invertible, so the full stream gives the original image. The correctness proof of this page has the details.

## Complexity

Each pass visits each entry of the LIP, the LIS and the LSP a constant number of times, and each list has at most $N$ entries, so a pass costs $O(N)$ and the whole coder $O(N p)$ with $p = n_{\max} + 1$ planes. An image whose coefficients are all large reaches this bound, because the refinement passes alone send about $N(p - 1)$ bits. The tables of the maxima over $D$ and $L$ cost $\Theta(N)$, and the lists and tables take $\Theta(N)$ space. The decoder does the same work as the encoder. The transform costs $\Theta(N)$ for any number of levels.

## Properties

- **Embedded.** Every prefix of the stream is a valid code of the image, so the encoder can stop at any target size and a reader can stop earlier.
- **Positions for free.** The decoder learns where the significant coefficients are from the order of the decisions. An insignificant tree costs one bit in each pass.
- **No training and no tables.** The coder needs no codebook, no Huffman table and no model; the binary version uses only comparisons, shifts and lists.
- **Lossless with an integer transform.** With the S-transform or another integer wavelet, the full stream returns the image exactly.
- **Fragile to bit errors.** A single wrong bit changes the branch the decoder takes, and the rest of the stream is decoded wrongly.

## Variants and improvements

- **Arithmetic coding of the symbols.** The paper also codes the significance bits of groups of coefficients with an adaptive arithmetic coder, which gives a small gain over the binary output.
- **Lossless coding with the S+P transform.** Said and Pearlman add a prediction step to the S-transform and code the result with the same set partitioning (Said and Pearlman, IEEE Transactions on Image Processing, 1996).
- **EZW.** Shapiro's zerotree coder (1993) is the predecessor: it codes the same kind of trees with a four-symbol alphabet and arithmetic coding.
- **Other sets.** Later coders use the same set partitioning with square blocks inside each subband instead of trees across levels, or with trees in three dimensions for video.
- **Block coding.** EBCOT (Taubman 2000) codes independent code blocks with contexts and chooses the cut of each block after coding. This gives better error resilience and random access, and [JPEG 2000](/jpeg-2000/) uses it.

## When to use it

Use SPIHT when an embedded stream from one simple encoder is needed, for example for progressive transmission, for a target size that is not known in advance, or for teaching how wavelet coders exploit the structure of the [subband](/subband-coding/) decomposition. Its binary version is small and needs no entropy coder. For images that must be exchanged, use a standard such as JPEG 2000. For channels with errors, use a block coder or protect the stream, because one wrong bit ruins the rest.

## Pitfalls

- **Entries appended during the pass.** The LIS loop must also process the entries appended in the same pass. If it runs over a copy of the list, a coefficient can become significant one pass late, and the decoder then places it in the wrong interval.
- **Refining new entries.** The refinement pass visits only the entries that were in the LSP before the pass. A coefficient found in this pass already has its bit for this plane, which is 1.
- **The roots.** The top-left root of each $2 \times 2$ group has no offspring. Giving it offspring makes some coefficients belong to two trees, which breaks the partition. The rule also needs even sides for the LL band.
- **Rounding of the transform.** With a real wavelet the coefficients must be rounded or scaled to integers before coding, and the reconstruction error then includes that rounding.
- **The norm of the transform.** The S-transform is not orthonormal: its bands have different gains, so a bit in one band changes the image error more than the same bit in another band. The bound on the coefficient error is not a bound on the pixel error, and the order of the bits is then not the best order for the mean squared error.
- **Reconstruction point.** A decoder that sets a significant coefficient to the lower end of its interval, $K$, has twice the worst-case error of the midpoint.

## Implementations

## History

Shapiro introduced embedded zerotree coding of wavelet coefficients in 1993: the bits are sent in the order of their importance, and a single symbol says that a coefficient and all its descendants are insignificant (Shapiro 1993). Said and Pearlman recast this as a partition of the coefficients into sets that are split when they become significant, with three lists that track the state. They published SPIHT in IEEE Transactions on Circuits and Systems for Video Technology in June 1996. They reported results that matched or surpassed those of earlier and more complex coders, and a binary version without arithmetic coding that was faster with only a small loss (Said and Pearlman 1996). In the same year they described the S+P transform for lossless coding with the same coder (Said and Pearlman, IEEE Transactions on Image Processing, 1996). The JPEG 2000 standard later chose block coding with EBCOT instead of trees across levels (Taubman 2000).

## References
