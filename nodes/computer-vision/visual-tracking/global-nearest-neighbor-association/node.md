---
tag: VW85MF
kind: algorithm
slug: global-nearest-neighbor-association
name: Global nearest neighbor association
aliases:
- GNN data association
area: computer-vision/visual-tracking
level: core
summary: Assign measurements to tracks by the one-to-one assignment of least total distance in each frame, solved with the Hungarian or auction algorithm.
solves: [data-association]
model: real-ram
complexity:
  vars: {n: the number of tracks, m: the number of measurements in the frame, p: the dimension of a measurement}
  time: {worst: O(n p³ + n m p² + (n + m)³), average: O(n p³ + n m p² + (n + m)³), best: Ω(n m p² + (n + m)²)}
  space: {extra: Θ((n + m)²)}
properties: {deterministic: true, exact: true, local: false, iterative: false, online: true}
history:
  year: 1986
  people: [Samuel S. Blackman]
  note: Radar tracking texts of the 1980s, among them Blackman's 1986 book, solved the measurement-to-track association of one scan as an optimal assignment with the Munkres algorithm, next to cheaper greedy rules. Blackman later called this the global nearest neighbor (GNN) approach.
prereqs: [kalman-filter, track-gating, assignment-problem, hungarian-algorithm]
see_also: [data-association, joint-probabilistic-data-association, multiple-hypothesis-tracking, auction-algorithm, jonker-volgenant-algorithm, greedy-algorithm, sort-tracker, tracking-by-detection]
sources:
  - book: isbn:9781580530064
    title: Samuel S. Blackman and Robert Popoli, Design and Analysis of Modern Tracking Systems, Artech House, 1999
    locator: the chapters on gating and on data association (the global nearest neighbor method and its solution as an assignment problem)
  - paper: doi:10.1109/MAES.2004.1263228
    title: Samuel S. Blackman, Multiple hypothesis tracking for multiple target tracking, IEEE Aerospace and Electronic Systems Magazine 19(1), 2004, 5 to 18
    locator: the introduction (the name GNN for the single best assignment of each scan, and its comparison with MHT)
  - book: isbn:9780120797608
    title: Yaakov Bar-Shalom and Thomas E. Fortmann, Tracking and Data Association, Academic Press, 1988
    locator: the chapters on validation gates and on the nearest neighbor and assignment approaches to association
  - paper: doi:10.1002/nav.3800020109
    title: Harold W. Kuhn, The Hungarian method for the assignment problem, Naval Research Logistics Quarterly 2(1-2), 1955, 83 to 97
    locator: the whole paper (the Hungarian method)
---

Global nearest neighbor association, or GNN, decides in each frame which measurement belongs to which track. Each track predicts where its next measurement should be, with a covariance. The cost of giving measurement $j$ to track $i$ is the squared Mahalanobis distance between them, and a pair outside the gate is not allowed. A track may stay without a measurement, and a measurement may stay without a track, each at a fixed cost. GNN then picks the one-to-one assignment of least total cost over all tracks at once, with the [Hungarian algorithm](/hungarian-algorithm/) or another solver of the [assignment problem](/assignment-problem/). The word "global" is the difference from the local nearest neighbor rule, which lets each track take its closest measurement and so can give one measurement to two tracks, or take a measurement that another track needs more. GNN keeps exactly one hypothesis per frame and never revises it, which is what separates it from [JPDA](/joint-probabilistic-data-association/) and [MHT](/multiple-hypothesis-tracking/).

## In plain words

A teacher has a seating chart with the places where each student should sit, but the students walked in and sat down a little off. To match students to names, the teacher could let each name grab the nearest student. That fails when two names want the same student. GNN instead looks at all possible ways to match names to students and picks the one where the sum of the distances is smallest. Some names may have no student today, because the student is absent, and some students may be new. Each of these leftovers costs a fixed penalty, so a far-away match is not forced just to use everyone. The teacher then moves each name to where its student actually sits, and the next day starts again.

## The problem

The input of one frame is a set of $n$ tracks and a set of $m$ measurements $z_1, \ldots, z_m$ in $\mathbb{R}^p$. Each track $i$ has a state estimate and a covariance, which a [Kalman filter](/kalman-filter/) predicts to the time of the frame. From the prediction come the predicted measurement $\hat z_i = H \hat x_i$ and the innovation covariance $S_i = H P_i H^{\mathsf T} + R$. The gate is a threshold $\gamma$ on the squared Mahalanobis distance, for example the 99 percent point $\gamma = 9.210$ of the chi-square distribution with 2 degrees of freedom, as on [track gating](/track-gating/).

A feasible answer is a partial one-to-one matching $M$ of tracks to measurements in which every pair is inside the gate. Its cost is

$$
J(M) = \sum_{(i, j) \in M} d^2_{ij} + c_{\text{miss}} \cdot (\text{tracks not in } M) + c_{\text{new}} \cdot (\text{measurements not in } M),
$$

with $d^2_{ij} = (z_j - \hat z_i)^{\mathsf T} S_i^{-1} (z_j - \hat z_i)$. GNN returns a matching of least cost. The tracks in $M$ are updated with their measurements, the other tracks coast on their prediction, and the other measurements can start new tracks. In a likelihood form, $d^2_{ij}$ is replaced by $d^2_{ij} + \ln \det S_i$, the negative log of the Gaussian density up to a constant. This page uses the plain distance, as many trackers do.

## The algorithm

```pseudo id=main
GNN-STEP(the tracks, the measurements z_1..z_m, the gate γ, the costs c_miss and c_new)
L1   for each track i: predict x̂_i and P_i, then ẑ_i ← H x̂_i and S_i ← H P_i Hᵀ + R
L2   for each track i and each measurement j do
L3       d²_ij ← (z_j - ẑ_i)ᵀ S_i⁻¹ (z_j - ẑ_i)
L4       c_ij ← d²_ij if d²_ij ≤ γ, else ∞
L5   A ← the (n + m) × (m + n) matrix [[C, D_miss], [D_new, 0]]    ▷ D_miss, D_new: c_miss, c_new on the diagonal, ∞ elsewhere
L6   solve the assignment problem on A with the Hungarian algorithm
L7   for each track i assigned to a column j ≤ m: Kalman update of track i with z_j
L8   other tracks: count a miss, delete after too many; other measurements: start a new track
```

The matrix of line L5 has one row per track and one dummy row per measurement, and one column per measurement and one dummy column per track. A track that takes its own dummy column is missed, at the cost $c_{\text{miss}}$. A measurement whose dummy row takes the measurement's column is left over, at the cost $c_{\text{new}}$. The block of zeros lets the dummy rows of the matched measurements take the dummy columns of the matched tracks for free. So every assignment of finite cost of $A$ is a partial matching of the same cost, and the reverse is also true. The default $c_{\text{miss}} = c_{\text{new}} = \gamma / 2$ makes every gated pair at least as cheap as leaving both of its ends unmatched.

Line L8 is the track management. It is a heuristic and not part of the optimization. The code deletes a track after 3 frames in a row with no measurement and starts a track at every leftover measurement, with zero velocity and a large velocity variance.

## Example

Two tracks predict $\hat z_A = (0, 0)$ and $\hat z_B = (2, 0)$, both with $S = I$. The frame has three measurements, $z_1 = (1.2, 0)$, $z_2 = (3.5, 0)$ and $z_3 = (10, 5)$. The gate is $\gamma = 9.21$, and $c_{\text{miss}} = c_{\text{new}} = 4.605$. The squared distances are

| | $z_1$ | $z_2$ | $z_3$ |
|---|---|---|---|
| A | 1.44 | 12.25 (outside the gate) | 125 (outside) |
| B | 0.64 | 2.25 | 89 (outside) |

**The local rule.** The closest gated pair is B and $z_1$, at 0.64. After it is taken, track A has no measurement left in its gate, so A is missed, and $z_2$ and $z_3$ start new tracks. The cost is $0.64 + 3 \cdot 4.605 = 14.455$. The real target of A is lost, and the real target of B gets a second track.

**GNN.** The augmented matrix, with the rows A, B and the dummy rows of $z_1, z_2, z_3$, and the columns $z_1, z_2, z_3$ and the dummy columns of A and B, is

$$
A = \begin{pmatrix}
1.44 & \infty & \infty & 4.605 & \infty \\
0.64 & 2.25 & \infty & \infty & 4.605 \\
4.605 & \infty & \infty & 0 & 0 \\
\infty & 4.605 & \infty & 0 & 0 \\
\infty & \infty & 4.605 & 0 & 0
\end{pmatrix}.
$$

Its least-cost assignment takes A to $z_1$, B to $z_2$, the dummy row of $z_3$ to $z_3$, and the dummy rows of $z_1$ and $z_2$ to the two dummy columns. The cost is $1.44 + 2.25 + 4.605 = 8.295$. Track B gives up its closest measurement because track A has no other choice, and only $z_3$, which is far from both tracks, starts a new track.

**A short sequence.** The code also runs a tracker with a constant velocity model on three targets for 30 frames, with measurement noise of standard deviation 0.5, one clutter point every 7 frames, and two targets whose paths cross near frame 14. Each target keeps the same track through the crossing, and the mean position error after frame 5 is below 0.6. The clutter points start short tracks that die after 3 frames.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows these facts.

- **Theorem: the gate.** If the true measurement is Gaussian with the predicted mean and covariance $S_i$, then $d^2_{ij}$ has the chi-square distribution with $p$ degrees of freedom. For $p = 2$ the gate $\gamma$ keeps it with probability exactly $1 - e^{-\gamma/2}$, which is 0.99 for $\gamma = 9.21$.
- **Theorem: the augmented matrix.** The partial matchings inside the gate and the assignments of finite cost of $A$ correspond, with equal costs. So an optimal assignment of $A$ gives an optimal matching for the cost $J$. Such an assignment always exists, because all tracks missed and all measurements new is finite.
- **Theorem: gated pairs are used.** If $d^2_{ij} < c_{\text{miss}} + c_{\text{new}}$, no optimal matching leaves both track $i$ and measurement $j$ unmatched.
- **Theorem: never worse than the local rule.** The cost of GNN is at most the cost of the greedy nearest neighbor matching, and the example shows that it can be strictly less.

These facts are about one frame. Whether the tracks follow the true targets over many frames depends on the motion model, the detection rate and the clutter, and is not proved.

## Complexity

With the inverse of $S_i$ computed once per track, the distances cost $O(n p^3 + n m p^2)$. The augmented matrix has $(n + m)^2$ entries. The Hungarian algorithm with potentials solves an $N \times N$ assignment in $O(N^3)$ time, so a frame costs $O(n p^3 + n m p^2 + (n + m)^3)$ time and $\Theta((n + m)^2)$ extra space. The Kalman updates of line L7 add $O(n d^3)$ for a state of dimension $d$. In practice the gate makes the matrix sparse, and trackers split it into independent clusters of tracks that share gated measurements, then solve each cluster alone. A cluster of size $k$ costs $O(k^3)$, so many small clusters are much cheaper than one large matrix.

## Properties

- **One hypothesis.** GNN keeps a single assignment per frame and never changes a past decision.
- **Optimal for its frame.** The assignment is the best one under the cost $J$, not just a good one.
- **Deterministic.** The same input gives the same output, up to ties between assignments of equal cost.
- **Hard decisions.** A track takes a full measurement or none. A wrong assignment is used as if it were right, and the error goes into the state.
- **Independent of order.** Unlike the greedy rule, the result does not depend on the order of the tracks or the measurements.

## Variants and improvements

- **Other assignment solvers.** The [auction algorithm](/auction-algorithm/) of Bertsekas and the [Jonker-Volgenant algorithm](/jonker-volgenant-algorithm/) solve the same problem, often faster on sparse matrices.
- **Rectangular matrices.** Instead of dummy rows and columns, a solver for rectangular matrices with a cost of non-assignment can work on the $n \times m$ matrix directly.
- **Likelihood costs.** Use $d^2_{ij} + \ln \det S_i$, and costs of a miss and of a new target taken from the detection probability and the clutter density.
- **Two-stage matching.** [ByteTrack](/bytetrack/) matches the high-confidence detections first and the low-confidence ones second, each stage by an assignment.
- **IoU costs.** [SORT](/sort-tracker/) uses $1 - \mathrm{IoU}$ between predicted and detected boxes as the cost, with a threshold on the IoU as the gate.
- **Soft association.** [JPDA](/joint-probabilistic-data-association/) replaces the single assignment by a weighted average over all feasible assignments.
- **Deferred decisions.** [MHT](/multiple-hypothesis-tracking/) keeps the best few assignments per frame and decides later.

## When to use it

Use GNN when targets are mostly well apart, the detection rate is high, and clutter is light. Many tracking-by-detection systems for video are of this kind, and GNN is their usual association step. It is cheap and easy to reason about. When targets come close and stay close for many frames, or the clutter is dense, a single wrong decision can swap identities for good, and [JPDA](/joint-probabilistic-data-association/) or [MHT](/multiple-hypothesis-tracking/) do better at a higher cost.

## Pitfalls

- **Costs of a miss and a new track that are too low.** Then the solver prefers to leave good pairs unmatched. With $c_{\text{miss}} + c_{\text{new}}$ below a gated distance, a true pair can be split.
- **Costs that are too high.** Then far pairs inside a wide gate are forced, and clutter attaches to tracks.
- **A large finite value instead of infinity.** If "forbidden" is a big number, the solver can still pick it when nothing else fits, and the caller must check every pair against the gate.
- **Distances with different covariances.** A track with a large $S_i$ gets small distances to everything. The term $\ln \det S_i$ fixes this in the likelihood form.
- **Greedy instead of global.** Taking the closest pair first is not GNN and can be much worse, as the example shows.
- **Track management taken as part of the method.** The rules for starting and deleting tracks are heuristics, and they often matter more than the assignment.

## Implementations

## History

The assignment problem was solved by Harold Kuhn's Hungarian method in 1955, and James Munkres showed in 1957 that it runs in polynomial time. Radar trackers of the 1970s and 1980s used it to associate the returns of one scan with the existing tracks. Samuel Blackman's book of 1986, Multiple-Target Tracking with Radar Applications, presented the optimal assignment by the Munkres algorithm next to cheaper suboptimal rules, and his later survey of 2004 named the single best assignment of each scan the global nearest neighbor approach. Bar-Shalom and Fortmann (1988) and Blackman and Popoli (1999) give the method with gating and track management. In computer vision, the same step became the core of tracking-by-detection systems such as [SORT](/sort-tracker/) (2016) and [Deep SORT](/deep-sort/) (2017), with box overlap or appearance features as the cost.

## References
