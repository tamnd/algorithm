---
tag: DX2BFW
kind: algorithm
slug: finite-cell-method
name: Finite cell method
aliases:
- Parvizian-Duster-Rank finite cell method
area: cad/cad-cae-integration
level: advanced
summary: Parvizian, Duster and Rank's fictitious domain method that embeds a part in a grid of high-order cells and integrates only over the material by adaptive quadrature.
solves: [poisson-equation]
model: real-ram
complexity:
  vars: {m: number of active cells, p: polynomial degree, d: bisection depth, g: Gauss points per subcell}
  time: {worst: "O(m (d + 1) g p^2 + (m p)^3)"}
  space: {extra: "O((m p)^2)"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2007
  people: [Jamshid Parvizian, Alexander Düster, Ernst Rank]
  note: Parvizian, Düster and Rank introduced the method in 2007 with h- and p-extension in 2D, and Düster, Parvizian, Yang and Rank extended it to 3D solids in 2008.
prereqs: [finite-element-method, galerkin-method, gauss-legendre-quadrature]
see_also: [cut-finite-element-method, immersogeometric-analysis, trimmed-isogeometric-analysis, adaptive-quadrature, condition-number, signed-distance-function, level-set-method, isogeometric-analysis]
sources:
  - paper: doi:10.1007/s00466-007-0173-y
    title: J. Parvizian, A. Düster and E. Rank, Finite cell method, h- and p-extension for embedded domain problems in solid mechanics, Computational Mechanics 41(1), 2007, 121 to 133
    locator: the whole paper (the fictitious domain with a small stiffness, the high-order cells and the adaptive integration of cut cells)
  - paper: doi:10.1016/j.cma.2008.02.036
    title: A. Düster, J. Parvizian, Z. Yang and E. Rank, The finite cell method for three-dimensional problems of solid mechanics, Computer Methods in Applied Mechanics and Engineering 197(45-48), 2008, 3768 to 3782
    locator: the whole paper, the 3D version with octree integration of the cut cells
  - paper: doi:10.1007/s11831-014-9115-y
    title: D. Schillinger and M. Ruess, The finite cell method, a review in the context of higher-order structural analysis of CAD and image-based geometric models, Archives of Computational Methods in Engineering 22(3), 2015, 391 to 455
    locator: the whole review (cut cell integration, boundary conditions by Nitsche's method, conditioning, CAD and image data)
  - paper: doi:10.1007/s10915-015-9997-3
    title: M. Dauge, A. Düster and E. Rank, Theoretical and numerical investigation of the finite cell method, Journal of Scientific Computing 65(3), 2015, 1039 to 1064
    locator: the whole paper, the analysis of the error caused by the fictitious stiffness alpha
---

The finite cell method (FCM) solves a boundary value problem on a complicated part without a mesh that fits the part. It embeds the part in a simple grid of large cells, uses a high-order basis on the cells, sets the material stiffness to a small value $\alpha$ times the real one outside the part, and integrates the cells that the boundary cuts with an adaptive rule that refines toward the boundary. The geometry enters only through an inside or outside test at the quadrature points, for example a [signed distance function](/signed-distance-function/) or a [level set](/level-set-method/). It differs from the other immersed methods of this site by its high order basis and the small stiffness $\alpha$ in the fictitious part: [CutFEM](/cut-finite-element-method/) stabilizes the cut cells with a ghost penalty instead, [immersogeometric analysis](/immersogeometric-analysis/) integrates the exact CAD boundary in a background spline mesh, and [trimmed isogeometric analysis](/trimmed-isogeometric-analysis/) cuts the CAD patches themselves, with no background mesh. This page shows the method on a 1D bar, where every effect of $\alpha$ can be proved and measured.

## In plain words

Making a mesh that follows every hole and fillet of a part is slow and fails often. The finite cell method skips it. It puts the part inside a box, cuts the box into a few large, equal cells, and gives each cell a rich set of smooth functions.

The space outside the part is filled with a very soft fake material, so that the equations stay solvable. To add up the energy of a cell, the computer asks for each sample point whether it is inside the part. In cells that the border crosses, it uses more and more sample points near the border, to see the border well.

The softer the fake material, the closer the answer gets to that of the part alone. But a very soft fake material makes the equations hard to solve with good accuracy, so in practice it stays small but not zero.

## The problem

The physical problem is a bar $(0, a)$ with stiffness $E > 0$, load $f$, a fixed end and a free or loaded end:

$$ -(E u')' = f \text{ in } (0, a), \qquad u(0) = 0, \qquad E u'(a) = P. $$

It is the 1D form of the [Poisson equation](/poisson-equation/) and of linear elasticity. The bar is embedded in the domain $(0, L)$, $L > a$, cut into $m_0$ equal cells $[x_c, x_{c+1}]$. The point $a$ need not be a cell vertex. The FCM problem on the embedding domain has the stiffness

$$ k_\alpha(x) = E \text{ for } x < a, \qquad k_\alpha(x) = \alpha E \text{ for } x > a, \qquad 0 \le \alpha \le 1, $$

the load $f$ on $(0, a)$ only, the point load $P$ at $a$, and the natural (traction free) condition at $L$. The weak form is: find $u_\alpha \in V_h$ with

$$ \int_0^L k_\alpha \, u_\alpha' v' \, dx = \int_0^a f v \, dx + P v(a) \quad \text{for all } v \in V_h, $$

where $V_h$ is the space of continuous functions with $v(0) = 0$ that are polynomials of degree $p$ on each active cell. A cell is *active* if it holds some material, that is $x_c < a$. Cells that lie fully outside are dropped.

The basis on a cell is the hierarchic p-version basis on $\xi \in [-1, 1]$: the two nodal modes $(1 \mp \xi)/2$, and for $k = 2, \ldots, p$ the integrated Legendre polynomials $N_k = (P_k - P_{k-2})/(2k - 1)$, which vanish at both ends of the cell and have the derivative $P_{k-1}$.

## The algorithm

```pseudo id=main
FINITE-CELL-BAR(cells, p, a, α, f, P)
L1  for each cell c = [x_0, x_1] with x_0 < a do        ▷ cells with no material are dropped
L2      S ← subcells of c: split exactly at a, or bisect toward a to depth d
L3      for each subcell of S and each of its Gauss points x with weight ω do
L4          k ← E if x < a, else α E                     ▷ the inside test
L5          k_e[i][j] += k N_i'(x) N_j'(x) ω; if x < a then f_e[i] += f(x) N_i(x) ω
L6      add k_e and f_e into K and F by the degrees of freedom of c
L7      skip the degree of freedom of the vertex x = 0      ▷ u(0) = 0
L8  solve K u = F
```

Line L2 is where FCM differs from a plain [finite element method](/finite-element-method/). In 2D and 3D the boundary is curved and cannot be followed exactly, so the cut cell is bisected into a quadtree or an octree toward the boundary, and each leaf gets a [Gauss-Legendre rule](/gauss-legendre-quadrature/). Line L4 then takes the coefficient at each Gauss point, so that a leaf crossed by the boundary is integrated with a discontinuous integrand. This is a form of [adaptive quadrature](/adaptive-quadrature/) that trades accuracy for simplicity. In 1D the exact split is possible, and the code offers both, so that the error of the bisection can be measured. The code uses $p + 3$ Gauss points per subcell. A point load $P$ is added to $f_e$ at $x = a$, and the dense solver of line L8 stands in for the sparse or banded solver of a real code.

## Example

**One cell, closed form.** Take $L = 1$ with one cell, $p = 2$, $a = \tfrac12$, $E = 1$, $f = 1$ and $P = 0$. The exact solution is $u = a x - x^2/2$, with $u(a) = \tfrac18$. The space $V_h$ is $\{c_1 x + c_2 x^2\}$, and solving the $2 \times 2$ system by hand gives

$$ u_\alpha(a) - u(a) = \frac{\alpha (1 - \alpha)}{8 (1 + 14 \alpha + \alpha^2)} . $$

So the error is $0$ for $\alpha = 0$, about $\alpha / 8$ for small $\alpha$, and grows with $\alpha$. The code matches this formula to $10^{-14}$ for seven values of $\alpha$.

**A smooth solution, p-extension.** Take $L = 1$, four cells, $a = 0.6$ (inside the third cell), $u = \sin(\pi x / (2a))$, $f = -u''$ and $P = 0$. The table gives the error in the energy norm on $(0, a)$ with the exact split of line L2:

| $p$ | $\alpha = 0$ | $\alpha = 10^{-4}$ | $\alpha = 10^{-8}$ |
|---|---|---|---|
| 2 | $2.3 \times 10^{-2}$ | $2.3 \times 10^{-2}$ | $2.3 \times 10^{-2}$ |
| 3 | $1.0 \times 10^{-3}$ | $1.2 \times 10^{-3}$ | $1.0 \times 10^{-3}$ |
| 4 | $5.2 \times 10^{-5}$ | $8.3 \times 10^{-4}$ | $5.2 \times 10^{-5}$ |
| 5 | $1.4 \times 10^{-6}$ | $2.6 \times 10^{-4}$ | $3.4 \times 10^{-6}$ |
| 6 | $4.7 \times 10^{-8}$ | $4.6 \times 10^{-4}$ | $1.0 \times 10^{-5}$ |
| 7 | $8.9 \times 10^{-10}$ | $1.8 \times 10^{-4}$ | $2.7 \times 10^{-6}$ |
| 8 | $3.4 \times 10^{-11}$ | $2.9 \times 10^{-4}$ | $4.9 \times 10^{-6}$ |

With $\alpha = 0$ the error falls exponentially in $p$, as for a fitted mesh. With $\alpha > 0$ it stalls at a level set by $\alpha$, near $\sqrt{\alpha}$ times a constant once $p$ is large. This is the bound of the Correctness section: the term $\alpha C_{\text{ext}}$ is small for low $p$, but $C_{\text{ext}}$ grows fast with $p$ ($33$ for $p = 2$, $4.7 \times 10^4$ for $p = 4$, $1.1 \times 10^8$ for $p = 6$ and $3.1 \times 10^{11}$ for $p = 8$), and then the bound $\sqrt{\alpha}/2$ takes over.

**Conditioning.** The price of $\alpha = 0$ is the [condition number](/condition-number/) of $K$, which grows from $17$ for $p = 1$ to $1.8 \times 10^{10}$ for $p = 7$ and $5.6 \times 10^{13}$ for $p = 9$ in the same example. At $p = 9$ the error with $\alpha = 0$ ($7.9 \times 10^{-11}$) is already larger than at $p = 8$, an effect of round-off. With $\alpha = 10^{-8}$ the condition number stays below about $6 \times 10^8$ for all $p$ up to 9.

**Bisection.** With $p = 4$ and $\alpha = 10^{-8}$, the largest error on $[0, a]$ for the bisection depths $d = 2, 4, 6, 8, 10$ is $1.2 \times 10^{-3}$, $2.9 \times 10^{-4}$, $7.2 \times 10^{-5}$, $1.8 \times 10^{-5}$ and $4.8 \times 10^{-6}$, and at $d = 16$ it is $2.79 \times 10^{-6}$, against $2.78 \times 10^{-6}$ for the exact split. The error falls by about 4 every two levels, that is about linearly in the size of the leaf that holds $a$. Without bisection ($d = 0$) the cut cell is integrated as if it were all material or all void at each Gauss point, and the error is $6$. The quadrature error, not the basis, limits the method unless the cut cells are integrated well.

## Correctness

The proof page proves four facts for the bar.

1. **The continuous problem is exact.** For every $\alpha > 0$ the FCM solution on $(0, L)$ is the exact solution on $(0, a)$ and is constant on $(a, L)$. The fictitious material carries no force, because the far end is free and it carries no load.
2. **The discrete problem is well posed for $\alpha = 0$.** The stiffness splits as $K = K_0 + \alpha K_1$, with $K_0$ from $(0, a)$ and $K_1$ from the fictitious part. Because only active cells are kept, $K_0$ is symmetric positive definite, so $u_0$ exists, and it is the [Galerkin](/galerkin-method/) solution of the physical bar on the mesh whose last element is the cut part $(x_c, a)$.
3. **The error as $\alpha \to 0$.** In the energy norm $\|v\|_0 = (v^T K_0 v)^{1/2}$ of the physical part,
$$ \|u_\alpha - u_0\|_0 \le \min\left( \alpha \, C_{\text{ext}} \, \|u_0\|_0, \ \tfrac12 \sqrt{\alpha} \, \|u_0\|_1 \right), $$
where $\|v\|_1 = (v^T K_1 v)^{1/2}$ is the energy in the fictitious part and $C_{\text{ext}}$ is the largest eigenvalue of $K_0^{-1} K_1$. So the total energy error is at most the best approximation error of the fitted mesh plus this term, and it tends to that of $\alpha = 0$.
4. **The one-cell formula** of the example.

The test checks both bounds for $p = 2, 4, 6$ and four values of $\alpha$. The rates in $p$, the growth of $C_{\text{ext}}$, the conditioning and the effect of the bisection are measured, not proved. Dauge, Düster and Rank (2015) analyze the effect of $\alpha$ in 2D and 3D.

## Complexity

In the [real RAM](/real-ram/) model, with $m$ active cells, degree $p$, bisection depth $d$ and $g = p + 3$ Gauss points per subcell:

- **Assembly.** A cut cell has $d + 1$ leaves in 1D, because each level splits only the leaf that holds $a$. Each Gauss point costs $O(p)$ for the basis and $O(p^2)$ for the cell matrix, so the assembly costs $O(m (d + 1) g p^2)$. In $\mathbb{R}^k$ a quadtree or octree of depth $d$ has $O(2^{(k-1) d})$ leaves along the boundary, which makes the integration of the cut cells the main cost of FCM in 3D.
- **Solve.** There are $n = m p$ unknowns. The dense solver of the code costs $O(n^3)$ time and $O(n^2)$ space. The matrix is banded with bandwidth $O(p)$ in 1D, so a [banded solver](/banded-matrix/) costs $O(n p^2)$.

## Properties

- **No fitted mesh.** The geometry is only an inside test, so CAD models, voxel images from CT scans and implicit models can all be used directly.
- **High order.** With $\alpha = 0$, a smooth solution and exact integration, the rate in $p$ is that of the p-version of the finite element method, since the cut cell is just a smaller element.
- **A modeling error from $\alpha$.** For $\alpha > 0$ the method solves a slightly different problem, with an error of order $\alpha$ for low $p$ and $\sqrt{\alpha}$ in the worst case.
- **Weak essential conditions.** A Dirichlet condition on a boundary that cuts a cell cannot be set on the degrees of freedom. It is imposed weakly, usually by Nitsche's method or a penalty.
- **Not exact.** The quadrature of cut cells and $\alpha$ both add errors.

## Variants and improvements

- **Spline bases.** B-spline and hierarchical B-spline bases replace the p-version basis, which links FCM to [isogeometric analysis](/isogeometric-analysis/) and to [immersogeometric analysis](/immersogeometric-analysis/).
- **Better cut cell integration.** Moment fitting, the smart octree and the integration on a local tetrahedral subdivision of the cut cells reduce the number of quadrature points compared with plain bisection.
- **Weak boundary conditions.** Nitsche's method for Dirichlet conditions on the cut boundary, as reviewed by Schillinger and Ruess (2015).
- **Stabilization.** Instead of a small $\alpha$, a ghost penalty as in [CutFEM](/cut-finite-element-method/) or the removal of basis functions with small support controls the conditioning.
- **Nonlinear and multi-physics problems.** Plasticity, large deformation and thermal problems on CT data of bones and foams.

## When to use it

Use FCM when the geometry is hard to mesh but easy to query: CT and voxel data, porous and cellular materials, and CAD models with many small features or gaps, as in the [trimmed](/trimmed-isogeometric-analysis/) setting. It pays off most when a high order basis can be used, because the cells are large. Use a fitted mesh when one is cheap, when stresses on the boundary must be very accurate, or when the solution has boundary layers that the cell grid cannot follow.

## Pitfalls

- **A Dirichlet condition on the fictitious part.** If the far end of the embedding domain is clamped instead of free, the fictitious material carries load. For $f = 1$, $u(0) = u(L) = 0$ and $E = 1$, the flux at $a$ becomes $E u'(a^-) = -\alpha a^2 / (2 (L - a + \alpha a))$ instead of $0$. Keep the fictitious boundary free, or impose the physical conditions on the physical boundary only.
- **Integration of the cut cells.** A plain Gauss rule on a cut cell can be very wrong, as the error of $6$ at $d = 0$ shows. Refine toward the boundary, and check the result for convergence in $d$.
- **Small cut cells.** When a cell holds only a sliver of material, $K_0$ is nearly singular and $C_{\text{ext}}$ is very large. Then the bound $\alpha C_{\text{ext}}$ is useless, and the error can reach the $\sqrt{\alpha}$ level.
- **The choice of $\alpha$.** A large $\alpha$ adds a modeling error, and $\alpha = 0$ gives a badly conditioned or singular matrix in floating point. Values from $10^{-6}$ to $10^{-12}$ are common. Check that the result does not change when $\alpha$ is divided by 100.
- **Stresses on the boundary.** The solution is accurate in energy, but values on the cut boundary converge more slowly. Do not read peak stresses off a cut cell without checking them.

## Implementations

## History

Fictitious domain methods, which extend a problem to a simple domain, go back to the 1960s. Parvizian, Düster and Rank (2007) combined the idea with the p-version of the finite element method, a small stiffness $\alpha$ in the fictitious part and adaptive integration of the cut cells, and named it the finite cell method. Düster, Parvizian, Yang and Rank (2008) extended it to 3D solids. Later work used B-spline and hierarchical spline bases, weak boundary conditions, and CAD and image data, as reviewed by Schillinger and Ruess (2015), and Dauge, Düster and Rank (2015) studied the error caused by $\alpha$.

## References
