---
tag: VFWRCA
kind: model
slug: quadrotor-dynamics
name: Quadrotor dynamics
aliases:
- quadcopter model
area: robotics/mobile-and-legged-robots
level: core
summary: A rigid body in SE(3) driven by four rotor thrusts that give a total thrust along the body axis and three moments.
prereqs: [newton-euler-equations, special-orthogonal-group]
see_also: [geometric-tracking-control-se3, quadrotor-differential-flatness, minimum-snap-trajectory, angular-velocity, euler-angles, unit-quaternion-rotation, lqr-problem, special-euclidean-group]
sources:
  - paper: doi:10.1109/MRA.2012.2206474
    title: "Robert Mahony, Vijay Kumar and Peter Corke, Multirotor aerial vehicles, modeling, estimation, and control of quadrotor"
    locator: "IEEE Robotics and Automation Magazine 19(3), pp. 20-32 (the rigid body model, the rotor thrust and drag moment, the map from rotor forces to thrust and moments, and the aerodynamic effects that the basic model leaves out)"
  - paper: doi:10.1109/ICRA.2011.5980409
    title: "Daniel Mellinger and Vijay Kumar, Minimum snap trajectory generation and control for quadrotors"
    locator: "Proceedings of the 2011 IEEE International Conference on Robotics and Automation, the model section (a z-up world frame, thrust along the body z axis, and the rotor forces and moments)"
  - paper: doi:10.1109/CDC.2010.5717652
    title: "Taeyoung Lee, Melvin Leok and N. Harris McClamroch, Geometric tracking control of a quadrotor UAV on SE(3)"
    locator: "Proceedings of the 49th IEEE Conference on Decision and Control, the dynamic model (with the z axis down, which this page converts to z up)"
---

A quadrotor is an aerial robot with four rotors in a plane, each of which pushes along the same body axis. The standard model treats it as one rigid body that moves in space, in the group [SE(3)](/special-euclidean-group/) of positions and orientations, with the four rotor thrusts as the inputs. The rotors give a total thrust along the body $z$ axis and three moments about the body axes. So the vehicle has six degrees of freedom and only four inputs: it cannot push sideways, and it must tilt to accelerate in a horizontal direction. Opposite rotors spin the same way and neighbor rotors spin the other way, so that their drag moments cancel at hover, and a difference in their speeds turns the vehicle about its vertical axis. This page uses a world frame with the $z$ axis up and $g = 9.81$ m/s². Some sources, such as Lee, Leok and McClamroch, use $z$ down; the equations here are converted.

## The machine

**State.** The position $x \in \mathbb{R}^3$ of the center of mass in the world frame (m), its velocity $v$ (m/s), the attitude $R \in$ [SO(3)](/special-orthogonal-group/), whose columns are the body axes $b_1, b_2, b_3$ in world coordinates, and the body [angular velocity](/angular-velocity/) $\Omega$ (rad/s). The state space has dimension 12.

**Inputs.** The thrusts $f_1, \dots, f_4 \ge 0$ of the four rotors (N). Each rotor at speed $\omega_i$ gives the thrust $f_i = k_F \omega_i^2$ along $b_3$, and a drag moment $k_M \omega_i^2$ about $b_3$ against its direction of spin. Write $c = k_M / k_F$ (m).

**Parameters.** The mass $m$ (kg), the inertia matrix $J$ about the center of mass in body coordinates (kg m²), the arm length $l$ from the center to each rotor (m), and $c$.

**Equations.** With $e_3 = (0, 0, 1)$, these are the [Newton-Euler equations](/newton-euler-equations/) for the body:

$$\dot x = v, \qquad m \dot v = f R e_3 - m g e_3, \qquad \dot R = R \hat\Omega, \qquad J \dot\Omega = M - \Omega \times J \Omega.$$

Here $\hat\Omega$ is the skew-symmetric matrix of $\Omega$, $f$ is the total thrust and $M$ is the moment in body coordinates.

**The mixer.** In the "+" layout, rotor 1 is on the $+b_1$ arm, rotor 2 on $+b_2$, rotor 3 on $-b_1$ and rotor 4 on $-b_2$. Rotors 1 and 3 spin clockwise seen from above, and rotors 2 and 4 counterclockwise. Then

$$\begin{pmatrix} f \\ M_1 \\ M_2 \\ M_3 \end{pmatrix} = \begin{pmatrix} 1 & 1 & 1 & 1 \\ 0 & l & 0 & -l \\ -l & 0 & l & 0 \\ c & -c & c & -c \end{pmatrix} \begin{pmatrix} f_1 \\ f_2 \\ f_3 \\ f_4 \end{pmatrix}.$$

The rows of $M_1$ and $M_2$ are the moments $r_i \times f_i b_3$ of the forces at the rotor positions $r_i$. The last row is the sum of the drag moments. For $l, c > 0$ the matrix is invertible:

$$f_{1,3} = \frac f4 \mp \frac{M_2}{2l} + \frac{M_3}{4c}, \qquad f_{2,4} = \frac f4 \pm \frac{M_1}{2l} - \frac{M_3}{4c}.$$

In the "×" layout, the arms are at $45°$ to $b_1$, and each moment row has all four rotors with factors $\pm l/\sqrt 2$; the matrix is still invertible.

**Standing assumptions.** The body is rigid and symmetric enough that $J$ is constant. The rotor thrust changes at once when the command changes; in reality a motor needs some tens of milliseconds. The thrust is along $b_3$ with no sideways part. The model leaves out rotor drag and blade flapping, which grow with the airspeed, the gyroscopic moments of the rotors, the ground effect near the floor, and wind. Mahony, Kumar and Corke discuss these effects.

## What it counts

The model predicts the motion of the vehicle for given rotor thrusts, and so it gives the thrusts that a wanted motion needs. Three cases can be checked by hand, for $m = 0.5$ kg, $l = 0.17$ m and $c = 0.016$ m.

- **Hover.** With $R = I$ (or any rotation about $e_3$), $v = 0$ and $\Omega = 0$, the state is constant if and only if $f = mg$ and $M = 0$, which gives $f_i = mg/4 = 1.22625$ N for each rotor.
- **Tilt.** To hold the height with $b_3$ tilted by an angle $\theta$ from the vertical, the vertical part of the thrust must be $mg$, so $f = mg/\cos\theta$. For $\theta = 10°$, this is $4.9807$ N, and the horizontal acceleration is $g \tan\theta = 1.7298$ m/s².
- **Yaw.** A yaw moment $M_3 = 0.01$ N m at hover thrust needs $f_1 = f_3 = 1.22625 + 0.15625 = 1.3825$ N and $f_2 = f_4 = 1.07$ N.

**Energy (theorem).** Let $E = \tfrac12 m |v|^2 + \tfrac12 \Omega^T J \Omega + m g x_3$. Along every solution, $\dot E = f\, v^T R e_3 + \Omega^T M$. *Proof.* From the equations, $m v^T \dot v = f v^T R e_3 - m g v_3$, the derivative of $m g x_3$ is $m g v_3$, and $\Omega^T J \dot\Omega = \Omega^T M$ because $\Omega^T(\Omega \times J\Omega) = 0$. $\square$ So with the rotors off, the energy is constant. A simulator that does not keep it constant has an integration error.

## Relation to other models

- **The rigid body.** The model is the free rigid body with a body-fixed force along one axis and a body moment. It is a special case of the [Newton-Euler equations](/newton-euler-equations/) and of floating-base dynamics with no limbs.
- **The planar quadrotor.** Restricting the motion to a vertical plane gives 3 degrees of freedom $(y, z, \phi)$ with 2 inputs, thrust and moment. It shows the same tilt-to-move behavior and is a common teaching model.
- **The point mass with a thrust vector.** If the attitude loop is much faster than the position loop, the vehicle acts as a point mass with a thrust vector $f R e_3$ that the controller can point in any upward direction. Trajectory planners such as [minimum snap](/minimum-snap-trajectory/) use this view, and the [flatness map](/quadrotor-differential-flatness/) makes it exact.
- **Linearization at hover.** With small roll $\phi$, pitch $\theta$ and yaw $\psi$, $R e_3 \approx (\theta, -\phi, 1)$, so $\ddot x_1 = g\theta$, $\ddot x_2 = -g\phi$ and $\ddot x_3 = (f - mg)/m$. This linear model is controllable and is the base of the [LQR](/lqr-problem/) and PID designs.
- **Attitude charts.** [Euler angles](/euler-angles/) have a singular set; [unit quaternions](/unit-quaternion-rotation/) double cover the rotations. The model above uses $R$ itself.
- **Other multirotors.** Hexarotors and octorotors have more rotors; their mixer is a wide matrix, and the choice among its many solutions can handle a failed rotor.

## Known results in the model

- **Underactuation.** Four inputs for six degrees of freedom: the horizontal force comes only from tilting, and the vehicle cannot hold a tilted attitude and a fixed position at once.
- **Differential flatness.** The position and the yaw angle are flat outputs: the whole state and the inputs are functions of them and their derivatives up to the fourth, when the thrust is not zero. See [differential flatness of the quadrotor](/quadrotor-differential-flatness/).
- **Geometric tracking control.** A law on $SO(3)$ follows a position and heading reference, with exponential stability of the attitude error for errors below 90 degrees and almost global convergence of the attitude. See [geometric tracking control on SE(3)](/geometric-tracking-control-se3/).
- **Input limits.** With $0 \le f_i \le f_{\max}$, the reachable $(f, M)$ form a box mapped by the mixer, a parallelepiped. A large yaw moment takes thrust from two rotors, so yaw is the first axis to saturate on most vehicles.
- **Thrust margin.** A common design rule asks for a maximum total thrust of about twice the hover thrust $mg$, to leave room for tilting and for control moments (heuristic).

## References
