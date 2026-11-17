---
tag: P020QC
kind: algorithm
slug: robust-point-matching
name: Robust point matching
aliases:
- TPS-RPM
- softassign point matching
area: computer-vision/point-clouds-and-registration
level: advanced
summary: "Softassign RPM (Gold et al.): match two point sets with outliers by alternating a soft match matrix, normalized by Sinkhorn with slacks, and a pose fit, while annealing the temperature."
solves: [point-cloud-registration]
model: real-ram
complexity:
  vars: {n: the number of points in X, m: the number of points in Y, N: the number of pose updates over the whole schedule, K: the number of Sinkhorn sweeps per update}
  time: {worst: Θ(N K n m), average: Θ(N K n m), best: Θ(N n m)}
  space: {extra: Θ(n m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1998
  people: [Steven Gold, Anand Rangarajan, Chien-Ping Lu, Suguna Pappu, Eric Mjolsness]
  note: "Gold, Rangarajan, Lu, Pappu and Mjolsness published softassign point matching in Pattern Recognition in 1998. Chui and Rangarajan (2003) replaced the affine map by a thin-plate spline for non-rigid matching."
prereqs: [point-cloud-registration, assignment-problem, weighted-least-squares]
see_also: [coherent-point-drift, iterative-closest-point, non-rigid-registration, hungarian-algorithm, simulated-annealing, expectation-maximization, kullback-leibler-divergence, quadratic-assignment-problem]
sources:
  - paper: doi:10.1016/S0031-3203(98)80010-1
    title: "Steven Gold, Anand Rangarajan, Chien-Ping Lu, Suguna Pappu and Eric Mjolsness, New algorithms for 2D and 3D point matching: pose estimation and correspondence, Pattern Recognition 31(8), 1998, 1019-1031"
    locator: "The energy with a match matrix and a reward for matches, the slack row and column for outliers, softassign with Sinkhorn normalization, deterministic annealing, and the alternation with the pose update"
  - paper: doi:10.1016/S1077-3142(03)00009-2
    title: "Haili Chui and Anand Rangarajan, A new point matching algorithm for non-rigid registration, Computer Vision and Image Understanding 89(2-3), 2003, 114-141"
    locator: "The non-rigid form of the method with a thin-plate spline map, and the annealing of the regularization weight"
  - paper: doi:10.1214/aoms/1177703591
    title: "Richard Sinkhorn, A relationship between arbitrary positive matrices and doubly stochastic matrices, The Annals of Mathematical Statistics 35(2), 1964, 876-879"
    locator: "The scaling of a positive square matrix to doubly stochastic form by alternating row and column normalization"
---

Robust point matching (RPM) finds both a map between two point sets and the correspondence between their points, when neither is known, some points have no partner, and some are outliers. This page is about the softassign method of Gold, Rangarajan, Lu, Pappu and Mjolsness (1998). Instead of a hard 0 or 1 match for each pair, as in the [assignment problem](/assignment-problem/), it keeps a soft match matrix $M$ whose entries lie between 0 and 1. An extra slack row and slack column take the mass of points with no partner. The method alternates two steps: compute $M$ from the current map by softassign, an exponential of the distances followed by Sinkhorn normalization of the rows and columns, then fit the map to all pairs weighted by $M$, as in [weighted least squares](/weighted-least-squares/). A temperature controls how soft $M$ is. It starts high, so that every point matches every point a little, and goes down slowly, so that $M$ hardens into a one-to-one match. This is deterministic annealing.

## In plain words

You have two sets of dots and want to slide and stretch one onto the other, but you do not know which dot goes with which, and some dots have no partner.

Do not decide at once. Let each dot spread a little interest over all dots of the other set, more over near ones. Make sure each dot hands out exactly one unit of interest in total, with an extra "no partner" box that can take some of it. Now move the first set to best fit all these soft pairings at once. Then share out the interest again from the new position.

At first, keep the interest very spread out, so only the rough shape matters. Step by step, make it sharper, so that each dot ends up with one clear partner or with none.

## The problem

**Input.** Two finite point sets in the plane, $X = \{x_1, \ldots, x_n\}$ and $Y = \{y_1, \ldots, y_m\}$, and a reward $\alpha > 0$ for each match.

**Output.** An affine map $y \mapsto A y + t$ and a partial one-to-one match between $X$ and $Y$ such that matched points lie close, $|x_j - A y_k - t|^2 < \alpha$, and as many points as possible are matched. Points with no good partner stay unmatched.

The energy that RPM lowers, at the inverse temperature $\beta$, is

$$E_\beta(M, A, t) = \sum_{j,k} M_{jk} \bigl( |x_j - A y_k - t|^2 - \alpha \bigr) + \lambda \|A - I\|_F^2 + \frac{1}{\beta} \sum M (\log M - 1),$$

where the last sum runs over all entries, the slacks included, and each row of $X$ and each column of $Y$ of $M$, with its slack, sums to 1. The entropy term makes $E_\beta$ strictly convex in $M$. As $\beta \to \infty$ it vanishes and the best $M$ becomes a 0 or 1 matrix: a match pays off exactly when its squared distance is below $\alpha$. This is a hard, non-convex problem in the match and the map together.

## The algorithm

```pseudo id=main
RPM(X, Y, α, β₀, β_f, r)
L1  A ← I ;  t ← 0 ;  β ← β₀
L2  while β ≤ β_f
L3      repeat a few times
L4          d_jk ← |x_j - A y_k - t|²
L5          M_jk ← exp(β(α - d_jk)) ;  slack entries ← 1
L6          Sinkhorn: divide each row of X, with its slack, by its sum
L7                    divide each column of Y, with its slack, by its sum ;  repeat L6 and L7 until the sums are 1
L8          (A, t) ← argmin Σ M_jk |x_j - A y_k - t|² + λ|A - I|²
L9      β ← β · r
L10 return A, t, and the matches read off from M
```

Lines L4 to L7 are softassign. Line L5 turns each distance into a positive weight; the slack column entry of row $j$ and the slack row entry of column $k$ start at $e^0 = 1$, the weight of a pair at the squared distance $\alpha$. Lines L6 and L7 are the iteration of Sinkhorn (1964): each step only scales a row or a column, so the result has the form $M_{jk} = e^{\beta(\alpha - d_{jk})} e^{-u_j - v_k}$. The slack column is part of the rows of $X$, and the slack row is part of the columns of $Y$, but the slacks themselves have no sum constraint, so a point can give most of its mass to its slack. Line L8 is a small linear system: for each row $r$ of $A$, three unknowns $(a_{r1}, a_{r2}, t_r)$. Line L10 reads off a match $(j, k)$ when $M_{jk}$ is the largest entry of its row and of its column and larger than both slacks.

Gold et al. handle rigid and affine maps in 2D and 3D, with a penalty on the affine part. The reference code uses the simple penalty $\lambda \|A - I\|_F^2$ with a weight $\lambda = \max(0.01, 10 \beta_0 / \beta)$ that is strong at the start and weak at the end; this schedule is a choice of the code. It starts at $\beta_0 = 0.5$, ends at $\beta_f = 500$, multiplies $\beta$ by $r = 1.2$, and does three updates and up to 30 Sinkhorn sweeps at each $\beta$.

## Example

**Softassign on three and two points.** Let $X = \{(0, 0), (1, 0), (3, 0)\}$, $Y = \{(0, 0), (1, 0)\}$, the map the identity and $\alpha = 0.5$. The squared distances from $x_1$ are 0 and 1, from $x_2$ are 1 and 0, and from $x_3$ are 9 and 4. After Sinkhorn has converged:

| $\beta$ | $M$, row $x_1$ | $M$, row $x_2$ | $M$, row $x_3$ | slacks of $x_1, x_2, x_3$ | slacks of $y_1, y_2$ |
|---:|---|---|---|---|---|
| 1 | 0.380, 0.138 | 0.141, 0.376 | 0.000, 0.014 | 0.482, 0.483, 0.986 | 0.479, 0.472 |
| 4 | 0.683, 0.013 | 0.013, 0.683 | 0.000, 0.000 | 0.304, 0.304, 1.000 | 0.304, 0.304 |
| 20 | 0.989, 0.000 | 0.000, 0.989 | 0.000, 0.000 | 0.004, 0.004, 1.000 | 0.011, 0.011 |

Every row of $X$ with its slack sums to 1, and so does every column of $Y$. At $\beta = 1$ the match is very soft: $x_1$ gives about half of its mass to its slack. As $\beta$ grows, the two good pairs take nearly all the mass, and the far point $x_3$ goes to its slack: it is an outlier.

**A full run.** $Y$ has 15 random points in $[-1, 1]^2$. $X$ holds the images of 13 of them under $A = \begin{pmatrix} 0.95 & -0.35 \\ 0.25 & 1.1 \end{pmatrix}$ and $t = (0.3, -0.2)$, with noise of standard deviation 0.01, plus 3 random outliers, in random order. With $\alpha = 0.04$, the run has 38 values of $\beta$:

| Step | $\beta$ | $\lambda$ | largest error in $A$ and $t$ | total real mass in $M$ |
|---:|---:|---:|---:|---:|
| 0 | 0.5 | 10.0 | 0.365 | 11.34 |
| 12 | 4.5 | 1.12 | 0.291 | 8.78 |
| 18 | 13.3 | 0.376 | 0.166 | 7.72 |
| 24 | 39.8 | 0.126 | 0.041 | 8.75 |
| 30 | 118.7 | 0.042 | 0.013 | 11.88 |
| 37 | 425.3 | 0.012 | 0.007 | 12.58 |

The real mass first drops, while the map is poor and many points prefer their slacks, and then rises as the map locks on. All 13 true pairs are found, and the 3 outliers of $X$ and the 2 points of $Y$ without an image go to their slacks.

## Correctness

At a fixed $\beta$ and $\lambda$, both steps lower the same energy $E_\beta$. Sinkhorn only scales rows and columns, so its result has the form $e^{\beta(\alpha - d_{jk})} e^{-u_j - v_k}$; once the sums are 1, this form satisfies the optimality conditions of the strictly convex problem in $M$, so it is the unique minimizer of $E_\beta$ over the match matrices with these sums. The pose step minimizes a strictly convex quadratic in $(A, t)$, since $\lambda > 0$. So the inner loop is block [coordinate descent](/coordinate-descent/), and $E_\beta$ never rises within it. The full proof is in [proofs/correctness.md](proofs/correctness.md).

The annealing itself has no such guarantee. When $\beta$ grows the energy changes, and the whole method is a heuristic that can end in a local minimum. In the tests, a run with a small fixed $\lambda$ lets the affine part go wrong early and never recovers.

## Complexity

The model is the [real RAM](/real-ram/). Line L4 computes $n m$ distances, and line L5 $n m$ exponentials. One Sinkhorn sweep reads every entry twice, in $\Theta(n m)$ time. Line L8 sums over all $n m$ entries and solves two $3 \times 3$ systems. So one update with $K$ sweeps takes $\Theta(K n m)$ time, and a run with $N$ updates takes $\Theta(N K n m)$ time; if each Sinkhorn call stops after one sweep, it takes $\Theta(N n m)$. With $\beta$ multiplied by $r$ from $\beta_0$ to $\beta_f$ and a fixed number of updates per $\beta$, $N$ is proportional to $\log(\beta_f / \beta_0) / \log r$. The match matrix needs $\Theta(n m)$ space.

## Properties

- **Joint.** It solves for the match and the map together, not one after the other.
- **Robust to outliers and missing points.** The slacks let points stay unmatched; the reward $\alpha$ sets the distance beyond which a match does not pay.
- **One-to-one in the limit.** The Sinkhorn constraints make $M$ close to a partial permutation at large $\beta$, unlike [ICP](/iterative-closest-point/), where many points can share one nearest neighbour.
- **Wide basin.** At a small $\beta$ every point sees all points, so the first maps depend on the overall shape, not on the nearest points. This gives a much wider basin than ICP, but no guarantee.
- **Deterministic.** There is no random choice; the same input and schedule give the same result.
- **Quadratic.** Each update costs $\Theta(n m)$ time and space, which limits it to a few thousand points.

## Variants and improvements

- **Non-rigid maps.** Chui and Rangarajan (2003) replace the affine map by a thin-plate spline, with a bending energy as the regularizer, and anneal its weight together with the temperature. This is the best known form of RPM; see [non-rigid registration](/non-rigid-registration/).
- **Probabilistic view.** [Coherent point drift](/coherent-point-drift/) uses a Gaussian mixture and [EM](/expectation-maximization/). Its posterior matrix is a softassign with only one of the two normalizations, plus a uniform outlier term, and its variance plays the part of the temperature.
- **Rigid and 3D.** The same scheme works for rotations and translations in 2D or 3D, with the pose step solved by the SVD instead of a linear system.
- **Graph matching.** The softassign idea also applies to matching graphs, where the cost is quadratic in $M$, as in the [quadratic assignment problem](/quadratic-assignment-problem/).

## When to use it

Use RPM when two point sets of moderate size must be matched without features, the start pose is poor, and points may be missing or extra on both sides, for example landmarks on two shapes or contour points. For a known one-to-one match with no outliers, the [Hungarian algorithm](/hungarian-algorithm/) gives the exact assignment for a fixed map. For large scans that already overlap well, [ICP](/iterative-closest-point/) is much cheaper. For smooth non-rigid maps of larger sets, [coherent point drift](/coherent-point-drift/) is a common choice.

## Pitfalls

- **The reward alpha.** It sets the distance at which a point becomes an outlier, in squared units of the data. Too small, and true pairs with noise go to the slacks; too large, and outliers get matched. Normalize the data first.
- **The schedule.** A fast increase of $\beta$ freezes the match too early, in a poor local minimum; a slow one costs time. The range of $\beta$ must match the scale of the data: $\beta_0$ well below $1 / \max d_{jk}$ and $\beta_f$ well above $1 / \alpha$.
- **The penalty.** With a weak penalty at the start, the affine map can shrink or shear the set onto a few points. Start with a strong penalty and relax it.
- **Overflow.** At a large $\beta$, $e^{\beta(\alpha - d)}$ overflows. Subtract the largest exponent of each row before the exponential; the row step cancels the common factor.
- **Sinkhorn sweeps.** At a large $\beta$, Sinkhorn converges slowly. A fixed number of sweeps leaves the sums off by a little, which is usually harmless but breaks the energy argument.
- **Memory.** The matrix has $n m$ entries. Subsample large sets.

## Implementations

## History

Gold, Rangarajan, Lu, Pappu and Mjolsness published softassign point matching in Pattern Recognition in 1998, for rigid and affine maps in 2D and 3D. It combines the softassign of a match matrix with Sinkhorn normalization, slack variables for outliers, and deterministic annealing from statistical physics. Sinkhorn's 1964 result on the scaling of positive matrices to doubly stochastic form gave the normalization step. Chui and Rangarajan (2003) extended the method to non-rigid maps with thin-plate splines, and this form became a standard baseline for non-rigid point set registration. [Coherent point drift](/coherent-point-drift/) later recast the problem as the fit of a Gaussian mixture.

## References
