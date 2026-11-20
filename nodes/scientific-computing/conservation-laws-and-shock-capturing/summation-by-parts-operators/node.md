---
tag: SK4AFB
kind: technique
slug: summation-by-parts-operators
name: Summation-by-parts operators
aliases:
- SBP-SAT method
area: scientific-computing/conservation-laws-and-shock-capturing
level: advanced
summary: "Difference operators D = H^-1 Q with Q + Q^T = B, a discrete form of integration by parts. With weak boundary terms (SAT) the energy method proves stability for the discrete scheme."
prereqs: [finite-difference-method, boundary-conditions]
see_also: [entropy-stable-scheme, discontinuous-galerkin-method, spectral-element-method, gauss-lobatto-quadrature, von-neumann-stability-analysis, advection-equation, wave-equation, nitsche-method]
sources:
  - paper: doi:10.1016/B978-0-12-208350-1.50012-1
    title: H.-O. Kreiss and G. Scherer, Finite element and finite difference methods for hyperbolic partial differential equations, in C. de Boor (ed.), Mathematical Aspects of Finite Elements in Partial Differential Equations, Academic Press, 1974, 195-212
    locator: the summation-by-parts property and the energy estimate for difference operators
  - paper: doi:10.1016/j.jcp.2014.02.031
    title: Magnus Svärd and Jan Nordström, Review of summation-by-parts schemes for initial-boundary-value problems, Journal of Computational Physics 268 (2014) 17-38
    locator: the definitions, the SAT boundary treatment, the energy method and the accuracy of SBP-SAT schemes
  - paper: "David C. Del Rey Fernández, Jason E. Hicken and David W. Zingg, Review of summation-by-parts operators with simultaneous approximation terms for the numerical solution of partial differential equations, Computers and Fluids 95 (2014) 171-196"
    locator: the general definition, diagonal and dense norms, generalized SBP operators and their link to DG and spectral element methods
---

A summation-by-parts (SBP) operator is a difference approximation $D \approx d/dx$ on the nodes $x_0, \dots, x_n$ of an interval that has the form $D = H^{-1}Q$, where $H$ is symmetric positive definite and

$$Q + Q^{T} = B = \operatorname{diag}(-1, 0, \dots, 0, 1).$$

Then $u^{T}H(Dv) + (Du)^{T}Hv = u_nv_n - u_0v_0$, which is the discrete form of $\int_a^b uv_x\,dx + \int_a^b u_xv\,dx = u(b)v(b) - u(a)v(a)$. $H$ acts as a quadrature rule and defines a discrete norm $\|u\|_H^2 = u^{T}Hu$. Because integration by parts holds exactly, the energy method that proves well-posedness of a PDE also proves stability of the semi-discrete scheme. Boundary conditions are imposed weakly with simultaneous approximation terms (SAT), penalty terms whose strength is chosen to make the energy estimate close. The SBP-SAT method gives provably stable high-order finite difference schemes on bounded domains, and the same structure appears in DG and spectral element methods on Gauss-Lobatto nodes.

## In plain words

A key tool for proving that a wave or flow equation behaves well is integration by parts: it moves a derivative from one function to another and leaves only terms at the ends of the interval. Ordinary difference formulas do not obey an exact discrete version of this rule, so proofs for the equation do not carry over to the computer program, and schemes can blow up near boundaries. SBP operators are difference formulas built so that the rule holds exactly with a matching set of weights. Boundary values are not forced in. Instead, a correction term pulls the solution toward the boundary data, with a strength chosen so the total energy can only go down. Then the stability proof for the equation also works for the program.

## When it applies

- Linear or linearized hyperbolic and parabolic problems on bounded domains where an energy estimate exists for the continuous problem: advection, wave equations, Maxwell's equations, the linearized Euler and Navier-Stokes equations.
- Nonlinear conservation laws, by combining SBP operators with split forms or two-point fluxes to get [entropy stable](/entropy-stable-scheme/) schemes.
- Structured grids or multiblock grids. Blocks are coupled with interface SAT terms, the same way as boundary data.
- High-order finite differences that must be stable near boundaries. Diagonal $H$ is preferred because it keeps the energy estimate valid on curvilinear grids and for variable coefficients.

## The template

```pseudo id=main
SBP-SAT(PDE with an energy estimate, boundary data g)
L1  choose a positive diagonal norm H, a quadrature rule of the required order
L2  choose D = H⁻¹Q with Q + Qᵀ = B, exact for polynomials up to the boundary and interior orders
L3  replace each ∂/∂x by D to get the semi-discrete system
L4  add penalty terms τ H⁻¹ e_k (u_k - g_k) at each boundary node k where data enter
L5  apply the energy method to uᵀHu and choose τ so that all boundary terms are nonpositive
```

For $u_t + au_x = 0$ on $[0, 1]$ with $a > 0$ and inflow $u(0, t) = g(t)$, the scheme is

$$\frac{du}{dt} = -aDu - \tau a H^{-1}e_0(u_0 - g).$$

The energy method with $g = 0$ gives (theorem)

$$\frac{d}{dt}u^{T}Hu = -a\,u^{T}(Q + Q^{T})u - 2\tau a u_0^2 = -a u_n^2 - (2\tau - 1)a u_0^2,$$

which is nonpositive for $\tau \ge \tfrac12$, the same estimate as $\frac{d}{dt}\|u\|^2 = -au(1)^2 + au(0)^2$ for the PDE once the boundary condition is used. The choice $\tau = 1$ is the usual one. With $g \ne 0$ the estimate bounds $\|u\|_H$ by the data.

Two standard diagonal-norm operators, with $h$ the grid spacing:

- **(2,1):** $H = h\,\operatorname{diag}(\tfrac12, 1, \dots, 1, \tfrac12)$, the trapezoidal rule. $D$ is the central difference $(u_{i+1} - u_{i-1})/(2h)$ inside and one-sided $(u_1 - u_0)/h$ and $(u_n - u_{n-1})/h$ at the ends.
- **(4,2):** $H = h\,\operatorname{diag}(\tfrac{17}{48}, \tfrac{59}{48}, \tfrac{43}{48}, \tfrac{49}{48}, 1, \dots)$, the fourth-order central difference inside, and four special rows at each end, which are exact for quadratics only.

The first number is the interior order and the second the boundary order. For a hyperbolic problem the global order is the boundary order plus one, because the less accurate rows touch only a fixed number of nodes (see Svärd and Nordström 2014 for the theory; measured below).

## Classic examples

- [Advection equation](/advection-equation/): the model problem below, with one SAT term at the inflow boundary.
- [Wave equation](/wave-equation/): in first-order form, two SAT terms per boundary give an energy estimate (exercise 2).
- [Spectral element method](/spectral-element-method/): collocation on Gauss-Lobatto nodes is an SBP operator with $H$ the Lobatto weights.
- [Discontinuous Galerkin method](/discontinuous-galerkin-method/): with Lobatto nodes, the numerical fluxes act as SAT terms that couple the elements.
- [Entropy stable schemes](/entropy-stable-scheme/): SBP operators with two-point entropy conservative fluxes give entropy stability for nonlinear laws.

**The (2,1) operator by hand.** With $n = 2$ and $h = \tfrac12$: $H = \operatorname{diag}(\tfrac14, \tfrac12, \tfrac14)$ and

$$D = \begin{pmatrix} -2 & 2 & 0 \\ -1 & 0 & 1 \\ 0 & -2 & 2 \end{pmatrix}, \qquad Q = HD = \begin{pmatrix} -\tfrac12 & \tfrac12 & 0 \\ -\tfrac12 & 0 & \tfrac12 \\ 0 & -\tfrac12 & \tfrac12 \end{pmatrix},$$

so $Q + Q^{T} = \operatorname{diag}(-1, 0, 1)$. For $a = 1$, $g = 0$, $\tau = 1$ and $u = (1, 2, 0)$: $-Du = (-2, 1, 4)$, the SAT term changes the first entry by $-(u_0 - 0)/H_{00} = -4$, so $du/dt = (-6, 1, 4)$. The energy rate is $2\sum_i H_{ii}u_i\,\dot u_i = 2(\tfrac14\cdot(-6) + \tfrac12\cdot 2 + 0) = -1$, and the formula gives $-u_2^2 - (2 - 1)u_0^2 = 0 - 1 = -1$.

**Gauss-Lobatto collocation.** On the three Lobatto nodes $-1, 0, 1$ the Lagrange differentiation matrix and the Lobatto weights are

$$D = \begin{pmatrix} -\tfrac32 & 2 & -\tfrac12 \\ -\tfrac12 & 0 & \tfrac12 \\ \tfrac12 & -2 & \tfrac32 \end{pmatrix}, \qquad H = \operatorname{diag}(\tfrac13, \tfrac43, \tfrac13).$$

Then $Q = HD$ has rows $(-\tfrac12, \tfrac23, -\tfrac16)$, $(-\tfrac23, 0, \tfrac23)$, $(\tfrac16, -\tfrac23, \tfrac12)$, and $Q + Q^{T} = \operatorname{diag}(-1, 0, 1)$. This holds for any number of Lobatto nodes, because the Lobatto rule integrates $u v'$ exactly for polynomials of degree $p$. So the DG spectral element method with Lobatto nodes is an SBP method, and its numerical fluxes play the role of SAT terms.

**Refinement study (measurement).** $u_t + u_x = 0$ on $[0, 1]$, $u_0 = \sin 2\pi x$, inflow $g(t) = \sin(-2\pi t)$, $\tau = 1$, classical RK4 with $\Delta t = 0.5h$, error in the $H$ norm at $T = 0.5$:

| $n$ | (2,1) | rate | (4,2) | rate |
|---|---|---|---|---|
| 20 | 3.405e-2 | | 4.767e-3 | |
| 40 | 8.423e-3 | 2.02 | 5.709e-4 | 3.06 |
| 80 | 2.100e-3 | 2.00 | 7.006e-5 | 3.03 |
| 160 | 5.247e-4 | 2.00 | 8.687e-6 | 3.01 |

The (4,2) operator is fourth order inside but its global order is 3, one more than its boundary order.

## Variations

- **Dense and block norms.** A full or block-diagonal $H$ allows higher boundary accuracy (up to the interior order), but the energy estimate then fails for variable coefficients and curvilinear grids unless extra care is taken.
- **Second-derivative SBP operators** $D_2 = H^{-1}(-M + BS)$ with $M$ symmetric positive semidefinite, for diffusion and wave equations in second-order form.
- **Upwind SBP operators**, pairs $D_+$ and $D_-$ with $Q_+ + Q_-^{T} = B$, which add dissipation at high wavenumbers.
- **Generalized SBP** operators on nodes that do not include the boundary, such as Gauss nodes, with $B = t_Rt_R^{T} - t_Lt_L^{T}$ built from extrapolation vectors.
- **Multidimensional SBP** operators on triangles and tetrahedra, used in entropy stable DG methods.
- **Interface SAT** for multiblock grids and for coupling to other methods; the [Nitsche method](/nitsche-method/) is the finite element relative of weak boundary conditions.

## Pitfalls

- **Strong boundary conditions.** Overwriting $u_0$ with $g$ after each stage breaks the energy estimate and can make high-order schemes unstable. Use the SAT term.
- **Penalty too weak.** With $\tau < \tfrac12$ the estimate fails, and the energy can grow; for example with $\tau = \tfrac14$ the energy rate of $u = (1, 0, 0, 0, 0)$ on the (2,1) grid is positive.
- **Penalty too strong.** A very large $\tau$ is stable but makes the system stiff and shrinks the explicit time step.
- **Expecting interior order globally.** The low-order boundary rows limit the global order, so a "fourth-order" diagonal-norm operator gives third order for hyperbolic problems.
- **Wrong norm in error measures.** Report errors in the $H$ norm or the maximum norm, and note that the boundary weights differ from $h$.
- **Nonlinear problems.** SBP alone does not give stability for nonlinear equations. It needs split forms or entropy conservative fluxes, because the product rule does not hold for $D$.

## Exercises

1. Show that the (2,1) operator is the only SBP operator with $H = h\,\operatorname{diag}(\tfrac12, 1, \dots, 1, \tfrac12)$ that is the central difference inside and has a two-point stencil at each boundary.
2. For the wave equation $u_{tt} = u_{xx}$ in first-order form $(u, v)_t = (v, u)_x$, write the SBP-SAT scheme with the boundary condition $u = 0$ at both ends and choose the penalty so that $u^{T}Hu + v^{T}Hv$ does not grow.
3. Verify $Q + Q^{T} = B$ for the (4,2) operator using its first four rows and the symmetry $D_{n-i, n-j} = -D_{ij}$.

## References
