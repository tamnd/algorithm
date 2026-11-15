---
tag: 4JVRZW
kind: technique
slug: describing-function
name: Describing function method
aliases:
- describing function analysis
- harmonic balance method
area: control/stability
level: core
summary: Replaces a nonlinearity by its gain on a sinusoid, and predicts limit cycles where the Nyquist plot meets minus the inverse describing function.
prereqs: [nyquist-plot, limit-cycle]
see_also: [limit-cycle, nyquist-plot, relay-autotuning, lure-problem, circle-criterion, popov-criterion, averaging-method, nyquist-stability-criterion]
sources:
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 7.2, The Describing Function Method
  - book: isbn:9780070231245
    title: Arthur Gelb and Wallace E. Vander Velde, Multiple-Input Describing Functions and Nonlinear System Design, McGraw-Hill, 1968
    locator: Chapter 2, the sinusoidal-input describing function and its tables for common nonlinearities
  - paper: "N. Krylov and N. Bogoliubov, Introduction to Non-Linear Mechanics, translated by S. Lefschetz, Annals of Mathematics Studies 11, Princeton University Press, 1943"
    locator: the method of equivalent linearization by the first harmonic
---

The describing function method predicts whether a feedback loop with one nonlinear element oscillates, and if so with what amplitude and frequency. It replaces the nonlinearity by its gain on a sinusoid: the ratio of the first harmonic of its output to the input sinusoid. This gain $N(a)$ depends on the amplitude $a$ and, for elements with memory, on the frequency. The loop can then sustain the oscillation $a \sin \omega t$ when $G(j\omega) N(a) = -1$, where $G$ is the linear part. Graphically, the [Nyquist plot](/nyquist-plot/) of $G$ meets the curve of $-1/N(a)$. The method is approximate. It assumes that the linear part removes the higher harmonics, and it can predict a [limit cycle](/limit-cycle/) that does not exist, or miss one that does. It is still the usual first tool for oscillations in relay loops, loops with saturation, backlash and friction, and it is the basis of [relay autotuning](/relay-autotuning/). The idea of keeping only the first harmonic goes back to Krylov and Bogoliubov in the 1930s. In control it was developed around 1950 by several authors independently, among them Kochenburger in the United States and Goldfarb in the Soviet Union.

## In plain words

Put a sine wave of amplitude $a$ into the nonlinear element. The output repeats with the same period, but it is not a sine wave: a relay, for example, gives a square wave. Keep only the part of the output at the input frequency, and divide it by the input. The result is a gain, possibly with a phase shift, that changes with $a$. Now treat the loop as linear with this gain. A loop oscillates without decay or growth when the signal comes back around the loop with the same size and the same phase, that is, when the total gain at that frequency is exactly $-1$ in negative feedback. Solve this for the amplitude and the frequency. The answer is correct to the extent that the linear part blocks the harmonics that were dropped.

## When it applies

- The loop has one nonlinear element $u = \phi(e)$ in negative feedback with a linear time-invariant part $y = G(s) u$, $e = -y$, after a block diagram rearrangement. This is the structure of the [Lur'e problem](/lure-problem/).
- $\phi$ is odd, or at least has no bias, so that a symmetric oscillation is plausible. A static $\phi$ gives a real $N(a)$. An element with memory, such as a relay with hysteresis or backlash, gives a complex $N(a)$.
- $G$ is low pass: $|G(jk\omega)|$ is much smaller than $|G(j\omega)|$ for $k = 2, 3, \dots$ near the predicted frequency. This is the *filtering hypothesis*. A plant with two or more poles beyond the oscillation frequency usually satisfies it.
- One wants a quick estimate of the amplitude and period of an oscillation, or a design rule to avoid it. For a proof that no oscillation exists, use the [circle criterion](/circle-criterion/) or the [Popov criterion](/popov-criterion/); for a proof that one exists, use the [averaging method](/averaging-method/) or a rigorous error bound.

## The template

1. **Compute the describing function.** For $e = a \sin \theta$, $\theta = \omega t$, let $b_1 = \frac{1}{\pi} \int_0^{2\pi} \phi(a \sin \theta) \sin \theta \, d\theta$ and $a_1 = \frac{1}{\pi} \int_0^{2\pi} \phi(a \sin \theta) \cos \theta \, d\theta$. Then $N(a) = (b_1 + j a_1)/a$. For a static odd $\phi$, $a_1 = 0$.
2. **Write the harmonic balance equation.** With $e \approx a \sin \omega t$, $u \approx$ the first harmonic, $y = G u$ and $e = -y$, the first harmonics balance when $G(j\omega) N(a) + 1 = 0$, or $G(j\omega) = -1/N(a)$.
3. **Solve it.** For a real $N$, the right side is real and negative, so $\omega$ is a phase crossover frequency of $G$, where $\arg G(j\omega) = -180°$, and $N(a) = -1/G(j\omega)$ gives $a$. For a complex $N$, solve the two real equations for $(\omega, a)$, or intersect the Nyquist plot with the curve $-1/N(a)$ on a plot.
4. **Decide whether the cycle attracts.** Replace $N(a)$ by a constant gain $k$. Suppose that the loop is asymptotically stable for $k$ just below the balance value $r = N(a^*)$ and unstable just above it. If $N$ decreases with $a$, then a slightly larger amplitude gives a smaller gain and decays, and a slightly smaller amplitude grows: the predicted cycle attracts. If $N$ increases with $a$, it repels. On the Nyquist plot this is the Loeb criterion: the cycle attracts when the point $-1/N(a)$ moves out of the region that the plot encircles as $a$ grows.
5. **Check the filtering hypothesis.** Compare $|G(3j\omega)|$ with $|G(j\omega)|$; for an odd $\phi$ the third harmonic is the largest one dropped. Confirm the prediction by a simulation whenever the result matters.

The implementation does steps 3 to 5 for a real describing function:

```pseudo id=main
HARMONIC-BALANCE(G, N, [ω_lo, ω_hi], [a_lo, a_hi])             ▷ N(a) real, negative feedback
L1  find ω* in [ω_lo, ω_hi] with Im G(jω*) = 0 by bisection; NONE if Im G does not change sign
L2  g ← Re G(jω*); if g ≥ 0 then return NONE                   ▷ the crossing must be on the negative real axis
L3  r ← -1/g                                                  ▷ harmonic balance needs N(a) = r
L4  if N(a_lo) - r and N(a_hi) - r have the same sign then return NONE
L5  find a* in [a_lo, a_hi] with N(a*) = r by bisection
L6  s ← dN/da at a*, by a central difference
L7  q ← |G(3jω*)| / |G(jω*)|                                   ▷ small q supports the filtering hypothesis
L8  return (a*, ω*, period 2π/ω*, attracting if s < 0, q)
```

Line L8 uses the rule of step 4, so it assumes that the loop with a constant gain becomes unstable as the gain passes $r$. The module also has the closed forms below, a numerical $N(a)$ by the midpoint rule for any static $\phi$, a Newton solver for a complex $N(a)$, and a simulation of the loop with the [classical Runge-Kutta method](/classical-runge-kutta-4/) to compare the prediction with the true oscillation.

## Classic examples

**Common describing functions.** For a nonlinearity with slope $k$ and break point $\delta$, and with $\rho = \delta / a$:

| Element | $N(a)$ |
|---|---|
| ideal relay, output $\pm d$ | $\dfrac{4d}{\pi a}$ |
| saturation | $k$ for $a \le \delta$; $\dfrac{2k}{\pi}\left(\arcsin \rho + \rho \sqrt{1 - \rho^2}\right)$ for $a > \delta$ |
| dead zone | $0$ for $a \le \delta$; $k$ minus the saturation value for $a > \delta$ |
| relay $\pm d$ with hysteresis $\pm h$ | $\dfrac{4d}{\pi a} e^{-j \arcsin(h/a)}$ for $a > h$ |

For the relay, the output is a square wave of amplitude $d$, whose first harmonic has amplitude $4d/\pi$. For the relay with hysteresis, the square wave is delayed by the angle $\arcsin(h/a)$, so $-1/N(a) = -\frac{\pi}{4d}\left(\sqrt{a^2 - h^2} + j h\right)$, a horizontal half line at height $-\pi h/(4d)$.

**A relay loop.** Take $G(s) = 1/(s(s+1)(s+2))$ and an ideal relay with $d = 1$. Then $G(j\omega) = 1/(-3\omega^2 + j\omega(2 - \omega^2))$, so the phase crossover is $\omega = \sqrt 2$, with $G(j\sqrt 2) = -1/6$. Harmonic balance gives $4/(\pi a) = 6$, so the prediction is

$$a = \frac{2}{3\pi} \approx 0.2122, \qquad T = \frac{2\pi}{\sqrt 2} \approx 4.443.$$

$N$ decreases with $a$, and the loop with a gain $k$ becomes unstable as $k$ passes $6$, so the predicted cycle attracts. The exact cycle is known for this plant. With $G = \frac{1}{2s} - \frac{1}{s+1} + \frac{1}{2(s+2)}$ and a square wave input of half period $h$, each mode has a periodic response in closed form, and the condition $y(0) = 0$ at the switch becomes $-h/4 + \tanh(h/2) - \tanh(h)/4 = 0$. Its root is $h \approx 2.2755$, so the true period is $4.5511$ and the true amplitude is $0.22004$. The prediction is $2.4\%$ low in the period and $3.6\%$ low in the amplitude. A simulation agrees with the exact values to better than $0.5\%$. The error is small because $|G(3j\sqrt 2)| / |G(j\sqrt 2)| \approx 0.069$ and the third harmonic of a square wave is $1/3$ of its fundamental, so the third harmonic in $y$ is about $2.3\%$ of the fundamental.

[Relay autotuning](/relay-autotuning/) uses this experiment to estimate the ultimate gain $K_u \approx 4d/(\pi a)$ and the ultimate period $T_u \approx T$ of a process. Here it would read $K_u \approx 5.79$ and $T_u \approx 4.55$, against the true values $6$ and $4.443$.

**Saturation.** Take $G(s) = K/(s(s+1)(s+2))$ with a unit saturation ($k = 1$, $\delta = 1$). The Nyquist plot crosses the negative real axis at $-K/6$, and $-1/N(a)$ covers $(-\infty, -1]$, since $N$ falls from $1$ to $0$. For $K < 6$ the two curves do not meet and no cycle is predicted; the loop with gain $1$ is asymptotically stable, and a simulation from $y(0) = 3$ with $K = 3$ decays to zero. For $K > 6$ they meet at $N(a) = 6/K$. For $K = 10$ this gives $a \approx 2.033$ at $\omega = \sqrt 2$, and the cycle attracts. A simulation gives an amplitude of about $2.07$ and a period of about $4.49$.

**Relay with hysteresis.** With the same plant, $d = 1$ and $h = 0.1$, the intersection with the half line $\operatorname{Im} = -\pi/40$ is at $\omega \approx 1.053$ and $a \approx 0.3684$, a period of $5.967$. The hysteresis adds phase lag, so the frequency is lower than for the ideal relay. A simulation gives about $0.381$ and $6.08$.

## Variations

- **Dual-input describing functions.** For a nonlinearity without odd symmetry, or with a bias in the loop, use the input $b + a \sin \omega t$ and balance the mean and the first harmonic together.
- **Random-input describing functions.** For a Gaussian input, the best linear gain in the mean square sense is the statistical linearization used for loops driven by noise. Gelb and Vander Velde treat this and the two-sinusoid case.
- **Harmonic balance with more harmonics.** Keep the harmonics up to order $m$ in a truncated Fourier series of the periodic solution and solve the larger algebraic system. Numerical codes for periodic solutions of nonlinear differential equations use this form, and the first-harmonic method of this page is its simplest case.
- **Rigorous versions.** Error bounds of Bergen, Franks and Mees take the dropped harmonics into account. They give a region around each intersection that must contain the true cycle and conditions under which a cycle does exist.
- **Exact relay oscillations.** For a relay loop, the exact symmetric oscillation can be found from the closed-form response to a square wave, as in the example; Tsypkin's method does this in general.

## Pitfalls

- The method is not a proof. It can predict a limit cycle that does not exist, and it can miss one that does. The risk is high when $G$ has a resonance near a harmonic of the predicted frequency, or when $G$ is not low pass.
- A missing intersection does not prove that the loop has no oscillation, and it does not prove that the equilibrium is globally asymptotically stable. The guess that the loop is globally asymptotically stable whenever the linear loop is asymptotically stable for every gain in the sector of $\phi$ is Aizerman's conjecture, which is false in general.
- Use the sign convention of the loop. With negative feedback the curve is $-1/N(a)$; with positive feedback it is $+1/N(a)$.
- With several intersections, check each one; attracting and repelling predicted cycles often alternate.
- For an element with memory, $N$ depends on the frequency too, and the real-$N$ procedure does not apply.
- When the phase of $G$ never reaches $-180°$, the method predicts no cycle with an ideal relay. The true loop can then switch at a frequency that is limited only by the switching speed of the relay. For $G = 1/(s(s+1))$ a simulation shows solutions that converge to the origin with faster and faster switching.

## Exercises

1. Derive $N(a) = 4d/(\pi a)$ for the ideal relay from the integral for $b_1$.
2. Derive the describing function of the saturation, and show that it decreases from $k$ to $0$ as $a$ goes from $\delta$ to $\infty$.
3. For the relay with hysteresis, show that $-1/N(a)$ lies on the line $\operatorname{Im} z = -\pi h/(4d)$, and explain why hysteresis lowers the frequency of a relay oscillation.
4. Predict the oscillation of an ideal relay with $d = 1$ in a loop with $G(s) = 1/(s+1)^3$. (Answer: $\omega = \sqrt 3$, $G(j\sqrt 3) = -1/8$, $a = 1/(2\pi) \approx 0.159$, $T \approx 3.628$. A simulation gives about $0.163$ and $3.68$.)
5. For the saturation loop with $K = 20$, find the predicted amplitude and decide whether the cycle attracts. (Answer: $a \approx 4.20$; it attracts.)

## References
