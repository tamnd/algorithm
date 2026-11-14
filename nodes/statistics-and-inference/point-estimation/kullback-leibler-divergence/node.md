---
tag: 51K26E
kind: definition
slug: kullback-leibler-divergence
name: Kullback-Leibler divergence
aliases:
- KL divergence
- relative entropy
- information divergence
area: statistics-and-inference/point-estimation
level: core
summary: The expected log ratio of two densities under the first one. It is never negative, is zero only for equal laws, is not symmetric, and the MLE minimizes its empirical version.
prereqs: [shannon-entropy, likelihood-function]
see_also: [cross-entropy-loss, bregman-divergence, total-variation-distance, evidence-lower-bound, variational-inference, asymptotic-normality-of-mle, fisher-information-matrix, akaike-information-criterion]
sources:
  - paper: doi:10.1214/aoms/1177729694
    title: S. Kullback and R. A. Leibler, On information and sufficiency, Annals of Mathematical Statistics 22(1), 1951
    locator: pages 79 to 86 (definition of the mean information for discrimination and the divergence, and their properties)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 2, Section 2.3 (relative entropy), Section 2.5 (chain rule) and Theorem 2.6.3 (information inequality); Chapter 11, Section 11.6 (Pinsker's inequality)
  - paper: "H. White, Maximum likelihood estimation of misspecified models, Econometrica 50(1), 1982"
    locator: pages 1 to 25 (the quasi-maximum likelihood estimator converges to the minimizer of the Kullback-Leibler divergence)
---

The Kullback-Leibler divergence $D(P \,\|\, Q)$ measures how much a probability law $Q$ differs from a law $P$, seen from the side of $P$. It is the expected log [likelihood](/likelihood-function/) ratio of $P$ to $Q$ when the data come from $P$. It is zero only when the two laws are equal and is positive otherwise, but it is not symmetric and it does not obey the triangle inequality, so it is not a distance. In statistics it is the target that [maximum likelihood](/maximum-likelihood-estimation/) estimates: the MLE minimizes an empirical version of $D(P \,\|\, Q_\theta)$ over the model, and its local curvature is the [Fisher information](/fisher-information-matrix/).

## Definition

Let $P$ and $Q$ be probability laws on the same space.

**Discrete case.** If $P$ and $Q$ have probability mass functions $p$ and $q$ on a countable set,

$$D(P \,\|\, Q) = \sum_{x} p(x)\,\log\frac{p(x)}{q(x)},$$

with the conventions $0\log(0/q) = 0$ for every $q \ge 0$ and $p\log(p/0) = +\infty$ for $p > 0$.

**Densities.** If $P$ and $Q$ have densities $p$ and $q$ with respect to a common measure $\mu$ (Lebesgue measure, counting measure, or $\mu = P + Q$),

$$D(P \,\|\, Q) = \int p(x)\,\log\frac{p(x)}{q(x)}\,\mu(dx) = \mathrm E_P\!\left[\log\frac{p(X)}{q(X)}\right].$$

**General case.** If $P$ is absolutely continuous with respect to $Q$ (every event with $Q(A) = 0$ also has $P(A) = 0$), then $D(P \,\|\, Q) = \mathrm E_P[\log (dP/dQ)]$, where $dP/dQ$ is the Radon-Nikodym derivative. Otherwise $D(P \,\|\, Q) = +\infty$.

The value lies in $[0, +\infty]$. With the natural log the unit is the nat; with $\log_2$ it is the bit. For a parametric family $f(x; \theta)$ we write $D(\theta_0 \,\|\, \theta)$ for $D(f(\cdot; \theta_0) \,\|\, f(\cdot; \theta))$.

### Properties

**Gibbs inequality.** $D(P \,\|\, Q) \ge 0$, with equality if and only if $P = Q$.

*Proof.* It suffices to treat the case where $D(P \,\|\, Q)$ is finite, so $q(x) > 0$ wherever $p(x) > 0$. Let $A = \{x : p(x) > 0\}$. For $u > 0$, $\log u \le u - 1$, with equality only at $u = 1$. Put $u = q(x)/p(x)$ for $x \in A$:

$$-D(P \,\|\, Q) = \int_A p\,\log\frac{q}{p}\,d\mu \le \int_A p\left(\frac{q}{p} - 1\right)d\mu = Q(A) - 1 \le 0.$$

Equality in the first step needs $q = p$ almost everywhere on $A$, and equality in the second needs $Q(A) = 1$. Together they give $q = p$ almost everywhere, so $P = Q$. $\blacksquare$

The integral in the first line is well defined, because its integrand is bounded above by the integrable function $q - p$.

**Not symmetric.** In general $D(P \,\|\, Q) \ne D(Q \,\|\, P)$; one can be finite while the other is infinite. The symmetric sum $D(P \,\|\, Q) + D(Q \,\|\, P)$ is what Kullback and Leibler called the divergence in 1951; today "KL divergence" means the one-sided quantity.

**Additive over independent coordinates.** If $P = P_1 \times P_2$ and $Q = Q_1 \times Q_2$, then $D(P \,\|\, Q) = D(P_1 \,\|\, Q_1) + D(P_2 \,\|\, Q_2)$, because the log of a product is a sum. For $n$ iid observations, $D(P^n \,\|\, Q^n) = n\,D(P \,\|\, Q)$.

**Local form.** If the family $f(x; \theta)$ satisfies the regularity conditions of [Fisher information](/fisher-information-matrix/) (enough smoothness to differentiate twice under the integral sign), then

$$D(\theta \,\|\, \theta + h) = \tfrac12\,h^{\mathsf T} I(\theta)\,h + o(\|h\|^2),$$

where $I(\theta)$ is the Fisher information of one observation. The first-order term vanishes because the [score](/score-function/) has mean zero, and the second-order term is the mean of minus the Hessian of $\log f$.

**Pinsker's inequality.** The [total variation distance](/total-variation-distance/) satisfies $\sup_A |P(A) - Q(A)| \le \sqrt{D(P \,\|\, Q)/2}$, with $D$ in nats (Cover and Thomas, Section 11.6). So a small divergence forces the two laws to give nearly equal probabilities to every event.

**Entropy and cross entropy.** For discrete laws, $D(P \,\|\, Q) = H(P, Q) - H(P)$, where $H(P) = -\sum p\log p$ is the [Shannon entropy](/shannon-entropy/) and $H(P, Q) = -\sum p\log q$ is the cross entropy. Minimizing [cross-entropy loss](/cross-entropy-loss/) over $Q$ with $P$ fixed is the same as minimizing $D(P \,\|\, Q)$.

**Maximum likelihood minimizes an empirical divergence.** Let $X_1, \ldots, X_n$ be iid from a law with density $g$, and let $\{f(\cdot; \theta)\}$ be a model that may not contain $g$. Then

$$D(g \,\|\, f_\theta) = \mathrm E_g[\log g(X)] - \mathrm E_g[\log f(X; \theta)].$$

The first term does not depend on $\theta$, so minimizing $D(g \,\|\, f_\theta)$ is the same as maximizing $\mathrm E_g[\log f(X; \theta)]$, and the MLE maximizes the sample mean $n^{-1}\sum \log f(X_i; \theta)$ of that expectation. Under regularity conditions the MLE converges almost surely to the minimizer $\theta^*$ of $D(g \,\|\, f_\theta)$ (White 1982). When the model is correct, $\theta^* = \theta_0$ by the Gibbs inequality, which is the core of consistency proofs for the MLE.

## Examples and non-examples

**Two Bernoulli laws.** $D(\mathrm{Bern}(0.5) \,\|\, \mathrm{Bern}(0.1)) = 0.5\log 5 + 0.5\log(5/9) = \log(5/3) = 0.51083$ nats, while $D(\mathrm{Bern}(0.1) \,\|\, \mathrm{Bern}(0.5)) = 0.36806$ nats. The two directions differ.

**An exact asymmetric example in bits.** On four points let $p = (1/2, 1/4, 1/8, 1/8)$ and $q = (1/8, 1/2, 1/4, 1/8)$. Every ratio is a power of 2, so the logs in base 2 are integers and the sums are exact rationals:

$$D(p \,\|\, q) = \tfrac12\cdot 2 + \tfrac14\cdot(-1) + \tfrac18\cdot(-1) + \tfrac18\cdot 0 = \tfrac58 \text{ bit}, \qquad D(q \,\|\, p) = \tfrac18\cdot(-2) + \tfrac12\cdot 1 + \tfrac14\cdot 1 + \tfrac18\cdot 0 = \tfrac12 \text{ bit}.$$

**One direction infinite.** Let $p = (1/2, 1/2, 0)$ and $q = (1/4, 1/4, 1/2)$. Then $D(p \,\|\, q) = 1$ bit, but $D(q \,\|\, p) = +\infty$, because $q$ puts mass $1/2$ on a point where $p$ is zero. A model that gives probability zero to an event that can happen is infinitely far from the truth in this direction.

**Normal laws.** For $N(\mu_1, \sigma_1^2)$ and $N(\mu_2, \sigma_2^2)$,

$$D = \log\frac{\sigma_2}{\sigma_1} + \frac{\sigma_1^2 + (\mu_1 - \mu_2)^2}{2\sigma_2^2} - \frac12.$$

With equal variances $\sigma^2$ this is $(\mu_1 - \mu_2)^2/(2\sigma^2)$, which is exactly $\tfrac12 h^2 I(\mu)$ with $h = \mu_2 - \mu_1$ and $I = 1/\sigma^2$. The local form is exact here.

**Local form for a Bernoulli law.** For $\mathrm{Bern}(0.3)$ the Fisher information is $1/(0.3 \cdot 0.7)$. At $h = 0.1$, $D(\mathrm{Bern}(0.3) \,\|\, \mathrm{Bern}(0.4)) = 0.021601$ nats against $\tfrac12 h^2 I = 0.023810$; at $h = 0.01$ the values are 0.00023517 and 0.00023810.

**Pinsker's inequality.** For $P = \mathrm{Bern}(0.5)$ and $Q = \mathrm{Bern}(0.75)$, $D(P \,\|\, Q) = 0.143841$ nats and the total variation distance is 0.25, below the bound $\sqrt{0.143841/2} = 0.26818$.

**A misspecified model.** Let the data come from a Gamma law with shape 2 and rate 1 (mean 2), and fit the exponential model $f(x; \lambda) = \lambda e^{-\lambda x}$. Then $\mathrm E[\log f(X; \lambda)] = \log\lambda - 2\lambda$, which is largest at $\lambda^* = 1/2$. The exponential MLE $1/\bar X$ converges almost surely to $1/2$, the rate of the exponential law closest to the Gamma law in Kullback-Leibler divergence.

**Non-example: not a metric.** The divergence is not symmetric (see above), and it does not satisfy the triangle inequality. For Bernoulli laws with success probabilities $0.1$, $0.5$ and $0.9$, $D(0.1 \,\|\, 0.5) + D(0.5 \,\|\, 0.9) = 0.36806 + 0.51083 = 0.87889$, but $D(0.1 \,\|\, 0.9) = 0.8\log 9 = 1.75778$ nats.

**Non-example: a difference of entropies.** $D(P \,\|\, Q)$ is not $H(Q) - H(P)$. Two laws with the same entropy, such as $p$ and a permutation of $p$, have equal entropies but positive divergence when the permutation moves mass.

## Related definitions

- [Shannon entropy](/shannon-entropy/): $H(P)$; the divergence from $P$ to the uniform law on $m$ points is $\log m - H(P)$.
- [Cross-entropy loss](/cross-entropy-loss/): $H(P, Q) = H(P) + D(P \,\|\, Q)$.
- [Bregman divergence](/bregman-divergence/): the KL divergence between members of an [exponential family](/exponential-family-distribution/) is a Bregman divergence of the log-partition function.
- [Total variation distance](/total-variation-distance/): bounded by the square root of half the divergence (Pinsker).
- [Fisher information](/fisher-information-matrix/): the Hessian of $D(\theta_0 \,\|\, \theta)$ at $\theta = \theta_0$.
- [Evidence lower bound](/evidence-lower-bound/) and [variational inference](/variational-inference/): fit an approximation $Q$ by minimizing $D(Q \,\|\, P)$, the reverse direction.
- [Akaike information criterion](/akaike-information-criterion/): an estimate of the expected divergence of a fitted model, up to a constant.
- [Asymptotic normality of the MLE](/asymptotic-normality-of-mle/): uses the Gibbs inequality for identifiability and consistency.

## References
