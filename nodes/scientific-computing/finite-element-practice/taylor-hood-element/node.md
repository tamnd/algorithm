---
tag: 7PW0QN
kind: definition
slug: taylor-hood-element
name: Taylor-Hood element
aliases:
- P2-P1 element
area: scientific-computing/finite-element-practice
level: core
summary: Continuous quadratic velocity with continuous linear pressure. In 2D this pair is inf-sup stable for Stokes flow on every triangulation with at least three triangles.
prereqs: [inf-sup-condition, lagrange-finite-element, mixed-finite-element-method]
see_also: [inf-sup-condition, mixed-finite-element-method, navier-stokes-equations, lagrange-finite-element, raviart-thomas-element, streamline-upwind-petrov-galerkin, schur-complement, minres]
sources:
  - paper: doi:10.1016/0045-7930(73)90027-3
    title: C. Taylor and P. Hood, A numerical solution of the Navier-Stokes equations using the finite element technique, Computers and Fluids 1(1) (1973) 73-100
    locator: the finite element solution of the Navier-Stokes equations with quadratic velocity and linear pressure on triangles
  - paper: doi:10.1137/0728032
    title: F. Brezzi and R. S. Falk, Stability of higher-order Hood-Taylor methods, SIAM Journal on Numerical Analysis 28(3) (1991) 581-590
    locator: the inf-sup stability of the higher-order pairs of continuous velocity of degree k + 1 and continuous pressure of degree k
  - paper: doi:10.1142/S0218202594000133
    title: Daniele Boffi, Stability of higher order triangular Hood-Taylor methods for the stationary Stokes equations, Mathematical Models and Methods in Applied Sciences 4(2) (1994) 223-235
    locator: the abstract, which states that the necessary and sufficient condition on the triangulation is that it contains at least three triangles
  - book: isbn:9783642365188
    title: Daniele Boffi, Franco Brezzi and Michel Fortin, Mixed Finite Element Methods and Applications, Springer Series in Computational Mathematics 44, Springer, 2013
    locator: Chapter 8 (incompressible materials and flow problems), the sections on the Hood-Taylor elements and on other stable and unstable Stokes pairs
---

The Taylor-Hood element is a pair of finite element spaces for the velocity and the pressure of incompressible flow: continuous piecewise quadratic velocities and continuous piecewise linear pressures on a mesh of triangles or tetrahedra. It is the most used stable pair for the Stokes and Navier-Stokes equations in a [mixed finite element method](/mixed-finite-element-method/), because it satisfies the [Babuška-Brezzi conditions](/inf-sup-condition/) with a constant that does not depend on the mesh size on almost every mesh, and it gives second order accuracy.

## Definition

Let $\Omega \subset \mathbb{R}^d$, $d = 2$ or $3$, be a polygon or polyhedron with a conforming triangulation $\mathcal{T}_h$ into simplices. Let $P_k(K)$ be the polynomials of degree at most $k$ on the cell $K$. The **Taylor-Hood pair of order $k \ge 1$** is

$$V_h = \{v \in C^0(\bar\Omega)^d : v|_K \in P_{k+1}(K)^d \text{ for all } K \in \mathcal{T}_h,\ v = 0 \text{ on } \partial\Omega\},$$

$$Q_h = \{q \in C^0(\bar\Omega) : q|_K \in P_k(K) \text{ for all } K \in \mathcal{T}_h,\ \textstyle\int_\Omega q = 0\}.$$

The case $k = 1$ is the element $P_2$-$P_1$. On each cell, the velocity degrees of freedom are the values of each component at the vertices and at the edge midpoints, which are the nodes of the [Lagrange element](/lagrange-finite-element/) of degree 2, and the pressure degrees of freedom are the values at the vertices. For the Stokes problem with viscosity $\nu$, the discrete problem is: find $(u_h, p_h) \in V_h \times Q_h$ with

$$\nu(\nabla u_h, \nabla v) - (\nabla\cdot v, p_h) = (f, v) \quad \text{for all } v \in V_h, \qquad (\nabla\cdot u_h, q) = 0 \quad \text{for all } q \in Q_h.$$

**Stability (theorem).** In 2D, Boffi (1994) proved that the pair of order $k \ge 1$ satisfies the inf-sup bound $\beta_h \ge \beta_0 > 0$ uniformly on a shape-regular family of triangulations, and that the necessary and sufficient condition on the triangulation is that it contains at least three triangles. Brezzi and Falk (1991) had proved the stability of the higher-order pairs under conditions on the mesh, and Boffi treated tetrahedral meshes in a later paper. Together with the theorem of Babuška and Brezzi, this gives for a smooth solution

$$\|u - u_h\|_{H^1} + \|p - p_h\|_{L^2} \le C h^{k+1}\bigl(|u|_{H^{k+2}} + |p|_{H^{k+1}}\bigr),$$

which is $O(h^2)$ for $P_2$-$P_1$ (theorem). The constant $C$ depends on the shape regularity of the mesh family.

**Mass conservation.** The divergence of $u_h$ is a discontinuous piecewise polynomial of degree $k$, and the second equation makes it orthogonal only to the continuous ones. So $\nabla\cdot u_h = 0$ holds in a weak sense but not at each point, and the mass is not conserved exactly on each cell.

## Examples and non-examples

**Example: a mesh of two triangles is too small (theorem, by counting).** Split the unit square along one diagonal into two triangles. The velocity is zero on the boundary, so the only free velocity node is the midpoint of the diagonal, and $\dim V_h = 2$. The pressure has the 4 vertex values with one mean condition, so $\dim Q_h = 3$. The matrix $B$ of the second equation is $3 \times 2$, so some $q_h \ne 0$ in $Q_h$ satisfies $(\nabla\cdot v, q_h) = 0$ for all $v \in V_h$. This $q_h$ is a spurious pressure mode, and $\beta_h = 0$. With the uniform mesh of $2N^2$ triangles on an $N \times N$ grid of squares, the counts are $\dim V_h = 2(2N - 1)^2$ and $\dim Q_h = (N + 1)^2 - 1$, so $N = 2$ already gives $18$ against $8$, and the theorem of Boffi gives stability for every $N \ge 2$.

**Example: the higher-order pairs.** $P_3$-$P_2$ and $P_4$-$P_3$ are Taylor-Hood pairs with $k = 2$ and $k = 3$, with error $O(h^3)$ and $O(h^4)$ for smooth solutions.

**Example: quadrilaterals.** The pair $Q_2$-$Q_1$ of continuous biquadratic velocity and continuous bilinear pressure is the Taylor-Hood pair on quadrilateral and hexahedral meshes, and it is also stable.

**Non-example: $P_1$-$P_1$.** Equal order linear velocity and pressure does not satisfy a uniform inf-sup bound. On structured meshes it has pressure modes that the discrete divergence cannot see, which appear as oscillations in the computed pressure. It is used only with a stabilization term.

**Non-example: $P_1$-$P_0$.** Linear velocity with piecewise constant pressure on the uniform mesh of $2N^2$ triangles has $\dim V_h = 2(N - 1)^2$ and $\dim Q_h = 2N^2 - 1$. Since $\dim Q_h > \dim V_h$, $\beta_h = 0$ (theorem). The velocity is over-constrained and [locks](/finite-element-locking/).

**Non-example: $Q_1$-$P_0$.** Bilinear velocity with piecewise constant pressure on a uniform mesh of squares has the checkerboard pressure mode, with values $+1$ and $-1$ on alternating squares (theorem). Other pressure modes have $\beta_h \to 0$ as $h \to 0$.

## Related definitions

- **MINI element.** Continuous $P_1$ velocity enriched with a cubic bubble function on each triangle, with continuous $P_1$ pressure. It is stable and has first order accuracy, with fewer unknowns than $P_2$-$P_1$.
- **$P_2$-$P_0$.** Quadratic velocity with piecewise constant pressure. It is stable, but the pressure is only first order accurate.
- **Taylor-Hood with discontinuous pressure.** $P_2$ with discontinuous $P_1$ pressure is not stable on general meshes in 2D. Adding a cubic bubble to the velocity gives the Crouzeix-Raviart pair $P_2^+$-$P_1^{\mathrm{disc}}$, which is stable and conserves mass on each cell.
- **Scott-Vogelius pair.** Continuous $P_k$ velocity with discontinuous $P_{k-1}$ pressure, $k \ge 4$ in 2D, on meshes without singular vertices. The discrete velocity is exactly divergence-free.
- **The inf-sup bound** and the error estimate are on the page for the [Babuška-Brezzi theorem](/inf-sup-condition/), and the solution of the indefinite system with [MINRES](/minres/) and the [Schur complement](/schur-complement/) is described on the page for the [mixed method](/mixed-finite-element-method/).

## References
