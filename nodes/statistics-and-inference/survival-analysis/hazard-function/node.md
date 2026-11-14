---
tag: 76MWP4
kind: definition
slug: hazard-function
name: Hazard function
aliases:
- hazard rate
- force of mortality
area: statistics-and-inference/survival-analysis
level: intro
summary: The instantaneous event rate at t among those still at risk, f(t) / S(t). The cumulative hazard H(t) satisfies S(t) = exp(-H(t)).
prereqs: [survival-function, probability-density-function, conditional-probability]
see_also: [nelson-aalen-estimator, kaplan-meier-estimator, censoring, log-rank-test, cox-proportional-hazards-model, competing-risks, frailty-model, poisson-distribution]
sources:
  - book: isbn:9780387953991
    title: John P. Klein and Melvin L. Moeschberger, Survival Analysis, Techniques for Censored and Truncated Data, 2nd edition, Springer, 2003
    locator: Chapter 2 (the hazard function and the cumulative hazard, their relations to the survival function and the density, and the hazards of common parametric models)
  - book: isbn:9780471363576
    title: John D. Kalbfleisch and Ross L. Prentice, The Statistical Analysis of Failure Time Data, 2nd edition, Wiley, 2002
    locator: Chapter 2 (the hazard in continuous and discrete time and the product-integral form of the survivor function)
---

The hazard function of an event time $T$ gives, at each time $t$, the rate at which events happen among the subjects who have not yet had one. If $h(t) = 0.02$ per day, then about 2% of those still at risk at day $t$ have the event during the next day, when the hazard is roughly constant over that day. The hazard is the natural object of survival analysis for three reasons. It describes how risk changes with time, rising with wear-out and falling after a dangerous early period. [Censoring](/censoring/) that is independent of the event leaves it unchanged among those still observed, so it can be estimated from the risk sets. And covariates multiply it by a constant factor in the main regression model, the [Cox model](/cox-proportional-hazards-model/). The hazard determines the [survival function](/survival-function/) through the cumulative hazard $H$.

## Definition

**Continuous time.** Let $T \ge 0$ have a [density](/probability-density-function/) $f$ and survival function $S(t) = P(T > t)$. The hazard function is

$$h(t) = \lim_{\Delta \downarrow 0} \frac{P(t \le T < t + \Delta \mid T \ge t)}{\Delta} = \frac{f(t)}{S(t)}, \qquad S(t) > 0,$$

the [conditional](/conditional-probability/) probability of an event in a short interval after $t$, given that none happened before $t$, per unit of time. The cumulative hazard is

$$H(t) = \int_0^t h(u)\, du.$$

Since $f = -S'$, the hazard is $h = -S'/S = -(\log S)'$, and integrating from 0 with $S(0) = 1$ gives

$$S(t) = \exp(-H(t)), \qquad f(t) = h(t)\exp(-H(t)).$$

So any one of $S$, $f$, $h$ and $H$ determines the others. Conversely, any function $h \ge 0$ with $\int_0^t h < \infty$ for each $t$ is the hazard of some $T$, which is proper when $\int_0^\infty h = \infty$. A hazard has units of one over time, and it can exceed 1.

**Discrete time.** If $T$ takes values $t_1 < t_2 < \cdots$, the hazard at $t_j$ is the probability

$$h_j = P(T = t_j \mid T \ge t_j),$$

the cumulative hazard is $H(t) = \sum_{t_j \le t} h_j$, and

$$S(t) = \prod_{t_j \le t} (1 - h_j).$$

Here $S \ne \exp(-H)$: since $-\log(1 - x) \ge x$, $S(t) \le \exp(-H(t))$, with near equality when every $h_j$ is small. A general $T$, with both a density part and atoms, has $S(t) = \prod_{u \le t}(1 - dH(u))$, a product integral that reduces to each formula above in its case.

**Proportional hazards.** Two groups have proportional hazards when $h_1(t) = \theta\, h_0(t)$ for all $t$, with a constant hazard ratio $\theta$. Then $H_1 = \theta H_0$ and $S_1 = S_0^\theta$ in continuous time.

## Examples and non-examples

**Uniform on $(0, 1)$.** $f(t) = 1$ and $S(t) = 1 - t$, so $h(t) = 1/(1 - t)$, which grows without bound as $t \to 1$, and $H(t) = -\log(1 - t)$, so $\exp(-H(t)) = 1 - t = S(t)$. At $t = 0.9$ the hazard is 10 per unit time: among those left at 0.9, the events arrive at that rate, and all of them happen within the remaining 0.1.

**A discrete example.** $T$ uniform on $\{1, 2, 3, 4\}$ has $h_1 = \frac14$, $h_2 = \frac13$, $h_3 = \frac12$, $h_4 = 1$. Then $S(3) = \frac34 \cdot \frac23 \cdot \frac12 = \frac14$, while $H(3) = \frac14 + \frac13 + \frac12 = \frac{13}{12}$ and $\exp(-\frac{13}{12}) \approx 0.338$, larger than $S(3)$ as the inequality says.

**Parametric shapes.**

| model | $h(t)$ | $H(t)$ | shape |
|---|---|---|---|
| exponential | $\lambda$ | $\lambda t$ | constant |
| Weibull | $k\lambda(\lambda t)^{k - 1}$ | $(\lambda t)^k$ | rising for $k > 1$, falling for $k < 1$ |
| Gompertz | $a e^{bt}$ | $\frac{a}{b}(e^{bt} - 1)$ | rising exponentially for $b > 0$ |

A constant hazard is the memoryless case. Events in a population with a constant hazard $\lambda$ and total time at risk $L$ are approximately a [Poisson](/poisson-distribution/) count with mean $\lambda L$, and $\hat\lambda = d/L$, events over time at risk, is the maximum likelihood estimate under right censoring. Human mortality has a bathtub shape: high in the first year, lowest in childhood, and then close to Gompertz in adult ages.

**A mixture.** Half of a population has hazard 1 and half has hazard 3. The population survival is $S(t) = \frac12(e^{-t} + e^{-3t})$ and the population hazard is

$$h(t) = \frac{e^{-t} + 3e^{-3t}}{e^{-t} + e^{-3t}} = 1 + \frac{2}{1 + e^{2t}},$$

which falls from 2 at $t = 0$ toward 1, although no individual's hazard changes. The high-risk subjects leave the risk set first. A falling population hazard therefore does not show that risk falls for anyone; [frailty models](/frailty-model/) describe this effect.

**Non-examples.**

- **Not a probability.** In continuous time $h(t)$ is a rate, and $h(t) = 10$ is possible, as in the uniform example. Only $h(t)\Delta$ for a short $\Delta$ approximates a probability. In discrete time $h_j$ is a probability.
- **Not the density.** $f(t)$ is the unconditional rate, relative to everyone at time 0. $h(t)$ is relative to those still at risk. For the uniform on $(0, 1)$ the density is flat while the hazard rises to infinity.
- **The cumulative hazard is not a probability.** $H(t)$ can exceed 1, and $1 - \exp(-H(t))$ is the probability of an event by $t$. $H(t)$ is the expected number of events by $t$ in a Poisson process with intensity $h$, where events recur and the rate at time $t$ is $h(t)$.
- **A hazard ratio is not a ratio of risks.** With $\theta = 2$ and $S_0(t) = 0.5$, the event probabilities by $t$ are $0.5$ and $1 - 0.5^2 = 0.75$, a risk ratio of $1.5$.

## Related definitions

- **Survival function.** $S = \exp(-H)$ in continuous time and $S = \prod(1 - h_j)$ in discrete time; see [survival function](/survival-function/).
- **Estimation.** At each distinct event time $t_j$, with $d_j$ events among $n_j$ at risk, $d_j/n_j$ estimates the discrete hazard. Summing gives the [Nelson-Aalen estimator](/nelson-aalen-estimator/) of $H$, and multiplying $1 - d_j/n_j$ gives the [Kaplan-Meier estimator](/kaplan-meier-estimator/) of $S$. A smooth estimate of $h$ itself needs kernel smoothing of the Nelson-Aalen increments.
- **Comparing groups.** The [log-rank test](/log-rank-test/) tests equality of hazards, and it is the score test of the Cox model with a group indicator, so it is aimed at proportional hazards. The Cox model writes $h(t \mid x) = h_0(t) e^{x^{\mathsf T}\beta}$, with an unspecified baseline $h_0$.
- **Cause-specific hazards.** With several event types, each type has its own hazard $h_k(t)$, the rate of type $k$ events among those still free of all events, and $\sum_k h_k$ is the hazard of the first event. This is the starting point of [competing risks](/competing-risks/).

## References
