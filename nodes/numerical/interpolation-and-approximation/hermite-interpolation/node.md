---
tag: B184Y7
kind: problem
slug: hermite-interpolation
name: Hermite interpolation
aliases:
- Osculating interpolation
- osculatory interpolation
- interpolation with derivatives
- confluent interpolation
area: numerical/interpolation-and-approximation
level: core
summary: Find the polynomial of least degree that matches given values and derivatives up to stated orders at distinct nodes. It exists and is unique; divided differences with repeated nodes build it.
prereqs: [interpolation-problem, divided-differences]
see_also: [cubic-hermite-spline, divided-differences, interpolating-polynomial-uniqueness, newton-interpolation, polynomial-interpolation-error-theorem, lagrange-interpolation, catmull-rom-spline, gauss-legendre-quadrature]
sources:
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 6, Polynomial interpolation (Hermite interpolation, its existence and uniqueness, and its error)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 3.6, Hermite interpolation (the formula with h_i and the error term)
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter I, Polynomial interpolation (osculatory interpolation and divided differences with repeated sites)
  - book: isbn:9780486624952
    title: Philip J. Davis, Interpolation and Approximation, Dover, 1975 (first published 1963)
    locator: Chapter II, Interpolation (Hermite and Birkhoff interpolation problems)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 5, Modular algorithms and interpolation (the Chinese remainder theorem for polynomials, which contains Hermite interpolation)
  - paper: "Charles Hermite, Sur la formule d'interpolation de Lagrange, Journal für die reine und angewandte Mathematik 84 (1878) 70-79"
    locator: the interpolation formula with prescribed derivatives and its contour integral remainder
---

Hermite interpolation asks for a polynomial that matches not only given values at the nodes but also given derivatives, up to a stated order at each node. With $m_i$ conditions at the node $z_i$ (the value and the first $m_i - 1$ derivatives) and $N + 1 = \sum_i m_i$ conditions in total, there is exactly one polynomial of degree at most $N$ that satisfies them. It joins two familiar cases: the [interpolation problem](/interpolation-problem/), where every $m_i = 1$, and the Taylor polynomial, where there is one node with $m_0 = N + 1$. It is solved by [divided differences](/divided-differences/) with repeated nodes, and it underlies [cubic Hermite splines](/cubic-hermite-spline/), dense output of ODE solvers and the proof of Gauss quadrature.

## In plain words

Plain interpolation draws a curve through given points. Sometimes you also know the slope of the curve at those points, for example the speed of a moving object as well as its position. Hermite interpolation draws a polynomial curve that passes through each point with the given slope, and if you know them, with the given bending and higher rates of change too.

Each piece of information is one condition, and a polynomial with that many free coefficients satisfies all of them in exactly one way. A point with a slope counts as two conditions, so two points with slopes fix a cubic. The method is a small change to the difference table for ordinary interpolation: you list a point twice and put its slope where a difference would go.

## Definition

Notation on the interpolation and approximation pages: $f$ is a function on $[a, b]$, usually $[-1, 1]$; $\mathcal{P}_N$ is the space of polynomials of degree at most $N$; $\omega(x)$ is the node polynomial, here with multiplicities; $f[\cdot]$ denotes a divided difference.

**Input.** Distinct nodes $z_0, \ldots, z_m$ (in any order), multiplicities $m_0, \ldots, m_m \ge 1$, and numbers $y_i^{(k)}$ for $0 \le i \le m$ and $0 \le k \le m_i - 1$. Put $N + 1 = \sum_{i=0}^{m} m_i$.

**Output.** The polynomial $p \in \mathcal{P}_N$ with
$$p^{(k)}(z_i) = y_i^{(k)}, \qquad 0 \le i \le m, \quad 0 \le k \le m_i - 1.$$
When $y_i^{(k)} = f^{(k)}(z_i)$, $p$ is the Hermite interpolant of $f$.

**Theorem (existence and uniqueness).** For any data there is exactly one such $p$. *Proof.* The conditions are $N + 1$ linear equations in the $N + 1$ coefficients of $p$, so it suffices that the homogeneous problem has only the zero solution. If $p \in \mathcal{P}_N$ has $p^{(k)}(z_i) = 0$ for $k < m_i$, then $z_i$ is a root of $p$ of multiplicity at least $m_i$, so $\prod_i (x - z_i)^{m_i}$, of degree $N + 1$, divides $p$. Since $\deg p \le N$, $p = 0$. $\square$ The matrix of the system in the monomial basis is the confluent Vandermonde matrix, which is therefore nonsingular.

**Theorem (error).** If $f \in C^{N+1}[a, b]$, all $z_i \in [a, b]$ and $x \in [a, b]$, then for some $\xi$ in the smallest interval that holds $x$ and the nodes,
$$f(x) - p(x) = \frac{f^{(N+1)}(\xi)}{(N+1)!}\, \omega(x), \qquad \omega(x) = \prod_{i=0}^{m} (x - z_i)^{m_i}.$$
*Proof sketch.* For $x$ not a node, let $g(s) = f(s) - p(s) - c\,\omega(s)$ with $c$ chosen so that $g(x) = 0$. Then $g$ has zeros of total multiplicity $N + 2$ counted with multiplicity, and repeated use of Rolle's theorem gives a zero $\xi$ of $g^{(N+1)} = f^{(N+1)} - c\,(N+1)!$ (Süli and Mayers, Chapter 6; Atkinson, Section 3.6). $\square$ This is a proved bound with exact hypotheses; it is the same formula as the [interpolation error theorem](/polynomial-interpolation-error-theorem/) with repeated nodes.

**Divided differences with repeated nodes.** List each $z_i$ $m_i$ times, giving the sequence $x_0 \le \cdots$ of $N + 1$ entries with equal entries adjacent. Define $f[z, \ldots, z] = f^{(k)}(z)/k!$ for $k + 1$ equal arguments, and use the usual recurrence otherwise. Then $p(x) = \sum_{k=0}^{N} f[x_0, \ldots, x_k] \prod_{j<k} (x - x_j)$, the Newton form; the [divided differences page](/divided-differences/) proves this through the Hermite and Genocchi formula, which is continuous as nodes coalesce.

**The case $m_i = 2$.** With values $y_i$ and slopes $y_i'$ at $n + 1$ nodes ($N = 2n + 1$) and the Lagrange basis $\ell_i$,
$$p(x) = \sum_{i=0}^{n} y_i \big(1 - 2\ell_i'(x_i)(x - x_i)\big)\ell_i(x)^2 + \sum_{i=0}^{n} y_i' (x - x_i)\ell_i(x)^2.$$

## Variants

- **Piecewise Hermite.** On each interval of a mesh, the cubic with values and slopes at both ends: the [cubic Hermite spline](/cubic-hermite-spline/), which is $C^1$. Slopes may be data, finite difference estimates ([Catmull-Rom](/catmull-rom-spline/)) or limited for monotonicity ([Fritsch and Carlson](/fritsch-carlson-monotone-interpolation/)).
- **Taylor interpolation.** One node with all $N + 1$ derivatives gives the Taylor polynomial; the error formula becomes Taylor's theorem with the Lagrange remainder.
- **Birkhoff (lacunary) interpolation.** Some derivatives are given without the lower ones, for example $p''(z)$ without $p'(z)$. Such problems need not be solvable; see the example below.
- **Hermite and Fejér interpolation.** All slopes are set to zero: $p(x_i) = f(x_i)$, $p'(x_i) = 0$. Fejér (1916) proved that at the Chebyshev points of the first kind these polynomials of degree $2n + 1$ converge uniformly for every continuous $f$, which ordinary interpolation does not.
- **Rational and trigonometric Hermite interpolation**, and barycentric formulas with weights for each derivative order.
- **Several variables.** Hermite finite elements prescribe values and derivatives at the vertices of triangles or rectangles; as in the Lagrange case, solvability depends on the geometry.

## Examples

**Two points with slopes.** Find the cubic with $p(0) = 0$, $p'(0) = 1$, $p(1) = 1$, $p'(1) = 0$. The divided difference table on $0, 0, 1, 1$ is:

| $x_k$ | $f[x_k]$ | first | second | third |
|---|---|---|---|---|
| 0 | 0 | | | |
| 0 | 0 | $f[0, 0] = 1$ | | |
| 1 | 1 | $f[0, 1] = 1$ | $f[0, 0, 1] = 0$ | |
| 1 | 1 | $f[1, 1] = 0$ | $f[0, 1, 1] = -1$ | $f[0, 0, 1, 1] = -1$ |

So $p(x) = 0 + 1 \cdot x + 0 \cdot x^2 - 1 \cdot x^2 (x - 1) = x + x^2 - x^3$, and indeed $p'(1) = 1 + 2 - 3 = 0$.

**Accuracy against Taylor.** For $f = e^x$ on $[0, 1]$, the Hermite cubic with values and slopes at 0 and 1 has maximum error $0.00437$, within the proved bound $\tfrac{e}{4!} \max_{[0,1]} x^2 (x - 1)^2 = e/384 \approx 0.00708$. The Taylor cubic at 0 uses the same number of conditions but has the error $0.0516$ at $x = 1$.

**A Birkhoff problem with no unique solution.** Ask for $p \in \mathcal{P}_2$ with $p(-1) = a$, $p'(0) = b$ and $p(1) = c$. For $p = c_0 + c_1 x + c_2 x^2$ the conditions are $c_0 - c_1 + c_2 = a$, $c_1 = b$, $c_0 + c_1 + c_2 = c$, and they force $c - a = 2b$. For other data there is no solution, and for data that satisfy it there are infinitely many, since $c_0$ and $c_2$ only enter as $c_0 + c_2$. Hermite data, where each derivative comes with all lower ones at the same node, never fail in this way.

## Known algorithms

- **Divided differences with repeated nodes**: $O(N^2)$ operations for the Newton coefficients, then $O(N)$ per evaluation by nested multiplication; see [Newton interpolation](/newton-interpolation/).
- **Explicit basis for $m_i = 2$**: the formula above, $O(n^2)$ per point directly, or $O(n)$ per point in barycentric form.
- **Piecewise cubic Hermite**: $O(1)$ per point after locating the interval; see [cubic Hermite spline](/cubic-hermite-spline/).
- **Confluent Vandermonde systems**: solvable in $O(N^2)$ operations by the method of Björck and Elfving, a variant of the Björck and Pereyra algorithm for [Vandermonde systems](/vandermonde-matrix/).
- **Exact arithmetic**: over a field, the Chinese remainder theorem with moduli $(x - z_i)^{m_i}$ gives the coefficients in $O(M(N) \log N)$ operations, where $M(N)$ is the cost of multiplying polynomials of degree $N$ (von zur Gathen and Gerhard, Chapter 5; [fast interpolation](/fast-interpolation/)).

## Bounds

- The problem has $N + 1$ data and an answer with $N + 1$ coefficients, so $\Omega(N)$ operations are needed to read the input; the fast algorithm above is within a logarithmic factor of $M(N)$.
- Conditioning: as for plain interpolation, the sensitivity of $p(x)$ to the data is measured by a Lebesgue function, now with one basis function per condition. Derivative data enter with factors that grow with the order of the derivative and with the inverse distances between nodes.
- Floating point: divided differences with nearby but distinct nodes suffer cancellation of order $u/h^k$; treating nodes that are equal in the data as exactly equal, and using the derivative values, avoids the worst case.

## Reductions

- Hermite interpolation reduces to a square linear system (the confluent Vandermonde system) and, over a field, to the Chinese remainder theorem for polynomials.
- It is the limit of Lagrange interpolation as groups of nodes coalesce: the interpolants at $z, z + h$ converge to the Hermite interpolant with $p(z)$ and $p'(z)$ as $h \to 0$, for $f \in C^1$.
- Gauss quadrature reduces to it: integrating the Hermite interpolant with $m_i = 2$ at the zeros of an orthogonal polynomial proves exactness for degree $2n + 1$ ([Gauss and Legendre quadrature](/gauss-legendre-quadrature/)).

## Applications

- Piecewise cubic Hermite curves in graphics and animation, and monotone interpolation of data.
- Dense output of Runge-Kutta and multistep ODE solvers, which know the solution and its derivative at the step ends.
- Finite elements for beams and plates, which need $C^1$ continuity.
- Error analysis of Gauss quadrature and of numerical differentiation.
- Coding theory and computer algebra: Hermite interpolation over finite fields appears in multiplicity codes and in modular algorithms.

## References
