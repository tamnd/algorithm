---
tag: H4E8X2
kind: algorithm
slug: golub-welsch-algorithm
name: Golub-Welsch algorithm
aliases:
- Golub-Welsch eigenvalue method
- Golub-Welsch method
- Jacobi matrix method for Gauss rules
area: numerical/quadrature
level: advanced
summary: Gets Gaussian nodes and weights from the Jacobi matrix. The nodes are its eigenvalues and the weights are the squared first eigenvector components times the integral of w.
solves: [gauss-nodes-and-weights]
model: floating-point-model
complexity:
  vars: {n: "the number of nodes"}
  time: {worst: "O(n^2)"}
  space: {extra: Θ(n)}
properties: {deterministic: true, any_weight_with_known_recurrence: true, output_is_sorted: true}
history:
  year: 1969
  people: [Gene H. Golub, John H. Welsch]
  note: Golub and Welsch showed in 1969 that the Gauss nodes are the eigenvalues of the symmetric tridiagonal Jacobi matrix and that the weights are the squared first components of its eigenvectors, and computed both with the QR algorithm.
prereqs: [gaussian-quadrature, tridiagonal-eigenproblem]
see_also: [gauss-nodes-and-weights, gauss-quadrature-theorem, qr-algorithm, wilkinson-shift, symmetric-eigenproblem, sturm-sequence-eigenvalue-count, gauss-legendre-quadrature, orthogonal-polynomials]
sources:
  - paper: "Gene H. Golub and John H. Welsch, Calculation of Gauss quadrature rules, Mathematics of Computation 23 (1969) 221-230"
    locator: the Jacobi matrix, the eigenvalues as nodes, the first eigenvector components as weights, and the QR iteration that tracks only those components
  - book: isbn:9780198506720
    title: Walter Gautschi, Orthogonal Polynomials, Computation and Approximation, Oxford University Press, 2004
    locator: Chapter 3, Section 3.1.1 (computation of Gauss-type quadrature rules by the eigenvalue method)
  - paper: "Gene H. Golub, Some modified matrix eigenvalue problems, SIAM Review 15(2) (1973) 318-334"
    locator: the modified Jacobi matrices for Gauss-Radau and Gauss-Lobatto rules
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 19, Clenshaw-Curtis and Gauss quadrature (the Golub-Welsch computation of Gauss-Legendre rules)
  - paper: "Nicholas Hale and Alex Townsend, Fast and accurate computation of Gauss-Legendre and Gauss-Jacobi quadrature nodes and weights, SIAM Journal on Scientific Computing 35(2) (2013) A652-A674"
    locator: the comparison of Golub-Welsch with Newton methods in cost and accuracy for large n
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 2, the section on integration rules of Gauss type (computation of the nodes and weights)
---

The Golub-Welsch algorithm computes the nodes and weights of an $n$-point [Gaussian quadrature](/gaussian-quadrature/) rule for a weight function $w$ from the recurrence coefficients of its [orthogonal polynomials](/orthogonal-polynomials/). The nodes are the eigenvalues of the symmetric tridiagonal Jacobi matrix $J_n$, and the weight of each node is $\int w$ times the square of the first component of the unit eigenvector. The eigenvalue problem is a [symmetric tridiagonal eigenproblem](/tridiagonal-eigenproblem/), solved here by the implicit QL algorithm with a [Wilkinson shift](/wilkinson-shift/) that tracks only the first row of the eigenvector matrix, so the cost is $O(n^2)$ operations.

## In plain words

A Gauss rule needs special points and special weights. The points are the roots of a polynomial, and finding roots of high-degree polynomials directly is fragile. Golub and Welsch noticed that the three-term recurrence of the orthogonal polynomials can be written as a small symmetric matrix with three diagonals. The roots are exactly the eigenvalues of that matrix, and the weights can be read off the first entries of its eigenvectors. Symmetric eigenvalue problems are among the best-understood computations in numerical linear algebra, so this turns a delicate problem into a routine one that works for any weight whose recurrence is known.

## The problem

**Notation.** As on all quadrature pages: $I(f) = \int_a^b f(x)\,w(x)\,dx$; $Q_n(f) = \sum_{i=1}^n w_i f(x_i)$ with $n$ nodes; $E_n(f) = I(f) - Q_n(f)$. The monic orthogonal polynomials satisfy $\pi_{k+1}(x) = (x - \alpha_k)\pi_k(x) - \beta_k\pi_{k-1}(x)$ with $\beta_0 = \int_a^b w$ and $\beta_k > 0$.

Given $n \ge 1$ and $\alpha_0, \ldots, \alpha_{n-1}$, $\beta_0, \ldots, \beta_{n-1}$, compute the nodes $x_1 < \cdots < x_n$ and weights $w_1, \ldots, w_n$ of the Gauss rule, which is exact for all polynomials of degree at most $2n - 1$. The recurrence coefficients of the classical weights are on the [Gaussian quadrature](/gaussian-quadrature/) page. The Jacobi matrix is

$$J_n = \begin{pmatrix} \alpha_0 & \sqrt{\beta_1} & & \\ \sqrt{\beta_1} & \alpha_1 & \ddots & \\ & \ddots & \ddots & \sqrt{\beta_{n-1}} \\ & & \sqrt{\beta_{n-1}} & \alpha_{n-1} \end{pmatrix}.$$

## The algorithm

If $J_n = V \Lambda V^T$ with $V$ orthogonal, the nodes are the diagonal of $\Lambda$ and $w_j = \beta_0 V_{1j}^2$. The QL algorithm builds $V$ as a product of plane rotations; since only its first row is needed, each rotation updates two entries of a vector $z$ instead of two columns of $V$.

```pseudo id=main
GOLUB-WELSCH(α, β, n)                        ▷ n ≥ 1, β_0 = ∫w, β_k > 0
L1  if n < 1 or some β_k ≤ 0 then error
L2  d ← (α_0, …, α_(n−1)); e ← (√β_1, …, √β_(n−1)); z ← (1, 0, …, 0)
L3  for l ← 1 to n do
L4      repeat
L5          m ← the first index ≥ l with |e_m| ≤ u(|d_m| + |d_(m+1)|), or n if none
L6          if m = l then leave the repeat loop        ▷ d_l has converged
L7          σ ← the eigenvalue of the 2×2 block at rows l, l+1 nearer to d_l
L8          one implicit QL sweep with shift σ on rows l..m, by rotations from m−1 up to l
L9          apply each rotation of line L8 to the pair (z_i, z_(i+1))
L10 w_j ← β_0 z_j^2 for each j
L11 sort the pairs (d_j, w_j) by d_j and return them
```

Line L5 looks for a negligible off-diagonal entry below row $l$; the block from row $l$ to row $m$ is then unreduced. When $e_l$ itself is negligible (line L6), $d_l$ is an eigenvalue and the algorithm moves to the next row. Line L8 performs an implicit shifted QL step on the block: it creates a bulge with the first rotation and chases it upward, which is equivalent to factoring $J - \sigma I = QL$ and forming $LQ + \sigma I$. Line L9 multiplies $z$ on the right by the same rotation, which keeps $z = \mathbf{e}_1^T V$ for the accumulated $V$. The rotations never touch $\beta_0$, so the weights come out as $\beta_0 z_j^2$ at the end.

## Example

Take $w = 1$ on $[-1, 1]$ and $n = 3$: $\alpha_k = 0$, $\beta_0 = 2$, $\sqrt{\beta_1} = 0.5773503$, $\sqrt{\beta_2} = 0.5163978$. Each row is one sweep of line L8.

| sweep | block | $d_1$ | $d_2$ | $d_3$ | $\lvert e_1 \rvert$ | $\lvert e_2 \rvert$ |
|---|---|---|---|---|---|---|
| start | | $0$ | $0$ | $0$ | $5.77 \times 10^{-1}$ | $5.16 \times 10^{-1}$ |
| 1 | rows 1 to 3 | $-0.6275546$ | $0.1143544$ | $0.5132002$ | $3.37 \times 10^{-1}$ | $3.89 \times 10^{-1}$ |
| 2 | rows 1 to 3 | $-0.7745201$ | $0.0776130$ | $0.6969071$ | $7.90 \times 10^{-3}$ | $2.33 \times 10^{-1}$ |
| 3 | rows 1 to 3 | $-0.774596669241482$ | $0.0210011$ | $0.7535955$ | $3.25 \times 10^{-8}$ | $1.26 \times 10^{-1}$ |
| 4 | rows 1 to 3 | $-0.7745966692414833$ | $0.0053593$ | $0.7692374$ | $0$ | $6.42 \times 10^{-2}$ |
| 5 | rows 2 to 3 | $-0.7745966692414833$ | $-1.0 \times 10^{-16}$ | $0.7745966692414833$ | $0$ | $1.4 \times 10^{-17}$ |

The entry $|e_1|$ falls as $0.34, 7.9 \times 10^{-3}, 3.2 \times 10^{-8}, 0$, the cubic convergence of the shifted iteration. Then $d_1 = -\sqrt{3/5}$ deflates, and the remaining $2 \times 2$ block converges in one sweep because the shift of line L7 is then an exact eigenvalue. The final vector is $z = (0.5270463, 0.6666667, 0.5270463)$, so the weights are $2z_j^2 = (0.5555556, 0.8888889, 0.5555556) = (\tfrac59, \tfrac89, \tfrac59)$. Indeed $z_2 = \tfrac23$ and $z_1^2 = \tfrac{5}{18}$.

## Correctness

The orthonormal recurrence says $x\,\mathbf{p}(x) = J_n \mathbf{p}(x) + \sqrt{\beta_n}\,p_n(x)\mathbf{e}_n$ for $\mathbf{p}(x) = (p_0(x), \ldots, p_{n-1}(x))^T$, so at each zero $x_j$ of $p_n$ the vector $\mathbf{p}(x_j)$ is an eigenvector with eigenvalue $x_j$. Normalizing it gives $v_{1j}^2 = p_0(x_j)^2/\sum_k p_k(x_j)^2 = \lambda_j/\beta_0$ by the Christoffel formula, which follows from the exactness of the Gauss rule on $p_k p_m$. The QL sweeps are orthogonal similarity transformations, and $z$ collects the first row of their product. The full proof, including the floating-point statement, is in [the correctness proof](proofs/correctness.md).

## Complexity

The cost model counts floating-point operations; the algorithm evaluates no integrand.

- **Per sweep.** A sweep on a block of $k$ rows costs $O(k)$ operations, including the update of $z$, which costs 6 operations per rotation instead of $6n$ for full eigenvectors.
- **Number of sweeps.** The shifted QL iteration converges cubically near the end; the implementation used about 2.1 sweeps per eigenvalue for Gauss-Legendre with $n = 10, 40, 100$. So the total is $O(n^2)$ operations in practice and $\Theta(n)$ extra space. Computing all eigenvectors instead would cost $O(n^3)$.
- **Measured.** In pure Python, $n = 100$ took 0.014 seconds and $n = 400$ took 0.19 seconds, about four times more per doubling.
- **Compared with other methods.** Sturm bisection with the Christoffel formula ([Gaussian quadrature](/gaussian-quadrature/) page) is also $O(n^2)$, with a larger constant. For Gauss-Legendre and Gauss-Jacobi, Newton's method with asymptotic starting values costs $O(n)$ for all nodes and gives better relative accuracy of the weights for $n$ in the thousands (Hale and Townsend 2013). See [computing Gaussian nodes and weights](/gauss-nodes-and-weights/).

## Properties

- **General.** Any weight whose recurrence coefficients are known (exactly or numerically) is handled by the same code.
- **Backward stable eigenvalues.** The computed nodes are the exact eigenvalues of $J_n + \Delta$ with $\|\Delta\| = O(u\|J_n\|)$, so each node has an absolute error of order $u\|J_n\|$. For Gauss-Laguerre, $\|J_n\| \approx 4n$, so the small nodes near $0$ have a larger relative error than the large ones.
- **Weights.** The weights add up to $\beta_0$ up to rounding, because $z$ stays a unit vector under rotations. Against the Christoffel weights of an independent bisection code, the largest relative difference was $4.5 \times 10^{-13}$ for Gauss-Legendre with $n = 100$, and $2.3 \times 10^{-13}$ for Gauss-Hermite with $n = 100$, where the smallest weight is about $6 \times 10^{-79}$.
- **Sorted output.** QL delivers the eigenvalues in no particular order, so line L11 sorts them.

## Variants and improvements

- **Gauss-Radau and Gauss-Lobatto.** Modify the last diagonal entry, or the last row, of $J_{n}$ so that a prescribed endpoint becomes an eigenvalue (Golub 1973); see [Gauss-Radau](/gauss-radau-quadrature/) and [Gauss-Lobatto](/gauss-lobatto-quadrature/).
- **Gauss-Kronrod.** Laurie (1997) computes Kronrod extensions from a modified Jacobi matrix of size $2n + 1$; see [Gauss-Kronrod quadrature](/gauss-kronrod-quadrature/).
- **QR instead of QL.** Golub and Welsch used QR with shifts. QL suits matrices whose entries grow down the diagonal, as for Laguerre; either works.
- **Divide and conquer, MRRR.** Other symmetric tridiagonal eigensolvers also deliver the first eigenvector components in $O(n^2)$ or better.
- **Symmetric weights.** For an even weight ($\alpha_k = 0$) the nodes are symmetric, and the problem can be halved into a bidiagonal singular value problem of size about $n/2$.
- **Newton with asymptotics.** For very large $n$, Glaser, Liu and Rokhlin (2007), Hale and Townsend (2013) and Bogaert (2014) avoid the matrix entirely.

## When to use it

Use Golub-Welsch to build a Gauss rule for a moderate $n$ (up to a few hundred) and for any weight whose recurrence coefficients you have, especially a nonclassical one. It is also the standard way to build Gauss-Radau, Gauss-Lobatto and Gauss-Kronrod rules from modified Jacobi matrices. For Gauss-Legendre with thousands of nodes, or when every weight must have full relative accuracy, use Newton's method with asymptotic starting values.

## Pitfalls

- **Computing all eigenvectors.** A general dense eigensolver costs $O(n^3)$ and stores $n^2$ entries; only the first row of $V$ is needed.
- **Monic instead of symmetric.** The companion-like matrix of the monic recurrence (with $\beta_k$ and $1$ off the diagonal) has the same eigenvalues but is not symmetric, so its eigenvectors are not orthonormal and the weight formula fails. Use $\sqrt{\beta_k}$ on both sides.
- **Forgetting $\beta_0$.** The formula is $w_j = \beta_0 v_{1j}^2$ with $\beta_0 = \int w$; using $\beta_0 = 1$ normalizes the weights to sum to 1. For Gauss-Laguerre with $w = x^a e^{-x}$, $\beta_0 = \Gamma(a + 1)$.
- **Unsorted nodes.** QL and QR return eigenvalues in the order in which they deflate.
- **A sign-changing or zero $\beta_k$.** If some $\beta_k \le 0$, the coefficients do not come from a positive weight, $\sqrt{\beta_k}$ is not real, and Gauss rules may not exist. Line L1 rejects this input.
- **Inaccurate recurrence coefficients.** The algorithm is only as good as $\alpha_k$ and $\beta_k$. Computing them from ordinary moments is ill-conditioned; use modified moments or the discretized Stieltjes procedure (Gautschi, Chapter 2).

## Implementations

## History

Before 1969, Gauss nodes were found as roots of the orthogonal polynomial by Newton's method, and the weights were computed from formulas for each family; for nonclassical weights, tables were built by laborious root finding. Golub and Welsch (Mathematics of Computation, 1969) observed that the recurrence makes the nodes the eigenvalues of the symmetric Jacobi matrix, with the weights given by the first eigenvector components, and computed them with the shifted QR algorithm that tracks only those components. Golub (1973) added the Radau and Lobatto modifications, and Laurie (1997) the Kronrod extension. The method was the standard for decades, until Newton methods with asymptotic starting values (from 2007) became faster for Gauss-Legendre rules with many nodes.

## References
