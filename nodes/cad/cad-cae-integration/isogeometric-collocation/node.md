---
tag: AE2H60
kind: algorithm
slug: isogeometric-collocation
name: Isogeometric collocation
aliases:
- IGA collocation
area: cad/cad-cae-integration
level: research
summary: Auricchio and coauthors' method that enforces the strong form of the equations at Greville or other points instead of integrating, cheap because it needs no quadrature.
solves: [poisson-equation]
model: real-ram
complexity:
  vars: {n: number of spline basis functions, p: spline degree}
  time: {worst: "O(n p^2)"}
  space: {extra: "O(n p)"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2010
  people: [Ferdinando Auricchio, Lourenço Beirão da Veiga, Thomas J. R. Hughes, Alessandro Reali, Giancarlo Sangalli]
  note: Auricchio, Beirão da Veiga, Hughes, Reali and Sangalli proposed collocation at the Greville abscissae of the spline basis of isogeometric analysis in 2010.
prereqs: [isogeometric-analysis, b-spline, collocation-method]
see_also: [galerkin-method, isogeometric-quadrature, k-refinement, curry-schoenberg-theorem, banded-matrix, isogeometric-boundary-element-method, finite-element-method, knot-vector]
sources:
  - paper: doi:10.1142/S0218202510004878
    title: F. Auricchio, L. Beirão da Veiga, T. J. R. Hughes, A. Reali and G. Sangalli, Isogeometric collocation methods, Mathematical Models and Methods in Applied Sciences 20(11), 2010, 2075 to 2107
    locator: the whole paper (collocation at the Greville abscissae, the 1D analysis, and the numerical convergence orders p for even and p - 1 for odd degree)
  - paper: doi:10.1016/j.cma.2013.07.017
    title: D. Schillinger, J. A. Evans, A. Reali, M. A. Scott and T. J. R. Hughes, Isogeometric collocation, cost comparison with Galerkin methods and extension to adaptive hierarchical NURBS discretizations, Computer Methods in Applied Mechanics and Engineering 267, 2013, 170 to 232
    locator: the operation counts of the formation and the solution of collocation and Galerkin systems
  - paper: doi:10.1016/j.cma.2016.09.043
    title: M. Montardini, G. Sangalli and L. Tamellini, Optimal-order isogeometric collocation at Galerkin superconvergent points, Computer Methods in Applied Mechanics and Engineering 316, 2017, 741 to 757
    locator: the introduction (the orders of Greville collocation in the L2, H1 and H2 norms) and the clustered superconvergent points
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter X (derivatives of B-splines) and Chapter XIII (the Schoenberg-Whitney theorem on spline interpolation)
  - paper: doi:10.1137/0710052
    title: Carl de Boor and Blair Swartz, Collocation at Gaussian points, SIAM Journal on Numerical Analysis 10(4), 1973, 582 to 606
    locator: the whole paper, spline collocation for ordinary boundary value problems, the older form of the idea
---

Isogeometric collocation solves a differential equation in the spline space of [isogeometric analysis](/isogeometric-analysis/) by asking the equation, in its strong form, to hold at one point per unknown. The points are usually the Greville abscissae of the [B-spline](/b-spline/) basis. Auricchio, Beirão da Veiga, Hughes, Reali and Sangalli proposed it in 2010 as a cheaper partner of the [Galerkin method](/galerkin-method/): there is no integral, so there is no [quadrature](/isogeometric-quadrature/), and each row of the matrix costs one evaluation of the $p+1$ non-zero basis functions and their derivatives. The price is accuracy: with Greville points the error in $L^2$ decreases like $h^p$ for even degree $p$ and like $h^{p-1}$ for odd $p$, against $h^{p+1}$ for Galerkin. The basis on this page is the B-spline basis, and the discretization is collocation, in 1D.

## In plain words

A spline is a smooth curve built from a row of overlapping bumps, each bump scaled by a number. To solve an equation with a spline, you must choose these numbers. The Galerkin way asks the equation to hold "on average" against every bump, and these averages are integrals that cost many function evaluations.

Collocation asks less. It picks one point for each unknown number, plugs the spline into the equation at that point, and asks the two sides to agree there. Each point gives one linear equation, so the unknowns follow from one linear system. A good choice of points is the "average position" of each bump, which comes from the knots alone. If the true answer is itself one of the splines, collocation finds it exactly.

## The problem

The model problem is the 1D [Poisson equation](/poisson-equation/) with Dirichlet [boundary conditions](/boundary-conditions/):

$$ -u''(x) = f(x) \text{ on } (a, b), \qquad u(a) = g_a, \quad u(b) = g_b. $$

The discrete space is $S_p(\xi) = \operatorname{span}\{N_{1,p}, \ldots, N_{n,p}\}$, the B-splines of degree $p \ge 2$ on an open [knot vector](/knot-vector/) $\xi = (\xi_1, \ldots, \xi_{n+p+1})$, with $\xi_1 = \cdots = \xi_{p+1} = a$, $\xi_{n+1} = \cdots = \xi_{n+p+1} = b$, and interior knots of multiplicity at most $p - 1$. So each function of $S_p$ is $C^1$ and has a second derivative on each knot span. The *Greville abscissae* are the knot averages

$$ \tau_i = \frac{\xi_{i+1} + \xi_{i+2} + \cdots + \xi_{i+p}}{p}, \qquad i = 1, \ldots, n. $$

They satisfy $\tau_1 = a$, $\tau_n = b$ and $\tau_1 < \tau_2 < \cdots < \tau_n$. They are also the abscissae of the control points of the identity: $x = \sum_i \tau_i N_{i,p}(x)$. The method looks for $u_h = \sum_j c_j N_{j,p}$ with

$$ u_h(a) = g_a, \qquad -u_h''(\tau_i) = f(\tau_i) \ (i = 2, \ldots, n-1), \qquad u_h(b) = g_b. $$

That is $n$ linear equations in $n$ unknowns. Where $\tau_i$ falls on a knot at which $u_h''$ jumps, the value is the limit from the right.

## The algorithm

```pseudo id=main
IGA-COLLOCATION(ξ, p, f, g_a, g_b)
L1  n ← |ξ| − p − 1                                ▷ number of basis functions
L2  τ_i ← (ξ_{i+1} + ⋯ + ξ_{i+p}) / p for i = 1..n   ▷ Greville abscissae
L3  row 1: A[1, j] ← N_j(a); b_1 ← g_a
L4  for i = 2 to n − 1 do
L5      A[i, j] ← −N_j''(τ_i) for the p + 1 values of j with N_j(τ_i) ≠ 0 or N_j''(τ_i) ≠ 0
L6      b_i ← f(τ_i)
L7  row n: A[n, j] ← N_j(b); b_n ← g_b
L8  solve the banded system A c = b and return c
```

Lines L3 and L7 are trivial for an open knot vector: $N_1(a) = 1$, $N_n(b) = 1$, and all other basis functions vanish at the ends, so $c_1 = g_a$ and $c_n = g_b$. Line L5 evaluates the second derivatives of the non-zero B-splines at one point with the derivative form of the [Cox-de Boor recursion](/cox-de-boor-recursion/), which gives all $p + 1$ of them in $O(p^2)$ operations. Row $i$ has its non-zeros in the columns of the B-splines whose support holds $\tau_i$, so the matrix is a [banded matrix](/banded-matrix/) of half bandwidth at most $p$. The matrix is not symmetric, unlike the Galerkin matrix.

For a problem in 2D or 3D on a NURBS map $F$ of the parameter square or cube, the points are the tensor products of the 1D Greville abscissae, the rows are the strong form pulled back by $F$ (which needs the first and second derivatives of $F$), and the boundary rows hold the boundary conditions at the Greville points of the boundary. The 1D case shows all the steps.

## Example

**A quadratic case by hand.** Take $p = 2$, two elements on $(0, 1)$, $\xi = (0, 0, 0, \tfrac12, 1, 1, 1)$, so $n = 4$ and $\tau = (0, \tfrac14, \tfrac34, 1)$. On the span $[0, \tfrac12]$ the second derivatives of $N_1, N_2, N_3$ are $8, -12, 4$, and on $[\tfrac12, 1]$ those of $N_2, N_3, N_4$ are $4, -12, 8$. For $f = 1$ and $g_a = g_b = 0$ the system is

$$ \begin{pmatrix} 1 & 0 & 0 & 0 \\ -8 & 12 & -4 & 0 \\ 0 & -4 & 12 & -8 \\ 0 & 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} c_1 \\ c_2 \\ c_3 \\ c_4 \end{pmatrix} = \begin{pmatrix} 0 \\ 1 \\ 1 \\ 0 \end{pmatrix}. $$

With $c_1 = c_4 = 0$ the middle rows read $12 c_2 - 4 c_3 = 1$ and $-4 c_2 + 12 c_3 = 1$, so $c_2 = c_3 = \tfrac18$. The spline is $u_h(x) = x(1 - x)/2$, the exact solution, for example $u_h(\tfrac12) = \tfrac12 \cdot \tfrac18 + \tfrac12 \cdot \tfrac18 = \tfrac18$. This is no accident: the exact solution is a quadratic, so it is in $S_2$, and the theorem below says that collocation then returns it.

**A cubic case.** With $p = 3$ and four elements, $\tau = (0, \tfrac1{12}, \tfrac14, \tfrac12, \tfrac34, \tfrac{11}{12}, 1)$. On a uniform mesh and away from the ends, the Greville points of odd degree lie on the knots, and those of even degree lie at the element midpoints. For $f = 1$ the coefficients are $(0, \tfrac1{24}, \tfrac5{48}, \tfrac{13}{96}, \tfrac5{48}, \tfrac1{24}, 0)$, again the exact solution.

**Convergence for a smooth solution.** For $u = \sin \pi x$, $f = \pi^2 \sin \pi x$, uniform meshes of $n_e$ elements, the largest error over 801 equally spaced points is:

| degree | $n_e = 8$ | $n_e = 16$ | $n_e = 32$ | $n_e = 64$ | observed order |
|---|---|---|---|---|---|
| $p = 2$ | $6.51 \times 10^{-3}$ | $1.61 \times 10^{-3}$ | $4.02 \times 10^{-4}$ | $1.00 \times 10^{-4}$ | 2.0 |
| $p = 3$ | $1.26 \times 10^{-2}$ | $3.20 \times 10^{-3}$ | $8.03 \times 10^{-4}$ | $2.01 \times 10^{-4}$ | 2.0 |
| $p = 4$ | $6.35 \times 10^{-5}$ | $4.69 \times 10^{-6}$ | $3.16 \times 10^{-7}$ | $2.04 \times 10^{-8}$ | 3.95 |
| $p = 5$ | $3.12 \times 10^{-5}$ | $2.06 \times 10^{-6}$ | $1.29 \times 10^{-7}$ | $8.07 \times 10^{-9}$ | 4.0 |

The order is $p$ for even $p$ and $p - 1$ for odd $p$, and the cubic is no better than the quadratic on the same mesh. The largest error of $u_h''$ on the same runs decreases with order $p - 1$ for each degree from 2 to 5. These are measurements on one smooth problem. They agree with the orders that the papers report, given under Complexity.

## Correctness

The method is a [collocation method](/collocation-method/) in a spline space, and two things need proof: the system has exactly one solution, and the method is exact when the solution lies in the space.

**Theorem.** Let $p \ge 2$, let $\xi$ be open with interior knots of multiplicity at most $p - 1$, and let $\tau$ be the Greville abscissae. Then the matrix of lines L3 to L7 is non-singular. So if the exact solution $u$ is in $S_p(\xi)$, the method returns $u_h = u$.

The idea of the proof: if $u_h$ solves the problem with zero data, then $u_h''$ is a spline of degree $p - 2$ that vanishes at the $n - 2$ interior Greville points. The space of such second derivatives has dimension $n - 2$, and the Greville point $\tau_i$ lies strictly inside the support of the $i$-th of its B-splines. The Schoenberg-Whitney theorem then forces $u_h'' = 0$, so $u_h$ is linear, and the boundary rows make it zero. Exactness follows: $u$ itself satisfies all $n$ equations, and the solution is unique. The full proof is below.

The theorem says nothing about the error when $u \notin S_p$. That error is the subject of the convergence results below, which are not proved on this page.

## Complexity

In the [real RAM](/real-ram/) model with $n$ unknowns and degree $p$:

- **Forming the system.** Each of the $n$ rows needs the span of one point, found by binary search in $O(\log n)$, and the second derivatives of $p + 1$ B-splines in $O(p^2)$. So the matrix costs $O(n (p^2 + \log n))$, and with the spans known in order, $O(n p^2)$. Galerkin needs about $p + 1$ quadrature points per element and $(p + 1)^2$ products at each, so $O(n p^3)$ in 1D. In $d$ dimensions a collocation row has $(p + 1)^d$ entries, while Galerkin needs $(p + 1)^d$ quadrature points per element, each adding to $(p + 1)^{2d}$ products. Schillinger and coauthors (2013) count these operations in detail and find that the gap grows with $p$ and $d$.
- **Solving.** The matrix has half bandwidth $p$. Gaussian elimination with partial pivoting on a band of this width takes $O(n p^2)$ time and $O(n p)$ space. The implementation below uses a dense solver, $O(n^3)$, which is enough for the tests.

**Accuracy.** For a smooth solution, uniform meshes of size $h$ and the smoothest splines ($C^{p-1}$), collocation at the Greville abscissae has these orders:

- In $L^2$ and in $H^1$: $O(h^p)$ for even $p$ and $O(h^{p-1})$ for odd $p$. The best approximation in $S_p$ is $O(h^{p+1})$ in $L^2$ and $O(h^p)$ in $H^1$, so the method loses one order in $L^2$ for even $p$ and two for odd $p$, and is optimal in $H^1$ only for even $p$.
- In $H^2$: $O(h^{p-1})$ for every $p$, the best possible order in this norm.

Auricchio and coauthors (2010) report these orders from numerical tests, and Montardini, Sangalli and Tamellini (2017) restate them in this form. The table of the Example measures the same orders in the maximum norm. Galerkin with the same space gives $O(h^{p+1})$ in $L^2$. So for equal accuracy collocation needs a finer mesh or a higher degree, and the cost comparison above has to be made at equal error, as Schillinger and coauthors do.

## Properties

- **No quadrature.** Each row needs one evaluation of the basis and its derivatives, at one point.
- **One point per unknown.** The matrix is square, banded and not symmetric. Its condition number grows like $h^{-2}$, as for the second derivative of any discretization.
- **Exact on the space.** A solution in $S_p$ is reproduced exactly, in particular every polynomial of degree at most $p$.
- **Strong form.** The method needs the second derivative of $u_h$ at the points, so the space must be at least $C^1$; the $C^0$ basis of standard finite elements does not work.
- **Same geometry as IGA.** The geometry stays exact under the refinements of [k-refinement](/k-refinement/), as in Galerkin IGA.

## Variants and improvements

- **Other points.** Demko abscissae, and points related to Galerkin superconvergence: Montardini, Sangalli and Tamellini (2017) choose a subset of the superconvergent points, more than one per element and fewer than two, solved in a least-squares or a clustered way, and reach the optimal order $p + 1$ in $L^2$ for odd $p$.
- **NURBS and multi-patch geometry.** The rows hold the pulled-back operator. At patch interfaces the strong form is replaced by a condition on the fluxes.
- **Hierarchical and local refinement.** Schillinger and coauthors (2013) use collocation on hierarchical NURBS, see [hierarchical B-splines](/hierarchical-b-spline/).
- **Explicit dynamics.** With a lumped mass, collocation gives a time step with one evaluation per node, which is the main use of the method in practice.
- **Systems.** Elasticity, beams and plates use the same idea with one row per component and point.

## When to use it

Use collocation when the cost of forming the system dominates: high degree, 3D, explicit dynamics or nonlinear problems that need many re-assemblies. Use Galerkin when the error per unknown matters most, when the equation has a weak form that the strong form cannot match (rough coefficients, point loads, interfaces), or when symmetry of the matrix is needed. For integral equations on the boundary, collocation is also the common choice, see the [isogeometric boundary element method](/isogeometric-boundary-element-method/).

## Pitfalls

- **An interior knot of multiplicity $p$.** Then $S_p$ holds a function with a kink and $u'' = 0$ on both sides, such as $\min(x, 1 - x)$ for $p = 2$ with a double knot at $\tfrac12$, and the matrix of lines L3 to L7 is singular. Keep the interior multiplicity at most $p - 1$, as the precondition says, or add a row for the jump of $u'$.
- **Expecting Galerkin accuracy.** Doubling the degree from 2 to 3 does not help here: the table shows the cubic worse than the quadratic on the same mesh. Use even degrees, or other points, when the $L^2$ error matters.
- **The value at a knot.** For $p = 2$ the second derivative jumps at each knot. Line L5 must use one fixed side, as the code does with the right limit, or the rows depend on rounding of $\tau_i$.
- **Neumann conditions.** A flux condition at an end is a row with $N_j'$, and it must replace one interior row, not be added to the system, or the matrix is no longer square.
- **Geometry derivatives.** In 2D and 3D the rows need second derivatives of the NURBS map. A geometry map with a weak or a zero Jacobian makes these rows large or undefined, see [volumetric spline parameterization](/volumetric-spline-parameterization/).

## Implementations

## History

Collocation with piecewise polynomials for ordinary boundary value problems is old. De Boor and Swartz (1973) proved the convergence orders of collocation at Gauss points with $C^{m-1}$ splines for equations of order $m$. Isogeometric analysis came in 2005, with Galerkin as its standard discretization. Auricchio, Beirão da Veiga, Hughes, Reali and Sangalli (2010) proposed to collocate at the Greville abscissae of the smooth spline basis, with an analysis of the 1D case and numerical tests of the orders. Schillinger, Evans, Reali, Scott and Hughes (2013) counted the operations against Galerkin and extended the method to hierarchical NURBS. Later work looked for points with better orders, such as the superconvergent points of Montardini, Sangalli and Tamellini (2017).

## References
