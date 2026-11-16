---
tag: YQZW8R
kind: algorithm
slug: hybrid-position-force-control
name: Hybrid position/force control
aliases:
- Raibert-Craig hybrid control
area: robotics/grasping-and-manipulation
level: core
summary: "Splits the task space by selection matrices into directions that control force and directions that control position, and runs one controller in each."
model: real-ram
complexity:
  vars: {n: "the number of joints, equal to the task dimension (a nonredundant arm); the bounds are for one control step"}
  time: {per_step: O(n^3)}
  space: {extra: O(n^2)}
properties: {deterministic: true, online: true, exact: false}
history:
  year: 1981
  people: [Marc H. Raibert, John J. Craig]
  note: Raibert and Craig combined position and force feedback through a selection matrix, building on the natural and artificial constraints of Mason.
prereqs: [wrench, rigid-body-twist, jacobian-statics-duality]
see_also: [impedance-control, admittance-control, operational-space-formulation, computed-torque-control, friction-cone, peg-in-hole, pid-controller, kinematic-singularity]
sources:
  - paper: "M. H. Raibert and J. J. Craig, Hybrid position/force control of manipulators, Journal of Dynamic Systems, Measurement, and Control 103(2), 126-133, 1981"
    locator: the whole paper
  - paper: doi:10.1109/TSMC.1981.4308708
    title: Matthew T. Mason, Compliance and force control for computer controlled manipulators, IEEE Transactions on Systems, Man, and Cybernetics 11(6), 1981
    locator: pages 418 to 432
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 11, Section 11.5 (force control) and Section 11.6 (hybrid motion-force control)
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Chapter 9 (force control, natural and artificial constraints, hybrid force/motion control)
  - book: isbn:9783319325507
    title: Bruno Siciliano and Oussama Khatib (editors), Springer Handbook of Robotics, second edition, Springer, 2016
    locator: Chapter 9 (Force Control, by Luigi Villani and Joris De Schutter)
---

Hybrid position/force control is a scheme for tasks in which a robot tool slides along a surface while it presses on it. The task space is split into directions in which the surface blocks motion, where the controller regulates the contact force, and the other directions, where the controller regulates the position. Diagonal selection matrices $S_f$ and $S_p = I - S_f$ in a task frame pick the two sets. Raibert and Craig introduced the scheme in 1981, using the natural and artificial constraints of Mason to choose the directions. Unlike [impedance control](/impedance-control/), it controls the force explicitly, but it needs a model of where the constraints are.

## In plain words

Think of wiping a table. Along the table you care about where the cloth goes. Down into the table you cannot move anyway, so you care about how hard you press. Hybrid control writes this down: in each direction of a frame fixed to the task, choose either "control the position" or "control the force", never both.

The table itself fixes the motion downward and the force sideways (if there is no friction). These are the natural constraints. The task adds the other half: a path along the table and a pressing force downward. These are the artificial constraints. The controller runs a position loop in the free directions and a force loop in the blocked ones.

## The problem

The arm has $n$ joints and obeys $M(q)\ddot q + C(q, \dot q)\dot q + g(q) = \tau + J(q)^T F_{\text{ext}}$, where $F_{\text{ext}}$ is the [wrench](/wrench/) of the environment on the tool and $J$ is square and nonsingular. In a task frame aligned with the contact, a diagonal matrix $S_f$ with entries 0 or 1 marks the directions in which the environment blocks the motion, and $S_p = I - S_f$ marks the free ones. A desired motion $x_d(t)$ is given in the free directions, and a desired force $F_d(t)$ that the tool should apply in the blocked directions. The task is to choose $\tau$ so that $S_p(x - x_d) \to 0$ and $S_f(F - F_d) \to 0$, where $F = -F_{\text{ext}}$ is the measured force that the tool applies.

## The algorithm

This is the task-space form with a dynamic model. The integral $\int(F_d - F)\,dt$ of the force error is kept as a state.

```pseudo id=main
HYBRID(q, q', x_d, x_d', x_d'', F_d, F, ∫(F_d - F), S_f)
L1  x ← f(q);  x' ← J(q) q'
L2  a_p ← x_d'' + K_d (x_d' - x') + K_p (x_d - x)          ▷ position loop
L3  F_f ← F_d + K_fi ∫(F_d - F) - K_v x'                  ▷ force loop with active damping
L4  Λ ← (J M⁻¹ Jᵀ)⁻¹;  μ ← Λ (J M⁻¹ (C q' + g) - J' q')
L5  F_cmd ← Λ (I - S_f) a_p + S_f F_f + μ
L6  τ ← Jᵀ F_cmd
L7  return τ
```

Line L4 computes the task-space inertia $\Lambda$ and the bias force $\mu$ of the [operational space formulation](/operational-space-formulation/). Line L5 uses them so that the position loop sees a unit mass in the free directions, while the force command passes through directly. Line L6 maps the task force to joint torques by [Jacobian-statics duality](/jacobian-statics-duality/). The term $-K_v x'$ in line L3 adds damping in the force directions; it is zero when the contact is rigid.

## Example

Take the planar 2R arm with $L_1 = L_2 = 1$ m and point masses of 1 kg at the link ends, in a vertical plane with gravity along $-y$. A frictionless wall at $x = 1$ m acts as a stiff spring with $k_e = 10^5$ N/m. The force direction is the wall normal $x$, so $S_f = \operatorname{diag}(1, 0)$, with $F_d = 10$ N. The position direction is $y$, with $y_d(t) = 0.5 + 0.1\sin 2t$ m. The gains are $K_p = 400$, $K_d = 40$ (critical damping at 20 rad/s), $K_v = 600$ N s/m and $K_{fi} = 0$. The arm starts at rest at $(1, 0.5)$, touching the wall with zero force.

At the start, $q = (-0.514, 1.955)$ rad, and line L4 gives $\Lambda = [[1.019, 0.149], [0.149, 2.144]]$ kg and $\mu = (1.19, 18.95)$ N. The position error is zero, but the speed error is $\dot y_d = 0.2$ m/s, so line L2 gives $a_{p,y} = 8$ m/s$^2$. Line L5 gives $F_{\text{cmd}} = (1.19 + 10 + 1.19,\ 17.15 + 18.95) = (12.38, 36.10)$ N, and line L6 gives $\tau = (29.91, -7.62)$ N m.

A simulation with RK4 and a step of 1 ms gives:

| time (s) | force on the wall (N) | error in $y$ (mm) |
|---|---|---|
| 0.01 | 8.48 | $-1.64$ |
| 0.02 | 9.95 | $-2.69$ |
| 0.05 | 10.000 | $-3.68$ |
| 0.10 | 10.000 | $-2.71$ |
| 0.50 | 10.000 | $-0.005$ |

The force settles in about 50 ms, with a peak of 10.0012 N. The $y$ error is $-0.2\,t\,e^{-20 t}$ m, the critically damped response to the initial speed error, as if the wall were not there. The tool presses 0.1 mm into the spring wall, which is $F_d/k_e$.

With a gravity model in which the second mass is 0.8 kg instead of 1 kg, and a fixed goal $y_d = 0.5$, the force settles at 10.152 N with $K_{fi} = 0$. With $K_{fi} = 20$ s$^{-1}$ it settles at 10.000 N. The $y$ position still ends 2.5 mm low, because the position loop has no integral term.

## Correctness

The claim is: with an exact model, the closed loop in task coordinates is

$$\ddot x = S_p a_p + \Lambda^{-1}(S_f F_f + F_{\text{ext}}).$$

If the contact is rigid and frictionless, the constraint keeps $S_f\ddot x = 0$ and $S_p F_{\text{ext}} = 0$. Because $\Lambda^{-1}$ is positive definite, these two facts force $S_f F_f + F_{\text{ext}} = 0$. So the force on the environment equals $S_f F_f$, which is $S_f F_d$ when $K_{fi} = 0$, and the free directions obey $\ddot e + K_d\dot e + K_p e = 0$ exactly. Against a frictionless spring surface, the same argument applies at every rest point: the position error is zero and the force is $S_f F_d$. With $K_{fi} > 0$, the force at rest is $S_f F_d$ even when the model is wrong, because the integral state can stop only when the force error is zero. The full proof is in the proof file.

## Complexity

In the [real-RAM](/real-ram/) model, with $n$ joints and task dimension $n$, one step needs the Jacobian ($O(n^2)$ entries), the inertia matrix and its inverse ($O(n^3)$), the product $J M^{-1} J^T$ and its inverse ($O(n^3)$), and a few matrix-vector products ($O(n^2)$). So it takes $O(n^3)$ time and $O(n^2)$ memory. For a 6-joint arm this is a fixed number of operations. The original joint-space form without $\Lambda$ costs $O(n^3)$ too, because of $J^{-1}$.

## Properties

- **Explicit force regulation.** Unlike impedance control, the force in the constrained directions follows $F_d$ directly and does not depend on the stiffness of the environment at rest.
- **Orthogonal split.** Position and force are never controlled in the same direction. This is consistent only when the selection matches the real constraints in a frame where they are axis-aligned.
- **Needs the contact geometry.** The task frame and $S_f$ come from a model of the contact. If the surface is tilted or curved and the frame is not updated, the position loop fights the surface and the force loop pushes into free space.
- **Needs contact.** In a force direction without contact, the force loop accelerates the tool until it hits something. Switching between free motion and contact needs care.

## Variants and improvements

- **Original joint-space form.** Raibert and Craig mapped the position errors to joint space through $J^{-1}$ and added a separate force term through $J^T$, with gains in joint space. Later analyses found that this form can be unstable in some arm configurations; the task-space form with $\Lambda$ above avoids the problem.
- **Constraint-based form.** Lynch and Park write the constraints as $A(q)\dot q = 0$ and use a projection matrix that depends on the state instead of a constant $S_f$. This handles constraints that are not aligned with fixed axes.
- **Hybrid impedance control.** Use an impedance law in the position directions, so that the tool stays compliant when it meets an unexpected obstacle there.
- **Force control on a position-controlled arm.** Realize the force loop as an outer loop that adjusts the position command, as in [admittance control](/admittance-control/) with $K_a = 0$ in the force directions.
- **Parallel force/position control.** Let both loops act in all directions, with the force loop given priority by an integral term, which avoids the need for an exact selection matrix.

## When to use it

Use it for contact tasks with known, simple geometry: pressing a tool on a flat surface while moving along it (grinding, polishing, deburring), turning a crank, or pushing a peg along the axis of a hole while keeping the side forces at zero. When the contact geometry is uncertain or contact starts and ends often, [impedance control](/impedance-control/) is usually more robust.

## Pitfalls

- **Wrong frame.** The selection matrix is meaningful only in a task frame aligned with the contact. Using it in a fixed base frame when the surface is tilted leads to conflicts between the loops.
- **Stiff contact and force gains.** The force loop includes the environment stiffness. Against a stiff surface, high force gains or too little damping $K_v$ make the contact chatter. For one force direction against a spring wall, with the effective mass $m_f = 1/(\Lambda^{-1})_{ff}$ held fixed, the loop is stable if and only if $K_{fi} < K_v/m_f$.
- **Friction.** With friction, the surface also applies forces in the position directions, so $S_p F_{\text{ext}} \ne 0$ and the position loop sees a disturbance. Friction also lets the surface hold the tool against forces inside the [friction cone](/friction-cone/).
- **Loss of contact.** If the force command is negative or the surface ends, the tool leaves the surface and the force loop has no plant to act on. Clamp the force command and detect the loss of contact.
- **Singularities.** $\Lambda$ and $J^{-1}$ fail near a [kinematic singularity](/kinematic-singularity/).

## Implementations

## History

In 1981, Mason published a formalism of natural and artificial constraints for compliant motion, and Raibert and Craig published the hybrid position/force controller in the Journal of Dynamic Systems, Measurement, and Control. Their controller used a selection matrix to choose force or position control in each direction of a constraint frame. Later work moved the scheme to task space with the dynamic model, as in Khatib's operational space formulation, and generalized the selection matrix to projections onto the constraint and motion subspaces.

## References
