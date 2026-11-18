---
tag: AGQN60
kind: algorithm
slug: position-based-dynamics
name: Position based dynamics
aliases:
- PBD
area: graphics-and-signals/deformable-body-simulation
level: core
summary: Predict particle positions, then project them onto constraints one at a time in Gauss-Seidel sweeps, and set velocities from the change in position.
solves: [cloth-simulation]
model: real-ram
complexity:
  vars: {n: "the number of particles", c: "the number of constraints, each on a bounded number of particles", k: "the number of solver sweeps per step"}
  time: {sweep: "Θ(c)", step: "O(n + k c)"}
  space: {step: "O(n + c)"}
properties: {deterministic: true, exact: false, linear_momentum_conserving: true, angular_momentum_conserving: false, stiffness_depends_on_iterations: true}
history:
  year: 2007
  people: [Matthias Müller, Bruno Heidelberger, Marcus Hennix, John Ratcliff]
  note: Müller, Heidelberger, Hennix and Ratcliff described the method in 2006 and in the Journal of Visual Communication and Image Representation in 2007. It grew out of the position based particle and stick methods of Jakobsen for the game Hitman (2001).
prereqs: [particle-system, symplectic-euler-method, gauss-seidel-method]
see_also: [extended-position-based-dynamics, small-steps-physics, shake-constraint-algorithm, projected-gauss-seidel, meshless-shape-matching, position-based-fluids, fast-mass-spring, cloth-simulation]
sources:
  - paper: doi:10.1016/j.jvcir.2007.01.005
    title: "Matthias Müller, Bruno Heidelberger, Marcus Hennix and John Ratcliff, Position based dynamics, Journal of Visual Communication and Image Representation 18(2), 109-118, 2007"
    locator: "Section 3.1 (the algorithm, lines (1) to (17)), Section 3.2 (the solver), Section 3.3 (constraint projection, equations (1) to (11) and the stiffness per iteration), Section 3.4 (collisions), Section 3.5 (damping), Section 3.6 (attachments)"
---

Position based dynamics (PBD) moves particles by working on their positions, not on forces. Each step predicts where the particles go with [symplectic Euler](/symplectic-euler-method/), then moves the predicted positions so that they satisfy constraints such as fixed distances, one constraint at a time in [Gauss-Seidel](/gauss-seidel-method/) sweeps, and at the end takes each velocity as the change of position divided by $\Delta t$. Müller, Heidelberger, Hennix and Ratcliff (2007) made it a general method for cloth, soft bodies and ropes in games. It is fast, simple and robust, but its stiffness depends on the time step and on the number of sweeps, so it is not a discretization of a fixed physical model.

## In plain words

Think of a rope made of beads joined by sticks. First let every bead fly freely for one frame, as if the sticks were not there. Now the sticks have the wrong lengths. Go through the sticks one by one, and for each stick move its two beads along the stick until the length is right again. A heavy bead moves less than a light one. One pass does not fix everything, because fixing one stick spoils its neighbors, so do a few passes.

At the end, the velocity of each bead is where it ended up minus where it started, divided by the frame time. The beads never get a force that can blow up, so the rope never explodes. The price is that the rope feels softer with fewer passes or larger frames.

## The problem

The input is a set of particles with positions $\mathbf x_i$, velocities $\mathbf v_i$ and inverse masses $w_i = 1/m_i$ ($w_i = 0$ for a pinned particle), a set of constraints $C_j(\mathbf p) = 0$ or $C_j(\mathbf p) \ge 0$, each on a few particles, external forces $\mathbf f_{\text{ext}}$, a step $\Delta t$ and a sweep count $k$. The output is the state after one step. The aim is not to solve an equation of motion exactly. It is a motion that keeps the constraints and looks plausible at a fixed cost, as needed in games and interactive [cloth simulation](/cloth-simulation/). The page uses 2D, $y$ up and $\mathbf g = (0, -9.81)$ m/s².

## The algorithm

```pseudo id=main
PBD-STEP(x, v, w, constraints, Δt, k)
L1  for each particle i: v_i <- v_i + Δt w_i f_ext,i          ▷ the weight gives v_i + Δt g
L2  damp the velocities (optional)
L3  for each particle i: p_i <- x_i + Δt v_i                     ▷ prediction
L4  make a collision constraint for each particle whose path x_i -> p_i hits an obstacle
L5  repeat k times:
L6      for each constraint C_j in a fixed order: project p onto C_j
L7  for each particle i: v_i <- (p_i - x_i) / Δt
L8  for each particle i: x_i <- p_i
```

**Projection (L6).** For a constraint $C$ on the particles $S$, PBD moves the particles along the gradients, weighted by the inverse masses (Section 3.3, equations (8) and (9) with masses):

$$s = \frac{C(\mathbf p)}{\sum_{j \in S} w_j |\nabla_j C(\mathbf p)|^2}, \qquad \Delta \mathbf p_i = -k' s\, w_i \nabla_i C(\mathbf p).$$

This is the smallest correction in the mass norm that makes the linearized constraint zero, a [Lagrange multiplier](/lagrange-multiplier/) step. An inequality constraint is projected only when it is violated. For a distance constraint $C = |\mathbf p_1 - \mathbf p_2| - d$ with $\mathbf n = (\mathbf p_1 - \mathbf p_2)/|\mathbf p_1 - \mathbf p_2|$ it gives equations (10) and (11):

$$\Delta \mathbf p_1 = -\frac{w_1}{w_1 + w_2} (|\mathbf p_1 - \mathbf p_2| - d)\,\mathbf n, \qquad \Delta \mathbf p_2 = +\frac{w_2}{w_1 + w_2} (|\mathbf p_1 - \mathbf p_2| - d)\,\mathbf n .$$

**Stiffness.** A constraint with stiffness $k \in [0, 1]$ scales its correction by $k' = 1 - (1 - k)^{1/n_s}$, where $n_s$ is the sweep count, so that $n_s$ sweeps of a single constraint remove the fraction $k$ of its error (Section 3.3). With many coupled constraints the effective stiffness still depends on $n_s$ and on $\Delta t$.

**Collisions (L4).** The paper tests each path $\mathbf x_i \to \mathbf p_i$ against the scene with [collision detection](/collision-detection/) and adds an inequality constraint for each hit, kept for the current step only (Section 3.4). The code uses a horizontal ground line, $C = p_y - h \ge 0$. The paper also changes the velocities of colliding particles after L7 for friction and restitution; the code leaves this out.

**Damping (L2).** Section 3.5 blends each velocity toward the rigid motion of the whole body with the same linear and angular momentum, $\mathbf v_i \leftarrow \mathbf v_i + k_d (\mathbf v_{cm} + \boldsymbol\omega \times \mathbf r_i - \mathbf v_i)$. This damps the deformation and keeps both momenta. The factor $k_d$ is a tuning value.

**Order.** Each projection uses the positions already moved by the earlier projections of the same sweep, as in Gauss-Seidel. The gradients are taken at the current positions $\mathbf p$. The [SHAKE algorithm](/shake-constraint-algorithm/) of molecular dynamics also corrects positions one constraint at a time, but it takes the gradients at the old positions $\mathbf x$ and iterates until the constraints hold to a tolerance. [Projected Gauss-Seidel](/projected-gauss-seidel/) for contact is also a sweep of this kind, but it works on velocities or impulses, and it solves a linear complementarity problem whose matrix does not change during the sweep, while PBD relinearizes the nonlinear constraints at every projection.

## Example

**One projection by hand.** Particle 1 has $m_1 = 1$ at $(0, 0)$, particle 2 has $m_2 = 3$ at $(1.5, 0)$, and the rest length is $d = 1$. Then $w_1 = 1$, $w_2 = 1/3$, $\mathbf n = (-1, 0)$ and $C = 0.5$, so $s = 0.5/(4/3) = 0.375$. The corrections are $\Delta \mathbf p_1 = (0.375, 0)$ and $\Delta \mathbf p_2 = (-0.125, 0)$. The new distance is $1.375 - 0.375 = 1$, and the momentum change is $1 \cdot 0.375 + 3 \cdot (-0.125) = 0$.

**A spinning rod loses angular momentum.** Two particles of mass 1 at $(\mp 0.5, 0)$ with a rod of length 1 spin at $\omega = 1$ rad/s. With $\Delta t = 0.1$ s, the prediction stretches the rod to $(1 + (\omega \Delta t)^2)^{1/2}$, and the projection pulls both ends back toward the center. The angular momentum goes from $0.5$ to $0.5/\sqrt{1.01} = 0.497519$, the factor $0.995037$ per step. With $\omega \Delta t = 1$ the factor is $0.707107$. The corrections are torque-free about the predicted positions, but the step does not keep the angular momentum.

**Stiffness depends on the sweeps (measured).** A chain of 11 particles of 1 kg, joined by 10 rods of 0.1 m, is pinned at one end and falls from a horizontal start under gravity, with $\Delta t = 1/60$ s. After 300 steps (5 s), the total length of the chain exceeds its rest length of 1 m by

| sweeps $k$ | 1 | 2 | 5 | 10 | 20 | 50 |
|---|---|---|---|---|---|---|
| stretch | 11.4% | 5.7% | 2.9% | 1.5% | 0.64% | 0.16% |

The rods have no stiffness parameter here ($k = 1$), but the chain behaves like an elastic rope whose stiffness grows with the number of sweeps.

## Correctness

The claims are proved in [proofs/correctness.md](proofs/correctness.md). PBD does not converge to the solution of a time integrator, so its correctness is a list of exact properties of the discrete step, with their hypotheses.

1. **Smallest correction (proved).** With $k' = 1$, each projection is the smallest correction in the mass norm that zeroes the linearized constraint, and a single distance constraint is satisfied exactly after one projection.
2. **Linear momentum (proved).** If every constraint is invariant under translation, no particle is pinned and there is no ground, a step changes $\sum m_i \mathbf v_i$ only by $\Delta t \sum m_i \mathbf g$, for any number of sweeps. The test checks this to $10^{-10}$ with random distance and area constraints and damping.
3. **Torque-free corrections (proved).** If a constraint is also invariant under rotation, each projection satisfies $\sum m_i \mathbf p_i \times \Delta \mathbf p_i = 0$ about the positions $\mathbf p$ where it acts. These are the conditions (1) and (2) of Section 3.3.
4. **Angular momentum is not kept (proved).** The step changes $L = \sum m_i \mathbf x_i \times \mathbf v_i$ by $\frac{1}{\Delta t} \sum m_i \mathbf x_i \times \Delta \mathbf p_i$, which is not zero in general; the spinning rod above loses the factor $(1 + (\omega \Delta t)^2)^{-1/2}$ per step. Gradients at the old positions, as in SHAKE, would keep it.
5. **Damping (proved).** The damping of L2 keeps the linear and the angular momentum.
6. **Stiffness per sweep (proved for one constraint).** For a single constraint whose gradient direction does not change, $n_s$ sweeps with $k'$ leave the error $(1 - k) C_0$. With coupled constraints the result depends on $n_s$, as the table shows (measured).

The tests also check the projection against a KKT solve, the gradients against central differences, the pins and the ground, and free fall against the symplectic Euler value $-5.3955$ m after 10 steps of $0.1$ s.

## Complexity

One projection costs $O(1)$ for a constraint on a bounded number of particles, so one sweep costs $\Theta(c)$. Lines L1 to L3 and L7 to L8 cost $\Theta(n)$. The collision detection of L4 is a separate cost; with the ground line it is $\Theta(n)$. A step costs $O(n + k c)$ time, and the state and the constraint list use $O(n + c)$ memory. There is no matrix to build or factor. The number of sweeps that gives a usable stiffness is a measurement for each scene.

## Properties

- **Robust, not accurate.** The particles end where the projections put them, so a large correction cannot feed back as a large force. The paper argues that the method is unconditionally stable; this is an argument, not a theorem, and a stable answer can still be far from the motion of the physical model.
- **Stiffness is not a material constant.** The behavior depends on $\Delta t$, the sweep count and the constraint order. Two scenes with the same $k$ but different settings look different.
- **Order dependence.** Gauss-Seidel sweeps depend on the constraint order. A Jacobi version projects all constraints from the same positions and averages, which is parallel but slower to converge.
- **Exact conservation.** Linear momentum is kept for translation invariant constraints. Angular momentum is not kept exactly (claim 4).
- **Energy.** There is no energy that the step decreases or keeps; the damping is a mix of the method itself and the tuning factor $k_d$.

## Variants and improvements

- **XPBD.** [Extended position based dynamics](/extended-position-based-dynamics/) adds a compliance and a Lagrange multiplier to each constraint, which removes the dependence on the sweep count and makes the method an approximate [backward Euler](/backward-euler-method/) solver.
- **Substeps.** [Small steps](/small-steps-physics/) use many substeps with one sweep each instead of one step with many sweeps, which reduces the error of XPBD for the same cost.
- **Shape matching.** [Meshless shape matching](/meshless-shape-matching/) pulls particles toward the best rigid fit of the rest shape, which is a position based method without a mesh.
- **Fluids.** [Position based fluids](/position-based-fluids/) project a density constraint per particle with the same machinery.
- **Strain limiting.** [Provot strain limiting](/provot-strain-limiting/) is an older position correction that shortens over-stretched springs after a force based step.
- **Jacobi and graph coloring.** On a GPU, constraints are projected in parallel either by averaging (Jacobi) or by [graph coloring](/graph-coloring/), so that constraints of one color share no particle.

## When to use it

Use PBD for interactive scenes where robustness and a fixed cost per frame matter more than a material that behaves the same at every step size: cloth, ropes, hair and soft objects in games, and controllers that move particles directly. It handles pins, collisions and other position goals easily, because they are all constraints.

Do not use plain PBD when the stiffness must match a material or stay the same when $\Delta t$ or the sweep count changes. Use XPBD then, or an implicit solver such as [projective dynamics](/projective-dynamics/) or [optimization time integration](/optimization-time-integration/).

## Pitfalls

- **Stiffness changes with settings.** Raising the sweep count makes cloth stiffer and changing the step changes the look. Tune with the final settings, or use XPBD.
- **Velocities from positions.** Line L7 must use the position at the start of the step, $\mathbf x_i$, not the position after the external force. A collision projection that moves a particle far also gives it a large velocity; the paper corrects the velocities of colliding particles after L7.
- **Zero gradients.** A distance constraint between two particles at the same point has no direction. Skip it, as the code does, instead of dividing by zero.
- **Pinned pairs.** If all particles of a constraint are pinned, the denominator of $s$ is zero. Skip such constraints.
- **Angular momentum drift.** A fast spinning body slows down by the factor of claim 4 per step. Use smaller steps or the SHAKE choice of gradients if this matters.

## Implementations

## History

Jakobsen (2001) described a position based approach with Verlet integration and sticks projected one at a time for the characters of the game Hitman, at the Game Developers Conference. Müller, Heidelberger, Hennix and Ratcliff generalized it to arbitrary constraints with mass weighting, stiffness, collisions and damping, first at VRIPHYS 2006 and then in the Journal of Visual Communication and Image Representation in 2007. Macklin, Müller and Chentanez added compliance in 2016 with XPBD, and Macklin, Storey, Lu, Terdiman, Chentanez, Jeschke and Müller showed in 2019 that small substeps work better than many sweeps.

## References
