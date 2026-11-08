---
tag: BPA5JP
kind: algorithm
slug: levin-method
name: Levin's method
aliases:
- Levin collocation method
- Levin collocation
- Levin-type method
area: numerical/quadrature
level: research
summary: Collocation method for highly oscillatory integrals based on an associated differential equation.
solves: [numerical-integration]
model: real-ram
complexity:
  vars: {n: "the degree of the collocation polynomial, with n + 1 Chebyshev-Lobatto nodes"}
  time: {worst: Θ(n^3), average: Θ(n^3), best: Θ(n^3)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [oscillatory-integration, chebyshev-nodes]
see_also: [filon-quadrature, collocation-method, chebyshev-polynomials, gaussian-elimination, condition-number, clenshaw-curtis-quadrature, gauss-legendre-quadrature]
sources:
  - paper: "David Levin, Procedures for computing one- and two-dimensional integrals of functions with rapid irregular oscillations, Mathematics of Computation 38(158), 1982, 531-538"
    locator: the reduction to p' + i omega g' p = f, collocation in a basis of nonoscillating functions, and the two-dimensional extension
  - paper: "David Levin, Analysis of a collocation method for integrating rapidly oscillatory functions, Journal of Computational and Applied Mathematics 78, 1997, 131-138"
    locator: existence of a nonoscillatory solution and the O(omega^(-2)) error of collocation that includes the end points, for phases without stationary points
  - paper: "Sheehan Olver, Moment-free numerical integration of highly oscillatory functions, IMA Journal of Numerical Analysis 26(2), 2006, 213-227"
    locator: the asymptotic order O(omega^(-s-1)) when derivatives up to order s - 1 are collocated at the end points, and the regularity condition on the basis
  - book: "Alfredo Deaño, Daan Huybrechs and Arieh Iserles, Computing Highly Oscillatory Integrals, SIAM, 2018"
    locator: Chapter 4 (Levin methods and their asymptotic and numerical analysis)
  - book: "Lloyd N. Trefethen, Approximation Theory and Approximation Practice, Extended Edition, SIAM, 2019"
    locator: Chapter 8, Theorem 8.2 (geometric convergence of Chebyshev interpolants of analytic functions)
  - book: "Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, 2nd ed., SIAM, 2002"
    locator: Chapter 9 (backward error of Gaussian elimination with partial pivoting)
---

Levin's method computes an oscillatory integral

$$I = \int_a^b f(x)\, e^{i\omega g(x)}\,dx$$

without sampling the oscillations. It looks for a function $p$ with $p' + i\omega g' p = f$; then $\frac{d}{dx}\big(p\,e^{i\omega g}\big) = f e^{i\omega g}$, so $I = p(b)e^{i\omega g(b)} - p(a)e^{i\omega g(a)}$. When $f$ and $g$ are smooth and $g'$ has no zero in $[a, b]$, this equation has a solution that does not oscillate, and a polynomial $p$ found by [collocation](/collocation-method/) at a few [Chebyshev nodes](/chebyshev-nodes/) captures it. The cost is a small dense linear system, independent of $\omega$, and the error falls as $\omega$ grows: like $\omega^{-2}$ for fixed $n$ when the end points are among the nodes. Unlike [Filon quadrature](/filon-quadrature/), it needs no moments $\int x^k e^{i\omega g}$. David Levin introduced it in 1982.

## In plain words

An integral of a wave that wiggles very fast is hard for ordinary rules: they need several points per wiggle, so the cost grows with the frequency, even though the answer is a single small number that depends mostly on what happens at the two ends.

Levin's method avoids the wiggles altogether. It asks for a smooth, slowly changing function whose product with the wave has exactly the integrand as its slope. Once such a function is known, the integral is just the change of that product from one end to the other. A smooth function is easy to approximate with a few well-placed points, so the work does not depend on how fast the wave wiggles, and faster waves actually make the answer more accurate.

## The problem

Given oracles for a smooth amplitude $f$ (real or complex), a smooth real phase $g$ and its derivative $g'$, a finite interval $[a, b]$, a frequency $\omega \ne 0$, and a tolerance $\tau$, approximate $I$ above. The phase must have no stationary point: $g'(x) \ne 0$ on $[a, b]$. Cost is counted in evaluations of $f$, $g$ and $g'$, plus the linear algebra. See [oscillatory integration](/oscillatory-integration/) for the problem and the other methods.

## The algorithm

```pseudo id=main
LEVIN(f, g, g', a, b, ω, n)                ▷ finite a ≠ b, ω ≠ 0, n ≥ 1, g' ≠ 0 on [a, b]
L1  c ← (a + b)/2;  r ← (b − a)/2
L2  for j ← 0 to n do
L3      t_j ← cos(π j / n);  x_j ← c + r t_j
L4      A[j][k] ← T_k'(t_j)/r + iω g'(x_j) T_k(t_j)   for k = 0..n
L5      F[j] ← f(x_j)
L6  solve A c = F by Gaussian elimination with partial pivoting
L7  p_b ← Σ_k c_k;  p_a ← Σ_k (−1)^k c_k
L8  return p_b e^{iω g(b)} − p_a e^{iω g(a)}
```

The unknown is $p(x) = \sum_{k=0}^n c_k T_k(t)$, $x = c + rt$, in the basis of [Chebyshev polynomials](/chebyshev-polynomials/), which is far better conditioned than monomials. Row $j$ of $A$ applied to $c$ is $p'(x_j) + i\omega g'(x_j) p(x_j)$, so line L6 enforces the differential equation at the $n + 1$ Chebyshev-Lobatto points, which include both end points ($x_0 = b$, $x_n = a$). Lines L3 and L4 compute $T_k$ and $T_k'$ by the three-term recurrence. Line L7 uses $T_k(\pm 1) = (\pm 1)^k$. The orientation of $[a, b]$ needs no special case, since line L8 is valid either way. The system is solved by [Gaussian elimination](/gaussian-elimination/) in complex arithmetic.

## Example

For $\int_0^1 e^x e^{i\omega x}\,dx = \frac{e^{1 + i\omega} - 1}{1 + i\omega}$, absolute errors with $n + 1$ nodes:

| $n$ | $\omega = 1$ | $\omega = 10$ | $\omega = 100$ | $\omega = 1000$ | $\omega = 10^4$ |
|---|---|---|---|---|---|
| 2 | $2.4 \times 10^{-3}$ | $1.9 \times 10^{-3}$ | $6.7 \times 10^{-6}$ | $1.4 \times 10^{-7}$ | $2.8 \times 10^{-9}$ |
| 4 | $2.1 \times 10^{-6}$ | $2.0 \times 10^{-5}$ | $1.6 \times 10^{-8}$ | $8.6 \times 10^{-10}$ | $1.7 \times 10^{-11}$ |
| 6 | $4.7 \times 10^{-10}$ | $2.2 \times 10^{-8}$ | $8.9 \times 10^{-11}$ | $2.0 \times 10^{-12}$ | $3.8 \times 10^{-14}$ |
| 8 | $1.5 \times 10^{-13}$ | $4.4 \times 10^{-12}$ | $2.6 \times 10^{-13}$ | $2.4 \times 10^{-15}$ | $4.4 \times 10^{-17}$ |
| 10 | $2.2 \times 10^{-16}$ | $3.9 \times 10^{-16}$ | $3.0 \times 10^{-16}$ | $1.9 \times 10^{-18}$ | $4.1 \times 10^{-20}$ |

Down a column the error falls geometrically, as Chebyshev interpolation of $e^x$ does; along a row it falls roughly like $\omega^{-2}$, while $|I|$ itself falls only like $\omega^{-1}$. A relative error below $10^{-10}$ takes 9 nodes for $\omega = 10$ and $100$ and 8 nodes for $\omega = 1000$ and $10^4$. [Gauss-Legendre](/gauss-legendre-quadrature/) needs 11, 42 and 287 points for $\omega = 10, 100, 1000$ (see [oscillatory integration](/oscillatory-integration/)).

With a nonlinear phase, $\int_0^1 \frac{1}{1 + x} e^{i\omega(x + x^2/2)}\,dx$, against a composite Gauss-Legendre reference:

| $n$ | $\omega = 10$ | $\omega = 100$ | $\omega = 1000$ |
|---|---|---|---|
| 2 | $5.5 \times 10^{-3}$ | $4.5 \times 10^{-5}$ | $5.5 \times 10^{-7}$ |
| 4 | $2.5 \times 10^{-4}$ | $3.6 \times 10^{-6}$ | $4.7 \times 10^{-8}$ |
| 8 | $6.5 \times 10^{-7}$ | $1.0 \times 10^{-8}$ | $1.3 \times 10^{-10}$ |
| 16 | $1.6 \times 10^{-17}$ | $4.8 \times 10^{-14}$ | $3.7 \times 10^{-16}$ |

Filon methods would need the moments $\int_0^1 x^k e^{i\omega(x + x^2/2)}\,dx$, which have no elementary closed form.

## Correctness

The full proof is in the correctness file. The key identity (Lemma 1) is that for every $C^1$ function $p$, $\int_a^b (p' + i\omega g'p)\, e^{i\omega g} = [p\,e^{i\omega g}]_a^b$; so the method integrates exactly the function $\mathcal{L}[p] = p' + i\omega g' p$ that collocation produces, and the error is $\int_a^b (f - \mathcal{L}[p])\, e^{i\omega g}$ (Theorem 1). Consequences, each proved there:

- **Exactness.** If $f = \mathcal{L}[q]$ for a polynomial $q$ of degree at most $n$, the method is exact (when $A$ is nonsingular).
- **Solvability.** If $g' \ne 0$ at the nodes, $A$ is nonsingular for all large enough $|\omega|$.
- **Linear phase.** For $g(x) = \kappa x + \gamma$, $A$ is always nonsingular, $\mathcal{L}[p]$ is the polynomial interpolant $\Pi_n f$ of $f$ at the nodes, and the error is at most $|b - a|\,\|f - \Pi_n f\|_\infty$ and at most $(|e_n'(a)| + |e_n'(b)| + \|e_n''\|_{L^1})/(\kappa\omega)^2$ with $e_n = f - \Pi_n f$, because $e_n$ vanishes at the end points.

For a general phase without stationary points, the $O(\omega^{-2})$ rate is cited (Levin 1997; Olver 2006), and so is the geometric convergence of Chebyshev interpolation (Trefethen 2019, Theorem 8.2).

## Complexity

The method makes $n + 1$ evaluations of $f$ and of $g'$ and 2 of $g$, independent of $\omega$. Filling $A$ costs $\Theta(n^2)$ and Gaussian elimination $\Theta(n^3)$ arithmetic with $\Theta(n^2)$ memory. For analytic $f$ and $g$ without stationary points, $n$ between 5 and 20 typically gives full double precision for every $\omega$ from about $1/(b - a)$ upward (asymptotic and empirical; see the tables), so the $n^3$ term is negligible next to a single standard rule at large $\omega$, whose cost grows linearly in $\omega$.

## Properties

- **Frequency independent cost, improving accuracy.** For fixed $n$, error $O(\omega^{-2})$ as $\omega \to \infty$ when both end points are collocation nodes.
- **No moments.** Only values of $f$, $g$ and $g'$ are needed, which is the main advantage over Filon methods for nonlinear phases.
- **Same as Filon for linear phase.** For $g(x) = x$ the result equals the Filon-type rule that integrates $\Pi_n f\, e^{i\omega x}$ exactly; Levin computes it without forming moments.
- **Basis free in principle.** Any basis of nonoscillating functions may be used for $p$; Chebyshev polynomials give good conditioning and spectral accuracy.
- **Generalizes to systems.** Integrands $\langle \mathbf f, \mathbf w \rangle$ with $\mathbf w' = \omega A(x)\mathbf w$, such as Bessel kernels, lead to a vector equation $\mathbf p' + \omega A^T \mathbf p = \mathbf f$ solved the same way.

## Variants and improvements

- **Levin-type methods with derivatives.** Collocating $f$ and its first $s - 1$ derivatives at the end points raises the asymptotic order to $O(\omega^{-s-1})$, as for Filon-Hermite rules (Olver 2006).
- **Vector Levin for special functions.** Levin (1996) and Olver handle $\int f(x) J_\nu(\omega x)\,dx$ and similar integrals through the linear differential systems the kernels satisfy.
- **Two-dimensional integrals.** Levin's 1982 paper also treats $\iint f\, e^{i\omega g}$ over rectangles by a partial differential equation of the same form.
- **Better linear algebra.** For large $n$ and small $\omega$ the collocation matrix becomes ill conditioned; truncated SVD or least squares solves, and spectral methods based on the ultraspherical basis, keep the method stable for larger $n$ (surveyed by Deaño, Huybrechs and Iserles 2018).
- **Stationary points.** With $g'(\xi) = 0$, either split off a neighbourhood of $\xi$ and treat it by a Filon rule with moments, or use [numerical steepest descent](/oscillatory-integration/); plain Levin collocation fails there.

## When to use it

- Integrals $\int f e^{i\omega g}$ with large $\omega(b - a)$, smooth $f$ and $g$, and no stationary point, especially with a nonlinear phase where Filon moments are unavailable.
- As one step in a larger computation where the same kind of integral recurs with many frequencies: the cost does not grow with $\omega$.
- Not for $\omega(b - a)$ of order 1 or less, where [Gauss-Legendre](/gauss-legendre-quadrature/) or [Clenshaw-Curtis](/clenshaw-curtis-quadrature/) are cheaper and the Levin system is ill conditioned, and not when $g'$ vanishes in $[a, b]$.

## Pitfalls

- **Stationary points.** For $\int_0^1 e^x e^{100 i (x - 1/2)^2}\,dx$, whose phase is stationary at $\tfrac12$, the errors for $n = 5$, $9$ and $17$ are $0.29$, $0.28$ and $0.26$, as large as the integral itself, whose modulus is $0.26$; only at $n = 33$, when the polynomial starts to resolve the oscillation directly, does the error drop, to $4.3 \times 10^{-3}$. The nonoscillatory solution of the differential equation does not exist near the stationary point.
- **Small frequency.** At $\omega = 0$ the column of $A$ belonging to $T_0$ is zero; as $\omega \to 0$ the system becomes nearly singular and line L8 cancels. With $n = 10$ on $\int_0^1 e^x e^{i\omega x}\,dx$ the errors are $6.9 \times 10^{-8}$, $4.7 \times 10^{-4}$ and $9.7$ for $\omega = 10^{-2}, 10^{-4}, 10^{-6}$. The implementation rejects $\omega = 0$.
- **Monomial basis.** Writing $p$ in powers of $x$ instead of Chebyshev polynomials makes $A$ ill conditioned already for moderate $n$, as for any Vandermonde system; see [condition number](/condition-number/).
- **The derivative $g'$ must be consistent with $g$.** A wrong $g'$ produces a finite, plausible looking and wrong answer; the method has no internal check.
- **No error estimate.** Comparing $n$ and a larger $n$ gives a heuristic estimate; for large $\omega$ both may agree to many digits while sharing an error of the linear algebra.

## Implementations

## History

David Levin introduced the method in 1982 in Mathematics of Computation, for one- and two-dimensional integrals of functions with rapid irregular oscillations, using collocation for the nonoscillatory solution of the associated differential equation. In 1996 and 1997 he extended it to Bessel-type kernels through vector equations and analysed its error, showing an $O(\omega^{-2})$ rate when the end points are collocated. Sheehan Olver (2006) connected it with Filon-type methods and with the asymptotic expansion, introducing Levin-type methods with end point derivatives and arbitrary asymptotic order. Later work on stable solvers and on stationary points is collected in the book of Deaño, Huybrechs and Iserles (2018).

## References
