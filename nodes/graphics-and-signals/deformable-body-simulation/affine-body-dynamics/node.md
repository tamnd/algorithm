---
tag: J2K8MW
kind: algorithm
slug: affine-body-dynamics
name: Affine body dynamics
aliases:
- ABD
area: graphics-and-signals/deformable-body-simulation
level: research
summary: Simulate stiff bodies as affine maps with a stiff orthogonality energy and the barrier contact of IPC; the paper measures large speedups over rigid IPC in its scenes.
model: real-ram
complexity:
  vars: {V: "the number of body vertices", L: "the number of obstacle lines", N: "the number of Newton iterations per step"}
  time: {iteration: "O(V L)", step: "O(N V L)"}
  space: {step: "Θ(V + L)"}
properties: {deterministic: true, exact: false, constant_mass_matrix: true, monotone_objective: true, penetration_free_with_conservative_ccd: true, angular_momentum_conserving: false, friction_in_code: false}
history:
  year: 2022
  people: [Lei Lan, Danny M. Kaufman, Minchen Li, Chenfanfu Jiang, Yin Yang]
  note: Lan, Kaufman, Li, Jiang and Yang presented affine body dynamics at SIGGRAPH 2022 as a fast replacement for rigid bodies in barrier based contact.
prereqs: [incremental-potential-contact, rigid-body-simulation-problem, newton-method-for-systems]
see_also: [rigid-contact-complementarity, stewart-trinkle-time-stepping, impulse-based-simulation, newton-euler-equations, conservative-advancement, meshless-shape-matching, as-rigid-as-possible-deformation, singular-value-decomposition]
sources:
  - paper: doi:10.1145/3528223.3530064
    title: "Lei Lan, Danny M. Kaufman, Minchen Li, Chenfanfu Jiang and Yin Yang, Affine body dynamics: fast, stable and intersection-free simulation of stiff materials, ACM Transactions on Graphics 41(4), 2022 (SIGGRAPH 2022)"
    locator: "Section 3 (equation (1) the affine map, equations (3) to (5) the mass matrix and the equation of motion), Section 3.2 (equations (6) to (8), the orthogonality energy), Section 4 (equations (9) to (12), the incremental potential with barrier and friction), Section 4.1 (collision checks on straight paths), Section 4.3 (the Hessian), Section 5 (measurements)"
---

Affine body dynamics (ABD) simulates stiff objects, which would normally be rigid bodies, as bodies that can only move by an affine map $\mathbf x = A\bar{\mathbf x} + \mathbf p$. A very stiff orthogonality energy keeps $A$ close to a rotation. Lan, Kaufman, Li, Jiang and Yang (2022) chose this model because every point of the body then moves on a straight line when the state moves on a straight line, and the mass matrix is constant. So the barrier contact and the [continuous collision checks](/continuous-collision-detection/) of [incremental potential contact](/incremental-potential-contact/) apply directly, with 12 unknowns per body in 3D. The paper measures speedups of about 30 to more than 1000 times over a rigid body version of IPC in its scenes; the code on this page is a 2D version with one body and fixed lines.

## In plain words

A rigid body can only turn and move. Turning is awkward for a solver, because angles wrap around and the motion of a point under a turn follows a curve. ABD lets the body also stretch and shear, which makes every motion a simple linear one, and then adds a very strong spring that pushes the body back to its true shape whenever it stretches. The body stays almost rigid. Because all point motions are now straight lines, checking whether a step would make the body hit something is easy and exact. The rest of the solver is the same safe contact method as IPC.

## The problem

The input is a body with rest vertices $\bar{\mathbf x}_v$, masses $m_v$, the state $\mathbf q = (\mathbf p, A)$ with $\mathbf p \in \mathbb R^d$ and $A \in \mathbb R^{d \times d}$ (12 numbers in 3D, 6 in 2D), its velocity $\dot{\mathbf q}$, obstacles and a step $\Delta t$. With $J(\bar{\mathbf x})\mathbf q = A\bar{\mathbf x} + \mathbf p$ (equation (1)), the mass matrix $M = \sum_v m_v J_v^TJ_v$ is constant, and the motion follows $M\ddot{\mathbf q} = -\nabla V + \mathbf f$ (equation (5)). The orthogonality energy (equation (6)) is

$$V_\perp(A) = \kappa_o\,\mathrm{vol}\,\|AA^T - I\|_F^2,$$

which is zero exactly when $A$ is orthogonal. The paper uses $\kappa_o$ above 100 GPa. One step minimizes the incremental potential with the IPC barrier $b$ (equations (9) to (11)):

$$E(\mathbf q) = \tfrac12(\mathbf q - \tilde{\mathbf q})^TM(\mathbf q - \tilde{\mathbf q}) + \Delta t^2V_\perp(A) + \kappa\sum_k b(d_k(\mathbf q)), \qquad \tilde{\mathbf q} = \mathbf q^n + \Delta t\dot{\mathbf q}^n + \Delta t^2M^{-1}\mathbf f.$$

The paper adds friction (equation (12)) and handles contact between bodies. The code covers one 2D rectangle with vertices on its border and lumped masses, contact against fixed lines $\mathbf n\cdot\mathbf x \ge h$, no friction, $y$ up and $\mathbf g = (0, -9.81)$ m/s².

## The algorithm

```pseudo id=main
ABD-STEP(q, q̇, Δt, κ, d̂, ε_d)
L1  q̃ <- q + Δt q̇ + Δt² M⁻¹ f
L2  z <- q
L3  repeat:
L4      g <- ∇E(z);  H <- M + Δt² PSD(∇²V_⊥) + Σ_k κ b''(d_k) ∇d_k ∇d_kᵀ
L5      p <- -H⁻¹ g
L6      if max_v |J_v p| / Δt < ε_d: stop
L7      α <- min(1, 0.8 · first time a vertex reaches an obstacle on z + t p)
L8      while E(z + α p) > E(z): α <- α/2
L9      z <- z + α p
L10 q̇ <- (z - q)/Δt;  q <- z
```

**The affine state (L1).** With the rest coordinates centered at the center of mass, $M$ is block diagonal: the total mass for $\mathbf p$ and a second moment matrix for $A$. It does not depend on $\mathbf q$, so there are no Coriolis or centrifugal forces, unlike the [Newton and Euler equations](/newton-euler-equations/) of a rigid body (claim 1).

**The Hessian (L4).** $V_\perp$ is not convex, so its Hessian is projected to a positive semidefinite matrix by clamping negative eigenvalues; the code uses a Jacobi eigen decomposition of the $4 \times 4$ block ($9 \times 9$ in 3D). A gap $d_k$ is affine in $\mathbf q$ for a vertex against a fixed line, so its barrier Hessian needs no projection. The paper builds a contact aware Hessian that keeps the per body blocks small (Section 4.3).

**The step bound (L7).** Along $\mathbf z + t\mathbf p$ every vertex moves on a straight line, $J_v\mathbf z + tJ_v\mathbf p$. So the time when a vertex reaches a line is a linear equation, and the code solves it exactly. Section 4.1 of the paper uses the same fact for 3D collision checks between bodies.

## Example

**Free fall by hand.** A body at rest with $A = I$ has $\nabla V_\perp(I) = 0$, so $A$ stays $I$, and with the rest coordinates centered the $\mathbf p$ part of $E$ is $\frac{m_{\text{tot}}}{2}|\mathbf p - \tilde{\mathbf p}|^2$. The step sets $\mathbf p = \tilde{\mathbf p} = \mathbf p^n + \Delta t\dot{\mathbf p}^n + \Delta t^2\mathbf g$, the [symplectic Euler](/symplectic-euler-method/) update: after 10 steps of 0.1 s the height is $-0.0981 \cdot 55 = -5.3955$ m.

**A spinning drop (measured).** A rectangle of $0.4 \times 0.2$ m with density 1000 kg/m² (80 kg) starts at height 1 m, turned by 0.3 rad, falling at 5 m/s and spinning at 10 rad/s, onto the ground $y \ge 0$ with $\hat d = 10^{-3}$ m, $\kappa = 1$ and $\Delta t = 0.01$ s, for 1 s:

| $\kappa_o$ | $10^5$ | $10^7$ | $10^9$ |
|---|---|---|---|
| smallest gap (m) | $3.4 \times 10^{-7}$ | $2.3 \times 10^{-7}$ | $2.3 \times 10^{-7}$ |
| largest $\|AA^T - I\|_F$ | 0.18 | $3.2 \times 10^{-3}$ | $3.2 \times 10^{-5}$ |
| most Newton iterations in a step | 10 | 12 | 15 |
| mean Newton iterations per step | 3.43 | 2.84 | 4.49 |

The gap stays positive at every iterate. With $\kappa_o = 10^5$ the impact deforms the body by 18%, which is no longer a stiff body; a factor of 100 in $\kappa_o$ cuts the deformation by about 100.

**Damping of rotation (measured).** The same body spins freely at 10 rad/s with no gravity and $\kappa_o = 10^7$ for 1 s. A rigid body would turn by 10 rad.

| $\Delta t$ (s) | 1/30 | 1/100 | 1/300 | 1/1000 |
|---|---|---|---|---|
| angle turned (rad) | 5.32 | 7.32 | 8.73 | 9.54 |
| final rate (rad/s) | 3.62 | 5.78 | 7.75 | 9.13 |

The loss comes from the [backward Euler](/backward-euler-method/) step, which moves $A$ along the tangent of the rotation and lets the stiff energy pull it back. It shrinks at first order in $\Delta t$.

## Correctness

The claims are proved in [proofs/correctness.md](proofs/correctness.md), in exact arithmetic.

1. **Affine model (proved).** $\frac12\dot{\mathbf q}^TM\dot{\mathbf q}$ is the kinetic energy of the vertices, $M$ is constant, and it is block diagonal and positive definite for centered rest coordinates with three points not on one line. The test checks $J\mathbf q = A\bar{\mathbf x} + \mathbf p$ and the kinetic energy identity.
2. **Orthogonality energy (proved).** $V_\perp \ge 0$ with equality exactly for orthogonal $A$, where its gradient is zero; the gradient is $4\kappa_o\mathrm{vol}\,CA$ with $C = AA^T - I$. It is not convex. The test checks the gradient and Hessian against central differences, and that the projection gives a positive semidefinite matrix that equals the Hessian when it is already semidefinite.
3. **No crossing (proved, under a hypothesis).** For a convex body against fixed lines, the step bound keeps the whole body strictly inside every half plane at every iterate and on the paths between them. In floating point this needs a conservative collision check, as in IPC. The test checks all 60 steps of the spinning drop.
4. **Monotone energy (proved).** $H$ is positive definite, so each Newton direction goes downhill, and the line search makes $E$ decrease. The test records $E$ at every iteration and checks by sampling 300 nearby states that a converged step is a local minimum of $E$.
5. **Linear momentum (proved).** Without active contact a converged step changes the linear momentum by exactly $\Delta t\,m_{\text{tot}}\mathbf g$. Angular momentum is not kept (measured above).
6. **Contact forces (proved).** At a stationary point, the forces $\lambda_k = -\kappa b'(d_k)/\Delta t^2 \ge 0$ balance inertia and elasticity, and for a body at rest they sum to its weight; the test checks this to 0.1%.

The tests also check free fall against $-5.3955$ m and that the orthogonality error of a spinning body falls by a factor between 50 and 200 when $\kappa_o$ grows 100 times.

## Complexity

The code does $O(VL)$ work per Newton iteration for the assembly and the step bound, plus a constant for the $4 \times 4$ eigen decomposition and the $6 \times 6$ solve, and $O(VL)$ per halving of the line search. In 3D a body has 12 unknowns, so a system of $B$ bodies has $12B$ unknowns however many vertices the bodies have. The cost of contact between bodies depends on the culling of pairs; the paper culls them with axis aligned bounding boxes (Section 4.2).

## Properties

- **Constant mass matrix.** No Coriolis or centrifugal terms and no rotation parameters (claim 1).
- **Straight vertex paths.** A straight step in $\mathbf q$ moves every vertex on a straight line, which makes collision checks simple (claim 3).
- **Almost rigid.** The body deforms by an amount that falls as $\kappa_o$ grows; it is never exactly rigid.
- **Free of intersection.** With the IPC barrier and conservative collision checks, as in [incremental potential contact](/incremental-potential-contact/).
- **Numerical damping.** The backward Euler step loses angular velocity at large $\Delta t$ (the rotation table).
- **Fast in the paper's scenes.** The paper reports 124 times faster than rigid IPC for a wrecking ball scene with 575 bodies (Fig. 3) and very large factors on a chain net (Fig. 4). These are measurements on its scenes and hardware, not a bound.

## Variants and improvements

- **Rigid IPC.** Ferguson et al. (2021) kept rigid body coordinates with curved trajectories and barrier contact; ABD replaces them with affine coordinates and straight trajectories.
- **Other near rigid models.** [Shape matching](/meshless-shape-matching/) also fits a linear map to a body, and [as rigid as possible deformation](/as-rigid-as-possible-deformation/) penalizes the distance to a rotation; ABD puts such a penalty inside an implicit step with barrier contact.
- **Friction.** Section 4 of the paper adds the lagged friction of IPC (equation (12)).

## When to use it

Use ABD for scenes with many stiff objects in tight contact, such as stacks, chains, gears and mechanisms, when contact must be free of intersection and a rigid body solver with [complementarity contact](/rigid-contact-complementarity/) or [impulses](/impulse-based-simulation/) gives jitter or passes through thin parts.

Do not use it when bodies must be exactly rigid, when angular momentum must be kept over long times at large steps, or when a fast game physics loop with simple contacts is enough.

## Pitfalls

- **Too soft $\kappa_o$.** The body visibly stretches on impact (the drop table at $10^5$). The paper's value is above 100 GPa.
- **Too stiff $\kappa_o$ for the step.** The Newton problem becomes badly conditioned: in the code, $\kappa_o = 10^{11}$ with $\Delta t = 1/30$ s reaches the cap of 100 iterations in some steps of the free spin.
- **Reading off the rotation.** $A$ is not exactly orthogonal; take its polar factor (in 2D, the angle $\operatorname{atan2}(a_{21} - a_{12}, a_{11} + a_{22})$) when a rotation is needed.
- **Reflections.** $V_\perp$ is also zero at reflections. A body cannot reach one by continuous motion with a stiff $\kappa_o$, but a bad initial state can start there.
- **Uncentered rest coordinates.** Then $M$ couples $\mathbf p$ and $A$; this is still correct, but the simple form of claim 5 needs the center of mass at the origin.

## Implementations

## History

Rigid body solvers with impulses, penalties or complementarity contact have a long history in graphics. Barrier contact for rigid bodies followed the 2020 IPC paper, with curved trajectories that make collision checks expensive. Lan, Kaufman, Li, Jiang and Yang (2022) replaced rigid coordinates by affine ones with a stiff orthogonality energy and presented affine body dynamics at SIGGRAPH 2022.

## References
