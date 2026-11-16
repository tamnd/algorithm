---
tag: QBGQCK
kind: algorithm
slug: superglue
name: SuperGlue
aliases:
- graph neural network feature matching
area: computer-vision/local-features
level: research
summary: Match two sets of keypoints with attention between and within the sets, then solve a partial assignment with a dustbin by Sinkhorn iterations.
solves: [feature-matching]
model: real-ram
complexity:
  vars: {M: the number of keypoints in image A, N: the number of keypoints in image B, T: the number of Sinkhorn iterations}
  time: {worst: O(T M N), average: O(T M N), best: O(T M N)}
  space: {extra: O(M N)}
properties: {deterministic: true, learned: true, partial_assignment: true, symmetric: true, network_cost_excluded: true}
history:
  year: 2020
  people: [Paul-Edouard Sarlin, Daniel DeTone, Tomasz Malisiewicz, Andrew Rabinovich]
  note: Sarlin, DeTone, Malisiewicz and Rabinovich presented SuperGlue at CVPR 2020. It replaced the hand-made filters of nearest neighbor matching by attention and an entropic optimal transport layer with a dustbin.
prereqs: [feature-matching, assignment-problem, log-sum-exp-trick]
see_also: [superpoint, loftr, mutual-nearest-neighbor-matching, lowe-ratio-test, maximum-weight-matching, hungarian-algorithm, ransac, relative-pose-problem]
sources:
  - paper: doi:10.1109/CVPR42600.2020.00499
    title: "Paul-Edouard Sarlin, Daniel DeTone, Tomasz Malisiewicz and Andrew Rabinovich, SuperGlue, learning feature matching with graph neural networks, IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2020 (arXiv 1911.11763)"
    locator: "Section 3.1 (the keypoint encoder and the attentional graph neural network), Section 3.2 (the score matrix, the dustbin, the marginals and the Sinkhorn iterations), Section 3.3 (the loss), Section 4 (the implementation details)"
  - paper: "Richard Sinkhorn and Paul Knopp, Concerning nonnegative matrices and doubly stochastic matrices, Pacific Journal of Mathematics 21(2), 1967"
    locator: "pages 343-348, the convergence of alternating row and column scaling"
  - paper: "Marco Cuturi, Sinkhorn distances, lightspeed computation of optimal transport, Advances in Neural Information Processing Systems 26 (NIPS), 2013"
    locator: "pages 2292-2300, entropic regularization of optimal transport and its solution by Sinkhorn iterations"
  - paper: doi:10.1109/CVPRW.2018.00060
    title: "Daniel DeTone, Tomasz Malisiewicz and Andrew Rabinovich, SuperPoint, self-supervised interest point detection and description, IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW), 2018"
    locator: the keypoints and descriptors that SuperGlue takes as input in most of its experiments
---

SuperGlue is a learned matcher for two sets of keypoints. A graph neural network takes the positions, scores and descriptors of the keypoints of both images, mixes them with attention inside each image and across the two images, and gives a score $S_{ij}$ for each pair. An optimal matching layer then adds a "dustbin" row and column for points without a partner, and turns the scores into a soft partial assignment with Sinkhorn iterations. Pairs that are mutual best choices with a high enough value are the matches. This page covers the optimal matching layer, with its proof and code; the network and its training are outside the page, and the quality of its scores is a measured result.

## In plain words

Each image has its own keypoints. A network looks at all of them together and gives each pair, one point from each image, a score that says how well they fit. Some points have no partner, because they are hidden or out of view in the other image. So we add an extra "nobody" slot on each side with a fixed score. Then we spread one unit of match per point over the partners and the "nobody" slot, and adjust the spread again and again until each point gives out exactly one unit and each slot takes exactly what it should. A pair is a match when each point puts most of its unit on the other, and the amount is above a threshold.

## The problem

The input is the output of the network:

- a score matrix $S$ with $M$ rows, the keypoints of image A, and $N$ columns, the keypoints of image B;
- the dustbin score $z$, a single learned number;
- the number of iterations $T$ and a match threshold $\theta$.

The output is a soft assignment $P$ of size $(M + 1) \times (N + 1)$ and a list of matches $(i, j)$ with $i < M$ and $j < N$, where each $i$ and each $j$ appears at most once.

The soft assignment solves an entropic optimal transport problem. Row $i < M$ of $P$ must sum to 1 (keypoint $i$ is matched once, maybe to the dustbin), and the dustbin row must sum to $N$ (it can take all points of B); the same holds for columns with the dustbin column summing to $M$. Among these plans, $P$ maximizes $\langle \bar S, P \rangle + H(P)$, where $\bar S$ is $S$ with the dustbin row and column added and $H$ is an entropy term.

## The algorithm

```pseudo id=main
SUPERGLUE-MATCHING-LAYER(S, z, T, θ)
L1  S̄ ← S with a column and then a row of value z added at the end     ▷ (M + 1) × (N + 1)
L2  a ← (1, …, 1, N) of length M + 1;  b ← (1, …, 1, M) of length N + 1
L3  u ← 0;  v ← 0
L4  repeat T times
L5      for each row i: u_i ← log a_i - log Σ_j exp(S̄_ij + v_j)
L6      for each column j: v_j ← log b_j - log Σ_i exp(S̄_ij + u_i)
L7  P_ij ← exp(S̄_ij + u_i + v_j) for all i, j
L8  for each real row i, c(i) ← the real column with the largest P_ij; for each real column j, r(j) ← the real row with the largest P_ij
L9  return P and the pairs (i, c(i)) with r(c(i)) = i and P_{i c(i)} > θ
```

Lines L5 and L6 are the Sinkhorn iterations in the log domain. Each line scales the rows or the columns of $\exp(\bar S)$ so that their sums are right; the log-sum-exp form (see the [log-sum-exp trick](/log-sum-exp-trick/)) keeps large scores from overflowing. Line L8 looks only at the real block, not at the dustbins, as the released code does. Ties go to the smaller index.

The network before this layer, from Section 3.1 of the paper: a keypoint encoder adds an embedding of the position and detection score of each point to its descriptor. Then $L$ layers alternate self-attention, between the points of one image, and cross-attention, between the points of the two images. The final vectors $f^A_i$ and $f^B_j$ give $S_{ij} = \langle f^A_i, f^B_j \rangle$. The dustbin score $z$ is a learned parameter. Training minimizes the negative log of $P$ at the ground-truth matches and at the dustbin entries of the unmatched points (Section 3.3), so the network learns the scale of its own scores.

## Example

Take $M = N = 2$, $S = \begin{pmatrix} 3 & 0 \\ 0 & 0.2 \end{pmatrix}$ and $z = 1$. Line L1 gives

$$\bar S = \begin{pmatrix} 3 & 0 & 1 \\ 0 & 0.2 & 1 \\ 1 & 1 & 1 \end{pmatrix}, \quad a = b = (1, 1, 2).$$

After one pass of lines L5 and L6, the column sums of $P$ are exactly $(1, 1, 2)$, but the row sums are $(0.7081, 1.2036, 2.0882)$. After $T = 100$ passes both are right to 4 digits:

$$P = \begin{pmatrix} 0.6316 & 0.0755 & 0.2929 \\ 0.0755 & 0.2213 & 0.7032 \\ 0.2929 & 0.7032 & 1.0039 \end{pmatrix}.$$

Row 0 picks column 0 and row 1 picks column 1, and each is picked back. With $\theta = 0.2$ both pairs are matches, $(0, 0)$ with 0.6316 and $(1, 1)$ with 0.2213.

Now multiply $S$ and $z$ by 4. The plan becomes sharper: $P_{00} = 0.9814$, $P_{11} = 0.0371$ and $P_{1,\text{dustbin}} = 0.9626$. Only $(0, 0)$ is a match. This is the answer of the limit problem: the weights $S_{ij} - z$ are $2$, $-1$, $-1$ and $-0.8$, and the best partial matching keeps only the pair of positive weight. Pair $(1, 1)$ is a mutual best pair, so [mutual nearest neighbor](/mutual-nearest-neighbor-matching/) matching would keep it; the dustbin is what rejects it.

## Correctness

The layer has a proof; the network does not. The proof in `proofs/correctness.md` shows:

- **Exact columns.** After each pass the column sums of $P$ equal $b$ exactly. The row sums tend to $a$ as the iterations converge; convergence for a positive matrix is Sinkhorn's theorem, which we cite.
- **The fixed point is the entropic optimum.** A converged $P$ is the unique maximizer of $\langle \bar S, P \rangle + H(P)$ over the plans with marginals $a$ and $b$, with $H(P) = -\sum P_{ij}(\log P_{ij} - 1)$.
- **The limit is a partial matching.** For every plan, $\langle \bar S, P \rangle = \sum (S_{ij} - z) Q_{ij} + z (M + N)$, where $Q$ is the real block, and the real blocks are exactly the doubly substochastic matrices. So the linear problem is a [maximum weight](/maximum-weight-matching/) partial matching with weights $S_{ij} - z$. With scores scaled by $\beta$, the value of the entropic plan is within $O(1/\beta)$ of it.
- **The output is a matching.** Each keypoint is in at most one listed pair.

What this does not show is that the scores are good. The paper measures it: it reports pose accuracy on indoor image pairs from ScanNet and on outdoor pairs from YFCC100M, and homography accuracy on synthetic warps (2020), with SuperPoint and SIFT features, against nearest neighbor matching with the [ratio test](/lowe-ratio-test/) or mutual checks and against learned outlier filters. These are benchmark results with the protocol of the paper.

## Complexity

The model is the real RAM, and the cost of the network is outside the page. Lines L1 and L2 take $O(M N)$. Each pass of lines L5 and L6 computes $M + 1$ and $N + 1$ log-sum-exp values of length $N + 1$ and $M + 1$, which is $O(M N)$. Lines L7 to L9 take $O(M N)$. The total is $O(T M N)$ time and $O(M N)$ space.

The number of passes needed for a given accuracy grows when the scores have a large range, because the scaled matrix is then close to having zero entries. The paper uses $T = 100$. The paper reports about 12 million parameters for the network with $D = 256$, $L = 9$ layers and 4 attention heads, and about 69 ms for one pair on a GTX 1080 GPU; these are measurements of 2020 and include the network.

## Properties

- **Partial assignment.** The dustbin lets a point stay unmatched. Without it, the plan would force every point onto some partner.
- **Symmetric.** Swapping the images transposes $S$, and at convergence $P$ is transposed too. The output pairs are the same up to the swap.
- **Soft output.** $P_{ij}$ is a number in $(0, 1)$ for real pairs and can serve as a match confidence, for example to weight [RANSAC](/ransac/) samples.
- **Differentiable.** Each line is smooth in $S$ and $z$, so the network can be trained through the layer with ordinary backpropagation. This is the reason for Sinkhorn iterations instead of the exact [Hungarian algorithm](/hungarian-algorithm/).
- **Learned.** The behavior of the full matcher depends on the training data, for example indoor or outdoor images.

## Variants and improvements

- **Exact assignment.** On fixed scores, the [Hungarian algorithm](/hungarian-algorithm/) on the weights $S_{ij} - z$ gives the limit matching of the proof directly, in $O((M + N)^3)$ time, but it is not differentiable.
- **Classical filters.** [Mutual nearest neighbor](/mutual-nearest-neighbor-matching/) matching and the [ratio test](/lowe-ratio-test/) work on raw descriptor distances without training. SuperGlue replaces them.
- **LightGlue (2023).** Lindenberger, Sarlin and Pollefeys replaced the Sinkhorn layer with a cheaper double softmax and a matchability score, and stop early on easy pairs.
- **Dense matchers.** [LoFTR](/loftr/) drops the detector and matches coarse feature maps with a related double softmax or with the same optimal transport layer.

## When to use it

Use SuperGlue when you match keypoints across large changes of viewpoint or light, for example for visual localization or [relative pose](/relative-pose-problem/), and a GPU and trained weights for the type of images are available. Use the optimal matching layer alone on any score matrix when you need a soft partial assignment that is differentiable. Use nearest neighbors with the [ratio test](/lowe-ratio-test/) when there is no GPU, when the image type is far from the training data, or when you need a method with no learned parts.

## Pitfalls

- **Iterations are not convergence.** After $T$ passes only the columns are exact. With a large score range the rows can still be far off; check the row error if you depend on it.
- **Overflow.** In the plain domain, $\exp(\bar S)$ overflows for scores of a few hundred. Use the log domain, as lines L5 and L6 do.
- **The dustbin marginals.** The dustbin row must sum to $N$ and the column to $M$. With 1 instead, the total masses differ for $M \ne N$, and no plan has those marginals.
- **Normalization in the released code.** The released code divides the scores by $\sqrt{D}$ and divides the marginals by $M + N$ so that $P$ sums to 1, then multiplies back. Mixed conventions shift the threshold.
- **Argmax over the dustbin.** Line L8 takes the best real column, even when the dustbin entry of the row is larger; the threshold then removes weak pairs. Taking the argmax over the dustbin too is a different rule.
- **The threshold is tuned.** $\theta = 0.2$ in the paper is a design choice.

## Implementations

The network is outside this page. The Python code in `impl/python/superglue.py` implements only the optimal matching layer of lines L1 to L9 on a given score matrix and dustbin score: the augmentation, the log-domain Sinkhorn iterations, the plan and the mutual best pairs above a threshold. The tests check that the columns are exact after each pass, that the rows converge, that the log-domain result equals a plain-domain Sinkhorn, that large scores do not overflow, that marginal-preserving changes of the converged plan do not raise the entropic objective, that at a high scale the matches equal a brute-force best partial matching and the gap bound of the proof holds, and that a weak row goes to the dustbin.

## History

Sinkhorn studied the scaling of a positive matrix to given row and column sums in the 1960s, and Sinkhorn and Knopp (1967) proved convergence for the doubly stochastic case. Cuturi (2013) used the iterations for entropic optimal transport and made them a common tool in machine learning. Before 2020, feature matching was nearest neighbor search with hand-made filters such as the [ratio test](/lowe-ratio-test/) and mutual checks, sometimes followed by a learned outlier filter. Sarlin, DeTone, Malisiewicz and Rabinovich (2020) learned the matching itself with attention and put a Sinkhorn layer with a dustbin at the end. With [SuperPoint](/superpoint/) features it became a common baseline, and LightGlue (2023) followed as a faster successor.

## References
