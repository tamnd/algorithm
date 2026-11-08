---
tag: Q6XB94
kind: algorithm
slug: gauss-kronrod-quadrature
name: Gauss-Kronrod quadrature
aliases:
- Kronrod extension
- G7-K15 rule
- Gauss-Kronrod rule
- Kronrod rule
area: numerical/quadrature
level: advanced
summary: "Adds n + 1 nodes to an n-point Gauss rule to get a rule of degree 3n + 1 that reuses every Gauss value. The difference of the two drives a heuristic error estimate; the basis of QUADPACK."
solves: [numerical-integration]
model: floating-point-model
complexity:
  vars: {n: "the number of Gauss nodes", k: "the number of panel splits"}
  time: {worst: "O(n^3 + k(n + log k))"}
  space: {extra: "Θ(n^2 + k)"}
  evaluations: {panel: "2n + 1", adaptive: "(2k + 1)(2n + 1)"}
properties: {deterministic: true, nested: true, degree_of_precision: "3n+1, or 3n+2 for odd n", positive_weights: true, error_estimate_is_heuristic: true, endpoints_evaluated: false}
history:
  year: 1964
  people: [A. S. Kronrod, T. N. L. Patterson, Robert Piessens, Elise de Doncker-Kapenga, Dirk P. Laurie]
  note: Kronrod published the extension and tables of nodes and weights in 1964 (English translation 1965). Patterson (1968) iterated it. QUADPACK (1983) made the G7-K15 pair the standard panel rule of adaptive integration.
prereqs: [gauss-legendre-quadrature, adaptive-quadrature]
see_also: [gaussian-quadrature, gauss-quadrature-theorem, golub-welsch-algorithm, clenshaw-curtis-quadrature, interpolatory-quadrature, quadrature-error, improper-integration, romberg-integration]
sources:
  - book: isbn:9783540125532
    title: Robert Piessens, Elise de Doncker-Kapenga, Christoph W. Überhuber and David K. Kahaner, QUADPACK, A Subroutine Package for Automatic Integration, Springer Series in Computational Mathematics 1, 1983
    locator: Chapter 2 (Gauss-Kronrod rules and the local error estimate) and the routines QK15 and QAG
  - book: "A. S. Kronrod, Nodes and Weights of Quadrature Formulas, Consultants Bureau, New York, 1965"
    locator: the extension of the Gauss-Legendre rules and the tables of nodes and weights
  - paper: "T. N. L. Patterson, The optimum addition of points to quadrature formulae, Mathematics of Computation 22(104) (1968) 847-856"
    locator: the iterated extensions 3, 7, 15, 31, 63, 127, 255
  - paper: "Giovanni Monegato, Stieltjes polynomials and related quadrature rules, SIAM Review 24(2) (1982) 137-158"
    locator: survey of the zeros of Stieltjes polynomials, interlacing and positivity of the Kronrod weights
  - paper: "Dirk P. Laurie, Calculation of Gauss-Kronrod quadrature rules, Mathematics of Computation 66(219) (1997) 1133-1145"
    locator: the Kronrod rule from a modified Jacobi matrix in O(n^2) operations
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 2 (Kronrod extensions of Gauss rules) and Chapter 6 (automatic integration)
---

Gauss-Kronrod quadrature pairs an $n$-point [Gauss-Legendre](/gauss-legendre-quadrature/) rule $G_n$ with a $(2n + 1)$-point rule $K_{2n+1}$ that contains its $n$ nodes and adds $n + 1$ more. The added nodes are the zeros of the Stieltjes polynomial $E_{n+1}$, chosen so that $K_{2n+1}$ has degree $3n + 1$ ($3n + 2$ for odd $n$) instead of the $2n$ of an arbitrary interpolatory rule on $2n + 1$ points. Since the Gauss values are reused, the pair costs $2n + 1$ evaluations, not $3n + 1$, and the difference $\lvert K - G \rvert$ gives an error estimate for free. QUADPACK's G7-K15 pair, 15 evaluations per panel with degree 23, is the panel rule inside most library integrators. This page computes the rule for any $n$, with exact rational arithmetic for $E_{n+1}$, and runs the globally adaptive QUADPACK driver on it. The error estimate is a heuristic, and the page says where it fails.

## In plain words

An integrator needs two things on each piece of the interval: a good answer and an idea of how wrong it is. The usual way to get the second is to compute the answer twice, once roughly and once carefully, and compare. Gauss-Kronrod makes this cheap. It starts from a very good rule for the rough answer and adds new sample points in the gaps between the old ones, placed so that the old and new points together form an even better rule. Every function value of the rough answer is used again in the careful one. The difference between the two answers tells the integrator which pieces to split, and the pieces where it is large get refined until the total is small enough.

## The problem

**Notation.** As on all quadrature pages: $I(f) = \int_a^b f(x)\,dx$ (weight $w = 1$); $Q_n(f) = \sum_{i} w_i f(x_i)$, where $n$ counts nodes; $E_n = I - Q_n$; $d$ is the [degree of precision](/degree-of-precision/). Here $n$ is the number of *Gauss* nodes, so $K_{2n+1}$ has $2n + 1$ nodes. On $[-1, 1]$, $P_k$ is the Legendre polynomial. An adaptive method stops at the tolerance $\tau$.

Given $n \ge 1$, find $n + 1$ nodes $y$ in $(-1, 1)$ and weights such that the rule on the $2n + 1$ nodes $\{x_i^G\} \cup \{y_j\}$ has the largest possible degree. With $s(x) = P_n(x)E_{n+1}(x)$ the node polynomial, the rule has degree $2n + 1 + m - 1$ exactly when $\int s\,q = 0$ for all $q$ of degree below $m$ (the same argument as in the [Gauss quadrature theorem](/gauss-quadrature-theorem/)). So $E_{n+1}$ must satisfy

$$\int_{-1}^1 E_{n+1}(x)\,P_n(x)\,x^k\,dx = 0 \qquad (k = 0, 1, \ldots, n),$$

$n + 1$ conditions on the $n + 1$ free coefficients of a monic $E_{n+1}$, giving $m = n + 1$ and $d = 3n + 1$. Then: given $f$, $a$, $b$ and $\tau$, return an approximation of $\int_a^b f$, an estimate of its error, the number of evaluations used, and a status.

## The algorithm

```pseudo id=main
GAUSS-KRONROD-PANEL(f, a, b, n)
L1  write E = Σ c_j P_j with c_(n+1) = 1; for k = 0..n, the condition ∫ E P_n P_k = 0 fixes c_(n−k) exactly
L2  nodes y ← the n Gauss nodes and one zero of E in each of the n + 1 gaps; Kronrod weights W from Σ W_i P_k(y_i) = 2[k = 0], k ≤ 2n
L3  c ← (a + b)/2; h ← (b − a)/2; f_i ← f(c + h y_i) for all 2n + 1 nodes
L4  K ← h Σ W_i f_i; G ← h Σ g_i f_i over the Gauss nodes
L5  e ← ρ min(1, (200 |K − G| / ρ)^1.5) with ρ = |h| Σ W_i |f_i − K/(2h)|, raised to at least 50 ε |h| Σ W_i |f_i|
L6  return (K, e, G)

ADAPTIVE-GK(f, a, b, τ, n, limit)
L7  if a = b return 0; evaluate the panel [a, b]; H ← max-heap of panels by e; total ← K; errsum ← e
L8  while errsum > τ and H holds fewer than limit panels
L9      pop the panel [l, r] with the largest e; if e is at its rounding floor or [l, r] cannot be halved in floating point then stop with "roundoff"; else evaluate both halves
L10     push both halves; total ← total − K[l, r] + K[l, m] + K[m, r]; errsum likewise
L11 return (fsum of K over H, fsum of e over H, evaluations, status)
```

Line L1 is triangular because $\int P_k P_n P_j = 0$ for $j < n - k$; the triple integrals come from Adams' formula $\int_{-1}^1 P_l P_m P_j = \frac{2}{l + m + j + 1}\frac{A(s-l)A(s-m)A(s-j)}{A(s)}$, $s = \frac{l + m + j}{2}$, $A(r) = \binom{2r}{r}4^{-r}$, so the coefficients are exact rationals. Line L2 finds the Kronrod nodes by bisection between consecutive Gauss nodes (and $\pm 1$), which works because the zeros interlace; the code raises an error if some gap has no sign change. The rule depends only on $n$ and is cached, so after the first panel the cost of a panel is its $2n + 1$ evaluations.

## Example

Take $n = 2$. Line L1: condition $k = 0$ gives $c_2 = 0$, condition $k = 1$ gives $c_1 = -\frac{9}{14}$, condition $k = 2$ gives $c_0 = 0$. So

$$E_3 = P_3 - \tfrac{9}{14}P_1 = \tfrac52\bigl(x^3 - \tfrac67 x\bigr),$$

with zeros $0$ and $\pm\sqrt{6/7} = \pm 0.9258201$. They interlace with the Gauss nodes $\pm 1/\sqrt3 = \pm 0.5773503$. The weights solve a $5 \times 5$ moment system; by symmetry it reduces to two equations, with the result

| node | $0$ | $\pm 1/\sqrt3$ | $\pm\sqrt{6/7}$ |
|---|---|---|---|
| Kronrod weight $W$ | $\frac{28}{45}$ | $\frac{27}{55}$ | $\frac{98}{495}$ |
| Gauss weight $g$ | $0$ | $1$ | $0$ |

The rule is exact up to degree $3n + 1 = 7$, and $E_5(x^8) = \frac29 - K(x^8) = -\frac{8}{2205}$. For comparison, the 5-point Newton-Cotes rule has degree 5 and the 5-point Gauss rule degree 9; the Kronrod rule sits between them but shares two nodes with $G_2$.

On $\int_0^1 e^x\,dx$ with $n = 2$: $K_5$ is off by $2.9 \times 10^{-10}$, $G_2$ by $-3.9 \times 10^{-4}$, and the estimate of line L5 is $0.033$, a factor $10^8$ above the true error of $K$. With $n = 3$ ($K_7$) the extra nodes are $\pm 0.9604913$ and $\pm 0.4342437$, the zeros of $x^4 - \frac{10}{9}x^2 + \frac{155}{891}$.

Measured for G7-K15 ($n = 7$) on single panels:

| integrand | error of $K_{15}$ | error of $G_7$ | estimate $e$ |
|---|---|---|---|
| $e^x$ on $[0, 1]$ | $2.2 \times 10^{-16}$ | $-2.2 \times 10^{-16}$ | $1.9 \times 10^{-14}$ (rounding floor) |
| $e^x$ on $[0, 4]$ | $1.4 \times 10^{-14}$ | $-5.5 \times 10^{-10}$ | $5.4 \times 10^{-12}$ |
| $\frac{1}{1 + 25x^2}$ on $[-1, 1]$ | $3.3 \times 10^{-3}$ | $6.7 \times 10^{-2}$ | $0.47$ |
| $\sqrt x$ on $[0, 1]$ | $1.3 \times 10^{-5}$ | $2.5 \times 10^{-4}$ | $0.023$ |
| $\cos 30x$ on $[0, 1]$ | $-5.0 \times 10^{-6}$ | $-0.43$ | $0.70$ |

The third row is the Runge function, whose poles at $\pm i/5$ are close to the interval; one panel is far from enough, and the driver splits it. The adaptive driver with $\tau = 10^{-10}$:

| integral | value | true error | estimate | evaluations |
|---|---|---|---|---|
| $\int_0^1 e^x$ | $e - 1$ | $2.2 \times 10^{-16}$ | $1.9 \times 10^{-14}$ | 15 |
| $\int_0^{2\pi} e^{\cos x}$ | $2\pi I_0(1)$ | $0$ | $6.6 \times 10^{-12}$ | 105 |
| $\int_{-5}^5 \frac{dx}{1 + x^2}$ | $2\arctan 5$ | $0$ | $7.3 \times 10^{-13}$ | 225 |
| $\int_0^1 \lvert x - \frac13 \rvert$ | $\frac{5}{18}$ | $1.6 \times 10^{-13}$ | $3.6 \times 10^{-11}$ | 495 |
| $\int_0^1 \sqrt x$ | $\frac23$ | $3.5 \times 10^{-14}$ | $6.0 \times 10^{-11}$ | 585 |
| $\int_0^1 \cos 100x$ | $\frac{\sin 100}{100}$ | $2 \times 10^{-17}$ | $7.1 \times 10^{-15}$ | 945 |
| $\int_0^1 [x \ge 0.3]$ | $0.7$ | $8.0 \times 10^{-12}$ | $6.4 \times 10^{-11}$ | 975 |
| $\int_0^1 \log x$ | $-1$ | $2.0 \times 10^{-13}$ | $8.6 \times 10^{-11}$ | 1005 |
| $\int_0^1 x^{-1/2}$ | $2$ | $3.8 \times 10^{-12}$ | $7.7 \times 10^{-11}$ | 2025 |

On every row the estimate exceeds the true error, usually by a factor of 10 to 1000. For $\sqrt x$ the evaluations grow from 315 to 465, 585 and 705 as $\tau$ goes from $10^{-6}$ to $10^{-12}$: about 60 evaluations per digit, because each digit needs a few more bisections toward the singular endpoint.

## Correctness

The node polynomial $s = P_n E_{n+1}$ has degree $2n + 1$ and is orthogonal to every polynomial of degree at most $n$. The weights make the rule interpolatory, so it is exact on degree $2n$. For $f$ of degree at most $3n + 1$, divide $f = q s + r$ with $\deg q \le n$ and $\deg r \le 2n$; then $K(f) = K(r) = I(r) = I(f) - I(qs) = I(f)$. For odd $n$ the rule is symmetric and $3n + 2$ is odd, which gives one more degree. The solve of line L1 is triangular with positive pivots by Adams' formula, so $E_{n+1}$ exists and is unique. The real, interlacing zeros and the positive weights are cited theorems (Szegő 1935; Monegato 1978) that the code checks when it builds the rule. The driver keeps a partition of $[a, b]$ and terminates after at most `limit` $- 1$ bisections. The details are in [the correctness proof](proofs/correctness.md).

**Error (proved).** If $f \in C^{d+1}$ on a panel of width $L$, the panel error is at most $C_n L^{d+2}\max\lvert f^{(d+1)} \rvert$ with $C_n$ depending only on the rule; under bisection it falls like $L^{3n+3}$ (even $n$) or $L^{3n+4}$ (odd $n$). The tests observe the exponents $7$ for $n = 1$ and $9$ for $n = 2$.

**Error estimate (heuristic).** No theorem bounds $\lvert I - K \rvert$ by $e$. $\lvert K - G \rvert$ estimates the error of $G$, and the power $1.5$ guesses how much better $K$ is; the constants $200$ and $50\epsilon$ are empirical. An integrand that vanishes at all $2n + 1$ nodes, but not identically, gets $K = G = 0$ and $e = 0$. "ok" from the driver means the estimates sum to at most $\tau$, not that the error does.

## Complexity

- **Evaluations per panel.** $2n + 1$, none at the endpoints; both $K$ and $G$ come from these values. Comparing $G_n$ with the separate Gauss rule $G_{2n+1}$ would cost $3n + 1$.
- **Adaptive.** After $k$ bisections, $(2k + 1)(2n + 1)$ evaluations and $O(k\log k)$ heap work; at most `limit` panels.
- **Building the rule.** $O(n^2)$ exact triple products for $E_{n+1}$, $O(n^2)$ floating operations per bisection sweep for its zeros, and $O(n^3)$ for the weights by Gaussian elimination. In pure Python the rule takes 2 ms for $n = 7$ and 36 ms for $n = 30$, once; the result is cached. Laurie's method builds it in $O(n^2)$ from the Jacobi matrix.
- **Rounding.** The weights are positive and sum to $2$, so evaluation errors of size $\delta$ change $K$ by at most $2\lvert h \rvert\delta$. The floor $50\epsilon\lvert h \rvert\sum W_i\lvert f_i \rvert$ in line L5 keeps the estimate from asking for more than double precision can give.

## Properties

- **Degree** $3n + 1$, or $3n + 2$ for odd $n$; G7-K15 has degree 23 and G7 has degree 13.
- **Nested.** $K_{2n+1} \supset G_n$. Patterson's extensions continue the nesting: 3, 7, 15, 31, ... points.
- **Positive weights and interlacing.** For the Legendre weight, the Kronrod nodes are real, interior and interlace with the Gauss nodes, and all weights are positive (checked here for $n \le 30$).
- **Kronrod extensions do not always exist.** For the Laguerre and Hermite weights, extensions with real nodes and positive weights exist only for a few small $n$ (Kahaner and Monegato 1978).
- **Symmetric.** Nodes and weights are symmetric about $0$, and the code imposes this exactly.

## Variants and improvements

- **Other pairs.** QUADPACK offers G7-K15, G10-K21, G15-K31, G20-K41, G25-K51 and G30-K61 (routines QK15 to QK61); higher pairs suit smooth integrands with tight tolerances.
- **Patterson extensions.** Iterate the construction: from $K_{2n+1}$ add $2n + 2$ nodes to reach degree about $6n$, and so on. Every level reuses all previous values, which suits automatic, non-adaptive integrators (QNG in QUADPACK).
- **Laurie's algorithm.** Builds the Kronrod Jacobi matrix of size $2n + 1$ and applies the [Golub-Welsch](/golub-welsch-algorithm/) method; works for any weight whose extension exists.
- **Extrapolation.** QAGS combines this driver with Wynn's epsilon algorithm to accelerate endpoint singularities such as $x^{-1/2}$ and $\log x$.
- **Clenshaw-Curtis as an alternative.** [Clenshaw-Curtis](/clenshaw-curtis-quadrature/) rules are nested by doubling, with almost the same accuracy per point for most integrands.
- **Infinite intervals.** QUADPACK's QAGI maps $[0, \infty)$ to $(0, 1]$ by $x = (1 - t)/t$ and integrates with G7-K15; see [improper integration](/improper-integration/).

## When to use it

Use a Gauss-Kronrod pair inside an adaptive integrator when nothing special is known about $f$ beyond that it can be evaluated anywhere in the open interval: piecewise smooth functions, integrable endpoint singularities, moderate oscillation. It is the default in QUADPACK, SciPy's `quad`, GSL and many others. Prefer a plain Gauss rule when the integrand is smooth and no estimate is needed, [tanh-sinh](/tanh-sinh-quadrature/) for strong endpoint singularities at very high precision, and Filon or Levin methods for highly oscillatory integrands.

## Pitfalls

- **The estimate can be fooled.** If $f$ is a narrow spike between nodes, all 15 samples may miss it, and the driver returns $0$ with status "ok". Split the interval at known features, or give the driver the location of the spike.
- **Singularities at $b \ne 0$.** Floating point numbers near $1$ are $1.1 \times 10^{-16}$ apart, so panels at $1$ cannot shrink below that size. For $\int_0^1 \frac{dx}{\sqrt{x(1 - x)}}$ the driver reaches $\tau = 10^{-6}$ but stops with "roundoff" at $\tau = 10^{-10}$, with an estimate of $6 \times 10^{-7}$. Move the singularity to $0$ by a substitution.
- **Unreachable tolerance.** $\tau = 10^{-20}$ on $\int_0^1 e^x$ stops after 15 evaluations with "roundoff", because the estimate is already at its floor; without the floor test, the driver would bisect forever.
- **Too pessimistic for smooth $f$.** For $e^x$ on $[0, 4]$ the estimate is about 400 times the true error, so smooth integrals sometimes get split once more than needed.
- **Mixing node counts.** $n$ counts Gauss nodes here, so "G7-K15" is $n = 7$. Some texts index the Kronrod rule by its own number of nodes.
- **Absolute versus relative tolerance.** For integrals of size $10^{-20}$, an absolute $\tau$ is met trivially; pass a relative tolerance too.

## Implementations

## History

A. S. Kronrod introduced the extension of Gauss-Legendre rules in a 1964 Russian monograph, translated in 1965 as *Nodes and Weights of Quadrature Formulas*, with tables of the nodes and weights. The polynomials $E_{n+1}$ had already been considered by Stieltjes in an 1894 letter to Hermite, and Szegő (1935) proved that their zeros interlace with those of $P_n$. Patterson (1968) iterated the construction to nested sequences. Piessens and de Doncker, with Überhuber and Kahaner, built QUADPACK (1983) on the G7-K15 and higher pairs with a globally adaptive strategy; it became the integrator behind most numerical libraries. Monegato proved positivity of the weights (1978) and surveyed the theory (1982), and Laurie (1997) gave the $O(n^2)$ Jacobi matrix method.

## References
