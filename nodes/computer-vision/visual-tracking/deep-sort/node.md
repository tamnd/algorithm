---
tag: Q69QVS
kind: algorithm
slug: deep-sort
name: Deep SORT
aliases:
- DeepSORT
area: computer-vision/visual-tracking
level: research
summary: SORT with an appearance embedding per detection and a matching cascade that combines Mahalanobis motion gating with cosine appearance distance.
solves: [multi-object-tracking]
model: real-ram
complexity:
  vars: {n: the number of tracks, m: the number of detections in a frame, L: the gallery size of a track, d: the embedding dimension, A: the largest track age, N: the number of frames}
  time: {worst: O(N (n m (n + m + L d) + A))}
  space: {extra: O(n L d + n m)}
properties: {deterministic: true, online: true, iterative: false, exact: false}
history:
  year: 2017
  people: [Nicolai Wojke, Alex Bewley, Dietrich Paulus]
  note: "Wojke, Bewley and Paulus added a learned appearance metric and a matching cascade to SORT at ICIP 2017, which reduced the identity switches on MOT16 by about 45 percent."
prereqs: [sort-tracker, kalman-filter, hungarian-algorithm, track-gating, cosine-similarity]
see_also: [sort-tracker, bytetrack, multi-object-tracking, tracking-by-detection, data-association, global-nearest-neighbor-association, idf1-score, clear-mot-metrics]
sources:
  - paper: doi:10.1109/ICIP.2017.8296962
    title: "Nicolai Wojke, Alex Bewley and Dietrich Paulus, Simple online and realtime tracking with a deep association metric, IEEE International Conference on Image Processing (ICIP), 2017, 3645-3649 (arXiv:1703.07402)"
    locator: "Section 2.1 (the state and track handling), Section 2.2 (the Mahalanobis gate, the gallery and the combined cost), Section 2.3 and Listing 1 (the matching cascade), Section 2.4 (the network), Section 3 (MOT16 results)"
  - paper: doi:10.1109/ICIP.2016.7533003
    title: "Alex Bewley, Zongyuan Ge, Lionel Ott, Fabio Ramos and Ben Upcroft, Simple online and realtime tracking, ICIP 2016, 3464-3468 (arXiv:1602.00763)"
    locator: "Section 3 (the SORT tracker that Deep SORT extends)"
  - paper: doi:10.1115/1.3662552
    title: "R. E. Kalman, A new approach to linear filtering and prediction problems, Journal of Basic Engineering 82(1), 1960, 35-45"
    locator: "the recursive linear estimator used for each track"
  - paper: doi:10.1002/nav.3800020109
    title: "Harold W. Kuhn, The Hungarian method for the assignment problem, Naval Research Logistics Quarterly 2(1-2), 1955, 83-97"
    locator: "the whole paper (the assignment in each stage)"
  - paper: arxiv:1603.00831
    title: "Anton Milan, Laura Leal-Taixe, Ian Reid, Stefan Roth and Konrad Schindler, MOT16: a benchmark for multi-object tracking, arXiv:1603.00831, 2016"
    locator: "the benchmark of the Deep SORT experiments"
---

Deep SORT is the [SORT tracker](/sort-tracker/) with an appearance score. Each detection comes with an embedding, a vector that a neural network computes from the image inside the box, so that boxes of the same person give close vectors. The network and its training are outside this page: here the embeddings are input data, and the page covers only the tracker that uses them. Deep SORT keeps for each track the embeddings of its last detections, gates pairs by the Mahalanobis distance of the [Kalman filter](/kalman-filter/), and scores them by the smallest cosine distance to the stored embeddings. It then matches tracks in a *cascade*, the most recently seen tracks first, and runs a SORT-like [IoU](/intersection-over-union/) stage on the rest. Compared with SORT, it keeps a lost track for 30 frames instead of 1, so a person who comes back after an occlusion can get the old identity. Compared with [ByteTrack](/bytetrack/), it adds appearance but uses only the detections above the detector threshold.

## In plain words

SORT only looks at where boxes are. When a person walks behind a tree and comes out a second later, SORT has already forgotten them and gives a new number. Deep SORT also looks at what a box looks like. A separate network turns each box into a list of numbers, and two boxes of the same person give similar lists. Each track remembers the lists of its last boxes. When new boxes come, a box can go to a track only if it is near where the track should be and if it looks like the track. Tracks that were seen most recently choose first, and tracks that have been missing longer choose later. A track that is missing is kept for a while, so the person gets the old number back.

## The problem

The input and output are those of the [SORT tracker](/sort-tracker/), and the problem is [multi-object tracking](/multi-object-tracking/). The only change in the input is that detection $j$ of a frame is a pair $(d_j, e_j)$ of a box and an embedding $e_j \in \mathbb{R}^d$.

**The state.** A track holds a [Kalman filter](/kalman-filter/) on $x = (u, v, \gamma, h, \dot u, \dot v, \dot\gamma, \dot h)$: the center $(u, v)$ of the box, the aspect ratio $\gamma = w / h$, the height $h$, and their velocities, with a constant velocity model. It also holds a gallery $G_i$ of the embeddings of its last $L$ detections, with $L = 100$ in the paper, a count of hits, and the count $a_i$ of frames since its last update. A new track is *tentative*. It becomes *confirmed* at its third detection in a row.

**The two distances.** For track $i$ with predicted measurement $y_i$ and covariance $S_i$, and detection $j$ with measurement $z_j$,

$$d_1(i, j) = (z_j - y_i)^{\mathsf T} S_i^{-1} (z_j - y_i), \qquad d_2(i, j) = \min_{g \in G_i} \left(1 - \frac{g \cdot e_j}{\|g\| \, \|e_j\|}\right).$$

A pair is *admissible* if $d_1 \le t_1$ and $d_2 \le t_2$. The gate $t_1 = 9.4877$ is the 95 percent point of the chi-square distribution with 4 degrees of freedom, so a correct measurement passes it with probability 0.95 under the Kalman model. The paper sets $t_2$ on a separate training set; the released code uses $t_2 = 0.2$. The cost of an admissible pair is $c(i, j) = \lambda d_1 + (1 - \lambda) d_2$. The paper uses $\lambda = 0$ in its experiments, so the motion term acts only through the gate.

## The algorithm

```pseudo id=main
DEEP-SORT-STEP(the tracks, the detections (d_j, e_j), A_max, t_1, t_2, λ)
L1   for each track i: Kalman predict; a_i ← a_i + 1
L2   U ← all detections;  for n = 1, 2, ..., A_max:  T_n ← the confirmed tracks with a_i = n
L3       c_ij ← λ d_1(i, j) + (1 - λ) d_2(i, j), admissible only if d_1 ≤ t_1 and d_2 ≤ t_2
L4       min-cost assignment of T_n to U; keep the admissible pairs; remove their detections from U
L5   C ← the tentative tracks and the unmatched tracks with a_i = 1; match C to U on 1 - IoU, keep pairs with IoU ≥ 0.3
L6   for each matched pair (i, j): Kalman update with d_j; add e_j to G_i (keep the last L); a_i ← 0; confirm at 3 hits
L7   delete each unmatched tentative track and each track with a_i > A_max
L8   for each detection j left in U: a new tentative track with G = {e_j}
L9   output the confirmed tracks updated in this frame
```

Lines L2 to L4 are the matching cascade of Listing 1 of the paper. Each level is a separate assignment, solved by the [Hungarian algorithm](/hungarian-algorithm/). In the released code, which the implementation follows, a pair that is not admissible gets a cost just above every admissible cost before the assignment and is removed after it. Line L5 is the IoU stage of the paper, with the IoU bound 0.3 of the released code (a largest IoU distance of 0.7). It helps with sudden changes of appearance and with new tracks that have only one embedding. The paper uses $A_{\max} = 30$ and $L = 100$.

**The filter.** The released code scales the noise by the height $h$ of the box. With $\sigma_p = 1/20$ and $\sigma_v = 1/160$, the standard deviations are $(\sigma_p h, \sigma_p h, 10^{-2}, \sigma_p h)$ for the position part and $(\sigma_v h, \sigma_v h, 10^{-5}, \sigma_v h)$ for the velocity part of the motion noise, $(\sigma_p h, \sigma_p h, 10^{-1}, \sigma_p h)$ for the measurement, and $(2\sigma_p h, 2\sigma_p h, 10^{-2}, 2\sigma_p h, 10\sigma_v h, 10\sigma_v h, 10^{-5}, 10\sigma_v h)$ for a new track.

## Example

**The gallery distance.** A track has the gallery $\{(1, 0), (0, 1)\}$ and a detection has the embedding $(0.6, 0.8)$. The cosine distances are $1 - 0.6 = 0.4$ and $1 - 0.8 = 0.2$, so $d_2 = 0.2$, and the pair passes $t_2 = 0.2$. The gallery lets a track match a view of the person that it saw some frames ago.

**Why the cascade.** A track of a box 40 pixels high moved 2 pixels per frame for 5 frames. A detection lies 10 pixels right and 10 pixels below the predicted center, with the same size. The squared Mahalanobis distance is 15.0 if the track was updated one frame ago, 9.0 after two predictions without an update, and 1.0 after ten. The covariance grows with each prediction, so a track that has been missing for long accepts almost any detection near it, and it gets a *smaller* $d_1$ than a track that is sure of its position. Matching all tracks at once would let old, uncertain tracks take detections from fresh ones. The cascade gives fresh tracks the first choice.

**What the cascade costs.** Track 1 was updated one frame ago and track 2 two frames ago. There are detections $a$ and $b$, with the costs $c(1, a) = 0.10$, $c(1, b) = 0.12$ and $c(2, a) = 0.05$, and the pair $(2, b)$ outside the gate. Level 1 matches track 1 alone and gives it $a$, its cheaper detection. Level 2 offers only $b$ to track 2, which is not admissible. Track 2 has $a_2 = 2$, so it is not in the IoU stage either, and $b$ starts a new track. One assignment over both tracks would match $1 \to b$ and $2 \to a$, two pairs at a total of 0.17. So the cascade can match fewer pairs than a single assignment. The design accepts this to protect fresh tracks.

**A short sequence.** Two people with 8-dimensional embeddings walk for 40 frames. Person 0 walks behind person 1 and is not detected for 10 frames. Deep SORT gives person 0 the same identity before and after the occlusion. With $A_{\max} = 1$, as in SORT, the track of person 0 is deleted during the occlusion and person 0 comes back with a new identity.

## Correctness

Deep SORT is a heuristic tracker, and the claims below are about one frame and about the parts of the method. The proofs are in [proofs/correctness.md](proofs/correctness.md).

- **Theorem: the gate.** If the measurement error is Gaussian with the covariance $S_i$ of the filter, then $d_1$ has the chi-square distribution with 4 degrees of freedom, and $\Pr(d_1 \le t) = 1 - e^{-t/2}(1 + t/2)$. For $t = 9.4877$ this is 0.95.
- **Theorem: each stage.** Each level of the cascade and the IoU stage return an assignment, all kept pairs are admissible, and no track or detection is matched twice over the whole frame.
- **Theorem: priority.** A detection that is admissible for a track of level $n$ and still free at that level is never taken by a track of a level above $n$.
- **Theorem: the cascade is not a global optimum.** The example above shows a frame where the cascade keeps fewer pairs than one assignment over all tracks.
- **Theorem: uncertainty widens the gate.** If $S \preceq S'$ (that is, $S' - S$ is positive semidefinite), then the Mahalanobis distance under $S'$ is at most the distance under $S$ for every offset. This is why the cascade is needed.
- **Not proved.** That the embedding separates people is a property of the network and the data. The improvement on MOT16 is a benchmark result.

## Complexity

Let $n$ be the number of tracks, $m$ the number of detections, $L$ the gallery size and $d$ the embedding dimension, in the [real RAM](/real-ram/) model. The appearance costs need $O(n m L d)$ time, and the gate needs $O(n m)$, since the filter has a fixed size. If level $k$ of the cascade has $n_k$ tracks, its assignment costs $O(n_k m (n_k + m))$, and these add up to $O(n m (n + m))$ because $\sum_k n_k \le n$. The IoU stage costs the same, and the $A$ levels add $O(A)$ for the loop. One frame costs $O(n m (n + m + L d) + A)$ time, and a video of $N$ frames $N$ times that. The galleries take $O(n L d)$ space and the cost matrices $O(n m)$. The network that computes the embeddings is usually the most expensive part, and it is not counted here.

## Properties

- **Online.** The output of a frame never changes later.
- **Long memory.** A confirmed track survives up to $A_{\max}$ missed frames.
- **Appearance needed.** With $\lambda = 0$, a pair is matched in the cascade only if the appearance distance is at most $t_2$, so a bad embedding blocks a match even when the motion fits.
- **Detections above a threshold.** The tracker uses only the detections that the detector reports; it does not look at weak boxes as [ByteTrack](/bytetrack/) does.

## Variants and improvements

- **The combined cost.** With $\lambda > 0$, the motion distance also ranks the pairs. The paper reports that $\lambda = 0$ worked well when the camera moves a lot.
- **Feature update by moving average.** Later trackers replace the gallery by one embedding per track, updated as an [exponential moving average](/exponential-moving-average/), which takes less space and memory traffic.
- **No cascade.** Some later trackers match all tracks in one assignment and handle uncertainty in other ways, for example with a better motion model. The gains are benchmark results.
- **ByteTrack.** [ByteTrack](/bytetrack/) keeps the SORT structure and adds a second round with low-score detections. It can use appearance in its first round too.

## When to use it

Use Deep SORT when objects are hidden for many frames and come back, and when an appearance network for the object class is available, as for pedestrians. It is a common baseline for tracking people. Do not use it when objects of the same class look alike (identical parts on a belt, players in the same jersey), since the appearance score then helps little and the stricter matching can lose tracks. Without a network, use [SORT](/sort-tracker/) or [ByteTrack](/bytetrack/).

## Pitfalls

- **Embeddings from another domain.** A network trained on pedestrians gives poor embeddings for cars. The gate $t_2$ then rejects good pairs or accepts bad ones.
- **Uncertain tracks winning.** Without the cascade, old tracks with large covariance take detections from current tracks, because their Mahalanobis distance is small. Keep the cascade or bound the covariance.
- **Mixing up the state.** The state uses aspect ratio and height, not area and aspect ratio as SORT does. Copying the noise values of one filter into the other gives a badly tuned filter.
- **Gallery size.** A long gallery keeps old views, which helps after occlusions but also matches a different person who looks like an old view. The cost of the appearance term grows with $L$.
- **Counting identity switches only.** Deep SORT trades some MOTA for fewer identity switches. Compare trackers with an identity measure such as [IDF1](/idf1-score/) or [HOTA](/hota-metric/) as well as with the [CLEAR MOT metrics](/clear-mot-metrics/).

## Implementations

The Python file follows the paper and its released code: the 8-dimensional filter with noise scaled by the height, the gate 9.4877, a gallery of 100 embeddings, $t_2 = 0.2$, $\lambda = 0$, the cascade over 30 levels, and an IoU stage with bound 0.3. The embeddings are inputs. The tests check the gate probability by sampling from the filter, compare the assignment with brute force, check the cascade example and the Mahalanobis values above, and run the occlusion sequence.

## History

In 2017, Wojke, Bewley and Paulus extended SORT with a deep association metric. The network was a wide residual network that gives a 128-dimensional embedding, trained on the MARS person re-identification data, with over 1,100,000 images of 1,261 pedestrians. They reported on MOT16 that the identity switches fell from 1423 for SORT to 781, with MOTA 61.4 against 59.8 for SORT. The paper presents the matching cascade as a way to give priority to the objects seen more often. Deep SORT became the base of many later trackers, which keep its structure and change the detector, the network or the motion model.

## References
