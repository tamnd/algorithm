---
tag: SR2Y5Z
kind: model
slug: output-error-model
name: Output error model
aliases:
- OE model
area: control/modeling-and-identification
level: core
summary: A linear model y = (B(q)/F(q))u + e in which white noise adds only to the output and not to the dynamics.
prereqs: [arx-model]
see_also: [armax-model, prediction-error-method, instrumental-variable-identification, closed-loop-identification, frequency-response, impulse-response, persistent-excitation, gauss-newton-algorithm]
sources:
  - book: isbn:9780136566953
    title: "Lennart Ljung, System Identification: Theory for the User, second edition, Prentice Hall, 1999"
    locator: "Chapter 4 (the output error structure), Chapter 7 (prediction error methods) and Chapter 8 (the limit of the criterion in the frequency domain and the consistency of G with a fixed noise model)"
  - book: isbn:9780138812362
    title: "Torsten Söderström and Petre Stoica, System Identification, Prentice Hall, 1989"
    locator: "the chapters on model parametrizations and on prediction error methods"
---

The output error (OE) model is a linear discrete-time model of a system with input $u$ and output $y$, written $y(k) = \big(B(q)/F(q)\big)\, u(k) + e(k)$, where $B$ and $F$ are polynomials in the backward shift $q^{-1}$. It says that the system is a noise-free rational transfer function, and that the measured output is its response plus an error $e$ that does not feed back into the dynamics. The predictor of the model is a pure simulation of $u$ through $B/F$, so fitting it means matching the simulated output to the measured one. When the data come from an open-loop experiment and the system is in the model set, the fitted transfer function converges to the true one whatever the color of the real disturbance. The price is a criterion that is not linear in the coefficients, so the fit needs an iterative search such as the [prediction error method](/prediction-error-method/).

## The machine

**Notation.** Time is discrete, $k \in \mathbb{Z}$, with sampling period $h$; $q^{-1} u(k) = u(k-1)$. $e$ is white noise with mean 0 and variance $\sigma^2$.

**Definition.** With orders $n_b \ge 1$, $n_f \ge 0$ and a delay $n_k \ge 0$,

$$B(q) = q^{-n_k} \sum_{j=1}^{n_b} b_j q^{-j+1}, \qquad F(q) = 1 + \sum_{i=1}^{n_f} f_i q^{-i},$$

the OE model is $y(k) = w(k) + e(k)$ with the undisturbed output $w$ defined by $F(q)\, w(k) = B(q)\, u(k)$. In the form $y = G u + H e$ it has $G = B/F$ and $H = 1$.

**Parameter space.** $\theta = (b, f) \in \mathbb{R}^d$ with $d = n_b + n_f$, restricted to the open set where $F$ is Schur, that is, all roots of $z^{n_f} F(z)$ lie inside the unit circle.

**The predictor.** Since $H = 1$, the predictor ignores past outputs:

$$\hat y(k \mid \theta) = \frac{B(q)}{F(q)}\, u(k) = w(k, \theta), \qquad \varepsilon(k, \theta) = y(k) - w(k, \theta).$$

The predictor is BIBO stable only when $F$ is Schur, which is why the parameter set is restricted. An unstable plant cannot be fitted with this structure.

**The gradient.** Differentiating $F w = B u$ gives

$$\frac{\partial w(k)}{\partial b_j} = \frac{u(k - n_k - j + 1)}{F(q)}, \qquad \frac{\partial w(k)}{\partial f_i} = -\frac{w(k - i)}{F(q)},$$

so $\psi = \partial w/\partial \theta$ is the vector of past inputs and past simulated outputs, both filtered through $1/F$.

**A worked case.** Take $B = q^{-1} + 0.5 q^{-2}$ and $F = 1 - 1.5 q^{-1} + 0.7 q^{-2}$, the same $G$ as the worked case of the [ARX model](/arx-model/). For $u = (1, 1, -1, \ldots)$ from rest, the simulation $w(k) = 1.5\, w(k-1) - 0.7\, w(k-2) + u(k-1) + 0.5\, u(k-2)$ gives $w(0) = 0$, $w(1) = 1$, $w(2) = 3$ and $w(3) = 3.3$. The output error model adds white noise to this sequence; the ARX model with the same $G$ adds the noise $e/A$ instead, which here has the spectrum $25\, \sigma^2$ at $\omega = 0$.

## What it counts

The model has $d + 1$ parameters $(\theta, \sigma^2)$. $N$ is the number of samples.

| quantity | formula | cost |
|---|---|---|
| simulated output | the recursion $F w = B u$ from zero initial values | $O(N d)$ |
| criterion | $V_N(\theta) = \frac{1}{N} \sum_k \big(y(k) - w(k, \theta)\big)^2$ | $O(N d)$ |
| gradient | the filtered regressors $\psi$ above | $O(N d)$ |
| Gauss-Newton matrix | $\frac{1}{N} \sum_k \psi \psi^T$ | $O(N d^2)$ |
| frequency response | $B(e^{i\omega}) / F(e^{i\omega})$ | $O(d)$ per frequency |
| limit criterion, open loop | $\bar V(\theta) = \frac{1}{2\pi} \int_{-\pi}^{\pi} \lvert G_0(e^{i\omega}) - G(e^{i\omega}, \theta) \rvert^2\, \Phi_u(\omega)\, d\omega + \mathbb{E}\, v^2$ | a weighted squared distance of transfer functions |

In the last row the data come from $y = G_0 u + v$ with $u$ independent of the disturbance $v$, and $\Phi_u$ is the input spectrum. The row follows by expanding $\mathbb{E}\,\big((G_0 - G) u + v\big)^2$: the cross term vanishes because $u$ and $v$ are independent.

## Relation to other models

- **[ARX model](/arx-model/).** ARX has $H = 1/A$, OE has $H = 1$. For the same $G$, the ARX predictor is linear in $\theta$ and the OE predictor is not. An ARX fit to OE data is biased, because the equation error $F e$ is colored.
- **[ARMAX model](/armax-model/).** ARMAX ties the noise poles to the system poles. OE and ARMAX are not nested.
- **Box-Jenkins model.** $y = (B/F)\, u + (C/D)\, e$. OE is the case $C = D = 1$. If the true disturbance is colored, Box-Jenkins can fit it and gain efficiency, while OE still gets $G$ right in open loop.
- **FIR model.** OE with $n_f = 0$ is the FIR model $y = B u + e$, which is also ARX with $n_a = 0$, so it is linear in $\theta$.
- **Simulation error.** OE fitting is the same as minimizing the simulation error of a model, which is how many engineers judge a model. ARX fitting minimizes the one-step prediction error, which can be small even for a model that simulates badly.

## Known results in the model

- **Consistent $G$ under colored noise (theorem).** If the data come from $y = G_0 u + v$ with $G_0$ in the model set, $u$ quasi-stationary, independent of $v$, and persistently exciting of order $n_b + n_f$, then $\bar V(\theta) - \mathbb{E}\, v^2$ is a weighted squared distance between $G_0$ and $G(\theta)$. It vanishes only at the true parameters, so the minimizer of $V_N$ gives a consistent $G$ whatever the spectrum of $v$ (Ljung 1999, Chapters 8 and 13). This holds for any fixed noise model, and $H = 1$ is the simplest one.
- **Bias distribution (theorem).** When $G_0$ is not in the model set, the limit model minimizes $\int \lvert G_0 - G \rvert^2 \Phi_u\, d\omega$, so the fit is best where the input has the most power (Ljung 1999, Chapter 8). Shaping $\Phi_u$, or prefiltering $u$ and $y$ by the same filter, moves the frequency range where the model is accurate.
- **The criterion is not convex (computation).** For $G_0 = q^{-1}/(1 - 0.7 q^{-1})$, a white input of unit variance and the model $b q^{-1}/(1 + f q^{-1})$, the excess $\bar V - \mathbb{E}\, v^2$ is $1.9608$ at $(b, f) = (0, 0)$ and $0.8695$ at $(0.5, -0.4)$, but $1.4445$ at the midpoint $(0.25, -0.2)$, above the average $1.4151$. A local search needs a good start; an instrumental variable estimate is the common choice.
- **Measurements on the worked case.** With a white $\pm 1$ input, white $e$ of unit variance and $N = 2000$ samples, the prediction error method gave $\hat b = (1.0308, 0.4617)$ and $\hat f = (-1.5076, 0.7066)$, while an ARX least squares fit of the same data gave $(\hat a, \hat b) = (-1.0644, 0.2957, 1.0666, 0.9306)$, far from the truth.
- **Closed loop breaks the consistency.** In closed loop the input depends on past disturbances, the cross term in $\bar V$ does not vanish, and an OE fit of $G$ is biased unless the noise model is also correct. See [closed-loop identification](/closed-loop-identification/).
- **Efficiency.** With white $e$ the OE estimate is asymptotically efficient. With colored $v$ it is consistent but not efficient: a model with a correct noise model gives a smaller variance.

## References
