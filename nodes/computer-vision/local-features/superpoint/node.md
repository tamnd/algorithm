---
tag: P2KH05
kind: algorithm
slug: superpoint
name: SuperPoint
aliases:
- self-supervised interest point detection
area: computer-vision/local-features
level: research
summary: A network that detects points and computes descriptors in one pass, trained on its own detections warped by random homographies, called homographic adaptation.
solves: [feature-detection]
model: real-ram
complexity:
  vars: {W: the image width, H: the image height, K: the number of kept points, C: the descriptor length, r: the suppression radius}
  time: {worst: O(W H log(W H) + K r^2 + K C), average: O(W H log(W H) + K r^2 + K C), best: O(W H + K C)}
  space: {extra: O(W H + K C)}
properties: {deterministic: true, learned: true, rotation_invariant: false, scale_invariant: false, network_cost_excluded: true}
history:
  year: 2018
  people: [Daniel DeTone, Tomasz Malisiewicz, Andrew Rabinovich]
  note: DeTone, Malisiewicz and Rabinovich of Magic Leap presented SuperPoint at the CVPR 2018 workshops, with a detector trained first on synthetic shapes and then on its own homographic adaptations.
prereqs: [feature-detection, feature-descriptor, non-maximum-suppression]
see_also: [superglue, loftr, harris-corner-detector, sift, orb-features, homography, bilinear-interpolation, detector-repeatability]
sources:
  - paper: doi:10.1109/CVPRW.2018.00060
    title: "Daniel DeTone, Tomasz Malisiewicz and Andrew Rabinovich, SuperPoint, self-supervised interest point detection and description, IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW), 2018 (arXiv 1712.07629)"
    locator: "Section 3.1 (the shared encoder with cells of 8 x 8 pixels), Section 3.2 (the 65-channel detector head, the softmax and the reshape), Section 3.3 (the descriptor head, the interpolation and the L2 normalization), the sections on the losses, on homographic adaptation and on the HPatches experiments"
  - paper: doi:10.1109/CVPR42600.2020.00499
    title: "Paul-Edouard Sarlin, Daniel DeTone, Tomasz Malisiewicz and Andrew Rabinovich, SuperGlue, learning feature matching with graph neural networks, IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2020 (arXiv 1911.11763)"
    locator: the experiments that use SuperPoint keypoints and descriptors as the input of the matcher
  - paper: doi:10.1109/CVPR46437.2021.00881
    title: "Jiaming Sun, Zehong Shen, Yuang Wang, Hujun Bao and Xiaowei Zhou, LoFTR, detector-free local feature matching with transformers, IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2021 (arXiv 2104.00680)"
    locator: the comparison with SuperPoint and SuperGlue as a detector-based baseline
---

SuperPoint is a convolutional network that takes a gray image and, in one forward pass, returns a score for each pixel of being an interest point and a [descriptor](/feature-descriptor/) for each point. A shared encoder reduces the image to cells of $8 \times 8$ pixels. The detector head gives 65 values per cell, one for each of the 64 pixels and one for "no point here", and the descriptor head gives a coarse map of 256-value vectors. The network is trained by homographic adaptation: it detects points on many random [homography](/homography/) warps of each training image and uses the merged detections as its own labels. This page covers the decoding step that turns the two outputs into keypoints and descriptors, with its proof and code; the network and its training are outside the page, and their quality is a measured result, not a theorem.

## In plain words

The network looks at the image in small squares of 8 by 8 pixels. For each square it gives 65 numbers. Sixty-four of them say how likely each pixel of the square is to be a good point, and the last one says how likely it is that the square has no good point at all. A softmax turns the 65 numbers into chances that add up to 1. We throw away the "no point" chance and put the other 64 back in their pixels, which gives a score for every pixel of the image. Then we keep pixels with a high score, and among pixels that are close together we keep only the best one. For each kept pixel we read a vector from a second output of the network and scale it to length 1. Two views of the same spot should give close vectors.

## The problem

The input is the output of the network for an image of $H \times W$ pixels, with $H = 8 H_c$ and $W = 8 W_c$:

- $X$, an array of $H_c \times W_c$ cells, each a vector of 65 logits $z_0, \dots, z_{64}$. Channel $c < 64$ belongs to the pixel at row $\lfloor c/8 \rfloor$ and column $c \bmod 8$ of the cell. Channel 64 is the no-point bin, which the paper calls the dustbin.
- $F$, an array of $H_c \times W_c$ descriptor vectors of length $C$, with $C = 256$ in the paper.
- A score threshold $\tau$, a suppression radius $r$ in pixels and a border width $\beta$.

The output is a list of keypoints $(u, v)$ with scores, where $u$ is the column and $v$ the row, and one descriptor of Euclidean norm 1 for each keypoint. The keypoints are the pixels of the heat map that survive the threshold, the border and greedy [non-maximum suppression](/non-maximum-suppression/).

## The algorithm

```pseudo id=main
SUPERPOINT-DECODE(X, F, τ, r, β)
L1  for each cell (c_x, c_y) of the H_c × W_c grid do
L2      p ← softmax of the 65 logits of X[c_y][c_x]
L3      for c = 0 to 63 do heat[8 c_y + ⌊c/8⌋][8 c_x + (c mod 8)] ← p_c     ▷ p_64 is dropped
L4  P ← the pixels (u, v) with heat[v][u] ≥ τ and at least β pixels from each border
L5  sort P by decreasing score, ties by row and then by column
L6  K ← empty list; mark every pixel free
L7  for each pixel (u, v) of P in this order do
L8      if (u, v) is free then append (u, v) to K and mark the (2r + 1) × (2r + 1) square around it not free
L9  for each (u, v) in K do
L10     f ← bilinear sample of F at ((u - 3.5)/8, (v - 3.5)/8), clamped to the grid
L11     output (u, v, heat[v][u]) and f / ‖f‖
```

Lines L1 to L3 are the softmax and the reshape of Section 3.2 of the paper. The softmax is taken over all 65 channels, so a cell with a large dustbin value gives low scores to all its pixels; a cell can hold at most one strong point. Line L3 is the "depth to space" step: the 64 channels become an $8 \times 8$ block of pixels. Lines L6 to L8 mark squares on a grid, so each test is $O(1)$; this is the same greedy suppression as a test against every kept point. Line L10 is our choice of interpolation. The paper samples $F$ with bicubic interpolation and then normalizes; we use [bilinear interpolation](/bilinear-interpolation/) with the center of coarse cell $(c_x, c_y)$ at pixel $(8 c_x + 3.5, 8 c_y + 3.5)$. Other alignments of the coarse grid with the pixels are in use, and descriptors are comparable only under the same one.

The network before the decoder, from Section 3 of the paper: a VGG-style encoder with three max-pooling layers turns the $H \times W$ image into an $H_c \times W_c$ map. The detector head and the descriptor head are small convolutional layers on this map. The detector is trained with a cross-entropy loss over the 65 classes of each cell, and the descriptor with a hinge loss that pulls together the descriptors of cells that correspond under a known homography and pushes apart the others, with one margin for the positive pairs and one for the negative pairs.

## Example

Take an image of $8 \times 16$ pixels, so $H_c = 1$ and $W_c = 2$. In cell 0 the logits are $z_{27} = 4$, $z_{28} = 3.5$, $z_{64} = 3$ and 0 for the other 62 channels. The softmax denominator is $e^4 + e^{3.5} + e^3 + 62 = 54.598 + 33.115 + 20.086 + 62 = 169.80$. So $p_{27} = 0.3215$, $p_{28} = 0.1950$, the dustbin gets $0.1183$, and each other channel $1/169.80 = 0.0059$. Channel 27 is row $\lfloor 27/8 \rfloor = 3$ and column $27 \bmod 8 = 3$, so pixel $(u, v) = (3, 3)$ gets 0.3215. Channel 28 goes to $(4, 3)$ with 0.1950.

In cell 1 only the dustbin is high, $z_{64} = 6$. Then $p_{64} = e^6 / (e^6 + 64) = 403.43 / 467.43 = 0.8631$, and each of the 64 pixels gets $1/467.43 = 0.0021$.

With $\tau = 0.015$ and $\beta = 0$, line L4 keeps only $(3, 3)$ and $(4, 3)$; the values 0.0059 and 0.0021 are below the threshold. With $r = 0$ both are kept. With $r = 1$ or more, $(3, 3)$ comes first, marks its square, and $(4, 3)$ at Chebyshev distance 1 is suppressed. The output is one keypoint, $(3, 3)$ with score 0.3215. Its descriptor is the bilinear sample of $F$ at $((3 - 3.5)/8, (3 - 3.5)/8) = (-0.0625, -0.0625)$, which the clamp moves to the center of cell 0, so it is $F[0][0]$ divided by its norm.

## Correctness

The decoder has a proof; the network does not. The proof in `proofs/correctness.md` shows:

- **Per-cell probabilities.** The 64 heat values of a cell are in $(0, 1)$ and add up, with the dustbin, to 1. Adding a constant to the 65 logits of a cell does not change them.
- **The reshape is a bijection.** Each of the $H W$ pixels gets exactly one channel of one cell.
- **Greedy suppression.** The grid marks of lines L6 to L8 give the same list as the test "no kept point within Chebyshev distance $r$" in order of score. Kept points are more than $r$ apart, and each removed candidate is within $r$ of a kept point with a score at least its own.
- **Descriptors.** The bilinear sample is a convex combination of four map vectors, it is exact for a map that is affine in the cell index, and the output has norm 1.

What the network outputs is not proved to be good. The paper measures it. On HPatches (116 scenes, 696 images, 2018), with a correct-distance threshold of 3 pixels, SuperPoint did better than LIFT and ORB on homography estimation and was comparable to SIFT; the paper also reports repeatability against classical detectors. These are benchmark results with the protocol and the image size of the paper.

## Complexity

The model is the real RAM, and the cost of the network is outside the page. Let $n = W H$.

- Lines L1 to L3 take $O(65 H_c W_c) = O(n)$ time.
- Line L4 is $O(n)$ and line L5 sorts at most $n$ candidates, $O(n \log n)$. A threshold that keeps few pixels makes this small; a bucket sort on quantized scores makes it $O(n)$.
- Lines L6 to L8 take $O(n)$ for the grid and $O(r^2)$ for each kept point, so $O(n + K r^2)$.
- Lines L9 to L11 take $O(C)$ per kept point, $O(K C)$ in total.

The total is $O(n \log n + K r^2 + K C)$ time and $O(n + K C)$ space. The paper reports about 11.15 ms for one forward pass of the network on a Titan X GPU for a $480 \times 640$ image, and about 1.5 ms on a CPU for the descriptor sampling of 1000 points. These are measurements on the hardware of 2018.

## Properties

- **One pass for both tasks.** Points and descriptors share the encoder, unlike a classical [detector](/feature-detection/) followed by a separate descriptor.
- **At most one strong point per cell.** The softmax over 65 channels makes the pixels of a cell compete, and the suppression removes the rest of the clusters.
- **Pixel accuracy.** The keypoints are pixel positions of the heat map. The decoder does not refine them to subpixel positions.
- **Not rotation invariant.** The network sees upright images with homographies of limited rotation during training. Large in-plane rotations lower the matching rate.
- **No explicit scale.** There is no scale space. Training warps include scale changes, so moderate scale changes work.
- **Learned.** The behavior depends on the training data and the weights. There is no invariance theorem as for [SIFT](/sift/).

## Variants and improvements

- **MagicPoint.** The detector alone, trained on synthetic shapes with known corners, is the first stage of the training.
- **Homographic adaptation.** The paper warps each training image with about 100 random homographies, runs the detector on each, warps the heat maps back and averages them, and uses the result as the label. Repeating this improves the labels.
- **Matchers on top.** [SuperGlue](/superglue/) matches SuperPoint points with attention and optimal transport, and LightGlue is a later faster matcher. Classical matching with [mutual nearest neighbors](/mutual-nearest-neighbor-matching/) or the [ratio test](/lowe-ratio-test/) also works on its descriptors.
- **Other learned features.** LIFT, D2-Net, R2D2 and DISK are other learned detectors and descriptors. [LoFTR](/loftr/) drops the detector and matches dense coarse features.

## When to use it

Use SuperPoint when you need repeatable points and good descriptors on images with strong changes of viewpoint or light, for example in visual localization or [structure from motion](/structure-from-motion-problem/), and a GPU is available. Pair it with SuperGlue or a [ratio test](/lowe-ratio-test/) and then [RANSAC](/ransac/). Use [ORB](/orb-features/) when there is no GPU and speed matters most, and [SIFT](/sift/) when you need scale and rotation invariance with well understood behavior.

## Pitfalls

- **The image size.** $H$ and $W$ must be multiples of 8, or the cells do not cover the image. Crop or pad first.
- **The channel order.** Channel $c$ is row $\lfloor c/8 \rfloor$ and column $c \bmod 8$ of the cell. A different order in the reshape gives keypoints at wrong pixels that still look plausible.
- **Softmax over 64 channels.** Dropping the dustbin before the softmax removes the "no point" option, and every cell then has a pixel with a high score.
- **Grid alignment.** The descriptor map is 8 times coarser. Sample it with the alignment used in training; an offset of half a cell changes the descriptors.
- **Normalize after sampling.** Interpolation of unit vectors gives vectors shorter than 1. Normalize after line L10, as line L11 does.
- **Border.** Points near the border have poor descriptors. Remove them with $\beta$ before matching.
- **Thresholds are tuned.** $\tau$, $r$ and $\beta$ are design choices. The paper evaluates suppression radii of 4 and 8 pixels on HPatches.

## Implementations

The network is outside this page. The Python code in `impl/python/superpoint.py` implements only the decoder of lines L1 to L11 on network outputs that the tests build by hand or with a fixed seed: the per-cell softmax and reshape, the threshold and border, the grid suppression, and the bilinear sampling and normalization of the descriptors. The tests check that each cell sums to 1 with its dustbin, that each channel goes to its pixel, that the grid suppression equals a brute-force greedy suppression (with ties), that the kept points satisfy the properties of the theorem, and that the sampling is exact on an affine map.

## History

Learned interest points before SuperPoint, such as LIFT (2016), used separate networks for detection, orientation and description, trained with points from a classical pipeline. DeTone, Malisiewicz and Rabinovich (2018) trained one network for both tasks without human labels: a detector trained on synthetic shapes labels real images through homographic adaptation, and the full network learns from those labels. In 2020 Sarlin and the same group added SuperGlue on top, and the pair became a common baseline for learned matching.

## References
