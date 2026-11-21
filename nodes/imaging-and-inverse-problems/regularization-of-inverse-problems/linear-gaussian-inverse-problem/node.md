---
tag: Q5XXTM
kind: model
slug: linear-gaussian-inverse-problem
name: Linear Gaussian inverse problem
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: core
summary: "y = A x + e with a Gaussian prior on x and Gaussian noise. The posterior is Gaussian in closed form, and its mean is a Tikhonov solution weighted by the two covariances."
prereqs: [inverse-problem, bayes-theorem, tikhonov-regularization]
see_also: [bayesian-inverse-problem, maximum-a-posteriori-estimation, generalized-least-squares, kalman-filter, gaussian-process, kriging, resolution-matrix, optimal-experimental-design]
sources:
  - book: isbn:9780387220734
    title: Jari Kaipio and Erkki Somersalo, Statistical and Computational Inverse Problems, Springer, 2005
    locator: Chapter 3, Statistical Inversion Theory (Gaussian priors and noise, the posterior mean and covariance)
  - book: "Albert Tarantola, Inverse Problem Theory and Methods for Model Parameter Estimation, SIAM, 2005"
    locator: Chapter 3, The Least-Squares Criterion (Gaussian prior and data, the posterior mean and covariance)
  - book: isbn:9780128135556
    title: William Menke, Geophysical Data Analysis, Discrete Inverse Theory, fourth edition, Academic Press, 2018
    locator: the chapters Solution of the Linear Gaussian Inverse Problem (the length method, generalized inverses and maximum likelihood viewpoints)
  - book: isbn:9780898716962
    title: Per Christian Hansen, Discrete Inverse Problems, Insight and Algorithms, SIAM, 2010
    locator: Chapter 4, Regularization Methods (Tikhonov regularization and its filter factors)
---

The linear Gaussian inverse problem is the statistical model $y = A x + e$ in which the unknown $x$ and the noise $e$ are independent Gaussian vectors, $x \sim N(x_{\mathrm{pr}}, \Gamma_{\mathrm{pr}})$ and $e \sim N(0, \Gamma_{\mathrm{n}})$, and $A$ is a known matrix. In this model the posterior law of $x$ given $y$ is Gaussian and has a closed form. Its mean is the minimizer of a [Tikhonov](/tikhonov-regularization/) functional whose weights are the inverse covariances, and its covariance does not depend on the data. It is the statistical counterpart of the deterministic setting of a [regularization method](/regularization-method/), the simplest [Bayesian inverse problem](/bayesian-inverse-problem/), and the base case for nonlinear and non-Gaussian models, which are often approximated by it locally.

## The machine

**The ingredients.** A forward matrix $A \in \mathbb{R}^{m \times n}$ (see [forward operator](/forward-operator/)), a prior mean $x_{\mathrm{pr}} \in \mathbb{R}^n$, a symmetric positive definite prior covariance $\Gamma_{\mathrm{pr}}$, and a symmetric positive definite noise covariance $\Gamma_{\mathrm{n}}$. The unknown and the noise are independent, and the data are $y = A x + e$.

**The posterior.** By [Bayes' theorem](/bayes-theorem/) the posterior density is proportional to the product of the likelihood and the prior:
$$\pi(x \mid y) \propto \exp\Big(-\tfrac12 \|y - A x\|_{\Gamma_{\mathrm{n}}^{-1}}^2 - \tfrac12 \|x - x_{\mathrm{pr}}\|_{\Gamma_{\mathrm{pr}}^{-1}}^2\Big),$$
where $\|z\|_M^2 = z^T M z$. The exponent is a quadratic in $x$, so the posterior is Gaussian, $N(x_{\mathrm{post}}, \Gamma_{\mathrm{post}})$, with
$$\Gamma_{\mathrm{post}} = \big(A^T \Gamma_{\mathrm{n}}^{-1} A + \Gamma_{\mathrm{pr}}^{-1}\big)^{-1}, \qquad x_{\mathrm{post}} = \Gamma_{\mathrm{post}} \big(A^T \Gamma_{\mathrm{n}}^{-1} y + \Gamma_{\mathrm{pr}}^{-1} x_{\mathrm{pr}}\big).$$
To see this, expand the exponent: the quadratic term is $x^T \Gamma_{\mathrm{post}}^{-1} x$ and the linear term is $-2 x^T (A^T \Gamma_{\mathrm{n}}^{-1} y + \Gamma_{\mathrm{pr}}^{-1} x_{\mathrm{pr}})$. Completing the square gives the mean.

**The gain form.** The same posterior in the data space, from the Woodbury identity or from the conditional law of the joint Gaussian vector $(x, y)$ with a [Schur complement](/schur-complement/):
$$x_{\mathrm{post}} = x_{\mathrm{pr}} + K (y - A x_{\mathrm{pr}}), \qquad K = \Gamma_{\mathrm{pr}} A^T (A \Gamma_{\mathrm{pr}} A^T + \Gamma_{\mathrm{n}})^{-1},$$
$$\Gamma_{\mathrm{post}} = \Gamma_{\mathrm{pr}} - \Gamma_{\mathrm{pr}} A^T (A \Gamma_{\mathrm{pr}} A^T + \Gamma_{\mathrm{n}})^{-1} A \Gamma_{\mathrm{pr}}.$$
The first form solves an $n \times n$ system, the second an $m \times m$ system. Use the one with the smaller size. The gain form is the update step of the [Kalman filter](/kalman-filter/).

**The white case.** With $x_{\mathrm{pr}} = 0$, $\Gamma_{\mathrm{pr}} = \gamma^2 I$ and $\Gamma_{\mathrm{n}} = \eta^2 I$, the posterior mean is
$$x_{\mathrm{post}} = (A^T A + \alpha I)^{-1} A^T y, \qquad \alpha = \eta^2/\gamma^2,$$
the Tikhonov solution with parameter $\alpha$ (the page [Tikhonov regularization](/tikhonov-regularization/) writes $\lambda$). The parameter is the ratio of the noise variance to the prior variance.

## What it counts

The model has two outputs, and each has a meaning that the deterministic setting does not give.

- **The estimate.** The posterior mean $x_{\mathrm{post}}$. Because the posterior is Gaussian, it is also the posterior mode, the [MAP estimate](/maximum-a-posteriori-estimation/), and the median of every coordinate.
- **The uncertainty.** The posterior covariance $\Gamma_{\mathrm{post}}$. Its diagonal gives a standard deviation for each unknown, and its off-diagonal entries show which combinations of unknowns the data determine. If $x$ is drawn from the prior, the expected squared error of the posterior mean is $\mathbb{E}\|x_{\mathrm{post}} - x\|^2 = \operatorname{tr} \Gamma_{\mathrm{post}}$.
- **The cost.** In flops: $O(m n^2 + n^3)$ for the first form with a [Cholesky](/cholesky-decomposition/) factorization, or $O(m^2 n + m^3)$ for the gain form. One SVD of a whitened matrix gives the posterior for every value of $\alpha$, as in the next section. For large imaging problems, $\Gamma_{\mathrm{post}}$ is not formed. The mean is computed by an iterative solver such as the [conjugate gradient method](/conjugate-gradient-method/), and the variances by low-rank or sampling approximations.

**The SVD view.** In the white case, let $A = \sum_i \sigma_i u_i v_i^T$. Then
$$x_{\mathrm{post}} = \sum_i f_i \frac{u_i^T y}{\sigma_i} v_i, \qquad \Gamma_{\mathrm{post}} = \sum_i \gamma^2 (1 - f_i)\, v_i v_i^T, \qquad f_i = \frac{\sigma_i^2}{\sigma_i^2 + \alpha}.$$
The [filter factors](/spectral-filter-factors/) $f_i$ of Tikhonov set both the estimate and the uncertainty. Along $v_i$, the posterior variance is the prior variance times $1 - f_i$. Where the data are informative ($f_i$ near 1), the variance is small. Where they are not ($f_i$ near 0), the posterior equals the prior: the data say nothing there, and the answer is the assumption.

## Relation to other models

- **The deterministic model.** There only $\|e\| \le \delta$ is known, and methods are judged by the worst case over all such $e$. Here $e$ is random with a known covariance, and methods are judged by averages. The same Tikhonov formula appears in both, with $\alpha$ chosen by a rule from $\delta$ in one case and given by $\eta^2/\gamma^2$ in the other. White noise of fixed variance has expected norm $\eta\sqrt{m}$, which grows with the number of data, so the two noise levels are not the same number.
- **The Bayesian inverse problem.** The general [Bayesian inverse problem](/bayesian-inverse-problem/) allows a nonlinear forward map and non-Gaussian laws. Then the posterior has no closed form and is explored by optimization (for the MAP point), by a Laplace approximation around it, or by sampling. The linear Gaussian model is the exact case of the Laplace approximation.
- **Generalized least squares.** If $A$ has full column rank and $\Gamma_{\mathrm{pr}}^{-1} \to 0$ (a flat prior), the posterior mean becomes the [generalized least squares](/generalized-least-squares/) estimator $(A^T \Gamma_{\mathrm{n}}^{-1} A)^{-1} A^T \Gamma_{\mathrm{n}}^{-1} y$, and $\Gamma_{\mathrm{post}}$ becomes its covariance. For an ill-posed problem this limit is useless, because the covariance blows up along the small singular directions.
- **Gaussian process regression and kriging.** With $A$ the evaluation of a function at points, the gain form is the formula of [Gaussian process](/gaussian-process/) regression and of [kriging](/kriging/).
- **The Kalman filter.** Each update step of the Kalman filter is a linear Gaussian inverse problem whose prior is the forecast.
- **Infinite dimensions.** For a function $x$, a white prior is not a law on $L^2$, and the prior covariance must be a trace-class operator. With that choice the formulas above hold for operators, and the posterior is well defined and depends continuously on the data.

## Known results in the model

- **Closed form.** The posterior is $N(x_{\mathrm{post}}, \Gamma_{\mathrm{post}})$ with the formulas above, and the two forms agree.
- **Tikhonov is the posterior mean.** $x_{\mathrm{post}}$ minimizes $\|y - A x\|_{\Gamma_{\mathrm{n}}^{-1}}^2 + \|x - x_{\mathrm{pr}}\|_{\Gamma_{\mathrm{pr}}^{-1}}^2$. Every Tikhonov method with quadratic penalty $\|L(x - x_0)\|^2$ and $L$ of full column rank is the posterior mean for white noise of variance $\eta^2$ and the prior $N(x_0, \gamma^2 (L^T L)^{-1})$, with $\alpha = \eta^2/\gamma^2$.
- **Best estimate in mean square.** Among all estimators $\hat x(y)$, the posterior mean minimizes $\mathbb{E}\|\hat x(y) - x\|^2$ over the joint law of $x$ and $y$, and the minimum is $\operatorname{tr}\Gamma_{\mathrm{post}}$. Among linear estimators it is optimal for any laws with these means and covariances, Gaussian or not.
- **The covariance does not depend on $y$.** $\Gamma_{\mathrm{post}}$ is known before any data are taken. So the design of an experiment (which rows $A$ to measure) can be optimized in advance, for example by minimizing $\operatorname{tr}\Gamma_{\mathrm{post}}$ (A-optimal) or $\log\det\Gamma_{\mathrm{post}}$ (D-optimal); see [optimal experimental design](/optimal-experimental-design/).
- **Resolution.** For a fixed true $x$, $\mathbb{E}[x_{\mathrm{post}} \mid x] - x_{\mathrm{pr}} = R (x - x_{\mathrm{pr}})$ with $R = K A = I - \Gamma_{\mathrm{post}} \Gamma_{\mathrm{pr}}^{-1}$, the [resolution matrix](/resolution-matrix/). The estimate is biased toward the prior mean wherever $R \ne I$.
- **The evidence.** The marginal law of the data is $y \sim N(A x_{\mathrm{pr}}, A \Gamma_{\mathrm{pr}} A^T + \Gamma_{\mathrm{n}})$. Maximizing it over $\gamma$ or $\eta$ is one way to choose $\alpha$ from the data (empirical Bayes).

**A worked example.** Let $A = \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$, $x_{\mathrm{pr}} = 0$, $\Gamma_{\mathrm{pr}} = I$, $\Gamma_{\mathrm{n}} = I$ and $y = (1, 2)$. Then $A^T A + I = \begin{pmatrix} 3 & 1 \\ 1 & 2 \end{pmatrix}$ has determinant $5$, so
$$\Gamma_{\mathrm{post}} = \begin{pmatrix} 2/5 & -1/5 \\ -1/5 & 3/5 \end{pmatrix}, \qquad A^T y = (3, 2), \qquad x_{\mathrm{post}} = (4/5,\ 3/5).$$
This is the Tikhonov solution with $\alpha = 1$. The gain form gives the same: $A A^T + I = \begin{pmatrix} 2 & 1 \\ 1 & 3 \end{pmatrix}$ has inverse $\frac15\begin{pmatrix} 3 & -1 \\ -1 & 2 \end{pmatrix}$, $K = \frac15\begin{pmatrix} 2 & 1 \\ -1 & 2 \end{pmatrix}$ and $K y = (4/5, 3/5)$. The posterior standard deviations are $\sqrt{0.4} = 0.632$ and $\sqrt{0.6} = 0.775$, both less than the prior value $1$, and the correlation is $-0.2/\sqrt{0.24} = -0.408$: the data fix the sum $x_1 + x_2$ better than each part. The expected squared error falls from $\operatorname{tr}\Gamma_{\mathrm{pr}} = 2$ to $\operatorname{tr}\Gamma_{\mathrm{post}} = 1$, and the resolution matrix is $I - \Gamma_{\mathrm{post}} = \begin{pmatrix} 3/5 & 1/5 \\ 1/5 & 2/5 \end{pmatrix}$, with trace $1$.

## References
