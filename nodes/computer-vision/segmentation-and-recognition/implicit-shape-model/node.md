---
tag: PS7F2C
kind: model
slug: implicit-shape-model
name: Implicit shape model
aliases:
- ISM
- Leibe-Schiele detector
area: computer-vision/segmentation-and-recognition
level: advanced
summary: "Detect objects by letting each matched codebook patch vote for the object center in a generalized Hough space and finding the maxima of the votes."
history:
  year: 2004
  people: [Bastian Leibe, Ales Leonardis, Bernt Schiele]
  note: "Leibe and Schiele introduced the implicit shape model in 2003 and 2004 for combined detection and segmentation; the journal version of Leibe, Leonardis and Schiele (2008) gives the full probabilistic voting, the mean-shift search and the MDL verification."
prereqs: [generalized-hough-transform, mean-shift]
see_also: [hough-transform, bag-of-visual-words, deformable-part-model, pictorial-structures, object-detection, sliding-window-detection, sift, instance-segmentation]
sources:
  - paper: doi:10.1007/s11263-007-0095-3
    title: "Bastian Leibe, Ales Leonardis and Bernt Schiele, Robust object detection with interleaved categorization and segmentation, International Journal of Computer Vision 77(1-3), 2008, 259-289"
    locator: "Section III (codebook by agglomerative clustering, Algorithm 1), Section IV.A and IV.B (the model and its training, Algorithm 2), Section IV.C (probabilistic Hough voting, Eq. (8) to (13), Algorithm 3, and the mean-shift search, Eq. (15) and (16), Algorithm 4), Section V (top-down segmentation), Section VI (MDL hypothesis verification)"
  - paper: doi:10.1016/0031-3203(81)90009-1
    title: "Dana H. Ballard, Generalizing the Hough transform to detect arbitrary shapes, Pattern Recognition 13(2), 1981, 111-122"
    locator: "The R-table of displacements from boundary points to a reference point, indexed by edge direction, and voting for the reference point"
---

The implicit shape model (ISM) is a part-based object model for [object detection](/object-detection/) by voting. It learns a codebook of local appearance patches, and for each codebook entry it stores where, relative to the object centre and at which scale, that patch was seen on the training objects. At test time every local feature that matches a codebook entry casts votes for possible object centres, as in the [generalized Hough transform](/generalized-hough-transform/), and objects are found as the maxima of the vote density with [mean-shift](/mean-shift/). The shape is *implicit*: there is no explicit set of parts or springs, only the cloud of stored offsets, so a test object can combine patches seen on different training objects.

## The machine

**Features.** Local features are found with a scale-invariant interest point detector and described by an image patch or a descriptor such as [SIFT](/sift/). Each feature $f$ has a position $\ell = (x_{\mathrm{img}}, y_{\mathrm{img}}, s_{\mathrm{img}})$ in the image.

**The codebook (Section III).** The descriptors of the training features are grouped by average-link agglomerative clustering, stopped at a similarity threshold $t$, so that each cluster is compact. The cluster centres $C_1, \ldots, C_N$ are the codebook. The paper does the clustering with a reciprocal nearest neighbour chain in $O(N^2 d)$ time and $O(N)$ space for $N$ features of dimension $d$ (Algorithm 1).

**The model (Section IV.A and IV.B).** The model of a category is $\mathrm{ISM}(\mathcal{C}) = (\mathcal{C}, P_{I, \mathcal{C}})$: the codebook and a non-parametric spatial distribution for each entry. Training (Algorithm 2) runs the detector on the training images, matches each feature to all codebook entries with similarity at least $t$, and for each match records an *occurrence*: the offset from the feature to the centre of the object, and the scale of the feature. The set $\mathrm{Occ}[i]$ of all occurrences of entry $i$ is its spatial distribution. This is a star model around the centre, with one star per category, but with an arbitrary set of offsets for each entry instead of one Gaussian spring per part.

**Voting (Section IV.C.1).** For a test feature $f$ at $\ell$, let $\mathcal{C}^*$ be the codebook entries that match it. Each entry $C_i \in \mathcal{C}^*$ and each of its occurrences gives a vote for a centre and a scale,
$$x_{\mathrm{vote}} = x_{\mathrm{img}} - x_{\mathrm{occ}} \frac{s_{\mathrm{img}}}{s_{\mathrm{occ}}}, \qquad y_{\mathrm{vote}} = y_{\mathrm{img}} - y_{\mathrm{occ}} \frac{s_{\mathrm{img}}}{s_{\mathrm{occ}}}, \qquad s_{\mathrm{vote}} = \frac{s_{\mathrm{img}}}{s_{\mathrm{occ}}},$$
with the weight
$$p(o_n, x \mid C_i, \ell) \, p(C_i \mid f) = \frac{1}{|\mathrm{Occ}[i]|} \cdot \frac{1}{|\mathcal{C}^*|}.$$
So each feature casts votes of total weight 1, spread uniformly over its matching entries and, within each entry, over its occurrences. The score of a hypothesis of category $o_n$ at position $x$ is the sum of the votes of all features near it (Eq. (8) to (13), Algorithm 3).

**Search (Section IV.C.2).** The votes are first summed into a coarse 3D accumulator over $(x, y, s)$ to find candidate maxima. Each candidate is then refined by mean-shift on the continuous votes, with a *balloon* kernel density estimator whose kernel width grows with the scale of the hypothesis (Eq. (15) and (16), Algorithm 4). The local maxima of the density, above a threshold, are the object hypotheses.

**Segmentation and verification (Sections V and VI).** The votes that support a hypothesis point back to the features that cast them, and through the stored figure-ground masks of the training occurrences give a per-pixel probability of figure and ground. Overlapping hypotheses are then resolved by a minimum description length criterion that selects the subset of hypotheses that best explains the image, which the paper writes as a quadratic Boolean optimization (Eq. (23) to (28)).

## What it counts

The model counts the cost of voting and of finding maxima. With $F$ test features, an average of $c$ matched codebook entries per feature and $o$ occurrences per entry, voting costs $O(F c o)$ plus the cost of matching each feature to the codebook ($O(FN d)$ by linear search over $N$ entries of dimension $d$, less with a search tree). The accumulator has one bin per cell of a grid over position and scale, and each mean-shift refinement costs time proportional to the votes in its kernel per step. Unlike [sliding-window detection](/sliding-window-detection/), the cost depends on the number of features in the image, not on the number of windows, and a category with large intra-class variation simply has more occurrences per entry.

Training counts the cost of clustering, $O(N^2 d)$ for $N$ training features with the reciprocal nearest neighbour method, and one pass over the training features to record the occurrences.

## Relation to other models

- **The generalized Hough transform.** Ballard (1981) stored, for each edge direction of a shape, the displacements from boundary points to a reference point, in an R-table. The ISM is the same scheme with learned appearance codebook entries in place of edge directions, scale in the vote, and probabilistic weights.
- **Bags of visual words.** The codebook is the same kind of vocabulary as in the [bag of visual words](/bag-of-visual-words/), but a bag forgets where each word was seen, and the ISM keeps it relative to the object centre.
- **Pictorial structures and the deformable part model.** A [pictorial structure](/pictorial-structures/) has a few explicit parts with a spring between each part and a reference; the [deformable part model](/deformable-part-model/) has a star of learned filters scored at every window. The ISM has a star of many small patches with a non-parametric spatial distribution, is trained generatively from positive examples only, and finds objects by voting from sparse features, not by scanning.
- **Hough forests.** Later methods learn the codebook and the votes jointly with random forests, and others train the voting weights discriminatively; they keep the voting scheme of the ISM.
- **Centre-based detectors.** Some convolutional detectors predict a heat map of object centres and an offset at each location; the maxima of that map play the role of the maxima of the vote density.

## Known results in the model

**Votes as a density.** Because each feature spreads weight 1 over its votes, the score of a hypothesis is a sum of per-feature contributions, and the maxima of the kernel density of the votes are the hypotheses that the most features agree on. Mean-shift with a fixed kernel converges to a stationary point of that density; the balloon estimator with a scale-adaptive kernel keeps the search scale invariant.

**Robustness to occlusion and novel combinations.** A hypothesis needs only enough supporting votes, so a partly hidden object can still be found. Because occurrences come from all training objects, a test object can be recognized from patches of several different training examples.

**Ambiguity of overlapping objects.** One feature can support two overlapping hypotheses, so the raw maxima double count. The MDL verification of Section VI assigns each pixel to at most one hypothesis and picks the subset with the best total savings. This is a quadratic Boolean problem, hard in general, but small in practice because only a few candidate hypotheses overlap.

**Experiments.** The paper evaluates the detector on several categories, among them side views of cars and pedestrians in crowded street scenes, and shows that the top-down segmentation and the MDL verification improve the detection of overlapping and partly hidden objects.

## References
