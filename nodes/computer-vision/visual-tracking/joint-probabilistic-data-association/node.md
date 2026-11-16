---
tag: GVT723
kind: algorithm
slug: joint-probabilistic-data-association
name: Joint probabilistic data association
aliases:
- JPDA
- JPDA filter
area: computer-vision/visual-tracking
level: advanced
summary: Update each track with a weighted mix of all gated measurements, the weights being posterior probabilities summed over all joint feasible assignments.
solves: [data-association]
model: real-ram
complexity:
  vars: {n: the number of tracks, m: the number of measurements, E: the number of joint events, p: the dimension of a measurement, d: the dimension of a state}
  time: {worst: O(E n + n m p² + n (p³ + d³)), average: O(E n + n m p² + n (p³ + d³)), best: O(E n + n m p² + n (p³ + d³))}
  space: {extra: O(n m + n d²)}
properties: {deterministic: true, exact: false, local: false, iterative: false, online: true}
history:
  year: 1983
  people: [Thomas E. Fortmann, Yaakov Bar-Shalom, Molly Scheffe]
  note: Fortmann, Bar-Shalom and Scheffe extended the probabilistic data association filter of Bar-Shalom and Tse (1975) from one target to several, and applied it to passive sonar tracking of several targets in clutter.
prereqs: [kalman-filter, track-gating, data-association, conditional-probability]
see_also: [global-nearest-neighbor-association, multiple-hypothesis-tracking, permanent-computation, ryser-formula, loopy-belief-propagation, phd-filter, poisson-distribution, multi-object-tracking]
sources:
  - paper: doi:10.1109/JOE.1983.1145560
    title: Thomas E. Fortmann, Yaakov Bar-Shalom and Molly Scheffe, Sonar tracking of multiple targets using joint probabilistic data association, IEEE Journal of Oceanic Engineering 8(3), 1983, 173 to 184
    locator: the whole paper (joint events, their probabilities and the state update)
  - paper: "Yaakov Bar-Shalom and Edison Tse, Tracking in a cluttered environment with probabilistic data association, Automatica 11(5), 1975, 451 to 460"
    locator: the whole paper (the PDA filter for one target)
  - book: isbn:9780120797608
    title: Yaakov Bar-Shalom and Thomas E. Fortmann, Tracking and Data Association, Academic Press, 1988
    locator: the chapters on the PDA and JPDA filters
  - paper: doi:10.1109/TAES.2014.120568
    title: Jason L. Williams and Roslyn A. Lau, Approximate evaluation of marginal association probabilities with belief propagation, IEEE Transactions on Aerospace and Electronic Systems 50(4), 2014, 2942 to 2959
    locator: the introduction (the link of the marginal probabilities to the permanent) and the belief propagation method
  - paper: doi:10.1109/7.256316
    title: Joseph B. Collins and Jeffrey K. Uhlmann, Efficient gating in data association with multivariate Gaussian distributed states, IEEE Transactions on Aerospace and Electronic Systems 28(3), 1992, 909 to 916
    locator: the whole paper (gating with search trees, which keeps the clusters and the joint events few)
---

Joint probabilistic data association, or JPDA, updates a fixed set of tracks when several measurements fall into the gates of several tracks and some of the measurements are clutter. It does not pick one assignment. It lists every joint event, an assignment in which each track takes at most one measurement in its gate and each measurement goes to at most one track, and it computes the probability of each event under a Gaussian measurement model and a Poisson clutter model. The probability $\beta_{ij}$ that measurement $j$ comes from track $i$ is the sum of the probabilities of the events that contain the pair. Each track is then updated with all its gated measurements at once, each weighted by $\beta_{ij}$, as in the probabilistic data association (PDA) filter for one target. Fortmann, Bar-Shalom and Scheffe published it in 1983. JPDA assumes that the number of targets is known. It does not start or delete tracks, which is the work of the track management around it.

## In plain words

Two dogs run close together in a park, and a camera sees three dark spots. One spot is surely the first dog, one is surely the second dog, and the middle spot could be either dog or a bush. Instead of betting on one story, JPDA writes down every story that makes sense: the middle spot is the first dog, or the second dog, or a bush, or one of the dogs was not seen at all. It scores each story by how well the spots fit where the dogs should be. Then each dog moves its estimate toward every spot it could own, more strongly toward the spots that the likely stories give it. If the stories disagree, the dog also becomes less sure of its position.

## The problem

The input of one frame is $n$ tracks, each with a predicted state $\hat x_i$, a covariance $\hat P_i$, a predicted measurement $\hat z_i$ and an innovation covariance $S_i$ from a [Kalman filter](/kalman-filter/), and $m$ measurements $z_1, \ldots, z_m$. The model is:

- each target is detected with probability $p_D$, and a detection falls in its gate with probability $p_G$;
- a detection of target $i$ is Gaussian with mean $\hat z_i$ and covariance $S_i$, so its likelihood is $L_{ij} = \mathcal N(z_j; \hat z_i, S_i)$;
- the clutter is a Poisson point process with constant density $\lambda$ per unit of measurement space, so the number of false measurements has a [Poisson distribution](/poisson-distribution/) and each is uniform;
- each measurement comes from at most one target, and each target gives at most one measurement.

A joint event $\theta$ is a set of pairs $(i, j)$ with $j$ in the gate of $i$, with no track and no measurement used twice. The output is the updated state and covariance of each track.

## The algorithm

```pseudo id=main
JPDA-STEP(the tracks, the measurements z_1..z_m, p_D, p_G, λ, the gate γ)
L1   for each track i: predict x̂_i, P̂_i, then ẑ_i, S_i and the gain K_i
L2   for each pair (i, j) with d²_ij ≤ γ: L_ij ← N(z_j; ẑ_i, S_i)
L3   for each joint event θ (each track at most one gated measurement, each measurement at most one track) do
L4       w(θ) ← Π_{(i,j) ∈ θ} p_D L_ij / λ  ×  Π_{i not in θ} (1 - p_D p_G)
L5   c ← Σ_θ w(θ);  β_ij ← Σ_{θ ∋ (i,j)} w(θ) / c;  β_i0 ← 1 - Σ_j β_ij
L6   for each track i: ν_ij ← z_j - ẑ_i;  ν_i ← Σ_j β_ij ν_ij;  x_i ← x̂_i + K_i ν_i
L7       P_i ← β_i0 P̂_i + (1 - β_i0)(P̂_i - K_i S_i K_iᵀ) + K_i (Σ_j β_ij ν_ij ν_ijᵀ - ν_i ν_iᵀ) K_iᵀ
```

The code enumerates the events of line L3 by depth-first search over the tracks: track $i$ is either missed, or takes one unused measurement in its gate. Line L7 has three parts. The first two are the covariance with no update and the covariance of a normal Kalman update, mixed by the probability that the track has a measurement. The third part is the spread of the innovations, which grows when the weights split between measurements that disagree.

## Example

**Three measurements, two tracks.** Track A gates $z_1$ and $z_2$, track B gates $z_2$ and $z_3$. The likelihoods are $L_{A1} = L_{B3} = 0.10$ and $L_{A2} = L_{B2} = 0.05$, with $p_D = 0.9$, $p_G = 1$ and $\lambda = 0.01$. A pair contributes $p_D L / \lambda$, which is 9 for a likelihood of 0.10 and 4.5 for 0.05, and a missed track contributes $1 - p_D = 0.1$. There are 8 joint events:

| Event | Weight |
|---|---|
| both missed | $0.1 \cdot 0.1 = 0.01$ |
| A-$z_1$, B missed | $9 \cdot 0.1 = 0.9$ |
| A-$z_2$, B missed | 0.45 |
| A missed, B-$z_2$ | 0.45 |
| A missed, B-$z_3$ | 0.9 |
| A-$z_1$, B-$z_2$ | $9 \cdot 4.5 = 40.5$ |
| A-$z_1$, B-$z_3$ | $9 \cdot 9 = 81$ |
| A-$z_2$, B-$z_3$ | 40.5 |

The sum is $c = 164.71$. For track A, $\beta_{A1} = (0.9 + 40.5 + 81) / 164.71 = 0.743$, $\beta_{A2} = (0.45 + 40.5) / 164.71 = 0.249$ and $\beta_{A0} = 1.36 / 164.71 = 0.008$. By symmetry B has the same numbers with $z_3$ in place of $z_1$. The single best event, A-$z_1$ and B-$z_3$, has probability only $81 / 164.71 = 0.49$. GNN would commit to it. JPDA lets the shared measurement $z_2$ pull both tracks a little.

**Two crossing targets.** In the code, two targets move with velocity $(1, \pm 0.3)$ and cross at frame 10. Each is detected with probability 0.9 and noise of standard deviation 0.5, and about one clutter point per frame falls in a $10 \times 10$ window around them. Over 25 frames the largest position error of the two tracks is 1.03 and the mean is 0.38. With the paths parallel and 2 units apart for 40 frames, the gap between the two estimates wanders between about 1 and 2.5, and in one of six runs it falls to 0.36 by the last frame. This is the coalescence described under Pitfalls.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows these facts.

- **Theorem: the event probabilities.** Under the model of the page, the posterior probability of a joint event given the measurements is $w(\theta) / c$.
- **Theorem: the update.** The marginal posterior of a track is a mixture of one Kalman update per gated measurement and the prediction, with the weights $\beta_{ij}$ and $\beta_{i0}$. Lines L6 and L7 give the exact mean and covariance of this mixture.
- **Theorem: one track is PDA.** For $n = 1$, $\beta_j = L_j / (b + \sum_k L_k)$ with $b = \lambda (1 - p_D p_G) / p_D$, the weights of the PDA filter.
- **Theorem: the normalizer is a permanent.** With $p_D = p_G = 1$ and $n = m$, $c = \operatorname{per}(L) / \lambda^n$. So computing $c$ exactly is #P-hard, and no polynomial algorithm is known for it.
- **Theorem: the number of events.** If every measurement is in every gate, there are $\sum_{k=0}^{\min(n,m)} \binom{n}{k} \binom{m}{k} k!$ joint events.

The approximation is that each track is kept as one Gaussian after the update, and that the tracks are treated as independent in the next frame. Neither is exact, and the tracking quality over many frames is not proved.

## Complexity

The likelihoods cost $O(n m p^2)$ after one inverse of $S_i$ per track, and the predictions and updates $O(n (p^3 + d^3))$. The enumeration visits each of the $E$ joint events once and adds its weight to at most $n$ sums, so it costs $O(E n)$. In the worst case, every measurement in every gate, $E$ is the count above. For $n = m = 3$ this is $1 + 9 + 18 + 6 = 34$, for $n = m = 6$ it is 13,327, and for $n = m = 10$ it is 234,662,231, so the time is exponential in the number of tracks in a cluster. Gating keeps clusters small in practice: tracks with no shared measurement are split into independent clusters, and each cluster is enumerated alone. The space is $O(n m)$ for the likelihoods and the sums, plus the covariances, and the depth-first search needs only $O(n + m)$ more.

## Properties

- **Soft decisions.** A track never takes a wrong measurement outright. A doubtful measurement gets a small weight.
- **Fixed number of targets.** JPDA itself does not create or delete tracks.
- **Exact marginals, approximate filter.** The $\beta_{ij}$ are exact under the model. The Gaussian kept after the update is an approximation of a mixture.
- **Exponential cost in the cluster size.** Close targets with shared measurements make the enumeration large.
- **Honest covariance.** The spread term makes the track less certain when the association is in doubt.

## Variants and improvements

- **PDA.** The case of one track, by Bar-Shalom and Tse (1975), with the closed form of the weights above.
- **Nonparametric JPDA.** If the clutter density is not known, replace $\lambda$ by the number of measurements in the gates divided by the gate volume.
- **Cheap JPDA and other approximations.** Approximate the $\beta_{ij}$ from the likelihoods directly, without enumeration, at a loss of accuracy.
- **k-best JPDA.** Sum only over the $k$ events of highest weight, found with Murty's method, as in [MHT](/multiple-hypothesis-tracking/).
- **Belief propagation.** Williams and Lau (2014) approximate the marginals by [loopy belief propagation](/loopy-belief-propagation/) on a graph of tracks and measurements, at a cost per iteration proportional to the number of gated pairs.
- **Coalescence avoidance.** JPDA* of Blom and Bloem (2000) prunes the events so that close tracks do not merge.
- **JIPDA.** Joint integrated PDA adds a probability that each target exists, so the filter can confirm and end tracks.
- **Random finite sets.** The [PHD filter](/phd-filter/) avoids the events altogether by tracking the density of targets.

## When to use it

Use JPDA when the number of targets is known or managed by other logic, the targets come close to each other for some frames, and the clutter is moderate. It is a standard method in radar and sonar tracking, and it is used in vision for people and cells when detections can be missed or false. If the targets are well apart, [GNN](/global-nearest-neighbor-association/) gives almost the same result at a lower cost. If the targets stay close for a long time and identity matters, [MHT](/multiple-hypothesis-tracking/) can defer the decision, while JPDA tends to merge the tracks.

## Pitfalls

- **Coalescence.** When two targets move close and parallel for many frames, the shared measurements pull both tracks toward the middle, and the tracks can merge onto one target.
- **Exponential enumeration.** A large cluster makes the number of events explode. Split clusters by gating, and fall back to an approximation when a cluster is too large.
- **Underflow.** Products of many small densities can underflow. Scale the likelihoods, or work with logarithms and subtract the largest before taking exponentials.
- **A wrong clutter density.** If $\lambda$ is too small, clutter gets a high weight. If it is too large, the tracks ignore their true measurements.
- **Measurements outside every gate.** They have no effect on JPDA, so new targets need a separate initiation rule.
- **A non-symmetric covariance.** Rounding in line L7 can break the symmetry of $P_i$. Symmetrize it after the update.

## Implementations

## History

Bar-Shalom and Tse introduced the probabilistic data association filter for one target in clutter in 1975. Fortmann, Bar-Shalom and Scheffe extended it to several targets in a conference paper in 1980 and in the IEEE Journal of Oceanic Engineering in 1983, with passive sonar as the application. The method became a standard part of the tracking books of Bar-Shalom and Fortmann (1988) and Blackman and Popoli (1999). The cost of the enumeration led to many approximations. Collins and Uhlmann (1992) studied efficient gating, which keeps the clusters small, and Williams and Lau (2014) noted that the exact marginals are closely related to the matrix permanent and are believed to be #P-complete, then gave a belief propagation method. In computer vision, JPDA was used for tracking people, cells and features in video.

## References
