---
tag: EBABAD
kind: algorithm
slug: kernel-ridge-regression
name: Kernel ridge regression
aliases:
- KRR
- dual ridge regression
- kernel regularized least squares
area: machine-learning/supervised-learning
level: advanced
summary: "Ridge regression in the feature space of a kernel. Solve (K + λI)α = y and predict f(x) = Σ α_i k(x_i, x). Training costs O(n^3), and each prediction costs n kernel values."
solves: [regression]
model: real-ram
complexity:
  vars: {n: the number of training points, t: the cost of one kernel evaluation}
  time: {worst: "Θ(n^2 t + n^3)", best: "Θ(n^2 t + n^3)"}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1998
  people: [Craig Saunders, Alexander Gammerman, Volodya Vovk]
  note: Kimeldorf and Wahba gave the kernel form of the penalized least squares solution in 1971. Saunders, Gammerman and Vovk presented ridge regression in dual variables with kernels in 1998.
prereqs: [ridge-regression, kernel-trick, representer-theorem, cholesky-decomposition]
see_also: [gaussian-process, support-vector-regression, ridge-regression, representer-theorem, mercer-theorem, support-vector-machine, kernel-pca, sherman-morrison-formula]
sources:
  - paper: "Craig Saunders, Alexander Gammerman and Volodya Vovk, Ridge regression learning algorithm in dual variables, Proceedings of the 15th International Conference on Machine Learning (ICML), 1998"
    locator: pp. 515 to 521 (the dual form α = (K + aI)^{-1} y and its use with kernels)
  - paper: doi:10.1016/0022-247X(71)90184-3
    title: George Kimeldorf and Grace Wahba, Some results on Tchebycheffian spline functions, Journal of Mathematical Analysis and Applications 33(1), 1971
    locator: pp. 82 to 95 (the penalized least squares solution as a combination of kernel functions)
  - book: isbn:9780521813976
    title: John Shawe-Taylor and Nello Cristianini, Kernel Methods for Pattern Analysis, Cambridge University Press, 2004
    locator: Chapter 2 (ridge regression in primal and dual form) and Chapter 7 (regression algorithms)
  - book: isbn:9780262182539
    title: Carl Edward Rasmussen and Christopher K. I. Williams, Gaussian Processes for Machine Learning, MIT Press, 2006
    locator: Chapter 2 (the predictive mean of Gaussian process regression) and Chapter 6 (the relation to regularization and kernel ridge regression)
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 6.1 (dual representations of regularized least squares)
---

Kernel ridge regression fits a function $f(x) = \sum_{i=1}^n \alpha_i k(x_i, x)$ to data $(x_i, y_i)$ by minimizing the squared error plus $\lambda$ times the squared norm of $f$ in the reproducing kernel Hilbert space of a kernel $k$. The coefficients solve one linear system, $(K + \lambda I)\alpha = y$, where $K$ is the Gram matrix. It is [ridge regression](/ridge-regression/) run in the feature space of $k$ by the [kernel trick](/kernel-trick/), and its prediction equals the posterior mean of [Gaussian process](/gaussian-process/) regression with covariance $k$ and noise variance $\lambda$.

## In plain words

Ridge regression fits a straight line or plane through data, and keeps the weights small so that the fit does not follow the noise. Kernel ridge regression does the same in a much larger space of features, such as all products of the inputs up to some degree, or infinitely many smooth features. It never builds those features. It only needs the kernel, which says how similar two inputs are.

The prediction at a new point is a weighted sum of its similarities to the training points. To find the weights, build the table of similarities between all pairs of training points, add a constant to its diagonal, and solve one system of linear equations. A larger constant gives a smoother, flatter fit.

## The problem

The input is a training set $(x_1, y_1), \ldots, (x_n, y_n)$ with $x_i$ in any set $X$ and $y_i \in \mathbb{R}$, a positive semidefinite kernel $k$ on $X$, and $\lambda > 0$. Let $\mathcal{H}$ be the reproducing kernel Hilbert space of $k$. The output is the function

$$\hat f = \operatorname*{arg\,min}_{f \in \mathcal{H}} \; \sum_{i=1}^{n} (f(x_i) - y_i)^2 + \lambda \lVert f \rVert_{\mathcal{H}}^2.$$

This page uses the plain sum of squared errors, as the [ridge regression](/ridge-regression/) page does. With the mean $\frac1n \sum_i (f(x_i) - y_i)^2$ instead, the same solution needs $n\lambda$ in place of $\lambda$, so the system becomes $(K + n\lambda I)\alpha = y$. There is no separate bias term: a constant can be included through the kernel, for example $k + c$ with $c > 0$, or by centering $y$ first.

## The algorithm

```pseudo id=main
KRR-FIT(x_1..n, y_1..n, k, λ)
L1  for i, j ← 1 to n do K[i][j] ← k(x_i, x_j)          ▷ the Gram matrix
L2  A ← K + λ I                                          ▷ positive definite for λ > 0
L3  L ← CHOLESKY(A)                                      ▷ A = L Lᵀ
L4  solve L u = y by forward substitution
L5  solve Lᵀ α = u by back substitution
L6  return α

KRR-PREDICT(α, x)
L7  return Σ_{i=1}^{n} α_i k(x_i, x)
```

Line L1 is the only place where the inputs are used during training. Line L2 adds $\lambda$ to the diagonal. Since $K$ is positive semidefinite, $A$ has all eigenvalues at least $\lambda > 0$, so the [Cholesky factorization](/cholesky-decomposition/) of line L3 exists and is numerically stable. Lines L4 and L5 solve $A\alpha = y$ without forming $A^{-1}$.

The residuals of the fit are $y - K\alpha = \lambda \alpha$, from line L2. So a point with a large $|\alpha_i|$ is a point that the fit does not reach.

## Example

Take the points $x = 0, 1, 2$ in $\mathbb{R}$ with $y = 0, 1, 0$, the kernel $k(x, z) = (xz + 1)^2$ and $\lambda = 1$. The Gram matrix and the system are

$$K = \begin{pmatrix} 1 & 1 & 1 \\ 1 & 4 & 9 \\ 1 & 9 & 25 \end{pmatrix}, \qquad \begin{pmatrix} 2 & 1 & 1 \\ 1 & 5 & 9 \\ 1 & 9 & 26 \end{pmatrix} \alpha = \begin{pmatrix} 0 \\ 1 \\ 0 \end{pmatrix},$$

with the exact solution $\alpha = (-\tfrac15, \tfrac35, -\tfrac15)$. The fitted function is

$$\hat f(x) = -\tfrac15 (1)^2 + \tfrac35 (x + 1)^2 - \tfrac15 (2x + 1)^2 = \tfrac15 + \tfrac25 x - \tfrac15 x^2.$$

Its values at the data are $\tfrac15, \tfrac25, \tfrac15$, and the residuals $y - \hat f = (-\tfrac15, \tfrac35, -\tfrac15)$ equal $\lambda \alpha$. At $x = 3/2$ the prediction is $7/20$.

In the explicit feature space $\varphi(x) = (1, \sqrt 2 x, x^2)$ of this kernel, the same function has the weights $w = \sum_i \alpha_i \varphi(x_i) = (\tfrac15, \tfrac{\sqrt 2}{5}, -\tfrac15)$, which is what ridge regression on the three features returns: $w = (\Phi^\top \Phi + I)^{-1} \Phi^\top y$.

## Correctness

By the [representer theorem](/representer-theorem/), every minimizer has the form $f = \sum_j \alpha_j k(x_j, \cdot)$. For such $f$, the values at the data are $K\alpha$ and $\lVert f \rVert^2 = \alpha^\top K \alpha$, so the objective is $\lVert K\alpha - y \rVert^2 + \lambda \alpha^\top K \alpha$. Its gradient is $2K((K + \lambda I)\alpha - y)$, which is 0 at $\alpha = (K + \lambda I)^{-1} y$. The objective is convex in $\alpha$, so this is a minimizer. The minimizing function is unique, because $\lambda \lVert f \rVert^2$ is strictly convex in $f$. The full proof is in the proofs folder.

**Equality with ridge in feature space.** Let $\varphi : X \to \mathbb{R}^D$ be a feature map with $k(x, z) = \varphi(x) \cdot \varphi(z)$, and $\Phi$ the $n \times D$ matrix with rows $\varphi(x_i)$, so $K = \Phi \Phi^\top$. Ridge regression on the features gives $w = (\Phi^\top \Phi + \lambda I_D)^{-1} \Phi^\top y$. The push-through identity $(\Phi^\top \Phi + \lambda I_D)^{-1} \Phi^\top = \Phi^\top (\Phi \Phi^\top + \lambda I_n)^{-1}$ follows from $\Phi^\top(\Phi\Phi^\top + \lambda I) = (\Phi^\top\Phi + \lambda I)\Phi^\top$. So $w = \Phi^\top \alpha$, and $w \cdot \varphi(x) = \sum_i \alpha_i k(x_i, x)$. The tests check this for the kernel $(x \cdot z + 1)^2$ on $\mathbb{R}^2$ against ridge on its 6 explicit features, for $n = 3$, 6 and 15 and three values of $\lambda$.

## Complexity

Let $t$ be the cost of one kernel evaluation, for example $\Theta(d)$ for a polynomial or Gaussian kernel on $\mathbb{R}^d$.

- **Training.** Line L1 costs $\Theta(n^2 t)$, and the Cholesky factorization costs $\Theta(n^3)$, about $n^3/3$ multiplications. The substitutions cost $\Theta(n^2)$. The memory is $\Theta(n^2)$ for $K$.
- **Prediction.** Each prediction costs $n$ kernel evaluations, $\Theta(n t)$, unlike the $\Theta(D)$ of a primal linear model.
- **Several values of $\lambda$.** One eigendecomposition $K = U \Lambda U^\top$ in $\Theta(n^3)$ gives $\alpha = U (\Lambda + \lambda I)^{-1} U^\top y$ for each new $\lambda$ in $\Theta(n^2)$.
- **Primal or dual.** With an explicit feature map of dimension $D$, primal ridge costs $\Theta(n D^2 + D^3)$. The dual form is cheaper when $D > n$, and it is the only option when $D$ is infinite.

## Properties

- **Closed form.** The solution is one linear system, with no iterations and no tuning of a step size.
- **Not sparse.** Usually every $\alpha_i \ne 0$, because $\alpha = (y - \hat f(x))/\lambda$ and the residuals are rarely exactly 0. [Support vector regression](/support-vector-regression/) gives sparse solutions with its $\varepsilon$-insensitive loss.
- **Linear smoother.** The fitted values are $\hat y = K(K + \lambda I)^{-1} y = S y$, linear in $y$. The effective number of parameters is $\operatorname{tr} S = \sum_j \mu_j/(\mu_j + \lambda)$ over the eigenvalues $\mu_j$ of $K$.
- **Fast leave-one-out.** The leave-one-out residual of point $i$ is $\alpha_i / [(K + \lambda I)^{-1}]_{ii}$, so one fit gives all $n$ of them. The tests check this against $n$ refits.
- **The Gaussian process connection.** With a prior $f \sim \mathcal{GP}(0, k)$ and noise $y_i = f(x_i) + \epsilon_i$, $\epsilon_i \sim \mathcal{N}(0, \sigma^2)$, the posterior mean is $k(x)^\top (K + \sigma^2 I)^{-1} y$, which is the KRR prediction with $\lambda = \sigma^2$. The Gaussian process also gives a posterior variance, which KRR does not.
- **Limits of $\lambda$.** As $\lambda \to \infty$, $\alpha \approx y/\lambda \to 0$. As $\lambda \to 0$ with a positive definite $K$, the fit interpolates the data.

## Variants and improvements

- **Low-rank approximations.** The Nyström method and random Fourier features replace $K$ by a rank $m$ approximation and cost $O(n m^2)$ to train.
- **Iterative solvers.** Conjugate gradients on $(K + \lambda I)\alpha = y$ need only products with $K$, at $O(n^2)$ each, and converge fast when $\lambda$ is not tiny relative to the spectrum of $K$.
- **Divide and conquer.** Fit KRR on $m$ disjoint parts of the data and average the predictions.
- **Smoothing splines.** The cubic smoothing spline is KRR with a particular kernel on an interval plus an unpenalized linear part. Its special structure gives an $O(n)$ solver with banded matrices.
- **Least squares SVM.** A variant with a bias term and equality constraints gives a slightly larger linear system of the same kind.
- **Kernel [logistic regression](/logistic-regression/).** It replaces the squared loss by the logistic loss and loses the closed form.

## When to use it

Use it for regression with a few thousand to a few tens of thousands of points, a good kernel, and the need for a simple and exact solver. It is a strong baseline for smooth targets with a Gaussian kernel. For large $n$, use a low-rank approximation or an iterative solver. For sparse solutions or robustness to outliers, use [support vector regression](/support-vector-regression/). For uncertainty estimates, use the [Gaussian process](/gaussian-process/) view.

## Pitfalls

- **The scaling of $\lambda$.** Libraries differ: some minimize the sum of squared errors and some the mean, which changes $\lambda$ by a factor of $n$. Some put the factor $\frac12$ on one term.
- **Forming $(K + \lambda I)^{-1}$.** Solving with a Cholesky factor is faster and more accurate than an explicit inverse.
- **Small $\lambda$ with a smooth kernel.** The Gaussian Gram matrix has eigenvalues that decay very fast, so $K + \lambda I$ is badly conditioned for tiny $\lambda$, and the coefficients become huge with opposite signs.
- **No intercept.** Without a constant in the kernel or a centered $y$, the fit is shrunk toward 0, not toward the mean of $y$.
- **Unscaled inputs.** A Gaussian kernel uses one bandwidth for all coordinates, so the features need comparable scales.
- **Memory.** $K$ for $n = 10^5$ points has $10^{10}$ entries, about 80 GB in double precision.

## Implementations

## History

Tikhonov (1963) and Hoerl and Kennard (1970) introduced the quadratic penalty. Kimeldorf and Wahba (1970, 1971) showed that the minimizer of a squared error plus a squared RKHS norm is a combination of kernel functions at the data, and linked it with the posterior mean of a Gaussian process. Saunders, Gammerman and Vovk (1998) presented ridge regression in dual variables as a kernel method for machine learning. The same estimator appears as kriging in geostatistics, as regularization networks, and as the least squares support vector machine without a bias.

## References
