---
tag: AGFQ2A
kind: model
slug: armax-model
name: ARMAX model
aliases:
- autoregressive moving average model with exogenous input
area: control/modeling-and-identification
level: core
summary: A linear model A(q)y = B(q)u + C(q)e that adds a moving average of the white noise to the ARX model.
history:
  year: 1965
  people: [Karl Johan Åström, Torsten Bohlin]
  note: "Åström and Bohlin fitted this model to normal operating records by maximum likelihood in a 1965 paper, and it became the standard noise model of stochastic control and identification."
prereqs: [arx-model, arma-model]
see_also: [prediction-error-method, output-error-model, least-squares-arx-identification, instrumental-variable-identification, state-space-model, kalman-filter, maximum-likelihood-estimation, gauss-newton-algorithm]
sources:
  - book: isbn:9780136566953
    title: "Lennart Ljung, System Identification: Theory for the User, second edition, Prentice Hall, 1999"
    locator: "Chapter 4 (the ARMAX structure in the family of transfer-function models), Chapter 7 (prediction error methods and pseudo-linear regressions) and Chapter 10 (computing the estimate)"
  - book: isbn:9780138812362
    title: "Torsten Söderström and Petre Stoica, System Identification, Prentice Hall, 1989"
    locator: "the chapters on model parametrizations and on prediction error methods"
  - paper: "Karl Johan Åström and Torsten Bohlin, Numerical identification of linear dynamic systems from normal operating records, IFAC Symposium on Self-Adaptive Systems, Teddington, 1965; in P. H. Hammond (editor), Theory of Self-Adaptive Control Systems, Plenum Press, 1966, pp. 96-111"
    locator: the maximum likelihood fit of the ARMAX structure
  - paper: doi:10.1109/TAC.1974.1100735
    title: "Karl Johan Åström and Torsten Söderström, Uniqueness of the maximum likelihood estimates of the parameters of an ARMA model, IEEE Transactions on Automatic Control 19(6), 769-773, 1974"
    locator: the limit of the criterion for ARMA models and the conditions for a unique local and global minimum
---

The ARMAX model is a linear discrete-time model of a system with input $u$ and output $y$, written $A(q)\, y(k) = B(q)\, u(k) + C(q)\, e(k)$, where $A$, $B$ and $C$ are polynomials in the backward shift $q^{-1}$ and $e$ is white noise. It extends the [ARX model](/arx-model/) by letting the equation error be a moving average $C(q)\, e(k)$ of the white noise instead of the white noise itself, so the disturbance can have its own zeros. The name means autoregressive moving average with exogenous input. It is the [ARMA model](/arma-model/) of time-series analysis with a measured input added, and it is read as a one-step predictor of $y$ from past data. The predictor is no longer linear in the coefficients, so the model is fitted by the [prediction error method](/prediction-error-method/) or by maximum likelihood, with an iterative search on a criterion that is not convex.

## The machine

**Notation.** Time is discrete, $k \in \mathbb{Z}$, with sampling period $h$; $q^{-1} u(k) = u(k-1)$. $e$ is white noise with mean 0 and variance $\sigma^2$.

**Definition.** With orders $n_a \ge 0$, $n_b \ge 1$, $n_c \ge 0$ and a delay $n_k \ge 0$,

$$A(q) = 1 + \sum_{i=1}^{n_a} a_i q^{-i}, \qquad B(q) = q^{-n_k} \sum_{j=1}^{n_b} b_j q^{-j+1}, \qquad C(q) = 1 + \sum_{i=1}^{n_c} c_i q^{-i},$$

the ARMAX model is $A(q)\, y(k) = B(q)\, u(k) + C(q)\, e(k)$. In the form $y = G u + H e$ it has $G = B/A$ and $H = C/A$, with the same denominator for both.

**Parameter space.** $\theta = (a, b, c) \in \mathbb{R}^d$ with $d = n_a + n_b + n_c$, restricted to the open set where $C$ is Schur, that is, all roots of $z^{n_c} C(z)$ lie inside the unit circle. Any $C$ with no roots on the unit circle can be replaced by a Schur $C$ with the same noise spectrum, by reflecting each root $z$ to $1/\bar z$ and changing $\sigma^2$ by a constant factor, so the restriction loses no spectra.

**The predictor.** From $H^{-1} = A/C$, the one-step-ahead predictor and the prediction error are

$$C(q)\, \hat y(k \mid \theta) = B(q)\, u(k) + \big(C(q) - A(q)\big)\, y(k), \qquad \varepsilon(k, \theta) = \frac{A(q)\, y(k) - B(q)\, u(k)}{C(q)}.$$

Only $C$ appears as a denominator, so the predictor is BIBO stable for every $\theta$ in the parameter set, even if $A$ is not Schur. In the time domain, with $\varphi(k, \theta) = \big(-y(k-1), \ldots, -y(k-n_a),\ u(k-n_k), \ldots, u(k-n_k-n_b+1),\ \varepsilon(k-1, \theta), \ldots, \varepsilon(k-n_c, \theta)\big)^T$,

$$\hat y(k \mid \theta) = \varphi(k, \theta)^T \theta.$$

This looks like a linear regression, but $\varphi$ depends on $\theta$ through the past prediction errors. It is called a pseudo-linear regression.

**The gradient.** Differentiating $C \varepsilon = A y - B u$ gives $\psi(k, \theta) = -\partial \varepsilon(k, \theta)/\partial \theta = \varphi(k, \theta)/C(q)$: the gradient is the pseudo-regressor filtered through $1/C$.

**A worked case.** Take $A = 1 - 1.5 q^{-1} + 0.7 q^{-2}$, $B = q^{-1} + 0.5 q^{-2}$ and $C = 1 - q^{-1} + 0.2 q^{-2}$. The roots of $z^2 - z + 0.2$ are $0.7236$ and $0.2764$, so $C$ is Schur. The prediction error obeys

$$\varepsilon(k) = y(k) - 1.5\, y(k-1) + 0.7\, y(k-2) - u(k-1) - 0.5\, u(k-2) + \varepsilon(k-1) - 0.2\, \varepsilon(k-2).$$

The disturbance spectrum $\sigma^2 \lvert C \rvert^2 / \lvert A \rvert^2$ is $\sigma^2 (0.2/0.2)^2 = \sigma^2$ at $\omega = 0$ and $\sigma^2 (2.2/3.2)^2 = 0.4727\, \sigma^2$ at $\omega = \pi$. An ARX model of this system cannot reproduce that shape, because its disturbance spectrum $\sigma^2/\lvert A \rvert^2$ is $25\, \sigma^2$ at $\omega = 0$.

## What it counts

The model has $d + 1$ parameters $(\theta, \sigma^2)$. $N$ is the number of samples.

| quantity | formula | cost |
|---|---|---|
| prediction errors | the recursion $C \varepsilon = A y - B u$ from zero initial values | $O(N d)$ |
| criterion | $V_N(\theta) = \frac{1}{N} \sum_k \varepsilon(k, \theta)^2$ | $O(N d)$ |
| gradient of $V_N$ | $-\frac{2}{N} \sum_k \psi(k, \theta)\, \varepsilon(k, \theta)$, with $\psi = \varphi/C$ | $O(N d)$ |
| Gauss-Newton matrix | $\frac{1}{N} \sum_k \psi \psi^T$ | $O(N d^2)$ |
| frequency response | $B(e^{i\omega})/A(e^{i\omega})$ | $O(n_a + n_b)$ per frequency |
| disturbance spectrum | $\sigma^2 \lvert C(e^{i\omega}) \rvert^2 / \lvert A(e^{i\omega}) \rvert^2$ | $O(n_a + n_c)$ per frequency |
| asymptotic covariance | $\frac{\sigma^2}{N} \big(\mathbb{E}\, \psi \psi^T\big)^{-1}$ at the true $\theta$ | $O(N d^2 + d^3)$ from data |

## Relation to other models

- **[ARMA model](/arma-model/).** With $n_b = 0$ the ARMAX model is an ARMA($n_a$, $n_c$) model of $y$, with the sign convention $A = 1 + a_1 q^{-1} + \cdots$. Time-series analysis asks for a causal and invertible stationary solution, so both $A$ and $C$ must be Schur. The identification view needs only $C$ Schur, because the predictor never divides by $A$; this allows unstable plants.
- **[ARX model](/arx-model/).** ARMAX with $n_c = 0$, that is $C = 1$. The predictor becomes linear in $\theta$ and least squares applies.
- **[Output error model](/output-error-model/).** Has $H = 1$ and a separate denominator $F$ for $G$. ARMAX and OE are not nested: ARMAX forces $G$ and $H$ to share their poles, and OE forces $H$ to be 1.
- **Box-Jenkins model.** $y = (B/F)\, u + (C/D)\, e$. ARMAX is the case $F = D = A$.
- **[State-space model](/state-space-model/).** A single-output innovations model $x(k+1) = \Phi x(k) + \Gamma u(k) + K e(k)$, $y(k) = c^T x(k) + e(k)$ of order $n$ has $G$ and $H$ with the common denominator $\det(zI - \Phi)$, so it is an ARMAX model with $n_a = n_c = n$. The ARMAX predictor is the steady-state [Kalman filter](/kalman-filter/) predictor of that model.

## Known results in the model

- **The criterion is not convex (computation).** For data from the AR(1) system $y(k) - 0.7\, y(k-1) = e(k)$ with $\sigma^2 = 1$, fitted with the model $(1 + a q^{-1})\, y = (1 + c q^{-1})\, e$, the limit criterion $\bar V(a, c) = \mathbb{E}\, \varepsilon^2$ takes the values $\bar V(-0.2, -0.4) = 2.8893$ and $\bar V(0.5, 0) = 3.8235$, but $\bar V(0.15, -0.2) = 3.4096$ at the midpoint, above the average $3.3564$. A local search therefore needs a good start, usually an ARX fit, a high-order ARX fit or an instrumental variable estimate.
- **No false minima for ARMA in the limit (theorem).** For ARMA data with the right orders and a Gaussian likelihood, the limit criterion has a unique local minimum in the region where both polynomials are Schur, so for large $N$ a local search converges to the true parameters (Åström and Söderström 1974). The paper treats ARMA models without an input; with an input, the result is not automatic.
- **Consistency and efficiency (theorem).** If the data come from an ARMAX system of the same orders, $A$, $B$ and $C$ have no common factor, and the open-loop input is persistently exciting of a high enough order, then the global minimizer of $V_N$ converges to the true $\theta$, and its asymptotic covariance is $\frac{\sigma^2}{N}(\mathbb{E}\, \psi \psi^T)^{-1}$ (Ljung 1999, Chapters 8 and 9). For Gaussian $e$ this is the Cramér-Rao bound.
- **Least squares is biased (theorem and measurement).** An ARX fit to ARMAX data is not consistent when $C \ne 1$, because the regressor is correlated with $C e$. For the worked case with a white $\pm 1$ input and $N = 2000$, least squares gave $(\hat a, \hat b) = (-1.2639, 0.4873, 1.0498, 0.7262)$; the prediction error method gave $(-1.5129, 0.7130, 1.0326, 0.4604)$ and $\hat c = (-0.9801, 0.1883)$, with the criterion value $1.04079$, against the true $(-1.5, 0.7, 1, 0.5)$ and $(-1, 0.2)$.
- **Pseudo-linear regression.** Treating $\varphi(k, \theta)$ as known and running recursive least squares on it gives the extended least squares method. It is cheap but needs a strict positive real condition on $1/C$ to converge, while a Gauss-Newton search on $V_N$ does not.

## References
