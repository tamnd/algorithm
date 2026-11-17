---
tag: XWJEV5
kind: problem
slug: rigid-body-simulation-problem
name: Rigid body simulation
aliases:
- rigid body animation
- rigid body dynamics simulation
area: graphics-and-signals/rigid-body-simulation
level: intro
summary: Advance the positions, orientations and velocities of rigid bodies over time under forces, collisions, contact and joints.
prereqs: [newton-euler-equations, unit-quaternion-rotation, symplectic-euler-method]
see_also: [collision-detection, collision-impulse, projected-gauss-seidel, baraff-contact-force-algorithm, impulse-based-simulation, stewart-trinkle-time-stepping, articulated-body-algorithm, mirtich-polyhedral-mass-properties]
sources:
  - url: https://www.cs.cmu.edu/~baraff/sigcourse/notesd1.pdf
    title: "David Baraff, Rigid Body Dynamics I, unconstrained motion, in Andrew Witkin and David Baraff, Physically Based Modeling: Principles and Practice, SIGGRAPH 97 course notes"
    locator: "the state of a rigid body (position, orientation, linear and angular momentum), its derivative, and the inertia tensor in world space (general locator)"
  - url: https://www.cs.cmu.edu/~baraff/sigcourse/notesd2.pdf
    title: "David Baraff, Rigid Body Dynamics II, motion with constraints, in Andrew Witkin and David Baraff, Physically Based Modeling: Principles and Practice, SIGGRAPH 97 course notes"
    locator: "colliding contact by impulses and resting contact by contact forces (general locator)"
  - paper: doi:10.1111/cgf.12272
    title: "Jan Bender, Kenny Erleben and Jeff Trinkle, Interactive simulation of rigid body dynamics in computer graphics, Computer Graphics Forum 33(1), 246-270, 2014"
    locator: the survey of the simulation loop, contact models with friction, joints and the numerical methods for them (general locator)
  - paper: doi:10.1137/s0036144599360110
    title: "David E. Stewart, Rigid-body dynamics with friction and impact, SIAM Review 42(1), 3-39, 2000"
    locator: "existence and uniqueness for rigid bodies with Coulomb friction, Painleve's paradox, and time stepping formulations (general locator)"
---

Rigid body simulation computes how solid objects that do not deform move over time: falling, colliding, sliding, resting in stacks, and hanging from joints. Each body has a position, an orientation, a linear velocity and an angular velocity, and its motion follows the [Newton-Euler equations](/newton-euler-equations/). The hard parts are the places where bodies meet. Rigid bodies cannot overlap, so a collision must change velocities in an instant, a body at rest on another needs a contact force that is just strong enough, and friction decides whether a contact sticks or slides. In computer graphics and games, the goal is usually a plausible motion at a fixed cost per frame, so most methods mix laws of mechanics with models and tuning. This page states the problem and lists its parts; the methods are on the pages linked below.

## In plain words

A game has boxes, balls and doors. Each one should fall, bounce, slide and stop the way real things do, many times per second. Between hits, every object just flies, and that part is easy. The hard part is when objects touch. They must not pass into each other. A hit must turn them away at once. A box on a table must stay still and not sink. A box on a slope must slide or hold, depending on how rough the slope is. Doors must stay on their hinges. A simulator splits the work into steps: move the objects, find which ones touch, fix the hits, find the pushes at the places where they rest, and keep the joints together.

## Definition

**State.** Body $i$ has mass $m_i$, the body-frame inertia tensor $I_{body,i}$, and the state

$$Y_i = (x_i, R_i, P_i, L_i),$$

the position of the center of mass, the orientation (a rotation matrix, or a [unit quaternion](/unit-quaternion-rotation/)), the linear momentum and the angular momentum, as in Baraff's course notes. The velocities are $v_i = P_i / m_i$ and $\omega_i = I_i^{-1} L_i$, with the world inertia tensor $I_i = R_i I_{body,i} R_i^T$. Without contact,

$$\dot x = v, \qquad \dot R = \omega^* R, \qquad \dot P = F, \qquad \dot L = \tau,$$

where $\omega^*$ is the cross product matrix of $\omega$, and $F$ and $\tau$ are the total force and torque. This is a law of classical mechanics.

**Input.** The bodies with their shapes, masses and inertia tensors; the initial state; the forces (gravity $(0, -9.81)$ in 2D or $(0, -9.81, 0)$ in 3D on these pages, with $y$ up); the material values, a [coefficient of restitution](/coefficient-of-restitution/) $e$ and a [friction coefficient](/coulomb-friction-law/) $\mu$ per pair; the joints as constraints $C(x) = 0$; a time step $\Delta t$ and an end time.

**Output.** The states at the times $k \Delta t$.

**Requirements.**

1. Between contacts, the bodies follow the Newton-Euler equations, up to the error of the integrator.
2. No two bodies overlap, or the overlap stays below a tolerance.
3. At a contact with normal $n$ from $B$ to $A$, the normal force or impulse only pushes ($\lambda_n \ge 0$), and it is zero when the bodies separate. The relative normal velocity $v_{rel} = n \cdot (v_A(p) - v_B(p))$ is negative when they approach.
4. A collision obeys a restitution law, and friction obeys Coulomb's law $\|f_t\| \le \mu f_n$.
5. Joint constraints hold, up to a tolerance.
6. The cost per step is bounded, for interactive use.

Requirements 3 and 4 together are complementarity conditions; see [rigid contact complementarity](/rigid-contact-complementarity/), where the robotics pages use $z$ up. The laws in requirement 4 are empirical models with measured coefficients.

## Variants

- **Collision response only.** Bodies bounce and never rest; each collision is resolved by a [collision impulse](/collision-impulse/).
- **Resting contact without friction.** Find contact forces with $\lambda \ge 0$, accelerations $a \ge 0$ and $\lambda^T a = 0$: a [linear complementarity problem](/linear-complementarity-problem/).
- **Contact with friction.** Add Coulomb friction; the instantaneous problem may then have no solution or several ([Painleve paradox](/painleve-paradox/), $z$ up on that page).
- **Time stepping.** Pose the problem for impulses over one step instead of forces at an instant, as in [Stewart-Trinkle time stepping](/stewart-trinkle-time-stepping/) ($z$ up) and in game engines.
- **Articulated bodies.** Chains and trees of bodies joined by joints, in reduced coordinates; see the [articulated body algorithm](/articulated-body-algorithm/).
- **Nonconvex bodies and stacking.** Bodies of any shape, with stable stacks as a requirement; see [shock propagation](/shock-propagation/).

## Examples

**Free fall (computed).** A body starts at rest at height 0 and falls for 1 s, with $\Delta t = 0.1$ s. The exact height is $-g/2 = -4.905$ m. Explicit [Euler](/euler-method/) gives $-g \Delta t^2 (0 + 1 + \cdots + 9) = -4.4145$ m, and [symplectic Euler](/symplectic-euler-method/), which updates the velocity first, gives $-g \Delta t^2 (1 + \cdots + 10) = -5.3955$ m. Both are first order; the integrator is part of the method.

**A spinning body (computed).** A body with $I_{body} = \mathrm{diag}(1, 2, 3)$, $R = I$ and $L = (1, 1, 1)$ has $\omega = I^{-1} L = (1, 1/2, 1/3)$ and kinetic energy $\tfrac12 L \cdot \omega = 11/12 \approx 0.916667$. Without torque, $L$ stays fixed in world space while $\omega$ changes as the body turns: the angular velocity is not a conserved quantity.

**A ball dropped on the floor.** It hits at $4.42945$ m/s after a fall of 1 m, and with $e = 0.5$ it bounces to $0.25$ m; its infinitely many bounces end after $1.354571$ s (see [coefficient of restitution](/coefficient-of-restitution/)).

**A block on a slope.** At $30°$ it sticks for $\mu \ge \tan 30° \approx 0.577$ and slides otherwise (see [Coulomb friction](/coulomb-friction-law/)).

## Known algorithms

The parts of a simulator, and the methods for each:

| part | what it does | methods |
|---|---|---|
| integration | advances the state between contacts | [symplectic Euler](/symplectic-euler-method/), [unit quaternion](/unit-quaternion-rotation/) updates, [Runge-Kutta methods](/runge-kutta-methods/); mass properties by [Mirtich's method](/mirtich-polyhedral-mass-properties/) |
| collision detection | finds pairs that touch, their points, normals and depths | broad phase by [sweep and prune](/sweep-and-prune/); narrow phase by [GJK](/gjk-algorithm/), [EPA](/expanding-polytope-algorithm/), [V-Clip](/v-clip/), [Lin-Canny](/lin-canny-closest-features/); [continuous collision detection](/continuous-collision-detection/) and [conservative advancement](/conservative-advancement/) for fast bodies; the result is a [contact manifold](/contact-manifold/) |
| collision response | changes the velocities at a collision | [collision impulse](/collision-impulse/), [impulse-based simulation](/impulse-based-simulation/) |
| resting contact and friction | finds the contact forces or impulses | [Baraff's pivoting algorithm](/baraff-contact-force-algorithm/), [projected Gauss-Seidel](/projected-gauss-seidel/), [penalty contact](/penalty-contact/), [Stewart-Trinkle time stepping](/stewart-trinkle-time-stepping/), [shock propagation](/shock-propagation/) for stacks |
| joints | keeps the bodies of a joint together | the same solvers with bilateral rows, [Baumgarte stabilization](/baumgarte-stabilization/) for drift, the [articulated body algorithm](/articulated-body-algorithm/) in reduced coordinates, [position-based dynamics](/position-based-dynamics/) |

Bender, Erleben and Trinkle (2014) survey these parts for interactive simulation.

## Bounds

- **Existence can fail.** With Coulomb friction, the instantaneous contact problem can have no solution or many; this is Painleve's paradox, surveyed by Stewart (2000). Impulse-based time stepping formulations restore existence.
- **Hardness.** Deciding whether consistent contact forces exist with Coulomb friction is NP-hard (Baraff 1991).
- **Frictionless contact is a convex problem.** Without friction, the contact LCP has a symmetric positive semidefinite matrix and is the optimality condition of a convex quadratic program. When $b$ lies in the range of $A$, it has a solution, and all solutions give the same accelerations (proved on the page of [Baraff's algorithm](/baraff-contact-force-algorithm/)); the forces need not be unique.
- **Cost per step.** Collision detection needs at least one test per pair that may touch, and a solver that reads every contact row needs $\Omega(c)$ time for $c$ rows. Iterative solvers such as projected Gauss-Seidel spend $O(K c)$ for $K$ sweeps, and the $K$ needed for a given accuracy grows with the height of a stack (a measurement on that page).
- **Zeno behavior.** A bouncing ball with $0 < e < 1$ makes infinitely many collisions in finite time, so an event-driven simulator cannot reach the end of the bounces without a rule that stops them.

## Reductions

- **Frictionless resting contact to an LCP and a QP.** The contact accelerations are affine in the contact forces, $a = A f + b$ with $A = J M^{-1} J^T$, so resting contact is the LCP $f \ge 0$, $a \ge 0$, $f^T a = 0$ (Baraff 1994), which is the KKT system of the [quadratic program](/quadratic-programming/) $\min \tfrac12 f^T A f + b^T f$ over $f \ge 0$ (Baraff 1989 used a quadratic program).
- **Friction to a nonsymmetric LCP.** With a polygonal [friction cone](/friction-cone/), the time stepping problem with friction becomes an LCP with a matrix that is not symmetric (Stewart-Trinkle).
- **Collision detection to distance queries.** Narrow phase contact generation reduces to distance and [penetration depth](/penetration-depth/) queries between convex pieces, after a convex decomposition of nonconvex shapes.

## Applications

- Games and virtual reality, where the cost per frame is fixed and plausible motion matters more than exact forces.
- Film effects: destruction, falling debris, piles of objects.
- Robotics: simulators for grasping and locomotion, which need forces that match the real ones more closely.
- Engineering: mechanisms, granular media and machine design, with measured friction and restitution values.

## References
