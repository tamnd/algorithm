---
tag: 89JZ0M
kind: definition
slug: influence-function
name: Influence function
aliases:
- influence curve
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: Hampel's measure of the effect of an infinitesimal contamination at a point on an estimator. Bounded influence means robustness to single outliers.
prereqs: [estimator, empirical-distribution-function, huber-contamination-model, median]
see_also: [breakdown-point, m-estimator, huber-m-estimator, tukey-biweight, median-absolute-deviation, jackknife-resampling, delta-method, cooks-distance]
sources:
  - paper: doi:10.1080/01621459.1974.10482962
    title: Frank R. Hampel, The influence curve and its role in robust estimation, Journal of the American Statistical Association 69(346), 1974
    locator: pp. 383 to 393 (the definition, the gross-error sensitivity and the link to the asymptotic variance)
  - book: isbn:9780471829218
    title: Frank R. Hampel, Elvezio M. Ronchetti, Peter J. Rousseeuw and Werner A. Stahel, Robust Statistics, The Approach Based on Influence Functions, Wiley, 1986
    locator: Chapter 2 (the influence function of one-dimensional estimators, the gross-error sensitivity and the optimal bounded-influence estimators)
  - book: isbn:9780470129906
    title: Peter J. Huber and Elvezio M. Ronchetti, Robust Statistics, second edition, Wiley, 2009
    locator: Chapter 1 (infinitesimal aspects) and Chapter 3 (the influence functions of M-, L- and R-estimators)
  - book: isbn:9781119214687
    title: Ricardo A. Maronna, R. Douglas Martin, Victor J. Yohai and Matías Salibián-Barrera, Robust Statistics, Theory and Methods (with R), second edition, Wiley, 2019
    locator: Chapter 3 (measuring robustness, the influence function and the sensitivity curve)
---

The influence function of an estimator gives the effect of one more observation at the point $x$, in the limit of an infinitesimal fraction of such observations. Hampel introduced it in 1974. An estimator with a bounded influence function is robust to a small fraction of outliers anywhere. Its mean square is also the asymptotic variance of the estimator. So one function measures both robustness and efficiency.

## Definition

Write the [estimator](/estimator/) as a functional $T$ of a law $F$, so that the estimate is $T(F_n)$ with $F_n$ the [empirical distribution function](/empirical-distribution-function/). Let $\delta_x$ be the point mass at $x$. The **influence function** of $T$ at $F$ is
$$\mathrm{IF}(x; T, F) = \lim_{t \downarrow 0} \frac{T\big((1-t)F + t\,\delta_x\big) - T(F)}{t},$$
for each $x$ where the limit exists. It is the directional derivative of $T$ at $F$ in the direction $\delta_x - F$. The law $(1-t)F + t\delta_x$ is the [contamination model](/huber-contamination-model/) with $G = \delta_x$.

Three numbers summarize it.

- **Gross-error sensitivity.** $\gamma^*(T, F) = \sup_x |\mathrm{IF}(x; T, F)|$. It bounds the first-order bias that a small fraction $t$ of outliers can cause: about $t\,\gamma^*$.
- **Rejection point.** The least $r$ with $\mathrm{IF}(x) = 0$ for all $|x - T(F)| > r$. It is finite for a redescending estimator such as [Tukey's biweight](/tukey-biweight/).
- **Local-shift sensitivity.** $\sup_{x \ne y} |\mathrm{IF}(x) - \mathrm{IF}(y)|/|x - y|$. It measures the effect of rounding or small shifts of the data.

The finite-sample version is Tukey's **sensitivity curve**. For a sample $x_1, \ldots, x_{n-1}$,
$$\mathrm{SC}_n(x) = n\,\big[T(x_1, \ldots, x_{n-1}, x) - T(x_1, \ldots, x_{n-1})\big].$$
This is the definition with $F = F_{n-1}$ and $t = 1/n$, without the limit.

Under regularity conditions (Hampel 1974; Hampel, Ronchetti, Rousseeuw and Stahel 1986, Chapter 2), $E_F[\mathrm{IF}(X; T, F)] = 0$, and the von Mises expansion
$$T(F_n) = T(F) + \frac1n \sum_{i=1}^n \mathrm{IF}(X_i; T, F) + o_p(n^{-1/2})$$
holds. Then $\sqrt n\,(T(F_n) - T(F))$ tends to $N(0, V)$ with $V = E_F[\mathrm{IF}(X; T, F)^2]$. This page cites that result and does not prove it.

## Examples and non-examples

The results below are proved here. In each, $F$ is a law on $\mathbb{R}$.

**The mean.** $T(F) = \int y\,dF(y) = \mu$, with a finite mean. Then $T((1-t)F + t\delta_x) = (1-t)\mu + t x$, which is linear in $t$. So
$$\mathrm{IF}(x; \text{mean}, F) = x - \mu.$$
It is unbounded, so $\gamma^* = \infty$. One outlier far away has an effect without bound. At $F = \Phi$, $V = E[X^2] = 1$, the variance of the mean.

**The median.** Let $m = F^{-1}(1/2)$, and assume that $F$ has a density $f$ that is continuous and positive at $m$. Then
$$\mathrm{IF}(x; \text{median}, F) = \frac{\operatorname{sign}(x - m)}{2 f(m)},$$
with the value 0 at $x = m$.

*Proof.* Let $F_t = (1-t)F + t\delta_x$ and let $m_t$ be its median, the point with $F_t(m_t) = 1/2$. Take $x > m$. For small $t$, $m_t < x$, so $F_t(m_t) = (1-t)F(m_t) = 1/2$, and $m_t = F^{-1}\big(\tfrac{1}{2(1-t)}\big)$. The inverse function rule gives $\frac{d}{dt} m_t \big|_{t=0} = \frac{1}{f(m)} \cdot \frac{d}{dt}\frac{1}{2(1-t)}\Big|_{t=0} = \frac{1}{2f(m)}$. Take $x < m$. For small $t$, $m_t > x$, so $(1-t)F(m_t) + t = 1/2$, and $F(m_t) = \frac{1/2 - t}{1 - t}$. Its derivative at $t = 0$ is $-1/2$, so $\frac{d}{dt} m_t \big|_{t=0} = -\frac{1}{2f(m)}$. Take $x = m$. Then $F_t(y) < 1/2$ for $y < m$ and $F_t(m) = 1/2 + t/2$, so $m_t = m$ for all $t$, and the derivative is 0. $\square$

The function is bounded but jumps at $m$. At $F = \Phi$, $\gamma^* = 1/(2\varphi(0)) = \sqrt{2\pi}/2 \approx 1.2533$ and $V = \pi/2 \approx 1.5708$. Hampel showed that the median has the least $\gamma^*$ among all Fisher-consistent location functionals at $\Phi$ (cited).

**The Huber estimator.** Let $\psi_k(u) = \max(-k, \min(k, u))$, and let $T(F)$ be the root $\theta$ of $\Lambda(\theta) = \int \psi_k(y - \theta)\,dF(y) = 0$ (fixed scale 1). Assume that $F$ is continuous near $T(F) \pm k$ and that $P_F(|Y - T(F)| < k) > 0$. Then
$$\mathrm{IF}(x; T, F) = \frac{\psi_k(x - T(F))}{P_F\big(|Y - T(F)| < k\big)}.$$

*Proof.* Put $\Lambda(\theta, t) = (1-t)\Lambda(\theta) + t\,\psi_k(x - \theta)$, so $T_t = T(F_t)$ solves $\Lambda(T_t, t) = 0$. The function $\psi_k$ is Lipschitz with derivative $\mathbf 1\{|u| < k\}$ except at $\pm k$. By dominated convergence, $\Lambda'(\theta) = -P_F(|Y - \theta| < k)$, and it is continuous near $T(F)$ because $F$ has no atoms there. So $\partial_\theta \Lambda(T(F), 0) = -P_F(|Y - T(F)| < k) < 0$. Also $\partial_t \Lambda(\theta, t) = -\Lambda(\theta) + \psi_k(x - \theta)$, which is $\psi_k(x - T(F))$ at $(T(F), 0)$. The implicit function theorem gives a differentiable root $T_t$ near $t = 0$ with
$$\frac{dT_t}{dt}\Big|_{t=0} = -\frac{\partial_t \Lambda}{\partial_\theta \Lambda} = \frac{\psi_k(x - T(F))}{P_F(|Y - T(F)| < k)}. \qquad \square$$

At $F = \Phi$ and $k = 1.345$, $P(|Z| < k) = 0.8214$, so $\gamma^* = 1.345/0.8214 \approx 1.637$, and $V = E[\psi_k(Z)^2]/P(|Z|<k)^2 \approx 1.0526$, an efficiency of 95 percent. This is the general rule $\mathrm{IF} = A^{-1}\psi$ of a Z-estimator; the [M-estimator](/m-estimator/) page derives it for any $\psi$.

**A sensitivity curve by hand.** Take the four points $(1, 2, 3, 4)$ and add a fifth point $x$, so $n = 5$.

| $x$ | $-100$ | 0 | 2.5 | 3 | 100 |
|---|---|---|---|---|---|
| $\mathrm{SC}_5$ of the mean, $x - 2.5$ | $-102.5$ | $-2.5$ | 0 | 0.5 | 97.5 |
| $\mathrm{SC}_5$ of the median, $5(\min(\max(x, 2), 3) - 2.5)$ | $-2.5$ | $-2.5$ | 0 | 2.5 | 2.5 |

For the mean, $\mathrm{SC}_5(x) = 5\,((10 + x)/5 - 2.5) = x - 2.5$. For the median, the median of five points is $x$ clamped to $[2, 3]$, so the curve stays in $[-2.5, 2.5]$. The shapes match the influence functions above: a line, and a step.

**Non-examples.**

- **A bounded influence function is not a high breakdown point.** The influence function is a derivative at $t = 0$. The $\alpha$-[trimmed mean](/trimmed-mean/) has a bounded influence function and breakdown point $\alpha$, which can be small. In regression, an M-estimator with a bounded $\psi$ of the residual has bounded influence in $y$, but not in the design point, and breaks down with one point.
- **The influence function can fail to exist.** The sample median at a law with $f(m) = 0$, or with an atom at $m$, has no finite derivative.
- **The sample standard deviation** has $\mathrm{IF}(x) = ((x - \mu)^2 - \sigma^2)/(2\sigma)$, which grows like $x^2$. The [MAD](/median-absolute-deviation/) has a bounded one.

## Related definitions

- **[Breakdown point](/breakdown-point/).** The global measure: the largest fraction of outliers that $T$ can carry.
- **Empirical influence.** The influence function evaluated at $F_n$. The infinitesimal [jackknife](/jackknife-resampling/) estimates the variance $V/n$ with it, and the jackknife uses $\mathrm{SC}$-like differences with $t = -1/(n-1)$.
- **[Cook's distance](/cooks-distance/).** A regression diagnostic that measures the effect of deleting one case. It is a finite-sample influence of each case on the fit.
- **Gâteaux and Fréchet derivatives.** The influence function is the kernel of the Gâteaux derivative of $T$. With a Fréchet derivative, the von Mises expansion holds, and the [delta method](/delta-method/) for smooth functionals follows.
- **Change-of-variance function.** The derivative of $V(T, F)$ in the same direction. It measures the robustness of the variance.

## References
