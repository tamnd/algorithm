---
tag: 9HR0MT
kind: algorithm
slug: phd-filter
name: Probability hypothesis density filter
aliases:
- PHD filter
- GM-PHD filter
area: computer-vision/visual-tracking
level: research
summary: "Propagate the first moment of the random finite set of targets, not each track. With linear Gaussian models, constant p_D and p_S and Gaussian mixture birth, the Gaussian mixture form is closed."
solves: [multi-object-tracking]
model: real-ram
complexity:
  vars: {J: the number of components after the prediction and the birth, m: the number of measurements, d: the dimension of a state, p: the dimension of a measurement with p ≤ d}
  time: {worst: O(J² (m + 1)² d² + J (m + 1) d³ + J p³), average: O(J² (m + 1)² d² + J (m + 1) d³ + J p³), best: O(J (m + 1) (d³ + log(J (m + 1))) + J p³)}
  space: {extra: O(J (m + 1) d²)}
properties: {deterministic: true, exact: false, local: false, iterative: false, online: true}
history:
  year: 2003
  people: [Ronald P. S. Mahler]
  note: Mahler derived the PHD filter from finite set statistics in 2003. Vo, Singh and Doucet gave a particle form in 2005, and Vo and Ma gave the closed Gaussian mixture form in 2006.
prereqs: [kalman-filter, gaussian-mixture-model, poisson-distribution, multi-object-tracking]
see_also: [joint-probabilistic-data-association, multiple-hypothesis-tracking, global-nearest-neighbor-association, data-association, track-gating, sequential-monte-carlo, particle-filter, bayes-filter]
sources:
  - paper: doi:10.1109/TAES.2003.1261119
    title: Ronald P. S. Mahler, Multitarget Bayes filtering via first-order multitarget moments, IEEE Transactions on Aerospace and Electronic Systems 39(4), 2003, 1152 to 1178
    locator: the whole paper (the PHD as the first moment of a random finite set, and the prediction and update equations of the PHD filter)
  - paper: doi:10.1109/TSP.2006.881190
    title: Ba-Ngu Vo and Wing-Kin Ma, The Gaussian mixture probability hypothesis density filter, IEEE Transactions on Signal Processing 54(11), 2006, 4091 to 4104
    locator: the whole paper (the closed form Gaussian mixture recursion and its assumptions, the pruning, merging and state extraction steps, and the extension to nonlinear models)
  - paper: doi:10.1109/TAES.2005.1561884
    title: Ba-Ngu Vo, Sumeetpal Singh and Arnaud Doucet, Sequential Monte Carlo methods for multitarget filtering with random finite sets, IEEE Transactions on Aerospace and Electronic Systems 41(4), 2005, 1224 to 1245
    locator: the whole paper (the particle form of the PHD filter)
  - paper: doi:10.1109/TAES.2007.4441756
    title: Ronald Mahler, PHD filters of higher order in target number, IEEE Transactions on Aerospace and Electronic Systems 43(4), 2007, 1523 to 1543
    locator: the whole paper (the cardinalized PHD filter)
  - book: isbn:9781596930926
    title: Ronald P. S. Mahler, Statistical Multisource-Multitarget Information Fusion, Artech House, 2007
    locator: the chapters on random finite sets and on the PHD and CPHD filters
---

The probability hypothesis density filter, or PHD filter, tracks an unknown and changing number of targets in clutter without assigning measurements to tracks. It treats the set of all targets as one random object, a random finite set, and it does not propagate the full distribution of that set, which is too large to handle. It propagates only its first moment, the PHD $D(x)$, a density on the state space of one target. The integral of $D$ over a region is the expected number of targets in that region. Ronald Mahler derived the prediction and update equations of the PHD in 2003. In general they have no closed form. Vo and Ma showed in 2006 that if the motion and measurement models are linear and Gaussian, the probabilities of detection $p_D$ and survival $p_S$ are constant, and the birth intensity is a Gaussian mixture, then a PHD that is a Gaussian mixture stays a Gaussian mixture. This Gaussian mixture PHD filter, or GM-PHD, is the form on this page. It runs one [Kalman filter](/kalman-filter/) update per component and measurement, and it keeps the number of components small by pruning and merging.

## In plain words

Picture a map of a harbor covered with sand. Where boats are likely to be, the sand is piled high, and the total amount of sand is the number of boats you expect. Each time step, every pile slides along with the current and loses a little sand for boats that may leave. New small piles appear where boats usually enter. Then the radar gives a set of blips. Each pile keeps some of its sand in case its boat was not seen. For each blip, sand is copied to the spot near that blip, in proportion to how well each pile explains it. A blip that no pile explains well is taken as noise and adds little sand. Small piles are swept away, and piles that sit on top of each other are joined. Wherever about one boat's worth of sand is gathered, you report a boat.

## The problem

The state of the scene at time $k$ is a finite set $X_k$ of target states in $\mathbb R^d$, and the measurements form a finite set $Z_k$ in $\mathbb R^p$. The model is:

- a target with state $x'$ survives with probability $p_S$ and moves to $x$ with density $\mathcal N(x; F x', Q)$;
- new targets appear as a Poisson point process with intensity $\gamma(x) = \sum_b w_b \, \mathcal N(x; m_b, P_b)$;
- a target with state $x$ is detected with probability $p_D$, and its measurement has density $\mathcal N(z; H x, R)$;
- the clutter is a Poisson point process with intensity $\kappa(z)$, independent of the targets.

The PHD of $X_k$ given $Z_1, \ldots, Z_k$ is the density $D_k$ with $\int_A D_k(x) \, dx = E\,|X_k \cap A|$ for every region $A$. The PHD filter computes $D_k$ from $D_{k-1}$ and $Z_k$ by Mahler's equations, with spawning left out:

$$D_{k|k-1}(x) = \int p_S \, \mathcal N(x; F x', Q) \, D_{k-1}(x') \, dx' + \gamma(x),$$

$$D_k(x) = (1 - p_D) D_{k|k-1}(x) + \sum_{z \in Z_k} \frac{p_D \, \mathcal N(z; H x, R) \, D_{k|k-1}(x)}{\kappa(z) + \int p_D \, \mathcal N(z; H y, R) \, D_{k|k-1}(y) \, dy}.$$

The update is exact when the predicted set of targets is a Poisson point process. In general it is an approximation. The output in each frame is the expected number of targets $\hat N_k = \int D_k$ and a set of state estimates.

## The algorithm

The PHD is kept as a mixture $\sum_k w_k \, \mathcal N(x; m_k, P_k)$.

```pseudo id=main
GM-PHD-STEP(the components (w_k, m_k, P_k), the measurements Z, F, Q, H, R, p_S, p_D, κ, the birth components)
L1   for each component: w_k ← p_S w_k;  m_k ← F m_k;  P_k ← F P_k Fᵀ + Q
L2   append the birth components (w_b, m_b, P_b)
L3   for each component k: η_k ← H m_k;  S_k ← H P_k Hᵀ + R;  K_k ← P_k Hᵀ S_k⁻¹;  P⁺_k ← (I - K_k H) P_k
L4   the missed terms: keep each component with the weight (1 - p_D) w_k
L5   for each z in Z: q_k ← N(z; η_k, S_k);  add (p_D w_k q_k / (κ(z) + Σ_l p_D w_l q_l), m_k + K_k (z - η_k), P⁺_k) for each k
L6   drop the components with w_k < T;  merge each heaviest component with those within distance U;  keep the J_max heaviest
L7   N̂ ← Σ_k w_k;  report m_k round(w_k) times for each component with w_k > 0.5
```

Line L6 follows Vo and Ma. Take the component $j$ of largest weight, and collect the components $i$ with $(m_i - m_j)^\mathsf{T} P_i^{-1} (m_i - m_j) \le U$. Replace them by one component with the sum of their weights, their weighted mean, and the covariance that keeps the second moment. Repeat with the rest. The code uses $T = 10^{-5}$, $U = 4$ and $J_{\max} = 100$.

## Example

**One update in one dimension.** Two predicted components have weight 1, means 0 and 10, and variance 0.75, so with $R = 0.25$ each has $S = 1$ and $K = 0.75$. Let $p_D = 0.9$ and $\kappa = 0.01$, and let the measurements be $0.5$, $9$ and $4$.

| Term | Weight | Mean |
|---|---|---|
| missed, component at 0 | $0.1$ | 0 |
| missed, component at 10 | $0.1$ | 10 |
| $z = 0.5$ | $0.9 \cdot 0.352 / (0.01 + 0.317) = 0.969$ | 0.375 |
| $z = 9$ | $0.9 \cdot 0.242 / (0.01 + 0.218) = 0.956$ | 9.25 |
| $z = 4$ | $1.2 \cdot 10^{-4} / (0.01 + 1.2 \cdot 10^{-4}) = 0.012$ | 3.0 |

The other three terms, each measurement paired with the far component, have weights below $10^{-15}$. The total weight is $\hat N = 2.137$, the expected number of targets. The measurement at 4 fits neither component, and the clutter term $\kappa$ takes almost all of its share, so it adds only 0.012 targets. After pruning and merging there are three components, with weights 1.069, 1.056 and 0.012 and means 0.34, 9.32 and 3.0, and the filter reports two targets, at 0.34 and 9.32.

**A scene in the plane.** In the test, three targets with constant velocity are born at frames 0, 0 and 8 near three birth components of weight 0.05, and one of them dies at frame 25. Each is detected with probability 0.95 and noise of standard deviation 0.5, and on average 5 clutter points per frame fall in a $60 \times 60$ window. Over 40 frames, leaving out the three frames after each birth or death, the filter reports the right number of targets, each within 1.5 of a true one, in 28 of 31 frames. Most of the errors come from a missed detection, after which the weight of the target falls to about $1 - p_D$ for one frame.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows these facts.

- **Theorem: the mixture is closed.** If $D_{k-1}$ is a Gaussian mixture, lines L1 and L2 give exactly the predicted PHD $D_{k|k-1}$, and lines L3 to L5 give exactly the updated PHD $D_k$ of the equations above.
- **Theorem: the expected number.** The weights after line L5 sum to $(1 - p_D) \hat N_{k|k-1} + \sum_{z \in Z} \rho(z)$, where $\hat N_{k|k-1} = p_S \hat N_{k-1} + \sum_b w_b$ and $\rho(z) = \sum_l p_D w_l q_l / (\kappa(z) + \sum_l p_D w_l q_l)$ lies in $[0, 1)$. So each measurement adds less than one expected target, and with no measurements the count is $(1 - p_D)(p_S \hat N_{k-1} + \sum_b w_b)$.
- **Theorem: merging keeps the moments.** A merge in line L6 keeps the total weight, the weighted mean and the weighted second moment of the components it joins.

Pruning and merging change the density, so the filter as a whole is an approximation of the PHD recursion, and the PHD recursion is itself an approximation of the full multi-target Bayes filter. The quality of the state estimates is not proved.

## Complexity

After the prediction there are $J$ components. Line L3 costs $O(J (d^3 + p^3))$, and line L5 costs $O(J m (p^2 + d p))$ for the likelihoods and the new means, and makes $J (m + 1)$ components. Merging needs the inverse of each covariance, $O(J (m + 1) d^3)$, and each round scans the remaining components at $O(d^2)$ each. In the worst case each round removes one component, so merging costs $O(J^2 (m + 1)^2 d^2)$. In the best case one round removes all, and the sort for the cap $J_{\max}$ costs $O(J (m + 1) \log(J (m + 1)))$. The space is $O(J (m + 1) d^2)$ for the covariances. The cost is polynomial in the number of targets and measurements, and there is no enumeration of assignments. The cap $J_{\max}$ keeps $J$ bounded from frame to frame.

## Properties

- **No explicit association.** Every measurement updates every component, and the weights do the work that assignments do in other trackers.
- **Varying number of targets.** Births, deaths, misses and clutter are all in the model, so tracks start and end without extra logic.
- **No identities.** The PHD is a density, not a set of labeled tracks. The estimates of two frames are not linked.
- **Closed form only under the stated model.** Linear Gaussian models, constant $p_D$ and $p_S$, and a Gaussian mixture birth intensity.
- **Polynomial cost.** The work is about $J m$ Kalman updates per frame.
- **Noisy count.** The expected number $\hat N$ has a high variance when the number of targets is large, and a single miss drops the weight of a target to about $1 - p_D$.

## Variants and improvements

- **Particle PHD.** Vo, Singh and Doucet (2005) represent the PHD by weighted particles, as in [sequential Monte Carlo](/sequential-monte-carlo/), for nonlinear and non-Gaussian models. The estimates then need clustering of the particles.
- **Nonlinear Gaussian models.** Vo and Ma (2006) replace the Kalman update of each component by an [extended](/extended-kalman-filter/) or [unscented](/unscented-kalman-filter/) Kalman update. The result is no longer exact.
- **Spawning.** Targets that split off from other targets add a further linear Gaussian term to the prediction, and the mixture stays closed.
- **Cardinalized PHD.** The CPHD filter of Mahler (2007) propagates the full distribution of the number of targets with the PHD. Its count is much more stable, at a cost cubic in the number of measurements.
- **Labeled filters.** Filters built on labeled random finite sets give each target an identity, so the output is a set of tracks.
- **Track labels as a post step.** A simple fix is to tag each component and pass the tag to the components it creates, then read the tags of the extracted estimates.

## When to use it

Use the GM-PHD filter when many targets appear and disappear, the clutter is heavy, and an estimate of the number of targets and their positions in each frame is the main output. It was designed for radar and sonar, and in vision it is used for people, vehicles and cells seen by a detector. When the motion is nonlinear, use the extended or unscented form, or the particle form. If each target must keep one identity over the whole video, add labels or use a tracker that keeps identities, such as [MHT](/multiple-hypothesis-tracking/). If the number of targets is known and small, [JPDA](/joint-probabilistic-data-association/) or [GNN](/global-nearest-neighbor-association/) is simpler.

## Pitfalls

- **A model outside the closed form.** A detection probability that depends on the state, or nonlinear models, break the exact recursion. The usual approximations work but are no longer exact.
- **A birth model that misses the entry points.** The filter can only start a target where the birth intensity has weight. A birth weight that is too large makes clutter turn into targets.
- **Missed detections.** One miss multiplies the weight of a target by $1 - p_D$. With $p_D = 0.95$ the target falls below the threshold of 0.5 for that frame.
- **Close targets.** Two targets closer than the merge distance $U$ become one component, of weight about 2. The extraction reports the same mean twice.
- **A wrong clutter intensity.** If $\kappa$ is too small, clutter adds targets. If it is too large, true measurements are discounted.
- **Pruning too hard.** A large threshold $T$ removes the weak components that a target needs to recover after a miss.
- **Loss of symmetry.** Rounding in $P^+_k$ can make it non-symmetric. The code symmetrizes it after the update.

## Implementations

## History

Mahler developed finite set statistics in the 1990s as a way to treat multi-target tracking as Bayesian filtering of a random finite set. The full multi-target Bayes filter needs integrals over sets of every size, which cannot be computed for more than a few targets. In 2003 Mahler proposed to propagate only the first moment, the PHD, and derived its prediction and update equations, by analogy with the use of the mean in place of the full density. Vo, Singh and Doucet gave the first general implementation by sequential Monte Carlo in 2005. Vo and Ma found the closed Gaussian mixture form in 2006, together with the pruning, merging and extraction steps used on this page. In 2007 Mahler introduced the cardinalized PHD filter to fix the unstable count of the PHD filter and collected the theory in a book. Later filters on labeled random finite sets gave the targets identities.

## References
