---
tag: RBM5RD
kind: algorithm
slug: selective-search
name: Selective search
aliases:
- hierarchical grouping proposals
area: computer-vision/segmentation-and-recognition
level: advanced
summary: Generate object proposals by greedily merging the most similar adjacent regions of an over-segmentation under several color spaces and similarity measures.
solves: [object-proposals]
model: real-ram
complexity:
  vars: {p: the number of pixels, n: the number of initial regions, b: the number of histogram bins}
  time: {worst: "O(p + n^2 (b + log n))"}
  space: {extra: "O(p + n b + n^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2011
  people: [Koen E. A. van de Sande, Jasper R. R. Uijlings, Theo Gevers, Arnold W. M. Smeulders]
  note: "Presented at ICCV 2011 as segmentation as selective search, and given in full in the 2013 journal paper. It became the proposal step of R-CNN and Fast R-CNN."
prereqs: [object-proposals, felzenszwalb-segmentation, priority-queue]
see_also: [r-cnn, fast-r-cnn, agglomerative-clustering, image-segmentation, slic-superpixels, faster-r-cnn, box-non-maximum-suppression, object-detection]
sources:
  - paper: doi:10.1007/s11263-013-0620-5
    title: "Jasper R. R. Uijlings, Koen E. A. van de Sande, Theo Gevers and Arnold W. M. Smeulders, Selective search for object recognition, International Journal of Computer Vision 104(2), 2013, 154-171"
    locator: "Section 3.1, Hierarchical grouping (Algorithm 1); Section 3.2, Diversification strategies (colour spaces, the similarities s_colour, s_texture, s_size and s_fill, starting regions); Section 3.3, Combining locations (the ranking RND times position); Tables 4 and 5"
  - paper: doi:10.1023/B:VISI.0000022288.19776.77
    title: "Pedro F. Felzenszwalb and Daniel P. Huttenlocher, Efficient graph-based image segmentation, International Journal of Computer Vision 59(2), 2004, 167-181"
    locator: "Section 4 (the segmentation used for the initial regions, with its scale parameter k)"
  - paper: doi:10.1109/CVPR.2014.81
    title: "Ross Girshick, Jeff Donahue, Trevor Darrell and Jitendra Malik, Rich feature hierarchies for accurate object detection and semantic segmentation, CVPR 2014, 580-587"
    locator: "Section 2.1, Module design (about 2000 region proposals per image from the fast mode of selective search)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.3, Object detection"
---

Selective search finds [object proposals](/object-proposals/) by grouping. It starts from many small regions of an over-segmentation, made by [Felzenszwalb-Huttenlocher segmentation](/felzenszwalb-segmentation/), and merges the two most similar neighboring regions again and again until one region is left. Every region that appears on the way, small or large, gives one box. Since objects come at all sizes, the hierarchy holds boxes at all sizes. The similarity mixes colour, texture, size and how well two regions fill their joint box. To catch objects that one rule misses, the method runs several grouping strategies, with different colour spaces, similarity mixes and starting segmentations, and combines their boxes. With $n$ starting regions one strategy gives $2n - 1$ boxes for a connected image. [R-CNN](/r-cnn/) and [Fast R-CNN](/fast-r-cnn/) used it to get about 2000 proposals per image.

## In plain words

Cut a photo into many small patches of nearly the same colour. A real object, such as a person, is made of several patches: a face, a shirt, trousers. So keep joining the two neighboring patches that look most alike, and write down the box around each new joined patch. Small patches join first, then bigger parts, and at the end the whole photo is one patch. Each box on the list is a guess where an object could be. Some objects are found by colour, others by texture or by the way their parts fit together, so run the joining several times with different rules and colour views, and merge the lists. The method learns nothing, so it is fast to set up and works for any kind of object.

## The problem

The input is an image of $p$ pixels and an over-segmentation into $n$ regions, given as a label map. Two regions are neighbors when a pixel of one is 4-connected to a pixel of the other. The output is a ranked list of boxes, each the bounding box of a union of regions, that covers as many objects as possible at IoU 0.5 or more, for as few boxes as possible. This is the [object proposal](/object-proposals/) problem; there is no exact optimum to compute, so the method is a heuristic. A box is $(x_1, y_1, x_2, y_2)$ with $x_2$ one past the last column.

## The algorithm

For a region $r$ let $\operatorname{size}(r)$ be its pixel count, $BB(r)$ its box, and $C(r)$ its colour histogram: 25 bins per channel, normalized to sum 1. For neighbors $r_i$ and $r_j$ in an image of $p$ pixels, the paper defines

$$s_{colour}(r_i, r_j) = \sum_{k} \min(c_i^k, c_j^k), \qquad s_{size}(r_i, r_j) = 1 - \frac{\operatorname{size}(r_i) + \operatorname{size}(r_j)}{p},$$

$$s_{fill}(r_i, r_j) = 1 - \frac{\operatorname{size}(BB_{ij}) - \operatorname{size}(r_i) - \operatorname{size}(r_j)}{p},$$

where $BB_{ij}$ is the box around both, and $s = a_1 s_{colour} + a_2 s_{texture} + a_3 s_{size} + a_4 s_{fill}$ with each $a_k \in \{0, 1\}$. Each of the four lies in $[0, 1]$. The size term makes small regions merge first, so that one large region does not eat its neighbors one by one. The fill term prefers pairs that fit well into one box, such as a region and a hole in it.

```pseudo id=main
SELECTIVE-SEARCH(I, R_0, a)          ▷ image, initial regions, similarity weights
L1  compute size, box, histogram and neighbors of each region of R_0
L2  S ← { s(r_i, r_j) : r_i, r_j neighbors in R_0 }      ▷ a max-priority queue
L3  L ← the boxes of R_0
L4  while S is not empty
L5      (r_i, r_j) ← the pair of largest s in S (ties: the smaller pair of ids)
L6      r_t ← r_i ∪ r_j with size_i + size_j, BB_ij and C_t = (size_i C_i + size_j C_j)/(size_i + size_j)
L7      remove from S every pair that holds r_i or r_j
L8      for each neighbor r_k of r_i or r_j, other than r_i and r_j: insert s(r_k, r_t) into S
L9      the neighbors of r_t are those r_k; append the box of r_t to L
L10 return L
```

Line L6 gets the histogram of the union without reading its pixels: a histogram normalized to sum 1 is the count vector divided by the size, so the size-weighted mean of the two normalized histograms is the normalized count vector of the union. The same holds for the texture histogram of the paper. The code keeps the queue as a [binary heap](/binary-heap/) and does line L7 lazily: a popped pair whose regions are gone is skipped.

**Diversification.** One strategy is one choice of colour space, starting segmentation and weights $a$. The paper uses colour spaces with different invariance properties (RGB, intensity, Lab, rgI, HSV, normalized rg, the opponent space C and the hue H), several values of the parameter $k$ of the starting segmentation, and the mixes C+T+S+F, T+S+F, F and S. Its "fast" setting has 8 strategies: HSV and Lab, C+T+S+F and T+S+F, and $k \in \{50, 100\}$.

**Ranking.** Within one hierarchy the region made last, the whole image, gets position 1, the one before it position 2, and so on. Each box gets the score RND times its position, with RND uniform in $[0, 1]$, the boxes of all strategies are sorted by that score, and duplicates are removed. So large regions tend to come first, but the order is mixed between strategies, and a box found by several strategies has several chances to come early. A budget of $N$ proposals takes the first $N$ boxes.

## Example

Take a $4 \times 6$ grayscale image with a bright top half and a dark bottom half, given with five starting regions:

| row | pixels | labels |
|---|---|---|
| 0 | 200 205 210 205 210 215 | 0 0 0 1 1 1 |
| 1 | 200 205 210 205 210 215 | 0 0 0 1 1 1 |
| 2 | 20 30 100 105 30 40 | 2 2 3 3 4 4 |
| 3 | 20 30 100 110 30 40 | 2 2 3 3 4 4 |

With 25 bins, the bin of a value $v$ is $\lfloor 25 v / 256 \rfloor$. Region 0 has 1/3 of its pixels in bin 19 and 2/3 in bin 20; region 1 has all in bin 20. So $s_{colour}(0, 1) = 2/3$. The image has $p = 24$ pixels. With all weights 1 (no texture), the neighbor pairs score:

| pair | colour | size | fill | total |
|---|---|---|---|---|
| 0, 1 | 2/3 | 1/2 | 1 | 13/6 |
| 2, 3 | 0 | 2/3 | 1 | 5/3 |
| 3, 4 | 0 | 2/3 | 1 | 5/3 |
| 0, 2 and 1, 4 | 0 | 7/12 | 11/12 | 3/2 |
| 0, 3 and 1, 3 | 0 | 7/12 | 3/4 | 4/3 |

The run goes:

1. Merge 0 and 1 into region 5, the top half, box $(0, 0, 6, 2)$.
2. Pairs (2, 3) and (3, 4) tie at 5/3, and the smaller pair wins: merge 2 and 3 into region 6, box $(0, 2, 4, 4)$, histogram 1/4 in each of the bins 1, 2, 9 and 10.
3. Pair (4, 6) scores $1/4 + 1/2 + 1 = 7/4$, since both have a quarter of their pixels in bin 2 and they fill their box $(0, 2, 6, 4)$ exactly. Pairs (5, 6) and (4, 5) score 1. Merge 4 and 6 into region 7, the bottom half.
4. Merge 5 and 7 into region 8, the whole image.

The list has $2 \cdot 5 - 1 = 9$ boxes. With the size term alone the merges are (2, 3), (1, 4), (0, 5) and (6, 7): the small regions go first.

## Correctness

There is no optimal output to compare with, so correctness here means that the code does what lines L1 to L10 say. The claims are proved in [the proof page](proofs/correctness.md).

1. **Hierarchy.** If the neighbor graph of $R_0$ has $c$ connected parts, the loop makes exactly $n - c$ merges and returns $2n - c$ boxes, and each box is the bounding box of the union of the starting regions below it. The neighbor sets stay correct after each merge: two current regions are neighbors exactly when some of their starting regions are.
2. **Exact features.** The histogram of line L6 equals the normalized histogram of the pixels of the union, and every similarity lies in $[0, 1]$ for weights in $\{0, 1\}$.
3. **Lazy deletion.** The heap version merges the same pairs in the same order as a version that scans all current pairs at each step, since the similarity of a pair of live regions never changes and stale pairs are skipped.

The tests check the first and third claims against a direct computation from the label map and against the scan version, on random label maps.

## Complexity

Line L1 reads each pixel once and costs $O(p)$, plus $O(nb)$ for the histograms. Each of the at most $n - 1$ merges costs $O(b)$ for the new histogram, and $O(b + \log Q)$ for each neighbor of the new region, where $Q$ is the queue size. A region can have up to $n - 1$ neighbors, and every push adds one entry to the queue, so $Q = O(n^2)$ and the worst case is $O(p + n^2 (b + \log n))$ in the [real RAM](/real-ram/) model. When each starting region is connected, as with Felzenszwalb-Huttenlocher segments, the neighbor graph is planar, and merging two neighbors keeps it planar, so at every step there are at most $3m - 6$ neighbor pairs among $m$ regions; on real images the degrees stay small, and the merges cost far less than the worst case. Space is $O(p)$ for the labels, $O(nb)$ for the histograms of the $2n - 1$ regions, and $O(n^2)$ for the queue in the worst case. A run of $s$ strategies costs $s$ times as much, plus one starting segmentation for each colour space and value of $k$. On a CPU the fast setting takes seconds per image.

## Properties

- **Deterministic for one strategy.** With exact similarities and a fixed tie rule the merges are a function of the input. The ranking across strategies is random by design.
- **Not exact.** It is a heuristic for a problem with no exact optimum, and a missed object cannot be found later by the detector.
- **Class-agnostic and training-free.** No part is learned, so it works for any object class. The paper trains a classifier only for the detection step that comes after the proposals.
- **Recall over precision.** The output holds many boxes that are not objects, by design.
- **All scales.** The hierarchy has regions of every size, from the starting regions to the image, with no image pyramid.
- **Greedy.** Each merge is final, as in [agglomerative clustering](/agglomerative-clustering/). Unlike single-linkage clustering, the similarity of a merged region is recomputed from its features.

## Variants and improvements

- **Fast and quality settings.** The paper's fast setting (8 strategies, about 2000 boxes per image) and quality setting (80 strategies, about 10000 boxes) trade time for recall.
- **Single strategy.** A single colour space and one mix of similarities is the cheapest variant and loses some recall.
- **Texture.** The full method adds $s_{texture}$, a histogram intersection of SIFT-like histograms of Gaussian derivatives in 8 orientations and 10 bins per channel. The code of this page leaves it out.
- **Other starting regions.** [SLIC superpixels](/slic-superpixels/) or a watershed can replace the Felzenszwalb-Huttenlocher segments.
- **Learned grouping.** MCG and similar methods group a contour hierarchy and rank the regions with a learned model. The region proposal network of [Faster R-CNN](/faster-r-cnn/) replaced selective search in most detectors, since it shares the network and runs much faster.

## When to use it

Use it when a detector needs class-agnostic proposals and no training data for them is at hand, or as a baseline for a proposal method. It suits images where objects differ from the background in colour or texture. Prefer a learned proposal network inside a detector that is trained end to end, and a single-stage detector when speed matters, since selective search takes seconds per image on a CPU.

## Pitfalls

- **The starting segmentation decides the finest boxes.** A region that spans two objects cannot be split later, so an object smaller than the starting regions has no box. Use a small $k$ and several values.
- **Histograms must be normalized.** Unnormalized counts make large regions look similar to everything.
- **Neighbor bookkeeping.** After a merge, every former neighbor of $r_i$ or $r_j$ must point to $r_t$. An asymmetric neighbor set, such as one filled while reading the label map in one pass and reset on the first pixel of a region, gives wrong pairs and can make the loop work on dead regions.
- **Ties.** Small integer images give exact ties, and the merge order then depends on the tie rule. Fix it.
- **Duplicates.** Different strategies give the same boxes many times. Remove them after the ranking, or the budget fills with copies.
- **Proposals near the border and tiny boxes.** R-CNN-style detectors often drop boxes below a minimum size; say so when reporting recall.

## Implementations

The Python code takes an image (gray or with channels) and a label map, and implements lines L1 to L10 with exact fractions for the histograms and similarities, a heap with lazy deletion, and the tie rule of the smaller pair of ids. It also has a slow version that scans all pairs at each step, the 4-connected components of equal values as a simple source of starting regions, and the ranking by RND times position with removal of duplicates. It does not have the Felzenszwalb-Huttenlocher segmentation, which has [its own page](/felzenszwalb-segmentation/), or the texture similarity. The tests check the example above, the heap version against the scan version, the number of merges and every box against the label map, the propagated histogram against one counted from the pixels, the range of the similarities, and the ranking.

## History

Before 2011, object detection was mostly done by [sliding windows](/sliding-window-detection/) with cheap classifiers, and segmentation was seen as a separate problem. Alexe, Deselaers and Ferrari (2010) scored windows by an objectness measure, and Carreira and Sminchisescu (CPMC) and Endres and Hoiem proposed regions from many figure-ground segmentations. Van de Sande, Uijlings, Gevers and Smeulders presented selective search at ICCV 2011, joining bottom-up grouping with the goal of high recall for detection, and the journal version of 2013 by Uijlings et al. gives the full evaluation. Girshick et al. used its fast mode for [R-CNN](/r-cnn/) in 2014, and Fast R-CNN kept it, until the region proposal network of Faster R-CNN in 2015 made proposals part of the network.

## References
