---
tag: MK9GM6
kind: algorithm
slug: fejer-quadrature
name: Fejér quadrature
aliases:
- Fejér's first rule
- Fejér's second rule
- Fejér rule
- Fejer quadrature
area: numerical/quadrature
level: advanced
summary: "Interpolatory rules on the Chebyshev zeros (first rule) or the interior Chebyshev extreme points (second rule), computed by an FFT. Open, positive weights, nearly as accurate as Gauss."
solves: [numerical-integration]
model: floating-point-model
complexity:
  vars: {n: "the number of nodes"}
  time: {worst: "O(n log n)"}
  space: {extra: Θ(n)}
  evaluations: {worst: "n"}
properties: {deterministic: true, open: true, nested: "second rule under N to 2N, first rule under n to 3n", degree_of_precision: "n-1, or n for odd n", positive_weights: true, interpolatory: true}
history:
  year: 1933
  people: [Lipót Fejér, Jörg Waldvogel, Lloyd N. Trefethen]
  note: Fejér (1933) introduced interpolatory quadrature on the Chebyshev zeros and on the interior extreme points and proved that their weights are positive. Waldvogel (2006) computed the weights of both rules with one FFT.
prereqs: [interpolatory-quadrature, chebyshev-polynomials]
see_also: [clenshaw-curtis-quadrature, gauss-legendre-quadrature, improper-integration, midpoint-rule, fast-fourier-transform, discrete-cosine-transform, tanh-sinh-quadrature, quadrature-error]
sources:
  - paper: "Lipót Fejér, Mechanische Quadraturen mit positiven Cotesschen Zahlen, Mathematische Zeitschrift 37 (1933) 287-309"
    locator: the two rules on Chebyshev points and the positivity of their weights
  - paper: "Jörg Waldvogel, Fast construction of the Fejér and Clenshaw-Curtis quadrature rules, BIT Numerical Mathematics 46 (2006) 195-202"
    locator: the weights of both Fejér rules and of Clenshaw-Curtis by one inverse FFT
  - paper: doi:10.1137/060659831
    title: "Lloyd N. Trefethen, Is Gauss quadrature better than Clenshaw-Curtis?, SIAM Review 50(1) (2008) 67-87"
    locator: convergence of Clenshaw-Curtis and Fejér rules compared with Gauss quadrature
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 2, interpolatory rules on Chebyshev points
  - book: "Lloyd N. Trefethen, Approximation Theory and Approximation Practice, Extended Edition, SIAM, 2019"
    locator: Chapter 19 (Clenshaw-Curtis and Fejér quadrature, and the comparison with Gauss)
---

Fejér's rules integrate the polynomial interpolant of $f$ on Chebyshev-type points exactly. The *first rule* uses the $n$ Chebyshev zeros $\cos\frac{(j + 1/2)\pi}{n}$; the *second rule* uses the $n$ interior Chebyshev extreme points $\cos\frac{j\pi}{n + 1}$, the [Clenshaw-Curtis](/clenshaw-curtis-quadrature/) nodes without the two endpoints. Both are *open*: they never evaluate $f$ at $a$ or $b$, so they apply directly to integrands such as $x^{-1/2}$ and $\log x$ that are infinite at an endpoint. Both have positive weights, degree $n - 1$ ($n$ for odd $n$), and errors close to those of Gauss-Legendre for smooth $f$. An FFT of length $2n$ or $2(n + 1)$ computes either rule in $O(n\log n)$ operations, and the second rule is nested under doubling.

## In plain words

These rules estimate an integral by sampling the function at points that bunch up toward the ends of the interval, without ever touching the ends themselves, fitting the smooth curve through the samples and integrating that curve. Avoiding the end points matters when the function blows up there, as many physically meaningful integrands do. Bunching the points toward the ends keeps the fitted curve well behaved. The second rule has a further convenience: doubling its number of points keeps all the old ones, so the answer can be refined until two successive answers agree.

## The problem

**Notation.** As on all quadrature pages: $I(f) = \int_a^b f(x)\,dx$ (weight $w = 1$); $Q_n(f) = \sum_i w_i f(x_i)$, where $n$ counts nodes; $E_n = I - Q_n$; $d$ is the [degree of precision](/degree-of-precision/). On $[a, b]$ the nodes are $c + h x_j$ with $c = \frac{a + b}{2}$ and $h = \frac{b - a}{2}$. For the second rule $N = n + 1$. The doubling driver stops at the tolerance $\tau$.

Given $f$, $[a, b]$, $n \ge 1$ and the kind, return $Q_n(f) = h\int_{-1}^1 p$, where $p$ is the polynomial of degree at most $n - 1$ interpolating $f(c + h x)$ at the nodes:

| | nodes $x_j = \cos\theta_j$ | weights |
|---|---|---|
| first rule | $\theta_j = \frac{(j + 1/2)\pi}{n}$, $j = 0, \ldots, n - 1$ | $\frac2n\bigl(1 - 2\sum_{l=1}^{\lfloor n/2\rfloor}\frac{\cos 2l\theta_j}{4l^2 - 1}\bigr)$ |
| second rule | $\theta_j = \frac{j\pi}{N}$, $j = 1, \ldots, n$ | $\frac{4\sin\theta_j}{N}\sum_{l=1}^{\lfloor N/2\rfloor}\frac{\sin(2l - 1)\theta_j}{2l - 1}$ |

## The algorithm

```pseudo id=main
FEJER(f, a, b, n, kind)
L1  if n < 1 or kind ∉ {1, 2} then error; if a = b then return 0
L2  θ_j ← (j + 1/2)π/n for j = 0..n−1 (kind 1), or θ_j ← jπ/N with N = n + 1 for j = 1..n (kind 2)
L3  f_j ← f(c + h cos θ_j)
L4  kind 1: a_k ← Re(e^(−ikπ/(2n)) Y_k)/n with Y = FFT(f_0..f_(n−1), f_(n−1)..f_0); halve a_0       ▷ DCT-II
L5  kind 2: s_j ← f_j sin θ_j; β_k ← −Im G_k / N with G = FFT(0, s_1..s_n, 0, −s_n..−s_1)         ▷ DST-I
L6  Q ← Σ over even k of a_k · 2/(1 − k^2) (kind 1), or Σ over odd k of β_k · 2/k (kind 2)
L7  return h · Q
```

For the first rule, $p = \sum_{k<n}a_kT_k$ and $\int_{-1}^1 T_k = \frac{2}{1 - k^2}$ for even $k$. For the second, the substitution $x = \cos\theta$ turns $\int p\,dx$ into $\int_0^\pi p(\cos\theta)\sin\theta\,d\theta$, and $p(\cos\theta)\sin\theta = \sum_{k=1}^{n}\beta_k\sin k\theta$ is a sine polynomial whose coefficients a discrete sine transform recovers from the samples; $\int_0^\pi\sin k\theta\,d\theta = \frac2k$ for odd $k$. The FFT is radix-2, with Bluestein's method for other lengths. The doubling driver uses the second rule with $n = 7, 15, 31, \ldots$, reusing all values, and stops when two successive results differ by at most $\tau$.

## Example

Take $n = 3$.

**Second rule.** $N = 4$, nodes $\cos\frac\pi4, \cos\frac\pi2, \cos\frac{3\pi}4 = \frac{1}{\sqrt2}, 0, -\frac{1}{\sqrt2}$. At $\theta = \frac\pi4$ the weight is $\sin\frac\pi4\,(\sin\frac\pi4 + \frac13\sin\frac{3\pi}4) = \frac12\cdot\frac43 = \frac23$; at $\theta = \frac\pi2$ it is $1 - \frac13 = \frac23$. All three weights are $\frac23$: this is Chebyshev's equal-weight rule for three points. It integrates $1, x, x^2, x^3$ exactly, and $E_3(x^4) = \frac25 - 2\cdot\frac23\cdot\frac14 = \frac{1}{15}$.

**First rule.** Nodes $\pm\frac{\sqrt3}{2}$, $0$, weights $\frac49, \frac{10}9, \frac49$. It is exact through degree 3, and $E_3(x^4) = \frac25 - 2\cdot\frac49\cdot\frac9{16} = -\frac1{10}$. In general the first rule errs low and the second high on $x^{d+1}$ (tested for $2 \le n \le 33$); the first rule's error is about $\frac{1}{16}$ of the second's at $n = 33$.

Measured errors, first rule / second rule:

| integral | $n = 16$ | $n = 64$ | $n = 256$ |
|---|---|---|---|
| $\int_{-1}^1\frac{dx}{1 + 25x^2}$ | $2.1 \times 10^{-3}$ / $1.8 \times 10^{-3}$ | $1.0 \times 10^{-10}$ / $5.9 \times 10^{-9}$ | rounding |
| $\int_0^1\sqrt x\,dx$ | $1.4 \times 10^{-5}$ / $5.9 \times 10^{-5}$ | $2.1 \times 10^{-7}$ / $1.0 \times 10^{-6}$ | $3.3 \times 10^{-9}$ / $1.7 \times 10^{-8}$ |
| $\int_0^1\log x\,dx$ | $2.3 \times 10^{-4}$ / $4.2 \times 10^{-3}$ | $1.4 \times 10^{-5}$ / $2.9 \times 10^{-4}$ | $8.6 \times 10^{-7}$ / $1.8 \times 10^{-5}$ |
| $\int_0^1 x^{-1/2}dx$ | $2.2 \times 10^{-2}$ / $7.0 \times 10^{-2}$ | $5.4 \times 10^{-3}$ / $1.8 \times 10^{-2}$ | $1.3 \times 10^{-3}$ / $4.6 \times 10^{-3}$ |
| $\int_0^1\cos 100x\,dx$ | $0.24$ / $1.5 \times 10^{-2}$ | $1.9 \times 10^{-8}$ / $7.4 \times 10^{-7}$ | rounding |

The endpoint singularities converge algebraically: like $N^{-3}$ for $\sqrt x$, about $N^{-2}$ for $\log x$, and $N^{-1}$ for $x^{-1/2}$ (measured ratios per doubling $8$, $4$, $2$). $e^x$ on $[0, 1]$ is exact to rounding at $n = 16$. The doubling driver at $\tau = 10^{-10}$ uses 31 evaluations for $e^x$, 255 for the Runge function and 4095 for $\sqrt x$; for $x^{-1/2}$ and $\log x$ it runs out of its budget.

## Correctness

At the first rule's nodes the cosines $\cos k\theta_j$, $k < n$, are discrete orthogonal; at the second rule's nodes the sines $\sin k\theta_j$, $1 \le k \le n$, are. So the coefficients of the interpolant are cosine or sine sums of the samples, and the FFT of the even (respectively odd) extension computes exactly those sums. Integrating the basis functions exactly gives $\int p$, so each rule has degree at least $n - 1$, and symmetry adds one for odd $n$. Substituting the coefficient formulas gives the explicit weights. For the first rule a telescoping sum shows they are positive; for the second, $\sum_l\frac{\sin(2l - 1)\theta}{2l - 1}$ is positive on $(0, \pi)$ because its derivative $\frac{\sin 2L\theta}{2\sin\theta}$ has alternating lobes of decreasing size. The details are in [the correctness proof](proofs/correctness.md).

**Error.** Proved here: exactness and positivity, which give convergence for every continuous $f$ and a rounding bound of $2\lvert h\rvert\delta$ for sample errors $\delta$. Cited: for $f$ analytic in a Bernstein ellipse $E_\rho$ the error decays like $\rho^{-n}$, as for Clenshaw-Curtis (Trefethen 2008; ATAP Chapter 19), and in practice often near the Gauss rate $\rho^{-2n}$ for moderate $n$. Measured: the algebraic rates for endpoint singularities above.

## Complexity

- **Evaluations.** $n$, all interior.
- **Operations.** One FFT of length $2n$ (first rule) or $2(n + 1)$ (second rule): $O(n\log n)$. The explicit weight formulas cost $O(n^2)$.
- **Nesting.** Second rule: from $N$ to $2N$, the $N - 1$ old values are reused and $N$ are new. First rule: the nodes for $n$ are among those for $3n$, so tripling reuses a third.
- **Space.** $\Theta(n)$.

## Properties

- **Degree** $n - 1$ for even $n$, $n$ for odd $n$; interpolatory.
- **Open.** Nodes in $(-1, 1)$; the second rule's extreme nodes are $\pm\cos\frac{\pi}{n + 1}$, at distance about $\frac{\pi^2}{2(n + 1)^2}$ from the ends.
- **Positive weights** for both rules and all $n$ (Fejér 1933).
- **Small cases.** $n = 1$ is the [midpoint rule](/midpoint-rule/) for both; the second rule with $n = 3$ is Chebyshev's equal-weight rule.
- **Relation to Clenshaw-Curtis.** Clenshaw-Curtis is the closed counterpart on the same extreme points; the second Fejér rule drops the endpoints and integrates a polynomial of lower degree through the interior values.
- **Relation to Gauss-Chebyshev.** The first rule uses the Gauss-Chebyshev nodes, but with weights for $w = 1$ instead of $w = (1 - x^2)^{-1/2}$.

## Variants and improvements

- **Waldvogel's weights.** One inverse FFT of a vector of moments produces the weights of either Fejér rule or Clenshaw-Curtis, which is what libraries do when the weights are needed.
- **Substitution plus Fejér.** For $x^{-1/2}$ or $\log x$, a substitution such as $x = t^2$ removes the singularity and restores geometric convergence; the open rule is a safe default, not a fast one.
- **Weighted versions.** Integrating Chebyshev polynomials against $\log x$, $x^\alpha$ or $\cos\omega x$ gives product rules on the same nodes; see [product quadrature](/product-quadrature/).
- **Sparse grids.** Nested Fejér-2 rules serve as one-dimensional rules in [sparse grids](/sparse-grid-quadrature/) when the endpoints should be avoided.

## When to use it

Use a Fejér rule for smooth or mildly singular integrands on a finite interval when the endpoints must not be evaluated: infinite endpoint values, integrals after a map of an infinite interval onto $(-1, 1)$, functions that are undefined at the boundary. Prefer the second rule when you want nesting, the first when you want slightly smaller errors at a fixed $n$. For strong endpoint singularities, [tanh-sinh](/tanh-sinh-quadrature/) or [Gauss-Jacobi](/gauss-jacobi-quadrature/) converge much faster; for interior kinks use an [adaptive](/adaptive-quadrature/) method.

## Pitfalls

- **Open does not mean fast.** $x^{-1/2}$ still converges only like $N^{-1}$: 255 nodes give about 3 digits. Remove the singularity by a substitution or use a rule designed for it.
- **Nodes very close to the ends.** At $n = 2^{16}$ the outermost node is about $10^{-9}$ from the endpoint; a singular integrand evaluated there is large but finite, which is fine, but an integrand that overflows near the end is not.
- **Indexing conventions.** Some texts index the second rule by $N = n + 1$, others the first rule by its degree; check which before comparing tables.
- **The doubling estimate is heuristic.** $\lvert Q_{2N} - Q_N\rvert$ estimates the error of the coarser rule. For slowly convergent integrands it may never fall below $\tau$, and the driver then reports "limit".
- **Not exactly symmetric nodes from cosines.** $\cos(j\pi/N)$ and $-\cos((N - j)\pi/N)$ can differ in the last bit; the code uses the sine form, which is exactly antisymmetric.

## Implementations

## History

Lipót Fejér published both rules in 1933, in a paper on quadrature formulas with positive Cotes numbers. He showed that interpolatory rules on the Chebyshev zeros and on the interior extreme points have positive weights, so that by Pólya's theorem they converge for every continuous function. The closed variant on the extreme points was proposed by Clenshaw and Curtis in 1960 and became better known. Interest in Fejér's rules returned with Trefethen's comparison of Clenshaw-Curtis and Gauss quadrature (2008) and Waldvogel's FFT construction of their weights (2006).

## References
