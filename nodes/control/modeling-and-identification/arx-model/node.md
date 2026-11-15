---
tag: 2SM5P8
kind: model
slug: arx-model
name: ARX model
aliases:
- autoregressive model with exogenous input
- equation error model
area: control/modeling-and-identification
level: core
summary: A linear model A(q)y = B(q)u + e in which the output is a linear regression on past outputs, past inputs and white noise.
prereqs: [system-identification, autoregressive-model]
see_also: [armax-model, output-error-model, least-squares-arx-identification, instrumental-variable-identification, rls-algorithm, persistent-excitation, transfer-function, state-space-model]
sources:
  - book: isbn:9780136566953
    title: "Lennart Ljung, System Identification: Theory for the User, second edition, Prentice Hall, 1999"
    locator: "Chapter 4 (the family of transfer-function models, with ARX as the equation error structure), Chapter 7 (least squares for linear regressions) and Chapter 13 (informative experiments)"
  - book: isbn:9780138812362
    title: "Torsten Söderström and Petre Stoica, System Identification, Prentice Hall, 1989"
    locator: "the chapters on linear regression and on model parametrizations"
  - paper: doi:10.1016/0005-1098(71)90059-8
    title: "Karl Johan Åström and Pieter Eykhoff, System identification: a survey, Automatica 7(2), 123-162, 1971"
    locator: the least squares method for difference equation models and its bias under correlated residuals
  - paper: "Lennart Ljung and Bo Wahlberg, Asymptotic properties of the least-squares method for estimating transfer functions and disturbance spectra, Advances in Applied Probability 24(2), 412-440, 1992"
    locator: the consistency of high-order ARX estimates of the transfer function and the disturbance spectrum when the order grows with the number of data
---

The ARX model is a linear discrete-time model of a system with an input $u$ and an output $y$, written $A(q)\, y(k) = B(q)\, u(k) + e(k)$ with polynomials $A$ and $B$ in the backward shift $q^{-1}$ and white noise $e$. It says that the present output is a fixed linear combination of a few past outputs and past inputs, plus a fresh random error. The name means autoregressive with exogenous input: it is the [autoregressive model](/autoregressive-model/) of time-series analysis with a known, measured input added on the right, and it is read as a predictor of the next output rather than as a description of a stationary process. Because the predictor is linear in the coefficients, the coefficients are fitted by ordinary least squares, which makes ARX the first model tried in [system identification](/system-identification/). Its weak point is the noise model: the disturbance is forced to share the poles of the system, and when the real disturbance does not, the least squares fit is biased.

## The machine

**Notation.** Time is discrete, $k \in \mathbb{Z}$, with sampling period $h$. The operator $q^{-1}$ is the backward shift, $q^{-1} u(k) = u(k - 1)$. $e$ is white noise: mean 0, variance $\sigma^2$, uncorrelated at different times.

**Definition.** With orders $n_a \ge 0$, $n_b \ge 1$ and an input delay $n_k \ge 0$,

$$A(q) = 1 + a_1 q^{-1} + \cdots + a_{n_a} q^{-n_a}, \qquad B(q) = q^{-n_k}\big(b_1 + b_2 q^{-1} + \cdots + b_{n_b} q^{-n_b + 1}\big),$$

the ARX model is

$$y(k) + a_1 y(k-1) + \cdots + a_{n_a} y(k - n_a) = b_1 u(k - n_k) + \cdots + b_{n_b} u(k - n_k - n_b + 1) + e(k).$$

In the general form $y = G u + H e$ of system identification it has $G(q) = B(q)/A(q)$ and $H(q) = 1/A(q)$.

**Parameter space.** $\theta = (a_1, \ldots, a_{n_a}, b_1, \ldots, b_{n_b}) \in \mathbb{R}^d$ with $d = n_a + n_b$, and $\sigma^2 > 0$. No constraint is needed for the predictor below, but $G$ is BIBO stable only if $A$ is Schur, that is, all roots of $z^{n_a} A(z)$ lie inside the unit circle (assuming $A$ and $B$ have no common factor).

**The predictor.** Put the past data in the regressor

$$\varphi(k) = \big(-y(k-1), \ldots, -y(k - n_a),\ u(k - n_k), \ldots, u(k - n_k - n_b + 1)\big)^T.$$

Then the model reads $y(k) = \varphi(k)^T \theta + e(k)$. Since $e(k)$ is independent of everything in $\varphi(k)$, the best one-step-ahead predictor is

$$\hat y(k \mid \theta) = \varphi(k)^T \theta = B(q)\, u(k) + \big(1 - A(q)\big)\, y(k),$$

and the prediction error is $\varepsilon(k, \theta) = A(q)\, y(k) - B(q)\, u(k)$. Both are finite filters of the data, so the predictor is BIBO stable for every $\theta$, even when $A$ is not Schur. This is the equation error view: $\varepsilon$ is the error in the difference equation, not in the output.

**A worked case.** Take $A(q) = 1 - 1.5 q^{-1} + 0.7 q^{-2}$, $B(q) = q^{-1} + 0.5 q^{-2}$, so $n_a = n_b = 2$ and $n_k = 1$. The predictor is $\hat y(k) = 1.5\, y(k-1) - 0.7\, y(k-2) + u(k-1) + 0.5\, u(k-2)$. The roots of $z^2 - 1.5 z + 0.7$ are $0.75 \pm 0.3708 i$, with modulus $\sqrt{0.7} = 0.8367$, so $A$ is Schur. The static gain is $B(1)/A(1) = 1.5/0.2 = 7.5$. The impulse response of $G$ starts $g_0 = 0$, $g_1 = 1$, $g_2 = 2$, $g_3 = 2.3$, $g_4 = 2.05$, $g_5 = 1.465$, each from $g_j = 1.5\, g_{j-1} - 0.7\, g_{j-2}$ after the input terms.

## What it counts

The model has $d + 1$ parameters $(\theta, \sigma^2)$. The quantities below follow from them; $N$ is the number of samples and $\omega \in [0, \pi]$ is a frequency in radians per sample.

| quantity | formula | cost |
|---|---|---|
| one-step prediction | $\hat y(k \mid \theta) = \varphi(k)^T \theta$ | $O(d)$ per sample |
| prediction error criterion | $V_N(\theta) = \frac{1}{N} \sum_k \big(y(k) - \varphi(k)^T \theta\big)^2$, a quadratic in $\theta$ | $O(N d)$ |
| simulated output | $y_s = (B/A)\, u$, by the difference equation without $e$ | $O(d)$ per sample |
| frequency response | $G(e^{i\omega}) = B(e^{i\omega})/A(e^{i\omega})$ | $O(d)$ per frequency |
| disturbance spectrum | $\Phi_v(\omega) = \sigma^2 / \lvert A(e^{i\omega}) \rvert^2$ | $O(n_a)$ per frequency |
| static gain | $B(1)/A(1)$, when $A(1) \ne 0$ | $O(d)$ |
| impulse response | $g_j$ from the recursion $A(q)\, g = B(q)\, \delta$ | $O(n_a)$ per coefficient |
| poles and zeros | roots of $z^{n_a} A(z)$ and of the polynomial of $B$ | eigenvalues of companion matrices, $O(d^3)$ |

The disturbance spectrum row shows the limitation of the structure: the noise is shaped by the same $1/A$ that shapes the response to $u$. A plant with a lightly damped pole and white measurement noise does not fit this pattern.

## Relation to other models

- **[Autoregressive model](/autoregressive-model/).** With $n_b = 0$ the ARX model is an AR($n_a$) model of $y$. The time-series view asks for a stationary solution and its autocorrelation. The identification view asks for the predictor of $y(k)$ from the past of $y$ and $u$, which exists and is BIBO stable for every $\theta$.
- **FIR model.** With $n_a = 0$, $y(k) = B(q)\, u(k) + e(k)$: a finite impulse response with white output noise. FIR models need many coefficients for slow systems, but they never have a bias from the noise model in open loop.
- **[ARMAX model](/armax-model/).** Adds a moving average $C(q)\, e(k)$ of the noise, so $H = C/A$. ARX is ARMAX with $C = 1$.
- **[Output error model](/output-error-model/).** Puts white noise on the output instead: $y = (B/F)\, u + e$, so $H = 1$. The model $G$ can be the same as an ARX model, but the predictor is no longer linear in $\theta$.
- **Box-Jenkins model.** $y = (B/F)\, u + (C/D)\, e$, with separate dynamics for $G$ and $H$. ARX, ARMAX and OE are all special cases.
- **[State-space model](/state-space-model/).** Every ARX model has an innovations state-space form of order $\max(n_a, n_k + n_b - 1)$, and the Kalman predictor of that form is exactly $\varphi(k)^T \theta$.
- **[Linear regression](/linear-regression/).** For fixed data the ARX criterion is a linear regression of $y(k)$ on $\varphi(k)$. The regressors are random and correlated with past noise, so the finite-sample results of regression with fixed regressors do not apply as they stand.

## Known results in the model

- **Least squares is the exact minimizer (theorem).** $V_N$ is a convex quadratic in $\theta$, so its minimizers are the solutions of the normal equations $\big(\sum_k \varphi \varphi^T\big) \theta = \sum_k \varphi\, y$. They are unique when the matrix is nonsingular. See [least-squares identification of ARX models](/least-squares-arx-identification/), which also works the six-sample example $\hat\theta = (-0.4851, 0.9655)$.
- **Consistency (theorem).** If the data come from an ARX system of the same orders with white $e$, $A$ Schur, $A$ and $B$ coprime, and an open-loop input that is quasi-stationary, independent of $e$ and [persistently exciting](/persistent-excitation/) of order $n_a + n_b$, then the least squares estimate converges to the true $\theta$ with probability 1 (Ljung 1999, Chapters 8 and 13).
- **Bias under colored noise (theorem and measurement).** If the true equation error is not white, then $\varphi(k)$ is correlated with it through the past outputs, and the least squares limit differs from the true $\theta$. For the worked case with the noise $(1 - q^{-1} + 0.2 q^{-2})\, e$, a white $\pm 1$ input and $N = 50000$, least squares gave $(-1.2286, 0.4547, 0.9965, 0.7650)$ against the true $(-1.5, 0.7, 1, 0.5)$. [Instrumental variable identification](/instrumental-variable-identification/) removes this bias without changing the model.
- **Covariance (theorem).** Under the conditions of the consistency result, $\sqrt{N}(\hat\theta_N - \theta_0)$ is asymptotically normal with covariance $\sigma^2 \big(\mathbb{E}\, \varphi \varphi^T\big)^{-1}$ (Ljung 1999, Chapter 9). For Gaussian $e$ this is the Cramér-Rao bound, so least squares is asymptotically efficient for ARX data.
- **High orders approximate any linear system (theorem).** If the true system is $y = G_0 u + H_0 e$ with BIBO stable $G_0$, $H_0$ and $H_0^{-1}$, an ARX model of order $n$ estimated by least squares gives consistent estimates of $G_0$ and of the noise spectrum when $n \to \infty$ slowly enough with $N$ (Ljung and Wahlberg 1992). This is why a long ARX fit is a common first step before a low-order model.
- **Recursive form.** Because the predictor is linear in $\theta$, the [RLS algorithm](/rls-algorithm/) updates the least squares estimate at each sample in $O(d^2)$ operations, the basis of the [self-tuning regulator](/self-tuning-regulator/).

## References
