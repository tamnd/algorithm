---
tag: 1N0W1F
kind: technique
slug: track-gating
name: Gating
aliases:
- validation gate
- ellipsoidal gating
area: computer-vision/visual-tracking
level: core
summary: Consider for each track only the measurements within a Mahalanobis distance threshold of its predicted position, which prunes the association problem.
prereqs: [kalman-filter, covariance-matrix]
see_also: [data-association, global-nearest-neighbor-association, joint-probabilistic-data-association, multiple-hypothesis-tracking, deep-sort, data-association-slam, kd-tree, chi-squared-goodness-of-fit-test]
sources:
  - book: isbn:9780120797608
    title: Yaakov Bar-Shalom and Thomas E. Fortmann, Tracking and Data Association, Academic Press, 1988
    locator: the chapters on validation gates and on probabilistic data association (the gate probability and the volume of the gate)
  - book: isbn:9781580530064
    title: Samuel S. Blackman and Robert Popoli, Design and Analysis of Modern Tracking Systems, Artech House, 1999
    locator: the chapter on gating (rectangular and ellipsoidal gates and the choice of the threshold)
  - paper: doi:10.1109/7.256316
    title: Joseph B. Collins and Jeffrey K. Uhlmann, Efficient gating in data association with multivariate Gaussian distributed states, IEEE Transactions on Aerospace and Electronic Systems 28(3), 1992, 909 to 916
    locator: the whole paper (gating with search trees, so that not every pair of a track and a measurement is tested)
  - paper: doi:10.1109/ICIP.2017.8296962
    title: Nicolai Wojke, Alex Bewley and Dietrich Paulus, Simple online and realtime tracking with a deep association metric, IEEE International Conference on Image Processing (ICIP), 2017, 3645 to 3649
    locator: the association step (the Mahalanobis gate at the 95 percent point of the chi-square distribution with 4 degrees of freedom, 9.4877)
---

Gating is the step of a tracker that decides, before any association, which measurements a track may take at all. Each track predicts its next measurement as a Gaussian with mean $\hat z$ and covariance $S$, the innovation covariance of a [Kalman filter](/kalman-filter/). A measurement $z$ passes the gate of the track if its squared Mahalanobis distance $d^2 = (z - \hat z)^\mathsf{T} S^{-1} (z - \hat z)$ is at most a threshold $\gamma$. The set of such $z$ is an ellipse, or an ellipsoid in more dimensions, around the prediction, stretched in the directions where the track is uncertain. If the track is right and the model holds, $d^2$ of the true measurement follows the chi-square distribution with $p$ degrees of freedom, where $p$ is the dimension of a measurement. So $\gamma$ is chosen as a quantile of that distribution, and the gate keeps the true measurement with a known probability $P_G$. Pairs outside the gate are dropped, which makes the [data association](/data-association/) problem smaller and splits it into independent clusters.

## In plain words

A track says: my object should show up about here, and I am more sure in some directions than in others. Gating draws an oval around that spot, long where the track is unsure and narrow where it is sure. Only the measurements inside the oval are candidates for the track. The size of the oval is set so that the true measurement lands inside it, say, 99 times out of 100. Everything outside is ignored for this track, so the later steps have far fewer choices to compare.

## When it applies

The setting is a tracker with a predicted measurement and a covariance for each track, such as a Kalman filter, an [extended Kalman filter](/extended-kalman-filter/) or a [particle filter](/particle-filter/) with a Gaussian summary. It applies when:

- **the prediction is close to Gaussian.** Then $d^2$ is close to chi-square and the threshold has its stated meaning. For other shapes the gate is still useful but its probability is not known;
- **the covariance is honest.** The gate is only as good as $S$. A filter that is too sure of itself gives gates that are too small;
- **there are many tracks or measurements.** With $n$ tracks and $m$ measurements, association methods cost at least $n m$ and often far more. Gating with a search structure avoids even the $n m$ tests.

Common thresholds for the ellipsoidal gate are:

| Degrees of freedom $p$ | $P_G = 0.95$ | $P_G = 0.99$ |
|---|---|---|
| 2 | 5.991 | 9.210 |
| 4 | 9.488 | 13.277 |

For $p = 2$ the distribution is exponential, so $P_G = 1 - e^{-\gamma / 2}$ and $\gamma = -2 \ln(1 - P_G)$. DeepSORT gates its 4-dimensional box measurement at 9.4877.

## The template

```pseudo id=main
GATE(the tracks, the measurements z_1..z_m, γ)
L1   for each track i: compute ẑ_i, S_i and S_i⁻¹ from the prediction
L2   for each track i: B_i ← the box |ν_k| ≤ sqrt(γ (S_i)_kk) for each coordinate k
L3       C_i ← COARSE-SEARCH(B_i, the measurements)       ▷ all of them, a grid, or a kd-tree
L4       for each j in C_i: d²_ij ← (z_j - ẑ_i)ᵀ S_i⁻¹ (z_j - ẑ_i)
L5           if d²_ij ≤ γ: add the pair (i, j) to the gate graph
L6   return the gate graph and its connected components, the clusters
```

The holes are the threshold $\gamma$, from the table above or tuned, and COARSE-SEARCH, which must return every measurement in the box $B_i$ and may return more. The box is safe: the largest value of a coordinate $\nu_k$ on the ellipse $\nu^\mathsf{T} S^{-1} \nu = \gamma$ is $\sqrt{\gamma S_{kk}}$, so the ellipse lies inside the box. Line L6 matters for [JPDA](/joint-probabilistic-data-association/) and [MHT](/multiple-hypothesis-tracking/): tracks in different clusters share no measurement, so each cluster is solved alone.

**A worked gate.** Let $S = \operatorname{diag}(4, 1)$ and $\gamma = 5.991$. The box is $|\nu_x| \le 4.90$, $|\nu_y| \le 2.45$. A measurement at offset $(3, 1)$ has $d^2 = 9/4 + 1 = 3.25$ and passes. A measurement at offset $(1, 2.6)$ is closer in plain distance, 2.79 against 3.16, but it fails the box test and has $d^2 = 0.25 + 6.76 = 7.01 > 5.991$. The track is sure of its $y$ coordinate, so a miss in $y$ counts more. The area of the gate is $\pi \gamma \sqrt{\det S} = 37.6$, and with a clutter density $\lambda$ the gate holds on average $37.6 \lambda$ false measurements.

## Classic examples

- **[Global nearest neighbor](/global-nearest-neighbor-association/).** Pairs outside the gate get an infinite cost in the assignment, and the cost of a miss is set from $\gamma$.
- **[JPDA](/joint-probabilistic-data-association/).** Only gated measurements enter the joint events, and the gate probability $P_G$ appears in the weight $1 - p_D P_G$ of a missed track.
- **[Multiple hypothesis tracking](/multiple-hypothesis-tracking/).** Gating limits the children of each hypothesis to the measurements a track can explain.
- **[DeepSORT](/deep-sort/).** The motion gate at 9.4877 removes pairs before the appearance distance decides among the rest.
- **[Network flow tracking](/network-flow-tracking/).** Links between detections are added only if they pass a gate, which keeps the graph sparse.
- **[Data association in SLAM](/data-association-slam/).** The individual compatibility test is a chi-square gate between a measurement and a landmark, and [joint compatibility](/joint-compatibility-branch-and-bound/) gates sets of pairs.

## Variations

- **Rectangular gates.** Only the box test of line L2, cheaper and used as a first stage.
- **Search trees.** Collins and Uhlmann (1992) used search trees to find the candidates of each gate without testing every pair. A [kd-tree](/kd-tree/) over the measurements, queried with the box of each track, is one such structure.
- **Overlap gates.** Trackers of boxes, such as [SORT](/sort-tracker/), reject pairs whose [intersection over union](/intersection-over-union/) is below a threshold.
- **Appearance gates.** A pair is dropped if the distance between appearance features is too large.
- **Maneuver gates.** A track that may turn gets a larger $\gamma$, or a gate from a second motion model.
- **Gates that grow.** A track that has not been seen for some frames has a larger $S$, so its gate grows by itself.

## Pitfalls

- **The wrong degrees of freedom.** The threshold depends on the dimension of the measurement. Using 5.991, the 2-dimensional value, for a 4-dimensional measurement keeps only about 80 percent of the true measurements, since $1 - e^{-\gamma/2}(1 + \gamma/2) = 0.80$ there.
- **Using $P$ in place of $S$.** The gate must use the covariance of the predicted measurement, $S = H P H^\mathsf{T} + R$, which includes the measurement noise $R$.
- **An overconfident filter.** If the process noise is too small, $S$ is too small, the true measurement falls outside the gate, and the track is lost for good.
- **A gate that is too large.** It admits clutter and other targets. The cost of JPDA and MHT grows quickly with the size of the clusters.
- **Mixed units.** If the coordinates have different units, Euclidean gates are meaningless. The Mahalanobis distance fixes this through $S$.
- **Forgetting $P_G$.** Probabilistic methods must account for the true measurements that fall outside the gate, or their weights are slightly wrong.

## Exercises

1. Show that for $p = 2$ the gate probability is $1 - e^{-\gamma/2}$, and find $\gamma$ for $P_G = 0.999$.
2. Prove that the largest value of $\nu_k$ on the ellipse $\nu^\mathsf{T} S^{-1} \nu = \gamma$ is $\sqrt{\gamma S_{kk}}$.
3. The volume of the gate in $p$ dimensions is $c_p \gamma^{p/2} \sqrt{\det S}$ with $c_p$ the volume of the unit ball. Compute it for $p = 2$ and $p = 3$, and explain why the expected number of clutter points in the gate is the volume times $\lambda$.
4. For $n$ tracks and $m$ measurements spread over a large area, estimate how many pairs a kd-tree search examines compared with testing all $n m$ pairs.
5. Two tracks have overlapping gates that share one measurement. Write down the clusters of line L6, and show how adding a third track can merge two clusters into one.

## References
