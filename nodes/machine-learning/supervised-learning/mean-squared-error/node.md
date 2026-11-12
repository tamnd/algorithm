---
tag: 6KT5V6
kind: definition
slug: mean-squared-error
name: Mean squared error
aliases:
- L2 loss
- MSE
- Mean squared error loss
- quadratic loss
- squared loss
area: machine-learning/supervised-learning
level: intro
summary: "The mean of the squared differences between predictions and targets. Its minimizer is the conditional mean, and for an estimator it splits into variance plus squared bias."
prereqs: [loss-function, expected-value, variance]
see_also: [bias-variance-tradeoff, ordinary-least-squares, linear-regression, conditional-expectation, maximum-likelihood-estimation, quantile-regression, cross-validation, median]
sources:
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 2.4 (statistical decision theory, the conditional mean for squared loss and the median for absolute loss) and Section 7.3 (the bias-variance decomposition)
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 1.5.5 (loss functions for regression, the conditional mean and the Minkowski loss)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 7.3.1 (mean squared error of a point estimator, variance plus squared bias)
---

The mean squared error (MSE) is the mean of the squared differences between predictions and targets. The name covers two uses that this page keeps apart: the *training loss* $L(\theta) = \frac1n \sum_i (y_i - \hat y_i)^2$ that a regression model minimizes, and the *risk of an estimator* $\mathbb{E}[(\hat\theta - \theta)^2]$, which splits exactly into variance plus squared bias. For predictions, the squared loss is minimized by the [conditional mean](/conditional-expectation/) of the target, which is why least squares methods estimate means.

## Definition

**Squared loss and the empirical MSE.** For a real prediction $\hat y$ and a real target $y$, the squared loss is $\ell(\hat y, y) = (\hat y - y)^2$. For a predictor $h_\theta$ and a training set $(x_1, y_1), \ldots, (x_n, y_n)$,

$$L(\theta) = \mathrm{MSE} = \frac1n \sum_{i=1}^{n} \big(y_i - h_\theta(x_i)\big)^2.$$

This is the empirical risk of the squared [loss function](/loss-function/). On held-out data the same formula is an estimate of the risk $R(h) = \mathbb{E}_{(x, y) \sim D}(y - h(x))^2$. For vector targets in $\mathbb{R}^k$ the squared Euclidean norm replaces the square; some libraries then divide by $nk$ and some by $n$.

**Its minimizer is the conditional mean.** If $\mathbb{E}[y^2] < \infty$, then for each $x$ and each constant $c$,

$$\mathbb{E}\big[(y - c)^2 \mid x\big] = \operatorname{Var}(y \mid x) + \big(\mathbb{E}[y \mid x] - c\big)^2.$$

*Proof.* Write $\mu = \mathbb{E}[y \mid x]$ and $(y - c)^2 = (y - \mu)^2 + 2(y - \mu)(\mu - c) + (\mu - c)^2$. Take the conditional expectation. The middle term is $2(\mu - c)\,\mathbb{E}[y - \mu \mid x] = 0$. $\blacksquare$

So $c = \mathbb{E}[y \mid x]$ is the unique minimizer at each $x$, the best predictor in squared loss is the regression function $f(x) = \mathbb{E}[y \mid x]$, and the smallest possible risk is $\mathbb{E}\operatorname{Var}(y \mid x)$. Averaging the identity over $x$ gives $R(h) = R(f) + \mathbb{E}_x (h(x) - f(x))^2$: the excess risk of any predictor is its mean squared distance to $f$.

**MSE of an estimator.** Let $\hat\theta$ be a function of a random sample that estimates a fixed number $\theta$. Its mean squared error is

$$\mathrm{MSE}(\hat\theta) = \mathbb{E}\big[(\hat\theta - \theta)^2\big] = \operatorname{Var}(\hat\theta) + \operatorname{bias}(\hat\theta)^2, \qquad \operatorname{bias}(\hat\theta) = \mathbb{E}\hat\theta - \theta.$$

The proof is the same identity with $\mu = \mathbb{E}\hat\theta$ and $c = \theta$. Here the expectation is over samples, not over a test point, and $\theta$ is a parameter, not a label. Apply the same split to the prediction $\hat g_S(x_0)$ of a learner trained on a random training set $S$, add the label noise, and you get the [bias-variance decomposition](/bias-variance-tradeoff/) of the expected test error.

**Gradient.** For a linear model $\hat y = Xw$ with the $n \times d$ data matrix $X$,

$$L(w) = \frac1n \lVert y - Xw \rVert^2, \qquad \nabla L(w) = \frac2n X^\top (Xw - y), \qquad \nabla^2 L(w) = \frac2n X^\top X.$$

The Hessian is positive semidefinite, so $L$ is [convex](/convex-function/), and the minimizers solve the normal equations $X^\top X w = X^\top y$ of [ordinary least squares](/ordinary-least-squares/). Many texts use $\frac{1}{2n}$ in front, which removes the factor 2 from the gradient and does not change the minimizer.

**Link to likelihood.** If $y = h_\theta(x) + \varepsilon$ with $\varepsilon \sim N(0, \sigma^2)$ and $\sigma$ fixed, then $-\ln p(y \mid x) = \frac{(y - h_\theta(x))^2}{2\sigma^2} + \frac12 \ln(2\pi\sigma^2)$. So minimizing the MSE is [maximum likelihood estimation](/maximum-likelihood-estimation/) under Gaussian noise.

## Examples and non-examples

**A training loss.** Targets $y = (3, -0.5, 2, 7)$ and predictions $\hat y = (2.5, 0, 2, 8)$ give squared errors $0.25, 0.25, 0, 1$, so $\mathrm{MSE} = 1.5 / 4 = 0.375$. The root mean squared error is $\sqrt{0.375} = 0.6124$, in the units of $y$. The mean absolute error is $0.5$.

**The mean against the median.** Fit one constant $c$ to $y = (1, 2, 3, 10)$. The MSE is smallest at the mean $c = 4$, where it equals $12.5$, the variance of the four values with divisor $n$ (the sample variance with divisor $n - 1$ is $50/3$); at $c = 2.5$ it is $14.75$. The mean absolute error $\frac14 \sum \lvert y_i - c \rvert$ is smallest on the whole interval $[2, 3]$ of [medians](/median/), with value $2.5$; at the mean $c = 4$ it is $3$. The single outlier 10 pulls the mean, not the median. This is the reason MAE is used when the noise has heavy tails, and the reason [quantile regression](/quantile-regression/) generalizes it.

**A biased estimator with a smaller MSE.** Draw $n$ i.i.d. values from $N(\mu, \sigma^2)$ and let $\mathrm{SS} = \sum_i (x_i - \bar x)^2$. Then $\mathrm{SS}/\sigma^2$ has the $\chi^2_{n-1}$ law, so $\mathbb{E}\,\mathrm{SS} = (n - 1)\sigma^2$ and $\operatorname{Var}\mathrm{SS} = 2(n - 1)\sigma^4$. For the estimator $\mathrm{SS}/c$,

$$\mathrm{MSE} = \sigma^4\Big(\frac{2(n - 1)}{c^2} + \Big(\frac{n - 1}{c} - 1\Big)^2\Big).$$

For $n = 10$ this is $\frac29\sigma^4 \approx 0.2222\sigma^4$ for the unbiased choice $c = n - 1$, $\frac{19}{100}\sigma^4$ for $c = n$, and $\frac{2}{11}\sigma^4 \approx 0.1818\sigma^4$ for $c = n + 1$, which is the minimum over $c$. A simulation with 200000 samples of size 10 (seed 3) gives 0.2209, 0.1891 and 0.1812. An unbiased estimator need not have the smallest MSE.

**Non-example: RMSE is not a mean of per-example losses.** $\sqrt{L}$ has the same minimizer as $L$, but it is not an average of a loss over examples, so the RMSE of a data set is not the mean of the RMSE of its parts, and its stochastic gradients are biased.

**Non-example: MSE on class probabilities is not cross-entropy.** The squared error between a predicted probability vector and a one-hot label is the Brier score. It is a proper scoring rule, but it is bounded, so it penalizes a confident wrong answer far less than the [cross-entropy loss](/cross-entropy-loss/).

## Related definitions

- [Loss function](/loss-function/): the general frame; squared loss is the case $\ell(\hat y, y) = (\hat y - y)^2$.
- [Bias-variance tradeoff](/bias-variance-tradeoff/): the decomposition of the expected squared test error of a learner into noise, squared bias and variance.
- [Ordinary least squares](/ordinary-least-squares/) and [linear regression](/linear-regression/): the minimizer of the training MSE over linear predictors; [ridge regression](/ridge-regression/) adds a penalty.
- [Cross-validation](/cross-validation/): estimates the test MSE; for least squares, leave-one-out has a closed form.
- [Variance](/variance/): the MSE of the constant predictor $\mathbb{E}y$.
- Mean absolute error $\frac1n \sum \lvert y_i - \hat y_i \rvert$: minimized by a median, more robust to outliers, not differentiable at 0.

## References
