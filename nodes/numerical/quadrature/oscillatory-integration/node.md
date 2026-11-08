---
tag: WSZ0K5
kind: problem
slug: oscillatory-integration
name: Oscillatory integration
aliases:
- highly oscillatory integrals
- highly oscillatory quadrature
- Fourier-type integrals
area: numerical/quadrature
level: advanced
summary: Integrals whose integrands oscillate rapidly, so standard rules need many points.
prereqs: [numerical-integration]
see_also: [filon-quadrature, levin-method, gauss-legendre-quadrature, clenshaw-curtis-quadrature, improper-integration, discrete-fourier-transform, tanh-sinh-quadrature, quadrature-error]
sources:
  - book: "Alfredo Deaño, Daan Huybrechs and Arieh Iserles, Computing Highly Oscillatory Integrals, SIAM, 2018"
    locator: Chapter 1 (the asymptotic expansion and stationary points), Chapter 3 (Filon methods), Chapter 4 (Levin methods), Chapter 5 (numerical steepest descent)
  - paper: doi:10.1098/rspa.2004.1401
    title: Arieh Iserles and Syvert P. Nørsett, Efficient quadrature of highly oscillatory integrals using derivatives, Proceedings of the Royal Society A 461, 2005, 1383-1399
    locator: Theorems 2.1 and 3.1 (the asymptotic method and Filon methods with derivatives, error O(omega^(-s-1)))
  - paper: "David Levin, Procedures for computing one- and two-dimensional integrals of functions with rapid irregular oscillations, Mathematics of Computation 38, 1982, 531-538"
    locator: the collocation method for the associated differential equation
  - paper: "L. N. G. Filon, On a quadrature formula for trigonometric integrals, Proceedings of the Royal Society of Edinburgh 49, 1928, 38-47"
    locator: the rule that interpolates the amplitude and integrates the oscillation exactly
  - paper: "Daan Huybrechs and Stefan Vandewalle, On the evaluation of highly oscillatory integrals by analytic continuation, SIAM Journal on Numerical Analysis 44(3), 2006, 1026-1048"
    locator: numerical steepest descent, with error decaying in omega for a fixed number of points
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Section 2.10, Integration of rapidly oscillatory functions, and Section 3.9, Oscillatory integrands over infinite ranges
---

Oscillatory integration is the computation of integrals such as

$$I_\omega[f] = \int_a^b f(x)\, e^{i \omega g(x)}\,dx$$

for a smooth amplitude $f$, a smooth real phase $g$, and a large frequency $\omega$. The integrand has about $\omega (b - a)/(2\pi)$ oscillations when $g(x) = x$, so a rule built for smooth functions needs a number of points that grows linearly with $\omega$, while the integral itself shrinks. Methods that use the known form of the oscillation do the opposite: they get more accurate as $\omega$ grows, for a fixed number of evaluations of $f$.

## In plain words

Some integrals wiggle: the integrand goes up and down many times across the interval, like a sound wave or a ripple. The positive and negative parts nearly cancel, so the answer is small, and an ordinary rule has to look at enough points to see every wiggle, otherwise it adds up noise. The faster the wiggling, the more points it needs.

But usually you know what the wiggle is, a sine or cosine of some known function, and only the slowly changing size in front of it is unknown. Good methods sample that slow part at a few points and handle the wiggle exactly with formulas. They become more accurate as the wiggling gets faster, which is the reverse of what ordinary rules do.

## Definition

**Input.** An interval $[a, b]$ (possibly infinite), an oracle for the amplitude $f$ (and possibly its derivatives), a phase $g$ known in closed form, and a frequency $\omega > 0$, typically large; a tolerance $\tau$.

**Output.** An approximation to $I_\omega[f] = \int_a^b f(x) e^{i\omega g(x)}\,dx$. Real forms $\int f \cos(\omega g)$ and $\int f \sin(\omega g)$ are the real and imaginary parts.

**Cost.** Evaluations of $f$ and its derivatives, counted separately from the work of computing moments $\int x^k e^{i\omega g(x)}\,dx$ or solving small linear systems.

**Accuracy.** Both the absolute error and the error relative to $|I_\omega|$ matter, since $|I_\omega|$ decays as $\omega$ grows. A method is called *asymptotic of order $p$* if, for fixed $f$, $g$ and number of evaluations, its absolute error is $O(\omega^{-p})$ as $\omega \to \infty$.

**Two regimes.** A point $c$ with $g'(c) = 0$ is a *stationary point*. Without stationary points $I_\omega = O(\omega^{-1})$; at a nondegenerate stationary point it is of order $\omega^{-1/2}$.

## Variants

- **Fourier integrals.** $g(x) = x$: $\int_a^b f(x) \cos(\omega x)\,dx$ and $\int_a^b f(x) \sin(\omega x)\,dx$, including Fourier coefficients of a function. For many frequencies on a uniform grid, the [discrete Fourier transform](/discrete-fourier-transform/) of samples serves instead.
- **Nonlinear phase.** $g$ general, with or without stationary points, as in wave scattering and the boundary integral equations of high-frequency acoustics.
- **Special-function kernels.** $\int f(x) J_\nu(\omega x)\,dx$ and other Bessel or Airy kernels, which oscillate but are not exponentials; Levin's method handles them through the differential equations they satisfy.
- **Infinite range.** $\int_0^\infty f(x) \sin x\,dx$ with slowly decaying $f$, such as $\int_0^\infty \frac{\sin x}{x}\,dx = \frac{\pi}{2}$, which converges only conditionally. See [improper integration](/improper-integration/).
- **Multivariate.** $\int_\Omega f(x) e^{i\omega g(x)}\,dx$ over a region in $\mathbb{R}^s$, with critical points of $g$ and resonance points on the boundary.

## Examples

**Cost of a standard rule.** For $I_\omega = \int_0^1 e^x e^{i\omega x}\,dx = \frac{e^{1 + i\omega} - 1}{1 + i\omega}$, the smallest number $n$ of [Gauss-Legendre](/gauss-legendre-quadrature/) points with relative error below $10^{-10}$ is 11 for $\omega = 10$, 42 for $\omega = 100$ and 287 for $\omega = 1000$. The growth is linear in $\omega$: a rule of degree $2n - 1$ must resolve a function that looks like a polynomial of degree about $\omega (b - a)/2$.

**Methods that improve with $\omega$.** On the same integral, the absolute errors of the two-term asymptotic expansion (which uses $f$ and $f'$ at the two endpoints), of the linear Filon rule (values of $f$ at the endpoints, the line through them integrated against $e^{i\omega x}$ exactly) and of the cubic Filon-Hermite rule (values and derivatives at the endpoints) are:

| $\omega$ | $\lvert I_\omega \rvert$ | asymptotic, 1 term | asymptotic, 2 terms | Filon, linear | Filon-Hermite, cubic |
|---|---|---|---|---|---|
| 10 | $3.58 \times 10^{-1}$ | $3.58 \times 10^{-2}$ | $3.58 \times 10^{-3}$ | $8.56 \times 10^{-3}$ | $1.89 \times 10^{-4}$ |
| 100 | $1.92 \times 10^{-2}$ | $1.92 \times 10^{-4}$ | $1.92 \times 10^{-6}$ | $1.67 \times 10^{-4}$ | $6.36 \times 10^{-8}$ |
| 1000 | $2.31 \times 10^{-3}$ | $2.31 \times 10^{-6}$ | $2.31 \times 10^{-9}$ | $1.52 \times 10^{-6}$ | $1.36 \times 10^{-10}$ |

Each method uses 2 or 4 values, independent of $\omega$, and the errors decay like $\omega^{-2}$, $\omega^{-3}$, $\omega^{-2}$ and $\omega^{-3}$, as the bounds below predict. Here the asymptotic expansion is unusually good, because every derivative of $e^x$ is $e^x$ and the error of the $K$-term expansion is exactly $|I_\omega| \omega^{-K}$. The [Filon](/filon-quadrature/) rules converge for fixed $\omega$ when more nodes are added, which the asymptotic expansion does not.

**Infinite range.** For $\int_0^\infty \frac{\sin x}{x}\,dx = \frac{\pi}{2}$, integrating over $[k\pi, (k+1)\pi]$ with 10-point Gauss-Legendre and summing $K$ pieces gives partial sums with error about $1/(K\pi)$: $3.2 \times 10^{-2}$ for $K = 10$ and $1.6 \times 10^{-2}$ for $K = 20$. The partial sums alternate around the limit, and repeatedly averaging neighbouring partial sums (the Euler transformation) reduces the error to $3.5 \times 10^{-5}$ and $1.4 \times 10^{-8}$ with the same 100 and 200 evaluations.

## Known algorithms

| method | data used | error for fixed data, $g' \ne 0$ | converges for fixed $\omega$ |
|---|---|---|---|
| standard [Gauss](/gauss-legendre-quadrature/) or [Clenshaw-Curtis](/clenshaw-curtis-quadrature/) rule | $n$ values | needs $n$ growing like $\omega$ | yes |
| asymptotic expansion, $K$ terms | $f, \ldots, f^{(K-1)}$ at $a, b$ | $O(\omega^{-K-1})$ | no |
| [Filon](/filon-quadrature/) (interpolate $f$, exact moments) | values, plus derivatives up to order $m - 1$ at $a, b$ | $O(\omega^{-m-1})$ | yes |
| [Levin collocation](/levin-method/) | values, plus endpoint derivatives | $O(\omega^{-m-1})$, as for Filon | yes |
| numerical steepest descent | values of $f$ on complex paths | $O(\omega^{-2n-1})$ with $n$ Gauss points per path, $f$ and $g$ analytic | no |
| panel or zero-to-zero splitting with series acceleration | values | depends on the acceleration | yes |
| double exponential rules for Fourier integrals (Ooura and Mori) | values | nearly exponential in the number of points | yes |

Filon methods need the moments $\int x^k e^{i\omega g(x)}\,dx$, which are easy for $g(x) = x$ and hard in general. Levin's method avoids moments by solving the differential equation $p' + i\omega g' p = f$ for a non-oscillating $p$, after which $I_\omega = p(b) e^{i\omega g(b)} - p(a) e^{i\omega g(a)}$; it needs no stationary points in $[a, b]$, or special handling of them.

## Bounds

- **Integration by parts (proved).** Let $g' \ne 0$ on $[a, b]$, $f \in C^{K+1}[a, b]$, $g \in C^{K+2}[a, b]$, and set $\sigma_0 = f$, $\sigma_{k+1} = (\sigma_k / g')'$. Then

$$I_\omega[f] = -\sum_{k=0}^{K-1} \frac{1}{(-i\omega)^{k+1}} \Big[ \frac{\sigma_k(x)}{g'(x)} e^{i\omega g(x)} \Big]_a^b + \frac{1}{(-i\omega)^{K}} I_\omega[\sigma_K].$$

*Proof.* Since $\frac{d}{dx} e^{i\omega g} = i\omega g' e^{i\omega g}$, integration by parts gives $I_\omega[\sigma] = \frac{1}{i\omega} \big[\frac{\sigma}{g'} e^{i\omega g}\big]_a^b - \frac{1}{i\omega} I_\omega[(\sigma/g')']$ for $\sigma \in C^1$. Apply this to $\sigma_0, \ldots, \sigma_{K-1}$ in turn. $\square$ The same identity with $K$ replaced by $1$ bounds the remainder: $|I_\omega[\sigma_K]| \le \frac{1}{\omega}\big(\frac{|\sigma_K(a)|}{|g'(a)|} + \frac{|\sigma_K(b)|}{|g'(b)|} + \|\sigma_{K+1}\|_{L^1}\big)$. So the $K$-term expansion has error $O(\omega^{-K-1})$, and with $K = 1$, $I_\omega = O(\omega^{-1})$. For fixed $\omega$ the series usually diverges as $K \to \infty$, so the expansion alone cannot reach an arbitrary tolerance.
- **Filon with derivatives (cited).** If $g' \ne 0$ on $[a, b]$ and the interpolant of $f$ matches $f, f', \ldots, f^{(m-1)}$ at both endpoints (and values at any interior nodes), then the Filon rule has error $O(\omega^{-m-1})$ (Iserles and Nørsett 2005, Theorem 3.1). This follows from the expansion above: the error is $I_\omega[f - p]$, and $f - p$ and its first $m - 1$ derivatives vanish at the endpoints, so the first $m$ terms of the expansion vanish.
- **Stationary points (cited, asymptotic).** If $g'(c) = 0$ at a single point $c \in (a, b)$ with $g''(c) \ne 0$, then $I_\omega[f] = f(c)\, e^{i\omega g(c) \pm i\pi/4} \sqrt{2\pi/(\omega |g''(c)|)} + O(\omega^{-1})$, the sign being that of $g''(c)$ (the method of stationary phase; Deaño, Huybrechs and Iserles 2018, Chapter 1). Filon methods with derivatives also at $c$ recover high asymptotic order there.
- **No fixed rule works for all $\omega$ (proved).** Let $Q(\phi) = \sum_{i=1}^{n} w_i \phi(x_i)$ with distinct nodes and not all $w_i = 0$, and put $F(\omega) = Q(e^{i\omega x}) = \sum_i w_i e^{i\omega x_i}$. Then $\frac{1}{T}\int_0^T |F(\omega)|^2\,d\omega = \sum_i |w_i|^2 + \sum_{i \ne j} w_i \overline{w_j} \frac{e^{iT(x_i - x_j)} - 1}{iT(x_i - x_j)} \to \sum_i |w_i|^2$ as $T \to \infty$. So $|F(\omega)| \ge \frac12 \|w\|_2$ for arbitrarily large $\omega$, while $I_\omega[1] = \int_a^b e^{i\omega x}\,dx \to 0$. Every fixed rule therefore has an error bounded away from 0 on $e^{i\omega x}$ for some arbitrarily large $\omega$; the number of points must grow with $\omega$ unless the rule depends on $\omega$.
- **Floating point.** Moments $\int_a^b x^k e^{i\omega x}\,dx$ computed by the recurrence from integration by parts are stable for $k$ small compared with $\omega(b - a)$ and unstable otherwise; Filon codes switch to other recurrences or to Chebyshev moments when $k$ is large.

## Reductions

- **To a non-oscillatory problem.** Levin's method reduces $I_\omega$ to the boundary values of a non-oscillatory solution of $p' + i\omega g' p = f$, computed by collocation.
- **To moments.** Filon's method reduces it to integrals of polynomials times the oscillator, computed exactly once per $\omega$ and reused for every $f$.
- **To exponentially decaying integrals.** If $f$ and $g$ are analytic, Cauchy's theorem lets the path leave the real line along curves where $e^{i\omega g}$ is real and decays exponentially; these integrals are then done with Gauss-Laguerre or Gauss-Hermite rules. This is numerical steepest descent.
- **To a series.** On an infinite range, split at the zeros of the oscillator, compute each piece with a standard rule, and sum the resulting alternating series with an acceleration method.
- **Change of variables.** Near a stationary point $c$, the substitution $u = \operatorname{sgn}(x - c)\sqrt{|g(x) - g(c)|}$ makes the phase quadratic, and splitting at $c$ gives two integrals without stationary points in the interior.

## Applications

- High-frequency wave scattering: boundary integral equations for the Helmholtz equation at large wavenumber.
- Fourier coefficients, Fourier transforms and their inverses at isolated frequencies.
- Electronic structure and quantum chemistry, where integrals of oscillatory basis functions appear.
- Special functions and their asymptotics: Bessel, Airy and Fresnel integrals.
- Signal processing and optics: diffraction integrals, with stationary points giving the geometric optics rays.

## References
