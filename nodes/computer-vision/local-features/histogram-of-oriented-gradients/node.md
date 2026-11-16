---
tag: DA8C98
kind: algorithm
slug: histogram-of-oriented-gradients
name: Histogram of oriented gradients
aliases:
- HOG
- HOG descriptor
area: computer-vision/local-features
level: core
summary: Describe a window by histograms of gradient orientation over a grid of small cells, normalized over overlapping blocks of cells; with linear SVMs it became a standard pedestrian detector.
solves: [object-detection]
model: real-ram
complexity:
  vars: {W: the window width in pixels, H: the window height in pixels, B: the number of orientation bins, c: the side of a cell in pixels}
  time: {worst: O(W H + W H B / c^2), average: O(W H + W H B / c^2), best: O(W H + W H B / c^2)}
  space: {extra: O(W H + W H B / c^2)}
properties: {deterministic: true, exact: true, rotation_invariant: false, scale_invariant: false, heuristic: true}
history:
  year: 2005
  people: [Navneet Dalal, Bill Triggs]
  note: Dalal and Triggs presented HOG with a linear SVM for detecting people at CVPR 2005, together with the INRIA person data set.
prereqs: [feature-descriptor, image-histogram]
see_also: [dalal-triggs-detector, sliding-window-detection, support-vector-machine, sift, deformable-part-model, sobel-operator, integral-image, local-binary-patterns]
sources:
  - paper: doi:10.1109/CVPR.2005.177
    title: Navneet Dalal and Bill Triggs, Histograms of oriented gradients for human detection, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), vol. 1, 886-893, 2005
    locator: Section 4 (overview of the method), Section 6.1 (gamma and color), Section 6.2 (gradient masks), Section 6.3 (orientation binning), Section 6.4 (blocks and the L2-norm, L2-Hys, L1-norm and L1-sqrt schemes), Section 6.5 (the 64 x 128 window), Section 6.6 (the linear SVM)
  - paper: doi:10.1023/B:VISI.0000029664.99615.94
    title: David G. Lowe, Distinctive image features from scale-invariant keypoints, International Journal of Computer Vision 60(2), 91-110, 2004
    locator: Section 6.1 (gradient histograms in cells, trilinear voting, the clipping at 0.2 that L2-Hys follows)
  - paper: doi:10.1109/TPAMI.2009.167
    title: Pedro F. Felzenszwalb, Ross B. Girshick, David McAllester and Deva Ramanan, Object detection with discriminatively trained part-based models, IEEE Transactions on Pattern Analysis and Machine Intelligence 32(9), 1627-1645, 2010
    locator: Section 6 (the HOG features of the part model and the reduced form)
---

The histogram of oriented gradients (HOG) describes the shape in an image window by the directions of its edges. It divides the window into small cells, for example $8 \times 8$ pixels, and builds for each cell a histogram of gradient orientations weighted by the gradient magnitude. It then groups the cells into overlapping blocks of $2 \times 2$ cells and normalizes each block, so that the descriptor does not depend much on the light and the contrast. Dalal and Triggs introduced HOG in 2005 for detecting people with a linear [support vector machine](/support-vector-machine/), the [Dalal-Triggs detector](/dalal-triggs-detector/). It describes a whole window, not a keypoint, but it uses the same cells of gradient histograms as the [SIFT](/sift/) descriptor.

## In plain words

Cut an image window into a grid of small squares. In each square, find the direction of the edges at each pixel, from the change of brightness to the next pixel. Count the directions in 9 groups, from horizontal through vertical and back, and let strong edges count more than weak ones. The 9 counts of each square show which way the edges in that square go. A person standing upright gives many vertical edges at the sides of the body and a round outline at the head. Then take groups of 2 by 2 squares and scale the counts of each group so that they do not depend on how bright or how contrasted that part of the image is. Write all the scaled counts one after the other. A classifier learns which patterns of counts belong to a person.

## The problem

The input is a gray window $I$ with $W$ columns and $H$ rows, a cell size $c$, a number of orientation bins $B$ and a block size of $2 \times 2$ cells. A pixel is $(u, v)$, with $u$ the column (to the right) and $v$ the row (down). The gradient is

$$g_u(u, v) = I(u + 1, v) - I(u - 1, v), \qquad g_v(u, v) = I(u, v + 1) - I(u, v - 1),$$

the centered mask $[-1, 0, 1]$ with no smoothing. The magnitude is $m = \sqrt{g_u^2 + g_v^2}$, and the unsigned orientation is $\varphi = \operatorname{atan2}(g_v, g_u)$ folded into $[0°, 180°)$, so a dark-to-bright edge and a bright-to-dark edge with the same direction get the same orientation. For color images Dalal and Triggs take, at each pixel, the gradient of the color channel with the largest magnitude.

The $B$ bins have the centers $(b + \frac12) \cdot 180°/B$ for $b = 0, \dots, B - 1$. A pixel votes $m$ into the two bins whose centers are nearest to $\varphi$ on the circle of 180 degrees, with weights that fall linearly with the distance. With spatial interpolation, the vote is also split between the four nearest cell centers by bilinear weights; this is trilinear voting. A block of $2 \times 2$ cells gives a vector $x$ of $4B$ values, normalized by L2-Hys:

$$x \leftarrow \frac{x}{\sqrt{\lVert x \rVert_2^2 + \varepsilon^2}}, \qquad x_k \leftarrow \min(x_k, 0.2), \qquad x \leftarrow \frac{x}{\sqrt{\lVert x \rVert_2^2 + \varepsilon^2}} .$$

The blocks move by one cell, so each inner cell is in four blocks with four different normalizations. The output is the concatenation of all normalized blocks. For the default window of $64 \times 128$ pixels, $c = 8$ and $B = 9$, there are $8 \times 16$ cells and $7 \times 15$ blocks of 36 values, so the descriptor has $7 \times 15 \times 36 = 3780$ values.

## The algorithm

```pseudo id=main
HOG(I, c, B)                            ▷ I is a W × H window
L1  g_u, g_v ← I filtered by [-1, 0, 1] in u and in v
L2  m ← sqrt(g_u^2 + g_v^2), φ ← atan2(g_v, g_u) mod 180°
L3  for each pixel, find the two orientation bins nearest to φ and their linear weights
L4  add m × (bin weight) × (bilinear cell weight) to the histograms of the four nearest cells
L5  for each block of 2 × 2 cells, moving by one cell do
L6      x ← the four cell histograms, one after the other
L7      x ← L2-Hys(x): divide by the L2 norm, clip at 0.2, divide by the L2 norm again; append x to the output
L8  return the output
```

The paper also weights the pixels of each block by a Gaussian window with $\sigma$ equal to half the block width, 8 pixels for a block of 16 pixels. This makes the cell histograms differ from block to block. Our code leaves the Gaussian window out, so it computes each cell histogram once and shares it among the blocks; the page says where this matters below.

For detection, a linear classifier scores the descriptor of each window position at each scale of an image pyramid, which is [sliding window detection](/sliding-window-detection/). Dalal and Triggs train a soft linear SVM ($C = 0.01$ with SVMLight) on the INRIA data, then search the negative images for hard false positives and train again.

## Example

**One vote.** A pixel has $g_u = 30$ and $g_v = 40$. Its magnitude is 50 and its orientation is $\varphi = \operatorname{atan2}(40, 30) \approx 53.13°$. With $B = 9$ the bin centers are $10°, 30°, 50°, \dots, 170°$. The angle lies between the centers $50°$ (bin 2) and $70°$ (bin 3), at $3.13 / 20 \approx 0.157$ of the way. So bin 2 gets $50 \times 0.843 \approx 42.17$ and bin 3 gets $50 \times 0.157 \approx 7.83$. Without spatial interpolation both votes go to the cell of the pixel.

**A vertical edge.** In a window that is 0 on the left half and 100 on the right half, the pixels next to the edge have $g_u = 100$ and $g_v = 0$, so $\varphi = 0°$. The angle 0 lies half way between the centers $170°$ and $10°$, so bins 8 and 0 each get 50. A row of 8 edge pixels in one cell gives 400 in bin 0 and 400 in bin 8. A black-to-white edge and a white-to-black edge give the same histogram.

**L2-Hys.** A block vector with the values $12, 4, 3$ and 0 elsewhere has the L2 norm 13 (take $\varepsilon = 0$). After the first division it is $0.923, 0.308, 0.231$. All three are above 0.2 and are clipped to 0.2, and the second division gives $0.577$ for each. The clipping stops the one strong edge from dominating the block.

**Length.** A $64 \times 64$ window has $8 \times 8$ cells and $7 \times 7$ blocks, so $7 \times 7 \times 36 = 1764$ values; the $64 \times 128$ window has 3780.

## Correctness

HOG is a definition, so correctness means that the code computes the histograms and blocks as defined. The proof in `proofs/correctness.md` shows that:

- The two orientation weights of a pixel are nonnegative and sum to 1, and so do the four bilinear cell weights for a pixel whose four nearest cell centers are in the window. So such a pixel adds exactly $m$ to the cells in total.
- The descriptor does not change when a constant is added to the window, since the gradient does not change. It does not change when the window is replaced by $a - I$, since the gradient changes sign and the unsigned orientation does not.
- A mirror image in $u$ maps the cell in column $x$ to the cell in column $n_x - 1 - x$ and the bin $b$ to the bin $B - 1 - b$.
- With $\varepsilon = 0$, the L2-Hys output has norm 1 and does not change when the block is multiplied by $a > 0$. With $\varepsilon > 0$ the change is small for blocks with a norm much larger than $\varepsilon$.

That HOG with a linear SVM detects people well is a benchmark result. Dalal and Triggs report miss rates at $10^{-4}$ false positives per window on their INRIA set of 1805 images of people of $64 \times 128$ pixels and on the MIT set.

## Complexity

The model is the [real RAM](/real-ram/), with the square root, atan2 and the floor in $O(1)$ time.

- Lines L1 and L2 take $O(W H)$ time.
- Lines L3 and L4 take $O(1)$ time per pixel, with 2 bins and at most 4 cells, so $O(W H)$ in total.
- There are about $(W/c)(H/c)$ blocks of $4B$ values. Lines L5 to L7 take $O(W H B / c^2)$ time.

The total time is $O(W H + W H B / c^2)$, and the extra space is $O(W H)$ for the gradients and $O(W H B / c^2)$ for the cells and the output. For dense detection, the cells are computed once for the whole image at each scale and shared by all windows, so the cost per window is only the reading of its blocks and the dot product with the SVM weights.

## Properties

- **Not rotation or scale invariant.** HOG fixes the grid to the window. Detection gets scale invariance from an image pyramid, and people are mostly upright, so rotation invariance is not wanted.
- **Robust to small shifts.** Each cell pools the gradients of $c \times c$ pixels, and trilinear voting removes the jumps at the cell borders.
- **Light and contrast.** The gradient removes a constant offset. The block normalization removes a gain, locally, which matters because shadows and backgrounds vary within a window.
- **Redundant.** Each inner cell appears in four blocks with four normalizations. Dalal and Triggs found that this overlap improved the miss rate considerably.
- **Design choices.** The cell size, the bins, the block size and the clip value 0.2 were chosen by experiments on the INRIA data. They are not optimal in general.

## Variants and improvements

- **Normalization schemes.** Section 6.4 compares L2-norm, L2-Hys, L1-norm and L1-sqrt, $\sqrt{x / (\lVert x \rVert_1 + \varepsilon)}$. L2-Hys, L2-norm and L1-sqrt did about equally well, and L1-norm was worse.
- **Signed orientation.** Bins over 0 to 360 degrees keep the sign of the edge. For people it made the results worse, even with twice as many bins, because clothes can be darker or lighter than the background.
- **R-HOG and C-HOG.** The rectangular blocks above are R-HOG. C-HOG uses circular blocks with log-polar cells, similar to the [shape context](/shape-context/).
- **Felzenszwalb HOG.** The [deformable part model](/deformable-part-model/) uses cells of 8 pixels with both signed and unsigned bins and a reduced form of 31 values per cell.
- **Fast HOG.** An [integral image](/integral-image/) per orientation bin gives the sum of any rectangle in $O(1)$ time, which speeds up the search over many window sizes at the cost of the trilinear voting.
- **Texture.** HOG and [local binary patterns](/local-binary-patterns/) are often concatenated for detection.

## When to use it

Use HOG to describe windows of objects with a typical outline, such as people, cars and faces, for a linear classifier or as an input to a part model. It is fast, needs no learning of the features, and works well with a few thousand training examples. For keypoint matching between views, use a descriptor with a keypoint frame such as [SIFT](/sift/). For large detection tasks with many classes, learned network features have replaced HOG; it is still useful when data or compute are scarce.

## Pitfalls

- **Smoothing before the gradient.** Dalal and Triggs found that smoothing hurts: with $\sigma = 2$ the recall at $10^{-4}$ false positives per window fell from 89 percent to 80 percent. The simple $[-1, 0, 1]$ mask worked best; the Sobel mask and larger masks did worse.
- **Unsigned angles.** $\operatorname{atan2}$ gives angles in $(-180°, 180°]$. Fold them into $[0°, 180°)$, and treat the bins as a circle, or angles near 0 and 180 go to different ends.
- **Bin centers.** Centers at $(b + \frac12)\,20°$ and centers at $b \cdot 20°$ are both used in libraries. They give different descriptors.
- **Block order.** Libraries differ in the order of cells inside a block and of blocks inside the window. A trained SVM only works with the order it was trained on.
- **Window margin.** The paper's $64 \times 128$ window has a margin of about 16 pixels around the person. Cutting the margin to 8 pixels made the results worse, so the context counts.
- **The Gaussian block window.** The paper weights each block by a Gaussian. Our code leaves it out, which changes the values but not the structure.

## Implementations

## History

Dalal and Triggs presented HOG at CVPR 2005. Their study tested each step on the new INRIA person data set: gamma and color, gradient masks, the number of bins, the size of cells and blocks, and the normalization. It made the cell-and-block descriptor with a linear SVM the standard pedestrian detector of its time. Earlier work had used edge orientation histograms, shape contexts and SIFT descriptors; HOG differs by its dense grid of overlapping, locally normalized blocks. Felzenszwalb and his coauthors built the deformable part model on HOG features, and HOG stayed a common baseline until learned network features took over around 2012.

## References
