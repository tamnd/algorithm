---
tag: 1RSZPR
kind: definition
slug: complete-statistic
name: Complete statistic
aliases:
- completeness of a statistic
area: statistics-and-inference/point-estimation
level: advanced
summary: A statistic T such that E g(T) = 0 for every parameter forces g(T) = 0 almost surely. Completeness makes unbiased functions of T unique.
prereqs: [sufficient-statistic, fisher-neyman-factorization-theorem, exponential-family-distribution, expected-value]
see_also: [lehmann-scheffe-theorem, rao-blackwell-theorem, minimum-variance-unbiased-estimator, order-statistic, estimator-bias]
sources:
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 6.2.4 (Definition 6.2.21, Basu's theorem 6.2.24, Theorem 6.2.25 on exponential families, Theorem 6.2.28 on minimal sufficiency)
  - book: isbn:9780387985022
    title: E. L. Lehmann and George Casella, Theory of Point Estimation, second edition, Springer, 1998
    locator: Chapter 1, Section 1.6 (completeness and Basu's theorem)
  - paper: "E. L. Lehmann and Henry Scheffé, Completeness, similar regions, and unbiased estimation, Part I, Sankhya 10 (1950)"
    title: Lehmann and Scheffé 1950
    locator: the definition of completeness and its use for unbiased estimation
  - paper: "D. Basu, On statistics independent of a complete sufficient statistic, Sankhya 15 (1955)"
    title: Basu 1955
    locator: the independence of a boundedly complete sufficient statistic and an ancillary statistic
---

A complete statistic is a statistic $T$ such that the only function of $T$ with mean zero under every parameter value is the zero function. Completeness says that the family of distributions of $T$ is rich enough that an expectation identity in $\theta$ pins down the function. Together with [sufficiency](/sufficient-statistic/) it gives the uniqueness part of the [Lehmann-Scheffé theorem](/lehmann-scheffe-theorem/): an unbiased estimator that is a function of a complete sufficient statistic is the [minimum variance unbiased estimator](/minimum-variance-unbiased-estimator/). Lehmann and Scheffé (1950) introduced the idea, and Basu (1955) used it to prove independence results.

## Definition

The sample $X$ has distribution $P_\theta$, $\theta \in \Theta$, and $T = t(X)$ is a statistic.

**Complete statistic.** $T$ is **complete** for the family $\{P_\theta : \theta \in \Theta\}$ when, for every measurable function $g$ with $\mathbb{E}_\theta \lvert g(T) \rvert < \infty$ for all $\theta$,

$$\mathbb{E}_\theta\, g(T) = 0 \ \text{ for every } \theta \in \Theta \quad \Longrightarrow \quad P_\theta(g(T) = 0) = 1 \ \text{ for every } \theta \in \Theta.$$

Strictly, completeness is a property of the family of distributions of $T$, $\{P_\theta \circ t^{-1} : \theta \in \Theta\}$.

**Boundedly complete statistic.** $T$ is **boundedly complete** when the same implication holds for every bounded measurable $g$. Every complete statistic is boundedly complete.

**Why it matters for estimation.** If $T$ is complete and $\delta_1(T)$, $\delta_2(T)$ are both unbiased for $\psi(\theta)$, then $g = \delta_1 - \delta_2$ has mean zero for every $\theta$, so $\delta_1(T) = \delta_2(T)$ with probability 1. A complete statistic carries at most one unbiased estimator of each $\psi(\theta)$. A function $g(T)$ with $\mathbb{E}_\theta\, g(T) = 0$ for all $\theta$ is an *unbiased estimator of zero*; completeness says that $T$ has no nonzero one.

### Properties

**(a) Exponential families.** Let $X_1, \ldots, X_n$ be iid with density $h(x)\exp(\eta^\top T(x) - A(\eta))$ in natural form, $\eta \in \mathcal H \subseteq \mathbb R^k$. If $\mathcal H$ contains an open set of $\mathbb R^k$ (a full-rank family), then $\sum_i T(X_i)$ is complete and sufficient (Casella and Berger, Theorem 6.2.25). The proof uses the uniqueness of the two-sided Laplace transform. See [exponential family](/exponential-family-distribution/).

**(b) Complete sufficient statistics are minimal.** If $T$ is complete and sufficient, and a minimal sufficient statistic exists, then $T$ is minimal sufficient (Bahadur 1957; Casella and Berger, Theorem 6.2.28).

**(c) Basu's theorem.** If $T$ is boundedly complete and sufficient, and $V$ is ancillary (its distribution does not depend on $\theta$), then $T$ and $V$ are independent under every $\theta$.

*Proof.* Fix a set $A$ and let $c = P_\theta(V \in A)$, which does not depend on $\theta$. Let $\eta(T) = P(V \in A \mid T)$; by sufficiency it does not depend on $\theta$, so it is a statistic, and it is bounded. By the tower property, $\mathbb{E}_\theta[\eta(T) - c] = P_\theta(V \in A) - c = 0$ for every $\theta$. Bounded completeness gives $\eta(T) = c$ with probability 1. So $P_\theta(V \in A \mid T) = P_\theta(V \in A)$ for every $A$, which is independence. $\square$

**(d) Functions of a complete statistic.** If $T$ is complete and $U = r(T)$, then $U$ is complete: a function of $U$ is a function of $T$.

## Examples and non-examples

**Binomial.** Let $X_1, \ldots, X_n$ be iid Bernoulli$(p)$, $0 < p < 1$, and $T = \sum_i X_i$. With $r = p/(1-p)$, which runs over $(0, \infty)$,

$$\mathbb{E}_p\, g(T) = (1-p)^n \sum_{t=0}^n g(t) \binom{n}{t} r^t.$$

If this is zero for all $p$, the polynomial $\sum_t g(t)\binom{n}{t} r^t$ is zero on $(0, \infty)$, so all its coefficients are zero and $g(t) = 0$ for $t = 0, \ldots, n$. So $T$ is complete.

**Poisson.** Let $X_1, \ldots, X_n$ be iid Poisson$(\lambda)$, $\lambda > 0$, and $T = \sum_i X_i \sim$ Poisson$(n\lambda)$. Then $\mathbb{E}_\lambda\, g(T) = e^{-n\lambda} \sum_{t \ge 0} g(t)(n\lambda)^t / t!$. A power series that is zero on $(0, \infty)$ has all coefficients zero, so $g(t) = 0$ for every $t$ and $T$ is complete.

**Uniform.** Let $X_1, \ldots, X_n$ be iid Uniform$(0, \theta)$ and $T = \max_i X_i$, with density $n t^{n-1}/\theta^n$ on $(0, \theta)$. If $\int_0^\theta g(t)\, t^{n-1}\, dt = 0$ for every $\theta > 0$, then differentiation in $\theta$ gives $g(\theta)\theta^{n-1} = 0$ for almost every $\theta$, so $T$ is complete. This family is not an exponential family; completeness can hold without one.

**Normal.** For iid $N(\mu, \sigma^2)$ with both parameters unknown, the natural parameter $(\mu/\sigma^2, -1/(2\sigma^2))$ ranges over an open half-plane, so $(\sum_i X_i, \sum_i X_i^2)$ is complete, and so is the equivalent pair $(\bar X, S^2)$, with divisor $n - 1$ in $S^2$. With $\sigma^2$ fixed, $\bar X$ is complete sufficient for $\mu$, and $S^2$ is ancillary for $\mu$. Basu's theorem then gives the independence of $\bar X$ and $S^2$ for each $\sigma^2$, which is the standard short proof of this fact.

**Non-example: a curved family.** Let $X_1, \ldots, X_n$ be iid $N(\theta, \theta^2)$, $\theta > 0$. The pair $(\bar X, S^2)$ is still minimal sufficient, but $\mathbb{E}_\theta \bar X^2 = \theta^2 + \theta^2/n$ and $\mathbb{E}_\theta S^2 = \theta^2$, so

$$g = \frac{n}{n+1}\bar X^2 - S^2$$

has mean zero for every $\theta$ and is not zero. The natural parameter $(1/\theta, -1/(2\theta^2))$ lies on a curve, which contains no open set of $\mathbb R^2$.

**Non-example: a location family with known width.** Let $X_1, \ldots, X_n$ be iid Uniform$(\theta, \theta + 1)$, $n \ge 2$. The minimal sufficient statistic is $(X_{(1)}, X_{(n)})$. The range $R = X_{(n)} - X_{(1)}$ is ancillary, with mean $(n-1)/(n+1)$ for every $\theta$. So $g = R - (n-1)/(n+1)$ is a nonzero function of the minimal sufficient statistic with mean zero, and $(X_{(1)}, X_{(n)})$ is not complete. In such a family no complete sufficient statistic exists, by property (b).

**Non-example: too few parameter values.** Let $X_1, X_2$ be iid Bernoulli$(p)$ with $p \in \{1/4, 1/2\}$ only, and $T = X_1 + X_2$. The function $g(0) = 1$, $g(1) = -2$, $g(2) = 3$ has $\mathbb{E}_p\, g(T) = (9 - 12 + 3)/16 = 0$ at $p = 1/4$ and $(1 - 4 + 3)/4 = 0$ at $p = 1/2$. Completeness depends on the parameter set: the same $T$ is complete when $p$ ranges over $(0, 1)$.

**Boundedly complete but not complete.** Let $X$ take the value $-1$ with probability $\theta$ and the value $k \in \{0, 1, 2, \ldots\}$ with probability $(1-\theta)^2\theta^k$, for $0 < \theta < 1$. Since $\sum_{k \ge 1} k\theta^k = \theta/(1-\theta)^2$, the condition $\mathbb{E}_\theta\, g(X) = 0$ for all $\theta$ becomes $\sum_{k \ge 0}\theta^k\,(g(k) + k\, g(-1)) = 0$, so $g(k) = -k\, g(-1)$. The choice $g(-1) = 1$, $g(k) = -k$ is a nonzero unbiased estimator of zero, so $X$ is not complete. It is unbounded; a bounded $g$ forces $g(-1) = 0$ and then $g = 0$, so $X$ is boundedly complete.

**A trivial complete statistic.** A constant statistic is complete, because $\mathbb{E}_\theta\, g(c) = g(c) = 0$ forces $g(c) = 0$. Completeness alone says nothing about information; it is useful together with sufficiency.

### Pitfalls

- **Completeness is not a property of the sample alone.** It depends on the model and on the parameter set, as the two-point Bernoulli example shows. Removing parameter values can destroy completeness.
- **Minimal sufficient does not imply complete.** The curved normal and the Uniform$(\theta, \theta + 1)$ examples have a minimal sufficient statistic that is not complete.
- **The "almost surely" matters.** Completeness gives $g(T) = 0$ with probability 1 under each $\theta$, not $g = 0$ at every point. For a continuous $T$, $g$ can be changed on a null set.

## Related definitions

- [Sufficient statistic](/sufficient-statistic/): the property that completeness is usually paired with.
- Ancillary statistic: a statistic whose distribution does not depend on $\theta$. By Basu's theorem, it is independent of every boundedly complete sufficient statistic.
- [Lehmann-Scheffé theorem](/lehmann-scheffe-theorem/): an unbiased function of a complete sufficient statistic is the unique [minimum variance unbiased estimator](/minimum-variance-unbiased-estimator/).
- [Rao-Blackwell theorem](/rao-blackwell-theorem/): conditioning on a sufficient statistic improves an estimator; completeness makes the result the same for every unbiased starting point.
- [Estimator bias](/estimator-bias/): an unbiased estimator of zero is an estimator with mean zero for every $\theta$; completeness of $T$ rules out nonzero ones that depend only on $T$.

## References
