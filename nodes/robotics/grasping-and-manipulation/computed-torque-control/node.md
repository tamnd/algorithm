---
tag: YZJ7AN
kind: algorithm
slug: computed-torque-control
name: Computed-torque control
aliases:
- inverse dynamics control
area: robotics/grasping-and-manipulation
level: core
summary: "Cancels the arm dynamics with an inverse dynamics model and adds PD feedback, so that with an exact model the joint error obeys a linear, decoupled equation."
model: real-ram
complexity:
  vars: {n: "the number of joints of a serial chain; the bounds are for one control step"}
  time: {per_step: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, online: true, exact: false}
history:
  year: 1980
  people: [J. Y. S. Luh, Michael W. Walker, Richard P. Paul]
  note: Luh, Walker and Paul computed the model torques online with the recursive Newton-Euler algorithm and gave the task-space form, resolved-acceleration control.
prereqs: [manipulator-equation, inverse-dynamics, feedback-linearization]
see_also: [pd-control-with-gravity-compensation, slotine-li-adaptive-control, recursive-newton-euler-algorithm, passivity-based-control, operational-space-formulation, sliding-mode-control, impedance-control, pid-controller]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: "Chapter 11, Section 11.4.2 (motion control of a multi-joint robot: computed torque control) and Section 11.2.2 (second-order linear error dynamics)"
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, second edition, Wiley, 2020
    locator: Chapter 9 (nonlinear and multivariable control, inverse dynamics control)
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Chapter 8 (motion control, centralized control, inverse dynamics control)
  - paper: doi:10.1109/TAC.1980.1102367
    title: J. Y. S. Luh, M. W. Walker and R. P. C. Paul, Resolved-acceleration control of mechanical manipulators, IEEE Transactions on Automatic Control 25(3), 1980
    locator: pages 468 to 474
  - paper: "J. Y. S. Luh, M. W. Walker and R. P. C. Paul, On-line computational scheme for mechanical manipulators, Journal of Dynamic Systems, Measurement, and Control 102(2), 69-76, 1980"
    locator: the whole paper (the recursive Newton-Euler computation of the joint torques)
---

Computed-torque control is a feedback law for a robot arm that uses a model of the arm's dynamics to cancel its nonlinear inertia, Coriolis and gravity terms, and then adds a PD feedback on the joint error. If the model is exact, the joint error of every joint obeys the same linear, decoupled second-order equation, so the designer picks its decay rate directly. It is the robot case of [feedback linearization](/feedback-linearization/), and it needs the [inverse dynamics](/inverse-dynamics/) of the arm at each control step. It differs from [PD control with gravity compensation](/pd-control-with-gravity-compensation/), which cancels only gravity, and from [passivity-based control](/passivity-based-control/), which keeps the inertia of the arm instead of cancelling it.

## In plain words

A robot arm is hard to steer because its joints push on each other. When the elbow moves, the shoulder feels a reaction, and gravity pulls with a force that changes with the pose. A simple spring-like feedback on each joint fights these effects without knowing them, so the arm lags behind the path.

Computed-torque control asks the model of the arm one question at each step: which joint torques give the arm the acceleration that I want now? It then sends those torques. The wanted acceleration is the acceleration of the path plus a correction that pulls the arm back toward the path. If the model is right, the arm behaves like a set of independent, simple systems, one for each joint, and the error dies away at a rate that the designer chooses.

## The problem

The arm has $n$ joints with positions $q \in \mathbb{R}^n$. It obeys the [manipulator equation](/manipulator-equation/)

$$M(q)\ddot q + C(q, \dot q)\dot q + g(q) = \tau,$$

where $M(q)$ is the symmetric positive definite [joint-space inertia matrix](/joint-space-inertia-matrix/), $C(q, \dot q)\dot q$ holds the Coriolis and centripetal torques, $g(q)$ is the gravity torque, and $\tau$ is the vector of joint torques (in N m for revolute joints, N for prismatic joints). There is no contact, so the term $J^T F_{\text{ext}}$ is zero. A desired trajectory $q_d(t)$ is given, twice differentiable, with $\dot q_d$ and $\ddot q_d$ known. The task is to choose $\tau$ from the measured $q$ and $\dot q$ so that the error $e = q_d - q$ goes to zero.

## The algorithm

The controller has a model $\hat M$, $\hat C$, $\hat g$ of the arm, and gain matrices $K_p$ and $K_d$, both symmetric positive definite. In practice they are diagonal.

```pseudo id=main
COMPUTED-TORQUE(q, q', q_d, q_d', q_d'', K_p, K_d)
L1  e ← q_d - q
L2  e' ← q_d' - q'
L3  a ← q_d'' + K_d e' + K_p e          ▷ the wanted joint acceleration
L4  τ ← M̂(q) a + Ĉ(q, q') q' + ĝ(q)     ▷ inverse dynamics of the model
L5  return τ
```

Line L4 is the inverse dynamics of the model at the state $(q, \dot q)$ with the acceleration $a$. A program does not need to form $\hat M$: one call of the [recursive Newton-Euler algorithm](/recursive-newton-euler-algorithm/) with the input $(q, \dot q, a)$ returns the same torque. With the model equal to the arm, the closed loop is $M(q)\ddot q = M(q) a$, so $\ddot q = a$, and line L3 gives

$$\ddot e + K_d \dot e + K_p e = 0.$$

With diagonal gains $K_p = \operatorname{diag}(\omega_i^2)$ and $K_d = \operatorname{diag}(2 \zeta_i \omega_i)$, joint $i$ is a second-order system with natural frequency $\omega_i$ in rad/s and damping ratio $\zeta_i$. The choice $\zeta_i = 1$ (critical damping) gives the fastest decay without overshoot for a given $\omega_i$.

## Example

Take the planar 2R arm with $L_1 = L_2 = 1$ m and point masses of 1 kg at the link ends, in a vertical plane, with $q_1$ measured from the horizontal and $g = 9.81$ m/s$^2$. Its inertia matrix is

$$M(q) = \begin{bmatrix} 3 + 2\cos q_2 & 1 + \cos q_2 \\ 1 + \cos q_2 & 1 \end{bmatrix},$$

and its gravity torque is $g(q) = (2 g \cos q_1 + g \cos(q_1 + q_2),\ g \cos(q_1 + q_2))$ in N m.

The arm is at rest at $q = (0, \pi/2)$, and the set point is $q_d = (0.1, \pi/2)$ rad with $\dot q_d = \ddot q_d = 0$. The gains are $K_p = 25 I$ and $K_d = 10 I$, so $\omega = 5$ rad/s and $\zeta = 1$.

| step | value |
|---|---|
| L1, L2 | $e = (0.1, 0)$, $\dot e = (0, 0)$ |
| L3 | $a = (2.5, 0)$ rad/s$^2$ |
| L4, inertia | $M(q) = [[3, 1], [1, 1]]$, so $M a = (7.5, 2.5)$ |
| L4, gravity | $g(q) = (19.62, 0)$, and $C \dot q = 0$ at rest |
| L5 | $\tau = (27.12, 2.5)$ N m |

The second joint needs a torque of 2.5 N m although its own error is zero: it must hold back the reaction of the first joint. With an exact model, the error of joint 1 is $e_1(t) = 0.1 (1 + 5 t) e^{-5 t}$ rad. This is 0.0736 at $t = 0.2$ s, 0.0287 at $t = 0.5$ s and 0.0040 at $t = 1$ s, and the error of joint 2 stays zero.

Now let the second mass be 1.5 kg, while the model keeps 1 kg, and let the set point be $q_d = (0.3, 0.4)$ with $K_p = 100 I$ and $K_d = 20 I$. A simulation with RK4 and a step of 2 ms comes to rest at $q = (0.29004, 0.38078)$. The steady error $(0.00996, 0.01922)$ rad is the solution of $K_p e = \hat M(q)^{-1}(g(q) - \hat g(q))$, which follows from the closed loop at rest.

## Correctness

The claim is: if $\hat M = M$, $\hat C \dot q = C \dot q$ and $\hat g = g$, and $K_p$, $K_d$ are symmetric positive definite, then $e = 0$, $\dot e = 0$ is a globally [exponentially stable](/exponential-stability/) equilibrium of the error dynamics. The proof substitutes line L4 into the manipulator equation, uses that $M(q)$ is invertible to get $\ddot q = a$, and then shows that the linear system $\ddot e + K_d \dot e + K_p e = 0$ has a Hurwitz state matrix. The full proof, and the formula for the steady error under a constant model error, are in the proof file.

## Complexity

In the [real-RAM](/real-ram/) model, with $n$ joints of a serial chain:

- Lines L1 to L3 take $O(n)$ operations with diagonal gains, and $O(n^2)$ with full gain matrices.
- Line L4 is one inverse dynamics call. The recursive Newton-Euler algorithm does it in $O(n)$ operations for a serial chain or a tree, without forming $M$.
- If a program forms $M(q)$ by the composite rigid body algorithm and multiplies it by $a$, the step costs $O(n^2)$ instead. No linear system is solved, because the law needs $M a$, not $M^{-1}$.

The extra memory is $O(n)$. The law runs once per control period, so the $O(n)$ bound is what makes it practical for arms with many joints.

## Properties

- **Decoupled linear error dynamics.** With an exact model, each joint error is a separate linear second-order system, independent of the pose and of the speed.
- **Model based.** The quality depends on the model. A constant error in the gravity model gives a constant offset; an error in the inertia model gives errors that grow with the acceleration of the trajectory.
- **Not robust by design.** The law has no term that rejects a constant disturbance. An integral term or a robust or adaptive outer law is needed for that.
- **Nominal stability is exponential.** This is stronger than the asymptotic stability of PD control with gravity compensation, but it holds only for the exact model.

## Variants and improvements

- **Task-space form.** Replace the joint error by the end-effector error and set $a = J^{-1}(\ddot x_d + K_d \dot{\tilde x} + K_p \tilde x - \dot J \dot q)$ for a square, nonsingular Jacobian. This is resolved-acceleration control (Luh, Walker and Paul 1980). The [operational space formulation](/operational-space-formulation/) is the version for redundant arms.
- **Integral action.** Lynch and Park add $K_i \int e\, dt$ to line L3, which removes the offset from a constant model error when the gains make the third-order error dynamics stable.
- **Feedforward with PD.** Compute $\hat M(q_d)\ddot q_d + \hat C(q_d, \dot q_d)\dot q_d + \hat g(q_d)$ on the desired trajectory, offline if needed, and add a PD term on the error. This needs less computation online, and its stability holds only locally or with large enough gains.
- **Robust and adaptive versions.** A [sliding mode](/sliding-mode-control/) term handles bounded model errors. The [Slotine-Li adaptive controller](/slotine-li-adaptive-control/) estimates the dynamic parameters online and has a proof that does not need the inverse of the estimated inertia.

## When to use it

Use it when a good dynamic model is known and the arm must follow fast trajectories with small error, for example on a direct drive arm or an arm with a calibrated model after [dynamic parameter identification](/dynamic-parameter-identification/). For slow motions, or set points only, [PD control with gravity compensation](/pd-control-with-gravity-compensation/) is simpler and needs only the gravity model. If the payload is unknown, use an adaptive law. For an arm that touches its environment, the motion goal alone is not enough; see [impedance control](/impedance-control/).

## Pitfalls

- **Joint friction and motor dynamics.** The manipulator equation above has no friction, no gear backlash and no motor dynamics. On a geared arm these effects are often larger than the rigid body terms, and they are not cancelled.
- **High gains and flexibility.** The linear error equation tempts the designer to choose a large $\omega$. Joint flexibility, sensor noise and the sampling period limit the gains on a real arm; the limit is found by tests, not derived.
- **A wrong $C$ term.** Only the product $C(q, \dot q)\dot q$ matters here, so any valid factorization works. Do not mix this with the Slotine-Li law, which needs $C$ from the Christoffel symbols.
- **Torque limits.** The law assumes that each computed torque can be applied. When a torque saturates, the cancellation fails and the error dynamics are no longer linear.
- **Singular task-space form.** The task-space variant needs $J^{-1}$, which does not exist at a [kinematic singularity](/kinematic-singularity/).

## Implementations

## History

Model-based torque computation for arms was studied in the 1970s. Luh, Walker and Paul published in 1980 the recursive Newton-Euler scheme that computes the torques online, and the resolved-acceleration control law, which is computed-torque control in task coordinates. The textbooks of Spong, Hutchinson and Vidyasagar, Siciliano et al. and Lynch and Park present the law as inverse dynamics control or computed torque control, as the robot case of feedback linearization.

## References
