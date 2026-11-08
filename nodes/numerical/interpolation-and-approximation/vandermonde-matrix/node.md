---
tag: GW0YQ4
kind: definition
slug: vandermonde-matrix
name: Vandermonde matrix
area: numerical/interpolation-and-approximation
level: intro
summary: The matrix of the powers of the nodes. It is invertible exactly when the nodes are distinct, and on a real interval its condition number grows exponentially with its size.
prereqs: [polynomial, determinant, condition-number]
see_also: [polynomial-interpolation, lagrange-interpolation, least-squares-problem, dft-matrix, hilbert-matrix, hermite-interpolation, interpolating-polynomial-uniqueness]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 22, Vandermonde systems (the inverse, its norm bounds, and the Björck-Pereyra algorithm with its error analysis)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 3.1, Polynomial interpolation theory (the Vandermonde determinant)
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 5, Barycentric interpolation formula (why the monomial basis and Vandermonde systems are avoided)
  - paper: "Walter Gautschi, On inverses of Vandermonde and confluent Vandermonde matrices, Numerische Mathematik 4 (1962) 117-123"
    locator: the bound on the norm of the inverse by the products of (1 + |x_j|)/|x_i - x_j|
  - paper: "Walter Gautschi, Norm estimates for inverses of Vandermonde matrices, Numerische Mathematik 23 (1975) 337-347"
    locator: the asymptotic growth of the condition number for equispaced and Chebyshev nodes
  - paper: "Ake Björck and Victor Pereyra, Solution of Vandermonde systems of equations, Mathematics of Computation 24 (1970) 893-903"
    locator: the O(n^2) algorithm for the primal and dual Vandermonde systems
  - paper: "Walter Gautschi and Gabriele Inglese, Lower bounds for the condition number of Vandermonde matrices, Numerische Mathematik 52 (1988) 241-250"
    locator: the exponential lower bounds for positive and for symmetric real nodes
  - paper: "Bernhard Beckermann, The condition number of real Vandermonde, Krylov and positive definite Hankel matrices, Numerische Mathematik 85 (2000) 553-577"
    locator: the exponential lower bound for every set of real nodes
---

The Vandermonde matrix of the nodes $x_0, \ldots, x_n$ is the matrix whose row $i$ holds the powers $1, x_i, x_i^2, \ldots, x_i^n$. It is the matrix of [polynomial interpolation](/polynomial-interpolation/) in the monomial basis: the coefficients $c$ of the interpolant solve $V c = y$. Its [determinant](/determinant/) is the product of all differences $x_j - x_i$, so it is invertible exactly when the nodes are distinct; but for real nodes its [condition number](/condition-number/) grows exponentially with $n$, which is why numerical codes avoid it.

## Definition

Let $K$ be a field and $x_0, \ldots, x_n \in K$. The **Vandermonde matrix** is
$$V = V(x_0, \ldots, x_n) = \begin{pmatrix} 1 & x_0 & x_0^2 & \cdots & x_0^n \\ 1 & x_1 & x_1^2 & \cdots & x_1^n \\ \vdots & & & & \vdots \\ 1 & x_n & x_n^2 & \cdots & x_n^n \end{pmatrix}, \qquad V_{ij} = x_i^{\,j} \quad (0 \le i, j \le n).$$
Some authors, Higham among them, use the transpose $V^T$; the results below hold for both with the norms swapped ($\|A\|_1 = \|A^T\|_\infty$). For $m + 1$ nodes and powers up to $n < m$ the same rule gives a rectangular $(m+1) \times (n+1)$ matrix, the matrix of a polynomial [least squares problem](/least-squares-problem/).

The notation is that of the interpolation pages: $p_n \in \mathcal{P}_n$ is the interpolating polynomial, $\ell_i$ are the Lagrange polynomials with $\ell_i(x_k) = \delta_{ik}$, and $\Lambda_n$ is the [Lebesgue constant](/lebesgue-constant/).

**Determinant.**
$$\det V(x_0, \ldots, x_n) = \prod_{0 \le i < j \le n} (x_j - x_i).$$

*Proof.* By induction on $n$. For $n = 0$ the matrix is $(1)$ and the empty product is 1. For $n \ge 1$, replace $x_n$ by a variable $t$ and expand the determinant along the last row. The result $D(t)$ is a polynomial in $t$ of degree at most $n$, and the coefficient of $t^n$ is the cofactor $\det V(x_0, \ldots, x_{n-1})$. For $t = x_i$ with $i < n$ two rows are equal, so $D(x_i) = 0$. If $x_0, \ldots, x_{n-1}$ are distinct, $D(t)$ has these $n$ roots and leading coefficient $\det V(x_0, \ldots, x_{n-1})$, so $D(t) = \det V(x_0, \ldots, x_{n-1}) \prod_{i < n} (t - x_i)$; with the induction hypothesis this is the formula at $t = x_n$. If two of $x_0, \ldots, x_{n-1}$ are equal, both sides are zero. $\square$

**Invertibility.** By the formula, $V$ is invertible if and only if the nodes are pairwise distinct. This is the matrix form of the existence and uniqueness of the interpolating polynomial ([uniqueness theorem](/interpolating-polynomial-uniqueness/)).

**The inverse.** Column $i$ of $V^{-1}$ holds the monomial coefficients of the Lagrange polynomial $\ell_i(x) = \prod_{j \ne i} (x - x_j)/(x_i - x_j)$. *Proof:* if $c$ is that coefficient vector, then $(V c)_k = \ell_i(x_k) = \delta_{ik}$, so $V c = e_i$.

**Norm of the inverse (Gautschi 1962).** For distinct nodes in $\mathbb{C}$,
$$\|V^{-1}\|_1 \le \max_{0 \le i \le n} \prod_{j \ne i} \frac{1 + |x_j|}{|x_i - x_j|},$$
with equality when all the nodes are real and of one sign. *Proof.* $\|V^{-1}\|_1$ is the largest column sum of absolute values, that is the largest sum of the absolute values of the coefficients of an $\ell_i$. The coefficients of $\prod_{j \ne i} (x - x_j)$ are, up to sign, the elementary symmetric functions of the $x_j$, and the sum of their absolute values is at most the value of $\prod_{j \ne i} (x + |x_j|)$ at $x = 1$, which is $\prod_{j \ne i} (1 + |x_j|)$. Dividing by $|\prod_{j \ne i} (x_i - x_j)|$ gives the bound. If all $x_j \le 0$, the coefficients of $\prod_{j \ne i}(x - x_j)$ are all nonnegative; if all $x_j \ge 0$, they alternate in sign. In both cases no cancellation occurs and the bound is an equality. $\square$

**Confluent Vandermonde matrix.** If a node $x_i$ repeats $k$ times, the repeated rows are replaced by the derivatives $\frac{d^r}{dx^r}(1, x, \ldots, x^n)\big|_{x = x_i}$ for $r = 0, \ldots, k - 1$. This is the matrix of [Hermite interpolation](/hermite-interpolation/), and it is invertible for distinct base nodes.

## Examples and non-examples

**Three nodes.** For the nodes $1, 2, 3$,
$$V = \begin{pmatrix} 1 & 1 & 1 \\ 1 & 2 & 4 \\ 1 & 3 & 9 \end{pmatrix}, \quad \det V = (2 - 1)(3 - 1)(3 - 2) = 2, \quad V^{-1} = \begin{pmatrix} 3 & -3 & 1 \\ -\tfrac{5}{2} & 4 & -\tfrac{3}{2} \\ \tfrac{1}{2} & -1 & \tfrac{1}{2} \end{pmatrix}.$$
The first column $(3, -\tfrac{5}{2}, \tfrac{1}{2})$ gives $\ell_0(x) = \tfrac{1}{2}(x - 2)(x - 3) = 3 - \tfrac{5}{2}x + \tfrac{1}{2}x^2$. The column sums of $|V^{-1}|$ are $6$, $8$ and $3$, so $\|V^{-1}\|_1 = 8$, and the bound of Gautschi gives $\max(\tfrac{3 \cdot 4}{2}, \tfrac{2 \cdot 4}{1}, \tfrac{2 \cdot 3}{2}) = 8$, an equality because the nodes are positive.

**Non-example: a repeated node.** For the nodes $1, 1, 2$ the first two rows are equal and $\det V = 0 \cdot 1 \cdot 1 = 0$. The interpolation problem with these nodes has no solution or infinitely many; with derivative data it becomes a confluent system.

**Ill-conditioning on a real interval.** The condition number $\kappa_1(V) = \|V\|_1 \|V^{-1}\|_1$, computed with an exact rational inverse, is:

| $n$ | equispaced on $[0, 1]$ | equispaced on $[-1, 1]$ | Chebyshev points of the first kind |
|---|---|---|---|
| 5 | $1.08 \times 10^4$ | 159 | 113 |
| 10 | $3.41 \times 10^8$ | $4.01 \times 10^4$ | $9.25 \times 10^3$ |
| 20 | $3.57 \times 10^{17}$ | $3.19 \times 10^9$ | $6.22 \times 10^7$ |
| 30 | $3.79 \times 10^{26}$ | $2.59 \times 10^{14}$ | $4.18 \times 10^{11}$ |

On $[-1, 1]$ the equispaced column grows by a factor of about 3.1 for each added node and the Chebyshev column by about $1 + \sqrt{2} \approx 2.41$; on $[0, 1]$ the growth is much faster. In double precision ($u \approx 1.1 \times 10^{-16}$) the bound $\kappa u$ on the relative error of the computed coefficients allows the loss of about 11 of the 16 digits at Chebyshev points with $n = 30$, and of all digits at equispaced points on $[0, 1]$, although the interpolant at Chebyshev points is well conditioned ($\Lambda_{30} \approx 3.1$). The bad conditioning belongs to the monomial basis, not to the interpolation problem.

**Non-example of ill-conditioning: roots of unity.** For the nodes $x_k = e^{2\pi i k/N}$, $k = 0, \ldots, N - 1$, the matrix $V/\sqrt{N}$ is unitary, so $\kappa_2(V) = 1$. This $V$ is the [DFT matrix](/dft-matrix/) up to conjugation. Exponential growth is a property of real nodes: Gautschi and Inglese (1988) proved it for positive nodes and for nodes symmetric about 0, and Beckermann (2000) for every set of real nodes.

**Rectangular case.** For $m + 1$ equispaced points on $[0, 1]$ and the powers up to $n$, the normal equations matrix $V^T V$ is a scaled approximation of the [Hilbert matrix](/hilbert-matrix/) $\big(1/(j + k + 1)\big)$ for large $m$, and its condition number is about the square of that of $V$. A polynomial fit through the [normal equations](/normal-equations/) in the monomial basis therefore loses accuracy twice as fast as one by [QR factorization](/qr-decomposition/).

## Related definitions

- [Polynomial interpolation](/polynomial-interpolation/): the problem whose matrix in the monomial basis is $V$.
- [Lagrange interpolation](/lagrange-interpolation/) and [barycentric interpolation](/barycentric-interpolation/): ways to use the columns of $V^{-1}$ without forming $V$.
- [Newton interpolation](/newton-interpolation/): the Newton basis turns $V$ into a lower triangular matrix; the Björck-Pereyra algorithm solves $V c = y$ in $O(n^2)$ operations by this route, and Higham (Chapter 22) shows that it is often far more accurate than Gaussian elimination for positive increasing nodes.
- [DFT matrix](/dft-matrix/): the Vandermonde matrix of the roots of unity.
- [Hilbert matrix](/hilbert-matrix/): the Gram matrix of the monomials on $[0, 1]$, another classic ill-conditioned matrix.
- [Chebyshev polynomials](/chebyshev-polynomials/) and [orthogonal polynomials](/orthogonal-polynomials/): bases whose analogue of $V$ is well conditioned on an interval.

## References
