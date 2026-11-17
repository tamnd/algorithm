---
tag: QX9B5V
kind: algorithm
slug: spatial-pyramid-matching
name: Spatial pyramid matching
aliases:
- spatial pyramid kernel
area: computer-vision/segmentation-and-recognition
level: advanced
summary: "Compare images by histograms of visual words over grids of finer and finer cells, combined by a weighted histogram intersection kernel."
solves: [object-recognition]
model: real-ram
complexity:
  vars: {n: the total number of features of the two images, L: the finest pyramid level, M: the number of visual words}
  time: {sparse: O(n L), dense: O(M 4^L)}
  space: {extra: O(n L)}
properties: {deterministic: true, exact: true, positive_semidefinite: true, symmetric: true}
history:
  year: 2006
  people: [Svetlana Lazebnik, Cordelia Schmid, Jean Ponce, Kristen Grauman, Trevor Darrell]
  note: "Grauman and Darrell (ICCV 2005) built the pyramid match kernel over a pyramid in feature space. Lazebnik, Schmid and Ponce (CVPR 2006) moved the pyramid to the image plane and kept the visual words as separate channels, which added coarse layout to the bag of words."
prereqs: [bag-of-visual-words]
see_also: [bag-of-visual-words, support-vector-machine, kernel-trick, image-pyramid, fisher-vector, histogram-of-oriented-gradients, object-recognition, vlad]
sources:
  - paper: doi:10.1109/CVPR.2006.68
    title: "Svetlana Lazebnik, Cordelia Schmid and Jean Ponce, Beyond bags of features: spatial pyramid matching for recognizing natural scene categories, CVPR 2006, vol. 2, 2169-2178"
    locator: "Section 3.1 (histogram intersection, Eq. 1, and the pyramid match kernel, Eq. 2 and 3), Section 3.2 (one channel per visual word, Eq. 4, and the concatenated weighted histograms), Section 5 (results on the 15 scene categories and Caltech-101)"
  - paper: doi:10.1109/ICCV.2005.239
    title: "Kristen Grauman and Trevor Darrell, The pyramid match kernel: discriminative classification with sets of image features, ICCV 2005, vol. 2, 1458-1465"
    locator: "The pyramid match kernel over a multi-resolution histogram in feature space, and its proof that it is a Mercer kernel"
  - paper: doi:10.1007/s11263-013-0636-x
    title: "Jorge Sanchez, Florent Perronnin, Thomas Mensink and Jakob Verbeek, Image classification with the Fisher vector: theory and practice, International Journal of Computer Vision 105(3), 2013, 222-245"
    locator: "The use of spatial pyramids with Fisher vectors"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.2, Image classification"
---

Spatial pyramid matching compares two images through their [visual words](/bag-of-visual-words/) and the rough places where those words occur. It cuts the image into a $1 \times 1$, $2 \times 2$, $4 \times 4$, ... grid of cells, counts the words in each cell, and adds up the histogram intersections of the levels with weights that favor matches in small cells. The result is a positive semidefinite kernel, used mostly with a [support vector machine](/support-vector-machine/) for scene and object classification. It is a classification method, not an [image retrieval](/image-retrieval/) method, and its level 0 is the plain bag of words.

## In plain words

A bag of words forgets where things are in the picture. A beach photo has sky at the top and sand at the bottom, and the bag of words cannot see that.

Spatial pyramid matching counts the words again in each half, each quarter and so on, of the image. Two photos get points when they have the same word in the whole image, more points when the word also appears in the same quarter, and still more when it appears in the same small cell. Points for a match are given once, at the finest level where it is found. The total is a similarity that a classifier can use directly.

## The problem

**Input.** Two images of size $W \times H$ (columns by rows), each given as a set of features $(u, v, m)$: a position with $0 \le u \le W$ and $0 \le v \le H$ ($u$ the column, $v$ the row, origin at the top left), and a visual word $m \in \{0, \ldots, M - 1\}$. The finest level $L \ge 0$.

**Cells.** Level $l \in \{0, \ldots, L\}$ cuts the image into $2^l \times 2^l$ equal cells. A feature at $(u, v)$ is in cell
$$\big( \min(\lfloor u\, 2^l / W \rfloor, 2^l - 1),\ \min(\lfloor v\, 2^l / H \rfloor, 2^l - 1) \big).$$
The minimum puts points on the right or bottom edge into the last cell. A *bin* at level $l$ is a pair (cell, word). $H_X^l(b)$ is the number of features of $X$ in bin $b$.

**Output.** With the histogram intersection $I^l = \sum_b \min(H_X^l(b), H_Y^l(b))$ (Lazebnik et al., Eq. 1), the kernel is (Eq. 2)
$$\kappa^L(X, Y) = I^L + \sum_{l=0}^{L-1} \frac{1}{2^{L-l}} \big( I^l - I^{l+1} \big) = \frac{1}{2^L} I^0 + \sum_{l=1}^{L} \frac{1}{2^{L-l+1}} I^l .$$
The second form is Eq. 3. Lazebnik et al. write the kernel for one channel (one word) and add the channels (Eq. 4); taking the word as part of the bin, as here, gives the same sum.

## The algorithm

```pseudo id=main
SPM-KERNEL(X, Y, L, W, H)
L1  for l = 0 to L do
L2      H_X^l ← the counts of X over the bins (cell at level l, word)
L3      H_Y^l ← the counts of Y over the same bins
L4      I^l ← the sum over the bins b of min(H_X^l(b), H_Y^l(b))
L5  kappa ← I^L
L6  for l = 0 to L - 1 do kappa ← kappa + (I^l - I^(l+1)) / 2^(L-l)
L7  return kappa
```

In practice each image is stored once as a single long vector: the histograms of all levels, each multiplied by its weight in Eq. 3, concatenated. The histogram intersection of two such vectors is $\kappa^L$, because $\min(a h, a h') = a \min(h, h')$ for $a > 0$. The vector has $M (1 + 4 + \cdots + 4^L) = M (4^{L+1} - 1)/3$ entries; for $M = 200$ and $L = 2$ this is 4,200, the size Lazebnik et al. give. They also divide each histogram by the number of features of the image, so that images with many features do not get larger values.

## Example

Take a $4 \times 4$ image, two words $a$ and $b$, and $L = 2$.

| | features $(u, v, m)$ |
|---|---|
| $X$ | $(0.5, 0.5, a)$, $(1.5, 0.5, a)$, $(3.5, 3.5, b)$, $(2.5, 0.5, b)$ |
| $Y$ | $(0.5, 1.5, a)$, $(3.5, 0.5, a)$, $(3.5, 2.5, b)$, $(0.5, 3.5, b)$ |

- Level 0, one cell. Both images have two $a$ and two $b$, so $I^0 = 2 + 2 = 4$. The bag of words sees two equal images.
- Level 1, cells of size 2. $X$ has $a$ twice in cell $(0, 0)$, $b$ in $(1, 1)$ and $b$ in $(1, 0)$. $Y$ has $a$ in $(0, 0)$, $a$ in $(1, 0)$, $b$ in $(1, 1)$ and $b$ in $(0, 1)$. The common bins are $((0, 0), a)$ with $\min(2, 1) = 1$ and $((1, 1), b)$ with 1, so $I^1 = 2$.
- Level 2, cells of size 1. No bin is shared, so $I^2 = 0$.

By Eq. 2, $\kappa^2 = 0 + \frac12 (2 - 0) + \frac14 (4 - 2) = 1.5$. By Eq. 3, $\frac14 \cdot 4 + \frac14 \cdot 2 + \frac12 \cdot 0 = 1.5$. Two matches are new at level 1 and count $1/2$ each, and two are new at level 0 and count $1/4$ each. For comparison, $\kappa^2(X, X) = 4$, so the layout costs more than half of the similarity. With the histograms divided by the 4 features, the kernel is $1.5/4 = 0.375$. With $L = 1$ instead, $\kappa^1 = 2 + \frac12(4 - 2) = 3$.

## Correctness

The proof in the correctness file shows four facts. First, Eq. 2 and Eq. 3 are equal, by collecting the coefficient of each $I^l$. Second, $I^l \ge I^{l+1}$: each bin at level $l$ is the union of four bins at level $l + 1$ with the same word, and $\min(a_1 + \cdots + a_4, b_1 + \cdots + b_4) \ge \sum_j \min(a_j, b_j)$; so $I^l - I^{l+1} \ge 0$ is the number of matches that are new at level $l$, and each new match has a nonnegative weight. Third, $I^l$ is the size of a largest one-to-one matching between $X$ and $Y$ that pairs only features with the same word in the same level-$l$ cell; the tests compare it with a matching by augmenting paths. Fourth, $\kappa^L$ is a positive semidefinite kernel, because $\min(a, b) = \int_0^\infty [t < a][t < b]\, dt$ for $a, b \ge 0$ makes each intersection an inner product, and a sum of such kernels with nonnegative weights is again one. Grauman and Darrell (2005) prove the same for their pyramid match.

## Complexity

In the [real RAM](/real-ram/) with a hash table or a direct index for the bins, lines L2 and L3 cost $O(n)$ per level for $n$ features in total, and line L4 costs $O(n)$ per level with sparse histograms, since at most $n$ bins are nonzero. The whole kernel costs $O(n (L + 1))$ time and $O(n (L + 1))$ space. With dense vectors of length $M (4^{L+1} - 1)/3$ it costs $O(M 4^L)$. For classification, an SVM needs the kernel between all pairs of $N$ training images, so the Gram matrix costs $O(N^2)$ kernel evaluations. This cost is the main limit of the method at scale.

The cell index needs one multiplication and one floor per level and coordinate. Quantizing the descriptors to words, which comes before this algorithm, costs $O(n M D)$ with a linear scan over $M$ centers of dimension $D$.

## Properties

- **Exact on integers.** The weights are powers of $1/2$ and the counts are integers, so the kernel is a dyadic rational. The code uses exact fractions.
- **Symmetric and positive semidefinite.** So it is a valid SVM kernel. The tests check the Gram matrices of random sets with exact elimination.
- **$\kappa^L(X, X) = |X|$** without normalization, and 1 with it. The kernel is largest for identical images when the counts are equal.
- **Level 0 is the bag of words.** $\kappa^0$ is the histogram intersection of the word histograms.
- **Not translation invariant.** The grid is fixed to the image frame. An object that moves by half a cell can change the counts of every finer level. This is wanted for scenes, whose layout is fairly stable, and a weakness for objects at random positions.
- **The weights are a design choice.** The weight $1/2^{L-l}$ of a new match at level $l$ follows the pyramid match of Grauman and Darrell. It is a heuristic, not derived from a model of the data.

## Variants and improvements

- **Pyramid match kernel** (Grauman and Darrell 2005). The pyramid is over the descriptor space, with bins that double in width, and there is no image layout. Spatial pyramid matching is the same weighting with the image plane as the space and the words as channels.
- **Other features per cell.** Any per-cell vector can be pooled in the pyramid, for example [HOG](/histogram-of-oriented-gradients/) like gradient features, [Fisher vectors](/fisher-vector/) or [VLAD](/vlad/). With such vectors the cells are usually concatenated and compared with a linear kernel.
- **Other pyramids.** A $1 \times 3$ level of horizontal bands is common for scenes, since sky, objects and ground lie in bands.
- **Max pooling and sparse coding.** Later work replaces the counts by the maximum of soft assignments or of sparse codes over each cell and uses a linear SVM.
- **Explicit feature maps.** The intersection kernel can be approximated by a finite-dimensional feature map, so that a linear SVM can be trained on large data.

## When to use it

Use the spatial pyramid for whole-image classification, especially of scenes, where the layout of a category is stable: sky above, ground below. For object instances at arbitrary positions and scales it helps less, and [spatial verification](/spatial-verification/) is a better way to use geometry. As a classical pipeline (dense SIFT, words, a pyramid, an SVM) it is a strong baseline. Convolutional networks later replaced it on most benchmarks.

## Pitfalls

- **Points on the far edge.** Without the minimum in the cell index, a point with $u = W$ falls into a cell that does not exist.
- **Different image sizes.** Use the size of each image for its own cells. The pyramid then compares relative positions, which assumes that the two images frame the scene in a similar way.
- **Forgetting the normalization** by the number of features. Without it, images with many features get large kernel values with every other image.
- **Counting a match twice.** Eq. 2 counts each match once, at its finest level. If the weights $1/2^{L-l}$ of Eq. 2 are put on the $I^l$ themselves instead of on the differences, a match found at level $L$ is counted again at every coarser level.
- **Too many levels.** At fine levels the cells hold few features and the intersections are almost zero; they add noise and cost. Lazebnik et al. found little gain beyond $L = 2$ on their data, which is a benchmark observation.

## Implementations

The Python code builds sparse histograms per level, computes the level intersections and the kernel by Eq. 2 and by Eq. 3, and builds the concatenated weighted vector, all with exact fractions. The tests check the example of this page, the cell rule at the far edge, the agreement of the three forms on random sets, the equality of each $I^l$ with a maximum matching found by augmenting paths, the decrease of $I^l$ with the level, the self kernel, level 0 as the bag of words, and the positive semidefiniteness of Gram matrices by exact elimination.

## History

Grauman and Darrell (2005) proposed the pyramid match kernel, an approximate optimal matching of two sets of feature vectors through histograms with bins that double in size. Lazebnik, Schmid and Ponce (2006) applied the same idea to the image plane, with one channel per visual word. On the 15 scene categories data set with $M = 200$ words, they report a mean recognition rate of 72.2 percent for the bag of words ($L = 0$) and 81.1 percent for the pyramid with $L = 2$, and 64.6 percent on Caltech-101 with 30 training images per class (Section 5). These are benchmark results for their features and training splits. The spatial pyramid then became a standard part of image classification systems, including those built on Fisher vectors and sparse codes.

## References
