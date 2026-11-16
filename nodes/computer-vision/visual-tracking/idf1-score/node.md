---
tag: QK543C
kind: definition
slug: idf1-score
name: IDF1 score
aliases:
- identity F1 score
area: computer-vision/visual-tracking
level: advanced
summary: The F1 score of detections correctly identified after a global one-to-one matching of predicted and true trajectories, a measure of identity preservation.
prereqs: [multi-object-tracking, precision-and-recall, bipartite-matching]
see_also: [clear-mot-metrics, hota-metric, multi-object-tracking, maximum-weight-matching, hungarian-algorithm, intersection-over-union, deep-sort, bytetrack]
sources:
  - paper: arxiv:1609.01775
    title: "Ergys Ristani, Francesco Solera, Roger S. Zou, Rita Cucchiara and Carlo Tomasi, Performance measures and a data set for multi-target, multi-camera tracking, ECCV 2016 Workshops, 17-35"
    locator: "Section 3.3 (the bipartite graph with false positive and false negative nodes, Eq. 3 and Eq. 4), Section 3.4 (IDFN, IDFP and IDTP, Eq. 6 to 8, and IDP, IDR and IDF1, Eq. 9 to 11), Figure 1 (the comparison with the counts of events)"
  - paper: doi:10.1155/2008/246309
    title: "Keni Bernardin and Rainer Stiefelhagen, Evaluating multiple object tracking performance: the CLEAR MOT metrics, EURASIP Journal on Image and Video Processing 2008, article 246309"
    locator: "the definitions of MOTA and of the mismatch count, which IDF1 is compared with"
  - paper: arxiv:2009.07736
    title: "Jonathon Luiten, Aljosa Osep, Patrick Dendorfer, Philip Torr, Andreas Geiger, Laura Leal-Taixe and Bastian Leibe, HOTA: a higher order metric for evaluating multi-object tracking, International Journal of Computer Vision 129(2), 2021, 548-578"
    locator: "Section 4.2 (IDF1 in the notation of HOTA) and Section 7 (detection matching against trajectory matching, and why IDF1 can fall when detection improves)"
---

The IDF1 score measures how well a [multi-object tracker](/multi-object-tracking/) keeps the identities of the objects over a whole video. Each true trajectory is matched to at most one computed trajectory, once, for the whole video, by a one-to-one matching that maximizes the number of frames in which the two agree. A detection counts as correct only if it belongs to the trajectory matched to its object. IDF1 is the F1 score, the harmonic mean of precision and recall, of these identity-correct detections. Ristani et al. introduced it in 2016 together with the identity precision IDP and recall IDR. Where [MOTA](/clear-mot-metrics/) counts an identity switch once, in one frame, IDF1 counts every frame that carries the wrong identity.

## Definition

The ground truth has true trajectories $o$, each a set of frames with a box, and the tracker has computed trajectories $h$. In one frame, the detections of $o$ and $h$ *agree* when both are present and the [intersection over union](/intersection-over-union/) of their boxes is at least a threshold $\Delta$, such as $0.5$; the paper also allows a distance on the ground plane, with $\Delta = 1$ meter. Let

$$n(o, h) = \text{the number of frames in which } o \text{ and } h \text{ agree},$$

and let $|o|$ and $|h|$ be the numbers of frames in which they are present. For a one-to-one matching $\mu$ of true to computed trajectories, the identity true positives are $\sum_{(o, h) \in \mu} n(o, h)$. The matching of IDF1 is one that makes this sum largest, and

$$\mathrm{IDTP} = \max_\mu \sum_{(o, h) \in \mu} n(o, h), \quad \mathrm{IDFN} = \sum_o |o| - \mathrm{IDTP}, \quad \mathrm{IDFP} = \sum_h |h| - \mathrm{IDTP},$$

$$\mathrm{IDP} = \frac{\mathrm{IDTP}}{\mathrm{IDTP} + \mathrm{IDFP}}, \quad \mathrm{IDR} = \frac{\mathrm{IDTP}}{\mathrm{IDTP} + \mathrm{IDFN}}, \quad \mathrm{IDF1} = \frac{2\, \mathrm{IDTP}}{2\, \mathrm{IDTP} + \mathrm{IDFP} + \mathrm{IDFN}} = \frac{2\, \mathrm{IDTP}}{\sum_o |o| + \sum_h |h|}.$$

The computation is a [maximum weight matching](/maximum-weight-matching/) in a [bipartite](/bipartite-matching/) graph:

```pseudo id=main
IDF1(the true and the computed trajectories, the threshold Δ)
L1  for each frame, each true detection and each computed detection: if IoU ≥ Δ, add 1 to n(o, h)
L2  find a one-to-one matching μ of true to computed trajectories with the largest sum of n (Hungarian)
L3  IDTP ← that sum; IDFN ← (true detections) - IDTP; IDFP ← (computed detections) - IDTP
L4  IDP ← IDTP / (computed detections); IDR ← IDTP / (true detections); IDF1 ← 2 IDTP / (both)
```

The paper writes line L2 as a minimum cost problem. It adds a false negative node for each true trajectory and a false positive node for each computed one, so that a trajectory can stay unmatched. Matching $o$ to $h$ costs the frames in which they do not agree, $|o| + |h| - 2 n(o, h)$; leaving $o$ unmatched costs $|o|$, and leaving $h$ unmatched costs $|h|$. These facts follow from the definition and are proved in the correctness file of this page:

- **Theorem: the two forms agree.** The minimum cost of the form of the paper is $\sum_o |o| + \sum_h |h| - 2\, \mathrm{IDTP}$, which is $\mathrm{IDFN} + \mathrm{IDFP}$. So both forms give the same IDTP.
- **Theorem: the bound by detection.** IDF1 is at most the F1 score of the detections, where each frame uses its own best one-to-one matching. Identity can only lower the score.
- **Theorem: symmetry.** Swapping the roles of the ground truth and the tracker keeps IDTP and IDF1 and swaps IDP and IDR.

With $m$ trajectories on the larger side, the Hungarian algorithm of line L2 costs $O(m^3)$, and line L1 costs one IoU for each pair of detections in the same frame.

## Examples and non-examples

- **A swap.** Two objects stand still for 6 frames, and the tracker follows them with $a$ and $b$. After frame 4 the two identities swap. Then $n(1, a) = 4$, $n(1, b) = 2$, $n(2, b) = 4$ and $n(2, a) = 2$, so the best matching is $1 \to a$, $2 \to b$ with $\mathrm{IDTP} = 8$. There are 12 true and 12 computed detections, so $\mathrm{IDFN} = \mathrm{IDFP} = 4$ and $\mathrm{IDF1} = \mathrm{IDP} = \mathrm{IDR} = 16/24 = 2/3$. MOTA counts 2 switches in 12 objects and gives $5/6$.
- **A late switch.** One object over 100 frames, tracked by $a$ in the first 50 frames and by $b$ in the last 50. The best matching takes one of them, so $\mathrm{IDTP} = 50$ and $\mathrm{IDF1} = 100/200 = 1/2$, while MOTA is $0.99$. A tracker that keeps one identity for all 100 frames but adds one false positive gets $\mathrm{IDF1} = 200/201$ and the same MOTA.
- **Not the F1 of detections.** In both examples every object is detected in every frame, so the F1 score of detections is 1. IDF1 is lower because it also asks for the right identity.
- **Not a frame by frame measure.** The matching is global: a computed trajectory that switches to a new object late in the video can still be matched to its first object, and the frames after the switch are errors.
- **More correct boxes can lower IDF1.** A computed trajectory $a$ is matched to object 1 and also covers object 2 for 3 frames in which nothing else covers object 2. Those 3 boxes are correct detections, but they count as IDFP, and object 2 stays IDFN either way. A tracker that leaves them out has the same IDTP and a smaller denominator, so a higher IDF1.

## Related definitions

[MOTA](/clear-mot-metrics/) uses a matching in each frame and counts identity switches as events; IDF1 uses one matching for the whole video and counts frames. The two often rank trackers in different orders. [HOTA](/hota-metric/) also measures association over the whole video, but for each true positive pair it looks at the overlap of the two whole trajectories, and it averages over the threshold $\Delta$; its authors point out that IDF1 ignores the association of the parts that are not matched, and that it can fall when the detection gets better, as in the example above. Detection F1 and [precision and recall](/precision-and-recall/) are the same formulas without identity. Trackers with appearance features, such as [Deep SORT](/deep-sort/), aim to raise IDF1 by keeping identities through occlusions, and the [ByteTrack](/bytetrack/) paper reports IDF1 together with MOTA and HOTA. The Python code of this page computes the identity measures with exact fractions, and its tests compare the matching with all matchings, check that the form of the paper with extra nodes gives the same minimum, and check the bound by detection and the symmetry on random sequences.

## References
