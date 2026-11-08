---
tag: VME7M6
kind: theorem
slug: interpolating-polynomial-uniqueness
name: Uniqueness of the interpolating polynomial
aliases:
- Uniqueness of an interpolating polynomial
- existence and uniqueness of polynomial interpolation
- unisolvence of polynomial interpolation
area: numerical/interpolation-and-approximation
level: core
summary: For n + 1 distinct nodes and any n + 1 values there is exactly one polynomial of degree at most n through the data. Equivalently, the Vandermonde matrix of distinct nodes is nonsingular.
prereqs: [polynomial, interpolation-problem]
see_also: [interpolation-problem, lagrange-interpolation, newton-interpolation, barycentric-interpolation, vandermonde-matrix, hermite-interpolation, divided-differences, polynomial-interpolation-error-theorem]
sources:
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 6, Polynomial interpolation (the Lagrange interpolation theorem, existence and uniqueness of the interpolating polynomial)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 3.1, Polynomial interpolation theory (existence and uniqueness through the Vandermonde determinant, and the Lagrange formula)
  - book: isbn:9780486624952
    title: Philip J. Davis, Interpolation and Approximation, Dover, 1975 (first published 1963)
    locator: Chapter II, Interpolation (the fundamental theorem of polynomial interpolation and the Vandermonde determinant)
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 4, Polynomial interpolation
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 5, Modular algorithms and interpolation (Lagrange interpolation over a field as a case of the Chinese remainder theorem)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 22, Vandermonde systems (the determinant and the conditioning of the Vandermonde matrix)
---

The uniqueness theorem for polynomial interpolation says that through $n + 1$ points with distinct abscissas there passes exactly one polynomial of degree at most $n$. Existence comes from the Lagrange basis, and uniqueness from the fact that a nonzero polynomial of degree at most $n$ has at most $n$ roots. The theorem makes "the interpolating polynomial $p_n$" a well-defined object. The [Lagrange](/lagrange-interpolation/), [Newton](/newton-interpolation/) and [barycentric](/barycentric-interpolation/) formulas are three ways to write the same polynomial, and a polynomial of degree at most $n$ is reproduced exactly by its own interpolant.

## Statement

Notation on the interpolation and approximation pages: $f$ is a function on $[a, b]$, usually $[-1, 1]$; the nodes are $x_0, \ldots, x_n$ with data $y_i = f(x_i)$; $\mathcal{P}_n$ is the space of polynomials of degree at most $n$; $p_n$ is the interpolating polynomial; $\omega(x) = \prod_{i=0}^{n} (x - x_i)$ is the node polynomial; $\Lambda_n$ is the [Lebesgue constant](/lebesgue-constant/). The nodes need not be sorted.

**Theorem.** Let $K$ be a field (for example $\mathbb{R}$, $\mathbb{C}$, $\mathbb{Q}$ or a finite field), let $x_0, \ldots, x_n \in K$ be pairwise distinct, and let $y_0, \ldots, y_n \in K$ be arbitrary. Then there is exactly one $p \in \mathcal{P}_n$ with
$$p(x_i) = y_i, \qquad i = 0, 1, \ldots, n.$$
It is
$$p_n(x) = \sum_{i=0}^{n} y_i\, \ell_i(x), \qquad \ell_i(x) = \prod_{j \ne i} \frac{x - x_j}{x_i - x_j}.$$

**Equivalent matrix form.** The Vandermonde matrix $V = (x_i^{\,k})_{i, k = 0}^{n}$ is nonsingular, with
$$\det V = \prod_{0 \le i < j \le n} (x_j - x_i).$$

**Complement.** The polynomials $q \in \mathcal{P}_{n+1}$ with $q(x_i) = y_i$ for all $i$ are exactly $q = p_n + c\,\omega$ for $c \in K$. So the degree bound $n$ is what makes the answer unique.

## In plain words

Two points fix a line, and three points fix a parabola, as long as no two of the points sit above the same $x$. In general, $n + 1$ points with different $x$ values fix one curve of degree $n$ through them. You can always find such a curve, and there is only one.

The reason for "only one" is short. If two such curves existed, their difference would be a polynomial of degree at most $n$ that is zero at $n + 1$ places. A nonzero polynomial of degree $n$ crosses zero at most $n$ times, so the difference is zero, and the two curves are the same.

## Proof

**Existence.** Each $\ell_i$ is a product of $n$ linear factors, so $\ell_i \in \mathcal{P}_n$. The denominators $x_i - x_j$ with $j \ne i$ are nonzero because the nodes are distinct, and $K$ is a field, so the quotients exist. At a node, $\ell_i(x_i) = 1$, since every factor is 1, and $\ell_i(x_k) = 0$ for $k \ne i$, since the factor with $j = k$ vanishes. Hence $p_n = \sum_i y_i \ell_i \in \mathcal{P}_n$ and $p_n(x_k) = \sum_i y_i \ell_i(x_k) = y_k$.

**Uniqueness.** Let $p, q \in \mathcal{P}_n$ both interpolate the data, and put $r = p - q \in \mathcal{P}_n$. Then $r(x_i) = 0$ for the $n + 1$ distinct nodes. Suppose $r \ne 0$, of degree $d \le n$. By the factor theorem (division by $x - x_0$ leaves the remainder $r(x_0) = 0$), $r = (x - x_0) r_1$ with $\deg r_1 = d - 1$. For $i \ge 1$, $0 = r(x_i) = (x_i - x_0) r_1(x_i)$ and $x_i - x_0 \ne 0$; since a field has no zero divisors, $r_1(x_i) = 0$. Repeating, after $d$ steps $r = c \prod_{i=0}^{d-1} (x - x_i)$ with a constant $c \ne 0$, and this still vanishes at $x_d$, a node that exists since $d \le n$. So $c \prod_{i < d} (x_d - x_i) = 0$, which is impossible because each factor is nonzero. Hence $r = 0$ and $p = q$.

**Matrix form.** Write $p(x) = \sum_{k=0}^{n} c_k x^k$. The conditions $p(x_i) = y_i$ are the square system $Vc = y$. Uniqueness for $y = 0$ means that the kernel of $V$ is $\{0\}$, so $V$ is nonsingular. The determinant formula follows by induction on $n$: with $x_0, \ldots, x_{n-1}$ fixed, $\det V$ is a polynomial in $x_n$ of degree at most $n$ that vanishes at $x_0, \ldots, x_{n-1}$ (two equal rows), and its coefficient of $x_n^n$ is the Vandermonde determinant $\det V_{n-1}$ of $x_0, \ldots, x_{n-1}$ (the cofactor of the last entry). So $\det V = \det V_{n-1} \prod_{i < n} (x_n - x_i)$, and the base case is $\det V_0 = 1$.

**Complement.** If $q \in \mathcal{P}_{n+1}$ interpolates, then $q - p_n \in \mathcal{P}_{n+1}$ vanishes at all $n + 1$ nodes. Dividing by $x - x_0$, then by $x - x_1$, and so on, as in the uniqueness proof, gives $q - p_n = c\,\omega$ with $c \in K$, since $\omega$ has degree $n + 1$. Conversely, $p_n + c\,\omega$ interpolates because $\omega(x_i) = 0$. $\square$

## Consequences

- **One polynomial, many formulas.** The Lagrange form, the Newton form with [divided differences](/divided-differences/), the [barycentric formula](/barycentric-interpolation/), Neville's scheme and the solution of the Vandermonde system all give the same polynomial in exact arithmetic. They differ only in cost and in their behavior in floating point.
- **Reproduction of polynomials.** If $f \in \mathcal{P}_n$, then $p_n = f$. In particular $\sum_i \ell_i(x) = 1$ (take $f = 1$) and $\sum_i x_i^k \ell_i(x) = x^k$ for $0 \le k \le n$. The barycentric formula is derived from the first identity.
- **Interpolation as a projection.** The map $L_n : f \mapsto p_n$ is linear and $L_n^2 = L_n$, since $L_n p = p$ for $p \in \mathcal{P}_n$. Its norm in the maximum norm is the [Lebesgue constant](/lebesgue-constant/) $\Lambda_n$, and the near-best bound $\|f - p_n\|_\infty \le (1 + \Lambda_n) E_n(f)$ uses $L_n p = p$.
- **Divided differences are well defined.** $f[x_0, \ldots, x_n]$ is the leading coefficient of the unique $p_n$, so it does not depend on the order of the nodes.
- **Error formula.** The proof of the [interpolation error theorem](/polynomial-interpolation-error-theorem/), $f(x) - p_n(x) = f^{(n+1)}(\xi)\,\omega(x)/(n+1)!$, applies Rolle's theorem to $f - p_n - c\,\omega$, which is the complement above in another form.
- **Polynomial identities.** Two polynomials of degree at most $n$ that agree at $n + 1$ points are equal. This is the basis of evaluation and interpolation methods for polynomial multiplication, of Reed and Solomon codes and of Shamir secret sharing over finite fields.

**Worked examples.**

**Real data.** Nodes $-1, 0, 1$ with values $2, 1, 2$. The unique quadratic is $p_2(x) = 1 + x^2$, and $\det V = (0 - (-1))(1 - (-1))(1 - 0) = 2$. Every cubic through the same points is $1 + x^2 + c(x^3 - x)$.

**A finite field.** Over $\mathrm{GF}(7)$, the nodes $1, 2, 3$ with values $3, 5, 2$ give the unique $p_2(x) = 3 + 6x + x^2$: indeed $p_2(1) = 10 \equiv 3$, $p_2(2) = 19 \equiv 5$ and $p_2(3) = 30 \equiv 2$. In Shamir's scheme these three shares recover the secret $p_2(0) = 3$, while any two of them are consistent with every value of $p_2(0)$.

**Order does not matter.** Listing the same nodes as $1, -1, 0$ permutes the rows of $V$ and may change the sign of $\det V$, but the interpolant $1 + x^2$ is the same.

## Tightness

- **The degree bound.** With $\mathcal{P}_{n-1}$ in place of $\mathcal{P}_n$ there are $n + 1$ conditions on $n$ coefficients, and the data $y_0 = \cdots = y_{n-1} = 0$, $y_n = 1$ have no solution: the unique interpolant is $\ell_n$, of degree exactly $n$. With $\mathcal{P}_{n+1}$ a solution exists but is not unique, by the complement.
- **Distinct nodes.** If $x_i = x_j$ with $i \ne j$ and $y_i \ne y_j$, no function interpolates; if $y_i = y_j$, the two conditions coincide and $\mathcal{P}_n$ has a line of solutions. Repeated nodes become meaningful when the repeated condition is read as a condition on a derivative; this is [Hermite interpolation](/hermite-interpolation/), for which the same theorem holds with the $n + 1$ conditions counted with multiplicity.
- **Fields, not rings.** Over the ring $\mathbb{Z}/4\mathbb{Z}$ with nodes $0$ and $2$, the nonzero polynomial $2x$ of degree 1 vanishes at both nodes, so uniqueness fails; the proof breaks at $x_1 - x_0 = 2$, a zero divisor. Over any commutative ring the theorem holds when every difference $x_i - x_j$ with $i \ne j$ is a unit.
- **Several variables.** The analogue fails. In the plane, the space of linear polynomials $a + bx + cy$ has dimension 3, but three points on one line $\alpha x + \beta y + \gamma = 0$ do not determine it: adding any multiple of $\alpha x + \beta y + \gamma$ leaves the three values unchanged. By the Mairhuber and Curtis theorem, no space of continuous functions of dimension at least 2 on a region of $\mathbb{R}^d$ with $d \ge 2$ is unisolvent for every set of distinct nodes (see the [interpolation problem](/interpolation-problem/)).
- **Numerical uniqueness.** Uniqueness is exact, but it does not make the monomial coefficients well determined. For real nodes the condition number of $V$ grows at least exponentially in $n$ (Higham, Chapter 22), so the coefficients $c_k$ computed from $Vc = y$ can be inaccurate even though the values of $p_n$ at good nodes are well conditioned, with condition number $\Lambda_n$. Evaluate $p_n$ in the [barycentric](/barycentric-interpolation/) or Newton form instead.

## History

Polynomial interpolation on equally spaced points is older than the general theorem: the finite difference formulas of Gregory and Newton in the seventeenth century produced the interpolant on an equally spaced table. The explicit formula with the basis $\ell_i$ was published by Edward Waring in 1779, then by Euler in 1783 and by Lagrange in 1795, whose name it carries. Uniqueness rests on the bound on the number of roots of a polynomial, which was standard algebra by then. The matrix is named after Vandermonde, but the product formula for its determinant is usually credited to Cauchy's work on alternating functions in the early nineteenth century.

## References
