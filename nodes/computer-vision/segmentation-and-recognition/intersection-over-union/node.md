---
tag: 20CWE7
kind: definition
slug: intersection-over-union
name: Intersection over union
aliases:
- IoU
- box overlap ratio
area: computer-vision/segmentation-and-recognition
level: intro
summary: "The area of the intersection of two boxes or regions divided by the area of their union, the measure of how well a detection matches an object."
prereqs: [axis-aligned-bounding-box]
see_also: [jaccard-similarity, box-non-maximum-suppression, detection-mean-average-precision, mean-intersection-over-union, object-detection, bounding-box-regression, convex-polygon-intersection, metric-space]
sources:
  - paper: doi:10.1111/j.1469-8137.1912.tb05611.x
    title: "Paul Jaccard, The distribution of the flora in the alpine zone, New Phytologist 11(2), 1912, 37-50"
    locator: "The coefficient of community: the number of species common to two areas as a fraction of the number of species in both"
  - paper: doi:10.1007/s11263-009-0275-4
    title: "Mark Everingham, Luc Van Gool, Christopher K. I. Williams, John Winn and Andrew Zisserman, The PASCAL Visual Object Classes (VOC) challenge, International Journal of Computer Vision 88(2), 2010, 303-338"
    locator: "Section 4.2, Bounding box evaluation, Eq. (3) (the overlap ratio must exceed 0.5, and why the threshold is low), and Section 4.2.1 (the segmentation measure, the same ratio on pixels)"
  - paper: doi:10.1016/j.patrec.2018.12.007
    title: "Sven Kosub, A note on the triangle inequality for the Jaccard distance, Pattern Recognition Letters 120, 2019, 36-38"
    locator: "The two proofs that 1 minus the Jaccard index is a metric on finite sets"
  - paper: doi:10.1109/CVPR.2019.00075
    title: "Hamid Rezatofighi, Nathan Tsoi, JunYoung Gwak, Amir Sadeghian, Ian Reid and Silvio Savarese, Generalized intersection over union: a metric and a loss for bounding box regression, CVPR 2019, 658-666"
    locator: "Section 3 (the definition of GIoU with the smallest enclosing box, its range and its properties)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.3, Object detection (the overlap of a detection and a ground truth box)"
---

Intersection over union (IoU) is the area of the overlap of two regions divided by the area of the region that they cover together. It is the [Jaccard index](/jaccard-similarity/) of two sets of points, applied to boxes or to pixel masks in an image. In [object detection](/object-detection/) it decides whether a predicted box matches a ground-truth box, and it is the overlap test inside [box non-maximum suppression](/box-non-maximum-suppression/) and [detection mean average precision](/detection-mean-average-precision/). The value is 1 for two equal regions, 0 for regions that do not overlap, and it does not change when both regions move or scale together.

## Definition

For two measurable regions $A$ and $B$ of the plane with $|A \cup B| > 0$, where $|\cdot|$ is the area,

$$\mathrm{IoU}(A, B) = \frac{|A \cap B|}{|A \cup B|} = \frac{|A \cap B|}{|A| + |B| - |A \cap B|}.$$

For two finite sets of pixels, $|\cdot|$ is the number of pixels. When both regions are empty the ratio is $0/0$, and a program must pick a value; this page uses 0, and a mask metric often uses 1.

On this page a box is $a = (x_1, y_1, x_2, y_2)$ with $x_1 \le x_2$ and $y_1 \le y_2$ in continuous image coordinates, the set $[x_1, x_2] \times [y_1, y_2]$, so its area is $(x_2 - x_1)(y_2 - y_1)$. An [axis-aligned box](/axis-aligned-bounding-box/) meets another axis-aligned box in a box or in nothing, so the IoU of two boxes costs a constant number of operations:

```pseudo id=main
IOU(a, b)
L1  w ← min(a.x2, b.x2) - max(a.x1, b.x1)
L2  h ← min(a.y2, b.y2) - max(a.y1, b.y1)
L3  if w ≤ 0 or h ≤ 0 then I ← 0 else I ← w · h
L4  U ← area(a) + area(b) - I
L5  return I / U
```

Line L3 tests the overlap of the two intervals in each axis, and line L4 is inclusion and exclusion. The proof that the procedure gives the ratio of areas is in the correctness file of this page. On integer boxes the value is a rational number, and an exact check uses fractions.

The PASCAL VOC development kit uses a different box form: $x_1$ and $x_2$ are the indices of the first and the last pixel, both inclusive, so a side has $x_2 - x_1 + 1$ pixels. This form is the continuous box $(x_1, y_1, x_2 + 1, y_2 + 1)$. Code that mixes the two forms gets a wrong value, and the error is large for small boxes.

The quantity $d(A, B) = 1 - \mathrm{IoU}(A, B)$ is the Jaccard distance. It is a [metric](/metric-space/): it is symmetric, it is 0 only for equal regions of positive area, and it satisfies the triangle inequality (Kosub 2019 gives two short proofs for finite sets; the box case follows through pixel cells). This is a theorem. The use of a fixed threshold on IoU, such as 0.5, to call a detection correct is a convention.

## Examples and non-examples

- **The check values.** $\mathrm{IoU}((0,0,2,2), (1,1,3,3)) = 1/7$: the intersection is the unit square, and the union is $4 + 4 - 1 = 7$. $\mathrm{IoU}((0,0,10,10), (5,0,15,10)) = 50 / 150 = 1/3$: a box shifted by half its width.
- **A shift by a third.** $\mathrm{IoU}((0,0,3,3), (1,0,4,3)) = 6 / 12 = 1/2$. A box moved sideways by one third of its width is exactly at the threshold 0.5 of PASCAL VOC, and VOC requires a value above 0.5, so this box does not count as a match.
- **A box that is too small.** A box of side 7 inside the box $(0,0,10,10)$ gives $49/100$. A detection that is correct in position but has sides at 70 percent of the true sides fails the 0.5 test.
- **The same numbers in the inclusive form.** As inclusive pixel boxes, $(0,0,2,2)$ and $(1,1,3,3)$ have 9 pixels each and share 4, so the IoU is $4/14 = 2/7$, twice the continuous value. $(0,0,10,10)$ and $(5,0,15,10)$ give $66 / 176 = 3/8$ instead of $1/3$.
- **Pixel masks.** For two masks of an instance, the IoU counts pixels: 120 shared pixels out of 200 pixels covered by either mask give $0.6$. The [mean IoU](/mean-intersection-over-union/) of semantic segmentation computes this ratio for each class over all pixels of a data set and averages over classes.
- **Not coverage.** The coverage ratios $|A \cap B| / |A|$ (the part of $A$ that $B$ covers) and $|A \cap B| / \min(|A|, |B|)$ are not IoU. For the box $A = (2,2,6,6)$ inside $B = (0,0,10,10)$ both are 1, while the IoU is $16/100 = 4/25$. The deformable part model of Felzenszwalb et al. (2010) suppresses a box when a kept box covers at least half of it, and a reader who takes that rule for an IoU threshold misreads it.
- **Not the Dice coefficient.** The Dice coefficient $2|A \cap B| / (|A| + |B|)$ is an increasing function of IoU, $D = 2J / (1 + J)$, so it ranks pairs in the same order but gives other values: IoU $1/3$ is Dice $1/2$. A threshold on one is not the same number on the other.
- **Disjoint boxes.** $(0,0,1,1)$ and $(2,0,3,1)$ have IoU 0, and so do $(0,0,1,1)$ and $(5,0,6,1)$. IoU does not say how far apart two disjoint boxes are, which is why a loss of $1 - \mathrm{IoU}$ has no gradient for them. The generalized IoU of Rezatofighi et al. subtracts $|C \setminus (A \cup B)| / |C|$, where $C$ is the smallest box that holds both, and gives $-1/3$ and $-2/3$ for these two pairs.

## Related definitions

The [Jaccard similarity](/jaccard-similarity/) is the same ratio for any two finite sets, such as sets of words or shingles; IoU is its name in vision, for regions of the plane. Detection uses IoU in three places. A matching rule calls a predicted box a true positive when its IoU with an unmatched ground-truth box is above a threshold, which [detection mean average precision](/detection-mean-average-precision/) turns into one score per class. [Box non-maximum suppression](/box-non-maximum-suppression/) and [Soft-NMS](/soft-nms/) remove or down-weight a box by its IoU with a box of higher score. Anchor assignment and [bounding box regression](/bounding-box-regression/) pick training targets by IoU. [Mean intersection over union](/mean-intersection-over-union/) is the segmentation metric built from pixel IoU per class.

Boxes that are not axis-aligned, such as rotated boxes, meet in a convex polygon, and their IoU needs a [convex polygon intersection](/convex-polygon-intersection/), which costs $O(m + n)$ for polygons of $m$ and $n$ vertices instead of $O(1)$. The generalized IoU (GIoU) has values in $(-1, 1]$, is equal to IoU when one box holds the other, and $1 - \mathrm{GIoU}$ is also a metric. The Python code of this page computes IoU for boxes in both forms, for pixel sets, the Jaccard distance and GIoU, and its tests compare the box formula with a count of pixel cells.

## References
