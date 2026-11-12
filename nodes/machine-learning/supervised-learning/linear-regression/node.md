---
tag: NQNAPV
kind: problem
slug: linear-regression
name: Linear regression
aliases:
- least squares regression
- multiple linear regression
area: machine-learning/supervised-learning
level: intro
summary: "Fit a function that is linear in its parameters to real-valued targets, usually by least squares. The fit is the projection of the targets onto the column space of the data."
prereqs: [regression, least-squares-problem]
see_also: [ordinary-least-squares, ridge-regression, lasso-regression, generalized-linear-model, logistic-regression, qr-decomposition, sherman-morrison-formula, mean-squared-error]
sources:
  - book: isbn:9780387848570
    title: "Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, 2nd edition, Springer, 2009"
    locator: Section 3.2 (linear regression models and least squares, the hat matrix, the Gauss-Markov theorem) and Section 3.4 (shrinkage methods)
  - book: isbn:9781421407944
    title: "Gene H. Golub and Charles F. Van Loan, Matrix Computations, 4th edition, Johns Hopkins University Press, 2013"
    locator: Section 5.3 (the full rank least squares problem by normal equations and by QR, with flop counts) and Section 5.5 (the rank deficient problem and the minimum norm solution by the SVD)
  - paper: doi:10.1145/2488608.2488620
    title: "Kenneth L. Clarkson and David P. Woodruff, Low rank approximation and regression in input sparsity time, STOC 2013"
    locator: the (1 + epsilon) approximation of least squares regression in O(nnz(X)) time plus a polynomial in d and 1/epsilon
  - paper: doi:10.1080/01621459.1983.10477941
    title: "Leo Breiman and David Freedman, How many variables should be entered in a regression equation?, Journal of the American Statistical Association 78(381), 1983"
    locator: pp. 131-136, the prediction error of least squares with Gaussian random design
---

Linear regression is the problem of fitting a function that is linear in its parameters, $f(x) = w^\top x + b$, to examples $(x_i, y_i)$ with real targets. It is the case of [regression](/regression/) with the class of linear functions, and in almost all uses the loss is the squared loss, so the task is the [least squares problem](/least-squares-problem/) $\min_\beta\|X\beta - y\|^2$. Legendre published the method of least squares in 1805 and Gauss gave it a probabilistic basis in 1809. The fitted values are the orthogonal projection of $y$ onto the column space of $X$. The standard estimator is [ordinary least squares](/ordinary-least-squares/); [ridge](/ridge-regression/), [lasso](/lasso-regression/) and the [elastic net](/elastic-net/) add a penalty, and [generalized linear models](/generalized-linear-model/) change the noise model.

## In plain words

You have a table of examples. Each row has some input numbers and one output number. You want a weighted sum of the inputs, plus a constant, that comes as close as possible to the output in each row.

The usual way to measure "close" is to square each miss and add the squares. Then there is a formula for the best weights, and a computer finds them with a few standard matrix steps. The answer has a picture: the outputs are a point in a large space, all possible weighted sums of the inputs make a flat surface in that space, and the best fit is the point of that surface nearest to the outputs.

The inputs can be anything you can compute from the raw data, such as powers or products of the measurements, so a curve can also be a "linear" fit.

## Definition

**Notation.** There are $n$ examples and $d$ features. Write $X$ for the $n \times p$ design matrix whose row $i$ is the feature vector of example $i$. With an intercept, the first column of $X$ is all ones and $p = d + 1$, and $\beta = (b, w)$; without one, $p = d$ and $\beta = w$. The features may be any fixed functions of the raw input, such as $1, x, x^2$ for a quadratic fit: the model is linear in $\beta$, not necessarily in the input.

**The problem.** Given $X \in \mathbb{R}^{n \times p}$ and $y \in \mathbb{R}^n$, find
$$
\hat\beta \in \arg\min_{\beta \in \mathbb{R}^p} \sum_{i=1}^n (y_i - x_i^\top\beta)^2 = \arg\min_\beta \|y - X\beta\|^2.
$$
A minimizer always exists. The minimizers are exactly the solutions of the normal equations
$$
X^\top X\beta = X^\top y,
$$
because the objective is a convex quadratic with gradient $2X^\top(X\beta - y)$. The fitted vector $\hat y = X\hat\beta$ is the same for all of them: it is the orthogonal projection of $y$ onto the column space of $X$, and the residual $y - \hat y$ is orthogonal to every column. If $X$ has rank $p$, the minimizer is unique, $\hat\beta = (X^\top X)^{-1}X^\top y$. Otherwise the minimizers form an affine set of dimension $p - \operatorname{rank}X$, and the one of least norm is $X^+y$, with $X^+$ the pseudoinverse.

**The statistical model.** The data model of the site is the random design: $(x_i, y_i)$ i.i.d. from an unknown $D$, and the goal is the risk $\mathbb{E}(y - x^\top\beta)^2$. The least squares $\beta$ for $D$ is the best linear predictor even when $\mathbb{E}[y \mid x]$ is not linear. The classical linear model is the fixed design version, $y = X\beta + \varepsilon$ with $\mathbb{E}\varepsilon = 0$ and $\operatorname{Cov}\varepsilon = \sigma^2 I$. Under it the least squares estimator is unbiased and, by the Gauss-Markov theorem, has the least variance among linear unbiased estimators (proved on the [ordinary least squares](/ordinary-least-squares/) page). If in addition $\varepsilon$ is normal, least squares is the [maximum likelihood](/maximum-likelihood-estimation/) estimate, and $\hat\sigma^2 = \|y - \hat y\|^2/(n - p)$ is an unbiased estimate of $\sigma^2$.

## Variants

- **Weighted and generalized least squares.** Minimize $\sum_i \omega_i(y_i - x_i^\top\beta)^2$, or $(y - X\beta)^\top\Sigma^{-1}(y - X\beta)$ for correlated noise with covariance $\Sigma$.
- **Penalized least squares.** [Ridge regression](/ridge-regression/) adds $\lambda\|w\|^2$, [lasso regression](/lasso-regression/) adds $\lambda\|w\|_1$, and the [elastic net](/elastic-net/) adds both. They are needed when $p > n$ or $X$ is nearly rank deficient.
- **Other losses.** Least absolute deviations and [quantile regression](/quantile-regression/) use the absolute and the pinball loss; robust regression uses losses that grow slowly, such as the Huber loss.
- **Total least squares.** When the features also have errors, minimize the perpendicular distances instead of the vertical ones. The solution comes from the smallest singular vector of $[X \; y]$.
- **Bayesian linear regression.** A normal prior on $\beta$ and normal noise give a normal posterior, whose mean is the ridge estimate.
- **Multivariate regression.** The target is a vector in $\mathbb{R}^k$, and the problem splits into $k$ separate least squares problems with the same $X$.
- **Online and recursive least squares.** The examples arrive one at a time and the fit is updated after each one.
- **Other noise models.** [Generalized linear models](/generalized-linear-model/) keep the linear predictor and change the distribution of $y$; [logistic regression](/logistic-regression/) is the case of a binary $y$.

## Examples

**A line through three points.** Take $(1, 1)$, $(2, 3)$, $(3, 2)$ and fit $y \approx b + wx$. Then
$$
X = \begin{pmatrix}1 & 1\\ 1 & 2\\ 1 & 3\end{pmatrix}, \quad X^\top X = \begin{pmatrix}3 & 6\\ 6 & 14\end{pmatrix}, \quad X^\top y = \begin{pmatrix}6\\ 13\end{pmatrix}.
$$
The determinant of $X^\top X$ is $6$, so $b = (14 \cdot 6 - 6 \cdot 13)/6 = 1$ and $w = (3 \cdot 13 - 6 \cdot 6)/6 = \frac12$. The fitted values are $1.5, 2, 2.5$ and the residuals are $-0.5, 1, -0.5$. The residuals add up to 0 (orthogonal to the column of ones) and $1(-0.5) + 2(1) + 3(-0.5) = 0$ (orthogonal to the $x$ column). The residual sum of squares is $1.5$, the total sum of squares about the mean $2$ is $2$, so $R^2 = 1 - 1.5/2 = 0.25$, and $\hat\sigma^2 = 1.5/(3 - 2) = 1.5$.

**A rank deficient design.** Use the same $y$ with the two features $x$ and $2x$ and no intercept. Every $\beta$ with $\beta_1 + 2\beta_2 = c$ gives the fit $cx$, and the best $c$ is $\sum x_iy_i/\sum x_i^2 = 13/14$. So all $\beta$ on the line $\beta_1 + 2\beta_2 = \frac{13}{14}$ are minimizers. The one of least norm is parallel to $(1, 2)$: $\beta = \frac{13}{70}(1, 2)$. A program that solves the normal equations by Cholesky fails on this $X$; a QR with column pivoting or an SVD finds the least norm solution.

## Known algorithms

The costs are arithmetic operations for a dense $n \times p$ matrix with $n \ge p$.

| Method | Cost | Notes |
|---|---|---|
| Normal equations with [Cholesky](/cholesky-decomposition/) | $np^2 + p^3/3$ | fastest; the condition number of $X^\top X$ is $\kappa(X)^2$, so accuracy is lost when $X$ is ill-conditioned |
| Householder [QR](/qr-decomposition/) ([ordinary least squares](/ordinary-least-squares/)) | $2np^2 - \frac23p^3$ | backward stable; the standard method |
| SVD | about $2np^2 + 11p^3$ | handles rank deficiency and gives the least norm solution |
| [Conjugate gradient](/conjugate-gradient-method/) on the normal equations (CGLS, LSQR) | one product with $X$ and one with $X^\top$ per iteration | for large sparse $X$; the number of iterations grows with $\kappa(X)$ |
| [Stochastic gradient descent](/stochastic-gradient-descent/) (the LMS rule of Widrow and Hoff) | $O(p)$ per example | online; converges to the least squares fit only with decreasing steps or averaging |
| Recursive least squares with the [Sherman-Morrison formula](/sherman-morrison-formula/) | $O(p^2)$ per example | exact online updates of $(X^\top X)^{-1}$ |
| Random sketching (Clarkson and Woodruff 2013) | $O(\operatorname{nnz}(X))$ plus a polynomial in $p$ and $1/\epsilon$ | a $(1 + \epsilon)$ approximation of the least residual, with high probability |

## Bounds

**Computation.** An exact solution must read all of $X$, which takes $\Omega(np)$ time. The direct methods above take $O(np^2)$, which fast matrix multiplication lowers to $O(np^{\omega - 1})$. The sketching method of Clarkson and Woodruff finds a $(1 + \epsilon)$ approximation in time linear in the number of nonzero entries for fixed $p$ and $\epsilon$.

**Statistics, fixed design.** In the classical linear model with $X$ of rank $p$, the in-sample prediction risk of least squares is $\frac1n\mathbb{E}\|X\hat\beta - X\beta\|^2 = \sigma^2p/n$ (proved on the [regression](/regression/) page), and $\operatorname{Cov}\hat\beta = \sigma^2(X^\top X)^{-1}$.

**Statistics, random design.** If the rows $x_i$ are i.i.d. $N(0, \Sigma)$ with $\Sigma$ invertible, the noise is independent with variance $\sigma^2$, the model has no intercept and $n > p + 1$, then the expected excess risk of least squares on a new point is
$$
\mathbb{E}\bigl[(x^\top\hat\beta - x^\top\beta)^2\bigr] = \frac{\sigma^2 p}{n - p - 1},
$$
which blows up as $p$ approaches $n$ (Breiman and Freedman 1983). This is one reason for the penalized variants when $p$ is not small compared with $n$.

## Reductions

- **To the least squares problem.** Linear regression with squared loss is the [least squares problem](/least-squares-problem/) of numerical linear algebra. All its algorithms apply.
- **Weighted to ordinary.** Weighted least squares with weights $\omega_i$ is ordinary least squares on the rows $\sqrt{\omega_i}\,(x_i, y_i)$.
- **Ridge to ordinary.** Ridge regression is ordinary least squares on $X$ with the $p$ rows of $\sqrt\lambda I$ added and $y$ with $p$ zeros added (without an intercept).
- **Nonlinear features.** Polynomial, spline and other basis expansions turn a curved fit in $x$ into linear regression on the expanded features.
- **Generalized linear models.** IRLS fits a [generalized linear model](/generalized-linear-model/) as a sequence of weighted linear regressions, and [logistic regression](/logistic-regression/) is fitted the same way.
- **Kernel methods.** [Kernel ridge regression](/kernel-ridge-regression/) is ridge regression in a feature space given by a kernel.

## Applications

- Estimating the effect of one variable with others held fixed, in econometrics, epidemiology and the social sciences.
- Calibration lines in chemistry and physics, and the fit of laws that are linear after a transformation, such as power laws on a log scale.
- Baselines for prediction tasks, and the last layer of many neural networks.
- Forecasting with autoregressive models, whose coefficients are fitted by least squares on lagged values.
- Signal processing: adaptive filters (the LMS and RLS algorithms) and linear prediction.

## References
