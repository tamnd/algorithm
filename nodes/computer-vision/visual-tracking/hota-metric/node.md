---
tag: SAT5C8
kind: definition
slug: hota-metric
name: Higher order tracking accuracy
aliases:
- HOTA
area: computer-vision/visual-tracking
level: research
summary: The geometric mean of detection accuracy and association accuracy, averaged over localization thresholds, which weighs detection and association evenly.
prereqs: [multi-object-tracking, intersection-over-union, jaccard-similarity]
see_also: [clear-mot-metrics, idf1-score, multi-object-tracking, jaccard-similarity, hungarian-algorithm, precision-and-recall, bytetrack, data-association]
sources:
  - paper: doi:10.1007/s11263-020-01375-2
    title: "Jonathon Luiten, Aljosa Osep, Patrick Dendorfer, Philip Torr, Andreas Geiger, Laura Leal-Taixe and Bastian Leibe, HOTA: a higher order metric for evaluating multi-object tracking, International Journal of Computer Vision 129(2), 2021, 548-578"
    locator: "Section 5 (TPA, FNA and FPA, Eq. 10 to 12; HOTA_alpha, Eq. 13 and 14; the matching score, Eq. 15; the mean over 19 thresholds, Eq. 16), Section 6 (LocA, DetA and AssA, Eq. 17 to 19; HOTA_alpha as the geometric mean, Eq. 21; the recall and precision parts, Eq. 22 to 27), Section 7 (detection against trajectory matching), Section 9.1 (the problems of MOTA)"
  - paper: doi:10.1155/2008/246309
    title: "Keni Bernardin and Rainer Stiefelhagen, Evaluating multiple object tracking performance: the CLEAR MOT metrics, EURASIP Journal on Image and Video Processing 2008, article 246309"
    locator: "the definition of MOTA, which HOTA is compared with"
  - paper: arxiv:1609.01775
    title: "Ergys Ristani, Francesco Solera, Roger S. Zou, Rita Cucchiara and Carlo Tomasi, Performance measures and a data set for multi-target, multi-camera tracking, ECCV 2016 Workshops, 17-35"
    locator: "Section 3.4 (IDF1, which HOTA is compared with)"
---

HOTA, higher order tracking accuracy, scores a [multi-object tracker](/multi-object-tracking/) with one number that gives the same weight to finding the objects and to keeping their identities. For a localization threshold $\alpha$, it matches the detections frame by frame and computes two parts. The detection accuracy DetA is the [Jaccard index](/jaccard-similarity/) of the detections: true positives over true positives plus misses plus false positives. The association accuracy AssA is the mean, over the true positives, of a Jaccard index of the two whole trajectories that the true positive links. $\mathrm{HOTA}_\alpha$ is the geometric mean of the two, and HOTA averages it over 19 thresholds from 0.05 to 0.95. Luiten et al. published it in 2021 as a balance between [MOTA](/clear-mot-metrics/), which is ruled by detection, and the [IDF1 score](/idf1-score/), which is ruled by one global matching of trajectories.

## Definition

The ground truth and the tracker give, in each frame, detections with an identity and a box; a similarity $S \in [0, 1]$ of two boxes is usually the [intersection over union](/intersection-over-union/). Fix $\alpha \in (0, 1)$. In each frame, a one-to-one matching of true to predicted detections with $S \ge \alpha$ gives the true positives TP; the other true detections are the misses FN, and the other predicted ones the false positives FP. For a true positive $c$ with the true identity $g$ and the predicted identity $p$:

- $\mathrm{TPA}(c)$ is the set of true positives with the same pair of identities $(g, p)$;
- $\mathrm{FNA}(c)$ is the set of true detections of $g$ that are not matched to $p$: true positives with another predicted identity, and misses;
- $\mathrm{FPA}(c)$ is the set of predicted detections of $p$ that are not matched to $g$: true positives with another true identity, and false positives.

$$\mathcal{A}(c) = \frac{|\mathrm{TPA}(c)|}{|\mathrm{TPA}(c)| + |\mathrm{FNA}(c)| + |\mathrm{FPA}(c)|}, \qquad \mathrm{HOTA}_\alpha = \sqrt{\frac{\sum_{c \in \mathrm{TP}} \mathcal{A}(c)}{|\mathrm{TP}| + |\mathrm{FN}| + |\mathrm{FP}|}}, \qquad \mathrm{HOTA} = \frac{1}{19} \sum_{\alpha \in \{0.05, 0.10, \ldots, 0.95\}} \mathrm{HOTA}_\alpha.$$

The parts are $\mathrm{DetA}_\alpha = |\mathrm{TP}| / (|\mathrm{TP}| + |\mathrm{FN}| + |\mathrm{FP}|)$, $\mathrm{AssA}_\alpha = \frac{1}{|\mathrm{TP}|} \sum_{c \in \mathrm{TP}} \mathcal{A}(c)$, and the localization accuracy $\mathrm{LocA}_\alpha$, the mean of $S$ over the true positives. If $|g|$ and $|p|$ are the numbers of detections of $g$ and $p$, then $|\mathrm{FNA}(c)| = |g| - |\mathrm{TPA}(c)|$ and $|\mathrm{FPA}(c)| = |p| - |\mathrm{TPA}(c)|$, so $\mathcal{A}(c)$ is the Jaccard index of the two trajectories' sets of frames, counting only the frames in which they are matched as shared.

The matching of each frame maximizes the sum of the score

$$\mathrm{MS}(g, p) = \frac{1}{\varepsilon} + \mathcal{A}_{\max}(g, p) + \varepsilon\, S(g, p) \quad \text{for } S(g, p) \ge \alpha,$$

with a small $\varepsilon$. The first term asks for the most true positives, the second for the best association, and the third for the best boxes. $\mathcal{A}_{\max}(g, p)$ is the largest $\mathcal{A}$ the pair could get if every frame could match it: $n / (|g| + |p| - n)$, where $n$ is the number of frames in which $g$ and $p$ have $S \ge \alpha$. The full procedure:

```pseudo id=main
HOTA(the true and the predicted detections)
L1  for each α in {0.05, 0.10, ..., 0.95}:
L2      in each frame, match the detections with S ≥ α, maximizing the sum of MS (Hungarian)
L3      count TP, FN and FP; for each identity pair (g, p), |TPA| = its number of true positives
L4      DetA_α ← TP / (TP + FN + FP); AssA_α ← mean of A(c) over TP; HOTA_α ← sqrt(DetA_α · AssA_α)
L5  HOTA ← the mean of HOTA_α over the 19 values of α
```

These facts follow from the definition and are proved in the correctness file of this page:

- **Theorem: the geometric mean.** $\mathrm{HOTA}_\alpha = \sqrt{\mathrm{DetA}_\alpha \cdot \mathrm{AssA}_\alpha}$ whenever there is a true positive (Eq. 21 of the paper).
- **Theorem: the most true positives.** If $1/\varepsilon > k (1 + \varepsilon)$, where $k$ is the largest number of pairs in a frame, the matching of line L2 has the largest possible number of true positives in each frame.
- **Theorem: DetA does not grow with $\alpha$.** A larger threshold allows fewer pairs, so the largest matching cannot grow, and $\mathrm{DetA}_\alpha$ falls or stays.
- **Theorem: the range.** $0 \le \mathrm{HOTA}_\alpha \le 1$, and $\mathrm{HOTA}_\alpha = 1$ exactly when there are no misses and no false positives and each true identity is matched to one predicted identity in all its frames, and the other way around.

## Examples and non-examples

- **A swap.** Two objects stand still for 6 frames, and the tracker follows them with exact boxes and the identities $a$ and $b$, which swap after frame 4. For every $\alpha$ all 12 detections are true positives, so $\mathrm{DetA}_\alpha = 1$. The pair $(1, a)$ has $|\mathrm{TPA}| = 4$ and $|g| = |p| = 6$, so $\mathcal{A} = 4 / (6 + 6 - 4) = 1/2$; the pair $(1, b)$ has $\mathcal{A} = 2 / 10 = 1/5$, and the same holds for object 2. So $\mathrm{AssA} = (8 \cdot \tfrac12 + 4 \cdot \tfrac15) / 12 = 2/5$ and $\mathrm{HOTA} = \sqrt{2/5} \approx 0.632$. On the same input $\mathrm{MOTA} = 5/6$ and $\mathrm{IDF1} = 2/3$.
- **A box that is a little off.** One object over 5 frames at $(0,0,8,10)$, and the tracker always gives $(2,0,10,10)$, with IoU $60/100 = 0.6$. For the 12 thresholds $\alpha \le 0.6$, every detection is a true positive and $\mathrm{HOTA}_\alpha = 1$; for the 7 thresholds above, there are no true positives and $\mathrm{HOTA}_\alpha = 0$. So $\mathrm{HOTA} = 12/19 \approx 0.632$, and $\mathrm{LocA} = 0.6$ on the thresholds with true positives. MOTA with the threshold 0.5 would be 1: HOTA also asks for good boxes.
- **Not the product.** $\mathrm{HOTA}_\alpha$ is a geometric mean, not a product. With $\mathrm{DetA} = 1$ and $\mathrm{AssA} = 0.25$ it is $0.5$, not $0.25$.
- **Not the mean of the parts over $\alpha$.** HOTA averages $\sqrt{\mathrm{DetA}_\alpha \mathrm{AssA}_\alpha}$, which is in general not $\sqrt{\mathrm{DetA} \cdot \mathrm{AssA}}$ of the averaged parts. In the second example the averaged parts are both $12/19$, and their geometric mean happens to agree, but with $\mathrm{DetA}_\alpha$ and $\mathrm{AssA}_\alpha$ that fall at different thresholds it does not.

## Related definitions

[MOTA](/clear-mot-metrics/) uses the same per frame matching, but it counts association only through identity switches, events against the last match, so detection errors dominate it. The [IDF1 score](/idf1-score/) matches whole trajectories once, so only the matched trajectories count as correct, and better detection in unmatched parts can lower it. HOTA scores every true positive with the overlap $\mathcal{A}$ of the two trajectories it links, which needs no global matching. DetA and AssA split into recall and precision parts, $\mathrm{DetRe}$, $\mathrm{DetPr}$, $\mathrm{AssRe}$ and $\mathrm{AssPr}$, in the same way as [precision and recall](/precision-and-recall/). The per frame matching is an [assignment problem](/assignment-problem/), solved with the [Hungarian algorithm](/hungarian-algorithm/). AssA measures the result of the [data association](/data-association/) step of a tracker, and the [ByteTrack](/bytetrack/) paper reports HOTA together with MOTA and IDF1. The Python code of this page computes the parts with exact fractions, and its tests compare the per frame matching with all matchings, compute $\mathcal{A}(c)$ again from the set definitions, and check that DetA does not grow with $\alpha$.

## References
