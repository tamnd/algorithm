---
tag: Y48S7A
kind: definition
slug: persistent-excitation
name: Persistent excitation
aliases:
- persistency of excitation
- persistently exciting input
area: control/modeling-and-identification
level: core
summary: An input is persistently exciting of order n if its covariance matrix of n lags is positive definite, so it reveals n parameters.
prereqs: [system-identification, positive-definite-matrix]
see_also: [prbs-input, least-squares-arx-identification, autocorrelation, power-spectral-density, closed-loop-identification, rls-algorithm, adaptive-control, arx-model]
sources:
  - book: isbn:9780138812362
    title: "Torsten Söderström and Petre Stoica, System Identification, Prentice Hall, 1989"
    locator: "Chapter 5 (input signals: the definition of persistent excitation, its spectral form, and the orders of white noise, sinusoids and pseudo-random binary sequences)"
  - book: isbn:9780136566953
    title: "Lennart Ljung, System Identification: Theory for the User, second edition, Prentice Hall, 1999"
    locator: "Chapter 13 (informative experiments, persistent excitation and the open-loop condition on the input)"
  - paper: "Karl Johan Åström and Torsten Bohlin, Numerical identification of linear dynamic systems from normal operating records, IFAC Symposium on Self-Adaptive Systems, Teddington, 1965; in P. H. Hammond (editor), Theory of Self-Adaptive Control Systems, Plenum Press, 1966, pp. 96-111"
    locator: the first use of the condition under the name persistently exciting
---

Persistent excitation is the property of an input signal that makes it rich enough to reveal a given number of parameters of a linear system. A signal $u$ is persistently exciting of order $n$ if the $n \times n$ matrix of its covariances at lags $0$ to $n - 1$ is positive definite. In the frequency domain this means that the spectrum of $u$ is nonzero at $n$ or more frequencies. In [system identification](/system-identification/), an open-loop input that is persistently exciting of a high enough order makes the data informative, so that the least squares and prediction error estimates have a unique limit. The name goes back to Åström and Bohlin (1965). In [adaptive control](/adaptive-control/) the same word names a related condition on the regressor vector.

## Definition

Time is discrete. A signal $u$ is quasi-stationary if it is bounded in mean square and the limits

$$r_u(\tau) = \lim_{N \to \infty} \frac{1}{N} \sum_{k=1}^{N} \mathbb{E}\, u(k)\, u(k - \tau)$$

exist for every integer $\tau$; for a deterministic signal drop the expectation. For a stationary random signal $r_u$ is the ordinary covariance function (the [autocorrelation](/autocorrelation/) without removing the mean). The covariance matrix of order $n$ is the symmetric Toeplitz matrix

$$\bar R_n = \begin{pmatrix} r_u(0) & r_u(1) & \cdots & r_u(n-1) \\ r_u(1) & r_u(0) & \cdots & r_u(n-2) \\ \vdots & & \ddots & \vdots \\ r_u(n-1) & r_u(n-2) & \cdots & r_u(0) \end{pmatrix} = \lim_{N \to \infty} \frac{1}{N} \sum_{k=1}^{N} \mathbb{E}\, \phi_n(k)\, \phi_n(k)^T,$$

with $\phi_n(k) = (u(k-1), \ldots, u(k-n))^T$.

**Definition.** $u$ is *persistently exciting of order $n$* if $\bar R_n$ is [positive definite](/positive-definite-matrix/). Since $\bar R_n$ is a leading block of $\bar R_{n+1}$, a signal that is persistently exciting of order $n + 1$ is also persistently exciting of order $n$. The *order* of $u$ is the largest such $n$, or infinity.

Two equivalent forms are used as often as the definition (Söderström and Stoica 1989, Chapter 5).

- **Filters (theorem).** $u$ is persistently exciting of order $n$ if and only if no nonzero polynomial $M(q) = m_1 q^{-1} + \cdots + m_n q^{-n}$ gives $\lim \frac{1}{N} \sum \mathbb{E}\, \big(M(q) u(k)\big)^2 = 0$. The reason is that this limit equals $m^T \bar R_n m$.
- **Spectrum (theorem).** For a signal with spectrum $\Phi_u$, $u$ is persistently exciting of order $n$ if and only if $\Phi_u(\omega) \ne 0$ on at least $n$ points of $(-\pi, \pi]$, counting $\pm\omega$ as two points. This follows from $m^T \bar R_n m = \frac{1}{2\pi} \int \lvert M(e^{i\omega}) \rvert^2\, d\Phi_u(\omega)$ and the fact that a polynomial of degree $n - 1$ has at most $n - 1$ zeros.

**Why it matters (theorem).** For the FIR model $y(k) = b_1 u(k-1) + \cdots + b_n u(k-n) + v(k)$, the least squares normal matrix divided by $N$ tends to $\bar R_n$, so the estimate has a unique limit exactly when $u$ is persistently exciting of order $n$. For rational models in open loop, an input that is persistently exciting of order $n_b + n_f$, the number of coefficients of $G = B/F$, makes the data informative for the model set (Ljung 1999, Chapter 13).

## Examples and non-examples

- **White noise.** $r_u(\tau) = \sigma^2$ for $\tau = 0$ and $0$ otherwise, so $\bar R_n = \sigma^2 I$ for every $n$. White noise is persistently exciting of every order.
- **A constant.** $u \equiv a$ with $a \ne 0$ has $r_u(\tau) = a^2$ for every $\tau$, so $\bar R_n = a^2\, \mathbf{1}\mathbf{1}^T$ has rank 1. A constant, and also a step, is persistently exciting of order 1 only: the filter $M(q) = q^{-1} - q^{-2}$ removes it. This is why a step test alone cannot separate $b_1$ from $b_2$ in a model with two input coefficients.
- **A sinusoid.** $u(k) = a \cos(\omega_0 k)$ with $0 < \omega_0 < \pi$ has $r_u(\tau) = \frac{a^2}{2} \cos(\omega_0 \tau)$. Then $\det \bar R_2 = \frac{a^4}{4} \sin^2 \omega_0 > 0$, and $\bar R_3$ is singular because $u(k) - 2\cos(\omega_0)\, u(k-1) + u(k-2) = 0$. The order is 2. For $\omega_0 = \pi/2$ and $a = 1$, $\bar R_2 = \frac{1}{2} I$. A sum of $m$ sinusoids at distinct frequencies in $(0, \pi)$ has order $2m$.
- **A PRBS.** A [maximum-length binary sequence](/prbs-input/) with levels $\pm a$ and period $M = 2^r - 1$ has $r_u(0) = a^2$ and $r_u(\tau) = -a^2/M$ for $0 < \tau < M$. For $n \le M$, $\bar R_n = a^2\big((1 + \tfrac{1}{M}) I - \tfrac{1}{M} \mathbf{1}\mathbf{1}^T\big)$, whose eigenvalues are $a^2 (1 + \tfrac{1}{M})$ with multiplicity $n - 1$ and $a^2 \tfrac{M + 1 - n}{M}$. All are positive for $n \le M$ and the last is $0$ for $n = M + 1$, so the order is exactly $M$. For $M = 15$ the order is 15.
- **Non-example: any periodic signal of period $M$.** The filter $M(q) = q^{-1} - q^{-M-1}$ removes it, so its order is at most $M$. Periodic inputs must have a period longer than the number of parameters.
- **Non-example: a single pulse.** A signal that is nonzero at finitely many times has $r_u \equiv 0$. It is not persistently exciting of any order, although it can still give exact parameters in the noise-free case.
- **Non-example: a feedback input.** If $u(k) = -c\, y(k)$, then $u$ may be persistently exciting of a high order and the data still fail to be informative, because $u$ is a filter of $y$. See [closed-loop identification](/closed-loop-identification/).

## Related definitions

- **Informative data.** The data are informative for a model set if any two models that give the same limit prediction errors have the same $G$ and $H$. Persistent excitation is a condition on the input; informativeness is a condition on the whole experiment, and in closed loop it also depends on the controller (Ljung 1999, Chapter 13).
- **Identifiability.** A parametrization is identifiable at $\theta_0$ if no other $\theta$ gives the same $G$ and $H$. Informative data and an identifiable parametrization together give a unique limit of the estimate.
- **Persistent excitation of a regressor.** In adaptive control and in the analysis of the [RLS algorithm](/rls-algorithm/), a vector signal $\varphi$ is called persistently exciting if there are $\alpha > 0$ and $T$ with $\sum_{j=k}^{k+T} \varphi(j) \varphi(j)^T \ge \alpha I$ for every $k$. This uniform condition gives exponential convergence of the parameter error.
- **Sufficiently rich.** A continuous-time signal is called sufficiently rich of order $n$ if its spectrum has at least $n$ points of support; it is the continuous-time analogue of the spectral form above.
- **[Power spectral density](/power-spectral-density/).** The spectral form of the definition counts the support points of $\Phi_u$.

## References
