---
tag: 29H0AF
kind: algorithm
slug: ridge-regression
name: Ridge regression
aliases:
- L2-regularized regression
- ridge estimator
area: machine-learning/supervised-learning
level: core
summary: Least squares with a penalty λ||w||^2. Solve (X^T X + λI) w = X^T y on centered data; each singular direction shrinks by σ^2/(σ^2 + λ).
solves: [linear-regression]
model: real-ram
complexity:
  vars: {n: the number of examples, d: the number of features}
  time: {worst: Θ(n d^2 + d^3), best: Θ(n d^2 + d^3)}
  space: {extra: Θ(n d + d^2)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1970
  people: [Arthur E. Hoerl, Robert W. Kennard, Andrey Tikhonov]
  note: Hoerl and Kennard named ridge regression in 1970 for nearly collinear predictors. Tikhonov had used the same penalty for ill-posed problems in 1963.
prereqs: [ordinary-least-squares, regularization, singular-value-decomposition]
see_also: [lasso-regression, elastic-net, kernel-ridge-regression, tikhonov-regularization, bias-variance-tradeoff, maximum-a-posteriori-estimation, cholesky-decomposition, cross-validation]
sources:
  - paper: doi:10.1080/00401706.1970.10488634
    title: Arthur E. Hoerl and Robert W. Kennard, Ridge regression, biased estimation for nonorthogonal problems, Technometrics 12(1), 55 to 67, 1970
    locator: Section 2 (the ridge estimator and the ridge trace) and Section 4 (the mean squared error and the existence of a better λ > 0)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 3.4.1 (ridge regression, centering, the SVD shrinkage and the effective degrees of freedom)
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 3.1.4 (regularized least squares) and Section 6.1 (the dual representation)
  - paper: doi:10.1080/00401706.1979.10489751
    title: Gene H. Golub, Michael Heath and Grace Wahba, Generalized cross-validation as a method for choosing a good ridge parameter, Technometrics 21(2), 215 to 223, 1979
    locator: Sections 1 and 2 (the GCV choice of λ with the trace of the hat matrix)
---

Ridge regression fits a [linear regression](/linear-regression/) by minimizing the sum of squared residuals plus $\lambda\|w\|_2^2$, a penalty on the size of the weights. For each $\lambda > 0$ the problem has one solution, $\hat w = (X^\top X + \lambda I)^{-1}X^\top y$ on centered data, even when [OLS](/ordinary-least-squares/) has none or many. The penalty shrinks the fit along each singular direction of $X$ by the factor $\sigma_i^2/(\sigma_i^2 + \lambda)$, so the directions with small singular values shrink most. Hoerl and Kennard (1970) introduced it for nearly collinear predictors, and showed that some $\lambda > 0$ always has a smaller mean squared error than OLS.

## In plain words

Ordinary least squares picks the weights that fit the data best. When two inputs carry almost the same information, these weights can become very large, with opposite signs that cancel. A small change in the data then changes them a lot.

Ridge regression adds a cost for large weights. It looks for weights that fit the data well and also stay small. One number sets the balance between the two goals. With a cost of zero you get least squares again. With a very large cost all the weights go to zero. In between, the weights are a little wrong on average, but they change much less from one data set to the next. Often the predictions get better on new data. The constant term is not part of the cost, so that moving all the outputs up by the same amount does not change the weights.

## The problem

The data are $X \in \mathbb{R}^{n \times d}$ with rows $x_i^\top$ and $y \in \mathbb{R}^n$. For a penalty $\lambda \ge 0$, find

$$(\hat w, \hat b) = \arg\min_{w \in \mathbb{R}^d,\, b \in \mathbb{R}} \; \|y - Xw - b\mathbf{1}\|_2^2 + \lambda\|w\|_2^2 .$$

This page uses this scaling, with no factor $1/n$, as in ESL Section 3.4.1. With the loss $\frac{1}{n}\|\cdot\|^2$ the same solution comes from $n\lambda$ in place of $\lambda$.

**The intercept is not penalized.** A penalty on $b$ would make the fit depend on where the origin of $y$ is. Instead, minimize over $b$ first. For a fixed $w$, the best $b$ is $\bar y - \bar x^\top w$, where $\bar x$ and $\bar y$ are the means of the columns and of $y$. Substitute it back: the problem becomes ridge without intercept on the centered data $X_c = X - \mathbf{1}\bar x^\top$ and $y_c = y - \bar y\mathbf{1}$. Its gradient is $-2X_c^\top(y_c - X_c w) + 2\lambda w$, which is zero exactly when

$$(X_c^\top X_c + \lambda I)\, w = X_c^\top y_c .$$

For $\lambda > 0$ the matrix is [positive definite](/positive-definite-matrix/), because $u^\top(X_c^\top X_c + \lambda I)u = \|X_c u\|^2 + \lambda\|u\|^2 > 0$ for $u \ne 0$. So the solution is unique for each $X$, also when $d > n$ or columns are equal.

## The algorithm

The primal method centers the data, forms the $d \times d$ system and solves it by [Cholesky](/cholesky-decomposition/).

```pseudo id=main
RIDGE(X, y, λ)                              ▷ λ > 0, or λ = 0 with X_c of rank d
L1  x̄ ← the column means of X;  ȳ ← the mean of y
L2  X_c ← X − 𝟏 x̄ᵀ;  y_c ← y − ȳ 𝟏
L3  G ← X_cᵀ X_c + λ I
L4  h ← X_cᵀ y_c
L5  L ← the Cholesky factor of G, so G = L Lᵀ
L6  solve L z = h by forward substitution
L7  solve Lᵀ w = z by back substitution
L8  b ← ȳ − x̄ᵀ w
L9  return (w, b)
```

Lines L1 and L2 remove the intercept from the problem. Line L3 adds $\lambda$ to the diagonal, and this is the only change from the normal equations of OLS. Lines L5 to L7 solve $Gw = h$. Line L8 puts back the intercept. The positive $\lambda$ improves the conditioning: the condition number of $G$ is $(\sigma_1^2 + \lambda)/(\sigma_d^2 + \lambda)$, which is at most $1 + \sigma_1^2/\lambda$. So the normal equations are much safer here than for OLS. For a fully stable method, run [Householder QR](/ordinary-least-squares/) on the stacked problem $\binom{X_c}{\sqrt\lambda I} w \approx \binom{y_c}{0}$, which has the same solution.

**The SVD form.** Let $X_c = U\Sigma V^\top$ be a thin [singular value decomposition](/singular-value-decomposition/) with singular values $\sigma_1 \ge \dots \ge \sigma_r > 0$. Then

$$\hat w = \sum_{i=1}^{r} \frac{\sigma_i}{\sigma_i^2 + \lambda}\, v_i\, u_i^\top y_c, \qquad X_c\hat w = \sum_{i=1}^{r} \frac{\sigma_i^2}{\sigma_i^2 + \lambda}\, u_i\, u_i^\top y_c .$$

OLS projects $y_c$ onto each direction $u_i$ and keeps the whole projection. Ridge keeps the fraction $\sigma_i^2/(\sigma_i^2 + \lambda)$. One SVD gives the solution for all values of $\lambda$ at once, which suits the search for a good $\lambda$.

**The dual form.** The identity $(X_c^\top X_c + \lambda I)X_c^\top = X_c^\top(X_c X_c^\top + \lambda I)$ gives

$$\hat w = X_c^\top \alpha, \qquad \alpha = (X_c X_c^\top + \lambda I)^{-1} y_c .$$

This needs an $n \times n$ solve, in $O(n^2 d + n^3)$ time, which is cheaper when $d > n$. The data enter only through the inner products $x_i^\top x_k$, so they can be replaced by a kernel. That is [kernel ridge regression](/kernel-ridge-regression/).

## Example

Fit $y \approx b + wx$ to the points $(1, 1), (2, 3), (3, 2), (4, 5), (5, 4), (6, 9)$. Line L1 gives $\bar x = 3.5$ and $\bar y = 4$. With the centered data, $X_c^\top X_c = \sum (x_i - 3.5)^2 = 17.5$ and $X_c^\top y_c = 23$. So line L3 gives $G = 17.5 + \lambda$, lines L5 to L7 give $w = 23/(17.5 + \lambda)$, and line L8 gives $b = 4 - 3.5w$.

| $\lambda$ | $w$ | $b$ | shrinkage $\sigma^2/(\sigma^2 + \lambda)$ | effective degrees of freedom |
|---|---|---|---|---|
| 0 (OLS) | $46/35 = 1.3143$ | $-0.6$ | 1 | 2 |
| 3.5 | $23/21 = 1.0952$ | $1/6 = 0.1667$ | $5/6$ | $1 + 5/6 = 1.8333$ |
| 17.5 | $23/35 = 0.6571$ | $1.7$ | $1/2$ | $1.5$ |
| $\to \infty$ | 0 | 4 | 0 | 1 |

The slope shrinks to 0 and the line turns about the point of means $(3.5, 4)$, which every fit passes through. The intercept never shrinks: for large $\lambda$ the fit is the mean of $y$, not 0.

## Correctness

Minimizing over $b$ for a fixed $w$ gives $b = \bar y - \bar x^\top w$, and the remaining problem in $w$ is ridge on the centered data. That problem is a strictly convex quadratic when $\lambda > 0$ (or when $X_c$ has rank $d$), so its only minimizer solves $Gw = h$. Cholesky exists for each positive definite $G$, and the two triangular solves give $G^{-1}h$. The proof below gives the details.

## Complexity

On a [real RAM](/real-ram/):

- **Primal (lines L1 to L9).** Centering is $O(nd)$. Forming $X_c^\top X_c$ takes $nd^2$ flops (with symmetry) and $X_c^\top y_c$ takes $2nd$. Cholesky takes $d^3/3$ flops and the two triangular solves $2d^2$. In total $\Theta(nd^2 + d^3)$ time and $\Theta(nd + d^2)$ extra memory for $X_c$, $G$ and $L$. Without the copy $X_c$ (center on the fly) the extra memory is $\Theta(d^2)$.
- **Dual.** $\Theta(n^2 d + n^3)$ time and $\Theta(n^2)$ memory, better when $d > n$.
- **SVD.** $O(nd\min(n, d))$ once, then $O(nd)$ for each further $\lambda$.

## Properties

### Effective degrees of freedom

The fitted values are a linear function of $y$: $\hat y = H_\lambda y$ with $H_\lambda = \frac{1}{n}\mathbf{1}\mathbf{1}^\top + X_c(X_c^\top X_c + \lambda I)^{-1}X_c^\top$. The effective degrees of freedom are its trace,

$$\operatorname{df}(\lambda) = \operatorname{tr} H_\lambda = 1 + \sum_{i=1}^{r} \frac{\sigma_i^2}{\sigma_i^2 + \lambda},$$

where the 1 counts the intercept (ESL Section 3.4.1 counts only the sum, for centered data). It falls from $1 + r$ at $\lambda = 0$ to 1 as $\lambda \to \infty$. It replaces the number of parameters in formulas such as generalized cross-validation, $\operatorname{GCV}(\lambda) = \frac{1}{n}\|y - \hat y\|^2 / (1 - \operatorname{df}(\lambda)/n)^2$ (Golub, Heath and Wahba 1979).

### Bias, variance and the Hoerl-Kennard theorem

Assume $y = b\mathbf{1} + X\beta + \varepsilon$ with $\mathbb{E}\varepsilon = 0$, $\operatorname{Cov}\varepsilon = \sigma^2 I$, and $X_c$ of rank $d$ with eigenvalues $e_i = \sigma_i^2$ of $X_c^\top X_c$. Let $\gamma = V^\top\beta$ be the coefficients in the eigenbasis. Then ridge is biased, $\mathbb{E}\hat w - \beta = -\lambda(X_c^\top X_c + \lambda I)^{-1}\beta$, and its total mean squared error is

$$\operatorname{MSE}(\lambda) = \mathbb{E}\|\hat w - \beta\|^2 = \sigma^2\sum_{i=1}^{d} \frac{e_i}{(e_i + \lambda)^2} + \lambda^2 \sum_{i=1}^{d} \frac{\gamma_i^2}{(e_i + \lambda)^2} .$$

The variance term falls and the squared bias term grows with $\lambda$. At $\lambda = 0$, the derivative of the first sum is $-2\sigma^2\sum_i 1/e_i^2 < 0$ and the derivative of the second is 0. So $\operatorname{MSE}(\lambda) < \operatorname{MSE}(0)$ for all small $\lambda > 0$: some ridge estimator beats OLS in mean squared error (Hoerl and Kennard 1970, Section 4). This does not contradict Gauss-Markov, which compares only unbiased estimators. The best $\lambda$ depends on the unknown $\beta$ and $\sigma^2$, so in practice it is chosen by [cross-validation](/cross-validation/) or GCV.

### The Bayesian view

If $\varepsilon \sim \mathcal{N}(0, \sigma^2 I)$ and the prior is $\beta \sim \mathcal{N}(0, (\sigma^2/\lambda) I)$, with a flat prior on $b$, then the posterior mode and mean of $\beta$ are the ridge estimate. So ridge is a [maximum a posteriori estimate](/maximum-a-posteriori-estimation/) with a Gaussian prior, and $\lambda$ is the ratio of the noise variance to the prior variance.

### Other properties

- **Not scale equivariant.** The penalty treats all weights in the same way, so multiplying a feature by 10 changes the fit. Standardize the columns first, unless their units are comparable.
- **No sparsity.** Each $\hat w_j$ shrinks, but none becomes exactly 0 for finite $\lambda$, in general. For exact zeros, use the [lasso](/lasso-regression/).
- **Equal columns share the weight.** If two columns are equal, their weights are equal, because the penalty $w_1^2 + w_2^2$ with a fixed sum $w_1 + w_2$ is smallest when they are equal.

## Variants and improvements

- **Generalized ridge.** A penalty $w^\top \Lambda w$ with a diagonal or general positive definite $\Lambda$, or $\|\Gamma w\|^2$ for a smoothness operator $\Gamma$. This is the [Tikhonov regularization](/tikhonov-regularization/) of numerical analysis.
- **Stacked QR.** Householder QR on $\binom{X_c}{\sqrt{\lambda}I}$, for full backward stability.
- **Iterative solvers.** Conjugate gradient on $(X_c^\top X_c + \lambda I)w = X_c^\top y_c$ converges in a number of steps that depends on $\sqrt{1 + \sigma_1^2/\lambda}$, and suits large sparse $X$.
- **[Kernel ridge regression](/kernel-ridge-regression/).** The dual form with a kernel matrix in place of $X_c X_c^\top$.
- **[Elastic net](/elastic-net/).** Adds an L1 penalty to get sparsity and keep the grouping of correlated features.
- **Ridge for classification.** An L2 penalty on [logistic regression](/logistic-regression/) uses the same idea and also makes the estimate finite on separable data.

## When to use it

Use ridge when the features are many or nearly collinear, when $d$ is close to $n$ or larger, and you want all the features to stay in the model with stable weights. It is the default first step past OLS for prediction. It has a closed form, the full path in $\lambda$ costs one SVD, and leave-one-out cross-validation has a closed form too. If you expect that only a few features matter, use the lasso or the elastic net.

## Pitfalls

- **Penalizing the intercept.** If you add a column of ones to $X$ and penalize it like the others, the fit depends on the origin of $y$. Center as in lines L1 and L2, or leave that column out of the penalty.
- **Unscaled features.** The penalty is not invariant to the units of the features. Standardize the columns, and transform the weights back after the fit.
- **Different scalings of $\lambda$.** Some libraries minimize $\frac{1}{2n}\|y - Xw\|^2 + \frac{\lambda}{2}\|w\|^2$, others $\|y - Xw\|^2 + \lambda\|w\|^2$. The same number then means different penalties, by a factor $n$.
- **Choosing $\lambda$ on the training error.** The training error always falls as $\lambda \to 0$. Choose $\lambda$ by cross-validation or GCV.
- **Explicit inverse.** Use a Cholesky solve, not $(X_c^\top X_c + \lambda I)^{-1}$.

## Implementations

## History

Tikhonov (1963) used a quadratic penalty to make ill-posed integral equations stable, and the same idea appears in Phillips (1962). Hoerl (1962) and then Hoerl and Kennard (1970) brought it into statistics as ridge regression, named for the ridge analysis of response surfaces. They proposed the ridge trace, a plot of $\hat w(\lambda)$, to choose $\lambda$, and proved that some $\lambda > 0$ has a smaller mean squared error than least squares. Golub, Heath and Wahba (1979) gave generalized cross-validation as a choice of $\lambda$ from the data.

## References
