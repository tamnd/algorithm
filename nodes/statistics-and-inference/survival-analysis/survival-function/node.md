---
tag: 60R77Q
kind: definition
slug: survival-function
name: Survival function
aliases:
- survivor function
- reliability function
area: statistics-and-inference/survival-analysis
level: intro
summary: S(t) = P(T > t), the probability that the event time T exceeds t. It equals one minus the distribution function.
prereqs: [random-variable, probability-distribution]
see_also: [hazard-function, kaplan-meier-estimator, empirical-distribution-function, censoring, quantile, expected-value, geometric-distribution, turnbull-estimator]
sources:
  - book: isbn:9780387953991
    title: John P. Klein and Melvin L. Moeschberger, Survival Analysis, Techniques for Censored and Truncated Data, 2nd edition, Springer, 2003
    locator: Chapter 2 (the survival function, the hazard, the mean residual life and common parametric models, for continuous and discrete times)
  - book: isbn:9780471363576
    title: John D. Kalbfleisch and Ross L. Prentice, The Statistical Analysis of Failure Time Data, 2nd edition, Wiley, 2002
    locator: Chapter 2 (failure time models, the survivor function and the hazard in continuous and discrete time)
---

The survival function of a nonnegative [random variable](/random-variable/) $T$, the time until some event, gives for each $t$ the probability that the event has not happened by time $t$: $S(t) = P(T > t)$. It carries the same information as the distribution function $F(t) = P(T \le t)$, since $S = 1 - F$, but it is the natural scale in survival analysis, where the questions are about who is still event-free, and where [censored](/censoring/) data are summarized by an estimate of $S$, the [Kaplan-Meier](/kaplan-meier-estimator/) curve. It is equivalent to the [hazard](/hazard-function/), the event rate among those still at risk, and its integral is the mean.

## Definition

Let $T$ be a random variable with values in $[0, \infty)$. Its survival function is

$$S(t) = P(T > t) = 1 - F(t), \qquad t \ge 0.$$

Every survival function has these properties, and every function with them is the survival function of some $T \ge 0$, possibly with an atom at $+\infty$:

1. $S$ is nonincreasing.
2. $S$ is right-continuous, and $S(t-) = P(T \ge t)$, so $S(t-) - S(t) = P(T = t)$.
3. $S(t) \le 1$ for all $t$, and $S(0-) = 1$.
4. $\lim_{t \to \infty} S(t) = P(T = \infty)$, which is $0$ for a proper time. A positive limit, such as a fraction of patients who are cured, makes $S$ improper.

**Mean and restricted mean.** For $T \ge 0$, writing $T = \int_0^\infty 1\{T > t\}\, dt$ and taking expectations (Tonelli's theorem) gives

$$E[T] = \int_0^\infty S(t)\, dt,$$

finite or infinite. When $S$ cannot be estimated over its whole range, as when follow-up ends at $\tau$, the restricted mean $E[\min(T, \tau)] = \int_0^\tau S(t)\, dt$ is used instead. For integer $T$, $E[T] = \sum_{t \ge 0} S(t)$.

**Quantiles and conditional survival.** The median survival time is $\inf\{t : S(t) \le 1/2\}$, and other [quantiles](/quantile/) are defined the same way. The probability of surviving another $s$ units given survival to $t$ is

$$P(T > t + s \mid T > t) = \frac{S(t + s)}{S(t)}, \qquad S(t) > 0.$$

**Discrete time.** If $T$ takes values $t_1 < t_2 < \cdots$, with discrete hazards $h_j = P(T = t_j \mid T \ge t_j)$, then surviving past $t$ means getting past each $t_j \le t$ in turn, and

$$S(t) = \prod_{j :\, t_j \le t} (1 - h_j).$$

The Kaplan-Meier estimator is this product with $h_j$ replaced by $d_j / n_j$, the events at $t_j$ over the number at risk.

## Examples and non-examples

**A discrete example.** Let $T$ be uniform on $\{1, 2, 3, 4\}$. Then $S(t) = 1, \frac34, \frac12, \frac14, 0$ on $[0, 1), [1, 2), [2, 3), [3, 4), [4, \infty)$. The mean is $\sum_{t \ge 0} S(t) = 1 + \frac34 + \frac12 + \frac14 = \frac52$, which matches $(1 + 2 + 3 + 4)/4$. The discrete hazards are $h_1 = \frac14$, $h_2 = \frac{1/4}{3/4} = \frac13$, $h_3 = \frac12$ and $h_4 = 1$, and $(1 - \frac14)(1 - \frac13)(1 - \frac12) = \frac14 = S(3)$. The median is 2, the first $t$ with $S(t) \le 1/2$.

**Exponential.** $S(t) = e^{-\lambda t}$ for a rate $\lambda > 0$. The mean is $\int_0^\infty e^{-\lambda t}\, dt = 1/\lambda$ and the median is $\log 2 / \lambda$. The conditional survival $S(t + s)/S(t) = e^{-\lambda s} = S(s)$ does not depend on $t$: the exponential is the only continuous distribution without memory. Its discrete counterpart is the [geometric distribution](/geometric-distribution/), with $S(t) = (1 - p)^t$ on the integers.

**Weibull.** $S(t) = \exp(-(\lambda t)^k)$ with shape $k > 0$. For $k > 1$ the conditional survival $S(t + s)/S(t)$ falls with $t$, which describes wear-out; for $k < 1$ it rises with $t$, which describes early failures that thin out a weak subpopulation. $k = 1$ is the exponential.

**A cure model.** $S(t) = \pi + (1 - \pi) e^{-\lambda t}$ with $0 < \pi < 1$: a fraction $\pi$ never has the event. $S$ is improper, with limit $\pi$, and the mean is infinite, while the restricted mean $\int_0^\tau S(t)\, dt = \pi\tau + (1 - \pi)(1 - e^{-\lambda\tau})/\lambda$ is finite.

**Non-examples.**

- **An estimate.** A Kaplan-Meier curve is a step function computed from a sample. It estimates $S$, it drops only at observed event times, and it may stop above 0 when the largest time is censored, which does not mean that $S$ is improper.
- **The empirical distribution complemented.** Without censoring, one minus the [empirical distribution function](/empirical-distribution-function/) is the natural estimate of $S$. With censoring, one minus the EDF of the observed times estimates $P(\min(T, C) > t) = S(t) G(t)$ for independent $C$ with survival $G$, which is lower than $S(t)$.
- **$P(T \ge t)$.** Some texts define the survival function as $P(T \ge t)$, which is left-continuous. For continuous $T$ the two agree. For discrete $T$ they differ at the atoms, and formulas taken from different sources must use the same convention.
- **A density.** $S$ is a probability, not a rate. $S(5) = 0.6$ means that 60% of subjects are event-free at time 5, not that 60% have the event near time 5.

## Related definitions

- **Hazard.** The [hazard](/hazard-function/) $h(t) = f(t)/S(t)$ is the event rate among those still at risk. With the cumulative hazard $H(t) = \int_0^t h(u)\, du$, a continuous $T$ has $S(t) = \exp(-H(t))$, so any one of $S$, $f$, $h$ and $H$ determines the others.
- **Distribution function and quantiles.** $S = 1 - F$, so every statement about $F$ in [probability distributions](/probability-distribution/) translates directly. The $p$-quantile of $T$ is the first $t$ where $S$ falls to $1 - p$ or below.
- **Mean residual life.** $m(t) = E[T - t \mid T > t] = \int_t^\infty S(u)\, du / S(t)$, the expected remaining time for a subject who has reached $t$. It equals $1/\lambda$ for every $t$ in the exponential case.
- **Estimation under censoring.** The [Kaplan-Meier estimator](/kaplan-meier-estimator/) for right-censored data and the [Turnbull estimator](/turnbull-estimator/) for interval-censored data estimate $S$ without a model. [Censoring](/censoring/) describes what these data contain.
- **Expectation.** The mean formula is a case of the tail-sum formula for the [expected value](/expected-value/) of a nonnegative variable.

## References
