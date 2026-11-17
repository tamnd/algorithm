---
tag: E0TQ57
kind: algorithm
slug: teaser-registration
name: TEASER
aliases:
- truncated least squares estimation and semidefinite relaxation
area: computer-vision/point-clouds-and-registration
level: research
summary: "Registration from putative matches with most of them wrong: it solves scale, rotation and translation in turn under a truncated least squares cost, with exact voting, a maximum clique and an SDP."
solves: [point-cloud-registration]
model: real-ram
complexity:
  vars: {m: the number of correspondences, N: the number of GNC iterations}
  time: {worst: O(3^(m/3) + N m^2), average: O(3^(m/3) + N m^2), best: Θ(m^2)}
  space: {extra: Θ(m^2)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2021
  people: [Heng Yang, Jingnan Shi, Luca Carlone]
  note: "Yang and Carlone gave a first form of the method in 2019. Yang, Shi and Carlone published TEASER and the faster TEASER++ in IEEE Transactions on Robotics in 2021."
prereqs: [point-cloud-registration, wahba-problem]
see_also: [go-icp, fast-global-registration, ransac, maximum-clique, semidefinite-programming, robust-model-fitting, point-feature-histograms, four-points-congruent-sets]
sources:
  - paper: doi:10.1109/TRO.2020.3033695
    title: "Heng Yang, Jingnan Shi and Luca Carlone, TEASER: Fast and certifiable point cloud registration, IEEE Transactions on Robotics 37(2), 2021, 314-333"
    locator: "The truncated least squares cost, the translation and rotation invariant measurements, adaptive voting and its exactness (Theorem 7), the inlier clique (Theorem 6), the semidefinite relaxation of the rotation (Proposition 12) with its tightness results, the optimality certifier (Theorem 14), and the error bounds (Theorem 17)"
  - paper: arxiv:1909.08605
    title: "Heng Yang, Pasquale Antonante, Vasileios Tzoumas and Luca Carlone, Graduated non-convexity for robust spatial perception: From non-minimal solvers to global outlier rejection, IEEE Robotics and Automation Letters, 2020"
    locator: "Graduated non-convexity for the truncated least squares cost: the weight update and the schedule of the control parameter, used by TEASER++ for the rotation"
  - paper: doi:10.1109/34.88573
    title: "Shinji Umeyama, Least-squares estimation of transformation parameters between two point patterns, IEEE Transactions on Pattern Analysis and Machine Intelligence 13(4), 1991, 376-380"
    locator: "The best rotation for weighted point pairs by the SVD, with the sign of the determinant, used in each GNC step"
---

TEASER registers two [point clouds](/point-cloud/) from a list of putative correspondences, such as the matches of [feature descriptors](/point-feature-histograms/), when most of the matches are wrong. It needs no start pose. It uses the truncated least squares (TLS) cost, which counts each match by its squared error up to a cap, so an outlier costs a fixed amount however far away it is. The method splits the problem into three smaller ones. Differences of pairs of matches do not depend on the translation, and their lengths do not depend on the rotation either. TEASER first estimates the scale from the ratios of lengths by adaptive voting, an exact solver for one-dimensional TLS. It then keeps only the matches in a [maximum clique](/maximum-clique/) of a graph of pairs that agree with this scale. It solves the rotation from the surviving differences by a [semidefinite](/semidefinite-programming/) relaxation, and it can check a certificate that the rotation is the global TLS optimum. Last, it finds the translation by adaptive voting on each axis. TEASER++ replaces the relaxation with graduated non-convexity (GNC), which is faster but has no guarantee, and checks the result afterwards.

## In plain words

You have a list of guessed matches between two scans, and most guesses are wrong. Take any two matches. If both are right, the distance between the two points in the first scan, times the scale, is about the same as the distance between their partners in the second scan, however the scan is turned or moved.

So first find the scale that the most pairs agree on. Then draw a line between every two matches that agree with this scale. Right matches all agree with each other, so they form a group in which everyone is joined to everyone. Find the largest such group and throw away the rest.

Now most of the wrong matches are gone. Find the turn that best fits the matches that are left, while still letting a few bad ones count only a fixed amount. Then find the shift.

## The problem

**Input.** Points $a_1, \ldots, a_m$ and $b_1, \ldots, b_m$ in $\mathbb{R}^3$, where $(a_i, b_i)$ is a putative correspondence; a noise bound $\beta > 0$; and a cap $\bar c > 0$, usually 1. The model is

$$b_i = s R a_i + t + o_i + \epsilon_i, \qquad |\epsilon_i| \le \beta ,$$

with a scale $s > 0$, a rotation $R \in SO(3)$ and a translation $t$. The match $i$ is an inlier when $o_i = 0$; for an outlier, $o_i$ is arbitrary.

**Output.** An estimate $(\hat s, \hat R, \hat t)$ that minimizes the TLS cost

$$\sum_{i=1}^{m} \min\left(\frac{|b_i - s R a_i - t|^2}{\beta^2}, \bar c^2\right).$$

TEASER does not minimize this cost jointly. It minimizes a TLS cost for each of the three unknowns in turn, on the invariant measurements below. The scale can also be known, which is the usual case for two scans of the same scene. This is a form of [point cloud registration](/point-cloud-registration/) and of [robust model fitting](/robust-model-fitting/).

## The algorithm

For a pair $i < j$, the translation invariant measurement (TIM) is $\bar a_{ij} = a_j - a_i$ and $\bar b_{ij} = b_j - b_i$. For two inliers, $\bar b_{ij} = s R \bar a_{ij} + \epsilon_j - \epsilon_i$, so the translation is gone and the noise bound is $2\beta$. The translation and rotation invariant measurement (TRIM) is the ratio $s_{ij} = |\bar b_{ij}| / |\bar a_{ij}|$; for two inliers it lies within $\alpha_{ij} = 2\beta / |\bar a_{ij}|$ of $s$.

Adaptive voting solves the scalar problem: minimize $\sum_k \min((x - v_k)^2 / b_k^2, \bar c^2)$ over $x$. Each value $v_k$ is an inlier of $x$ on the interval $[v_k - \bar c b_k, v_k + \bar c b_k]$. Sort the $2K$ interval ends. Between two consecutive ends the set of inliers is fixed, and the best $x$ for a fixed set is its weighted mean, with weights $1 / b_k^2$. Adaptive voting computes the cost of every such piece and returns the best one.

```pseudo id=main
TEASER(A, B, β, c̄)            ▷ pairs (a_i, b_i), i = 1 .. m, noise bound β
L1  for each pair i < j:  ā_ij ← a_j - a_i ;  b̄_ij ← b_j - b_i
L2      s_ij ← |b̄_ij| / |ā_ij| ;  α_ij ← 2β / |ā_ij|
L3  ŝ ← ADAPTIVE-VOTING({s_ij}, {α_ij}, c̄)      ▷ or the known scale
L4  E ← {(i, j) : |s_ij - ŝ| ≤ c̄ α_ij}
L5  C ← MAX-CLIQUE({1 .. m}, E)
L6  R̂ ← TLS rotation from the TIMs (ŝ ā_ij, b̄_ij) with i, j in C, bound 2β
L7  for each axis d:  t̂_d ← ADAPTIVE-VOTING({(b_i - ŝ R̂ a_i)_d : i in C}, β, c̄)
L8  return ŝ, R̂, t̂
```

Lines L1 and L2 form all $m(m-1)/2$ TIMs and TRIMs. Line L3 estimates the scale by adaptive voting over the TRIMs. Line L4 builds the consistency graph: a pair is an edge when its ratio agrees with the scale. Line L5 keeps a [maximum clique](/maximum-clique/) of this graph; the reference code uses [Bron-Kerbosch](/bron-kerbosch/) with a pivot and a size bound. Line L6 solves the rotation. TEASER writes the rotation TLS problem with binary variables and a unit quaternion, relaxes it to a semidefinite program, and reads the rotation from the solution; a dual certificate then shows whether the relaxation was tight, which means the rotation is the global TLS optimum. TEASER++ and the reference code use GNC instead: they replace the TLS cost by a smooth surrogate controlled by a value $\mu$, solve a weighted [Wahba problem](/wahba-problem/) by the [SVD](/singular-value-decomposition/), update the weights from the residuals, and make the surrogate closer to TLS by $\mu \leftarrow 1.4 \mu$ until the weights are all 0 or 1. Line L7 solves the translation one coordinate at a time by adaptive voting.

## Example

First, adaptive voting alone. Take the values 1.0, 1.1, 0.9, 3.0 and 5.0, all with the bound 0.2, and $\bar c = 1$. The intervals are $[0.8, 1.2]$, $[0.9, 1.3]$, $[0.7, 1.1]$, $[2.8, 3.2]$ and $[4.8, 5.2]$. The sorted ends give 7 pieces with a nonempty inlier set, below the limit $2K - 1 = 9$.

| piece | inliers | weighted mean | cost |
|---|---|---|---|
| (0.7, 0.8) | 0.9 | 0.9 | 4 |
| (0.8, 0.9) | 1.0, 0.9 | 0.95 | 3.125 |
| (0.9, 1.1) | 1.0, 1.1, 0.9 | 1.0 | 2.5 |
| (1.1, 1.2) | 1.0, 1.1 | 1.05 | 3.125 |
| (1.2, 1.3) | 1.1 | 1.1 | 4 |
| (2.8, 3.2) | 3.0 | 3.0 | 4 |
| (4.8, 5.2) | 5.0 | 5.0 | 4 |

The best piece gives $x = 1.0$ with cost 2.5: three values fit, and the two others each pay the cap 1. The plain mean of the five values is 2.2, which no value supports.

Second, the whole method with the scale known. Random points in the cube $[-1, 1]^3$ are turned by a random rotation, moved, and given Gaussian noise with standard deviation 0.005; then most of the matches are replaced by random points. The noise bound is $\beta = 0.03$.

| $m$ | outliers | TIMs | edges kept | inlier edges kept | clique | rotation error | translation error |
|---|---|---|---|---|---|---|---|
| 20 | 12 | 190 | 30 | 28 of 28 | 8, all inliers | 0.26° | 0.0016 |
| 60 | 51 | 1770 | 72 | 36 of 36 | 9, all inliers | 0.19° | 0.0011 |
| 100 | 90 | 4950 | 168 | 45 of 45 | 10, all inliers | 0.31° | 0.0035 |

With 90% outliers, the pruning keeps under 4% of the pairs, every inlier pair survives as the proof promises, and the maximum clique is exactly the set of inliers. The rotation and translation from the clique are then within the noise.

## Correctness

Two steps are exact. First, adaptive voting returns a global minimizer of the scalar TLS cost. A minimizer $x^\star$ exists and has cost below $K \bar c^2$, so it lies inside some interval. Just to the left of $x^\star$ there is a piece whose inlier set $S$ gives exactly the cost of $x^\star$. The weighted mean of $S$ is at least as good for the quadratic cost of $S$, and the TLS cost is never above that quadratic cost. So the best piece is as good as $x^\star$. Second, every pair of inliers passes the test of line L4 when the scale is right: $\big| |\bar b_{ij}| - s |\bar a_{ij}| \big| \le |\bar b_{ij} - s R \bar a_{ij}| \le 2\beta$. So the inliers form a clique, and the maximum clique is at least as large. The full proof is in [proofs/correctness.md](proofs/correctness.md).

The other steps have weaker claims. The maximum clique can still hold outliers. The semidefinite relaxation is not always tight; when it is, the certificate proves global optimality of the rotation, and the paper gives conditions under which it is tight. GNC has no guarantee. The paper also bounds the error of the estimate in terms of $\beta$, under conditions on the inliers.

## Complexity

The model is the [real RAM](/real-ram/). Lines L1 and L2 take $\Theta(m^2)$ time. Adaptive voting on $K$ values sorts $2K$ ends and sweeps them with running sums, $O(K \log K)$; on the TRIMs this is $O(m^2 \log m)$, and with a known scale line L3 costs nothing. Line L4 takes $\Theta(m^2)$. Line L5 solves an [NP-hard](/np-hard/) problem; Bron-Kerbosch with a pivot takes $O(3^{m/3})$ time in the worst case, but the consistency graph is sparse after pruning, and practical clique solvers are fast on it. Each GNC iteration of line L6 solves a $3 \times 3$ SVD over at most $m(m-1)/2$ TIMs, so $N$ iterations take $O(N m^2)$. Line L7 takes $O(m \log m)$. The front matter states the cost with the known scale; the unknown scale adds $O(m^2 \log m)$. The space is $\Theta(m^2)$ for the TIMs and the graph.

The semidefinite program of TEASER has a matrix of side $4(K + 1)$, where $K$ is the number of TIMs it uses, so its cost grows fast with $K$. This is why TEASER++ uses GNC and checks optimality afterwards with a cheaper certifier.

## Properties

- **Needs no start pose.** All steps are global; no step starts from a guess of the pose.
- **Robust to very high outlier rates.** The paper reports correct results with more than 99% outliers in its benchmarks. This is a measured result, not a bound.
- **Certifiable.** TEASER can prove that its rotation is the global TLS optimum when the relaxation is tight. TEASER++ checks the GNC result with the certifier.
- **Decoupled.** Scale, rotation and translation are found one at a time. The translation does not affect the TIMs, and neither translation nor rotation affects the TRIMs.
- **Needs a noise bound.** The user must give $\beta$. The method uses it to decide what is an inlier.
- **Needs correspondences.** TEASER does not look for matches; it only sorts good matches from bad ones.
- **Deterministic.** The same input gives the same output, unlike [RANSAC](/ransac/).

## Variants and improvements

- **TEASER++.** GNC for the rotation, a fast parallel maximum clique solver, and a separate certifier. It is the form most people use.
- **Known scale.** Skip line L3 and prune with $s$. The reference code does this when the scale is given.
- **Without the clique.** Line L5 can be skipped, so the rotation step sees all TIMs that pass line L4. The clique step costs time, but it removes most outliers before the rotation step, which is the slowest and the least robust step.
- **Other robust costs.** The same split into invariant measurements works with other robust costs in place of TLS, but adaptive voting and the certificate are specific to TLS.

## When to use it

Use TEASER or TEASER++ for global registration from feature matches when many of the matches are wrong, for example in loop closure or object pose estimation from 3D descriptors, and when a guarantee or a check of the result matters. With a few hundred matches it is fast; with many thousands the $\Theta(m^2)$ pairs and the clique step become costly, so keep only the best matches first. When most matches are good, [RANSAC](/ransac/) or [fast global registration](/fast-global-registration/) are simpler. When no matches exist, use a method that searches over poses, such as [Go-ICP](/go-icp/) or [4-points congruent sets](/four-points-congruent-sets/). Refine the result with [ICP](/iterative-closest-point/) on the full clouds, because TEASER uses only the matched points.

## Pitfalls

- **A bad noise bound.** If $\beta$ is too small, true inlier pairs fail line L4, the clique breaks up, and the method fails. If $\beta$ is too large, many outlier pairs pass, and the clique grows with outliers. Set $\beta$ from the sensor noise and the descriptor accuracy, in the units of the points.
- **Symmetric scenes.** If the scene has a symmetry, a set of wrong matches can be as consistent as the right ones, and the largest clique can be the wrong one. No method that uses only the matches can tell them apart.
- **Too few inliers.** The rotation needs at least three inliers that are not on one line. With fewer, the clique is too small to fix the rotation.
- **Close points.** A pair with a short $|\bar a_{ij}|$ has a large bound $\alpha_{ij}$, so it agrees with almost any scale and adds weak edges. The reference code skips pairs with $|\bar a_{ij}| = 0$.
- **The clique as the answer.** The clique is a filter, not a proof that its members are inliers. The rotation step must still use a robust cost.
- **Trusting GNC.** GNC can fail without notice. Use the certifier when the result matters.

## Implementations

## History

Yang and Carlone gave a first form of the method in 2019, with the TLS cost and the semidefinite relaxation of the rotation. Yang, Shi and Carlone published TEASER and TEASER++ in IEEE Transactions on Robotics in 2021, with the decoupling by invariant measurements, adaptive voting, the maximum clique step, the certifier, the error bounds and an open source C++ library. The GNC method for TLS that TEASER++ uses is from Yang, Antonante, Tzoumas and Carlone (2020), building on the graduated non-convexity of Blake and Zisserman for robust costs. The use of a clique of pairwise consistent matches to remove outliers is older, and was used for example in point cloud registration and in the matching of features before RANSAC.

## References
