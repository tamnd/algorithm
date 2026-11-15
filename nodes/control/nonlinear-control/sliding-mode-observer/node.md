---
tag: V32494
kind: algorithm
slug: sliding-mode-observer
name: Sliding mode observer
aliases:
- sliding mode state observer
area: control/nonlinear-control
level: advanced
summary: An observer with a discontinuous injection term that drives the output error to zero in finite time and is robust to matched uncertainty.
model: real-ram
complexity:
  vars: {N: the number of samples, q: the number of arithmetic operations to evaluate the known model once}
  time: {worst: "O(N q)"}
  space: {extra: "O(1)"}
properties: {deterministic: true, exact: false, recursive: false, online: true}
history:
  year: 1992
  people: [Vadim I. Utkin, Christopher Edwards, Sarah K. Spurgeon, Jorge Davila, Leonid Fridman, Arie Levant]
  note: "Utkin's 1992 book presented observers with switching injection and the equivalent output injection; Edwards and Spurgeon (1998) developed the design for uncertain linear systems; Davila, Fridman and Levant (2005) used the super-twisting algorithm to estimate velocities of mechanical systems in finite time."
prereqs: [sliding-mode-control, super-twisting-algorithm, state-observer]
see_also: [high-gain-observer, luenberger-observer, unknown-input-observer, disturbance-observer, active-disturbance-rejection-control, chattering, kalman-filter, separation-principle]
sources:
  - book: isbn:9783540535164
    title: Vadim I. Utkin, Sliding Modes in Control and Optimization, Springer, 1992
    locator: the chapter on state observers with sliding modes and the equivalent output injection
  - book: isbn:9780748406012
    title: Christopher Edwards and Sarah K. Spurgeon, Sliding Mode Control, Theory and Applications, Taylor and Francis, 1998
    locator: the chapter on sliding mode observers for uncertain linear systems
  - paper: doi:10.1109/TAC.2005.858636
    title: "J. Davila, L. Fridman and A. Levant, Second-order sliding-mode observer for mechanical systems, IEEE Transactions on Automatic Control 50(11), 1785-1789, 2005"
    locator: the super-twisting observer for x1' = x2, x2' = f(t, x1, x2, u) with a measured position, and its finite-time convergence
  - paper: doi:10.1016/S0005-1098(97)00209-4
    title: "A. Levant, Robust exact differentiation via sliding mode technique, Automatica 34(3), 379-384, 1998"
    locator: the robust exact differentiator based on the super-twisting algorithm
---

A sliding mode observer is a [state observer](/state-observer/) whose correction term is a switching function of the output error, instead of the linear term $L_o (y - \hat y)$ of the [Luenberger observer](/luenberger-observer/). The switching term forces the output error to zero in finite time and then keeps it there, even when the model has an unknown bounded term that enters through the same channel as the correction. While the error is held at zero, the average of the switching term equals the unknown term, so the observer also estimates it. This page gives the version for mechanical systems with a measured position, whose correction is the [super-twisting algorithm](/super-twisting-algorithm/), and describes the classical first order form in the variants.

## In plain words

You can measure where a cart is, but not how fast it moves, and you only know part of the forces on it. An observer runs a copy of the cart inside the computer and nudges the copy toward the measured position. A linear observer nudges in proportion to the error, so an unknown force always leaves a small error behind. A sliding mode observer nudges with a fixed strength, always toward the measurement, and its nudge is stronger than the largest unknown force. After a short time the copy sits exactly on the measured position, and its speed matches the real speed. The nudges switch fast between left and right, and their average tells you the unknown force. The weak points are noise on the measurement and the fast switching.

## The problem

**Input.** A system

$$\dot x_1 = x_2, \qquad \dot x_2 = f_0(x_1, u) + F(t, x), \qquad y = x_1,$$

where $x_1$ is a position that is measured, $x_2$ a velocity that is not, $u$ a known input, $f_0$ a known function, and $F$ an unknown term with a known bound $|F(t, x(t))| \le L$ along the motion. Gains $\lambda > 0$ and $\alpha > 0$, a sampling period $h$, and an initial estimate $\hat x(0)$.

**Output.** Estimates $\hat x_1(t), \hat x_2(t)$ with $\hat x(t) = x(t)$ after a finite time in continuous time, and with errors of order $h^2$ in $x_1$ and $h$ in $x_2$ with sampling. Also an estimate of $F$, from the average of the injection term.

The known part $f_0$ depends only on the measured position and the input, so the observer can use it with the measured value. Velocity-dependent terms such as friction go into $F$.

## The algorithm

```pseudo id=main
SMO-STEP(x̂, y, u, f_0, λ, α, h)
L1  e ← y - x̂_1
L2  v_1 ← λ |e|^{1/2} sgn(e); v_2 ← α sgn(e)
L3  x̂_1 ← x̂_1 + h (x̂_2 + v_1)
L4  x̂_2 ← x̂_2 + h (f_0(y, u) + v_2)
L5  return x̂, v_2
```

Line L1 computes the output error. Line L2 computes the two injection terms of the super-twisting law. Lines L3 and L4 take one explicit Euler step of the observer

$$\dot{\hat x}_1 = \hat x_2 + \lambda |e|^{1/2} \operatorname{sgn}(e), \qquad \dot{\hat x}_2 = f_0(y, u) + \alpha \operatorname{sgn}(e).$$

The errors $e_1 = x_1 - \hat x_1$ and $e_2 = x_2 - \hat x_2$ then obey

$$\dot e_1 = e_2 - \lambda |e_1|^{1/2} \operatorname{sgn}(e_1), \qquad \dot e_2 = F(t, x) - \alpha \operatorname{sgn}(e_1),$$

which is the super-twisting closed loop with $s = e_1$, $v = e_2$ and $F$ in the place of $\dot d$. Line L5 returns the estimate and the injection $v_2$, whose average estimates $F$.

## Example

Take a pendulum with unknown friction and an unknown external torque,

$$\dot x_1 = x_2, \qquad \dot x_2 = -9.81 \sin x_1 + F, \qquad F = -0.2 x_2 + 0.5 \sin 2t,$$

with $x(0) = (1, 0)$ and $\hat x(0) = (0, 0)$. The observer knows $f_0(y) = -9.81 \sin y$ and nothing about $F$. Along this motion $|x_2| \le 2.76$ and $|F| \le 1.0$ (measured), and $L = 2$ is a safe bound. The gains $\lambda = 3$, $\alpha = 4$ satisfy the super-twisting condition $\alpha > L + 2L^2/\lambda^2 = 2.89$. The plant is integrated with 4th order Runge-Kutta with step $h = 0.002$, and the observer takes one step per sample.

| $t$ | $e_1$ | $e_2$ |
|---|---|---|
| 0.25 | 0.289902 | -0.919116 |
| 0.5 | -0.058885 | -0.780191 |
| 1 | 0.000009 | -0.006787 |
| 2 | -0.000003 | 0.008478 |

Measurements:

- $|e_2| < 0.05$ for good from $t = 0.774$.
- For $t \ge 3$: $|e_1| \le 2.5 \cdot 10^{-5}$ and $|e_2| \le 0.0207$ with $h = 0.002$; $|e_1| \le 6.3 \cdot 10^{-6}$ and $|e_2| \le 0.0105$ with $h = 0.001$. So $e_1$ is of order $h^2$ and $e_2$ of order $h$.
- The mean of $v_2$ over windows of length $0.5$ matches the mean of $F$ within $0.079$.
- A linear observer with the gains $(20, 100)$, that is $\dot{\hat x}_1 = \hat x_2 + 20 e$, $\dot{\hat x}_2 = f_0 + 100 e$, leaves errors up to $0.0057$ in $x_1$ and $0.12$ in $x_2$, because it has no way to cancel $F$.

## Correctness

The full proof is in proofs/correctness.md. Its main steps:

- **Error equations.** Subtracting the observer from the plant gives the equations above. The known term $f_0(y, u)$ cancels exactly, because the observer evaluates it at the measured $y = x_1$.
- **Theorem (finite-time convergence).** The error equations are the super-twisting closed loop with $s = e_1$, $v = e_2$ and the perturbation $F$ in the $v$ equation. If $|F| \le L$ along the motion and $\alpha > L + 2L^2 / \lambda^2$, the quadratic Lyapunov function of the [super-twisting algorithm](/super-twisting-algorithm/) proves that $e = 0$ after a finite time, with the same bound on that time.
- **Theorem (equivalent output injection).** Once $e_1 = e_2 = 0$, the error equation for $e_2$ gives $0 = F - \alpha \sigma(t)$ almost everywhere, where $\alpha \sigma(t)$ is the Filippov value of the injection. So the injection equals $F$, and any low-pass filter or moving average of $v_2$ estimates $F$.
- **Sampling.** With sampling period $h$, the accuracy is of order $h^2$ in $e_1$ and $h$ in $e_2$ (Levant 1993; Davila, Fridman and Levant 2005). The tests measure it.

The tests check one step by hand, the table, the convergence and accuracy for $h = 0.002$ and $h = 0.001$, the equivalent injection, and the comparison with the linear observer.

## Complexity

Count real operations at unit cost, as in the real RAM. Each sample evaluates $f_0$ once and does a square root, a sign and a few sums, so it costs $O(q)$ time, where $q$ is the cost of $f_0$. The observer keeps two numbers, so the extra space is $O(1)$. A run over $N$ samples costs $O(N q)$.

For a general system of order $n$ with a linear model, the classical first order observer (below) costs $O(n p)$ per sample with $p$ outputs, for the matrix products.

## Properties

- **Finite-time exact estimation.** In continuous time the estimate equals the state after a finite time. A Luenberger or [high-gain observer](/high-gain-observer/) converges only asymptotically, or to a neighborhood when there is an unknown term.
- **Robust to matched uncertainty.** An unknown term in the equation where the injection acts has no effect after convergence. A term in the $\dot x_1$ equation is unmatched and is not rejected.
- **Estimates the unknown input.** The equivalent output injection reconstructs $F$, which is useful for fault detection and for cancelling $F$ in the controller.
- **Separation holds in practice.** Because the error reaches zero in finite time, a controller that uses $\hat x$ uses the true state after that time. With bounded inputs the [separation principle](/separation-principle/) argument then works without the usual linear assumptions, as long as the state stays bounded during the transient.
- **Sensitive to noise.** The square root term reacts strongly to small errors, so measurement noise of size $\varepsilon$ gives an error in $e_2$ of order $\varepsilon^{1/2}$ (Levant 1998, for the differentiator).

## Variants and improvements

- **First order sliding mode observer.** For a linear system $\dot x = A x + B u + D \xi$, $y = C x$, the observer $\dot{\hat x} = A \hat x + B u + L_o (y - C \hat x) + G_n \nu$ with $\nu = \rho \operatorname{sgn}(y - C \hat x)$ (or $\rho (y - C\hat x) / \|y - C\hat x\|$ for several outputs) reaches a sliding mode on $y = C \hat x$ if $\rho$ exceeds the bound on $\xi$ and the matching conditions hold (Edwards and Spurgeon 1998). The injection switches, so its average must be filtered to recover $\xi$.
- **Utkin's cascade observer.** For a system in observable form, a chain of first order sliding modes estimates one state at a time: each step reaches the sliding mode, and the filtered injection of that step is the next measured output (Utkin 1992).
- **Higher order differentiators.** Levant's arbitrary order robust exact differentiator estimates $n$ derivatives of the output in finite time, which gives an observer for systems of order $n + 1$ in observable form.
- **Linear terms.** Adding linear terms $k_1 e$ and $k_2 e$ to the injections speeds up the transient from far away.

## When to use it

Use it when the position (or a similar output) is measured with low noise, the model has an unknown term with a known bound in the equation where the injection acts, and you need the velocity and the unknown term quickly and exactly, for example for fault detection, for friction compensation or for a controller that cancels the disturbance. If the measurement is noisy, a [Kalman filter](/kalman-filter/) or a [high-gain observer](/high-gain-observer/) with a moderate gain is usually better. If the model is accurate, a [Luenberger observer](/luenberger-observer/) with a good linearization is simpler. For linear systems with unknown inputs and no bound, the [unknown input observer](/unknown-input-observer/) decouples them by geometry instead.

## Pitfalls

- **Bound L too small at line L2.** If $|F| > L$ along the motion and $\alpha$ is tuned for $L$, the error can leave zero. Check the bound over the whole range of states, including the transient.
- **Unknown term in f_0 at line L4.** If $f_0$ depends on the unmeasured $x_2$ and the observer uses $\hat x_2$, the difference $f_0(x) - f_0(\hat x)$ adds to $F$, and its bound must be included in $L$.
- **Noise at line L2.** The term $|e|^{1/2}$ amplifies small noise. Filter the measurement with care, because a filter adds delay, and delay also degrades sliding modes.
- **Reading the injection directly.** $v_2$ switches between $\pm \alpha$; it estimates $F$ only after averaging. A window that is too short gives a noisy estimate; one that is too long lags.
- **Large sampling period.** The errors grow like $h^2$ and $h$. With a slow sampling rate, the observer can be worse than a linear one.

## Implementations

## History

Utkin's 1992 book, which collected the Soviet work on sliding modes, described observers that use switching injection and the idea of reading an unknown signal from the average of the switching term, the equivalent output injection. Edwards and Spurgeon developed observers of this kind for uncertain linear systems in the 1990s, with conditions on the system structure under which the unknown inputs can be rejected and reconstructed, and they summarized the work in their 1998 book. After Levant (1998) showed that the super-twisting algorithm gives a robust exact differentiator, Davila, Fridman and Levant (2005) built an observer for mechanical systems on it, which estimates the velocity in finite time from the position alone. Higher order sliding mode observers and differentiators are now a standard tool for fault detection and output feedback.

## References
