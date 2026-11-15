---
tag: 7TPQZY
kind: model
slug: time-delay-system
name: Time-delay system
aliases:
- dead-time system
- system with transport delay
area: control/modeling-and-identification
level: core
summary: "A system whose rate of change depends on past states or inputs, with a delay tau. Its transfer function has the factor e^(-s tau), which is not rational, and its state is a function on [-tau, 0]."
prereqs: [laplace-transform, state-space-representation]
see_also: [smith-predictor, pade-approximation, process-reaction-curve, phase-margin, nyquist-stability-criterion, laplace-transform, sampled-data-system, linear-time-invariant-system]
sources:
  - paper: doi:10.1016/S0005-1098(03)00167-5
    title: Jean-Pierre Richard, Time-delay systems, an overview of some recent advances and open problems, Automatica 39(10), 2003
    locator: pp. 1667 to 1694 (the classes of delay equations, the characteristic quasi-polynomial and the Lyapunov-Krasovskii approach)
  - book: isbn:9780817642129
    title: Keqin Gu, Vladimir L. Kharitonov and Jie Chen, Stability of Time-Delay Systems, Birkhäuser, 2003
    locator: the chapters Introduction to Time-Delay Systems and Systems with Single Delay (frequency-domain tests and Lyapunov-Krasovskii functionals)
  - book: isbn:9780387940762
    title: Jack K. Hale and Sjoerd M. Verduyn Lunel, Introduction to Functional Differential Equations, Applied Mathematical Sciences 99, Springer, 1993
    locator: the whole book (existence and uniqueness, the state space of continuous functions, the characteristic equation and stability of retarded and neutral equations)
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Section 6.8, Time Delay (the phase lag of a delay in the frequency response, and Pade approximations), and Section 5.6.3, Time Delay (an online section)
---

A time-delay system is a dynamical system whose rate of change at time $t$ depends on values of the state or the input at an earlier time $t - \tau$. Delays come from transport (a fluid in a pipe, a belt, a signal on a network), from computation and from measurement. In process control a delay is also called dead time. The simplest case, a pure delay $y(t) = u(t - \tau)$, has the transfer function $e^{-s\tau}$: it does not change the gain of a sinusoid, but it adds a phase lag of $\omega\tau$ radians at frequency $\omega$, and that lag grows without bound. Because of this, a delay limits the bandwidth of every feedback loop around it. A delay system is not finite dimensional: its transfer function is not rational, and its characteristic equation has infinitely many roots.

## The machine

**Notation.** The delay is $\tau > 0$ in seconds. Write $x_t$ for the segment of the past state, $x_t(\theta) = x(t + \theta)$ for $\theta \in [-\tau, 0]$.

**Input and output delay.** A linear time-invariant system with a delay at the input is $x'(t) = A x(t) + B u(t - \tau)$, $y = C x$. Its transfer function is $C(sI - A)^{-1} B\, e^{-s\tau}$, by the time shift rule of the [Laplace transform](/laplace-transform/). A common process model of this kind is the first-order plus dead time model $K e^{-s\tau}/(T_1 s + 1)$, with gain $K$, time constant $T_1$ and delay $\tau$, which the [process reaction curve](/process-reaction-curve/) fits from a step test.

**State delay.** A linear retarded system with one delay is

$$x'(t) = A_0 x(t) + A_1 x(t - \tau) + B u(t), \qquad x_0 = \varphi \in C([-\tau, 0], \mathbb{R}^n).$$

The initial condition is a whole function $\varphi$ on $[-\tau, 0]$, not a vector. The state at time $t$ is the segment $x_t$, an element of the infinite-dimensional space $C([-\tau, 0], \mathbb{R}^n)$. *Retarded* means that the highest derivative appears without delay. A *neutral* system also has delayed derivatives, as in $x'(t) - D x'(t - \tau) = A_0 x(t) + A_1 x(t - \tau)$; it needs extra conditions on $D$, and the results below are for retarded systems.

**Solutions by steps.** On $[0, \tau]$ the term $A_1 x(t - \tau) = A_1 \varphi(t - \tau)$ is known, so the equation is an ordinary differential equation for $x$ on that interval. Its solution gives the history for $[\tau, 2\tau]$, and so on. So for continuous $\varphi$ and a locally integrable input, a unique solution exists for all $t \ge 0$ (a theorem; the general nonlinear case is in Hale and Verduyn Lunel). The solution need not be smooth at $t = 0$, but each step makes it one derivative smoother.

**Characteristic equation.** Trying $x(t) = e^{st} v$ with $u = 0$ gives

$$\det\bigl(sI - A_0 - A_1 e^{-s\tau}\bigr) = 0,$$

a *quasi-polynomial* equation in $s$ and $e^{-s\tau}$. It has infinitely many roots. For a retarded system, only finitely many roots lie in any half plane $\operatorname{Re} s > c$, and the system is exponentially stable exactly when every root has $\operatorname{Re} s < 0$ (a theorem). With input delay only, the characteristic equation of a feedback loop has this form as well: unity feedback around $G_0(s) e^{-s\tau}$ gives $1 + G_0(s) e^{-s\tau} = 0$.

**Discrete time.** In discrete time a delay of $d$ samples is $z^{-d}$, which is rational. It adds $d$ states (a shift register), so a sampled delay system is finite dimensional. With a sampling period $h$, a delay $\tau = d h$ becomes $z^{-d}$ exactly; see [sampled-data system](/sampled-data-system/).

## What it counts

- **Phase lag.** At frequency $\omega$, $e^{-i\omega\tau}$ has gain 1 and phase $-\omega\tau$ rad. At $\omega\tau = 1$ the lag is $57.3$ degrees.
- **Delay margin.** For a loop $L(s)$ with negative feedback, the delay margin is the least extra delay $\tau$ in the loop that makes the closed loop not asymptotically stable. If $|L(i\omega)| = 1$ at exactly one frequency $\omega_c$ and the closed loop is asymptotically stable with the [phase margin](/phase-margin/) $\varphi_m$ in radians, the delay margin is $\varphi_m/\omega_c$: the delay reduces the phase at $\omega_c$ by $\omega_c\tau$ and changes nothing else on the gain crossover.
- **Characteristic roots.** The rightmost roots of the quasi-polynomial, which fix the decay rate of the solutions.

## Relation to other models

- **Finite-dimensional LTI systems.** With $\tau = 0$ the model is an ordinary [linear time-invariant system](/linear-time-invariant-system/). The transfer function $G_0(s) e^{-s\tau}$ has the same gain as $G_0$ at every frequency but more phase lag. So a delay acts like an all-pass factor with zeros in the right half plane, such as $(1 - s)/(1 + s)$: both add phase lag without changing the gain, and both limit the achievable bandwidth.
- **Rational approximation.** The [Padé approximation](/pade-approximation/) replaces $e^{-s\tau}$ by an all-pass rational function. The first-order one is $(1 - s\tau/2)/(1 + s\tau/2)$, and the second-order one is $(1 - s\tau/2 + (s\tau)^2/12)/(1 + s\tau/2 + (s\tau)^2/12)$. Both have gain exactly 1 on the imaginary axis, so the error is in the phase only:

| $\omega\tau$ | exact phase (deg) | first order (deg) | second order (deg) |
|---|---|---|---|
| 0.5 | -28.65 | -28.07 | -28.65 |
| 1 | -57.30 | -53.13 | -57.22 |
| 2 | -114.59 | -90.00 | -112.62 |
| 3 | -171.89 | -112.62 | -161.08 |

A Padé model is a design rule of thumb, not an equivalent model: it is accurate only below some $\omega\tau$ (for the first-order form, up to about $\omega\tau = 1$), and it has right half plane zeros that the delay does not have. Check a design based on it against the exact delay.
- **Sampled data.** A zero-order hold behaves, at frequencies well below the sampling rate, like a delay of $h/2$ (a rule of thumb used to estimate the phase cost of sampling).
- **Smith predictor.** The [Smith predictor](/smith-predictor/) uses a model of the delay inside the controller so that, when the model is exact, the delay leaves the characteristic equation.

## Known results in the model

- **The scalar equation (a theorem).** $x'(t) = -k x(t - \tau)$ with $k > 0$ is asymptotically stable if and only if $k\tau < \pi/2$. Proof sketch: for $\tau = 0$ the only root of $s + k e^{-s\tau} = 0$ is $-k$, and as $\tau$ grows the roots move continuously, with the new roots coming from $\operatorname{Re} s = -\infty$. A root crosses the imaginary axis at $s = i\omega$ only if $k\cos\omega\tau = 0$ and $\omega = k \sin\omega\tau$, which first happens at $\omega = k$, $k\tau = \pi/2$. A numerical solution with $\tau = 1$ (a measurement) decays for $k = 1.4$ and $1.5$ and grows for $k = 1.65$ and $1.7$.
- **An integrator loop.** The same equation is the closed loop of unity negative feedback around $L(s) = k e^{-s\tau}/s$. Here $\omega_c = k$ and the phase margin is $90 - k\tau \cdot 180/\pi$ degrees; for $k = 1$ and $\tau = 0.5$ it is $61.35$ degrees. Without delay the delay margin is $\pi/(2k)$, which agrees with the bound $k\tau < \pi/2$.
- **A third-order loop.** For $L(s) = 1/(s(s + 1)(s + 2))$ there is one gain crossover, at $\omega_c = 0.44575$ rad/s, with the phase margin $53.41$ degrees, so the delay margin is $0.93219/0.44575 = 2.0913$ s.
- **Stability for all delays (a theorem).** If there are symmetric $P > 0$ and $Q > 0$ with
$$\begin{pmatrix} A_0^{\mathsf T} P + P A_0 + Q & P A_1 \\ A_1^{\mathsf T} P & -Q \end{pmatrix} < 0,$$
then $x' = A_0 x + A_1 x(t - \tau)$ is asymptotically stable for every $\tau \ge 0$. The proof uses the Lyapunov-Krasovskii functional $V(x_t) = x(t)^{\mathsf T} P x(t) + \int_{t - \tau}^{t} x(\theta)^{\mathsf T} Q\, x(\theta)\, d\theta$, whose derivative along solutions is the quadratic form of this matrix in $(x(t), x(t - \tau))$. Conditions that depend on $\tau$, such as the bound $k\tau < \pi/2$ above, need functionals with more terms; Gu, Kharitonov and Chen treat them.
- **The Nyquist test.** For a loop $G_0(s) e^{-s\tau}$ with a rational $G_0$, the [Nyquist stability criterion](/nyquist-stability-criterion/) still holds, with the plot of $G_0(i\omega) e^{-i\omega\tau}$, which spirals in toward the origin when $G_0$ is strictly proper.

## References
