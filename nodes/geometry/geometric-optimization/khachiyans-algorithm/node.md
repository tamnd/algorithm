---
tag: QERG9C
kind: algorithm
slug: khachiyans-algorithm
name: Khachiyan's algorithm
aliases:
- Khachiyan minimum volume ellipsoid algorithm
- Khachiyan's barycentric coordinate ascent
- Fedorov-Wynn-Khachiyan algorithm
area: geometry/geometric-optimization
level: advanced
summary: First-order method for the minimum volume enclosing ellipsoid. It moves weight to the point farthest in the current ellipsoid's norm and reaches volume factor (1+ε)^((d+1)/2).
solves: [minimum-volume-enclosing-ellipsoid]
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, k: the number of iterations}
  time: {worst: O(k n d)}
  space: {extra: O(n + d^2)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1996
  people: [Leonid G. Khachiyan]
  note: Khachiyan gave the weight update with exact line search on log det, its iteration bound, and the rounding of polytopes by the resulting ellipsoid.
prereqs: [minimum-volume-enclosing-ellipsoid, coreset]
see_also: [badoiu-clarkson-algorithm, minimum-enclosing-ball, lp-type-problem, welzls-algorithm, clarksons-algorithm, minimum-area-enclosing-rectangle, convex-hull, weiszfelds-algorithm]
sources:
  - paper: "Leonid G. Khachiyan, Rounding of polytopes in the real number model of computation, Mathematics of Operations Research 21(2), 1996"
    locator: the algorithm on the lifted points, the step size, Lemma 4 (the halving argument), Lemma 5 and Theorem 3 (from the relaxed optimality conditions to a rounding and to a (1 + η)-approximation of the minimum volume ellipsoid)
  - paper: "Michael J. Todd and E. Alper Yıldırım, On Khachiyan's algorithm for the computation of minimum-volume enclosing ellipsoids, Discrete Applied Mathematics 155(13), 2007"
    locator: Section 2 (the dual problem and the ε-approximate optimality conditions), equation (4) (Khachiyan's operation count), equation (5) (the Kumar-Yıldırım count), Section 3 (O(nd) work per iteration by rank-one updates), Theorem 4.1 (O(d(log d + 1/ε)) iterations with away steps)
  - paper: "Piyush Kumar and E. Alper Yıldırım, Minimum-volume enclosing ellipsoids and core sets, Journal of Optimization Theory and Applications 126(1), 2005"
    locator: the initialization with 2d points, the bound without the log log n term, and core sets whose size does not depend on n
  - paper: "Fritz John, Extremum problems with inequalities as subsidiary conditions, Studies and Essays presented to R. Courant on his 60th Birthday, Interscience, 1948"
    locator: uniqueness of the minimum volume ellipsoid, the contact points, at most d(d + 3)/2 of them, and the factor d by which it shrinks into the convex hull
---

Khachiyan's algorithm computes an approximate [minimum volume enclosing ellipsoid](/minimum-volume-enclosing-ellipsoid/) of $n$ points in $\mathbb{R}^d$. It works on the dual problem, a concave maximization of $\log\det$ over weights on the points. It lifts each point $a_i$ to $q_i = (a_i, 1) \in \mathbb{R}^{d+1}$, starts with equal weights, and in each step finds the point farthest from the current ellipsoid in that ellipsoid's own norm. It then moves weight to that point by the step that maximizes $\log\det$ exactly. It stops when no point is more than a factor $1 + \varepsilon$ outside, and returns an ellipsoid that contains all points and has volume at most $(1 + \varepsilon(d+1)/d)^{d/2}$ times the minimum. Khachiyan (1996) bounded the work by $O\bigl(n d^2 (1/\varepsilon + \log d + \log\log n)\bigr)$ arithmetic operations, which is $O(d(1/\varepsilon + \log d + \log\log n))$ steps of $O(nd)$ each. It is the ellipsoid counterpart of the [Bădoiu-Clarkson algorithm](/badoiu-clarkson-algorithm/) for balls.

## In plain words

You want the smallest egg shape, in any number of dimensions, that holds a cloud of points. Give each point a share of weight, equal at first. The weights define an egg: its center is the weighted average of the points, and its shape follows how the weighted points spread out.

Now look for the point that sticks out farthest from this egg, measured in the egg's own stretched units. Move some weight to that point. The egg then grows toward it and shrinks elsewhere. The amount of weight to move has a simple formula that gives the best egg along that move.

Repeat until no point sticks out by more than a small margin. The final egg holds every point, and its volume is almost the smallest possible.

## The problem

Notation: $P = \{a_1, \dots, a_n\} \subset \mathbb{R}^d$ is the input; it must span $\mathbb{R}^d$ affinely (otherwise every enclosing ellipsoid is flat and has volume 0). An ellipsoid is $E(c, Q) = \{x : (x - c)^\top Q (x - c) \le 1\}$ with $Q$ symmetric positive definite, and $\mathrm{vol}\, E(c, Q) = \omega_d \det(Q)^{-1/2}$, where $\omega_d$ is the volume of the unit ball. The minimum volume enclosing ellipsoid $E^*$, the Löwner-John ellipsoid, exists and is unique. Given $\varepsilon > 0$, the task is an ellipsoid $E \supseteq P$ with a proved bound on $\mathrm{vol}(E)/\mathrm{vol}(E^*)$.

**The lift.** Put $q_i = (a_i, 1) \in \mathbb{R}^{d+1}$. For weights $p$ in the simplex $\{p \ge 0, \sum_i p_i = 1\}$ put

$$\Lambda(p) = \sum_{i} p_i\, q_i q_i^\top, \qquad w_i(p) = q_i^\top \Lambda(p)^{-1} q_i.$$

The dual problem is to maximize $\log\det \Lambda(p)$ over the simplex. Its optimum $p^*$ gives $E^*$: with $c = \sum_i p^*_i a_i$ and $S = \sum_i p^*_i a_i a_i^\top - c c^\top$, $E^* = \{x : (x - c)^\top S^{-1} (x - c) \le d\}$. A weight vector $p$ is $\varepsilon$-optimal if $w_i(p) \le (1 + \varepsilon)(d + 1)$ for all $i$ (Khachiyan's relaxed optimality conditions). Two identities drive the method: $\sum_i p_i w_i(p) = \mathrm{tr}(\Lambda^{-1}\Lambda) = d + 1$, so the largest $w_i$ is at least $d + 1$; and, by the Schur complement,

$$w_i(p) = (a_i - c_p)^\top S_p^{-1} (a_i - c_p) + 1, \qquad c_p = \sum_i p_i a_i, \quad S_p = \sum_i p_i a_i a_i^\top - c_p c_p^\top.$$

So $w_i - 1$ is the squared distance of $a_i$ from $c_p$ in the norm of $S_p^{-1}$.

**The measure.** The guarantee is on volume. Khachiyan's form: if $p$ is $\varepsilon$-optimal, a $(1 + \eta)$-approximation in volume follows with $1 + \eta = (1 + \varepsilon)^{(d+1)/2}$. The ellipsoid returned here satisfies the slightly sharper bound $(1 + \varepsilon(d + 1)/d)^{d/2}$ proved below. No guarantee is given on the center or the axes directly; they converge, but more slowly.

Model: real RAM for the analysis. The implementation is numerical, in floating point.

## The algorithm

```pseudo id=main
KHACHIYAN(a₁, …, aₙ, ε)
L1  q_i ← (a_i, 1) for every i;  p ← (1/n, …, 1/n)
L2  loop
L3      Λ ← Σ p_i q_i q_iᵀ
L4      w_i ← q_iᵀ Λ⁻¹ q_i for every i;  j ← argmax_i w_i;  κ ← w_j
L5      if κ ≤ (1 + ε)(d + 1) then exit the loop
L6      β ← (κ − d − 1) / ((d + 1)(κ − 1))
L7      p ← (1 − β) p + β e_j
L8  c ← Σ p_i a_i;  S ← Σ p_i a_i a_iᵀ − c cᵀ
L9  return E(c, S⁻¹/(κ − 1))
```

Line L6 is the exact maximizer of $\log\det((1 - \beta)\Lambda + \beta q_j q_j^\top)$ over $\beta$. Line L9 scales the ellipsoid of $S^{-1}$ so that the farthest point lies on its boundary, which by the Schur identity is $\max_i (w_i - 1) = \kappa - 1$. Khachiyan's implementation keeps $\Lambda^{-1}$ and all $w_i$ up to date with a rank-one formula in $O(nd)$ per step; the implementation here recomputes $\Lambda$ in $O(nd^2)$, which is simpler.

## Example

Take the six points $(0, 0)$, $(10, 0)$, $(0, 6)$, $(4, 8)$, $(9, 7)$, $(5, 3)$ in the plane, so $d + 1 = 3$. The first steps, from equal weights $1/6$:

| step | $w$ for the six points | farthest | $\kappa$ | $\beta$ | $\log\det\Lambda$ before |
|---|---|---|---|---|---|
| 1 | 4.060, 4.329, 2.779, 2.567, 3.161, 1.103 | $(10, 0)$ | 4.3289 | 0.1331 | 5.0574 |
| 2 | 4.596, 3.000, 3.013, 2.904, 3.451, 1.036 | $(0, 0)$ | 4.5959 | 0.1479 | 5.1385 |
| 3 | 3.000, 3.476, 3.053, 3.393, 3.629, 1.010 | $(9, 7)$ | 3.6293 | 0.0798 | 5.2449 |

The weighted mean of the $w_i$ is exactly 3 in every row: for example $(4.060 + 4.329 + 2.779 + 2.567 + 3.161 + 1.103)/6 = 3$. After a step, the point that just got weight has $w = 3$ in the next row. The inner point $(5, 3)$ has small $w$ throughout, and its weight decays toward 0.

Runs to the stopping test give:

| $\varepsilon$ | steps | center | area of $E$ | certified bound $\mathrm{vol}(E)/\mathrm{vol}(E^*)$ |
|---|---|---|---|---|
| $10^{-1}$ | 14 | $(5.1194, 3.0409)$ | 105.43 | 1.1309 |
| $10^{-2}$ | 168 | $(5.0530, 3.0550)$ | 99.94 | 1.0143 |
| $10^{-3}$ | 1655 | $(5.0473, 3.0504)$ | 99.42 | 1.0015 |
| $10^{-4}$ | 16376 | $(5.0468, 3.0495)$ | 99.37 | 1.00015 |

The last column is the ratio of the area to the lower bound $\omega_2 \det(2 S_p)^{1/2}$ from the final weights, so it bounds the true ratio; each value is below $1 + 1.5\varepsilon$, the guarantee for $d = 2$. So the minimum area is between $99.35$ and $99.37$. At $\varepsilon = 10^{-3}$ the weights are $0.2804$, $0.2905$, $0.1048$, $0.1547$, $0.1688$, $0.0009$: five points carry the ellipse, and the inner point carries almost nothing. The number of steps grows like $1/\varepsilon$.

## Correctness

The full proof is in [proofs/correctness](proofs/correctness.md). Its parts:

1. **The output contains $P$.** By the Schur identity, $(a_i - c)^\top S^{-1} (a_i - c) = w_i - 1 \le \kappa - 1$ for every $i$, so every point lies in $E(c, S^{-1}/(\kappa - 1))$.
2. **A lower bound on every enclosing ellipsoid.** If $E(z, M) \supseteq P$, then $\sum_i p_i (a_i - z)^\top M (a_i - z) \le 1$, and the left side is at least $\mathrm{tr}(M S_p)$. By the inequality of arithmetic and geometric means applied to the eigenvalues of $M^{1/2} S_p M^{1/2}$, $\det(M S_p) \le d^{-d}$, so $\mathrm{vol}\, E(z, M) \ge \omega_d \det(d S_p)^{1/2}$. This holds for every weight vector $p$, so it is a certificate.
3. **The volume bound.** At exit, $\mathrm{vol}(E) = \omega_d \det((\kappa - 1) S)^{1/2}$, and the ratio to the bound in part 2 is $((\kappa - 1)/d)^{d/2} \le (1 + \varepsilon(d + 1)/d)^{d/2}$.
4. **Each step increases $\log\det\Lambda$.** By the matrix determinant lemma, the step on L7 changes $\log\det\Lambda$ by $h(\kappa) = d \log\frac{d\,\kappa}{(d+1)(\kappa - 1)} + \log\frac{\kappa}{d + 1}$, which is positive for $\kappa > d + 1$ and at least $\varepsilon^2/(2(1 + \varepsilon)^2)$ when $\kappa > (1 + \varepsilon)(d + 1)$.
5. **Termination.** Weak duality gives $\log\det\Lambda(p) \le \log\det\Lambda(p_0) + (d + 1)\ln n$ for every $p$, so there are at most $2(1 + \varepsilon)^2 (d + 1) \ln n/\varepsilon^2$ steps. Khachiyan's halving argument improves this to $O(d(1/\varepsilon + \log d + \log\log n))$.

## Complexity

- **Steps.** Khachiyan (1996): a $(1 + \eta)$-approximation in volume in $O\bigl(n d^2 ([(1 + \eta)^{2/(d+1)} - 1]^{-1} + \log d + \log\log n)\bigr)$ operations, where $[(1 + \eta)^{2/(d+1)} - 1]^{-1} = O(d/\eta)$ for $\eta \le 1$. In terms of the relaxed conditions this is $O(d(1/\varepsilon + \log d + \log\log n))$ steps. Kumar and Yıldırım (2005) start from $2d$ well-chosen points and remove the $\log\log n$ term. Todd and Yıldırım (2007) add steps that remove weight and prove $O(d(\log d + 1/\varepsilon))$ steps.
- **Work per step.** $O(nd)$ with rank-one updates of $\Lambda^{-1}$ and of all $w_i$; $O(nd^2)$ when, as here, $\Lambda$ is rebuilt and inverted. So $O(knd)$ time for $k$ steps.
- **Space.** $O(n)$ weights and $O(d^2)$ for $\Lambda^{-1}$.
- **Convergence of the shape.** The guarantee is on volume only. The center and the matrix also converge, but they can lag behind the volume, because many ellipsoids have nearly the minimum volume.

## Properties

- **Always feasible output.** The returned ellipsoid contains every point at every step, not only at the end, so one may stop at any time with a valid enclosing ellipsoid and a certified ratio.
- **A certificate of quality.** Part 2 of the proof gives a lower bound from the current weights, so the ratio printed in the example is a proof, not an estimate.
- **Monotone dual.** $\log\det\Lambda(p)$ increases in every step.
- **Affine invariance.** The steps do not change under an invertible affine map of the points: the $w_i$ are affine invariant. So badly scaled or thin point sets cost no extra steps.
- **Weights stay positive.** The plain method never sets a weight to 0: a point inside keeps a positive weight that decays slowly. This is one reason the plain method needs $O(1/\varepsilon)$ steps and why away steps help.
- **Core sets.** With the Kumar-Yıldırım start, the points that ever get weight form a core set of size $O(d(\log d + 1/\varepsilon))$, independent of $n$. John (1948) showed that at most $d(d + 3)/2$ contact points determine $E^*$.

## Variants and improvements

- **Kumar-Yıldırım initialization.** Start with weight on $2d$ points found by $d$ directional extremes; this bounds the initial gap by $O(d \log d)$ instead of $O(d \log n)$.
- **Todd-Yıldırım away steps.** Also allow a step that removes weight from the point with the smallest $w_i$ among those with positive weight. This gives $O(d(\log d + 1/\varepsilon))$ steps and, in practice and under conditions, linear convergence.
- **Rounding.** Khachiyan's original goal: the ellipsoid $E$, shrunk by the factor about $d$ (or $\sqrt{d}$ for symmetric sets), lies inside $\mathrm{conv}(P)$, a rounding of the polytope used in convex optimization and volume estimation.
- **Interior-point methods.** For high accuracy, interior-point methods for $\log\det$ maximization solve the problem in polynomially many steps that depend on $\log(1/\varepsilon)$, at a higher cost per step.
- **Exact algorithms in fixed dimension.** The minimum volume ellipsoid is an [LP-type problem](/lp-type-problem/) with combinatorial dimension $d(d + 3)/2$, so [Welzl's algorithm](/welzls-algorithm/) and [Clarkson's algorithm](/clarksons-algorithm/) solve it in expected $O(n)$ time for fixed $d$, with a small exact solver on $O(d^2)$ points.
- **D-optimal design.** The same update, with the same step, is the Fedorov-Wynn algorithm for D-optimal experimental design, whose dual is this problem.

## When to use it

- **Moderate accuracy in moderate dimension.** For $d$ up to the hundreds and $\varepsilon$ of $10^{-2}$ to $10^{-4}$, it is simple and stable with rank-one updates. Each extra digit of accuracy costs about 10 times more steps.
- **Bounding volumes.** Enclosing ellipsoids for collision tests, outlier detection and covariance-type summaries of point clouds, where a certified $1 + \varepsilon$ factor is enough.
- **Not for high accuracy.** The $O(1/\varepsilon)$ step count makes $\varepsilon = 10^{-8}$ slow; use away steps, an interior-point method, or a core set followed by an exact solver.
- **Not in the plane for exact answers.** For an exact smallest ellipse of points in the plane, use an exact LP-type method; Khachiyan's algorithm is numerical.

## Pitfalls

- **Degenerate input.** If the points lie in a hyperplane, $\Lambda$ is singular and the method breaks. Detect it, and solve the problem in the affine hull.
- **Numerical inverse.** Rebuilding $\Lambda^{-1}$ by explicit inversion each step loses accuracy for thin point sets. Keep a Cholesky factor with rank-one updates, as Todd and Yıldırım recommend.
- **Reporting the wrong scale.** $E(c, S^{-1}/d)$ is the optimal ellipsoid only at the optimum; for $\varepsilon$-optimal weights it may miss points. Scale by $\kappa - 1$, or by $d + \varepsilon(d + 1)$, as on L9.
- **Confusing the measures.** $\varepsilon$ bounds $w_i$, not the volume. The volume factor is about $1 + \varepsilon(d+1)/2$ for small $\varepsilon$, and the radius-like factor is $\sqrt{1 + \varepsilon(d+1)/d}$.
- **Stopping on the center.** The center changes very little near the end even when the volume is still far from optimal, and vice versa; stop on $\kappa$, which is what the guarantee uses.
- **Integer weights.** The method needs real weights; with floating point, renormalize $p$ to sum 1 now and then.

## Implementations

## History

Fritz John (1948) proved that the minimum volume ellipsoid is unique and that it shrinks by a factor $d$ into the convex hull. In optimal experimental design, Fedorov (1972) and Wynn (1970) gave the exchange algorithm for D-optimal designs, which moves weight toward the point of largest variance; the dual of D-optimal design is the minimum volume enclosing ellipsoid of the design points. Khachiyan (1996) analyzed this method for the ellipsoid problem in the real number model, with the step on L6, and bounded its work by $O(nd^2(1/\varepsilon + \log d + \log\log n))$; he used it to round polytopes. Kumar and Yıldırım (2005) improved the start and found core sets, and Todd and Yıldırım (2007) added away steps and a careful numerical implementation. The [Bădoiu-Clarkson algorithm](/badoiu-clarkson-algorithm/) for balls (2003) is the same Frank-Wolfe pattern with a fixed step.

## References
