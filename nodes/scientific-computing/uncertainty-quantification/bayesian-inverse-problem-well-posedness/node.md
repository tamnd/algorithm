---
tag: ZMDR6F
kind: theorem
slug: bayesian-inverse-problem-well-posedness
name: Well-posedness of Bayesian inverse problems
area: scientific-computing/uncertainty-quantification
level: research
summary: Under mild conditions on the forward map and the prior, the posterior exists and depends Lipschitz continuously on the data in the Hellinger distance.
prereqs: [bayesian-inverse-problem, bayes-theorem, well-posed-problem]
see_also: [total-variation-distance, kullback-leibler-divergence, linear-gaussian-inverse-problem, preconditioned-crank-nicolson-mcmc, forward-operator, karhunen-loeve-theorem, tikhonov-regularization, kennedy-ohagan-calibration]
sources:
  - paper: doi:10.1017/S0962492910000061
    title: Andrew M. Stuart, Inverse problems, a Bayesian perspective, Acta Numerica 19, 2010, 451-559
    locator: the conditions on the potential, the existence of the posterior as a measure with a density with respect to the prior, and its Lipschitz dependence on the data in the Hellinger distance
  - paper: doi:10.1007/978-3-319-12385-1_7
    title: Masoumeh Dashti and Andrew M. Stuart, The Bayesian approach to inverse problems, in Handbook of Uncertainty Quantification, Springer, 2017, 311-428
    locator: the well-posedness of the posterior, the Hellinger distance and its bounds on expectations, and Fernique's theorem for Gaussian measures
  - paper: doi:10.1137/19M1247176
    title: Jonas Latz, On the well-posedness of Bayesian inverse problems, SIAM/ASA Journal on Uncertainty Quantification, 2020
    locator: the transfer of the well-posedness of Hadamard to Bayesian inverse problems, and versions with weaker assumptions and other metrics
---

The well-posedness theorem for [Bayesian inverse problems](/bayesian-inverse-problem/) says that, under mild conditions, the posterior distribution is a stable solution of the inverse problem in the sense of [Hadamard](/well-posed-problem/): it exists, it is unique, and a small change of the data gives a small change of the posterior. The distance is the Hellinger distance between probability measures, and the bound is Lipschitz, locally in the data. The unknown can be a function, so the result holds in infinite dimensions and does not depend on the discretization. This is a contrast with the inverse problem itself: the map from the data to the least squares solution can be discontinuous, and [Tikhonov regularization](/tikhonov-regularization/) is a way to make it stable. In the Bayesian form the prior does this work.

The [linear Gaussian inverse problem](/linear-gaussian-inverse-problem/) is the special case with a linear forward map, where the posterior is Gaussian and the result can be checked by hand. The theorem covers nonlinear forward maps, for which the posterior has no closed form and is sampled, for example by [preconditioned Crank-Nicolson MCMC](/preconditioned-crank-nicolson-mcmc/).

## Statement

**Setting.** Let $X$ be a separable Banach space with the norm $\|\cdot\|$, let the prior $\mu_0$ be a Gaussian measure on $X$, and let the [forward map](/forward-operator/) $\mathcal{G} : X \to \mathbb{R}^J$ be Borel measurable. The data are $y = \mathcal{G}(u) + \eta$ with the noise $\eta \sim N(0, \Gamma)$ independent of $u$, for a symmetric positive definite $\Gamma$. Write $|v|_\Gamma = |\Gamma^{-1/2} v|$ and define the potential

$$\Phi(u; y) = \tfrac12 |y - \mathcal{G}(u)|_\Gamma^2 \ \ge 0 .$$

**Assumption (growth).** For every $\varepsilon > 0$ there is $M(\varepsilon)$ with $|\mathcal{G}(u)|_\Gamma \le \exp(\varepsilon \|u\|^2 + M(\varepsilon))$ for all $u \in X$.

**Hellinger distance.** For probability measures $\mu$ and $\nu$ with densities with respect to $\mu_0$,

$$d_H(\mu, \nu)^2 = \frac12 \int_X \left( \sqrt{\frac{d\mu}{d\mu_0}} - \sqrt{\frac{d\nu}{d\mu_0}} \right)^2 d\mu_0 .$$

**Theorem.** Under the growth assumption:

1. For every $y \in \mathbb{R}^J$, $Z(y) = \int_X \exp(-\Phi(u; y))\, d\mu_0(u)$ lies in $(0, 1]$. So the posterior $\mu^y$, defined by

$$\frac{d\mu^y}{d\mu_0}(u) = \frac{\exp(-\Phi(u; y))}{Z(y)},$$

is a well-defined probability measure on $X$, and it is unique.

2. For every $r > 0$ there is $C(r)$ such that $d_H(\mu^{y_1}, \mu^{y_2}) \le C(r)\, |y_1 - y_2|_\Gamma$ for all $y_1, y_2$ with $|y_1|_\Gamma, |y_2|_\Gamma \le r$.

## In plain words

You put a Gaussian guess on an unknown function and measure a few numbers that depend on it, with Gaussian noise. Bayes' rule then gives a new distribution, the posterior. If the measured numbers do not grow too fast as the function grows, this posterior always exists, and if you change the data a little, the posterior changes a little, by an amount proportional to the change. So the Bayesian answer is stable even when the plain inverse problem is not.

## Proof

**A fact about Gaussian measures (Fernique's theorem, cited).** If $\mu_0$ is a Gaussian measure on a separable Banach space, there is $\alpha > 0$ with $\int_X \exp(\alpha \|u\|^2)\, d\mu_0(u) < \infty$. Fix such an $\alpha$, and let $\varepsilon = \alpha / 2$ and $M = M(\varepsilon)$ in the growth assumption. Then

$$\int_X |\mathcal{G}(u)|_\Gamma^2\, d\mu_0 \le e^{2M} \int_X e^{\alpha \|u\|^2}\, d\mu_0 = : G_2 < \infty .$$

**Step 1 (the normalization).** $\Phi$ is measurable in $u$, because $\mathcal{G}$ is. Since $\Phi \ge 0$, $\exp(-\Phi) \le 1$ and $Z(y) \le 1$. For the lower bound, the closed balls $B_R = \{\|u\| \le R\}$ increase to $X$, so there is $R$ with $\mu_0(B_R) \ge 1/2$. On $B_R$, $|\mathcal{G}(u)|_\Gamma \le g_R = \exp(\varepsilon R^2 + M)$, so $\Phi(u; y) \le \frac12 (|y|_\Gamma + g_R)^2$. Hence

$$Z(y) \ge \tfrac12 \exp\!\big(-\tfrac12 (|y|_\Gamma + g_R)^2\big) > 0,$$

and for $|y|_\Gamma \le r$ this is at least $z(r) = \frac12 \exp(-\frac12 (r + g_R)^2)$. So the density of $\mu^y$ is a nonnegative measurable function with the integral 1, and $\mu^y$ is a probability measure. It is unique, because a measure is fixed by its density with respect to $\mu_0$. This proves part 1.

**Step 2 (the potential is Lipschitz in the data).** For $y_1, y_2$ with $|y_i|_\Gamma \le r$, write $\Phi_i = \Phi(u; y_i)$. Expanding the squares,

$$\Phi_1 - \Phi_2 = \tfrac12 \langle y_1 - y_2, \Gamma^{-1} (y_1 + y_2 - 2\mathcal{G}(u)) \rangle, \qquad |\Phi_1 - \Phi_2| \le |y_1 - y_2|_\Gamma\, (r + |\mathcal{G}(u)|_\Gamma),$$

by the Cauchy-Schwarz inequality in the inner product of $\Gamma^{-1}$. Let $S(r) = \int_X (r + |\mathcal{G}(u)|_\Gamma)^2\, d\mu_0 \le 2 r^2 + 2 G_2 < \infty$.

**Step 3 (the two parts of the distance).** Let $Z_i = Z(y_i) \ge z = z(r)$ and $f_i = \exp(-\Phi_i / 2)$. Then

$$\sqrt{\frac{d\mu^{y_1}}{d\mu_0}} - \sqrt{\frac{d\mu^{y_2}}{d\mu_0}} = \frac{f_1 - f_2}{\sqrt{Z_1}} + f_2 \Big( \frac{1}{\sqrt{Z_1}} - \frac{1}{\sqrt{Z_2}} \Big),$$

and $(a + b)^2 \le 2a^2 + 2b^2$ with $\int f_2^2\, d\mu_0 = Z_2$ gives

$$d_H(\mu^{y_1}, \mu^{y_2})^2 \le I_1 + I_2, \qquad I_1 = \frac{1}{Z_1} \int_X (f_1 - f_2)^2\, d\mu_0, \qquad I_2 = Z_2 \Big( \frac{1}{\sqrt{Z_1}} - \frac{1}{\sqrt{Z_2}} \Big)^2 .$$

**Step 4 (the bound on $I_1$).** The function $t \mapsto e^{-t/2}$ has the derivative at most $1/2$ in absolute value on $[0, \infty)$, and $\Phi_i \ge 0$, so $|f_1 - f_2| \le \frac12 |\Phi_1 - \Phi_2|$. With Step 2, $I_1 \le \frac{1}{4z} S(r)\, |y_1 - y_2|_\Gamma^2$.

**Step 5 (the bound on $I_2$).** In the same way $|e^{-\Phi_1} - e^{-\Phi_2}| \le |\Phi_1 - \Phi_2|$, so by Step 2 and the Cauchy-Schwarz inequality

$$|Z_1 - Z_2| \le \int_X |\Phi_1 - \Phi_2|\, d\mu_0 \le |y_1 - y_2|_\Gamma\, \sqrt{S(r)} .$$

The function $t \mapsto t^{-1/2}$ has the derivative at most $\frac12 z^{-3/2}$ in absolute value on $[z, \infty)$, so $|Z_1^{-1/2} - Z_2^{-1/2}| \le \frac12 z^{-3/2} |Z_1 - Z_2|$. With $Z_2 \le 1$, $I_2 \le \frac{1}{4 z^3} S(r)\, |y_1 - y_2|_\Gamma^2$.

**Step 6 (the result).** Steps 3 to 5 give $d_H(\mu^{y_1}, \mu^{y_2}) \le C(r) |y_1 - y_2|_\Gamma$ with

$$C(r) = \tfrac12 \sqrt{S(r) \big( z(r)^{-1} + z(r)^{-3} \big)} .$$

This proves part 2. $\blacksquare$

## Consequences

- **Stable expectations.** For a function $f$ of the unknown with finite second moments under both posteriors, the Cauchy-Schwarz inequality gives $|\operatorname{E}^{\mu^{y_1}} f - \operatorname{E}^{\mu^{y_2}} f| \le 2 \big(\operatorname{E}^{\mu^{y_1}} f^2 + \operatorname{E}^{\mu^{y_2}} f^2\big)^{1/2} d_H(\mu^{y_1}, \mu^{y_2})$. So the posterior mean and covariance, and the probabilities of events, are locally Lipschitz in the data. For the mean and the covariance, Fernique's theorem gives the moments.
- **Total variation.** With $d_{TV}(\mu, \nu) = \frac12 \int |d\mu/d\mu_0 - d\nu/d\mu_0|\, d\mu_0$, the same inequality gives $d_{TV} \le \sqrt{2}\, d_H$, so the posterior is also Lipschitz in the [total variation distance](/total-variation-distance/).
- **Approximation of the forward map.** The same steps, with $\mathcal{G}$ replaced by an approximation $\mathcal{G}_N$, bound the distance between the two posteriors by the error of $\mathcal{G}_N$ in a weighted mean square sense. So a finite element solver, a [Karhunen-Loeve](/karhunen-loeve-theorem/) truncation or a surrogate with a small error gives a close posterior.
- **Discretization invariance.** The statement holds in the function space $X$, so a sampler designed for $\mu^y$ on $X$, such as preconditioned Crank-Nicolson, has properties that do not degrade as the mesh is refined.

## Tightness

**The linear rate is the right one (by hand).** Let $X = \mathbb{R}$, $\mu_0 = N(0, 1)$, $\mathcal{G}(u) = u$ and $\Gamma = \gamma^2$. The posterior is $N\big(y/(1 + \gamma^2), \gamma^2/(1 + \gamma^2)\big)$. For two Gaussians with the same variance $s^2$, $d_H^2 = 1 - \exp(-(m_1 - m_2)^2 / (8 s^2))$, so here

$$d_H(\mu^{y_1}, \mu^{y_2})^2 = 1 - \exp\!\Big( -\frac{(y_1 - y_2)^2}{8 \gamma^2 (1 + \gamma^2)} \Big).$$

As $y_2 \to y_1$, $d_H / |y_1 - y_2| \to 1 / \sqrt{8 \gamma^2 (1 + \gamma^2)} > 0$. So the posterior is not Hölder continuous with an exponent above 1, and the Lipschitz bound cannot be improved in its order. With $1 - e^{-x} \le x$ the bound holds for all data with the constant $1 / \sqrt{8 (1 + \gamma^2)}$ in the norm $|\cdot|_\Gamma$.

**The constant depends on the noise.** In the same example, measured in the plain norm $|y_1 - y_2|$, the constant is $1 / (\gamma \sqrt{8 (1 + \gamma^2)})$, which goes to infinity as $\gamma \to 0$. Small noise makes the posterior sensitive to the data, and in the limit of no noise the posterior is a point mass that moves with the data.

**The prior must control the forward map.** The growth assumption and the tails of the prior work together. The proof needs $\int |\mathcal{G}|_\Gamma^2\, d\mu_0 < \infty$; Fernique's theorem gives this for maps of growth $\exp(\varepsilon \|u\|^2)$ under a Gaussian prior. For a prior with heavier tails, such as a Besov or Cauchy prior, the same proof needs a stronger condition on $\mathcal{G}$.

## History

Hadamard defined a well-posed problem as one with a solution that exists, is unique and depends continuously on the data. Stuart, in his 2010 review in Acta Numerica, gave conditions on the potential $\Phi$ under which the posterior of a Bayesian inverse problem in function space exists and is locally Lipschitz in the data in the Hellinger distance. He thus transferred the idea of Hadamard to the Bayesian setting. Dashti and Stuart gave a full account with Gaussian and Besov priors in the Handbook of Uncertainty Quantification. Latz studied well-posedness with weaker assumptions and in other metrics.

## References
