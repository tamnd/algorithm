---
tag: 9APN7H
kind: algorithm
slug: support-vector-regression
name: Support vector regression
aliases:
- SVR
- epsilon support vector regression
- epsilon-SVR
area: machine-learning/supervised-learning
level: advanced
summary: "Kernel regression that ignores errors smaller than ε and penalizes larger ones linearly. Its dual QP in α and α* gives a sparse fit; only points on or outside the tube count."
solves: [regression]
model: real-ram
complexity:
  vars: {n: the number of training points, t: the cost of one kernel evaluation, s: the number of solver iterations, n_sv: the number of support vectors}
  time: {worst: "O(n^2 t + s n)", best: "Θ(n^2 t)"}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1997
  people: [Vladimir N. Vapnik, Harris Drucker, Christopher J. C. Burges, Linda Kaufman, Alexander J. Smola]
  note: Vapnik introduced the ε-insensitive loss in 1995, and Drucker, Burges, Kaufman, Smola and Vapnik published support vector regression machines in 1997. Smola and Schölkopf wrote the standard tutorial in 2004.
prereqs: [support-vector-machine, regression, kkt-conditions]
see_also: [svm-training, sequential-minimal-optimization, kernel-ridge-regression, ridge-regression, quantile-regression, hinge-loss, representer-theorem, loss-function]
sources:
  - paper: doi:10.1023/B:STCO.0000035301.49549.88
    title: Alex J. Smola and Bernhard Schölkopf, A tutorial on support vector regression, Statistics and Computing 14(3), 2004
    locator: pp. 199 to 222; Section 1.2 (the primal problem with ε and the slacks ξ and ξ*), Section 1.3 (the dual problem in α and α*), Section 1.5 (the KKT conditions and the computation of b)
  - paper: "Harris Drucker, Christopher J. C. Burges, Linda Kaufman, Alex Smola and Vladimir Vapnik, Support vector regression machines, Advances in Neural Information Processing Systems 9 (NIPS 1996), MIT Press, 1997"
    locator: pp. 155 to 161 (support vector regression with the ε-insensitive loss, compared with ridge regression)
  - paper: doi:10.1162/089976600300015565
    title: Bernhard Schölkopf, Alex J. Smola, Robert C. Williamson and Peter L. Bartlett, New support vector algorithms, Neural Computation 12(5), 2000
    locator: pp. 1207 to 1245 (ν-SVR, which chooses the width ε of the tube automatically)
  - paper: doi:10.1145/1961189.1961199
    title: Chih-Chung Chang and Chih-Jen Lin, LIBSVM, a library for support vector machines, ACM Transactions on Intelligent Systems and Technology 2(3), 2011
    locator: Article 27, Section 2.3 (the ε-SVR dual written as one problem in 2n variables) and Section 4 (its solution by the SMO type decomposition method)
  - book: isbn:9780262194754
    title: Bernhard Schölkopf and Alexander J. Smola, Learning with Kernels, MIT Press, 2002
    locator: Chapter 9 (regression estimation; the ε-insensitive loss, the dual and ν-SVR)
---

Support vector regression (SVR) fits a function $f(x) = w \cdot \varphi(x) + b$ to real targets with the *ε-insensitive loss* $\lvert r \rvert_\varepsilon = \max(0, \lvert r \rvert - \varepsilon)$: residuals inside a tube of width $\varepsilon$ around $f$ cost nothing, and larger residuals cost their excess linearly. Together with the penalty $\tfrac12 \lVert w \rVert^2$ this gives a convex quadratic program. Its dual has two multipliers $\alpha_i$ and $\alpha_i^*$ per point, uses the data only through a kernel, and has a sparse solution: only the points on or outside the tube are support vectors. It is the regression form of the [support vector machine](/support-vector-machine/), and the same SMO type solvers train it.

## In plain words

Draw a tube of a fixed width around a curve. Points inside the tube are close enough: they cost nothing and have no effect on the curve. Points outside the tube pull the curve toward them, with a force that does not grow with the distance. Among all curves that do this well, SVR prefers the flattest one.

So the fit depends only on the points at the edge of the tube or outside it. Moving a point that is inside the tube does not change the answer, as long as it stays inside. A wider tube ignores more points, which gives a simpler fit that uses fewer points. A constant $C$ sets how much a point outside the tube costs compared with the flatness.

## The problem

The input is a training set $(x_1, y_1), \ldots, (x_n, y_n)$ with $y_i \in \mathbb{R}$, a positive semidefinite kernel $k$ with feature map $\varphi$ ([kernel trick](/kernel-trick/)), a tube width $\varepsilon \ge 0$ and $C > 0$. This is [regression](/regression/).

**Primal (Smola and Schölkopf 2004).**

$$\min_{w, b, \xi, \xi^*} \; \tfrac12 \lVert w \rVert^2 + C \sum_i (\xi_i + \xi_i^*)$$

subject to $y_i - w \cdot \varphi(x_i) - b \le \varepsilon + \xi_i$, $\; w \cdot \varphi(x_i) + b - y_i \le \varepsilon + \xi_i^*$ and $\xi_i, \xi_i^* \ge 0$. The slack $\xi_i$ measures how far $y_i$ lies above the tube and $\xi_i^*$ how far below. At the optimum $\xi_i + \xi_i^* = \lvert y_i - f(x_i) \rvert_\varepsilon$, so the primal is

$$\min_{w, b} \; \tfrac12 \lVert w \rVert^2 + C \sum_i \lvert y_i - f(x_i) \rvert_\varepsilon .$$

**Dual.** With multipliers $\alpha_i$ for the upper constraints and $\alpha_i^*$ for the lower ones,

$$\max_{\alpha, \alpha^*} \; -\tfrac12 \sum_{i,j} (\alpha_i - \alpha_i^*)(\alpha_j - \alpha_j^*) k(x_i, x_j) - \varepsilon \sum_i (\alpha_i + \alpha_i^*) + \sum_i y_i (\alpha_i - \alpha_i^*)$$

subject to $\sum_i (\alpha_i - \alpha_i^*) = 0$ and $0 \le \alpha_i, \alpha_i^* \le C$. Then $w = \sum_i (\alpha_i - \alpha_i^*) \varphi(x_i)$, and

$$f(x) = \sum_i (\alpha_i - \alpha_i^*) k(x_i, x) + b.$$

**KKT conditions.** Let $r_i = y_i - f(x_i)$. At an optimum with $\varepsilon > 0$, $\alpha_i \alpha_i^* = 0$, and:

| $\alpha_i$ | condition | $\alpha_i^*$ | condition |
|---|---|---|---|
| $0$ | $r_i \le \varepsilon$ | $0$ | $r_i \ge -\varepsilon$ |
| in $(0, C)$ | $r_i = \varepsilon$ | in $(0, C)$ | $r_i = -\varepsilon$ |
| $C$ | $r_i \ge \varepsilon$ | $C$ | $r_i \le -\varepsilon$ |

So a point strictly inside the tube ($\lvert r_i \rvert < \varepsilon$) has $\alpha_i = \alpha_i^* = 0$. A point on the upper edge can have a free $\alpha_i$, and a point above the tube has $\alpha_i = C$. The support vectors are the points with $\alpha_i - \alpha_i^* \ne 0$.

## The algorithm

Write the dual as a minimization in $2n$ variables $\beta = (\alpha, \alpha^*)$ with signs $z = (+1, \ldots, +1, -1, \ldots, -1)$:

$$\min_\beta \; \tfrac12 \beta^\top Q \beta + p^\top \beta \quad \text{subject to } z^\top \beta = 0, \; 0 \le \beta \le C,$$

where $Q_{st} = z_s z_t K_{s \bmod n,\, t \bmod n}$ and $p = (\varepsilon - y_1, \ldots, \varepsilon - y_n, \varepsilon + y_1, \ldots, \varepsilon + y_n)$. Indeed $\beta^\top Q \beta = (\alpha - \alpha^*)^\top K (\alpha - \alpha^*)$ and $p^\top \beta = \varepsilon \sum_i (\alpha_i + \alpha_i^*) - y^\top (\alpha - \alpha^*)$. This is the form of the SVM dual, so LIBSVM solves it with the same code.

```pseudo id=main
SVR-TRAIN(S, k, C, ε)                                    ▷ S = ((x_1, y_1), ..., (x_n, y_n))
L1  K[i][j] ← k(x_i, x_j) for i, j ← 1 to n
L2  z ← (+1 n times, −1 n times); Q[s][t] ← z_s z_t K[s mod n][t mod n]; p ← (ε − y, ε + y)
L3  β ← argmin ½ βᵀQβ + pᵀβ subject to zᵀβ = 0, 0 ≤ β ≤ C      ▷ SMO type with WSS3
L4  θ_i ← β_i − β_{n+i} for i ← 1 to n                          ▷ θ_i = α_i − α_i*
L5  b ← the mean of −z_t G_t over the free t, with G = Qβ + p; if none, the middle of the feasible interval
L6  return (θ, b, SV = {i : θ_i ≠ 0})

SVR-PREDICT(x)
L7  return Σ_{i ∈ SV} θ_i k(x_i, x) + b
```

Line L3 runs the decomposition method of the [SVM training](/svm-training/) page with pairs of variables, as in [sequential minimal optimization](/sequential-minimal-optimization/). With the gradient $G = Q\beta + p$, it takes the index sets $I_{up} = \{t : \beta_t < C, z_t = 1\} \cup \{t : \beta_t > 0, z_t = -1\}$ and $I_{low}$ (the same with the signs swapped). It picks $i = \arg\max_{t \in I_{up}} -z_t G_t$ and then $j \in I_{low}$ by the second order rule WSS3 of Fan, Chen and Lin: among $t$ with $b_t = -z_i G_i + z_t G_t > 0$, it minimizes $-b_t^2 / a_t$ with $a_t = Q_{ii} + Q_{tt} - 2 z_i z_t Q_{it}$. It moves $\beta_i$ by $z_i d$ and $\beta_j$ by $-z_j d$ with $d = \min(b_j / a_j, d_{max})$, which keeps $z^\top \beta = 0$ and the box. It stops when $\max_{I_{up}} -z_t G_t - \min_{I_{low}} -z_t G_t$ is below a tolerance.

For a free $\alpha_i$, $G_i = f(x_i) - b + \varepsilon - y_i$ and the KKT condition $r_i = \varepsilon$ give $b = -G_i$. For a free $\alpha_i^*$, $G_{n+i} = -(f(x_i) - b) + \varepsilon + y_i$ and $r_i = -\varepsilon$ give $b = G_{n+i}$. Both are $-z_t G_t$, which is line L5.

## Example

Take $x = 0, 1, 2$ with $y = 0, 1, 2$, the linear kernel $k(x, z) = xz$, $\varepsilon = 0.5$ and $C = 10$.

**The step.** At $\beta = 0$ the gradient is $G = p = (0.5, -0.5, -1.5 \mid 0.5, 1.5, 2.5)$. All $\alpha_i$ are in $I_{up}$ with $-z_t G_t = (-0.5, 0.5, 1.5)$, so $i = \alpha_3$ with value 1.5. All $\alpha_i^*$ are in $I_{low}$ with $-z_t G_t = (0.5, 1.5, 2.5)$. Only $\alpha_1^*$ has $b_t = 1.5 - 0.5 = 1 > 0$, with $a_t = K_{33} + K_{11} - 2 K_{31} = 4$. The step is $d = 1/4$, so $\alpha_3 = \alpha_1^* = 1/4$. The new gaps are below the tolerance, and the solver stops after this single step.

**The fit.** $\theta = (-1/4, 0, 1/4)$, so $w = \sum_i \theta_i x_i = 1/2$. Both moved variables are free, and $b = 1/2$. The fit is $f(x) = x/2 + 1/2$ with $f = 0.5, 1, 1.5$. The residuals are $-0.5, 0, 0.5$: points 1 and 3 are on the lower and upper edges of the tube, and point 2 is inside it. This is the flattest line that keeps every point in the tube. The primal value is $\tfrac12 \cdot \tfrac14 = 0.125$, and the dual value is $-0.125 - 0.5 \cdot 0.5 + (2 \cdot \tfrac14) = 0.125$.

**A small $C$.** With $C = 0.1$ the step is cut at $d = C$, and $\theta = (-0.1, 0, 0.1)$, $w = 0.2$. Now no multiplier is free. Any $b \in [0.5, 1.1]$ is optimal: the total excess of points 1 and 3 is $1 - 2w$ for every such $b$. The solver takes the middle, $b = 0.8$, so $f(x) = 0.2 x + 0.8$. The primal and dual values are both $0.08$.

## Correctness

The primal is a convex QP with affine constraints, so strong duality holds and the KKT conditions are necessary and sufficient. The proofs folder derives the dual and the table of KKT conditions, shows that $\alpha_i \alpha_i^* = 0$ when $\varepsilon > 0$, and shows that the KKT conditions of the $2n$ variable problem, with $b$ as the multiplier of $z^\top \beta = 0$, are exactly the table above. The solver of line L3 stops when the largest violation is below its tolerance, so the result is optimal within the tolerance.

The tests check the example exactly. On 36 problems with the linear and the Gaussian kernel, $C \in \{0.1, 1, 10\}$ and $\varepsilon \in \{0.05, 0.2\}$, they check the box, $\alpha_i \alpha_i^* = 0$, $\sum_i \theta_i = 0$, the KKT table within $10^{-6}$ and a duality gap below $10^{-6}$ relative. For a linear kernel in one dimension they compare the primal value with a direct minimization over $(w, b)$.

## Complexity

- **Training.** The kernel matrix costs $\Theta(n^2 t)$ time and $\Theta(n^2)$ memory; the $2n \times 2n$ matrix $Q$ needs no new kernel values. Each solver step costs $O(n)$ to update the gradient, so the total is $O(n^2 t + s n)$. The number of steps $s$ grows with $C$ and as $\varepsilon$ decreases. In one run on 40 noisy sine points with a Gaussian kernel and $\varepsilon = 0.1$, the solver took 103 steps with $C = 1$ and about 32000 steps with $C = 100$.
- **Prediction.** $O(n_{sv} t)$ per point.

## Properties

- **Sparse.** Points strictly inside the tube have $\theta_i = 0$. A larger $\varepsilon$ usually gives fewer support vectors: in the test on 40 points, the counts fall as $\varepsilon$ grows from 0.02 to 0.6.
- **Robust to outliers in $y$.** The loss grows linearly, so each point's influence is bounded: $\lvert \theta_i \rvert \le C$. Squared loss methods such as [kernel ridge regression](/kernel-ridge-regression/) let one outlier pull the fit without bound.
- **Unique $f$ up to $b$.** The penalty $\tfrac12 \lVert w \rVert^2$ is strictly convex, so $w$ is unique. The bias $b$ is unique when some multiplier is free, and otherwise lies in an interval, as in the example.
- **Fractions of points (ν property).** In ν-SVR, $\nu$ is an upper bound on the fraction of points outside the tube and a lower bound on the fraction of support vectors.
- **Special cases.** With $\varepsilon = 0$ the loss is the absolute error, so SVR becomes a kernel least absolute deviations fit with a ridge penalty.

## Variants and improvements

- **ν-SVR (Schölkopf et al. 2000).** It adds $\varepsilon$ as a variable with the penalty $C \nu \varepsilon$, so the tube width adapts to the noise.
- **Linear SVR.** For a linear kernel, dual coordinate descent as in LIBLINEAR keeps $w$ explicitly and costs $O(d)$ per step.
- **Squared ε-insensitive loss.** The L2 version uses $\sum_i (\xi_i^2 + \xi_i^{*2})$ and gives a smooth, strongly convex dual.
- **Least squares SVM.** It replaces the loss by the squared error and the inequalities by equalities. The dual is then a linear system, as in [kernel ridge regression](/kernel-ridge-regression/), and the solution is not sparse.
- **[Quantile regression](/quantile-regression/).** The pinball loss is the asymmetric relative of the absolute error, and kernel quantile regression has a dual of the same form.

## When to use it

Use SVR for nonlinear regression on up to tens of thousands of points when a moderate amount of noise is expected and a sparse model or robustness to outliers in the targets is useful. Choose $\varepsilon$ near the noise level. When the data is large, a linear kernel with dual coordinate descent scales further. When an exact least squares fit or predictive variances matter, use [kernel ridge regression](/kernel-ridge-regression/) or a Gaussian process.

## Pitfalls

- **Three hyperparameters.** $C$, $\varepsilon$ and the kernel width interact. Scale the targets first, set $\varepsilon$ from the noise level or use ν-SVR, and cross-validate the rest.
- **$\varepsilon$ too large.** If the tube contains all points, the solution is $w = 0$ with $f$ a constant, whatever the trend in the data.
- **Unscaled inputs.** As for the SVM, the kernel distances depend on the units of the features. Standardize them.
- **Reading $b$.** With no free multiplier, $b$ is only fixed to an interval. Taking it from one bound support vector gives an end of the interval, not a robust value.
- **Slow convergence with a large $C$.** The number of solver steps grows quickly with $C$. Use a loose tolerance, or increase $C$ along a path with warm starts.
- **Dropping $\alpha_i \alpha_i^* = 0$.** With $\varepsilon = 0$ both multipliers of a point can be positive at an optimum. Only $\theta_i = \alpha_i - \alpha_i^*$ matters.

## Implementations

## History

Vapnik introduced the ε-insensitive loss and the support vector method for regression in The Nature of Statistical Learning Theory (1995). Drucker, Burges, Kaufman, Smola and Vapnik (1997) compared it with ridge regression and regression trees. Schölkopf, Smola, Williamson and Bartlett (2000) proposed ν-SVR, and Smola and Schölkopf (2004) wrote the standard tutorial. LIBSVM trains ε-SVR and ν-SVR with the same decomposition method as classification.

## References
