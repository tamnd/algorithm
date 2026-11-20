---
tag: 9VWB60
kind: algorithm
slug: hp-finite-element-method
name: hp finite element method
aliases:
- hp-FEM
- p-version finite element method
area: scientific-computing/finite-element-practice
level: advanced
summary: "Refines both mesh size h and degree p, small h near singularities and high p where the solution is smooth. On geometric meshes, piecewise analytic solutions converge like exp(-b N^(1/3)) in 2D."
model: real-ram
complexity:
  vars: {N: the number of unknowns}
  time: {average: "Θ(N)"}
  space: {extra: "Θ(N)"}
properties: {deterministic: true, exponential_convergence: true, conforming: true, hierarchic_basis: true}
history:
  year: 1986
  people: [Ivo Babuska, Benqi Guo, Wen Gui]
  note: Guo and Babuska proved exponential convergence of hp-FEM on geometric meshes in 2D in 1986, and Gui and Babuska analyzed the 1D case in the same year.
prereqs: [finite-element-method, lagrange-finite-element, legendre-polynomials]
see_also: [spectral-element-method, adaptive-finite-element-method, static-condensation, residual-error-estimator, dorfler-marking, gauss-lobatto-quadrature, thomas-algorithm, cea-lemma]
sources:
  - paper: doi:10.1007/BF00298636
    title: "B. Guo and I. Babuska, The h-p version of the finite element method. Part 1: The basic approximation results, Computational Mechanics 1(1) (1986) 21-41"
    locator: geometric meshes, linear degree vectors and the exponential rate in 2D
  - paper: doi:10.1007/BF00272624
    title: "B. Guo and I. Babuska, The h-p version of the finite element method. Part 2: General results and applications, Computational Mechanics 1(3) (1986) 203-220"
    locator: the rate exp(-b N^(1/3)) for piecewise analytic solutions on polygons
  - book: isbn:9780198503903
    title: "Christoph Schwab, p- and hp-Finite Element Methods: Theory and Applications in Solid and Fluid Mechanics, Oxford University Press (1998)"
    locator: the 1D analysis on geometric meshes and the hierarchic Legendre basis
  - book: isbn:9780198528692
    title: George Em Karniadakis and Spencer J. Sherwin, Spectral/hp Element Methods for Computational Fluid Dynamics, 2nd edition, Oxford University Press (2005)
    locator: the modal basis of integrated Legendre polynomials and its sparsity
---

The hp finite element method improves a finite element solution in two ways at once: by smaller elements (h refinement) and by higher polynomial degree (p refinement). Where the solution is smooth, a higher degree gives errors that fall faster than any power of the number of unknowns $N$. Near a singularity, such as the corner of an L-shaped domain, high degree does not help much, and small elements graded toward the singular point do. A geometric mesh, with element sizes that shrink by a fixed factor $\sigma$ toward the singularity, combined with degrees that grow linearly away from it, gives exponential convergence: $\exp(-b\sqrt{N})$ in 1D and $\exp(-bN^{1/3})$ in 2D for solutions that are piecewise analytic with corner singularities. Uniform h refinement with a fixed degree can only reach an algebraic rate $N^{-s}$, with $s$ limited by the singularity.

## In plain words

There are two ways to make a finite element solution better. You can cut the elements into smaller ones, or you can use polynomials of higher degree on the same elements. Higher degree is very effective where the solution is smooth, but bad at a sharp corner, where the solution has a kink in its slope. Small elements are the right tool at the corner. The hp method does both: it puts layers of smaller and smaller elements toward the corner, and it uses a low degree on the tiny elements and a higher degree on the large ones farther away. Then the error falls faster than with either tool alone.

## The problem

**Input.** An elliptic boundary value problem with a solution that is analytic except at known points, such as the corners of a polygon. Here the 1D model problem $-u'' = f$ on $(0, 1)$ with $u(0) = u(1) = 0$ and a solution like $u = x^{\alpha} - x$ with $\tfrac12 < \alpha < 1$, singular at 0. Also a number of layers $n$, a grading factor $0 < \sigma < 1$ and a slope $\mu > 0$ for the degrees.

**Output.** The Galerkin solution $u_h$ in the space of continuous piecewise polynomials on the geometric mesh with degree $p_i$ on element $i$, and its energy error $|u - u_h|_1$.

## The algorithm

HP-GEOMETRIC builds the a priori hp space and solves on it. The basis is the hat functions at the nodes plus, on each element, the integrated Legendre bubbles $\psi_k = (P_k - P_{k-2})/\sqrt{2(2k-1)}$, $k = 2, \ldots, p_i$, in the local coordinate $\xi \in [-1, 1]$. In 1D their derivatives are scaled [Legendre polynomials](/legendre-polynomials/), so the bubbles are orthogonal to each other and to the hats in the energy product.

```pseudo id=main
HP-GEOMETRIC(n, sigma, mu, u)
L1  x_0 <- 0; x_i <- sigma^(n - i) for i = 1..n          ▷ n layers toward the singularity at 0
L2  p_i <- max(1, ceil(mu * i)) for i = 1..n              ▷ the degree grows away from the singularity
L3  for each element K_i: add (1 / h_i) [[1, -1], [-1, 1]] to the hat system and its loads to b
L4  V <- solve the tridiagonal hat system                 ▷ the Thomas algorithm
L5  c_ik <- (h_i / 2) * b_ik for k = 2..p_i               ▷ the bubble stiffness is the diagonal 2 / h_i
L6  return V and c
```

The loads are $b_j = \int u'\phi_j'$ and $b_{ik} = \int u'\psi_{ik}'$, which equal $\int f\phi_j$ and $\int f\psi_{ik}$ for the exact solution $u$. In 2D the same basis has bubbles and edge functions that are coupled, and the solve is the main cost. There the interior bubbles are removed first by [static condensation](/static-condensation/).

## Example

**By hand.** Take one element $[0, 1]$ with $p = 2$ and $u = x - x^2$. There are no interior nodes, so the only unknown is the coefficient $c$ of $\psi_2 = \tfrac{3}{2}(\xi^2 - 1)/\sqrt6$. With $x = (\xi + 1)/2$, $u' = 1 - 2x = -\xi$, so $b = \sqrt{3/2}\int_{-1}^1(-\xi)\,\xi\,d\xi = -\tfrac23\sqrt{3/2}$. The stiffness is $2/h = 2$, so $c = b/2 = -\tfrac13\sqrt{3/2}$. Then $u_h(\tfrac12) = c\,\psi_2(0) = -\tfrac13\sqrt{3/2}\cdot(-\tfrac{3}{2\sqrt6}) = \tfrac14 = u(\tfrac12)$, and in fact $u_h = u$, because $u$ is a quadratic. The error identity gives $|u|_1^2 - bc = \tfrac13 - \tfrac13 = 0$.

**Measured.** For $u = x^{0.7} - x$, with $|u|_1^2 = 0.225$, the reference code gives these relative energy errors.

| Method | $N$ | Relative error |
|---|---|---|
| Uniform h, $p = 1$ | 63 | 0.437 |
| Uniform h, $p = 1$ | 255 | 0.331 |
| Uniform h, $p = 1$ | 1023 | 0.251 |
| One element, $p = 8$ | 7 | 0.441 |
| One element, $p = 16$ | 15 | 0.334 |
| One element, $p = 32$ | 31 | 0.253 |
| Geometric, $\sigma = 0.15$, $\mu = \tfrac12$, $n = 8$ | 19 | $8.08 \times 10^{-2}$ |
| Geometric, $n = 12$ | 41 | $1.79 \times 10^{-2}$ |
| Geometric, $n = 16$ | 71 | $3.96 \times 10^{-3}$ |
| Geometric, $n = 20$ | 109 | $8.71 \times 10^{-4}$ |
| Geometric, $n = 24$ | 155 | $1.91 \times 10^{-4}$ |

Uniform h refinement gives $N^{-0.2}$, the rate allowed by $u \in H^{1.2 - \epsilon}$. Higher degree on one element gives $N^{-0.4}$, twice the rate, but still algebraic. With 109 unknowns the hp error is about 290 times smaller than the uniform h error with 1023 unknowns, and the slope of $\ln(\text{error})$ against $\sqrt{N}$ settles at $-0.75$. A geometric mesh with $p = 1$ everywhere stalls at 0.343: the large elements far from the singularity need the higher degree.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). The derivative of $\psi_k$ is $\sqrt{(2k-1)/2}\,P_{k-1}$, so the Legendre orthogonality makes the bubble stiffness diagonal and decouples it from the hats, and lines L4 and L5 solve the Galerkin system exactly. Galerkin orthogonality gives the error identity $|u - u_h|_1^2 = |u|_1^2 - b^{\mathsf T}U$ that the code uses. For the rate, the error is at most the error of any function in the space. On element $[\sigma^{k+1}, \sigma^k]$ the ratio of distance to size is fixed, so $u'$ is analytic in an ellipse of fixed shape around it, and polynomials of degree $p$ approximate it with error $C\sigma^{k(\alpha - 1)}r^{-p}$. The small element at 0 contributes $C\sigma^{n(\alpha - 1/2)}$. Linear degrees balance the two, each term is at most $Cq^n$ with $q < 1$, and $N \le Cn^2$ turns $q^n$ into $\exp(-b\sqrt N)$.

## Complexity

In 1D the hat system is tridiagonal and the bubbles are decoupled, so the solve costs $\Theta(N)$. The loads need quadrature with a number of points that grows with $p$: with $p + c$ Gauss points per bubble on each element, the load costs $O(\sum_i p_i^2)$, which is $O(N\max_i p_i)$. In 2D and 3D the element matrices for degree $p$ have $O(p^{2d})$ entries, and static condensation of the interior bubbles costs $O(p^{3d})$ per element with dense algebra, which is why codes for high $p$ use sum factorization on tensor product elements. Memory is $\Theta(N)$ in 1D.

## Properties

- **Exponential convergence.** For solutions that are piecewise analytic with point singularities, geometric meshes with linear degrees give $\exp(-b\sqrt N)$ in 1D and $\exp(-bN^{1/3})$ in 2D, with $b$ independent of $N$.
- **Hierarchic basis.** Raising $p$ on an element adds new bubbles and keeps the old ones, so the matrix for degree $p$ is a submatrix of the one for $p + 1$.
- **Nodal exactness in 1D.** For $-u'' = f$, the Galerkin solution equals $u$ at every node, whatever the degrees. The bubbles only add the interior detail.
- **Robust grading.** The rate is exponential for every $\sigma \in (0, 1)$ and every $\mu > 0$. Only the constant $b$ depends on them. In this test, $\sigma$ from 0.15 to 0.2 and $\mu$ from 0.5 to 1 all worked.
- **Conforming.** The space is a subspace of $H^1_0$, so [Cea's lemma](/cea-lemma/) holds with the usual constant.

## Variants and improvements

- **hp-adaptivity.** When the singularities are not known, an adaptive loop marks elements by an [error estimator](/residual-error-estimator/) and then decides per element whether to split it or raise its degree. A common test is the decay of the Legendre coefficients of $u_h$ on the element: fast decay means the solution is smooth there, so raise $p$.
- **Spectral elements.** The [spectral element method](/spectral-element-method/) is the p refinement of quadrilaterals or hexahedra with a nodal basis at Gauss-Lobatto points, usually on a fixed mesh.
- **Nodal versus modal bases.** The basis here is modal. A nodal basis at Gauss-Lobatto points spans the same space, with a different conditioning.
- **hp discontinuous Galerkin.** [Discontinuous Galerkin methods](/discontinuous-galerkin-method/) allow a different degree on each element without the conformity constraints, which makes hp-adaptivity simpler.
- **Anisotropic hp.** For boundary layers, elements that are thin in one direction with a high degree along the layer give robust exponential rates.

## When to use it

Use hp-FEM for elliptic problems with smooth data on domains with corners, edges or material interfaces, when high accuracy is needed: structural mechanics, electromagnetics and the computation of stress intensity factors are classical examples. It reaches an accuracy in a few hundred unknowns that h refinement would need millions for. It is less attractive for problems with low regularity everywhere, such as rough coefficients or shocks, where high degree gives no gain.

## Pitfalls

- **Degree at the singularity.** Use a low degree on the smallest elements. A high degree there wastes unknowns, because the solution is not smooth there.
- **Too few layers.** If the mesh grading stops early, the error of the element at the singularity dominates and the rate becomes algebraic.
- **Quadrature.** For high degree, the quadrature must grow with $p$, or the loads and the matrices lose the accuracy that the high degree should give. Near the singularity a special rule or an exact formula is needed.
- **Roundoff in the error identity.** $|u|_1^2 - b^{\mathsf T}U$ subtracts two numbers that are close, so it cannot measure errors below about $10^{-8}$ times $|u|_1$ in double precision.
- **Conditioning.** The condition number of the stiffness matrix grows like a power of $p$, and the power depends on the basis and the dimension. Choose a basis with good conditioning, and use preconditioners made for high degree.
- **Not the same as pure p refinement.** Raising the degree on a fixed mesh is only one part of the method. With a singularity it converges at an algebraic rate, as the table shows.

## Implementations

## History

Engineers used elements of high degree in structural codes in the 1970s, and around 1980 Barna Szabo and Ivo Babuska studied the p refinement of fixed meshes. In 1986 Wen Gui and Babuska analyzed the h, p and hp versions in one dimension, and Benqi Guo and Babuska proved in two papers that geometric meshes with linearly increasing degrees give exponential convergence for piecewise analytic solutions on polygons. Christoph Schwab's 1998 book gave a full account of the theory. Later work extended the results to 3D, to hp-adaptivity with a posteriori estimators and to discontinuous Galerkin methods.

## References
