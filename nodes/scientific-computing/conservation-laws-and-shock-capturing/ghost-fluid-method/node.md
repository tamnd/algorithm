---
tag: 73K8P0
kind: algorithm
slug: ghost-fluid-method
name: Ghost fluid method
area: scientific-computing/conservation-laws-and-shock-capturing
level: advanced
summary: Treats a material interface given by a level set by filling ghost cells with values that carry the interface jump conditions, so it is not smeared.
solves: [euler-equations-of-gas-dynamics, poisson-equation]
model: real-ram
complexity:
  vars: {M: "the number of grid cells", N: "the number of time steps"}
  time: {worst: "Θ(N M)"}
  space: {extra: "Θ(M)"}
properties: {deterministic: true, explicit: true, conservative: false, sharp_interface: true, order_at_interface: "first"}
history:
  year: 1999
  people: [R. P. Fedkiw, T. Aslam, B. Merriman, S. Osher, X.-D. Liu, M. Kang]
  note: Fedkiw, Aslam, Merriman and Osher (1999) introduced the method for compressible flows of two materials. Liu, Fedkiw and Kang (2000) applied the same idea to the Poisson equation with jumps, and Kang, Fedkiw and Liu (2000) to incompressible flow of two fluids.
prereqs: [level-set-method, finite-volume-method, euler-equations-of-gas-dynamics]
see_also: [rusanov-flux, exact-riemann-solver, riemann-problem, particle-level-set, volume-of-fluid-method, front-tracking-method, immersed-boundary-method, stable-fluids]
sources:
  - paper: doi:10.1006/jcph.1999.6236
    title: Ronald P. Fedkiw, Tariq Aslam, Barry Merriman and Stanley Osher, A non-oscillatory Eulerian approach to interfaces in multimaterial flows (the ghost fluid method), Journal of Computational Physics 152(2) (1999) 457-492
    locator: the ghost cells with the pressure and velocity of the real fluid and the entropy of the ghost fluid, the isobaric fix, the one-dimensional tests
  - paper: doi:10.1006/jcph.2000.6444
    title: Xu-Dong Liu, Ronald P. Fedkiw and Myungjoo Kang, A boundary condition capturing method for Poisson's equation on irregular domains, Journal of Computational Physics 160(1) (2000) 151-178
    locator: the one-dimensional derivation with the effective coefficient, the jumps in u and in beta u_n, the convergence proof
  - paper: doi:10.1023/A:1011178417620
    title: Myungjoo Kang, Ronald P. Fedkiw and Xu-Dong Liu, A boundary condition capturing method for multiphase incompressible flow, Journal of Scientific Computing 15(3) (2000) 323-360
    locator: the jumps in density and viscosity and the surface tension as a pressure jump in the projection
---

The ghost fluid method (GFM) computes two fluids that meet at a sharp interface on one fixed grid, without smearing the interface over several cells. A [level set](/level-set-method/) function $\phi$ marks the interface: $\phi < 0$ in one fluid and $\phi > 0$ in the other. Near the interface, each fluid gets ghost cells on the other side. Their values are chosen so that the jump conditions of the interface hold, and then each fluid is computed with an ordinary single-fluid scheme. In compressible flow (Fedkiw, Aslam, Merriman and Osher, 1999), a ghost cell takes the pressure and the velocity of the real fluid in that cell and the entropy of its own fluid. In an incompressible pressure solve (Liu, Fedkiw and Kang, 2000), the known jumps of the pressure and of its normal derivative go into the right-hand side of the Poisson equation, and the matrix stays symmetric. Water, smoke and fire solvers in graphics usually use the simplest case, a free surface where the pressure is zero at the level set, with the fractional distance $\theta$ to the interface in the stencil. The full method adds jumps in density, viscosity and equation of state, surface tension as a pressure jump, and moving material interfaces in gas dynamics. Its price is that it is not exactly conservative, and its error at the interface is of first order.

## In plain words

When water meets air, or one gas meets another, the two materials follow different rules, and a numerical method that mixes them in the cells near the interface gives wrong values there, such as false pressure jumps. The ghost fluid method does not mix. For each material it imagines that the material continues a little beyond the interface, into "ghost" cells. It fills those cells with values that agree with the other material on what must be equal at the interface, the pressure and the speed, and it keeps the material's own character there. Then each material is computed alone with a standard method, and each cell keeps the result of the material that is really in it.

## The problem

Two ideal gases with ratios of specific heats $\gamma_0$ and $\gamma_1$ fill a tube. Each follows the [Euler equations](/euler-equations-of-gas-dynamics/) $U_t + F(U)_x = 0$ with $U = (\rho, \rho u, E)$ and $p = (\gamma_k - 1)(E - \tfrac12\rho u^2)$. They meet at a contact discontinuity, where pressure and velocity are continuous and density, entropy and $\gamma$ jump. The interface moves with the fluid. Compute the flow on a fixed grid of $M$ cells, so that the interface stays sharp and the pressure has no spurious oscillations there.

## The algorithm

Each cell holds $U_i$ and $\phi_i$. The fluid of cell $i$ is $k(i) = 0$ if $\phi_i \le 0$, else $1$. One time step:

```pseudo id=main
GHOST-FLUID-STEP(U, φ, γ_0, γ_1, Δx, Δt)
L1  for k ∈ {0, 1}: in each cell of the other fluid put the ghost state (ρ_g, u, p), with u and p of the real state and ρ_g = (p/s)^(1/γ_k), where s = p/ρ^γ_k at the nearest cell of fluid k
L2      U^(k) ← one step of a single-fluid scheme with γ_k on all cells, real and ghost
L3  φ ← one upwind step of φ_t + u φ_x = 0 with the cell velocities
L4  for each cell i: U_i ← U^(k)_i, where k is the fluid given by the sign of the new φ_i
```

L1 extrapolates the entropy $s = p/\rho^{\gamma_k}$ of fluid $k$ across the interface as a constant, and copies $p$ and $u$, the quantities that are continuous at a contact. The reference code uses the Rusanov flux in L2 and the nearest real cell in L1. In two and three dimensions the constant extrapolation is done by solving $q_\tau \pm n\cdot\nabla q = 0$ for a few pseudo-time steps, with $n = \nabla\phi/|\nabla\phi|$.

**The pressure solve.** For $(\beta u_x)_x = f$ with $\beta = \beta^-$ on the left of an interface at $\alpha$ and $\beta^+$ on the right, and jumps $[u] = a$, $[\beta u_x] = b$, let $x_k \le \alpha < x_{k+1}$ and $\theta = (\alpha - x_k)/\Delta x$. Liu, Fedkiw and Kang replace $\beta$ at the face $k + \tfrac12$ by

$$\hat\beta = \frac{\beta^+\beta^-}{\beta^+\theta + \beta^-(1 - \theta)},$$

add $\hat\beta a/\Delta x^2 + \hat\beta b(1 - \theta)/(\beta^+\Delta x)$ to the right-hand side at node $k$, and add $-\hat\beta a/\Delta x^2 + \hat\beta b\theta/(\beta^-\Delta x)$ at node $k + 1$. All other rows are the standard three-point stencil. The matrix is symmetric and negative definite. In the pressure equation of a projection method, $\beta = 1/\rho$. For water under air with $a = b = 0$, the limit $\beta^+ \to \infty$ gives $\hat\beta = \beta^-/\theta$, which is the free-surface condition $p = 0$ at the interface used in graphics.

## Example

**Ghost values by hand.** Air ($\gamma_0 = 1.4$) with $\rho = 1$, $p = 1$ on the left, and helium ($\gamma_1 = \tfrac53$) with $\rho = 0.125$, $p = 0.1$ on the right, both at rest. For air, the ghost cell on the helium side gets $u = 0$, $p = 0.1$ and the air entropy $s = 1$, so $\rho_g = 0.1^{1/1.4} = 0.1931$. For helium, the ghost cell on the air side gets $p = 1$ and the helium entropy $s = 0.1/0.125^{5/3} = 3.200$, so $\rho_g = (1/3.200)^{3/5} = 0.4976$. Each gas now sees a single-gas shock tube with its own $\gamma$ on the whole grid.

**Moving contact.** $p = 1$ and $u = 0.5$ everywhere, $\rho = 1$ (air) for $x < 0.3$ and $\rho = 0.1$ (helium) to the right, 100 cells, $T = 0.2$. GFM keeps $p$ and $u$ to $10^{-12}$, the density stays a perfect step, and the interface is at $x = 0.4$, within one cell. The conservative one-fluid Rusanov scheme with the $\gamma$ of each cell taken from $\phi$ makes pressure errors larger than 5% at the interface, the oscillations first explained by Abgrall (1996).

**Two-gas shock tube (measurement).** The data of the example by hand, $T = 0.15$, Courant number 0.5. The exact solution, from a two-$\gamma$ exact Riemann solver, has $p^* = 0.3144$ and $u^* = 0.9014$, so the contact is at $x = 0.6352$.

| cells | $L^1$ error of $\rho$, GFM | $L^1$ error of $\rho$, one-fluid | $p$ within 0.03 of the contact, GFM | same, one-fluid | mass error, GFM |
|---|---|---|---|---|---|
| 100 | 2.17e-2 | 2.31e-2 | 0.3143 to 0.3145 | 0.320 to 0.353 | -4.6e-3 |
| 200 | 1.37e-2 | 1.58e-2 | 0.3143 to 0.3143 | 0.256 to 0.365 | -2.8e-3 |
| 400 | 8.84e-3 | 1.06e-2 | 0.3143 to 0.3143 | 0.278 to 0.387 | -1.9e-3 |

GFM has no pressure oscillation at the contact, and the one-fluid scheme has oscillations of about 20% that do not shrink with the grid. The price is a small loss of mass, because each fluid is computed on its own grid and the flux at the interface face is not shared. The interface is at 0.615, 0.6225 and 0.626 for 100, 200 and 400 cells: it lags because the first-order scheme smears the velocity near the interface at early times.

**Pressure solve with jumps.** With $\beta^- = 1$, $\beta^+ = 10$ and a solution that is linear on each side, the discrete solution is exact to rounding. With $u = e^x$ on the left of $\alpha = 0.4321$, $u = \cos x$ on the right, and the matching $f$, $a$ and $b$, the largest error is 3.8e-3, 3.0e-3, 4.6e-4, 1.2e-3 and 3.8e-4 for 20 to 320 cells. It is below $0.25\Delta x$ on every grid. It is first order but not monotone in $\Delta x$, because it depends on $\theta$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows that one GFM step keeps a contact with uniform pressure and velocity exactly in exact arithmetic, for any densities and any two values of $\gamma$: each fluid sees a single-gas contact, which the Rusanov scheme keeps, and the upwind level set step moves a linear $\phi$ exactly with the flow. It also shows that the pressure-solve discretization is exact for solutions that are linear on each side and that its matrix is symmetric and negative definite, so the solve has a unique solution.

## Complexity

One step costs about twice a single-fluid step: two flux sweeps over the grid, plus the extrapolation and the level set step, so $\Theta(M)$ per step and $\Theta(NM)$ in all. In practice only a band of a few cells around the interface needs ghost values, so the second fluid can be computed in a narrow band. The pressure solve is a sparse symmetric system with the same pattern as the standard Poisson matrix, so the same [conjugate gradient](/conjugate-gradient-method/) or [multigrid](/multigrid-method/) solvers work.

## Properties

- The interface is sharp: no cell holds a mixture.
- Contacts with uniform pressure and velocity are kept exactly, with no pressure oscillations.
- Not conservative: mass, momentum and energy change by an amount that goes to zero with the grid, about 0.5% of the mass at 200 cells in the shock tube.
- First order at the interface for the Euler equations and for the Poisson equation with jumps.
- Any single-fluid scheme can be used in L2, including high-order [WENO](/weno-scheme/) schemes.
- The Poisson matrix is symmetric, so conjugate gradients with the usual preconditioners apply.

## Variants and improvements

- **Isobaric fix.** Fedkiw et al. also set the entropy of the first real cells next to the interface from their neighbours, which removes overheating errors when a shock hits a wall or an interface.
- **Real GFM and modified GFM.** For strong shocks at the interface, the ghost states come from a Riemann problem at the interface instead of from the real fluid, which fixes the errors of the original method for large impedance jumps.
- **Boundary condition capturing.** The Poisson form with jumps (Liu, Fedkiw and Kang) and its use for incompressible flow of two fluids with surface tension (Kang, Fedkiw and Liu).
- **Free surfaces in graphics.** One fluid only, $p = 0$ at $\phi = 0$, and the stencil uses $\theta$: the ghost pressure is $p_g = (\theta - 1)p_i/\theta$. Combined with a [particle level set](/particle-level-set/) this is the standard water solver.
- **Flames and detonations.** The interface moves relative to the fluid, and the jump conditions are the Rankine-Hugoniot conditions of a deflagration, as in the graphics [fire model](/fire-simulation/) of Nguyen, Fedkiw and Jensen.
- **Second-order versions.** Symmetric second-order discretizations exist for the Dirichlet case and for some jump problems, at the cost of a more complex stencil.

## When to use it

Use GFM when an interface between materials with different equations of state or properties must stay sharp, and when exact conservation across the interface matters less than the absence of oscillations: multimaterial compressible flow, bubbles and droplets, water and fire in graphics. When exact conservation of mass matters (for example over a long run of a two-phase flow), [volume of fluid](/volume-of-fluid-method/) or conservative cut-cell methods are better. For interfaces that carry forces from elastic bodies, the [immersed boundary method](/immersed-boundary-method/) is the usual choice.

## Pitfalls

- **Extrapolating density instead of entropy.** Constant extrapolation of $\rho$ across a contact with a pressure gradient gives the wrong ghost state. Extrapolate $s$ and compute $\rho$ from $p$ and $s$.
- **Expecting conservation.** The method loses or gains a small amount of mass at the interface in each step. Check the total in long runs.
- **Strong shocks at the interface.** Copying $p$ and $u$ from the real fluid is wrong when a strong shock crosses an interface with a large impedance jump. Use a Riemann-problem based ghost state.
- **Level set drift.** The level set loses its distance property and mass over time. Reinitialize it, or use a particle level set.
- **Small $\theta$ in the pressure solve.** For $\theta \to 0$ the free-surface stencil has a large diagonal entry. Clamp $\theta$ to a small minimum such as $10^{-3}$.
- **Mixing up the sides of the jumps.** $a$ and $b$ are right value minus left value. A sign error gives a solution that looks smooth but is wrong by $O(1)$.

## Implementations

## History

Fedkiw, Aslam, Merriman and Osher (1999) introduced the ghost fluid method for compressible flows with several materials, as a way to avoid the pressure oscillations of conservative capturing schemes at material interfaces, which Abgrall had studied. Liu, Fedkiw and Kang (2000) applied the idea to the Poisson equation, and Kang, Fedkiw and Liu (2000) to incompressible multiphase flow with surface tension. Fedkiw and his students then used it for water, smoke and fire in computer graphics, where its free-surface form is the standard pressure boundary condition.

## References
