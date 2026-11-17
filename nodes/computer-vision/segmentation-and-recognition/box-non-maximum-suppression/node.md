---
tag: 5JRR0P
kind: algorithm
slug: box-non-maximum-suppression
name: Non-maximum suppression for detections
aliases:
- greedy NMS
- box NMS
area: computer-vision/segmentation-and-recognition
level: core
summary: "Sort detections by score, keep the best, drop every remaining box whose IoU with it exceeds a threshold, and repeat on what is left."
solves: [object-detection]
model: real-ram
complexity:
  vars: {n: the number of input boxes, k: the number of kept boxes}
  time: {worst: Θ(n^2), average: O(n log n + k n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2005
  people: [Navneet Dalal, Bill Triggs, Pedro F. Felzenszwalb, Ross Girshick]
  note: "Detectors of the 1990s and 2000s merged overlapping windows in many ad hoc ways. Dalal and Triggs (2005) call greedy suppression conventional, Felzenszwalb et al. (2010) use a greedy rule with a coverage overlap, and R-CNN (2014) fixes the IoU form used today."
prereqs: [intersection-over-union]
see_also: [soft-nms, non-maximum-suppression, sliding-window-detection, object-detection, detection-mean-average-precision, dalal-triggs-detector, detr, greedy-algorithm]
sources:
  - paper: doi:10.1109/TPAMI.2009.167
    title: "Pedro F. Felzenszwalb, Ross B. Girshick, David McAllester and Deva Ramanan, Object detection with discriminatively trained part-based models, IEEE Transactions on Pattern Analysis and Machine Intelligence 32(9), 2010, 1627-1645"
    locator: "Section 7.2, Non-maximum suppression (greedy, skipping a box that is at least 50 percent covered by a box already selected)"
  - paper: doi:10.1109/CVPR.2014.81
    title: "Ross Girshick, Jeff Donahue, Trevor Darrell and Jitendra Malik, Rich feature hierarchies for accurate object detection and semantic segmentation, CVPR 2014, 580-587"
    locator: "Section 2.2, Test-time detection (greedy NMS for each class independently, with an IoU threshold)"
  - paper: doi:10.1109/ICCV.2017.593
    title: "Navaneeth Bodla, Bharat Singh, Rama Chellappa and Larry S. Davis, Soft-NMS: improving object detection with one line of code, ICCV 2017, 5562-5570"
    locator: "Figure 2, Algorithm 1 (the greedy NMS loop and its O(N^2) cost), and Section 2, Related work"
  - paper: doi:10.1109/CVPR.2005.177
    title: "Navneet Dalal and Bill Triggs, Histograms of oriented gradients for human detection, CVPR 2005, vol. 1, 886-893"
    locator: "Figure 1 (the detection chain ends with conventional non-maximum suppression over the pyramid)"
  - url: https://arxiv.org/abs/1904.02689
    title: "Daniel Bolya, Chong Zhou, Fanyi Xiao and Yong Jae Lee, YOLACT: real-time instance segmentation, ICCV 2019"
    locator: "Section 5, Fast NMS (removed boxes may suppress others, computed with matrix operations)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.3, Object detection"
---

Greedy non-maximum suppression (NMS) turns a list of scored detection boxes, in which one object often has many overlapping boxes, into a short list with one box per object. It keeps the box with the highest score, removes every remaining box whose [intersection over union](/intersection-over-union/) with that box is above a threshold, and repeats on the boxes that are left. This page is about boxes; the [non-maximum suppression](/non-maximum-suppression/) of image processing works on pixels instead, and thins edge or corner responses to their local maxima along the gradient or in a window. [Soft-NMS](/soft-nms/) is the variant that lowers the scores of overlapping boxes instead of removing them.

## In plain words

A detector looks at a photo and says "person here" many times around each person, with boxes that are shifted a little and have different confidence values. You want one box per person.

Take the box with the highest confidence and keep it. Throw away every other box that covers almost the same area as the kept box. Then take the most confident box that is still in the pile and do the same. Stop when the pile is empty.

The rule "covers almost the same area" is a number: the shared area divided by the total area of the two boxes. Most detectors throw a box away when this number is above one half. Two people who stand close together can make their boxes overlap that much, and then one of the two people is lost.

## The problem

The input is a list of $n$ boxes $B_1, \ldots, B_n$, each $B_i = (x_1, y_1, x_2, y_2)$ in continuous image coordinates, with scores $s_1, \ldots, s_n$, a threshold $t \in [0, 1]$, and an overlap function $o$, by default $o = \mathrm{IoU}$. Order the indices by decreasing score, with ties broken by the smaller index; say that box $i$ *suppresses* box $j$ when $i$ comes before $j$ in this order and $o(B_i, B_j) > t$. The output is the list $K$ of kept indices, in score order, with two properties: no member of $K$ is suppressed by another member of $K$, and every box outside $K$ is suppressed by a member of $K$. The correctness proof shows that exactly one set has both properties. NMS runs separately for each class in a multi-class detector, so boxes of different classes do not remove each other.

The output is not the best set of boxes for any stated score; it is defined by the greedy order. A problem such as "pick a set of pairwise non-overlapping boxes with the largest total score" is a weighted [maximum independent set](/maximum-independent-set/) in the overlap graph, which is NP-hard in general, and greedy NMS does not solve it.

## The algorithm

```pseudo id=main
GREEDY-NMS(B, s, t)                       ▷ n = |B|
L1  π ← the indices sorted by s, decreasing, ties by index
L2  K ← empty list, removed[1..n] ← false
L3  for each i in π, in order do
L4      if removed[i] then continue
L5      append i to K
L6      for each j after i in π do
L7          if not removed[j] and o(B_i, B_j) > t then
L8              removed[j] ← true
L9  return K
```

Line L7 compares with a strict "greater than". The Soft-NMS paper writes its hard rule with "greater than or equal"; the two differ only for a box exactly at the threshold, but a test with integer boxes can hit that case, so a program must say which one it uses. A box that line L8 removes never removes another box, because line L4 skips it before line L6.

## Example

Take five boxes with $t = 0.5$:

| box | corners | score |
|---|---|---|
| 1 | $(0, 0, 10, 10)$ | 0.90 |
| 2 | $(1, 1, 11, 11)$ | 0.80 |
| 3 | $(6, 0, 16, 10)$ | 0.75 |
| 4 | $(20, 20, 30, 30)$ | 0.60 |
| 5 | $(7, 1, 17, 11)$ | 0.50 |

The scores are distinct, so the order is $1, 2, 3, 4, 5$. The IoU values that matter are $\mathrm{IoU}(B_1, B_2) = 81/119 \approx 0.681$, $\mathrm{IoU}(B_1, B_3) = 40/160 = 0.25$, $\mathrm{IoU}(B_1, B_5) = 27/173 \approx 0.156$ and $\mathrm{IoU}(B_3, B_5) = 81/119 \approx 0.681$. Box 4 does not touch any other box.

| step | line | action | kept | removed |
|---|---|---|---|---|
| 1 | L5 | keep box 1 | 1 | |
| 2 | L7, L8 | box 2: $0.681 > 0.5$, remove | 1 | 2 |
| 3 | L7 | box 3: $0.25$, box 4: $0$, box 5: $0.156$, all stay | 1 | 2 |
| 4 | L4 | box 2 is removed, skip | 1 | 2 |
| 5 | L5, L8 | keep box 3; box 5: $0.681 > 0.5$, remove | 1, 3 | 2, 5 |
| 6 | L5 | keep box 4 | 1, 3, 4 | 2, 5 |
| 7 | L4 | box 5 is removed, skip | 1, 3, 4 | 2, 5 |

The output is $K = (1, 3, 4)$. With $t = 0.2$ the result is $(1, 4, 5)$: box 1 now removes box 3 as well ($0.25 > 0.2$), and box 5, which only box 3 suppressed before, survives with $0.156 < 0.2$. A lower threshold does not always give a subset of the output for a higher threshold.

## Correctness

The proof in the correctness file has two lemmas. First, at the time line L3 reaches box $j$, the flag of $j$ is set exactly when a box already in $K$ that comes before $j$ suppresses it; line L8 is the only place that sets a flag, and the inner loop of each kept box visits every later box. Second, each box is decided once, in score order. Together they give the two properties of the problem statement: no kept box is suppressed by another kept box, and every removed box has a kept suppressor. An induction along the score order then shows that any set with these two properties agrees with $K$ on every box, so the output is unique and does not depend on how the loop is written. The tests compare the code with a search over all subsets of up to 8 boxes. The proof does not use the symmetry of $o$, so it also holds for the coverage overlap of the deformable part model.

## Complexity

The sort of line L1 costs $O(n \log n)$ comparisons. Each kept box runs the loop of lines L6 to L8 over the boxes after it, at most $n - 1$ of them, and one IoU costs $O(1)$ in the [real RAM](/real-ram/). With $k$ kept boxes the time is $O(n \log n + k n)$. The worst case is $\Theta(n^2)$: for $n$ pairwise disjoint boxes every box is kept, and line L7 evaluates all $n(n-1)/2$ pairs. The best case is one box that suppresses all others, with $n - 1$ overlap tests after the sort. Extra space is $\Theta(n)$ for the order and the flags.

In practice $n$ is the number of boxes above a score threshold, often a few thousand before NMS in a modern detector, and implementations cap it with a pre-NMS top-$k$. The cost of the network that makes the boxes is outside this page.

## Properties

- **Deterministic and exact.** With the tie rule fixed, the output is a function of the input, and the code computes it exactly; on integer boxes the IoU is a rational number and the test is exact.
- **The best box always survives.** The first box in the order has no possible suppressor.
- **Kept boxes are pairwise below the threshold** for a symmetric overlap such as IoU, by the first property of the output.
- **Not monotone in the threshold.** The example shows a box that survives at $t = 0.2$ and is removed at $t = 0.5$.
- **Not monotone in the scores of other boxes.** Raising the score of a removed box can make it a suppressor and change which other boxes survive.
- **A hard decision.** A removed box is gone with its score, so a second object behind the first one cannot be recovered by any later step. This costs recall in crowds and is the motivation for Soft-NMS.
- **Order of output.** $K$ is in decreasing score order, which is the input that [detection mean average precision](/detection-mean-average-precision/) needs.

## Variants and improvements

- **Class-aware NMS.** Run the loop once for each class. Many libraries do this in one call by shifting the boxes of each class by a large offset, so that boxes of different classes never overlap.
- **Coverage overlap.** The deformable part model code skips a box when a kept box covers at least 50 percent of it, $|B_i \cap B_j| / |B_j| \ge 0.5$. This removes small boxes inside a large kept box, which IoU does not.
- **Soft-NMS.** [Soft-NMS](/soft-nms/) multiplies the scores of the other boxes by a decay that depends on the IoU, and keeps all boxes with a new order. Its hard rule, a decay to 0 above the threshold, gives back greedy NMS.
- **Fast NMS.** Bolya et al. (2019) let removed boxes suppress others too: a box goes when any box with a higher score overlaps it above $t$. This needs only the upper triangle of the IoU matrix and a column maximum, so it runs as matrix operations on a GPU, and it removes a superset of the boxes that greedy NMS removes.
- **Merging instead of removing.** Viola and Jones average each group of overlapping detections into one box (see [the Viola-Jones detector](/viola-jones-detector/)). Dalal's thesis finds modes with [mean shift](/mean-shift/) in position and scale. Weighted box fusion and similar methods average the coordinates of the removed boxes into the kept one.
- **Learned or removed NMS.** Hosang, Benenson and Schiele (2017) train a network to do the suppression. [DETR](/detr/) predicts a set of boxes with a one-to-one matching loss and needs no NMS at all.

## When to use it

Use greedy NMS after any detector that produces many overlapping boxes per object: a [sliding-window detector](/sliding-window-detection/) such as the [Dalal-Triggs detector](/dalal-triggs-detector/), or a network with dense anchors such as [Faster R-CNN](/faster-r-cnn/) or [YOLO](/yolo-detector/). It is simple, has one parameter, and its cost is small next to the detector. Prefer Soft-NMS when objects of the same class overlap a lot, as with people in a crowd, and a class-aware run whenever boxes of different classes can overlap. When the detector is trained with a one-to-one matching, as in DETR, do not add NMS.

## Pitfalls

- **The threshold is a tuned value.** 0.5 is a convention, and R-CNN describes its value as learned on validation data. A lower value merges nearby objects; a higher value leaves duplicates. Report the value with any benchmark number.
- **Mixed box forms.** A box in the inclusive pixel form of the VOC devkit, with side $x_2 - x_1 + 1$, gives a different IoU from the same four numbers as a continuous box. Small boxes change the most.
- **Strict or non-strict test.** "Greater than" and "greater than or equal" differ on boxes exactly at the threshold, which is common on integer test data.
- **Ties.** Equal scores need a fixed tie rule, or the output depends on the sort routine. An unstable sort can give different results between runs of the same program.
- **Classes.** A class-agnostic run lets a "dog" box remove a "person" box. That may be intended, but say so.
- **Using a removed box as a suppressor.** A loop that removes boxes after the scan, or that compares each box with all earlier boxes instead of the kept ones, computes Fast NMS, not greedy NMS. The example of the tests shows a case where the two differ.
- **Edge NMS for boxes.** The image-processing [non-maximum suppression](/non-maximum-suppression/) keeps a pixel when it is the largest along its gradient direction. It has no boxes and no scores to sort, and it is a different algorithm with the same name.

## Implementations

The Python code takes boxes as tuples, scores and a threshold, and returns the kept indices in score order, with the tie rule of the page and an optional overlap function. It includes class-aware NMS, the coverage overlap of the deformable part model, Fast NMS for comparison, and a check of the two properties. The tests compare the output with a search over all subsets on random instances with many tied scores, check the example of this page with exact fractions, and count the $n(n-1)/2$ overlap tests of the worst case.

## History

Face and people detectors of the 1990s and early 2000s all had to merge the many windows that fire around one object, and each paper used its own rule: grouping of overlapping windows, averaging, or mode finding. Dalal and Triggs (2005) describe the end of their detection chain as conventional non-maximum suppression over the pyramid, and Dalal's thesis replaces it with mean-shift fusion. Felzenszwalb, Girshick, McAllester and Ramanan (2010) state the greedy rule exactly, with the coverage overlap, in the paper on the [deformable part model](/deformable-part-model/). Girshick et al. (2014) use the IoU form for each class in [R-CNN](/r-cnn/), and the code of the R-CNN family made it the default. Bodla et al. (2017) replaced the hard decision with a score decay, and Bolya et al. (2019) made a parallel variant. The name comes from the edge thinning step of edge detectors, which keeps only local maxima of the gradient magnitude.

## References
