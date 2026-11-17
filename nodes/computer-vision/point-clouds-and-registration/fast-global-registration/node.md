---
tag: MFA6WR
kind: algorithm
slug: fast-global-registration
name: Fast global registration
aliases:
- FGR
area: computer-vision/point-clouds-and-registration
level: research
summary: "Aligns point clouds from feature matches by minimizing a Geman-McClure robust cost with a line process and a shrinking scale, with no closest point queries."
solves: [point-cloud-registration]
model: real-ram
complexity:
  vars: {m: the number of correspondences, N: the number of iterations}
  time: {worst: Θ(N m), average: Θ(N m), best: Θ(N m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2016
  people: [Qian-Yi Zhou, Jaesik Park, Vladlen Koltun]
  note: "Zhou, Park and Koltun presented FGR at ECCV 2016. It combines the line process of Black and Rangarajan with graduated non-convexity, on matches of local features."
prereqs: [point-cloud-registration, m-estimator, gauss-newton-algorithm]
see_also: [teaser-registration, iterative-closest-point, point-feature-histograms, iteratively-reweighted-least-squares, ransac, mutual-nearest-neighbor-matching, go-icp, four-points-congruent-sets]
sources:
  - paper: doi:10.1007/978-3-319-46475-6_47
    title: "Qian-Yi Zhou, Jaesik Park and Vladlen Koltun, Fast global registration, Computer Vision, ECCV 2016, Lecture Notes in Computer Science 9906, Springer, 2016, 766-782"
    locator: "The scaled Geman-McClure cost, the line process and its closed-form weights, the linearized update of the pose, the schedule of the scale mu, and the reciprocity and tuple tests for the correspondences"
  - paper: doi:10.1109/34.121791
    title: "Paul J. Besl and Neil D. McKay, A method for registration of 3-D shapes, IEEE Transactions on Pattern Analysis and Machine Intelligence 14(2), 1992, 239-256"
    locator: "The ICP algorithm, the local method with closest point queries that FGR avoids"
---

Fast global registration (FGR) aligns two [point clouds](/point-cloud/) from a fixed set of correspondences, found once by matching local [feature descriptors](/feature-descriptor/) such as [FPFH](/point-feature-histograms/). Many of the matches can be wrong. FGR minimizes a robust cost, the scaled Geman-McClure function of the match residuals, which grows like a square for small residuals and tends to a constant $\mu$ for large ones, so a wrong match has a bounded effect. It writes this cost with a line process: a weight per match, chosen in closed form, turns the cost into a weighted least squares problem in the pose. Each iteration sets the weights, takes one [Gauss-Newton](/gauss-newton-algorithm/) step on the six parameters of a small rigid motion, and every few iterations makes $\mu$ smaller, so the cost moves from nearly least squares to strongly robust. Unlike [iterative closest point](/iterative-closest-point/), FGR never searches for closest points during the optimization, which makes each iteration cheap, and it needs no start pose.

## In plain words

You have a list of guessed matches between two scans, made once from the shape around each point. Some guesses are wrong.

Give each match a weight. Find the turn and shift that best fit the matches, counting each by its weight. A match that the current pose fits badly gets a small weight, so it pulls less in the next round. Repeat.

At first, the method is tolerant: even a badly fit match keeps much of its weight, so all matches pull together and the scans swing into rough place. Then, step by step, it becomes strict: a match must fit closely to keep its weight. The wrong matches fade out, and the right ones fix the pose.

The method never asks which point is closest to which. It only works with the list it was given.

## The problem

**Input.** Correspondences $(p_k, q_k)$ with $p_k, q_k \in \mathbb{R}^3$, for $k = 1, \ldots, m$; a start value $\mu_0$ of the scale; and a final value $\delta^2$.

**Output.** A rigid motion $T = (R, t)$, with $R \in SO(3)$, at a stationary point of

$$E(T) = \sum_{k=1}^{m} \rho(|q_k - T p_k|), \qquad \rho(x) = \frac{\mu x^2}{\mu + x^2},$$

reached through the sequence of decreasing $\mu$. The cost $\rho$ is a redescending [M-estimator](/m-estimator/): its influence goes to zero for large residuals. FGR does not promise the global minimum. This is [point cloud registration](/point-cloud-registration/) with given correspondences, a form of [robust model fitting](/robust-model-fitting/).

## The algorithm

**The line process.** FGR minimizes the joint cost

$$E(T, L) = \sum_{k} l_k |q_k - T p_k|^2 + \sum_k \mu (\sqrt{l_k} - 1)^2$$

over the pose and the weights $l_k \ge 0$. For a fixed pose, the best weight of a match with residual $r$ is $l = (\mu / (\mu + r^2))^2$, and putting it in gives back $\rho(r)$. For fixed weights, the cost is a weighted least squares cost in $T$.

**The pose step.** Write a small motion as $\xi = (\omega, v)$: the rotation by the vector $\omega$, then the shift $v$. For $x_k = T p_k$, the residual after the motion is about $r_k + J_k \xi$, with $r_k = x_k - q_k$ and $J_k = [-[x_k]_\times \mid I]$. Minimizing $\sum_k l_k |r_k + J_k \xi|^2$ gives the $6 \times 6$ normal equations $H \xi = -g$.

```pseudo id=main
FGR(P, Q, μ₀, δ)                 ▷ correspondences (p_k, q_k), k = 1 .. m
L1  R ← I ;  t ← 0 ;  μ ← μ₀
L2  for it = 1 .. N
L3      l_k ← (μ / (μ + |T p_k - q_k|²))²   for each k
L4      H ← Σ_k l_k J_kᵀ J_k ;  g ← Σ_k l_k J_kᵀ (T p_k - q_k)
L5      ξ ← -H⁻¹ g
L6      T ← exp(ξ) T
L7      if it is a multiple of 4:  μ ← max(μ / 2, δ²)
L8  return T
```

Line L1 starts at the identity. The paper sets $\mu_0 = D^2$, where $D$ is the diameter of the largest surface; the reference code uses the diagonal of the box around both sets. Line L3 is the closed-form weight of the line process. Lines L4 and L5 are the Gauss-Newton step of [weighted least squares](/weighted-least-squares/) with these weights. Line L6 applies the motion: the rotation by $\omega$, as in [Rodrigues' formula](/rodrigues-rotation-formula/), then the shift. Line L7 is the graduated non-convexity schedule: the paper halves $\mu$ every four iterations until it reaches $\delta^2$, for a small distance threshold $\delta$ set by the user. Some implementations, such as Open3D, divide by 1.4 instead of 2.

**The correspondences.** FGR finds them once, before line L1. For each point it computes a descriptor such as FPFH and finds the nearest descriptor in the other cloud, in both directions. The reciprocity test keeps a pair only if each point is the other's nearest, as in [mutual nearest neighbor matching](/mutual-nearest-neighbor-matching/). The tuple test then picks random triples of pairs and keeps the pairs of a triple when all three distances in one cloud agree with the matching distances in the other within a factor $\tau$, with $\tau = 0.9$: $\tau < |p_i - p_j| / |q_i - q_j| < 1 / \tau$. A rigid motion keeps distances, so right matches pass this test.

## Example

Take eight points $p_1, \ldots, p_8$: $(0, 0, 0)$, $(1, 0, 0)$, $(0, 2, 0)$, $(0, 0, 3)$, $(1, 1, 0)$, $(2, 0, 1)$, $(0, 1, 2)$, $(1, 2, 3)$. The true motion turns by 90 degrees about the $z$ axis and shifts by $(1, 0, 0)$. Six matches are right; the matches of $p_3$ and $p_6$ are wrong, with $q_3 = (3, 3, 3)$ and $q_6 = (-2, 1, 0)$. The box around both sets has the diagonal $D^2 = 43$, so $\mu_0 = 43$, and $\delta^2$ is small. The table shows the state after each listed iteration: the $\mu$ of that iteration, the angle between the estimate and the true rotation, the translation, the weights of the two wrong matches, and the cost $E$ at that $\mu$.

| iteration | $\mu$ | rotation error | $t$ | $l_3$ | $l_6$ | $E$ |
|---|---|---|---|---|---|---|
| 1 | 43 | 83.51° | (-0.009, 0.411, -0.163) | 0.481 | 0.497 | 31.608 |
| 4 | 43 | 84.10° | (0.060, 0.564, -0.120) | 0.516 | 0.516 | 31.390 |
| 8 | 21.5 | 8.49° | (0.766, -0.045, -0.050) | 0.174 | 0.361 | 20.798 |
| 12 | 10.75 | 18.85° | (1.023, 0.063, 0.018) | 0.053 | 0.335 | 13.236 |
| 16 | 5.375 | 7.37° | (1.001, 0.016, 0.004) | 0.018 | 0.130 | 8.187 |
| 20 | 2.688 | 2.27° | (0.999, 0.004, 0.001) | 0.005 | 0.041 | 4.643 |
| 24 | 1.344 | 0.67° | (0.999, 0.001, 0.000) | 0.001 | 0.012 | 2.489 |
| 32 | 0.336 | 0.049° | (1.000, 0.000, 0.000) | 0.000 | 0.001 | 0.659 |
| 40 | 0.084 | 0.003° | (1.000, 0.000, 0.000) | 0.000 | 0.000 | 0.167 |

With $\mu = 43$, every match keeps about half its weight or more, and the fit is close to least squares over all eight matches: the rotation is still far off. When $\mu$ falls to 21.5, the pose swings to within 8.5 degrees. At $\mu = 10.75$ the error grows again to about 19 degrees while $E$ falls: the wrong match $q_6$ still has weight 0.34 and pulls the pose toward it. As $\mu$ falls further, the two wrong matches lose their weight, and the six right ones fix the pose. After 64 iterations the rotation error is below $10^{-5}$ degrees and $t = (1, 0, 0)$ to eight digits. Within each stage of fixed $\mu$, $E$ falls at every step in this run.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows three facts. First, the line process is exact: $l = (\mu / (\mu + r^2))^2$ is the unique best weight, and the joint cost with this weight equals $\rho(r)$. Second, the vector $g$ of line L4 is half the gradient of $E$ with respect to a small motion, because $\rho'$ as a function of $r^2$ is exactly the weight $l$. Third, if the points $T p_k$ do not all lie on one line, $H$ is positive definite, so the step $\xi = -H^{-1} g$ is zero exactly at a stationary point of $E$, and otherwise it is a descent direction: a short enough step along $\xi$ lowers $E$. This is the standard link between [iteratively reweighted least squares](/iteratively-reweighted-least-squares/) and robust costs.

The claims are weaker than they may seem. FGR takes the full step, and a full Gauss-Newton step is not proved to lower $E$; a line search would make each stage monotone. Each change of $\mu$ changes the cost. A stationary point need not be the global minimum, and graduated non-convexity is a heuristic, not a guarantee. The method is called global because it needs no start pose, not because it proves global optimality.

## Complexity

The model is the [real RAM](/real-ram/). Lines L3 and L4 take $\Theta(m)$ time per iteration, and line L5 solves a $6 \times 6$ system in $O(1)$. So $N$ iterations take $\Theta(N m)$ time and $\Theta(m)$ extra space. The reference code uses a fixed number of iterations, 64 by default, so the cost of the optimization is small.

The correspondences cost more. For $n$ points per cloud, the descriptors take time that depends on the descriptor; FPFH with $k$ neighbors takes $O(n k)$ after a neighbor search. The nearest neighbor search in descriptor space takes $\Theta(n^2)$ by brute force, as in the reference code, or less with a [k-d tree](/kd-tree/) or an [approximate](/approximate-nearest-neighbor/) search. The tuple test takes $O(1)$ per triple.

## Properties

- **No closest point queries.** The correspondences are fixed. ICP searches for closest points in every iteration; FGR does not.
- **No start pose.** FGR starts at the identity, and the large first $\mu$ lets distant matches pull the clouds into place.
- **Robust.** The Geman-McClure cost bounds the cost of a wrong match by $\mu$, and its weight tends to 0. In tests, the reference code recovers the pose with 70% of the matches wrong.
- **Not certified.** FGR gives no proof that its result is the global minimum, unlike [TEASER](/teaser-registration/).
- **Deterministic.** The optimization is deterministic. The tuple test uses random triples.
- **Depends on the features.** If the descriptors give too few right matches, no robust cost can recover the pose.

## Variants and improvements

- **Multi-way registration.** The paper also aligns many scans at once, with one line process per pair of scans and a joint step over all poses.
- **The schedule.** Open3D divides $\mu$ by 1.4 and stops when $\mu$ is small. Other robust costs, such as the [Tukey biweight](/tukey-biweight/) or truncated least squares, fit into the same scheme.
- **Graduated non-convexity in general.** Yang, Antonante, Tzoumas and Carlone (2020) give the same idea for many robust costs and many problems, and TEASER++ uses it for the rotation.
- **Refinement.** A few iterations of ICP after FGR refine the pose on all points.

## When to use it

Use FGR for global registration of two scans when good local features are available and a fast answer matters, such as in the reconstruction of indoor scenes from many scans. It is usually faster than [RANSAC](/ransac/) on the same matches, because it needs no sampling and no repeated tests of hypotheses. When the fraction of wrong matches is very high, use [TEASER](/teaser-registration/), which is built for that case and can certify its result. When the clouds are already close, use ICP. When no features are available, use [Go-ICP](/go-icp/) or [4-points congruent sets](/four-points-congruent-sets/).

## Pitfalls

- **Units.** $\mu$ and $\delta$ are squared lengths. If the clouds are in millimeters and $\delta$ was set for meters, the final cost is far too strict or too tolerant. Normalize the clouds or set $\delta$ from the noise level.
- **Stopping too early.** If $\mu$ stays large, the wrong matches keep their weight and bias the pose, as in iteration 12 of the example.
- **Degenerate geometry.** If the points of the matches lie near one line, $H$ is singular or badly conditioned, and the step is not defined.
- **Rotation updates.** Apply the step as a rotation, not as $I + [\omega]_\times$, or the estimate drifts away from a rotation matrix.
- **Too many tuples.** The tuple test keeps a pair if any of its triples passes. With many random triples, a wrong pair often finds one that passes by chance, so the test removes fewer wrong pairs.
- **Symmetric scenes.** If the scene has a symmetry, the matches can support a wrong pose as well as the right one.

## Implementations

## History

Zhou, Park and Koltun presented FGR at ECCV 2016. The method combines three older ideas: the line process of Black and Rangarajan (1996), which links robust costs and weighted least squares; graduated non-convexity, from the work of Blake and Zisserman on visual reconstruction; and the matching of local 3D features such as the FPFH descriptor of Rusu, Blodow and Beetz (2009). FGR became part of the Open3D library, where it is a common first step before ICP.

## References
