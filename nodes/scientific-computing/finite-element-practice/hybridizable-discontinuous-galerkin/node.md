---
tag: EC181T
kind: algorithm
slug: hybridizable-discontinuous-galerkin
name: Hybridizable discontinuous Galerkin method
aliases:
- HDG method
area: scientific-computing/finite-element-practice
level: research
summary: A discontinuous Galerkin method that removes the cell unknowns by static condensation, so that the only global unknowns are the traces on the faces.
solves: [poisson-equation]
model: real-ram
complexity:
  vars: {m: the number of cells, k: the polynomial degree}
  time: {worst: "Θ(m k^3)"}
  space: {extra: "Θ(m k + k^2)"}
properties: {deterministic: true, consistent: true, symmetric_positive_definite_trace_system: true, locally_conservative: true, exact_nodal_traces_in_1d_for_k_at_least_1: true}
history:
  year: 2009
  people: [Bernardo Cockburn, Jayadeep Gopalakrishnan, Raytcho Lazarov]
  note: Hybridization of mixed methods goes back to Fraeijs de Veubeke in 1965 and to Arnold and Brezzi in 1985. Cockburn, Gopalakrishnan and Lazarov defined the HDG methods in 2009.
prereqs: [discontinuous-galerkin-method, static-condensation, symmetric-interior-penalty-galerkin]
see_also: [symmetric-interior-penalty-galerkin, mixed-finite-element-method, discontinuous-galerkin-method, static-condensation, raviart-thomas-element, schur-complement, thomas-algorithm, finite-element-method]
sources:
  - paper: doi:10.1137/070706616
    title: Bernardo Cockburn, Jayadeep Gopalakrishnan and Raytcho Lazarov, Unified hybridization of discontinuous Galerkin, mixed, and continuous Galerkin methods for second order elliptic problems, SIAM Journal on Numerical Analysis 47(2) (2009) 1319-1365
    locator: the definition of the HDG methods with the numerical flux q n + tau (u - uhat), the local solvers and the global trace system
  - paper: doi:10.1090/S0025-5718-10-02334-3
    title: Bernardo Cockburn, Jayadeep Gopalakrishnan and Francisco-Javier Sayas, A projection-based error analysis of HDG methods, Mathematics of Computation 79(271) (2010) 1351-1367
    locator: the HDG projection and the order k + 1 for both the scalar and the flux variable
  - paper: doi:10.1090/S0025-5718-06-01895-3
    title: Fatih Celiker and Bernardo Cockburn, Superconvergence of the numerical traces of discontinuous Galerkin and hybridized methods for convection-diffusion problems in one space dimension, Mathematics of Computation 76(257) (2007) 67-96
    locator: the superconvergence of the numerical traces in one space dimension
  - paper: doi:10.1051/m2an/1985190100071
    title: Douglas N. Arnold and Franco Brezzi, Mixed and nonconforming finite element methods, implementation, postprocessing and error estimates, ESAIM Mathematical Modelling and Numerical Analysis 19(1) (1985) 7-32
    locator: the hybridization of mixed methods with Lagrange multipliers on the faces
---

The hybridizable discontinuous Galerkin method (HDG) solves elliptic problems such as $-\Delta u = f$ with two fields, the solution $u$ and its flux $q = -\nabla u$, both discontinuous polynomials on the cells, plus a third field $\hat u$ that lives only on the faces. On each cell the method solves a small problem for $(q, u)$ with $\hat u$ as boundary data, and the flux through a face is $\hat q\cdot n = q\cdot n + \tau(u - \hat u)$ with a stabilization parameter $\tau > 0$. The only global equation is that this flux is the same seen from both sides of each face. After the cell unknowns are removed by [static condensation](/static-condensation/), the global system has only the face unknowns, and it is symmetric positive definite. Both $u$ and $q$ converge with the order $h^{k+1}$.

## In plain words

Picture a chain of rooms with a door between each pair. In each room you can solve the problem alone if somebody tells you the value at the doors. The method makes the door values the only shared unknowns. For a guess of the door values, every room computes its answer and the flow that it sends through its doors. The flow that leaves one room through a door must enter the next room, and this balance gives one equation per door. You solve these door equations first, which is a small system, and then each room finds its own answer from the door values. The rooms do not have to agree at the doors, and a parameter controls how strongly the room values are pulled toward the door values.

## The problem

**Input.** A mesh of a domain $\Omega$, a source $f$, Dirichlet data $g$, a degree $k \ge 0$ and a parameter $\tau > 0$. The reference code takes $\Omega = (0, 1)$, $-u'' = f$, $u(0) = g_0$, $u(1) = g_1$, and $m$ cells $K_j = (x_j, x_{j+1})$ of width $h = 1/m$.

**Output.** Polynomials $q_h, u_h$ of degree $k$ on each cell and the traces $\hat u_h$ on the faces (in 1D, one value $\hat u_e$ at each node), with $\hat u_h = g$ on the boundary and, on every cell $K$ and for all polynomials $r, w$ of degree $k$,

$$(q_h, r)_K - (u_h, \nabla\cdot r)_K + \langle\hat u_h, r\cdot n\rangle_{\partial K} = 0,$$

$$-(q_h, \nabla w)_K + \langle\hat q_h\cdot n, w\rangle_{\partial K} = (f, w)_K, \qquad \hat q_h\cdot n = q_h\cdot n + \tau(u_h - \hat u_h),$$

and on every interior face the two values of $\hat q_h\cdot n$ add up to $0$.

## The algorithm

```pseudo id=main
HDG(f, m, k, tau, g0, g1)                       ▷ -u'' = f on (0, 1), degree k, m cells, h = 1/m
L1  for each cell K_j do
L2      solve the local problem for (q, u) with three right sides: uhat_L = 1, uhat_R = 1, and f
L3      write the end fluxes qhat n as affine functions of (uhat_j, uhat_(j+1))
L4      add minus the end fluxes to rows j and j + 1 of the tridiagonal trace system
L5  move the known values uhat_0 = g0 and uhat_m = g1 to the right side
L6  uhat <- THOMAS(trace system)                ▷ symmetric positive definite
L7  for each cell K_j do (q, u) <- uhat_j s_L + uhat_(j+1) s_R + s_f
L8  return uhat and (q, u) on every cell
```

Lines L1 to L4 are static condensation. The local problem on line L2 has $2(k+1)$ unknowns, and it has one solution for every $\tau > 0$. Since the problem is linear in the data, its solution for any traces is the combination $\hat u_j s_L + \hat u_{j+1}s_R + s_f$ of the three columns, and the cell stores them for line L7. A cell touches only two traces, so the global system is tridiagonal in 1D, and line L6 solves it with the [Thomas algorithm](/thomas-algorithm/). In several dimensions each face carries a polynomial of degree $k$, and the global matrix couples the faces of each cell.

## Example

Take $-u'' = 2$ with $u(0) = u(1) = 0$, so $u = x(1 - x)$, with $m = 2$, $k = 1$, $\tau = 1$ and $h = \frac12$. On each cell $q = q_0 + q_1\xi$ and $u = u_0 + u_1\xi$ with $\xi = (x - x_j)/h$.

| step | result |
|---|---|
| L2, $\hat u_L = 1$ | $q = 2$, $u = 1 - \xi$ |
| L2, $\hat u_R = 1$ | $q = -2$, $u = \xi$ |
| L2, load $f = 2$ | $q = -\frac{6}{13} + \frac{12}{13}\xi$, $u = \frac1{26}$ |
| L3 | left flux $-2\hat u_L + 2\hat u_R + \frac12$, right flux $2\hat u_L - 2\hat u_R + \frac12$ |
| L4, node $x = \frac12$ | row $4\hat u_1 - 1 = 0$ (the two cells give the same numbers) |
| L5, L6 | $\hat u = (0, \frac14, 0)$ |
| L7, cell 0 | $q = -\frac{25}{26} + \frac{12}{13}\xi$, $u = \frac1{26} + \frac14\xi$ |
| L7, cell 1 | $q = \frac1{26} + \frac{12}{13}\xi$, $u = \frac{15}{52} - \frac14\xi$ |

The trace $\hat u_1 = \frac14$ is the exact value $u(\frac12)$. The cell values are not exact, and $u_h(\frac12^-) = \frac{15}{52}$ differs from the trace. With $k = 0$ and the same data the method gives $\hat u_1 = \frac15$, which is not exact.

**Convergence (measurement).** For $u = \sin(\pi x)$ and $\tau = 1$ the reference code gives, at $m = 4, 8, 16, 32$:

| $k$ | $L^2$ errors of $u$ | order | $L^2$ errors of $q$ | order |
|---|---|---|---|---|
| 0 | $0.729$, $0.384$, $0.196$, $0.0991$ | 0.99 | $0.604$, $0.296$, $0.146$, $0.0725$ | 1.01 |
| 1 | $6.53 \times 10^{-2}$, $1.67 \times 10^{-2}$, $4.22 \times 10^{-3}$, $1.06 \times 10^{-3}$ | 2.00 | $5.64 \times 10^{-2}$, $1.40 \times 10^{-2}$, $3.47 \times 10^{-3}$, $8.66 \times 10^{-4}$ | 2.01 |
| 2 | $4.03 \times 10^{-3}$, $5.13 \times 10^{-4}$, $6.46 \times 10^{-5}$, $8.09 \times 10^{-6}$ | 3.00 | $3.66 \times 10^{-3}$, $4.56 \times 10^{-4}$, $5.68 \times 10^{-5}$, $7.09 \times 10^{-6}$ | 3.00 |
| 3 | $3.91 \times 10^{-4}$, $2.45 \times 10^{-5}$, $1.53 \times 10^{-6}$, $9.57 \times 10^{-8}$ | 4.00 | $2.97 \times 10^{-4}$, $1.85 \times 10^{-5}$, $1.15 \times 10^{-6}$, $7.20 \times 10^{-8}$ | 4.00 |

The orders are those of the last refinement. For $k \ge 1$ the largest nodal trace errors are $6.2 \times 10^{-7}$, $9.5 \times 10^{-9}$, $1.5 \times 10^{-10}$ and $2.3 \times 10^{-12}$, the same for every $k$ and $\tau$. They come only from the quadrature of the load, because the traces are exact when the load is exact.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). Testing the local problem with $r = q$ and $w = u$ gives $\|q\|_K^2 + \tau\sum_{\partial K}u^2 = 0$ for zero data, so for $\tau > 0$ the local problem has one solution, and lines L2 to L4 build the flux balance rows exactly. The same test with two sets of traces gives the energy identity

$$\hat v^{\mathsf T} S\hat u = \sum_K\Bigl((q_{\hat u}, q_{\hat v})_K + \tau\sum_{\partial K}(u_{\hat u} - \hat u)(u_{\hat v} - \hat v)\Bigr),$$

so the trace matrix $S$ is symmetric positive definite for every $k \ge 0$ and $\tau > 0$. In 1D with $k \ge 1$, testing the second local equation with $1 - \xi$ and $\xi$ shows that the end fluxes are $(f, 1 - \xi)_K + (\hat u_R - \hat u_L)/h$ at the left end and $(f, \xi)_K - (\hat u_R - \hat u_L)/h$ at the right end. So the trace system is exactly the system of linear finite elements, $\frac1h(2\hat u_e - \hat u_{e-1} - \hat u_{e+1}) = (f, \phi_e)$, for every $\tau$ and $k$, and since linear elements are exact at the nodes in 1D, the traces are the exact values $u(x_e)$. If $u$ is a polynomial of degree at most $k$, the method returns $u$ and $q = -u'$ exactly.

## Complexity

Line L2 solves a dense system of size $2(k+1)$ with three right sides, which costs $\Theta(k^3)$ per cell. Line L3 costs $\Theta(k)$ and line L4 costs $O(1)$, so the loop takes $\Theta(mk^3)$ time. Line L6 costs $\Theta(m)$ and line L7 costs $\Theta(mk)$. The code keeps three columns of length $2(k+1)$ for each cell and one local matrix, which is $\Theta(mk + k^2)$ memory. Discontinuous Galerkin methods such as [SIPG](/symmetric-interior-penalty-galerkin/) couple all $m(k+1)$ cell unknowns. HDG couples only the $m - 1$ interior traces in 1D, and in several dimensions only the face polynomials. For high degrees in 3D this is much smaller than the DG system, but the local solves then dominate the cost.

## Properties

- **Symmetric positive definite global system (theorem).** For every $k \ge 0$ and $\tau > 0$, by the energy identity above.
- **Order $h^{k+1}$ for $u$ and $q$ (theorem).** With $\tau$ of order one, the projection-based analysis of Cockburn, Gopalakrishnan and Sayas gives $h^{k+1}$ for both fields. Mixed methods also have this property, but most DG methods give the flux only with order $h^k$.
- **Exact traces in 1D (theorem).** For $k \ge 1$ the trace system does not depend on $\tau$ or $k$ and equals the linear element system, so the traces are exact at the nodes when the load is integrated exactly. For $k = 0$ this is false: with $u = x^4 - x$ and $m = 4$ the trace errors are $\frac{51}{1280}$, $\frac{3}{40}$ and $\frac{99}{1280}$. In several dimensions the traces are not exact, but they superconverge.
- **Effect of $\tau$ (measurement).** With $\tau = 10$ in place of $1$ the $u$ errors in the table become smaller and the $q$ errors larger, and for $k \ge 1$ the observed orders of $q$ approach $k + 1$ more slowly: $1.94$, $2.96$ and $3.98$ at the last refinement. For $k = 0$ and $\tau = 10$ the order of $u$ is only $0.82$ at $m = 32$.
- **Local conservation.** Taking $w = 1$ in the second local equation gives $\langle\hat q_h\cdot n, 1\rangle_{\partial K} = (f, 1)_K$ on every cell, with a single-valued flux.
- **Local postprocessing.** Because $q_h$ has order $h^{k+1}$, a new local problem on each cell gives an approximation $u_h^*$ of degree $k + 1$ with order $h^{k+2}$ for $k \ge 1$ in several dimensions.

## Variants and improvements

- **Choice of $\tau$.** A constant $\tau$ of order one is common. A $\tau$ that is positive on only one face of each cell gives another member of the family, and the limit $\tau \to \infty$ approaches a continuous Galerkin method. For convection-diffusion, $\tau$ includes an upwind part.
- **Hybridized mixed methods.** With [Raviart-Thomas](/raviart-thomas-element/) spaces for $q$ and no stabilization, the same local-solve and trace structure gives the hybridized [mixed method](/mixed-finite-element-method/) of Arnold and Brezzi. Cockburn, Gopalakrishnan and Lazarov put mixed, HDG and continuous Galerkin methods into one framework with different local solvers.
- **HDG+ and reduced trace spaces.** Using degree $k + 1$ for $u$ and degree $k$ for the traces, with a $\tau$ of order $1/h$, keeps the order with fewer global unknowns.
- **Other equations.** HDG methods exist for Stokes, linear elasticity, Maxwell and compressible flow, where the face unknowns are the traces of velocity or of the tangential field.

## When to use it

Use HDG for high polynomial degrees on unstructured meshes, where a standard discontinuous Galerkin method has too many globally coupled unknowns, and when an accurate flux and local conservation matter, as in porous media flow or convection-dominated transport. The local solves are independent, so they run in parallel. For low degrees on a conforming mesh, continuous Galerkin with static condensation often has a smaller global system, and the HDG trace system is then no advantage.

## Pitfalls

- **$\tau = 0$ without a mixed space.** With equal-degree polynomials for $q$ and $u$, the local problem of line L2 is singular for $\tau = 0$. The energy argument then gives only $q = 0$, and $u = cL_k$, with $L_k$ the Legendre polynomial of degree $k$ on the cell, solves the local problem with zero data. Keep $\tau > 0$.
- **Wrong sign of the normal.** The flux in line L3 uses $n = -1$ at the left end. With the wrong sign the local equations no longer follow from integration by parts, and the exact solution does not satisfy them.
- **Forgetting the $-\tau\hat u$ part of the flux.** The flux of line L3 contains $\tau(u - \hat u)$. If the $-\tau\hat u$ term is dropped, the trace system is no longer the balance of the true fluxes, and the method is not consistent.
- **Comparing $u_h$ with the trace.** At a node $u_h$ from the left, $u_h$ from the right and $\hat u_h$ are three different numbers. Use the trace for nodal values.
- **Postprocessing with $k = 0$.** The flux has only order $h$ for $k = 0$, so the postprocessed solution does not gain an order.

## Implementations

## History

Fraeijs de Veubeke introduced hybridization for finite element models in 1965, with Lagrange multipliers on the faces that remove the continuity constraints between cells. Arnold and Brezzi showed in 1985 that the multipliers of the hybridized mixed method carry information that allows a local postprocessing of higher order. Celiker and Cockburn proved in 2007 the superconvergence of the numerical traces of DG and hybridized methods in one space dimension. In 2009 Cockburn, Gopalakrishnan and Lazarov defined the hybridizable DG methods with the flux $q\cdot n + \tau(u - \hat u)$, and in 2010 Cockburn, Gopalakrishnan and Sayas proved the order $h^{k+1}$ for both fields with a projection designed for the method.

## References
