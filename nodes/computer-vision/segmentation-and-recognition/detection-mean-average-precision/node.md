---
tag: ZNZ16Q
kind: definition
slug: detection-mean-average-precision
name: Mean average precision for detection
aliases:
- detection mAP
- COCO mAP
area: computer-vision/segmentation-and-recognition
level: core
summary: "For each class, the area under the precision-recall curve of detections matched to objects at an IoU threshold, averaged over classes and often over thresholds."
prereqs: [intersection-over-union, precision-and-recall]
see_also: [mean-average-precision, interpolated-precision-recall-curve, object-detection, box-non-maximum-suppression, soft-nms, mean-intersection-over-union, faster-r-cnn, dalal-triggs-detector]
sources:
  - paper: doi:10.1007/s11263-009-0275-4
    title: "Mark Everingham, Luc Van Gool, Christopher K. I. Williams, John Winn and Andrew Zisserman, The PASCAL Visual Object Classes (VOC) challenge, International Journal of Computer Vision 88(2), 2010, 303-338"
    locator: "Section 4.2, Eq. (1) and (2) (11-point interpolated AP), Eq. (3) (overlap above 50 percent), the rule that extra detections of one object are false positives, and Section 6.2.3 (the effect of the overlap threshold)"
  - paper: doi:10.1007/s11263-014-0733-5
    title: "Mark Everingham, S. M. Ali Eslami, Luc Van Gool, Christopher K. I. Williams, John Winn and Andrew Zisserman, The PASCAL Visual Object Classes challenge: a retrospective, International Journal of Computer Vision 111(1), 2015, 98-136"
    locator: "Section 2.4 (from 2010 on, AP uses all data points instead of 11 recall levels)"
  - paper: doi:10.1007/978-3-319-10602-1_48
    title: "Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays, Pietro Perona, Deva Ramanan, Piotr Dollar and C. Lawrence Zitnick, Microsoft COCO: common objects in context, ECCV 2014, LNCS 8693, 740-755"
    locator: "The COCO data set and its detection task"
  - url: https://cocodataset.org/#detection-eval
    title: "COCO consortium, Detection evaluation"
    locator: "The 12 metrics: AP averaged over IoU 0.50:0.05:0.95, AP at 0.50 and 0.75, the area ranges below 32^2 and above 96^2, at most 100 detections per image, and no distinction between AP and mAP"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.3, Object detection (precision, recall and average precision for detectors)"
---

Mean average precision (mAP) for detection is one number that scores a program that finds objects in images and reports each one as a box with a class name and a confidence. For each class, the reports are sorted by confidence and each is judged right or wrong, which gives a [precision and recall](/precision-and-recall/) value after every report; the average precision (AP) is the area under this precision-recall curve, and mAP is the mean of AP over the classes. What makes the detection version different from the [mean average precision](/mean-average-precision/) of information retrieval is the judging step: a reported box counts as right only if its [intersection over union](/intersection-over-union/) with a true object box is above a threshold and no better-ranked box has already claimed that object. PASCAL VOC uses one threshold, 0.5, and COCO averages over ten thresholds from 0.5 to 0.95.

## Definition

The input for one class is a list of detections $d_1, \ldots, d_M$, each with an image, a score and a box, and a set $G$ of ground-truth boxes of that class in the same images. Let $N = |G|$. The VOC rule is:

```pseudo id=main
DETECTION-AP(D, G, τ)                       ▷ one class, VOC matching
L1  sort D by score, decreasing, ties by input order
L2  used[g] ← false for every g in G; tp ← 0; fp ← 0
L3  for k ← 1 to |D| do
L4      g ← the box of G in the image of d_k with the largest IoU with d_k
L5      if g exists and IoU(d_k, g) > τ and not used[g] then used[g] ← true; tp ← tp + 1
L6      else fp ← fp + 1
L7      P_k ← tp / (tp + fp); R_k ← tp / N
L8  p_interp(r) ← max{P_k : R_k ≥ r}, and 0 if no k has R_k ≥ r
L9  return Σ_k (R_k - R_{k-1}) · p_interp(R_k)        ▷ R_0 = 0
```

Line L5 is where the boxes enter. A second detection of an object that is already matched is a false positive, so five detections of one object give one true positive and four false positives. The VOC development kit also has "difficult" objects; a detection that matches one is ignored, and these objects are not counted in $N$.

Line L8 makes the curve monotone: the precision at recall $r$ is replaced by the best precision at any recall of at least $r$. The [interpolated precision-recall curve](/interpolated-precision-recall-curve/) of retrieval uses the same rule. The sum of line L9 is the area under this staircase. Three versions of AP are in use, and they give different numbers for the same detections:

- **VOC 2007, 11 points.** $\mathrm{AP} = \frac{1}{11} \sum_{r \in \{0, 0.1, \ldots, 1\}} p_{\mathrm{interp}}(r)$, Eq. (1) and (2) of Everingham et al. (2010).
- **VOC 2010 and later, all points.** The area of line L9. Since recall grows by $1/N$ at each true positive, this is the mean over the $N$ objects of the best precision at or after the rank where the object is found, with 0 for a missed object.
- **COCO, 101 points.** The mean of $p_{\mathrm{interp}}$ at $r \in \{0, 0.01, \ldots, 1\}$. The COCO code also changes the matching: a detection takes the unmatched ground-truth box with the largest IoU among those with IoU of at least $\tau$, so an already matched object does not block a detection that also overlaps another object.

mAP is the mean of AP over the classes. The COCO metric "AP" is the mean over the classes and over the ten thresholds $\tau = 0.50, 0.55, \ldots, 0.95$; COCO writes AP for what other papers call mAP, and also reports AP at $\tau = 0.5$ and $0.75$, AP for small (area below $32^2$ pixels), medium and large (above $96^2$) objects, and keeps at most 100 detections per image.

The value is in $[0, 1]$ and depends only on the order of the scores, not on their values (both are proved in the correctness file). AP is 1 exactly when every object is found and every false positive is ranked after the last true positive. The thresholds 0.5 and 0.5 to 0.95 are conventions of the benchmarks. The VOC paper calls the 50 percent threshold deliberately low and studies other values in Section 6.2.3.

## Examples and non-examples

- **A small example.** Image A has the objects $(0,0,10,10)$ and $(20,0,30,10)$, and image B has $(0,0,10,10)$, so $N = 3$. The detections, by score, are a box $(1,0,11,10)$ in A (IoU $9/11$ with the first object, a true positive), a box $(0,1,10,11)$ in A (IoU $9/11$ with the same object, which is used, so a false positive), a box $(0,0,9,10)$ in B (IoU $9/10$, a true positive), a box $(24,0,34,10)$ in A (IoU $3/7 < 0.5$ with the second object, a false positive) and a box far from everything in B (a false positive). The precisions are $1, 1/2, 2/3, 1/2, 2/5$ and the recalls $1/3, 1/3, 2/3, 2/3, 2/3$. The all-point AP is $\frac{1}{3} \cdot 1 + \frac{1}{3} \cdot \frac{2}{3} = 5/9 \approx 0.556$; the 11-point AP is $(4 \cdot 1 + 3 \cdot \frac{2}{3}) / 11 = 6/11 \approx 0.545$; the 101-point AP is $(34 + 33 \cdot \frac{2}{3}) / 101 = 56/101 \approx 0.554$.
- **The same example in COCO.** For $\tau$ from 0.50 to 0.80 the labels do not change and AP is $56/101$. At 0.85 and 0.90 only the detection with IoU $9/10$ is a true positive, at rank 3, and AP is $34/303 \approx 0.112$; at 0.90 it still counts because COCO tests "at least $\tau$" while VOC tests "above $\tau$". At 0.95 AP is 0. The COCO AP is the mean of the ten values, $622/1515 \approx 0.411$, much lower than the VOC value because the boxes are only roughly right.
- **The matching rules differ.** Two objects $(0,0,10,10)$ and $(2,0,12,10)$ overlap with IoU $2/3$. A detection $(1,0,11,10)$ with the higher score has IoU $9/11$ with both and takes the first. A second detection $(0,0,10,10)$ has IoU 1 with the first object and $2/3$ with the second. VOC sends it to the first object, which is used, so it is a false positive and AP is $1/2$; COCO sends it to the second object and AP is 1.
- **Not accuracy.** True negatives do not appear anywhere: there is no fixed set of "non-objects". A detector that adds many low-score false positives after its last true positive does not lose any AP.
- **Not the retrieval mAP of one query.** In retrieval a document is relevant or not by itself. Here a box is right or wrong only after the matching, and its label depends on the boxes ranked before it.
- **Not mean IoU.** The [mean intersection over union](/mean-intersection-over-union/) of semantic segmentation averages a pixel ratio over classes and has no ranking at all.

## Related definitions

[Precision and recall](/precision-and-recall/) and the [interpolated precision-recall curve](/interpolated-precision-recall-curve/) are the parts from which AP is built, and the [mean average precision](/mean-average-precision/) of retrieval is the same average over a ranking with relevance given in advance. The IoU threshold and the matching come from [object detection](/object-detection/) benchmarks. Since mAP depends only on the ranking, the last step of a detector matters: [box non-maximum suppression](/box-non-maximum-suppression/) removes duplicates that would be false positives, and [Soft-NMS](/soft-nms/) instead moves them down the ranking, which can raise AP because a second object near the first is no longer lost. DET curves of miss rate against false positives per window, used by the [Dalal-Triggs detector](/dalal-triggs-detector/), and miss rate against false positives per image, used for pedestrians, are other summaries of the same detections.

The Python code of this page gives both matching rules, the three AP versions and the COCO average over thresholds, all with exact fractions. Its tests check the example above, compare the all-point AP with the mean over objects of the best later precision, check that only the order of the scores matters, and check that the COCO true positives never exceed a maximum matching found by search.

## References
