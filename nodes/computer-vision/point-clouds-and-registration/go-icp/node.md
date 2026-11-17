---
tag: AT1CTF
kind: algorithm
slug: go-icp
name: Go-ICP
aliases:
- globally optimal ICP
area: computer-vision/point-clouds-and-registration
level: research
summary: "Finds the rigid motion that minimizes the ICP cost over a whole box of rotations and translations, within a gap eps, by nested branch and bound with local ICP for upper bounds."
solves: [point-cloud-registration]
model: real-ram
complexity:
  vars: {n: the number of source points, m: the number of target points, K: the number of rotation cubes examined, T: the largest number of translation cubes examined for one rotation cube}
  time: {worst: O(K T n m), average: O(K T n m), best: Θ(n m)}
  space: {extra: O(K + T + n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2013
  people: [Jiaolong Yang, Hongdong Li, Yunde Jia, Dylan Campbell]
  note: "Yang, Li and Jia presented Go-ICP at ICCV 2013. The journal version with Campbell (IEEE TPAMI, 2016) adds trimming for outliers and more experiments."
prereqs: [iterative-closest-point, best-first-branch-and-bound]
see_also: [axis-angle-representation, distance-transform, trimmed-icp, teaser-registration, fast-global-registration, four-points-congruent-sets, icp-convergence-theorem, point-cloud-registration]
sources:
  - paper: doi:10.1109/TPAMI.2015.2513405
    title: "Jiaolong Yang, Hongdong Li, Dylan Campbell and Yunde Jia, Go-ICP: A globally optimal solution to 3D ICP point-set registration, IEEE Transactions on Pattern Analysis and Machine Intelligence 38(11), 2016, 2241-2254"
    locator: "The angle-axis parametrization of rotations in the cube [-pi, pi]^3, Theorem 1 (the uncertainty radius of a rotation cube), Theorem 2 (the bounds of the residuals), the nested branch and bound with ICP for the upper bounds, the trimmed extension for outliers, and the 3D distance transform for closest-point distances"
  - paper: doi:10.1109/34.121791
    title: "Paul J. Besl and Neil D. McKay, A method for registration of 3-D shapes, IEEE Transactions on Pattern Analysis and Machine Intelligence 14(2), 1992, 239-256"
    locator: "The ICP algorithm and its cost, which Go-ICP minimizes globally"
  - paper: doi:10.1109/ICPR.2002.1047997
    title: "Dmitry Chetverikov, Dmitry Svirko, Dmitry Stepanov and Pavel Krsek, The Trimmed Iterative Closest Point algorithm, Proceedings of the 16th International Conference on Pattern Recognition (ICPR 2002), volume 3"
    locator: "The trimmed cost that Go-ICP adopts for outliers"
---

Go-ICP finds the rigid motion that best aligns a source [point cloud](/point-cloud/) $P$ to a target $Q$ under the cost of [iterative closest point](/iterative-closest-point/), the sum of squared closest-point distances, over a whole box of rotations and translations, not only near a start pose. It searches the rotations, written as angle-axis vectors in a cube, by best-first [branch and bound](/best-first-branch-and-bound/). For each rotation cube, an inner branch and bound over the translations gives a lower bound of the cost on the cube. Local ICP, started from the best poses that the search finds, gives upper bounds. The search stops when the best cost found is within $\epsilon$ of the least lower bound, so the result is within $\epsilon$ of the global minimum over the box. The bounds come from two inequalities of Yang, Li, Campbell and Jia: how far a point can move when the rotation varies in a cube, and how much each residual can change. The price is time: the search can examine many thousands of cubes.

## In plain words

Plain ICP walks downhill from where it starts and stops in the first valley. Go-ICP looks at every possible turn and slide, but in a clever way.

It splits the space of all turns into boxes. For a box, it asks: what is the best cost that any turn in this box could possibly reach? A short calculation gives a number that is sure to be at most that cost. If this number is already worse than the best answer found so far, the whole box is dropped. Otherwise the box is split into eight smaller boxes, and the question is asked again.

To find good answers early, it runs plain ICP from promising places. The search ends when no box left could beat the best answer by more than a small margin $\epsilon$.

## The problem

**Input.** A source $P = (p_1, \ldots, p_n)$ and a target $Q = \{q_1, \ldots, q_m\}$ in $\mathbb{R}^3$, a cube $C_r$ of angle-axis vectors (by default $[-\pi, \pi]^3$), a cube $C_t$ of translations, and a gap $\epsilon > 0$. Coordinates are unitless in the tests.

**Output.** A pose $(R, t)$ with $R \in SO(3)$ and its cost $E = E(R, t)$, where

$$E(R, t) = \sum_{i=1}^{n} e_i(R, t)^2, \qquad e_i(R, t) = \min_j |R p_i + t - q_j|,$$

such that $E < m^\star + \epsilon$, with $m^\star$ the least cost over the rotations $R_r$, $r \in C_r$ with $|r| \le \pi$, and the translations $t \in C_t$. Here $R_r$ is the rotation by the angle $|r|$ about the axis $r / |r|$ (see the [axis-angle representation](/axis-angle-representation/)); the ball $|r| \le \pi$ holds every rotation.

## The algorithm

The bounds rest on two facts. Let $r$ lie in a rotation cube of half side $\sigma_r$ with center $r_0$, and $t$ in a translation cube of half side $\sigma_t$ with center $t_0$.

- Rotation uncertainty (Theorem 1 of the paper): $|R_r x - R_{r_0} x| \le \gamma_r(x) = 2 \sin(\min(\sqrt{3}\sigma_r/2, \pi/2))\, |x|$. The angle between $R_r x$ and $R_{r_0} x$ is at most $|r - r_0| \le \sqrt{3}\sigma_r$, a lemma that goes back to Hartley and Kahl (2009), and the chord of that angle is the bound.
- Residual bound (Theorem 2 of the paper): with $\gamma_t = \sqrt{3}\sigma_t$, $e_i(R_r, t) \ge \max(e_i(R_{r_0}, t_0) - \gamma_r(p_i) - \gamma_t, 0)$, by the triangle inequality.

For a rotation cube with center $r_0$, the inner search minimizes $f(t) = \sum_i \max(e_i(R_{r_0}, t) - \gamma_i, 0)^2$ with $\gamma_i = \gamma_r(p_i)$. Since $E(R_r, t) \ge f(t)$ on the cube, a lower bound of $f$ over $C_t$ is a lower bound of $E$ over the cube.

```pseudo id=main
GO-ICP(P, Q, ε, C_r, C_t)
L1  (R, t, E) ← LOCAL-ICP(P, Q) from the start pose ;  queue ← {(0, C_r)}
L2  while the queue is not empty and E - (least bound in the queue) ≥ ε
L3      pop the cube of least bound ;  h ← its half side / 2 ;  γ_i ← 2 sin(min(√3 h / 2, π/2)) |p_i|
L4      for each of its 8 sub-cubes, with center r0 and half side h, skipping those with |r0| - √3 h > π
L5          (E_t, t_b, L) ← INNER-BNB(R_r0 P, γ, Q, C_t, E, ε/2, ε)
L6          if t_b ≠ none and E(R_r0, t_b) < E then update (R, t, E), then run LOCAL-ICP from (R_r0, t_b) and keep it if better
L7          if L < E then push (L, sub-cube)
L8  return R, t, E

INNER-BNB(X, γ, Q, C_t, E_b, δ, enough)        ▷ X = R_r0 P ;  f(t) = Σ max(e_i(t) - γ_i, 0)²
L9   E_t ← E_b ;  t_b ← none ;  try the center of C_t ;  push C_t with its bound if the bound < E_t
L10  while the queue is not empty and E_t - lb ≥ δ and E_b - lb ≥ enough   ▷ lb = least bound
L11      pop the cube of least bound ;  s ← its half side / 2 ;  γ_t ← √3 s ;  for each of its 8 sub-cubes, center c:
L12          if f(c) < E_t then E_t ← f(c) ;  t_b ← c
L13          f_low ← Σ max(e_i(c) - γ_i - γ_t, 0)² ;  if f_low < E_t then push (f_low, sub-cube)
L14  return E_t, t_b, L = min(E_t, least bound in the queue)
```

The outer search (lines L1 to L8) keeps the best cost $E$ and a queue of rotation cubes ordered by their lower bounds. Line L3 splits the cube of least bound. Line L4 drops sub-cubes that lie wholly outside the ball of radius $\pi$, since they hold no new rotation. Line L5 runs the inner search over translations with the rotation uncertainties of the sub-cube. Line L6 evaluates the true cost at the center rotation and the best translation of the inner search. If it beats $E$, it becomes the new $E$, and a local ICP from there often lowers $E$ at once. Line L7 keeps the sub-cube only if its bound can still beat $E$.

The inner search (lines L9 to L14) is the same idea over translations. It stops when its best value is within $\delta = \epsilon/2$ of its least bound, or when its least bound is within $\epsilon$ of the outer $E$, which is enough for the outer test. It returns a true lower bound $L$ of $f$ over $C_t$.

The reference code differs from the paper in three ways. First, the paper runs a second inner search with $\gamma = 0$ for the upper bound; the code reads the upper bound off the lower-bound search in line L6, which keeps the guarantee, as the proof shows, and costs much less. Second, the inner search returns a certified lower bound and uses the two stop rules of line L10. Third, closest points are found by brute force, $\Theta(n m)$ per evaluation; the paper looks them up in a precomputed 3D [distance transform](/distance-transform/), which makes each lookup $O(1)$ but adds the error of the grid.

## Example

The target is 20 points drawn uniformly in $[-0.6, 0.6]^3$ (seed 5). The source is 10 of them, moved by the inverse of a rotation of 150 degrees about the axis $(1, -1, 2)$ and the translation $(0.1, -0.05, 0.08)$, without noise. So the true cost is 0.

- Local ICP from the identity stops at the cost 0.7042, a wrong pose.
- Go-ICP over $C_r = [-\pi, \pi]^3$, $C_t = [-0.5, 0.5]^3$ and $\epsilon = 0.01$ returns the cost $7.2 \times 10^{-31}$ and the true pose to within $10^{-6}$. It examines 217 rotation cubes and runs local ICP 3 times, in about 0.36 s of pure Python.

Noise makes the certificate expensive. With 6 source points out of 10 target points and Gaussian noise of standard deviation 0.03 on each coordinate, the minimum is above $\epsilon$, so the bounds must prune instead of stopping at a zero cost. Over a rotation cube of half side 0.3 that holds the true rotation, with $C_t = [-0.2, 0.2]^3$ and $\epsilon = 0.014$, Go-ICP returns the cost 0.015472 after 248 rotation cubes and one local ICP, in about 0.74 s. The test checks it against 61 runs of local ICP from random rotations and from the true one: none of them is lower by $\epsilon$ or more. Over the full cube $[-\pi, \pi]^3$ with $\epsilon = 0.01$, the same scene takes 3980 rotation cubes and about 27 s. These times are measurements of the reference code on one machine.

## Correctness

Claim: Go-ICP stops, and returns $(R, t, E)$ with $E = E(R, t)$, $\det R = +1$ and $E < m^\star + \epsilon$. The invariant is: every pose of the domain has its rotation in a cube of the queue, or has a cost of at least the current $E$. Cubes leave the queue only by a split, by line L4 (no rotation of the ball), or by line L7 (a bound of at least $E$, which stays valid because $E$ only falls). The bounds are valid by the two facts above. So when the least bound in the queue is above $E - \epsilon$, so is $m^\star$. Termination holds because the gap between the true cost and the bound of a cube of half side $h$ shrinks in proportion to $h$, so small cubes either are dropped or end the search when they reach the top of the queue. The full proof, with a proof of the rotation uncertainty bound, is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

The model is the [real RAM](/real-ram/). Each evaluation of the residuals at one pose costs $\Theta(n m)$ by brute force. The inner search for one rotation cube evaluates 8 sub-cubes per pop, so it costs $O(T n m)$ if it examines at most $T$ translation cubes. The outer search examines $K$ rotation cubes, and each one costs one inner search, so the total is $O(K T n m)$ plus the local ICP runs, which cost $\Theta(n m)$ per ICP iteration. With a distance transform, each evaluation costs $\Theta(n)$ after the preprocessing of a grid.

$K$ and $T$ are not polynomial in the input in the worst case. A cube must shrink until the gap between its bound and the cost is below about $\epsilon$, which needs a half side proportional to $\epsilon$, and there are about $(1/h)^3$ cubes of half side $h$ in a fixed box. So the worst case grows like $\epsilon^{-3}$ for each of the two searches. In practice, local ICP finds a near-optimal cost early, and most cubes are dropped at large sizes. The counts in the example are benchmark results, not bounds. The space holds the two queues and the residuals, $O(K + T + n)$.

## Properties

- **Global within $\epsilon$.** The result is within $\epsilon$ of the least cost over the domain, as a proved bound, not a measured rate.
- **A certificate.** The least bound in the queue at the stop is a lower bound of the optimal cost.
- **Deterministic.** The same input gives the same output.
- **Slow in the worst case.** The running time grows quickly as $\epsilon$ falls and as noise lifts the optimal cost above zero.
- **Sensitive to outliers in the plain form.** The plain cost sums all residuals, so points without partners lift the optimum; the trimmed form handles them.

## Variants and improvements

- **Trimming.** The paper extends the bounds to a trimmed cost that keeps a fixed fraction of the smallest residuals, as in [trimmed ICP](/trimmed-icp/).
- **Distance transform.** A precomputed 3D [distance transform](/distance-transform/) of the target replaces the nearest neighbor search by a table lookup.
- **Better bounds.** Later work tightens the rotation bounds or searches rotations and translations jointly, which prunes more cubes.
- **Other global methods.** [TEASER](/teaser-registration/) certifies a robust pose from feature matches. [Fast global registration](/fast-global-registration/) and [4PCS](/four-points-congruent-sets/) are fast, but they give no certificate of the optimum.

## When to use it

Use Go-ICP when no start pose is known, the clouds are small (hundreds to a few thousand points), and a proof of near-optimality matters, for example to check other methods or in safety reviews. For large clouds or when time is short, get a rough pose by feature matching with [RANSAC](/ransac/) or by a fast global method, then refine it with [ICP](/iterative-closest-point/). If the clouds overlap only in part, use the trimmed cost. Limit the rotation and translation domains when prior knowledge allows: the example shows that a small rotation cube is much cheaper than the full one.

## Pitfalls

- **A translation box that is too small in line L5.** The guarantee holds only over $C_t$. If the true translation lies outside it, Go-ICP returns the best pose inside, which can be wrong. Center the clouds and choose $C_t$ large enough.
- **The rotation bound without the min in line L3.** Using $\sqrt{3} h |p_i|$ for large cubes is valid but loose; using $2 \sin(\sqrt{3} h / 2) |p_i|$ without the min is wrong when $\sqrt{3} h > \pi$, because the sine then falls. Use $2 \sin(\min(\sqrt{3} h/2, \pi/2)) |p_i|$.
- **A best value in place of a lower bound in line L14.** If the inner search returns its best value $E_t$ instead of $\min(E_t, \text{least bound})$, the outer bound is not valid, and the search can drop the cube that holds the optimum.
- **Too small an $\epsilon$ in line L2.** With noise, a tiny gap makes the search split cubes until rounding error, and the time explodes. Choose $\epsilon$ on the scale of the noise times the number of points.
- **Uncentered clouds.** The rotation bound grows with $|p_i|$. Center $P$ at its centroid first, so that the bounds are tight.

## Implementations

## History

Yang, Li and Jia presented Go-ICP at ICCV in 2013. The journal version, with Campbell, appeared in IEEE TPAMI in 2016, with the trimmed cost for outliers and more tests. It was the first globally optimal method for the ICP cost of 3D registration with both rotation and translation unknown. The rotation search builds on the branch and bound over rotation space of Hartley and Kahl (2009), and the trimming on the trimmed ICP of Chetverikov et al. (2002).

## References
