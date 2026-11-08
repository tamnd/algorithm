---
tag: ZQ5R4Y
kind: concept
slug: chebyshev-series
name: Chebyshev series
aliases:
- Chebyshev expansion
- Chebyshev-Fourier series
- expansion in Chebyshev polynomials
area: numerical/interpolation-and-approximation
level: advanced
summary: f(x) = Σ a_k T_k(x) on [-1, 1], the Fourier cosine series of f(cos θ). Coefficients decay like the smoothness of f allows, geometrically for analytic f, and are computed by a DCT.
prereqs: [chebyshev-polynomials, orthogonal-polynomials]
see_also: [chebyshev-interpolation, chebyshev-economization, discrete-cosine-transform, fast-dct, clenshaw-curtis-quadrature, spectral-methods, gibbs-phenomenon, minimax-approximation]
sources:
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 3 (Chebyshev series, Theorem 3.1), Chapter 4 (interpolants, projections and aliasing), Chapter 7 (convergence for differentiable functions) and Chapter 8 (convergence for analytic functions, Bernstein ellipses)
  - book: isbn:9780849303555
    title: J. C. Mason and D. C. Handscomb, Chebyshev Polynomials, Chapman and Hall/CRC, 2003
    locator: Chapter 4 (best and near-best approximation) and Chapter 5 (Chebyshev series, convergence and the Fourier connection)
  - book: isbn:9780471628965
    title: Theodore J. Rivlin, Chebyshev Polynomials, second edition, Wiley, 1990
    locator: Chapter 3, Expansions in Chebyshev polynomials
  - book: isbn:9780486411835
    title: John P. Boyd, Chebyshev and Fourier Spectral Methods, second edition, Dover, 2001
    locator: Chapter 2, Chebyshev and Fourier series (coefficient decay and the Darboux principle)
  - paper: "C. W. Clenshaw, A note on the summation of Chebyshev series, Mathematical Tables and Other Aids to Computation 9 (1955) 118-120"
    locator: the three-term recurrence for evaluating a Chebyshev series
  - paper: "C. Lanczos, Trigonometric interpolation of empirical and analytical functions, Journal of Mathematics and Physics 17 (1938) 123-199"
    locator: expansions in Chebyshev polynomials and their use for economizing power series
---

A Chebyshev series writes a function $f$ on $[-1, 1]$ as
$$f(x) = \sum_{k=0}^{\infty} a_k T_k(x), \qquad a_k = \frac{2}{\pi}\int_{-1}^{1} \frac{f(x) T_k(x)}{\sqrt{1 - x^2}}\,dx \quad (k \ge 1), \qquad a_0 = \frac{1}{\pi}\int_{-1}^{1} \frac{f(x)}{\sqrt{1 - x^2}}\,dx,$$
where $T_k$ are the [Chebyshev polynomials](/chebyshev-polynomials/). With $x = \cos\theta$ it is the Fourier cosine series of $f(\cos\theta)$, so everything known about Fourier series transfers, and the coefficients can be computed by a fast cosine transform. The coefficients decay as fast as $f$ is smooth: algebraically for functions with finitely many derivatives, geometrically for analytic functions. The truncation $f_n = \sum_{k \le n} a_k T_k$ is within a factor of order $\log n$ of the best polynomial approximation, which makes the Chebyshev series the standard representation of functions in numerical software.

## In plain words

Any reasonable function on an interval can be built by adding up a few standard wavy curves, each with a weight. For Chebyshev series the standard curves are the Chebyshev polynomials: the first is flat, the second a straight line, and each next one wiggles once more, always staying between $-1$ and $1$.

The weights tell you how much of each wiggle the function contains. For smooth functions the weights shrink very quickly, so a short sum gives an excellent approximation, and the size of the first dropped weight tells you roughly how large the error is. Since every curve stays between $-1$ and $1$, the error of dropping the tail is at most the sum of the dropped weights.

## The idea

**Notation.** As on the other interpolation and approximation pages, $f$ is a function on $[-1, 1]$ (other intervals are mapped by an affine change of variable), $T_k(\cos\theta) = \cos k\theta$, $p_n$ is the polynomial interpolant of degree at most $n$, $E_n(f)$ is the error of the best approximation by polynomials of degree at most $n$ in the maximum norm, and $\Lambda_n$ is a Lebesgue constant.

**Existence (proved, Trefethen ATAP Theorem 3.1).** If $f$ is Lipschitz continuous on $[-1, 1]$, its Chebyshev series converges absolutely and uniformly to $f$, and the coefficients are given by the integrals above. The proof substitutes $x = \cos\theta$: $F(\theta) = f(\cos\theta)$ is even, $2\pi$-periodic and Lipschitz, so its Fourier series is the cosine series $\sum a_k \cos k\theta$, and the integrals are the Fourier coefficients after the change of variables. The $T_k$ are orthogonal for the weight $(1 - x^2)^{-1/2}$, with $\int T_j T_k (1 - x^2)^{-1/2} dx = 0$ for $j \ne k$, $\pi$ for $j = k = 0$ and $\pi/2$ for $j = k \ge 1$, so $f_n$ is the best approximation of degree $n$ in that weighted $L^2$ norm.

**Decay of the coefficients (proved, ATAP Theorems 7.1 and 8.1).**

- If $f, f', \ldots, f^{(\nu - 1)}$ are absolutely continuous and $f^{(\nu)}$ has bounded variation $V$, for some $\nu \ge 1$, then $|a_k| \le \dfrac{2V}{\pi k(k-1)\cdots(k-\nu)}$ for $k \ge \nu + 1$, so $a_k = O(k^{-\nu-1})$.
- If $f$ is analytic in the open region bounded by the Bernstein ellipse $E_\rho$, $\rho > 1$ (foci $\pm1$, semi-axes summing to $\rho$), and $|f| \le M$ there, then $|a_0| \le M$ and $|a_k| \le 2M\rho^{-k}$ for $k \ge 1$.

The ellipse is the natural region for $[-1, 1]$, as the disk is for Taylor series: the largest admissible $\rho$ is set by the singularity of $f$ nearest to the interval in this elliptical sense.

**Truncation error (proved, ATAP Theorems 7.2 and 8.2).** Under the first hypothesis with $\nu \ge 1$ and $n > \nu$, $\|f - f_n\|_\infty \le \dfrac{2V}{\pi\nu(n - \nu)^\nu}$; under the second, $\|f - f_n\|_\infty \le \dfrac{2M\rho^{-n}}{\rho - 1}$. The [Chebyshev interpolant](/chebyshev-interpolation/) satisfies the same bounds with the constant doubled. In all cases $\|f - f_n\|_\infty \le \sum_{k > n} |a_k|$, since $|T_k| \le 1$.

**Near-best (proved).** Truncation is a linear projection whose norm $L_n$ equals the Lebesgue constant of Fourier partial sums, $L_n = \frac{1}{\pi}\int_0^\pi \left|\frac{\sin((n + 1/2)\theta)}{\sin(\theta/2)}\right| d\theta = \frac{4}{\pi^2}\log n + O(1)$. Hence $\|f - f_n\|_\infty \le (1 + L_n)E_n(f)$: never worse than the best approximation by more than a logarithmic factor, and in practice, for analytic $f$, within a factor of about 2.

**Computing the coefficients.** Sample $f$ at the $n + 1$ [Chebyshev points](/chebyshev-nodes/) of the second kind $x_j = \cos(j\pi/n)$; a [discrete cosine transform](/discrete-cosine-transform/) (DCT-I) of the samples gives the coefficients $c_k$ of the interpolant $p_n$ in $O(n \log n)$ operations with a [fast DCT](/fast-dct/). They differ from the $a_k$ by aliasing (ATAP Theorem 4.2): $c_k = a_k + \sum_{m \ge 1} (a_{2mn - k} + a_{2mn + k})$ for $0 < k < n$, with modified formulas at $k = 0$ and $k = n$. For smooth $f$ the aliasing terms are tiny, so in practice one samples on a growing grid until the trailing $c_k$ fall to the level of rounding, then chops.

**Evaluation.** A finite series $\sum_{k=0}^n a_k T_k(x)$ is evaluated by Clenshaw's recurrence $b_k = a_k + 2x b_{k+1} - b_{k+2}$ ($b_{n+1} = b_{n+2} = 0$), with value $a_0 + x b_1 - b_2$, in about $3n$ operations (one multiplication by $2x$, one addition and one subtraction per step), without forming the $T_k$ and without converting to the monomial basis (whose coefficients can be exponentially larger than the $a_k$, see [Chebyshev economization](/chebyshev-economization/)). Its rounding errors are bounded by a modest multiple of $u\sum|a_k|$ times a factor that grows at most polynomially in $n$; in practice the observed error is close to $u\sum|a_k|$.

**Floating point.** For a function of size about 1 computed in double precision, the coefficients of the sampled interpolant decrease until about $10^{-16}$ and then level off in a plateau of rounding noise. The position of the plateau tells you the degree needed for machine accuracy; continuing past it adds noise, not accuracy (observed behaviour; Chebfun's chopping rule is built on it).

## Examples

**$e^x$.** The coefficients are $a_0 = I_0(1)$ and $a_k = 2I_k(1)$, with $I_k$ the modified Bessel functions:
$$a_0 \approx 1.26607, \ a_1 \approx 1.13032, \ a_2 \approx 0.271495, \ a_3 \approx 0.0443368, \ a_4 \approx 0.00547424, \ a_5 \approx 5.42926 \times 10^{-4},$$
falling faster than geometrically because $e^x$ is entire. The truncation errors (maximum on a fine grid, computed in double precision) are $5.91 \times 10^{-4}$ for $n = 4$, $1.16 \times 10^{-8}$ for $n = 8$, and rounding level for $n = 16$; each is close to the first dropped coefficient ($5.43 \times 10^{-4}$ and $1.10 \times 10^{-8}$).

**The Runge function $1/(1 + 25x^2)$.** It has poles at $\pm i/5$, which lie on the Bernstein ellipse with $\rho = \frac15 + \sqrt{1 + \frac{1}{25}} \approx 1.2198$. Only even coefficients are nonzero, and the ratio $|a_{k+2}/a_k|^{1/2}$ is $0.81980$ at $k = 20$ and $k = 40$, matching $1/\rho \approx 0.81980$. The truncation errors are $1.10 \times 10^{-1}$, $1.51 \times 10^{-2}$ and $2.84 \times 10^{-4}$ for $n = 10, 20, 40$: geometric convergence with rate $\rho^{-n}$, where equispaced interpolation diverges ([Runge phenomenon](/runge-phenomenon/)).

**$|x|$.** From $|\cos\theta| = \frac{2}{\pi} + \frac{4}{\pi}\sum_{j \ge 1} \frac{(-1)^{j+1}}{4j^2 - 1}\cos 2j\theta$,
$$|x| = \frac{2}{\pi} + \frac{4}{\pi}\left(\frac{T_2(x)}{3} - \frac{T_4(x)}{15} + \frac{T_6(x)}{35} - \cdots\right).$$
Here $\nu = 1$ (the derivative jumps), the coefficients decay like $k^{-2}$, and the truncation error is attained at $x = 0$: $5.79 \times 10^{-2}$, $3.03 \times 10^{-2}$ and $1.55 \times 10^{-2}$ for $n = 10, 20, 40$, halving as $n$ doubles, as the bound $O(1/n)$ predicts.

**Non-example: a jump.** For the sign function the coefficients decay only like $1/k$, the series converges pointwise but not uniformly, and partial sums overshoot near $0$ by about 9 percent of the jump, the [Gibbs phenomenon](/gibbs-phenomenon/). Chebyshev series are a tool for smooth functions; for piecewise smooth ones, split the interval at the breakpoints.

## Where it is used

- **Function evaluation.** Special-function libraries and numerical recipes store precomputed Chebyshev coefficients on subintervals and evaluate them by Clenshaw's recurrence.
- **[Chebyshev interpolation](/chebyshev-interpolation/) and Chebfun.** Represent functions to machine precision by adaptively chosen Chebyshev coefficients, then differentiate, integrate, find roots and solve equations on that representation.
- **[Chebyshev economization](/chebyshev-economization/).** Convert a power series to a Chebyshev series and drop the small tail to lower the degree with little loss.
- **Quadrature.** [Clenshaw-Curtis quadrature](/clenshaw-curtis-quadrature/) integrates the Chebyshev interpolant term by term, using $\int_{-1}^1 T_k = 2/(1 - k^2)$ for even $k$.
- **[Spectral methods](/spectral-methods/)** for differential equations on nonperiodic intervals.
- **Near-minimax approximation.** The truncated series is a good starting point for the [Remez algorithm](/remez-algorithm/) and often a good enough answer by itself ([minimax approximation](/minimax-approximation/)).

## References
