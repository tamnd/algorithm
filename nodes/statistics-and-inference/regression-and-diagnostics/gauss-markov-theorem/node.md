---
tag: 4143Z0
kind: theorem
slug: gauss-markov-theorem
name: Gauss-Markov theorem
aliases:
- BLUE theorem
- best linear unbiased estimator
area: statistics-and-inference/regression-and-diagnostics
level: core
summary: In a linear model with uncorrelated errors of equal variance, ordinary least squares has the least variance among all linear unbiased estimators.
prereqs: [ordinary-least-squares, linear-regression, estimator-bias, covariance-matrix]
see_also: [minimum-variance-unbiased-estimator, lehmann-scheffe-theorem, generalized-least-squares, weighted-least-squares, ridge-regression, james-stein-estimator, heteroscedasticity, hat-matrix]
sources:
  - book: isbn:9780898713473
    title: Carl Friedrich Gauss, Theory of the Combination of Observations Least Subject to Errors, translated by G. W. Stewart, SIAM Classics in Applied Mathematics 11, 1995
    locator: Part One and Part Two of the Theoria combinationis (1821 and 1823), where least squares is shown to give the linear unbiased combination of least mean squared error for any error law
  - paper: doi:10.1017/S0370164600014346
    title: "A. C. Aitken, On least squares and linear combination of observations, Proceedings of the Royal Society of Edinburgh 55, 1935, pp. 42 to 48"
    locator: The whole paper (the matrix form of the theorem and the generalized least squares estimator for correlated errors)
  - paper: doi:10.1093/biomet/36.3-4.458
    title: "R. L. Plackett, A historical note on the method of least squares, Biometrika 36(3/4), 1949, pp. 458 to 460"
    locator: The whole note (Gauss's 1821 to 1823 proof, Markov's textbook account and the name)
  - book: isbn:9780471415404
    title: George A. F. Seber and Alan J. Lee, Linear Regression Analysis, second edition, Wiley, 2003
    locator: Chapter 3 (least squares estimation, the Gauss-Markov theorem and its generalization to correlated errors)
  - paper: doi:10.1214/aoms/1177698505
    title: "William Kruskal, When are Gauss-Markov and least squares estimators identical? A coordinate-free approach, Annals of Mathematical Statistics 39(1), 1968, pp. 70 to 75"
    locator: The whole paper (least squares is best linear unbiased under a general covariance if and only if the covariance maps the column space of X into itself)
  - paper: doi:10.3982/ECTA20819
    title: "Benedikt M. Pötscher and David Preinerstorfer, A comment on: A modern Gauss-Markov theorem, Econometrica 92(3), 2024, pp. 913 to 924"
    locator: The whole comment (the version of Hansen 2022 without the word linear covers the same estimators as the classical Aitken theorem)
---

The Gauss-Markov theorem says that in a linear model whose errors have mean 0, are uncorrelated and have equal variance, the [ordinary least squares](/ordinary-least-squares/) estimator is the best linear unbiased estimator (BLUE): every other estimator that is linear in $y$ and unbiased for every value of the coefficients has a covariance matrix at least as large, in the order of positive semidefinite matrices. No normality is needed and no independence beyond zero correlation. All three conditions matter, and so do the two restrictions on the competitors: biased estimators such as ridge regression, and nonlinear unbiased estimators under a known non-normal error law, can do better. Gauss proved the result in 1821 to 1823; Aitken gave the matrix form and the extension to correlated errors in 1935.

## Statement

Let $y = Xb + \varepsilon$, where $y$ is the $n$-vector of responses, $X$ is an $n \times p$ design matrix (its $p$ columns include the intercept, if any), $b \in \mathbb{R}^p$ is the unknown coefficient vector, and $\varepsilon$ is the error vector. Assume:

1. **Linear model of full rank.** $X$ is fixed, or random with all statements conditional on $X$, and has rank $p$.
2. **Zero mean.** $\mathbb{E}[\varepsilon \mid X] = 0$.
3. **Spherical errors.** $\operatorname{Var}(\varepsilon \mid X) = \sigma^2 I_n$ for some $\sigma^2 > 0$: the errors are uncorrelated and have equal variance. They need not be independent, identically distributed or normal.

A *linear estimator* of $b$ is $\tilde b = Cy$, where the $p \times n$ matrix $C$ may depend on $X$ but not on $y$. It is *unbiased* if $\mathbb{E}[\tilde b \mid X] = b$ for every $b \in \mathbb{R}^p$. Let $\hat b = (X^\top X)^{-1}X^\top y$ be the least squares estimator. Then:

1. $\hat b$ is linear and unbiased, with $\operatorname{Var}(\hat b \mid X) = \sigma^2(X^\top X)^{-1}$.
2. **Best in the matrix order.** For every linear unbiased $\tilde b$, the matrix $\operatorname{Var}(\tilde b \mid X) - \operatorname{Var}(\hat b \mid X)$ is positive semidefinite.
3. **Best and unique for every linear function.** For every $c \in \mathbb{R}^p$, $c^\top\hat b$ has the smallest variance among linear unbiased estimators of $c^\top b$, and any linear unbiased estimator of $c^\top b$ with that variance equals $c^\top\hat b$.

If $X$ is random, the same order holds for the unconditional covariance matrices whenever $\mathbb{E}[(X^\top X)^{-1}]$ is finite.

## In plain words

You want to estimate the slope of a straight-line law from noisy measurements, using a weighted sum of the measurements. You ask for a recipe that is right on average whatever the true line is. Many recipes do this: for example, take the last measurement minus the first and divide by the distance between them. Among all of them, least squares scatters least around the truth, provided the measurement errors average to zero, do not move together, and all have the same spread. The bell curve is not needed. If you allow recipes that are wrong on average, or recipes that are not weighted sums and use a known shape of the errors, you can sometimes beat least squares.

## Proof

**Part 1.** $\hat b = Ay$ with $A = (X^\top X)^{-1}X^\top$, which exists because $X$ has rank $p$, so $X^\top X$ is positive definite. $\mathbb{E}[\hat b \mid X] = AXb = b$. $\operatorname{Var}(\hat b \mid X) = A(\sigma^2 I)A^\top = \sigma^2(X^\top X)^{-1}X^\top X(X^\top X)^{-1} = \sigma^2(X^\top X)^{-1}$.

**Unbiasedness of a linear estimator.** $\mathbb{E}[Cy \mid X] = CXb$. This equals $b$ for every $b$ if and only if $CX = I_p$: take $b$ to be each unit vector in turn.

**Part 2.** Let $Cy$ be linear and unbiased, and write $C = A + D$. Then $I = CX = AX + DX = I + DX$, so $DX = 0$, and also $AD^\top = (X^\top X)^{-1}(DX)^\top = 0$. Hence

$$\operatorname{Var}(Cy \mid X) = \sigma^2CC^\top = \sigma^2(AA^\top + AD^\top + DA^\top + DD^\top) = \sigma^2(X^\top X)^{-1} + \sigma^2DD^\top.$$

The difference from $\operatorname{Var}(\hat b \mid X)$ is $\sigma^2DD^\top$, and $c^\top DD^\top c = \lVert D^\top c\rVert^2 \ge 0$ for every $c$, so it is positive semidefinite.

**Part 3.** A linear estimator $a^\top y$ of $c^\top b$ is unbiased for every $b$ if and only if $X^\top a = c$, by the same argument. Let $H = X(X^\top X)^{-1}X^\top$, the [hat matrix](/hat-matrix/), which is the orthogonal projection onto the column space of $X$. Write $a = Ha + (I - H)a$. The first part is $a_\ast = Ha = X(X^\top X)^{-1}X^\top a = X(X^\top X)^{-1}c$, the same for every admissible $a$, and $a_\ast^\top y = c^\top(X^\top X)^{-1}X^\top y = c^\top\hat b$. The two parts are orthogonal, so

$$\operatorname{Var}(a^\top y \mid X) = \sigma^2\lVert a\rVert^2 = \sigma^2\lVert a_\ast\rVert^2 + \sigma^2\lVert(I - H)a\rVert^2 = \operatorname{Var}(c^\top\hat b \mid X) + \sigma^2\lVert(I - H)a\rVert^2.$$

So $\operatorname{Var}(a^\top y \mid X) \ge \operatorname{Var}(c^\top\hat b \mid X)$, with equality if and only if $(I - H)a = 0$, that is, $a = a_\ast$, so the estimator is $c^\top\hat b$. (Part 2 also follows from part 3 by taking $a = C^\top c$ for each $c$.)

**Random $X$.** If $\tilde b$ is conditionally unbiased, then by the law of total variance $\operatorname{Var}(\tilde b) = \mathbb{E}[\operatorname{Var}(\tilde b \mid X)] + \operatorname{Var}(\mathbb{E}[\tilde b \mid X]) = \mathbb{E}[\operatorname{Var}(\tilde b \mid X)]$, because $\mathbb{E}[\tilde b \mid X] = b$ is constant. The same holds for $\hat b$, and the expectation of a positive semidefinite matrix is positive semidefinite. $\blacksquare$

The proof uses only the first two moments of $\varepsilon$. Normality enters nowhere.

## Consequences

- **Predictions and fitted values.** For any point $x_0$, $x_0^\top\hat b$ is the BLUE of the mean response $x_0^\top b$. Every fitted value is BLUE for its mean, and $\operatorname{Var}(\hat y \mid X) = \sigma^2H$.
- **Scalar summaries.** The matrix order implies the order of every monotone summary: the total variance $\operatorname{tr}\operatorname{Var}(\tilde b)$, the generalized variance $\det\operatorname{Var}(\tilde b)$ and the mean squared prediction error over any set of points are all smallest for $\hat b$ within the linear unbiased class.
- **Rank-deficient designs.** If $X$ has rank $r < p$, $b$ itself has no unbiased estimator, but every estimable function $c^\top b$, with $c$ in the row space of $X$, has the BLUE $c^\top\hat b$ for any least squares solution $\hat b$. This is the form used for analysis of variance models.
- **Correlated errors (Aitken).** If $\operatorname{Var}(\varepsilon \mid X) = \sigma^2\Sigma$ with $\Sigma$ known and positive definite, apply the theorem to $\Sigma^{-1/2}y = \Sigma^{-1/2}Xb + \Sigma^{-1/2}\varepsilon$, whose errors are spherical. The BLUE is the [generalized least squares](/generalized-least-squares/) estimator $(X^\top\Sigma^{-1}X)^{-1}X^\top\Sigma^{-1}y$, with covariance $\sigma^2(X^\top\Sigma^{-1}X)^{-1}$. With a diagonal $\Sigma$ this is [weighted least squares](/weighted-least-squares/).
- **Normal errors.** If in addition $\varepsilon \sim N(0, \sigma^2I)$, then $(X^\top y, \lVert y\rVert^2)$ is a complete sufficient statistic, and by the [Lehmann-Scheffé theorem](/lehmann-scheffe-theorem/) $c^\top\hat b$ is the [minimum variance unbiased estimator](/minimum-variance-unbiased-estimator/) among all unbiased estimators, linear or not. It also reaches the Cramér-Rao bound.
- **The residual variance.** Under the same three conditions, $s^2 = \lVert y - X\hat b\rVert^2/(n - p)$ is unbiased for $\sigma^2$, since $\mathbb{E}\lVert(I - H)\varepsilon\rVert^2 = \sigma^2\operatorname{tr}(I - H) = \sigma^2(n - p)$. So $s^2(X^\top X)^{-1}$ is an unbiased estimate of $\operatorname{Var}(\hat b \mid X)$, which is what the usual standard errors use.

## Tightness

**A linear unbiased competitor that loses.** With $x = (1, 2, 3, 4, 5)$, the endpoint slope $(y_5 - y_1)/4$ is linear and unbiased for the slope, with variance $2\sigma^2/16 = 0.125\sigma^2$. The least squares slope has variance $\sigma^2/S_{xx} = \sigma^2/10 = 0.1\sigma^2$. The theorem says that no choice of weights can go below $0.1\sigma^2$.

**Linearity is needed when the error law is known.** Let $y_i = \mu + \varepsilon_i$ with $\varepsilon_i$ iid uniform on $[-\tfrac12, \tfrac12]$, so $X = \mathbf 1$ and $\hat b = \bar y$, with variance $1/(12n)$. The midrange $\frac12(\min_i y_i + \max_i y_i)$ is unbiased for $\mu$ (by symmetry) and has variance $1/(2(n + 1)(n + 2))$. For $n = 10$ that is $0.00379$ against $0.00833$ for the mean, and the ratio tends to 0 as $n$ grows. The midrange is not linear, and it is unbiased only because the error law is symmetric. Hansen (2022) argued that "linear" can be dropped if unbiasedness is required for every error distribution with the stated moments; Pötscher and Preinerstorfer (2024) showed that this class of estimators is the same as in the classical theorem. Dropping "linear" while keeping unbiasedness only for one error law is false, as the midrange shows.

**Unbiasedness is needed.** [Ridge regression](/ridge-regression/), $(X^\top X + \lambda I)^{-1}X^\top y$, is linear but biased. Hoerl and Kennard (1970) showed that for every $b$ and $\sigma^2$ some $\lambda > 0$ gives a smaller total mean squared error than least squares. For $p \ge 3$ coefficients with normal errors, the [James-Stein estimator](/james-stein-estimator/), which is neither linear nor unbiased, has smaller total mean squared error than $\hat b$ for every $b$ (with the error measured in the metric of $X^\top X$). So "best" is only within the class.

**Equal variances are needed.** Let $x = (1, 2, 3, 4, 5)$ and $\operatorname{Var}(\varepsilon_i) = x_i^2$, uncorrelated. The least squares slope is still unbiased, with variance $\sum_i (x_i - \bar x)^2x_i^2/S_{xx}^2 = 124/100 = 1.24$. Weighted least squares with weights $1/x_i^2$ has variance $5269/7576 = 0.6955$, 44% less. See [heteroscedasticity](/heteroscedasticity/).

**Uncorrelatedness is needed, but not exactly.** Kruskal (1968) showed that, for a general error covariance $\sigma^2\Sigma$, least squares is still BLUE if and only if $\Sigma$ maps the column space of $X$ into itself. For example, equicorrelated errors, $\Sigma = (1 - \rho)I + \rho\mathbf 1\mathbf 1^\top$ with $-1/(n - 1) < \rho < 1$, leave least squares BLUE in any model with an intercept, since $\Sigma x = (1 - \rho)x + \rho(\mathbf 1^\top x)\mathbf 1$ stays in the column space. So condition 3 is sufficient but not necessary.

**Zero mean is needed.** If $\mathbb{E}[\varepsilon \mid X] \ne 0$, for example when a relevant predictor is omitted and correlated with the included ones, or when a predictor is measured with error, $\hat b$ is biased, and the theorem says nothing.

## History

Gauss first justified least squares in 1809 by assuming normal errors. In the Theoria combinationis observationum erroribus minimis obnoxiae, presented in two parts in 1821 and 1823, he dropped that assumption and proved that, for any error law with mean 0 and finite variance, least squares gives the linear unbiased combination of the observations with the least mean squared error; this is the theorem in its scalar form. Andrei Markov presented the result in his probability textbook (first edition 1900, second 1908). Jerzy Neyman, in 1934, called it Markov's theorem, which gave the name its second half; Plackett's 1949 note set out Gauss's priority. Alexander Aitken gave the matrix statement and the extension to correlated errors with a known covariance in 1935. Kruskal's 1968 coordinate-free paper settled when least squares and the Aitken estimator coincide.

## References
