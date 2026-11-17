---
tag: XFXA1G
kind: algorithm
slug: iterative-closest-point
name: Iterative closest point
aliases:
- ICP algorithm
- Besl-McKay ICP
area: computer-vision/point-clouds-and-registration
level: core
summary: "Aligns a source point cloud to a target by repeating two steps: match each point to its closest target point, then fit the best rigid motion to the pairs. The error never rises; the result is local."
solves: [point-cloud-registration]
model: real-ram
complexity:
  vars: {n: the number of source points, m: the number of target points, N: the number of iterations}
  time: {worst: Θ(N n m), average: Θ(N n m), best: Θ(n m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1992
  people: [Paul J. Besl, Neil D. McKay, Yang Chen, Gérard Medioni, Zhengyou Zhang]
  note: "Besl and McKay named the method and proved that its mean squared error converges monotonically. Chen and Medioni (1991 and 1992) and Zhang (1992 and 1994) published close methods at the same time."
prereqs: [point-cloud-registration, kabsch-algorithm, nearest-neighbor-search]
see_also: [icp-convergence-theorem, point-to-plane-icp, generalized-icp, trimmed-icp, go-icp, icp-variants-taxonomy, quaternion-superposition, wahba-problem]
sources:
  - paper: doi:10.1109/34.121791
    title: "Paul J. Besl and Neil D. McKay, A method for registration of 3-D shapes, IEEE Transactions on Pattern Analysis and Machine Intelligence 14(2), 1992, 239-256"
    locator: "The statement of the ICP algorithm, the closed-form registration step by unit quaternions, and the theorem that the mean square error decreases monotonically and converges"
  - paper: doi:10.1016/0262-8856(92)90066-C
    title: "Yang Chen and Gérard Medioni, Object modelling by registration of multiple range images, Image and Vision Computing 10(3), 1992, 145-155"
    locator: "The iterative registration of range images with the point-to-plane error, a method developed at the same time as ICP"
  - paper: doi:10.1007/BF01427149
    title: "Zhengyou Zhang, Iterative point matching for registration of free-form curves and surfaces, International Journal of Computer Vision 13(2), 1994, 119-152"
    locator: "The iterative matching with a k-d tree for the closest points and a statistical threshold that rejects far pairs"
  - paper: doi:10.1109/TPAMI.1987.4767965
    title: "K. S. Arun, Thomas S. Huang and Steven D. Blostein, Least-squares fitting of two 3-D point sets, IEEE Transactions on Pattern Analysis and Machine Intelligence 9(5), 1987, 698-700"
    locator: "The SVD solution of the rotation for matched points, and the degenerate case where it returns a reflection"
  - paper: doi:10.1109/34.88573
    title: "Shinji Umeyama, Least-squares estimation of transformation parameters between two point patterns, IEEE Transactions on Pattern Analysis and Machine Intelligence 13(4), 1991, 376-380"
    locator: "The main theorem: the optimal rotation V diag(1, 1, d) U^T with the sign of the determinant, which fixes the reflection case"
  - paper: doi:10.1364/JOSAA.4.000629
    title: "Berthold K. P. Horn, Closed-form solution of absolute orientation using unit quaternions, Journal of the Optical Society of America A 4(4), 1987, 629-642"
    locator: "The best rotation as the eigenvector of the largest eigenvalue of a 4 by 4 symmetric matrix, used by Besl and McKay for the fit step"
  - paper: doi:10.1007/s11263-006-5167-2
    title: "Helmut Pottmann, Qi-Xing Huang, Yong-Liang Yang and Shi-Min Hu, Geometry and convergence analysis of algorithms for registration of 3D shapes, International Journal of Computer Vision 67(3), 2006, 277-296"
    locator: "The convergence analysis of ICP: linear convergence near a zero-residual solution"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 13.2.1, Range data merging (ICP and its variants)"
---

Iterative closest point (ICP) aligns a source [point cloud](/point-cloud/) $P$ to a target point cloud $Q$ when no point pairs are known. It repeats two steps. First it matches each moved source point $R p_i + t$ to its closest point of $Q$. Then it replaces the rotation $R$ and the translation $t$ by the rigid motion that best fits the source points to their matches, which the [Kabsch algorithm](/kabsch-algorithm/) gives in closed form. The mean squared distance never goes up, and for finite clouds the loop stops at a fixed point after finitely many steps (the [ICP convergence theorem](/icp-convergence-theorem/)). The result is local: from a bad start, ICP stops at a wrong pose. The Kabsch algorithm, the [quaternion method](/quaternion-superposition/) and the [Wahba problem](/wahba-problem/) solve only the fit step, with the pairs given; ICP adds the search for the pairs.

## In plain words

You have two scans of the same object, taken from different places. You want to turn and slide the first scan until it lies on the second one. Nobody tells you which point goes with which.

ICP guesses. For each point of the first scan, it takes the nearest point of the second scan as its partner. With these partners fixed, there is an exact formula for the best turn and slide. Apply it, and the scans come closer. Now the nearest points may be different, so guess the partners again and repeat.

Each round makes the average squared gap smaller or keeps it the same. When the partners stop changing, ICP stops. If the first scan starts far from the right place, the nearest-point guesses are wrong in a consistent way, and ICP settles on a wrong answer.

## The problem

**Input.** A source cloud $P = (p_1, \ldots, p_n)$ and a target cloud $Q = \{q_1, \ldots, q_m\}$ in $\mathbb{R}^3$, with $n, m \ge 1$, and a start pose $(R_0, t_0)$ with $R_0 \in SO(3)$. Coordinates are in meters or are unitless.

**Output.** A rotation $R \in SO(3)$ (so $R^{\mathsf T} R = I$ and $\det R = +1$) and a translation $t \in \mathbb{R}^3$ at a fixed point of the iteration. The goal is a small value of

$$E(R, t) = \frac{1}{n} \sum_{i=1}^{n} \min_{j} |R p_i + t - q_j|^2,$$

the mean squared closest-point distance. ICP does not promise the global minimum of $E$; this is the [point cloud registration](/point-cloud-registration/) problem with the closest-point cost and a local method.

## The algorithm

Write $c(i)$ for the index of the target point matched to $p_i$. For a fixed match $c$, the cost $\frac1n \sum_i |R p_i + t - q_{c(i)}|^2$ is the cost of the [optimal superposition](/optimal-superposition/) problem. The Kabsch step centers both sets, forms $H = \sum_i (p_i - \bar p)(q_{c(i)} - \bar q)^{\mathsf T}$, takes the SVD $H = U S V^{\mathsf T}$, and returns $R = V \operatorname{diag}(1, 1, d)\, U^{\mathsf T}$ with $d = \operatorname{sign}\det(V U^{\mathsf T})$, and $t = \bar q - R \bar p$.

```pseudo id=main
ICP(P, Q, R0, t0, tol)            ▷ P = (p_1 .. p_n), Q = {q_1 .. q_m}
L1  R ← R0 ;  t ← t0 ;  e_prev ← ∞ ;  c_prev ← none
L2  repeat (up to an iteration cap)
L3      c(i) ← index j of the closest q_j to R p_i + t,  for i = 1 .. n
L4      e ← (1/n) Σ_i |R p_i + t - q_c(i)|²
L5      if c = c_prev or e_prev - e ≤ tol then return R, t
L6      (R, t) ← KABSCH((p_i), (q_c(i)))       ▷ R = V diag(1, 1, d) Uᵀ
L7      e_prev ← e ;  c_prev ← c
L8  return R, t                     ▷ only when the cap ends the loop
```

Line L3 is the closest-point step. The reference code uses brute force and breaks ties by the lowest index; a [k-d tree](/kd-tree/) on $Q$ is the usual choice for real data (see [nearest neighbor search](/nearest-neighbor-search/)). Line L4 is the cost at the current pose, which is the value of $E$. Line L5 has two stop rules. A repeated match means that line L6 would return the same pose again. The rule $e_{\text{prev}} - e \le \text{tol}$ stops when the cost no longer falls by more than tol; with tol $= 0$ it stops only at a fixed point. Line L6 is the alignment step. The sign $d$ keeps $\det R = +1$ when the best orthogonal matrix would be a reflection. Besl and McKay used the [quaternion method](/quaternion-superposition/) of Horn for this step, which gives the same rotation.

## Example

Take five source points $p_1 = (0, 0, 0)$, $p_2 = (2, 0, 0)$, $p_3 = (0, 1, 0)$, $p_4 = (0, 0, 1)$ and $p_5 = (1, 1, 1)$. The target is $q_i = R_z(60°) p_i + (0.5, 0, 0)$, where $R_z(\theta)$ turns by $\theta$ about the $z$ axis. Start at $R = I$, $t = 0$, with tol $= 0$. The table gives the match (1-based) and the MSE after each step.

| step | lines | match $c$ | MSE | pose after the step |
|---|---|---|---|---|
| 1 | L3, L4 | (1, 1, 3, 4, 5) | 0.8036 | the start pose |
| 1 | L6 | (1, 1, 3, 4, 5) | 0.5096 | a rotation of 36.04 degrees, $t = (-0.0532, -0.3839, 0.2871)$ |
| 2 | L3, L4 | (1, 2, 3, 4, 5) | 0.4422 | same |
| 2 | L6 | (1, 2, 3, 4, 5) | 0 | $R = R_z(60°)$, $t = (0.5, 0, 0)$ |
| 3 | L3, L4, L5 | (1, 2, 3, 4, 5) | 0 | stop: the match repeats |

In step 1, $p_2 = (2, 0, 0)$ is closer to $q_1 = (0.5, 0, 0)$ than to its true partner $q_2 = (1.5, 1.732, 0)$, so the first fit uses a wrong pair. The fit still lowers the MSE, and the second match is correct. The MSE values 0.8036, 0.5096, 0.4422, 0 never go up.

With the same points and other angles: 20 and 40 degrees give the exact answer after one fit (from MSE 0.2459 and 0.5076). At 90 degrees, ICP stops after one fit at MSE 0.6563, with a rotation error of 48.4 degrees. At 120 degrees it stops at MSE 0.4257 with an error of 143.0 degrees, and at 180 degrees with an error of 179.2 degrees. These are fixed points that are not the true pose: ICP is a local method.

## Correctness

Claim: with tol $= 0$, ICP stops after finitely many iterations, the MSE values it meets never increase, and the returned pose has $\det R = +1$ and is a least squares fit to a closest-point match of itself. The key inequality is $e_k \ge F(R_{k+1}, t_{k+1}, c_k) \ge e_{k+1}$: line L6 minimizes the fixed-match cost $F$, so it cannot be worse than the old pose, and the next line L3 picks the closest point for each source point, so it cannot be worse than the old match. Since the costs fall strictly until the stop, no match repeats, and there are at most $m^n$ matches. The full proof is in [proofs/correctness.md](proofs/correctness.md). The fixed point need not be a local minimum of $E$ when distances tie; the [convergence theorem](/icp-convergence-theorem/) page gives an example.

## Complexity

The model is the [real RAM](/real-ram/). Line L3 with brute force computes $n m$ squared distances, $\Theta(n m)$ time. Line L4 is $\Theta(n)$. Line L6 forms $H$ in $\Theta(n)$ time and then works on $3 \times 3$ matrices in $O(1)$ time, so it is $\Theta(n)$. One iteration is therefore $\Theta(n m)$, and $N$ iterations cost $\Theta(N n m)$. The best case is two passes of line L3, $\Theta(n m)$. With a k-d tree on $Q$, built once in $O(m \log m)$ time, each query of line L3 takes logarithmic expected time on well-spread 3D data (the analysis of Friedman, Bentley and Finkel); this is not a worst-case bound. The extra space holds the moved points and the match, $\Theta(n)$.

The number of iterations $N$ is a separate matter. The proof gives only $N \le m^n + 2$, a crude count. The rate near a solution is linear (Pottmann et al. 2006), and the constant gets worse when the surfaces slide along each other. Measured iteration counts on real data are benchmark results, not bounds.

## Properties

- **Monotone.** The MSE never increases from step to step (lines L4 and L6).
- **Local.** The result depends on the start pose. The example above has fixed points far from the truth.
- **Deterministic.** With a fixed tie rule in line L3, the same input gives the same output.
- **Exact recovery without noise.** If $Q$ contains $R^\star p_i + t^\star$ for every $i$ and the start is close enough, the matches become correct and line L6 returns $(R^\star, t^\star)$ exactly.
- **Not symmetric.** Swapping $P$ and $Q$ changes the cost, because every source point must find a partner but not every target point is used.
- **Proper rotation.** With the sign fix of line L6, $\det R = +1$ always.

## Variants and improvements

- **Point-to-plane error.** [Point-to-plane ICP](/point-to-plane-icp/) measures the distance along the target normal. It converges much faster on smooth surfaces.
- **Plane-to-plane error.** [Generalized ICP](/generalized-icp/) puts a covariance on each point and gives a maximum likelihood fit step.
- **Partial overlap.** [Trimmed ICP](/trimmed-icp/) fits only the fraction $\xi$ of pairs with the least distances, which removes points without a partner.
- **Global optimum.** [Go-ICP](/go-icp/) wraps ICP in a branch and bound search over all poses and returns a pose within $\epsilon$ of the global minimum.
- **Many small choices.** Rusinkiewicz and Levoy sort the variants by stage: selection, matching, weighting, rejection, error metric and minimization; see [efficient variants of ICP](/icp-variants-taxonomy/).
- **Robust weights.** Weights from an [M-estimator](/m-estimator/), solved by [iteratively reweighted least squares](/iteratively-reweighted-least-squares/), reduce the pull of far pairs.

## When to use it

Use ICP when a rough pose is known, for example from odometry, from the previous frame of a depth camera, or from a feature match with [RANSAC](/ransac/). It is simple, it has no parameters except the stop rule, and each step has a closed form. For surfaces sampled at different places, the point-to-plane form is usually faster. For clouds that only partly overlap, use trimming or a distance threshold. Without a rough pose, use a global method first: [fast global registration](/fast-global-registration/), [TEASER](/teaser-registration/), [4PCS](/four-points-congruent-sets/), or Go-ICP when a certificate of the optimum is needed. For 2D laser scans with a grid map, [correlative scan matching](/correlative-scan-matching/) searches over a window of poses instead.

## Pitfalls

- **No sign fix in line L6.** $R \leftarrow V U^{\mathsf T}$ from the SVD can return a reflection, with $\det R = -1$, for nearly planar or noisy pairs. Use $R \leftarrow V \operatorname{diag}(1, 1, d)\, U^{\mathsf T}$ with $d = \operatorname{sign}\det(V U^{\mathsf T})$.
- **The wrong direction of matching in line L3.** Matching each target point to its closest source point and then fitting $P$ to $Q$ mixes two different costs, and the proof of monotone decrease fails. Match each moved source point $R p_i + t$ to $Q$.
- **The wrong cost in line L5.** Comparing the cost after line L6 (with the old pairs) with the cost after line L3 (with the new pairs) mixes two quantities. Compare the values of line L4 of two iterations, as the pseudocode does.
- **A bad start.** ICP has many fixed points. In the example, a start 90 degrees away ends 48 degrees off. Get a rough pose first.
- **Partial overlap.** Points of $P$ with no true partner in $Q$ still get a closest point, and these pairs bias the fit. Reject pairs farther than a threshold, or use trimmed ICP.
- **Exact float tests.** With tol $= 0$ in floating point, rounding can make $e$ rise by a tiny amount at the fixed point. Line L5 then stops, which is the right result; do not treat it as an error.

## Implementations

## History

Besl and McKay published ICP in 1992 in IEEE TPAMI, for registering free-form shapes such as point sets, curves and surfaces. They used Horn's 1987 quaternion solution for the fit step and proved that the mean square error converges monotonically. Chen and Medioni presented a close method at ICRA in 1991 and in Image and Vision Computing in 1992, with the distance to the tangent plane of the target. Zhang's method, in a 1992 report and in IJCV in 1994, used a k-d tree and a statistical rule that rejects far pairs. The SVD solution of the fit step goes back to Arun, Huang and Blostein (1987), and Umeyama (1991) fixed its reflection case. Rusinkiewicz and Levoy (2001) compared the many variants and gave a fast combination.

## References
