---
tag: 61XER4
kind: technique
slug: isogeometric-quadrature
name: Quadrature for isogeometric analysis
aliases:
- half-point rule
- weighted quadrature
area: cad/cad-cae-integration
level: advanced
summary: How to integrate the Galerkin matrices of isogeometric analysis. Gauss rules with p + 1 points per element, and rules that use the spline smoothness to need fewer points.
prereqs: [gauss-legendre-quadrature, gauss-quadrature-theorem, b-spline, nurbs, galerkin-method, finite-element-method]
see_also: [isogeometric-analysis, bezier-extraction, k-refinement, degree-of-precision, gaussian-quadrature, partition-of-unity, isogeometric-collocation, finite-cell-method]
sources:
  - paper: doi:10.1016/j.cma.2008.12.004
    title: T. J. R. Hughes, A. Reali and G. Sangalli, Efficient quadrature for NURBS-based isogeometric analysis, Computer Methods in Applied Mechanics and Engineering 199(5-8), 2010, 301 to 313
    locator: Section 1 (Table 1, points per element against continuity), Section 2 (the exact rule with one point every two elements on a uniform mesh, with its proof), Section 3 (rules for macro-elements found numerically) and the Appendix (reduced Gauss rules)
  - paper: doi:10.1016/j.cma.2016.09.013
    title: F. Calabrò, G. Sangalli and M. Tani, Fast formation of isogeometric Galerkin matrices by weighted quadrature, Computer Methods in Applied Mechanics and Engineering 316, 2017, 606 to 622
    locator: Section 1 (the idea and the cost estimates), Section 2 (the univariate rules), Section 4 (multivariate rules and the choice of points), Section 5 (cost), Section 7 (numerical tests)
  - paper: doi:10.1016/j.cma.2004.10.008
    title: "T. J. R. Hughes, J. A. Cottrell and Y. Bazilevs, Isogeometric analysis: CAD, finite elements, NURBS, exact geometry and mesh refinement, Computer Methods in Applied Mechanics and Engineering 194(39-41), 2005, 4135 to 4195"
    locator: the description of the method, element-wise Gauss quadrature on the parametric elements
  - paper: doi:10.1016/j.cma.2014.12.013
    title: "P. Antolin, A. Buffa, F. Calabrò, M. Martinelli and G. Sangalli, Efficient matrix computation for tensor-product isogeometric analysis: the use of sum factorization, Computer Methods in Applied Mechanics and Engineering 285, 2015, 817 to 828"
    locator: the whole paper, sum factorization for element-wise Gauss quadrature
  - book: isbn:9780470748732
    title: J. A. Cottrell, T. J. R. Hughes and Y. Bazilevs, Isogeometric Analysis, Toward Integration of CAD and FEA, Wiley, 2009
    locator: Chapter 3 (NURBS as a basis for analysis, p. 69), the numerical integration of the element matrices
---

In [isogeometric analysis](/isogeometric-analysis/) the [Galerkin method](/galerkin-method/) needs integrals such as the mass entries $M_{ij} = \int_\Omega R_i R_j\,dx$ and the stiffness entries $K_{ij} = \int_\Omega \nabla R_i \cdot \nabla R_j\,dx$, where $R_i$ are the [B-spline](/b-spline/) or [NURBS](/nurbs/) basis functions mapped to the physical domain by the geometry. They are computed with quadrature. The default, inherited from [finite elements](/finite-element-method/), is the tensor [Gauss-Legendre rule](/gauss-legendre-quadrature/) with $p + 1$ points per direction on each element. This page shows when that rule is exact and when it is not, and then two methods that use the smoothness of splines to need fewer points: the rule of Hughes, Reali and Sangalli (2010) with one point every two elements, which they call the half-point rule, and the row by row weighted quadrature of Calabrò, Sangalli and Tani (2017). The two are different methods with different aims.

Notation: degree $p$ in each direction, $d$ the dimension, elements are the nonempty knot spans, $\xi$ the parametric and $x = F(\xi)$ the physical point, $J = \partial x / \partial \xi$ the Jacobian matrix. An $n$-point Gauss rule has [degree of precision](/degree-of-precision/) $2n - 1$ ([Gauss quadrature theorem](/gauss-quadrature-theorem/)).

## In plain words

To build the system of equations, the program must add up products of basis functions over the whole shape. It does this by sampling the products at a few points and adding the samples with weights. The usual way, taken from the finite element method, takes a fixed set of points inside each small piece of the domain. For splines of degree two or three that are smooth across the pieces, this uses more samples than needed, because the samples do not know that the pieces are glued smoothly. Better rules place points across several pieces at once. One rule uses only one point for every two pieces. Another rule changes the weights for each row of the matrix and uses about two points per piece in each direction, whatever the degree.

## When it applies

- You compute Galerkin matrices or load vectors for a spline basis: mass, stiffness, advection or a right-hand side.
- Element-wise Gauss is the safe default for any basis, any geometry and any coefficient, but it is exact only in the setting given below.
- The faster rules of this page need extra structure: high smoothness ($C^{p-1}$ is the case studied in both papers), often a uniform or tensor product mesh, and a code that can loop over macro-elements or over matrix rows instead of over elements.
- For trimmed or immersed domains, the integration over cut elements is a separate problem (see [trimmed isogeometric analysis](/trimmed-isogeometric-analysis/) and the [finite cell method](/finite-cell-method/)). For collocation no integrals are needed (see [isogeometric collocation](/isogeometric-collocation/)).

## The template

The standard element loop in one parametric dimension, for the mass and stiffness matrices. In $d$ dimensions the loop over Gauss points runs over the tensor grid of $(p + 1)^d$ points.

```pseudo id=main
ASSEMBLE(knots t, degree p, geometry control points X, weights w)
L1  for each element e = [t_k, t_{k+1}] with t_k < t_{k+1}:
L2      for each point s_q with weight ω_q of the (p+1)-point Gauss rule on [0, 1]:
L3          u ← t_k + (t_{k+1} − t_k) s_q; evaluate N_{k−p..k}(u) and their derivatives, then R = wN/W
L4          J ← Σ X_i R_i'(u); dx ← ω_q (t_{k+1} − t_k) J
L5          for local a, b: M_ab += R_a R_b dx and K_ab += (R_a'/J)(R_b'/J) dx
L6  return M, K (assembled with the global numbers k − p, ..., k of the local functions)
```

Line L3 can use the [Cox-de Boor recursion](/cox-de-boor-recursion/) or [Bezier extraction](/bezier-extraction/). Line L4 is the derivative of the geometry map $x(u)$.

**When $p + 1$ Gauss points are exact.** Suppose (a) the basis is a B-spline basis, with no rational weights (or with equal weights), (b) the geometry map is affine on each element, $x = A \xi + b$, and (c) the coefficients of the equation are constant. Then the tensor Gauss rule with $p + 1$ points per direction computes $M$ and $K$ exactly.

*Proof.* On one element each $N_a$ is a product of univariate polynomials of degree at most $p$ in each variable. With an affine map, $\nabla_x N_a = A^{-T} \nabla_\xi N_a$ and $dx = |\det A|\,d\xi$ with constant $A$. So $N_a N_b |\det A|$ has degree at most $2p$ in each variable, and $\nabla N_a \cdot \nabla N_b |\det A|$ is a sum of products $\partial_{\xi_r} N_a\, \partial_{\xi_s} N_b$ times constants, each of degree at most $2p$ in each variable, since a partial derivative lowers the degree in its own variable and keeps the others. The univariate rule with $n = p + 1$ points is exact up to degree $2n - 1 = 2p + 1$ by the Gauss quadrature theorem. The tensor rule integrates a product $x_1^{a_1} \cdots x_d^{a_d}$ as the product of the univariate rules, so it is exact for all polynomials of degree at most $2p + 1$ in each variable separately. By linearity it is exact for both integrands. $\square$

**When exactness fails.** Each of the three conditions can fail in practice, and then no rule with a fixed number of points per element is exact, or a larger number is needed.

- *Polynomial but not affine geometry.* In one dimension with a B-spline map of degree $p$, $x'(\xi)$ has degree $p - 1$, so the mass integrand $N_a N_b x'$ has degree $3p - 1$ and needs $\lceil 3p/2 \rceil$ Gauss points. For $p = 2$ that is still 3 points, but for $p = 3$ it is 5. In two dimensions $\det J$ has degree $2p - 1$ in each variable, and the mass integrand degree $4p - 1$, which needs $2p$ points per direction. The stiffness integrand contains $J^{-1}$, a ratio with $\det J$ in the denominator, so it is not a polynomial and no Gauss rule is exact.
- *Rational weights.* A NURBS function $R_a = w_a N_a / W$ is a ratio of polynomials on each element, unless the weight function $W$ is constant there. Then no rule of the form $\sum \omega_q f(\xi_q)$ is exact for all the entries.
- *Variable coefficients.* $\int c(x) R_a R_b$ is exact only if $c \circ F$ is a polynomial of low enough degree.

In these cases the $p + 1$ rule is not exact. It is used because the quadrature error is of higher order than the discretization error for smooth geometry, which is the usual finite element argument with the Strang lemma. This is the standard practice of Hughes, Cottrell and Bazilevs (2005). Hughes, Reali and Sangalli (2010), Appendix, report that on a one-dimensional eigenvalue problem even reduced Gauss rules lose neither stability nor accuracy for the smooth NURBS basis. That is a numerical observation, not a proof.

**Hughes, Reali and Sangalli: one point every two elements.** Take the uniform mesh of the whole real line with knots $jh$, and the space $S$ of splines of degree $p \ge 1$ with $C^{p-1}$ smoothness at every knot (finite sums of the B-splines $N_{j,p}$, with support $(jh, (j + p + 1)h)$). Put the points

$$\xi^{\mathrm{half}}_i = 2ih \text{ for } p \text{ even}, \qquad \xi^{\mathrm{half}}_i = \big(2i + \tfrac12\big)h \text{ for } p \text{ odd}, \qquad i \in \mathbb{Z},$$

all with weight $2h$. Then $\sum_i 2h\, f(\xi^{\mathrm{half}}_i) = \int_{\mathbb{R}} f$ for every $f \in S$. This is Section 2 of their paper.

*Proof.* By linearity it is enough to take $f = N_{j,p}$. Its integral is $h$: the integral of a B-spline is $(t_{j+p+1} - t_j)/(p + 1) = (p + 1)h/(p + 1)$. Let $X$ be the set of points and $Y = X + h$. Then $X \cup Y = \{x_0 + kh : k \in \mathbb{Z}\}$ with $x_0 = 0$ or $h/2$, and

$$\sum_{x \in X \cup Y} N_{j,p}(x) = \sum_k N_{j,p}(x_0 + kh) = \sum_k N_{j-k,p}(x_0) = 1,$$

by translation of the uniform B-splines and the [partition of unity](/partition-of-unity/). Now $N_{j,p}$ is symmetric about the middle of its support: $N_{j,p}(jh + y) = N_{j,p}((j + p + 1)h - y)$. The reflection $x \mapsto (2j + p + 1)h - x$ maps $X$ onto $Y$: for $p$ even it maps the even multiples of $h$ to $(2j + p + 1 - 2i)h$, odd multiples since $p + 1$ is odd; for $p$ odd it maps $(2i + \tfrac12)h$ to $(2j + p + \tfrac12 - 2i)h$, and $p - 2i$ is odd, so the image is in $X + h$. So the sums over $X$ and over $Y$ are equal, each is $\tfrac12$, and the rule gives $2h \cdot \tfrac12 = h$. All sums are finite because the support is bounded. $\square$

The rule has one point per two elements, while element-wise Gauss needs $\lceil (p + 1)/2 \rceil$ points per element for the same functions, which have degree $p$ on each element. The space has one degree of freedom per element, and the rule uses half of that, which is why the authors call it the half-point rule and state the rule of thumb that optimal rules use about half as many points as the space has functions. The rule is exact for the space $S$ of degree $p$ only. A mass integrand $N_a N_b$ has degree $2p$ and only $C^{p-1}$ smoothness, so it is outside $S$, and the rule is not exact for it (see the example below). For such integrands Section 3 of the paper computes rules numerically on macro-elements, in two dimensions, for $C^0$ bilinear and $C^1$ biquadratic splines and for mass, stiffness and advection matrices. These rules also use about half as many points as the space has functions.

**Calabrò, Sangalli and Tani: weighted quadrature.** Write the mass entry as $M_{ij} = \int c\, B_j \,(B_i\, d\xi)$ and treat $B_i\,d\xi$, the test function times the measure, as the weight of the integral. For each row $i$, choose a rule $Q_i(g) = \sum_q \omega_{i,q}\, g(\xi_q)$ with points shared by all rows and weights for row $i$ only, and ask that $Q_i(B_j) = \int B_i B_j\,d\xi$ for all $j$. These conditions are linear in the weights, and only the $2p + 1$ functions $B_j$ that meet the support of $B_i$ matter. In the $C^{p-1}$ case the points are the knots and the midpoints of the elements, plus $p + 1$ points on each boundary element, so there are about $2^d$ points per element in $d$ dimensions, whatever $p$ (their Remark 4.1). Then $M_{ij} \approx Q_i(c\, B_j)$, exact when $c$ is constant on a parametric domain. The authors count $O(N_{\mathrm{DOF}}\, p^{d+1})$ floating point operations for the matrix formation, with sum factorization, against $O(N_{\mathrm{DOF}}\, p^{3d})$ for element-wise Gauss (Section 1). In their MATLAB tests the time grows at most like $N_{\mathrm{DOF}}\, p^d$ because memory operations dominate, and the convergence rates stay optimal. Both are measured, not proved.

## Classic examples

**Gauss, exact case.** For B-splines of degree $p = 1, \ldots, 4$ on 5 uniform elements of $[0, 1]$, and the map $x = 3\xi$ (geometry control points at 3 times the Greville abscissae, which reproduces a linear map), the $(p + 1)$-point rule gives the mass and stiffness matrices to rounding. The $p$-point rule gives a mass matrix that is wrong by more than $10^{-6}$.

**Gauss, curved map.** Take $p = 3$, knots $(0, 0, 0, 0, \tfrac14, \tfrac12, \tfrac34, 1, 1, 1, 1)$ and a cubic map $x(\xi)$ whose control points are the Greville abscissae moved by small multiples of $1/100$. The largest entry error against a 40-point reference is:

| Gauss points per element | mass error | stiffness error |
|---|---|---|
| 4 ($p + 1$) | $1.0 \times 10^{-5}$ | $3.8 \times 10^{-4}$ |
| 5 ($\lceil 3p/2 \rceil$) | rounding ($10^{-16}$) | $2.0 \times 10^{-5}$ |
| 6 | rounding | $7.4 \times 10^{-7}$ |
| 8 | rounding | $5.1 \times 10^{-10}$ |

The mass integrand has degree $3p - 1 = 8$, so 5 points are exact. The stiffness integrand $N_a' N_b' / x'$ is rational, and its error only goes down as points are added.

**One point every two elements.** For $p = 2$ the points are $0, \pm 2h, \pm 4h, \ldots$ For the quadratic B-spline on $(0, 3h)$, which has values $0, \tfrac12, \tfrac12, 0$ at the knots, the rule picks the point $2h$ and gives $2h \cdot \tfrac12 = h$, the exact integral. For the shifted B-spline on $(h, 4h)$ it picks $2h$ again, with value $\tfrac12$. For $p = 1$ the points are $\tfrac12 h, \tfrac52 h, \ldots$, and the hat function on $(0, 2h)$ has the value $\tfrac12$ at $\tfrac12 h$ and $0$ at $\tfrac52 h$, so again $h$. Outside the space the rule fails: the $p = 2$ rule applied to the cubic B-spline on $(0, 4h)$ gives $2h \cdot \tfrac23 = \tfrac43 h$ instead of $h$, and applied to $N^2$ for the quadratic B-spline with $h = 1$ it gives $\tfrac12$ instead of $\int N^2 = \tfrac{11}{20}$.

**Weighted quadrature weights.** On a periodic uniform mesh with $h = 1$ and the test function $B_i$ with support $(i, i + p + 1)$, the points are $i + \tfrac12, i + 1, \ldots, i + p + \tfrac12$ and the exact weights are:

| $p$ | weights |
|---|---|
| 1 | $\tfrac13, \tfrac13, \tfrac13$ |
| 2 | $\tfrac1{15}, \tfrac7{30}, \tfrac25, \tfrac7{30}, \tfrac1{15}$ |
| 3 | $\tfrac1{105}, \tfrac3{35}, \tfrac5{21}, \tfrac13, \tfrac5{21}, \tfrac3{35}, \tfrac1{105}$ |

For $p = 1$ this is the composite Cavalieri-Simpson rule, as the paper notes. The weights of each row sum to $\int B_i = 1$. They reproduce the mass matrix with $c = 1$ exactly. With $c(\xi) = \xi^2$ and $p = 3$ the two entries of rows 3 and 4 are $Q_3(c B_4) = \tfrac{144959}{20160}$ and $Q_4(c B_3) = \tfrac{16087}{2240} = \tfrac{144783}{20160}$: the matrix is no longer symmetric, which the authors also note (Remark 7.1).

## Variations

- **Generalized Gaussian rules.** Rules exact for a whole spline space, such as the splines of degree $2p$ with $C^{p-1}$ smoothness that contain the mass integrands, with about half as many points as the space has functions. Their points and weights are found numerically, for example by Newton iteration.
- **Reduced Gauss rules.** Fewer than $p + 1$ points per element. Not exact, but reported to be stable and accurate for smooth splines in the Appendix of Hughes, Reali and Sangalli.
- **Sum factorization.** Keep element-wise Gauss but compute the element matrices of a tensor product basis one direction at a time (Antolin, Buffa, Calabrò, Martinelli and Sangalli 2015). This lowers the cost without changing the rule.
- **Rules on Bezier elements.** With [Bezier extraction](/bezier-extraction/), the Bernstein values at the Gauss points are tabulated once for each degree.

## Pitfalls

- **Exact is not the same as accurate.** With a curved map or NURBS weights, no fixed rule is exact. The $p + 1$ rule is a choice that keeps the convergence rate, not an exact integration.
- **The rule of one point every two elements is for one space.** It is exact for splines of degree $p$, $C^{p-1}$, on a uniform mesh without boundary. It is not exact for the products in a mass or stiffness matrix, it needs changes near the boundary of a patch and for nonuniform knots, and using it as a mass matrix rule makes the matrix wrong.
- **Too few points make the matrix singular.** A rule with fewer points than the rank of the matrix needs (for example a reduced rule on a stiffness matrix) can give spurious zero energy modes, as in classical finite elements. Check the rank or the spectrum.
- **Weighted quadrature changes the code structure.** The loop is over rows, the weights depend on the row, and a matrix with a variable coefficient is not symmetric. Codes that rely on symmetry, such as a Cholesky solver, need the symmetric part or another approach.
- **Counting points is not counting time.** In the tests of Calabrò, Sangalli and Tani memory operations dominate the time for high $p$. Compare wall time, not only the number of points.

## Exercises

1. Show that the 2-point Gauss rule is exact for the mass and stiffness matrices of linear B-splines on any mesh with an affine map, and that one point is not exact for the mass matrix.
2. Prove that for a B-spline geometry of degree $p$ in two dimensions, $\det J$ has degree at most $2p - 1$ in each variable, and conclude that $2p$ points per direction integrate the mass matrix exactly.
3. Check the rule of one point every two elements for $p = 3$ on the cubic B-spline on $(0, 4h)$: list the points in the support, their values, and the sum.
4. Show that the trapezoidal rule with one point per knot uses twice as many points as needed for continuous piecewise linear functions on a uniform mesh of the whole line.
5. Derive the weighted quadrature weights $\tfrac13, \tfrac13, \tfrac13$ for $p = 1$ from the three exactness conditions $Q_i(B_{i-1}) = \tfrac16$, $Q_i(B_i) = \tfrac23$, $Q_i(B_{i+1}) = \tfrac16$.

## References
