---
tag: N0JQXA
kind: technique
slug: averaging-method
name: Averaging method for nonlinear systems
aliases:
- averaging theory
area: control/nonlinear-control
level: advanced
summary: Approximates a system with fast periodic forcing by its time average, which keeps stability of hyperbolic equilibria for small periods.
prereqs: [exponential-stability, gronwall-inequality]
see_also: [singular-perturbation-method, extremum-seeking-control, limit-cycle, describing-function, lyapunov-indirect-method, linear-time-varying-system, sampled-data-system]
sources:
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Chapter 10, Section 10.4 (the averaging theorem, with the O(epsilon) estimate on time intervals of order 1/epsilon and the periodic solution near an exponentially stable equilibrium of the averaged system), and the later sections of Chapter 10 on weakly nonlinear oscillators and general averaging
  - book: isbn:9780387489162
    title: Jan A. Sanders, Ferdinand Verhulst and James Murdock, Averaging Methods in Nonlinear Dynamical Systems, second edition, Springer, 2007
    locator: first-order periodic averaging and its error estimate on the time scale 1/epsilon, and the extension to infinite time under attraction
---

The averaging method approximates a system that is forced by a fast periodic signal with the system whose right side is the time average of the forcing over one period. The averaged system does not depend on time, so its equilibria, stability and phase portrait are easy to study. In the standard form $\dot x = \varepsilon f(t, x, \varepsilon)$ with $f$ periodic in $t$, the solutions of the full and averaged systems stay within $O(\varepsilon)$ of each other on time intervals of length $O(1/\varepsilon)$. If the averaged system has an exponentially stable equilibrium, the full system has an exponentially stable periodic solution near it, and the closeness holds for all time. The method goes back to Krylov and Bogoliubov in the 1930s. In control it explains dither and vibrational stabilization, the gradient behavior of [extremum seeking](/extremum-seeking-control/), and the amplitude of oscillations in weakly nonlinear systems.

## In plain words

Some systems are shaken fast by a periodic input, or contain a part that oscillates fast. Over one fast cycle, the slow state moves only a little, so what matters is the mean push over the cycle, not the push at each instant. The method replaces the shaking by its mean and studies the simpler system that results. The answer is close to the truth for a long time, and the error gets smaller when the shaking gets faster compared with the slow motion. If the simpler system settles at a point, the real system settles near that point, with a small wobble at the period of the shaking. If the simpler system does not settle, the approximation can drift away after a long time.

## When it applies

- The system can be put in the **standard form** $\dot x = \varepsilon f(t, x, \varepsilon)$, with $f$ periodic in $t$ of period $T$ and $\varepsilon > 0$ small. An equal form is $\frac{dx}{ds} = f(s / \varepsilon, x, \varepsilon)$ in the slow time $s = \varepsilon t$: the forcing has the short period $\varepsilon T$.
- $f$ and its partial derivatives with respect to $(x, \varepsilon)$ up to second order are continuous and bounded on $[0, \infty) \times D \times [0, \varepsilon_0]$, for a domain $D$ (Khalil 2002, Section 10.4).
- The question is about time intervals of order $1/\varepsilon$, or the averaged system has an **exponentially stable equilibrium** (more generally, a hyperbolic one), which gives results on infinite time.
- A system that is not yet in standard form, such as a weakly nonlinear oscillator $\ddot y + \omega^2 y = \varepsilon g(y, \dot y)$, can often be put in it by a change to amplitude and phase coordinates.

## The template

1. **Put the system in standard form.** Scale time so that the forcing is fast compared with the drift, or for an oscillator use $y = r \cos \theta$, $\dot y = -\omega r \sin \theta$ with $\theta = \omega t + \phi$. Then $(r, \phi)$ changes at rate $\varepsilon$, and the right side is periodic in $t$.
2. **Average.** Compute $f_{\text{av}}(x) = \frac{1}{T} \int_0^T f(\tau, x, 0)\, d\tau$, with $x$ held fixed during the integration.
3. **Analyze the averaged system** $\dot x_{\text{av}} = \varepsilon f_{\text{av}}(x_{\text{av}})$. Find its equilibria and check their stability with the Jacobian (see [Lyapunov's indirect method](/lyapunov-indirect-method/)).
4. **Apply the averaging theorem** (theorem, Khalil 2002, Section 10.4).
   - *Finite time:* if $x(0) - x_{\text{av}}(0) = O(\varepsilon)$ and $x_{\text{av}}(t)$ stays in a compact subset of $D$ for $t \in [0, b/\varepsilon]$, then there is $\varepsilon^*$ such that $x(t) - x_{\text{av}}(t) = O(\varepsilon)$ on $[0, b/\varepsilon]$ for $0 < \varepsilon < \varepsilon^*$.
   - *Infinite time:* if $p^*$ is an exponentially stable equilibrium of the averaged system, then for small $\varepsilon$ the full system has a unique $T$-periodic solution within $O(\varepsilon)$ of $p^*$, it is exponentially stable, and if $p^* = 0$ is also an equilibrium of the full system for every $\varepsilon$, then 0 is exponentially stable for the full system. A solution that starts in a compact subset of the region of attraction of $p^*$ stays within $O(\varepsilon)$ of the averaged solution for all $t \ge 0$.
5. **Undo the change of coordinates** to read the answer in the original variables, with an $O(\varepsilon)$ periodic wobble on top of the averaged motion.

**Why it works.** The proof is a near-identity change of variables $x = y + \varepsilon w(t, y)$ with $w(t, y) = \int_0^t [f(\tau, y, 0) - f_{\text{av}}(y)]\, d\tau$. The integrand has mean zero, so $w$ is periodic and bounded. In the new variable, $\dot y = \varepsilon f_{\text{av}}(y) + \varepsilon^2 q(t, y, \varepsilon)$ with a bounded $q$. The [Gronwall inequality](/gronwall-inequality/) bounds the effect of the $\varepsilon^2$ term by $O(\varepsilon)$ on $[0, b/\varepsilon]$, and the change of variables adds another $O(\varepsilon)$. On infinite time, exponential stability of the averaged system keeps the errors from adding up.

## Classic examples

**A scalar system with periodic forcing.** For $\dot x = \varepsilon(-x + \sin^2 t)$, $x(0) = 0$, the period is $\pi$ and $f_{\text{av}}(x) = -x + \frac12$. The averaged solution is $x_{\text{av}}(t) = \frac12 (1 - e^{-\varepsilon t})$, and its equilibrium $\frac12$ is exponentially stable. The exact steady state is $\frac12$ plus an oscillation of amplitude $\varepsilon / (2 \sqrt{4 + \varepsilon^2}) \approx \varepsilon / 4$. Measured with RK4 and step 0.01, the largest error $|x(t) - x_{\text{av}}(t)|$ on $[0, 10/\varepsilon]$ is 0.0260 for $\varepsilon = 0.1$ and 0.00251 for $\varepsilon = 0.01$.

**The Van der Pol oscillator.** For $\ddot y + y = \varepsilon (1 - y^2) \dot y$, amplitude and phase coordinates and averaging give $\dot r = \frac{\varepsilon}{2} r \bigl(1 - \frac{r^2}{4}\bigr)$ and $\dot \phi = 0$. The averaged amplitude has an exponentially stable equilibrium at $r = 2$, so the oscillator has a stable [limit cycle](/limit-cycle/) with amplitude $2 + O(\varepsilon)$. From $y(0) = 0.5$, $\dot y(0) = 0$, the averaged amplitude is $r(t) = 2 / \sqrt{1 + 15 e^{-\varepsilon t}}$. Measured with RK4 and step 0.005, the largest error between $\sqrt{y^2 + \dot y^2}$ and $r(t)$ on $[0, 5/\varepsilon]$ is 0.0614, 0.0304 and 0.0151 for $\varepsilon = 0.1$, 0.05 and 0.025. The peak of $y$ on the limit cycle is 2.0001 for $\varepsilon = 0.1$. The [describing function](/describing-function/) method gives the same amplitude by a related first harmonic argument.

**Vibrational stabilization (the Kapitza pendulum).** A pendulum of length $l$ whose pivot moves up and down as $a \cos \omega t$ obeys $\ddot \theta = \frac{1}{l} (g - a \omega^2 \cos \omega t) \sin \theta - c \dot \theta$, with $\theta$ measured from the upright position. After a change of variables and averaging over the fast period, the upright position is stable when $a^2 \omega^2 > 2 g l$. For $l = 1$, $g = 9.81$, $a = 0.1$ the threshold is $\omega = 44.3$ rad/s. Measured with RK4, step 0.0005, damping $c = 0.5$ and $\theta(0) = 0.2$: for $\omega = 60$, $|\theta|$ never exceeds 0.2 and is below 0.0043 after $t = 15$; for $\omega = 35$, the pendulum falls and $|\theta|$ reaches 4.67.

**Extremum seeking.** [Extremum seeking control](/extremum-seeking-control/) adds a small sinusoidal dither $a \sin \omega t$ to a parameter and multiplies the measured cost by the same sinusoid. Averaging shows that the parameter then follows, on average, a gradient descent of the cost, with a gain proportional to $a^2$.

**Switching power converters.** State-space averaging replaces a converter that switches at a high frequency by the average of its two linear models, weighted by the duty cycle. The averaged model is a smooth nonlinear system used for control design. The error is small when the switching period is short compared with the time constants of the filter.

## Variations

- **Higher-order averaging.** Continue the near-identity change of variables to order $\varepsilon^2$ or more. It is needed when the first-order average is zero, as for the Kapitza pendulum, whose effect appears at second order.
- **General averaging.** For forcing that is not periodic, use $f_{\text{av}}(x) = \lim_{T \to \infty} \frac{1}{T} \int_t^{t + T} f(\tau, x, 0)\, d\tau$, when the limit exists uniformly. The error bound then depends on how fast the limit converges, and may be worse than $O(\varepsilon)$.
- **Hyperbolic equilibria.** If the averaged system has a hyperbolic equilibrium that is not stable, such as a saddle, the full system has a hyperbolic periodic solution of the same type nearby (theorem, Sanders, Verhulst and Murdock 2007). This is the sense of the summary.
- **Averaging with a slow and a fast state.** When some states change fast and are not periodic, combine averaging with the [singular perturbation method](/singular-perturbation-method/).
- **Linear periodic systems.** For $\dot x = \varepsilon A(t) x$ with $A$ periodic, the averaged system is $\dot x = \varepsilon \bar A x$. If $\bar A$ is Hurwitz, the [linear time-varying system](/linear-time-varying-system/) is exponentially stable for small $\varepsilon$.

## Pitfalls

- **Using the result beyond time $1/\varepsilon$.** The finite-time estimate holds on $[0, b/\varepsilon]$ only. Without exponential stability of the averaged system, the error can grow after that, and long simulations of the averaged model can be wrong.
- **A center in the averaged system.** If the averaged system has an equilibrium that is stable but not asymptotically stable, such as the undamped Kapitza pendulum, which averages to a conservative system, averaging decides nothing about stability on infinite time. Add damping or go to a higher order.
- **A zero first-order average.** If $f_{\text{av}} = 0$, the averaged system says nothing. The effect is in a higher-order term, as with vibrational stabilization.
- **Forcing that is not fast enough.** The theorem gives existence of $\varepsilon^*$ but not its size. In the Kapitza example, $\omega = 35$ rad/s looks fast compared with the natural rate $\sqrt{g/l} = 3.1$ rad/s, but it is below the threshold and the pendulum falls. Check the prediction with a simulation of the full system.
- **The wrong standard form.** Averaging $\dot x = f(t, x)$ when the drift of $x$ is not slow compared with the period gives a wrong answer. The factor $\varepsilon$ must be there, after a scaling.
- **Resonance.** For oscillators with several frequencies, combinations that are near zero (small divisors) make $w$ in the near-identity transformation large, and the simple average must be replaced by an average that keeps the resonant terms.

## Exercises

1. Average $\dot x = \varepsilon (-x + \cos^2 t)\, x$ and find the equilibria of the averaged system and their stability.
2. For $\ddot y + y = \varepsilon(1 - y^2) \dot y$, derive the averaged equation for $r$ from $y = r \cos(t + \phi)$, $\dot y = -r \sin(t + \phi)$.
3. For the scalar example, solve the full equation exactly and show that the steady-state oscillation has amplitude $\varepsilon / (2 \sqrt{4 + \varepsilon^2})$.
4. Show that for $\dot x = \varepsilon A(t) x$ with $A$ of period $T$, the near-identity change of variables gives $\dot y = \varepsilon \bar A y + O(\varepsilon^2) y$, and conclude exponential stability when $\bar A$ is Hurwitz.
5. For the Kapitza pendulum, linearize the averaged equation near the upright position and derive the condition $a^2 \omega^2 > 2 g l$.

## References
