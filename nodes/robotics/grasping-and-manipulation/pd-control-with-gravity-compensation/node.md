---
tag: 0ACG13
kind: algorithm
slug: pd-control-with-gravity-compensation
name: PD control with gravity compensation
aliases:
- Takegaki-Arimoto controller
area: robotics/grasping-and-manipulation
level: core
summary: "Joint PD feedback plus a gravity model. With exact gravity, a rigid arm and positive definite gains, every set point is globally asymptotically stable."
model: real-ram
complexity:
  vars: {n: "the number of joints of a serial chain; the bounds are for one control step"}
  time: {per_step: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, online: true, exact: false}
history:
  year: 1981
  people: [Morikazu Takegaki, Suguru Arimoto]
  note: Takegaki and Arimoto showed with an energy-like Lyapunov function that PD feedback plus gravity compensation brings a manipulator to any set point.
prereqs: [manipulator-equation, lyapunov-function, lasalle-invariance-principle]
see_also: [computed-torque-control, slotine-li-adaptive-control, passivity-based-control, pid-controller, skew-symmetry-of-manipulator-dynamics, impedance-control, ida-pbc, lyapunov-direct-method]
sources:
  - paper: doi:10.1115/1.3139651
    title: M. Takegaki and S. Arimoto, A new feedback method for dynamic control of manipulators, Journal of Dynamic Systems, Measurement, and Control 103(2), 1981
    locator: pages 119 to 125
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, second edition, Wiley, 2020
    locator: Chapter 9, Section 9.2 (PD control revisited)
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 11, Section 11.4.2 (motion control of a multi-joint robot)
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Chapter 8 (motion control, centralized control)
---

PD control with gravity compensation is a set-point controller for a robot arm. It applies a spring and a damper on each joint error and adds the torque that holds the arm up against gravity. It needs only the gravity part of the dynamic model, not the inertia or the Coriolis terms, and with an exact gravity model, symmetric positive definite gains and a rigid arm, the arm comes to rest at the set point from every initial state. Takegaki and Arimoto proved this in 1981 with a [Lyapunov function](/lyapunov-function/) that is the kinetic energy of the arm plus the energy of the virtual springs. It is the simplest member of the family of [passivity-based](/passivity-based-control/) robot controllers.

## In plain words

Imagine a spring and a shock absorber on each joint, pulling the joint toward its goal angle. Without help, gravity drags the arm down, so the arm stops where the spring force balances its weight, short of the goal. Now add, at every moment, exactly the torque that cancels gravity in the current pose. The arm then behaves as if it were weightless with springs on its joints. The springs store energy, the dampers remove it, and the arm can rest only where the springs are relaxed, which is the goal.

This works for a fixed goal. For a moving goal the arm lags behind, and a law such as computed-torque control is better.

## The problem

The arm has $n$ joints with positions $q \in \mathbb{R}^n$ and obeys the [manipulator equation](/manipulator-equation/)

$$M(q)\ddot q + C(q, \dot q)\dot q + g(q) = \tau,$$

with no contact forces. Here $M(q)$ is the symmetric positive definite inertia matrix, $C(q, \dot q)\dot q$ the Coriolis and centripetal torques and $g(q)$ the gravity torque. A constant set point $q_d$ is given. The task is to choose the torque $\tau$ from the measured $q$ and $\dot q$ so that $q \to q_d$ and $\dot q \to 0$ from every initial state.

## The algorithm

The controller has a gravity model $\hat g$ and gain matrices $K_p$ and $K_d$, both symmetric positive definite. In practice they are diagonal.

```pseudo id=main
PD-GRAVITY(q, q', q_d, K_p, K_d)
L1  e ← q_d - q
L2  τ ← K_p e - K_d q' + ĝ(q)        ▷ spring, damper and gravity
L3  return τ
```

The damper acts on the joint speed $\dot q$, not on $\dot e$. For a constant set point both are the same up to the sign, because $\dot e = -\dot q$. Line L2 needs only $\hat g(q)$, which is the inverse dynamics at the state $(q, 0)$ with zero acceleration.

## Example

Take the planar 2R arm with $L_1 = L_2 = 1$ m and point masses of 1 kg at the link ends, in a vertical plane, with $q_1$ measured from the horizontal and $g = 9.81$ m/s$^2$. Its gravity torque is $g(q) = (2 g \cos q_1 + g \cos(q_1 + q_2),\ g \cos(q_1 + q_2))$ N m. The arm starts at rest at $q = (0, 0)$, the set point is $q_d = (0.3, 0.4)$ rad, and the gains are $K_p = 100 I$ and $K_d = 20 I$.

At the start, line L1 gives $e = (0.3, 0.4)$. The spring part is $K_p e = (30, 40)$ N m, the damper part is zero, and $\hat g(0, 0) = (29.43, 9.81)$ N m, so line L2 gives $\tau = (59.43, 49.81)$ N m.

The table shows where the arm comes to rest in a simulation with RK4, for three gravity models.

| gravity model in line L2 | rest pose $q$ (rad) | rest error $e$ (rad) |
|---|---|---|
| exact, $\hat g = g$ | $(0.3, 0.4)$ | $(0, 0)$ |
| none, $\hat g = 0$ (plain PD) | $(0.0106, 0.3068)$ | $(0.2894, 0.0932)$ |
| second mass 1.5 kg, model 1 kg | $(0.2107, 0.3587)$ | $(0.0893, 0.0413)$ |

Without gravity compensation the first joint hardly moves: at rest $K_p e = g(q)$, and the gravity torque at the shoulder, about 28.9 N m, needs an error of about 0.29 rad in a spring of 100 N m/rad. With a wrong gravity model, the rest error satisfies $K_p e = g(q) - \hat g(q)$.

## Correctness

The claim is: if $\hat g = g$, the gains are symmetric positive definite, and the smallest eigenvalue of $M(q)$ is bounded below by a positive constant for all $q$, then $(q, \dot q) = (q_d, 0)$ is a globally asymptotically stable equilibrium of the closed loop. The proof uses

$$V = \tfrac12 \dot q^T M(q) \dot q + \tfrac12 e^T K_p e,$$

which is positive definite and radially unbounded in $(e, \dot q)$. Along the closed loop, $\dot V = -\dot q^T K_d \dot q \le 0$, because the term $\dot q^T(\dot M - 2C)\dot q$ is zero (the [skew symmetry](/skew-symmetry-of-manipulator-dynamics/) of the arm dynamics). $\dot V$ is zero only when $\dot q = 0$, and the only solution that stays in that set is the set point, so the [LaSalle invariance principle](/lasalle-invariance-principle/) gives global asymptotic stability. The full proof is in the proof file.

## Complexity

In the [real-RAM](/real-ram/) model, with $n$ joints and diagonal gains, lines L1 and L2 take $O(n)$ operations plus one call of the gravity model. The gravity torque of a serial chain is the output of the [recursive Newton-Euler algorithm](/recursive-newton-euler-algorithm/) with zero joint speed and acceleration, which takes $O(n)$ operations. So one control step takes $O(n)$ time and $O(n)$ extra memory. Full gain matrices raise the cost to $O(n^2)$.

## Properties

- **Global stability for set points.** The result holds from every initial state, with no bound on the gains other than positive definiteness.
- **Needs only gravity.** The law does not use $M$ or $C$, so errors in the inertial parameters do not move the rest pose. Only errors in $\hat g$ do.
- **Asymptotic, not exponential, by this proof.** The Lyapunov function above has a negative semidefinite derivative, so the proof gives asymptotic stability. Local exponential convergence near the set point follows from the linearization, but the rate depends on the pose through $M(q)$.
- **Passive structure.** The closed loop is the arm with a virtual spring and a virtual damper. This is why the law stays stable when the arm touches a passive environment, a fact that [impedance control](/impedance-control/) builds on.

## Variants and improvements

- **Constant gravity term.** Use $\hat g(q_d)$ in place of $\hat g(q)$. This needs no online model, but global stability then needs $K_p$ large enough to dominate the change of $g$ over the workspace.
- **PID control.** An integral term removes the offset from an unknown constant gravity error. For a robot, the resulting stability is only local or semi-global, so the gains need care. See [PID controller](/pid-controller/).
- **Adaptive gravity compensation.** Since $g(q)$ is linear in a few parameters (see [linearity in dynamic parameters](/linearity-in-dynamic-parameters/)), the parameters can be estimated online, which gives an adaptive set-point law.
- **Tracking.** For a moving set point, add feedforward or move to [computed-torque control](/computed-torque-control/) or the [Slotine-Li controller](/slotine-li-adaptive-control/), which keep the energy-based proof.
- **Energy shaping.** Line L2 shapes the potential energy of the arm into the spring energy and injects damping. [IDA-PBC](/ida-pbc/) generalizes this idea to other mechanical systems.

## When to use it

Use it for point-to-point motions and holding a pose, when the gravity model is good but the inertial model is poor or costly to compute. It is the default joint-level law of many torque-controlled arms, and the base of compliant behavior in contact. For fast trajectory tracking use a law with a full model, such as computed-torque control.

## Pitfalls

- **Conditions of the result.** The global stability needs an exact gravity model, a rigid arm (no joint flexibility), and symmetric positive definite gains. A gravity error leaves a rest error with $K_p e = g(q) - \hat g(q)$.
- **Friction.** Static joint friction stops the arm before the set point. The rest error is then the friction torque divided by the spring gain.
- **Damping from noisy speeds.** The damping term needs $\dot q$, which is often a numerical derivative of the joint angles. Filtering adds phase lag and can destabilize a high-gain loop.
- **Not for tracking.** With a moving goal, the law has no feedforward term, and the tracking error does not go to zero.
- **Slow modes.** The decay rate depends on the inertia seen at each joint. The same gains give a fast decay at the wrist and a slow one at the shoulder.

## Implementations

## History

Takegaki and Arimoto published the result in 1981, in the Journal of Dynamic Systems, Measurement, and Control. They chose a Lyapunov function made of the kinetic energy of the arm and an artificial potential energy, and showed that a manipulator under PD feedback with gravity compensation reaches the set point. This energy view became the start of passivity-based robot control. The textbooks of Spong, Hutchinson and Vidyasagar and of Siciliano et al. present the result with LaSalle's invariance principle.

## References
