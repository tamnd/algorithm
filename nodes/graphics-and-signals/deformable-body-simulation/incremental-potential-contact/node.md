---
tag: TZGCEP
kind: algorithm
slug: incremental-potential-contact
name: Incremental potential contact
aliases:
- IPC contact model
area: graphics-and-signals/deformable-body-simulation
level: research
summary: Add a smooth log barrier on distances to the implicit time step energy and cap each Newton step by a collision check, which keeps every state free of intersection if the check is conservative.
model: real-ram
complexity:
  vars: {n: "the number of free vertices", s: "the number of springs", c: "the number of obstacle segments", N: "the number of Newton iterations per step"}
  time: {iteration: "O(n^3 + s + n c)", step: "O(N (n^3 + s + n c))"}
  space: {step: "Θ(n^2 + s + c)"}
properties: {deterministic: true, exact: false, monotone_objective: true, penetration_free_with_conservative_ccd: true, friction_in_code: false}
history:
  year: 2020
  people: [Minchen Li, Zachary Ferguson, Teseo Schneider, Timothy Langlois, Denis Zorin, Daniele Panozzo, Chenfanfu Jiang, Danny M. Kaufman]
  note: Li, Ferguson, Schneider, Langlois, Zorin, Panozzo, Jiang and Kaufman presented incremental potential contact at SIGGRAPH 2020 as a contact model for implicit time steps with a guarantee of no intersection.
prereqs: [optimization-time-integration, barrier-method, continuous-collision-detection, backtracking-line-search, newton-method-for-systems]
see_also: [affine-body-dynamics, interior-point-method, elementary-ccd-tests, conservative-advancement, penalty-contact, robust-cloth-collision, coulomb-friction-law, vertex-block-descent]
sources:
  - paper: doi:10.1145/3386569.3392425
    title: "Minchen Li, Zachary Ferguson, Teseo Schneider, Timothy Langlois, Denis Zorin, Daniele Panozzo, Chenfanfu Jiang and Danny M. Kaufman, Incremental potential contact: intersection- and inversion-free, large-deformation dynamics, ACM Transactions on Graphics 39(4), Article 49, 2020 (SIGGRAPH 2020)"
    locator: "Section 2 (equation (1) the incremental potential, equations (2) and (3) admissibility and complementarity), Section 4 (Algorithm 1, barrier aware projected Newton), Sections 4.1 and 4.2 (equations (5) and (6), the barrier), Section 4.3 (the projected Hessian, equation (7)), Section 4.4 (the step bound by collision checks), Section 4.5 (equations (8) and (9), contact forces), Section 5 (friction)"
---

Incremental potential contact (IPC) handles contact in an implicit time step by adding a barrier energy that grows without bound as the distance between two primitives goes to zero. Li et al. (2020) minimize the [backward Euler](/backward-euler-method/) energy plus this barrier with a projected [Newton method](/newton-method-for-systems/), and they cap each Newton step by a [continuous collision check](/continuous-collision-detection/), so that no primitive touches another on the path between two iterates. If the collision check is conservative, every iterate and every state is free of intersection, and a [line search](/backtracking-line-search/) makes the energy decrease at every iteration. The paper handles points against triangles and edges against edges in 3D, with friction; the code on this page is a 2D version with points against fixed segments and no friction.

## In plain words

Think of a ball falling onto a floor. Instead of letting it pass into the floor and then pushing it back, IPC puts an invisible cushion just above the floor. The cushion is soft far away and becomes infinitely hard right at the floor, so the ball can never reach it. Each frame, the solver looks for the most comfortable position of everything, balancing motion, springs and cushions. It moves toward that position in steps, and before each step it checks the whole path for a collision and shortens the step if one would happen. So nothing ever passes through anything, even when objects move very fast.

## The problem

The input is a set of vertices with masses $m_i$, positions $\mathbf x^n$, velocities $\mathbf v^n$, a step $\Delta t$, an elastic energy $\Psi$ and obstacles. The output is the next state $\mathbf x^{n+1}$ that minimizes the incremental potential of equation (1) of the paper, under the constraint that all distances stay positive:

$$E(\mathbf x) = \tfrac12(\mathbf x - \hat{\mathbf x})^T M(\mathbf x - \hat{\mathbf x}) + \Delta t^2\Psi(\mathbf x), \qquad \hat{\mathbf x} = \mathbf x^n + \Delta t\mathbf v^n + \Delta t^2 M^{-1}\mathbf f_e,$$

with the paper's $h$ written as $\Delta t$. Without contacts, the minimizer is the variational form of the backward Euler step, as in [optimization time integration](/optimization-time-integration/). IPC replaces the constraint by a barrier (equations (5) and (6)):

$$B(\mathbf x) = E(\mathbf x) + \kappa\sum_k b(d_k(\mathbf x)), \qquad b(d) = -(d - \hat d)^2\ln\frac{d}{\hat d} \text{ for } 0 < d < \hat d, \quad b(d) = 0 \text{ for } d \ge \hat d,$$

where $d_k$ is the distance of a pair of primitives, $\hat d$ is the activation distance and $\kappa > 0$ is the stiffness. The paper adapts $\kappa$ during the solve; the code fixes it. In the code, the elastic energy is a sum of 2D springs, the pairs are free vertices against fixed segments, $y$ is up and $\mathbf g = (0, -9.81)$ m/s².

## The algorithm

```pseudo id=main
IPC-STEP(x, v, Δt, κ, d̂, ε_d)
L1  x̂ <- x + Δt v + Δt² g                        ▷ pinned vertices stay
L2  z <- x                                       ▷ start at the last state, which is free of intersection
L3  repeat:
L4      p <- -H⁻¹ ∇B(z)                          ▷ H: every stencil Hessian projected to PSD
L5      if max |p| / Δt < ε_d: stop
L6      α <- min(1, 0.8 · first time of contact on the path z + t p, t in [0, 1])
L7      while B(z + α p) > B(z): α <- α/2
L8      z <- z + α p
L9  v <- (z - x)/Δt;  x <- z
```

**The barrier (L4).** $b$ is positive and decreasing on $(0, \hat d)$, tends to infinity at $0$ and is twice continuously differentiable at $\hat d$, where it meets zero (claim 1). So only pairs closer than $\hat d$ add terms, and the Newton method sees a smooth energy.

**The projected Hessian (L4).** The paper projects the Hessian of each element and each contact stencil to a positive semidefinite matrix by clamping its negative eigenvalues (Section 4.3). For a 2D spring this sets the factor $1 - r/\ell$ of the transverse term to zero when the spring is compressed. For a point near the end of a segment the barrier Hessian is $\kappa(b''\nabla d\nabla d^T + b'\nabla^2 d)$, equation (7), and the second term is negative semidefinite, so the projection drops it. With the mass matrix added, $H$ is positive definite and $\mathbf p$ is a descent direction (claim 2).

**The step bound (L6).** A Newton step can jump over a thin obstacle, because $B$ at the far side can be finite and small. A continuous collision check along the straight path from $\mathbf z$ to $\mathbf z + \mathbf p$ finds the first time of contact, and the step is cut to a fraction of it (Section 4.4). In 2D, a point moving on a line meets a segment at most once unless it moves along the line of the segment, and the code solves this in closed form. The paper uses 3D [point and triangle and edge and edge tests](/elementary-ccd-tests/).

**Stopping (L5).** Algorithm 1 stops when the Newton direction, scaled to a velocity, is below $\varepsilon_d$. The code uses $\varepsilon_d = 10^{-6}$ m/s unless a test sets another value.

**Friction.** Section 5 adds a smoothed Coulomb friction with lagged normal forces and tangent bases. The code leaves it out.

## Example

**A fast point by hand.** A point of mass 1 is at height 0.5 m above a segment from $(-1, 0)$ to $(1, 0)$, with $v = -1000$ m/s, $\Delta t = 1/30$ s, $\hat d = 10^{-3}$ m and $\kappa = 1$. Then $\hat y = 0.5 - 33.333 - 0.0109 = -32.844$. At the start the barrier is not active, so $H = 1$ and $p = \hat y - 0.5 = -33.344$. The path meets the segment at $t = 0.5/33.344$, so $\alpha = 0.8t$ and the point moves to $y = 0.5 - 0.8 \cdot 0.5 = 0.1$. Each later iteration does the same from the new height, so the heights are $0.5, 0.1, 0.02, 0.004, 8 \times 10^{-4}, \dots$; the code reaches $5.1 \times 10^{-8}$ after 10 iterations and stops after 11 at $1.6 \times 10^{-8}$ m, above the segment. Plain Newton with a line search but without L6 takes the full step to $y = -32.844$, where $B$ is finite, and the point passes through the segment.

**A box drop (measured).** A square of side 0.2 m with four vertices of 0.25 kg, edge and diagonal springs of $k = 10^4$ N/m, $\hat d = 10^{-3}$ m and $\kappa = 1$ starts with its lowest vertices at 0.5 m and falls at 20 m/s onto flat ground. Over one second of simulation:

| $\Delta t$ (s) | 1/30 | 1/100 | 1/300 |
|---|---|---|---|
| smallest gap over the run (m) | $4.1 \times 10^{-6}$ | $2.1 \times 10^{-5}$ | $8.4 \times 10^{-5}$ |
| most Newton iterations in a step | 10 | 9 | 8 |
| mean Newton iterations per step | 1.13 | 0.73 | 1.34 |

The gap stays positive at every iterate. The box comes to rest at a gap of $2.1 \times 10^{-4}$, $6.5 \times 10^{-4}$ and $8.7 \times 10^{-4}$ m. The rest gap depends on $\Delta t$ because the contact force is $\lambda = -\kappa b'(d)/\Delta t^2$ (claim 5), so a fixed $\kappa$ gives a different barrier force at each step size. The paper sets $\kappa$ adaptively for this reason.

**Rest gap against stiffness (measured).** For the same box at rest with $\Delta t = 0.01$ s, the gap is $2.3 \times 10^{-5}$, $6.5 \times 10^{-4}$ and $9.6 \times 10^{-4}$ m for $\kappa = 10^{-2}$, $1$ and $10^2$. The sum of the contact forces is 9.810 N in all three cases, the weight of the box. A smaller $\kappa$ gives a smaller gap, but a stiffer and harder Newton problem near contact.

## Correctness

The claims are proved in [proofs/correctness.md](proofs/correctness.md), in exact arithmetic.

1. **The barrier (proved).** $b$ is twice continuously differentiable, positive, decreasing and convex on $(0, \hat d)$, zero beyond $\hat d$, and infinite in the limit $d \to 0$. The test checks $b'$ and $b''$ against central differences and the smooth join at $\hat d$.
2. **Descent direction (proved).** Each stencil projection clamps exactly the negative eigenvalues, so $H$ is positive definite and $\mathbf p$ goes downhill when $\nabla B \ne 0$. The test checks the gradient and the unprojected Hessian against central differences, and that the projected matrix is positive semidefinite where the unprojected one is not.
3. **No intersection (proved, under a hypothesis).** The step bound keeps every distance positive on the whole straight path between iterates, so all iterates and all states are free of intersection. In floating point this needs a collision check that is conservative, which is the hypothesis of the paper's guarantee. The test checks the time of contact against sampling for 300 random cases and the fast point above.
4. **Monotone energy (proved).** The line search ends after a finite number of halvings with $B$ not larger than before. Convergence of the iterates to a minimizer is not proved here. The test records $B$ over all iterations of 30 steps of the box drop.
5. **Contact forces (proved).** At a stationary point, $M(\mathbf x - \hat{\mathbf x})/\Delta t^2 = -\nabla\Psi + \sum\lambda_k\nabla d_k$ with $\lambda_k = -\kappa b'(d_k)/\Delta t^2 \ge 0$, nonzero only for $d_k < \hat d$, equations (8) and (9). The test checks that the forces of a box at rest sum to its weight.
6. **No contact (proved).** Without active pairs the step is a Newton solve of backward Euler; the test checks a spring against the closed form and free fall against the symplectic Euler value $-5.3955$ m after 10 steps of $0.1$ s.

## Complexity

One Newton iteration of the code assembles the gradient and Hessian in $O(s + nc)$, solves the dense $2n \times 2n$ system in $O(n^3)$ and checks every vertex and segment pair for the step bound in $O(nc)$. Each halving of the line search costs $O(n + s + nc)$. The memory is $\Theta(n^2 + s + c)$. The paper uses a sparse Cholesky solver, culls pairs with a spatial structure and filters the collision checks (Section 4.6). The number of Newton iterations depends on the scene, on $\Delta t$ and on how close contacts are to $\hat d$.

## Properties

- **Free of intersection.** Given conservative collision checks, no state and no iterate has an intersection, at any $\Delta t$ (claim 3).
- **Monotone solver.** The barrier augmented potential decreases at every iteration (claim 4).
- **Smooth contact forces.** Forces act from a distance $\hat d$ and are always compressive; the contact gap is positive, not zero.
- **Large time steps.** The step is implicit, so stiff springs and fast motion do not force small steps for stability, but the accuracy still depends on $\Delta t$.
- **Expensive.** Each iteration needs a global linear solve and collision checks, so IPC is much slower than [penalty contact](/penalty-contact/) or [XPBD](/extended-position-based-dynamics/) contact.

## Variants and improvements

- **Friction.** Section 5 of the paper adds smoothed friction (equations (10) to (17)), with a mollifier for small slip speeds and lagged normal forces. The paper states that it has no convergence guarantee for the lagged iterations.
- **Edge and edge mollifier.** In 3D, nearly parallel edges give a nonsmooth distance; Section 4.2 multiplies the barrier by a mollifier.
- **Rigid and stiff bodies.** [Affine body dynamics](/affine-body-dynamics/) restricts each body to an affine map, which keeps the barrier and step bound of IPC with far fewer unknowns.
- **Codimensional and other elements.** Later work applies the same barrier to shells, rods and particles.
- **Relation to optimization.** The [interior point method](/interior-point-method/) and other [barrier methods](/barrier-method/) of optimization use the same idea of a barrier that keeps iterates feasible; IPC keeps the barrier with a fixed small $\hat d$ instead of driving a barrier weight to zero.

## When to use it

Use IPC when contact must be free of intersection with no tuning per scene, for example for tight knots, stacked cloth, large deformation with self contact, or a fast moving body that hits thin obstacles. It fits offline simulation and engineering use where a guaranteed result is worth the cost.

Do not use it for real time scenes with many contacts on a tight budget; use [VBD](/vertex-block-descent/), [XPBD](/extended-position-based-dynamics/) or [penalty contact](/penalty-contact/) there. For cloth with a simpler pipeline, [robust cloth collision](/robust-cloth-collision/) with [impact zones](/impact-zones/) is another route to no intersection.

## Pitfalls

- **Starting in contact.** The guarantee needs a start free of intersection. A start with a zero or negative distance gives an infinite barrier.
- **Collision checks that are not conservative.** A floating point check that reports a late time of contact can let a vertex cross. Use checks that are conservative by design.
- **A fixed stiffness.** With a fixed $\kappa$ the gap and the conditioning change with $\Delta t$ (the box drop table). The paper adapts $\kappa$ from the scene.
- **Too large $\hat d$.** Contacts act from far away and objects float visibly; too small $\hat d$ makes the Newton problem stiff near contact.
- **No projection.** Without the stencil projection, $H$ can be indefinite and the Newton direction can go uphill.
- **A step bound of exactly the time of contact.** A step that ends on the obstacle gives an infinite barrier. The code takes $0.8$ of the time of contact as a safety margin; this value is a choice of the code.

## Implementations

## History

Barrier methods are old tools of constrained optimization. Contact in graphics used penalty forces, impulses or complementarity solvers, each with trade-offs between robustness and parameter tuning. Li, Ferguson, Schneider, Langlois, Zorin, Panozzo, Jiang and Kaufman (2020) combined a smooth barrier, a projected Newton solve and a step bound from continuous collision checks into IPC, and presented it at SIGGRAPH 2020.

## References
