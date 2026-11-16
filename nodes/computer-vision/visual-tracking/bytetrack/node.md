---
tag: 0E34WD
kind: algorithm
slug: bytetrack
name: ByteTrack
aliases:
- BYTE association
area: computer-vision/visual-tracking
level: research
summary: Associate high-score detections to tracks first, then match the remaining tracks to low-score detections, recovering occluded objects that a threshold drops.
solves: [multi-object-tracking]
model: real-ram
complexity:
  vars: {n: the number of tracks, m: the number of detections in a frame, N: the number of frames}
  time: {worst: O(N n m (n + m))}
  space: {extra: O(n m)}
properties: {deterministic: true, online: true, iterative: false, exact: false}
history:
  year: 2022
  people: [Yifu Zhang, Peize Sun, Yi Jiang, Dongdong Yu, Fucheng Weng, Zehuan Yuan, Ping Luo, Wenyu Liu, Xinggang Wang]
  note: "Zhang and others published BYTE and the tracker ByteTrack at ECCV 2022 (arXiv 2021), with the idea to associate every detection box, also the low-score ones."
prereqs: [sort-tracker, kalman-filter, hungarian-algorithm, intersection-over-union, object-detection]
see_also: [sort-tracker, deep-sort, multi-object-tracking, tracking-by-detection, data-association, jonker-volgenant-algorithm, maximum-weight-matching, hota-metric]
sources:
  - paper: doi:10.1007/978-3-031-20047-2_1
    title: "Yifu Zhang, Peize Sun, Yi Jiang, Dongdong Yu, Fucheng Weng, Zehuan Yuan, Ping Luo, Wenyu Liu and Xinggang Wang, ByteTrack: multi-object tracking by associating every detection box, ECCV 2022, LNCS 13682, 1-21 (arXiv:2110.06864)"
    locator: "Section 3 and Algorithm 1 (BYTE), Section 4.1 (the threshold 0.6, the IoU bound 0.2, lost tracks kept 30 frames), Section 4.2 (BYTE added to nine other trackers)"
  - paper: doi:10.1109/ICIP.2016.7533003
    title: "Alex Bewley, Zongyuan Ge, Lionel Ott, Fabio Ramos and Ben Upcroft, Simple online and realtime tracking, ICIP 2016, 3464-3468 (arXiv:1602.00763)"
    locator: "Section 3 (the Kalman filter and IoU assignment that BYTE keeps)"
  - paper: doi:10.1109/ICIP.2017.8296962
    title: "Nicolai Wojke, Alex Bewley and Dietrich Paulus, Simple online and realtime tracking with a deep association metric, ICIP 2017, 3645-3649 (arXiv:1703.07402)"
    locator: "Section 2.1 (the Kalman filter on center, aspect ratio and height that the released ByteTrack code also uses)"
  - paper: doi:10.1007/BF02278710
    title: "Roy Jonker and Anton Volgenant, A shortest augmenting path algorithm for dense and sparse linear assignment problems, Computing 38(4), 1987, 325-340"
    locator: "the whole paper (the assignment solver of the released code)"
  - paper: arxiv:1603.00831
    title: "Anton Milan, Laura Leal-Taixe, Ian Reid, Stefan Roth and Konrad Schindler, MOT16: a benchmark for multi-object tracking, arXiv:1603.00831, 2016"
    locator: "the benchmark protocol used for MOT17 results"
---

ByteTrack is a [multi-object tracker](/multi-object-tracking/) of the [tracking by detection](/tracking-by-detection/) kind, built on the [SORT](/sort-tracker/) scheme of a [Kalman filter](/kalman-filter/) per track and an [IoU](/intersection-over-union/) assignment per frame. Its association step, called BYTE, uses every detection box. Other trackers drop the boxes whose detector score is below a threshold, but an object that is partly hidden often gets exactly such a low score. BYTE first matches the tracks with the high-score boxes, then matches the tracks still unmatched with the low-score boxes, and treats the low boxes that match no track as background. A low box can keep a track alive but can never start one. Compared with [Deep SORT](/deep-sort/), ByteTrack needs no appearance network and has no cascade; compared with SORT, it keeps lost tracks for 30 frames and adds the second round.

## In plain words

A detector gives each box a score that says how sure it is. Most trackers throw away the boxes with a low score, because many of them are wrong. But when a person walks behind a car, the detector still sees part of the person and gives a box with a low score. ByteTrack keeps those boxes for a second look. First it pairs the tracks with the boxes it trusts. Then, for each track that found no box, it looks at the doubtful boxes and takes one only if it overlaps the predicted place well. A doubtful box that no track wants is thrown away and never starts a new track. In this way the hidden person keeps a track, and wrong boxes do not create false tracks.

## The problem

The input is that of the [SORT tracker](/sort-tracker/), and each detection also has a score $s \in [0, 1]$ from the detector. Boxes are $(x_1, y_1, x_2, y_2)$ with area $(x_2 - x_1)(y_2 - y_1)$. The output of each frame is a list of (identity, box) pairs, and the tracker is online.

**The split.** With the threshold $\tau$, the high detections are $D_{\text{high}} = \{d : s > \tau\}$ and the low detections are $D_{\text{low}} = \{d : s_{\min} < s \le \tau\}$. The paper uses $\tau = 0.6$. The released code drops boxes with $s \le 0.1$, so $s_{\min} = 0.1$.

**The tracks.** A track holds a Kalman filter on center, aspect ratio and height with their velocities, the same filter as in [Deep SORT](/deep-sort/). Its state is *tracked* if it was matched in the last frame, *lost* if not. A lost track is kept for 30 frames and then removed. A new track is *unconfirmed* until it is matched in the next frame.

**The matching.** Each association step on tracks $R$ and detections $C$ with an IoU bound $\beta$ returns a matching of largest total weight $\sum (\mathrm{IoU}(i, j) - \beta)$, using only pairs with $\mathrm{IoU}(i, j) \ge \beta$. This is a [maximum weight matching](/maximum-weight-matching/) in a bipartite graph. The released code computes it with the [Jonker-Volgenant algorithm](/jonker-volgenant-algorithm/) with a cost limit of $1 - \beta$ on the cost $1 - \mathrm{IoU}$. A cost limit is built by extending the matrix with dummy rows and columns, and that extension gives a matching of the same largest weight.

## The algorithm

```pseudo id=main
BYTE-STEP(the tracks, the detections (d_j, s_j), τ, s_min)
L1   D_high ← {j : s_j > τ};  D_low ← {j : s_min < s_j ≤ τ}
L2   for each track: Kalman predict
L3   match the tracked and lost tracks with D_high by IoU, bound 0.2; update the matched tracks
L4   match the tracked tracks still unmatched with D_low by IoU, bound 0.5; update the matched tracks
L5   the tracked tracks still unmatched become lost; remove lost tracks older than 30 frames; drop the rest of D_low
L6   match the unconfirmed tracks with the rest of D_high by IoU, bound 0.3; remove the unconfirmed tracks that miss
L7   for each detection j left in D_high with s_j ≥ τ + 0.1: start an unconfirmed track
L8   output the confirmed tracks updated in this frame
```

Lines L1 to L5 and the start of new tracks from the unmatched high boxes are Algorithm 1 of the paper. The paper rejects a pair of the first round with IoU below 0.2 and keeps lost tracks for 30 frames. The bounds 0.5 and 0.3 of lines L4 and L6, the floor $s_{\min} = 0.1$, the start threshold $\tau + 0.1$ and the unconfirmed state are from the released code. A track is confirmed at once in the first frame of a video. The paper allows an appearance similarity in the first round when the tracker has one, but it uses IoU only in the second round, because low boxes often show an occluded or blurred object whose appearance is not reliable.

## Example

**One frame.** Two confirmed tracks predict the boxes $A = (0, 0, 10, 20)$ and $B = (30, 0, 40, 20)$. The detector gives three boxes:

| box | score | set |
|---|---|---|
| $(31, 1, 41, 21)$ | 0.9 | high |
| $(2, 0, 12, 20)$ | 0.4 | low |
| $(80, 80, 90, 100)$ | 0.15 | low |

In the first round, the only high box has IoU $171/229 \approx 0.747$ with $B$ (an overlap of $9 \times 19 = 171$ and a union of $400 - 171 = 229$) and 0 with $A$, so $B$ takes it. In the second round, track $A$ meets the low boxes. The box $(2, 0, 12, 20)$ has IoU $160/240 = 2/3 \ge 0.5$ with $A$, so $A$ takes it. The box at $(80, 80)$ matches nothing and is dropped, and it does not start a track. Both tracks are reported. A tracker that drops the low boxes, here the same code without line L4, reports only $B$, and track $A$ becomes lost.

**A short sequence.** Two people walk for 40 frames. Person 0 is half hidden in frames 12 to 21, where the detector gives a correct box with score 0.3. Weak false boxes with score 0.2 appear now and then. ByteTrack reports both people in all 40 frames with one identity each. Without the second round, person 0 is not reported in the 10 hidden frames. In this case the lost track is found again in frame 22 by the first round, because it is kept for 30 frames, so the identity is the same; with a memory of 5 frames, person 0 gets a new identity. The false boxes never start a track in either version.

## Correctness

ByteTrack is a heuristic tracker. The proved parts are about one frame. The proofs are in [proofs/correctness.md](proofs/correctness.md).

- **Theorem: each round is a largest weight matching.** The matching of each round has the largest total of $\mathrm{IoU} - \beta$ among all matchings that use only pairs with $\mathrm{IoU} \ge \beta$, and the method with a full assignment on the clipped weights computes it.
- **Theorem: the rounds are consistent.** Over the frame, no track and no detection is matched twice.
- **Theorem: low boxes start nothing.** A detection with score at most $\tau$ never starts a track. So in a frame without high boxes the set of tracks can only shrink.
- **Theorem: BYTE only adds matches.** For the same tracks and detections, the pairs of the first round are those of the same tracker without the second round, and the second round only adds pairs. So in one frame, the set of matched tracks of BYTE contains the set of the baseline.
- **Not proved.** That a low box with a large IoU belongs to the object of the track, and not to a nearby object, is an assumption. The gains on MOT17 and MOT20 are benchmark results.

## Complexity

Let $n$ be the number of tracks and $m$ the number of detections, in the [real RAM](/real-ram/) model. The IoU values cost $O(n m)$. Each round is an assignment of at most $n$ tracks and $m$ detections, which the Hungarian or Jonker-Volgenant method solves in $O(n m (n + m))$ time. The Kalman steps cost $O(n + m)$, since the filter has a fixed size. One frame costs $O(n m (n + m))$ time and $O(n m)$ extra space, and $N$ frames cost $N$ times that. The paper reports 30 frames per second for the whole system on one V100 GPU, almost all of it in the detector; that is a benchmark result.

## Properties

- **Online.** The output of a frame never changes later.
- **No appearance needed.** The benchmark version of the paper uses IoU in both rounds.
- **Asymmetric use of scores.** Low boxes can extend tracks but cannot start them, so lowering $\tau$ does not by itself create false tracks.
- **Detector dependent.** The scores must be calibrated in the sense that the boxes of hidden objects get low but nonzero scores. The method helps less with a detector that suppresses such boxes.

## Variants and improvements

- **Appearance in the first round.** The paper shows that BYTE can replace the association of trackers with an appearance model, such as FairMOT, and keep their appearance score in the first round. It reports IDF1 gains of 1 to 10 points on nine trackers, which is a benchmark result.
- **Score fusion.** The released code multiplies the IoU by the detection score in the first round on MOT17, so that strong boxes win ties.
- **Later trackers.** BoT-SORT adds camera motion compensation and appearance, and OC-SORT changes the Kalman update after a lost period. Both keep the two rounds of BYTE.

## When to use it

Use ByteTrack when the detector is strong but objects are often partly hidden, as in crowds, and when a fast tracker without an appearance network is wanted. It works best at high frame rates, where the IoU of an object with its own box in the next frame is large. Do not expect it to keep identities when objects are fully hidden for longer than the lost period, or when similar objects cross while hidden, since it has no appearance score by default. For long occlusions, add appearance, as in [Deep SORT](/deep-sort/).

## Pitfalls

- **Treating the thresholds as universal.** The values 0.6, 0.2, 0.5, 0.3 and 0.1 are tuned for pedestrian benchmarks and one detector. A different detector has a different score scale.
- **Starting tracks from low boxes.** That defeats the method: low boxes are mostly background, and only a match with an existing track makes them useful.
- **Using appearance in the second round.** The appearance of a hidden or blurred object is not reliable, which is why the paper uses IoU there.
- **Low boxes from nearby objects.** In a dense crowd a low box of one person can overlap the prediction of another. The bound 0.5 of the second round limits this but does not prevent it.
- **Comparing trackers with different detectors.** Most of the score of a tracker on MOT17 comes from the detector. Compare association methods on the same detections, as the paper does in its ablations.

## Implementations

The Python file follows Algorithm 1 of the paper with the values of the paper and of the released code. Each round is a largest weight matching computed by the Hungarian algorithm on the clipped weights. The tests compare the matching with a search over all matchings, check the frame of the example with exact IoU values, check that low boxes never start tracks, and compare BYTE with the same tracker without the second round on the occlusion sequence above.

## History

Trackers before ByteTrack, from [SORT](/sort-tracker/) and [Deep SORT](/deep-sort/) on, kept only detections above a score threshold. In 2021 Zhang, Sun, Jiang, Yu, Weng, Yuan, Luo, Liu and Wang posted ByteTrack, published at ECCV 2022. They argued that low-score boxes hold the occluded objects and should be associated, not dropped. With the YOLOX detector, they reported 80.3 MOTA, 77.3 IDF1 and 63.1 [HOTA](/hota-metric/) on the MOT17 test set at 30 frames per second. The two rounds of BYTE were then taken up by many later trackers.

## References
