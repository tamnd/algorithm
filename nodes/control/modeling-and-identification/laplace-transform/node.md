---
tag: PFZ473
kind: definition
slug: laplace-transform
name: Laplace transform
aliases:
- unilateral Laplace transform
- one-sided Laplace transform
area: control/modeling-and-identification
level: intro
summary: "The map from a signal f(t), t >= 0, to F(s) = integral from 0- to infinity of f(t) e^(-st) dt. It turns linear ODEs with constant coefficients into algebraic equations in s."
prereqs: [ode-initial-value-problem]
see_also: [transfer-function, poles-and-zeros, partial-fraction-decomposition, final-value-theorem, z-transform, convolution, impulse-response, time-delay-system]
sources:
  - book: doi:10.1007/978-3-642-99536-1
    title: Gustav Doetsch, Theorie und Anwendung der Laplace-Transformation, Grundlehren der mathematischen Wissenschaften 47, Julius Springer, Berlin, 1937
    locator: the whole book (the first textbook on the theory of the transform, its region of convergence, the inversion integral and the uniqueness theorem)
  - paper: doi:10.1109/MCS.2007.284506
    title: Kent H. Lundberg, Haynes R. Miller and David L. Trumper, Initial conditions, generalized functions, and the Laplace transform, troubles at the origin, IEEE Control Systems Magazine 27(1), 2007
    locator: pp. 22 to 35 (the case for the lower limit 0-, the transform of the delta, and the derivative rule with f(0-))
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Section 3.1, Review of Laplace Transforms (3.1.3 the L- Laplace transform, 3.1.4 properties, 3.1.5 inversion by partial fractions, 3.1.7 the solution of differential equations) and Appendix A
  - book: isbn:9780691193984
    title: Karl Johan Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Chapter 9, Transfer Functions (the section on Laplace transforms)
---

The Laplace transform maps a function $f(t)$ of time, defined for $t \ge 0$, to a function $F(s) = \int_{0^-}^{\infty} f(t)\, e^{-st}\, dt$ of a complex variable $s$. It turns differentiation into multiplication by $s$ and convolution into multiplication, so a linear differential equation with constant coefficients becomes an algebraic equation that one solves for $F(s)$ and then transforms back. Control and circuit theory use it to define the [transfer function](/transfer-function/) of a continuous-time system, and probability uses the same integral, $\mathbb{E}[e^{-sZ}]$, to describe the distribution of a nonnegative random variable $Z$. This page uses the one-sided transform with the lower limit $0^-$, and so does every page of the control area.

## Definition

**Notation.** Time $t$ is in seconds and $s = \sigma + i\omega$ is a complex number, with $\omega$ in rad/s. A function $f : [0, \infty) \to \mathbb{C}$ is *of exponential order* $a$ if it is integrable on each bounded interval and $|f(t)| \le M e^{a t}$ for some $M$ and all $t \ge 0$.

**Definition.** The (one-sided) Laplace transform of $f$ is

$$F(s) = \mathcal{L}\{f\}(s) = \int_{0^-}^{\infty} f(t)\, e^{-st}\, dt = \lim_{\varepsilon \to 0^+,\ R \to \infty} \int_{-\varepsilon}^{R} f(t)\, e^{-st}\, dt,$$

for each $s$ where the limit exists. If $f$ is of exponential order $a$, the integral converges absolutely for $\operatorname{Re} s > a$, and $F$ is analytic in that half plane. The smallest such bound is the *abscissa of convergence*; the half plane to its right is the *region of convergence*.

**Why $0^-$.** For an ordinary function the value at one point does not change the integral, so $0^-$ and $0^+$ give the same $F$. The two limits differ only when $f$ holds a Dirac delta $\delta(t)$ or its derivatives at $t = 0$. With $0^-$, the delta is inside the range of integration, so $\mathcal{L}\{\delta\} = 1$, and the derivative rule uses the value just before the input starts:

$$\mathcal{L}\{f'\}(s) = s F(s) - f(0^-).$$

The value $f(0^-)$ is the stored state of the system before $t = 0$, which is what a user knows. The value $f(0^+)$ after an impulse is usually not known in advance. Lundberg, Miller and Trumper (2007) show the errors that a mix of the two conventions causes in textbooks.

**Rules.** Let $F = \mathcal{L}\{f\}$ and $G = \mathcal{L}\{g\}$ in a common half plane, and let $\mathbb{1}(t)$ be the unit step.

| time domain | transform | condition |
|---|---|---|
| $a f(t) + b g(t)$ | $a F(s) + b G(s)$ | |
| $f'(t)$ | $s F(s) - f(0^-)$ | $f'$ of exponential order |
| $f''(t)$ | $s^2 F(s) - s f(0^-) - f'(0^-)$ | |
| $\int_{0^-}^{t} f(\tau)\, d\tau$ | $F(s) / s$ | |
| $f(t - \tau)\, \mathbb{1}(t - \tau)$ | $e^{-s\tau} F(s)$ | $\tau \ge 0$ |
| $e^{a t} f(t)$ | $F(s - a)$ | |
| $t\, f(t)$ | $-F'(s)$ | |
| $(f * g)(t) = \int_{0^-}^{t} f(\tau)\, g(t - \tau)\, d\tau$ | $F(s)\, G(s)$ | |

The convolution rule is the reason for transfer functions: a [linear time-invariant system](/linear-time-invariant-system/) at rest with impulse response $g$ maps the input $u$ to $y = g * u$, so $Y(s) = G(s)\, U(s)$. The time shift rule gives the factor $e^{-s\tau}$ of a [time-delay system](/time-delay-system/).

**Common pairs.** For $t \ge 0$, with $a$ and $\omega$ real:

| $f(t)$ | $F(s)$ | region |
|---|---|---|
| $\delta(t)$ | $1$ | all $s$ |
| $\mathbb{1}(t)$ | $1/s$ | $\operatorname{Re} s > 0$ |
| $t^n / n!$ | $1 / s^{n+1}$ | $\operatorname{Re} s > 0$ |
| $e^{-a t}$ | $1/(s + a)$ | $\operatorname{Re} s > -a$ |
| $\sin \omega t$ | $\omega / (s^2 + \omega^2)$ | $\operatorname{Re} s > 0$ |
| $\cos \omega t$ | $s / (s^2 + \omega^2)$ | $\operatorname{Re} s > 0$ |
| $e^{-a t} \sin \omega t$ | $\omega / ((s + a)^2 + \omega^2)$ | $\operatorname{Re} s > -a$ |

**Inversion.** If $F$ is the transform of $f$ and $c$ is larger than the abscissa of convergence, the Bromwich integral $f(t) = \frac{1}{2\pi i} \int_{c - i\infty}^{c + i\infty} F(s)\, e^{st}\, ds$ gives $f$ at each point where $f$ is continuous and of bounded variation nearby. Two functions with the same transform agree almost everywhere (Lerch's theorem), and two continuous functions with the same transform are equal. For a rational $F$, inversion in practice is a [partial fraction decomposition](/partial-fraction-decomposition/) followed by the table above: a pole $p$ of order $k$ gives the terms $t^j e^{p t}$ for $j < k$.

**Limit theorems.** The initial value theorem says $f(0^+) = \lim_{s \to \infty} s F(s)$ when $f$ and $f'$ are of exponential order and $f$ has no delta at 0. The [final value theorem](/final-value-theorem/) says $\lim_{t \to \infty} f(t) = \lim_{s \to 0} s F(s)$ when every pole of $s F(s)$ has a negative real part. Without that condition the right side can be finite while $f$ oscillates or grows.

## Examples and non-examples

- **A step into a second-order system.** Solve $y'' + 3y' + 2y = \mathbb{1}(t)$ with $y(0^-) = y'(0^-) = 0$. The transform gives $(s^2 + 3s + 2)\, Y = 1/s$, so
$$Y(s) = \frac{1}{s(s+1)(s+2)} = \frac{1/2}{s} - \frac{1}{s+1} + \frac{1/2}{s+2}, \qquad y(t) = \tfrac12 - e^{-t} + \tfrac12 e^{-2t}.$$
At $t = 2$ s this gives $y = 0.37382$. The steady value $1/2$ is $\lim_{s \to 0} s Y(s)$.
- **Initial conditions and no input.** The same equation with zero input, $y(0^-) = 1$ and $y'(0^-) = 0$, gives $s^2 Y - s + 3(sY - 1) + 2Y = 0$, so $Y = (s + 3)/((s + 1)(s + 2)) = 2/(s + 1) - 1/(s + 2)$ and $y(t) = 2e^{-t} - e^{-2t}$. The initial conditions enter as a polynomial in the numerator. This is why a transfer function assumes a system at rest.
- **An impulse.** For $y' + y = \delta(t)$ with $y(0^-) = 0$, the $0^-$ rules give $sY + Y = 1$ and $y(t) = e^{-t}$ for $t > 0$. The state jumps from $y(0^-) = 0$ to $y(0^+) = 1$, and $\lim_{s \to \infty} sY(s) = 1$ gives the value after the jump. With the $0^+$ convention, $\mathcal{L}\{\delta\} = 0$, and one must know $y(0^+) = 1$ before one can solve the equation.
- **Probability.** If $Z$ is exponential with rate $\lambda$, its density $\lambda e^{-\lambda t}$ has the transform $\mathbb{E}[e^{-sZ}] = \lambda/(s + \lambda)$.
- **Non-example: growth too fast.** $f(t) = e^{t^2}$ is not of exponential order, and the integral diverges for every $s$. It has no Laplace transform.
- **Non-example: not integrable at 0.** $f(t) = 1/t$ is not integrable near $t = 0$, so the integral diverges for every $s$.
- **Non-example: the Fourier transform is not $F(i\omega)$ in general.** The unit step has $F(s) = 1/s$ only for $\operatorname{Re} s > 0$. The imaginary axis is not in the region of convergence, and the Fourier transform of the step has an extra delta term at $\omega = 0$. The [frequency response](/frequency-response/) $G(i\omega)$ of a system is its transfer function on the imaginary axis only when that axis lies in the region of convergence, as for a BIBO stable system.
- **Non-example: the two-sided transform.** $\int_{-\infty}^{\infty} f(t) e^{-st} dt$ is a different transform. It needs a strip of convergence to fix $f$, and it does not carry initial conditions.

## Related definitions

- [Transfer function](/transfer-function/): $G(s) = Y(s)/U(s)$ for a system at rest; that page treats the discrete-time form in $z$.
- [Z-transform](/z-transform/): the discrete analogue. For samples $f(kh)$ with sampling period $h$, the map $z = e^{s h}$ links the two planes.
- [Poles and zeros](/poles-and-zeros/): the roots of the denominator and the numerator of a rational $F$, which set the terms $t^j e^{pt}$ of $f$.
- [Impulse response](/impulse-response/): the inverse transform of a transfer function.
- [Final value theorem](/final-value-theorem/): the limit of $f$ from $s F(s)$ near $s = 0$, with its hypothesis.
- [Partial fraction decomposition](/partial-fraction-decomposition/): the algebra step of inversion.
- [Convolution](/convolution/): the operation that the transform turns into a product.
- [Time-delay system](/time-delay-system/): a model whose transfer function has the factor $e^{-s\tau}$, which is not rational.

## References
