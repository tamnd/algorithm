---
tag: TXWACJ
kind: definition
slug: clear-mot-metrics
name: CLEAR MOT metrics
aliases:
- MOTA
- MOTP
area: computer-vision/visual-tracking
level: core
summary: MOTA counts misses, false positives and identity switches against the number of objects, and MOTP averages the localization error of matched pairs.
prereqs: [multi-object-tracking, intersection-over-union, hungarian-algorithm]
see_also: [idf1-score, hota-metric, multi-object-tracking, precision-and-recall, assignment-problem, sort-tracker, bytetrack, tracking-by-detection]
sources:
  - paper: doi:10.1155/2008/246309
    title: "Keni Bernardin and Rainer Stiefelhagen, Evaluating multiple object tracking performance: the CLEAR MOT metrics, EURASIP Journal on Image and Video Processing 2008, article 246309"
    locator: "the whole paper (the frame by frame mapping of hypotheses to objects, the counting of mismatches, and the definitions of MOTP and MOTA)"
  - paper: arxiv:1603.00831
    title: "Anton Milan, Laura Leal-Taixe, Ian Reid, Stefan Roth and Konrad Schindler, MOT16: a benchmark for multi-object tracking, arXiv:1603.00831, 2016"
    locator: "Section IV-A1 (the kept correspondences and the switches against the last known match), Section IV-A2 (the IoU threshold 0.5), Section IV-A4, Eq. 1 (MOTA) and Section IV-A5, Eq. 2 (MOTP)"
  - paper: arxiv:1609.01775
    title: "Ergys Ristani, Francesco Solera, Roger S. Zou, Rita Cucchiara and Carlo Tomasi, Performance measures and a data set for multi-target, multi-camera tracking, ECCV 2016 Workshops, 17-35"
    locator: "the discussion of the measures based on events, such as MOTA, compared with the identity measures"
  - paper: arxiv:2009.07736
    title: "Jonathon Luiten, Aljosa Osep, Patrick Dendorfer, Philip Torr, Andreas Geiger, Laura Leal-Taixe and Bastian Leibe, HOTA: a higher order metric for evaluating multi-object tracking, International Journal of Computer Vision 129(2), 2021, 548-578"
    locator: "Section 4.1 (MOTA in the notation of HOTA) and Section 9.1 (the problems of MOTA, among them that detection outweighs association and that a switch looks only at the previous match)"
---

The CLEAR MOT metrics are two numbers that score the output of a [multi-object tracker](/multi-object-tracking/) against a ground truth. In each frame, the tracker's hypotheses are matched one to one with the true objects. MOTA, the multiple object tracking accuracy, counts three kinds of errors over the whole video: missed objects, false positives and identity switches, and divides their sum by the number of true objects. MOTP, the multiple object tracking precision, is the mean localization quality of the matched pairs. MOTA weighs detection errors much more than identity errors, which is the weakness that the [IDF1 score](/idf1-score/) and [HOTA](/hota-metric/) address.

## Definition

The ground truth gives, for each frame $t$, a set of objects $o$ with boxes, and the tracker gives a set of hypotheses $h$ with boxes; an identity stays the same over the frames. A similarity $s(o, h)$, here the [intersection over union](/intersection-over-union/) of the boxes, and a threshold $T$ decide when a pair is *valid*: $s(o, h) \ge T$. The MOT16 benchmark, on boxes, uses $T = 0.5$. The original paper also allows a distance, such as the distance of two points on the ground, with a pair valid when the distance is below a threshold.

The matching is made frame by frame, and it remembers the matches of the frame before:

```pseudo id=main
CLEAR-MOT(the objects and the hypotheses of each frame, the threshold T)
L1  for each frame t:
L2      keep each match (o, h) of frame t - 1 when o and h are present and s(o, h) ≥ T
L3      match the other objects and hypotheses: the most valid pairs, then the largest total s
L4      for each match (o, h): if o was last matched to some h' ≠ h, count an identity switch
L5      count the misses (unmatched objects), the false positives (unmatched hypotheses) and the matches
L6  MOTA ← 1 - (FN + FP + IDSW) / GT;   MOTP ← (sum of s over all matches) / (number of matches)
```

Line L2 keeps a match even when another hypothesis is closer, as the MOT16 protocol states. Line L3 is an [assignment problem](/assignment-problem/), solved with the [Hungarian algorithm](/hungarian-algorithm/). Implementations differ in how they weigh the number of pairs against the total similarity; this page takes the most pairs first. The *last* match of line L4 may be from any earlier frame, so an object that is missed for some frames and then found again by the same hypothesis gives no switch. With $\mathrm{GT}_t$ the number of objects in frame $t$, $\mathrm{FN}_t$, $\mathrm{FP}_t$ and $\mathrm{IDSW}_t$ the counts of the frame, $c_t$ the number of matches and $s_{t,i}$ the similarity of match $i$,

$$\mathrm{MOTA} = 1 - \frac{\sum_t (\mathrm{FN}_t + \mathrm{FP}_t + \mathrm{IDSW}_t)}{\sum_t \mathrm{GT}_t}, \qquad \mathrm{MOTP} = \frac{\sum_{t,i} s_{t,i}}{\sum_t c_t}.$$

With a distance instead of a similarity, MOTP is the mean distance of the matches, and lower is better. These facts follow from the definition and are proved in the correctness file of this page:

- **Theorem: the counts add up.** In every frame, the matches plus the misses equal the objects, and the matches plus the false positives equal the hypotheses. The switches are at most the matches.
- **Theorem: the range.** $\mathrm{MOTA} \le 1$, with equality exactly when there are no errors. MOTA has no lower bound: false positives can make it as negative as we like. With overlap, $T \le \mathrm{MOTP} \le 1$.
- **Theorem: the matching of line L3 is optimal.** It has the most valid pairs among the remaining objects and hypotheses, and among those the largest total similarity.

## Examples and non-examples

- **A small sequence.** Two objects move to the right by 2 pixels per frame, from the boxes $(0,0,10,10)$ and $(20,0,30,10)$. In frame 1 the hypotheses are $a = (1,0,11,10)$ with IoU $9/11$ to object 1, $b$ exactly on object 2, and $c = (50,50,60,60)$ on nothing. In frame 2 only $b$ is there, exactly on object 2, so object 1 is missed. In frame 3 a new hypothesis $d$ is exactly on object 1, and $b = (25,0,35,10)$ has IoU $9/11$ to object 2. The counts are 6 objects, 5 matches, 1 miss (frame 2), 1 false positive ($c$) and 1 identity switch (object 1 goes from $a$ to $d$). So $\mathrm{MOTA} = 1 - 3/6 = 1/2$ and $\mathrm{MOTP} = (9/11 + 1 + 1 + 1 + 9/11) / 5 = 51/55 \approx 0.93$.
- **Keeping the last match.** An object at $(0,0,10,10)$ is matched to $h$ in frame 1. In frame 2, $h$ is at $(3,0,13,10)$ with IoU $7/13 \ge 0.5$, and a second hypothesis $g$ at $(1,0,11,10)$ has the better IoU $9/11$. Line L2 keeps $(o, h)$, so $g$ is a false positive and there is no switch: MOTA is $1/2$. A matching without line L2 would take $g$, count a switch and a false positive, and give MOTA 0. Line L2 is what keeps a correct track from being punished for a better box nearby.
- **Negative MOTA.** One object over 3 frames, found in each frame, and 3 false positives in each frame: $\mathrm{MOTA} = 1 - 9/3 = -2$. MOTA is not a fraction of correct answers.
- **Not a measure of identity.** One object over 100 frames. Tracker A follows it with hypothesis $a$ for 50 frames and then with $b$ for 50 frames: one switch, $\mathrm{MOTA} = 0.99$. Tracker B finds it in all 100 frames with the same identity, but adds one false positive: also $\mathrm{MOTA} = 0.99$. The [IDF1 score](/idf1-score/) of tracker A is $1/2$, and that of B is $200/201$.
- **Not a mean over frames.** MOTA sums the errors over the whole video before it divides, so frames with many objects weigh more. A per-frame average of $1 - \text{errors}_t / \mathrm{GT}_t$ is a different number.

## Related definitions

MOTA is built from the same counts as [precision and recall](/precision-and-recall/) of detections: with $\mathrm{TP}$ the matches, $\mathrm{FN} = \mathrm{GT} - \mathrm{TP}$ and $\mathrm{FP} = \mathrm{H} - \mathrm{TP}$, the score without switches is $1 - (\mathrm{FN} + \mathrm{FP})/\mathrm{GT}$. Identity enters only through switches, which are events in single frames, so a tracker that keeps a wrong identity for a long time pays only once. The [IDF1 score](/idf1-score/) instead matches whole trajectories once for the full video and counts the frames that agree with that match. [HOTA](/hota-metric/) combines a detection score and an association score with equal weight, and averages over the threshold $T$. The papers of [SORT](/sort-tracker/) and [Deep SORT](/deep-sort/) report MOTA and MOTP; the paper of [ByteTrack](/bytetrack/) reports MOTA, IDF1 and HOTA. The Python code of this page computes MOTA and MOTP with exact fractions, and its tests check the matching of line L3 against all matchings, and the whole procedure against a version that uses that brute force matching in every frame.

## References
