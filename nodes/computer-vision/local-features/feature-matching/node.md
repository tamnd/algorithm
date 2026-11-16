---
tag: F0B3WT
kind: problem
slug: feature-matching
name: Feature matching
aliases:
- keypoint matching
- descriptor matching
area: computer-vision/local-features
level: intro
summary: Given the features of two images, find the pairs that show the same scene point, usually by nearest neighbors in descriptor space and a filter of the doubtful ones.
model: real-ram
complexity:
  vars: {m: the number of features of the first image, n: the number of features of the second image, D: the length of a descriptor}
  time: {worst: O(m n D)}
prereqs: [feature-descriptor, nearest-neighbor-search]
see_also: [lowe-ratio-test, mutual-nearest-neighbor-matching, best-bin-first-search, randomized-kd-forest, rootsift, superglue, loftr, ransac]
sources:
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision: Algorithms and Applications, 2nd edition, Springer, 2022"
    locator: "Section 7.1.3, feature matching: matching strategies and error rates, efficient matching, and feature match verification"
  - paper: doi:10.1023/B:VISI.0000029664.99615.94
    title: "David G. Lowe, Distinctive image features from scale-invariant keypoints, International Journal of Computer Vision 60(2), 2004, 91-110"
    locator: "Section 7, keypoint matching with the ratio of the two nearest distances, approximate search with best bin first, and verification by a pose"
  - paper: doi:10.1109/TPAMI.2014.2321376
    title: "Marius Muja and David G. Lowe, Scalable nearest neighbor algorithms for high dimensional data, IEEE Transactions on Pattern Analysis and Machine Intelligence 36(11), 2014, 2227-2240"
    locator: the approximate nearest neighbor methods for descriptor matching and their measured speed and precision
  - paper: doi:10.1109/CVPR42600.2020.00499
    title: "Paul-Edouard Sarlin, Daniel DeTone, Tomasz Malisiewicz and Andrew Rabinovich, SuperGlue, learning feature matching with graph neural networks, IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2020"
    locator: the formulation of matching as a partial assignment with a dustbin for unmatched features
---

Feature matching takes the features of two images, each a position and a [descriptor](/feature-descriptor/), and returns pairs that show the same point of the scene. The true pairs are fixed by the geometry of the scene, which the matcher does not know, so in practice the problem is solved in two parts. First each feature gets candidates by [nearest neighbor search](/nearest-neighbor-search/) in descriptor space. Then doubtful candidates are removed by filters such as [Lowe's ratio test](/lowe-ratio-test/) and the [mutual check](/mutual-nearest-neighbor-matching/), and often by a geometric test with [RANSAC](/ransac/). Exact search with brute force costs $O(m n D)$; approximate search with a [kd-forest](/randomized-kd-forest/) is much faster for SIFT-sized descriptors. Learned matchers such as [SuperGlue](/superglue/) and [LoFTR](/loftr/) replace the hand-made filters with a network. Feature matching is the first step of [image stitching](/image-stitching/), [structure from motion](/structure-from-motion-problem/) and [visual odometry](/visual-odometry/).

## In plain words

Take two photos of the same building from two places. A detector marks a few hundred small spots in each photo, such as corners of windows, and describes each spot by a list of numbers. Feature matching draws lines between spots of the two photos that show the same corner. The easy idea is to link each spot to the spot with the most similar numbers. That goes wrong when many windows look the same, or when a spot is hidden in the other photo, because a hidden spot still has some most similar spot. So matchers add checks: is the best partner clearly better than the second best, do the two spots pick each other, and do all lines agree with one camera motion?

## Definition

**Input.** Two finite lists of features. The first image has $m$ features $(\mathbf x_i, a_i)$ for $0 \le i < m$, and the second has $n$ features $(\mathbf y_j, b_j)$ for $0 \le j < n$. Here $\mathbf x_i, \mathbf y_j \in \mathbb R^2$ are image positions and $a_i, b_j \in \mathbb R^D$ are descriptors. A distance $d$ on descriptors is given, usually the Euclidean distance, or the [Hamming distance](/hamming-distance/) for binary descriptors.

**Output.** A set $M \subseteq \{0, \dots, m-1\} \times \{0, \dots, n-1\}$ of pairs. Most methods return a partial matching: each $i$ and each $j$ is in at most one pair.

**The goal.** Let $M^*$ be the set of true pairs, those whose two features show the same scene point within a tolerance $\varepsilon$. For example, for a plane seen by two cameras, $M^* = \{ (i, j) : \lVert \pi(H \tilde{\mathbf x}_i) - \mathbf y_j \rVert \le \varepsilon \}$ for a [homography](/homography/) $H$, where $\tilde{\mathbf x}$ adds a coordinate 1 and $\pi$ divides by the last coordinate. The matcher does not know $H$ or the 3D scene, so $M^*$ is not a function of the input, and a matcher is judged by its precision $\lvert M \cap M^* \rvert / \lvert M \rvert$ and its recall $\lvert M \cap M^* \rvert / \lvert M^* \rvert$ on data with known geometry.

**The computable versions.** The following are exact problems with a unique answer once a tie rule is fixed, for example "the smaller index wins":

- *Nearest neighbor matching:* $M = \{ (i, f(i)) \}$ with $f(i) = \arg\min_j d(a_i, b_j)$. This is the bichromatic all nearest neighbors problem.
- *Filtered matching:* the pairs of nearest neighbor matching that pass a filter, such as $d(a_i, b_{f(i)}) < r \cdot d_2(i)$, where $d_2(i)$ is the distance to the second nearest neighbor, or $g(f(i)) = i$, where $g$ is nearest neighbor matching in the other direction.
- *Optimal partial assignment:* a partial matching $M$ that maximizes $\sum_{(i, j) \in M} (z - d(a_i, b_j))$ for a value $z > 0$, the gain of a pair minus its distance. Pairs with $d \ge z$ never help, so features without a good partner stay unmatched.

The number of partial matchings is $\sum_{k=0}^{\min(m, n)} \binom{m}{k} \binom{n}{k} k!$, so the optimization version cannot be solved by trying them all, except on tiny inputs.

## Variants

- **Sparse and dense.** Sparse matching uses keypoints from a detector. Dense or detector-free matching, such as [LoFTR](/loftr/), matches cells of a grid and refines the positions, which helps on surfaces with little texture.
- **One-to-many.** Keep the $k$ nearest neighbors of each feature, for example to give RANSAC more candidates. The result is not a matching.
- **Guided matching.** When a [fundamental matrix](/fundamental-matrix/) or a homography is already known, search only near the [epipolar line](/epipolar-geometry/) or the predicted position.
- **Matching against a database.** Match the features of one image against those of many images, as in [image retrieval](/image-retrieval/), where the features are often quantized into visual words.
- **Binary descriptors.** With [ORB](/orb-features/) or [BRIEF](/brief-descriptor/), the distance is the Hamming distance and hashing replaces kd-trees.

## Examples

One-dimensional descriptors make a case that you can check by hand. Let $a_0 = 0$, $a_1 = 1$, $a_2 = 5$ and $b_0 = 0.1$, $b_1 = 1.2$, $b_2 = 1.22$, $b_3 = 9$, with $d(a, b) = \lvert a - b \rvert$. Suppose the true pairs are $M^* = \{(0, 0), (1, 1)\}$, and $a_2$ has no true partner.

| feature | nearest | $d_1$ | second nearest | $d_2$ | $d_1 / d_2$ | picked back? |
|---|---|---|---|---|---|---|
| $a_0$ | $b_0$ | 0.1 | $b_1$ | 1.2 | 0.083 | yes |
| $a_1$ | $b_1$ | 0.2 | $b_2$ | 0.22 | 0.909 | yes |
| $a_2$ | $b_2$ | 3.78 | $b_1$ | 3.8 | 0.995 | no, $b_2$ picks $a_1$ |

| method | output $M$ | precision | recall |
|---|---|---|---|
| nearest neighbor | $\{(0,0), (1,1), (2,2)\}$ | 2/3 | 1 |
| ratio test, $r = 0.8$ | $\{(0,0)\}$ | 1 | 1/2 |
| mutual check | $\{(0,0), (1,1)\}$ | 1 | 1 |
| optimal partial assignment, $z = 1$ | $\{(0,0), (1,1)\}$, gain $0.9 + 0.8 = 1.7$ | 1 | 1 |
| full assignment of minimum total distance | $\{(0,0), (1,1), (2,2)\}$, total $4.08$ | 2/3 | 1 |

The ratio test drops the true pair $(1, 1)$, because $b_1$ and $b_2$ are almost equally close to $a_1$: it cannot tell a repeated pattern from a true partner. The mutual check keeps $(1, 1)$ and drops $(2, 2)$, because $b_2$ prefers $a_1$. For the partial assignment, only the pairs $(0,0)$, $(1,1)$, $(1,2)$ and $(1,0)$ have $d < 1$ and a positive gain; the best choice is $(0,0)$ with $(1,1)$, since $(0,0)$ with $(1,2)$ gives only 1.68. A full assignment must use $a_2$, so it adds the false pair $(2, 2)$. No method wins on every input; the table shows one input.

## Known algorithms

- **Brute force.** Compute all $m n$ distances: $O(m n D)$ time, exact. On a GPU this is often the fastest choice for a few thousand features.
- **[kd-tree](/kd-tree/) search.** Exact nearest neighbors with the [kd-tree search](/kd-tree-nearest-neighbor-search/), fast in low dimension, but for $D = 128$ it visits most of the leaves.
- **[Best bin first](/best-bin-first-search/).** Approximate search in one kd-tree that stops after a fixed number of leaves, which bounds the time per query; Lowe (2004) used it for SIFT.
- **[Randomized kd-forest](/randomized-kd-forest/).** Several trees with random splits searched with one priority queue, a default of the FLANN library.
- **[Locality-sensitive hashing](/locality-sensitive-hashing/).** Approximate search by hashing, common for binary descriptors.
- **Filters.** The [ratio test](/lowe-ratio-test/) and the [mutual check](/mutual-nearest-neighbor-matching/) cost one more nearest neighbor and one more search in the other direction. [RootSIFT](/rootsift/) changes the descriptors before the search.
- **Global assignment.** The optimal partial assignment is a [maximum weight matching](/maximum-weight-matching/) in a bipartite graph and can be solved with the [Hungarian algorithm](/hungarian-algorithm/) in $O((m + n)^3)$ time.
- **Learned matchers.** [SuperGlue](/superglue/) refines the descriptors with attention and solves an entropic partial assignment with Sinkhorn iterations; [LoFTR](/loftr/) matches a coarse grid without a detector and refines each match in a window.
- **Verification.** [RANSAC](/ransac/) or [PROSAC](/prosac/) fits a homography or a fundamental matrix and keeps the pairs that agree with it, as in [spatial verification](/spatial-verification/).

## Bounds

In the real RAM with $O(1)$ cost per arithmetic operation, brute force gives $O(m n D)$ for nearest neighbor matching and for both filters. Every exact method must read the input, so $\Omega((m + n) D)$ is a trivial lower bound. In fixed low dimension, kd-trees and other point location structures answer each query in about logarithmic time on typical data, but descriptors have $D$ from 32 to 256. For such dimensions, results of fine-grained complexity under the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/) indicate that the exact [bichromatic closest pair](/bichromatic-closest-pair/) problem, and so also exact nearest neighbor matching, has no algorithm that is much faster than $m n$ when $D$ grows like $\log n$. This is why practical matchers use approximate search.

The goal $M^*$ has a different limit, which is not about time. Two scene points with equal descriptors give the same input whichever of them is the true partner, so no method that uses only the descriptors can be correct on both. Filters reduce this risk by dropping such features; geometry, as in RANSAC, or context, as in SuperGlue, can resolve it. Precision and recall of real methods are measured on benchmarks, not proved.

## Reductions

- **To nearest neighbor search.** Nearest neighbor matching is $m$ queries of [nearest neighbor search](/nearest-neighbor-search/) against $n$ points, plus the cost to build the index. The ratio test needs two nearest neighbors per query, and the mutual check needs $n$ more queries in the other direction.
- **From bichromatic closest pair.** The closest pair between the two lists is the nearest neighbor pair of smallest distance, which takes $O(m)$ more time. So a fast exact matcher gives a fast exact [bichromatic closest pair](/bichromatic-closest-pair/) algorithm, which is the reason for the bound above.
- **To the assignment problem.** Add a dummy partner for each feature with gain 0. The optimal partial assignment becomes an [assignment problem](/assignment-problem/) on $m + n$ rows and columns.

## Applications

- [Image stitching](/image-stitching/) and [homography estimation](/homography-estimation/) from matched points.
- [Structure from motion](/structure-from-motion-problem/), where matches are chained into [feature tracks](/feature-track/), and the [relative pose problem](/relative-pose-problem/) with the [essential matrix](/essential-matrix/).
- [Visual odometry](/visual-odometry/) and localization of a camera in a known map.
- [Image retrieval](/image-retrieval/) and [visual place recognition](/visual-place-recognition/), with matching as the [spatial verification](/spatial-verification/) of the best results.

## References
