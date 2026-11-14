---
tag: N5HH8Q
kind: definition
slug: estimator
name: Estimator
aliases:
- point estimator
area: statistics-and-inference/point-estimation
level: intro
summary: A function of the sample used to guess an unknown parameter. Its quality is judged by its sampling distribution, through bias, variance and risk.
prereqs: [random-variable, probability-distribution, expected-value]
see_also: [sampling-distribution, estimator-bias, standard-error, consistent-estimator, mean-squared-error, maximum-likelihood-estimation, method-of-moments, statistical-decision-theory]
sources:
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 7.1 (the definition of a point estimator as any function of the sample) and Section 7.3.1 (mean squared error)
  - book: isbn:9780387985022
    title: E. L. Lehmann and George Casella, Theory of Point Estimation, second edition, Springer, 1998
    locator: Chapter 1 (the estimation problem, loss and risk) and Chapter 2 (unbiasedness)
  - book: isbn:9780387402727
    title: Larry Wasserman, All of Statistics, Springer, 2004
    locator: Section 6.3 (point estimation, bias, standard error, consistency and mean squared error)
---

An estimator is a [random variable](/random-variable/) computed from the sample by a rule that does not use the unknown parameter, and it serves as a guess for a quantity $\psi(\theta)$ of the model. The number that the rule gives on the observed data is an *estimate*. The quality of an estimator is not a property of one estimate: it is a property of its [sampling distribution](/sampling-distribution/), measured by its [bias](/estimator-bias/), its [standard error](/standard-error/), its [mean squared error](/mean-squared-error/) and its [consistency](/consistent-estimator/).

## Definition

**The model.** The data are random variables $X_1, \ldots, X_n$ with values in a set $\mathcal X$. Their joint density or mass function is $f(x_1, \ldots, x_n; \theta)$, where the parameter $\theta$ lies in a parameter space $\Theta$. On these pages the $X_i$ are independent and identically distributed (iid) with density or mass function $f(x; \theta)$ unless a page says otherwise. $\mathbb{E}_\theta$, $\operatorname{Var}_\theta$ and $P_\theta$ are the [expected value](/expected-value/), the variance and the probability when $\theta$ is the true value. The observed values are $x_1, \ldots, x_n$.

**Statistic.** A statistic is a random variable $T = t(X_1, \ldots, X_n)$, where $t : \mathcal X^n \to \mathbb{R}^k$ is a fixed measurable function. The function $t$ may depend on $n$ and on known constants, but not on $\theta$.

**Estimand.** The estimand is the quantity to estimate, $\psi(\theta)$, for a fixed function $\psi : \Theta \to \mathbb{R}^k$. When $\psi(\theta) = \theta$ we estimate the parameter itself.

**Estimator.** An estimator of $\psi(\theta)$ is a statistic $T = t(X_1, \ldots, X_n)$ with values in a set that contains $\psi(\Theta)$. A hat marks it: $\hat\theta$ estimates $\theta$, $\hat\psi$ estimates $\psi(\theta)$, and $\hat\theta_n$ shows the sample size. The estimate is the number $t(x_1, \ldots, x_n)$. A rule that gives one estimator for each sample size, $T_n = t_n(X_1, \ldots, X_n)$ for $n = 1, 2, \ldots$, is a *sequence of estimators*; [consistency](/consistent-estimator/) is a property of such a sequence.

The definition asks for nothing more. A good estimator is one whose distribution under $P_\theta$ is concentrated near $\psi(\theta)$ for every $\theta \in \Theta$, not only for one. The standard measures, each a property of the sampling distribution of $T$ at each $\theta$:

| measure | formula | page |
|---|---|---|
| bias | $\operatorname{bias}_\theta(T) = \mathbb{E}_\theta[T] - \psi(\theta)$ | [bias of an estimator](/estimator-bias/) |
| standard error | $\operatorname{se}_\theta(T) = \sqrt{\operatorname{Var}_\theta(T)}$ | [standard error](/standard-error/) |
| mean squared error | $\mathbb{E}_\theta[(T - \psi(\theta))^2] = \operatorname{Var}_\theta(T) + \operatorname{bias}_\theta(T)^2$ | [mean squared error](/mean-squared-error/) |
| consistency | $P_\theta(\lvert T_n - \psi(\theta) \rvert > \varepsilon) \to 0$ for each $\varepsilon > 0$ | [consistent estimator](/consistent-estimator/) |
| risk | $R(\theta, T) = \mathbb{E}_\theta[L(T, \psi(\theta))]$ for a [loss function](/loss-function/) $L$ | [statistical decision theory](/statistical-decision-theory/) |

**No estimator is best at every $\theta$.** Fix $\theta_0 \in \Theta$ and let $T \equiv \psi(\theta_0)$, a constant. Its mean squared error is $0$ at $\theta = \theta_0$. So an estimator with the smallest mean squared error at every $\theta$ would have mean squared error $0$ at every $\theta$: $T = \psi(\theta)$ with $P_\theta$-probability 1 for each $\theta$. Take $\theta_1, \theta_2$ with $\psi(\theta_1) \ne \psi(\theta_2)$. The events $A_1 = \{T = \psi(\theta_1)\}$ and $A_2 = \{T = \psi(\theta_2)\}$ are disjoint, $P_{\theta_1}(A_1) = 1$ and $P_{\theta_2}(A_2) = 1$, so $P_{\theta_2}(A_1) = 0$: the two laws of the data are mutually singular. In most models they are not (two normal laws have positive densities on the same set), so no such estimator exists. Theory therefore compares estimators inside a class (unbiased estimators, as in [minimum variance unbiased estimator](/minimum-variance-unbiased-estimator/)), or by one number for each estimator: an average risk (Bayes) or the largest risk (minimax). See [admissible estimator](/admissible-estimator/).

## Examples and non-examples

The sample $x = (3, 7, 7, 9, 14)$ serves as a running example on the pages of this sub-area.

- **Three estimators of one mean.** For iid data with mean $\mu$, the sample mean $\bar X = \frac1n \sum_i X_i$, the sample [median](/median/) and the midrange $\frac12(\min_i X_i + \max_i X_i)$ are estimators of $\mu$. On $x$ they give the estimates $8$, $7$ and $8.5$. All three are unbiased when the distribution is symmetric about $\mu$ and the means exist. They differ in their standard errors, and so in their mean squared error.
- **Two estimators of a variance.** The [sample variance](/sample-variance/) $S^2 = \frac{1}{n - 1} \sum_i (X_i - \bar X)^2$ (divisor $n - 1$) gives $64/4 = 16$ on $x$. The version with divisor $n$ gives $64/5 = 12.8$. Both are estimators of $\sigma^2$; only the first is unbiased.
- **The uniform model.** For iid Uniform$(0, \theta)$ data, $\max_i X_i$, $\frac{n + 1}{n} \max_i X_i$ and $2 \bar X$ are estimators of $\theta$. On $x$ they give $14$, $16.8$ and $16$.
- **A proportion.** For iid Bernoulli$(p)$ data, $\bar X$ is the sample proportion, an estimator of $p$.
- **A function of the parameter.** For iid Bernoulli$(p)$ data, $\bar X (1 - \bar X)$ is an estimator of $\psi(p) = p(1 - p)$, the variance of one observation.
- **A constant.** $T \equiv 5$ is an estimator of $\mu$. It is a statistic, so it meets the definition. Its bias $5 - \mu$ is unbounded over $\mu \in \mathbb{R}$, and it ignores the data.
- **Non-example: a function of the parameter.** $\bar X - \mu$ and $(\bar X - \mu)/(S/\sqrt n)$ are not statistics when $\mu$ is unknown, because their values need $\mu$. They are *pivots*: random variables whose distribution does not depend on the parameter, used to build a [confidence interval](/confidence-interval/).
- **Non-example: the parameter.** $\theta$ is a fixed unknown number, not a function of the data.
- **Non-example: an estimate.** The number $8$ is an estimate. It has no bias and no standard error. Those are properties of the rule $\bar X$ over repeated samples.

## Related definitions

- [Sampling distribution](/sampling-distribution/): the distribution of $T$ under $P_\theta$. Every measure in the table above is a property of it.
- [Bias of an estimator](/estimator-bias/), [standard error](/standard-error/), [consistent estimator](/consistent-estimator/) and [mean squared error](/mean-squared-error/): the location, the spread, the large-sample behaviour and the total squared error of $T$.
- Interval estimator: a pair of statistics $(L, U)$ with a coverage statement, as in [confidence interval](/confidence-interval/). A point estimator gives one value.
- [Sufficient statistic](/sufficient-statistic/): a statistic that keeps all the information about $\theta$ in the sample; the [Rao-Blackwell theorem](/rao-blackwell-theorem/) improves an estimator by conditioning on one.
- Ways to construct estimators: [maximum likelihood](/maximum-likelihood-estimation/) (from the [likelihood function](/likelihood-function/)), the [method of moments](/method-of-moments/), [M-estimators](/m-estimator/), and the [MAP estimate](/maximum-a-posteriori-estimation/) of Bayesian inference.
- [Statistical decision theory](/statistical-decision-theory/): an estimator as a decision rule, judged by its risk function.

## References
