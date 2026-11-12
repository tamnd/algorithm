---
tag: XR74GK
kind: problem
slug: regression
name: Regression
aliases:
- supervised regression
- regression analysis
area: machine-learning/supervised-learning
level: intro
summary: "Learn a function that predicts a real number from an input. Under squared loss the best possible predictor is the conditional mean of the output given the input."
prereqs: [loss-function, conditional-expectation]
see_also: [linear-regression, classification, mean-squared-error, empirical-risk-minimization, bias-variance-tradeoff, quantile-regression, k-nearest-neighbors, curve-fitting]
sources:
  - book: isbn:9780387848570
    title: "Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, 2nd edition, Springer, 2009"
    locator: Section 2.4 (statistical decision theory, the conditional mean for squared loss and the conditional median for absolute loss) and Section 2.9 (model selection and the bias-variance tradeoff)
  - book: isbn:9780387954417
    title: "Laszlo Gyorfi, Michael Kohler, Adam Krzyzak and Harro Walk, A Distribution-Free Theory of Nonparametric Regression, Springer, 2002"
    locator: Chapter 1 (the regression problem and the L2 risk decomposition) and Chapter 3 (lower bounds, with no uniform rate of convergence over all distributions)
  - paper: doi:10.1214/aos/1176345969
    title: "Charles J. Stone, Optimal global rates of convergence for nonparametric regression, Annals of Statistics 10(4), 1982"
    locator: pp. 1040-1053, the rate n^(-2p/(2p+d)) for p-smooth regression functions in d dimensions
  - book: isbn:9780387946184
    title: "Luc Devroye, Laszlo Gyorfi and Gabor Lugosi, A Probabilistic Theory of Pattern Recognition, Springer, 1996"
    locator: Theorem 2.2, the excess error of a plug-in classifier is bounded by the L1 and L2 errors of the regression estimate
---

Regression is the supervised learning problem in which the output is a real number. From $n$ examples $(x_i, y_i)$ a learner builds a function $f$ that predicts $y$ for a new input $x$: a price from the features of a house, a dose response from a dose, tomorrow's load from today's weather. The quality of $f$ is its expected loss on new data. For the squared loss the best possible predictor is the conditional mean $\mathbb{E}[y \mid x]$, so regression with squared loss is the estimation of a [conditional expectation](/conditional-expectation/). [Linear regression](/linear-regression/) is the case in which $f$ is a linear function of $x$.

## In plain words

You have examples of inputs together with a number that goes with each one, and you want a rule that guesses the number for inputs you have not seen. The rule is good if its guesses on new inputs are close to the true numbers on average.

Two things decide what "close" means and what rules you allow. The first is the penalty for a wrong guess: if large misses cost much more than small ones, the best guess is the average of the possible outcomes; if all misses cost in proportion to their size, the best guess is the middle value. The second is the family of rules, from straight lines to trees to neural networks. A rule that is too simple misses the pattern. A rule that is too flexible copies the noise of the examples and guesses badly on new ones.

## Definition

**Data model.** The examples $(x_1, y_1), \dots, (x_n, y_n)$ are drawn i.i.d. from an unknown distribution $D$ on $\mathcal{X} \times \mathbb{R}$, usually with $\mathcal{X} = \mathbb{R}^d$. This is the random design. In the fixed design, common in statistics, the $x_i$ are given numbers and only the $y_i$ are random.

**Loss and risk.** A [loss function](/loss-function/) $\ell(\hat y, y) \ge 0$ measures the cost of predicting $\hat y$ when the truth is $y$. The risk of a predictor $f : \mathcal{X} \to \mathbb{R}$ is
$$
R(f) = \mathbb{E}_{(x, y) \sim D}\bigl[\ell(f(x), y)\bigr],
$$
and the empirical risk is $\hat R(f) = \frac1n\sum_{i=1}^n \ell(f(x_i), y_i)$. The default loss is the squared loss $\ell(\hat y, y) = (\hat y - y)^2$; its risk is the [mean squared error](/mean-squared-error/).

**Task.** Given the sample, output $\hat f$ with small risk $R(\hat f)$. Since $D$ is unknown, the goal is stated relative to a benchmark: the excess risk $R(\hat f) - \inf_f R(f)$ over all measurable $f$, or $R(\hat f) - \inf_{f \in \mathcal{H}} R(f)$ over a [hypothesis class](/hypothesis-class/) $\mathcal{H}$, should be small, in expectation or with high probability.

**The best predictor.** Let $m(x) = \mathbb{E}[y \mid x]$, the regression function. For the squared loss and every $f$,
$$
R(f) = R(m) + \mathbb{E}\bigl[(f(x) - m(x))^2\bigr], \qquad R(m) = \mathbb{E}\bigl[\operatorname{Var}(y \mid x)\bigr].
$$
*Proof.* Write $y - f(x) = (y - m(x)) + (m(x) - f(x))$ and expand the square. The cross term has expectation 0, because given $x$ the factor $m(x) - f(x)$ is fixed and $\mathbb{E}[y - m(x) \mid x] = 0$. $\square$

So $m$ minimizes the risk, $R(m)$ is the noise that no predictor can remove, and the excess risk of $f$ is its $L_2$ distance to $m$. For other losses the best predictor changes: the absolute loss $|\hat y - y|$ gives a conditional [median](/median/) of $y$ given $x$, and the pinball loss of level $\tau$ gives the conditional $\tau$-[quantile](/quantile/).

## Variants

- **The loss.** Squared loss (least squares), absolute loss (least absolute deviations), the Huber loss (squared near 0 and linear far away, for data with outliers), and the pinball loss of [quantile regression](/quantile-regression/).
- **The class of functions.** Linear functions ([linear regression](/linear-regression/)), a linear predictor with a link function ([generalized linear models](/generalized-linear-model/)), monotone functions ([isotonic regression](/isotonic-regression/)), functions in a kernel space, trees, nearest neighbor averages and neural networks.
- **A penalty.** Regularized regression minimizes $\hat R(f)$ plus a penalty on $f$: the squared norm in [ridge regression](/ridge-regression/), the $\ell_1$ norm in [lasso regression](/lasso-regression/), both in the [elastic net](/elastic-net/).
- **Parametric or nonparametric.** A parametric model has a fixed number of parameters. A nonparametric method, such as [k-nearest neighbors](/k-nearest-neighbors/) or a kernel smoother, lets the complexity of $f$ grow with $n$.
- **More outputs.** Multi-output regression predicts a vector $y \in \mathbb{R}^k$. Probabilistic regression predicts a whole distribution of $y$ given $x$, for example a [Gaussian process](/gaussian-process/) posterior.
- **In numerical analysis** the same task with a fixed design and no probability model is [curve fitting](/curve-fitting/): fit a function from a given family to points, with the error measured on those points only.

## Examples

**The best predictor depends on the loss.** Let $x$ take one value and let $y$ be $0$, $0$ or $3$ with probability $\frac13$ each. The mean is $1$ and the median is $0$.

| prediction | squared risk | absolute risk |
|---|---|---|
| $1$ (the mean) | $\frac13(1 + 1 + 4) = 2$ | $\frac13(1 + 1 + 2) = \frac43$ |
| $0$ (the median) | $\frac13(0 + 0 + 9) = 3$ | $\frac13(0 + 0 + 3) = 1$ |

The mean wins under the squared loss and the median wins under the absolute loss. For the squared loss the gap is $3 - 2 = (1 - 0)^2$, as the decomposition above says.

**Simple and flexible fits.** Take the three points $(1, 1)$, $(2, 3)$, $(3, 2)$.

| predictor | fitted values | training squared error (sum) |
|---|---|---|
| the constant $\bar y = 2$ | $2, 2, 2$ | $1 + 1 + 0 = 2$ |
| the least squares line $1 + \frac12 x$ | $1.5, 2, 2.5$ | $0.25 + 1 + 0.25 = 1.5$ |
| the quadratic through the three points | $1, 3, 2$ | $0$ |

The training error falls as the class grows, and the quadratic has error 0. That says nothing about new data: the quadratic $-\frac32x^2 + \frac{13}{2}x - 4$ predicts $-9$ at $x = 5$, while the line predicts $3.5$. Which one is better depends on $D$, and it is judged on held-out data, for example by [cross-validation](/cross-validation/). This is the [bias-variance tradeoff](/bias-variance-tradeoff/) and the risk of [overfitting](/overfitting/).

## Known algorithms

| Method | Class of functions and loss | Training cost |
|---|---|---|
| [Ordinary least squares](/ordinary-least-squares/) | linear, squared | $O(nd^2)$ by QR |
| [Ridge regression](/ridge-regression/) | linear, squared plus $\ell_2$ penalty | $O(nd^2 + d^3)$ |
| [Lasso](/lasso-regression/) and [elastic net](/elastic-net/) | linear, squared plus $\ell_1$ (and $\ell_2$) penalty | $O(nd)$ per sweep of coordinate descent |
| [Generalized linear model](/generalized-linear-model/) by IRLS | linear predictor and link, likelihood | $O(nd^2 + d^3)$ per iteration |
| [Quantile regression](/quantile-regression/) | linear, pinball | a linear program |
| [Isotonic regression](/isotonic-regression/) by [pool adjacent violators](/pool-adjacent-violators/) | monotone in one variable, squared | $O(n)$ after sorting |
| [k-nearest neighbors](/k-nearest-neighbors/) | local averages | none to train, $O(nd)$ per query by brute force |
| [Kernel ridge regression](/kernel-ridge-regression/) | a kernel space, squared plus norm penalty | $O(n^3)$ |
| [Support vector regression](/support-vector-regression/) | a kernel space, the $\epsilon$-insensitive loss | a quadratic program |
| [CART](/cart/) regression trees | piecewise constant, squared | $O(dn\log n)$ to sort, then $O(dn)$ per level |
| [Gradient boosting](/gradient-boosting/) | sums of trees, any differentiable loss | one tree per round |

Most of these minimize the empirical risk over a class, perhaps with a penalty ([empirical risk minimization](/empirical-risk-minimization/)). Nearest neighbors and kernel smoothers instead estimate $m(x)$ directly by local averages.

## Bounds

**Linear regression, fixed design.** Let $y = X\beta + \varepsilon$ with $X$ an $n \times d$ matrix of rank $d$ and noise with $\mathbb{E}\varepsilon = 0$ and $\operatorname{Cov}\varepsilon = \sigma^2 I$. The least squares fit $\hat y = Hy$, with the projection $H = X(X^\top X)^{-1}X^\top$, has in-sample prediction risk
$$
\frac1n\mathbb{E}\|X\hat\beta - X\beta\|^2 = \frac{\sigma^2 d}{n}.
$$
*Proof.* $X\hat\beta - X\beta = H\varepsilon$, and $\mathbb{E}\|H\varepsilon\|^2 = \sigma^2\operatorname{tr}(H^\top H) = \sigma^2\operatorname{tr} H = \sigma^2 d$, since $H$ is symmetric, $H^2 = H$, and the trace of a projection is its rank. $\square$

So the error grows with the number of parameters and falls as $1/n$.

**Nonparametric regression.** No method has a rate of convergence that holds for all distributions: for every estimator and every sequence that tends to 0, some distribution makes the excess risk fall more slowly (Gyorfi et al., Chapter 3). Rates need assumptions on $m$. If $m$ is $p$ times smooth on a bounded set in $\mathbb{R}^d$ and the noise is regular, the best rate of the excess squared risk is $n^{-2p/(2p+d)}$ (Stone 1982). The exponent shrinks as $d$ grows, which is the curse of dimensionality for regression.

## Reductions

- **Classification to regression.** For labels $y \in \{0, 1\}$, $m(x) = P(y = 1 \mid x)$, and the [Bayes optimal classifier](/bayes-optimal-classifier/) predicts 1 when $m(x) > \frac12$. A plug-in classifier that thresholds an estimate $\hat m$ at $\frac12$ has excess error at most $2\,\mathbb{E}|\hat m(x) - m(x)| \le 2\sqrt{\mathbb{E}(\hat m(x) - m(x))^2}$ (Devroye, Gyorfi and Lugosi, Theorem 2.2). So a good regression estimate gives a good classifier, although [classification](/classification/) can be easier than regression.
- **Linear least squares to linear algebra.** Linear regression with squared loss is the [least squares problem](/least-squares-problem/) $\min_\beta\|X\beta - y\|^2$ of numerical linear algebra.
- **Quantiles to linear programming.** Linear quantile regression is a linear program.
- **Regression inside other methods.** [Gradient boosting](/gradient-boosting/) fits a regression tree to the negative gradient in each round, and [fitted Q-iteration](/fitted-q-iteration/) in reinforcement learning solves a regression problem in each iteration.

## Applications

- Forecasting: demand, prices, loads and other quantities from past values and covariates.
- Science and engineering: dose-response curves, calibration curves of instruments, and the fit of physical laws to measurements.
- Econometrics and the social sciences: the effect of one variable on another with the others held fixed, which is causal only under further assumptions.
- Probability calibration of classifiers, by isotonic regression or logistic regression on the classifier scores.
- Value function and reward estimation in reinforcement learning.

## References
