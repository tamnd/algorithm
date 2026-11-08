---
tag: AP29J0
kind: algorithm
slug: clenshaw-curtis-quadrature
name: Clenshaw-Curtis quadrature
aliases:
- Clenshaw-Curtis rule
- Chebyshev quadrature on extreme points
- Curtis-Clenshaw quadrature
area: numerical/quadrature
level: advanced
summary: "Integrate the polynomial interpolant at the Chebyshev extreme points exactly, with its coefficients from an FFT. Nested, positive weights, and nearly as accurate as Gauss for most integrands."
solves: [numerical-integration]
model: floating-point-model
complexity:
  vars: {n: "the number of nodes"}
  time: {worst: "O(n log n)"}
  space: {extra: Θ(n)}
  evaluations: {worst: "n"}
properties: {deterministic: true, nested: true, degree_of_precision: "n-1, or n for odd n", positive_weights: true, endpoints_evaluated: true, interpolatory: true}
history:
  year: 1960
  people: [Charles W. Clenshaw, Alan R. Curtis, Lipót Fejér, W. Morven Gentleman, Lloyd N. Trefethen]
  note: Fejér (1933) studied interpolatory rules on Chebyshev points. Clenshaw and Curtis (1960) proposed the rule on the extreme points with a cosine-series computation. Gentleman (1972) computed it with the FFT, and Trefethen (2008) showed it is nearly as accurate as Gauss quadrature for most integrands.
prereqs: [interpolatory-quadrature, chebyshev-polynomials]
see_also: [fejer-quadrature, gauss-legendre-quadrature, gauss-kronrod-quadrature, fast-fourier-transform, discrete-cosine-transform, newton-cotes-formulas, quadrature-error, sparse-grid-quadrature]
sources:
  - paper: doi:10.1007/BF01386223
    title: "C. W. Clenshaw and A. R. Curtis, A method for numerical integration on an automatic computer, Numerische Mathematik 2 (1960) 197-205"
    locator: the rule on the Chebyshev extreme points and its cosine-series evaluation
  - book: "Lloyd N. Trefethen, Approximation Theory and Approximation Practice, Extended Edition, SIAM, 2019"
    locator: Chapter 19, Clenshaw-Curtis and Gauss quadrature (Theorem 19.3 for analytic integrands)
  - paper: doi:10.1137/060659831
    title: "Lloyd N. Trefethen, Is Gauss quadrature better than Clenshaw-Curtis?, SIAM Review 50(1) (2008) 67-87"
    locator: the comparison with Gauss quadrature and the factor of two in convergence rates
  - paper: "J. A. C. Weideman and L. N. Trefethen, The kink phenomenon in Fejér and Clenshaw-Curtis quadrature, Numerische Mathematik 107 (2007) 707-727"
    locator: the change of convergence rate from about rho^(-2N) to rho^(-N)
  - paper: "Jörg Waldvogel, Fast construction of the Fejér and Clenshaw-Curtis quadrature rules, BIT Numerical Mathematics 46 (2006) 195-202"
    locator: the weights of Clenshaw-Curtis and both Fejér rules by one FFT
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 2, interpolatory rules on Chebyshev points (Fejér and Clenshaw-Curtis)
---

Clenshaw-Curtis quadrature samples $f$ at the $n$ Chebyshev extreme points $x_j = \cos(j\pi/N)$, $N = n - 1$, interpolates by a polynomial of degree $N$, and integrates the interpolant exactly. The Chebyshev coefficients of the interpolant come from one FFT of length $2N$, and $\int_{-1}^1 T_k = \frac{2}{1 - k^2}$ for even $k$, so the whole rule costs $n$ evaluations and $O(n\log n)$ operations, with no precomputed table. Its degree is only $N$ ($N + 1$ for even $N$), about half that of the [Gauss-Legendre](/gauss-legendre-quadrature/) rule with the same number of nodes, yet for most integrands it is almost as accurate: for $f$ analytic in a Bernstein ellipse the error falls geometrically, and in practice usually at close to the Gauss rate. The weights are positive, the rules for $N$ and $2N$ are nested, and the nodes include the endpoints.

## In plain words

To integrate a function, sample it at points crowded toward the two ends of the interval, fit the one smooth polynomial curve that passes through all the samples, and integrate that curve exactly. Crowding the points toward the ends is what makes such a fit reliable; evenly spaced points can make the curve swing wildly. The fit and its integral come out of a fast Fourier transform, so even millions of samples are cheap. Doubling the number of points keeps every old point, which gives a natural way to check the answer: compare the old and new results, and stop when they agree.

## The problem

**Notation.** As on all quadrature pages: $I(f) = \int_a^b f(x)\,dx$ (weight $w = 1$); $Q_n(f) = \sum_i w_i f(x_i)$, where $n$ counts nodes; $E_n = I - Q_n$; $d$ is the [degree of precision](/degree-of-precision/). Here $N = n - 1$ is the degree of the interpolant, $T_k(\cos\theta) = \cos k\theta$ is the Chebyshev polynomial, and on $[a, b]$ the nodes are $c + h x_j$ with $c = \frac{a + b}{2}$, $h = \frac{b - a}{2}$. The doubling driver stops at the tolerance $\tau$.

Given $f$, $[a, b]$ and $n \ge 2$, compute $Q_n(f) = h\int_{-1}^1 p$, where $p$ is the polynomial of degree at most $N$ with $p(x_j) = f(c + h x_j)$ for $j = 0, \ldots, N$.

## The algorithm

```pseudo id=main
CLENSHAW-CURTIS(f, a, b, n)
L1  if n < 2 then error; if a = b then return 0
L2  N ← n − 1; c ← (a + b)/2; h ← (b − a)/2; f_j ← f(c + h cos(jπ/N)) for j = 0..N
L3  g ← (f_0, f_1, …, f_N, f_(N−1), …, f_1)            ▷ even extension, length 2N
L4  G ← FFT(g); a_k ← G_k / N for k = 0..N            ▷ G is real
L5  a_0 ← a_0/2; a_N ← a_N/2                          ▷ now p = Σ a_k T_k
L6  Q ← Σ over even k ≤ N of a_k · 2/(1 − k^2)
L7  return h · Q
```

Lines L3 to L5 are a type-I discrete cosine transform: the discrete orthogonality of $\cos(jk\pi/N)$ over the extreme points turns interpolation into a cosine sum. Line L6 integrates each $T_k$ exactly. The nodes are computed as $\sin(\pi(N - 2j)/(2N))$, which equals $\cos(j\pi/N)$ but is exactly antisymmetric in floating point. The FFT is radix-2 for powers of two, and Bluestein's chirp transform for other lengths, so every $n$ costs $O(n\log n)$.

The weights, if wanted, are the same transform applied to the moments: $w_j = \frac{c_j}{N}\bigl(1 - \sum_{l=1}^{\lfloor N/2\rfloor}\frac{b_l}{4l^2 - 1}\cos\frac{2lj\pi}{N}\bigr)$, with $c_j = 1$ at the ends and $2$ inside, $b_l = 1$ if $2l = N$ and $2$ otherwise. The doubling driver evaluates $Q$ at $N = 8, 16, 32, \ldots$, reusing all old values, and stops when two successive results differ by at most $\tau$.

## Example

Take $n = 5$, so $N = 4$ and the nodes are $\pm1$, $\pm\frac{1}{\sqrt2}$, $0$. The weight formula gives

$$w_0 = \tfrac14\bigl(1 - \tfrac23 - \tfrac1{15}\bigr) = \tfrac1{15}, \qquad w_1 = \tfrac24\bigl(1 + \tfrac1{15}\bigr) = \tfrac8{15}, \qquad w_2 = \tfrac24\bigl(1 + \tfrac23 - \tfrac1{15}\bigr) = \tfrac45,$$

summing to $2$. The rule is exact through degree $5 = N + 1$ (even $N$); on $x^6$ it gives $2\cdot\frac1{15} + 2\cdot\frac8{15}\cdot\frac18 = \frac{4}{15}$, so $E_5(x^6) = \frac27 - \frac4{15} = \frac{2}{105}$. For comparison, Boole's rule (the 5-point [Newton-Cotes](/newton-cotes-formulas/) rule) also has degree 5; the difference shows for larger $n$, where Newton-Cotes weights turn negative (at 9 nodes and from 11 nodes on) while Clenshaw-Curtis weights stay positive. On $\int_0^1 e^x\,dx$, $n = 5$ is off by $3.4 \times 10^{-7}$, $n = 9$ by $1.6 \times 10^{-14}$, and $n = 17$ is exact to rounding.

For odd $N$ the degree is exactly $N$, and $E_n(x^{N+1}) = \frac{2^{3-N}}{N(N^2 - 4)}$ for $N \ge 3$ (for example $\frac1{15}$ at $N = 3$).

Measured against [Gauss-Legendre](/gauss-legendre-quadrature/) with the same number $n$ of nodes (absolute errors):

| integral | $n$ | 9 | 17 | 33 | 65 |
|---|---|---|---|---|---|
| $\int_{-1}^1\frac{dx}{1 + 25x^2}$ | CC | $5.5 \times 10^{-2}$ | $2.2 \times 10^{-3}$ | $3.9 \times 10^{-6}$ | $2.9 \times 10^{-11}$ |
| | Gauss | $2.9 \times 10^{-2}$ | $1.2 \times 10^{-3}$ | $2.1 \times 10^{-6}$ | $6.2 \times 10^{-12}$ |
| $\int_0^1\sqrt x\,dx$ | CC | $2.2 \times 10^{-4}$ | $2.7 \times 10^{-5}$ | $3.3 \times 10^{-6}$ | $4.1 \times 10^{-7}$ |
| | Gauss | $1.2 \times 10^{-4}$ | $1.9 \times 10^{-5}$ | $2.7 \times 10^{-6}$ | $3.7 \times 10^{-7}$ |
| $\int_0^1\lvert x - \frac13\rvert dx$ | CC | $1.5 \times 10^{-3}$ | $2.8 \times 10^{-4}$ | $1.7 \times 10^{-4}$ | $5.1 \times 10^{-5}$ |
| | Gauss | $3.4 \times 10^{-3}$ | $5.0 \times 10^{-4}$ | $1.3 \times 10^{-4}$ | $4.5 \times 10^{-5}$ |
| $\int_0^1\cos 100x\,dx$ | CC | $0.27$ | $0.25$ | $2.1 \times 10^{-4}$ | $5.5 \times 10^{-10}$ |
| | Gauss | $3.7 \times 10^{-2}$ | $0.20$ | $2.4 \times 10^{-5}$ | $4.8 \times 10^{-17}$ |

On the Runge function both rules gain a factor of about $\rho^2 = 1.49$ per node, $\rho = (1 + \sqrt{26})/5$ being the parameter of the largest ellipse free of poles; the proved Clenshaw-Curtis bound only guarantees $\rho$ per node. For $\sqrt x$ both converge like $N^{-3}$ (the ratio per doubling is $8.0$), and for the kink both like roughly $N^{-2}$, irregularly. For $e^{\cos x}$ on $[0, 2\pi]$ the error at $n = 33$ is $7 \times 10^{-15}$. The doubling driver uses 17 evaluations for $e^x$, 257 for the Runge function and 2049 for $\sqrt x$ at $\tau = 10^{-10}$.

## Correctness

The values $\cos(jk\pi/N)$, $j = 0, \ldots, N$, are orthogonal under the sum that halves the end terms, so the coefficients of the interpolant are a cosine sum of the samples. The FFT of the even extension computes exactly that sum. Since $\int_{-1}^1 T_k = \frac{2}{1 - k^2}$ for even $k$ and $0$ for odd $k$, line L6 returns the integral of the interpolant, and the rule is exact for polynomials of degree at most $N$; symmetry adds one degree for even $N$. Substituting the coefficient formula gives the explicit weights, and a telescoping sum shows $w_j \ge \frac{c_j}{N(2\lfloor N/2\rfloor + 1)} > 0$. The details are in [the correctness proof](proofs/correctness.md).

**Error (proved, cited).** If $f$ is analytic and bounded by $M$ in the open Bernstein ellipse $E_\rho$ (foci $\pm 1$, semi-axes summing to $\rho > 1$), then for $N \ge 2$ (Trefethen, ATAP Theorem 19.3)

$$\lvert E_n(f)\rvert \le \frac{64}{15}\,\frac{M\rho^{1-N}}{\rho^2 - 1}.$$

The Gauss rule with $n$ nodes has the bound with $\rho^{-2n}$. In practice Clenshaw-Curtis often converges at nearly the Gauss rate until the error is very small, then switches to the $\rho^{-N}$ rate (the kink phenomenon; observed, explained by Weideman and Trefethen 2007). If $f^{(\nu-1)}$ is absolutely continuous and $f^{(\nu)}$ has bounded variation, the error is $O(N^{-\nu})$ for both rules (ATAP Theorem 19.4); observed rates are often higher: $N^{-3}$ for $\sqrt x$ at an endpoint and about $N^{-2}$ for the kink $\lvert x - \frac13\rvert$.

**Rounding.** The weights are positive and sum to $2$, so errors of size $\delta$ in the samples change $Q$ by at most $2\lvert h\rvert\delta$; the FFT adds $O(\epsilon\log n)$ relative error in the coefficients.

## Complexity

- **Evaluations.** $n$, including both endpoints. Doubling from $N$ to $2N$ costs only the $N$ new values.
- **Operations.** One FFT of length $2N$: $O(n\log n)$; Bluestein's method for lengths that are not powers of two costs three power-of-two FFTs. In pure Python, $n = 2^{16} + 1$ takes about $0.5$ seconds, against $O(n^2)$ for the explicit weight formula.
- **No table.** Unlike Gauss rules, which need nodes and weights (computed by [Golub-Welsch](/golub-welsch-algorithm/) or Newton's method), the transform works directly on the samples.
- **Space.** $\Theta(n)$.

## Properties

- **Degree** $N$ for odd $N$, $N + 1$ for even $N$; interpolatory.
- **Positive weights** for all $n$ (Imhof 1963), with $w_0 = \frac{1}{N^2 - 1}$ ($N$ even) or $\frac{1}{N^2}$ ($N$ odd) at the endpoints.
- **Nested.** The $(N + 1)$-point nodes are every other node of the $(2N + 1)$-point rule.
- **Closed.** The endpoints are nodes; $f$ must be finite there.
- **Small cases.** $n = 2$ is the trapezoidal rule and $n = 3$ is [Simpson's rule](/simpsons-rule/).
- **Convergence for every continuous $f$**, by positivity and the Weierstrass theorem (Pólya's criterion).

## Variants and improvements

- **Fejér's rules.** Use the Chebyshev zeros (first rule) or the interior extreme points (second rule); both are open, so endpoint singularities are never evaluated. See [Fejér quadrature](/fejer-quadrature/).
- **Weights by FFT.** Waldvogel (2006) computes the weights of Clenshaw-Curtis and both Fejér rules with one inverse FFT; this page does the same with the moments as input.
- **Chebyshev-tail stopping.** Instead of comparing $Q_N$ and $Q_{2N}$, stop when the last Chebyshev coefficients fall below $\tau$ (as in Chebfun); this estimates the error of $Q_{2N}$ itself, again heuristically.
- **Sparse grids.** Nestedness makes Clenshaw-Curtis the standard one-dimensional rule in Smolyak [sparse grids](/sparse-grid-quadrature/).
- **Weighted and oscillatory versions.** Integrating $T_k$ against a weight, such as $\cos\omega x$ or $\log x$, gives modified Clenshaw-Curtis rules; QUADPACK's QAWO and QAWS use them.

## When to use it

Use Clenshaw-Curtis when $f$ is smooth on a finite interval and you want nested rules, many nodes, or no node tables: automatic non-adaptive integration by doubling, Chebyshev-based solvers, sparse grids. It is as good as Gauss for practical purposes on most smooth integrands. Prefer [Gauss-Legendre](/gauss-legendre-quadrature/) when every evaluation is very expensive and $f$ is analytic in a large region, [Fejér's second rule](/fejer-quadrature/) or [tanh-sinh](/tanh-sinh-quadrature/) when $f$ is singular at an endpoint, the [trapezoidal rule](/trapezoidal-rule/) for periodic integrands, and an [adaptive](/adaptive-quadrature/) method for kinks and jumps.

## Pitfalls

- **Endpoint singularities.** $x^{-1/2}$ and $\log x$ on $[0, 1]$ are evaluated at $0$: Python raises an exception, and other languages return $\infty$ or NaN. Use an open rule or a substitution.
- **Kinks and jumps.** A single global interpolant converges only algebraically: errors near $5 \times 10^{-5}$ at $n = 65$ for $\lvert x - \frac13\rvert$. Split at the breakpoint.
- **Oscillation.** $\cos 100x$ on $[0, 1]$ needs $N$ above about $50 = \omega(b - a)/2$ before the error drops (a heuristic, matching the measurements: $0.25$ at $n = 17$, $5.5 \times 10^{-10}$ at $n = 65$).
- **Indexing.** Here $n$ counts nodes and $N = n - 1$; many texts write "$N$-point" for the rule with $N + 1$ nodes.
- **The doubling estimate.** $\lvert Q_{2N} - Q_N\rvert$ is an estimate for $Q_N$; it is usually far larger than the error of $Q_{2N}$, so doubling stops late rather than early, but for nonsmooth $f$ it can also stop early. It is a heuristic.
- **Weights from the explicit formula** cost $O(n^2)$; use the FFT for large $n$.

## Implementations

## History

Fejér (1933) studied interpolatory quadrature on the Chebyshev points and proved positivity of the weights for his rules. Clenshaw and Curtis (1960) proposed the rule on the extreme points and computed it from a Chebyshev series of the integrand, an idea that fits automatic computers well. Imhof (1963) proved positivity of its weights, and Gentleman (1972) implemented it with the fast Fourier transform. For decades the rule was considered half as efficient as Gauss quadrature because of its lower degree, until Trefethen (2008) showed that the two have nearly the same accuracy for most integrands, and Weideman and Trefethen (2007) explained the transition in the convergence rate. Waldvogel (2006) gave the FFT construction of the weights.

## References
