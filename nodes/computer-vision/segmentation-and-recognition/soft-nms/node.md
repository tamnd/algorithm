---
tag: CXYXEQ
kind: algorithm
slug: soft-nms
name: Soft-NMS
aliases:
- soft non-maximum suppression
area: computer-vision/segmentation-and-recognition
level: advanced
summary: "Non-maximum suppression that lowers the scores of overlapping boxes by a function of their IoU instead of removing them, which helps with crowded objects."
solves: [object-detection]
model: real-ram
complexity:
  vars: {n: the number of input boxes}
  time: {worst: Θ(n^2), average: O(n^2), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2017
  people: [Navaneeth Bodla, Bharat Singh, Rama Chellappa, Larry S. Davis]
  note: "Bodla, Singh, Chellappa and Davis presented Soft-NMS at ICCV 2017 as a change of one line in the greedy NMS loop that raised the COCO mAP of standard two-stage detectors without retraining."
prereqs: [box-non-maximum-suppression]
see_also: [box-non-maximum-suppression, intersection-over-union, detection-mean-average-precision, object-detection, faster-r-cnn, detr, non-maximum-suppression]
sources:
  - paper: doi:10.1109/ICCV.2017.593
    title: "Navaneeth Bodla, Bharat Singh, Rama Chellappa and Larry S. Davis, Soft-NMS: improving object detection with one line of code, ICCV 2017, 5562-5570"
    locator: "Figure 2, Algorithm 1 (the loop with the hard and the soft rule), the linear and Gaussian rescoring functions and the O(N^2) cost, Section 6 (results on PASCAL VOC 2007 and MS-COCO), Section 6.2 (sensitivity analysis)"
  - url: https://arxiv.org/abs/1704.04503
    title: "Navaneeth Bodla, Bharat Singh, Rama Chellappa and Larry S. Davis, Soft-NMS: improving object detection with one line of code, arXiv:1704.04503, 2017"
    locator: "The preprint of the ICCV paper, with the same Algorithm 1"
  - paper: doi:10.1007/978-3-319-10602-1_48
    title: "Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays, Pietro Perona, Deva Ramanan, Piotr Dollar and C. Lawrence Zitnick, Microsoft COCO: common objects in context, ECCV 2014, LNCS 8693, 740-755"
    locator: "The COCO data set and its detection task, on which the gains of Soft-NMS are reported"
  - url: https://arxiv.org/abs/1705.02950
    title: "Jan Hosang, Rodrigo Benenson and Bernt Schiele, Learning non-maximum suppression, CVPR 2017"
    locator: "A network that learns the suppression step, an alternative to a fixed rescoring rule"
---

Soft-NMS is a change to greedy [non-maximum suppression for detections](/box-non-maximum-suppression/). Greedy NMS removes every box whose [intersection over union](/intersection-over-union/) with a kept box is above a threshold; Soft-NMS keeps the box and multiplies its score by a decay that gets smaller as the overlap grows. A second object that stands close behind the first one then stays in the output with a lower score instead of being lost. Bodla, Singh, Chellappa and Davis (2017) describe it as a change of one line in the NMS loop, and it needs no retraining of the detector.

## In plain words

A detector gives many scored boxes, several around each object. Greedy NMS keeps the best box and throws away every box that overlaps it a lot. When two people stand close together, the box of the second person overlaps the box of the first, and greedy NMS throws it away too.

Soft-NMS does not throw boxes away. It keeps the best box, then lowers the score of every other box: a little for a small overlap, a lot for a large overlap. Then it takes the box with the highest new score, and so on. A duplicate of the first person sits almost on top of the first box, so its score drops close to zero. The second person overlaps less, so its box keeps a useful score. The output is all boxes with new scores, and a final score threshold removes the ones that are left with almost nothing.

## The problem

The input is $n$ boxes $B_1, \ldots, B_n$ with scores $s_1, \ldots, s_n \ge 0$, a decay function $f$ with values in $[0, 1]$, and a pruning threshold $s_{\min} \ge 0$. The output is a list of pairs (index, new score) in the order in which the loop selects them. Detection uses this list to compute [detection mean average precision](/detection-mean-average-precision/), which only looks at the order of the boxes by score and at their positions. Bodla et al. give three rules for $f$, with $o$ the IoU of a box and the box just selected:

- **hard**: $f(o) = 1$ for $o < N_t$ and $0$ for $o \ge N_t$, which is greedy NMS;
- **linear**: $f(o) = 1$ for $o < N_t$ and $1 - o$ for $o \ge N_t$;
- **Gaussian**: $f(o) = e^{-o^2 / \sigma}$.

The linear rule jumps at $N_t$ from 1 to $1 - N_t$; the Gaussian rule is smooth and decays every overlapping box, even one with a small overlap.

## The algorithm

```pseudo id=main
SOFT-NMS(B, s, f, s_min)                       ▷ n = |B|
L1  D ← empty list, S ← copy of s, R ← {1, ..., n}
L2  while R is not empty do
L3      m ← the index in R with the largest S_m, ties by the smaller index
L4      remove m from R and append (m, S_m) to D
L5      for each i in R do
L6          o ← IoU(B_m, B_i)
L7          S_i ← S_i · f(o)
L8          if S_i < s_min then remove i from R
L9  return D
```

Line L7 is the one line that differs from greedy NMS. With the hard rule, a box with $o \ge N_t$ gets the score 0 and line L8 removes it, which is the removal step of greedy NMS. A small $s_{\min}$ makes sure that boxes with almost no score do not stay in the loop.

## Example

Take the five boxes of the [box NMS page](/box-non-maximum-suppression/), with the linear rule and $N_t = 0.3$:

| box | corners | score |
|---|---|---|
| 1 | $(0, 0, 10, 10)$ | 0.90 |
| 2 | $(1, 1, 11, 11)$ | 0.80 |
| 3 | $(6, 0, 16, 10)$ | 0.75 |
| 4 | $(20, 20, 30, 30)$ | 0.60 |
| 5 | $(7, 1, 17, 11)$ | 0.50 |

The IoU values are $\mathrm{IoU}(B_1, B_2) = \mathrm{IoU}(B_3, B_5) = 81/119 \approx 0.681$, $\mathrm{IoU}(B_1, B_3) = \mathrm{IoU}(B_2, B_5) = 1/4$, $\mathrm{IoU}(B_2, B_3) = 9/31 \approx 0.290$ and $\mathrm{IoU}(B_1, B_5) = 27/173 \approx 0.156$, and box 4 does not touch any other box.

| step | selected (L3) | its score | changes in L7 |
|---|---|---|---|
| 1 | box 1 | 0.90 | box 2: $0.681 \ge 0.3$, $0.80 \cdot (1 - 81/119) = 152/595 \approx 0.2555$; boxes 3, 4, 5 are below $N_t$ and keep their scores |
| 2 | box 3 | 0.75 | box 5: $0.681 \ge 0.3$, $0.50 \cdot 38/119 = 19/119 \approx 0.1597$; box 2: $0.290 < 0.3$, no change |
| 3 | box 4 | 0.60 | no overlaps |
| 4 | box 2 | 0.2555 | box 5: $0.25 < 0.3$, no change |
| 5 | box 5 | 0.1597 | |

The output order is $1, 3, 4, 2, 5$ with nonincreasing scores. Greedy NMS with the same threshold, which is the hard rule, keeps only boxes 1, 3 and 4. The Gaussian rule with $\sigma = 0.5$ gives the same order with the scores $0.90$, $0.75 \cdot e^{-0.125} \approx 0.6619$, $0.60$, $0.2676$ and $0.1664$. Here box 3 loses some score although its overlap with box 1 is only 0.25.

## Correctness

Soft-NMS has no optimality claim; it is a rescoring rule, and its value is measured by benchmark. What can be proved is what it outputs. The correctness file shows four facts. The loop stops after at most $n$ rounds and outputs each box at most once. The score that a box has when it is selected is $s_i \prod f(o(B_m, B_i))$ over the boxes $m$ selected before it, so the result does not depend on how the loop stores the scores. The output scores are nonincreasing, because the selected box has the largest current score and the decay never raises a score. With the hard rule and $0 < s_{\min} \le \min_i s_i$, the selected boxes are exactly the output of greedy NMS with the test $o \ge N_t$. The tests check the closed form and the equality with greedy NMS on random inputs, and compare the code with a slow version that recomputes every score from the closed form.

## Complexity

Each round scans the remaining set twice, once to find the maximum in line L3 and once in lines L5 to L8. With $s_{\min} = 0$ and the Gaussian rule nothing is pruned, so the rounds visit $n - 1, n - 2, \ldots, 0$ boxes and evaluate $n(n-1)/2$ IoU values: $\Theta(n^2)$ in the [real RAM](/real-ram/), the same order as the worst case of greedy NMS. The paper states the cost as $O(N^2)$. The best case is the hard rule with one box that removes all others, $\Theta(n)$. A heap would make line L3 cheaper, but the scores of many boxes change in each round and the loop of line L5 is already linear, so it does not change the order of the cost. The extra space is the copy of the scores and the remaining set, $\Theta(n)$.

## Properties

- **Deterministic.** With the tie rule fixed, the output is a function of the input.
- **Keeps the order of the best box.** The first box of the output is the box with the highest input score, with its score unchanged.
- **Nonincreasing output scores**, a theorem for any decay with values in $[0, 1]$.
- **Generalizes greedy NMS.** The hard rule gives greedy NMS with the test "at least $N_t$".
- **No retraining.** The rule acts on the outputs of a trained detector, so it can be added to an existing system at test time.
- **Changes scores, not boxes.** The boxes are not moved or merged. Methods that average coordinates of overlapping boxes are a different family.
- **Every box can stay.** With $s_{\min} = 0$ and the Gaussian rule the output has all $n$ boxes, so a score threshold or a top-$k$ cut must follow if the application needs a short list.

## Variants and improvements

- **Linear or Gaussian.** The paper uses $N_t = 0.3$ for the linear rule and $\sigma = 0.5$ for the Gaussian rule, and Section 6.2 studies how the results change with these parameters. They are tuned values for the benchmarks of the paper, not values that follow from a theory.
- **Class-aware runs.** As with greedy NMS, the loop runs once for each class.
- **Learned suppression.** Hosang, Benenson and Schiele (2017) train a network to rescore the boxes, which learns the step that Soft-NMS fixes by hand.
- **NMS-free detectors.** [DETR](/detr/) and other set-prediction detectors are trained with a one-to-one matching and need neither greedy NMS nor Soft-NMS.

## When to use it

Use Soft-NMS in place of greedy NMS when the score that matters is an average precision over many recall levels, such as COCO mAP, and when objects of the same class overlap, as in crowds, traffic or animal herds. The gain is a benchmark result, not a guarantee. Bodla et al. (2017) report on the MS-COCO test-dev set, with the COCO mAP averaged over IoU 0.5 to 0.95, gains of 1.3 points for R-FCN and 1.1 points for [Faster R-CNN](/faster-r-cnn/), and gains of 1.7 points for both on PASCAL VOC 2007 with the same metric. Keep greedy NMS when the next stage needs a short list with no near-duplicates, for example to count objects, because Soft-NMS leaves the duplicates in the output with low scores.

## Pitfalls

- **Forgetting the final threshold.** Soft-NMS keeps more boxes. A system that drew every output box would show many faint duplicates, so a score cut must follow for display or counting.
- **Comparing with the wrong threshold.** The hard rule here uses "at least $N_t$", and many NMS codes use "greater than"; the two differ only at the threshold, but a comparison on integer boxes can hit it.
- **Pruning too early.** A large $s_{\min}$ throws away boxes that the decay would have kept, and with the hard rule any $s_{\min}$ above a box's input score removes that box before it can compete.
- **Using it to fix a poor detector.** Soft-NMS reorders the boxes that the detector produced. It cannot add a box that the detector missed, and it does not move a badly placed box.
- **Floating-point ties.** Two programs that multiply the same decays in a different order can get scores that differ in the last bits, and then break a tie in the other direction.

## Implementations

The Python code gives the loop of the page with the three rules, a decay function as a parameter, and a pruning threshold. It also has a slow reference that recomputes every score from the closed form, and greedy NMS with the test "at least $N_t$" for comparison. The tests check the example of this page with exact fractions, the equality of the hard rule with greedy NMS on random inputs with tied scores, the agreement with the reference for the linear and Gaussian rules, the order of the output scores, a crowd case in which only Soft-NMS keeps the second object, and the count of $n(n-1)/2$ IoU values when nothing is pruned.

## History

Greedy NMS with a fixed IoU threshold had been the last step of almost every detector for years, and its loss of recall in crowds was known. Bodla, Singh, Chellappa and Davis (2017) observed that the removal step can be read as a score decay that is a step function of the overlap, and replaced it with a continuous one. The paper, titled "improving object detection with one line of code", appeared at ICCV 2017 with code for the detectors of that time, and the method was added to many detection libraries. The same year, Hosang, Benenson and Schiele proposed to learn the suppression step. Set-prediction detectors such as DETR (2020) later removed the need for a suppression step altogether.

## References
