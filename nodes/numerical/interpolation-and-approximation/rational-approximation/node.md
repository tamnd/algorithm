---
tag: GEPH6Z
kind: problem
slug: rational-approximation
name: Rational approximation
aliases:
- Rational function approximation
- Best rational approximation
- Rational Chebyshev approximation
area: numerical/interpolation-and-approximation
level: advanced
summary: Approximate a function by r = p/q with deg p at most m and deg q at most n. Rationals handle poles, kinks and infinite intervals far better than polynomials, but the problem is nonlinear.
prereqs: [polynomial, minimax-approximation]
see_also: [pade-approximation, remez-algorithm, thiele-continued-fraction-interpolation, barycentric-interpolation, chebyshev-equioscillation-theorem, continued-fraction, function-approximation, chebyshev-interpolation]
sources:
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 23, Nonlinear approximation, why rational functions?; Chapter 24, Rational best approximation; Chapter 25, Two famous problems; Chapter 26, Rational interpolation and linearized least-squares
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 10, Rational approximation by the exchange algorithm (characterization of best rational approximations and the rational exchange algorithm)
  - book: isbn:9780821813744
    title: E. W. Cheney, Introduction to Approximation Theory, second edition, AMS Chelsea Publishing, 1998
    locator: Chapter 5, Rational approximation (existence, characterization by alternation, uniqueness)
  - paper: "Donald J. Newman, Rational approximation to |x|, Michigan Mathematical Journal 11 (1964) 11-14"
    locator: the explicit rational function with error at most 3 e^(-sqrt(n)), against order 1/n for polynomials
  - paper: "Yuji Nakatsukasa, Olivier Sète and Lloyd N. Trefethen, The AAA algorithm for rational approximation, SIAM Journal on Scientific Computing 40(3) (2018) A1494-A1522"
    locator: barycentric representation, greedy support point selection and linearized least squares by the SVD
  - book: isbn:9780521450072
    title: George A. Baker Jr. and Peter Graves-Morris, Padé Approximants, second edition, Cambridge University Press, 1996
    locator: Part I, Chapter 1 (Padé approximants as rational approximants determined by Taylor coefficients) and the chapters on multipoint Padé approximation
---

Rational approximation replaces a function $f$ by a quotient $r = p/q$ of two polynomials. The family of rational functions of type $(m, n)$, with $\deg p \le m$ and $\deg q \le n$, is not a linear space, so finding the best $r$ is a nonlinear problem. In exchange, rational functions approximate functions with poles, branch points, kinks, steep layers or infinite domains far better than polynomials of the same number of parameters: for $|x|$ on $[-1, 1]$ the best error falls like $e^{-\pi\sqrt{n}}$ instead of $1/n$.

## In plain words

A polynomial cannot blow up and cannot stay flat for long, so it struggles to imitate a function with a sharp corner, a spike or a vertical asymptote. A fraction of two polynomials can do all three: its bottom can almost vanish near the trouble spot, which lets it bend sharply there and stay calm elsewhere.

The price is that the problem is harder. Adding two fractions makes a more complicated fraction, so the usual tools for straight-line problems do not apply directly. Good methods exist anyway: matching derivatives at one point, matching values at chosen points, a fitting method that chooses its own points, and an exchange method for the smallest worst-case error.

## Definition

Notation on the interpolation pages: $f$ is a real function on $[a, b]$, usually $[-1, 1]$; $\mathcal{R}_{m,n}$ is the set of rational functions $r = p/q$ of type $(m, n)$, with $\deg p \le m$, $\deg q \le n$, $q \ne 0$; $\|g\|_\infty = \max_{[a,b]} |g|$; $E_{m,n}(f) = \inf_{r \in \mathcal{R}_{m,n}} \|f - r\|_\infty$ and $E_n(f) = E_{n,0}(f)$ is the polynomial case.

**Best rational approximation problem.** Given $f \in C[a, b]$ and $(m, n)$, find $r^* \in \mathcal{R}_{m,n}$ with no pole in $[a, b]$ and $\|f - r^*\|_\infty = E_{m,n}(f)$.

**Existence, characterization, uniqueness** (Chebyshev; Achieser; Powell Chapter 10). For every $f \in C[a, b]$ a best approximation exists in $\mathcal{R}_{m,n}$ and is unique. Write $r^* = p/q$ in lowest terms with $\deg p = m - \mu$, $\deg q = n - \nu$; the **defect** is $d = \min(\mu, \nu)$ (take $d = n$ if $p = 0$). Then $r^*$ is best if and only if $f - r^*$ equioscillates at $m + n + 2 - d$ points of $[a, b]$: it attains $\pm\|f - r^*\|_\infty$ with alternating signs. When $d = 0$ the best approximation is called **nondegenerate**.

**Why it is nonlinear.** $\mathcal{R}_{m,n}$ is closed under scaling but not under addition: $1/(1 + x) + 1/(2 + x)$ has type $(1, 2)$, not $(0, 1)$. The error $\|f - r\|_\infty$ as a function of the coefficients is not convex, and the best approximation need not depend continuously on $f$ when the defect is positive.

## Variants

- **Discrete or least squares.** Minimize over samples $f(x_i)$, in the max norm or in $\ell^2$. The true nonlinear least-squares problem $\min \sum |f_i - p(x_i)/q(x_i)|^2$ is solved iteratively; the **linearized** problem $\min \sum |f_i q(x_i) - p(x_i)|^2$ with a normalization of $q$ is a linear least-squares or SVD problem, but its solution may have spurious poles.
- **Rational interpolation.** Find $r \in \mathcal{R}_{m,n}$ with $r(x_i) = f_i$ at $m + n + 1$ points; solvable as a linear system for $(p, q)$, though $r$ may fail to interpolate where $q(x_i) = 0$ (unattainable points). [Thiele continued fractions](/thiele-continued-fraction-interpolation/) and barycentric rational forms compute it.
- **Padé approximation.** Match $m + n + 1$ Taylor coefficients at one point ([Padé approximation](/pade-approximation/)); the limit of rational interpolation with all points merged.
- **Domains.** Unbounded intervals ($e^{-x}$ on $[0, \infty)$), disks and other regions of the complex plane, or unions of intervals (Zolotarev problems).
- **Fixed poles.** Prescribe the poles and optimize only the numerator: the problem becomes linear, as in partial-fraction and exponential-sum approximations.

## Examples

**Rational functions are exact.** The Runge function $1/(1 + 25x^2)$ has type $(0, 2)$, so $E_{0,2} = 0$, while the polynomial errors are $E_{10} = 0.066$, $E_{20} = 9.0 \times 10^{-3}$ and $E_{40} = 1.7 \times 10^{-4}$ (see [Remez algorithm](/remez-algorithm/)). More generally, a pole at distance $\delta$ from the interval slows polynomial convergence to about $(1 + \delta)^{-n}$, but it costs a rational approximant only one degree in $q$.

**$|x|$ on $[-1, 1]$: Newman's construction.** Let $a = e^{-1/\sqrt{n}}$, $p(x) = \prod_{k=0}^{n-1} (x + a^k)$ and
$$r(x) = x\, \frac{p(x) - p(-x)}{p(x) + p(-x)}.$$
Newman (1964) proved $\| |x| - r \|_\infty \le 3 e^{-\sqrt{n}}$. Measured on a fine grid (with a logarithmic grid near 0, where the error peaks):

| $n$ | Newman's $r$, measured | bound $3e^{-\sqrt n}$ | best polynomial $\approx 0.28/n$ |
|---|---|---|---|
| 4 | $2.8 \times 10^{-2}$ | 0.41 | $7.0 \times 10^{-2}$ |
| 16 | $1.5 \times 10^{-3}$ | $5.5 \times 10^{-2}$ | $1.8 \times 10^{-2}$ |
| 64 | $1.2 \times 10^{-5}$ | $1.0 \times 10^{-3}$ | $4.4 \times 10^{-3}$ |
| 256 | $2.0 \times 10^{-9}$ | $3.4 \times 10^{-7}$ | $1.1 \times 10^{-3}$ |

The poles of $r$ cluster exponentially toward 0 on the imaginary axis, at the scale of the kink. Best approximations do better still: Stahl (1993) proved $E_{n,n}(|x|) \sim 8 e^{-\pi\sqrt{n}}$.

**$e^x$ on $[-1, 1]$.** For entire functions rational approximation still helps, though less dramatically. The asymptotic formula $E_{m,n}(e^x) \sim \frac{m!\, n!}{2^{m+n} (m+n)!\, (m+n+1)!}$ (Braess 1984) gives about $8.7 \times 10^{-5}$ for type $(2, 2)$ and $1.5 \times 10^{-10}$ for type $(4, 4)$, against $E_4 \approx 5.2 \times 10^{-4}$ and $E_8 \approx 1.1 \times 10^{-8}$ for polynomials with the same number of coefficients. The $[2/2]$ Padé approximant, which matches only at 0, has max error $4.0 \times 10^{-3}$ on the interval, at $x = 1$.

**$e^{-x}$ on $[0, \infty)$.** No polynomial approximates it at all on the unbounded interval, but $E_{n,n}$ decreases geometrically, like $9.28903^{-n}$ (the "1/9 problem", settled by Gonchar and Rakhmanov in 1987). This is why rational approximations of $e^{-x}$ are used for matrix exponentials of stiff problems.

## Known algorithms

- **[Padé approximation](/pade-approximation/).** Linear algebra on Taylor coefficients; local, cheap, and often good far from the point. $\Theta(n^3)$ dense, $\Theta(n^2)$ with Toeplitz solvers.
- **Rational interpolation** in barycentric or continued-fraction form ([Thiele](/thiele-continued-fraction-interpolation/)); $\Theta(N^2)$ for $N$ points.
- **AAA algorithm** (Nakatsukasa, Sète and Trefethen 2018). Represent $r(x) = \sum_j \frac{w_j f_j}{x - z_j} \Big/ \sum_j \frac{w_j}{x - z_j}$ in barycentric form; greedily add the sample of largest error to the support points $z_j$, and choose the weights $w$ as the smallest right singular vector of a Loewner matrix (linearized least squares on the remaining samples). Cost $O(M n^3)$ for $M$ samples and degree $n$; very robust in practice, though without a convergence proof. Spurious poles with tiny residues are removed by a cleanup step.
- **Rational Remez algorithm.** The exchange idea of the [Remez algorithm](/remez-algorithm/) with a reference of $m + n + 2$ points; each step solves a nonlinear (eigenvalue) problem for the levelled error. Convergence is locally quadratic for nondegenerate problems but can fail from a poor start; good starts come from AAA or from Carathéodory-Fejér approximation.
- **Differential correction** (Cheney and Loeb 1961). Minimizes the max error by a sequence of linear programs; it converges globally for the discrete problem.
- **Linearized and iteratively reweighted least squares** (Loeb, Sanathanan-Koerner, vector fitting); fast but without a guarantee of reaching the true optimum.

## Bounds

- **Polynomials as a special case:** $E_{m,n}(f) \le E_{m}(f)$, since polynomials are rationals of type $(m, 0)$.
- **Newman and Stahl:** $E_{n,n}(|x|) \le 3e^{-\sqrt{n}}$ (Newman 1964), $\sim 8 e^{-\pi\sqrt{n}}$ (Stahl 1993); polynomials give $E_n(|x|) \sim \beta/n$ with $\beta \approx 0.2802$ (Bernstein, Varga-Carpenter).
- **Functions with branch points.** For functions analytic in a region except at branch points, root-exponential rates $e^{-c\sqrt{n}}$ of this kind are typical, which is the basis of the lightning methods for PDEs.
- **Markov functions and Stieltjes functions:** Padé and best rational approximants converge geometrically off the support of the measure.
- **Zolotarev (1877).** The best rational approximations of $\operatorname{sign}(x)$ on $[-1, -\delta] \cup [\delta, 1]$ and of $\sqrt{x}$ are given by elliptic functions, with error decreasing like $\exp(-c n / \log(1/\delta))$.
- **Lower bound by oscillation:** if $f - r$ alternates in sign with values of size at least $h$ at $m + n + 2 - d$ points, where $d$ is the defect of $r$, then $E_{m,n}(f) \ge h$ (de la Vallée Poussin type bound, as in the polynomial case).

## Reductions

- **Polynomial case.** $n = 0$ is [minimax approximation](/minimax-approximation/) by polynomials; the alternation theorem with $d = 0$ is the [Chebyshev equioscillation theorem](/chebyshev-equioscillation-theorem/).
- **Padé from interpolation.** Rational interpolation with all nodes merged at 0 gives the Padé approximant; the linear equations become Toeplitz.
- **To linear algebra.** Linearized rational interpolation and least squares reduce to a null-vector problem for a Loewner or Vandermonde-type matrix. Fixing the poles reduces the problem to linear least squares.
- **Continued fractions.** Convergents of a [continued fraction](/continued-fraction/) expansion of $f$ are rational approximants on a staircase of types; the Euclidean algorithm on polynomials computes them.
- **Sequence extrapolation.** Shanks' transformation and Wynn's epsilon algorithm evaluate Padé approximants of a series at a point ([sequence extrapolation](/sequence-extrapolation/)).

## Applications

- Special function libraries: rational minimax approximations on reduced ranges for $\exp$, $\log$, $\Gamma$, the error function and Bessel functions.
- Matrix functions: Padé and best rational approximants of $e^x$ in scaling and squaring, Zolotarev approximants for the matrix sign function and square root, contour-integral (rational filter) eigensolvers.
- Model order reduction and system identification: transfer functions of linear systems are rational, fitted from frequency data by vector fitting or AAA.
- Digital filter design: elliptic (Cauer) filters are Zolotarev rational approximations.
- Analytic continuation, locating poles and singularities from samples, and lightning solvers for Laplace problems with corner singularities.

## References
