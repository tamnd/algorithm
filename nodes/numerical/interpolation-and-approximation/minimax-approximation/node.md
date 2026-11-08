---
tag: CAJJWW
kind: problem
slug: minimax-approximation
name: Minimax approximation
aliases:
- Best uniform approximation
- Chebyshev approximation
- Best approximation in the maximum norm
area: numerical/interpolation-and-approximation
level: advanced
summary: Find the approximant of a fixed form, usually a polynomial of degree n, that minimizes the maximum error on an interval. It exists, is unique, and is characterized by equioscillation.
prereqs: [approximation-theory, weierstrass-approximation-theorem, chebyshev-polynomials]
see_also: [remez-algorithm, chebyshev-equioscillation-theorem, chebyshev-interpolation, lebesgue-constant, jackson-theorem, rational-approximation, chebyshev-economization, least-squares-approximation]
sources:
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 1, The approximation problem and existence of best approximations; Chapter 2, The uniqueness of best approximations; Chapter 7, The theory of minimax approximation
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 10, Best approximation, and Chapter 16, Best and near-best
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 8, Approximation in the infinity-norm
  - book: isbn:9780821813744
    title: E. W. Cheney, Introduction to Approximation Theory, second edition, AMS Chelsea Publishing, 1998
    locator: Chapter 1, existence of best approximations, and Chapter 3, Tchebycheff approximation (characterization, uniqueness and the Haar condition)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 4.2, The minimax approximation problem, and Section 4.6, Minimax approximation
  - paper: "Pafnuty L. Chebyshev, Théorie des mécanismes connus sous le nom de parallélogrammes, Mémoires des savants étrangers présentés à l'Académie de Saint-Pétersbourg 7 (1854)"
    locator: the problem of least maximum deviation and the polynomials of least deviation from zero
---

Minimax approximation asks for the approximant, from a fixed family such as the polynomials of degree at most $n$, whose largest error over an interval is as small as possible. The answer, the **best uniform approximation**, gives the smallest worst-case error that any formula of that form can achieve. That is why it is the design target for the approximations inside mathematical function libraries. For polynomials it exists, is unique, and is characterized by an error curve that reaches its maximum with alternating signs at $n + 2$ points. The [Remez algorithm](/remez-algorithm/) computes it.

## In plain words

You want to replace a complicated function by a simple formula, say a polynomial of a given degree, and you care only about the worst mistake anywhere on the interval. Minimax approximation finds the formula whose worst mistake is the smallest possible.

The best formula has a recognizable shape of error. Its mistakes swing up and down across the interval, reaching the same largest size again and again with alternating signs, as many times as the formula has free numbers plus one. If any peak were taller than the others, the formula could be nudged to lower it. Finding this formula takes an iterative method, but cheaper formulas, built from Chebyshev's special points, are usually almost as good.

## Definition

Notation on the interpolation pages: $f$ is continuous on $[a, b]$ (often $[-1, 1]$), $\|g\|_\infty = \max_{x \in [a, b]} |g(x)|$, $\mathcal{P}_n$ is the space of polynomials of degree at most $n$, and
$$E_n(f) = \min_{p \in \mathcal{P}_n} \|f - p\|_\infty.$$
$T_k$ are the Chebyshev polynomials.

**Problem.** Given $f$ and $n$, find $p^* \in \mathcal{P}_n$ with $\|f - p^*\|_\infty = E_n(f)$. More generally, given a subset $\mathcal{A}$ of $C[a, b]$, find $a^* \in \mathcal{A}$ minimizing $\|f - a\|_\infty$.

**Existence.** For any finite-dimensional subspace $\mathcal{A}$ a best approximation exists: the minimization can be restricted to $\{a : \|a\| \le 2\|f\|\}$, a closed bounded set in a finite-dimensional space, hence compact, and $a \mapsto \|f - a\|$ is continuous.

**Characterization (Chebyshev).** $p^* \in \mathcal{P}_n$ is a best approximation to $f$ if and only if there are $n + 2$ points $x_0 < \cdots < x_{n+1}$ in $[a, b]$ at which
$$f(x_i) - p^*(x_i) = \sigma (-1)^i \|f - p^*\|_\infty, \qquad \sigma \in \{-1, 1\}.$$
This is the [Chebyshev equioscillation theorem](/chebyshev-equioscillation-theorem/).

**Uniqueness.** The best polynomial approximation is unique. If $p$ and $q$ are both best, so is $(p + q)/2$, and at its alternation points both $f - p$ and $f - q$ must equal the same extreme value, so $p - q$ has $n + 2$ zeros and $p = q$. The same holds for any **Haar subspace**, an $(n+1)$-dimensional space in which every nonzero element has at most $n$ zeros on $[a, b]$. The best approximation is even **strongly unique**: $\|f - p\| \ge E_n(f) + \gamma \|p - p^*\|$ for some $\gamma > 0$ depending on $f$.

## Variants

- **Weighted and relative error.** Minimize $\|w (f - p)\|_\infty$ for a positive continuous weight $w$; $w = 1/|f|$ gives relative error, which is what floating-point libraries need. The theory is unchanged.
- **Rational minimax.** Minimize over $r = p/q$ of type $(m, n)$. Best approximations exist and are unique, with an alternation of $m + n + 2 - d$ points, where $d$ is the defect; the problem is nonlinear. See [rational approximation](/rational-approximation/).
- **Trigonometric and other Haar spaces.** Trigonometric polynomials of degree $n$ on a period form a Haar space of dimension $2n + 1$, with alternation at $2n + 2$ points.
- **Discrete minimax.** Minimize over a finite set of points; this is a linear program.
- **Several variables.** By Mairhuber's theorem (1956), no Haar space of dimension at least 2 exists on a domain containing a two-dimensional region, so multivariate best approximations need not be unique and no alternation theorem holds.
- **Complex domains.** Best approximation on a compact set in $\mathbb{C}$; the polynomials of least deviation from zero on a set are its Chebyshev polynomials, central in potential theory and in Krylov methods.
- **Other norms.** In $L^2$ the best approximation is an orthogonal projection, computed linearly ([least-squares approximation](/least-squares-approximation/)); in $L^1$ it is characterized by sign changes at canonical points.

## Examples

- **$x^{n+1}$.** $E_n(x^{n+1}) = 2^{-n}$ on $[-1, 1]$, with $p^*(x) = x^{n+1} - 2^{-n} T_{n+1}(x)$; the error $2^{-n} T_{n+1}$ alternates at the $n + 2$ points $\cos(k\pi/(n+1))$. This is the extremal property of [Chebyshev polynomials](/chebyshev-polynomials/).
- **A convex function, degree 1.** For $e^x$ on $[-1, 1]$, the best line has slope $\sinh 1$, equal to the chord slope, and touches the error extremes at $-1$, $\xi = \log \sinh 1 \approx 0.1614$ and $1$; $E_1(e^x) = \tfrac12\big(e^{-1} - \sinh 1 + \sinh 1\,(1 + \xi)\big) \approx 0.2788$.
- **$|x|$, degree 2.** $p^*(x) = x^2 + \tfrac18$, $E_2(|x|) = \tfrac18$, with five alternation points $-1, -\tfrac12, 0, \tfrac12, 1$; $p^*$ is also the best cubic, since $|x|$ is even.
- **Computed values and near-best approximations.** Maximum errors on $[-1, 1]$, best approximation (by the Remez algorithm) against interpolation at the $n + 1$ Chebyshev points of the first kind:

| $f$ | $n$ | $E_n(f)$ | Chebyshev interpolant | ratio |
|---|---|---|---|---|
| $e^x$ | 4 | $5.467 \times 10^{-4}$ | $6.397 \times 10^{-4}$ | 1.17 |
| $e^x$ | 8 | $1.106 \times 10^{-8}$ | $1.219 \times 10^{-8}$ | 1.10 |
| $1/(1 + 25x^2)$ | 8 | $9.809 \times 10^{-2}$ | 0.1708 | 1.74 |
| $1/(1 + 25x^2)$ | 16 | $2.001 \times 10^{-2}$ | $3.261 \times 10^{-2}$ | 1.63 |
| $\lvert x\rvert$ | 8 | $3.469 \times 10^{-2}$ | $6.698 \times 10^{-2}$ | 1.93 |
| $\lvert x\rvert$ | 16 | $1.747 \times 10^{-2}$ | $3.521 \times 10^{-2}$ | 2.02 |

For $e^x$, $E_n$ is close to $1/(2^n (n+1)!)$, which is $1.076 \times 10^{-8}$ at $n = 8$: the leading term of the error behaves like a multiple of $T_{n+1}$. In every case the Chebyshev interpolant loses at most about one bit of accuracy.

## Known algorithms

- **[Remez algorithm](/remez-algorithm/).** Solve a levelled interpolation problem on $n + 2$ reference points and exchange them for the extrema of the error. It converges for every continuous $f$ (single exchange) and quadratically for smooth $f$ (multiple exchange); each step costs $O(n^3)$ for the linear solve plus the search for extrema.
- **Linear programming.** On a finite grid of $m$ points, minimize $t$ subject to $-t \le f(x_j) - p(x_j) \le t$: a linear program with $n + 2$ variables and $2m$ constraints. Solving it on a fine grid gives an approximation to the continuous problem.
- **Near-best methods.** [Chebyshev interpolation](/chebyshev-interpolation/) gives $\|f - p_n\| \le (1 + \Lambda_n) E_n(f)$ with $\Lambda_n \le \tfrac{2}{\pi}\log(n + 1) + 1$; truncating the Chebyshev series is within a similar logarithmic factor; Carathéodory-Fejér approximation is often indistinguishable from best for smooth $f$. [Chebyshev economization](/chebyshev-economization/) lowers the degree of a polynomial with a nearly minimax error.
- **Rational case.** Rational Remez, and the AAA-Lawson iteration for rational approximations, as in [rational approximation](/rational-approximation/).

## Bounds

- **de la Vallée Poussin.** If $f - p$ alternates in sign at $n + 2$ points, then $\min_i |f(x_i) - p(x_i)| \le E_n(f)$: a computable lower bound from any trial polynomial.
- **Interpolation error.** If $f \in C^{n+1}[-1, 1]$, interpolation at Chebyshev points and the [error theorem](/polynomial-interpolation-error-theorem/) give $E_n(f) \le \|f^{(n+1)}\|_\infty/(2^n (n+1)!)$. Conversely, $E_n(f) \ge \min |f^{(n+1)}|/(2^n (n+1)!)$ when $f^{(n+1)}$ does not change sign, from the same alternation argument.
- **Jackson's theorems.** $E_n(f) \le C\, \omega_f(1/n)$ for continuous $f$ on $[-1, 1]$, and $E_n(f) \le C_k\, n^{-k} \omega_{f^{(k)}}(1/n)$ if $f \in C^k$ ([Jackson's theorem](/jackson-theorem/)). Bernstein's inverse theorems show these rates characterize the smoothness of $f$ away from the endpoints.
- **Analytic functions.** If $f$ is analytic and bounded by $M$ inside the Bernstein ellipse with foci $\pm 1$ and semi-axis sum $\rho > 1$, then $E_n(f) \le 2M\rho^{-n}/(\rho - 1)$, and the rate $\rho^{-n}$ is sharp for the largest such $\rho$ (Bernstein).
- **No rate in general.** By the [Weierstrass theorem](/weierstrass-approximation-theorem/), $E_n(f) \to 0$ for every continuous $f$, but for any non-increasing sequence tending to 0 some continuous $f$ has $E_n(f)$ equal to it.
- **$|x|$.** $\lim_{n \to \infty} n\, E_n(|x|) = \beta \approx 0.28017$, Bernstein's constant (for even $n$; Varga and Carpenter computed it to many digits).

## Reductions

- **To linear programming** on a finite set, as above; the exchange algorithm is the simplex method on the dual program.
- **Rational minimax to a sequence of linear problems.** For fixed $h$, the levelled rational equations are linear in the coefficients of $p$ and $q$; differential correction and rational Remez exploit this.
- **Near-best to interpolation.** The bound $\|f - p_n\| \le (1 + \Lambda_n) E_n(f)$ reduces approximate minimax approximation to interpolation at nodes with a small [Lebesgue constant](/lebesgue-constant/).
- **Shift of the problem.** Approximating $f$ by $\mathcal{P}_n$ on $[a, b]$ is the same problem on $[-1, 1]$ after an affine change of variable; adding a polynomial of degree $n$ to $f$ shifts $p^*$ by it.

## Applications

- **Elementary function libraries.** After argument reduction, $\sin$, $\exp$, $\log$ and others are computed by polynomials or rationals designed by weighted Remez to minimize the relative error.
- **Digital filter design.** The Parks-McClellan algorithm designs FIR filters by trigonometric minimax approximation of the ideal frequency response.
- **Krylov methods.** Error bounds for conjugate gradients and [Chebyshev iteration](/chebyshev-iteration/) come from polynomials of least maximum norm on an interval containing the spectrum, $T_k$ rescaled.
- **Model reduction and signal processing.** Zolotarev's rational minimax problems give elliptic filters and optimal parameters for ADI iterations.
- **Theory.** $E_n(f)$ measures the intrinsic polynomial approximability of $f$; it is the yardstick against which interpolation, series truncation and quadrature are judged.

## References
