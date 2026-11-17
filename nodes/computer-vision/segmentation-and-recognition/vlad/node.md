---
tag: D9847P
kind: algorithm
slug: vlad
name: VLAD
aliases:
- vector of locally aggregated descriptors
area: computer-vision/segmentation-and-recognition
level: advanced
summary: "Represent an image by summing, for each visual word, the residuals of the descriptors assigned to it, then normalizing the concatenated vector."
solves: [image-retrieval]
model: real-ram
complexity:
  vars: {n: the number of local descriptors of the image, K: the number of centers, D: the descriptor dimension}
  time: {worst: O(n K D), best: O(n K D)}
  space: {extra: O(K D)}
properties: {deterministic: true, exact: true, order_invariant: true, output_size: K D}
history:
  year: 2010
  people: [Herve Jegou, Matthijs Douze, Cordelia Schmid, Patrick Perez]
  note: "Jegou, Douze, Schmid and Perez (CVPR 2010) proposed VLAD for compact image search. The journal version (TPAMI 2012, with Perronnin and Sanchez) adds power normalization and the link to the Fisher vector. Arandjelovic and Zisserman (2013) added intra-normalization, and NetVLAD (2016) made the assignment soft and trainable."
prereqs: [bag-of-visual-words, k-means]
see_also: [fisher-vector, bag-of-visual-words, image-retrieval, product-quantization, principal-component-analysis, rootsift, visual-place-recognition, vocabulary-tree]
sources:
  - paper: doi:10.1109/CVPR.2010.5540039
    title: "Herve Jegou, Matthijs Douze, Cordelia Schmid and Patrick Perez, Aggregating local descriptors into a compact image representation, CVPR 2010, 3304-3311"
    locator: "The definition of VLAD as the sum of the residuals to the nearest center, followed by L2 normalization, and its use with compact codes"
  - paper: doi:10.1109/TPAMI.2011.235
    title: "Herve Jegou, Florent Perronnin, Matthijs Douze, Jorge Sanchez, Patrick Perez and Cordelia Schmid, Aggregating local image descriptors into compact codes, IEEE Transactions on Pattern Analysis and Machine Intelligence 34(9), 2012, 1704-1716"
    locator: "The VLAD descriptor, its power-law normalization, and VLAD as a simplified Fisher vector"
  - paper: doi:10.1109/CVPR.2013.207
    title: "Relja Arandjelovic and Andrew Zisserman, All about VLAD, CVPR 2013, 1578-1585"
    locator: "Intra-normalization of each residual block against bursty features"
  - paper: doi:10.1007/s11263-013-0636-x
    title: "Jorge Sanchez, Florent Perronnin, Thomas Mensink and Jakob Verbeek, Image classification with the Fisher vector: theory and practice, International Journal of Computer Vision 105(3), 2013, 222-245"
    locator: "Section 2.5, Relationship with other methods (VLAD as a Fisher vector with hard assignment and only the gradient with respect to the means)"
  - paper: doi:10.1109/CVPR.2016.572
    title: "Relja Arandjelovic, Petr Gronat, Akihiko Torii, Tomas Pajdla and Josef Sivic, NetVLAD: CNN architecture for weakly supervised place recognition, CVPR 2016, 5297-5307"
    locator: "The NetVLAD layer: soft assignment with trainable centers, intra-normalization and L2 normalization (arXiv 1511.07247)"
---

VLAD (vector of locally aggregated descriptors) turns the set of local descriptors of an image into one vector of fixed length. Each descriptor is assigned to its nearest center of a small codebook, as in the [bag of visual words](/bag-of-visual-words/), but instead of counting, VLAD adds up the residuals $x - c_k$, the vectors from the center to the descriptors. The $K$ sums of dimension $D$ are concatenated and normalized, so two images can be compared by one inner product. VLAD is a simplified [Fisher vector](/fisher-vector/): hard assignment and the first-order statistics only.

## In plain words

Pick a small set of typical patch descriptors, the centers. For each patch of an image, find its closest center and write down the difference between the patch and that center. Add up the differences that belong to the same center. The result is one short list of numbers for each center, and together these lists describe the image.

A count only says how many patches are near a center. The sum of differences also says in which direction they lie from it. So a few dozen centers already give a detailed description, and the whole image fits in one vector that a computer can compare fast and compress.

## The problem

**Input.** A codebook $C = (c_1, \ldots, c_K)$ of $K$ centers in $\mathbb{R}^D$, usually from [k-means](/k-means/) on training descriptors, and the $n$ local descriptors $X = \{x_1, \ldots, x_n\} \subset \mathbb{R}^D$ of one image (for example SIFT with $D = 128$, or [RootSIFT](/rootsift/)). Optional parameters: the power $\alpha \in (0, 1]$ and a flag for intra-normalization.

**Output.** A vector $z \in \mathbb{R}^{K D}$. The nearest center is $\mathrm{NN}(x) = \arg\min_k \lVert x - c_k \rVert_2$ with ties to the smaller index. Before normalization, block $k$ of $z$ is
$$v_k = \sum_{x \in X,\ \mathrm{NN}(x) = k} (x - c_k).$$
Images are compared by $\langle z_q, z_d \rangle$, or by the Euclidean distance, which gives the same ranking for unit vectors.

## The algorithm

```pseudo id=main
VLAD(X, C, alpha, intra)                  ▷ K = |C|, each c_k in R^D
L1  v_k ← 0 in R^D for k = 1..K
L2  for each descriptor x in X do
L3      k ← index of the nearest center to x, ties to the smaller index
L4      v_k ← v_k + (x - c_k)
L5  if intra then v_k ← v_k / ||v_k|| for each k with v_k ≠ 0
L6  z ← (v_1, ..., v_K), the concatenation of the blocks
L7  if alpha < 1 then z_i ← sign(z_i) |z_i|^alpha for each i
L8  if z ≠ 0 then z ← z / ||z||
L9  return z
```

Lines L1 to L4 are the aggregation of Jegou et al. (2010). Line L7 is the power normalization of the journal version, with $\alpha = 0.5$ as the usual choice (the signed square root). Line L5 is the intra-normalization of Arandjelovic and Zisserman (2013), which they use against bursty features. Line L8 is always applied.

## Example

Take $D = 2$, $K = 2$, $c_1 = (0, 0)$, $c_2 = (4, 0)$, and five descriptors $(1, 1)$, $(-1, 2)$, $(3, 1)$, $(5, -1)$, $(6, 0)$.

| $x$ | squared distance to $c_1$, $c_2$ | cell | residual |
|---|---|---|---|
| $(1, 1)$ | 2, 10 | 1 | $(1, 1)$ |
| $(-1, 2)$ | 5, 29 | 1 | $(-1, 2)$ |
| $(3, 1)$ | 10, 2 | 2 | $(-1, 1)$ |
| $(5, -1)$ | 26, 2 | 2 | $(1, -1)$ |
| $(6, 0)$ | 36, 4 | 2 | $(2, 0)$ |

The blocks are $v_1 = (0, 3)$ and $v_2 = (2, 0)$, so $z = (0, 3, 2, 0)$ before line L8, and $z = (0, 3, 2, 0)/\sqrt{13} = (0, 0.8321, 0.5547, 0)$ after it. With $\alpha = 0.5$, line L7 gives $(0, \sqrt 3, \sqrt 2, 0)$ and line L8 gives $(0, 0.7746, 0.6325, 0)$. With intra-normalization, line L5 gives $v_1 = (0, 1)$ and $v_2 = (1, 0)$, and the result is $(0, 0.7071, 0.7071, 0)$: both cells now weigh the same, whatever their counts.

The residuals $(-1, 1)$ and $(1, -1)$ in cell 2 cancel. Two descriptors on opposite sides of a center leave no trace in its block. The tests check all these numbers.

## Correctness

The proof in the correctness file shows four facts. First, each descriptor adds its residual to exactly one block in line L4, so the result does not depend on the order of $X$, and $v_k = n_k (\bar x_k - c_k)$, where $n_k$ is the number of descriptors in cell $k$ and $\bar x_k$ is their mean. Second, for two images without normalization,
$$\langle v(X), v(Y) \rangle = \sum_{k=1}^{K} \sum_{x \in X_k} \sum_{y \in Y_k} \langle x - c_k, y - c_k \rangle,$$
so VLAD is the explicit feature map of a match kernel that compares only descriptors in the same cell, and the inner product costs $O(K D)$ instead of $O(n m D)$ for $m$ descriptors in the second image. Third, this kernel is positive semidefinite, since it is an inner product of feature vectors. Fourth, if a [Fisher vector](/fisher-vector/) uses a mixture with weights $w_k = 1/K$, unit variances, means $c_k$ and hard assignment, its gradient with respect to the means is $(\sqrt{K}/n)\, v$, so after L2 normalization the two vectors are equal (Sanchez et al. 2013, Section 2.5).

## Complexity

In the [real RAM](/real-ram/), line L3 costs $O(K D)$ with a linear scan over the centers, so lines L2 to L4 cost $O(n K D)$. Lines L5 to L8 cost $O(K D)$. Extra space is the $K D$ entries of the output. With an approximate nearest center search (a [k-d tree](/kd-tree/) or a [randomized k-d forest](/randomized-kd-forest/)), line L3 costs less, but then the assignment is approximate.

The output size is fixed: $K = 64$ centers and SIFT with $D = 128$ give 8,192 values, whatever $n$ is. Comparing two images costs $O(K D)$. For large collections the vector is reduced with [principal component analysis](/principal-component-analysis/) and coded with [product quantization](/product-quantization/), so that one image takes a few dozen bytes.

## Properties

- **Order invariant and additive.** The unnormalized blocks of $X \cup Y$ (disjoint sets) are the sums of the blocks of $X$ and of $Y$. This is useful when descriptors arrive in batches, for example over the frames of a video.
- **Dense.** Almost every entry is nonzero, unlike the sparse [bag of words](/bag-of-visual-words/) histogram. An inverted file does not help, and search is [nearest neighbor search](/nearest-neighbor-search/) on dense vectors.
- **First order only.** VLAD keeps the offset of the cell mean from the center, weighted by the count. It does not keep the spread of the cell (the Fisher vector keeps a second order term for that), and it keeps the count only through the length of the offset.
- **Not invariant to the codebook.** A different k-means run gives different centers and a different vector space. Vectors made with different codebooks cannot be compared.
- **Exact.** The code computes the definition exactly up to floating point rounding; the tests compare it with a direct evaluation of the match kernel.

## Variants and improvements

- **Power normalization** (Jegou et al. 2012). Line L7 with $\alpha = 0.5$ reduces the weight of large components, which come from many similar descriptors (bursts such as repeated windows on a facade).
- **Intra-normalization** (Arandjelovic and Zisserman 2013). Line L5 makes each cell contribute a unit vector, so one bursty cell cannot dominate. They also adapt the centers to a new data set without recomputing the whole vocabulary, and pool VLADs over several regions of the image.
- **Soft assignment.** Each descriptor adds weighted residuals to several near centers. NetVLAD (Arandjelovic et al. 2016) uses a softmax of $w_k^\top x + b_k$ with trainable $w_k$, $b_k$ and $c_k$ on top of a convolutional network, and is trained for [place recognition](/visual-place-recognition/). The network is outside this page.
- **Fisher vector.** Soft assignment by a Gaussian mixture, with gradients for the means and the variances, gives the [Fisher vector](/fisher-vector/).
- **Residual normalization.** Some systems scale each residual $x - c_k$ to unit length before line L4, so that each descriptor counts equally.

## When to use it

Use VLAD when each image must be one vector of fixed size: for search in very large collections with compressed codes, for place recognition, or as input to a linear classifier. It needs only a small codebook (tens to hundreds of centers), so training is cheap. For the best accuracy with a few hundred thousand images, a [bag of words](/bag-of-visual-words/) with a large vocabulary and [spatial verification](/spatial-verification/) can rank better, because VLAD keeps no geometry. Today, VLAD on learned features (NetVLAD) is common for place recognition.

## Pitfalls

- **Forgetting the normalization.** Without line L8, images with more descriptors get longer vectors and higher scores. Without line L7 or L5, bursts dominate. These steps are not optional details: they change the ranking.
- **Cancellation.** Residuals on opposite sides of a center cancel, as in the example. A cell with many descriptors can have a short block. This is part of the method, but it means that the length of $v_k$ is not a count.
- **Empty cells.** An image with no descriptor in cell $k$ has $v_k = 0$. Intra-normalization must skip such blocks, or it divides by zero.
- **Codebook from other data.** Centers learned on one kind of image fit another kind poorly, and the residuals become large and similar for all images. Adapt the centers or learn them on similar data.
- **Signs of the power step.** Line L7 must keep the sign. Taking $|z_i|^\alpha$ alone loses half of the information.

## Implementations

The Python code computes the blocks, the optional intra-normalization, the signed power and the final L2 normalization, with a linear scan for the nearest center and the tie rule of this page. It also has a direct match-kernel function for the tests. The tests check the example of this page, the cancellation, the invariance to the order of the descriptors, the identity $v_k = n_k(\bar x_k - c_k)$, the equality of the inner product with the match kernel on random sets, and the equality with the hard-assignment Fisher vector mean gradient after normalization.

## History

Jegou, Douze, Schmid and Perez introduced VLAD at CVPR 2010 as a compact alternative to the bag of words, to be combined with dimension reduction and product quantization for search in collections of millions of images. The 2012 journal version with Perronnin and Sanchez adds power normalization, compares VLAD with the Fisher vector of Perronnin and Dance (2007), and shows that VLAD is a simplified Fisher vector. Arandjelovic and Zisserman (2013) proposed intra-normalization and vocabulary adaptation. Arandjelovic et al. (2016) made VLAD a trainable layer, NetVLAD, for place recognition.

## References
