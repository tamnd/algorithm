---
tag: X122XF
kind: technique
slug: mixed-finite-element-method
name: Mixed finite element method
aliases:
- mixed method
area: scientific-computing/finite-element-practice
level: core
summary: Approximates two unknowns such as flux and pressure together from a saddle point formulation. The pair of spaces must satisfy an inf-sup bound that does not depend on the mesh.
prereqs: [inf-sup-condition, galerkin-method, finite-element-method]
see_also: [inf-sup-condition, taylor-hood-element, raviart-thomas-element, nedelec-element, finite-element-locking, hybridizable-discontinuous-galerkin, schur-complement, minres]
sources:
  - book: isbn:9783642365188
    title: Daniele Boffi, Franco Brezzi and Michel Fortin, Mixed Finite Element Methods and Applications, Springer Series in Computational Mathematics 44, Springer, 2013
    locator: Chapter 3 (algebraic aspects of saddle point problems), Chapter 5 (approximation of saddle point problems), Chapter 7 (mixed methods for elliptic problems) and Chapter 8 (incompressible materials and flow problems)
  - paper: doi:10.1051/m2an/197408R201291
    title: Franco Brezzi, On the existence, uniqueness and approximation of saddle-point problems arising from Lagrangian multipliers, RAIRO Analyse Numérique 8(R2) (1974) 129-151
    locator: the abstract saddle point problem, its discrete approximation and the error estimate
  - paper: doi:10.1007/BFb0064470
    title: P.-A. Raviart and J.-M. Thomas, A mixed finite element method for 2-nd order elliptic problems, in Mathematical Aspects of Finite Element Methods, Lecture Notes in Mathematics 606, Springer, 1977, 292-315
    locator: the mixed formulation of the Poisson problem and the first stable family of flux spaces
  - paper: doi:10.1051/m2an/1985190100071
    title: D. N. Arnold and F. Brezzi, Mixed and nonconforming finite element methods, implementation, postprocessing and error estimates, ESAIM Mathematical Modelling and Numerical Analysis 19(1) (1985) 7-32
    locator: the hybridization of the mixed method with Lagrange multipliers on the edges and the postprocessing of the scalar unknown
---

A mixed finite element method approximates two fields at the same time, for example a flux $\sigma$ and a potential $u$, or a velocity and a pressure, from a variational problem of saddle point form

$$a(\sigma, \tau) + b(\tau, u) = f(\tau) \quad \text{for all } \tau \in V_h, \qquad b(\sigma, v) = g(v) \quad \text{for all } v \in Q_h.$$

The second field is often a [Lagrange multiplier](/lagrange-multiplier/) for a constraint on the first, such as $\nabla\cdot u = 0$ in incompressible flow. The method gives direct and often locally conservative approximations of the quantity of interest, and it avoids [locking](/finite-element-locking/) when a parameter makes a constraint nearly exact. The cost is that $V_h$ and $Q_h$ cannot be chosen independently: the pair must satisfy the [Babuška-Brezzi conditions](/inf-sup-condition/) with constants independent of the mesh size $h$, and the linear system is indefinite.

## In plain words

Some problems ask for two things at once, such as how fast a fluid moves and how hard it pushes, or how much heat flows and how hot it is. A mixed method gives each of the two its own set of shape functions and solves for both together. This lets it get the flow quantity accurately and conserve it cell by cell. The two sets of shape functions must fit each other. If there are too many pressure shapes for the velocity shapes, the pressure can show a chessboard pattern that has nothing to do with the physics. If there are too few, the velocity becomes too stiff. Known good pairs exist, and the theory gives a test that tells which pairs are safe on which meshes.

## When it applies

- The problem has a natural first-order form with two fields: Darcy flow and the Poisson problem in flux form, Stokes and incompressible [Navier-Stokes](/navier-stokes-equations/) flow, nearly incompressible elasticity, the Reissner-Mindlin plate, and Maxwell's equations.
- A constraint is enforced through a multiplier, as in Stokes flow, where the pressure is the multiplier for the divergence constraint.
- The flux or the stress is the quantity of interest, or local conservation on each cell matters, as in porous media flow.
- A primal method locks or loses accuracy when a parameter goes to a limit, such as the Poisson ratio going to $1/2$ (see [locking](/finite-element-locking/)).

It does not apply directly when no stable pair is known for the mesh type, or when an indefinite solver is not acceptable. In those cases a stabilized method or a primal method is used.

## The template

**Notation.** $V$ and $Q$ are Hilbert spaces, $a$ and $b$ are bounded bilinear forms, and $V_h \subset V$ and $Q_h \subset Q$ are finite element spaces with bases $\phi_1, \dots, \phi_n$ and $\psi_1, \dots, \psi_m$. The coefficient vectors are $U$ for the first field and $P$ for the second. $\alpha_h$ is the coercivity constant of $a$ on the discrete kernel and $\beta_h$ is the inf-sup constant of $b$ on $V_h \times Q_h$.

```pseudo id=main
MIXED-FEM(a, b, f, g, mesh)
L1  choose V_h and Q_h with alpha_h ≥ alpha_0 and beta_h ≥ beta_0 on the mesh family   ▷ hole: a stable pair
L2  A[i, j] ← a(φ_j, φ_i) for i, j in 1..n                                    ▷ hole: quadrature for the integrals
L3  B[k, j] ← b(φ_j, ψ_k) for k in 1..m and j in 1..n
L4  F[i] ← f(φ_i) and G[k] ← g(ψ_k)
L5  solve [[A, Bᵀ], [B, 0]] [U; P] = [F; G]                                     ▷ hole: MINRES, Schur complement or hybridization
L6  return σ_h = Σ_j U[j] φ_j and u_h = Σ_k P[k] ψ_k
```

Line L1 is the step that makes the method work or fail. The error estimate of the [Babuška-Brezzi theorem](/inf-sup-condition/) (theorem) is

$$\|\sigma - \sigma_h\|_V + \|u - u_h\|_Q \le C\Bigl(\inf_{\tau_h \in V_h}\|\sigma - \tau_h\|_V + \inf_{v_h \in Q_h}\|u - v_h\|_Q\Bigr),$$

with $C$ depending only on $\alpha_0$, $\beta_0$ and the norms of $a$ and $b$. So the method is as accurate as the best approximation in the two spaces, as long as L1 holds. The matrix in L5 is symmetric when $a$ is symmetric, but it is indefinite: it has $n$ positive and $m$ negative eigenvalues when $A$ is positive definite and $B$ has full row rank. The system is solved with [MINRES](/minres/) and a block-diagonal [preconditioner](/preconditioning/), with the [Schur complement](/schur-complement/) $BA^{-1}B^{\mathsf T}$ when $A$ is easy to invert, or by hybridization, which gives a positive definite system for multipliers on the faces (see [static condensation](/static-condensation/)).

**Mixed Poisson problem in 1D, by hand.** Solve $-u'' = 2$ on $(0, 1)$ with $u(0) = u(1) = 0$, written as $\sigma = -u'$ and $\sigma' = 2$. The exact solution is $u = x(1 - x)$ and $\sigma = 2x - 1$. Multiply $\sigma + u' = 0$ by $\tau$ and integrate by parts: the boundary terms vanish because $u = 0$ at both ends, so the condition on $u$ is natural here. The weak form is $(\sigma, \tau) - (u, \tau') = 0$ and $(\sigma', v) = (2, v)$. Take $m = 2$ cells of width $h = 1/2$, $\sigma_h$ continuous and piecewise linear with nodal values $U = (\sigma_0, \sigma_1, \sigma_2)$, and $u_h$ piecewise constant with values $P = (u_1, u_2)$. The mass matrix and the cell differences are

$$A = \frac{1}{12}\begin{pmatrix} 2 & 1 & 0 \\ 1 & 4 & 1 \\ 0 & 1 & 2\end{pmatrix}, \qquad D = \begin{pmatrix} -1 & 1 & 0 \\ 0 & -1 & 1\end{pmatrix},$$

and the equations are $AU - D^{\mathsf T}P = 0$ and $DU = (1, 1)$. The solution is $U = (-1, 0, 1)$ and $P = (1/6, 1/6)$. Check: $DU = (1, 1)$, and $AU = (-1/6, 0, 1/6) = D^{\mathsf T}P$. The flux is exact at the nodes, and each $u_i$ equals the mean of $x(1 - x)$ over its cell, for example $2\int_0^{1/2}x(1 - x)\,dx = 1/6$.

## Classic examples

- **Stokes flow with the [Taylor-Hood element](/taylor-hood-element/).** Velocity in continuous $P_2$, pressure in continuous $P_1$. Here $a$ is coercive on the whole velocity space, and the work is to prove $\beta_h \ge \beta_0$.
- **Mixed Poisson and Darcy flow with the [Raviart-Thomas element](/raviart-thomas-element/).** Flux in $\mathrm{RT}_k$, potential in discontinuous $P_k$. The divergence of the flux space is exactly the potential space, so the discrete flux is conservative on each cell.
- **Maxwell's equations with the [Nédélec element](/nedelec-element/).** The electric field in $H(\mathrm{curl})$, with a multiplier in $H^1$ for the divergence condition in some formulations.
- **Nearly incompressible elasticity.** Displacement and pressure as two fields remove the [volumetric locking](/finite-element-locking/) of the primal method.
- **Hybridized mixed methods and [HDG](/hybridizable-discontinuous-galerkin/).** The flux space is made discontinuous, and a multiplier on the faces restores normal continuity. Then the cell unknowns are removed by static condensation.

## Variations

- **Hybridization** (Fraeijs de Veubeke, Arnold and Brezzi 1985): a positive definite system for face multipliers, and a postprocessed potential that is one order more accurate.
- **Stabilized mixed methods.** Terms such as $-\delta h^2(\nabla p, \nabla q)$ are added to the second equation so that pairs with $\beta_h = 0$, such as equal-order $P_1$-$P_1$, become stable. This is related to [SUPG](/streamline-upwind-petrov-galerkin/).
- **Augmented Lagrangian** forms add $r(\nabla\cdot u, \nabla\cdot v)$ to $a$, which makes $a$ coercive on the whole space and helps iterative solvers.
- **Exactly divergence-free pairs**, such as the Scott-Vogelius pair on suitable meshes, where the discrete divergence space contains the divergence of every discrete velocity.
- **Discontinuous Galerkin** mixed forms, such as the local DG method and [HDG](/hybridizable-discontinuous-galerkin/), where the stability comes from the numerical flux and not from the choice of the pair.

## Pitfalls

- **Equal-order pairs.** $P_1$-$P_1$ for Stokes flow has $\beta_h \to 0$ or $\beta_h = 0$, and the pressure shows a checkerboard mode. The velocity can still look correct, so check the pressure.
- **Stability depends on the mesh family.** A pair can be stable on one family and unstable on another. For example, Taylor-Hood fails on a mesh of two triangles, and the Scott-Vogelius pair fails on criss-cross meshes. State the family.
- **Counting unknowns is only a heuristic.** If $\dim Q_h > \dim V_h$, the method fails. If $\dim Q_h \le \dim V_h$, it can still fail.
- **Wrong solver.** Conjugate gradients assume a positive definite matrix and can break down on the saddle point system. Use MINRES or GMRES, or a method for the Schur complement.
- **Pressure defined only up to a constant.** With pure Dirichlet conditions on the velocity, fix the mean of the pressure or one pressure value, or the matrix is singular.
- **Wrong norm.** The flux of the mixed Poisson problem belongs to $H(\mathrm{div})$, not to $H^1$. A continuous $P_1$ flux works in 1D, where $H(\mathrm{div}) = H^1$, but in 2D the natural flux spaces are only normally continuous.

## Exercises

1. Repeat the 1D mixed Poisson example with $m = 3$ cells and $f = 2$, and show again that the nodal fluxes are exact and that the potential values are the cell means of $x(1 - x)$.
2. In the 1D example, replace the piecewise constant potential by a continuous piecewise linear one with zero boundary values. Count the unknowns and find a nonzero potential $v$ with $(\tau', v) = 0$ for all $\tau$, or show that none exists.
3. Show that the saddle point matrix $\begin{pmatrix} A & B^{\mathsf T} \\ B & 0\end{pmatrix}$ with $A$ positive definite and $B$ of full row rank has exactly $n$ positive and $m$ negative eigenvalues. Hint: use the block factorization with the Schur complement and Sylvester's law of inertia.
4. Prove the Fortin criterion: if a bounded linear map $\Pi_h : V \to V_h$ satisfies $b(v - \Pi_h v, q_h) = 0$ for all $q_h \in Q_h$, then $\beta_h \ge \beta/\|\Pi_h\|$.

## References
