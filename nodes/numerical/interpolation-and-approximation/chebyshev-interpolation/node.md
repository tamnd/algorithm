---
tag: YWEZA4
kind: algorithm
slug: chebyshev-interpolation
name: Chebyshev interpolation
aliases:
- Interpolation at Chebyshev nodes
- Chebyshev polynomial interpolation
- Chebyshev-Lobatto interpolation
area: numerical/interpolation-and-approximation
level: advanced
summary: Sample f at n + 1 Chebyshev points, get the Chebyshev coefficients of the interpolant by a cosine transform, and evaluate by Clenshaw's recurrence. Near-best, and geometric for analytic f.
solves: [interpolation-problem, function-approximation]
model: real-ram
complexity:
  vars: {n: "the degree, with n + 1 samples of f"}
  time: {setup: Θ(n log n), per_point: Θ(n)}
  space: {extra: Θ(n)}
  flops: {setup_direct: "2n^2", per_point: "3n + 8"}
properties: {deterministic: true, recursive: false, near_best: true, exact_on: "polynomials of degree at most n"}
history:
  year: 1938
  people: [Pafnuty Chebyshev, Cornelius Lanczos, Charles W. Clenshaw, Sergei Bernstein, Lloyd N. Trefethen]
  note: Lanczos (1938) used Chebyshev expansions computed from samples; Clenshaw (1955) gave the summation recurrence; Chebfun (Battles and Trefethen, 2004) made adaptive Chebyshev interpolation a general tool.
prereqs: [chebyshev-nodes, chebyshev-series, polynomial-interpolation]
see_also: [barycentric-interpolation, lebesgue-constant, runge-phenomenon, discrete-cosine-transform, fast-dct, clenshaw-curtis-quadrature, chebyshev-economization, polynomial-interpolation-error-theorem]
sources:
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapters 2 to 4 (Chebyshev points, series and interpolants, aliasing), Chapters 7 and 8 (Theorems 7.2 and 8.2, convergence rates), Chapter 15 (Lebesgue constants) and Chapter 16 (best approximation versus Chebyshev interpolation)
  - book: isbn:9780849303555
    title: J. C. Mason and D. C. Handscomb, Chebyshev Polynomials, Chapman and Hall/CRC, 2003
    locator: Chapter 6, Chebyshev interpolation (discrete orthogonality and the coefficient formulas)
  - paper: doi:10.1093/imanum/24.4.547
    title: "Nicholas J. Higham, The numerical stability of barycentric Lagrange interpolation, IMA Journal of Numerical Analysis 24(4) (2004) 547-556"
    locator: forward stability of the second barycentric formula for Chebyshev points
  - paper: doi:10.1137/S0036144502417715
    title: "Jean-Paul Berrut and Lloyd N. Trefethen, Barycentric Lagrange interpolation, SIAM Review 46(3) (2004) 501-517"
    locator: Section 5, Chebyshev points and their barycentric weights
  - paper: "C. W. Clenshaw, A note on the summation of Chebyshev series, Mathematical Tables and Other Aids to Computation 9 (1955) 118-120"
    locator: the recurrence of lines L5 and L6
  - paper: "Zachary Battles and Lloyd N. Trefethen, An extension of MATLAB to continuous functions and operators, SIAM Journal on Scientific Computing 25(5) (2004) 1743-1770"
    locator: adaptive Chebyshev interpolation with chopping of the coefficients
---

Chebyshev interpolation approximates a function $f$ on $[a, b]$ by the polynomial $p_n$ of degree at most $n$ that agrees with $f$ at the $n + 1$ [Chebyshev points](/chebyshev-nodes/) $x_j = \cos(j\pi/n)$, mapped to $[a, b]$. The interpolant is stored by its coefficients in the [Chebyshev series](/chebyshev-series/) basis, $p_n = \sum_{k=0}^n c_k T_k$, which a discrete cosine transform of the samples produces, and is evaluated by Clenshaw's recurrence in $O(n)$ per point. Unlike interpolation at equispaced points, it converges for every Lipschitz function: its error is at most $1 + \Lambda_n \le 2 + \frac{2}{\pi}\log(n + 1)$ times the best possible, and it decreases geometrically, like $\rho^{-n}$, when $f$ is analytic in a Bernstein ellipse $E_\rho$. It is the basis of Chebfun and of most modern function approximation on intervals.

## In plain words

To copy a curve with a polynomial, you choose some points on the curve and draw the polynomial through them. With evenly spaced points this goes badly: the polynomial swings wildly near the ends. If instead you crowd the points toward the two ends, in the pattern you get by projecting equally spaced points on a semicircle down onto its diameter, the swings disappear and the copy gets better and better as you add points.

The polynomial is kept as a list of weights on standard wavy curves (Chebyshev polynomials). Getting the weights from the sampled values is a cosine transform, the same kind of computation as a Fourier transform. The size of the last weights tells you when you have taken enough points.

## The problem

The input is a way to evaluate $f$ on $[a, b]$ (a black box, or a table of values at the Chebyshev points), a degree $n \ge 0$, and evaluation points $t$. The output is the coefficients $c_0, \ldots, c_n$ of the interpolant
$$p_n(x) = \sum_{k=0}^n c_k T_k(x), \qquad p_n(x_j) = f\big(\tfrac{a + b}{2} + \tfrac{b - a}{2}x_j\big), \quad x_j = \cos\frac{j\pi}{n}, \ j = 0, \ldots, n,$$
and the values $p_n$ at the points $t$. For $n = 0$ the single point is $x_0 = 0$. The interpolant exists and is unique ([uniqueness theorem](/interpolating-polynomial-uniqueness/)).

Notation on the interpolation and approximation pages: $f$ is the function, mapped to $[-1, 1]$; $T_k$ are the Chebyshev polynomials; $p_n$ is the interpolant of degree at most $n$; $\omega(x) = \prod_j (x - x_j)$ is the node polynomial; $\Lambda_n$ is the Lebesgue constant; $E_n(f)$ is the best approximation error in the maximum norm. Costs are arithmetic operations on the [real RAM](/real-ram/), plus $n + 1$ evaluations of $f$.

## The algorithm

```pseudo id=main
CHEBYSHEV-INTERPOLATE(f, n, a, b)                       ▷ n ≥ 1
L1  for j ← 0 to n: x[j] ← cos(jπ/n);  v[j] ← f((a + b)/2 + (b − a)/2 · x[j])
L2  for k ← 0 to n: c[k] ← (2/n) Σ'' over j of v[j]·cos(jkπ/n)  ▷ Σ'' halves the j = 0 and j = n terms
L3  c[0] ← c[0]/2;  c[n] ← c[n]/2                      ▷ L2 and L3 together are a DCT-I
CHEBYSHEV-EVAL(c, t, a, b)
L4  x ← (2t − a − b)/(b − a)
L5  b[n+1] ← 0;  b[n+2] ← 0;  for k ← n down to 1: b[k] ← c[k] + 2x·b[k+1] − b[k+2]
L6  return c[0] + x·b[1] − b[2]
```

Line L2 is written as a direct sum, $O(n^2)$; a fast DCT computes the same numbers in $O(n \log n)$ by an FFT of length $2n$. The implementation computes the points in the form $x_j = \sin(\pi(n - 2j)/(2n))$, which gives exactly symmetric points, and reduces the cosine arguments $jk \bmod 2n$ so that only $2n$ cosines are needed.

**Choosing $n$ adaptively.** Double $n$ (8, 16, 32, ...) until the last few coefficients are below a tolerance relative to the largest, then drop the trailing small coefficients. Doubling reuses all previous samples, since the points for $n$ are among those for $2n$. This is the strategy of Chebfun, refined there by a more careful chopping rule.

**Evaluating without coefficients.** The values $p_n(t)$ can also be computed directly from the samples by the second [barycentric formula](/barycentric-interpolation/) with the weights $w_j = (-1)^j$, halved for $j = 0$ and $j = n$, in $O(n)$ per point with no transform at all.

## Example

**$e^x$ with $n = 4$.** The coefficients of the interpolant (double precision) are
$$c_0 = 1.26607, \ c_1 = 1.13032, \ c_2 = 0.27154, \ c_3 = 0.0448798, \ c_4 = 0.00547424.$$
Compare the Chebyshev series coefficients $a_0 = 1.26607$, $a_1 = 1.13032$, $a_2 = 0.271495$, $a_3 = 0.0443368$, $a_4 = 0.00547424$. The differences show aliasing: on these 5 points $T_6$ and $T_5$ are indistinguishable from $T_2$ and $T_3$, so $c_2 - a_2 \approx a_6 = 4.5 \times 10^{-5}$ and $c_3 - a_3 \approx a_5 = 5.4 \times 10^{-4}$. The maximum error is $1.07 \times 10^{-3}$, about twice that of the truncated series, as the bounds below predict.

**The Runge function $1/(1 + 25x^2)$.** Maximum errors on a fine grid (double precision):

| $n$ | 10 | 20 | 40 | 80 | 160 |
|---|---|---|---|---|---|
| Chebyshev interpolation | 1.32e-1 | 1.77e-2 | 3.40e-4 | 1.20e-7 | 1.52e-14 |
| $\rho^{-n}$, $\rho = 1.2198$ | 1.37e-1 | 1.88e-2 | 3.54e-4 | 1.25e-7 | 1.56e-14 |

The error follows $\rho^{-n}$, where $\rho = \frac15 + \sqrt{1 + \frac1{25}}$ is set by the poles at $\pm i/5$. At equispaced points the same interpolants diverge ([Runge phenomenon](/runge-phenomenon/)). The adaptive rule with tolerance $10^{-14}$ stops at 165 coefficients with error $5.8 \times 10^{-15}$; for $e^x$ it stops at 14.

**$|x|$.** The errors for $n = 10, 20, 40, 80$ are $5.92 \times 10^{-2}$, $2.98 \times 10^{-2}$, $1.49 \times 10^{-2}$, $7.46 \times 10^{-3}$: they halve as $n$ doubles, the rate $O(1/n)$ for a function whose derivative has a jump.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The steps are these.

1. *Discrete orthogonality.* For $0 \le k, m \le n$, $\sum''_j T_k(x_j) T_m(x_j)$ is $0$ if $k \ne m$, $n/2$ if $k = m \notin \{0, n\}$, and $n$ if $k = m \in \{0, n\}$. This is a cosine sum identity, since $T_k(x_j) = \cos(jk\pi/n)$.
2. *Coefficients.* If $p_n = \sum c_m T_m$ takes the values $v_j$ at the points, multiplying by $T_k(x_j)$ and summing with $\sum''$ isolates $c_k$, which gives lines L2 and L3. So the $c_k$ are the coefficients of the unique interpolant.
3. *Clenshaw.* With $b_k$ as in L5, the three-term recurrence $T_{k+1} = 2xT_k - T_{k-1}$ telescopes the sum to $c_0 + x b_1 - b_2$, so L6 returns $p_n(x)$. Line L4 maps $[a, b]$ affinely onto $[-1, 1]$.
4. *Aliasing.* On the points, $T_{2mn \pm k}(x_j) = T_k(x_j)$, so the interpolant of $\sum a_k T_k$ has $c_k = a_k + \sum_{m \ge 1}(a_{2mn - k} + a_{2mn + k})$ for $0 < k < n$ (ATAP Theorem 4.2).

**Error bounds (proved, Trefethen ATAP).**

- *Near-best.* $\|f - p_n\|_\infty \le (1 + \Lambda_n)E_n(f)$ for every continuous $f$, and for these points $\Lambda_n \le \frac{2}{\pi}\log(n + 1) + 1$ (Theorem 15.2). At $n = 1000$ this factor is below 6.
- *Differentiable $f$.* If $f, \ldots, f^{(\nu - 1)}$ are absolutely continuous and $f^{(\nu)}$ has bounded variation $V$, $\nu \ge 1$, then $\|f - p_n\|_\infty \le \dfrac{4V}{\pi\nu(n - \nu)^\nu}$ for $n > \nu$ (Theorem 7.2). For $|x|$, $\nu = 1$ and $V = 2$.
- *Analytic $f$.* If $f$ is analytic inside the Bernstein ellipse $E_\rho$ and $|f| \le M$ there, then $\|f - p_n\|_\infty \le \dfrac{4M\rho^{-n}}{\rho - 1}$ (Theorem 8.2).
- *Smooth $f$, derivative form.* If $f \in C^{n+1}[-1, 1]$, then $|f(x) - p_n(x)| \le \|f^{(n+1)}\|_\infty \|\omega\|_\infty/(n + 1)!$ with $\|\omega\|_\infty = 2^{1-n}$ for these points ([interpolation error theorem](/polynomial-interpolation-error-theorem/)).

**Limits (proved).** No interpolation scheme converges for every continuous function: for any triangular array of nodes there is a continuous $f$ whose interpolants do not converge uniformly (Faber, 1914). So the Lipschitz or bounded-variation hypotheses above cannot simply be dropped; for merely continuous $f$, Chebyshev interpolation still converges whenever $E_n(f)\log n \to 0$ (Dini-Lipschitz functions, by the near-best bound).

## Complexity

- **Samples.** $n + 1$ evaluations of $f$, usually the dominant cost.
- **Coefficients.** The direct DCT of lines L2 and L3 costs about $2(n + 1)^2$ operations; an FFT-based DCT-I costs $O(n \log n)$. In the adaptive loop with doubling, the total over all stages is within a constant factor of the last stage.
- **Evaluation.** Line L4 costs 4 operations, forming $2x$ costs 1, line L5 costs 3 per step and line L6 costs 3: $3n + 8$ operations per point, and $O(n)$ space for the coefficients.
- **Barycentric alternative.** About $5n$ operations per point from the samples directly, with no setup.

**Rounding.** The DCT is a sum of terms bounded by $\max|v_j|$, so the computed coefficients have absolute errors of order $u\max|f|$ (times a slowly growing factor for the direct sum; [`fsum`](/floating-point-model/) in the implementation keeps it small). Clenshaw's recurrence and the barycentric formula are both accurate to a modest multiple of $u\sum|c_k|$ and $u\Lambda_n\max|f|$ respectively in practice; for the barycentric formula with Chebyshev points this is proved (Higham 2004). In contrast, converting $p_n$ to the monomial basis is unstable: the monomial coefficients of $T_n$ have size up to roughly $(1 + \sqrt2)^n$ while $|T_n| \le 1$ on the interval, so the monomial sum cancels massively and loses about $0.38n$ decimal digits.

## Properties

- **Near-best.** Within the factor $1 + \Lambda_n = O(\log n)$ of the best approximation for every $f$; in practice, for analytic $f$, within a factor of about 2 of the truncated series.
- **Spectral accuracy.** Geometric convergence for analytic $f$, faster than any power of $n$ for $C^\infty$ functions.
- **Exact on polynomials of degree at most $n$.**
- **Nested points.** The points for $n$ are a subset of those for $2n$.
- **Linear in $f$**, and the coefficients come from a fast transform.
- **Self-diagnosing.** The decay of $|c_k|$ shows how well $f$ is resolved.

## Variants and improvements

- **First-kind points** $\cos((j + \frac12)\pi/(n + 1))$, the zeros of $T_{n+1}$: the coefficients come from a DCT-II, $\|\omega\| = 2^{-n}$ is the smallest possible for monic $\omega$, but the points do not include $\pm1$ and are not nested under doubling.
- **Barycentric evaluation** from the samples, with no coefficients ([barycentric interpolation](/barycentric-interpolation/)).
- **Piecewise Chebyshev interpolation.** Split $[a, b]$ at singularities or where $f$ varies rapidly, as Chebfun does with "splitting on".
- **Calculus on the coefficients.** Differentiate and integrate term by term; [Clenshaw-Curtis quadrature](/clenshaw-curtis-quadrature/) integrates $p_n$ exactly; roots come from the eigenvalues of the colleague matrix.
- **[Chebyshev economization](/chebyshev-economization/)** lowers the degree of a given polynomial by truncating its Chebyshev expansion.
- **Best approximation.** If the last factor of 2 matters, the [Remez algorithm](/remez-algorithm/) improves $p_n$ to the minimax polynomial.

## When to use it

Use Chebyshev interpolation whenever you may choose where to sample a smooth function on an interval and want a polynomial approximation: for function evaluation, quadrature, root finding, spectral methods and as a general-purpose representation. It is the default choice over equispaced interpolation, Taylor series and least-squares fits of high degree. When the data come at fixed equispaced points, use splines, least squares of modest degree or rational methods instead. When $f$ has singularities, split the interval there, or use rational approximation, which converges much faster near singularities.

## Pitfalls

- **Not mapping the interval.** The points and bounds are for $[-1, 1]$; forgetting the affine map L4 gives wrong values outside the reference interval.
- **Monomial coefficients.** Converting to $\sum b_k x^k$ loses accuracy rapidly with $n$; keep the Chebyshev basis.
- **Computing points as $\cos(j\pi/n)$ naively.** This works, but the sine form is exactly symmetric and slightly more accurate near $\pm1$.
- **Chopping too early.** A single small coefficient (for example for an odd or even function, where every other coefficient vanishes) is not evidence of convergence; look at several trailing coefficients.
- **Noise in $f$.** If $f$ is only accurate to $\epsilon$, coefficients plateau at about $\epsilon$; asking for a smaller tolerance makes the adaptive loop run to its maximum degree.
- **Extrapolation.** Outside $[a, b]$ the interpolant grows like $|T_n|$, which is exponential in $n$; never evaluate far outside.

## Implementations

## History

Chebyshev introduced his polynomials in 1854 in work on best approximation. Bernstein showed (1912 to 1918) that interpolation in the zeros of $T_{n+1}$ converges for much wider classes of functions than equispaced interpolation, and Faber (1914) proved that no fixed node scheme works for all continuous functions. Cornelius Lanczos (1938) promoted expansions in Chebyshev polynomials computed from samples as a practical tool, and Clenshaw (1955) gave the stable summation recurrence; Clenshaw and Curtis (1960) built quadrature on it. Fox and Parker's 1968 book made Chebyshev methods standard. Salzer (1972) gave the simple barycentric weights for Chebyshev points, and Higham (2004) proved the stability of barycentric evaluation. Battles and Trefethen's Chebfun (2004) made adaptive Chebyshev interpolation to machine precision a general-purpose tool, and Trefethen's book (2013, extended 2019) is the standard account.

## References
