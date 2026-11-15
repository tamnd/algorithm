---
tag: R10NPS
kind: model
slug: second-order-system
name: Standard second-order system
aliases:
- damped harmonic oscillator model
area: control/classical-control
level: intro
summary: "The transfer function omega_n^2 / (s^2 + 2 zeta omega_n s + omega_n^2). The damping ratio zeta and the natural frequency omega_n fix the overshoot, the speed and the resonance in closed form."
prereqs: [transfer-function, laplace-transform, poles-and-zeros]
see_also: [step-response-specifications, root-locus, complementary-sensitivity-function, phase-margin, h2-norm, h-infinity-norm, state-space-representation, zero-order-hold-discretization]
sources:
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Chapter 3, Dynamic Response (the poles of a second-order system, the time-domain specifications, and the effects of zeros and extra poles)
  - book: isbn:9780136156734
    title: Katsuhiko Ogata, Modern Control Engineering, fifth edition, Prentice Hall, 2010
    locator: Chapter 5, Transient and Steady-State Response Analyses (second-order systems and their step response specifications), and Chapter 7 (the resonant peak and frequency of the second-order system)
  - book: isbn:9780691193984
    title: Karl J. Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Chapter 6, Linear Systems (the step response and its specifications), and Chapter 7, State Feedback (second-order systems and the damping ratio)
---

The standard second-order system is the linear model with the [transfer function](/transfer-function/)

$$G(s) = \frac{\omega_n^2}{s^2 + 2 \zeta \omega_n s + \omega_n^2},$$

with the natural frequency $\omega_n > 0$ in rad/s and the dimensionless damping ratio $\zeta \ge 0$. It is the damped harmonic oscillator with unit static gain: a mass on a spring with a damper, or a series RLC circuit. Two numbers fix all of its behavior, and the overshoot, the peak time, the resonant peak and the bandwidth have exact formulas in $\zeta$ and $\omega_n$. That is why closed-loop specifications are often stated as a target pair of poles $-\zeta\omega_n \pm j\omega_n\sqrt{1 - \zeta^2}$, and why a higher-order loop is often read through a "dominant" second-order pair. That reading is an approximation, and this page says when it fails.

## The machine

**Equations.** The input $u(t)$ and the output $y(t)$ are real, and time $t \ge 0$ is continuous, in seconds. The model is the linear ordinary differential equation

$$\ddot y + 2\zeta\omega_n \dot y + \omega_n^2 y = \omega_n^2 u.$$

With zero initial conditions and the one-sided [Laplace transform](/laplace-transform/), $Y(s) = G(s)\,U(s)$. A [state-space representation](/state-space-representation/) with the state $x = (y, \dot y) \in \mathbb{R}^2$ is

$$\dot x = \begin{bmatrix} 0 & 1 \\ -\omega_n^2 & -2\zeta\omega_n \end{bmatrix} x + \begin{bmatrix} 0 \\ \omega_n^2 \end{bmatrix} u, \qquad y = \begin{bmatrix} 1 & 0 \end{bmatrix} x.$$

This realization is minimal, so the poles of $G$ are the eigenvalues of the matrix.

**Physical forms.** A mass $m$ (kg) on a spring of stiffness $k$ (N/m) with a damper $c$ (N s/m), driven by the force $k u$, obeys $m \ddot y + c \dot y + k y = k u$. So $\omega_n = \sqrt{k/m}$ and $\zeta = c/(2\sqrt{k m})$. A series RLC circuit with the output at the capacitor has $\omega_n = 1/\sqrt{L C}$ and $\zeta = (R/2)\sqrt{C/L}$.

**Poles.** The poles are $s = -\zeta\omega_n \pm \omega_n\sqrt{\zeta^2 - 1}$. There are four cases:

| case | $\zeta$ | poles |
|---|---|---|
| undamped | $\zeta = 0$ | $\pm j \omega_n$ |
| underdamped | $0 < \zeta < 1$ | $-\sigma \pm j\omega_d$, with $\sigma = \zeta\omega_n$ and $\omega_d = \omega_n\sqrt{1 - \zeta^2}$ |
| critically damped | $\zeta = 1$ | $-\omega_n$, twice |
| overdamped | $\zeta > 1$ | two distinct negative real poles $p_1, p_2$ with $p_1 p_2 = \omega_n^2$ |

In the underdamped case the poles lie on the circle of radius $\omega_n$, at the angle $\theta = \arccos \zeta$ from the negative real axis. So $\zeta$ fixes the angle of the poles and $\omega_n$ their distance from the origin. For $\zeta < 0$ the poles are in the right half plane and the system is unstable; the formulas below assume $\zeta > 0$ unless they say otherwise.

## What it counts

The model predicts the whole response to any input from the two parameters. The usual uses are:

- **Step response numbers.** The overshoot, the peak time, the rise time and the settling time of the [step response specifications](/step-response-specifications/), as exact functions or bounds in $\zeta$ and $\omega_n$.
- **Frequency response numbers.** The resonant peak, the resonant frequency and the bandwidth.
- **Parameter fits.** From a measured step response with overshoot $M_p$ and peak time $t_p$, the inverse formulas give $\zeta = -\ln M_p / \sqrt{\pi^2 + \ln^2 M_p}$ and $\omega_n = \pi/(t_p\sqrt{1 - \zeta^2})$. With $M_p = 0.16303$ and $t_p = 3.6276$ s they return $\zeta = 0.5$ and $\omega_n = 1$ rad/s. The fit is exact only if the plant is of this form; on a real plant it is a measurement with an error.

## Relation to other models

- **First-order system** $1/(\tau s + 1)$: the limit of an overdamped second-order system when one pole is much faster than the other. It never overshoots.
- **Higher-order systems with a dominant pair.** If a [linear time-invariant system](/linear-time-invariant-system/) has a pair of complex poles much closer to the imaginary axis than all other poles and zeros, its step response is close to that of the pair with the same static gain. This is a design approximation, not a theorem with a stated error. It fails when a zero is near the pair (a zero at $-a$ adds the term $(1/a)\,\dot y$ and raises the overshoot), when a third pole is not far away (it slows the response and lowers the overshoot), and when a pole and a zero nearly cancel (they leave a slow tail). A ratio of 5 to 10 between the real parts is a common rule of thumb.
- **Second-order system with a zero.** $\omega_n^2 (s/a + 1)/(s^2 + 2\zeta\omega_n s + \omega_n^2)$; for $a < 0$ the zero is in the right half plane and the step response starts in the wrong direction.
- **Discrete time.** Sampling with a zero-order hold and the period $h$ maps the poles to $e^{p h}$; see [zero-order-hold discretization](/zero-order-hold-discretization/).
- **As a closed loop.** The loop transfer function $L(s) = \omega_n^2/(s(s + 2\zeta\omega_n))$ in a unity feedback loop gives the closed loop $T = G$. So the model is also the closed loop of a type 1 plant with a proportional controller; see [complementary sensitivity function](/complementary-sensitivity-function/).

## Known results in the model

All results below are exact for the model, and each one follows from the formula for $y$ in a few lines.

**Step response.** For a unit step input and zero initial state,

- underdamped: $y(t) = 1 - e^{-\sigma t}\left(\cos \omega_d t + \frac{\sigma}{\omega_d} \sin \omega_d t\right) = 1 - \frac{e^{-\sigma t}}{\sqrt{1 - \zeta^2}} \sin(\omega_d t + \theta)$, with $\theta = \arccos\zeta$;
- undamped: $y(t) = 1 - \cos \omega_n t$;
- critically damped: $y(t) = 1 - e^{-\omega_n t}(1 + \omega_n t)$;
- overdamped: $y(t) = 1 + \frac{p_2 e^{p_1 t} - p_1 e^{p_2 t}}{p_1 - p_2}$.

Each follows from the [partial fraction decomposition](/partial-fraction-decomposition/) of $G(s)/s$. The [impulse response](/impulse-response/) is the derivative; in the underdamped case it is $g(t) = \frac{\omega_n}{\sqrt{1 - \zeta^2}}\, e^{-\sigma t} \sin \omega_d t$.

**Peak time and overshoot** ($0 < \zeta < 1$). The derivative $\dot y = g$ is zero at $t = k\pi/\omega_d$, $k = 1, 2, \ldots$, and the largest value is at $k = 1$, where $\cos \omega_d t = -1$ and $\sin \omega_d t = 0$. So

$$t_p = \frac{\pi}{\omega_d}, \qquad M_p = y(t_p) - 1 = e^{-\zeta\pi/\sqrt{1 - \zeta^2}}.$$

For $\zeta = 0.5$ and $\omega_n = 1$: $t_p = 3.62760$ s and $M_p = 0.16303$. For $\zeta \ge 1$ there is no overshoot. The overshoot depends on $\zeta$ only.

**Rise time.** The first time $y = 1$ is $t = (\pi - \theta)/\omega_d$, the 0 to 100 percent rise time; for $\zeta = 0.5$, $\omega_n = 1$ it is 2.4184 s. The 10 to 90 percent rise time has no closed form; for $\zeta = 0.5$, $\omega_n = 1$ it is 1.6376 s. The formula $t_r \approx 1.8/\omega_n$ is a rule of thumb, tuned near $\zeta = 0.5$.

**Settling time.** The response stays inside the envelope $1 \pm e^{-\sigma t}/\sqrt{1 - \zeta^2}$. So the response is inside the band $\pm\varepsilon$ for all $t \ge t_\varepsilon$ with

$$t_\varepsilon = \frac{1}{\zeta\omega_n} \ln \frac{1}{\varepsilon\sqrt{1 - \zeta^2}},$$

which is an upper bound on the true settling time. For $\zeta = 0.5$, $\omega_n = 1$ and $\varepsilon = 0.02$, the bound is 8.1117 s and the true 2 percent settling time is 8.0763 s. The common formula $4/(\zeta\omega_n)$ drops the factor $\sqrt{1 - \zeta^2}$ and rounds $\ln 50 = 3.912$ to 4; it gives 8 s here and is a rule of thumb. For the 5 percent band, the true value is 5.2891 s and the rule $3/(\zeta\omega_n)$ gives 6 s.

**Frequency response.** With $u = \omega/\omega_n$,

$$|G(j\omega)|^2 = \frac{1}{(1 - u^2)^2 + 4\zeta^2 u^2}, \qquad \angle G(j\omega) = -\operatorname{atan2}(2\zeta u,\ 1 - u^2).$$

The phase is $-90$ degrees at $\omega = \omega_n$ for every $\zeta$. Minimizing the denominator over $u^2$ gives:

- *Resonance.* For $\zeta < 1/\sqrt 2$, the peak is $M_r = 1/(2\zeta\sqrt{1 - \zeta^2})$ at $\omega_r = \omega_n\sqrt{1 - 2\zeta^2}$. For $\zeta \ge 1/\sqrt 2$, $|G|$ decreases from 1 and there is no resonance. For $\zeta = 0.1$: $M_r = 5.02519$ at $\omega_r = 0.98995\,\omega_n$. For $\zeta = 0.5$: $M_r = 1.1547$.
- *Bandwidth.* $|G(j\omega_B)| = 1/\sqrt 2$ at $\omega_B = \omega_n \sqrt{1 - 2\zeta^2 + \sqrt{4\zeta^4 - 4\zeta^2 + 2}}$; for $\zeta = 0.5$, $\omega_B = 1.2720\,\omega_n$.

**System norms.** The [H-infinity norm](/h-infinity-norm/) is $M_r$ for $\zeta < 1/\sqrt 2$ and 1 otherwise. The [H2 norm](/h2-norm/) satisfies $\|G\|_2^2 = \int_0^\infty g(t)^2\,dt = \omega_n/(4\zeta)$ for $\zeta > 0$. For $\zeta = 0.1$, $\omega_n = 1$, that is $G(s) = 1/(s^2 + 0.2 s + 1)$, the norms are 5.02519 and $\sqrt{2.5} = 1.58114$.

**As a unity feedback loop.** For $L(s) = \omega_n^2/(s(s + 2\zeta\omega_n))$, $|L(j\omega_c)| = 1$ at $\omega_c = \omega_n\sqrt{\sqrt{1 + 4\zeta^4} - 2\zeta^2}$, and the phase margin is $\varphi_m = \arctan(2\zeta\omega_n/\omega_c)$. For $\zeta = 0.5$ it is 51.83 degrees. The rule $\varphi_m \approx 100\,\zeta$ degrees for $\zeta \le 0.6$ is a fit to this formula, not an identity. The velocity error constant is $K_v = \omega_n/(2\zeta)$ (in 1/s), so a ramp is followed with the [steady-state error](/steady-state-error/) $2\zeta/\omega_n$.

**Design regions.** A bound $M_p \le \bar M$ is the same as $\zeta \ge \bar\zeta$, a sector around the negative real axis; a bound on the 0 to 100 percent rise time or on $t_p$ bounds $\omega_d$; the settling bound bounds $\sigma = \zeta\omega_n$ from below. These regions in the $s$ plane are what the [root locus](/root-locus/) method aims at. For a loop of higher order they are targets for the dominant pair, with the caveats above.

## References
