---
tag: GXDF6Q
kind: problem
slug: data-association
name: Data association
aliases:
- measurement-to-track assignment
area: computer-vision/visual-tracking
level: core
summary: Decide which measurement in a frame comes from which existing track, which is a new track and which is clutter.
model: real-ram
complexity:
  vars: {n: the number of tracks, m: the number of measurements in the frame}
  time: {worst: O((n + m)³)}
prereqs: [track-gating, kalman-filter, assignment-problem]
see_also: [multi-object-tracking, tracking-by-detection, data-association-slam, hungarian-algorithm, bipartite-matching, three-dimensional-matching, permanent-computation, min-cost-flow-problem]
sources:
  - book: isbn:9780120797608
    title: Yaakov Bar-Shalom and Thomas E. Fortmann, Tracking and Data Association, Academic Press, 1988
    locator: the whole book (validation gates, nearest neighbor and probabilistic data association, track initiation)
  - book: isbn:9781580530064
    title: Samuel S. Blackman and Robert Popoli, Design and Analysis of Modern Tracking Systems, Artech House, 1999
    locator: the chapters on gating and on data association
  - paper: doi:10.1007/BF01440847
    title: Ingemar J. Cox, A review of statistical data association techniques for motion correspondence, International Journal of Computer Vision 10(1), 1993, 53 to 66
    locator: the whole paper (nearest neighbor, PDA, JPDA and MHT, presented for motion correspondence in vision)
  - paper: doi:10.1109/TAC.1979.1102177
    title: Donald B. Reid, An algorithm for tracking multiple targets, IEEE Transactions on Automatic Control 24(6), 1979, 843 to 854
    locator: the whole paper (association hypotheses with new targets and false alarms, and their probabilities)
  - paper: doi:10.1109/JOE.1983.1145560
    title: Thomas E. Fortmann, Yaakov Bar-Shalom and Molly Scheffe, Sonar tracking of multiple targets using joint probabilistic data association, IEEE Journal of Oceanic Engineering 8(3), 1983, 173 to 184
    locator: the whole paper (joint association events and their probabilities)
---

Data association is the problem of deciding, for the measurements of one frame, which one comes from which existing track, which one starts a new track, and which one is clutter, a false measurement. A measurement here is a detection, a radar return or a feature point, and a track is a running estimate of one object, usually kept by a [Kalman filter](/kalman-filter/) that predicts where its next measurement should fall. Each track gives rise to at most one measurement and each measurement comes from at most one object, so an answer is a partial one-to-one matching between tracks and measurements. Data association is the central subproblem of [multi-object tracking](/multi-object-tracking/), which also includes detecting the objects and managing the tracks. [Tracking by detection](/tracking-by-detection/) is the design that runs a detector and then solves data association in every frame. [SORT](/sort-tracker/), [DeepSORT](/deep-sort/) and [ByteTrack](/bytetrack/) are complete trackers that each solve this problem one frame at a time with an assignment and add their own rules for starting and ending tracks. The same name is used in robotics for [data association in SLAM](/data-association-slam/), where the measurements are matched to fixed landmarks of a map. There the landmarks do not move, the main danger is an error that corrupts the map, and pairings are tested for joint consistency. In tracking the objects move, are born and die, and clutter is part of the model.

## In plain words

A lighthouse keeper writes down the boats he knows and where each should be by now. Then the radar shows some blips. He must say which blip is which boat. Some boats may not show on the radar this time. Some blips are waves, not boats. A blip far from every known boat may be a new boat. If two boats are close, a blip between them could be either one, and a wrong guess gives one boat the other's path. The keeper wants the explanation that makes the most sense for all the boats and blips together, not one boat at a time.

## Definition

**One frame.** There are $n$ tracks, and track $i$ predicts its measurement as a Gaussian with mean $\hat z_i$ and covariance $S_i$. There are $m$ measurements $z_1, \ldots, z_m$. An *association* is a set of pairs $(i, j)$ in which no track and no measurement appears twice. The tracks in no pair are *missed*, and the measurements in no pair are new tracks or clutter. A pair is *allowed* only if $z_j$ falls inside the [gate](/track-gating/) of track $i$, that is, if the squared Mahalanobis distance $d_{ij}^2 = (z_j - \hat z_i)^\mathsf{T} S_i^{-1} (z_j - \hat z_i)$ is at most a threshold $\gamma$.

There are two kinds of output.

- **A hard decision.** One association of least cost, where the cost is the sum of the costs of the pairs, often $d_{ij}^2$ or the negative log-likelihood, plus a cost for each missed track and each leftover measurement.
- **Soft weights.** For each pair, the probability $\beta_{ij}$ that it is in the true association, under a model of detection probability, measurement noise and clutter.

**Several frames.** The measurements of $S$ frames are given at once, and the answer is a set of tracks, each taking at most one measurement per frame, with no measurement in two tracks. The cost of a track can depend on all its measurements.

## Variants

- **Single-scan and multi-scan.** One frame at a time, as in [GNN](/global-nearest-neighbor-association/) and [JPDA](/joint-probabilistic-data-association/), or several frames, as in [MHT](/multiple-hypothesis-tracking/) and [network flow tracking](/network-flow-tracking/).
- **Hard and soft.** One best association, or weights over all of them.
- **Known and unknown number of objects.** JPDA keeps a fixed set of tracks. GNN, MHT and network flows also decide births and deaths.
- **Motion and appearance.** In vision, the cost can add a distance between appearance features, as in DeepSORT, or use the overlap of boxes, as in SORT.
- **No association.** The [PHD filter](/phd-filter/) updates a density of targets with all measurements and never forms pairs.
- **Static landmarks.** [Data association in SLAM](/data-association-slam/) matches measurements to map features, often with the [joint compatibility test](/joint-compatibility-branch-and-bound/).

## Examples

**Greedy against global.** Two tracks $A$ and $B$ and two measurements have the costs

| | $z_1$ | $z_2$ |
|---|---|---|
| $A$ | 1 | 4 |
| $B$ | 2 | 8 |

Taking the cheapest pair first gives $A$-$z_1$ for 1, and then $B$ must take $z_2$ for 8, a total of 9. The association $A$-$z_2$, $B$-$z_1$ costs $4 + 2 = 6$. A rule that looks at one track at a time misses it, and solving the [assignment problem](/assignment-problem/) finds it.

**Gating and leftovers.** Let the gate be $\gamma = 9.21$, the 99 percent point of the chi-square distribution with 2 degrees of freedom, and let a missed track or a leftover measurement cost $\gamma / 2$. Leaving a track and a measurement both unpaired then costs $9.21 / 2 + 9.21 / 2 = 9.21$. A pair with $d^2 = 6$ is inside the gate and costs less than that, so a track and a measurement that have no better partners are paired. A pair with $d^2 = 10$ is outside the gate, so the measurement starts a new track or is clutter.

**Counting hypotheses.** If every measurement is in every gate, the number of associations is $\sum_{k=0}^{\min(n,m)} \binom{n}{k} \binom{m}{k} k!$. For $n = m = 3$ this is 34, and for $n = m = 10$ it is 234,662,231.

## Known algorithms

| Algorithm | Output | Frames | Cost |
|---|---|---|---|
| Nearest neighbor (greedy) | one association, not optimal | one | $O(n m \log(n m))$ |
| [Global nearest neighbor](/global-nearest-neighbor-association/) | one association of least cost | one | $O((n + m)^3)$ |
| [JPDA](/joint-probabilistic-data-association/) | soft weights $\beta_{ij}$ | one | exponential in the cluster size |
| [Multiple hypothesis tracking](/multiple-hypothesis-tracking/) | the most likely associations, kept over frames | several | grows with the hypotheses kept |
| [Network flow tracking](/network-flow-tracking/) | all tracks of a video | all | $O(K n (n + L))$ for $K$ tracks and $L$ links |

The assignment inside GNN and MHT can be solved by the [Hungarian algorithm](/hungarian-algorithm/), the [Jonker-Volgenant algorithm](/jonker-volgenant-algorithm/) or the [auction algorithm](/auction-algorithm/). [Gating](/track-gating/) removes the pairs that are too far apart before any of them run.

## Bounds

- **One frame, hard decision.** Add one dummy column per track for a miss and one dummy row per measurement for a leftover. The result is an assignment problem of size $n + m$, solved in $O((n + m)^3)$ time, the bound in the front matter. The proof is on the [GNN](/global-nearest-neighbor-association/) page.
- **One frame, unit costs.** If every allowed pair costs the same, the best association is a maximum [bipartite matching](/bipartite-matching/) of the gate graph.
- **Three or more frames.** Data association over three frames, with a cost for each track of three measurements, is NP-hard. It contains [three-dimensional matching](/three-dimensional-matching/). The reduction is in the proof on the [MHT](/multiple-hypothesis-tracking/) page. So multi-scan methods prune, limit the window or accept approximate answers.
- **Pairwise costs over many frames.** If the cost of a track is a sum over consecutive pairs, the problem over all frames is a [min-cost flow problem](/min-cost-flow-problem/) and is solved in polynomial time.
- **Soft weights.** With detection probability 1, $n = m$ and every pair allowed, the normalizing sum of JPDA is the [permanent](/permanent-computation/) of the likelihood matrix divided by $\lambda^n$, so exact weights are #P-hard. The proof is on the [JPDA](/joint-probabilistic-data-association/) page.

## Reductions

- **To the assignment problem.** One frame with a hard decision, as above.
- **To min-cost flow.** All frames with pairwise costs.
- **From three-dimensional matching.** This shows the hardness of three or more frames.
- **To the permanent.** The JPDA weights with every pair allowed.
- **From multi-object tracking.** Each frame of an online tracker poses one instance of data association.

## Applications

- The association step of radar, sonar and air traffic trackers.
- The linking step of tracking-by-detection in video, for people, vehicles and cells.
- Feature correspondence between frames for motion estimation.
- Matching measurements to landmarks in mapping, in its SLAM form.
- Linking particle detections into trajectories in physics and biology.

## References
