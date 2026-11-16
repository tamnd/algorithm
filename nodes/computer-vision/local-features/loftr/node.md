---
tag: JB95QG
kind: algorithm
slug: loftr
name: LoFTR
aliases:
- detector-free local feature matching
area: computer-vision/local-features
level: research
summary: Match two images without a detector, by transformer attention over coarse feature maps followed by a refinement of each match at a fine level.
solves: [feature-matching]
model: real-ram
complexity:
  vars: {M: the number of coarse cells of image A, N: the number of coarse cells of image B, d: the feature length, K: the number of coarse matches, w: the window size}
  time: {worst: O(M N d + K w^2 d), average: O(M N d + K w^2 d), best: O(M N d + K w^2 d)}
  space: {extra: O(M N + w^2)}
properties: {deterministic: true, learned: true, detector_free: true, subpixel: true, symmetric_coarse_matches: true, network_cost_excluded: true}
history:
  year: 2021
  people: [Jiaming Sun, Zehong Shen, Yuang Wang, Hujun Bao, Xiaowei Zhou]
  note: Sun, Shen, Wang, Bao and Zhou presented LoFTR at CVPR 2021. It matched dense coarse features after linear-attention transformer layers and refined each match in a fine window, with no keypoint detector.
prereqs: [feature-matching, mutual-nearest-neighbor-matching]
see_also: [superglue, superpoint, sift, optical-flow, ransac, relative-pose-problem, homography-estimation, log-sum-exp-trick]
sources:
  - paper: doi:10.1109/CVPR46437.2021.00881
    title: "Jiaming Sun, Zehong Shen, Yuang Wang, Hujun Bao and Xiaowei Zhou, LoFTR, detector-free local feature matching with transformers, IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2021 (arXiv 2104.00680)"
    locator: "Section 3.2 (the LoFTR module, positional encoding and linear attention), Section 3.3 (the score matrix, the dual-softmax and the match selection with a threshold and mutual nearest neighbors), Section 3.4 (the coarse-to-fine module), Section 3.5 (the losses), Section 3.6 (the implementation details), Section 4 (the experiments)"
  - paper: doi:10.1109/CVPR42600.2020.00499
    title: "Paul-Edouard Sarlin, Daniel DeTone, Tomasz Malisiewicz and Andrew Rabinovich, SuperGlue, learning feature matching with graph neural networks, IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2020 (arXiv 1911.11763)"
    locator: "Section 3.2, the optimal transport layer that LoFTR offers as an alternative to the dual-softmax"
---

LoFTR matches two images without a keypoint detector. A convolutional network computes a coarse feature map at 1/8 of the image size and a fine map at 1/2. Transformer layers with self-attention and cross-attention then mix the coarse features of both images. Each coarse cell of one image is compared with each cell of the other, a softmax over rows and a softmax over columns turn the scores into a confidence matrix, and the mutual best pairs above a threshold are the coarse matches. Each coarse match is then refined to a subpixel position inside a small window of the fine map. This page covers the matching steps, the dual-softmax with the mutual check and the window refinement, with their proof and code; the networks and their training are outside the page, and the quality of the features is a measured result.

## In plain words

Instead of first picking special points, LoFTR cuts each image into small squares of 8 by 8 pixels and gives each square a vector. Before the vectors are compared, a network lets every square look at the other squares of its own image and of the other image, so a square on a plain wall can still learn where it is. Then every square of one image is scored against every square of the other. A square pair is a match when each is the other's favorite and the confidence is high. Last, each match is made more exact: we look at a small patch of a finer map around the matched square and take the weighted center of where the point fits best.

## The problem

The input is the output of the networks:

- the coarse features $f^A_1, \dots, f^A_M$ and $f^B_1, \dots, f^B_N$ in $\mathbb{R}^d$, one per cell of the $1/8$ grids of images A and B, after the transformer layers;
- the fine feature maps of the two images at $1/2$ resolution, after the fine transformer layers;
- a temperature $\tau$, a threshold $\theta$, a window size $w$ and a scale $s$ for the fine correlation.

The output is a list of matches $(x^A, x^B)$, where $x^A$ is the image position of a coarse cell of A and $x^B$ is a subpixel position in B, each with a confidence. Each coarse cell is in at most one match.

## The algorithm

```pseudo id=main
LOFTR-MATCH(f^A, f^B, τ, θ, fine maps, w, s)
L1  S_ij ← ⟨f^A_i, f^B_j⟩ / τ for all cells i of A and j of B
L2  R ← softmax of each row of S;  C ← softmax of each column of S
L3  P_ij ← R_ij · C_ij
L4  M_c ← the pairs (i, j) where j is the best column of row i, i is the best row of column j, and P_ij ≥ θ
L5  for each (i, j) in M_c do
L6      c ← the fine vector of A at cell i;  W ← the w × w fine window of B centered at cell j
L7      q_k ← softmax over the window positions k of s · ⟨c, W_k⟩
L8      output (position of i, Σ_k q_k · position of k, P_ij)
```

Lines L1 to L3 are the dual-softmax of Section 3.3 of the paper. $P_{ij}$ is large only when $j$ is a likely partner of $i$ among all cells of B and $i$ is a likely partner of $j$ among all cells of A, so it is a soft form of [mutual nearest neighbor matching](/mutual-nearest-neighbor-matching/). Line L4 is the match selection of the paper: a threshold $\theta$ and the mutual nearest neighbor criterion on $P$. Ties go to the smaller index. Lines L6 to L8 are the coarse-to-fine module of Section 3.4: the center vector of the window of A is correlated with all vectors of the window of B, a softmax gives a heat map, and the expectation over it is the subpixel position.

The networks before these steps, from Section 3 of the paper: a ResNet-18 backbone with a feature pyramid gives the coarse and the fine maps. The coarse maps are flattened, a 2D positional encoding is added, and $N_c$ layers alternate self-attention and cross-attention. The attention is linear attention, with the kernel $\varphi(x) = \mathrm{elu}(x) + 1$, so its cost is linear in the number of cells instead of quadratic. A smaller module with $N_f$ layers transforms the cropped fine windows. Training uses the negative log-likelihood of $P$ at the ground-truth coarse matches and an $\ell_2$ loss on the refined positions weighted by the inverse variance of the heat map. Instead of the dual-softmax, the paper also allows the optimal transport layer of [SuperGlue](/superglue/) with $-S$ as the cost.

## Example

Coarse matching. Let A have two cells with $f^A_0 = (1, 0)$ and $f^A_1 = (0, 1)$, and B three cells with $f^B_0 = (1, 0)$, $f^B_1 = (0.6, 0.8)$ and $f^B_2 = (0, 1)$. With $\tau = 0.5$, line L1 gives

$$S = \begin{pmatrix} 2 & 1.2 & 0 \\ 0 & 1.6 & 2 \end{pmatrix}.$$

The row softmax is $R = \begin{pmatrix} 0.631 & 0.2835 & 0.0854 \\ 0.075 & 0.3712 & 0.5538 \end{pmatrix}$, and the column softmax gives $(0.8808, 0.1192)$, $(0.4013, 0.5987)$ and $(0.1192, 0.8808)$ for the three columns. Their product is

$$P = \begin{pmatrix} 0.5558 & 0.1138 & 0.0102 \\ 0.0089 & 0.2223 & 0.4878 \end{pmatrix}.$$

With $\theta = 0.2$, line L4 keeps $(0, 0)$ with 0.5558 and $(1, 2)$ with 0.4878. The pair $(1, 1)$ has $P_{11} = 0.2223$, above the threshold, but row 1 prefers column 2, so the mutual check removes it. Cell 1 of B, which lies between the two directions, gets no match.

Refinement. Take a $3 \times 3$ window with scale $s = 1$, where the score $s \langle c, W_k \rangle$ is 1 at the center, 2 one fine pixel to the right, and 0 at the other seven positions. The softmax gives 0.4319 to the right position, 0.1589 to the center and 0.0585 to each of the others. The expected horizontal offset is $0.4319 + 2 \times 0.0585 - 3 \times 0.0585 = 0.3735$ fine pixels, and the vertical offset is 0 by symmetry. At stride 2 this moves the match 0.747 image pixels to the right of the cell of B.

## Correctness

The matching steps have a proof; the networks do not. The proof in `proofs/correctness.md` shows:

- **Bounds.** Each $P_{ij}$ is in $(0, 1]$, at most both of its softmax factors, and each row and column of $P$ sums to at most 1.
- **One half.** If $P_{ij} > 1/2$, it is the unique largest value of its row and of its column. So with $\theta > 1/2$ the mutual check removes nothing.
- **Invariance and symmetry.** A constant added to all scores does not change $P$, and swapping the images transposes $P$ and gives the same coarse matches.
- **A matching.** Each coarse cell is in at most one coarse match.
- **Refinement.** The refined position is a convex combination of the window positions. If one position leads the others by $\Delta$ in score, the result is within $(w^2 - 1) e^{-\Delta} (w - 1)\sqrt{2}$ fine pixels of it.

What this does not show is that the features are good. The paper measures it (2021): the AUC of the corner error for homography estimation on HPatches, the AUC of the pose error on ScanNet for indoor pairs and on MegaDepth for outdoor pairs, and visual localization on InLoc and Aachen Day-Night. In these tests it did better than detector-based methods such as [SuperPoint](/superpoint/) with SuperGlue, and it found matches in regions with little texture, where a detector finds few points. These are benchmark results with the protocol of the paper.

## Complexity

The model is the real RAM, and the cost of the networks is outside the page. Line L1 computes $M N$ dot products of length $d$, $O(M N d)$. Lines L2 to L4 take $O(M N)$. For each of the $K$ coarse matches, lines L6 to L8 compute $w^2$ dot products, $O(w^2 d)$. The total is $O(M N d + K w^2 d)$ time and $O(M N + w^2)$ space for the score matrix and one window.

The score matrix is the main cost of the matching steps: for two $640 \times 480$ images the coarse grids have $80 \times 60 = 4800$ cells each, so $S$ has about 23 million entries. The paper reports 116 ms for the full model with dual-softmax on a $640 \times 480$ pair on an RTX 2080Ti GPU, and 130 ms with the optimal transport layer and three Sinkhorn iterations; these are measurements of 2021 and include the networks.

## Properties

- **No detector.** Every coarse cell is a candidate, so matches can appear on low-texture surfaces where a detector finds no repeatable points.
- **One match per coarse cell.** The mutual check makes the coarse matches a partial matching of cells. The density of matches is at most one per $8 \times 8$ block.
- **Subpixel in B, cell-centered in A.** The position in A is the center of the coarse cell at fine resolution; only the position in B is refined.
- **Symmetric at the coarse level.** The coarse matches do not depend on which image is called A. The refinement is not symmetric.
- **Learned.** The features depend on the training data. The paper trains separate models for indoor and outdoor scenes.

## Variants and improvements

- **Optimal transport instead of dual-softmax.** The paper allows the Sinkhorn layer of [SuperGlue](/superglue/) with a dustbin, at a small extra cost.
- **Later dense matchers.** Methods such as QuadTree attention, ASpanFormer and the efficient LoFTR variants keep the coarse-to-fine design and change the attention or the refinement.
- **Detector-based matching.** [SuperPoint](/superpoint/) with [SuperGlue](/superglue/), or [SIFT](/sift/) with the [ratio test](/lowe-ratio-test/), matches only detected points.
- **Dense flow.** [Optical flow](/optical-flow/) methods give a vector for every pixel, but they usually assume small motion between the frames; LoFTR targets wide-baseline pairs.

## When to use it

Use LoFTR for wide-baseline image pairs with little texture, such as indoor walls and floors, when a GPU is available and you need a [relative pose](/relative-pose-problem/) or a [homography](/homography-estimation/) after [RANSAC](/ransac/). Use a detector and descriptor, such as [SIFT](/sift/) or SuperPoint, when you need matches across many images, because a detector gives the same points in every image, while LoFTR finds new cells for each pair, which makes tracks across many views harder to build.

## Pitfalls

- **Memory.** The score matrix has $M N$ entries. Large images need downsampling or a cap on the number of cells.
- **Threshold and temperature.** $\theta = 0.2$ in the paper and the temperature $\tau$ are tuned values. The text of the paper does not give a number for $\tau$; take it from the trained model you use.
- **Grid alignment.** The image position of a coarse cell and the window position in the fine map depend on the strides and on a convention for the cell center. The coarse and the fine maps must use the same one.
- **Border windows.** A window near the image border is partly outside the map. Leave those positions out of the softmax, or pad, but do it the same way as in training.
- **Not a keypoint set.** Matches of one image pair do not chain into tracks over many images as detected points do.
- **Low resolution.** A coarse match is at most one per $8 \times 8$ cell, so two nearby true matches inside one cell give one result.

## Implementations

The networks are outside this page. The Python code in `impl/python/loftr.py` implements only the matching steps of lines L1 to L8 on given coarse features and fine maps: the score matrix, the dual-softmax, the mutual check with a threshold, and the window refinement by a softmax and an expectation. The coarse cell $i$ of a grid of width $W_c$ is placed at pixel $(8 (i \bmod W_c), 8 \lfloor i / W_c \rfloor)$, and window positions outside the fine map are left out; both are conventions of this code. The tests check the dual-softmax against its formula, the mutual check against a brute-force definition with ties, the one-half lemma, shift invariance and symmetry, that the refined position stays in the window and near a clear peak, and that a shuffled grid of features is matched back to the right cells.

## History

Dense matching of learned features goes back to neighborhood consensus networks (Rocco and others, 2018), which scored all pairs of cells with 4D convolutions. [SuperGlue](/superglue/) (2020) brought attention between and within two sets of detected points. Sun, Shen, Wang, Bao and Zhou (2021) applied the same attention to all coarse cells, made it affordable with linear attention, and added a coarse-to-fine step, so the matcher no longer depends on a detector. Several later dense and semi-dense matchers follow the same coarse-to-fine design.

## References
