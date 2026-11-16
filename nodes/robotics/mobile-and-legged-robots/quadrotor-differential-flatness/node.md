---
tag: DJV70J
kind: theorem
slug: quadrotor-differential-flatness
name: Differential flatness of the quadrotor
aliases:
- quadrotor flat outputs
area: robotics/mobile-and-legged-robots
level: advanced
summary: "The full state and inputs of a quadrotor follow from position, yaw and their derivatives, so trajectories can be planned in those four outputs."
prereqs: [quadrotor-dynamics, differential-flatness]
see_also: [minimum-snap-trajectory, geometric-tracking-control-se3, feedback-linearization, trajectory-generation-problem, euler-angles, angular-velocity, special-orthogonal-group, unicycle-model]
sources:
  - paper: doi:10.1109/ICRA.2011.5980409
    title: "Daniel Mellinger and Vijay Kumar, Minimum snap trajectory generation and control for quadrotors"
    locator: "Proceedings of the 2011 IEEE International Conference on Robotics and Automation, the section on differential flatness (the flat outputs position and yaw, the body axes from the acceleration and the yaw, and the body rates from the jerk)"
  - paper: doi:10.1109/MRA.2012.2206474
    title: "Robert Mahony, Vijay Kumar and Peter Corke, Multirotor aerial vehicles, modeling, estimation, and control of quadrotor"
    locator: "IEEE Robotics and Automation Magazine 19(3), pp. 20-32 (the model, and trajectory planning with the flat outputs)"
---

## Statement

Take the [quadrotor model](/quadrotor-dynamics/) with the world $z$ axis up, $e_3 = (0, 0, 1)$ and $g = 9.81$ m/s²:

$$\dot x = v, \qquad m\dot v = f R e_3 - m g e_3, \qquad \dot R = R\hat\Omega, \qquad J\dot\Omega = M - \Omega \times J\Omega,$$

with mass $m > 0$, inertia $J$ positive definite, thrust $f$ and body moment $M$. Write $b_1, b_2, b_3$ for the columns of $R$. For an angle $\psi$, let $x_c = (\cos\psi, \sin\psi, 0)$ and $y_c = (-\sin\psi, \cos\psi, 0)$. Say that $\psi$ is the **yaw** of $R$ when $b_2 \cdot x_c = 0$ and $b_1 \cdot x_c > 0$. This is the yaw angle of the Z-X-Y [Euler angles](/euler-angles/), the convention of Mellinger and Kumar.

**Theorem.** Let $x : I \to \mathbb{R}^3$ be of class $C^4$ and $\psi : I \to \mathbb{R}$ of class $C^2$ on an interval $I$. Write $a = \ddot x$, $j = \dddot x$ and $s = x^{(4)}$, and let $t = a + g e_3$. Assume that for all times in $I$:

- **(C1) nonzero thrust:** $t \ne 0$, that is, $\ddot x \ne -g e_3$;
- **(C2) a defined heading:** $t$ is not parallel to $x_c(\psi)$.

Then there is exactly one solution $(x, v, R, \Omega, f, M)$ of the model on $I$ with $f > 0$ whose position is $x$ and whose yaw is $\psi$. It is given by:

$$f = m|t|, \qquad b_3 = \frac{t}{|t|}, \qquad b_2 = \frac{b_3 \times x_c}{|b_3 \times x_c|}, \qquad b_1 = b_2 \times b_3, \qquad v = \dot x,$$

$$\dot f = m\, b_3 \cdot j, \qquad \Omega_1 = -\frac{m}{f}\, b_2 \cdot j, \qquad \Omega_2 = \frac{m}{f}\, b_1 \cdot j, \qquad \Omega_3 = \frac{\Omega_1\, b_3 \cdot x_c + \dot\psi\, b_2 \cdot y_c}{b_1 \cdot x_c},$$

$$\dot\Omega_1 = \frac{-m\, b_2 \cdot s - 2\dot f\,\Omega_1 + f\,\Omega_2\Omega_3}{f}, \qquad \dot\Omega_2 = \frac{m\, b_1 \cdot s - 2\dot f\,\Omega_2 - f\,\Omega_1\Omega_3}{f},$$

$$\dot\Omega_3 = \frac{\Omega_1\Omega_2\, b_1 \cdot x_c + (\Omega_2\Omega_3 + \dot\Omega_1)\, b_3 \cdot x_c + 2\dot\psi\,(\Omega_1\, b_3 \cdot y_c - \Omega_3\, b_1 \cdot y_c) + \ddot\psi\, b_2 \cdot y_c}{b_1 \cdot x_c},$$

$$M = J\dot\Omega + \Omega \times J\Omega.$$

So the position and the yaw are **flat outputs** of the quadrotor in the sense of [differential flatness](/differential-flatness/): they are functions of the state, and the state and the inputs are functions of them and of finitely many of their derivatives, up to the fourth derivative of $x$ and the second of $\psi$. The four rotor thrusts follow from $(f, M)$ by the invertible mixer on the [quadrotor dynamics](/quadrotor-dynamics/) page.

## In plain words

A quadrotor has twelve numbers in its state and four controls, so it seems hard to plan its motion. But if you draw any smooth path through space and say which way the nose should point along the way, everything else is fixed. The push must point along the acceleration plus gravity, so the tilt follows from the path. The nose direction then fixes the full orientation. How fast the tilt changes follows from how fast the acceleration changes. And the turning effort follows from that. So a planner needs to draw only four smooth curves: three for the position and one for the heading.

This works only while the motors push. In free fall the push is zero and the tilt can be anything, so the path does not fix it.

## Proof

*Existence.* Define $f$, $R$ and $\Omega$ by the formulas. By (C1), $|t| > 0$, so $f > 0$ and $b_3$ is a unit vector. By (C2), $b_3 \times x_c \ne 0$, so $b_2$ is a unit vector orthogonal to $b_3$ and to $x_c$, and $b_1 = b_2 \times b_3$ completes a right-handed orthonormal frame. So $R = [b_1\ b_2\ b_3] \in SO(3)$, and it is $C^2$ in $t$ since $t$ is $C^2$ and $\psi$ is $C^2$. Since $b_1$ is parallel to $x_c - (x_c \cdot b_3)b_3$, $b_1 \cdot x_c = |b_3 \times x_c| > 0$, so $\psi$ is the yaw of $R$.

Translation: $f R e_3 = f b_3 = m t = m\ddot x + m g e_3$, which is the second equation with $v = \dot x$.

Rotation: let $\Omega$ be the body angular velocity of $R(t)$, that is $\hat\Omega = R^T\dot R$, so the third equation holds by definition. It remains to show that $\Omega$ has the stated components. Since $\dot R = R\hat\Omega$, the columns satisfy

$$\dot b_1 = \Omega_3 b_2 - \Omega_2 b_3, \qquad \dot b_2 = -\Omega_3 b_1 + \Omega_1 b_3, \qquad \dot b_3 = \Omega_2 b_1 - \Omega_1 b_2.$$

Differentiate $m t = f b_3$: $m j = \dot f b_3 + f(\Omega_2 b_1 - \Omega_1 b_2)$. Taking the dot product with $b_3$, $b_1$ and $b_2$ gives $\dot f$, $\Omega_2$ and $\Omega_1$. Differentiate the yaw condition $b_2 \cdot x_c = 0$, with $\dot x_c = \dot\psi y_c$: $(-\Omega_3 b_1 + \Omega_1 b_3) \cdot x_c + \dot\psi\, b_2 \cdot y_c = 0$, which gives $\Omega_3$, since $b_1 \cdot x_c > 0$.

Differentiate once more for $\dot\Omega$ (here $x$ is $C^4$ and $\psi$ is $C^2$). From $m s = \ddot f b_3 + 2\dot f\dot b_3 + f(\dot\Omega_2 b_1 - \dot\Omega_1 b_2) + f(\Omega_2\dot b_1 - \Omega_1\dot b_2)$, and $\Omega_2\dot b_1 - \Omega_1\dot b_2 = \Omega_1\Omega_3 b_1 + \Omega_2\Omega_3 b_2 - (\Omega_1^2 + \Omega_2^2) b_3$, the dot products with $b_1$ and $b_2$ give $\dot\Omega_2$ and $\dot\Omega_1$. The second derivative of the yaw condition, $\ddot b_2 \cdot x_c + 2\dot\psi\, \dot b_2 \cdot y_c + b_2 \cdot (\ddot\psi y_c - \dot\psi^2 x_c) = 0$, with $\ddot b_2 = -\dot\Omega_3 b_1 + \dot\Omega_1 b_3 - \Omega_3\dot b_1 + \Omega_1\dot b_3$ and $b_2 \cdot x_c = 0$, gives $\dot\Omega_3$. Finally, defining $M$ by the last formula makes the fourth equation hold.

*Uniqueness.* Let $(x, v, R, \Omega, f, M)$ be any solution with $f > 0$, position $x$ and yaw $\psi$. The translation equation forces $f b_3 = m t$, and with $f > 0$ and $|b_3| = 1$ this forces $f = m|t|$ and $b_3 = t/|t|$; in particular (C1) is necessary. The yaw condition says that $b_2$ is a unit vector orthogonal to $b_3$ and to $x_c$, so $b_2 = \pm(b_3 \times x_c)/|b_3 \times x_c|$, and $b_1 \cdot x_c > 0$ picks the plus sign. Then $R$ is fixed, $\Omega$ is fixed by $\hat\Omega = R^T\dot R$, and $M$ by the fourth equation. $\square$

*Check.* A scratch script evaluated these formulas on a generic trajectory ($x(t)$ a sum of sines and a quadratic, $\psi(t)$ a sine) at five times, and compared them with central differences of $R$, $\Omega$ and $f$ and with the translation equation. The largest difference was $5 \times 10^{-10}$ (measurement).

## Consequences

- **Planning in the flat outputs.** Any $C^4$ position path and $C^2$ yaw path that keep (C1) and (C2) can be flown in the model. [Minimum snap trajectories](/minimum-snap-trajectory/) are polynomials in these outputs, chosen so that the snap, and so the moment through $\dot\Omega$, is small.
- **Feedforward for tracking.** The formulas give $R_d$, $\Omega_d$ and $\dot\Omega_d$ along the plan. The [geometric tracking controller on SE(3)](/geometric-tracking-control-se3/) uses them as its reference and adds feedback for the errors.
- **Feasibility checks.** The thrust is $m|\ddot x + g e_3|$, and the body rates are bounded by $|\Omega_1|, |\Omega_2| \le m|j|/f$. So limits on the thrust and on the rates become limits on the acceleration and the jerk of the plan, which a planner can check before it flies.
- **Examples by hand.** With a constant acceleration $\ddot x = (g, 0, 0)$ and $\psi = 0$: $f = \sqrt 2\, m g$, $b_3 = (1, 0, 1)/\sqrt 2$ and $b_1 = (1, 0, -1)/\sqrt 2$, a pitch of $45°$, with $\Omega = 0$. On the circle $x = (\cos 2t, \sin 2t, 0)$ m with $\psi = 0$ and $m = 0.5$ kg, at $t = 0$: $f = 5.2971$ N, $b_3 = (-0.37757, 0, 0.92598)$ and $\Omega = (0.75513, 0, -0.30790)$ rad/s. The body yaw rate is not zero even though $\psi$ is constant, because $b_3$ is tilted.

## Tightness

- **(C1) cannot be dropped.** If $\ddot x = -g e_3$ on an interval, as on a ballistic arc, then $f = 0$, and every attitude and every moment give the same position, so the state is not a function of the outputs. At an isolated time where $t = 0$, $b_3 = t/|t|$ can jump, which needs an infinite angular velocity: a path that goes through free fall and then pushes in another direction cannot be flown smoothly in general.
- **(C2) is a chart singularity.** When $b_3$ is parallel to $x_c$, the nose direction $x_c$ cannot be projected onto the rotor plane, and the yaw is not defined. Another yaw chart, such as Z-Y-X angles with the condition $b_1 \cdot y_c = 0$, is singular at a different place ($b_3$ parallel to $y_c$), so switching charts covers both cases, at the cost of a jump in the yaw signal.
- **Smoothness.** If $x$ is only $C^3$, the moment $M$ is not defined at the points where the snap jumps. Piecewise polynomial plans must keep the position $C^4$ at the joints, or accept a jump in the moment.
- **Input limits are not part of the theorem.** The formulas give the inputs a path needs, not whether the rotors can give them. Each rotor needs $0 \le f_i \le f_{\max}$, which must be checked after the mixer.
- **Model limits.** The theorem is about the rigid body model. With rotor drag that grows with the speed, the position and the yaw are still flat outputs under extra conditions, but the formulas change.

## History

Fliess, Lévine, Martin and Rouchon introduced differentially flat systems in the 1990s; see [differential flatness](/differential-flatness/). Mellinger and Kumar used the position and the yaw as flat outputs of a quadrotor in 2011, built minimum snap polynomial trajectories in these outputs, and flew them with a nonlinear controller on SO(3). Since then, flatness has been the standard way to plan quadrotor trajectories. Later work extended it to rotor drag and to quadrotors that carry a load on a cable.

## References
