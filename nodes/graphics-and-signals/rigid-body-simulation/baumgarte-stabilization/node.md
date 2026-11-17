---
tag: YW8E8N
kind: technique
slug: baumgarte-stabilization
name: Baumgarte stabilization
aliases:
- Baumgarte constraint stabilization
- Baumgarte bias
area: graphics-and-signals/rigid-body-simulation
level: core
summary: Feed back the constraint position error into the velocity constraint, so that numerical drift of joints and contacts decays over time.
prereqs: [projected-gauss-seidel, symplectic-euler-method, lagrange-multiplier, differential-algebraic-equations]
see_also: [penalty-contact, collision-impulse, shock-propagation, rattle-algorithm, shake-constraint-algorithm, position-based-dynamics, extended-position-based-dynamics, small-steps-physics]
sources:
  - paper: doi:10.1016/0045-7825(72)90018-7
    title: "J. Baumgarte, Stabilization of constraints and integrals of motion in dynamical systems, Computer Methods in Applied Mechanics and Engineering 1(1), 1-16, 1972"
    locator: the stabilized constraint equation with feedback of the constraint and its derivative (general locator)
  - url: https://box2d.org/files/ErinCatto_IterativeDynamics_GDC2005.pdf
    title: "Erin Catto, Iterative Dynamics with Temporal Coherence, Game Developers Conference, 2005"
    locator: "Section 3.6 (the bias term) and Section 4.2 (Baumgarte stabilization of the normal constraint, J_n V = -beta C_n, and the range 0 < beta < 2 / Delta t)"
  - url: https://box2d.org/posts/2024/02/solver2d/
    title: "Erin Catto, Solver2D, Box2D blog, February 2024"
    locator: "the sections on Baumgarte stabilization, soft constraints, NGS with pseudo velocities, and relaxation"
---

Baumgarte stabilization keeps the constraints of a simulation from drifting. A solver that works on velocities, such as [projected Gauss-Seidel](/projected-gauss-seidel/), makes the velocity of each joint or contact satisfy its constraint, but the positions are integrated with a finite step, so the position error $C$ grows slowly: a pendulum gets longer, a joint comes apart, a box sinks into the floor. Baumgarte (1972) replaced the constraint $\ddot C = 0$ by a damped equation that drives $C$ back to zero. Game engines use a velocity form of the same idea: they ask the solver for a velocity that removes a fraction $\beta$ of the error in each step. The feedback is tuning, not physics. The correction velocity is real velocity, so it can add energy: overlapping bodies push apart faster than they met, and a deep overlap makes a body jump. Split impulses are one fix.

## In plain words

A door on a hinge should stay on the hinge. A computer moves the door in small steps, and each step adds a tiny error, so after many steps the door is a little off its hinge. Baumgarte's idea is to look at how far off the door is, and to add a small push back toward the hinge at every step. A weak push fixes the error slowly. A strong push fixes it fast, but it can overshoot and shake. The push also gives the door real speed, which the door keeps after the error is gone. So a box that sinks into the floor can be pushed out so fast that it jumps. A common fix is to use a separate, pretend speed for the push, which moves the box back but is then thrown away.

## When it applies

- Constraints $C(x) = 0$ for joints, or $C(x) \ge 0$ for contacts, solved at the velocity level, $\dot C = J v = 0$ (or $\ge 0$), with the Jacobian $J$.
- Index reduction of [differential-algebraic equations](/differential-algebraic-equations/): the constraint is differentiated to the velocity or acceleration level, and the differentiated form no longer holds $C$ at zero.
- Time stepping with a fixed step, where a small, steady correction is acceptable and an exact projection of the positions is too costly.

## The template

**Baumgarte's form.** For a holonomic constraint $C(x) = 0$, solve the dynamics with the stabilized constraint

$$\ddot C + 2\alpha \dot C + \beta^2 C = 0, \qquad \alpha, \beta > 0,$$

in place of $\ddot C = 0$. The error then obeys a damped linear oscillator and decays to zero for any start, if the dynamics are integrated exactly (a law of linear differential equations, not a property of the discrete solver). $\alpha = \beta$ is the critically damped choice. The values are tuning: too small and the drift stays, too large and the equations become stiff for the integrator.

**The velocity form used in games.** At the velocity level, the solver asks for

$$J v + \frac{\beta}{\Delta t} C = 0 \qquad (0 < \beta \le 1),$$

or $J v + (\beta / \Delta t) C \ge 0$ with an impulse $\lambda \ge 0$ for a contact, where $C < 0$ is the overlap. The extra term is a bias in the right-hand side of the solver ([projected Gauss-Seidel](/projected-gauss-seidel/), line L4). Catto (2005, Section 4.2) writes $J_n V = -\beta C_n$ with a $\beta$ that has the units of $1/\text{s}$; his $\beta$ is the $\beta / \Delta t$ of this page. Each step does the following.

1. Add the external forces to the velocities.
2. For each constraint row, compute the position error $C$ and the bias $b = (\beta / \Delta t) C$, often with a slop: no bias while the overlap is below a few millimeters.
3. Solve the velocity problem with the target $J v + b = 0$ (or $\ge 0$).
4. Integrate the positions with the new velocities.

```pseudo id=main
BAUMGARTE-STEP(bodies, rows, β, Δt)
L1  v ← v + Δt M⁻¹ f_ext
L2  for each row i: C_i ← position error of row i; b_i ← (β / Δt) C_i
L3  solve for impulses λ with J v + b = 0 (contacts: ≥ 0 with λ ≥ 0)
L4  x ← x + Δt v
```

**The error decays by $1 - \beta$ per step (proved for the model).** Take a linear constraint $C = J x$ and a step in which the solver meets its target exactly. After line L3, $J v = -(\beta / \Delta t) C$, so line L4 gives $C^{new} = C + \Delta t J v = (1 - \beta) C$. After $k$ steps the error is $(1 - \beta)^k C^0$. It goes to zero if and only if $0 < \beta < 2$; it decays without changing sign if and only if $\beta \le 1$. In Catto's units this is his range $0 < \beta < 2/\Delta t$ for convergence and $\beta \le 1/\Delta t$ for a smooth decay. For a nonlinear constraint, a contact that may separate, or a solver that stops after a few sweeps, the factor is only an estimate.

**It adds energy (computed).** A box of mass 1 at rest overlaps a wall by $d = 0.01$ m, without gravity. With $\beta = 0.2$ and $\Delta t = 1/60$, the first solve gives the box the separating velocity $\beta d / \Delta t = 0.12$ m/s. In the next step the box already separates faster than the new target, so the contact applies no impulse, and the box keeps $0.12$ m/s forever: it gains $0.0072$ J of kinetic energy from nothing. With $d = 0.1$ m the speed is $1.2$ m/s. Under gravity, a box that overlaps the floor by $0.3$ m rises to $0.39$ m above the floor with $\beta = 0.2$, and one that overlaps by $0.1$ m rises $1.79$ m with $\beta = 1$ (measured, $\Delta t = 1/60$, $g = 9.81$). Catto's Solver2D notes say the same of Baumgarte stabilization: "it can lead to energy creation and jitter if not tuned carefully".

## Classic examples

**A drifting pendulum (measurement).** A point mass on a rod of length 1 starts horizontal at rest and swings for 10 s under gravity, with $\Delta t = 1/60$ and symplectic Euler; each step projects the velocity onto $J v + (\beta / \Delta t) C = 0$ with $C = |x| - 1$.

| $\beta$ | 0 | 0.05 | 0.1 | 0.2 | 0.5 | 1 |
|---|---|---|---|---|---|---|
| largest $\lvert C \rvert$ in 10 s | 0.475 | 0.0357 | 0.0226 | 0.0128 | 0.0054 | 0.0027 |

Without the bias, the rod stretches by almost half its length, because each step moves the mass along the tangent and so off the circle. With the bias, the error stays at a small, steady value that falls as $\beta$ grows. A pendulum hanging at rest with a rod that is too long by $0.1$ m shortens by the factor $(1 - \beta)$ per step, exactly as in the proof, because then all motion is along the rod.

**Resting contact.** Catto (2005, Section 4.2) applies the bias to the normal constraint of each contact, so that boxes that sink into each other are pushed back out over a few steps. With a slop, the bias acts only on the part of the overlap above the slop, and a resting box keeps a small, steady overlap instead of bouncing in and out of contact. The slop is tuning.

## Variations

- **Split impulses.** Solve a second velocity problem for pseudo velocities that carry only the position correction. The pseudo velocities move the positions in line L4 and are then thrown away, so the correction adds no kinetic energy.
- **Position projection.** Early versions of Box2D corrected the positions with a separate nonlinear Gauss-Seidel pass on pseudo velocities, which Solver2D calls NGS and describes as a way of dealing with the energetic response of Baumgarte stabilization. [Position-based dynamics](/position-based-dynamics/) and [XPBD](/extended-position-based-dynamics/) work on the positions from the start.
- **Relaxation.** Solver2D solves with the bias, then runs relaxation iterations with the bias turned off, so that the final velocities do not carry it.
- **Soft constraints.** A spring and damper in the constraint, with a stiffness and damping ratio in place of $\beta$; Solver2D calls them "an evolution of Baumgarte Stabilization". The relation to the [penalty method](/penalty-contact/) is direct: both turn the error into a restoring push.
- **Exact projections.** [RATTLE](/rattle-algorithm/) and [SHAKE](/shake-constraint-algorithm/) solve the position constraints to a tolerance in each step, at a higher cost, with no drift parameter.

## Pitfalls

- **Overshoot.** $\beta > 1$ in the velocity form makes the error change sign each step, and $\beta \ge 2$ makes it grow, in the linear model.
- **Bias with restitution.** If the bias and the restitution target are added, a contact bounces higher than the coefficient of restitution says. Do not add the two targets.
- **Contacts that pop.** A deep overlap from a fast collision turns into a large separating speed. Clamp the bias, use a slop, or use split impulses.
- **Warm starting with bias.** Cached impulses from a step with a large bias can carry the extra push into the next step.
- **Stiff limits.** In Baumgarte's form, large $\alpha$ and $\beta$ make the system stiff, and an explicit integrator then needs smaller steps.

## References
