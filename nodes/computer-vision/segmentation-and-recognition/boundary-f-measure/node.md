---
tag: 87X9C9
kind: definition
slug: boundary-f-measure
name: Boundary F-measure
aliases:
- BSDS boundary benchmark
- boundary precision and recall
area: computer-vision/segmentation-and-recognition
level: advanced
summary: The harmonic mean of precision and recall of predicted boundary pixels matched to human boundaries within a small distance by bipartite matching.
prereqs: [precision-and-recall, bipartite-matching, edge-detection]
see_also: [hopcroft-karp, mean-intersection-over-union, ultrametric-contour-map, canny-edge-detector, image-segmentation, hausdorff-distance, distance-transform, assignment-problem]
sources:
  - paper: doi:10.1109/TPAMI.2004.1273918
    title: "David R. Martin, Charless C. Fowlkes and Jitendra Malik, Learning to detect natural image boundaries using local brightness, color, and texture cues, IEEE Transactions on Pattern Analysis and Machine Intelligence 26(5), 2004, 530-549"
    locator: "the evaluation methodology (the correspondence of machine and human boundary pixels within a distance tolerance as a bipartite assignment, precision, recall and the F-measure, several human segmentations per image)"
  - paper: doi:10.1109/TPAMI.2010.161
    title: "Pablo Arbelaez, Michael Maire, Charless Fowlkes and Jitendra Malik, Contour detection and hierarchical image segmentation, IEEE Transactions on Pattern Analysis and Machine Intelligence 33(5), 2011, 898-916"
    locator: "Section 4.3 and Section 4.4.1 (precision and recall of boundaries, the F-measure at the optimal data set scale ODS, at the optimal image scale OIS, and the average precision AP)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 7.5, Image segmentation (the evaluation of boundaries and regions on the Berkeley data set)"
---

The boundary F-measure scores a boundary map against human boundary maps. A predicted boundary pixel is correct if it can be paired with a human boundary pixel within a small distance, and each human pixel can be used only once. The pairs come from a maximum [bipartite matching](/bipartite-matching/). Precision is the share of predicted pixels that are matched, recall is the share of human pixels that are matched, and the F-measure is their harmonic mean. Martin, Fowlkes and Malik (2004) defined it for the Berkeley Segmentation Data Set (BSDS), and it is the standard score of [edge detection](/edge-detection/) and of the boundaries of segmentations.

## Definition

Let $B$ be the set of predicted boundary pixels of an image, $G$ the set of human boundary pixels, and $d \ge 0$ a distance tolerance in pixels. The graph $\Gamma_d$ has an edge between $b \in B$ and $g \in G$ when $\lVert b - g \rVert \le d$. Let $\nu$ be the size of a maximum matching of $\Gamma_d$. Then
$$P = \frac{\nu}{|B|}, \qquad R = \frac{\nu}{|G|}, \qquad F = \frac{2 P R}{P + R} = \frac{2 \nu}{|B| + |G|}.$$
This page sets $P = 0$ when $B$ is empty, $R = 0$ when $G$ is empty, and $F = 0$ when $P + R = 0$.

BSDS has several human segmentations $G_1, \ldots, G_H$ of each image. The counts are then summed: a predicted pixel counts for precision if it is matched to at least one human map, and recall is the number of matched human pixels over the number of all human pixels.

```pseudo id=main
BOUNDARY-F(B, G, d)
L1  E ← the pairs (b, g) with b ∈ B, g ∈ G and ‖b - g‖ ≤ d
L2  M ← a maximum matching of the bipartite graph (B, G, E), by augmenting paths
L3  P ← |M| / |B| ; R ← |M| / |G|
L4  return P, R and 2 P R / (P + R)

BSDS-COUNTS(B, G_1, ..., G_H, d)
L5  A ← ∅ ; c_R ← 0 ; s_R ← 0
L6  for h ← 1 to H do
L7      M ← a maximum matching of the graph for B, G_h and d
L8      A ← A ∪ (the pixels of B matched in M) ; c_R ← c_R + |M| ; s_R ← s_R + |G_h|
L9  return (|A|, |B|, c_R, s_R)      ▷ P = |A| / |B|, R = c_R / s_R
```

The proof file shows that line L2 finds a maximum matching, so that $P$ and $R$ are the largest values that any one-to-one rule within the tolerance can give (a theorem). Larger $d$ never lowers them, and swapping $B$ and $G$ swaps $P$ and $R$. With several humans the recall does not depend on which maximum matching is found, but the precision can, so a program must fix the rule.

The tolerance in the benchmark code is a fraction of the image diagonal, 0.0075 by default, which is about 4 pixels for the BSDS images of $481 \times 321$ pixels. A detector gives a soft map $s$, and a threshold $t$ gives $B_t = \{x : s(x) \ge t\}$. Arbelaez et al. (2011) report three numbers over a range of thresholds:

- **ODS**, the optimal data set scale: the counts of all images are summed at each $t$, and the best $F$ over $t$ is reported.
- **OIS**, the optimal image scale: each image gets its own best $t$, and the counts at those thresholds are summed.
- **AP**, the average precision: the area under the precision and recall curve over $t$.

The Python code of this page uses augmenting paths, which take $O(|B| (|B| + |G| + E))$ time for $E$ edges, with $E = O(|B| d^2)$. The [Hopcroft-Karp algorithm](/hopcroft-karp/) needs $O(E \sqrt{|B| + |G|})$. The reference code of the benchmark solves an [assignment problem](/assignment-problem/) on the same graph.

## Examples and non-examples

- **A double edge.** The human boundary is a vertical line of 4 pixels in column 2. The prediction is two lines, in columns 1 and 3, with $d = 1$. Every predicted pixel is within distance 1 of a human pixel, but each human pixel can take only one of its two neighbors. So $\nu = 4$, $P = 4/8 = 1/2$, $R = 1$ and $F = 2/3$. A rule that only asks for a human pixel within $d$ would give $P = 1$ and reward thick or doubled edges.
- **Tolerance.** The same line moved by one pixel gives $F = 1$ for $d = 1$ and $F = 0$ for $d < 1$. On a $64 \times 64$ image the default tolerance is $0.0075 \cdot 90.5 \approx 0.68$ pixels, so only exact positions match. The tolerance must be stated with the score.
- **Two humans.** The prediction is the line in column 2. One human drew it in column 2 and another in column 4, with $d = 1$. All 4 predicted pixels match the first human, so $P = 1$. Recall is $(4 + 0)/(4 + 4) = 1/2$, and $F = 2/3$.
- **ODS against OIS.** Two images of one row of 4 pixels, each with one human pixel at position 0, and $d = 0.5$. The soft maps are $(0.9, 0.6, 0, 0)$ and $(0.6, 0, 0, 0)$, with thresholds 0.5 and 0.7. At 0.5 the sums are 2 matched pixels of 3 predicted and 2 human pixels, so $F = 4/5$. At 0.7 they are 1 of 1 and 2, so $F = 2/3$. ODS is $4/5$ at 0.5. OIS takes 0.7 for the first image and 0.5 for the second, and gets $F = 1$. OIS is often above ODS, but the proof file gives a case where it is below.
- **Not a region score.** The boundary F-measure ignores the labels of regions. A segmentation with the right boundaries but one missing piece of boundary loses only a little recall, while it merges two regions. Region scores such as the [mean intersection over union](/mean-intersection-over-union/) for labels, or the [Rand index](/rand-index/) for partitions, see this.
- **Not the Hausdorff distance.** The [Hausdorff distance](/hausdorff-distance/) gives the worst distance between the two sets and is ruled by one outlier. The boundary F-measure counts pixels within a fixed tolerance and ignores how far the unmatched ones are.

## Related definitions

[Precision and recall](/precision-and-recall/) are the general ratios, and the boundary F-measure computes them on pixels with a tolerance and a one-to-one rule. The matching is a maximum [bipartite matching](/bipartite-matching/), and with distances as costs it becomes an [assignment problem](/assignment-problem/). A [distance transform](/distance-transform/) of the human map gives a faster test of whether some human pixel is within $d$, but it does not enforce the one-to-one rule. The [ultrametric contour map](/ultrametric-contour-map/) gives a soft boundary map whose thresholds are segmentations, and its quality is reported with ODS, OIS and AP. For a learned or classical detector such as [Canny](/canny-edge-detector/), the threshold sweep gives the precision and recall curve. Scores for segmentations as partitions, such as segmentation covering and the variation of information, appear in the same benchmark next to the boundary F-measure.

The Python code of this page computes the matching, the scores for one and for several humans, and ODS and OIS with exact fractions. Its tests compare the matching with a brute-force maximum matching on small random maps.

## References
