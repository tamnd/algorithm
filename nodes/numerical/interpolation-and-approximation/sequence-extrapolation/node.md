---
tag: CDRZPB
kind: problem
slug: sequence-extrapolation
name: Sequence extrapolation
aliases:
- Limit extrapolation
- Convergence acceleration
- Series acceleration
- Sequence transformation
area: numerical/interpolation-and-approximation
level: advanced
summary: Estimate the limit s of a sequence s_k from finitely many terms by assuming a model of the error, as Aitken, Richardson, Shanks, Wynn and Levin do. No single method accelerates every sequence.
prereqs: [geometric-series]
see_also: [aitken-delta-squared, richardson-extrapolation, pade-approximation, romberg-integration, euler-maclaurin-formula, bulirsch-stoer-method, continued-fraction, neville-algorithm]
sources:
  - book: isbn:9780444888143
    title: Claude Brezinski and Michela Redivo Zaglia, Extrapolation Methods, Theory and Practice, North-Holland, 1991
    locator: Chapter 1, Introduction to the theory (kernels, acceleration, the impossibility results); Chapter 2, Scalar extrapolation algorithms (Richardson, Aitken, Shanks and the epsilon-algorithm, Levin-type transformations)
  - paper: "Alexander C. Aitken, On Bernoulli's numerical solution of algebraic equations, Proceedings of the Royal Society of Edinburgh 46 (1926) 289-305"
    locator: the delta-squared process
  - paper: "Daniel Shanks, Non-linear transformations of divergent and slowly convergent sequences, Journal of Mathematics and Physics 34 (1955) 1-42"
    locator: the e_k transformation, its kernel and its relation to Padé approximants
  - paper: "Peter Wynn, On a device for computing the e_m(S_n) transformation, Mathematical Tables and Other Aids to Computation 10 (1956) 91-96"
    locator: the epsilon-algorithm
  - paper: "David Levin, Development of non-linear transformations for improving convergence of sequences, International Journal of Computer Mathematics B 3 (1973) 371-388"
    locator: the t, u and v transformations
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 28, Analytic continuation and convergence acceleration
---

Sequence extrapolation estimates the limit $s$ of a sequence $s_0, s_1, s_2, \ldots$ from its first few terms, faster than waiting for the terms to settle. Every method assumes a model of how $s_k$ approaches $s$, such as a geometric error, a power series in a step size, or an asymptotic expansion of the terms of a series, and solves for $s$ as a parameter of the model. When the model fits, a handful of terms can give many more correct digits than the terms themselves; when it does not, the method can do nothing or even do harm.

## In plain words

If you know how a sequence is closing in on its target, you can jump ahead. When each error is about half the previous one, three consecutive values are enough to guess where they are heading. When the error shrinks like the step size squared, two runs at different step sizes are enough to cancel it.

Extrapolation methods turn such guesses into formulas. They can turn ten terms of a slowly converging sum into an answer accurate to ten digits, and they can even give sensible values to sums that diverge. They work only when the assumed pattern is right, and it has been proved that no single method works for every slowly converging sequence.

## Definition

Notation on the interpolation pages: $(s_k)_{k \ge 0}$ is a sequence of real or complex numbers with limit $s$ (or an antilimit, when $s_k$ diverges); for series, $s_k = \sum_{j=0}^{k} a_j$ are the partial sums; $\Delta s_k = s_{k+1} - s_k$.

**Problem.** Given $s_0, \ldots, s_K$, produce an estimate of $s$.

A **sequence transformation** $T$ maps $(s_k)$ to a new sequence $(t_k)$, each $t_k$ depending on finitely many $s_j$. It is

- **exact** on its **kernel**, the set of sequences for which $t_k = s$ for all $k$;
- **accelerating** for a class of sequences if $(t_k - s)/(s_{k+j} - s) \to 0$, where $s_{k+j}$ is the last term $t_k$ uses.

**Kinds of convergence.** If $(s_{k+1} - s)/(s_k - s) \to \rho$, convergence is **linear** when $0 < |\rho| < 1$ and **logarithmic** when $\rho = 1$. Linear sequences come from fixed-point iterations and alternating series; logarithmic ones from series with terms like $k^{-2}$ and from discretizations with a step size $h = 1/k$.

**Impossibility.** Delahaye and Germain-Bonnefoy (1980) proved that no sequence transformation accelerates all logarithmically convergent sequences, and similar results hold for other large classes. So the problem has no universal solution; a method is chosen by the error model.

## Variants

- **Geometric error model:** $s_k = s + c\lambda^k$ (Aitken's $\Delta^2$), or a sum of $m$ geometric terms $s_k = s + \sum_{i=1}^{m} c_i \lambda_i^k$ (Shanks' $e_k$ transformation, computed by Wynn's epsilon algorithm).
- **Step-size model:** $s(h) = s + c_1 h^{p_1} + c_2 h^{p_2} + \cdots$ with known exponents ([Richardson extrapolation](/richardson-extrapolation/)), as in [Romberg integration](/romberg-integration/) and the [Bulirsch-Stoer method](/bulirsch-stoer-method/).
- **Term-based models (Levin type):** $s_k = s + \omega_k \sum_{j=0}^{m-1} c_j (k + \beta)^{-j}$ with the remainder estimate $\omega_k$ taken from the terms $a_k$ themselves ($\omega_k = (k + \beta) a_k$ for Levin's $u$, $a_k$ for $t$).
- **Series transformations:** Euler's transformation of alternating series, Kummer's comparison with a known series, and the [Euler-Maclaurin formula](/euler-maclaurin-formula/) for sums of smooth functions.
- **Summation of divergent series:** assign an antilimit by Padé, Borel or Shanks summation.
- **Vector and matrix sequences:** vector epsilon, minimal and reduced rank extrapolation, Anderson acceleration of fixed-point iterations.

## Examples

All numbers below come from exact rational arithmetic on the given terms, rounded at the end.

**Alternating series: $\ln 2 = 1 - \tfrac12 + \tfrac13 - \cdots$.** With 11 partial sums $s_0, \ldots, s_{10}$ the error of $s_{10}$ is $4.3 \times 10^{-2}$. Iterated Aitken $\Delta^2$ (5 rounds) gives $1.0 \times 10^{-10}$, Wynn's epsilon algorithm $4.4 \times 10^{-9}$, and Levin's $u$ transformation $2.3 \times 10^{-13}$. For Leibniz's series $\pi/4 = 1 - \tfrac13 + \tfrac15 - \cdots$ the same 11 terms give $2.3 \times 10^{-2}$ raw, $4.9 \times 10^{-9}$ by epsilon and $2.3 \times 10^{-13}$ by Levin $u$.

**Logarithmic convergence: $\pi^2/6 = \sum 1/(k+1)^2$.** The error of $s_{10}$ is $8.7 \times 10^{-2}$, decreasing like $1/k$. Aitken (once: $4.8 \times 10^{-2}$; five times: $1.7 \times 10^{-3}$) and Wynn's epsilon ($2.5 \times 10^{-2}$) barely help: their geometric model is wrong. Richardson extrapolation in $h = 1/(k + 1)$ through all 11 values, and Levin's $u$, both give $3.0 \times 10^{-10}$, because the error has an expansion in powers of $1/k$.

**Fixed-point iteration $x_{k+1} = \cos x_k$, $x_0 = 1$.** The limit is $0.739085\ldots$ and $\rho = -\sin(0.739) \approx -0.674$. The error of $x_{10}$ is $5.2 \times 10^{-3}$; Aitken applied to $x_8, x_9, x_{10}$ gives $1.9 \times 10^{-5}$. Restarting the iteration from each Aitken value (Steffensen's method) gives errors $1.1 \times 10^{-2}$, $1.8 \times 10^{-5}$, $4.9 \times 10^{-11}$ and then below $10^{-16}$: quadratic convergence using only evaluations of $\cos$.

**Divergent series.** Euler's series $\sum_k (-1)^k k!\, x^k$ diverges for every $x \ne 0$. At $x = 0.1$ its Borel sum is $\int_0^\infty e^{-t}/(1 + xt)\, dt = 0.9156333\ldots$. The best partial sum (truncating at the smallest term) is off by $1.8 \times 10^{-4}$, while Wynn's epsilon and Levin's $u$ on the first 13 partial sums are off by about $5 \times 10^{-9}$ and $4 \times 10^{-9}$.

## Known algorithms

- **[Aitken's $\Delta^2$ process](/aitken-delta-squared/):** $t_k = s_{k+2} - (\Delta s_{k+1})^2/\Delta^2 s_k$. Exact for $s + c\lambda^k$; accelerates every linearly convergent sequence ($0 < |\rho| < 1$); fails in general for logarithmic convergence. Three terms per output, $O(1)$ operations each.
- **Shanks' transformation and Wynn's epsilon algorithm.** $e_m(s_k)$ is exact for sums of $m$ geometric terms; Wynn's rhombus rule $\varepsilon_{j+1}^{(k)} = \varepsilon_{j-1}^{(k+1)} + 1/(\varepsilon_j^{(k+1)} - \varepsilon_j^{(k)})$ with $\varepsilon_{-1} = 0$, $\varepsilon_0^{(k)} = s_k$ computes all $e_m(s_k) = \varepsilon_{2m}^{(k)}$ from $K$ terms in $\Theta(K^2)$ operations. Applied to partial sums of a power series at $x$, $e_m(s_k)$ equals the [Padé approximant](/pade-approximation/) $[k + m / m]$ at $x$.
- **[Richardson extrapolation](/richardson-extrapolation/):** polynomial extrapolation to $h = 0$, computed by the [Neville scheme](/neville-algorithm/) in $\Theta(K^2)$ operations; exact when $s(h)$ is a polynomial in $h$ of the assumed form.
- **Levin's transformations** $t$, $u$, $v$ and the Weniger and Sidi variants: a weighted divided-difference formula, $\Theta(K)$ per output; among the most effective general-purpose methods for both alternating and logarithmic series.
- **Brezinski's $\theta$ algorithm, the $\rho$ algorithm, Overholt's process, Lubkin's transformation:** other rhombus rules aimed at logarithmic sequences.
- **Bulirsch-Stoer rational extrapolation:** extrapolation by rational functions in $h^2$ instead of polynomials ([Thiele continued fractions](/thiele-continued-fraction-interpolation/)).

## Bounds

- **Aitken (proved):** if $s_{k+1} - s = (\rho + \epsilon_k)(s_k - s)$ with $\epsilon_k \to 0$ and $\rho \ne 1$, then $(t_k - s)/(s_{k+2} - s) \to 0$.
- **Richardson (proved):** if $s(h) = s + \sum_{j=1}^{J} c_j h^{j} + O(h^{J+1})$ and the $h_i$ shrink geometrically, the extrapolated value from $J + 1$ steps has error $O(h^{J+1})$ with a constant depending on the step ratio.
- **Shanks and Padé:** for series whose terms are moments of a positive measure (Stieltjes series), the epsilon table converges, by the convergence theory of Padé approximants (Markov).
- **Impossibility (proved):** no transformation accelerates every logarithmically convergent sequence (Delahaye and Germain-Bonnefoy 1980).
- **Rounding (observed and analyzed):** most transformations divide by differences $\Delta s_k$ that become tiny as the sequence converges, so cancellation limits attainable accuracy. Typically the best result comes before all terms are used; for logarithmic sequences, Levin-type methods may lose half the digits or more. Monitor successive estimates and stop when they stop improving.

## Reductions

- **Shanks to Padé:** $e_m$ of the partial sums of $\sum c_j x^j$ is the $[k + m / m]$ Padé approximant at $x$; the epsilon algorithm is a way to evaluate Padé approximants without computing their coefficients.
- **Richardson to polynomial interpolation:** extrapolating to $h = 0$ is evaluating the [polynomial interpolant](/polynomial-interpolation/) of $(h_i, s(h_i))$ at 0.
- **Aitken to the secant method:** applied to a fixed-point iteration, Aitken's formula is the secant step for $g(x) - x = 0$, and Steffensen's method is the resulting iteration.
- **Euler-Maclaurin:** for sums of smooth functions, the error expansion that justifies Richardson extrapolation is the [Euler-Maclaurin formula](/euler-maclaurin-formula/).

## Applications

- Numerical integration ([Romberg integration](/romberg-integration/)) and ODE solvers (Bulirsch-Stoer, extrapolated midpoint rules).
- Evaluating slowly convergent series and integrals in physics and special functions (lattice sums, Fourier integrals, zeta values).
- Summing divergent perturbation series in quantum mechanics and field theory.
- Speeding up fixed-point and iterative linear solvers (Steffensen's method, vector extrapolation, Anderson acceleration).
- Estimating limits of computations under refinement: grid refinement in PDE solvers, and continuum limits in lattice computations.

## References
