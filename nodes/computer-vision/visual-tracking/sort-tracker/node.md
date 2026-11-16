---
tag: 2C1PFP
kind: algorithm
slug: sort-tracker
name: SORT tracker
aliases:
- simple online and realtime tracking
area: computer-vision/visual-tracking
level: advanced
summary: Predict each track with a constant velocity Kalman filter on its box and assign detections by the Hungarian algorithm on IoU, frame by frame.
solves: [multi-object-tracking]
model: real-ram
complexity:
  vars: {n: the number of tracks, m: the number of detections in a frame, N: the number of frames}
  time: {worst: O(N n m (n + m))}
  space: {extra: O(n m)}
properties: {deterministic: true, online: true, iterative: false, exact: false}
history:
  year: 2016
  people: [Alex Bewley, Zongyuan Ge, Lionel Ott, Fabio Ramos, Ben Upcroft]
  note: "Bewley, Ge, Ott, Ramos and Upcroft presented SORT at ICIP 2016 to show that a good detector with a Kalman filter and the Hungarian algorithm is enough for a fast online tracker."
prereqs: [kalman-filter, hungarian-algorithm, intersection-over-union, tracking-by-detection]
see_also: [deep-sort, bytetrack, global-nearest-neighbor-association, multi-object-tracking, data-association, assignment-problem, track-gating, clear-mot-metrics]
sources:
  - paper: doi:10.1109/ICIP.2016.7533003
    title: "Alex Bewley, Zongyuan Ge, Lionel Ott, Fabio Ramos and Ben Upcroft, Simple online and realtime tracking, IEEE International Conference on Image Processing (ICIP), 2016, 3464-3468 (arXiv:1602.00763)"
    locator: "Section 3.2 (the state and the constant velocity model), Section 3.3 (the IoU assignment by the Hungarian algorithm), Section 3.4 (track creation and deletion), Section 4 (the setup and the MOT benchmark results)"
  - paper: doi:10.1115/1.3662552
    title: "R. E. Kalman, A new approach to linear filtering and prediction problems, Journal of Basic Engineering 82(1), 1960, 35-45"
    locator: "the recursive linear estimator used for each track"
  - paper: doi:10.1002/nav.3800020109
    title: "Harold W. Kuhn, The Hungarian method for the assignment problem, Naval Research Logistics Quarterly 2(1-2), 1955, 83-97"
    locator: "the whole paper (the assignment step)"
  - paper: doi:10.1109/ICIP.2017.8296962
    title: "Nicolai Wojke, Alex Bewley and Dietrich Paulus, Simple online and realtime tracking with a deep association metric, ICIP 2017, 3645-3649 (arXiv:1703.07402)"
    locator: "Section 1 and Section 3 (the identity switches of SORT under occlusion, which motivate Deep SORT)"
  - paper: arxiv:1504.01942
    title: "Laura Leal-Taixe, Anton Milan, Ian Reid, Stefan Roth and Konrad Schindler, MOTChallenge 2015: towards a benchmark for multi-target tracking, arXiv:1504.01942, 2015"
    locator: "the benchmark and the metrics on which SORT reports its results"
---

SORT, short for simple online and realtime tracking, is a [multi-object tracker](/multi-object-tracking/) of the [tracking by detection](/tracking-by-detection/) kind. An object detector gives boxes in each frame, and SORT links them into tracks. Each track has a constant velocity [Kalman filter](/kalman-filter/) on its box. In each frame the tracks predict their boxes, the [intersection over union](/intersection-over-union/) (IoU) between each prediction and each detection is the score of the pair, and the [Hungarian algorithm](/hungarian-algorithm/) picks the one-to-one assignment of largest total IoU. SORT uses no appearance and no past frames beyond the filter state, so it is fast and simple. Its weak point is identity switches after occlusions, which [Deep SORT](/deep-sort/) and [ByteTrack](/bytetrack/) address. The page [global nearest neighbor association](/global-nearest-neighbor-association/) describes the same one-assignment-per-frame idea with a Mahalanobis cost; SORT replaces it with an IoU score and adds simple rules to start and end tracks.

## In plain words

A camera watches a street, and a detector draws a box around each person in every picture, but it does not say who is who. SORT keeps a list of tracks, one per person. For each track it guesses where the box will be in the next picture, by assuming the person keeps the same speed. When the next picture comes, it compares each guessed box with each new box and measures how much they overlap. Then it pairs guesses and boxes so that the total overlap is as large as possible, with each box used once. A pair that overlaps too little is not accepted. Each track moves to its new box. A box that no track takes starts a new track, and a track that gets no box for too long is dropped.

## The problem

The input is a sequence of frames. Frame $t$ comes with a list of $m$ detections $d_1, \ldots, d_m$, each a box $(x_1, y_1, x_2, y_2)$ in continuous image coordinates with $x_1 < x_2$ and $y_1 < y_2$, and area $(x_2 - x_1)(y_2 - y_1)$, with no $+1$ term. The output of frame $t$ is a list of pairs (identity, box). The tracker is *online*: the output of frame $t$ depends only on frames $1$ to $t$. The goal is the one of [multi-object tracking](/multi-object-tracking/): each object keeps one identity for as long as it is in view, with few misses and few false tracks.

**The state of a track.** A track holds the Kalman state

$$x = (u, v, s, r, \dot u, \dot v, \dot s),$$

where $(u, v)$ is the box center, $s = w h$ the area, $r = w / h$ the aspect ratio, and the dots are velocities in pixels per frame (and pixels squared per frame for $s$). The ratio $r$ has no velocity: SORT takes it as constant. A box maps to the measurement $z = (u, v, s, r)$, and back by $w = \sqrt{s r}$ and $h = s / w$. The motion is $x_{t+1} = F x_t + \text{noise}$, with $F$ the identity plus ones that add $\dot u, \dot v, \dot s$ to $u, v, s$. The measurement matrix $H$ picks the first four entries.

## The algorithm

```pseudo id=main
SORT-STEP(the tracks, the detections d_1..d_m, IoU_min, max_age, min_hits)
L1   for each track i: Kalman predict x_i and P_i; drop the track if its box has s ≤ 0
L2   for each track i and each detection j: c_ij ← IoU(box of x_i, d_j)
L3   σ ← the assignment of largest total Σ c_iσ(i), by the Hungarian algorithm
L4   keep only the pairs (i, σ(i)) with c_iσ(i) ≥ IoU_min
L5   for each kept pair (i, j): Kalman update of track i with z(d_j)
L6   for each detection j in no kept pair: a new track with x = (z(d_j), 0, 0, 0)
L7   delete each track whose time since its last update exceeds max_age
L8   output the tracks updated in this frame that have at least min_hits updates in a row
```

The assignment of line L3 has size $\min(n, m)$ and uses every pair, also pairs with IoU 0. Line L4 then removes the weak pairs, so a track may end the frame with no detection. The paper says that a minimum IoU rejects weak pairs; the released code uses $\mathrm{IoU}_{\min} = 0.3$.

**Track management.** A new track starts with zero velocity and a large variance on the velocity, so the first updates set the velocity. The paper deletes a track that is not detected for $T_{\text{lost}} = 1$ frame. In the released code, which this page follows, a track is deleted when its count of frames since the last update passes `max_age` = 1, so it survives one missed frame and dies at the second. A new track is not reported until it has `min_hits` = 3 updates in a row, except in the first 3 frames of the video; the paper calls this the probation period. These rules are heuristics. They are tuned, and they often change the score of the tracker more than the assignment does.

**The filter.** The noise matrices of the released code are $R = \mathrm{diag}(1, 1, 10, 10)$ for the measurement, $Q = \mathrm{diag}(1, 1, 1, 1, 0.01, 0.01, 10^{-4})$ for the motion, and $P_0 = \mathrm{diag}(10, 10, 10, 10, 10^4, 10^4, 10^4)$ for a new track. If the predicted area $s + \dot s$ would be negative, the code sets $\dot s$ to 0 first.

## Example

**One frame.** Two tracks predict the boxes $A = (0, 0, 10, 10)$ and $B = (6, 0, 16, 10)$. The detector gives $d_1 = (4, 0, 14, 10)$, $d_2 = (9, 0, 19, 10)$ and $d_3 = (40, 40, 50, 50)$. All boxes are 10 by 10, so each union is $200$ minus the overlap. The IoU matrix is

| | $d_1$ | $d_2$ | $d_3$ |
|---|---|---|---|
| $A$ | $60/140 = 3/7 \approx 0.429$ | $10/190 = 1/19 \approx 0.053$ | 0 |
| $B$ | $80/120 = 2/3 \approx 0.667$ | $70/130 = 7/13 \approx 0.538$ | 0 |

The assignment $A \to d_1$, $B \to d_2$ has total $0.429 + 0.538 = 0.967$. The other choice that uses $d_1$ and $d_2$, $A \to d_2$, $B \to d_1$, has total $0.053 + 0.667 = 0.719$. The Hungarian algorithm returns the first one. Both pairs pass $\mathrm{IoU}_{\min} = 0.3$, so both tracks are updated, and $d_3$ starts a new track. A greedy rule that takes the largest IoU first would pair $B$ with $d_1$, and then $A$ could only have $d_2$ at IoU $1/19$, below the threshold. Track $A$ would miss its detection, and $d_2$ would start a false new track.

For the box $d_1$ the measurement is $z = (9, 5, 100, 1)$: center $(9, 5)$, area 100 and ratio 1.

**A short sequence.** Three boxes of size 20 by 40 move at constant velocity for 30 frames, and the detections are the true corners plus Gaussian noise of 1 pixel. Two of the boxes pass each other, with an IoU of at most $1/7$ between them. The detector misses object 0 in frame 12, and a false box appears in frame 20 only. SORT gives each object one identity for the whole sequence. The track of object 0 survives the missed frame, but its run of updates restarts, so it is not reported in frames 12, 13 and 14 and comes back with the same identity in frame 15. The false box starts a track that is never reported and is deleted two frames later. The mean error of the reported box centers is 0.65 pixels.

## Correctness

SORT is a heuristic tracker, and nothing guarantees that it keeps identities on real video. The proved parts are about one frame and about ideal input. The proofs are in [proofs/correctness.md](proofs/correctness.md).

- **Theorem: the assignment.** Line L3 returns an assignment of largest total IoU among all one-to-one assignments of size $\min(n, m)$. After line L4, the kept pairs form a partial matching in which every pair has IoU at least $\mathrm{IoU}_{\min}$.
- **Theorem: separated objects keep their identities.** Suppose that in every frame each object is detected, the predicted box of its track has IoU at least $\mathrm{IoU}_{\min} > 0$ with its own detection, and IoU 0 with every other detection. Then every optimal assignment of line L3 pairs each track with its own object, and no identity switch occurs.
- **Theorem: the filter.** Under the linear Gaussian model, each prediction and update is the Kalman recursion, which gives the mean and covariance of the state given the measurements so far. The update in Joseph form keeps $P$ symmetric and positive definite.
- **Not proved.** With overlapping objects, missed detections or false boxes, the outcome depends on the detector and on the tuned thresholds. The Kalman model of a box is also not a true model of a person's motion.

## Complexity

Let $n$ be the number of tracks and $m$ the number of detections in a frame, in the [real RAM](/real-ram/) model. The IoU matrix costs $O(n m)$. The Hungarian algorithm with potentials solves an $r \times c$ assignment with $r \le c$ in $O(r^2 c)$ time, and $r^2 c \le n m (n + m)$. Each Kalman step works on a state of fixed size 7, so it costs $O(1)$, and $O(n + m)$ for all tracks. One frame costs $O(n m (n + m))$ time and $O(n m)$ extra space, and a video of $N$ frames costs $O(N n m (n + m))$ with $n$ and $m$ the largest counts over all frames. The detector is not part of this cost. The paper reports 260 frames per second for the tracking part on one CPU core, which is a measurement on its hardware and data, not a bound.

## Properties

- **Online.** The output of a frame never changes later.
- **One hypothesis.** SORT keeps a single assignment per frame, like [global nearest neighbor association](/global-nearest-neighbor-association/).
- **No appearance.** Two objects that swap places while one of them is not detected get swapped identities, since IoU sees only geometry.
- **Short memory.** With `max_age` = 1, a track dies after two missed frames, and the object gets a new identity when it comes back.
- **Deterministic.** The output depends only on the detections, up to ties in the assignment.

## Variants and improvements

- **Deep SORT.** [Deep SORT](/deep-sort/) adds an appearance embedding per detection, a Mahalanobis gate and a matching cascade, and keeps tracks for 30 frames.
- **ByteTrack.** [ByteTrack](/bytetrack/) also matches the low-score detections, in a second round, so that occluded objects keep their tracks.
- **Gating before the assignment.** Set the score of pairs with IoU below the threshold to a forbidden value before line L3, instead of removing them after. The two can give different matchings, as the pitfalls below show.
- **Other scores.** Generalized IoU, center distance, or the Mahalanobis distance of [track gating](/track-gating/) can replace IoU.
- **Later trackers of the same family.** OC-SORT changes the Kalman update after an occlusion, and BoT-SORT adds camera motion compensation and appearance. Their gains are benchmark results.

## When to use it

Use SORT when the detector is good, the frame rate is high so that boxes of one object overlap from frame to frame, and speed matters more than identity through long occlusions. It is a strong baseline and a common first step before an appearance model is added. Do not use it alone when objects are often hidden for several frames, or when the camera moves fast, since then the predicted box no longer overlaps the detection.

## Pitfalls

- **Low frame rate or fast motion.** If an object moves more than its width between frames, the IoU with its own detection is 0, and the track is lost. A center distance or a Mahalanobis gate does better there.
- **Filtering after the assignment.** Because line L3 maximizes the total IoU over all pairs, a pair below the threshold can take part in the optimum and be removed in line L4, while another assignment would have kept more pairs above the threshold. The released code accepts this.
- **Box conventions.** Mixing $(x, y, w, h)$ with $(x_1, y_1, x_2, y_2)$, or adding 1 to widths in one place only, gives wrong IoU values without an error.
- **Negative area.** A box that shrinks fast can predict a negative area. Clamp the area velocity, as the released code does.
- **Benchmark numbers taken as properties.** The MOTA of 33.4 on the 2015 MOT benchmark that the paper reports used Faster R-CNN detections. With other detections the score changes much, as the paper itself shows.

## Implementations

The Python file follows the released code: the same state, the same noise matrices, the IoU threshold 0.3, `max_age` = 1 and `min_hits` = 3. The Hungarian algorithm and the small matrix routines are in the same file. The tests compare the assignment with brute force over all assignments, check the IoU values $1/7$ and $1/3$ exactly, check the page example, and run the 30-frame sequence above.

## History

Tracking by detection with a Kalman filter per target and an optimal assignment per frame comes from radar tracking, where it is the [global nearest neighbor](/global-nearest-neighbor-association/) method. In 2016, Bewley, Ge, Ott, Ramos and Upcroft showed with SORT that this simple scheme, with IoU as the score and detections from Faster R-CNN, was close to the best online trackers of the MOT benchmark of 2015, and much faster. They also showed that a better detector improved the tracking score more than a more complex tracker. In 2017 Wojke, Bewley and Paulus added an appearance metric and called the result Deep SORT. Many later trackers keep the SORT structure and change the score, the filter or the track rules.

## References
