---
tag: R3QEN8
kind: algorithm
slug: geometric-tracking-control-se3
name: Geometric tracking control on SE(3)
aliases:
- Lee-Leok-McClamroch controller
area: robotics/mobile-and-legged-robots
level: research
summary: "Quadrotor position and attitude tracking with errors on SO(3); exponentially stable below 90 degrees of attitude error, almost globally attractive below 180."
model: real-ram
complexity:
  vars: {s: "the size of the state, fixed at 18 numbers (position, velocity, rotation matrix, angular velocity); the bounds are for one control step"}
  time: {worst: O(1)}
  space: {extra: O(1)}
properties: {deterministic: true, randomized: false, online: true, exact: false}
history:
  year: 2010
  people: [Taeyoung Lee, Melvin Leok, N. Harris McClamroch]
  note: "Lee, Leok and McClamroch gave the controller and its stability proofs at the IEEE Conference on Decision and Control in 2010; Mellinger and Kumar used the same attitude error in their minimum snap work of 2011."
prereqs: [quadrotor-dynamics, special-orthogonal-group, lyapunov-function]
see_also: [quadrotor-differential-flatness, minimum-snap-trajectory, so3-logarithm-map, feedback-linearization, exponential-stability, unit-quaternion-rotation, pid-controller, model-predictive-control]
sources:
  - paper: doi:10.1109/CDC.2010.5717652
    title: Geometric tracking control of a quadrotor UAV on SE(3)
    locator: "Section II (the model, z down), Section III (the controller, Propositions 1 to 3), Section IV (the numerical example: mass, inertia, gains, Cases I and II) and the Appendix (the proofs); also arXiv:1003.2005"
  - paper: doi:10.1109/ICRA.2011.5980409
    title: Minimum snap trajectory generation and control for quadrotors
    locator: the sections on differential flatness and on the controller (the attitude error on SO(3))
  - paper: doi:10.1109/MRA.2012.2206474
    title: "Multirotor aerial vehicles: modeling, estimation, and control of quadrotor"
    locator: the sections on the dynamic model and on attitude and position control
  - book: isbn:9781107156302
    title: "Modern Robotics: Mechanics, Planning, and Control"
    locator: "Chapter 3 (rotation matrices, the exponential and logarithm on SO(3))"
---

Geometric tracking control on SE(3) is a feedback law that makes a [quadrotor](/quadrotor-dynamics/) follow a desired position $x_d(t)$ and a desired heading. It works with the rotation matrix $R$ directly and does not use Euler angles or quaternions, so it has no singularity of a chart and no double cover. The outer loop computes the force $A$ that the vehicle should produce; the thrust is the part of $A$ along the current body $z$ axis, and the desired attitude $R_d$ turns the body $z$ axis toward $A$. The inner loop drives the attitude error $e_R = \tfrac12(R_d^TR - R^TR_d)^\vee$ to zero with a proportional and derivative term on [SO(3)](/special-orthogonal-group/) plus a feedforward that cancels the gyroscopic term. Lee, Leok and McClamroch proved that the attitude loop is exponentially stable when the attitude error is less than 90 degrees, and that the full error converges exponentially from almost every attitude error less than 180 degrees. These are theorems for the continuous-time law with exact derivatives of $R_d$. The page uses a z-up world frame; the paper uses z down, and the page converts every sign.

## In plain words

A quadrotor can only push along one direction, straight out of its top. To move sideways, it must first tilt. So the controller works in two layers. The outer layer says where the push should point and how hard it should be, from the position error and the speed error. The inner layer turns the body toward that direction, and the motors give the part of the push that the body can give in its current attitude.

The inner layer measures the attitude error on the set of all orientations itself, not in angles. This avoids the bad points that angle sets have. One problem remains: when the vehicle is exactly upside down from the wanted attitude, no single direction of turning is best. The law handles every other start, even one that is almost upside down.

## The problem

**The model.** The vehicle is a rigid body with mass $m$ and body inertia $J$, with the world $z$ axis up and gravity $-ge_3$, $g = 9.81$ m/s². The thrust $f$ acts along the third column of the rotation $R$, and the moment $M$ acts in body coordinates:
$$\dot x = v,\quad m\dot v = fRe_3 - mge_3,\quad \dot R = R\hat\Omega,\quad J\dot\Omega = M - \Omega\times J\Omega.$$
Here $\hat\Omega$ is the [skew-symmetric matrix](/skew-symmetric-matrix-of-a-vector/) of the body [angular velocity](/angular-velocity/) $\Omega$. The four rotor forces map to $(f, M)$ through an invertible matrix, given on the [quadrotor dynamics](/quadrotor-dynamics/) page. Arithmetic, square roots and trigonometric functions cost one step each, as in the [real RAM](/real-ram/).

**Input.** The state $(x, v, R, \Omega)$; the reference $x_d, \dot x_d, \ddot x_d$ and a unit vector $b_{1d}$ that gives the wanted heading; the gains $k_x, k_v, k_R, k_\Omega > 0$; $m$, $J$ and the control period $\Delta t$.

**Output.** The thrust $f$ in newtons and the moment $M$ in newton meters, held for one control period.

**How it differs from close pages.** A cascade of [PID controllers](/pid-controller/) on roll, pitch and yaw angles works near hover and fails near the singularity of the [Euler angles](/euler-angles/). A law on [unit quaternions](/unit-quaternion-rotation/) must choose one of the two quaternions for each attitude, and a careless choice makes the vehicle turn the long way round. [Feedback linearization](/feedback-linearization/) needs local coordinates. [Model predictive control](/model-predictive-control/) handles rotor limits but costs much more per step. The [differential flatness of the quadrotor](/quadrotor-differential-flatness/) gives the feedforward $R_d$, $\Omega_d$ and $\dot\Omega_d$ along a smooth trajectory, and this law is the usual feedback around it.

## The algorithm

```pseudo id=main
GEOMETRIC-CONTROL(x, v, R, Ω; xd, vd, ad, b1d)
L1  ex ← x - xd;  ev ← v - vd
L2  A ← -kx ex - kv ev + m g e3 + m ad
L3  f ← A · (R e3)
L4  b3d ← A / |A|;  b2d ← b3d × b1d / |b3d × b1d|;  Rd ← [b2d × b3d, b2d, b3d]
L5  Ωd, Ω̇d ← the angular velocity and acceleration of Rd, given or from differences of Rd
L6  eR ← (1/2) (Rd^T R - R^T Rd)^∨;  eΩ ← Ω - R^T Rd Ωd
L7  M ← -kR eR - kΩ eΩ + Ω × JΩ - J (Ω̂ R^T Rd Ωd - R^T Rd Ω̇d)
L8  apply (f, M) for one control period; repeat from L1
```

Line L2 is the force that would make the position error obey the stable linear equation $m\ddot e_x = -k_xe_x - k_v\dot e_x$ if the body $z$ axis pointed along $A$. Line L3 takes only the part of $A$ that the body can give now. Line L4 needs $A \ne 0$ and $b_{1d}$ not parallel to $A$; the code raises an error in these cases. The first column of $R_d$ is the projection of $b_{1d}$ onto the plane normal to $b_{3d}$, so the heading is followed as closely as the thrust direction allows. Version 1 of the paper on arXiv writes $R_d$ without the normalization of $b_{2d}$; the normalized form here is a rotation for every valid input. Line L5 in the code uses $\Omega_d = \log(R_{d,k-1}^TR_{d,k})^\vee/\Delta t$ with the [SO(3) logarithm](/so3-logarithm-map/) and a backward difference of $\Omega_d$ for $\dot\Omega_d$, when the caller does not give them. Line L8 integrates the model with the classical [Runge-Kutta method](/runge-kutta-methods/), with $(f, M)$ held, and re-orthonormalizes $R$.

## Example

Take the vehicle of the paper: $m = 4.34$ kg, $J = \operatorname{diag}(0.0820, 0.0845, 0.1377)$ kg m², $k_x = 16m$, $k_v = 5.6m$, $k_R = 8.81$, $k_\Omega = 2.54$. The vehicle hovers level ($R = I$, $v = 0$, $\Omega = 0$) at $x = (1, 0, 0)$ m, and the target is the origin with $b_{1d} = (1, 0, 0)$.

Line L2 gives $A = (-16 \cdot 4.34, 0, 4.34 \cdot 9.81) = (-69.44, 0, 42.575)$ N. Line L3 gives $f = 42.575$ N, which is $mg$: the body $z$ axis is still vertical. Line L4 gives $|A| = 81.453$ N and $b_{3d} = (-0.8525, 0, 0.5227)$, a tilt of 58.5 degrees toward the target; $b_{2d} = (0, 1, 0)$ and $b_{1d}$ becomes $(0.5227, 0, 0.8525)$. Line L6 gives $\Psi = 1 - \cos 58.5° = 0.4773$ and $e_R = (0, 0.8525, 0)$, and line L7 gives $M = (0, -7.511, 0)$ N m, a moment that tips the nose toward $-x$. Measured: in the simulation with $\Delta t = 10$ ms, the position error stays below 1 cm after 1.81 s, and the attitude error never exceeds its first value. The large tilt shows that these gains are aggressive for a 1 m step; a real vehicle limits the tilt and the thrust.

The paper's two simulations, converted to z up:

| Case | Start | Measured with this code ($\Delta t = 10$ ms) | Reported in the paper |
|---|---|---|---|
| I: elliptic helix $x_d = (0.4t, -0.4\sin\pi t, -0.6\cos\pi t)$, $b_{1d} = (\cos\pi t, -\sin\pi t, 0)$ | rest at the origin, level | position error 5.3 mm at steady state; 2.6 mm at 5 ms, 1.1 mm at 2 ms | the error converges |
| II: hover at the origin | rotated 178 degrees about $x$, $\Psi(0) = 1.9994$ | $\Psi < 1$ after 1.29 s, $\Psi < 10^{-3}$ after 2.2 s, position error below 1 cm after 3.45 s, largest excursion 1.0 m | $\Psi < 1$ after 0.88 s |

The steady error of Case I is proportional to $\Delta t$, so it comes from the zero-order hold and from the differences of line L5, not from the law. In Case I the first attitude error is $\Psi(0) = 0.366$ here; the paper reports a value below 0.15, and the time of 0.88 s in Case II also differs. The paper does not give every detail of its setup, so these numbers are not expected to match.

## Correctness

The [proof](proofs/correctness/) has four parts. Lemma 1: with $R_d^TR = \exp(\hat\xi)$ and $\theta = |\xi|$, the error function is $\Psi = 1 - \cos\theta$ and $e_R = (\sin\theta/\theta)\xi$; so $e_R$ is zero both at the target and at every rotation error of 180 degrees. Lemma 2: the moment of line L7 gives the attitude error dynamics $J\dot e_\Omega = -k_Re_R - k_\Omega e_\Omega$. Theorem 1 uses the [Lyapunov function](/lyapunov-function/) $\tfrac12 e_\Omega\cdot Je_\Omega + k_R\Psi$, whose derivative is $-k_\Omega|e_\Omega|^2$, to show that the attitude stays away from the 180 degree set when it starts away from it with a small enough angular velocity. Theorem 2 adds a cross term and gives [exponential stability](/exponential-stability/) of the attitude. Theorem 3 quotes Propositions 2 and 3 of the paper for the full loop: exponential stability when $\Psi(0) < 1$ (less than 90 degrees) and the gains meet the inequalities of the paper, and almost global exponential attractiveness for $1 \le \Psi(0) < 2$. Because of the topology of SO(3), no continuous feedback can stabilize one attitude from every start, so a continuous law cannot remove the 180 degree set.

## Complexity

- **Time per step.** A fixed number of $3 \times 3$ matrix products, cross products, one square root for each normalization and, in line L5, one logarithm on SO(3): $O(1)$. Measured: one call of the command function takes about 150 microseconds in CPython on a laptop.
- **Space.** $O(1)$: the previous $R_d$ and $\Omega_d$ for the differences of line L5.

## Properties

- **Coordinate-free.** The law uses $R$ only through matrix products, so it has no gimbal lock and no sign ambiguity of a quaternion.
- **Thrust along the body axis.** The thrust of line L3 is never more than $|A|$, and it is negative when the body $z$ axis points away from $A$. Most rotors cannot reverse, so a real vehicle clamps it at zero.
- **Gains in physical units.** The position gains scale with the mass in the paper's example; the attitude gains act on $e_R$, which has no unit.
- **Not exact in discrete time.** With a zero-order hold and differences for $\Omega_d$, the measured tracking error is proportional to the control period.
- **Almost global, not global.** At a rotation error of exactly 180 degrees with zero angular velocity, $e_R = 0$ and the attitude loop exerts no moment.

## Variants and improvements

- **Given feedforward.** Along a trajectory from [minimum snap](/minimum-snap-trajectory/) optimization, the [flatness map](/quadrotor-differential-flatness/) gives $\Omega_d$ and $\dot\Omega_d$ exactly from the jerk and the snap, and line L5 needs no differences. Mellinger and Kumar used this combination in 2011.
- **Attitude tracking alone.** Lines L6 and L7 alone, with $R_d$ given by a pilot or a planner, are an attitude controller for any rigid body; Proposition 1 of the paper covers this case.
- **Hybrid control for global results.** A switching law with a second error function removes the 180 degree critical set at the cost of a discontinuity; later papers by Lee and others use this.
- **Integral terms and robust terms.** Later work adds an integral of the errors or a term for a bounded disturbance, to cancel a constant wind or a wrong mass.
- **Rotor limits.** The law does not know the rotor limits. Practical code clamps the tilt in line L4 and the thrust in line L3, which removes the proof.

## When to use it

Use it for a quadrotor or another vehicle with one thrust direction that must make large attitude changes: aggressive flight, recovery from a flip, or tracking of fast trajectories. Near hover with small angles, a cascade of PID loops on Euler angles is simpler and works as well. When the rotor limits or obstacles matter, use model predictive control and keep this law as the inner loop or as a fallback.

## Pitfalls

- **Frame conventions.** The paper uses z down, and the signs of $g$ and $f$ differ from code with z up. A wrong sign in line L2 makes the vehicle push itself into the ground.
- **The singular cases of line L4.** $A = 0$ happens when the commanded acceleration equals $-ge_3$, for example in a commanded free fall. $b_{1d}$ parallel to $A$ happens when the vehicle must point its thrust along the heading direction. Both make $R_d$ undefined; a robust implementation keeps the previous $R_d$ or picks another heading vector.
- **Noisy differences.** The backward differences of line L5 amplify the noise of $R_d$, which itself depends on the measured position and velocity. Filter them, or use the flatness map.
- **Version of the paper.** The bound on the first angular velocity in Proposition 1 of version 1 on arXiv uses the smallest eigenvalue of $J$; the Lyapunov argument needs the largest one. Use the conservative form.
- **Large position errors.** With the gains of the example, a 1 m error gives a tilt of 58 degrees and a large thrust. Saturate the position error or plan a feasible trajectory first.

## Implementations

## History

Attitude control on SO(3) without coordinates goes back to the study of rigid spacecraft. Bhat and Bernstein showed in 2000 that no continuous feedback stabilizes one attitude globally on SO(3), because of its topology. Lee, Leok and McClamroch combined an attitude law on SO(3) with a position loop for a quadrotor and proved the stability results in their paper at the IEEE Conference on Decision and Control in 2010. Mellinger and Kumar used the same attitude error with flat trajectories in 2011, and their demonstrations of aggressive flight made the law common in research code for multirotors.

## References
