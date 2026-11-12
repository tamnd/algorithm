---
tag: J4MKX9
kind: algorithm
slug: lasso-regression
name: Lasso regression
aliases:
- lasso
- L1-regularized regression
- least absolute shrinkage and selection operator
area: machine-learning/supervised-learning
level: core
summary: Least squares with an L1 penalty, which sets some weights exactly to zero. Solved by cyclic coordinate descent with soft thresholding, or for the whole path by LARS.
solves: [linear-regression]
model: real-ram
complexity:
  vars: {n: the number of examples, d: the number of features, k: the number of sweeps}
  time: {worst: O(k n d), best: Θ(n d)}
  space: {extra: Θ(n d)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1996
  people: [Robert Tibshirani, Bradley Efron, Trevor Hastie, Jerome Friedman]
  note: Tibshirani proposed the lasso in 1996. LARS (2004) gave the whole path, and pathwise coordinate descent (glmnet, 2007 to 2010) became the standard solver.
prereqs: [ordinary-least-squares, regularization, coordinate-descent, subgradient]
see_also: [ridge-regression, elastic-net, proximal-operator, proximal-gradient-method, fista, kkt-conditions, cross-validation, quadratic-programming]
sources:
  - paper: doi:10.1111/j.2517-6161.1996.tb02080.x
    title: Robert Tibshirani, Regression shrinkage and selection via the lasso, Journal of the Royal Statistical Society Series B 58(1), 267 to 288, 1996
    locator: Section 2 (the definition as a constrained problem, the orthonormal case and the geometry) and Section 6 (the quadratic programming algorithm)
  - paper: doi:10.18637/jss.v033.i01
    title: Jerome Friedman, Trevor Hastie and Robert Tibshirani, Regularization paths for generalized linear models via coordinate descent, Journal of Statistical Software 33(1), 1 to 22, 2010
    locator: Section 2.1 (the coordinate update with soft thresholding and the scaling 1/(2N)), Section 2.2 (covariance updates) and Section 2.5 (the path with warm starts from λ_max)
  - paper: doi:10.1214/009053604000000067
    title: Bradley Efron, Trevor Hastie, Iain Johnstone and Robert Tibshirani, Least angle regression, Annals of Statistics 32(2), 407 to 499, 2004
    locator: Section 2 (the LARS algorithm), Section 3.1 (the lasso modification) and Theorem 1 (LARS with the modification gives the lasso path)
  - paper: doi:10.1214/13-EJS815
    title: Ryan J. Tibshirani, The lasso problem and uniqueness, Electronic Journal of Statistics 7, 1456 to 1490, 2013
    locator: Section 2 (Lemma 1, the fit and the L1 norm are unique, and Lemma 2, general position gives a unique solution with at most min(n, p) nonzero entries)
  - paper: doi:10.1023/A:1017501703105
    title: Paul Tseng, Convergence of a block coordinate descent method for nondifferentiable minimization, Journal of Optimization Theory and Applications 109(3), 475 to 494, 2001
    locator: Theorem 4.1 (convergence of cyclic coordinate descent for a smooth function plus a separable convex function)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 3.4.2 (the lasso), Section 3.4.4 (least angle regression) and Section 3.8.6 (pathwise coordinate optimization)
---

The lasso fits a [linear regression](/linear-regression/) by minimizing the squared error plus $\lambda\|w\|_1$, a penalty on the sum of the absolute values of the weights. Unlike the squared penalty of [ridge regression](/ridge-regression/), the absolute value has a corner at 0, so for a large enough $\lambda$ many weights are exactly zero, and the lasso selects features while it fits. Tibshirani (1996) introduced it. The problem is convex but not smooth. The standard solver is cyclic [coordinate descent](/coordinate-descent/), where each step is a soft thresholding of one weight in $O(n)$ time. LARS computes the whole path of solutions as $\lambda$ changes.

## In plain words

You want weights for a linear prediction, as in least squares, and you also want most of the weights to be zero, so that the model uses only a few inputs. The lasso adds a cost equal to the sum of the sizes of the weights. A weight whose input helps the fit less than this cost stays at zero.

The usual solver changes one weight at a time. For that weight, it measures how much its input agrees with what the model still gets wrong. If the agreement is weaker than the cost, the weight becomes zero. If it is stronger, the weight moves by the amount of agreement that is left after the cost is subtracted. The solver goes over all the weights again and again, until no weight changes.

## The problem

The data are $X \in \mathbb{R}^{n \times d}$ with columns $x_j$ and $y \in \mathbb{R}^n$. This page uses the scaling of glmnet (Friedman, Hastie and Tibshirani 2010). For $\lambda \ge 0$, find

$$(\hat w, \hat b) = \arg\min_{w,\, b} \; F(w, b) = \frac{1}{2n}\|y - Xw - b\mathbf{1}\|_2^2 + \lambda\|w\|_1 .$$

Other texts minimize $\frac{1}{2}\|y - Xw\|^2 + \lambda\|w\|_1$, which is the same problem with $n\lambda$ in place of $\lambda$. Tibshirani (1996) wrote the equivalent constrained form: minimize $\|y - Xw\|^2$ subject to $\|w\|_1 \le t$. Each $t$ matches some $\lambda$.

The intercept $b$ is not penalized. As for ridge, for a fixed $w$ the best $b$ is $\bar y - \bar x^\top w$, and the problem in $w$ is the lasso on the centered data $X_c$ and $y_c$. From here on, $X$ and $y$ are centered and $b$ is left out.

**Optimality (the KKT conditions).** $F$ is convex, so $w$ is a minimizer exactly when $0$ is in its [subdifferential](/subgradient/). With $r = y - Xw$ this reads, for each $j$,

$$\frac{1}{n}x_j^\top r = \lambda\,\operatorname{sign}(w_j) \text{ if } w_j \ne 0, \qquad \left|\frac{1}{n}x_j^\top r\right| \le \lambda \text{ if } w_j = 0 .$$

So each feature in the model has a correlation with the residual of size exactly $\lambda$, with the sign of its weight, and each feature outside has a correlation of size at most $\lambda$. In the scaling $\frac12\|y - Xw\|^2 + \lambda\|w\|_1$ the conditions are $|x_j^\top(y - Xw)| \le \lambda$, with equality on the support. If $\lambda \ge \lambda_{\max} = \max_j |x_j^\top y|/n$, then $w = 0$ satisfies them, so $\hat w = 0$.

## The algorithm

Fix all the weights except $w_j$. As a function of $w_j$ alone, $F$ is $\frac{a_j}{2}w_j^2 - \rho_j w_j + \lambda|w_j|$ plus a constant, with $a_j = \|x_j\|^2/n$ and $\rho_j = \frac{1}{n}x_j^\top r_{(j)}$, where $r_{(j)} = r + x_j w_j$ is the residual without feature $j$. The minimizer of this one-dimensional function is

$$w_j = \frac{S(\rho_j, \lambda)}{a_j}, \qquad S(z, t) = \operatorname{sign}(z)\max(|z| - t, 0),$$

the soft thresholding operator, which is the [proximal operator](/proximal-operator/) of $t|\cdot|$. Cyclic coordinate descent applies this update to $j = 1, \dots, d$ in turn and repeats.

```pseudo id=main
LASSO-CD(X, y, λ, tol)
L1  x̄ ← the column means of X;  ȳ ← the mean of y;  center X and y
L2  a_j ← ‖x_j‖² / n for each j;  w ← 0;  r ← y
L3  repeat
L4      for j ← 1 to d with a_j > 0 do
L5          ρ ← x_jᵀ r / n + a_j w_j
L6          w_new ← S(ρ, λ) / a_j
L7          r ← r − x_j (w_new − w_j);  w_j ← w_new
L8  until no weight moved by more than tol in the last sweep
L9  b ← ȳ − x̄ᵀ w
L10 return (w, b)
```

Line L5 computes $\rho_j$ from the full residual: $x_j^\top r_{(j)}/n = x_j^\top r/n + a_j w_j$. Line L7 keeps $r$ up to date in $O(n)$, so one sweep costs $O(nd)$. A zero column has $a_j = 0$ and its weight stays 0. glmnet adds three things to this loop: a path of decreasing $\lambda$ from $\lambda_{\max}$ with warm starts, sweeps over only the active set until it stops changing, and the covariance form that keeps $x_j^\top x_k$ for the active features.

## Example

Take $n = 6$ examples with two features that are strongly correlated:

| $x_1$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $x_2$ | 2 | 1 | 4 | 3 | 6 | 5 |
| $y$ | 1 | 3 | 2 | 5 | 4 | 9 |

After centering, $a_1 = a_2 = 35/12 = 2.9167$, $x_1^\top x_2/n = 29/12 = 2.4167$ (correlation 0.83), $x_1^\top y/n = 23/6 = 3.8333$ and $x_2^\top y/n = 13/6 = 2.1667$. So $\lambda_{\max} = 23/6$.

**Coordinate descent with $\lambda = 1$.**

| sweep | $j$ | $\rho$ | $S(\rho, 1)$ | new $w$ |
|---|---|---|---|---|
| 1 | 1 | $23/6 = 3.8333$ | $2.8333$ | $(34/35, 0) = (0.9714, 0)$ |
| 1 | 2 | $13/6 - (29/12)(34/35) = -0.1810$ | 0 | $(0.9714, 0)$ |
| 2 | 1 | $3.8333$ | $2.8333$ | no change |
| 2 | 2 | $-0.1810$ | 0 | no change |

The second sweep changes nothing, so line L8 stops, and line L9 gives $b = 4 - 3.5 \cdot 34/35 = 0.6$. Check the KKT conditions: $x_1^\top r/n = 23/6 - (35/12)(34/35) = 1 = \lambda$ with $w_1 > 0$, and $|x_2^\top r/n| = 0.1810 \le 1$ with $w_2 = 0$. The lasso keeps only $x_1$.

**The path.** OLS ($\lambda = 0$) gives $w = (107/48, -53/48) = (2.229, -1.104)$, with a negative weight on $x_2$ that partly cancels $x_1$. As $\lambda$ grows, both weights move linearly: at $\lambda = 1/2$, $w = (59/48, -5/48)$. At $\lambda = 53/96 = 0.552$ the weight $w_2$ reaches 0 and leaves. For $0.552 \le \lambda \le 23/6$, $w = ((23/6 - \lambda)\cdot 12/35, 0)$, and for $\lambda \ge 23/6$, $w = 0$ and $b = \bar y = 4$. For $\lambda = 1/2$ coordinate descent needs many sweeps, because the two features are correlated and each update undoes part of the other.

## Correctness

Each update of line L6 is the exact minimizer of $F$ in one coordinate, so $F$ never increases. Since $F$ is strongly convex in each coordinate with $a_j > 0$, each update lowers $F$ by at least $\frac{a_j}{2}(\Delta w_j)^2$. So the sum of the squared movements is finite, the movements go to 0, and line L8 stops. At any limit point no coordinate can move, which is the KKT conditions above, and for a convex $F$ these mean a global minimum. This argument is Tseng's theorem (2001) for a smooth function plus a separable convex function. The proof below gives it in full.

## Complexity

On a [real RAM](/real-ram/), with $k$ sweeps:

- **One sweep** costs $\Theta(nd)$: $d$ inner products of length $n$ in line L5 and $d$ residual updates in line L7. Centering is $\Theta(nd)$. So the time is $O(knd)$, and $\Theta(nd)$ at best, when one sweep already finds the solution, as for $\lambda \ge \lambda_{\max}$.
- **The number of sweeps** depends on the conditioning of the active features. For strongly convex problems cyclic coordinate descent converges linearly. With warm starts along a path of $\lambda$ values, few sweeps are needed for each $\lambda$.
- **Covariance updates.** If the active set has $m$ features, keeping $x_j^\top x_k$ for them makes a sweep cost $O(dm)$ after an $O(nm)$ setup for each new feature (Friedman, Hastie and Tibshirani 2010, Section 2.2).
- **LARS** computes the whole piecewise linear path. When $d < n$ and no variable leaves, it takes $d$ steps and has the cost of one OLS fit, $O(nd^2 + d^3)$ (Efron et al. 2004).
- **Memory.** $\Theta(nd)$ for the centered copy of $X$, and $\Theta(n + d)$ for $r$, $a$ and $w$.

## Properties

### Sparsity and the orthonormal case

If the columns are orthogonal with $x_j^\top x_j/n = 1$, the coordinates do not interact, one sweep is enough, and $\hat w_j = S(\hat w_j^{\text{OLS}}, \lambda)$. Small OLS weights become exactly 0 and large ones move toward 0 by $\lambda$. Ridge, in the same case, divides all of them by the same factor larger than 1 and makes none zero. In general, the corner of the L1 ball at the axes is what puts the solution on a face with zeros.

### Uniqueness (Tibshirani 2013)

- The fitted values $X\hat w$ are the same for all solutions, and so is $\|\hat w\|_1$ when $\lambda > 0$. The proof: $F$ is strictly convex in $Xw$, so two solutions with different fits would give a better midpoint.
- The set $E = \{j : |x_j^\top(y - X\hat w)|/n = \lambda\}$ is therefore the same for all solutions. If the columns $x_j$, $j \in E$, are linearly independent, the solution is unique.
- If the columns of $X$ are in general position (for example, if their entries come from a continuous distribution), the solution is unique for every $\lambda > 0$ and has at most $\min(n, d)$ nonzero weights.
- The solution can be non-unique. With two equal columns, any split of the weight between them with the same sign is optimal.

### Other properties

- **Piecewise linear path.** As $\lambda$ falls from $\lambda_{\max}$ to 0, $\hat w(\lambda)$ is continuous and piecewise linear, with knots where a feature enters or leaves. Within a piece, $\hat w_E = (X_E^\top X_E)^{-1}(X_E^\top y - n\lambda s_E)$ for the signs $s_E$.
- **Bayesian view.** The lasso is the [maximum a posteriori estimate](/maximum-a-posteriori-estimation/) with independent Laplace priors on the weights.
- **Not scale equivariant.** As for ridge, standardize the features first.
- **Biased large weights.** Each weight in the model is shrunk by about $\lambda$, also when it is large and clearly needed.

## Variants and improvements

- **[Elastic net](/elastic-net/).** Adds $\frac{\lambda_2}{2}\|w\|^2$ to the penalty, which keeps groups of correlated features together and makes the solution unique.
- **LARS and homotopy.** Least angle regression with the lasso modification (Efron et al. 2004) and the homotopy method of Osborne, Presnell and Turlach (2000) follow the path exactly.
- **[Proximal gradient](/proximal-gradient-method/) (ISTA) and [FISTA](/fista/).** Update all weights at once with $w \leftarrow S(w + \eta X^\top r/n, \eta\lambda)$. They suit problems where $X$ is given only as a fast operator.
- **[Quadratic programming](/quadratic-programming/).** Split $w = w^+ - w^-$ with $w^\pm \ge 0$. Tibshirani (1996) solved the constrained form this way.
- **Screening rules.** Strong rules and safe rules remove features that must have weight 0 before the sweeps.
- **Adaptive lasso, group lasso, relaxed lasso.** Weighted penalties to fix the bias, penalties on groups of weights, and an OLS refit on the selected features.
- **L1-penalized GLMs.** The same coordinate descent, inside an IRLS loop, fits the lasso for [logistic regression](/logistic-regression/) and other [GLMs](/generalized-linear-model/).

## When to use it

Use the lasso when you believe that only a few features matter, when you want a model that is easy to read, or when $d$ is larger than $n$. Choose $\lambda$ by [cross-validation](/cross-validation/) along the path from $\lambda_{\max}$ down. If the features come in groups of strongly correlated ones and you want to keep whole groups, use the elastic net. If all features matter a little, ridge usually predicts better.

## Pitfalls

- **Mixed scalings.** Some libraries use $\frac{1}{2n}\|\cdot\|^2$, some $\frac12\|\cdot\|^2$, some $\|\cdot\|^2$. The same $\lambda$ then means a penalty that differs by a factor $n$ or 2.
- **Penalizing the intercept.** Center the data, as in lines L1 and L9.
- **Unscaled features.** The L1 penalty is not invariant to the units of the features. Standardize them first.
- **Unstable selection.** Among strongly correlated features, the lasso picks one more or less at random. Small changes of the data can change which one.
- **Stopping too early.** With correlated features, coordinate descent can need many sweeps, as in the example with $\lambda = 1/2$. Check the KKT conditions or the duality gap, not only a fixed number of sweeps.
- **Reading weights as effects.** The weights are biased toward 0, and the selected set is chosen from the data. Classical confidence intervals do not hold for them.

## Implementations

## History

Tibshirani (1996) proposed the lasso, built on the nonnegative garrote of Breiman (1995). The same problem appeared in signal processing as basis pursuit denoising (Chen, Donoho and Saunders, 1998). Osborne, Presnell and Turlach (2000) gave a homotopy algorithm and the dual problem. Efron, Hastie, Johnstone and Tibshirani (2004) gave least angle regression, which computes the whole path. Fu (1998) had already proposed coordinate descent with shooting, and Friedman, Hastie, Hoefling and Tibshirani (2007) and Friedman, Hastie and Tibshirani (2010) made pathwise coordinate descent the standard method in glmnet. Tibshirani (2013) settled when the solution is unique.

## References
