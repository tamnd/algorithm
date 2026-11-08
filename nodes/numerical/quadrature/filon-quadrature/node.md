---
tag: 1BJZ9V
kind: algorithm
slug: filon-quadrature
name: Filon quadrature
aliases:
- Filon's method
- Filon-Simpson rule
- Filon's formula
area: numerical/quadrature
level: advanced
summary: Integrates the oscillatory weight exactly while interpolating the smooth factor.
solves: [oscillatory-integration]
model: floating-point-model
complexity:
  vars: {m: "the number of panels (even)"}
  time: {worst: "Θ(m)"}
  space: {extra: Θ(m)}
  evaluations: {worst: "m + 1"}
properties: {deterministic: true, closed: true, nested: "under m to 2m", exact_for: "quadratics times cos(ωx) and sin(ωx), for every ω", reduces_to: "composite Simpson rule at ω = 0", interpolatory: true}
history:
  year: 1928
  people: [Louis Napoleon George Filon, Arieh Iserles, Syvert P. Nørsett]
  note: Filon (1928) replaced the smooth factor by piecewise quadratics and integrated their products with cos(ωx) and sin(ωx) exactly. Iserles and Nørsett (2004 and 2005) explained why the error falls as ω grows and added derivative values at the endpoints.
prereqs: [oscillatory-integration, simpsons-rule]
see_also: [levin-method, product-quadrature, composite-quadrature, clenshaw-curtis-quadrature, adaptive-quadrature, trigonometric-interpolation, fast-fourier-transform, gauss-legendre-quadrature]
sources:
  - paper: "L. N. G. Filon, On a quadrature formula for trigonometric integrals, Proceedings of the Royal Society of Edinburgh 49 (1928) 38-47"
    locator: the rule with piecewise quadratic interpolation and the coefficients α, β, γ
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Section 2.10, integration of rapidly oscillatory functions (Filon's method and its error)
  - book: "Milton Abramowitz and Irene A. Stegun, Handbook of Mathematical Functions, National Bureau of Standards, 1964"
    locator: formula 25.4.47 (Filon's formula and the series of its coefficients for small θ)
  - paper: "Arieh Iserles, On the numerical quadrature of highly-oscillating integrals I: Fourier transforms, IMA Journal of Numerical Analysis 24 (2004) 365-391"
    locator: Filon-type methods and the decay of their error as the frequency grows
  - paper: "Arieh Iserles and Syvert P. Nørsett, Efficient quadrature of highly oscillatory integrals using derivatives, Proceedings of the Royal Society A 461 (2005) 1383-1399"
    locator: Filon-type rules with endpoint derivatives and their asymptotic order
  - paper: "E. O. Tuck, A simple Filon-trapezoidal rule, Mathematics of Computation 21 (1967) 239-241"
    locator: the piecewise linear variant
---

Filon quadrature computes $\int_a^b f(x)\cos\omega x\,dx$ and $\int_a^b f(x)\sin\omega x\,dx$ when $\omega$ is large and $f$ is smooth. A standard rule such as [Simpson's rule](/simpsons-rule/) must resolve every oscillation of the integrand, so it needs several points per period. Filon's method interpolates only the smooth factor $f$ by quadratics on pairs of panels, as Simpson does, and then integrates each quadratic times $\cos\omega x$ or $\sin\omega x$ *exactly*. The oscillation is handled by formulas, not by samples. With $m + 1$ values of $f$ the error is at most a constant times $\min(h^3, h/\omega^2)$, so a few dozen points give many digits even when they are far apart compared with the period.

## In plain words

Some integrals multiply a slowly changing quantity by a wave that goes up and down very fast. Ordinary methods must sample the wave many times per swing or they get nonsense. Filon's idea is to sample only the slowly changing part, which needs few points, and to treat the wave exactly, because its integral against simple curves is known in closed form. The result works even when the samples are much farther apart than one swing of the wave, and it gets better, not worse, as the wave gets faster.

## The problem

**Notation.** As on all quadrature pages: $I(f)$ is the target integral, $Q$ the computed value, $E = I - Q$ the error, and $\tau$ the driver's tolerance. Here the weight is oscillatory: $I_C(f) = \int_a^b f(x)\cos\omega x\,dx$ and $I_S(f) = \int_a^b f(x)\sin\omega x\,dx$, with $\omega$ real. The interval is cut into $m$ panels, $m$ even, of width $h = \frac{b - a}{m}$; $x_k = a + kh$, $f_k = f(x_k)$, and $\theta = \omega h$, the phase change across one panel. The cost is counted in evaluations of $f$; the rule needs $m + 1$, shared by both integrals.

Given $f$, $a$, $b$, $\omega$ and $m$, return $Q_C \approx I_C(f)$ and $Q_S \approx I_S(f)$.

## The algorithm

```pseudo id=main
FILON(f, a, b, ω, m)
L1  if m < 2 or m is odd then error; if a = b then return (0, 0)
L2  h ← (b − a)/m; f_k ← f(a + kh) for k = 0..m
L3  θ ← ωh; (α, β, γ) ← Taylor series if |θ| ≤ 1, else closed forms
L4  C_e ← Σ even k of f_k cos ωx_k minus half the end terms; C_o ← Σ odd k of f_k cos ωx_k; S_e, S_o likewise with sin
L5  return (h(α(f_m sin ωb − f_0 sin ωa) + β C_e + γ C_o),  h(−α(f_m cos ωb − f_0 cos ωa) + β S_e + γ S_o))
```

The coefficients are

$$\alpha = \frac{\theta^2 + \theta\sin\theta\cos\theta - 2\sin^2\theta}{\theta^3},\quad \beta = \frac{2\bigl(\theta(1 + \cos^2\theta) - 2\sin\theta\cos\theta\bigr)}{\theta^3},\quad \gamma = \frac{4(\sin\theta - \theta\cos\theta)}{\theta^3}.$$

For small $\theta$ these formulas subtract nearly equal numbers, so line L3 switches to their Taylor series, $\alpha = \frac{2\theta^3}{45} - \frac{2\theta^5}{315} + \cdots$, $\beta = \frac23 + \frac{2\theta^2}{15} - \frac{4\theta^4}{105} + \cdots$, $\gamma = \frac43 - \frac{2\theta^2}{15} + \frac{\theta^4}{210} - \cdots$. The code computes these coefficients exactly with rational arithmetic, through $\theta^{31}$. At $\theta = 0$, $(\alpha, \beta, \gamma) = (0, \frac23, \frac43)$ and the rule is the composite Simpson rule.

The implementation also has a doubling driver: $m = 2, 4, 8, \ldots$, reusing every old value, stopping when $\lvert\Delta Q_C\rvert + \lvert\Delta Q_S\rvert \le \tau$ or when $m$ would exceed a limit.

## Example

Take $f(x) = x^2$ on $[0, \pi]$, $\omega = 1$, $m = 2$. Then $h = \frac\pi2$, $\theta = \frac\pi2$, $\sin\theta = 1$, $\cos\theta = 0$, and

$$\alpha = \frac{\pi^2/4 - 2}{\pi^3/8} = \frac{2\pi^2 - 16}{\pi^3},\quad \beta = \frac{2}{\theta^2} = \frac{8}{\pi^2},\quad \gamma = \frac{4}{\theta^3} = \frac{32}{\pi^3}.$$

The values are $f_0 = 0$, $f_1 = \frac{\pi^2}{4}$, $f_2 = \pi^2$.

- Cosine: $Q_C = \frac\pi2\bigl(\alpha\cdot 0 + \beta\cdot\frac12\pi^2\cos\pi + \gamma\cdot\frac{\pi^2}{4}\cos\frac\pi2\bigr) = \frac\pi2\cdot\bigl(-4\bigr) = -2\pi$.
- Sine: $Q_S = \frac\pi2\bigl(-\alpha(\pi^2\cos\pi - 0) + 0 + \gamma\frac{\pi^2}{4}\bigr) = \frac\pi2\cdot\frac{2\pi^2 - 16 + 8}{\pi} = \pi^2 - 4$.

Both are exact: $\int_0^\pi x^2\cos x\,dx = -2\pi$ and $\int_0^\pi x^2\sin x\,dx = \pi^2 - 4$, as they must be for a quadratic $f$. Simpson's rule with the same three points gives $-\frac{\pi^3}{6} \approx -5.17$ for the first integral instead of $-6.28$.

Measured errors in $Q_C$ for $f = e^x$ on $[0, 1]$, Filon / composite Simpson applied to $e^x\cos\omega x$, with the same $m + 1$ points:

| $\omega$ | $m = 8$ | $m = 32$ | $m = 128$ | $m = 512$ |
|---|---|---|---|---|
| 10 | $2.1 \times 10^{-5}$ / $4.9 \times 10^{-4}$ | $6.7 \times 10^{-8}$ / $2.4 \times 10^{-6}$ | $2.6 \times 10^{-10}$ / $9.4 \times 10^{-9}$ | $1.0 \times 10^{-12}$ / $3.7 \times 10^{-11}$ |
| 100 | $5.7 \times 10^{-7}$ / $1.6$ | $5.1 \times 10^{-7}$ / $0.53$ | $1.2 \times 10^{-10}$ / $3.2 \times 10^{-5}$ | $4.4 \times 10^{-13}$ / $1.2 \times 10^{-7}$ |
| 1000 | $3.9 \times 10^{-9}$ / $0.39$ | $9.4 \times 10^{-11}$ / $0.39$ | $1.0 \times 10^{-11}$ / $9.7 \times 10^{-3}$ | $2.7 \times 10^{-13}$ / $3.2 \times 10^{-4}$ |

At $\omega = 1000$, $m = 8$ means one sample every 20 periods, and Filon still has 9 digits. For fixed $\omega$ the error ratio per halving of $h$ tends to 16 (measured $15.96$ to $16.0$ at $\omega = 1$). For less smooth $f$, with $\omega = 50$: $\sqrt x$ on $[0, 1]$ converges like $h^{3/2}$ (ratio $2.85$), and a jump at $x = \frac13$ like $h$ (ratio $2.0$). On $\int_0^{2\pi}e^{\cos x}\cos 5x\,dx = 2\pi I_5(1)$, $m = 128$ gives an error of $1.0 \times 10^{-7}$.

## Correctness

On each pair of panels with midpoint $c$, write $x = c + hu$. The quadratic interpolant of $f$ times $e^{i\omega x}$ integrates to $he^{i\omega c}\sum_j W_jf(c + jh)$, where the $W_j$ are combinations of the moments $\int_{-1}^1u^ke^{i\theta u}\,du$, $k \le 2$, which have closed forms. Multiplying out shows that the middle node gets $\gamma$, each end gets $\frac\beta2 \mp i\alpha$ times its own phase, and the $\alpha$ terms cancel at every interior even node where two pairs meet. Summing the pairs gives the formula of line L5 as the real and imaginary parts of one complex sum. So the rule returns the exact integral of the piecewise quadratic interpolant times $\cos\omega x$ and $\sin\omega x$, and in particular it is exact when $f$ is a quadratic, for every $\omega$. The details are in [the correctness proof](proofs/correctness.md).

**Error.** Proved, for $f \in C^3$ with $M_3 = \max\lvert f'''\rvert$:
$$\lvert E\rvert \le M_3\lvert b - a\rvert\min\Bigl(\frac{\lvert h\rvert^3}{9\sqrt3}, \frac{7\lvert h\rvert}{3\omega^2}\Bigr).$$
The first bound uses only the interpolation error. The second integrates by parts twice on each pair, using that the interpolation error vanishes at the pair's ends. Asymptotic and cited (Davis and Rabinowitz, Section 2.10): for fixed $\omega$ and $f \in C^4$ the error is $O(h^4)$, as for Simpson. Measured: the ratios above, and that the error at fixed $m$ falls roughly like $\omega^{-2}$ as $\omega$ grows. The driver's stopping test is a heuristic.

## Complexity

- **Evaluations.** $m + 1$ values of $f$ for both integrals together. The driver at tolerance $\tau$ uses $m + 1$ for the final $m$, since doubling reuses all old values.
- **Operations.** $\Theta(m)$: one cosine and one sine per node, plus constant work for the coefficients. The Taylor coefficients are computed once, exactly, and cached.
- **Space.** $\Theta(m)$ as written; the sums can be accumulated in $O(1)$ space.
- **Independence of $\omega$.** The work for a given accuracy does not grow with $\omega$; by the second bound it shrinks.

## Properties

- **Exact** for $f$ of degree at most 2, for every $\omega$; not exact for $x^3$ when $\omega \ne 0$ (on $[-1, 1]$ with $m = 2$, the error in $\int u^3e^{i\theta u}\,du$ begins $\frac{4}{15}i\theta$).
- **Reduces to Simpson** at $\omega = 0$, where it is exact for cubics.
- **Closed** and **nested** under $m \to 2m$.
- **Symmetric in $\omega$.** Replacing $\omega$ by $-\omega$ leaves $Q_C$ unchanged and negates $Q_S$. Reversing the interval negates both.
- **Weights depend on $\omega$.** It is a [product rule](/product-quadrature/): the oscillatory factor is part of the weight function, and only $f$ is sampled.

## Variants and improvements

- **Filon-trapezoidal** (Tuck 1967): piecewise linear interpolation of $f$, simpler and of lower order.
- **Filon-type methods with derivatives** (Iserles and Nørsett 2005): interpolate $f$ and its first $s - 1$ derivatives at the endpoints. The error then decays like $\omega^{-s-1}$ as $\omega \to \infty$ with fixed nodes.
- **Higher-degree Filon.** Interpolate by polynomials of higher degree on each panel group, or by one Chebyshev interpolant on the whole interval, and integrate against $e^{i\omega x}$ with modified moments. QUADPACK's QAWO (Piessens and Branders) does the latter with Clenshaw-Curtis nodes.
- **Levin's method.** Instead of interpolating $f$, solve a differential equation for an antiderivative of $fe^{i\omega x}$; it extends to phases other than $\omega x$. See the [Levin method](/levin-method/).
- **Numerical steepest descent.** For analytic $f$, deform the path into the complex plane where $e^{i\omega x}$ decays; the cost can fall as $\omega$ grows.

## When to use it

Use Filon's method when the integrand is a smooth, non-oscillating $f$ times $\cos\omega x$ or $\sin\omega x$ with $\omega(b - a)$ large, and you can call $f$ alone: Fourier coefficients, Fourier transforms on a finite interval, and responses of linear systems. It is cheap, simple, and its accuracy does not degrade as $\omega$ grows. For irregular $f$, for phases $g(x)$ other than $\omega x$, or for infinite intervals with slowly decaying $f$, use [Levin's method](/levin-method/) or the methods surveyed on the [oscillatory integration](/oscillatory-integration/) page. For small $\omega(b - a)$ an ordinary rule such as [Gauss-Legendre](/gauss-legendre-quadrature/) or [adaptive quadrature](/adaptive-quadrature/) on the full integrand is as good.

## Pitfalls

- **Cancellation in the closed forms.** For small $\theta$ the formulas for $\alpha, \beta, \gamma$ lose about $3\log_{10}(1/\theta)$ digits; at $\theta = 10^{-4}$ the closed form gives $\alpha = 0$ instead of $4.4 \times 10^{-14}$. Use the series, as line L3 does.
- **Plateaus fool the driver.** While $\omega h$ is large the error can stall: for $e^x\cos 100x$ the errors at $m = 8$ and $16$ are both near $5 \times 10^{-7}$. Two successive results then agree, and with $\tau = 10^{-6}$ the driver stops at $m = 16$ with a true error of $1.6 \times 10^{-6}$. Require a minimum $m$, or $\omega h \lesssim 1$, before trusting the test.
- **Endpoint singularities.** The rule evaluates $f(a)$ and $f(b)$. For $f = \log x$ or $x^{-1/2}$ at $a = 0$ it fails; for $\sqrt x$ it works but converges only like $h^{3/2}$. Use a weight with the singularity built in, or split off the singular part.
- **Accuracy in $f$, not in the integrand.** The error depends on $f'''$, not on $\omega$. If $f$ itself oscillates (for example $f = \cos 90x$ inside $\cos 100x$), Filon has no advantage.
- **Infinite intervals.** The rule needs a finite interval. Truncate where $f$ is negligible: $\int_0^{40}e^{-x}\cos\omega x\,dx$ with $m = 4096$ matches $\frac{1}{1 + \omega^2}$ to $10^{-8}$. For slowly decaying $f$, truncation is poor; use a method for Fourier integrals.
- **Odd $m$.** The pairing needs an even number of panels.

## Implementations

## History

Louis Napoleon George Filon published the method in 1928, in a short paper on integrals of the form $\int f(x)\cos kx\,dx$. The formula, with the coefficients $\alpha, \beta, \gamma$ and their series for small $\theta$, entered the Abramowitz and Stegun handbook in 1964, and Tuck gave the simpler piecewise linear version in 1967. Iserles (2004) and Iserles and Nørsett (2005) showed that the error of Filon-type methods *decreases* as the frequency grows, gave its asymptotic order, and made these methods a central part of the modern study of highly oscillatory quadrature.

## References
