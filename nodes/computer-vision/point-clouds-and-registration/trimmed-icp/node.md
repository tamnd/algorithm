---
tag: J43W5E
kind: algorithm
slug: trimmed-icp
name: Trimmed ICP
aliases:
- TrICP
area: computer-vision/point-clouds-and-registration
level: advanced
summary: "ICP for partly overlapping clouds: in each iteration only the fraction xi of pairs with the least distances enters the fit. The trimmed mean squared error never rises; the result is local."
solves: [point-cloud-registration]
model: real-ram
complexity:
  vars: {n: the number of source points, m: the number of target points, N: the number of iterations}
  time: {worst: Θ(N n m), average: Θ(N n m), best: Θ(n m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2002
  people: [Dmitry Chetverikov, Dmitry Svirko, Dmitry Stepanov, Pavel Krsek]
  note: "Presented at ICPR 2002. The journal paper of Chetverikov, Stepanov and Krsek (Image and Vision Computing, 2005) gives the proof of monotone convergence and the automatic choice of the overlap."
prereqs: [iterative-closest-point, least-trimmed-squares]
see_also: [quickselect, statistical-outlier-removal, ransac, m-estimator, generalized-icp, go-icp, icp-variants-taxonomy, point-cloud-registration]
sources:
  - paper: doi:10.1109/ICPR.2002.1047997
    title: "Dmitry Chetverikov, Dmitry Svirko, Dmitry Stepanov and Pavel Krsek, The Trimmed Iterative Closest Point algorithm, Proceedings of the 16th International Conference on Pattern Recognition (ICPR 2002), volume 3"
    locator: "The TrICP algorithm: the number of kept pairs N_po from the overlap, the trimmed sum of squares and the stop rules"
  - paper: doi:10.1016/j.imavis.2004.05.007
    title: "Dmitry Chetverikov, Dmitry Stepanov and Pavel Krsek, Robust Euclidean alignment of 3D point sets: the trimmed iterative closest point algorithm, Image and Vision Computing 23(3), 2005, 299-309"
    locator: "The algorithm, the proof that the trimmed mean squared error converges monotonically, the automatic choice of the overlap, and the tests with partial overlap and noise"
  - paper: doi:10.1080/01621459.1984.10477105
    title: "Peter J. Rousseeuw, Least median of squares regression, Journal of the American Statistical Association 79(388), 1984, 871-880"
    locator: "The least trimmed squares estimator, which sums only the smallest squared residuals"
  - paper: doi:10.1109/34.121791
    title: "Paul J. Besl and Neil D. McKay, A method for registration of 3-D shapes, IEEE Transactions on Pattern Analysis and Machine Intelligence 14(2), 1992, 239-256"
    locator: "The point-to-point ICP that TrICP trims, and its monotone convergence"
---

Trimmed ICP (TrICP) aligns a source [point cloud](/point-cloud/) $P$ of $n$ points to a target cloud $Q$ when only part of $P$ has a partner in $Q$. It is [iterative closest point](/iterative-closest-point/) with one change: after the closest-point match, it sorts the pairs by distance and keeps only the $N_{po} = \lfloor \xi n \rfloor$ pairs with the least squared distances, where $\xi \in (0, 1]$ is the overlap, the fraction of source points that have a partner. The fit step uses only the kept pairs. This is the idea of [least trimmed squares](/least-trimmed-squares/) applied to registration. The trimmed mean squared error never goes up, and for finite clouds the loop stops at a fixed point. With $\xi = 1$ it is plain ICP. Like ICP, it is local and needs a rough start.

## In plain words

Two scans of a room taken from different places see different parts of it. Each scan has points that the other scan never saw. Plain ICP still gives each of those points a nearest partner, which is wrong, and these wrong pairs drag the answer away.

Trimmed ICP says: I expect, say, 70 percent of my points to have a real partner. In every round it pairs each point with its nearest point, as before, but then it throws away the 30 percent of pairs with the longest gaps. It fits the turn and slide to the rest only.

The points without a partner usually have the longest gaps, so they are the ones that go. You must give the overlap, or let the method guess it.

## The problem

**Input.** A source cloud $P = (p_1, \ldots, p_n)$ and a target cloud $Q = \{q_1, \ldots, q_m\}$ in $\mathbb{R}^3$, the overlap $\xi \in (0, 1]$, a start pose $(R_0, t_0)$, and stop parameters eps and tol.

**Output.** A pose $(R, t)$ with $R \in SO(3)$ at a fixed point of the iteration. The cost is the trimmed mean squared error

$$e(R, t) = \frac{1}{N_{po}} \sum_{k=1}^{N_{po}} d_{(k)}^2, \qquad d_i = \min_j |R p_i + t - q_j|,$$

where $d_{(1)} \le d_{(2)} \le \cdots$ are the distances in increasing order, and $N_{po} = \max(3, \lfloor \xi n \rfloor)$ in the reference code (three pairs are the least that fix a rotation in general position).

## The algorithm

```pseudo id=main
TRIMMED-ICP(P, Q, ξ, R0, t0, eps, tol)
L1  R ← R0 ;  t ← t0 ;  N_po ← max(3, ⌊ξ n⌋) ;  e_prev ← ∞
L2  repeat (up to an iteration cap)
L3      c(i) ← index of the closest q_j to R p_i + t ;  d_i² ← |R p_i + t - q_c(i)|²
L4      S ← the N_po indices i with the least d_i²
L5      e ← (1/N_po) Σ_{i ∈ S} d_i²
L6      if e ≤ eps or e_prev - e ≤ tol then return R, t
L7      (R, t) ← KABSCH((p_i), (q_c(i))) over i ∈ S       ▷ with the sign fix
L8      e_prev ← e
L9  return R, t
```

Line L3 is the closest-point step of ICP; the code uses brute force. Line L4 is the trimming. The code sorts the $n$ distances; a selection algorithm such as [quickselect](/quickselect/) finds the $N_{po}$ least ones in $O(n)$ expected time. Line L5 is the trimmed MSE of the current pose. Line L6 stops when the error is small enough, or when it no longer falls by more than tol. Line L7 is the [Kabsch](/kabsch-algorithm/) fit with $R = V \operatorname{diag}(1, 1, d)\, U^{\mathsf T}$, applied to the kept pairs only.

## Example

The test scene has 40 shared points drawn in $[-1, 1]^3$ (seed 1). The target $Q$ holds these points moved by a rotation of 12 degrees about $(1, -1, 2)$ and the translation $(0.1, 0.05, -0.08)$, plus 10 points in $[-2.5, -1.5]^3$ that the source does not see. The source $P$ holds the 40 shared points in their original place, plus 14 points in the slab $1.2 \le x \le 1.8$ that the target does not see. So $n = 54$, $m = 50$, and the true overlap is $40/54 \approx 0.741$. The start is the identity, with eps $= 0$ and tol $= 0$.

With $\xi = 40/54$, so $N_{po} = 40$:

| iteration | after line L5 | after line L7 (kept pairs) |
|---|---|---|
| 1 | 0.0412 | 0.0105 |
| 2 | 0.00226 | 4.7e-32 |
| 3 | 4.7e-32 | 4.7e-32 |
| 4 | 4.7e-32, stop | |

The pose is exact up to rounding. The values never go up, as the proof says. The other values of $\xi$ give:

| $\xi$ | $N_{po}$ | final trimmed MSE | rotation error | translation error |
|---|---|---|---|---|
| 0.6 | 32 | about 2e-31 | 0 | 0 |
| 40/54 | 40 | 4.7e-32 | 0 | 0 |
| 0.85 | 45 | 0.0425 | 2.94 degrees | (-0.063, -0.013, -0.020) |
| 1 (plain ICP) | 54 | 0.145 | 8.77 degrees | (-0.185, -0.073, -0.017) |

A $\xi$ below the true overlap still finds the exact pose here, because the kept pairs are all true pairs. A $\xi$ above it forces some of the 14 unseen points into the fit and biases the result. Plain ICP keeps all of them and is the worst.

## Correctness

Claim: with eps $= 0$ and tol $= 0$, TrICP stops after finitely many iterations, the trimmed MSE never rises, the rotation is proper, and the returned pose is a least squares fit to a set of $N_{po}$ pairs that are closest-point pairs with the least distances at that pose. The key inequality is $e_k \ge F_k(R_{k+1}, t_{k+1}) \ge e_{k+1}$. Line L7 minimizes the cost $F_k$ of the kept pairs, so it is no worse than the old pose. Then line L3 can only shorten each distance, and line L4 picks the $N_{po}$ shortest, whose sum is at most the sum over the old kept set. The full proof is in [proofs/correctness.md](proofs/correctness.md). Chetverikov, Stepanov and Krsek (2005) prove the monotone convergence of TrICP.

## Complexity

The model is the [real RAM](/real-ram/). Per iteration, line L3 costs $\Theta(n m)$ by brute force, or about $n \log m$ with a [k-d tree](/kd-tree/) on typical 3D data (an expected cost, not a worst case). Line L4 costs $\Theta(n \log n)$ by sorting, or $O(n)$ expected with quickselect. Lines L5 and L7 cost $\Theta(n)$. So an iteration costs $\Theta(n m)$, and $N$ iterations cost $\Theta(N n m)$. The best case is two passes, $\Theta(n m)$. The extra space is $\Theta(n)$.

The number of iterations $N$ is finite by the proof, but the bound there is a crude count of match and trim sets. Measured counts are benchmark results.

## Properties

- **Monotone.** The trimmed MSE never rises.
- **Local.** As for ICP, the result depends on the start pose.
- **Needs the overlap.** The user gives $\xi$, or an outer search chooses it.
- **Contains ICP.** With $\xi = 1$ every pair is kept, and TrICP is point-to-point ICP.
- **Breakdown.** Up to a fraction $1 - \xi$ of source points without a partner can be ignored, if they have the longest distances. This is not guaranteed: an unseen point can lie close to some target point by chance.

## Variants and improvements

- **Automatic overlap.** Chetverikov, Stepanov and Krsek (2005) run TrICP for a range of $\xi$ and choose the value that minimizes an objective that divides the trimmed MSE by a power of $\xi$, so that a larger overlap is preferred when the error allows it. The form $e(\xi)/\xi^{1 + \lambda}$ with $\lambda = 2$ comes from slides of the authors; we did not confirm it in the paper. A one-dimensional search, such as [golden section search](/golden-section-search/), can run this outer loop; it assumes that the objective has one minimum in the range of $\xi$, which is not proved.
- **Distance threshold.** Many ICP codes drop pairs farther than a fixed distance instead. This needs a threshold in distance units instead of a fraction.
- **Robust weights.** Weights from an [M-estimator](/m-estimator/) reduce the effect of far pairs smoothly instead of cutting them.
- **Other error metrics.** The same trimming works with the point-to-plane error of [point-to-plane ICP](/point-to-plane-icp/) and in [generalized ICP](/generalized-icp/).
- **Global search.** [Go-ICP](/go-icp/) uses trimming inside its branch and bound search to handle outliers.

## When to use it

Use TrICP when the two clouds overlap only in part and a rough pose is known: scans of a scene from different places, a model against a scan that sees one side of it, or a cloud with clutter. If the overlap is roughly known, give it. If not, run the automatic choice or try a few values and compare the fit. Prefer a $\xi$ a little below the true overlap: in the example, a too small $\xi$ still worked, and a too large one did not. For heavy outlier rates with no rough pose, use a robust global method such as [RANSAC](/ransac/) on feature matches or [TEASER](/teaser-registration/) first.

## Pitfalls

- **The trimmed sum without the trimmed fit.** Computing $e$ over the kept set in line L5 and then fitting all $n$ pairs in line L7 loses the robustness and the proof of monotone decrease. Fit only the pairs in $S$.
- **Dividing by $n$ in line L5.** The MSE must be divided by $N_{po}$. Dividing by $n$ does not change the pose, but it makes errors for different $\xi$ incomparable, which breaks the automatic choice of the overlap.
- **A $\xi$ that is too large in line L1.** Pairs without a true partner enter the fit and bias it, as in the row $\xi = 0.85$ of the example.
- **A $\xi$ that is too small in line L1.** Fewer pairs make the fit noisier, and with very few pairs the kept points may lie on one patch and leave a slide free.
- **No floor on $N_{po}$.** With $\lfloor \xi n \rfloor < 3$ the fit in line L7 is not defined in general. Keep at least three pairs.

## Implementations

## History

Chetverikov, Svirko, Stepanov and Krsek presented the Trimmed ICP at ICPR in 2002. The method uses the least trimmed squares idea of Rousseeuw (1984) inside the ICP loop of Besl and McKay (1992). In 2005 Chetverikov, Stepanov and Krsek published the journal version in Image and Vision Computing, with the proof of monotone convergence, an automatic choice of the overlap, and tests on partly overlapping 3D scans.

## References
